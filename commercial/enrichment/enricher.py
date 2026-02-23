"""Automated lead enrichment pipeline using Apollo.io.

Replaces the manual Clay upload/enrich/export workflow with a single function call.

Usage:
    python -m enrichment.enricher --input data/raw/businesses_real_estate_agents_20260214.csv --icp-type real_estate_agents
    python -m enrichment.enricher --input data/raw/businesses_real_estate_agents_20260214.csv --icp-type real_estate_agents --dry-run
"""

import argparse
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd

from commercial.enrichment.apollo_client import ApolloClient, domain_from_url

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENRICHED_DIR = PROJECT_ROOT / "data" / "enriched"


def enrich_businesses(
    df: pd.DataFrame,
    icp_type: str,
    client: ApolloClient,
    skip_existing_email: bool = True,
) -> pd.DataFrame:
    """Enrich a business DataFrame with decision-maker contacts via Apollo.

    Adds columns: dm_first_name, dm_last_name, dm_title, dm_email, dm_linkedin
    Preserves all existing columns.

    Args:
        df: Raw business DataFrame (from gmaps_scraper output)
        icp_type: ICP category for title matching
        client: Initialized ApolloClient
        skip_existing_email: Skip enrichment if row already has a dm_email
    """
    # Initialize new columns
    for col in ["dm_first_name", "dm_last_name", "dm_title", "dm_email", "dm_linkedin"]:
        if col not in df.columns:
            df[col] = ""

    total = len(df)
    enriched_count = 0
    skipped = 0
    failed = 0

    for idx, row in df.iterrows():
        i = df.index.get_loc(idx) + 1
        company = row.get("name", "") or row.get("company_name", "")
        website = row.get("website", "")

        # Skip if already enriched
        if skip_existing_email and row.get("dm_email"):
            skipped += 1
            continue

        print(f"  [{i}/{total}] {company}...", end=" ", flush=True)

        try:
            result = client.find_decision_maker(
                company_name=company,
                website=website,
                icp_type=icp_type,
            )
        except Exception as e:
            log.warning(f"Failed to enrich {company}: {e}")
            print(f"ERROR: {e}")
            failed += 1
            continue

        df.at[idx, "dm_first_name"] = result["first_name"]
        df.at[idx, "dm_last_name"] = result["last_name"]
        df.at[idx, "dm_title"] = result["title"]
        df.at[idx, "dm_email"] = result["email"]
        df.at[idx, "dm_linkedin"] = result["linkedin_url"]

        if result["email"]:
            enriched_count += 1
            print(f"{result['first_name']} {result['last_name']} ({result['title']}) — {result['email']}")
        elif result["first_name"]:
            enriched_count += 1
            print(f"{result['first_name']} {result['last_name']} ({result['title']}) — no email found")
        else:
            print("no match")
            failed += 1

        # Small delay between requests to be respectful
        if i < total:
            time.sleep(0.5)

    print(f"\n  Enrichment complete: {enriched_count} found, {failed} no match, {skipped} skipped")
    print(f"  Apollo API stats: {client.stats}")

    return df


def enrich_homeowners(
    df: pd.DataFrame,
    icp_type: str,
    client: ApolloClient,
) -> pd.DataFrame:
    """Enrich homeowner DataFrame with owner contact info via Apollo.

    For homeowners we search by name (from listing agent) or address.
    This is lower hit-rate than businesses since homeowners aren't in B2B databases.
    Returns DataFrame with added dm_email column where found.
    """
    # Homeowner enrichment is limited via Apollo (B2B database).
    # For now, pass through — homeowners are better enriched via
    # property records or direct mail.
    log.info("Homeowner enrichment via Apollo is limited — B2B database has low coverage for individuals.")
    log.info("Recommend using property records or direct mail for homeowner outreach.")
    return df


def save_enriched(df: pd.DataFrame, icp_type: str, output_dir: Path = ENRICHED_DIR) -> Path:
    """Save enriched DataFrame to CSV."""
    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    path = output_dir / f"{icp_type}_{date_str}.csv"
    df.to_csv(path, index=False)
    return path


def print_enrichment_summary(df: pd.DataFrame, icp_type: str) -> None:
    """Print enrichment quality metrics."""
    total = len(df)
    has_dm_email = (df.get("dm_email", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()
    has_dm_name = (df.get("dm_first_name", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()
    has_phone = (df.get("phone", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()
    has_website = (df.get("website", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()

    print(f"\n{'='*60}")
    print(f"Enrichment Summary: {icp_type}")
    print(f"{'='*60}")
    print(f"  Total leads:         {total}")
    print(f"  Decision maker found: {has_dm_name} ({has_dm_name/total*100:.0f}%)")
    print(f"  Email found:          {has_dm_email} ({has_dm_email/total*100:.0f}%)")
    print(f"  Phone (from GMaps):   {has_phone} ({has_phone/total*100:.0f}%)")
    print(f"  Website:              {has_website} ({has_website/total*100:.0f}%)")

    # Reachability: has email OR phone
    reachable = ((df.get("dm_email", pd.Series(dtype=str)).fillna("").str.len() > 0) |
                 (df.get("phone", pd.Series(dtype=str)).fillna("").str.len() > 0)).sum()
    print(f"  Reachable (email|phone): {reachable} ({reachable/total*100:.0f}%)")

    if "market" in df.columns:
        print(f"\n  By market:")
        for market, group in df.groupby("market"):
            m_email = (group.get("dm_email", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()
            print(f"    {market}: {len(group)} leads, {m_email} emails ({m_email/len(group)*100:.0f}%)")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(description="Enrich leads via Apollo.io API")
    parser.add_argument("--input", required=True, help="Path to raw CSV (from gmaps_scraper or clay_ready)")
    parser.add_argument("--icp-type", required=True, help="ICP category (e.g. real_estate_agents)")
    parser.add_argument("--output-dir", default=str(ENRICHED_DIR), help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be enriched without calling API")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}")
        sys.exit(1)

    df = pd.read_csv(input_path)
    print(f"Loaded {len(df)} rows from {input_path}")

    if args.dry_run:
        has_website = (df.get("website", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()
        has_phone = (df.get("phone", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()
        print(f"\nDry run — would enrich {len(df)} businesses:")
        print(f"  {has_website} have websites (domain lookup)")
        print(f"  {has_phone} already have phone numbers")
        print(f"  Estimated Apollo credits: {len(df)} email credits (people search is free)")
        print(f"  Estimated time: ~{len(df) * 2 // 60} minutes")
        return

    client = ApolloClient()
    output_dir = Path(args.output_dir)

    print(f"\nEnriching {args.icp_type} ({len(df)} leads)...")
    df = enrich_businesses(df, args.icp_type, client)

    path = save_enriched(df, args.icp_type, output_dir)
    print(f"\nSaved to {path}")

    print_enrichment_summary(df, args.icp_type)


if __name__ == "__main__":
    main()
