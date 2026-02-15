"""Enterprise prospect sourcing via Apollo.io People Search API.

Uses org keyword tags + title contains matching + seniority/size filters to find
senior decision makers at enterprise grocery retailers, manufacturers, and distributors.

Apollo People Search is FREE (0 credits). Email reveal costs 1 credit each.

Usage:
    python scrapers/apollo_prospector.py --segment segment_a_buyers --dry-run
    python scrapers/apollo_prospector.py --segment all --region united_states --max-pages 10
    python scrapers/apollo_prospector.py --segment all --reveal-emails --max-reveals 100
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from enrichment.apollo_client import ApolloClient

log = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "icp_definitions.json"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
ENRICHED_DIR = PROJECT_ROOT / "data" / "enriched"


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


def flatten_locations(config: dict, region_filter: str | None = None) -> list[str]:
    """Get all Apollo location strings from geography config, optionally filtered."""
    geo = config.get("geography", {})
    included = geo.get("included_regions", {})
    excluded_countries = set(geo.get("excluded_countries", []))

    locations = []
    for region_key, region_data in included.items():
        if region_filter and region_key != region_filter:
            continue
        for loc in region_data.get("apollo_locations", []):
            if loc not in excluded_countries:
                locations.append(loc)

    return locations


def title_matches_include(title: str, include_keywords: list[str]) -> bool:
    """Check if a title contains at least one inclusion keyword."""
    if not title or not include_keywords:
        return True  # no filter = pass through
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in include_keywords)


def title_matches_exclude(title: str, exclude_keywords: list[str]) -> bool:
    """Check if a title matches any exclusion keyword."""
    if not title or not exclude_keywords:
        return False
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in exclude_keywords)


def search_segment(
    client: ApolloClient,
    segment_key: str,
    segment_cfg: dict,
    locations: list[str],
    max_pages: int = 10,
    per_page: int = 100,
) -> pd.DataFrame:
    """Run enterprise people search using org keyword tags + title fuzzy matching.

    Apollo's person_titles does fuzzy/contains matching, so passing "procurement"
    matches "Director of Procurement", "VP Procurement", etc.

    Uses q_organization_keyword_tags to filter to food/grocery industry companies.
    """
    title_include = segment_cfg.get("title_include_keywords", [])
    title_exclude = segment_cfg.get("title_exclude_keywords", [])
    seniorities = segment_cfg.get("target_seniorities", ["director", "vp", "c_suite"])
    employee_ranges = segment_cfg.get("apollo_employee_ranges", [])
    revenue_ranges = segment_cfg.get("apollo_revenue_ranges", [])
    org_keyword_tags = segment_cfg.get("apollo_organization_keyword_tags", [])

    all_records = []
    seen_ids = set()
    excluded_by_title = 0

    # Use title include keywords as the person_titles filter (Apollo does fuzzy matching)
    # This is the key insight: passing "procurement" to person_titles matches any title
    # containing "procurement" — Director of Procurement, VP Procurement, etc.
    person_titles = title_include

    for page in range(1, max_pages + 1):
        print(f"  Page {page}...", end=" ", flush=True)

        try:
            body = {
                "per_page": per_page,
                "page": page,
                "person_titles": person_titles,
                "person_seniorities": seniorities,
                "organization_locations": locations,
                "organization_num_employees_ranges": employee_ranges,
            }
            if revenue_ranges:
                body["organization_revenue_ranges"] = revenue_ranges
            if org_keyword_tags:
                body["q_organization_keyword_tags"] = org_keyword_tags

            data = client._request("POST", "mixed_people/api_search", json=body)
            people = data.get("people", [])
            pagination = data.get("pagination", {})
            total = pagination.get("total_entries", 0)
        except Exception as e:
            print(f"ERROR: {e}")
            break

        if not people:
            print("no more results")
            break

        new_count = 0
        for person in people:
            pid = person.get("id", "")
            if pid in seen_ids:
                continue
            seen_ids.add(pid)

            title = person.get("title", "")

            # Post-filter: exclude unwanted titles
            if title_matches_exclude(title, title_exclude):
                excluded_by_title += 1
                continue

            org = person.get("organization", {}) or {}
            employment = person.get("employment_history", []) or []
            current_org_name = org.get("name", "") or person.get("organization_name", "")

            record = {
                "apollo_id": pid,
                "first_name": person.get("first_name", ""),
                "last_name": person.get("last_name", ""),
                "title": title,
                "seniority": person.get("seniority", ""),
                "departments": ", ".join(person.get("departments", []) or []),
                "linkedin_url": person.get("linkedin_url", ""),
                "has_email": person.get("has_email", False),
                "email_status": person.get("email_status", ""),
                "city": person.get("city", ""),
                "state": person.get("state", ""),
                "country": person.get("country", ""),
                "company_name": current_org_name,
                "company_domain": org.get("primary_domain", ""),
                "company_website": org.get("website_url", ""),
                "company_linkedin": org.get("linkedin_url", ""),
                "company_industry": org.get("industry", ""),
                "company_employees": org.get("estimated_num_employees"),
                "company_revenue": org.get("annual_revenue"),
                "company_city": org.get("city", ""),
                "company_state": org.get("state", ""),
                "company_country": org.get("country", ""),
                "segment": segment_key,
            }
            all_records.append(record)
            new_count += 1

        if page == 1:
            print(f"{len(people)} results, {new_count} new, ~{total} total available")
        else:
            print(f"{len(people)} results, {new_count} new (cumulative: {len(all_records)})")

        if len(people) < per_page:
            break  # last page

        time.sleep(1)

    if excluded_by_title:
        print(f"\n  Post-filtered {excluded_by_title} prospects by title exclusion rules")

    if not all_records:
        return pd.DataFrame()

    df = pd.DataFrame(all_records)

    # Dedup by apollo_id (already done), then by company_domain + title combo
    before = len(df)
    df = df.drop_duplicates(subset=["company_domain", "title"], keep="first")
    dupes = before - len(df)
    if dupes:
        print(f"  Deduped {dupes} records (same company domain + title)")

    return df


def reveal_emails(client: ApolloClient, df: pd.DataFrame, max_reveals: int = 100) -> pd.DataFrame:
    """Reveal emails for prospects that have email available. Costs 1 credit each."""
    df["email"] = ""

    has_email = df[df["has_email"] == True]
    to_reveal = has_email.head(max_reveals)

    print(f"\n  Revealing emails for {len(to_reveal)} prospects (of {len(has_email)} with email available)...")

    revealed = 0
    for idx, row in to_reveal.iterrows():
        i = to_reveal.index.get_loc(idx) + 1
        apollo_id = row["apollo_id"]
        name = f"{row['first_name']} {row['last_name']}"
        print(f"    [{i}/{len(to_reveal)}] {name} @ {row['company_name']}...", end=" ", flush=True)

        try:
            enriched = client.enrich_person(apollo_id=apollo_id)
        except Exception as e:
            print(f"ERROR: {e}")
            continue

        if enriched and enriched.get("email"):
            df.at[idx, "email"] = enriched["email"]
            if enriched.get("last_name"):
                df.at[idx, "last_name"] = enriched["last_name"]
            print(f"{enriched['email']}")
            revealed += 1
        else:
            print("no email revealed")

        time.sleep(0.5)

    print(f"\n  Emails revealed: {revealed}/{len(to_reveal)} attempts ({revealed} credits used)")
    return df


def apply_exclusions(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Apply geographic exclusion rules."""
    excluded = set(config.get("geography", {}).get("excluded_countries", []))
    if not excluded:
        return df

    # Check both person country and company country
    before = len(df)
    mask = pd.Series(True, index=df.index)
    for col in ["country", "company_country"]:
        if col in df.columns:
            mask &= ~df[col].isin(excluded)
    df = df[mask]
    removed = before - len(df)
    if removed:
        print(f"  Excluded {removed} prospects from {', '.join(excluded)}")
    return df


def save_results(df: pd.DataFrame, segment: str, output_dir: Path, enriched: bool = False) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    suffix = "_enriched" if enriched else "_raw"
    path = output_dir / f"{segment}{suffix}_{date_str}.csv"
    df.to_csv(path, index=False)
    return path


def print_summary(df: pd.DataFrame, segment: str) -> None:
    total = len(df)
    if total == 0:
        print(f"\n{segment}: 0 prospects found")
        return

    has_email_flag = (df["has_email"] == True).sum()
    has_revealed_email = (df.get("email", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()
    unique_companies = df["company_name"].nunique()

    print(f"\n{'='*70}")
    print(f"RESULTS: {segment}")
    print(f"{'='*70}")
    print(f"  Total prospects:       {total}")
    print(f"  Unique companies:      {unique_companies}")
    print(f"  With email available:  {has_email_flag} ({has_email_flag/total*100:.0f}%)")
    if has_revealed_email:
        print(f"  Emails revealed:       {has_revealed_email}")

    if "company_country" in df.columns:
        countries = df["company_country"].fillna(df.get("country", "")).value_counts().head(15)
        if not countries.empty:
            print(f"\n  By country:")
            for country, count in countries.items():
                if country:
                    print(f"    {country}: {count}")

    if "company_industry" in df.columns:
        industries = df["company_industry"].value_counts().head(10)
        if not industries.empty:
            print(f"\n  By industry:")
            for industry, count in industries.items():
                if industry:
                    print(f"    {industry}: {count}")

    if "title" in df.columns:
        print(f"\n  Top titles:")
        for title, count in df["title"].value_counts().head(15).items():
            print(f"    {title}: {count}")

    if "company_name" in df.columns:
        print(f"\n  Companies found ({min(unique_companies, 25)} shown):")
        for company in df["company_name"].unique()[:25]:
            company_rows = df[df["company_name"] == company]
            emp = company_rows["company_employees"].iloc[0]
            n_contacts = len(company_rows)
            emp_str = f"({emp:,} emp)" if pd.notna(emp) and emp else ""
            company_safe = company.encode("ascii", "replace").decode("ascii")
            print(f"    {company_safe} {emp_str} -- {n_contacts} contact(s)")


def dry_run(config: dict, segments: list[str], region_filter: str | None) -> None:
    locations = flatten_locations(config, region_filter)

    for seg_key in segments:
        seg = config["segments"][seg_key]
        title_include = seg.get("title_include_keywords", [])
        title_exclude = seg.get("title_exclude_keywords", [])
        seniorities = seg.get("target_seniorities", [])
        emp_ranges = seg.get("apollo_employee_ranges", [])
        rev_ranges = seg.get("apollo_revenue_ranges", [])
        org_tags = seg.get("apollo_organization_keyword_tags", [])

        print(f"\n{'='*70}")
        print(f"SEGMENT: {seg['display_name']}")
        print(f"{'='*70}")
        print(f"  Title CONTAINS (any of) — used as person_titles with fuzzy match:")
        for t in title_include:
            print(f"    - \"{t}\"")
        print(f"  Title EXCLUDE keywords:")
        for t in title_exclude:
            print(f"    - \"{t}\"")
        print(f"  Seniority filter: {seniorities}")
        print(f"  Employee ranges: {emp_ranges}")
        print(f"  Revenue ranges: {rev_ranges}")
        print(f"  Org keyword tags ({len(org_tags)}):")
        for tag in org_tags:
            print(f"    - \"{tag}\"")
        print(f"  Locations ({len(locations)}):")
        for loc in locations[:10]:
            print(f"    - {loc}")
        if len(locations) > 10:
            print(f"    ... and {len(locations) - 10} more")

        print(f"\n  Strategy: Single paginated search (up to 100/page, 500 pages max)")
        print(f"  Cost: FREE (People Search = 0 credits)")
        print(f"  Email reveals: 1 credit each (optional)")

    print(f"\n  Total locations: {len(locations)}")
    print(f"  Excluded countries: {config['geography']['excluded_countries']}")


def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(
        description="Source enterprise prospects via Apollo.io People Search"
    )
    parser.add_argument(
        "--segment", required=True,
        help='Segment key (segment_a_buyers, segment_b_suppliers, or "all")',
    )
    parser.add_argument(
        "--region", default=None,
        help="Limit to region (united_states, united_kingdom, eu_eea_switzerland)",
    )
    parser.add_argument(
        "--max-pages", type=int, default=10,
        help="Max pages to fetch (default: 10, each page = 100 results)",
    )
    parser.add_argument(
        "--reveal-emails", action="store_true",
        help="Reveal emails for matched prospects (costs 1 Apollo credit each)",
    )
    parser.add_argument(
        "--max-reveals", type=int, default=100,
        help="Max email reveals per run (default: 100)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show search parameters without calling the API",
    )
    args = parser.parse_args()

    config = load_config()
    segments = config["segments"]

    if args.segment == "all":
        target_segments = list(segments.keys())
    else:
        if args.segment not in segments:
            print(f"Unknown segment: {args.segment}. Options: {', '.join(segments.keys())}, all")
            sys.exit(1)
        target_segments = [args.segment]

    if args.dry_run:
        dry_run(config, target_segments, args.region)
        return

    client = ApolloClient()
    locations = flatten_locations(config, args.region)

    if not locations:
        print("ERROR: No locations found. Check region filter and config.")
        sys.exit(1)

    print(f"Searching {len(locations)} location(s) across {len(target_segments)} segment(s)")
    print(f"Pagination: up to {args.max_pages} pages x 100 results/page")

    for seg_key in target_segments:
        seg_cfg = segments[seg_key]
        print(f"\n{'='*70}")
        print(f"SEGMENT: {seg_cfg['display_name']}")
        print(f"{'='*70}")

        df = search_segment(client, seg_key, seg_cfg, locations, max_pages=args.max_pages)

        if df.empty:
            print(f"\n  No prospects found for {seg_key}")
            continue

        df = apply_exclusions(df, config)

        raw_path = save_results(df, seg_key, RAW_DIR, enriched=False)
        print(f"\n  Saved {len(df)} raw prospects to {raw_path}")

        if args.reveal_emails:
            df = reveal_emails(client, df, max_reveals=args.max_reveals)
            enriched_path = save_results(df, seg_key, ENRICHED_DIR, enriched=True)
            print(f"  Saved enriched prospects to {enriched_path}")

        print_summary(df, seg_key)

    print(f"\nApollo API stats: {client.stats}")


if __name__ == "__main__":
    main()
