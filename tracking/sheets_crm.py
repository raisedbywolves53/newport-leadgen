"""Government Contract Pipeline Tracker — Google Sheets CRM.

Tracks the full federal contracting lifecycle from opportunity identification
through bid/no-bid decision, proposal drafting, submission, and outcome.

Manages four tabs:
  - Opportunities: pipeline of solicitations with stage tracking + bid scores
  - Agencies: government buyer profiles and relationship tracking
  - Contacts: contracting officer / procurement point of contact database
  - Dashboard: computed pipeline summary and deadline alerts

Supports --dry-run mode with an in-memory sheet store for testing without
Google API credentials.

Usage:
    python tracking/sheets_crm.py --dry-run --init
    python tracking/sheets_crm.py --dry-run --add-opp --solicitation W51YHZ-24-R-0001 \\
        --title "Fresh Produce" --agency "DEPT OF DEFENSE" --state FL \\
        --naics 424480 --category military_dla --tier federal
    python tracking/sheets_crm.py --dry-run --update-stage OPP_ID qualifying
    python tracking/sheets_crm.py --dry-run --import-csv data/final/govt_opportunity_pipeline_*.csv
    python tracking/sheets_crm.py --dry-run --dashboard
    python tracking/sheets_crm.py --dry-run --deadlines --days-ahead 14
"""

import argparse
import csv
import json
import logging
import os
import sys
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# ── Logging ──────────────────────────────────────────────────────────────

LOG_DIR = _project_root / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("govcon_tracker")
logger.setLevel(logging.DEBUG)

_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))
logger.addHandler(_console)

_file_handler = logging.FileHandler(LOG_DIR / f"govcon_{datetime.now():%Y%m%d}.log")
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(_file_handler)

# ── Constants ────────────────────────────────────────────────────────────

VALID_STAGES = [
    "identified", "qualifying", "bid_decision", "capture",
    "drafting_proposal", "review", "submitted", "under_evaluation",
    "awarded", "lost", "no_bid", "cancelled",
]

VALID_BUYER_CATEGORIES = [
    "k12_school_meals", "corrections", "military_dla", "va_hospital",
    "fema_disaster", "county_general", "city_general", "university_dining",
    "food_bank_lfpa", "state_agency", "other",
]

VALID_GOV_TIERS = ["federal", "state", "county", "city"]

VALID_RELATIONSHIP_STATUSES = [
    "none", "identified", "introduced", "engaged", "active", "dormant",
]

TAB_DEFINITIONS = {
    "Opportunities": [
        "opp_id", "solicitation_number", "title", "source", "gov_tier",
        "buyer_category", "agency", "state", "naics_code", "contract_size_est",
        "annual_value_est", "set_aside", "posted_date", "response_deadline",
        "days_until_deadline", "stage", "bid_score", "incumbent",
        "competition_level", "evaluation_criteria", "proposal_status",
        "outcome", "win_loss_notes", "contract_value_actual",
        "contract_start", "contract_end", "notes", "first_seen", "last_updated",
    ],
    "Agencies": [
        "agency_id", "agency_name", "tier", "state", "portal_url",
        "registration_status", "key_contact", "annual_food_spend",
        "current_vendor", "contract_expiration", "notes",
    ],
    "Contacts": [
        "contact_id", "name", "title", "agency", "email", "phone",
        "role", "source", "last_contact", "relationship_status", "notes",
    ],
    "Dashboard": [],
}

DASHBOARD_LAYOUT = {
    (1, 1): "Newport GovCon Command Center",
    (3, 1): "Last Updated:",
    (3, 2): "",
    (5, 1): "PIPELINE BY STAGE",
    (6, 1): "Identified:",
    (6, 2): '=COUNTIF(Opportunities!P2:P,"identified")',
    (7, 1): "Qualifying:",
    (7, 2): '=COUNTIF(Opportunities!P2:P,"qualifying")',
    (8, 1): "Bid Decision:",
    (8, 2): '=COUNTIF(Opportunities!P2:P,"bid_decision")',
    (9, 1): "Capture:",
    (9, 2): '=COUNTIF(Opportunities!P2:P,"capture")',
    (10, 1): "Drafting Proposal:",
    (10, 2): '=COUNTIF(Opportunities!P2:P,"drafting_proposal")',
    (11, 1): "Review:",
    (11, 2): '=COUNTIF(Opportunities!P2:P,"review")',
    (12, 1): "Submitted:",
    (12, 2): '=COUNTIF(Opportunities!P2:P,"submitted")',
    (13, 1): "Under Evaluation:",
    (13, 2): '=COUNTIF(Opportunities!P2:P,"under_evaluation")',
    (14, 1): "Awarded:",
    (14, 2): '=COUNTIF(Opportunities!P2:P,"awarded")',
    (15, 1): "Lost:",
    (15, 2): '=COUNTIF(Opportunities!P2:P,"lost")',
    (16, 1): "No-Bid:",
    (16, 2): '=COUNTIF(Opportunities!P2:P,"no_bid")',
    (18, 1): "PIPELINE VALUE",
    (19, 1): "Total Est. Value:",
    (19, 2): '=SUMPRODUCT((Opportunities!P2:P<>"awarded")*(Opportunities!P2:P<>"lost")*(Opportunities!P2:P<>"no_bid")*(Opportunities!P2:P<>"cancelled")*Opportunities!J2:J)',
    (20, 1): "Awarded Value:",
    (20, 2): '=SUMPRODUCT((Opportunities!P2:P="awarded")*Opportunities!X2:X)',
    (22, 1): "BY BUYER CATEGORY",
    (23, 1): "K-12 School Meals:",
    (23, 2): '=COUNTIF(Opportunities!F2:F,"k12_school_meals")',
    (24, 1): "Corrections:",
    (24, 2): '=COUNTIF(Opportunities!F2:F,"corrections")',
    (25, 1): "Military/DLA:",
    (25, 2): '=COUNTIF(Opportunities!F2:F,"military_dla")',
    (26, 1): "VA Hospital:",
    (26, 2): '=COUNTIF(Opportunities!F2:F,"va_hospital")',
    (27, 1): "FEMA Disaster:",
    (27, 2): '=COUNTIF(Opportunities!F2:F,"fema_disaster")',
    (29, 1): "BY STATE (Top)",
    (30, 1): "FL:",
    (30, 2): '=COUNTIF(Opportunities!H2:H,"FL")',
    (31, 1): "GA:",
    (31, 2): '=COUNTIF(Opportunities!H2:H,"GA")',
    (32, 1): "AL:",
    (32, 2): '=COUNTIF(Opportunities!H2:H,"AL")',
    (33, 1): "SC:",
    (33, 2): '=COUNTIF(Opportunities!H2:H,"SC")',
    (34, 1): "NC:",
    (34, 2): '=COUNTIF(Opportunities!H2:H,"NC")',
    (36, 1): "DEADLINES",
    (37, 1): "This Week:",
    (37, 2): '=COUNTIFS(Opportunities!O2:O,">="&TODAY(),Opportunities!O2:O,"<="&TODAY()+7)',
    (38, 1): "This Month:",
    (38, 2): '=COUNTIFS(Opportunities!O2:O,">="&TODAY(),Opportunities!O2:O,"<="&TODAY()+30)',
    (40, 1): "TRACKING",
    (41, 1): "Tracked Agencies:",
    (41, 2): '=COUNTA(Agencies!A2:A)',
    (42, 1): "Tracked Contacts:",
    (42, 2): '=COUNTA(Contacts!A2:A)',
}


# ── Helpers ──────────────────────────────────────────────────────────────

def _generate_id() -> str:
    return uuid.uuid4().hex[:8]


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _today_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d")


# ── Rate limiter ─────────────────────────────────────────────────────────

class _RateLimiter:
    def __init__(self, min_interval: float = 0.5):
        self.min_interval = min_interval
        self._last_call = 0.0

    def wait(self):
        elapsed = time.time() - self._last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_call = time.time()


# ── In-memory sheet store (dry-run) ──────────────────────────────────────

class _DryRunSheet:
    def __init__(self, title: str, headers: list[str] | None = None):
        self.title = title
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
        self._rows.append([str(v) for v in values])

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
        if end_index is None:
            end_index = start_index
        del self._rows[start_index - 1 : end_index]


class _DryRunSpreadsheet:
    def __init__(self):
        self._sheets: dict[str, _DryRunSheet] = {}

    def worksheets(self) -> list:
        return [type("WS", (), {"title": t})() for t in self._sheets]

    def worksheet(self, title: str) -> _DryRunSheet:
        if title not in self._sheets:
            raise Exception(f"Worksheet '{title}' not found")
        return self._sheets[title]

    def add_worksheet(self, title: str, rows: int = 1000, cols: int = 26) -> _DryRunSheet:
        ws = _DryRunSheet(title)
        self._sheets[title] = ws
        return ws


# ── GovCon Pipeline Tracker ──────────────────────────────────────────────

class GovConPipelineTracker:
    """Google Sheets pipeline tracker for government contract opportunities."""

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

    # ── Connection ───────────────────────────────────────────────────────

    def connect(self) -> bool:
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
                import google.auth
                import google.auth.transport.requests
                creds, _ = google.auth.default(scopes=scopes)
                creds.refresh(google.auth.transport.requests.Request())
                self.client = gspread.authorize(creds)
                logger.info("Authenticated via Application Default Credentials")
            else:
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
        return self._api_call(self.spreadsheet.worksheet, tab_name)

    # ── Sheet Initialization ─────────────────────────────────────────────

    def initialize_sheets(self) -> None:
        existing = [ws.title for ws in self.spreadsheet.worksheets()]
        logger.info(f"Existing tabs: {existing}")

        for tab_name, headers in TAB_DEFINITIONS.items():
            if tab_name == "Dashboard":
                continue
            if tab_name in existing:
                logger.info(f"Tab '{tab_name}' already exists — skipping")
                continue

            logger.info(f"Creating tab '{tab_name}' with {len(headers)} columns")
            ws = self._api_call(
                self.spreadsheet.add_worksheet,
                title=tab_name, rows=1000, cols=max(len(headers), 20),
            )
            self._api_call(ws.append_row, headers, value_input_option="RAW")

        if "Dashboard" not in existing:
            logger.info("Creating Dashboard tab with formulas")
            ws = self._api_call(
                self.spreadsheet.add_worksheet,
                title="Dashboard", rows=50, cols=5,
            )
        else:
            ws = self._get_worksheet("Dashboard")
            logger.info("Dashboard tab exists — updating formulas")

        batch_data = []
        for (row, col), value in DASHBOARD_LAYOUT.items():
            col_letter = chr(ord("A") + col - 1)
            cell_ref = f"{col_letter}{row}"
            batch_data.append({"range": cell_ref, "values": [[value]]})

        batch_data.append({"range": "B3", "values": [["=NOW()"]]})

        self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")

        if "Sheet1" in existing:
            try:
                sheet1 = self._get_worksheet("Sheet1")
                if not self.dry_run:
                    self._api_call(self.spreadsheet.del_worksheet, sheet1)
                    logger.info("Deleted default 'Sheet1' tab")
            except Exception:
                pass

        logger.info("Sheet initialization complete")

    # ── Opportunity Management ───────────────────────────────────────────

    def add_opportunity(self, opp_data: dict) -> str:
        """Add a new opportunity. Deduplicates by solicitation_number.

        Returns opp_id (new or existing).
        """
        ws = self._get_worksheet("Opportunities")
        headers = TAB_DEFINITIONS["Opportunities"]

        sol_num = opp_data.get("solicitation_number", "").strip()

        # Check for duplicates
        if sol_num:
            existing_records = self._api_call(ws.get_all_records)
            for record in existing_records:
                if str(record.get("solicitation_number", "")).strip() == sol_num:
                    existing_id = str(record.get("opp_id", ""))
                    logger.info(f"Duplicate solicitation {sol_num} (opp_id={existing_id}), updating")
                    updates = {k: v for k, v in opp_data.items() if v}
                    updates["last_updated"] = _now_iso()
                    self.update_opportunity(existing_id, updates)
                    return existing_id

        opp_id = f"OPP_{_generate_id()}"
        row = []
        for col in headers:
            if col == "opp_id":
                row.append(opp_id)
            elif col == "stage":
                row.append(opp_data.get("stage", "identified"))
            elif col == "first_seen":
                row.append(opp_data.get("first_seen", _today_iso()))
            elif col == "last_updated":
                row.append(_now_iso())
            else:
                row.append(opp_data.get(col, ""))

        self._api_call(ws.append_row, row, value_input_option="USER_ENTERED")
        logger.info(f"Added opportunity {opp_id}: {opp_data.get('title', '')[:50]}")
        return opp_id

    def update_opportunity(self, opp_id: str, updates: dict) -> bool:
        """Update specific fields on an opportunity."""
        ws = self._get_worksheet("Opportunities")
        headers = TAB_DEFINITIONS["Opportunities"]

        cell = self._api_call(ws.find, opp_id)
        if not cell:
            logger.warning(f"Opportunity {opp_id} not found")
            return False

        row_num = cell.row
        batch_data = []
        for field, value in updates.items():
            if field in headers:
                col_idx = headers.index(field) + 1
                col_letter = _col_letter(col_idx)
                batch_data.append({
                    "range": f"{col_letter}{row_num}",
                    "values": [[str(value)]],
                })

        # Always update last_updated
        if "last_updated" not in updates:
            col_idx = headers.index("last_updated") + 1
            col_letter = _col_letter(col_idx)
            batch_data.append({
                "range": f"{col_letter}{row_num}",
                "values": [[_now_iso()]],
            })

        if batch_data:
            self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")
            logger.info(f"Updated opportunity {opp_id}: {list(updates.keys())}")
            return True
        return False

    def update_stage(self, opp_id: str, new_stage: str) -> bool:
        """Update opportunity stage with validation."""
        if new_stage not in VALID_STAGES:
            logger.error(f"Invalid stage '{new_stage}'. Valid: {VALID_STAGES}")
            return False
        return self.update_opportunity(opp_id, {"stage": new_stage})

    def get_opportunity(self, opp_id: str) -> dict:
        """Get a single opportunity by ID."""
        ws = self._get_worksheet("Opportunities")
        headers = TAB_DEFINITIONS["Opportunities"]

        cell = self._api_call(ws.find, opp_id)
        if not cell:
            logger.warning(f"Opportunity {opp_id} not found")
            return {}

        row_values = self._api_call(ws.row_values, cell.row)
        row_values = row_values + [""] * (len(headers) - len(row_values))
        return dict(zip(headers, row_values))

    def find_opportunities(self, filters: dict) -> list[dict]:
        """Find opportunities matching filters (stage, state, category, etc.)."""
        ws = self._get_worksheet("Opportunities")
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

        logger.info(f"Found {len(results)} opportunities matching {filters}")
        return results

    def import_from_sam_pipeline(self, csv_path: str) -> dict:
        """Import opportunities from a contract_scanner CSV.

        Maps SAM.gov pipeline CSV fields to tracker schema.
        Returns {imported, duplicates, errors}.
        """
        results = {"imported": 0, "duplicates": 0, "errors": 0}

        try:
            with open(csv_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, start=1):
                    try:
                        row = {k.strip(): v.strip() for k, v in row.items() if k}
                        opp_data = _map_sam_fields(row)
                        opp_data["source"] = "sam_pipeline_csv"

                        # Check for duplicate
                        sol_num = opp_data.get("solicitation_number", "")
                        ws = self._get_worksheet("Opportunities")
                        existing = self._api_call(ws.get_all_records)
                        is_dup = any(
                            str(r.get("solicitation_number", "")).strip() == sol_num
                            for r in existing
                            if sol_num
                        )

                        if is_dup:
                            results["duplicates"] += 1
                        else:
                            self.add_opportunity(opp_data)
                            results["imported"] += 1

                    except Exception as e:
                        logger.error(f"Row {row_num}: Error importing — {e}")
                        results["errors"] += 1

        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_path}")
            results["errors"] += 1

        logger.info(
            f"Import complete: {results['imported']} imported, "
            f"{results['duplicates']} duplicates, {results['errors']} errors"
        )
        return results

    def import_from_opportunity_dicts(self, opps: list[dict], source: str = "api") -> dict:
        """Import opportunities from a list of flat dicts (API integration).

        This is the integration point for daily_monitor.py.
        Returns {imported, duplicates, errors}.
        """
        results = {"imported": 0, "duplicates": 0, "errors": 0}

        for opp in opps:
            try:
                opp_data = _map_sam_fields(opp)
                opp_data["source"] = source

                sol_num = opp_data.get("solicitation_number", "")
                ws = self._get_worksheet("Opportunities")
                existing = self._api_call(ws.get_all_records)
                is_dup = any(
                    str(r.get("solicitation_number", "")).strip() == sol_num
                    for r in existing
                    if sol_num
                )

                if is_dup:
                    results["duplicates"] += 1
                else:
                    self.add_opportunity(opp_data)
                    results["imported"] += 1

            except Exception as e:
                logger.error(f"Error importing opportunity: {e}")
                results["errors"] += 1

        logger.info(
            f"Dict import: {results['imported']} imported, "
            f"{results['duplicates']} duplicates, {results['errors']} errors"
        )
        return results

    # ── Agency Management ────────────────────────────────────────────────

    def add_agency(self, agency_data: dict) -> str:
        """Add a new agency. Deduplicates by agency_name. Returns agency_id."""
        ws = self._get_worksheet("Agencies")
        headers = TAB_DEFINITIONS["Agencies"]

        name = agency_data.get("agency_name", "").strip()
        if name:
            existing = self._api_call(ws.get_all_records)
            for rec in existing:
                if str(rec.get("agency_name", "")).strip().lower() == name.lower():
                    existing_id = str(rec.get("agency_id", ""))
                    logger.info(f"Duplicate agency '{name}' (id={existing_id})")
                    return existing_id

        agency_id = f"AGY_{_generate_id()}"
        row = []
        for col in headers:
            if col == "agency_id":
                row.append(agency_id)
            else:
                row.append(agency_data.get(col, ""))

        self._api_call(ws.append_row, row, value_input_option="USER_ENTERED")
        logger.info(f"Added agency {agency_id}: {name}")
        return agency_id

    def update_agency(self, agency_id: str, updates: dict) -> bool:
        """Update agency fields."""
        ws = self._get_worksheet("Agencies")
        headers = TAB_DEFINITIONS["Agencies"]

        cell = self._api_call(ws.find, agency_id)
        if not cell:
            logger.warning(f"Agency {agency_id} not found")
            return False

        batch_data = []
        for field, value in updates.items():
            if field in headers:
                col_idx = headers.index(field) + 1
                col_letter = _col_letter(col_idx)
                batch_data.append({
                    "range": f"{col_letter}{cell.row}",
                    "values": [[str(value)]],
                })

        if batch_data:
            self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")
            logger.info(f"Updated agency {agency_id}: {list(updates.keys())}")
            return True
        return False

    def find_agencies(self, filters: dict) -> list[dict]:
        """Find agencies matching filters."""
        ws = self._get_worksheet("Agencies")
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
        return results

    # ── Contact Management ───────────────────────────────────────────────

    def add_contact(self, contact_data: dict) -> str:
        """Add a new contact. Deduplicates by email. Returns contact_id."""
        ws = self._get_worksheet("Contacts")
        headers = TAB_DEFINITIONS["Contacts"]

        email = contact_data.get("email", "").strip().lower()
        if email:
            existing = self._api_call(ws.get_all_records)
            for rec in existing:
                if str(rec.get("email", "")).strip().lower() == email:
                    existing_id = str(rec.get("contact_id", ""))
                    logger.info(f"Duplicate contact email '{email}' (id={existing_id})")
                    return existing_id

        contact_id = f"CON_{_generate_id()}"
        row = []
        for col in headers:
            if col == "contact_id":
                row.append(contact_id)
            elif col == "last_contact":
                row.append(contact_data.get("last_contact", ""))
            elif col == "relationship_status":
                row.append(contact_data.get("relationship_status", "none"))
            else:
                row.append(contact_data.get(col, ""))

        self._api_call(ws.append_row, row, value_input_option="USER_ENTERED")
        logger.info(f"Added contact {contact_id}: {contact_data.get('name', '')}")
        return contact_id

    def update_contact(self, contact_id: str, updates: dict) -> bool:
        """Update contact fields."""
        ws = self._get_worksheet("Contacts")
        headers = TAB_DEFINITIONS["Contacts"]

        cell = self._api_call(ws.find, contact_id)
        if not cell:
            logger.warning(f"Contact {contact_id} not found")
            return False

        batch_data = []
        for field, value in updates.items():
            if field in headers:
                col_idx = headers.index(field) + 1
                col_letter = _col_letter(col_idx)
                batch_data.append({
                    "range": f"{col_letter}{cell.row}",
                    "values": [[str(value)]],
                })

        if batch_data:
            self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")
            logger.info(f"Updated contact {contact_id}: {list(updates.keys())}")
            return True
        return False

    def find_contacts(self, filters: dict) -> list[dict]:
        """Find contacts matching filters."""
        ws = self._get_worksheet("Contacts")
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
        return results

    # ── Analytics ────────────────────────────────────────────────────────

    def get_pipeline_summary(self) -> dict:
        """Compute pipeline summary metrics from all tabs."""
        opps = self.find_opportunities({})
        agencies = self.find_agencies({})
        contacts = self.find_contacts({})

        summary = {
            "total_opportunities": len(opps),
            "by_stage": {},
            "by_buyer_category": {},
            "by_state": {},
            "pipeline_value": 0.0,
            "awarded_value": 0.0,
            "tracked_agencies": len(agencies),
            "tracked_contacts": len(contacts),
        }

        active_stages = {"identified", "qualifying", "bid_decision", "capture",
                         "drafting_proposal", "review", "submitted", "under_evaluation"}

        for stage in VALID_STAGES:
            count = sum(1 for o in opps if str(o.get("stage", "")).lower() == stage)
            if count > 0:
                summary["by_stage"][stage] = count

        for category in VALID_BUYER_CATEGORIES:
            count = sum(1 for o in opps if str(o.get("buyer_category", "")).lower() == category)
            if count > 0:
                summary["by_buyer_category"][category] = count

        # State distribution
        state_counts = {}
        for o in opps:
            st = str(o.get("state", "")).strip().upper()
            if st:
                state_counts[st] = state_counts.get(st, 0) + 1
        summary["by_state"] = dict(sorted(state_counts.items(), key=lambda x: -x[1])[:10])

        # Pipeline value (active stages only)
        for o in opps:
            stage = str(o.get("stage", "")).lower()
            if stage in active_stages:
                try:
                    val = float(o.get("contract_size_est", 0) or 0)
                    summary["pipeline_value"] += val
                except (ValueError, TypeError):
                    pass
            if stage == "awarded":
                try:
                    val = float(o.get("contract_value_actual", 0) or 0)
                    summary["awarded_value"] += val
                except (ValueError, TypeError):
                    pass

        return summary

    def get_deadline_report(self, days_ahead: int = 14) -> list[dict]:
        """Get opportunities with deadlines in the next N days."""
        opps = self.find_opportunities({})
        today = datetime.now()
        cutoff = today + timedelta(days=days_ahead)

        upcoming = []
        for opp in opps:
            deadline_str = str(opp.get("response_deadline", "")).strip()
            if not deadline_str:
                continue
            try:
                # Try multiple date formats
                deadline = None
                for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"]:
                    try:
                        deadline = datetime.strptime(deadline_str[:19], fmt)
                        break
                    except ValueError:
                        continue
                if deadline and today <= deadline <= cutoff:
                    opp["_days_until"] = (deadline - today).days
                    upcoming.append(opp)
            except (ValueError, TypeError):
                continue

        upcoming.sort(key=lambda x: x.get("_days_until", 999))
        return upcoming

    # ── Bulk Operations ──────────────────────────────────────────────────

    def export_pipeline_csv(self, output_path: str = "") -> str:
        """Export all opportunities to CSV."""
        opps = self.find_opportunities({})
        if not opps:
            logger.warning("No opportunities to export")
            return ""

        if not output_path:
            from scrapers.contract_scanner import FINAL_DIR
            FINAL_DIR.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d_%H%M")
            output_path = str(FINAL_DIR / f"govcon_pipeline_export_{date_str}.csv")

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        headers = TAB_DEFINITIONS["Opportunities"]
        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
            writer.writeheader()
            for opp in opps:
                writer.writerow({k: str(v) for k, v in opp.items()})

        logger.info(f"Exported {len(opps)} opportunities to {output_path}")
        return str(output)

    def refresh_days_until_deadline(self) -> int:
        """Recalculate days_until_deadline for all opportunities."""
        ws = self._get_worksheet("Opportunities")
        headers = TAB_DEFINITIONS["Opportunities"]
        records = self._api_call(ws.get_all_records)

        today = datetime.now()
        deadline_col = headers.index("response_deadline") + 1
        days_col = headers.index("days_until_deadline") + 1
        days_col_letter = _col_letter(days_col)

        updated = 0
        batch_data = []
        for i, record in enumerate(records):
            row_num = i + 2  # 1-indexed, skip header
            deadline_str = str(record.get("response_deadline", "")).strip()
            if not deadline_str:
                continue
            try:
                deadline = None
                for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%Y-%m-%dT%H:%M:%S"]:
                    try:
                        deadline = datetime.strptime(deadline_str[:19], fmt)
                        break
                    except ValueError:
                        continue
                if deadline:
                    days = (deadline - today).days
                    batch_data.append({
                        "range": f"{days_col_letter}{row_num}",
                        "values": [[str(days)]],
                    })
                    updated += 1
            except (ValueError, TypeError):
                continue

        if batch_data:
            self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")

        logger.info(f"Refreshed days_until_deadline for {updated} opportunities")
        return updated


# ── Field mapping helper ─────────────────────────────────────────────────

def _map_sam_fields(row: dict) -> dict:
    """Map SAM.gov / contract_scanner CSV fields to tracker schema."""
    return {
        "solicitation_number": row.get("solicitation_number", ""),
        "title": row.get("title", ""),
        "agency": row.get("agency", row.get("fullParentPathName", "")),
        "state": row.get("pop_state", row.get("office", "")),
        "naics_code": row.get("naics_code", ""),
        "set_aside": row.get("set_aside", row.get("set_aside_description", "")),
        "posted_date": row.get("posted_date", ""),
        "response_deadline": row.get("response_deadline", ""),
        "days_until_deadline": row.get("days_until_deadline", ""),
        "bid_score": row.get("bid_score", ""),
        "gov_tier": "federal",
        "buyer_category": _infer_buyer_category(row),
        "competition_level": row.get("competition_level", ""),
    }


def _infer_buyer_category(row: dict) -> str:
    """Attempt to infer buyer_category from agency name."""
    agency = (row.get("agency", "") or "").lower()
    if any(kw in agency for kw in ["defense", "army", "navy", "air force", "dla", "marine"]):
        return "military_dla"
    if any(kw in agency for kw in ["veterans", "va "]):
        return "va_hospital"
    if any(kw in agency for kw in ["fema", "emergency"]):
        return "fema_disaster"
    if any(kw in agency for kw in ["justice", "prisons", "corrections", "bop"]):
        return "corrections"
    if any(kw in agency for kw in ["education", "school"]):
        return "k12_school_meals"
    if any(kw in agency for kw in ["agriculture", "usda"]):
        return "food_bank_lfpa"
    return "other"


def _col_letter(col_idx: int) -> str:
    """Convert 1-based column index to letter(s). Supports AA, AB, etc."""
    result = ""
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result


# ── CLI ──────────────────────────────────────────────────────────────────

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Newport GovCon Pipeline Tracker — Google Sheets CRM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--dry-run", action="store_true",
                        help="Use in-memory store instead of Google Sheets API")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--init", action="store_true",
                       help="Initialize sheet tabs, headers, and dashboard formulas")
    group.add_argument("--add-opp", action="store_true",
                       help="Add a new opportunity")
    group.add_argument("--update-stage", nargs=2, metavar=("OPP_ID", "STAGE"),
                       help="Update opportunity stage")
    group.add_argument("--get-opp", metavar="OPP_ID",
                       help="Get opportunity details by ID")
    group.add_argument("--find-opps", action="store_true",
                       help="Find opportunities matching filters")
    group.add_argument("--import-csv", metavar="CSV_PATH",
                       help="Import opportunities from contract_scanner CSV")
    group.add_argument("--add-agency", action="store_true",
                       help="Add a new agency")
    group.add_argument("--add-contact", action="store_true",
                       help="Add a new contact")
    group.add_argument("--dashboard", action="store_true",
                       help="Display pipeline summary dashboard")
    group.add_argument("--deadlines", action="store_true",
                       help="Show upcoming deadlines")
    group.add_argument("--export", action="store_true",
                       help="Export pipeline to CSV")

    # Opportunity fields
    parser.add_argument("--solicitation", help="Solicitation number")
    parser.add_argument("--title", help="Opportunity title")
    parser.add_argument("--agency", help="Agency name")
    parser.add_argument("--state", help="State code (e.g., FL)")
    parser.add_argument("--naics", dest="naics_code", help="NAICS code")
    parser.add_argument("--category", dest="buyer_category",
                        choices=VALID_BUYER_CATEGORIES, help="Buyer category")
    parser.add_argument("--tier", dest="gov_tier",
                        choices=VALID_GOV_TIERS, help="Government tier")
    parser.add_argument("--stage", choices=VALID_STAGES, help="Pipeline stage filter")
    parser.add_argument("--size", dest="contract_size_est", help="Estimated contract size")

    # Agency fields
    parser.add_argument("--agency-name", help="Agency name (for --add-agency)")
    parser.add_argument("--portal-url", help="Agency procurement portal URL")

    # Contact fields
    parser.add_argument("--name", help="Contact name")
    parser.add_argument("--contact-title", help="Contact job title")
    parser.add_argument("--email", help="Contact email")
    parser.add_argument("--phone", help="Contact phone")

    # Deadline report
    parser.add_argument("--days-ahead", type=int, default=14,
                        help="Days ahead for deadline report (default: 14)")

    # Export
    parser.add_argument("--output", default="",
                        help="Output path for export")

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    tracker = GovConPipelineTracker(dry_run=args.dry_run)

    if not tracker.connect():
        logger.error("Failed to connect. Check credentials and spreadsheet ID.")
        sys.exit(1)

    # --- Init ---
    if args.init:
        tracker.initialize_sheets()
        print("GovCon pipeline tracker initialized successfully.")
        if not args.dashboard:
            return

    # In dry-run, always initialize so in-memory store has tabs
    if args.dry_run and not args.init:
        tracker.initialize_sheets()

    # --- Add Opportunity ---
    if args.add_opp:
        opp_data = {}
        for field in ["solicitation", "title", "agency", "state", "naics_code",
                       "buyer_category", "gov_tier", "contract_size_est"]:
            cli_field = field
            if field == "solicitation":
                cli_field = "solicitation"
                field = "solicitation_number"
            val = getattr(args, cli_field, None) if cli_field != "solicitation" else args.solicitation
            if val:
                opp_data[field] = val

        if not opp_data.get("solicitation_number") and not opp_data.get("title"):
            print("ERROR: At least --solicitation or --title is required.")
            sys.exit(1)

        opp_id = tracker.add_opportunity(opp_data)
        print(f"Opportunity added: {opp_id}")
        return

    # --- Update Stage ---
    if args.update_stage:
        opp_id, new_stage = args.update_stage
        if tracker.update_stage(opp_id, new_stage):
            print(f"Opportunity {opp_id} stage updated to '{new_stage}'.")
        else:
            print(f"Failed to update opportunity {opp_id}.")
            sys.exit(1)
        return

    # --- Get Opportunity ---
    if args.get_opp:
        opp = tracker.get_opportunity(args.get_opp)
        if not opp:
            print(f"Opportunity {args.get_opp} not found.")
            sys.exit(1)
        print(json.dumps(opp, indent=2))
        return

    # --- Find Opportunities ---
    if args.find_opps:
        filters = {}
        if args.stage:
            filters["stage"] = args.stage
        if args.state:
            filters["state"] = args.state
        if args.buyer_category:
            filters["buyer_category"] = args.buyer_category

        opps = tracker.find_opportunities(filters)
        if not opps:
            print("No opportunities found matching filters.")
        else:
            print(f"Found {len(opps)} opportunities:")
            for opp in opps:
                print(f"  {opp.get('opp_id', '?')}: "
                      f"{(opp.get('title') or '?')[:50]} | "
                      f"{opp.get('agency', '')[:30]} | "
                      f"stage={opp.get('stage', '')} | "
                      f"state={opp.get('state', '')}")
        return

    # --- Import CSV ---
    if args.import_csv:
        results = tracker.import_from_sam_pipeline(args.import_csv)
        print(f"Import results: {results['imported']} imported, "
              f"{results['duplicates']} duplicates, {results['errors']} errors")
        return

    # --- Add Agency ---
    if args.add_agency:
        agency_data = {}
        if args.agency_name:
            agency_data["agency_name"] = args.agency_name
        if args.tier:
            agency_data["tier"] = args.tier if hasattr(args, "tier") and args.tier else ""
        if args.state:
            agency_data["state"] = args.state
        if args.portal_url:
            agency_data["portal_url"] = args.portal_url

        if not agency_data.get("agency_name"):
            print("ERROR: --agency-name is required for --add-agency.")
            sys.exit(1)

        agency_id = tracker.add_agency(agency_data)
        print(f"Agency added: {agency_id}")
        return

    # --- Add Contact ---
    if args.add_contact:
        contact_data = {}
        if args.name:
            contact_data["name"] = args.name
        if args.contact_title:
            contact_data["title"] = args.contact_title
        if args.agency:
            contact_data["agency"] = args.agency
        if args.email:
            contact_data["email"] = args.email
        if args.phone:
            contact_data["phone"] = args.phone

        if not contact_data.get("name"):
            print("ERROR: --name is required for --add-contact.")
            sys.exit(1)

        contact_id = tracker.add_contact(contact_data)
        print(f"Contact added: {contact_id}")
        return

    # --- Dashboard ---
    if args.dashboard:
        summary = tracker.get_pipeline_summary()
        print(f"\n{'='*60}")
        print(f"  Newport GovCon Command Center")
        print(f"{'='*60}")
        print(f"\n  Total Opportunities: {summary['total_opportunities']}")
        print(f"  Pipeline Value: ${summary['pipeline_value']:,.0f}")
        print(f"  Awarded Value: ${summary['awarded_value']:,.0f}")

        print(f"\n  PIPELINE BY STAGE:")
        for stage, count in summary.get("by_stage", {}).items():
            print(f"    {stage:25s} {count}")

        print(f"\n  BY BUYER CATEGORY:")
        for cat, count in summary.get("by_buyer_category", {}).items():
            print(f"    {cat:25s} {count}")

        if summary.get("by_state"):
            print(f"\n  BY STATE:")
            for state, count in summary["by_state"].items():
                print(f"    {state:5s} {count}")

        print(f"\n  Tracked Agencies: {summary['tracked_agencies']}")
        print(f"  Tracked Contacts: {summary['tracked_contacts']}")

        # Deadline preview
        upcoming = tracker.get_deadline_report(days_ahead=14)
        if upcoming:
            print(f"\n  DEADLINES (next 14 days): {len(upcoming)}")
            for opp in upcoming[:5]:
                days = opp.get("_days_until", "?")
                title = (opp.get("title") or "?")[:40]
                print(f"    {days:>3} days | {title}")

        return

    # --- Deadlines ---
    if args.deadlines:
        upcoming = tracker.get_deadline_report(days_ahead=args.days_ahead)
        if not upcoming:
            print(f"No deadlines in the next {args.days_ahead} days.")
            return

        print(f"\n{'='*60}")
        print(f"  Upcoming Deadlines ({args.days_ahead} days)")
        print(f"{'='*60}")
        for opp in upcoming:
            days = opp.get("_days_until", "?")
            title = (opp.get("title") or "?")[:45]
            sol = opp.get("solicitation_number", "")
            agency = (opp.get("agency") or "")[:30]
            stage = opp.get("stage", "")
            print(f"  {days:>3} days | {title}")
            print(f"          {sol} | {agency} | stage={stage}")
        return

    # --- Export ---
    if args.export:
        output_path = tracker.export_pipeline_csv(args.output)
        if output_path:
            print(f"Exported to {output_path}")
        else:
            print("No opportunities to export.")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
