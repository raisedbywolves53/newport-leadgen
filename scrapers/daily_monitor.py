"""Daily SAM.gov opportunity monitor with change detection and notifications.

Wraps the existing report_opportunity_pipeline() with:
  1. State persistence — tracks seen notice_ids across runs
  2. Change detection — identifies new opportunities since last run
  3. Optional scoring via bid_scorer
  4. Slack + email notifications for new finds
  5. Optional push to GovCon Pipeline Tracker sheet

Usage:
    python scrapers/daily_monitor.py
    python scrapers/daily_monitor.py --dry-run
    python scrapers/daily_monitor.py --score --no-notify
    python scrapers/daily_monitor.py --score --push-to-sheet --dry-run
    python scrapers/daily_monitor.py --max-pages 3
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from dotenv import load_dotenv

load_dotenv()

from scrapers.contract_scanner import (
    load_config,
    report_opportunity_pipeline,
    save_results,
)

log = logging.getLogger(__name__)

STATE_FILE = _project_root / "data" / "cache" / "last_opportunities.json"


# ── State persistence ────────────────────────────────────────────────────

def load_previous_state() -> set[str]:
    """Load set of previously-seen notice_ids from state file."""
    if not STATE_FILE.exists():
        log.info("No previous state file found — all opportunities will be 'new'")
        return set()
    try:
        data = json.loads(STATE_FILE.read_text())
        ids = set(data.get("notice_ids", []))
        last_run = data.get("last_run", "unknown")
        log.info(f"Loaded {len(ids)} previous notice_ids (last run: {last_run})")
        return ids
    except (json.JSONDecodeError, KeyError) as e:
        log.warning(f"Corrupt state file, starting fresh: {e}")
        return set()


def save_current_state(notice_ids: set[str]) -> None:
    """Save current notice_ids to state file."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "last_run": datetime.now().isoformat(),
        "count": len(notice_ids),
        "notice_ids": sorted(notice_ids),
    }
    STATE_FILE.write_text(json.dumps(data, indent=2))
    log.info(f"Saved {len(notice_ids)} notice_ids to state file")


# ── Main monitor logic ───────────────────────────────────────────────────

def run_monitor(
    max_pages: int = 3,
    do_score: bool = False,
    do_notify: bool = True,
    push_to_sheet: bool = False,
    dry_run: bool = False,
) -> dict:
    """Run the daily monitoring cycle.

    Returns summary dict with counts and lists.
    """
    config = load_config()

    print(f"\n{'='*70}")
    print(f"DAILY SAM.GOV MONITOR — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}")

    # 1. Load previous state
    previous_ids = load_previous_state()

    # 2. Fetch current opportunities
    print(f"\nFetching opportunities (max_pages={max_pages})...")
    try:
        df = report_opportunity_pipeline(config, max_pages=max_pages)
    except ValueError as e:
        print(f"\nERROR: {e}")
        print("Set SAM_API_KEY in .env to enable the daily monitor.")
        return {"error": str(e)}

    if df.empty:
        print("No opportunities found.")
        save_current_state(set())
        return {"total": 0, "new": 0, "removed": len(previous_ids)}

    # 3. Detect changes
    current_ids = set(df["notice_id"].dropna().unique())
    new_ids = current_ids - previous_ids
    removed_ids = previous_ids - current_ids

    new_opps_df = df[df["notice_id"].isin(new_ids)].copy()
    new_opps = new_opps_df.to_dict("records")

    print(f"\n  Total opportunities: {len(current_ids)}")
    print(f"  New since last run:  {len(new_ids)}")
    print(f"  Removed/expired:     {len(removed_ids)}")

    # 4. Score new opportunities
    if do_score and new_opps:
        print(f"\nScoring {len(new_opps)} new opportunities...")
        from scoring.bid_scorer import score_opportunities_batch
        scored = score_opportunities_batch(new_opps, config=config)
        # Sort by score descending
        scored.sort(key=lambda x: x.get("bid_score", 0), reverse=True)
        # Remove internal field
        for item in scored:
            item.pop("_score_result", None)
        new_opps = scored

        # Print top scored
        print(f"\n  Top scored new opportunities:")
        for opp in new_opps[:5]:
            title = (opp.get("title") or "?")[:50]
            score = opp.get("bid_score", "N/A")
            decision = opp.get("bid_decision", "")
            print(f"    {score:>5} ({decision:10s}) {title}")

    # 5. Send notifications
    if do_notify and new_opps:
        _send_notifications(new_opps, len(current_ids), dry_run=dry_run)

    # 6. Push to pipeline tracker
    if push_to_sheet and new_opps:
        _push_to_tracker(new_opps, dry_run=dry_run)

    # 7. Save results and state
    if not df.empty:
        path = save_results(df, "opportunity_pipeline")
        print(f"\n  Saved full pipeline to {path}")

    if not dry_run:
        save_current_state(current_ids)
    else:
        print("\n  [DRY-RUN] State file not updated")

    return {
        "total": len(current_ids),
        "new": len(new_ids),
        "removed": len(removed_ids),
        "new_opportunities": new_opps,
    }


def _send_notifications(new_opps: list[dict], total_count: int, dry_run: bool = False) -> None:
    """Send Slack and email notifications."""
    from notifications.notify import (
        format_email_opportunity_summary,
        format_slack_opportunity_summary,
        send_email_notification,
        send_slack_notification,
    )

    # Slack
    slack_url = os.getenv("SLACK_WEBHOOK_URL", "")
    if slack_url or dry_run:
        text, blocks = format_slack_opportunity_summary(new_opps, total_count)
        if dry_run:
            print(f"\n  [DRY-RUN] Slack notification preview:")
            print(f"    {text}")
            for opp in new_opps[:3]:
                title = (opp.get("title") or "?")[:60]
                print(f"    - {title}")
        else:
            send_slack_notification(slack_url, text, blocks)

    # Email
    resend_key = os.getenv("RESEND_API_KEY", "")
    resend_to = os.getenv("RESEND_TO_EMAIL", "")
    if (resend_key and resend_to) or dry_run:
        subject, html = format_email_opportunity_summary(new_opps, total_count)
        if dry_run:
            print(f"\n  [DRY-RUN] Email notification preview:")
            print(f"    Subject: {subject}")
            print(f"    To: {resend_to or '(not configured)'}")
        else:
            send_email_notification(resend_key, resend_to, subject, html)


def _push_to_tracker(new_opps: list[dict], dry_run: bool = False) -> None:
    """Push new opportunities to the GovCon Pipeline Tracker sheet."""
    try:
        from tracking.sheets_crm import GovConPipelineTracker
        tracker = GovConPipelineTracker(dry_run=dry_run)
        if not tracker.connect():
            log.warning("Failed to connect to pipeline tracker — skipping push")
            return
        if dry_run:
            tracker.initialize_sheets()
        result = tracker.import_from_opportunity_dicts(new_opps, source="daily_monitor")
        print(f"\n  Pipeline tracker: {result.get('imported', 0)} imported, "
              f"{result.get('duplicates', 0)} duplicates")
    except Exception as e:
        log.warning(f"Failed to push to pipeline tracker: {e}")


# ── CLI ──────────────────────────────────────────────────────────────────

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(
        description="Daily SAM.gov opportunity monitor with change detection"
    )
    parser.add_argument(
        "--max-pages", type=int, default=3,
        help="Max pages to fetch from SAM.gov (default: 3)",
    )
    parser.add_argument(
        "--score", action="store_true",
        help="Score new opportunities using bid/no-bid framework",
    )
    parser.add_argument(
        "--no-notify", action="store_true",
        help="Skip sending Slack/email notifications",
    )
    parser.add_argument(
        "--push-to-sheet", action="store_true",
        help="Push new opportunities to GovCon Pipeline Tracker sheet",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Run without saving state or sending real notifications",
    )

    args = parser.parse_args()

    result = run_monitor(
        max_pages=args.max_pages,
        do_score=args.score,
        do_notify=not args.no_notify,
        push_to_sheet=args.push_to_sheet,
        dry_run=args.dry_run,
    )

    if "error" in result:
        sys.exit(1)

    print(f"\nMonitor complete: {result['total']} total, "
          f"{result['new']} new, {result['removed']} removed")


if __name__ == "__main__":
    main()
