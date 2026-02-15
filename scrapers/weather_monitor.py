"""Monitor weather events for storm damage outreach triggers.

Usage:
    python scrapers/weather_monitor.py --check-now
    python scrapers/weather_monitor.py --market oakland_county_mi
    python scrapers/weather_monitor.py --test --market triangle_nc
    python scrapers/weather_monitor.py --monitor
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "markets.json"
ALERTS_DIR = Path(__file__).resolve().parent.parent / "data" / "alerts"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

# One representative zip per market
MARKET_CHECK_ZIPS = {
    "oakland_county_mi": "48084",
    "wayne_county_mi": "48126",
    "triangle_nc": "27601",
}

# OWM condition code ranges that count as severe
SEVERE_CONDITION_GROUPS = {2}  # 2xx = thunderstorm
HEAVY_RAIN_IDS = {502, 503, 504, 522, 531}  # 5xx heavy-intensity rain
TORNADO_SQUALL_IDS = {771, 781}  # 7xx squall and tornado

SIMULATED_STORM = {
    "wind_speed": 62,
    "weather_id": 202,
    "weather_description": "thunderstorm with heavy rain",
    "temperature": 58,
}


def load_markets(config_path: Path = CONFIG_PATH) -> dict:
    with open(config_path) as f:
        return json.load(f)["markets"]


def get_api_key() -> str:
    key = os.environ.get("OPENWEATHER_API_KEY", "")
    if not key:
        print("ERROR: OPENWEATHER_API_KEY not set in environment / .env")
        sys.exit(1)
    return key


def fetch_weather(zip_code: str, api_key: str) -> dict:
    """Fetch current weather for a US zip code."""
    params = {
        "zip": f"{zip_code},US",
        "appid": api_key,
        "units": "imperial",
    }
    resp = requests.get(WEATHER_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def is_severe(weather_data: dict, threshold_wind: float) -> tuple[bool, str]:
    """Check if weather data indicates severe conditions.

    Returns (is_severe, severity) where severity is 'high' or 'medium'.
    """
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    conditions = weather_data.get("weather", [])

    # Check wind speed
    if wind_speed > threshold_wind:
        return True, "high"

    for cond in conditions:
        cond_id = cond.get("id", 0)
        group = cond_id // 100

        # Thunderstorm family (2xx)
        if group in SEVERE_CONDITION_GROUPS:
            return True, "high" if cond_id >= 210 else "medium"

        # Heavy rain (specific 5xx codes)
        if cond_id in HEAVY_RAIN_IDS:
            return True, "medium"

        # Tornado / squall (specific 7xx codes)
        if cond_id in TORNADO_SQUALL_IDS:
            return True, "high"

    return False, ""


def build_alert(market_key: str, market_cfg: dict, weather_data: dict,
                severity: str) -> dict:
    """Build a storm alert dict from weather data."""
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    conditions = weather_data.get("weather", [])
    description = conditions[0].get("description", "unknown") if conditions else "unknown"
    temp = weather_data.get("main", {}).get("temp", 0)

    return {
        "market": market_key,
        "market_name": f"{market_cfg['name']} {market_cfg['state']}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
        "severity": severity,
        "weather_description": description,
        "wind_speed": round(wind_speed, 1),
        "temperature": round(temp, 1),
        "affected_zips": market_cfg["zip_codes"],
    }


def build_simulated_alert(market_key: str, market_cfg: dict) -> dict:
    """Build a simulated storm alert for testing."""
    return {
        "market": market_key,
        "market_name": f"{market_cfg['name']} {market_cfg['state']}",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
        "severity": "high",
        "weather_description": SIMULATED_STORM["weather_description"],
        "wind_speed": SIMULATED_STORM["wind_speed"],
        "temperature": SIMULATED_STORM["temperature"],
        "affected_zips": market_cfg["zip_codes"],
        "simulated": True,
    }


def save_alert(alert: dict) -> Path:
    """Save a storm alert JSON to data/alerts/."""
    ALERTS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    path = ALERTS_DIR / f"storm_{alert['market']}_{date_str}.json"
    with open(path, "w") as f:
        json.dump(alert, f, indent=2)
    return path


def print_alert(alert: dict) -> None:
    """Print a storm alert to stdout."""
    wind = alert["wind_speed"]
    desc = alert["weather_description"]
    market = alert["market_name"]
    severity = alert["severity"].upper()
    sim = " (SIMULATED)" if alert.get("simulated") else ""
    print(
        f"  STORM ALERT{sim}: {desc} ({wind}mph) in {market} "
        f"[{severity}] — trigger storm outreach"
    )
    print(f"  Affected zips: {len(alert['affected_zips'])}")


def check_market(market_key: str, market_cfg: dict, api_key: str,
                 threshold_wind: float) -> dict | None:
    """Check weather for one market. Returns alert dict or None."""
    zip_code = MARKET_CHECK_ZIPS.get(market_key)
    if not zip_code:
        print(f"  No check zip configured for {market_key}, skipping")
        return None

    market_name = f"{market_cfg['name']} {market_cfg['state']}"
    print(f"  Checking {market_name} (zip {zip_code})...", end=" ", flush=True)

    try:
        data = fetch_weather(zip_code, api_key)
    except Exception as exc:
        print(f"ERROR: {exc}")
        return None

    severe, severity = is_severe(data, threshold_wind)

    if severe:
        print("SEVERE")
        alert = build_alert(market_key, market_cfg, data, severity)
        return alert

    wind = data.get("wind", {}).get("speed", 0)
    desc = ""
    if data.get("weather"):
        desc = data["weather"][0].get("description", "")
    print(f"OK ({desc}, {wind}mph)")
    return None


def check_all(markets: dict, api_key: str, threshold_wind: float) -> list[dict]:
    """Check all markets. Returns list of alerts."""
    alerts = []
    for key, cfg in markets.items():
        alert = check_market(key, cfg, api_key, threshold_wind)
        if alert:
            alerts.append(alert)
    return alerts


def run_monitor(markets: dict, api_key: str, threshold_wind: float) -> None:
    """Continuous monitoring loop — checks every 6 hours."""
    import schedule

    def job():
        print(f"\n{'='*60}")
        print(f"Weather check: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*60}")
        alerts = check_all(markets, api_key, threshold_wind)
        for alert in alerts:
            print_alert(alert)
            path = save_alert(alert)
            print(f"  Saved to {path}")
        if not alerts:
            print("All clear — no severe weather in any market")

    # Run immediately, then every 6 hours
    job()
    schedule.every(6).hours.do(job)

    print("\nMonitoring active — checking every 6 hours (Ctrl+C to stop)")
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor weather for storm damage outreach triggers"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--check-now",
        action="store_true",
        help="One-shot check of all markets",
    )
    mode.add_argument(
        "--monitor",
        action="store_true",
        help="Continuous check every 6 hours",
    )
    parser.add_argument(
        "--market",
        help="Check a specific market only (used with --check-now)",
    )
    parser.add_argument(
        "--threshold-wind",
        type=float,
        default=50,
        help="Wind speed threshold in mph (default: 50)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Simulate a storm alert without calling the API",
    )
    args = parser.parse_args()

    markets = load_markets()

    # Determine target markets
    if args.market:
        if args.market not in markets:
            print(
                f"Unknown market: {args.market}. "
                f"Options: {', '.join(markets.keys())}"
            )
            sys.exit(1)
        targets = {args.market: markets[args.market]}
    else:
        targets = markets

    # Test mode — simulate storm, no API needed
    if args.test:
        print(f"{'='*60}")
        print("TEST MODE — simulating storm alert")
        print(f"{'='*60}")
        for key, cfg in targets.items():
            alert = build_simulated_alert(key, cfg)
            print_alert(alert)
            path = save_alert(alert)
            print(f"  Saved to {path}")
        return

    # Live modes require API key
    api_key = get_api_key()

    if args.monitor:
        run_monitor(targets, api_key, args.threshold_wind)
    else:
        # --check-now
        print(f"{'='*60}")
        print(f"Weather check: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"Wind threshold: {args.threshold_wind} mph")
        print(f"{'='*60}")
        alerts = check_all(targets, api_key, args.threshold_wind)
        for alert in alerts:
            print_alert(alert)
            path = save_alert(alert)
            print(f"  Saved to {path}")
        if not alerts:
            print("All clear — no severe weather in any market")


if __name__ == "__main__":
    main()
