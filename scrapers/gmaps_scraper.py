"""Scrape Google Maps/Places API (New) for referral partner and commercial businesses.

Usage:
    python scrapers/gmaps_scraper.py --category real_estate_agents
    python scrapers/gmaps_scraper.py --category all --dry-run
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "search_queries.json"

# Places API (New) endpoint
TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"

# Field mask — controls which fields are returned (and billing tier).
# Phone + website are included here so no separate Details call is needed.
FIELD_MASK = ",".join([
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.rating",
    "places.userRatingCount",
    "places.nationalPhoneNumber",
    "places.websiteUri",
    "places.location",
])

STATE_TO_MARKET = {
    "MI": ["oakland_county_mi", "wayne_county_mi"],
    "NC": ["triangle_nc"],
}


def load_queries(config_path: Path = CONFIG_PATH) -> dict:
    with open(config_path) as f:
        return json.load(f)["icp_queries"]


def get_api_key() -> str:
    key = os.environ.get("GOOGLE_PLACES_API_KEY", "")
    if not key:
        print("ERROR: GOOGLE_PLACES_API_KEY not set in environment / .env")
        sys.exit(1)
    return key


def parse_address(formatted_address: str) -> dict:
    """Parse city, state, and zip from a Google Places formatted_address."""
    parts = {"city": "", "state": "", "zip": ""}
    if not formatted_address:
        return parts
    # Typical format: "123 Main St, Troy, MI 48084, USA"
    chunks = [c.strip() for c in formatted_address.split(",")]
    if len(chunks) >= 3:
        parts["city"] = chunks[-3] if len(chunks) >= 3 else ""
        state_zip = chunks[-2].strip() if len(chunks) >= 2 else ""
        match = re.match(r"([A-Z]{2})\s*(\d{5})?", state_zip)
        if match:
            parts["state"] = match.group(1)
            parts["zip"] = match.group(2) or ""
    return parts


def text_search(query: str, city: str, state: str, api_key: str) -> list[dict]:
    """Run a Places Text Search (New API), handling pagination. Returns raw results."""
    search_query = f"{query} in {city} {state}"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": FIELD_MASK,
    }
    body = {"textQuery": search_query, "pageSize": 20}
    all_results = []

    while True:
        # Retry with backoff on transient 403s (Google rate limiting)
        for attempt in range(3):
            resp = requests.post(TEXT_SEARCH_URL, headers=headers, json=body, timeout=30)
            if resp.status_code == 403 and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            resp.raise_for_status()
            break
        data = resp.json()

        all_results.extend(data.get("places", []))

        next_token = data.get("nextPageToken")
        if not next_token:
            break

        # Google requires ~2s before nextPageToken becomes valid
        time.sleep(2)
        body["pageToken"] = next_token

    return all_results


def extract_business(raw: dict, query_info: dict) -> dict:
    """Extract a flat business record from a new Places API result."""
    addr = raw.get("formattedAddress", "")
    parsed = parse_address(addr)
    location = raw.get("location", {})

    return {
        "name": raw.get("displayName", {}).get("text", ""),
        "formatted_address": addr,
        "city": parsed["city"],
        "state": parsed["state"],
        "zip": parsed["zip"],
        "rating": raw.get("rating"),
        "user_ratings_total": raw.get("userRatingCount", 0),
        "place_id": raw.get("id", ""),
        "lat": location.get("latitude"),
        "lng": location.get("longitude"),
        "icp_category": query_info["category"],
        "market": query_info["market"],
        "query_used": query_info["query"],
        "phone": raw.get("nationalPhoneNumber", ""),
        "website": raw.get("websiteUri", ""),
    }


def scrape_category(category: str, cat_cfg: dict, api_key: str) -> pd.DataFrame:
    """Scrape all queries in one ICP category, return combined DataFrame."""
    queries = cat_cfg["queries"]
    min_rating = cat_cfg.get("min_rating", 0)
    min_reviews = cat_cfg.get("min_reviews", 0)
    all_records: list[dict] = []

    for i, q in enumerate(queries, start=1):
        search_text = f"{q['query']} in {q['city']} {q['state']}"
        print(f"  [{i}/{len(queries)}] {search_text}...", end=" ", flush=True)
        try:
            results = text_search(q["query"], q["city"], q["state"], api_key)
            print(f"found {len(results)}")
        except Exception as exc:
            print(f"ERROR: {exc}")
            continue

        query_info = {
            "category": category,
            "market": q["market"],
            "query": f"{q['query']} in {q['city']} {q['state']}",
        }

        for raw in results:
            record = extract_business(raw, query_info)
            all_records.append(record)

        if i < len(queries):
            time.sleep(2)

    if not all_records:
        print(f"  No results for {category}.")
        return pd.DataFrame()

    df = pd.DataFrame(all_records)

    # Apply rating/review filters
    if "rating" in df.columns and min_rating > 0:
        df = df[df["rating"].fillna(0) >= min_rating]
    if "user_ratings_total" in df.columns and min_reviews > 0:
        df = df[df["user_ratings_total"].fillna(0) >= min_reviews]

    # Deduplicate by name + city
    before = len(df)
    df = df.drop_duplicates(subset=["name", "city"], keep="first")
    dupes = before - len(df)
    if dupes:
        print(f"  Removed {dupes} duplicates")

    return df


def save(df: pd.DataFrame, category: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    path = output_dir / f"businesses_{category}_{date_str}.csv"
    df.to_csv(path, index=False)
    print(f"  Saved {len(df)} rows to {path}")
    return path


def print_summary(df: pd.DataFrame, category: str) -> None:
    """Print state-level breakdown for a category."""
    if df.empty:
        print(f"{category}: 0 businesses found")
        return
    state_counts = df["state"].value_counts()
    breakdown = ", ".join(f"{count} {state}" for state, count in state_counts.items())
    print(f"{category}: {len(df)} businesses found ({breakdown})")


def dry_run(categories: dict, targets: list[str]) -> None:
    """Show what queries would run without calling the API."""
    total = 0
    for cat in targets:
        cat_cfg = categories[cat]
        queries = cat_cfg["queries"]
        print(f"\n{cat} ({len(queries)} queries, "
              f"min_rating={cat_cfg.get('min_rating', 0)}, "
              f"min_reviews={cat_cfg.get('min_reviews', 0)}):")
        for q in queries:
            print(f"  -> {q['query']} in {q['city']} {q['state']} "
                  f"[{q['market']}]")
        total += len(queries)
    print(f"\nTotal: {total} text search API calls")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape Google Places for referral partner businesses"
    )
    parser.add_argument(
        "--category",
        required=True,
        help='ICP category (e.g. real_estate_agents) or "all"',
    )
    parser.add_argument(
        "--output-dir",
        default="./data/raw/",
        help="Directory for output CSVs (default: ./data/raw/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show queries without calling the API",
    )
    args = parser.parse_args()

    categories = load_queries()
    output_dir = Path(args.output_dir)

    if args.category == "all":
        targets = list(categories.keys())
    else:
        if args.category not in categories:
            print(
                f"Unknown category: {args.category}. "
                f"Options: {', '.join(categories.keys())}, all"
            )
            sys.exit(1)
        targets = [args.category]

    if args.dry_run:
        dry_run(categories, targets)
        return

    api_key = get_api_key()

    for cat in targets:
        cat_cfg = categories[cat]
        print(f"\n{'='*60}")
        print(f"Category: {cat} ({len(cat_cfg['queries'])} queries)")
        print(f"{'='*60}")

        df = scrape_category(cat, cat_cfg, api_key)
        if not df.empty:
            save(df, cat, output_dir)
            print_summary(df, cat)
        else:
            print(f"{cat}: 0 businesses found")


if __name__ == "__main__":
    main()
