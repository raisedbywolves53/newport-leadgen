"""Instantly.ai cold email client — API integration + CSV fallback for manual upload.

Usage:
    python outreach/email/instantly_client.py create-campaign --template templates/agent_partner.json --account tal@goldmansgaragedoor.com
    python outreach/email/instantly_client.py push-leads --campaign-id abc123 --leads data/clay_enriched/agents.csv
    python outreach/email/instantly_client.py export --leads data/clay_enriched/agents.csv --template agent_partner --output data/instantly_ready/
    python outreach/email/instantly_client.py stats --campaign-id abc123
    python outreach/email/instantly_client.py list
"""

import argparse
import csv
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.instantly.ai/api/v2"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

# Merge-tag format conversion: templates use {tag}, Instantly uses {{tag}}
# These are the known custom variable fields from our templates
CUSTOM_VARIABLE_FIELDS = [
    "city", "county", "street", "state", "phone", "trade_type",
    "year_built", "nearby_city",
]

# CSV column → Instantly lead field mapping
CSV_TO_LEAD_FIELD = {
    "email": "email",
    "first_name": "first_name",
    "last_name": "last_name",
    "company_name": "company_name",
    "phone": "phone",
    "website": "website",
}

# CSV column → Instantly custom_variables mapping
CSV_TO_CUSTOM_VAR = {
    "city": "city",
    "county": "county",
    "street": "street",
    "state": "state",
    "trade_type": "trade_type",
    "year_built": "year_built",
    "nearby_city": "nearby_city",
}

# For manual CSV export: column → Instantly custom slot mapping
EXPORT_CUSTOM_SLOTS = {
    "company_name": "company_name",
    "city": "city",
    "county": "county",
    "street": "street",
    "phone": "phone",
    "state": "state",
    "trade_type": "trade_type",
    "year_built": "year_built",
    "nearby_city": "nearby_city",
}


def setup_logging() -> logging.Logger:
    """Configure logging to console + daily log file."""
    logger = logging.getLogger("instantly")
    logger.setLevel(logging.DEBUG)

    # Console handler — INFO and above
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console)

    # File handler — DEBUG and above
    log_dir = Path(__file__).resolve().parent.parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    file_handler = logging.FileHandler(log_dir / f"instantly_{date_str}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(file_handler)

    return logger


log = setup_logging()


def convert_merge_tags(text: str) -> str:
    """Convert template {tag} format to Instantly {{tag}} format."""
    import re
    # Match single-braced tags that aren't already double-braced
    return re.sub(r'(?<!\{)\{([a-z_]+)\}(?!\})', r'{{\1}}', text)


class InstantlyClient:
    """Manage cold email campaigns through Instantly.ai API (V2)."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("INSTANTLY_API_KEY", "")
        if not self.api_key:
            log.error(
                "ERROR: INSTANTLY_API_KEY not set. "
                "Add it to your .env file:\n  INSTANTLY_API_KEY=your_key_here\n"
                "Get your API key at https://app.instantly.ai/app/settings/integrations"
            )
            sys.exit(1)
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def _request(self, method: str, path: str, **kwargs) -> dict:
        """Make an API request with retry logic for rate limits and connection errors."""
        url = f"{BASE_URL}{path}"
        max_retries = 3

        for attempt in range(max_retries):
            try:
                log.debug(f"API {method} {path} (attempt {attempt + 1})")
                resp = self.session.request(method, url, timeout=30, **kwargs)

                if resp.status_code == 429:
                    wait = 2 ** (attempt + 1)
                    log.warning(f"Rate limited (429). Retrying in {wait}s...")
                    time.sleep(wait)
                    continue

                if resp.status_code == 401:
                    log.error("Authentication failed (401). Check your INSTANTLY_API_KEY.")
                    sys.exit(1)

                resp.raise_for_status()
                return resp.json() if resp.text else {}

            except requests.ConnectionError as exc:
                if attempt < max_retries - 1:
                    wait = 2 ** (attempt + 1)
                    log.warning(f"Connection error: {exc}. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    log.error(f"Connection failed after {max_retries} attempts: {exc}")
                    raise
            except requests.HTTPError as exc:
                log.error(f"API error: {exc} — {resp.text}")
                raise

        log.error(f"Request failed after {max_retries} attempts")
        raise RuntimeError(f"Max retries exceeded for {method} {path}")

    # ------------------------------------------------------------------
    # Campaign management
    # ------------------------------------------------------------------

    def create_campaign(self, template_path: str, sending_account: str) -> str:
        """Create an Instantly campaign from a template JSON file.

        Args:
            template_path: Path to template JSON (absolute or relative to templates dir).
            sending_account: Email address of the sending account in Instantly.

        Returns:
            Campaign ID (uuid string).
        """
        path = Path(template_path)
        if not path.is_absolute():
            path = TEMPLATES_DIR / path
        if not path.exists():
            log.error(f"Template not found: {path}")
            sys.exit(1)

        with open(path) as f:
            template = json.load(f)

        log.info(f"Creating campaign: {template['campaign_name']}")
        log.info(f"  Template: {path.name}")
        log.info(f"  Steps: {len(template['steps'])}")
        log.info(f"  Sending account: {sending_account}")

        # Build email steps for Instantly sequences format
        steps = []
        sorted_template_steps = sorted(template["steps"], key=lambda s: s["step_number"])

        for i, step in enumerate(sorted_template_steps):
            # Calculate delay: days between this step and the next
            if i < len(sorted_template_steps) - 1:
                delay = sorted_template_steps[i + 1]["send_day"] - step["send_day"]
            else:
                delay = 0  # Last step, no delay needed

            steps.append({
                "type": "email",
                "delay": delay,
                "delay_unit": "days",
                "variants": [{
                    "subject": convert_merge_tags(step["subject"]),
                    "body": convert_merge_tags(step["body"]),
                }],
            })

        payload = {
            "name": template["campaign_name"],
            "email_list": [sending_account],
            "campaign_schedule": {
                "schedules": [{
                    "name": "Weekday Business Hours",
                    "timing": {"from": "08:00", "to": "18:00"},
                    "days": {
                        "0": False,  # Sunday
                        "1": True,   # Monday
                        "2": True,   # Tuesday
                        "3": True,   # Wednesday
                        "4": True,   # Thursday
                        "5": True,   # Friday
                        "6": False,  # Saturday
                    },
                    "timezone": "America/New_York",
                }],
            },
            "sequences": [{"steps": steps}],
            "daily_limit": 30,
            "stop_on_reply": True,
            "stop_on_auto_reply": True,
            "text_only": True,
            "open_tracking": True,
            "link_tracking": False,
        }

        result = self._request("POST", "/campaigns", json=payload)
        campaign_id = result.get("id", "")
        status = result.get("status", "")

        log.info(f"  Campaign created: {campaign_id} (status: {status})")
        return campaign_id

    def add_leads_to_campaign(self, campaign_id: str, leads_csv: str) -> int:
        """Add leads from an enriched CSV to an Instantly campaign.

        Args:
            campaign_id: Instantly campaign UUID.
            leads_csv: Path to enriched CSV file (from Clay export).

        Returns:
            Count of leads successfully added.
        """
        csv_path = Path(leads_csv)
        if not csv_path.exists():
            log.error(f"Leads CSV not found: {csv_path}")
            sys.exit(1)

        df = pd.read_csv(csv_path)
        log.info(f"Loaded {len(df)} rows from {csv_path.name}")

        added = 0
        skipped = 0
        skip_reasons = {}

        for _, row in df.iterrows():
            email = str(row.get("email", "")).strip()

            # Skip rows without email
            if not email or email == "nan" or "@" not in email:
                reason = "missing/invalid email"
                skip_reasons[reason] = skip_reasons.get(reason, 0) + 1
                skipped += 1
                continue

            # Build lead payload
            lead = {
                "campaign": campaign_id,
                "email": email,
                "skip_if_in_campaign": True,
            }

            # Map standard fields
            for csv_col, lead_field in CSV_TO_LEAD_FIELD.items():
                if csv_col == "email":
                    continue  # Already set
                val = row.get(csv_col)
                if pd.notna(val) and str(val).strip():
                    lead[lead_field] = str(val).strip()

            # Map custom variables
            custom_vars = {}
            for csv_col, var_name in CSV_TO_CUSTOM_VAR.items():
                val = row.get(csv_col)
                if pd.notna(val) and str(val).strip():
                    custom_vars[var_name] = str(val).strip()

            if custom_vars:
                lead["custom_variables"] = custom_vars

            try:
                self._request("POST", "/leads", json=lead)
                added += 1
                if added % 25 == 0:
                    log.info(f"  Progress: {added} leads added...")
            except Exception as exc:
                reason = str(exc)[:80]
                skip_reasons[reason] = skip_reasons.get(reason, 0) + 1
                skipped += 1

        log.info(f"  Done: {added} leads added, {skipped} skipped")
        if skip_reasons:
            for reason, count in skip_reasons.items():
                log.info(f"    Skipped ({count}): {reason}")

        return added

    def get_campaign_stats(self, campaign_id: str) -> dict:
        """Get analytics for a specific campaign.

        Returns dict with: leads_count, sent, opened, replied, bounced, etc.
        """
        result = self._request("GET", "/campaigns/analytics", params={"id": campaign_id})

        # API returns an array; grab the first (and only) item
        if isinstance(result, list) and result:
            stats = result[0]
        else:
            stats = result

        summary = {
            "campaign_name": stats.get("campaign_name", ""),
            "campaign_id": stats.get("campaign_id", ""),
            "status": stats.get("campaign_status", ""),
            "leads_count": stats.get("leads_count", 0),
            "contacted": stats.get("contacted_count", 0),
            "sent": stats.get("emails_sent_count", 0),
            "opened": stats.get("open_count", 0),
            "opened_unique": stats.get("open_count_unique", 0),
            "replied": stats.get("reply_count", 0),
            "replied_unique": stats.get("reply_count_unique", 0),
            "bounced": stats.get("bounced_count", 0),
            "unsubscribed": stats.get("unsubscribed_count", 0),
            "completed": stats.get("completed_count", 0),
            "link_clicks": stats.get("link_click_count", 0),
        }
        return summary

    def list_campaigns(self) -> list:
        """List all campaigns with basic info.

        Returns list of dicts with id, name, and status.
        """
        all_campaigns = []
        starting_after = None

        while True:
            params = {"limit": 100}
            if starting_after:
                params["starting_after"] = starting_after

            result = self._request("GET", "/campaigns", params=params)
            items = result.get("items", [])
            if not items:
                break

            for c in items:
                all_campaigns.append({
                    "id": c.get("id", ""),
                    "name": c.get("name", ""),
                    "status": c.get("status", ""),
                })

            starting_after = result.get("next_starting_after")
            if not starting_after:
                break

        return all_campaigns

    def pause_campaign(self, campaign_id: str) -> None:
        """Pause a running campaign."""
        self._request("POST", f"/campaigns/{campaign_id}/pause")
        log.info(f"Campaign {campaign_id} paused")

    def resume_campaign(self, campaign_id: str) -> None:
        """Resume (activate) a paused campaign."""
        self._request("POST", f"/campaigns/{campaign_id}/activate")
        log.info(f"Campaign {campaign_id} activated")

    # ------------------------------------------------------------------
    # CSV fallback for manual upload
    # ------------------------------------------------------------------

    @staticmethod
    def export_for_manual_upload(leads_csv: str, template_name: str,
                                 output_path: str) -> Path:
        """Export leads as a CSV formatted for Instantly's manual upload UI.

        Instantly's CSV import expects:
          - email (required)
          - first_name, last_name, company_name (standard columns)
          - Any additional columns become custom variables automatically

        Args:
            leads_csv: Path to enriched CSV from Clay.
            template_name: Template name (for naming the output file).
            output_path: Directory for the output CSV.

        Returns:
            Path to the exported CSV.
        """
        csv_path = Path(leads_csv)
        if not csv_path.exists():
            log.error(f"Leads CSV not found: {csv_path}")
            sys.exit(1)

        df = pd.read_csv(csv_path)
        initial_count = len(df)

        # Drop rows without email
        df["email"] = df["email"].astype(str).str.strip()
        df = df[df["email"].str.contains("@", na=False)]
        df = df[df["email"] != "nan"]
        skipped = initial_count - len(df)

        # Build output columns in Instantly's expected order
        output_cols = ["email", "first_name"]

        # Add all custom variable columns that exist in the source data
        for col in EXPORT_CUSTOM_SLOTS:
            if col in df.columns and col not in output_cols:
                output_cols.append(col)

        # Also include last_name and website if present
        for extra in ["last_name", "website"]:
            if extra in df.columns:
                output_cols.append(extra)

        # Filter to only columns that exist
        available = [c for c in output_cols if c in df.columns]
        export_df = df[available].copy()

        # Clean up NaN values to empty strings
        export_df = export_df.fillna("")

        # Write output
        out_dir = Path(output_path)
        out_dir.mkdir(parents=True, exist_ok=True)

        clean_name = template_name.replace(".json", "").replace("/", "_")
        date_str = datetime.now().strftime("%Y%m%d")
        out_file = out_dir / f"instantly_{clean_name}_{date_str}.csv"
        export_df.to_csv(out_file, index=False, quoting=csv.QUOTE_ALL)

        log.info(f"Exported {len(export_df)} leads for '{clean_name}' campaign → {out_file}")
        if skipped:
            log.info(f"  Skipped {skipped} rows (missing/invalid email)")

        return out_file


# ------------------------------------------------------------------
# Status display helpers
# ------------------------------------------------------------------

STATUS_LABELS = {
    0: "Draft",
    1: "Active",
    2: "Paused",
    3: "Completed",
    4: "Running Subsequences",
    -99: "Account Suspended",
    -1: "Accounts Unhealthy",
    -2: "Bounce Protect",
}


def format_status(code) -> str:
    return STATUS_LABELS.get(code, f"Unknown ({code})")


def print_stats(stats: dict) -> None:
    """Pretty-print campaign analytics."""
    print(f"\n{'='*50}")
    print(f"Campaign: {stats['campaign_name']}")
    print(f"ID:       {stats['campaign_id']}")
    print(f"Status:   {format_status(stats['status'])}")
    print(f"{'='*50}")
    print(f"  Leads:        {stats['leads_count']}")
    print(f"  Contacted:    {stats['contacted']}")
    print(f"  Emails sent:  {stats['sent']}")
    print(f"  Opened:       {stats['opened_unique']} unique ({stats['opened']} total)")
    print(f"  Replied:      {stats['replied_unique']} unique ({stats['replied']} total)")
    print(f"  Bounced:      {stats['bounced']}")
    print(f"  Unsubscribed: {stats['unsubscribed']}")
    print(f"  Completed:    {stats['completed']}")

    if stats['sent'] > 0:
        open_rate = stats['opened_unique'] / stats['sent'] * 100
        reply_rate = stats['replied_unique'] / stats['sent'] * 100
        bounce_rate = stats['bounced'] / stats['sent'] * 100
        print(f"\n  Open rate:    {open_rate:.1f}%")
        print(f"  Reply rate:   {reply_rate:.1f}%")
        print(f"  Bounce rate:  {bounce_rate:.1f}%")
    print()


def print_campaign_list(campaigns: list) -> None:
    """Pretty-print campaign list."""
    if not campaigns:
        print("No campaigns found.")
        return
    print(f"\n{'ID':<40} {'Status':<22} {'Name'}")
    print("-" * 90)
    for c in campaigns:
        status = format_status(c["status"])
        print(f"{c['id']:<40} {status:<22} {c['name']}")
    print(f"\nTotal: {len(campaigns)} campaigns\n")


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Instantly.ai cold email client for Goldman's lead gen"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create-campaign
    create_p = subparsers.add_parser(
        "create-campaign", help="Create a campaign from a template JSON"
    )
    create_p.add_argument(
        "--template", required=True,
        help="Path to template JSON (e.g. templates/agent_partner.json)"
    )
    create_p.add_argument(
        "--account", required=True,
        help="Sending email account in Instantly (e.g. tal@goldmansgaragedoor.com)"
    )

    # push-leads
    push_p = subparsers.add_parser(
        "push-leads", help="Push enriched leads CSV to an existing campaign"
    )
    push_p.add_argument("--campaign-id", required=True, help="Instantly campaign ID")
    push_p.add_argument("--leads", required=True, help="Path to enriched leads CSV")

    # export (CSV fallback)
    export_p = subparsers.add_parser(
        "export", help="Export leads CSV formatted for Instantly manual upload"
    )
    export_p.add_argument("--leads", required=True, help="Path to enriched leads CSV")
    export_p.add_argument(
        "--template", required=True,
        help="Template name for output file naming (e.g. agent_partner)"
    )
    export_p.add_argument(
        "--output", default="./data/instantly_ready/",
        help="Output directory (default: ./data/instantly_ready/)"
    )

    # stats
    stats_p = subparsers.add_parser("stats", help="Get analytics for a campaign")
    stats_p.add_argument("--campaign-id", required=True, help="Instantly campaign ID")

    # list
    subparsers.add_parser("list", help="List all campaigns")

    # pause
    pause_p = subparsers.add_parser("pause", help="Pause a campaign")
    pause_p.add_argument("--campaign-id", required=True, help="Instantly campaign ID")

    # resume
    resume_p = subparsers.add_parser("resume", help="Resume a paused campaign")
    resume_p.add_argument("--campaign-id", required=True, help="Instantly campaign ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Export command doesn't need API key
    if args.command == "export":
        InstantlyClient.export_for_manual_upload(
            args.leads, args.template, args.output
        )
        return

    # All other commands need the API client
    client = InstantlyClient()

    if args.command == "create-campaign":
        campaign_id = client.create_campaign(args.template, args.account)
        print(f"\nCampaign created: {campaign_id}")
        print(f"Next: push leads with:")
        print(f"  python outreach/email/instantly_client.py push-leads "
              f"--campaign-id {campaign_id} --leads <enriched_csv>")

    elif args.command == "push-leads":
        count = client.add_leads_to_campaign(args.campaign_id, args.leads)
        print(f"\n{count} leads added to campaign {args.campaign_id}")

    elif args.command == "stats":
        stats = client.get_campaign_stats(args.campaign_id)
        print_stats(stats)

    elif args.command == "list":
        campaigns = client.list_campaigns()
        print_campaign_list(campaigns)

    elif args.command == "pause":
        client.pause_campaign(args.campaign_id)
        print(f"Campaign {args.campaign_id} paused")

    elif args.command == "resume":
        client.resume_campaign(args.campaign_id)
        print(f"Campaign {args.campaign_id} activated")


if __name__ == "__main__":
    main()
