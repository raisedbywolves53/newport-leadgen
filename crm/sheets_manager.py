#!/usr/bin/env python3
"""
Google Sheets CRM for Goldman's Garage Door Repair.

Manages leads, outreach logging, referral partners, campaigns,
and a summary dashboard via Google Sheets (gspread).

Supports --dry-run mode for testing without Google API credentials.

Usage:
    python crm/sheets_manager.py --init
    python crm/sheets_manager.py --add-lead --first-name John --last-name Smith --email j@test.com --market oakland --icp new_homeowner
    python crm/sheets_manager.py --dashboard
    python crm/sheets_manager.py --dry-run --dashboard
"""

import argparse
import csv
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("sheets_manager")
logger.setLevel(logging.DEBUG)

_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))
logger.addHandler(_console)

_file_handler = logging.FileHandler(LOG_DIR / f"crm_{datetime.now():%Y%m%d}.log")
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(_file_handler)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_STATUSES = [
    "new", "contacted", "responded", "qualified",
    "scheduled", "closed_won", "closed_lost", "unsubscribed",
]

VALID_CHANNELS = ["email", "sms", "voice", "manual"]

VALID_DIRECTIONS = ["outbound", "inbound"]

VALID_ACTIVITY_STATUSES = [
    "sent", "delivered", "opened", "clicked", "replied",
    "bounced", "failed", "connected", "voicemail", "no_answer", "transferred",
]

VALID_PARTNER_STATUSES = [
    "prospecting", "contacted", "interested", "active", "inactive",
]

VALID_CAMPAIGN_STATUSES = ["draft", "active", "paused", "completed"]

VALID_MARKETS = ["oakland", "wayne", "triangle"]

VALID_ICP_TYPES = [
    "new_homeowner", "real_estate_agent", "property_manager",
    "commercial", "aging_neighborhood", "storm_damage",
]

VALID_PIPELINES = ["direct_customer", "referral_partner"]

VALID_SOURCES = [
    "homeowner_scraper", "gmaps_scraper", "clay", "manual", "storm_alert",
]

# Tab definitions: name -> list of column headers
TAB_DEFINITIONS = {
    "Leads": [
        "lead_id", "created_date", "source", "icp_type", "pipeline", "market",
        "first_name", "last_name", "company", "email", "phone",
        "address", "city", "zip", "status", "score", "notes", "last_activity",
    ],
    "Outreach Log": [
        "activity_id", "lead_id", "timestamp", "channel", "direction",
        "campaign_name", "subject_or_message", "status", "notes",
    ],
    "Referral Partners": [
        "partner_id", "business_name", "contact_name", "partner_type",
        "market", "phone", "email", "status",
        "referrals_sent", "referrals_received", "last_contact", "notes",
    ],
    "Campaigns": [
        "campaign_id", "name", "channel", "icp_type", "market",
        "start_date", "status", "total_leads", "sent", "delivered",
        "opened", "replied", "interested", "scheduled", "closed",
        "cost", "notes",
    ],
    "Dashboard": [],  # Special — populated with formulas
}

# Dashboard layout: (row, col) -> value or formula
# Rows/cols are 1-indexed to match Sheets
DASHBOARD_LAYOUT = {
    (1, 1): "Goldman's Garage Door Repair — Lead Gen Dashboard",
    (3, 1): "Last Updated:",
    (3, 2): "",  # Will hold NOW() formula
    (5, 1): "PIPELINE SUMMARY",
    (6, 1): "Total Leads:",
    (6, 2): "=COUNTA(Leads!A2:A)",
    (7, 1): "New (uncontacted):",
    (7, 2): '=COUNTIF(Leads!O2:O,"new")',
    (8, 1): "Contacted:",
    (8, 2): '=COUNTIF(Leads!O2:O,"contacted")',
    (9, 1): "Responded:",
    (9, 2): '=COUNTIF(Leads!O2:O,"responded")',
    (10, 1): "Qualified:",
    (10, 2): '=COUNTIF(Leads!O2:O,"qualified")',
    (11, 1): "Scheduled:",
    (11, 2): '=COUNTIF(Leads!O2:O,"scheduled")',
    (12, 1): "Closed Won:",
    (12, 2): '=COUNTIF(Leads!O2:O,"closed_won")',
    (14, 1): "BY MARKET",
    (15, 1): "Oakland:",
    (15, 2): '=COUNTIF(Leads!F2:F,"oakland")',
    (16, 1): "Wayne:",
    (16, 2): '=COUNTIF(Leads!F2:F,"wayne")',
    (17, 1): "Triangle:",
    (17, 2): '=COUNTIF(Leads!F2:F,"triangle")',
    (19, 1): "BY CHANNEL",
    (20, 1): "Email Sent:",
    (20, 2): '=COUNTIF(\'Outreach Log\'!D2:D,"email")',
    (21, 1): "SMS Sent:",
    (21, 2): '=COUNTIF(\'Outreach Log\'!D2:D,"sms")',
    (22, 1): "Calls Made:",
    (22, 2): '=COUNTIF(\'Outreach Log\'!D2:D,"voice")',
    (24, 1): "Active Referral Partners:",
    (24, 2): '=COUNTIF(\'Referral Partners\'!H2:H,"active")',
}


def _generate_id() -> str:
    """Generate a short 8-character UUID."""
    return uuid.uuid4().hex[:8]


def _now_iso() -> str:
    """Current timestamp in ISO format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _today_iso() -> str:
    """Current date in ISO format."""
    return datetime.now().strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------

class _RateLimiter:
    """Enforce minimum delay between Google Sheets API calls."""

    def __init__(self, min_interval: float = 0.5):
        self.min_interval = min_interval
        self._last_call = 0.0

    def wait(self):
        elapsed = time.time() - self._last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_call = time.time()


# ---------------------------------------------------------------------------
# In-memory sheet store for dry-run mode
# ---------------------------------------------------------------------------

class _DryRunSheet:
    """Mimics a gspread Worksheet using an in-memory list-of-lists."""

    def __init__(self, title: str, headers: list[str] | None = None):
        self.title = title
        # Row 0 = headers, rows 1+ = data
        if headers:
            self._rows: list[list[str]] = [headers]
        else:
            self._rows: list[list[str]] = []

    @property
    def row_count(self) -> int:
        return len(self._rows)

    def row_values(self, row: int) -> list[str]:
        if 1 <= row <= len(self._rows):
            return list(self._rows[row - 1])
        return []

    def get_all_records(self) -> list[dict]:
        if len(self._rows) < 2:
            return []
        headers = self._rows[0]
        records = []
        for row in self._rows[1:]:
            padded = row + [""] * (len(headers) - len(row))
            records.append(dict(zip(headers, padded)))
        return records

    def get_all_values(self) -> list[list[str]]:
        return [list(r) for r in self._rows]

    def append_row(self, values: list, value_input_option: str = "USER_ENTERED"):
        str_values = [str(v) for v in values]
        self._rows.append(str_values)

    def update_cell(self, row: int, col: int, value):
        while len(self._rows) < row:
            self._rows.append([])
        while len(self._rows[row - 1]) < col:
            self._rows[row - 1].append("")
        self._rows[row - 1][col - 1] = str(value)

    def batch_update(self, data: list[dict], value_input_option: str = "USER_ENTERED"):
        for entry in data:
            range_str = entry["range"]
            values = entry["values"]
            # Parse "A1" style range — only single-cell supported here
            col_letter = ""
            row_num = ""
            for ch in range_str:
                if ch.isalpha():
                    col_letter += ch
                else:
                    row_num += ch
            if not col_letter or not row_num:
                continue
            col = 0
            for ch in col_letter.upper():
                col = col * 26 + (ord(ch) - ord("A") + 1)
            row = int(row_num)
            val = values[0][0] if values and values[0] else ""
            self.update_cell(row, col, val)

    def col_values(self, col: int) -> list[str]:
        result = []
        for row in self._rows:
            if col <= len(row):
                result.append(row[col - 1])
            else:
                result.append("")
        return result

    def find(self, query: str):
        """Find first cell matching query. Returns a cell-like object or None."""
        for r_idx, row in enumerate(self._rows):
            for c_idx, val in enumerate(row):
                if val == query:
                    return type("Cell", (), {"row": r_idx + 1, "col": c_idx + 1, "value": val})()
        return None

    def findall(self, query: str):
        results = []
        for r_idx, row in enumerate(self._rows):
            for c_idx, val in enumerate(row):
                if val == query:
                    results.append(
                        type("Cell", (), {"row": r_idx + 1, "col": c_idx + 1, "value": val})()
                    )
        return results

    def delete_rows(self, start_index: int, end_index: int = None):
        """Delete row(s) by 1-based index."""
        if end_index is None:
            end_index = start_index
        # Convert 1-based to 0-based and delete
        del self._rows[start_index - 1 : end_index]


class _DryRunSpreadsheet:
    """Mimics a gspread Spreadsheet using in-memory worksheets."""

    def __init__(self):
        self._sheets: dict[str, _DryRunSheet] = {}

    def worksheets(self) -> list:
        return [
            type("WS", (), {"title": t})()
            for t in self._sheets
        ]

    def worksheet(self, title: str) -> _DryRunSheet:
        if title not in self._sheets:
            raise Exception(f"Worksheet '{title}' not found")
        return self._sheets[title]

    def add_worksheet(self, title: str, rows: int = 1000, cols: int = 26) -> _DryRunSheet:
        ws = _DryRunSheet(title)
        self._sheets[title] = ws
        return ws


# ---------------------------------------------------------------------------
# SheetsManager
# ---------------------------------------------------------------------------

class SheetsManager:
    """Google Sheets CRM for Goldman's lead tracking."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.creds_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")
        self.spreadsheet_id = os.getenv("GOOGLE_SHEETS_ID")
        self.client = None
        self.spreadsheet = None
        self._rate_limiter = _RateLimiter(min_interval=0.5)

        if dry_run:
            logger.info("DRY-RUN mode — using in-memory sheet store")
            self.spreadsheet = _DryRunSpreadsheet()

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    def connect(self) -> bool:
        """Authenticate and open spreadsheet.

        Supports two modes:
        - GOOGLE_SHEETS_CREDENTIALS=ADC  → Application Default Credentials
          (set up via ``gcloud auth application-default login``)
        - GOOGLE_SHEETS_CREDENTIALS=path/to/service-account.json
        """
        if self.dry_run:
            logger.info("[DRY-RUN] Skipping Google authentication")
            return True

        try:
            import gspread

            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]

            if self.creds_file.upper() == "ADC":
                # Use Application Default Credentials (gcloud auth)
                import google.auth
                import google.auth.transport.requests
                creds, _ = google.auth.default(scopes=scopes)
                creds.refresh(google.auth.transport.requests.Request())
                self.client = gspread.authorize(creds)
                logger.info("Authenticated via Application Default Credentials")
            else:
                # Use service account JSON key file
                from google.oauth2.service_account import Credentials
                creds = Credentials.from_service_account_file(self.creds_file, scopes=scopes)
                self.client = gspread.authorize(creds)
                logger.info("Authenticated via service account key")

            self._rate_limiter.wait()
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            logger.info("Connected to Google Sheets successfully")
            return True
        except FileNotFoundError:
            logger.error(f"Credentials file not found: {self.creds_file}")
            return False
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {e}")
            return False

    def _api_call(self, func, *args, **kwargs):
        """Wrap an API call with rate limiting and retry logic."""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self.dry_run:
                    self._rate_limiter.wait()
                return func(*args, **kwargs)
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    wait_time = 2 ** (attempt + 1)
                    logger.warning(f"Rate limited, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                elif attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"API error: {e}, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    raise

    def _get_worksheet(self, tab_name: str):
        """Get a worksheet by tab name."""
        return self._api_call(self.spreadsheet.worksheet, tab_name)

    # ------------------------------------------------------------------
    # Sheet Initialization
    # ------------------------------------------------------------------

    def initialize_sheets(self) -> None:
        """Create all 5 tabs with headers and Dashboard formulas.

        Only creates tabs that don't already exist (safe to re-run).
        """
        existing = [ws.title for ws in self.spreadsheet.worksheets()]
        logger.info(f"Existing tabs: {existing}")

        # Create data tabs with headers
        for tab_name, headers in TAB_DEFINITIONS.items():
            if tab_name == "Dashboard":
                continue  # Handle separately
            if tab_name in existing:
                logger.info(f"Tab '{tab_name}' already exists — skipping")
                continue

            logger.info(f"Creating tab '{tab_name}' with {len(headers)} columns")
            ws = self._api_call(
                self.spreadsheet.add_worksheet,
                title=tab_name, rows=1000, cols=max(len(headers), 20),
            )
            self._api_call(
                ws.append_row, headers, value_input_option="RAW",
            )

        # Create Dashboard tab with labels and formulas
        if "Dashboard" not in existing:
            logger.info("Creating Dashboard tab with formulas")
            ws = self._api_call(
                self.spreadsheet.add_worksheet,
                title="Dashboard", rows=30, cols=5,
            )
        else:
            ws = self._get_worksheet("Dashboard")
            logger.info("Dashboard tab exists — updating formulas")

        # Batch-write dashboard cells
        batch_data = []
        for (row, col), value in DASHBOARD_LAYOUT.items():
            col_letter = chr(ord("A") + col - 1)
            cell_ref = f"{col_letter}{row}"
            batch_data.append({
                "range": cell_ref,
                "values": [[value]],
            })

        # Add NOW() formula for last updated
        batch_data.append({
            "range": "B3",
            "values": [["=NOW()"]],
        })

        self._api_call(
            ws.batch_update, batch_data, value_input_option="USER_ENTERED",
        )

        # Try to delete default "Sheet1" if it exists
        if "Sheet1" in existing:
            try:
                sheet1 = self._get_worksheet("Sheet1")
                if not self.dry_run:
                    self._api_call(self.spreadsheet.del_worksheet, sheet1)
                    logger.info("Deleted default 'Sheet1' tab")
            except Exception:
                pass  # Not critical

        logger.info("Sheet initialization complete")

    # ------------------------------------------------------------------
    # Lead Management
    # ------------------------------------------------------------------

    def add_lead(self, lead_data: dict) -> str:
        """Add a new lead. Auto-generates lead_id, sets created_date,
        status='new'. Returns lead_id.

        Deduplicates by email OR phone — if match found, updates existing.
        """
        ws = self._get_worksheet("Leads")
        headers = TAB_DEFINITIONS["Leads"]

        # Check for duplicates by email or phone
        email = lead_data.get("email", "").strip().lower()
        phone = lead_data.get("phone", "").strip()

        existing_records = self._api_call(ws.get_all_records)

        for record in existing_records:
            rec_email = str(record.get("email", "")).strip().lower()
            rec_phone = str(record.get("phone", "")).strip()

            match_email = email and rec_email and email == rec_email
            match_phone = phone and rec_phone and phone == rec_phone

            if match_email or match_phone:
                existing_id = str(record.get("lead_id", ""))
                logger.info(f"Duplicate found (lead_id={existing_id}), updating existing record")
                # Update existing record with new data
                updates = {k: v for k, v in lead_data.items() if v}
                updates["last_activity"] = _now_iso()
                self.update_lead(existing_id, updates)
                return existing_id

        # No duplicate — create new lead
        lead_id = _generate_id()
        row = []
        for col in headers:
            if col == "lead_id":
                row.append(lead_id)
            elif col == "created_date":
                row.append(_today_iso())
            elif col == "status":
                row.append(lead_data.get("status", "new"))
            elif col == "last_activity":
                row.append(_now_iso())
            elif col == "score":
                row.append(lead_data.get("score", ""))
            else:
                row.append(lead_data.get(col, ""))

        self._api_call(ws.append_row, row, value_input_option="USER_ENTERED")
        logger.info(f"Added lead {lead_id}: {lead_data.get('first_name', '')} {lead_data.get('last_name', '')}")
        return lead_id

    def update_lead(self, lead_id: str, updates: dict) -> bool:
        """Update specific fields on a lead by lead_id."""
        ws = self._get_worksheet("Leads")
        headers = TAB_DEFINITIONS["Leads"]

        cell = self._api_call(ws.find, lead_id)
        if not cell:
            logger.warning(f"Lead {lead_id} not found")
            return False

        row_num = cell.row
        batch_data = []
        for field, value in updates.items():
            if field in headers:
                col_idx = headers.index(field) + 1
                col_letter = chr(ord("A") + col_idx - 1) if col_idx <= 26 else "A"
                batch_data.append({
                    "range": f"{col_letter}{row_num}",
                    "values": [[str(value)]],
                })

        if batch_data:
            self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")
            logger.info(f"Updated lead {lead_id}: {list(updates.keys())}")
            return True
        return False

    def get_lead(self, lead_id: str) -> dict:
        """Get a lead by ID."""
        ws = self._get_worksheet("Leads")
        headers = TAB_DEFINITIONS["Leads"]

        cell = self._api_call(ws.find, lead_id)
        if not cell:
            logger.warning(f"Lead {lead_id} not found")
            return {}

        row_values = self._api_call(ws.row_values, cell.row)
        # Pad row_values to match headers length
        row_values = row_values + [""] * (len(headers) - len(row_values))
        return dict(zip(headers, row_values))

    def find_leads(self, filters: dict) -> list[dict]:
        """Find leads matching filters (status, market, icp_type, etc.)."""
        ws = self._get_worksheet("Leads")
        records = self._api_call(ws.get_all_records)

        results = []
        for record in records:
            match = True
            for key, value in filters.items():
                rec_val = str(record.get(key, "")).strip().lower()
                if rec_val != str(value).strip().lower():
                    match = False
                    break
            if match:
                results.append(record)

        logger.info(f"Found {len(results)} leads matching {filters}")
        return results

    def update_lead_status(self, lead_id: str, new_status: str) -> bool:
        """Update lead status and last_activity timestamp."""
        if new_status not in VALID_STATUSES:
            logger.error(f"Invalid status '{new_status}'. Valid: {VALID_STATUSES}")
            return False
        return self.update_lead(lead_id, {
            "status": new_status,
            "last_activity": _now_iso(),
        })

    def delete_lead(self, lead_id: str) -> bool:
        """Delete a lead by lead_id. Used for test cleanup.

        Returns True if the lead was found and deleted.
        """
        ws = self._get_worksheet("Leads")

        cell = self._api_call(ws.find, lead_id)
        if not cell:
            logger.warning(f"Lead {lead_id} not found for deletion")
            return False

        self._api_call(ws.delete_rows, cell.row)
        logger.info(f"Deleted lead {lead_id}")
        return True

    # ------------------------------------------------------------------
    # Outreach Logging
    # ------------------------------------------------------------------

    def log_activity(self, lead_id: str, channel: str, direction: str,
                     campaign_name: str, subject_or_message: str,
                     status: str, notes: str = "") -> str:
        """Log an outreach activity. Returns activity_id."""
        ws = self._get_worksheet("Outreach Log")

        activity_id = _generate_id()
        # Truncate message to 200 chars
        truncated_msg = subject_or_message[:200] if subject_or_message else ""

        row = [
            activity_id,
            lead_id,
            _now_iso(),
            channel,
            direction,
            campaign_name,
            truncated_msg,
            status,
            notes,
        ]
        self._api_call(ws.append_row, row, value_input_option="USER_ENTERED")
        logger.info(f"Logged activity {activity_id} for lead {lead_id} ({channel}/{status})")

        # Update last_activity on the lead
        self.update_lead(lead_id, {"last_activity": _now_iso()})

        return activity_id

    def get_lead_history(self, lead_id: str) -> list[dict]:
        """Get all outreach activities for a lead, sorted by timestamp."""
        ws = self._get_worksheet("Outreach Log")
        headers = TAB_DEFINITIONS["Outreach Log"]
        records = self._api_call(ws.get_all_records)

        history = [r for r in records if str(r.get("lead_id", "")) == lead_id]
        history.sort(key=lambda r: r.get("timestamp", ""))
        return history

    # ------------------------------------------------------------------
    # Referral Partners
    # ------------------------------------------------------------------

    def add_partner(self, lead_id: str, partner_data: dict) -> None:
        """Add/update a referral partner entry linked to a lead."""
        ws = self._get_worksheet("Referral Partners")
        headers = TAB_DEFINITIONS["Referral Partners"]

        # Check if partner already exists
        cell = self._api_call(ws.find, lead_id)
        if cell:
            logger.info(f"Partner {lead_id} already exists, updating")
            batch_data = []
            for field, value in partner_data.items():
                if field in headers:
                    col_idx = headers.index(field) + 1
                    col_letter = chr(ord("A") + col_idx - 1)
                    batch_data.append({
                        "range": f"{col_letter}{cell.row}",
                        "values": [[str(value)]],
                    })
            if batch_data:
                self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")
            return

        row = []
        for col in headers:
            if col == "partner_id":
                row.append(lead_id)
            elif col == "referrals_sent":
                row.append(partner_data.get("referrals_sent", "0"))
            elif col == "referrals_received":
                row.append(partner_data.get("referrals_received", "0"))
            elif col == "status":
                row.append(partner_data.get("status", "prospecting"))
            elif col == "last_contact":
                row.append(_now_iso())
            else:
                row.append(partner_data.get(col, ""))

        self._api_call(ws.append_row, row, value_input_option="USER_ENTERED")
        logger.info(f"Added referral partner {lead_id}: {partner_data.get('business_name', '')}")

    def get_active_partners(self, market: str = None) -> list[dict]:
        """Get all active referral partners, optionally filtered by market."""
        ws = self._get_worksheet("Referral Partners")
        records = self._api_call(ws.get_all_records)

        results = []
        for r in records:
            if str(r.get("status", "")).lower() != "active":
                continue
            if market and str(r.get("market", "")).lower() != market.lower():
                continue
            results.append(r)

        return results

    def log_referral(self, partner_id: str, direction: str) -> None:
        """Increment referral count. direction: 'sent' or 'received'."""
        ws = self._get_worksheet("Referral Partners")
        headers = TAB_DEFINITIONS["Referral Partners"]

        cell = self._api_call(ws.find, partner_id)
        if not cell:
            logger.warning(f"Partner {partner_id} not found")
            return

        if direction == "sent":
            col_name = "referrals_sent"
        elif direction == "received":
            col_name = "referrals_received"
        else:
            logger.error(f"Invalid referral direction: {direction}")
            return

        col_idx = headers.index(col_name) + 1
        row_values = self._api_call(ws.row_values, cell.row)
        current_count = 0
        if col_idx <= len(row_values):
            try:
                current_count = int(row_values[col_idx - 1])
            except (ValueError, IndexError):
                current_count = 0

        col_letter = chr(ord("A") + col_idx - 1)
        batch_data = [
            {"range": f"{col_letter}{cell.row}", "values": [[str(current_count + 1)]]},
        ]
        # Update last_contact too
        lc_idx = headers.index("last_contact") + 1
        lc_letter = chr(ord("A") + lc_idx - 1)
        batch_data.append(
            {"range": f"{lc_letter}{cell.row}", "values": [[_now_iso()]]}
        )
        self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")
        logger.info(f"Logged referral {direction} for partner {partner_id}")

    # ------------------------------------------------------------------
    # Campaign Tracking
    # ------------------------------------------------------------------

    def create_campaign(self, campaign_data: dict) -> str:
        """Register a new campaign. Returns campaign_id."""
        ws = self._get_worksheet("Campaigns")
        headers = TAB_DEFINITIONS["Campaigns"]

        campaign_id = _generate_id()
        row = []
        for col in headers:
            if col == "campaign_id":
                row.append(campaign_id)
            elif col == "start_date":
                row.append(campaign_data.get("start_date", _today_iso()))
            elif col == "status":
                row.append(campaign_data.get("status", "draft"))
            elif col in ("total_leads", "sent", "delivered", "opened",
                         "replied", "interested", "scheduled", "closed"):
                row.append(campaign_data.get(col, "0"))
            elif col == "cost":
                row.append(campaign_data.get("cost", "0"))
            else:
                row.append(campaign_data.get(col, ""))

        self._api_call(ws.append_row, row, value_input_option="USER_ENTERED")
        logger.info(f"Created campaign {campaign_id}: {campaign_data.get('name', '')}")
        return campaign_id

    def update_campaign_stats(self, campaign_id: str, stats: dict) -> None:
        """Update campaign metrics (sent, delivered, opened, etc.)."""
        ws = self._get_worksheet("Campaigns")
        headers = TAB_DEFINITIONS["Campaigns"]

        cell = self._api_call(ws.find, campaign_id)
        if not cell:
            logger.warning(f"Campaign {campaign_id} not found")
            return

        batch_data = []
        for field, value in stats.items():
            if field in headers:
                col_idx = headers.index(field) + 1
                col_letter = chr(ord("A") + col_idx - 1)
                batch_data.append({
                    "range": f"{col_letter}{cell.row}",
                    "values": [[str(value)]],
                })

        if batch_data:
            self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")
            logger.info(f"Updated campaign {campaign_id} stats: {list(stats.keys())}")

    def get_campaign(self, campaign_id: str) -> dict:
        """Get campaign details."""
        ws = self._get_worksheet("Campaigns")
        headers = TAB_DEFINITIONS["Campaigns"]

        cell = self._api_call(ws.find, campaign_id)
        if not cell:
            logger.warning(f"Campaign {campaign_id} not found")
            return {}

        row_values = self._api_call(ws.row_values, cell.row)
        row_values = row_values + [""] * (len(headers) - len(row_values))
        return dict(zip(headers, row_values))

    # ------------------------------------------------------------------
    # Bulk Operations
    # ------------------------------------------------------------------

    def import_leads_from_csv(self, csv_path: str, source: str,
                              icp_type: str, market: str) -> dict:
        """Import leads from a CSV file (output of scrapers/clay).

        Maps CSV columns to CRM fields. Handles various column naming
        conventions from different scrapers.

        Returns: {imported: int, duplicates: int, errors: int}
        """
        # Column mapping: CSV column variations -> CRM field
        column_map = {
            "first_name": ["first_name", "firstname", "first", "fname"],
            "last_name": ["last_name", "lastname", "last", "lname"],
            "email": ["email", "email_address", "e-mail"],
            "phone": ["phone", "phone_number", "telephone", "tel", "mobile"],
            "address": ["address", "street", "street_address", "full_address"],
            "city": ["city"],
            "zip": ["zip", "zipcode", "zip_code", "postal_code", "postal"],
            "company": ["company", "company_name", "business", "business_name"],
            "notes": ["notes", "note", "comments"],
        }

        results = {"imported": 0, "duplicates": 0, "errors": 0}

        try:
            with open(csv_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                csv_headers = [h.strip().lower() for h in (reader.fieldnames or [])]

                # Build actual mapping from CSV columns to CRM fields
                field_lookup = {}
                for crm_field, variations in column_map.items():
                    for var in variations:
                        if var in csv_headers:
                            field_lookup[crm_field] = var
                            break

                for row_num, row in enumerate(reader, start=1):
                    try:
                        # Normalize keys to lowercase
                        row = {k.strip().lower(): v.strip() for k, v in row.items() if k}

                        lead_data = {
                            "source": source,
                            "icp_type": icp_type,
                            "market": market,
                            "pipeline": "referral_partner" if icp_type in (
                                "real_estate_agent", "property_manager"
                            ) else "direct_customer",
                        }

                        for crm_field, csv_col in field_lookup.items():
                            val = row.get(csv_col, "").strip()
                            if val:
                                lead_data[crm_field] = val

                        # Need at least email or phone
                        if not lead_data.get("email") and not lead_data.get("phone"):
                            logger.warning(f"Row {row_num}: No email or phone — skipping")
                            results["errors"] += 1
                            continue

                        # Check for duplicates by trying add_lead (it handles dedup)
                        ws = self._get_worksheet("Leads")
                        existing_records = self._api_call(ws.get_all_records)
                        is_dup = False
                        email = lead_data.get("email", "").lower()
                        phone = lead_data.get("phone", "")
                        for rec in existing_records:
                            rec_email = str(rec.get("email", "")).strip().lower()
                            rec_phone = str(rec.get("phone", "")).strip()
                            if (email and rec_email and email == rec_email) or \
                               (phone and rec_phone and phone == rec_phone):
                                is_dup = True
                                break

                        if is_dup:
                            results["duplicates"] += 1
                            # Still update existing via add_lead
                            self.add_lead(lead_data)
                        else:
                            self.add_lead(lead_data)
                            results["imported"] += 1

                    except Exception as e:
                        logger.error(f"Row {row_num}: Error importing — {e}")
                        results["errors"] += 1

        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_path}")
            results["errors"] += 1
        except Exception as e:
            logger.error(f"Error reading CSV: {e}")
            results["errors"] += 1

        logger.info(
            f"Import complete: {results['imported']} imported, "
            f"{results['duplicates']} duplicates, {results['errors']} errors"
        )
        return results

    def export_leads_to_csv(self, filters: dict = None,
                            output_path: str = "data/crm_export.csv") -> str:
        """Export filtered leads to CSV for use in campaigns."""
        leads = self.find_leads(filters or {})

        if not leads:
            logger.warning("No leads found matching filters — nothing to export")
            return ""

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        headers = TAB_DEFINITIONS["Leads"]
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()
            for lead in leads:
                # Ensure all keys are strings
                cleaned = {k: str(v) for k, v in lead.items()}
                writer.writerow(cleaned)

        logger.info(f"Exported {len(leads)} leads to {output_path}")
        return str(output)

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    def get_dashboard_summary(self) -> dict:
        """Compute summary metrics from Leads and Outreach Log tabs."""
        leads = self.find_leads({})
        ws_outreach = self._get_worksheet("Outreach Log")
        activities = self._api_call(ws_outreach.get_all_records)

        ws_partners = self._get_worksheet("Referral Partners")
        partners = self._api_call(ws_partners.get_all_records)

        summary = {
            "total_leads": len(leads),
            "by_status": {},
            "by_market": {},
            "by_channel": {},
            "active_referral_partners": 0,
        }

        for status in VALID_STATUSES:
            count = sum(1 for l in leads if str(l.get("status", "")).lower() == status)
            if count > 0:
                summary["by_status"][status] = count

        for market in VALID_MARKETS:
            count = sum(1 for l in leads if str(l.get("market", "")).lower() == market)
            if count > 0:
                summary["by_market"][market] = count

        for channel in VALID_CHANNELS:
            count = sum(1 for a in activities if str(a.get("channel", "")).lower() == channel)
            if count > 0:
                summary["by_channel"][channel] = count

        summary["active_referral_partners"] = sum(
            1 for p in partners if str(p.get("status", "")).lower() == "active"
        )

        return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Goldman's CRM — Google Sheets Lead Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--dry-run", action="store_true",
                        help="Use in-memory store instead of Google Sheets API")

    # Actions
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--init", action="store_true",
                       help="Initialize sheet tabs, headers, and formulas")
    group.add_argument("--add-lead", action="store_true",
                       help="Add a new lead")
    group.add_argument("--find", action="store_true",
                       help="Find leads matching filters")
    group.add_argument("--get-lead", metavar="LEAD_ID",
                       help="Get a lead by ID")
    group.add_argument("--update-status", nargs=2, metavar=("LEAD_ID", "STATUS"),
                       help="Update lead status")
    group.add_argument("--import", dest="import_csv", metavar="CSV_PATH",
                       help="Import leads from CSV file")
    group.add_argument("--export", action="store_true",
                       help="Export leads to CSV")
    group.add_argument("--dashboard", action="store_true",
                       help="Display dashboard summary")

    # Lead fields
    parser.add_argument("--first-name", help="Lead first name")
    parser.add_argument("--last-name", help="Lead last name")
    parser.add_argument("--email", help="Lead email")
    parser.add_argument("--phone", help="Lead phone (E.164)")
    parser.add_argument("--company", help="Lead company name")
    parser.add_argument("--address", help="Lead address")
    parser.add_argument("--city", help="Lead city")
    parser.add_argument("--zip", help="Lead zip code")
    parser.add_argument("--market", choices=VALID_MARKETS, help="Market")
    parser.add_argument("--icp", dest="icp_type", choices=VALID_ICP_TYPES,
                        help="ICP type")
    parser.add_argument("--pipeline", choices=VALID_PIPELINES, help="Pipeline")
    parser.add_argument("--status", choices=VALID_STATUSES, help="Lead status filter")
    parser.add_argument("--score", type=int, choices=range(1, 6), help="Lead quality score (1-5)")

    # Import fields
    parser.add_argument("--source", choices=VALID_SOURCES,
                        help="Lead source (for import)")

    # Export path
    parser.add_argument("--output", default="data/crm_export.csv",
                        help="Output path for export (default: data/crm_export.csv)")

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    mgr = SheetsManager(dry_run=args.dry_run)

    # Connect (or skip in dry-run)
    if not mgr.connect():
        logger.error("Failed to connect. Check credentials and spreadsheet ID.")
        sys.exit(1)

    # --- Init ---
    if args.init:
        mgr.initialize_sheets()
        print("CRM sheets initialized successfully.")
        return

    # In dry-run, initialize sheets so the in-memory store has tabs
    if args.dry_run:
        mgr.initialize_sheets()

    # --- Add Lead ---
    if args.add_lead:
        lead_data = {}
        for field in ["first_name", "last_name", "email", "phone", "company",
                       "address", "city", "zip", "market", "icp_type", "pipeline"]:
            val = getattr(args, field, None)
            if val:
                lead_data[field] = val
        if args.score:
            lead_data["score"] = str(args.score)

        if not lead_data.get("email") and not lead_data.get("phone"):
            print("ERROR: At least --email or --phone is required.")
            sys.exit(1)

        lead_id = mgr.add_lead(lead_data)
        print(f"Lead added: {lead_id}")
        return

    # --- Find Leads ---
    if args.find:
        filters = {}
        if args.market:
            filters["market"] = args.market
        if args.status:
            filters["status"] = args.status
        if args.icp_type:
            filters["icp_type"] = args.icp_type

        leads = mgr.find_leads(filters)
        if not leads:
            print("No leads found matching filters.")
        else:
            print(f"Found {len(leads)} leads:")
            for lead in leads:
                print(f"  {lead.get('lead_id', '?')}: "
                      f"{lead.get('first_name', '')} {lead.get('last_name', '')} | "
                      f"{lead.get('email', '')} | {lead.get('phone', '')} | "
                      f"status={lead.get('status', '')} | market={lead.get('market', '')}")
        return

    # --- Get Lead ---
    if args.get_lead:
        lead = mgr.get_lead(args.get_lead)
        if not lead:
            print(f"Lead {args.get_lead} not found.")
            sys.exit(1)
        print(json.dumps(lead, indent=2))
        return

    # --- Update Status ---
    if args.update_status:
        lead_id, new_status = args.update_status
        if mgr.update_lead_status(lead_id, new_status):
            print(f"Lead {lead_id} status updated to '{new_status}'.")
        else:
            print(f"Failed to update lead {lead_id}.")
            sys.exit(1)
        return

    # --- Import CSV ---
    if args.import_csv:
        if not args.source:
            print("ERROR: --source is required for import.")
            sys.exit(1)
        if not args.icp_type:
            print("ERROR: --icp is required for import.")
            sys.exit(1)
        if not args.market:
            print("ERROR: --market is required for import.")
            sys.exit(1)

        results = mgr.import_leads_from_csv(
            args.import_csv, args.source, args.icp_type, args.market,
        )
        print(f"Import results: {results['imported']} imported, "
              f"{results['duplicates']} duplicates, {results['errors']} errors")
        return

    # --- Export ---
    if args.export:
        filters = {}
        if args.market:
            filters["market"] = args.market
        if args.status:
            filters["status"] = args.status
        if args.icp_type:
            filters["icp_type"] = args.icp_type

        output_path = mgr.export_leads_to_csv(filters, args.output)
        if output_path:
            print(f"Exported to {output_path}")
        else:
            print("No leads to export.")
        return

    # --- Dashboard ---
    if args.dashboard:
        summary = mgr.get_dashboard_summary()
        print("\n=== Goldman's Garage Door Repair — Lead Gen Dashboard ===\n")
        print(f"Total Leads: {summary['total_leads']}")
        print("\nPIPELINE STATUS:")
        for status, count in summary.get("by_status", {}).items():
            print(f"  {status}: {count}")
        print("\nBY MARKET:")
        for market, count in summary.get("by_market", {}).items():
            print(f"  {market}: {count}")
        print("\nBY CHANNEL:")
        for channel, count in summary.get("by_channel", {}).items():
            print(f"  {channel}: {count}")
        print(f"\nActive Referral Partners: {summary['active_referral_partners']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
