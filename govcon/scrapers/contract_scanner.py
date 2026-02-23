"""Government contract intelligence pipeline for federal food procurement.

Produces ten reports from free federal APIs:
  - Expiring contracts (USASpending.gov — no key needed)
  - Incumbent analysis (USASpending.gov — no key needed)
  - Small contracts $10K-$350K (USASpending.gov — no key needed)
  - FEMA food procurement (USASpending.gov — no key needed)
  - Market sizing (USASpending.gov — no key needed)
  - Opportunity pipeline (SAM.gov Opportunities — needs SAM_API_KEY)
  - Competitor registry (SAM.gov Entity API — needs SAM_API_KEY)
  - Computed analytics (USASpending.gov — no key needed)
  - Grants pipeline (Grants.gov — no key needed)
  - Competition density (FPDS ATOM feed — no key needed)

SAM.gov: 1,000 requests/day, key required (free at sam.gov).
USASpending: unlimited, no API key needed.
Grants.gov: unlimited, no API key needed.
FPDS: unlimited, no API key needed.

Usage:
    python scrapers/contract_scanner.py --report small-contracts --state FL --fiscal-years 2024,2025
    python scrapers/contract_scanner.py --report fema --fiscal-years 2024,2025
    python scrapers/contract_scanner.py --report expiring --months-ahead 12
    python scrapers/contract_scanner.py --report incumbents --max-pages 10
    python scrapers/contract_scanner.py --report market-size --fiscal-years 2023,2024,2025
    python scrapers/contract_scanner.py --report opportunities --naics-scope primary
    python scrapers/contract_scanner.py --report competitors --states FL,GA,AL
    python scrapers/contract_scanner.py --report analytics --fiscal-years 2023,2024,2025
    python scrapers/contract_scanner.py --report grants
    python scrapers/contract_scanner.py --report competition-density --fiscal-years 2024,2025
    python scrapers/contract_scanner.py --report all --dry-run
"""

import argparse
import hashlib
import json
import logging
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

# Ensure project root is on sys.path when running as script
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
_govcon = _project_root / "govcon"
if str(_govcon) not in sys.path:
    sys.path.insert(0, str(_govcon))

import pandas as pd
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()

from enrichment.usaspending_client import USASpendingClient

log = logging.getLogger(__name__)

PROJECT_ROOT = _project_root
CONFIG_PATH = PROJECT_ROOT / "config" / "government_contracts.json"
FINAL_DIR = PROJECT_ROOT / "data" / "final"
CACHE_DIR = PROJECT_ROOT / "data" / "cache"


# =============================================================================
# Config
# =============================================================================

def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def get_naics_codes(config: dict, scope: str = "primary") -> list[str]:
    """Get NAICS codes based on scope flag."""
    codes = list(config["naics_codes"]["primary"].keys())
    if scope == "all":
        codes.extend(config["naics_codes"]["secondary"].keys())
    return codes


def get_naics_prefixes(config: dict, scope: str = "primary") -> list[str]:
    """Get NAICS prefixes for USASpending queries (e.g., '4244' matches all 4244xx)."""
    prefixes = set()
    for code in get_naics_codes(config, scope):
        prefixes.add(code[:4])
    return sorted(prefixes)


# =============================================================================
# Cache layer
# =============================================================================

def cache_key(params: dict) -> str:
    """Generate MD5 hash of sorted query params for cache key."""
    serialized = json.dumps(params, sort_keys=True, default=str)
    return hashlib.md5(serialized.encode()).hexdigest()


def read_cache(key: str, ttl_hours: int = 24) -> list[dict] | None:
    """Read cached data if it exists and hasn't expired."""
    cache_file = CACHE_DIR / f"{key}.json"
    if not cache_file.exists():
        return None

    try:
        data = json.loads(cache_file.read_text())
        cached_at = datetime.fromisoformat(data["cached_at"])
        if datetime.now() - cached_at > timedelta(hours=ttl_hours):
            return None  # expired
        log.info(f"Cache hit: {key}")
        return data["results"]
    except (json.JSONDecodeError, KeyError, ValueError):
        return None


def write_cache(key: str, results: list[dict]) -> None:
    """Write results to cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = CACHE_DIR / f"{key}.json"
    data = {
        "cached_at": datetime.now().isoformat(),
        "count": len(results),
        "results": results,
    }
    cache_file.write_text(json.dumps(data, default=str))


# =============================================================================
# Output helpers
# =============================================================================

def save_results(df: pd.DataFrame, report_name: str) -> Path:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    path = FINAL_DIR / f"govt_{report_name}_{date_str}.csv"
    df.to_csv(path, index=False)
    return path


def print_summary(df: pd.DataFrame, report_name: str) -> None:
    total = len(df)
    print(f"\n{'='*70}")
    print(f"REPORT: {report_name} ({total} records)")
    print(f"{'='*70}")

    if total == 0:
        print("  No results found.")
        return

    # Dollar summary
    amount_col = None
    for col in ["award_amount", "total_value", "amount"]:
        if col in df.columns:
            amount_col = col
            break

    if amount_col:
        amounts = pd.to_numeric(df[amount_col], errors="coerce").dropna()
        if not amounts.empty:
            print(f"\n  Dollar summary:")
            print(f"    Total: ${amounts.sum():,.0f}")
            print(f"    Mean:  ${amounts.mean():,.0f}")
            print(f"    Median: ${amounts.median():,.0f}")
            print(f"    Min:   ${amounts.min():,.0f}")
            print(f"    Max:   ${amounts.max():,.0f}")

    # Agency breakdown
    agency_col = None
    for col in ["awarding_agency", "awarding_sub_agency", "agency"]:
        if col in df.columns:
            agency_col = col
            break

    if agency_col:
        print(f"\n  Top agencies:")
        for agency, count in df[agency_col].value_counts().head(10).items():
            if agency:
                print(f"    {agency}: {count}")

    # Vendor/recipient breakdown
    vendor_col = None
    for col in ["recipient_name", "vendor_name"]:
        if col in df.columns:
            vendor_col = col
            break

    if vendor_col:
        unique_vendors = df[vendor_col].nunique()
        print(f"\n  Unique vendors: {unique_vendors}")
        print(f"  Top vendors:")
        for vendor, count in df[vendor_col].value_counts().head(10).items():
            if vendor:
                print(f"    {vendor}: {count}")

    # State breakdown
    if "pop_state" in df.columns:
        print(f"\n  Top states (place of performance):")
        for state, count in df["pop_state"].value_counts().head(10).items():
            if state:
                print(f"    {state}: {count}")

    # NAICS breakdown
    if "naics_code" in df.columns:
        print(f"\n  NAICS codes represented:")
        for code, count in df["naics_code"].value_counts().head(10).items():
            if code:
                print(f"    {code}: {count}")


# =============================================================================
# Report: Expiring Contracts (USASpending)
# =============================================================================

def report_expiring_contracts(
    config: dict,
    naics_scope: str = "primary",
    months_ahead: int = 12,
    max_pages: int = 10,
    min_value: float = 0,
    max_value: float | None = None,
    agency_name: str = "",
    state: str = "",
    use_cache: bool = True,
) -> pd.DataFrame:
    """Find contracts with period of performance ending in the next N months.

    Uses USASpending.gov (free, no key needed) instead of SAM.gov.
    """
    naics_prefixes = get_naics_prefixes(config, naics_scope)
    today = datetime.now()
    future = today + relativedelta(months=months_ahead)

    print(f"\nExpiring Contracts Report (USASpending)")
    print(f"  NAICS prefixes: {naics_prefixes}")
    print(f"  Window: {today.strftime('%Y-%m-%d')} to {future.strftime('%Y-%m-%d')}")
    print(f"  Max pages: {max_pages}")
    if state:
        print(f"  State filter: {state}")
    if agency_name:
        print(f"  Agency filter: {agency_name}")

    # Check cache
    ck = cache_key({
        "report": "expiring_v2",
        "naics": naics_prefixes,
        "from": today.strftime("%Y-%m-%d"),
        "to": future.strftime("%Y-%m-%d"),
        "max_pages": max_pages,
        "state": state,
        "agency": agency_name,
    })

    cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
    if cached is not None:
        print(f"  Using cached data ({len(cached)} records)")
        all_awards = cached
    else:
        client = USASpendingClient()
        agencies = [agency_name] if agency_name else None
        all_awards = client.search_expiring_awards(
            naics_require=naics_prefixes,
            months_ahead=months_ahead,
            award_amount_min=min_value if min_value else None,
            award_amount_max=max_value,
            agencies=agencies,
            state=state,
            max_pages=max_pages,
        )
        print(f"  USASpending API stats: {client.stats}")
        if use_cache and all_awards:
            write_cache(ck, all_awards)

    if not all_awards:
        print("  No expiring contracts found.")
        return pd.DataFrame()

    # Flatten and process
    records = [USASpendingClient.flatten_award(a) for a in all_awards]
    df = pd.DataFrame(records)

    # Calculate months until expiry
    if "pop_end_date" in df.columns:
        df["pop_end_date_parsed"] = pd.to_datetime(df["pop_end_date"], errors="coerce")
        df["months_until_expiry"] = df["pop_end_date_parsed"].apply(
            lambda d: round((d - today).days / 30.44, 1) if pd.notna(d) else None
        )
        df.drop(columns=["pop_end_date_parsed"], inplace=True)

    # Filter by min value
    if min_value and "award_amount" in df.columns:
        df["award_amount"] = pd.to_numeric(df["award_amount"], errors="coerce")
        df = df[df["award_amount"] >= min_value]

    # Sort by months until expiry
    if "months_until_expiry" in df.columns:
        df = df.sort_values("months_until_expiry", ascending=True)

    return df


# =============================================================================
# Report: Incumbent Analysis (USASpending)
# =============================================================================

def report_incumbent_analysis(
    config: dict,
    naics_scope: str = "primary",
    max_pages: int = 10,
    vendor_filter: str = "",
    state: str = "",
    agency_name: str = "",
    use_cache: bool = True,
) -> pd.DataFrame:
    """Analyze incumbent vendors in federal food procurement.

    Uses USASpending.gov (free, no key needed).
    Pulls awards for the last N years with food NAICS codes.
    Groups by vendor: count contracts, sum value, list agencies.
    """
    naics_prefixes = get_naics_prefixes(config, naics_scope)
    lookback = config["analysis"]["incumbent_lookback_years"]
    today = datetime.now()
    start = today - relativedelta(years=lookback)

    print(f"\nIncumbent Analysis Report (USASpending)")
    print(f"  NAICS prefixes: {naics_prefixes}")
    print(f"  Lookback: {lookback} years ({start.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')})")
    print(f"  Max pages: {max_pages}")
    if state:
        print(f"  State filter: {state}")

    # Check cache
    ck = cache_key({
        "report": "incumbents_v2",
        "naics": naics_prefixes,
        "from": start.strftime("%Y-%m-%d"),
        "to": today.strftime("%Y-%m-%d"),
        "max_pages": max_pages,
        "state": state,
        "agency": agency_name,
    })

    cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
    if cached is not None:
        print(f"  Using cached data ({len(cached)} records)")
        all_awards = cached
    else:
        client = USASpendingClient()
        agencies = [agency_name] if agency_name else None
        all_awards = client.search_awards_all_pages(
            naics_require=naics_prefixes,
            time_period_start=start.strftime("%Y-%m-%d"),
            time_period_end=today.strftime("%Y-%m-%d"),
            agencies=agencies,
            state=state,
            max_pages=max_pages,
        )
        print(f"  USASpending API stats: {client.stats}")
        if use_cache and all_awards:
            write_cache(ck, all_awards)

    if not all_awards:
        print("  No awards found for incumbent analysis.")
        return pd.DataFrame()

    # Flatten
    records = [USASpendingClient.flatten_award(a) for a in all_awards]
    df = pd.DataFrame(records)

    if df.empty or "recipient_name" not in df.columns:
        return pd.DataFrame()

    # Parse numeric fields
    df["award_amount"] = pd.to_numeric(df["award_amount"], errors="coerce").fillna(0)

    # Group by vendor
    grouped = df.groupby("recipient_name").agg(
        total_contracts=("award_id", "count"),
        total_value=("award_amount", "sum"),
        avg_value=("award_amount", "mean"),
        agencies=("awarding_sub_agency", lambda x: ", ".join(sorted(set(s for s in x if s))[:5])),
        top_naics=("naics_code", lambda x: x.mode().iloc[0] if not x.mode().empty else ""),
        states=("pop_state", lambda x: ", ".join(sorted(set(s for s in x if s))[:5])),
    ).reset_index()

    grouped["avg_value"] = grouped["avg_value"].round(0)

    # Sort by total value descending
    grouped = grouped.sort_values("total_value", ascending=False)

    # Rename for output
    grouped = grouped.rename(columns={
        "agencies": "agencies_served",
        "states": "performance_states",
    })

    # Filter by vendor name
    if vendor_filter:
        grouped = grouped[grouped["recipient_name"].str.contains(vendor_filter, case=False, na=False)]

    return grouped


# =============================================================================
# Report: Small Contracts ($10K-$350K)
# =============================================================================

def report_small_contracts(
    config: dict,
    naics_scope: str = "primary",
    fiscal_years: list[int] | None = None,
    max_pages: int = 10,
    state: str = "",
    agency_name: str = "",
    min_value: float | None = None,
    max_value: float | None = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Find small/micro federal food contracts in the simplified acquisition range.

    Defaults to $10K-$350K (simplified acquisition threshold).
    This is THE report that validates the pitchbook's Year 1 targets.
    """
    if fiscal_years is None:
        fiscal_years = config["analysis"]["fiscal_years"]

    sa = config.get("simplified_acquisition", {})
    if min_value is None:
        min_value = sa.get("small_contract_min", 10000)
    if max_value is None:
        max_value = sa.get("small_contract_max", 350000)

    naics_prefixes = get_naics_prefixes(config, naics_scope)

    print(f"\nSmall Contracts Report (USASpending)")
    print(f"  NAICS prefixes: {naics_prefixes}")
    print(f"  Dollar range: ${min_value:,.0f} - ${max_value:,.0f}")
    print(f"  Fiscal years: {fiscal_years}")
    if state:
        print(f"  State filter: {state}")
    if agency_name:
        print(f"  Agency filter: {agency_name}")

    client = USASpendingClient()
    all_awards = []

    for fy in fiscal_years:
        start, end = USASpendingClient.fiscal_year_range(fy)
        print(f"\n  FY{fy} ({start} to {end})...")

        ck = cache_key({
            "report": "small_contracts",
            "naics": naics_prefixes,
            "fy": fy,
            "min": min_value,
            "max": max_value,
            "state": state,
            "agency": agency_name,
            "max_pages": max_pages,
        })

        cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
        if cached is not None:
            print(f"  Using cached data ({len(cached)} records)")
            fy_awards = cached
        else:
            agencies = [agency_name] if agency_name else None
            fy_awards = client.search_awards_all_pages(
                naics_require=naics_prefixes,
                time_period_start=start,
                time_period_end=end,
                award_amount_min=min_value,
                award_amount_max=max_value,
                agencies=agencies,
                state=state,
                max_pages=max_pages,
            )
            if use_cache and fy_awards:
                write_cache(ck, fy_awards)

        # Tag with fiscal year
        for award in fy_awards:
            award["_fiscal_year"] = f"FY{fy}"
        all_awards.extend(fy_awards)

    print(f"\n  USASpending API stats: {client.stats}")

    if not all_awards:
        print("  No small contracts found.")
        return pd.DataFrame()

    # Flatten
    records = []
    for a in all_awards:
        flat = USASpendingClient.flatten_award(a)
        flat["fiscal_year"] = a.get("_fiscal_year", "")
        records.append(flat)

    df = pd.DataFrame(records)
    df["award_amount"] = pd.to_numeric(df["award_amount"], errors="coerce")

    # Print size distribution
    print(f"\n  Size distribution:")
    bins = [10000, 25000, 50000, 100000, 150000, 250000, 350000]
    labels = ["$10K-25K", "$25K-50K", "$50K-100K", "$100K-150K", "$150K-250K", "$250K-350K"]
    df["size_bucket"] = pd.cut(df["award_amount"], bins=bins, labels=labels, include_lowest=True)
    for bucket, count in df["size_bucket"].value_counts().sort_index().items():
        print(f"    {bucket}: {count} contracts")

    # FY breakdown
    print(f"\n  By fiscal year:")
    for fy in df["fiscal_year"].unique():
        fy_df = df[df["fiscal_year"] == fy]
        print(f"    {fy}: {len(fy_df)} contracts, ${fy_df['award_amount'].sum():,.0f} total")

    return df


# =============================================================================
# Report: FEMA Food Procurement
# =============================================================================

def report_fema_contracts(
    config: dict,
    naics_scope: str = "primary",
    fiscal_years: list[int] | None = None,
    max_pages: int = 10,
    state: str = "",
    use_cache: bool = True,
) -> pd.DataFrame:
    """FEMA food procurement volume, typical contract sizes, common products.

    Convenience wrapper that filters to FEMA as the awarding subtier agency.
    """
    if fiscal_years is None:
        fiscal_years = config["analysis"]["fiscal_years"]

    fema_config = config.get("fema", {})
    fema_name = fema_config.get("agency_name", "Federal Emergency Management Agency")
    naics_prefixes = get_naics_prefixes(config, naics_scope)

    print(f"\nFEMA Food Procurement Report (USASpending)")
    print(f"  Agency: {fema_name}")
    print(f"  NAICS prefixes: {naics_prefixes}")
    print(f"  Fiscal years: {fiscal_years}")
    if state:
        print(f"  State filter: {state}")

    client = USASpendingClient()
    all_awards = []

    for fy in fiscal_years:
        start, end = USASpendingClient.fiscal_year_range(fy)
        print(f"\n  FY{fy} ({start} to {end})...")

        ck = cache_key({
            "report": "fema",
            "naics": naics_prefixes,
            "fy": fy,
            "agency": fema_name,
            "state": state,
            "max_pages": max_pages,
        })

        cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
        if cached is not None:
            print(f"  Using cached data ({len(cached)} records)")
            fy_awards = cached
        else:
            fy_awards = client.search_awards_all_pages(
                naics_require=naics_prefixes,
                time_period_start=start,
                time_period_end=end,
                agencies=[fema_name],
                state=state,
                max_pages=max_pages,
            )
            if use_cache and fy_awards:
                write_cache(ck, fy_awards)

        for award in fy_awards:
            award["_fiscal_year"] = f"FY{fy}"
        all_awards.extend(fy_awards)

    print(f"\n  USASpending API stats: {client.stats}")

    if not all_awards:
        print("  No FEMA food contracts found.")
        return pd.DataFrame()

    records = []
    for a in all_awards:
        flat = USASpendingClient.flatten_award(a)
        flat["fiscal_year"] = a.get("_fiscal_year", "")
        records.append(flat)

    df = pd.DataFrame(records)
    df["award_amount"] = pd.to_numeric(df["award_amount"], errors="coerce")

    # FY breakdown
    print(f"\n  By fiscal year:")
    for fy in sorted(df["fiscal_year"].unique()):
        fy_df = df[df["fiscal_year"] == fy]
        print(f"    {fy}: {len(fy_df)} contracts, ${fy_df['award_amount'].sum():,.0f} total")

    return df


# =============================================================================
# Report: Opportunity Pipeline (SAM.gov — needs API key)
# =============================================================================

def report_opportunity_pipeline(
    config: dict,
    naics_scope: str = "primary",
    max_pages: int = 10,
    agency_filter: str = "",
    use_cache: bool = True,
) -> pd.DataFrame:
    """Find active solicitations, pre-solicitations, and sources sought.

    This is the ONLY report that requires a SAM.gov API key.
    Searches across all food NAICS codes and deduplicates by noticeId.
    """
    from enrichment.sam_client import SAMClient

    sam = SAMClient()
    naics_codes = get_naics_codes(config, naics_scope)
    today = datetime.now()
    posted_from = (today - timedelta(days=90)).strftime("%m/%d/%Y")

    print(f"\nOpportunity Pipeline Report (SAM.gov)")
    print(f"  NAICS codes: {len(naics_codes)} ({naics_scope} scope)")
    print(f"  Posted since: {posted_from}")
    print(f"  Opportunity types: pre-sol, solicitation, sources sought, combined")

    # Check cache
    ck = cache_key({
        "report": "opportunities",
        "naics": naics_codes,
        "from": posted_from,
    })

    cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
    if cached is not None:
        print(f"  Using cached data ({len(cached)} records)")
        all_opps = cached
    else:
        all_opps = sam.search_opportunities_all_naics(
            naics_codes=naics_codes,
            ptypes=["p", "o", "r", "k"],
            posted_from=posted_from,
        )
        if use_cache and all_opps:
            write_cache(ck, all_opps)

    if not all_opps:
        print("  No opportunities found.")
        return pd.DataFrame()

    # Flatten
    records = [SAMClient.flatten_opportunity(o) for o in all_opps]
    df = pd.DataFrame(records)

    # Calculate days until deadline
    if "response_deadline" in df.columns:
        df["response_deadline_parsed"] = pd.to_datetime(
            df["response_deadline"], format="mixed", errors="coerce"
        )
        df["days_until_deadline"] = df["response_deadline_parsed"].apply(
            lambda d: (d - today).days if pd.notna(d) else None
        )
        df.drop(columns=["response_deadline_parsed"], inplace=True)

    # Filter by agency
    if agency_filter and "agency" in df.columns:
        df = df[df["agency"].str.contains(agency_filter, case=False, na=False)]

    # Sort by deadline (soonest first)
    if "days_until_deadline" in df.columns:
        df = df.sort_values("days_until_deadline", ascending=True)

    print(f"\n  SAM.gov API stats: {sam.stats}")

    return df


# =============================================================================
# Report: Market Sizing (USASpending)
# =============================================================================

def report_market_sizing(
    config: dict,
    naics_scope: str = "primary",
    fiscal_years: list[int] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Size the federal food procurement market using USASpending.gov.

    No SAM key needed — USASpending is free and unlimited.
    Returns two DataFrames: spending by NAICS and spending by agency.
    """
    if fiscal_years is None:
        fiscal_years = config["analysis"]["fiscal_years"]

    naics_prefixes = get_naics_prefixes(config, naics_scope)

    print(f"\nMarket Sizing Report (USASpending)")
    print(f"  NAICS prefixes: {naics_prefixes}")
    print(f"  Fiscal years: {fiscal_years}")

    client = USASpendingClient()

    by_naics_records = []
    by_agency_records = []

    for fy in fiscal_years:
        start, end = USASpendingClient.fiscal_year_range(fy)
        print(f"\n  FY{fy} ({start} to {end})...")

        # Spending by NAICS
        print(f"    Spending by NAICS...", end=" ", flush=True)
        naics_results = client.spending_by_naics(
            naics_require=naics_prefixes,
            time_period_start=start,
            time_period_end=end,
        )
        print(f"{len(naics_results)} categories")

        for item in naics_results:
            by_naics_records.append({
                "fiscal_year": f"FY{fy}",
                "naics_code": item.get("code", ""),
                "naics_name": item.get("name", ""),
                "amount": item.get("amount", 0),
            })

        # Spending by agency
        print(f"    Spending by agency...", end=" ", flush=True)
        agency_results = client.spending_by_agency(
            naics_require=naics_prefixes,
            time_period_start=start,
            time_period_end=end,
        )
        print(f"{len(agency_results)} agencies")

        for item in agency_results:
            by_agency_records.append({
                "fiscal_year": f"FY{fy}",
                "agency": item.get("name", ""),
                "amount": item.get("amount", 0),
            })

        time.sleep(0.5)

    df_naics = pd.DataFrame(by_naics_records) if by_naics_records else pd.DataFrame()
    df_agency = pd.DataFrame(by_agency_records) if by_agency_records else pd.DataFrame()

    # Sort by amount descending within each FY
    if not df_naics.empty:
        df_naics = df_naics.sort_values(["fiscal_year", "amount"], ascending=[True, False])
    if not df_agency.empty:
        df_agency = df_agency.sort_values(["fiscal_year", "amount"], ascending=[True, False])

    print(f"\n  USASpending API stats: {client.stats}")

    return df_naics, df_agency


# =============================================================================
# Report: Competitor Registry (SAM.gov Entity API)
# =============================================================================

def report_competitor_registry(
    config: dict,
    naics_scope: str = "primary",
    states: list[str] | None = None,
    max_pages_per_query: int = 20,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Find registered federal food contractors by NAICS and state.

    Uses SAM.gov Entity Management API v3 (same SAM_API_KEY, 1,000 req/day).
    Shows who Newport is competing against — names, CAGE codes, certs, contacts.
    """
    from enrichment.sam_entity_client import SAMEntityClient

    entity_client = SAMEntityClient()
    naics_codes = get_naics_codes(config, naics_scope)

    if states is None:
        states = config.get("target_states", ["FL", "GA", "AL", "SC", "NC"])

    print(f"\nCompetitor Registry Report (SAM.gov Entity API)")
    print(f"  NAICS codes: {len(naics_codes)} ({naics_scope} scope)")
    print(f"  States: {states}")
    print(f"  Max pages per query: {max_pages_per_query}")

    # Check cache
    ck = cache_key({
        "report": "competitor_registry",
        "naics": naics_codes,
        "states": states,
        "max_pages": max_pages_per_query,
    })

    cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
    if cached is not None:
        print(f"  Using cached data ({len(cached)} records)")
        all_entities = cached
    else:
        all_entities = entity_client.search_food_wholesalers_by_state(
            naics_codes=naics_codes,
            states=states,
            max_pages_per_query=max_pages_per_query,
        )
        print(f"\n  SAM Entity API stats: {entity_client.stats}")
        if use_cache and all_entities:
            write_cache(ck, all_entities)

    if not all_entities:
        print("  No registered entities found.")
        return pd.DataFrame()

    records = [SAMEntityClient.flatten_entity(e) for e in all_entities]
    df = pd.DataFrame(records)

    # Summary stats
    if not df.empty:
        print(f"\n  By state:")
        for state, count in df["physical_state"].value_counts().head(10).items():
            if state:
                print(f"    {state}: {count} registered vendors")

        if "primary_naics" in df.columns:
            print(f"\n  By primary NAICS:")
            for naics, count in df["primary_naics"].value_counts().head(10).items():
                if naics:
                    print(f"    {naics}: {count} vendors")

        if "business_types" in df.columns:
            print(f"\n  Small business certifications:")
            small_biz = df[df["business_types"].str.contains("Small", case=False, na=False)]
            print(f"    Small business: {len(small_biz)} ({len(small_biz)/len(df)*100:.0f}%)")

    return df


# =============================================================================
# Report: Computed Analytics (trends, saturation, concentration)
# =============================================================================

def report_analytics(
    config: dict,
    naics_scope: str = "primary",
    fiscal_years: list[int] | None = None,
    state: str = "",
    use_cache: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Computed analytics: spending trends, geographic heatmap, recipient concentration.

    Combines multiple USASpending endpoints into 3 analytical DataFrames:
    1. Monthly spending trends (12-month rolling)
    2. State-level geographic heatmap
    3. Top recipients with concentration metrics
    """
    if fiscal_years is None:
        fiscal_years = config["analysis"]["fiscal_years"]

    naics_prefixes = get_naics_prefixes(config, naics_scope)

    print(f"\nComputed Analytics Report (USASpending)")
    print(f"  NAICS prefixes: {naics_prefixes}")
    print(f"  Fiscal years: {fiscal_years}")
    if state:
        print(f"  State focus: {state}")

    client = USASpendingClient()

    # --- 1. Monthly spending trends ---
    print(f"\n  1. Spending trends (monthly)...")
    trend_records = []
    for fy in fiscal_years:
        start, end = USASpendingClient.fiscal_year_range(fy)
        results = client.new_awards_over_time(
            naics_require=naics_prefixes,
            time_period_start=start,
            time_period_end=end,
            group="month",
            state=state,
        )
        for item in results:
            trend_records.append({
                "fiscal_year": f"FY{fy}",
                "time_period": f"{item.get('time_period', {}).get('fiscal_year', '')}-{item.get('time_period', {}).get('month', '')}",
                "new_award_count": item.get("new_award_count_in_period", 0),
                "aggregated_amount": item.get("aggregated_amount", 0),
            })
        time.sleep(0.5)

    df_trends = pd.DataFrame(trend_records) if trend_records else pd.DataFrame()
    if not df_trends.empty:
        total_by_fy = df_trends.groupby("fiscal_year")["aggregated_amount"].sum()
        print(f"    Trends by FY:")
        for fy, total in total_by_fy.items():
            print(f"      {fy}: ${total:,.0f}")

    # --- 2. Geographic heatmap (state-level) ---
    print(f"\n  2. Geographic distribution (state level)...")
    geo_records = []
    for fy in fiscal_years:
        start, end = USASpendingClient.fiscal_year_range(fy)
        results = client.spending_by_geography(
            naics_require=naics_prefixes,
            time_period_start=start,
            time_period_end=end,
            geo_layer="state",
            scope="place_of_performance",
        )
        for item in results:
            geo_records.append({
                "fiscal_year": f"FY{fy}",
                "state_code": item.get("shape_code", ""),
                "state_name": item.get("display_name", ""),
                "aggregated_amount": item.get("aggregated_amount", 0),
                "per_capita": item.get("per_capita", 0),
                "award_count": item.get("award_count", 0),
            })
        time.sleep(0.5)

    df_geo = pd.DataFrame(geo_records) if geo_records else pd.DataFrame()
    if not df_geo.empty:
        # Show Newport target states
        target_states = config.get("target_states", ["FL", "GA", "AL", "SC", "NC"])
        latest_fy = f"FY{max(fiscal_years)}"
        latest_geo = df_geo[df_geo["fiscal_year"] == latest_fy]
        if not latest_geo.empty:
            target_geo = latest_geo[latest_geo["state_code"].isin(target_states)]
            if not target_geo.empty:
                print(f"    {latest_fy} Newport target states:")
                for _, row in target_geo.sort_values("aggregated_amount", ascending=False).iterrows():
                    print(f"      {row['state_code']}: ${row['aggregated_amount']:,.0f} ({row.get('award_count', 'N/A')} awards)")

    # --- 3. Top recipients (concentration) ---
    print(f"\n  3. Recipient concentration...")
    recipient_records = []
    for fy in fiscal_years:
        start, end = USASpendingClient.fiscal_year_range(fy)
        results = client.spending_by_recipient(
            naics_require=naics_prefixes,
            time_period_start=start,
            time_period_end=end,
            limit=50,
        )
        fy_total = sum(r.get("amount", 0) for r in results)
        cumulative = 0
        for i, item in enumerate(results):
            amount = item.get("amount", 0)
            cumulative += amount
            recipient_records.append({
                "fiscal_year": f"FY{fy}",
                "rank": i + 1,
                "recipient_name": item.get("name", ""),
                "recipient_id": item.get("id", ""),
                "amount": amount,
                "market_share_pct": round(amount / fy_total * 100, 2) if fy_total else 0,
                "cumulative_share_pct": round(cumulative / fy_total * 100, 2) if fy_total else 0,
            })
        time.sleep(0.5)

    df_recipients = pd.DataFrame(recipient_records) if recipient_records else pd.DataFrame()
    if not df_recipients.empty:
        latest_fy = f"FY{max(fiscal_years)}"
        latest_recip = df_recipients[df_recipients["fiscal_year"] == latest_fy]
        if not latest_recip.empty:
            top5 = latest_recip.head(5)
            top5_share = top5["market_share_pct"].sum()
            top10_share = latest_recip.head(10)["market_share_pct"].sum()
            print(f"    {latest_fy} concentration:")
            print(f"      Top 5 vendors: {top5_share:.1f}% market share")
            print(f"      Top 10 vendors: {top10_share:.1f}% market share")
            print(f"    {latest_fy} top 5:")
            for _, row in top5.iterrows():
                print(f"      {row['recipient_name']}: ${row['amount']:,.0f} ({row['market_share_pct']:.1f}%)")

    print(f"\n  USASpending API stats: {client.stats}")
    return df_trends, df_geo, df_recipients


# =============================================================================
# Report: Grants Pipeline (Grants.gov)
# =============================================================================

def report_grants_pipeline(
    config: dict,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Find USDA food-related grant opportunities from Grants.gov.

    No API key needed. Searches 14+ food-related keywords plus broader terms.
    Covers LFPA, TEFAP, CSFP, FDPIR, Farm to School, DoD Fresh, etc.
    """
    from enrichment.grants_client import GrantsClient

    grants_client = GrantsClient()

    print(f"\nGrants Pipeline Report (Grants.gov)")
    print(f"  Source: https://api.grants.gov/v1/api")
    print(f"  API key: not required")

    # Check cache
    ck = cache_key({"report": "grants_pipeline"})

    cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
    if cached is not None:
        print(f"  Using cached data ({len(cached)} records)")
        all_grants = cached
    else:
        all_grants = grants_client.search_food_grants()
        print(f"\n  Grants.gov API stats: {grants_client.stats}")
        if use_cache and all_grants:
            write_cache(ck, all_grants)

    if not all_grants:
        print("  No food grants found.")
        return pd.DataFrame()

    records = [GrantsClient.flatten_grant(g) for g in all_grants]
    df = pd.DataFrame(records)

    # Summary
    if not df.empty:
        print(f"\n  By status:")
        if "status" in df.columns:
            for status, count in df["status"].value_counts().items():
                print(f"    {status}: {count}")

        if "agency_name" in df.columns:
            print(f"\n  By agency:")
            for agency, count in df["agency_name"].value_counts().head(10).items():
                if agency:
                    print(f"    {agency}: {count}")

        # Dollar summary
        if "estimated_funding" in df.columns:
            amounts = pd.to_numeric(df["estimated_funding"], errors="coerce").dropna()
            if not amounts.empty and amounts.sum() > 0:
                print(f"\n  Estimated funding:")
                print(f"    Total: ${amounts.sum():,.0f}")
                print(f"    Avg per grant: ${amounts.mean():,.0f}")

    return df


# =============================================================================
# Report: Competition Density (FPDS ATOM Feed)
# =============================================================================

def report_competition_density(
    config: dict,
    naics_scope: str = "primary",
    fiscal_years: list[int] | None = None,
    state: str = "",
    min_value: float = 25000,
    use_cache: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Analyze competition density using FPDS number-of-offers-received data.

    No API key needed. Uses the fpds Python library for ATOM feed queries.
    Returns two DataFrames:
      1. Raw contract transactions with offers_received field
      2. Competition density summary by NAICS/agency (avg offers per award)

    The key insight: NAICS/agency combos with low avg offers (2-3) = easy entry.
    Those with 8+ avg offers = crowded. This metric is unique to FPDS.
    """
    from enrichment.fpds_client import FPDSClient

    if fiscal_years is None:
        fiscal_years = config["analysis"]["fiscal_years"]

    naics_codes = get_naics_codes(config, naics_scope)

    print(f"\nCompetition Density Report (FPDS)")
    print(f"  Source: FPDS ATOM Feed (no key required)")
    print(f"  NAICS codes: {len(naics_codes)} ({naics_scope} scope)")
    print(f"  Fiscal years: {fiscal_years}")
    print(f"  Min obligated amount: ${min_value:,.0f}")
    if state:
        print(f"  Vendor state filter: {state}")

    client = FPDSClient()
    all_records = []

    for fy in fiscal_years:
        # FPDS uses calendar-style date ranges
        fy_start = f"{fy - 1}/10/01"  # FY starts Oct 1 of prior year
        fy_end = f"{fy}/09/30"
        date_range = f"[{fy_start}, {fy_end}]"
        amount_range = f"[{int(min_value)}, 999999999]"

        print(f"\n  FY{fy} ({fy_start} to {fy_end})...")

        # Check cache
        ck = cache_key({
            "report": "competition_density",
            "naics": naics_codes,
            "fy": fy,
            "min_value": min_value,
            "state": state,
        })

        cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
        if cached is not None:
            print(f"  Using cached data ({len(cached)} records)")
            fy_records = cached
        else:
            raw = client.search_contracts_multi_naics(
                naics_codes=naics_codes,
                date_range=date_range,
                amount_range=amount_range,
                vendor_state=state,
            )
            fy_records = [FPDSClient.flatten_contract(r) for r in raw]
            if use_cache and fy_records:
                write_cache(ck, fy_records)

        for rec in fy_records:
            rec["fiscal_year"] = f"FY{fy}"
        all_records.extend(fy_records)

    print(f"\n  FPDS stats: {client.stats}")

    if not all_records:
        print("  No FPDS records found.")
        return pd.DataFrame(), pd.DataFrame()

    df = pd.DataFrame(all_records)

    # Filter to base awards only (mod_number 0 or empty) for clean competition counts
    df_base = df[df["mod_number"].isin(["0", "", "00000"])].copy()
    print(f"\n  Total transactions: {len(df)}")
    print(f"  Base awards (mod=0): {len(df_base)}")

    # Filter to records with offers data
    df_with_offers = df_base[df_base["offers_received"].notna()].copy()
    print(f"  Awards with offers data: {len(df_with_offers)}")

    if df_with_offers.empty:
        print("  No offers-received data available for density analysis.")
        return df, pd.DataFrame()

    # --- Competition Density Summary ---
    # Group by NAICS + agency to find avg offers per award
    density_records = []

    for (naics, agency), group in df_with_offers.groupby(["naics_code", "agency_name"]):
        offers = group["offers_received"]
        amounts = group["obligated_amount"]

        avg_offers = offers.mean()
        median_offers = offers.median()
        total_awards = len(group)
        total_value = amounts.sum()

        # Competition level classification
        if avg_offers <= 2:
            level = "LOW (easy entry)"
        elif avg_offers <= 5:
            level = "MODERATE"
        elif avg_offers <= 10:
            level = "HIGH"
        else:
            level = "VERY HIGH (crowded)"

        density_records.append({
            "naics_code": naics,
            "agency_name": agency,
            "total_awards": total_awards,
            "total_value": total_value,
            "avg_offers_per_award": round(avg_offers, 1),
            "median_offers": round(median_offers, 1),
            "min_offers": int(offers.min()),
            "max_offers": int(offers.max()),
            "competition_level": level,
            "pct_sole_source": round((offers == 1).sum() / total_awards * 100, 1),
        })

    df_density = pd.DataFrame(density_records)
    df_density = df_density.sort_values("avg_offers_per_award", ascending=True)

    # Print summary
    print(f"\n  Competition Density Summary ({len(df_density)} NAICS/agency combos):")
    print(f"  {'-' * 70}")

    low = df_density[df_density["avg_offers_per_award"] <= 2]
    mod = df_density[(df_density["avg_offers_per_award"] > 2) & (df_density["avg_offers_per_award"] <= 5)]
    high = df_density[df_density["avg_offers_per_award"] > 5]

    print(f"    LOW competition (avg <=2 offers):  {len(low)} combos — BEST ENTRY POINTS")
    print(f"    MODERATE (avg 3-5 offers):         {len(mod)} combos")
    print(f"    HIGH (avg >5 offers):              {len(high)} combos — crowded")

    if not low.empty:
        print(f"\n  Top 10 easiest entry points (lowest competition):")
        for _, row in low.head(10).iterrows():
            print(
                f"    {row['naics_code']} | {row['agency_name'][:45]:45s} | "
                f"avg {row['avg_offers_per_award']:.1f} offers | "
                f"{row['total_awards']} awards | ${row['total_value']:,.0f}"
            )

    # Overall stats
    overall_avg = df_with_offers["offers_received"].mean()
    overall_median = df_with_offers["offers_received"].median()
    sole_source_pct = (df_with_offers["offers_received"] == 1).sum() / len(df_with_offers) * 100
    print(f"\n  Overall competition metrics:")
    print(f"    Average offers per award: {overall_avg:.1f}")
    print(f"    Median offers per award: {overall_median:.1f}")
    print(f"    Sole-source rate: {sole_source_pct:.1f}%")

    return df, df_density


# =============================================================================
# Dry Run
# =============================================================================

def dry_run(config: dict, args) -> None:
    """Show what would be queried without making API calls."""
    naics_codes = get_naics_codes(config, args.naics_scope)
    naics_prefixes = get_naics_prefixes(config, args.naics_scope)

    all_reports = ["expiring", "incumbents", "opportunities", "market-size", "small-contracts", "fema", "competitors", "analytics", "grants"]
    reports = [args.report] if args.report != "all" else all_reports

    print(f"\n{'='*70}")
    print(f"DRY RUN — Government Contract Intelligence Pipeline")
    print(f"{'='*70}")
    print(f"  Reports: {', '.join(reports)}")
    print(f"  NAICS scope: {args.naics_scope}")
    print(f"  NAICS codes ({len(naics_codes)}):")
    for code in naics_codes:
        all_codes = {**config["naics_codes"]["primary"], **config["naics_codes"]["secondary"]}
        name = all_codes.get(code, "")
        print(f"    {code}: {name}")
    print(f"  NAICS prefixes for USASpending: {naics_prefixes}")

    # Estimate API calls
    sam_calls = 0
    usa_calls = 0

    if "expiring" in reports:
        today = datetime.now()
        future = today + relativedelta(months=args.months_ahead)
        print(f"\n  EXPIRING CONTRACTS (USASpending — no key needed)")
        print(f"    Window: {today.strftime('%Y-%m-%d')} to {future.strftime('%Y-%m-%d')}")
        print(f"    Max pages: {args.max_pages}")
        print(f"    Min value: ${args.min_value:,.0f}" if args.min_value else "    Min value: none")
        print(f"    Max value: ${args.max_value:,.0f}" if args.max_value else "    Max value: none")
        print(f"    State: {args.state or 'all'}")
        print(f"    Agency: {args.agency_name or 'all'}")
        print(f"    Est. USASpending calls: {args.max_pages}")
        usa_calls += args.max_pages

    if "incumbents" in reports:
        lookback = config["analysis"]["incumbent_lookback_years"]
        print(f"\n  INCUMBENT ANALYSIS (USASpending — no key needed)")
        print(f"    Lookback: {lookback} years")
        print(f"    Max pages: {args.max_pages}")
        print(f"    Vendor filter: {args.vendor or 'none'}")
        print(f"    State: {args.state or 'all'}")
        print(f"    Est. USASpending calls: {args.max_pages}")
        usa_calls += args.max_pages

    if "small-contracts" in reports:
        sa = config.get("simplified_acquisition", {})
        sc_min = args.min_value or sa.get("small_contract_min", 10000)
        sc_max = args.max_value or sa.get("small_contract_max", 350000)
        fiscal_years = [int(y) for y in args.fiscal_years.split(",")] if args.fiscal_years else config["analysis"]["fiscal_years"]
        print(f"\n  SMALL CONTRACTS (USASpending — no key needed)")
        print(f"    Dollar range: ${sc_min:,.0f} - ${sc_max:,.0f}")
        print(f"    Fiscal years: {fiscal_years}")
        print(f"    State: {args.state or 'all'}")
        print(f"    Agency: {args.agency_name or 'all'}")
        print(f"    Est. USASpending calls: {len(fiscal_years) * args.max_pages}")
        usa_calls += len(fiscal_years) * args.max_pages

    if "fema" in reports:
        fema_name = config.get("fema", {}).get("agency_name", "Federal Emergency Management Agency")
        fiscal_years = [int(y) for y in args.fiscal_years.split(",")] if args.fiscal_years else config["analysis"]["fiscal_years"]
        print(f"\n  FEMA FOOD PROCUREMENT (USASpending — no key needed)")
        print(f"    Agency: {fema_name}")
        print(f"    Fiscal years: {fiscal_years}")
        print(f"    State: {args.state or 'all'}")
        print(f"    Est. USASpending calls: {len(fiscal_years) * args.max_pages}")
        usa_calls += len(fiscal_years) * args.max_pages

    if "opportunities" in reports:
        n_types = 7  # p, o, r, k, a, s, i
        print(f"\n  OPPORTUNITY PIPELINE (SAM.gov — needs SAM_API_KEY)")
        print(f"    NAICS codes: {len(naics_codes)} x {n_types} ptypes = {len(naics_codes) * n_types} requests")
        print(f"    Agency filter: {args.agency_name or 'none'}")
        print(f"    Est. SAM calls: {len(naics_codes) * n_types}")
        sam_calls += len(naics_codes) * n_types

    if "market-size" in reports:
        fiscal_years = [int(y) for y in args.fiscal_years.split(",")] if args.fiscal_years else config["analysis"]["fiscal_years"]
        print(f"\n  MARKET SIZING (USASpending — no key needed)")
        print(f"    Fiscal years: {fiscal_years}")
        print(f"    NAICS prefixes: {naics_prefixes}")
        print(f"    Est. USASpending calls: {len(fiscal_years) * 2} (by-NAICS + by-agency per FY)")
        usa_calls += len(fiscal_years) * 2

    if "competitors" in reports:
        comp_states = [s.strip() for s in args.states.split(",")] if args.states else config.get("target_states", ["FL", "GA", "AL", "SC", "NC"])
        print(f"\n  COMPETITOR REGISTRY (SAM.gov Entity API — needs SAM_API_KEY)")
        print(f"    NAICS codes: {len(naics_codes)}")
        print(f"    States: {comp_states}")
        n_entity_queries = len(naics_codes) * len(comp_states)
        print(f"    Est. SAM Entity calls: {n_entity_queries} combos x ~20 pages = ~{n_entity_queries * 20}")
        sam_calls += n_entity_queries * 20

    if "analytics" in reports:
        fiscal_years = [int(y) for y in args.fiscal_years.split(",")] if args.fiscal_years else config["analysis"]["fiscal_years"]
        print(f"\n  COMPUTED ANALYTICS (USASpending — no key needed)")
        print(f"    Fiscal years: {fiscal_years}")
        print(f"    State focus: {args.state or 'all'}")
        print(f"    Sub-reports: trends (monthly), geography (state), recipients (top 50)")
        n_analytics = len(fiscal_years) * 3  # trends + geo + recipients per FY
        print(f"    Est. USASpending calls: {n_analytics}")
        usa_calls += n_analytics

    if "grants" in reports:
        print(f"\n  GRANTS PIPELINE (Grants.gov — no key needed)")
        print(f"    Keywords: 14 food-specific + 3 broad")
        print(f"    Funding category: AR (Agriculture)")
        print(f"    Est. Grants.gov calls: ~17")

    fpds_calls = 0
    if "competition-density" in reports:
        fiscal_years = [int(y) for y in args.fiscal_years.split(",")] if args.fiscal_years else config["analysis"]["fiscal_years"]
        print(f"\n  COMPETITION DENSITY (FPDS ATOM Feed — no key needed)")
        print(f"    Fiscal years: {fiscal_years}")
        print(f"    NAICS codes: {len(naics_codes)}")
        print(f"    Min obligated amount: ${args.min_value if args.min_value > 0 else 25000:,.0f}")
        print(f"    State: {args.state or 'all'}")
        fpds_est = len(naics_codes) * len(fiscal_years)
        print(f"    Est. FPDS queries: {fpds_est} (1 per NAICS per FY, auto-paginated)")
        fpds_calls = fpds_est

    print(f"\n  RATE LIMIT ESTIMATE")
    print(f"    SAM.gov calls: ~{sam_calls} (limit: 1,000/day, needs SAM_API_KEY)")
    print(f"    USASpending calls: ~{usa_calls} (unlimited, no key needed)")
    if fpds_calls:
        print(f"    FPDS calls: ~{fpds_calls} (unlimited, no key needed)")
    print(f"    Cache: {'disabled' if args.no_cache else 'enabled (24hr TTL)'}")
    if sam_calls > 0:
        print(f"    Note: Only the 'opportunities' and 'competitors' reports need a SAM API key")


# =============================================================================
# Main
# =============================================================================

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(
        description="Government contract intelligence pipeline for federal food procurement"
    )
    parser.add_argument(
        "--report", required=True,
        choices=["expiring", "incumbents", "opportunities", "market-size", "small-contracts", "fema", "competitors", "analytics", "grants", "competition-density", "all"],
        help="Report to generate",
    )
    parser.add_argument(
        "--naics-scope", default="primary", choices=["primary", "all"],
        help="NAICS code scope: primary (10 food wholesale) or all (+ food manufacturing)",
    )
    parser.add_argument(
        "--months-ahead", type=int, default=12,
        help="Months to look ahead for expiring contracts (default: 12)",
    )
    parser.add_argument(
        "--fiscal-years", default="",
        help="Comma-separated fiscal years for reports (default: from config)",
    )
    parser.add_argument(
        "--max-pages", type=int, default=10,
        help="Max pages to fetch per query (default: 10, 100 results/page)",
    )
    parser.add_argument(
        "--state", default="",
        help="2-letter state code for place of performance filter (e.g., FL)",
    )
    parser.add_argument(
        "--agency-name", default="",
        help="Agency subtier name filter (e.g., 'Federal Emergency Management Agency')",
    )
    parser.add_argument(
        "--vendor", default="",
        help="Filter incumbent analysis to a specific vendor (substring match)",
    )
    parser.add_argument(
        "--min-value", type=float, default=0,
        help="Minimum contract value in dollars (default: 0)",
    )
    parser.add_argument(
        "--max-value", type=float, default=0,
        help="Maximum contract value in dollars (default: 0 = no limit)",
    )
    parser.add_argument(
        "--states", default="",
        help="Comma-separated state codes for competitor registry (e.g., FL,GA,AL)",
    )
    parser.add_argument(
        "--no-cache", action="store_true",
        help="Skip cache and fetch fresh data",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show query parameters and rate limit estimate without calling APIs",
    )
    parser.add_argument(
        "--score", action="store_true",
        help="Score opportunities through bid/no-bid framework (use with --report opportunities)",
    )

    # Keep --agency as a hidden alias for backward compatibility
    parser.add_argument("--agency", default="", help=argparse.SUPPRESS)

    args = parser.parse_args()

    # Merge --agency into --agency-name for backward compat
    if args.agency and not args.agency_name:
        args.agency_name = args.agency

    config = load_config()
    use_cache = config["cache"]["enabled"] and not args.no_cache

    if args.dry_run:
        dry_run(config, args)
        return

    all_reports = ["expiring", "incumbents", "opportunities", "market-size", "small-contracts", "fema", "competitors", "analytics", "grants", "competition-density"]
    reports = [args.report] if args.report != "all" else all_reports

    fiscal_years = (
        [int(y) for y in args.fiscal_years.split(",")]
        if args.fiscal_years
        else config["analysis"]["fiscal_years"]
    )

    max_val = args.max_value if args.max_value > 0 else None

    for report in reports:
        if report == "expiring":
            df = report_expiring_contracts(
                config,
                naics_scope=args.naics_scope,
                months_ahead=args.months_ahead,
                max_pages=args.max_pages,
                min_value=args.min_value,
                max_value=max_val,
                agency_name=args.agency_name,
                state=args.state,
                use_cache=use_cache,
            )
            if not df.empty:
                path = save_results(df, "expiring_contracts")
                print(f"\n  Saved {len(df)} records to {path}")
                print_summary(df, "Expiring Contracts")

        elif report == "incumbents":
            df = report_incumbent_analysis(
                config,
                naics_scope=args.naics_scope,
                max_pages=args.max_pages,
                vendor_filter=args.vendor,
                state=args.state,
                agency_name=args.agency_name,
                use_cache=use_cache,
            )
            if not df.empty:
                path = save_results(df, "incumbent_analysis")
                print(f"\n  Saved {len(df)} records to {path}")
                print_summary(df, "Incumbent Analysis")

        elif report == "small-contracts":
            df = report_small_contracts(
                config,
                naics_scope=args.naics_scope,
                fiscal_years=fiscal_years,
                max_pages=args.max_pages,
                state=args.state,
                agency_name=args.agency_name,
                min_value=args.min_value if args.min_value > 0 else None,
                max_value=max_val,
                use_cache=use_cache,
            )
            if not df.empty:
                suffix = f"small_contracts_{args.state.lower()}" if args.state else "small_contracts_nationwide"
                path = save_results(df, suffix)
                print(f"\n  Saved {len(df)} records to {path}")
                print_summary(df, f"Small Contracts{' (' + args.state + ')' if args.state else ' (Nationwide)'}")

        elif report == "fema":
            df = report_fema_contracts(
                config,
                naics_scope=args.naics_scope,
                fiscal_years=fiscal_years,
                max_pages=args.max_pages,
                state=args.state,
                use_cache=use_cache,
            )
            if not df.empty:
                path = save_results(df, "fema_contracts")
                print(f"\n  Saved {len(df)} records to {path}")
                print_summary(df, "FEMA Food Procurement")

        elif report == "opportunities":
            try:
                df = report_opportunity_pipeline(
                    config,
                    naics_scope=args.naics_scope,
                    max_pages=args.max_pages,
                    agency_filter=args.agency_name,
                    use_cache=use_cache,
                )
                if not df.empty:
                    if args.score:
                        from scoring.bid_scorer import score_opportunities_batch, format_scorecard
                        print(f"\n  Scoring {len(df)} opportunities...")
                        opps = df.to_dict("records")
                        scored = score_opportunities_batch(opps, config=config)
                        scored.sort(key=lambda x: x.get("bid_score", 0), reverse=True)
                        for item in scored[:5]:
                            result = item.pop("_score_result", None)
                            if result:
                                print(format_scorecard(result, item))
                        for item in scored[5:]:
                            item.pop("_score_result", None)
                        df = pd.DataFrame(scored)
                    path = save_results(df, "opportunity_pipeline")
                    print(f"\n  Saved {len(df)} records to {path}")
                    print_summary(df, "Opportunity Pipeline")
            except ValueError as e:
                print(f"\n  SKIPPED: opportunities report — {e}")
                print("  Set SAM_API_KEY in .env to enable this report.")

        elif report == "market-size":
            df_naics, df_agency = report_market_sizing(
                config,
                naics_scope=args.naics_scope,
                fiscal_years=fiscal_years,
            )
            if not df_naics.empty:
                path = save_results(df_naics, "market_size_by_naics")
                print(f"\n  Saved {len(df_naics)} NAICS records to {path}")
            if not df_agency.empty:
                path = save_results(df_agency, "market_size_by_agency")
                print(f"  Saved {len(df_agency)} agency records to {path}")

            # Print totals per FY
            if not df_naics.empty:
                print(f"\n{'='*70}")
                print(f"REPORT: Market Sizing")
                print(f"{'='*70}")
                for fy in df_naics["fiscal_year"].unique():
                    fy_total = df_naics[df_naics["fiscal_year"] == fy]["amount"].sum()
                    print(f"  {fy}: ${fy_total:,.0f} total federal food procurement spend")

        elif report == "competitors":
            try:
                comp_states = [s.strip() for s in args.states.split(",")] if args.states else None
                df = report_competitor_registry(
                    config,
                    naics_scope=args.naics_scope,
                    states=comp_states,
                    max_pages_per_query=args.max_pages,
                    use_cache=use_cache,
                )
                if not df.empty:
                    path = save_results(df, "competitor_registry")
                    print(f"\n  Saved {len(df)} records to {path}")
                    print_summary(df, "Competitor Registry")
            except ValueError as e:
                print(f"\n  SKIPPED: competitors report — {e}")
                print("  Set SAM_API_KEY in .env to enable this report.")

        elif report == "analytics":
            df_trends, df_geo, df_recipients = report_analytics(
                config,
                naics_scope=args.naics_scope,
                fiscal_years=fiscal_years,
                state=args.state,
                use_cache=use_cache,
            )
            if not df_trends.empty:
                path = save_results(df_trends, "analytics_trends")
                print(f"\n  Saved {len(df_trends)} trend records to {path}")
            if not df_geo.empty:
                path = save_results(df_geo, "analytics_geography")
                print(f"  Saved {len(df_geo)} geography records to {path}")
            if not df_recipients.empty:
                path = save_results(df_recipients, "analytics_recipients")
                print(f"  Saved {len(df_recipients)} recipient records to {path}")

        elif report == "grants":
            df = report_grants_pipeline(
                config,
                use_cache=use_cache,
            )
            if not df.empty:
                path = save_results(df, "grants_pipeline")
                print(f"\n  Saved {len(df)} records to {path}")
                print_summary(df, "Grants Pipeline")

        elif report == "competition-density":
            df_transactions, df_density = report_competition_density(
                config,
                naics_scope=args.naics_scope,
                fiscal_years=fiscal_years,
                state=args.state,
                min_value=args.min_value if args.min_value > 0 else 25000,
                use_cache=use_cache,
            )
            if not df_transactions.empty:
                path = save_results(df_transactions, "fpds_transactions")
                print(f"\n  Saved {len(df_transactions)} transaction records to {path}")
            if not df_density.empty:
                path = save_results(df_density, "competition_density")
                print(f"  Saved {len(df_density)} density records to {path}")


if __name__ == "__main__":
    main()
