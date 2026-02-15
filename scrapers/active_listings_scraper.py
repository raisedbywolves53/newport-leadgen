"""Scrape active home listings for two lead types:

1. Properties for sale with aging/expiring garage door warranties
   (direct customer leads — inspection period = repair window)
2. Listing agents actively selling homes
   (referral partner leads — agent contacts come free with listing data)

Usage:
    python scrapers/active_listings_scraper.py --market oakland_county_mi
    python scrapers/active_listings_scraper.py --market all
    python scrapers/active_listings_scraper.py --market all --dry-run
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from homeharvest import scrape_property

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "markets.json"
HOMEHARVEST_RESULT_CAP = 10_000

# Current year for warranty calculations
CURRENT_YEAR = datetime.now().year

# Warranty lifespans (years from original install / build date)
WARRANTY_THRESHOLDS = {
    "door_panels":  15,   # Most manufacturers: 10-15 year limited
    "springs":      10,   # Torsion springs: 7-10 year / 10k cycles
    "opener":        5,   # Motor/opener: 3-5 year
}


def load_markets(config_path: Path = CONFIG_PATH) -> dict:
    with open(config_path) as f:
        return json.load(f)["markets"]


def classify_warranty(year_built) -> dict:
    """Classify garage door warranty status based on year_built."""
    if pd.isna(year_built):
        return {
            "door_warranty_expired": None,
            "spring_warranty_expired": None,
            "opener_warranty_expired": None,
            "warranty_risk_level": "unknown",
        }

    year = int(year_built)
    door_expired = (CURRENT_YEAR - year) >= WARRANTY_THRESHOLDS["door_panels"]
    spring_expired = (CURRENT_YEAR - year) >= WARRANTY_THRESHOLDS["springs"]
    opener_expired = (CURRENT_YEAR - year) >= WARRANTY_THRESHOLDS["opener"]

    expired_count = sum([door_expired, spring_expired, opener_expired])
    if expired_count == 3:
        risk = "high"
    elif expired_count >= 1:
        risk = "medium"
    else:
        risk = "low"

    return {
        "door_warranty_expired": door_expired,
        "spring_warranty_expired": spring_expired,
        "opener_warranty_expired": opener_expired,
        "warranty_risk_level": risk,
    }


def parse_agent_phone(agent_phones) -> str:
    """Extract primary phone number from HomeHarvest agent_phones field."""
    try:
        if agent_phones is None or (isinstance(agent_phones, float) and pd.isna(agent_phones)):
            return ""
    except (ValueError, TypeError):
        pass
    if isinstance(agent_phones, str):
        # Sometimes stored as string repr of list
        try:
            import ast
            phones = ast.literal_eval(agent_phones)
        except (ValueError, SyntaxError):
            return ""
    elif isinstance(agent_phones, list):
        phones = agent_phones
    else:
        return ""

    for p in phones:
        if isinstance(p, dict) and p.get("number"):
            num = str(p["number"])
            if len(num) == 10:
                return f"({num[:3]}) {num[3:6]}-{num[6:]}"
            return num
    return ""


def scrape_market(market_key: str, market_cfg: dict) -> pd.DataFrame:
    """Scrape active for-sale listings across all zip codes in a market."""
    zips = market_cfg["zip_codes"]
    frames: list[pd.DataFrame] = []

    for i, zip_code in enumerate(zips, start=1):
        print(f"  Scraping {zip_code} ({i}/{len(zips)})...", end=" ", flush=True)
        try:
            df = scrape_property(
                location=zip_code,
                listing_type="for_sale",
                extra_property_data=False,
            )
            print(f"found {len(df)} listings")
            if not df.empty:
                frames.append(df)
        except Exception as exc:
            print(f"ERROR: {exc}")

        if i < len(zips):
            time.sleep(2)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)

    # Deduplicate by property address
    if "formatted_address" in combined.columns:
        before = len(combined)
        combined = combined.drop_duplicates(subset="formatted_address", keep="first")
        dupes = before - len(combined)
        if dupes:
            print(f"  Removed {dupes} duplicate listings")

    # Filter to single-family only
    if "style" in combined.columns:
        has_style = combined["style"].notna()
        if has_style.any():
            combined = combined[~has_style | (combined["style"] == "SINGLE_FAMILY")]

    combined = combined.copy()
    combined["market"] = market_key

    # Add warranty classification
    if "year_built" in combined.columns:
        warranty_data = combined["year_built"].apply(classify_warranty)
        warranty_df = pd.DataFrame(warranty_data.tolist(), index=combined.index)
        combined = pd.concat([combined, warranty_df], axis=1)
    else:
        combined["door_warranty_expired"] = None
        combined["spring_warranty_expired"] = None
        combined["opener_warranty_expired"] = None
        combined["warranty_risk_level"] = "unknown"

    return combined


def extract_listing_agents(df: pd.DataFrame, market_key: str) -> pd.DataFrame:
    """Extract unique listing agents from for-sale data as referral leads."""
    if df.empty:
        return pd.DataFrame()

    agents = []
    seen = set()

    for _, row in df.iterrows():
        name = row.get("agent_name", "")
        email = row.get("agent_email", "")
        if pd.isna(name) or not name:
            continue

        # Deduplicate by name+email
        key = f"{name}|{email}".lower()
        if key in seen:
            continue
        seen.add(key)

        phone = parse_agent_phone(row.get("agent_phones"))
        agents.append({
            "agent_name": name,
            "agent_email": email if pd.notna(email) else "",
            "agent_phone": phone,
            "broker_name": row.get("broker_name", "") if pd.notna(row.get("broker_name")) else "",
            "office_name": row.get("office_name", "") if pd.notna(row.get("office_name")) else "",
            "office_email": row.get("office_email", "") if pd.notna(row.get("office_email")) else "",
            "city": row.get("city", "") if pd.notna(row.get("city")) else "",
            "state": row.get("state", "") if pd.notna(row.get("state")) else "",
            "market": market_key,
            "active_listing_count": 0,  # Will be filled below
            "source": "active_listing_agent",
        })

    if not agents:
        return pd.DataFrame()

    agent_df = pd.DataFrame(agents)

    # Count active listings per agent
    if "agent_name" in df.columns:
        listing_counts = df["agent_name"].value_counts()
        agent_df["active_listing_count"] = agent_df["agent_name"].map(listing_counts).fillna(0).astype(int)

    # Sort by listing count (most active agents first)
    agent_df = agent_df.sort_values("active_listing_count", ascending=False)

    return agent_df


def extract_warranty_leads(df: pd.DataFrame) -> pd.DataFrame:
    """Extract properties with expired warranties as direct customer leads."""
    if df.empty:
        return pd.DataFrame()

    # Filter to properties with at least medium warranty risk
    warranty_leads = df[df["warranty_risk_level"].isin(["high", "medium"])].copy()

    if warranty_leads.empty:
        return pd.DataFrame()

    # Select relevant columns
    cols = [
        "formatted_address", "city", "state", "zip_code",
        "year_built", "list_price", "sqft", "beds", "days_on_mls",
        "parking_garage", "agent_name", "agent_email",
        "door_warranty_expired", "spring_warranty_expired", "opener_warranty_expired",
        "warranty_risk_level", "market",
    ]
    available = [c for c in cols if c in warranty_leads.columns]
    warranty_leads = warranty_leads[available]

    return warranty_leads.sort_values("year_built", ascending=True)


def save_results(
    listings_df: pd.DataFrame,
    agents_df: pd.DataFrame,
    warranty_df: pd.DataFrame,
    market_key: str,
    output_dir: Path,
) -> dict:
    """Save all outputs and return paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    paths = {}

    # All active listings (raw)
    path = output_dir / f"active_listings_{market_key}_{date_str}.csv"
    listings_df.to_csv(path, index=False)
    print(f"  Active listings: {path} ({len(listings_df)} properties)")
    paths["listings"] = path

    # Listing agents (referral leads)
    if not agents_df.empty:
        path = output_dir / f"listing_agents_{market_key}_{date_str}.csv"
        agents_df.to_csv(path, index=False)
        print(f"  Listing agents: {path} ({len(agents_df)} agents)")
        paths["agents"] = path

    # Warranty leads (direct customer)
    if not warranty_df.empty:
        path = output_dir / f"warranty_leads_{market_key}_{date_str}.csv"
        warranty_df.to_csv(path, index=False)
        print(f"  Warranty leads: {path} ({len(warranty_df)} properties)")
        paths["warranty"] = path

    return paths


def print_summary(listings_df: pd.DataFrame, agents_df: pd.DataFrame,
                  warranty_df: pd.DataFrame, market_key: str):
    """Print market summary."""
    print(f"\n{'='*60}")
    print(f"Active Listings Summary: {market_key}")
    print(f"{'='*60}")
    print(f"  Total active listings: {len(listings_df)}")

    if not listings_df.empty and "year_built" in listings_df.columns:
        avg_year = listings_df["year_built"].dropna().mean()
        print(f"  Average year built: {avg_year:.0f}")

    if not listings_df.empty:
        risk_counts = listings_df["warranty_risk_level"].value_counts()
        for risk, count in risk_counts.items():
            print(f"  Warranty risk {risk}: {count} ({count/len(listings_df)*100:.0f}%)")

    if not agents_df.empty:
        has_email = (agents_df["agent_email"].fillna("").str.len() > 0).sum()
        has_phone = (agents_df["agent_phone"].fillna("").str.len() > 0).sum()
        print(f"\n  Listing agents found: {len(agents_df)}")
        print(f"  With email: {has_email} ({has_email/len(agents_df)*100:.0f}%)")
        print(f"  With phone: {has_phone} ({has_phone/len(agents_df)*100:.0f}%)")
        print(f"  Top agents by active listings:")
        for _, row in agents_df.head(5).iterrows():
            print(f"    {row['agent_name']} ({row['active_listing_count']} listings) "
                  f"— {row['agent_email']}")

    if not warranty_df.empty:
        print(f"\n  Warranty expiration leads: {len(warranty_df)}")
        high = (warranty_df["warranty_risk_level"] == "high").sum()
        med = (warranty_df["warranty_risk_level"] == "medium").sum()
        print(f"    High risk (all warranties expired): {high}")
        print(f"    Medium risk (some warranties expired): {med}")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape active home listings for warranty leads and agent contacts"
    )
    parser.add_argument("--market", required=True, help='Market key or "all"')
    parser.add_argument("--output-dir", default="./data/raw/", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be scraped")
    args = parser.parse_args()

    markets = load_markets()
    output_dir = Path(args.output_dir)

    if args.market == "all":
        targets = list(markets.keys())
    else:
        if args.market not in markets:
            print(f"Unknown market: {args.market}. Options: {', '.join(markets.keys())}, all")
            sys.exit(1)
        targets = [args.market]

    if args.dry_run:
        for mk in targets:
            cfg = markets[mk]
            print(f"{mk}: {len(cfg['zip_codes'])} zip codes to scrape for active listings")
        return

    for mk in targets:
        cfg = markets[mk]
        print(f"\n{'='*60}")
        print(f"Scraping active listings: {cfg['name']} {cfg['state']}")
        print(f"{'='*60}")

        df = scrape_market(mk, cfg)
        if df.empty:
            print(f"  No active listings found in {mk}")
            continue

        agents_df = extract_listing_agents(df, mk)
        warranty_df = extract_warranty_leads(df)

        save_results(df, agents_df, warranty_df, mk, output_dir)
        print_summary(df, agents_df, warranty_df, mk)


if __name__ == "__main__":
    main()
