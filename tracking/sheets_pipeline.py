"""GovCon Pipeline — Google Sheets Pipeline Tracker (Phase 2).

Manages the government contract opportunity lifecycle through a Google Sheets
backend with three tabs:

  - Pipeline: Main opportunity tracking (23 columns) with 12 lifecycle stages,
    bid/no-bid scoring, buyer categories, and deadline management.
  - Agencies: Relationship tracker (13 columns) with contact info, relationship
    status, and win/bid/opportunity counts from Pipeline data.
  - Dashboard: Auto-calculated summary views — stage counts, category breakdowns,
    win rate, active pipeline value, upcoming deadlines, monthly activity.

Supports --dry-run mode with an in-memory sheet store for testing without
Google API credentials.

Usage:
    python tracking/sheets_pipeline.py --dry-run --init
    python tracking/sheets_pipeline.py --dry-run --add-opp --title "Fresh Produce" \\
        --agency "DEPT OF DEFENSE" --state FL --naics 424480 \\
        --category "Military/DoD" --tier Federal
    python tracking/sheets_pipeline.py --dry-run --update-stage OPP_ID "Qualifying"
    python tracking/sheets_pipeline.py --dry-run --import-csv data/final/govt_opportunity_pipeline_*.csv
    python tracking/sheets_pipeline.py --dry-run --dashboard
    python tracking/sheets_pipeline.py --dry-run --deadlines --days-ahead 14
    python tracking/sheets_pipeline.py --dry-run --score OPP_ID
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

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

LOG_DIR = _project_root / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("govcon_pipeline")
logger.setLevel(logging.DEBUG)

_console = logging.StreamHandler()
_console.setLevel(logging.INFO)
_console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))
logger.addHandler(_console)

_file_handler = logging.FileHandler(LOG_DIR / f"pipeline_{datetime.now():%Y%m%d}.log")
_file_handler.setLevel(logging.DEBUG)
_file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(_file_handler)

# ---------------------------------------------------------------------------
# Constants — Phase 2 Schema
# ---------------------------------------------------------------------------

VALID_STAGES = [
    "Identified", "Qualifying", "Bid Decision", "Capture",
    "Drafting Proposal", "Internal Review", "Submitted", "Under Evaluation",
    "Awarded", "Lost", "No-Bid", "Cancelled",
]

TERMINAL_STAGES = {"Awarded", "Lost", "No-Bid", "Cancelled"}

VALID_BUYER_CATEGORIES = [
    "School District", "Corrections", "Military/DoD", "FEMA/Emergency",
    "VA/Healthcare", "University/College", "State Agency", "County/Municipal",
    "Federal Civilian", "Food Bank/Nonprofit",
]

VALID_TIERS = ["Federal", "State", "Local", "Education"]

VALID_OUTCOMES = ["Pending", "Won", "Lost", "No-Bid", "Cancelled"]

VALID_SOURCES = ["SAM.gov", "MFMP", "BidSync", "HigherGov", "GovSpend", "Manual"]

VALID_RELATIONSHIP_STATUSES = ["Cold", "Warm", "Active", "Past Winner"]

# --- Sheet 1: Pipeline (23 columns A-W) ---

PIPELINE_HEADERS = [
    "Opportunity ID",        # A — auto-generated or SAM.gov notice ID
    "Title",                 # B
    "Agency",                # C
    "Buyer Category",        # D — dropdown
    "Tier",                  # E — dropdown
    "NAICS Code",            # F
    "Contract Value",        # G — currency
    "State",                 # H
    "Stage",                 # I — dropdown (12 stages)
    "Bid/No-Bid Score",      # J — number 0-100
    "Recommendation",        # K — Strong Bid / Bid / Review / No-Bid
    "Source",                # L
    "Response Deadline",     # M — date
    "Days Until Deadline",   # N — formula =M[row]-TODAY()
    "Award Date",            # O — date
    "Outcome",               # P — dropdown
    "Contract Number",       # Q
    "Contracting Officer",   # R
    "CO Email",              # S
    "Notes",                 # T
    "Date Added",            # U — auto
    "Last Updated",          # V — auto
    "Solicitation URL",      # W — URL
]

# --- Sheet 2: Agencies (13 columns A-M) ---

AGENCIES_HEADERS = [
    "Agency Name",           # A
    "Buyer Category",        # B
    "Tier",                  # C
    "State",                 # D
    "Primary Contact",       # E
    "Contact Email",         # F
    "Contact Phone",         # G
    "Relationship Status",   # H — dropdown
    "Last Contact Date",     # I
    "Total Opportunities",   # J — count from Pipeline
    "Total Bids",            # K — count from Pipeline
    "Total Wins",            # L — count from Pipeline
    "Notes",                 # M
]

# --- Sheet 3: Dashboard layout ---

DASHBOARD_LAYOUT = {
    (1, 1): "Newport GovCon Command Center",
    (2, 1): "Last Updated:",
    (2, 2): "=NOW()",

    (4, 1): "OPPORTUNITIES BY STAGE",
    (5, 1): "Identified:",
    (5, 2): '=COUNTIF(Pipeline!I2:I,"Identified")',
    (6, 1): "Qualifying:",
    (6, 2): '=COUNTIF(Pipeline!I2:I,"Qualifying")',
    (7, 1): "Bid Decision:",
    (7, 2): '=COUNTIF(Pipeline!I2:I,"Bid Decision")',
    (8, 1): "Capture:",
    (8, 2): '=COUNTIF(Pipeline!I2:I,"Capture")',
    (9, 1): "Drafting Proposal:",
    (9, 2): '=COUNTIF(Pipeline!I2:I,"Drafting Proposal")',
    (10, 1): "Internal Review:",
    (10, 2): '=COUNTIF(Pipeline!I2:I,"Internal Review")',
    (11, 1): "Submitted:",
    (11, 2): '=COUNTIF(Pipeline!I2:I,"Submitted")',
    (12, 1): "Under Evaluation:",
    (12, 2): '=COUNTIF(Pipeline!I2:I,"Under Evaluation")',
    (13, 1): "Awarded:",
    (13, 2): '=COUNTIF(Pipeline!I2:I,"Awarded")',
    (14, 1): "Lost:",
    (14, 2): '=COUNTIF(Pipeline!I2:I,"Lost")',
    (15, 1): "No-Bid:",
    (15, 2): '=COUNTIF(Pipeline!I2:I,"No-Bid")',
    (16, 1): "Cancelled:",
    (16, 2): '=COUNTIF(Pipeline!I2:I,"Cancelled")',

    (18, 1): "OPPORTUNITIES BY BUYER CATEGORY",
    (19, 1): "School District:",
    (19, 2): '=COUNTIF(Pipeline!D2:D,"School District")',
    (19, 3): '=SUMPRODUCT((Pipeline!D2:D="School District")*Pipeline!G2:G)',
    (20, 1): "Corrections:",
    (20, 2): '=COUNTIF(Pipeline!D2:D,"Corrections")',
    (20, 3): '=SUMPRODUCT((Pipeline!D2:D="Corrections")*Pipeline!G2:G)',
    (21, 1): "Military/DoD:",
    (21, 2): '=COUNTIF(Pipeline!D2:D,"Military/DoD")',
    (21, 3): '=SUMPRODUCT((Pipeline!D2:D="Military/DoD")*Pipeline!G2:G)',
    (22, 1): "FEMA/Emergency:",
    (22, 2): '=COUNTIF(Pipeline!D2:D,"FEMA/Emergency")',
    (22, 3): '=SUMPRODUCT((Pipeline!D2:D="FEMA/Emergency")*Pipeline!G2:G)',
    (23, 1): "VA/Healthcare:",
    (23, 2): '=COUNTIF(Pipeline!D2:D,"VA/Healthcare")',
    (23, 3): '=SUMPRODUCT((Pipeline!D2:D="VA/Healthcare")*Pipeline!G2:G)',
    (24, 1): "University/College:",
    (24, 2): '=COUNTIF(Pipeline!D2:D,"University/College")',
    (24, 3): '=SUMPRODUCT((Pipeline!D2:D="University/College")*Pipeline!G2:G)',
    (25, 1): "State Agency:",
    (25, 2): '=COUNTIF(Pipeline!D2:D,"State Agency")',
    (25, 3): '=SUMPRODUCT((Pipeline!D2:D="State Agency")*Pipeline!G2:G)',
    (26, 1): "County/Municipal:",
    (26, 2): '=COUNTIF(Pipeline!D2:D,"County/Municipal")',
    (26, 3): '=SUMPRODUCT((Pipeline!D2:D="County/Municipal")*Pipeline!G2:G)',
    (27, 1): "Federal Civilian:",
    (27, 2): '=COUNTIF(Pipeline!D2:D,"Federal Civilian")',
    (27, 3): '=SUMPRODUCT((Pipeline!D2:D="Federal Civilian")*Pipeline!G2:G)',
    (28, 1): "Food Bank/Nonprofit:",
    (28, 2): '=COUNTIF(Pipeline!D2:D,"Food Bank/Nonprofit")',
    (28, 3): '=SUMPRODUCT((Pipeline!D2:D="Food Bank/Nonprofit")*Pipeline!G2:G)',

    (30, 1): "WIN RATE",
    (31, 1): "Win Rate:",
    (31, 2): '=IFERROR(COUNTIF(Pipeline!I2:I,"Awarded")/(COUNTIF(Pipeline!I2:I,"Awarded")+COUNTIF(Pipeline!I2:I,"Lost")),0)',

    (33, 1): "ACTIVE PIPELINE VALUE",
    (34, 1): "Active Value:",
    (34, 2): '=SUMPRODUCT((Pipeline!I2:I<>"Awarded")*(Pipeline!I2:I<>"Lost")*(Pipeline!I2:I<>"No-Bid")*(Pipeline!I2:I<>"Cancelled")*Pipeline!G2:G)',
    (35, 1): "Awarded Value:",
    (35, 2): '=SUMPRODUCT((Pipeline!I2:I="Awarded")*Pipeline!G2:G)',

    (37, 1): "UPCOMING DEADLINES (Next 14 Days)",
    (38, 1): "This Week:",
    (38, 2): '=COUNTIFS(Pipeline!M2:M,">="&TODAY(),Pipeline!M2:M,"<="&TODAY()+7)',
    (39, 1): "Next 14 Days:",
    (39, 2): '=COUNTIFS(Pipeline!M2:M,">="&TODAY(),Pipeline!M2:M,"<="&TODAY()+14)',

    (41, 1): "MONTHLY ACTIVITY",
    (42, 1): "Added This Month:",
    (42, 2): '=COUNTIFS(Pipeline!U2:U,">="&TEXT(EOMONTH(TODAY(),-1)+1,"YYYY-MM-DD"),Pipeline!U2:U,"<="&TEXT(TODAY(),"YYYY-MM-DD"))',
    (43, 1): "Updated This Month:",
    (43, 2): '=COUNTIFS(Pipeline!V2:V,">="&TEXT(EOMONTH(TODAY(),-1)+1,"YYYY-MM-DD"),Pipeline!V2:V,"<="&TEXT(TODAY(),"YYYY-MM-DD"))',

    (45, 1): "TRACKING",
    (46, 1): "Tracked Agencies:",
    (46, 2): '=COUNTA(Agencies!A2:A)',
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _generate_id() -> str:
    """Generate a short unique ID."""
    return uuid.uuid4().hex[:8]


def _now_iso() -> str:
    """Current datetime as ISO string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _today_iso() -> str:
    """Current date as ISO string."""
    return datetime.now().strftime("%Y-%m-%d")


def _col_letter(col_idx: int) -> str:
    """Convert 1-based column index to letter(s). Supports AA, AB, etc."""
    result = ""
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result


def _normalize_stage(stage: str) -> str | None:
    """Case-insensitive match to a valid stage name. Returns None if no match."""
    lookup = {s.lower().replace(" ", "").replace("-", "").replace("_", ""): s for s in VALID_STAGES}
    normalized = stage.strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    return lookup.get(normalized)


def _normalize_category(cat: str) -> str | None:
    """Case-insensitive match to a valid buyer category. Returns None if no match."""
    lookup = {c.lower().replace(" ", "").replace("/", "").replace("-", ""): c for c in VALID_BUYER_CATEGORIES}
    normalized = cat.strip().lower().replace(" ", "").replace("/", "").replace("-", "")
    return lookup.get(normalized)


def _normalize_tier(tier: str) -> str | None:
    """Case-insensitive match to a valid tier. Returns None if no match."""
    lookup = {t.lower(): t for t in VALID_TIERS}
    return lookup.get(tier.strip().lower())


def _map_sam_fields(row: dict) -> dict:
    """Map SAM.gov / contract_scanner CSV fields to Phase 2 Pipeline schema."""
    # Extract solicitation number for dedup (stored as Opportunity ID if present)
    sol_num = (
        row.get("solicitation_number", "")
        or row.get("notice_id", "")
        or ""
    ).strip()

    # Title
    title = row.get("title", "").strip()

    # Agency
    agency = (
        row.get("agency", "")
        or row.get("fullParentPathName", "")
        or row.get("department_name", "")
        or ""
    ).strip()

    # State
    state = (
        row.get("pop_state", "")
        or row.get("state", "")
        or row.get("place_of_performance_state", "")
        or ""
    ).strip().upper()

    # NAICS
    naics = (
        row.get("naics_code", "")
        or row.get("naicsCode", "")
        or row.get("naics", "")
        or ""
    ).strip()

    # Contract value
    contract_value = (
        row.get("award_amount", "")
        or row.get("contract_value", "")
        or row.get("contract_size_est", "")
        or row.get("estimated_value", "")
        or ""
    )

    # Set-aside / competition info
    set_aside = (
        row.get("set_aside", "")
        or row.get("set_aside_description", "")
        or ""
    ).strip()

    # Dates
    response_deadline = (
        row.get("response_deadline", "")
        or row.get("responseDeadLine", "")
        or row.get("close_date", "")
        or ""
    ).strip()
    posted_date = row.get("posted_date", "").strip()

    # Bid score (may come pre-scored from contract_scanner --score)
    bid_score = row.get("bid_score", "")
    bid_decision = row.get("bid_decision", "")

    # URL
    sol_url = row.get("uiLink", row.get("solicitation_url", row.get("url", ""))).strip() if row.get("uiLink") or row.get("solicitation_url") or row.get("url") else ""

    # Source
    source = row.get("source", "SAM.gov").strip()

    return {
        "Opportunity ID": sol_num,
        "Title": title,
        "Agency": agency,
        "Buyer Category": _infer_buyer_category(row),
        "Tier": "Federal",
        "NAICS Code": naics,
        "Contract Value": str(contract_value).strip(),
        "State": state,
        "Stage": "Identified",
        "Bid/No-Bid Score": str(bid_score).strip(),
        "Recommendation": str(bid_decision).strip(),
        "Source": source,
        "Response Deadline": response_deadline,
        "Days Until Deadline": "",
        "Award Date": "",
        "Outcome": "Pending",
        "Contract Number": "",
        "Contracting Officer": "",
        "CO Email": "",
        "Notes": f"Set-aside: {set_aside}" if set_aside else "",
        "Date Added": _today_iso(),
        "Last Updated": _now_iso(),
        "Solicitation URL": sol_url,
    }


def _infer_buyer_category(row: dict) -> str:
    """Attempt to infer buyer category from agency name and other fields."""
    agency = (row.get("agency", "") or row.get("Agency", "") or "").lower()
    title = (row.get("title", "") or row.get("Title", "") or "").lower()
    combined = f"{agency} {title}"

    if any(kw in combined for kw in ["defense", "army", "navy", "air force", "dla", "marine", "dod"]):
        return "Military/DoD"
    if any(kw in combined for kw in ["veterans", "va "]):
        return "VA/Healthcare"
    if any(kw in combined for kw in ["fema", "emergency"]):
        return "FEMA/Emergency"
    if any(kw in combined for kw in ["justice", "prisons", "corrections", "bop", "correctional"]):
        return "Corrections"
    if any(kw in combined for kw in ["school", "k-12", "k12", "education dept"]):
        return "School District"
    if any(kw in combined for kw in ["university", "college"]):
        return "University/College"
    if any(kw in combined for kw in ["agriculture", "usda", "food bank", "lfpa"]):
        return "Food Bank/Nonprofit"
    if any(kw in combined for kw in ["county", "municipal", "city of"]):
        return "County/Municipal"
    if any(kw in combined for kw in ["state of", "state dept", "state agency"]):
        return "State Agency"
    return "Federal Civilian"


# ---------------------------------------------------------------------------
# Rate Limiter
# ---------------------------------------------------------------------------

class _RateLimiter:
    """Simple rate limiter for Google Sheets API calls."""

    def __init__(self, min_interval: float = 0.5):
        self.min_interval = min_interval
        self._last_call = 0.0

    def wait(self):
        elapsed = time.time() - self._last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_call = time.time()


# ---------------------------------------------------------------------------
# In-memory sheet store (dry-run mode)
# ---------------------------------------------------------------------------

class _DryRunSheet:
    """In-memory worksheet that mimics the gspread Worksheet interface."""

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
    """In-memory spreadsheet that mimics gspread Spreadsheet interface."""

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


# ---------------------------------------------------------------------------
# GovConPipeline — Main class
# ---------------------------------------------------------------------------

class GovConPipeline:
    """Google Sheets pipeline tracker for government contract opportunities.

    Manages three tabs: Pipeline (23 cols), Agencies (13 cols), Dashboard.
    Supports Google Sheets API or in-memory dry-run mode.
    """

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.creds_file = os.getenv(
            "GOOGLE_SHEETS_CREDENTIALS_PATH",
            os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json"),
        )
        self.spreadsheet_id = os.getenv("GOOGLE_SHEETS_ID")
        self.client = None
        self.spreadsheet = None
        self._rate_limiter = _RateLimiter(min_interval=0.5)

        if dry_run:
            logger.info("DRY-RUN mode -- using in-memory sheet store")
            self.spreadsheet = _DryRunSpreadsheet()

    # ---- Connection -------------------------------------------------------

    def connect(self) -> bool:
        """Authenticate and connect to Google Sheets."""
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
            logger.error("Credentials file not found: %s", self.creds_file)
            return False
        except Exception as e:
            logger.error("Failed to connect to Google Sheets: %s", e)
            return False

    def _api_call(self, func, *args, **kwargs):
        """Execute a Google Sheets API call with retry and rate limiting."""
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
                    logger.warning(
                        "Rate limited, retrying in %ds (attempt %d/%d)",
                        wait_time, attempt + 1, max_retries,
                    )
                    time.sleep(wait_time)
                elif attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(
                        "API error: %s, retrying in %ds (attempt %d/%d)",
                        e, wait_time, attempt + 1, max_retries,
                    )
                    time.sleep(wait_time)
                else:
                    raise

    def _get_worksheet(self, tab_name: str):
        """Get a worksheet by name."""
        return self._api_call(self.spreadsheet.worksheet, tab_name)

    # ---- Sheet Initialization (idempotent) --------------------------------

    def setup_sheets(self) -> None:
        """Create Pipeline, Agencies, Dashboard sheets with headers and formatting.

        Idempotent: skips existing tabs, updates Dashboard formulas on re-run.
        Applies data validation dropdowns and conditional formatting.
        """
        existing = [ws.title for ws in self.spreadsheet.worksheets()]
        logger.info("Existing tabs: %s", existing)

        # --- Pipeline tab ---
        if "Pipeline" not in existing:
            logger.info("Creating Pipeline tab with %d columns", len(PIPELINE_HEADERS))
            ws = self._api_call(
                self.spreadsheet.add_worksheet,
                title="Pipeline", rows=1000, cols=len(PIPELINE_HEADERS),
            )
            self._api_call(ws.append_row, PIPELINE_HEADERS, value_input_option="RAW")
            self._apply_pipeline_validation(ws)
            self._apply_pipeline_conditional_formatting(ws)
        else:
            logger.info("Tab 'Pipeline' already exists -- skipping creation")

        # --- Agencies tab ---
        if "Agencies" not in existing:
            logger.info("Creating Agencies tab with %d columns", len(AGENCIES_HEADERS))
            ws = self._api_call(
                self.spreadsheet.add_worksheet,
                title="Agencies", rows=500, cols=len(AGENCIES_HEADERS),
            )
            self._api_call(ws.append_row, AGENCIES_HEADERS, value_input_option="RAW")
            self._apply_agencies_validation(ws)
        else:
            logger.info("Tab 'Agencies' already exists -- skipping creation")

        # --- Dashboard tab ---
        if "Dashboard" not in existing:
            logger.info("Creating Dashboard tab with formulas")
            ws = self._api_call(
                self.spreadsheet.add_worksheet,
                title="Dashboard", rows=50, cols=5,
            )
        else:
            ws = self._get_worksheet("Dashboard")
            logger.info("Dashboard tab exists -- updating formulas")

        batch_data = []
        for (row, col), value in DASHBOARD_LAYOUT.items():
            col_l = _col_letter(col)
            cell_ref = f"{col_l}{row}"
            batch_data.append({"range": cell_ref, "values": [[value]]})

        self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")

        # --- Remove default Sheet1 if present ---
        if "Sheet1" in existing:
            try:
                sheet1 = self._get_worksheet("Sheet1")
                if not self.dry_run:
                    self._api_call(self.spreadsheet.del_worksheet, sheet1)
                    logger.info("Deleted default 'Sheet1' tab")
            except Exception:
                pass

        logger.info("Sheet initialization complete")

    def _apply_pipeline_validation(self, ws) -> None:
        """Apply data validation (dropdowns) to Pipeline sheet.

        Applies dropdowns for Buyer Category (D), Tier (E), Stage (I),
        Outcome (P), and Source (L).

        Note: gspread data validation requires gspread >= 5.x. In dry-run
        mode this is a no-op.
        """
        if self.dry_run:
            logger.info("[DRY-RUN] Skipping data validation (dropdowns)")
            return

        try:
            from gspread_formatting import (
                DataValidationRule,
                BooleanCondition,
                set_data_validation_for_cell_range,
            )

            validations = {
                "D2:D1000": VALID_BUYER_CATEGORIES,
                "E2:E1000": VALID_TIERS,
                "I2:I1000": VALID_STAGES,
                "P2:P1000": VALID_OUTCOMES,
                "L2:L1000": VALID_SOURCES,
            }

            for cell_range, options in validations.items():
                rule = DataValidationRule(
                    BooleanCondition("ONE_OF_LIST", options),
                    showCustomUi=True,
                )
                set_data_validation_for_cell_range(ws, cell_range, rule)
                logger.info("Applied dropdown validation to %s", cell_range)

        except ImportError:
            logger.warning(
                "gspread-formatting not installed; skipping data validation. "
                "Install with: pip install gspread-formatting"
            )
        except Exception as e:
            logger.warning("Failed to apply data validation: %s", e)

    def _apply_pipeline_conditional_formatting(self, ws) -> None:
        """Apply conditional formatting for deadline coloring.

        Red for deadlines <7 days, Yellow for <14 days, Green for >14 days.
        Applied to column N (Days Until Deadline).

        Note: requires gspread_formatting. In dry-run mode this is a no-op.
        """
        if self.dry_run:
            logger.info("[DRY-RUN] Skipping conditional formatting")
            return

        try:
            from gspread_formatting import (
                CellFormat,
                Color,
                ConditionalFormatRule,
                BooleanCondition,
                GridRange,
                get_conditional_format_rules,
                set_frozen,
            )
            from gspread_formatting.conditionals import (
                BooleanRule,
            )

            # Freeze header row
            try:
                set_frozen(ws, rows=1)
            except Exception:
                pass

            # Days Until Deadline is column N = 14 (0-indexed: 13)
            rules = get_conditional_format_rules(ws)

            # Red: <7 days
            rules.append(ConditionalFormatRule(
                ranges=[GridRange.from_a1_range("N2:N1000", ws)],
                booleanRule=BooleanRule(
                    condition=BooleanCondition("NUMBER_LESS", ["7"]),
                    format=CellFormat(backgroundColor=Color(0.92, 0.6, 0.6)),
                ),
            ))

            # Yellow: 7-14 days
            rules.append(ConditionalFormatRule(
                ranges=[GridRange.from_a1_range("N2:N1000", ws)],
                booleanRule=BooleanRule(
                    condition=BooleanCondition("NUMBER_BETWEEN", ["7", "14"]),
                    format=CellFormat(backgroundColor=Color(1.0, 0.95, 0.6)),
                ),
            ))

            # Green: >14 days
            rules.append(ConditionalFormatRule(
                ranges=[GridRange.from_a1_range("N2:N1000", ws)],
                booleanRule=BooleanRule(
                    condition=BooleanCondition("NUMBER_GREATER", ["14"]),
                    format=CellFormat(backgroundColor=Color(0.72, 0.88, 0.72)),
                ),
            ))

            rules.save()
            logger.info("Applied conditional formatting to Days Until Deadline column")

        except ImportError:
            logger.warning(
                "gspread-formatting not installed; skipping conditional formatting. "
                "Install with: pip install gspread-formatting"
            )
        except Exception as e:
            logger.warning("Failed to apply conditional formatting: %s", e)

    def _apply_agencies_validation(self, ws) -> None:
        """Apply data validation to Agencies sheet.

        Dropdowns for Buyer Category (B), Tier (C), Relationship Status (H).
        """
        if self.dry_run:
            logger.info("[DRY-RUN] Skipping Agencies data validation")
            return

        try:
            from gspread_formatting import (
                DataValidationRule,
                BooleanCondition,
                set_data_validation_for_cell_range,
            )

            validations = {
                "B2:B500": VALID_BUYER_CATEGORIES,
                "C2:C500": VALID_TIERS,
                "H2:H500": VALID_RELATIONSHIP_STATUSES,
            }

            for cell_range, options in validations.items():
                rule = DataValidationRule(
                    BooleanCondition("ONE_OF_LIST", options),
                    showCustomUi=True,
                )
                set_data_validation_for_cell_range(ws, cell_range, rule)

        except ImportError:
            logger.warning("gspread-formatting not installed; skipping Agencies validation")
        except Exception as e:
            logger.warning("Failed to apply Agencies validation: %s", e)

    # ---- Opportunity Management -------------------------------------------

    def add_opportunity(self, data: dict) -> str:
        """Add a new opportunity to Pipeline. Deduplicates by Opportunity ID.

        Auto-populates Date Added and Last Updated.

        Args:
            data: Dict with Pipeline column names as keys. At minimum provide
                  'Title' or 'Opportunity ID'.

        Returns:
            Opportunity ID (new or existing if duplicate).
        """
        ws = self._get_worksheet("Pipeline")

        # Determine the opportunity ID for dedup
        opp_id = data.get("Opportunity ID", "").strip()

        # Check for duplicates by Opportunity ID (solicitation number)
        if opp_id:
            existing_records = self._api_call(ws.get_all_records)
            for record in existing_records:
                if str(record.get("Opportunity ID", "")).strip() == opp_id:
                    logger.info(
                        "Duplicate Opportunity ID '%s' found, updating existing record", opp_id
                    )
                    updates = {k: v for k, v in data.items() if v}
                    updates["Last Updated"] = _now_iso()
                    self._update_row_by_opp_id(opp_id, updates)
                    return opp_id

        # Generate ID if not provided
        if not opp_id:
            opp_id = f"OPP_{_generate_id()}"
            data["Opportunity ID"] = opp_id

        # Build row in column order
        row = []
        for header in PIPELINE_HEADERS:
            if header == "Opportunity ID":
                row.append(opp_id)
            elif header == "Stage":
                val = data.get("Stage", "Identified")
                row.append(_normalize_stage(val) or "Identified")
            elif header == "Outcome":
                row.append(data.get("Outcome", "Pending"))
            elif header == "Date Added":
                row.append(data.get("Date Added", _today_iso()))
            elif header == "Last Updated":
                row.append(_now_iso())
            elif header == "Days Until Deadline":
                # Insert formula =M[row]-TODAY() — row number is determined after append
                row.append("")  # Placeholder; formula set after append
            else:
                row.append(data.get(header, ""))

        self._api_call(ws.append_row, row, value_input_option="USER_ENTERED")

        # Set the Days Until Deadline formula for the new row
        row_num = ws.row_count if hasattr(ws, '_rows') else None
        if row_num and row_num > 1:
            days_col_idx = PIPELINE_HEADERS.index("Days Until Deadline") + 1
            days_col_letter = _col_letter(days_col_idx)
            deadline_col_letter = _col_letter(PIPELINE_HEADERS.index("Response Deadline") + 1)
            formula = f'=IF({deadline_col_letter}{row_num}="","",{deadline_col_letter}{row_num}-TODAY())'
            self._api_call(
                ws.update_cell, row_num, days_col_idx, formula
            )

        logger.info("Added opportunity %s: %s", opp_id, data.get("Title", "")[:50])
        return opp_id

    def _update_row_by_opp_id(self, opp_id: str, updates: dict) -> bool:
        """Update specific fields on a Pipeline row found by Opportunity ID."""
        ws = self._get_worksheet("Pipeline")
        cell = self._api_call(ws.find, opp_id)
        if not cell:
            logger.warning("Opportunity ID '%s' not found in Pipeline", opp_id)
            return False

        row_num = cell.row
        batch_data = []
        for field, value in updates.items():
            if field in PIPELINE_HEADERS:
                col_idx = PIPELINE_HEADERS.index(field) + 1
                col_l = _col_letter(col_idx)
                batch_data.append({
                    "range": f"{col_l}{row_num}",
                    "values": [[str(value)]],
                })

        # Always update Last Updated
        if "Last Updated" not in updates:
            col_idx = PIPELINE_HEADERS.index("Last Updated") + 1
            col_l = _col_letter(col_idx)
            batch_data.append({
                "range": f"{col_l}{row_num}",
                "values": [[_now_iso()]],
            })

        if batch_data:
            self._api_call(ws.batch_update, batch_data, value_input_option="USER_ENTERED")
            logger.info("Updated opportunity %s: %s", opp_id, list(updates.keys()))
            return True
        return False

    def update_stage(self, opp_id: str, new_stage: str) -> bool:
        """Move opportunity to a new stage with validation.

        Args:
            opp_id:    Opportunity ID to update.
            new_stage: New stage name (case-insensitive, flexible formatting).

        Returns:
            True if update succeeded, False otherwise.
        """
        normalized = _normalize_stage(new_stage)
        if not normalized:
            logger.error(
                "Invalid stage '%s'. Valid stages: %s", new_stage, VALID_STAGES
            )
            return False

        updates = {"Stage": normalized}

        # Auto-set Outcome based on terminal stages
        if normalized == "Awarded":
            updates["Outcome"] = "Won"
        elif normalized == "Lost":
            updates["Outcome"] = "Lost"
        elif normalized == "No-Bid":
            updates["Outcome"] = "No-Bid"
        elif normalized == "Cancelled":
            updates["Outcome"] = "Cancelled"

        return self._update_row_by_opp_id(opp_id, updates)

    def score_opportunity(self, opp_id: str, overrides: dict | None = None) -> dict | None:
        """Run bid/no-bid scorer on an opportunity and update columns J-K.

        Imports and runs scoring/bid_no_bid.BidNoBidScorer against the
        opportunity data, then writes the score and recommendation back
        to the Pipeline sheet.

        Args:
            opp_id:    Opportunity ID to score.
            overrides: Optional manual overrides for scoring factors.

        Returns:
            Score result dict, or None if opportunity not found.
        """
        ws = self._get_worksheet("Pipeline")
        cell = self._api_call(ws.find, opp_id)
        if not cell:
            logger.warning("Opportunity %s not found for scoring", opp_id)
            return None

        # Get opportunity data
        row_values = self._api_call(ws.row_values, cell.row)
        row_values = row_values + [""] * (len(PIPELINE_HEADERS) - len(row_values))
        opp_data = dict(zip(PIPELINE_HEADERS, row_values))

        # Map to scorer-compatible field names
        scorer_input = {
            "title": opp_data.get("Title", ""),
            "notice_id": opp_data.get("Opportunity ID", ""),
            "solicitation_number": opp_data.get("Opportunity ID", ""),
            "agency": opp_data.get("Agency", ""),
            "naics_code": opp_data.get("NAICS Code", ""),
            "pop_state": opp_data.get("State", ""),
            "award_amount": opp_data.get("Contract Value", ""),
            "response_deadline": opp_data.get("Response Deadline", ""),
            "set_aside": "",
        }

        try:
            from scoring.bid_no_bid import BidNoBidScorer
            scorer = BidNoBidScorer()
            result = scorer.score(scorer_input, overrides=overrides)
        except ImportError:
            logger.error(
                "Could not import scoring.bid_no_bid. Ensure scoring/bid_no_bid.py exists."
            )
            return None
        except Exception as e:
            logger.error("Scoring failed for %s: %s", opp_id, e)
            return None

        # Write score and recommendation back to Pipeline
        self._update_row_by_opp_id(opp_id, {
            "Bid/No-Bid Score": str(result["total_score"]),
            "Recommendation": result["recommendation"],
        })

        logger.info(
            "Scored %s: %.1f/100 (%s)",
            opp_id, result["total_score"], result["recommendation"],
        )
        return result

    def get_opportunity(self, opp_id: str) -> dict:
        """Get a single opportunity by Opportunity ID.

        Returns:
            Dict with Pipeline column names as keys, or empty dict if not found.
        """
        ws = self._get_worksheet("Pipeline")
        cell = self._api_call(ws.find, opp_id)
        if not cell:
            logger.warning("Opportunity %s not found", opp_id)
            return {}

        row_values = self._api_call(ws.row_values, cell.row)
        row_values = row_values + [""] * (len(PIPELINE_HEADERS) - len(row_values))
        return dict(zip(PIPELINE_HEADERS, row_values))

    def get_active_pipeline(self) -> list[dict]:
        """Return all opportunities not in terminal states.

        Terminal states: Awarded, Lost, No-Bid, Cancelled.

        Returns:
            List of opportunity dicts.
        """
        ws = self._get_worksheet("Pipeline")
        records = self._api_call(ws.get_all_records)
        return [
            r for r in records
            if r.get("Stage", "") not in TERMINAL_STAGES
        ]

    def get_upcoming_deadlines(self, days: int = 14) -> list[dict]:
        """Return opportunities with deadlines within N days.

        Args:
            days: Number of days ahead to check (default 14).

        Returns:
            List of opportunity dicts sorted by deadline (soonest first),
            each with an added '_days_until' key.
        """
        ws = self._get_worksheet("Pipeline")
        records = self._api_call(ws.get_all_records)
        today = datetime.now()
        cutoff = today + timedelta(days=days)

        upcoming = []
        for record in records:
            # Skip terminal stages
            if record.get("Stage", "") in TERMINAL_STAGES:
                continue

            deadline_str = str(record.get("Response Deadline", "")).strip()
            if not deadline_str:
                continue

            deadline = _parse_date(deadline_str)
            if deadline and today <= deadline <= cutoff:
                record["_days_until"] = (deadline - today).days
                upcoming.append(record)

        upcoming.sort(key=lambda x: x.get("_days_until", 999))
        return upcoming

    def get_dashboard_data(self) -> dict:
        """Return summary metrics for Dashboard sheet.

        Returns:
            Dict with keys: total_opportunities, by_stage, by_category,
            win_rate, active_pipeline_value, awarded_value, upcoming_deadlines,
            monthly_added, monthly_updated, tracked_agencies.
        """
        ws = self._get_worksheet("Pipeline")
        records = self._api_call(ws.get_all_records)

        summary = {
            "total_opportunities": len(records),
            "by_stage": {},
            "by_category": {},
            "by_state": {},
            "win_rate": 0.0,
            "active_pipeline_value": 0.0,
            "awarded_value": 0.0,
            "upcoming_deadlines_7d": 0,
            "upcoming_deadlines_14d": 0,
            "monthly_added": 0,
            "monthly_updated": 0,
            "tracked_agencies": 0,
        }

        today = datetime.now()
        month_start = today.replace(day=1).strftime("%Y-%m-%d")
        awarded_count = 0
        lost_count = 0

        for stage in VALID_STAGES:
            count = sum(1 for r in records if r.get("Stage", "") == stage)
            if count > 0:
                summary["by_stage"][stage] = count
            if stage == "Awarded":
                awarded_count = count
            if stage == "Lost":
                lost_count = count

        for category in VALID_BUYER_CATEGORIES:
            matching = [r for r in records if r.get("Buyer Category", "") == category]
            if matching:
                total_value = 0.0
                for r in matching:
                    try:
                        total_value += float(r.get("Contract Value", 0) or 0)
                    except (ValueError, TypeError):
                        pass
                summary["by_category"][category] = {
                    "count": len(matching),
                    "value": total_value,
                }

        # State distribution
        state_counts = {}
        for r in records:
            st = str(r.get("State", "")).strip().upper()
            if st:
                state_counts[st] = state_counts.get(st, 0) + 1
        summary["by_state"] = dict(sorted(state_counts.items(), key=lambda x: -x[1])[:10])

        # Win rate
        total_decided = awarded_count + lost_count
        if total_decided > 0:
            summary["win_rate"] = awarded_count / total_decided

        # Pipeline values
        for r in records:
            stage = r.get("Stage", "")
            try:
                val = float(r.get("Contract Value", 0) or 0)
            except (ValueError, TypeError):
                val = 0.0
            if stage not in TERMINAL_STAGES:
                summary["active_pipeline_value"] += val
            if stage == "Awarded":
                summary["awarded_value"] += val

        # Upcoming deadlines
        cutoff_7 = today + timedelta(days=7)
        cutoff_14 = today + timedelta(days=14)
        for r in records:
            if r.get("Stage", "") in TERMINAL_STAGES:
                continue
            deadline_str = str(r.get("Response Deadline", "")).strip()
            if not deadline_str:
                continue
            deadline = _parse_date(deadline_str)
            if deadline:
                if today <= deadline <= cutoff_7:
                    summary["upcoming_deadlines_7d"] += 1
                if today <= deadline <= cutoff_14:
                    summary["upcoming_deadlines_14d"] += 1

        # Monthly activity
        for r in records:
            added = str(r.get("Date Added", "")).strip()
            if added >= month_start:
                summary["monthly_added"] += 1
            updated = str(r.get("Last Updated", "")).strip()[:10]
            if updated >= month_start:
                summary["monthly_updated"] += 1

        # Tracked agencies
        try:
            agencies_ws = self._get_worksheet("Agencies")
            agency_records = self._api_call(agencies_ws.get_all_records)
            summary["tracked_agencies"] = len(agency_records)
        except Exception:
            summary["tracked_agencies"] = 0

        return summary

    def sync_agencies(self) -> dict:
        """Update Agencies sheet from Pipeline data.

        For each unique agency in Pipeline, upserts a row in Agencies with
        computed counts for Total Opportunities, Total Bids, and Total Wins.

        Returns:
            Dict with {added, updated} counts.
        """
        pipeline_ws = self._get_worksheet("Pipeline")
        pipeline_records = self._api_call(pipeline_ws.get_all_records)

        agencies_ws = self._get_worksheet("Agencies")
        existing_agencies = self._api_call(agencies_ws.get_all_records)
        existing_names = {
            str(r.get("Agency Name", "")).strip().lower(): i
            for i, r in enumerate(existing_agencies)
        }

        # Aggregate from pipeline
        agency_stats: dict[str, dict] = {}
        for r in pipeline_records:
            name = str(r.get("Agency", "")).strip()
            if not name:
                continue
            if name not in agency_stats:
                agency_stats[name] = {
                    "Agency Name": name,
                    "Buyer Category": r.get("Buyer Category", ""),
                    "Tier": r.get("Tier", ""),
                    "State": r.get("State", ""),
                    "Total Opportunities": 0,
                    "Total Bids": 0,
                    "Total Wins": 0,
                }
            agency_stats[name]["Total Opportunities"] += 1
            stage = r.get("Stage", "")
            bid_stages = {
                "Capture", "Drafting Proposal", "Internal Review",
                "Submitted", "Under Evaluation", "Awarded", "Lost",
            }
            if stage in bid_stages:
                agency_stats[name]["Total Bids"] += 1
            if stage == "Awarded":
                agency_stats[name]["Total Wins"] += 1

        results = {"added": 0, "updated": 0}

        for name, stats in agency_stats.items():
            name_lower = name.strip().lower()
            if name_lower in existing_names:
                # Update counts on existing row
                idx = existing_names[name_lower]
                row_num = idx + 2  # 1-indexed, skip header
                batch_data = []
                for field in ["Total Opportunities", "Total Bids", "Total Wins"]:
                    col_idx = AGENCIES_HEADERS.index(field) + 1
                    col_l = _col_letter(col_idx)
                    batch_data.append({
                        "range": f"{col_l}{row_num}",
                        "values": [[str(stats[field])]],
                    })
                if batch_data:
                    self._api_call(
                        agencies_ws.batch_update, batch_data,
                        value_input_option="USER_ENTERED",
                    )
                results["updated"] += 1
            else:
                # Add new agency row
                row = []
                for header in AGENCIES_HEADERS:
                    row.append(str(stats.get(header, "")))
                self._api_call(
                    agencies_ws.append_row, row,
                    value_input_option="USER_ENTERED",
                )
                results["added"] += 1

        logger.info(
            "Agency sync: %d added, %d updated", results["added"], results["updated"]
        )
        return results

    # ---- Import Methods ---------------------------------------------------

    def import_from_csv(self, csv_path: str) -> dict:
        """Import opportunities from a contract_scanner CSV.

        Maps SAM.gov pipeline CSV fields to Pipeline schema. Deduplicates
        by Opportunity ID (solicitation number).

        Args:
            csv_path: Path to CSV file.

        Returns:
            Dict with {imported, duplicates, errors}.
        """
        results = {"imported": 0, "duplicates": 0, "errors": 0}

        try:
            with open(csv_path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row_num, row in enumerate(reader, start=1):
                    try:
                        row = {k.strip(): v.strip() for k, v in row.items() if k}
                        opp_data = _map_sam_fields(row)

                        opp_id = opp_data.get("Opportunity ID", "")
                        if opp_id:
                            ws = self._get_worksheet("Pipeline")
                            existing = self._api_call(ws.get_all_records)
                            is_dup = any(
                                str(r.get("Opportunity ID", "")).strip() == opp_id
                                for r in existing
                            )
                            if is_dup:
                                results["duplicates"] += 1
                                continue

                        self.add_opportunity(opp_data)
                        results["imported"] += 1

                    except Exception as e:
                        logger.error("Row %d: import error -- %s", row_num, e)
                        results["errors"] += 1

        except FileNotFoundError:
            logger.error("CSV file not found: %s", csv_path)
            results["errors"] += 1

        logger.info(
            "CSV import complete: %d imported, %d duplicates, %d errors",
            results["imported"], results["duplicates"], results["errors"],
        )
        return results

    def import_from_dicts(self, opps: list[dict], source: str = "SAM.gov") -> dict:
        """Import opportunities from a list of flat dicts (API integration).

        This is the integration point for daily_monitor.py.

        Args:
            opps:   List of flat dicts with SAM.gov-style field names.
            source: Source label for the Source column.

        Returns:
            Dict with {imported, duplicates, errors}.
        """
        results = {"imported": 0, "duplicates": 0, "errors": 0}

        for opp in opps:
            try:
                opp_data = _map_sam_fields(opp)
                opp_data["Source"] = source

                opp_id = opp_data.get("Opportunity ID", "")
                if opp_id:
                    ws = self._get_worksheet("Pipeline")
                    existing = self._api_call(ws.get_all_records)
                    is_dup = any(
                        str(r.get("Opportunity ID", "")).strip() == opp_id
                        for r in existing
                    )
                    if is_dup:
                        results["duplicates"] += 1
                        continue

                self.add_opportunity(opp_data)
                results["imported"] += 1

            except Exception as e:
                logger.error("Dict import error: %s", e)
                results["errors"] += 1

        logger.info(
            "Dict import: %d imported, %d duplicates, %d errors",
            results["imported"], results["duplicates"], results["errors"],
        )
        return results

    # ---- Export ------------------------------------------------------------

    def export_pipeline_csv(self, output_path: str = "") -> str:
        """Export all Pipeline opportunities to CSV.

        Args:
            output_path: Destination path. If empty, auto-generates in data/final/.

        Returns:
            Output file path, or empty string if no data.
        """
        ws = self._get_worksheet("Pipeline")
        records = self._api_call(ws.get_all_records)

        if not records:
            logger.warning("No opportunities to export")
            return ""

        if not output_path:
            out_dir = _project_root / "data" / "final"
            out_dir.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d_%H%M")
            output_path = str(out_dir / f"govcon_pipeline_export_{date_str}.csv")

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=PIPELINE_HEADERS, extrasaction="ignore")
            writer.writeheader()
            for record in records:
                writer.writerow({k: str(v) for k, v in record.items()})

        logger.info("Exported %d opportunities to %s", len(records), output_path)
        return str(output)


# ---------------------------------------------------------------------------
# Date parsing helper
# ---------------------------------------------------------------------------

def _parse_date(date_str: str) -> datetime | None:
    """Parse a date string in common formats."""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%m/%d/%Y",
        "%m/%d/%y",
        "%m-%d-%Y",
        "%Y%m%d",
        "%d-%b-%Y",
    ]
    date_str = date_str.strip()
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, IndexError):
            continue
    return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Newport GovCon Pipeline Tracker -- Google Sheets Pipeline (Phase 2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  python tracking/sheets_pipeline.py --dry-run --init\n'
            '  python tracking/sheets_pipeline.py --dry-run --add-opp --title "Fresh Produce" '
            '--agency "DEPT OF DEFENSE" --state FL --naics 424480 '
            '--category "Military/DoD" --tier Federal\n'
            '  python tracking/sheets_pipeline.py --dry-run --update-stage OPP_ID "Qualifying"\n'
            '  python tracking/sheets_pipeline.py --dry-run --import-csv data/final/govt_opportunity_pipeline_*.csv\n'
            '  python tracking/sheets_pipeline.py --dry-run --dashboard\n'
            '  python tracking/sheets_pipeline.py --dry-run --deadlines --days-ahead 14\n'
            '  python tracking/sheets_pipeline.py --dry-run --score OPP_ID\n'
        ),
    )

    parser.add_argument("--dry-run", action="store_true",
                        help="Use in-memory store instead of Google Sheets API")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--init", action="store_true",
                       help="Initialize sheet tabs, headers, validation, and dashboard formulas")
    group.add_argument("--add-opp", action="store_true",
                       help="Add a new opportunity")
    group.add_argument("--update-stage", nargs=2, metavar=("OPP_ID", "STAGE"),
                       help="Update opportunity stage")
    group.add_argument("--import-csv", metavar="CSV_PATH",
                       help="Import opportunities from contract_scanner CSV")
    group.add_argument("--dashboard", action="store_true",
                       help="Display pipeline summary dashboard")
    group.add_argument("--deadlines", action="store_true",
                       help="Show upcoming deadlines")
    group.add_argument("--score", metavar="OPP_ID",
                       help="Run bid/no-bid scorer on an opportunity")
    group.add_argument("--sync-agencies", action="store_true",
                       help="Sync Agencies sheet from Pipeline data")
    group.add_argument("--active-pipeline", action="store_true",
                       help="Show active (non-terminal) pipeline")
    group.add_argument("--export", action="store_true",
                       help="Export pipeline to CSV")

    # Opportunity fields
    parser.add_argument("--title", help="Opportunity title")
    parser.add_argument("--agency", help="Agency name")
    parser.add_argument("--state", help="State code (e.g., FL)")
    parser.add_argument("--naics", help="NAICS code")
    parser.add_argument("--category", help="Buyer category")
    parser.add_argument("--tier", help="Government tier (Federal, State, Local, Education)")
    parser.add_argument("--source", help="Source (SAM.gov, MFMP, BidSync, etc.)")
    parser.add_argument("--value", help="Contract value (dollar amount)")
    parser.add_argument("--deadline", help="Response deadline (YYYY-MM-DD)")
    parser.add_argument("--solicitation", help="Solicitation number / Opportunity ID")
    parser.add_argument("--url", help="Solicitation URL")

    # Scoring overrides
    parser.add_argument("--overrides", default="{}",
                        help='JSON string of scoring overrides, e.g. \'{"past_performance": 100}\'')

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

    pipeline = GovConPipeline(dry_run=args.dry_run)

    if not pipeline.connect():
        logger.error("Failed to connect. Check credentials and spreadsheet ID.")
        sys.exit(1)

    # --- Init ---
    if args.init:
        pipeline.setup_sheets()
        print("GovCon pipeline tracker initialized successfully.")
        if not args.dashboard:
            return

    # In dry-run, always initialize so in-memory store has tabs
    if args.dry_run and not args.init:
        pipeline.setup_sheets()

    # --- Add Opportunity ---
    if args.add_opp:
        opp_data = {}
        if args.solicitation:
            opp_data["Opportunity ID"] = args.solicitation
        if args.title:
            opp_data["Title"] = args.title
        if args.agency:
            opp_data["Agency"] = args.agency
        if args.state:
            opp_data["State"] = args.state.upper()
        if args.naics:
            opp_data["NAICS Code"] = args.naics
        if args.category:
            normalized_cat = _normalize_category(args.category)
            if normalized_cat:
                opp_data["Buyer Category"] = normalized_cat
            else:
                opp_data["Buyer Category"] = args.category
        if args.tier:
            normalized_tier = _normalize_tier(args.tier)
            if normalized_tier:
                opp_data["Tier"] = normalized_tier
            else:
                opp_data["Tier"] = args.tier
        if args.source:
            opp_data["Source"] = args.source
        if args.value:
            opp_data["Contract Value"] = args.value
        if args.deadline:
            opp_data["Response Deadline"] = args.deadline
        if args.url:
            opp_data["Solicitation URL"] = args.url

        if not opp_data.get("Opportunity ID") and not opp_data.get("Title"):
            print("ERROR: At least --solicitation or --title is required.")
            sys.exit(1)

        opp_id = pipeline.add_opportunity(opp_data)
        print(f"Opportunity added: {opp_id}")
        return

    # --- Update Stage ---
    if args.update_stage:
        opp_id, new_stage = args.update_stage
        if pipeline.update_stage(opp_id, new_stage):
            normalized = _normalize_stage(new_stage) or new_stage
            print(f"Opportunity {opp_id} stage updated to '{normalized}'.")
        else:
            print(f"Failed to update opportunity {opp_id}.")
            sys.exit(1)
        return

    # --- Score Opportunity ---
    if args.score:
        try:
            overrides = json.loads(args.overrides)
        except json.JSONDecodeError as exc:
            print(f"ERROR: Invalid JSON in --overrides: {exc}")
            sys.exit(1)

        result = pipeline.score_opportunity(args.score, overrides=overrides or None)
        if result:
            print(f"\nScored {args.score}: {result['total_score']:.1f}/100")
            print(f"Recommendation: {result['recommendation']}")
            print(f"\nReasoning:\n{result['reasoning']}")
        else:
            print(f"Failed to score opportunity {args.score}.")
            sys.exit(1)
        return

    # --- Import CSV ---
    if args.import_csv:
        csv_path = args.import_csv
        # Handle glob expansion
        if "*" in csv_path:
            import glob as glob_mod
            matches = sorted(glob_mod.glob(csv_path))
            if matches:
                csv_path = matches[-1]
                logger.info("Glob matched: %s", csv_path)
            else:
                print(f"ERROR: No files matching: {args.import_csv}")
                sys.exit(1)

        results = pipeline.import_from_csv(csv_path)
        print(
            f"Import results: {results['imported']} imported, "
            f"{results['duplicates']} duplicates, {results['errors']} errors"
        )
        return

    # --- Dashboard ---
    if args.dashboard:
        summary = pipeline.get_dashboard_data()
        print(f"\n{'=' * 60}")
        print(f"  Newport GovCon Command Center")
        print(f"{'=' * 60}")
        print(f"\n  Total Opportunities: {summary['total_opportunities']}")
        print(f"  Active Pipeline Value: ${summary['active_pipeline_value']:,.0f}")
        print(f"  Awarded Value: ${summary['awarded_value']:,.0f}")
        print(f"  Win Rate: {summary['win_rate']:.1%}")

        print(f"\n  PIPELINE BY STAGE:")
        for stage, count in summary.get("by_stage", {}).items():
            print(f"    {stage:25s} {count}")

        print(f"\n  BY BUYER CATEGORY:")
        for cat, info in summary.get("by_category", {}).items():
            print(f"    {cat:25s} {info['count']:3d}  (${info['value']:,.0f})")

        if summary.get("by_state"):
            print(f"\n  BY STATE:")
            for state, count in summary["by_state"].items():
                print(f"    {state:5s} {count}")

        print(f"\n  UPCOMING DEADLINES:")
        print(f"    This week:   {summary['upcoming_deadlines_7d']}")
        print(f"    Next 14 days: {summary['upcoming_deadlines_14d']}")

        print(f"\n  MONTHLY ACTIVITY:")
        print(f"    Added this month:   {summary['monthly_added']}")
        print(f"    Updated this month: {summary['monthly_updated']}")

        print(f"\n  Tracked Agencies: {summary['tracked_agencies']}")

        # Deadline preview
        upcoming = pipeline.get_upcoming_deadlines(days=14)
        if upcoming:
            print(f"\n  DEADLINE DETAIL (next 14 days): {len(upcoming)}")
            for opp in upcoming[:5]:
                days = opp.get("_days_until", "?")
                title = str(opp.get("Title", "?"))[:40]
                print(f"    {days:>3} days | {title}")

        return

    # --- Deadlines ---
    if args.deadlines:
        upcoming = pipeline.get_upcoming_deadlines(days=args.days_ahead)
        if not upcoming:
            print(f"No deadlines in the next {args.days_ahead} days.")
            return

        print(f"\n{'=' * 60}")
        print(f"  Upcoming Deadlines ({args.days_ahead} days)")
        print(f"{'=' * 60}")
        for opp in upcoming:
            days = opp.get("_days_until", "?")
            title = str(opp.get("Title", "?"))[:45]
            opp_id = opp.get("Opportunity ID", "")
            agency = str(opp.get("Agency", ""))[:30]
            stage = opp.get("Stage", "")
            score = opp.get("Bid/No-Bid Score", "")
            print(f"  {days:>3} days | {title}")
            print(f"          {opp_id} | {agency} | stage={stage} | score={score}")
        return

    # --- Sync Agencies ---
    if args.sync_agencies:
        results = pipeline.sync_agencies()
        print(f"Agency sync: {results['added']} added, {results['updated']} updated")
        return

    # --- Active Pipeline ---
    if args.active_pipeline:
        active = pipeline.get_active_pipeline()
        if not active:
            print("No active opportunities in pipeline.")
            return

        print(f"\n{'=' * 60}")
        print(f"  Active Pipeline ({len(active)} opportunities)")
        print(f"{'=' * 60}")
        for opp in active:
            title = str(opp.get("Title", "?"))[:45]
            stage = opp.get("Stage", "")
            agency = str(opp.get("Agency", ""))[:25]
            score = opp.get("Bid/No-Bid Score", "")
            value = opp.get("Contract Value", "")
            print(
                f"  {opp.get('Opportunity ID', '?'):15s} | {title}"
            )
            print(
                f"  {'':15s} | {agency} | stage={stage} | "
                f"score={score} | value={value}"
            )
        return

    # --- Export ---
    if args.export:
        output_path = pipeline.export_pipeline_csv(args.output)
        if output_path:
            print(f"Exported to {output_path}")
        else:
            print("No opportunities to export.")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
