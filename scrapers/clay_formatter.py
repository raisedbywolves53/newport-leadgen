"""Format scraped data for Clay enrichment platform and generate instruction docs.

Usage:
    python scrapers/clay_formatter.py --input data/raw/homeowners_oakland_county_mi_20260214.csv --icp-type new_homeowners
    python scrapers/clay_formatter.py --input data/raw/businesses_real_estate_agents_20260214.csv --icp-type real_estate_agents
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

ICP_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "icp_definitions.json"

HOMEOWNER_ICP_TYPES = {"new_homeowners", "aging_neighborhoods", "storm_damage"}

BUSINESS_ICP_TYPES = {
    "real_estate_agents",
    "property_managers",
    "home_inspectors",
    "insurance_agents",
    "home_builders",
    "adjacent_trades",
    "commercial_properties",
}

ALL_ICP_TYPES = HOMEOWNER_ICP_TYPES | BUSINESS_ICP_TYPES

HOMEOWNER_COLUMNS = [
    "full_address",
    "city",
    "state",
    "zip",
    "year_built",
    "sold_date",
    "sold_price",
    "sqft",
    "aging_door",
    "spring_risk",
    "icp_type",
    "market",
    "outreach_channels",
]

BUSINESS_COLUMNS = [
    "company_name",
    "address",
    "city",
    "state",
    "zip",
    "phone",
    "website",
    "rating",
    "review_count",
    "icp_type",
    "market",
    "outreach_channels",
    "notes",
]

CLAYGENT_PROMPTS = {
    "new_homeowners": (
        "Visit the property listing for {full_address}. What year was the home "
        "built? Does the listing mention garage door condition, age, or inspection "
        "issues? Does it have an attached garage?"
    ),
    "real_estate_agents": (
        "Find this real estate agent's recent activity. How many homes have they "
        "sold or listed in the last 12 months? Do they focus on residential "
        "single-family homes? What brokerage are they with?"
    ),
    "property_managers": (
        "Visit {website}. How many properties or units does this company manage? "
        "Do they manage residential properties with garages? Who is the owner, "
        "operations manager, or maintenance director?"
    ),
    "home_inspectors": (
        "Visit {website}. How many inspections has this company completed? Do "
        "they serve the local area? What certifications do they list (ASHI, "
        "InterNACHI)?"
    ),
    "insurance_agents": (
        "Visit {website}. Does this agent specialize in homeowners or property "
        "insurance? Are they independent or captive?"
    ),
    "home_builders": (
        "Visit {website}. Does this company build new homes? Approximately how "
        "many per year? What cities or developments do they build in? Do they "
        "mention garage specifications?"
    ),
    "adjacent_trades": (
        "Visit {website}. How long has this company been in business? Do they "
        "serve residential customers? What areas do they serve?"
    ),
    "commercial_properties": (
        "Look at this business on Google Maps. Does it have visible commercial "
        "garage doors, loading docks, or overhead doors? Approximately how many "
        "doors?"
    ),
}


def load_icp_config(config_path: Path = ICP_CONFIG_PATH) -> dict:
    """Load ICP definitions and return a dict keyed by icp_type."""
    with open(config_path) as f:
        icps = json.load(f)["icps"]
    return {icp["icp_type"]: icp for icp in icps}


def get_outreach_channels(icp_type: str, icp_config: dict) -> str:
    """Get comma-separated outreach channels for an ICP type."""
    icp = icp_config.get(icp_type, {})
    channels = icp.get("outreach_channels", [])
    return ", ".join(channels)


def format_homeowner(df: pd.DataFrame, icp_type: str, channels: str) -> pd.DataFrame:
    """Map raw homeowner scraper columns to Clay-ready columns."""
    out = pd.DataFrame()

    out["full_address"] = df.get("formatted_address", pd.Series(dtype=str))
    out["city"] = df.get("city", pd.Series(dtype=str))
    out["state"] = df.get("state", pd.Series(dtype=str))
    out["zip"] = df.get("zip_code", pd.Series(dtype=str))
    out["year_built"] = df.get("year_built")
    out["sold_date"] = df.get("last_sold_date", pd.Series(dtype=str))
    out["sold_price"] = df.get("sold_price")
    out["sqft"] = df.get("sqft")
    out["aging_door"] = df.get("aging_door", False)
    out["spring_risk"] = df.get("spring_risk", False)
    out["icp_type"] = icp_type
    out["market"] = df.get("market", "")
    out["outreach_channels"] = channels

    return out[HOMEOWNER_COLUMNS]


def format_business(df: pd.DataFrame, icp_type: str, channels: str) -> pd.DataFrame:
    """Map raw gmaps scraper columns to Clay-ready columns."""
    out = pd.DataFrame()

    out["company_name"] = df.get("name", pd.Series(dtype=str))
    out["address"] = df.get("formatted_address", pd.Series(dtype=str))
    out["city"] = df.get("city", pd.Series(dtype=str))
    out["state"] = df.get("state", pd.Series(dtype=str))
    out["zip"] = df.get("zip", pd.Series(dtype=str))
    out["phone"] = df.get("phone", "")
    out["website"] = df.get("website", "")
    out["rating"] = df.get("rating")
    out["review_count"] = df.get("user_ratings_total", 0)
    out["icp_type"] = icp_type
    out["market"] = df.get("market", "")
    out["outreach_channels"] = channels
    out["notes"] = ""

    return out[BUSINESS_COLUMNS]


def generate_instructions(icp_type: str, icp_config: dict) -> str:
    """Generate Clay workflow instructions markdown for an ICP type."""
    icp = icp_config.get(icp_type, {})
    display_name = icp.get("display_name", icp_type)
    claygent_prompt = CLAYGENT_PROMPTS.get(icp_type, "")
    is_business = icp_type in BUSINESS_ICP_TYPES

    decision_maker_step = ""
    if is_business:
        decision_maker_step = (
            "\n## Step 4: Add enrichment — Find Decision Maker\n\n"
            "1. Click **+ Add Column** > **Find Decision Maker**\n"
            "2. Map the `company_name` column as the company input\n"
            "3. Set role filter to relevant titles (e.g., Owner, Manager, "
            "Director of Operations)\n"
            "4. Run the enrichment\n"
        )
        remaining_offset = 1
    else:
        remaining_offset = 0

    step5 = 4 + remaining_offset
    step6 = 5 + remaining_offset
    step7 = 6 + remaining_offset

    lines = f"""# Clay Import Instructions: {display_name}

**ICP Type:** `{icp_type}`
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Step 1: Import CSV into Clay

1. Log into [Clay](https://app.clay.com)
2. Click **Create New Table**
3. Click **Import CSV** and upload the corresponding `{icp_type}_*.csv` file from `data/clay_ready/`
4. Verify all columns imported correctly

## Step 2: Add enrichment — Find Work Email

1. Click **+ Add Column** > **Find Work Email (Waterfall)**
2. Map the following input columns:
   - {"`full_address`" if not is_business else "`company_name`"} as the primary lookup
   - `city`, `state` as location context
3. Enable all available email providers for maximum coverage
4. Run the enrichment and wait for completion

## Step 3: Add enrichment — Find Phone Number

1. Click **+ Add Column** > **Find Phone Number (Waterfall)**
2. Map the {"`full_address`" if not is_business else "`company_name`"} column as input
3. Enable all available phone providers
4. Run the enrichment
{decision_maker_step}
## Step {step5}: Add Claygent research column

1. Click **+ Add Column** > **Claygent**
2. Use this research prompt:

```
{claygent_prompt}
```

3. Map the referenced columns from your table
4. Run the Claygent — this will take longer as it visits websites

## Step {step6}: Review and clean results

1. Sort by the new email/phone columns
2. **Remove** any rows with no email AND no phone (no way to reach them)
3. Review Claygent output for quality — flag or remove irrelevant results
4. Check for obviously wrong data (e.g., businesses outside target markets)

## Step {step7}: Export enriched CSV

1. Click **Export** > **Download as CSV**
2. Save to: `data/clay_enriched/{icp_type}_{{market}}_{{date}}.csv`
3. This enriched file is the input for the outreach campaign system
"""
    return lines


def main():
    parser = argparse.ArgumentParser(
        description="Format scraped data for Clay enrichment upload"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to raw CSV from homeowner_scraper or gmaps_scraper",
    )
    parser.add_argument(
        "--icp-type",
        required=True,
        choices=sorted(ALL_ICP_TYPES),
        help="ICP type for this data",
    )
    parser.add_argument(
        "--output-dir",
        default="./data/clay_ready/",
        help="Directory for Clay-ready outputs (default: ./data/clay_ready/)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}")
        sys.exit(1)

    icp_type = args.icp_type
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    icp_config = load_icp_config()

    channels = get_outreach_channels(icp_type, icp_config)

    print(f"Reading {input_path}...")
    df = pd.read_csv(input_path)
    print(f"  {len(df)} rows, {len(df.columns)} columns")

    if icp_type in HOMEOWNER_ICP_TYPES:
        formatted = format_homeowner(df, icp_type, channels)
    else:
        formatted = format_business(df, icp_type, channels)

    # Save Clay-ready CSV
    date_str = datetime.now().strftime("%Y%m%d")
    csv_path = output_dir / f"{icp_type}_{date_str}.csv"
    formatted.to_csv(csv_path, index=False)
    print(f"  Saved {len(formatted)} rows to {csv_path}")

    # Generate and save instructions
    instructions = generate_instructions(icp_type, icp_config)
    md_path = output_dir / f"clay_instructions_{icp_type}.md"
    md_path.write_text(instructions)
    print(f"  Saved instructions to {md_path}")

    # Summary
    print(f"\nDone: {icp_type}")
    print(f"  CSV columns: {list(formatted.columns)}")
    print(f"  Rows: {len(formatted)}")
    if "market" in formatted.columns:
        markets = formatted["market"].value_counts()
        for market, count in markets.items():
            print(f"    {market}: {count}")


if __name__ == "__main__":
    main()
