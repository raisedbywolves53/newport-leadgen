"""Daily SAM.gov opportunity monitor with change detection and notifications.

Runs the full monitoring cycle:
  1. Query SAM.gov Opportunities API for all Newport NAICS codes
  2. Compare against previous run to detect new opportunities
  3. Score new opportunities via BidNoBidScorer
  4. Push to Google Sheets pipeline tracker
  5. Send email + Slack digest with new finds, deadlines, and pipeline snapshot

Usage:
    python scrapers/daily_monitor.py --dry-run
    python scrapers/daily_monitor.py --score --dry-run
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

log = logging.getLogger(__name__)

STATE_FILE = _project_root / "data" / "cache" / "last_opportunities.json"

NEWPORT_NAICS = [
    "424410",  # General Line Grocery Merchant Wholesalers
    "424450",  # Confectionery Merchant Wholesalers
    "424490",  # Other Grocery and Related Products
    "722310",  # Food Service Contractors
    "424420",  # Packaged Frozen Food
    "424430",  # Dairy Product
    "424440",  # Poultry and Poultry Product
    "424460",  # Fish and Seafood
    "424470",  # Meat and Meat Product
    "424480",  # Fresh Fruit and Vegetable
]

# Opportunity types to search
PTYPES = ["o", "p", "r", "k"]  # solicitation, pre-sol, sources sought, combined


# -- State persistence --------------------------------------------------------

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


# -- SAM.gov fetching --------------------------------------------------------

def fetch_opportunities(max_pages: int = 3) -> list[dict]:
    """Fetch current opportunities from SAM.gov for all Newport NAICS codes.

    Uses SAMClient directly. Each NAICS x ptype combo = 1 API request.
    Returns list of flattened opportunity dicts, deduplicated by notice_id.
    """
    from enrichment.sam_client import SAMClient

    try:
        client = SAMClient()
    except ValueError as e:
        print(f"\nERROR: {e}")
        print("Set SAM_GOV_API_KEY in .env to enable the daily monitor.")
        raise

    print(f"\nFetching opportunities for {len(NEWPORT_NAICS)} NAICS codes...")
    raw_results = client.search_opportunities_all_naics(
        naics_codes=NEWPORT_NAICS,
        ptypes=PTYPES,
        max_per_query=100,
    )

    # Flatten all results
    flattened = []
    seen = set()
    for raw in raw_results:
        flat = SAMClient.flatten_opportunity(raw)
        nid = flat.get("notice_id", "")
        if nid and nid not in seen:
            seen.add(nid)
            flattened.append(flat)

    print(f"  Total unique opportunities: {len(flattened)}")
    print(f"  SAM.gov API usage: {client.stats}")
    return flattened


# -- Main monitor logic -------------------------------------------------------

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
    print(f"\n{'='*70}")
    print(f"DAILY SAM.GOV MONITOR — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*70}")

    # 1. Load previous state
    previous_ids = load_previous_state()

    # 2. Fetch current opportunities
    try:
        all_opps = fetch_opportunities(max_pages=max_pages)
    except ValueError:
        return {"error": "SAM_GOV_API_KEY not set"}

    if not all_opps:
        print("No opportunities found.")
        save_current_state(set())
        return {"total": 0, "new": 0, "removed": len(previous_ids)}

    # 3. Detect changes
    current_ids = {opp["notice_id"] for opp in all_opps if opp.get("notice_id")}
    new_ids = current_ids - previous_ids
    removed_ids = previous_ids - current_ids

    new_opps = [opp for opp in all_opps if opp.get("notice_id") in new_ids]

    print(f"\n  Total opportunities: {len(current_ids)}")
    print(f"  New since last run:  {len(new_ids)}")
    print(f"  Removed/expired:     {len(removed_ids)}")

    # 4. Score new opportunities
    if do_score and new_opps:
        print(f"\nScoring {len(new_opps)} new opportunities...")
        from scoring.bid_no_bid import BidNoBidScorer

        scorer = BidNoBidScorer()
        scored = scorer.score_batch(new_opps)
        new_opps = scored

        print(f"\n  Top scored new opportunities:")
        for opp in new_opps[:5]:
            title = (opp.get("title") or "?")[:50]
            score = opp.get("bid_score", "N/A")
            decision = opp.get("bid_decision", "")
            print(f"    {score:>5} ({decision:10s}) {title}")

    # 5. Get pipeline context for digest (deadlines + snapshot)
    deadlines = []
    pipeline_stats = None
    if push_to_sheet:
        pipeline_stats, deadlines = _get_pipeline_context(
            new_opps, dry_run=dry_run
        )

    # 6. Send notifications
    if do_notify and new_opps:
        _send_notifications(
            new_opps, len(current_ids),
            deadlines=deadlines,
            pipeline_stats=pipeline_stats,
            dry_run=dry_run,
        )

    # 7. Save state
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


def _get_pipeline_context(
    new_opps: list[dict],
    dry_run: bool = False,
) -> tuple[dict | None, list]:
    """Push new opps to pipeline and get dashboard context.

    Returns (pipeline_stats, deadlines).
    """
    try:
        from tracking.sheets_pipeline import GovConPipeline

        pipeline = GovConPipeline(dry_run=dry_run)
        if not pipeline.connect():
            log.warning("Failed to connect to pipeline — skipping push")
            return None, []

        if dry_run:
            pipeline.setup_sheets()

        # Import new opportunities
        if new_opps:
            result = pipeline.import_from_dicts(new_opps, source="SAM.gov")
            print(f"\n  Pipeline tracker: {result.get('imported', 0)} imported, "
                  f"{result.get('duplicates', 0)} duplicates")

        # Get context for digest
        deadlines = pipeline.get_upcoming_deadlines(days=7)
        dashboard = pipeline.get_dashboard_data()

        pipeline_stats = {
            "active_count": dashboard.get("total_opportunities", 0)
                           - dashboard.get("by_stage", {}).get("Awarded", 0)
                           - dashboard.get("by_stage", {}).get("Lost", 0)
                           - dashboard.get("by_stage", {}).get("No-Bid", 0)
                           - dashboard.get("by_stage", {}).get("Cancelled", 0),
            "proposals_in_progress": (
                dashboard.get("by_stage", {}).get("Drafting Proposal", 0)
                + dashboard.get("by_stage", {}).get("Internal Review", 0)
            ),
            "submitted_awaiting": (
                dashboard.get("by_stage", {}).get("Submitted", 0)
                + dashboard.get("by_stage", {}).get("Under Evaluation", 0)
            ),
            "pipeline_value": dashboard.get("pipeline_value", 0),
        }

        return pipeline_stats, deadlines

    except Exception as e:
        log.warning(f"Failed to get pipeline context: {e}")
        return None, []


def _send_notifications(
    new_opps: list[dict],
    total_count: int,
    deadlines: list[dict] | None = None,
    pipeline_stats: dict | None = None,
    dry_run: bool = False,
) -> None:
    """Send Slack and email notifications."""
    from notifications.notify import (
        format_email_digest,
        format_slack_opportunity_summary,
        send_email_notification,
        send_slack_notification,
    )

    # Slack
    slack_url = os.getenv("SLACK_WEBHOOK_URL", "")
    if slack_url or dry_run:
        text, blocks = format_slack_opportunity_summary(
            new_opps, total_count,
            deadlines=deadlines,
            pipeline_stats=pipeline_stats,
        )
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
    resend_to = os.getenv("NOTIFICATION_EMAIL", "")
    if (resend_key and resend_to) or dry_run:
        subject, html = format_email_digest(
            new_opps, total_count,
            deadlines=deadlines,
            pipeline_stats=pipeline_stats,
        )
        if dry_run:
            print(f"\n  [DRY-RUN] Email notification preview:")
            print(f"    Subject: {subject}")
            print(f"    To: {resend_to or '(not configured)'}")
        else:
            send_email_notification(resend_key, resend_to, subject, html)


# -- CLI ----------------------------------------------------------------------

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(
        description="Daily SAM.gov opportunity monitor with change detection"
    )
    parser.add_argument(
        "--max-pages", type=int, default=3,
        help="Max pages to fetch from SAM.gov per query (default: 3)",
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
