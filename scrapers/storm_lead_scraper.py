"""Generate storm damage lead lists by combining weather alerts with property data.

When a storm hits, this scraper targets:
1. Active listings in storm-affected zip codes (deals at risk — agents need fast repair)
2. Homes sold in last 90 days (new homeowners unfamiliar with emergency services)
3. Older homes in affected areas (most vulnerable to storm damage)

Also identifies insurance agents in affected areas for claim referral partnerships.

Usage:
    python scrapers/storm_lead_scraper.py --market oakland_county_mi
    python scrapers/storm_lead_scraper.py --market oakland_county_mi --test
    python scrapers/storm_lead_scraper.py --market all
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from homeharvest import scrape_property

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Import weather monitor for storm detection
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scrapers import weather_monitor


def load_markets() -> dict:
    with open(CONFIG_DIR / "markets.json") as f:
        return json.load(f)["markets"]


def scrape_affected_properties(
    affected_zips: list[str],
    listing_type: str = "for_sale",
    past_days: int = 7,
    max_zips: int = 20,
) -> pd.DataFrame:
    """Scrape properties in storm-affected zip codes.

    Args:
        affected_zips: Zip codes in the storm path
        listing_type: "for_sale" or "sold"
        past_days: Days back for sold listings
        max_zips: Limit zip codes to scrape (budget control)
    """
    # Sample zips if too many to keep API costs reasonable
    zips = affected_zips[:max_zips]
    frames = []

    for i, z in enumerate(zips, start=1):
        print(f"    [{i}/{len(zips)}] {z} ({listing_type})...", end=" ", flush=True)
        try:
            kwargs = {"location": z, "listing_type": listing_type, "extra_property_data": False}
            if listing_type == "sold":
                kwargs["past_days"] = past_days
            df = scrape_property(**kwargs)
            print(f"{len(df)} properties")
            if not df.empty:
                frames.append(df)
        except Exception as e:
            print(f"ERROR: {e}")

        if i < len(zips):
            time.sleep(2)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)

    # Deduplicate
    if "formatted_address" in combined.columns:
        combined = combined.drop_duplicates(subset="formatted_address", keep="first")

    # Filter to single-family
    if "style" in combined.columns:
        has_style = combined["style"].notna()
        if has_style.any():
            combined = combined[~has_style | (combined["style"] == "SINGLE_FAMILY")]

    return combined


def score_storm_vulnerability(df: pd.DataFrame) -> pd.DataFrame:
    """Score properties by storm damage vulnerability."""
    df = df.copy()

    # Older homes are more vulnerable
    if "year_built" in df.columns:
        df["home_age"] = datetime.now().year - df["year_built"].fillna(datetime.now().year)
        df["vulnerability"] = pd.cut(
            df["home_age"],
            bins=[0, 10, 20, 30, 50, 200],
            labels=["low", "moderate", "elevated", "high", "critical"],
        )
    else:
        df["home_age"] = None
        df["vulnerability"] = "unknown"

    return df


def build_storm_leads(
    market_key: str,
    market_cfg: dict,
    alert: dict,
) -> dict:
    """Build comprehensive storm lead package for a market.

    Returns dict with DataFrames: active_listings, recent_buyers, and summary stats.
    """
    affected_zips = alert.get("affected_zips", market_cfg.get("zip_codes", []))
    severity = alert.get("severity", "medium")
    weather = alert.get("weather_description", "severe weather")

    print(f"\n  Storm alert: {severity} — {weather}")
    print(f"  Wind: {alert.get('wind_speed', '?')} mph")
    print(f"  Affected zip codes: {len(affected_zips)}")

    # 1. Active listings in storm area (agents need fast repair to keep deals alive)
    print(f"\n  Scraping active listings in storm zone...")
    active = scrape_affected_properties(affected_zips, listing_type="for_sale", max_zips=15)
    if not active.empty:
        active = score_storm_vulnerability(active)
        active["storm_context"] = f"Storm alert ({severity}): {weather}"
        active["market"] = market_key
        print(f"  Found {len(active)} active listings in storm zone")
    else:
        print(f"  No active listings found")

    # 2. Recent buyers (past 90 days — new to area, need emergency contacts)
    print(f"\n  Scraping recent home buyers in storm zone...")
    recent = scrape_affected_properties(affected_zips, listing_type="sold", past_days=90, max_zips=15)
    if not recent.empty:
        recent = score_storm_vulnerability(recent)
        recent["storm_context"] = f"Storm alert ({severity}): {weather}"
        recent["market"] = market_key
        print(f"  Found {len(recent)} recent buyers in storm zone")
    else:
        print(f"  No recent buyers found")

    # 3. Find insurance agents we've already enriched in this market
    insurance_path = DATA_DIR / "enriched" / f"insurance_agents_{datetime.now():%Y%m%d}.csv"
    insurance_agents = pd.DataFrame()
    if insurance_path.exists():
        all_agents = pd.read_csv(insurance_path)
        insurance_agents = all_agents[all_agents["market"] == market_key]
        print(f"\n  Insurance agents in market: {len(insurance_agents)} (from enriched data)")

    return {
        "active_listings": active,
        "recent_buyers": recent,
        "insurance_agents": insurance_agents,
        "alert": alert,
    }


def save_storm_leads(leads: dict, market_key: str) -> dict:
    """Save storm lead data to CSVs."""
    out_dir = DATA_DIR / "storm_leads"
    out_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    paths = {}

    active = leads["active_listings"]
    if not active.empty:
        # Properties at risk
        path = out_dir / f"storm_active_listings_{market_key}_{date_str}.csv"
        cols = [c for c in [
            "formatted_address", "city", "state", "zip_code", "year_built",
            "list_price", "sqft", "days_on_mls", "parking_garage",
            "agent_name", "agent_email", "vulnerability", "home_age",
            "storm_context", "market",
        ] if c in active.columns]
        active[cols].to_csv(path, index=False)
        print(f"  Saved: {path} ({len(active)} listings)")
        paths["active_listings"] = str(path)

        # Agents from storm-affected listings (high-urgency referral leads)
        agents = active[active["agent_email"].notna()][["agent_name", "agent_email"]].drop_duplicates()
        if not agents.empty:
            agent_path = out_dir / f"storm_listing_agents_{market_key}_{date_str}.csv"
            agents.to_csv(agent_path, index=False)
            print(f"  Saved: {agent_path} ({len(agents)} agents in storm zone)")
            paths["storm_agents"] = str(agent_path)

    recent = leads["recent_buyers"]
    if not recent.empty:
        path = out_dir / f"storm_recent_buyers_{market_key}_{date_str}.csv"
        cols = [c for c in [
            "formatted_address", "city", "state", "zip_code", "year_built",
            "last_sold_date", "sold_price", "sqft", "parking_garage",
            "vulnerability", "home_age", "storm_context", "market",
        ] if c in recent.columns]
        recent[cols].to_csv(path, index=False)
        print(f"  Saved: {path} ({len(recent)} recent buyers)")
        paths["recent_buyers"] = str(path)

    return paths


def print_storm_summary(leads: dict, market_key: str):
    """Print actionable storm response summary."""
    alert = leads["alert"]
    active = leads["active_listings"]
    recent = leads["recent_buyers"]
    insurance = leads["insurance_agents"]

    print(f"\n{'='*60}")
    print(f"STORM RESPONSE PACKAGE: {market_key}")
    print(f"{'='*60}")
    print(f"  Severity: {alert.get('severity', '?').upper()}")
    print(f"  Weather: {alert.get('weather_description', '?')}")
    print(f"  Wind: {alert.get('wind_speed', '?')} mph")

    if not active.empty:
        high_vuln = (active["vulnerability"].isin(["high", "critical"])).sum() if "vulnerability" in active.columns else 0
        agents_with_email = active["agent_email"].notna().sum() if "agent_email" in active.columns else 0
        print(f"\n  Active listings at risk: {len(active)}")
        print(f"    High/critical vulnerability: {high_vuln}")
        print(f"    Listing agents contactable: {agents_with_email}")

    if not recent.empty:
        print(f"\n  Recent buyers needing emergency service: {len(recent)}")

    if not insurance.empty:
        has_email = (insurance.get("dm_email", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()
        print(f"\n  Insurance agents for claim referrals: {len(insurance)} ({has_email} with DM email)")

    total = len(active) + len(recent)
    print(f"\n  TOTAL STORM LEADS: {total}")
    print(f"\n  RECOMMENDED ACTIONS:")
    print(f"    1. Call listing agents in storm zone — their deals need fast repair")
    print(f"    2. SMS recent buyers — emergency service offer")
    print(f"    3. Contact insurance agents — position as preferred storm repair vendor")


def main():
    parser = argparse.ArgumentParser(
        description="Generate storm damage lead lists from weather alerts + property data"
    )
    parser.add_argument("--market", required=True, help='Market key or "all"')
    parser.add_argument("--test", action="store_true", help="Use simulated storm alert")
    args = parser.parse_args()

    markets = load_markets()
    api_key = os.environ.get("OPENWEATHER_API_KEY", "")

    if args.market == "all":
        target_keys = list(markets.keys())
    else:
        if args.market not in markets:
            print(f"Unknown market: {args.market}. Options: {', '.join(markets.keys())}, all")
            sys.exit(1)
        target_keys = [args.market]

    for mk in target_keys:
        cfg = markets[mk]
        print(f"\n{'='*60}")
        print(f"Storm Lead Builder: {cfg['name']} {cfg['state']}")
        print(f"{'='*60}")

        if args.test:
            alert = weather_monitor.build_simulated_alert(mk, cfg)
            print("  (Using simulated storm alert for testing)")
        else:
            if not api_key:
                print("  ERROR: OPENWEATHER_API_KEY not set")
                continue
            alert = weather_monitor.check_market(mk, cfg, api_key, wind_threshold=50.0)
            if not alert:
                print(f"  No severe weather detected in {mk}")
                continue

        leads = build_storm_leads(mk, cfg, alert)
        paths = save_storm_leads(leads, mk)
        print_storm_summary(leads, mk)


if __name__ == "__main__":
    main()
