#!/usr/bin/env python3
"""Collect market data from FPDS + USASpending for deliverables.

Pulls live data from existing API clients and writes deliverables/market_data.json,
consumed by web/src/data/*.js for the React web presentation.

Data collected:
  A. FPDS competition density by NAICS (10 primary food codes)
  B. FPDS competition density by PSC (13 food product categories)
  C. TAM sizing via USASpending (spending by NAICS + geography)
  D. Product opportunity rankings (research-based)

Usage:
    python deliverables/collect_market_data.py
    python deliverables/collect_market_data.py --fiscal-year 2025
"""

import argparse
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime

# Add project root + govcon to path
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, _project_root)
sys.path.insert(0, os.path.join(_project_root, "govcon"))

from enrichment.fpds_client import FPDSClient
from enrichment.usaspending_client import USASpendingClient


def load_config():
    """Load government contracts config."""
    config_path = os.path.join(
        _project_root,
        "config", "government_contracts.json"
    )
    with open(config_path) as f:
        return json.load(f)


def collect_fpds_by_naics(client, naics_codes, date_range):
    """Pull competition density stats per NAICS code from FPDS."""
    results = []

    for naics, desc in naics_codes.items():
        print(f"  FPDS NAICS {naics} ({desc})...", end=" ", flush=True)
        records = client.search_contracts(naics_code=naics, date_range=date_range)

        if not records:
            print("0 records")
            results.append({
                "naics": naics, "description": desc,
                "awards": 0, "avg_offers": 0, "sole_source_pct": 0, "avg_value": 0,
            })
            continue

        flat = [client.flatten_contract(r) for r in records]
        offers = [f["offers_received"] for f in flat if f["offers_received"] is not None]
        amounts = [f["obligated_amount"] for f in flat if f["obligated_amount"] > 0]
        sole_source = sum(1 for o in offers if o <= 1)

        avg_offers = round(sum(offers) / len(offers), 1) if offers else 0
        sole_pct = round(sole_source / len(offers) * 100, 1) if offers else 0
        avg_value = round(sum(amounts) / len(amounts)) if amounts else 0

        print(f"{len(records)} records, avg offers={avg_offers}, sole source={sole_pct}%")

        results.append({
            "naics": naics, "description": desc,
            "awards": len(records), "avg_offers": avg_offers,
            "sole_source_pct": sole_pct, "avg_value": avg_value,
        })
        time.sleep(0.5)

    return results


def collect_fpds_by_psc(client, psc_codes, date_range):
    """Pull competition density stats per PSC (product service code) from FPDS."""
    # Opportunity tier ratings based on market research
    opportunity_tiers = {
        "8905": "LOW",       # Meat — dominated by Tyson/JBS/Cargill
        "8910": "MODERATE",  # Dairy — regional distribution feasible
        "8915": "HIGH",      # Fruits & Vegetables — lowest concentration
        "8920": "MODERATE",  # Bakery — regional vendors compete well
        "8925": "HIGH",      # Confectionery — Newport's candy expertise
        "8930": "LOW",       # Jams — very niche
        "8935": "LOW",       # Soups — very niche
        "8940": "MODERATE",  # Special Dietary
        "8945": "MODERATE",  # Food Oils — commodity, regional feasible
        "8950": "MODERATE",  # Condiments — fewer mega-vendors
        "8955": "MODERATE",  # Coffee/Tea
        "8960": "MODERATE",  # Beverages
        "8970": "NONE",      # MREs — specialized military manufacturing
        "8975": "NONE",      # Tobacco — not relevant
    }

    results = []

    for psc, desc in psc_codes.items():
        print(f"  FPDS PSC {psc} ({desc})...", end=" ", flush=True)
        records = client.search_contracts(psc_code=psc, date_range=date_range)

        if not records:
            print("0 records")
            results.append({
                "psc": psc, "description": desc,
                "awards": 0, "avg_offers": 0, "sole_source_pct": 0,
                "total_spending": 0, "avg_value": 0,
                "top_vendors": [],
                "opportunity_tier": opportunity_tiers.get(psc, "UNKNOWN"),
            })
            continue

        flat = [client.flatten_contract(r) for r in records]
        offers = [f["offers_received"] for f in flat if f["offers_received"] is not None]
        amounts = [f["obligated_amount"] for f in flat if f["obligated_amount"] > 0]
        sole_source = sum(1 for o in offers if o <= 1)

        # Top vendors by contract count
        vendor_counts = Counter(f["vendor_name"] for f in flat if f["vendor_name"])
        top_vendors = [name for name, _ in vendor_counts.most_common(5)]

        avg_offers = round(sum(offers) / len(offers), 1) if offers else 0
        sole_pct = round(sole_source / len(offers) * 100, 1) if offers else 0
        total_spending = round(sum(amounts))
        avg_value = round(sum(amounts) / len(amounts)) if amounts else 0

        print(f"{len(records)} records, ${total_spending:,.0f} total")

        results.append({
            "psc": psc, "description": desc,
            "awards": len(records), "avg_offers": avg_offers,
            "sole_source_pct": sole_pct,
            "total_spending": total_spending, "avg_value": avg_value,
            "top_vendors": top_vendors,
            "opportunity_tier": opportunity_tiers.get(psc, "UNKNOWN"),
        })
        time.sleep(0.5)

    return results


def collect_tam_data(client, naics_prefixes, fiscal_year, target_states):
    """Pull TAM (Total Addressable Market) sizing from USASpending."""
    start, end = client.fiscal_year_range(fiscal_year)

    # Spending by NAICS
    print(f"  USASpending: spending by NAICS (FY{fiscal_year})...")
    by_naics = client.spending_by_naics(
        naics_require=naics_prefixes,
        time_period_start=start, time_period_end=end,
    )
    total = sum(r.get("aggregated_amount", 0) for r in by_naics)

    # Spending by geography (target states)
    print(f"  USASpending: spending by geography (FY{fiscal_year})...")
    by_geo = client.spending_by_geography(
        naics_require=naics_prefixes,
        time_period_start=start, time_period_end=end,
    )
    target_spending = sum(
        r.get("aggregated_amount", 0) for r in by_geo
        if r.get("shape_code") in target_states
    )

    return {
        "by_naics": [
            {
                "naics": r.get("code", ""),
                "name": r.get("name", ""),
                "amount": r.get("aggregated_amount", 0),
                "fiscal_year": fiscal_year,
            }
            for r in by_naics
        ],
        "total_spending": total,
        "target_states_spending": target_spending,
        "fiscal_year": fiscal_year,
        "target_states": target_states,
    }


def build_product_opportunity():
    """Product opportunity rankings based on federal food procurement research."""
    return {
        "priority_products": [
            {
                "psc": "8915", "name": "Fresh Produce", "tier": 1,
                "annual_spending": 1_900_000_000,
                "rationale": "Lowest vendor concentration, USDA actively diversifying vendors, FL location ideal for year-round sourcing",
            },
            {
                "psc": "8925", "name": "Confectionery & Nuts", "tier": 1,
                "annual_spending": 100_000_000,
                "rationale": "Directly aligned with Newport's candy wholesale expertise (Segment E), niche with fewer mega-vendors",
            },
            {
                "psc": "8910", "name": "Dairy & Eggs", "tier": 2,
                "annual_spending": 552_000_000,
                "rationale": "Regional distribution feasible, fluid milk and eggs more accessible than cheese market",
            },
            {
                "psc": "8920", "name": "Bakery & Cereal Products", "tier": 2,
                "annual_spending": 276_000_000,
                "rationale": "Covered by NAICS 424410, regional vendors compete well, lower barriers",
            },
            {
                "psc": "8950", "name": "Condiments & Related", "tier": 3,
                "annual_spending": 176_000_000,
                "rationale": "Niche categories with fewer mega-vendors, covered by general grocery NAICS",
            },
        ],
        "avoid": [
            {
                "psc": "8905", "name": "Meat, Poultry, Fish",
                "rationale": "Dominated by Tyson/JBS/Cargill (83% pork, 72% poultry market share)",
            },
            {
                "psc": "8970", "name": "MREs/Composite Food Packages",
                "rationale": "Specialized military manufacturing, requires dedicated production facilities",
            },
        ],
        "key_insight": "In 10 of 13 food categories, just 5 companies control majority of USDA spending. Top 25 vendors get 45% of all spending. Concentration creates opportunity in underserved categories.",
    }


def main():
    parser = argparse.ArgumentParser(description="Collect market data for deliverables")
    parser.add_argument("--fiscal-year", type=int, default=2025,
                        help="Fiscal year for data collection (default: 2025)")
    args = parser.parse_args()

    config = load_config()
    primary_naics = config["naics_codes"]["primary"]
    psc_codes = config["psc_codes"]
    target_states = config["target_states"]
    naics_prefixes = ["4244", "7231"]  # food wholesale + food service

    # FPDS date range for fiscal year
    fy_start = f"{args.fiscal_year - 1}/10/01"
    fy_end = f"{args.fiscal_year}/09/30"
    date_range = f"[{fy_start}, {fy_end}]"

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "market_data.json")

    print("=" * 60)
    print("Newport GovCon Market Data Collector")
    print(f"Fiscal Year: {args.fiscal_year}")
    print("=" * 60)

    market_data = {
        "generated_at": datetime.now().isoformat(),
        "fiscal_year": args.fiscal_year,
    }

    # 1. FPDS competition by NAICS
    print(f"\n[1/4] FPDS competition density by NAICS ({len(primary_naics)} codes)...")
    fpds_client = FPDSClient()
    by_naics = collect_fpds_by_naics(fpds_client, primary_naics, date_range)

    # Compute aggregate totals
    total_awards = sum(r["awards"] for r in by_naics)
    weighted_sole = sum(r["awards"] * r["sole_source_pct"] / 100 for r in by_naics if r["awards"] > 0)
    total_sole_pct = round(weighted_sole / total_awards * 100, 1) if total_awards > 0 else 0
    weighted_offers = sum(r["awards"] * r["avg_offers"] for r in by_naics if r["awards"] > 0)
    total_avg_offers = round(weighted_offers / total_awards, 1) if total_awards > 0 else 0

    market_data["fpds"] = {
        "by_naics": by_naics,
        "totals": {
            "transactions": total_awards,
            "avg_offers": total_avg_offers,
            "sole_source_pct": total_sole_pct,
        },
    }

    # 2. FPDS competition by PSC
    print(f"\n[2/4] FPDS competition density by PSC ({len(psc_codes)} product codes)...")
    by_psc = collect_fpds_by_psc(fpds_client, psc_codes, date_range)
    market_data["fpds"]["by_psc"] = by_psc

    print(f"\n  FPDS stats: {fpds_client.stats}")

    # 3. TAM sizing
    print(f"\n[3/4] USASpending TAM sizing (FY{args.fiscal_year})...")
    usa_client = USASpendingClient()
    tam = collect_tam_data(usa_client, naics_prefixes, args.fiscal_year, target_states)
    market_data["tam"] = tam

    print(f"  Total federal food spending: ${tam['total_spending']:,.0f}")
    print(f"  Target states spending: ${tam['target_states_spending']:,.0f}")

    # 4. Product opportunity analysis
    print("\n[4/4] Building product opportunity analysis...")
    market_data["product_opportunity"] = build_product_opportunity()

    # Write output
    with open(output_path, "w") as f:
        json.dump(market_data, f, indent=2)

    print(f"\nSaved: {output_path}")
    print(f"File size: {os.path.getsize(output_path):,} bytes")
    print("\nDone.")


if __name__ == "__main__":
    main()
