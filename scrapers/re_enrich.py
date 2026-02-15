"""Re-enrich already-revealed prospects to capture all missing fields.

Apollo doesn't re-charge credits for people already revealed in your account.
This script calls enrich_person for each prospect and fills in:
- last_name, linkedin_url, phone
- company_website, company_linkedin, company_industry
- company_city, company_state, company_country

Usage:
    PYTHONPATH=. python scrapers/re_enrich.py
"""

import pandas as pd
import sys
import io
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from enrichment.apollo_client import ApolloClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENRICHED_DIR = PROJECT_ROOT / "data" / "enriched"


def re_enrich(df: pd.DataFrame, client: ApolloClient, segment_name: str) -> pd.DataFrame:
    """Re-enrich all prospects to capture full field set."""

    # Ensure all target columns exist
    for col in [
        "last_name", "linkedin_url", "phone",
        "company_website", "company_linkedin", "company_industry",
        "company_city", "company_state", "company_country",
    ]:
        if col not in df.columns:
            df[col] = ""

    total = len(df)
    updated = 0
    failed = 0

    print(f"\n  Re-enriching {total} prospects for {segment_name}...")

    for idx, row in df.iterrows():
        i = df.index.get_loc(idx) + 1
        apollo_id = row.get("apollo_id", "")

        if not apollo_id:
            failed += 1
            continue

        if i % 50 == 0 or i == 1:
            print(f"    Progress: {i}/{total} ({updated} updated)")

        try:
            enriched = client.enrich_person(apollo_id=apollo_id)
        except Exception as e:
            failed += 1
            continue

        if not enriched:
            failed += 1
            continue

        # Person fields
        if enriched.get("last_name"):
            df.at[idx, "last_name"] = enriched["last_name"]
        if enriched.get("first_name") and not row.get("first_name"):
            df.at[idx, "first_name"] = enriched["first_name"]
        if enriched.get("linkedin_url"):
            df.at[idx, "linkedin_url"] = enriched["linkedin_url"]
        if enriched.get("title"):
            df.at[idx, "title"] = enriched["title"]
        if enriched.get("email"):
            df.at[idx, "email"] = enriched["email"]
        if enriched.get("city"):
            df.at[idx, "city"] = enriched["city"]
        if enriched.get("state"):
            df.at[idx, "state"] = enriched["state"]
        if enriched.get("country"):
            df.at[idx, "country"] = enriched["country"]

        # Phone — check multiple sources
        phone = ""
        phone_numbers = enriched.get("phone_numbers") or []
        if phone_numbers:
            # Prefer sanitized_number from first entry
            phone = phone_numbers[0].get("sanitized_number", "") or phone_numbers[0].get("raw_number", "")
        if not phone:
            phone = enriched.get("organization_phone", "") or ""
        df.at[idx, "phone"] = phone

        # Organization fields
        org = enriched.get("organization", {}) or {}
        if org.get("website_url"):
            df.at[idx, "company_website"] = org["website_url"]
        if org.get("linkedin_url"):
            df.at[idx, "company_linkedin"] = org["linkedin_url"]
        if org.get("industry"):
            df.at[idx, "company_industry"] = org["industry"]
        if org.get("city"):
            df.at[idx, "company_city"] = org["city"]
        if org.get("state"):
            df.at[idx, "company_state"] = org["state"]
        if org.get("country"):
            df.at[idx, "company_country"] = org["country"]
        if org.get("primary_domain"):
            df.at[idx, "company_domain"] = org["primary_domain"]
        if org.get("name") and not row.get("company_name"):
            df.at[idx, "company_name"] = org["name"]

        updated += 1
        time.sleep(0.3)

    print(f"    DONE: {updated} updated, {failed} failed")
    print(f"    API stats: {client.stats}")
    return df


def audit(df: pd.DataFrame, name: str):
    """Print field completeness audit."""
    total = len(df)
    print(f"\n  {name} — FIELD AUDIT ({total} rows):")
    fields = [
        "first_name", "last_name", "title", "linkedin_url", "email", "phone",
        "company_name", "company_website", "company_linkedin",
        "company_industry", "company_city", "company_state", "company_country",
        "segment",
    ]
    for col in fields:
        if col in df.columns:
            filled = (df[col].fillna("").astype(str).str.strip().str.len() > 0).sum()
            pct = filled / total * 100
            print(f"    {col:25s} {filled:>5}/{total}  ({pct:5.1f}%)")
        else:
            print(f"    {col:25s}   MISSING")


def main():
    client = ApolloClient()

    for seg_file, seg_name in [
        ("segment_a_buyers_enriched.csv", "Segment A — Buyers"),
        ("segment_b_suppliers_enriched.csv", "Segment B — Suppliers"),
    ]:
        path = ENRICHED_DIR / seg_file
        if not path.exists():
            print(f"  Skipping {seg_file} — not found")
            continue

        df = pd.read_csv(path)
        df = re_enrich(df, client, seg_name)

        # Save
        df.to_csv(path, index=False)
        print(f"  Saved to {path}")

        audit(df, seg_name)

    print(f"\nTotal API stats: {client.stats}")


if __name__ == "__main__":
    main()
