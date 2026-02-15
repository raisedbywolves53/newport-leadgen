"""Scrape recently sold homes using HomeHarvest (Realtor.com).

Usage:
    python scrapers/homeowner_scraper.py --market oakland_county_mi --days 14
    python scrapers/homeowner_scraper.py --market all --days 30
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from homeharvest import scrape_property

HOMEHARVEST_RESULT_CAP = 10_000
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "markets.json"


def load_markets(config_path: Path = CONFIG_PATH) -> dict:
    with open(config_path) as f:
        return json.load(f)["markets"]


def scrape_market(market_key: str, market_cfg: dict, days: int) -> pd.DataFrame:
    """Scrape all zip codes for a single market, return combined DataFrame."""
    zips = market_cfg["zip_codes"]
    market_name = f"{market_cfg['name']} {market_cfg['state']}"
    frames: list[pd.DataFrame] = []

    for i, zip_code in enumerate(zips, start=1):
        print(f"Scraping {zip_code} ({i}/{len(zips)})...", end=" ", flush=True)
        try:
            df = scrape_property(
                location=zip_code,
                listing_type="sold",
                past_days=days,
                extra_property_data=False,
            )
            print(f"found {len(df)} properties")
            if len(df) >= HOMEHARVEST_RESULT_CAP:
                print(
                    f"  WARNING: Hit {HOMEHARVEST_RESULT_CAP} result cap for {zip_code} — "
                    "results may be incomplete. Consider reducing --days."
                )
            if not df.empty:
                frames.append(df)
        except Exception as exc:
            print(f"ERROR: {exc}")

        if i < len(zips):
            time.sleep(2)

    if not frames:
        print(f"No results for {market_name}.")
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    combined = enrich(combined, market_key, days)
    print(
        f"{market_name}: {len(combined)} sold homes "
        f"({combined['aging_door'].sum()} aging doors, "
        f"{combined['spring_risk'].sum()} spring risk)"
    )
    return combined


def enrich(df: pd.DataFrame, market_key: str, days: int) -> pd.DataFrame:
    """Deduplicate, filter, and add derived columns."""
    # Deduplicate by full address
    if "formatted_address" in df.columns:
        df = df.drop_duplicates(subset="formatted_address", keep="first")

    # Filter to single-family only when style column has data
    if "style" in df.columns:
        has_style = df["style"].notna()
        if has_style.any():
            df = df[~has_style | (df["style"] == "SINGLE_FAMILY")]

    df = df.copy()
    df["market"] = market_key

    # aging_door: home built before 2011 (15+ years old relative to ~2026)
    if "year_built" in df.columns:
        df["aging_door"] = df["year_built"].apply(
            lambda y: bool(pd.notna(y) and int(y) < 2011)
        )
        df["spring_risk"] = df["year_built"].apply(
            lambda y: bool(pd.notna(y) and 2000 <= int(y) <= 2010)
        )
    else:
        df["aging_door"] = False
        df["spring_risk"] = False

    # days_since_sold
    if "last_sold_date" in df.columns:
        now = pd.Timestamp.now()
        df["days_since_sold"] = df["last_sold_date"].apply(
            lambda d: (now - pd.Timestamp(d)).days if pd.notna(d) else None
        )
    else:
        df["days_since_sold"] = None

    return df


def save(df: pd.DataFrame, market_key: str, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    path = output_dir / f"homeowners_{market_key}_{date_str}.csv"
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Scrape recently sold homes via HomeHarvest"
    )
    parser.add_argument(
        "--market",
        required=True,
        help='Market key (e.g. oakland_county_mi) or "all"',
    )
    parser.add_argument(
        "--days",
        type=int,
        default=14,
        help="How many days back to search (default: 14)",
    )
    parser.add_argument(
        "--output-dir",
        default="./data/raw/",
        help="Directory for output CSVs (default: ./data/raw/)",
    )
    args = parser.parse_args()

    markets = load_markets()
    output_dir = Path(args.output_dir)

    if args.market == "all":
        targets = list(markets.keys())
    else:
        if args.market not in markets:
            print(
                f"Unknown market: {args.market}. "
                f"Options: {', '.join(markets.keys())}, all"
            )
            sys.exit(1)
        targets = [args.market]

    for market_key in targets:
        print(f"\n{'='*60}")
        print(f"Market: {markets[market_key]['name']} {markets[market_key]['state']}")
        print(f"Zip codes: {len(markets[market_key]['zip_codes'])}")
        print(f"Looking back: {args.days} days")
        print(f"{'='*60}")

        df = scrape_market(market_key, markets[market_key], args.days)
        if not df.empty:
            save(df, market_key, output_dir)


if __name__ == "__main__":
    main()
