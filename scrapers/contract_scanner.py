"""Government contract intelligence pipeline for federal food procurement.

Produces four reports from free federal APIs:
  - Expiring contracts (SAM.gov Contract Awards)
  - Incumbent analysis (SAM.gov Contract Awards)
  - Opportunity pipeline (SAM.gov Opportunities)
  - Market sizing (USASpending.gov — no SAM key needed)

SAM.gov: 1,000 requests/day. Cache prevents re-fetching within 24hrs.
USASpending: unlimited, no API key needed.

Usage:
    python scrapers/contract_scanner.py --report expiring --dry-run
    python scrapers/contract_scanner.py --report incumbents --max-pages 20
    python scrapers/contract_scanner.py --report opportunities --naics-scope primary
    python scrapers/contract_scanner.py --report market-size --fiscal-years 2023,2024,2025
    python scrapers/contract_scanner.py --report all
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
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

import pandas as pd
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()

from enrichment.sam_client import SAMClient
from enrichment.usaspending_client import USASpendingClient

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
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

    if "agency" in df.columns:
        print(f"\n  Top agencies:")
        for agency, count in df["agency"].value_counts().head(10).items():
            if agency:
                print(f"    {agency}: {count}")

    if "vendor_name" in df.columns:
        unique_vendors = df["vendor_name"].nunique()
        print(f"\n  Unique vendors: {unique_vendors}")
        print(f"  Top vendors:")
        for vendor, count in df["vendor_name"].value_counts().head(10).items():
            if vendor:
                print(f"    {vendor}: {count}")

    if "naics_code" in df.columns:
        print(f"\n  NAICS codes represented:")
        for code, count in df["naics_code"].value_counts().head(10).items():
            if code:
                print(f"    {code}: {count}")


# =============================================================================
# Report: Expiring Contracts
# =============================================================================

def report_expiring_contracts(
    sam: SAMClient,
    config: dict,
    naics_scope: str = "primary",
    months_ahead: int = 12,
    max_pages: int = 10,
    min_value: float = 0,
    agency_filter: str = "",
    use_cache: bool = True,
) -> pd.DataFrame:
    """Find contracts expiring in the next N months.

    Queries SAM Contract Awards with currentCompletionDate range = today to today + N months.
    Groups by PIID, keeps latest modification to get current contract state.
    """
    naics_codes = get_naics_codes(config, naics_scope)
    today = datetime.now()
    future = today + relativedelta(months=months_ahead)

    print(f"\nExpiring Contracts Report")
    print(f"  NAICS codes: {len(naics_codes)} ({naics_scope} scope)")
    print(f"  Window: {today.strftime('%m/%d/%Y')} to {future.strftime('%m/%d/%Y')}")
    print(f"  Max pages: {max_pages}")

    # Check cache
    ck = cache_key({
        "report": "expiring",
        "naics": naics_codes,
        "from": today.strftime("%m/%d/%Y"),
        "to": future.strftime("%m/%d/%Y"),
        "max_pages": max_pages,
    })

    cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
    if cached is not None:
        print(f"  Using cached data ({len(cached)} records)")
        all_awards = cached
    else:
        all_awards = sam.search_contract_awards_all_pages(
            naics_codes=naics_codes,
            current_completion_from=today.strftime("%m/%d/%Y"),
            current_completion_to=future.strftime("%m/%d/%Y"),
            max_pages=max_pages,
        )
        if use_cache and all_awards:
            write_cache(ck, all_awards)

    if not all_awards:
        print("  No expiring contracts found.")
        return pd.DataFrame()

    # Flatten and process
    records = [SAMClient.flatten_award(a) for a in all_awards]
    df = pd.DataFrame(records)

    # Calculate months until expiry
    if "current_completion_date" in df.columns:
        df["current_completion_date_parsed"] = pd.to_datetime(
            df["current_completion_date"], format="mixed", errors="coerce"
        )
        df["months_until_expiry"] = df["current_completion_date_parsed"].apply(
            lambda d: round((d - today).days / 30.44, 1) if pd.notna(d) else None
        )
        df.drop(columns=["current_completion_date_parsed"], inplace=True)

    # Option years remaining (gap between current and ultimate completion dates)
    if "ultimate_completion_date" in df.columns and "current_completion_date" in df.columns:
        curr = pd.to_datetime(df["current_completion_date"], format="mixed", errors="coerce")
        ult = pd.to_datetime(df["ultimate_completion_date"], format="mixed", errors="coerce")
        df["option_years_remaining"] = ((ult - curr).dt.days / 365.25).round(1)
        df["option_years_remaining"] = df["option_years_remaining"].clip(lower=0)

    # Map competition levels
    comp_map = config["analysis"]["competition_level_map"]
    if "extent_competed" in df.columns:
        df["competition_level"] = df["extent_competed"].map(comp_map).fillna(df["extent_competed"])

    # Filter by min value
    if min_value and "dollars_obligated" in df.columns:
        df["dollars_obligated"] = pd.to_numeric(df["dollars_obligated"], errors="coerce")
        df = df[df["dollars_obligated"] >= min_value]

    # Filter by agency
    if agency_filter and "agency" in df.columns:
        df = df[df["agency"].str.contains(agency_filter, case=False, na=False)]

    # Sort by months until expiry
    if "months_until_expiry" in df.columns:
        df = df.sort_values("months_until_expiry", ascending=True)

    return df


# =============================================================================
# Report: Incumbent Analysis
# =============================================================================

def report_incumbent_analysis(
    sam: SAMClient,
    config: dict,
    naics_scope: str = "primary",
    max_pages: int = 10,
    vendor_filter: str = "",
    use_cache: bool = True,
) -> pd.DataFrame:
    """Analyze incumbent vendors in federal food procurement.

    Pulls base awards for the last 5 years with food NAICS codes.
    Groups by vendor: count contracts, sum value, avg offers, % sole-source.
    """
    naics_codes = get_naics_codes(config, naics_scope)
    lookback = config["analysis"]["incumbent_lookback_years"]
    today = datetime.now()
    start = today - relativedelta(years=lookback)

    print(f"\nIncumbent Analysis Report")
    print(f"  NAICS codes: {len(naics_codes)} ({naics_scope} scope)")
    print(f"  Lookback: {lookback} years ({start.strftime('%m/%d/%Y')} to {today.strftime('%m/%d/%Y')})")
    print(f"  Max pages: {max_pages}")

    # Check cache
    ck = cache_key({
        "report": "incumbents",
        "naics": naics_codes,
        "from": start.strftime("%m/%d/%Y"),
        "to": today.strftime("%m/%d/%Y"),
        "max_pages": max_pages,
    })

    cached = read_cache(ck, config["cache"]["ttl_hours"]) if use_cache else None
    if cached is not None:
        print(f"  Using cached data ({len(cached)} records)")
        all_awards = cached
    else:
        all_awards = sam.search_contract_awards_all_pages(
            naics_codes=naics_codes,
            date_signed_from=start.strftime("%m/%d/%Y"),
            date_signed_to=today.strftime("%m/%d/%Y"),
            max_pages=max_pages,
        )
        if use_cache and all_awards:
            write_cache(ck, all_awards)

    if not all_awards:
        print("  No awards found for incumbent analysis.")
        return pd.DataFrame()

    # Flatten
    records = [SAMClient.flatten_award(a) for a in all_awards]
    df = pd.DataFrame(records)

    if df.empty or "vendor_name" not in df.columns:
        return pd.DataFrame()

    # Parse numeric fields
    df["dollars_obligated"] = pd.to_numeric(df.get("dollars_obligated", 0), errors="coerce").fillna(0)
    df["number_of_offers"] = pd.to_numeric(df.get("number_of_offers", 0), errors="coerce").fillna(0)

    # Determine if competed
    comp_map = config["analysis"]["competition_level_map"]
    sole_source_codes = {"B", "C", "G", "NDO"}
    df["is_sole_source"] = df["extent_competed"].isin(sole_source_codes)

    # Group by vendor
    grouped = df.groupby("vendor_name").agg(
        total_contracts=("piid", "count"),
        total_value=("dollars_obligated", "sum"),
        avg_value=("dollars_obligated", "mean"),
        avg_offers=("number_of_offers", "mean"),
        sole_source_count=("is_sole_source", "sum"),
        agencies=("agency", lambda x: ", ".join(sorted(set(s for s in x if s))[:5])),
        top_naics=("naics_code", lambda x: x.mode().iloc[0] if not x.mode().empty else ""),
        most_recent=("date_signed", "max"),
    ).reset_index()

    grouped["pct_competed"] = (
        (1 - grouped["sole_source_count"] / grouped["total_contracts"]) * 100
    ).round(1)
    grouped["avg_value"] = grouped["avg_value"].round(0)
    grouped["avg_offers"] = grouped["avg_offers"].round(1)

    # Sort by total value descending
    grouped = grouped.sort_values("total_value", ascending=False)

    # Rename for output
    grouped = grouped.rename(columns={
        "agencies": "agencies_served",
        "most_recent": "most_recent_award",
    })

    # Drop helper column
    grouped = grouped.drop(columns=["sole_source_count"], errors="ignore")

    # Filter by vendor name
    if vendor_filter:
        grouped = grouped[grouped["vendor_name"].str.contains(vendor_filter, case=False, na=False)]

    return grouped


# =============================================================================
# Report: Opportunity Pipeline
# =============================================================================

def report_opportunity_pipeline(
    sam: SAMClient,
    config: dict,
    naics_scope: str = "primary",
    max_pages: int = 10,
    agency_filter: str = "",
    use_cache: bool = True,
) -> pd.DataFrame:
    """Find active solicitations, pre-solicitations, and sources sought.

    Searches across all food NAICS codes and deduplicates by noticeId.
    This is the most expensive report: 1 request per NAICS x ptype combo.
    """
    naics_codes = get_naics_codes(config, naics_scope)
    today = datetime.now()
    # Look back 90 days for recently posted opportunities
    posted_from = (today - timedelta(days=90)).strftime("%m/%d/%Y")

    print(f"\nOpportunity Pipeline Report")
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

    return df


# =============================================================================
# Report: Market Sizing
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

    print(f"\nMarket Sizing Report")
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
# Dry Run
# =============================================================================

def dry_run(config: dict, args) -> None:
    """Show what would be queried without making API calls."""
    naics_codes = get_naics_codes(config, args.naics_scope)
    naics_prefixes = get_naics_prefixes(config, args.naics_scope)

    reports = [args.report] if args.report != "all" else [
        "expiring", "incumbents", "opportunities", "market-size"
    ]

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
        print(f"\n  EXPIRING CONTRACTS")
        print(f"    Window: {today.strftime('%m/%d/%Y')} to {future.strftime('%m/%d/%Y')}")
        print(f"    Max pages: {args.max_pages}")
        print(f"    Min value: ${args.min_value:,.0f}" if args.min_value else "    Min value: none")
        print(f"    Agency filter: {args.agency or 'none'}")
        print(f"    Est. SAM calls: {args.max_pages} (NAICS codes batched in single request)")
        sam_calls += args.max_pages

    if "incumbents" in reports:
        lookback = config["analysis"]["incumbent_lookback_years"]
        print(f"\n  INCUMBENT ANALYSIS")
        print(f"    Lookback: {lookback} years")
        print(f"    Max pages: {args.max_pages}")
        print(f"    Vendor filter: {args.vendor or 'none'}")
        print(f"    Est. SAM calls: {args.max_pages}")
        sam_calls += args.max_pages

    if "opportunities" in reports:
        n_types = 4  # p, o, r, k
        print(f"\n  OPPORTUNITY PIPELINE")
        print(f"    NAICS codes: {len(naics_codes)} x {n_types} ptypes = {len(naics_codes) * n_types} requests")
        print(f"    Agency filter: {args.agency or 'none'}")
        print(f"    Est. SAM calls: {len(naics_codes) * n_types}")
        sam_calls += len(naics_codes) * n_types

    if "market-size" in reports:
        fiscal_years = [int(y) for y in args.fiscal_years.split(",")] if args.fiscal_years else config["analysis"]["fiscal_years"]
        print(f"\n  MARKET SIZING (USASpending — no SAM key needed)")
        print(f"    Fiscal years: {fiscal_years}")
        print(f"    NAICS prefixes: {naics_prefixes}")
        print(f"    Est. USASpending calls: {len(fiscal_years) * 2} (by-NAICS + by-agency per FY)")
        usa_calls += len(fiscal_years) * 2

    print(f"\n  RATE LIMIT ESTIMATE")
    print(f"    SAM.gov calls: ~{sam_calls} (limit: 1,000/day)")
    print(f"    USASpending calls: ~{usa_calls} (unlimited)")
    print(f"    Cache: {'disabled' if args.no_cache else 'enabled (24hr TTL)'}")
    if sam_calls > 0:
        print(f"    SAM budget remaining after run: ~{1000 - sam_calls}")


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
        choices=["expiring", "incumbents", "opportunities", "market-size", "all"],
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
        help="Comma-separated fiscal years for market sizing (default: from config)",
    )
    parser.add_argument(
        "--max-pages", type=int, default=10,
        help="Max pages to fetch per SAM query (default: 10)",
    )
    parser.add_argument(
        "--agency", default="",
        help="Filter results to a specific agency (substring match)",
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
        "--no-cache", action="store_true",
        help="Skip cache and fetch fresh data",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show query parameters and rate limit estimate without calling APIs",
    )
    args = parser.parse_args()

    config = load_config()
    use_cache = config["cache"]["enabled"] and not args.no_cache

    if args.dry_run:
        dry_run(config, args)
        return

    reports = [args.report] if args.report != "all" else [
        "expiring", "incumbents", "opportunities", "market-size"
    ]

    # SAM client needed for everything except market-size
    sam = None
    needs_sam = any(r in reports for r in ["expiring", "incumbents", "opportunities"])
    if needs_sam:
        sam = SAMClient()

    fiscal_years = (
        [int(y) for y in args.fiscal_years.split(",")]
        if args.fiscal_years
        else config["analysis"]["fiscal_years"]
    )

    for report in reports:
        if report == "expiring":
            df = report_expiring_contracts(
                sam, config,
                naics_scope=args.naics_scope,
                months_ahead=args.months_ahead,
                max_pages=args.max_pages,
                min_value=args.min_value,
                agency_filter=args.agency,
                use_cache=use_cache,
            )
            if not df.empty:
                path = save_results(df, "expiring_contracts")
                print(f"\n  Saved {len(df)} records to {path}")
                print_summary(df, "Expiring Contracts")

        elif report == "incumbents":
            df = report_incumbent_analysis(
                sam, config,
                naics_scope=args.naics_scope,
                max_pages=args.max_pages,
                vendor_filter=args.vendor,
                use_cache=use_cache,
            )
            if not df.empty:
                path = save_results(df, "incumbent_analysis")
                print(f"\n  Saved {len(df)} records to {path}")
                print_summary(df, "Incumbent Analysis")

        elif report == "opportunities":
            df = report_opportunity_pipeline(
                sam, config,
                naics_scope=args.naics_scope,
                max_pages=args.max_pages,
                agency_filter=args.agency,
                use_cache=use_cache,
            )
            if not df.empty:
                path = save_results(df, "opportunity_pipeline")
                print(f"\n  Saved {len(df)} records to {path}")
                print_summary(df, "Opportunity Pipeline")

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

    if sam:
        print(f"\nSAM.gov API stats: {sam.stats}")


if __name__ == "__main__":
    main()
