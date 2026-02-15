"""Mine competitor garage door companies' reviews for intent-based leads.

Finds garage door companies in each service area, pulls their reviews,
and identifies negative reviews (1-3 stars) as high-intent lead signals.

Outputs:
  1. Competitor scorecard — all competitors ranked by opportunity
  2. Negative review leads — unhappy customers who still need service

Usage:
    python scrapers/competitor_review_scraper.py --market all
    python scrapers/competitor_review_scraper.py --market oakland_county_mi
    python scrapers/competitor_review_scraper.py --market all --dry-run
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

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Places API (New) endpoints
TEXT_SEARCH_URL = "https://places.googleapis.com/v1/places:searchText"
PLACE_DETAILS_URL = "https://places.googleapis.com/v1/places"

# Field mask for competitor search (includes reviews — Pro tier billing)
SEARCH_FIELD_MASK = ",".join([
    "places.id",
    "places.displayName",
    "places.formattedAddress",
    "places.rating",
    "places.userRatingCount",
    "places.nationalPhoneNumber",
    "places.websiteUri",
    "places.reviews",
    "places.location",
])

# Search queries to find garage door competitors
COMPETITOR_QUERIES = [
    "garage door repair",
    "garage door installation",
    "garage door company",
    "overhead door repair",
    "garage door service",
]

# Goldman's own place names to exclude from competitors
OWN_BUSINESS_NAMES = {
    "goldman", "goldmans", "goldman's",
}


def load_markets() -> dict:
    with open(CONFIG_DIR / "markets.json") as f:
        return json.load(f)["markets"]


def get_api_key() -> str:
    key = os.environ.get("GOOGLE_PLACES_API_KEY", "")
    if not key:
        print("ERROR: GOOGLE_PLACES_API_KEY not set")
        sys.exit(1)
    return key


def is_own_business(name: str) -> bool:
    """Check if a business name is Goldman's own listing."""
    return any(own in name.lower() for own in OWN_BUSINESS_NAMES)


def is_garage_door_business(name: str) -> bool:
    """Filter for businesses that are actually garage door companies."""
    name_lower = name.lower()
    keywords = ["garage", "door", "overhead", "opener", "gdo"]
    return any(kw in name_lower for kw in keywords)


def search_competitors(query: str, location: str, api_key: str) -> list[dict]:
    """Search for garage door companies in a location."""
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": SEARCH_FIELD_MASK,
    }
    body = {"textQuery": f"{query} in {location}", "pageSize": 20}
    all_results = []

    while True:
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
        time.sleep(2)
        body["pageToken"] = next_token

    return all_results


def extract_competitor(raw: dict, market: str) -> dict:
    """Extract competitor info from Places API result."""
    name = raw.get("displayName", {}).get("text", "")
    addr = raw.get("formattedAddress", "")
    location = raw.get("location", {})

    return {
        "name": name,
        "formatted_address": addr,
        "rating": raw.get("rating"),
        "review_count": raw.get("userRatingCount", 0),
        "phone": raw.get("nationalPhoneNumber", ""),
        "website": raw.get("websiteUri", ""),
        "place_id": raw.get("id", ""),
        "lat": location.get("latitude"),
        "lng": location.get("longitude"),
        "market": market,
    }


def extract_reviews(raw: dict, competitor_name: str, market: str) -> list[dict]:
    """Extract individual reviews from a Places API result."""
    reviews = []
    for r in raw.get("reviews", []):
        author = r.get("authorAttribution", {})
        text_obj = r.get("text", {})
        rating = r.get("rating", 0)

        reviews.append({
            "reviewer_name": author.get("displayName", ""),
            "reviewer_profile_url": author.get("uri", ""),
            "rating": rating,
            "review_text": text_obj.get("text", ""),
            "publish_time": r.get("publishTime", ""),
            "relative_time": r.get("relativePublishTimeDescription", ""),
            "competitor_name": competitor_name,
            "market": market,
            "is_negative": rating <= 3,
        })

    return reviews


def scrape_market(market_key: str, market_cfg: dict, api_key: str) -> tuple[list[dict], list[dict]]:
    """Scrape all competitors and reviews for one market.

    Returns (competitors, reviews) as lists of dicts.
    """
    state = market_cfg["state"]
    # Use county-level searches plus major city searches for better coverage
    locations = set()
    locations.add(f"{market_cfg['name']} County {state}" if "County" not in market_cfg["name"]
                  else f"{market_cfg['name']} {state}")
    # Add top cities for more granular results
    for city in market_cfg.get("major_cities", [])[:5]:
        locations.add(f"{city} {state}")

    seen_ids = set()
    all_competitors = []
    all_reviews = []

    total_queries = len(COMPETITOR_QUERIES) * len(locations)
    i = 0

    for query in COMPETITOR_QUERIES:
        for location in sorted(locations):
            i += 1
            search_text = f"{query} in {location}"
            print(f"  [{i}/{total_queries}] {search_text}...", end=" ", flush=True)

            try:
                results = search_competitors(query, location, api_key)
                print(f"found {len(results)}")
            except Exception as e:
                print(f"ERROR: {e}")
                continue

            for raw in results:
                name = raw.get("displayName", {}).get("text", "")
                place_id = raw.get("id", "")

                # Skip own business
                if is_own_business(name):
                    continue

                # Skip non-garage-door businesses
                if not is_garage_door_business(name):
                    continue

                # Deduplicate by place_id
                if place_id in seen_ids:
                    continue
                seen_ids.add(place_id)

                competitor = extract_competitor(raw, market_key)
                all_competitors.append(competitor)

                reviews = extract_reviews(raw, name, market_key)
                all_reviews.extend(reviews)

            if i < total_queries:
                time.sleep(1.5)

    return all_competitors, all_reviews


def score_competitors(competitors: list[dict], reviews: list[dict]) -> pd.DataFrame:
    """Create a competitor scorecard with opportunity ranking."""
    if not competitors:
        return pd.DataFrame()

    df = pd.DataFrame(competitors)

    # Calculate negative review ratio from sampled reviews
    review_df = pd.DataFrame(reviews) if reviews else pd.DataFrame()
    if not review_df.empty:
        neg_counts = review_df[review_df["is_negative"]].groupby("competitor_name").size()
        total_counts = review_df.groupby("competitor_name").size()
        neg_ratio = (neg_counts / total_counts).fillna(0)

        df["sampled_negative_pct"] = df["name"].map(neg_ratio).fillna(0)
        df["sampled_negative_pct"] = (df["sampled_negative_pct"] * 100).round(0)
    else:
        df["sampled_negative_pct"] = 0

    # Opportunity score: lower rating + more reviews = bigger opportunity
    # (more unhappy customers in the area)
    df["opportunity_score"] = (
        (5.0 - df["rating"].fillna(5)) * df["review_count"].fillna(0).clip(upper=500) / 100
    ).round(1)

    df = df.sort_values("opportunity_score", ascending=False)
    return df


def save_results(
    competitors_df: pd.DataFrame,
    reviews_df: pd.DataFrame,
    market_key: str,
) -> tuple[Path, Path | None]:
    """Save competitor scorecard and negative review leads."""
    out_dir = DATA_DIR / "competitor_intel"
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")

    # Competitor scorecard
    scorecard_path = out_dir / f"competitors_{market_key}_{date_str}.csv"
    competitors_df.to_csv(scorecard_path, index=False)
    print(f"  Competitor scorecard: {scorecard_path} ({len(competitors_df)} companies)")

    # Negative reviews
    neg_path = None
    if not reviews_df.empty:
        neg_reviews = reviews_df[reviews_df["is_negative"]].copy()
        if not neg_reviews.empty:
            neg_path = out_dir / f"negative_reviews_{market_key}_{date_str}.csv"
            neg_reviews.to_csv(neg_path, index=False)
            print(f"  Negative review leads: {neg_path} ({len(neg_reviews)} reviews)")
        else:
            print("  No negative reviews found in sample")

    # Also save all reviews for analysis
    all_reviews_path = out_dir / f"all_reviews_{market_key}_{date_str}.csv"
    reviews_df.to_csv(all_reviews_path, index=False)

    return scorecard_path, neg_path


def print_market_summary(competitors_df: pd.DataFrame, reviews_df: pd.DataFrame, market_key: str):
    """Print actionable summary for a market."""
    print(f"\n{'='*60}")
    print(f"Competitor Intelligence: {market_key}")
    print(f"{'='*60}")

    total = len(competitors_df)
    avg_rating = competitors_df["rating"].mean() if not competitors_df.empty else 0

    print(f"  Total competitors found: {total}")
    print(f"  Average competitor rating: {avg_rating:.1f}")

    if not competitors_df.empty:
        # Weak competitors (below 4.0)
        weak = competitors_df[competitors_df["rating"] < 4.0]
        print(f"  Competitors below 4.0 stars: {len(weak)} ({len(weak)/total*100:.0f}%)")

        # Top opportunities
        top = competitors_df.head(5)
        print(f"\n  Top 5 opportunities (most unhappy customer bases):")
        for _, row in top.iterrows():
            print(f"    {row['name']}: {row['rating']}/5 ({row['review_count']} reviews) "
                  f"— opportunity score: {row['opportunity_score']}")

    if not reviews_df.empty:
        neg = reviews_df[reviews_df["is_negative"]]
        print(f"\n  Review sample: {len(reviews_df)} total, {len(neg)} negative ({len(neg)/len(reviews_df)*100:.0f}%)")

        # Common complaint themes
        if not neg.empty:
            texts = " ".join(neg["review_text"].fillna("").tolist()).lower()
            themes = {
                "price/cost": len(re.findall(r"\b(expensive|overcharg|price|cost|rip.?off|goug)\w*", texts)),
                "slow/late": len(re.findall(r"\b(slow|late|wait|delay|hours|days|week)\w*", texts)),
                "quality": len(re.findall(r"\b(broke|break|fail|poor|cheap|defect|wrong)\w*", texts)),
                "communication": len(re.findall(r"\b(call|respond|answer|ignor|ghost|rude|unprofessional)\w*", texts)),
                "no-show": len(re.findall(r"\b(no.?show|never came|didn.?t show|stood up)\w*", texts)),
            }
            themes = {k: v for k, v in sorted(themes.items(), key=lambda x: x[1], reverse=True) if v > 0}
            if themes:
                print(f"\n  Complaint themes (from negative reviews):")
                for theme, count in themes.items():
                    print(f"    {theme}: {count} mentions")


def main():
    parser = argparse.ArgumentParser(
        description="Mine competitor reviews for intent-based leads"
    )
    parser.add_argument(
        "--market", required=True,
        help='Market key (oakland_county_mi, etc.) or "all"',
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Show what would be searched without calling the API",
    )
    args = parser.parse_args()

    markets = load_markets()

    if args.market == "all":
        target_markets = list(markets.keys())
    else:
        if args.market not in markets:
            print(f"Unknown market: {args.market}. Options: {', '.join(markets.keys())}, all")
            sys.exit(1)
        target_markets = [args.market]

    if args.dry_run:
        total_queries = 0
        for mk in target_markets:
            cfg = markets[mk]
            locations = set()
            locations.add(f"{cfg['name']} County {cfg['state']}" if "County" not in cfg["name"]
                          else f"{cfg['name']} {cfg['state']}")
            for city in cfg.get("major_cities", [])[:5]:
                locations.add(f"{city} {cfg['state']}")
            n = len(COMPETITOR_QUERIES) * len(locations)
            total_queries += n
            print(f"\n{mk}: {n} queries across {len(locations)} locations")
            for q in COMPETITOR_QUERIES:
                for loc in sorted(locations):
                    print(f"  -> {q} in {loc}")
        print(f"\nTotal: {total_queries} API calls")
        return

    api_key = get_api_key()

    for mk in target_markets:
        cfg = markets[mk]
        print(f"\n{'='*60}")
        print(f"Mining competitors: {mk}")
        print(f"{'='*60}")

        competitors, reviews = scrape_market(mk, cfg, api_key)

        if not competitors:
            print(f"  No competitors found in {mk}")
            continue

        competitors_df = score_competitors(competitors, reviews)
        reviews_df = pd.DataFrame(reviews) if reviews else pd.DataFrame()

        save_results(competitors_df, reviews_df, mk)
        print_market_summary(competitors_df, reviews_df, mk)


if __name__ == "__main__":
    main()
