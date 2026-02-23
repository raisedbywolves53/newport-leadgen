"""Compile FL decision maker contacts from multiple source CSVs into unified format.

Reads:
  - data/final/florida_school_districts_food_service_contacts.csv
  - data/final/fl_federal_food_procurement_contacts_20260221.csv
  - data/final/florida_county_jail_food_contacts_20260221.csv

Writes:
  - data/contacts/fl_decision_makers.csv (unified format for dashboard)
"""

import csv
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
FINAL_DIR = DATA_DIR / "final"
CONTACTS_DIR = DATA_DIR / "contacts"


def load_school_districts():
    """Transform school district contacts into unified format."""
    path = FINAL_DIR / "florida_school_districts_food_service_contacts.csv"
    if not path.exists():
        print(f"  SKIP: {path} not found")
        return []

    contacts = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Food Service Director Name", "").strip()
            if not name or name.startswith("Not confirmed"):
                name = "[TBD — Call District]"

            enrollment = row.get("Approx Student Enrollment", "")
            district = row.get("District Name", "")
            county = row.get("County", "")
            email = row.get("Email", "").strip()
            phone = row.get("Department Phone", "").strip()
            notes_raw = row.get("Notes", "").strip()

            # Determine tier based on enrollment
            try:
                enroll_num = int(str(enrollment).replace(",", ""))
            except (ValueError, TypeError):
                enroll_num = 0

            if enroll_num >= 100000:
                tier = "Tier 1"
                influence = "High"
            elif enroll_num >= 50000:
                tier = "Tier 2"
                influence = "High"
            else:
                tier = "Tier 3"
                influence = "Medium"

            notes_parts = []
            if enrollment:
                notes_parts.append(f"~{enrollment} students")
            if notes_raw:
                notes_parts.append(notes_raw)

            contacts.append({
                "name": name,
                "title": row.get("Title", "Food Service Director"),
                "organization": district,
                "org_type": "Local — School District",
                "role_type": "Food Service",
                "tier": tier,
                "influence": influence,
                "geography": f"{county} County, FL",
                "source": "District Website",
                "email_available": "Yes" if email else "No",
                "phone_available": "Yes" if phone else "No",
                "contact_status": "Not Started",
                "last_contact": "",
                "next_action": "Schedule introductory call" if email else "Call department phone",
                "current_vendor": "Chartwells (Compass)" if "Chartwells" in notes_raw else "Unknown",
                "notes": "; ".join(notes_parts),
                "email": email,
                "phone": phone,
            })

    print(f"  School districts: {len(contacts)} contacts")
    return contacts


def load_federal_contacts():
    """Transform BOP/VA/Military contacts into unified format."""
    path = FINAL_DIR / "fl_federal_food_procurement_contacts_20260221.csv"
    if not path.exists():
        print(f"  SKIP: {path} not found")
        return []

    contacts = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            category = row.get("category", "")
            facility = row.get("facility_name", "")
            facility_type = row.get("facility_type", "")
            city = row.get("city", "")
            director = row.get("director_or_warden", "")
            main_phone = row.get("main_phone", "")
            food_phone = row.get("food_service_phone", "")
            food_contact = row.get("food_service_contact", "")
            branch = row.get("branch", "")
            commissary_dir = row.get("commissary_director", "")
            commissary_phone = row.get("commissary_phone", "")
            pop = row.get("population_approx", "")
            security = row.get("security_level", "")
            notes_raw = row.get("notes", "")

            if category == "BOP":
                org_type = "Federal — BOP"
                try:
                    pop_num = int(str(pop).replace(",", ""))
                except (ValueError, TypeError):
                    pop_num = 0
                tier = "Tier 1" if pop_num >= 1000 else "Tier 2"
                influence = "High"
                role_type = "Food Service"
                name = "[Food Service Administrator — Call]"
                title = "Food Service Administrator"
                phone = main_phone
                next_action = "Call institution, ask for Food Service Administrator"
                vendor = "Unknown — verify via SAM.gov"
                notes = f"~{pop} inmates. {security} security." if pop else ""
                if notes_raw:
                    notes += f" {notes_raw}"

                contacts.append({
                    "name": name,
                    "title": title,
                    "organization": facility,
                    "org_type": org_type,
                    "role_type": role_type,
                    "tier": tier,
                    "influence": influence,
                    "geography": f"{city}, FL",
                    "source": "BOP.gov",
                    "email_available": "No",
                    "phone_available": "Yes" if phone else "No",
                    "contact_status": "Not Started",
                    "last_contact": "",
                    "next_action": next_action,
                    "current_vendor": vendor,
                    "notes": notes.strip(),
                    "email": "",
                    "phone": phone,
                })

                # Also add warden if named
                if director and "call to confirm" not in director.lower():
                    contacts.append({
                        "name": director,
                        "title": "Warden",
                        "organization": facility,
                        "org_type": org_type,
                        "role_type": "Facility Leadership",
                        "tier": tier,
                        "influence": "Medium",
                        "geography": f"{city}, FL",
                        "source": "BOP.gov / Public Records",
                        "email_available": "No",
                        "phone_available": "Yes" if phone else "No",
                        "contact_status": "Not Started",
                        "last_contact": "",
                        "next_action": "Call institution main number",
                        "current_vendor": vendor,
                        "notes": f"Facility head. {notes.strip()}",
                        "email": "",
                        "phone": phone,
                    })

            elif category == "VA":
                org_type = "Federal — VA"
                tier = "Tier 2"
                influence = "High"
                phone_to_use = food_phone if food_phone and "call main" not in food_phone.lower() else main_phone

                contacts.append({
                    "name": "[NFS Manager — Call]",
                    "title": "Nutrition & Food Service Manager",
                    "organization": facility,
                    "org_type": org_type,
                    "role_type": "Food Service",
                    "tier": tier,
                    "influence": influence,
                    "geography": f"{city}, FL",
                    "source": "VA.gov",
                    "email_available": "No",
                    "phone_available": "Yes",
                    "contact_status": "Not Started",
                    "last_contact": "",
                    "next_action": f"Call NFS: {phone_to_use}" if phone_to_use else "Call facility",
                    "current_vendor": "Unknown",
                    "notes": notes_raw.strip() if notes_raw else f"VISN 8. Director: {director}",
                    "email": "",
                    "phone": phone_to_use,
                })

            elif category == "Military":
                org_type = f"Federal — Military ({branch})"
                # Commissary contacts
                if commissary_dir and "No full commissary" not in commissary_dir:
                    tier = "Tier 2"
                    contacts.append({
                        "name": commissary_dir,
                        "title": "Commissary Store Director",
                        "organization": facility,
                        "org_type": org_type,
                        "role_type": "Commissary",
                        "tier": tier,
                        "influence": "Medium",
                        "geography": f"{city}, FL",
                        "source": "DeCA / Installation Directory",
                        "email_available": "No",
                        "phone_available": "Yes" if commissary_phone else "No",
                        "contact_status": "Not Started",
                        "last_contact": "",
                        "next_action": "Call commissary, introduce Newport",
                        "current_vendor": "DeCA Prime Vendor (Sysco/US Foods)",
                        "notes": notes_raw.strip() if notes_raw else "",
                        "email": "",
                        "phone": commissary_phone,
                    })
                elif "shoppette" in (commissary_dir or "").lower():
                    # Skip shoppette-only bases
                    pass

    print(f"  Federal (BOP/VA/Military): {len(contacts)} contacts")
    return contacts


def load_county_jails():
    """Transform county jail contacts into unified format."""
    path = FINAL_DIR / "florida_county_jail_food_contacts_20260221.csv"
    if not path.exists():
        print(f"  SKIP: {path} not found")
        return []

    contacts = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            county = row.get("county", "")
            facility = row.get("facility_name", "")
            agency = row.get("managing_agency", "")
            pop = row.get("approx_daily_inmate_pop", "")
            model = row.get("food_service_model", "")
            vendor = row.get("food_service_vendor", "")
            purch_phone = row.get("purchasing_dept_phone", "")
            food_contact = row.get("food_service_contact", "")
            food_phone = row.get("food_service_phone", "")
            main_phone = row.get("main_facility_phone", "")
            county_purch_email = row.get("county_purchasing_email", "")

            try:
                pop_num = int(str(pop).replace(",", ""))
            except (ValueError, TypeError):
                pop_num = 0

            if pop_num >= 3000:
                tier = "Tier 1"
                influence = "High"
            elif pop_num >= 2000:
                tier = "Tier 2"
                influence = "High"
            else:
                tier = "Tier 2"
                influence = "Medium"

            is_self_op = "self-operated" in model.lower() if model else False
            is_contracted = "contracted" in model.lower() if model else False

            # Clean vendor
            if "N/A" in (vendor or ""):
                vendor_clean = "Self-Operated"
            elif vendor and "Unknown" not in vendor:
                vendor_clean = vendor.split("(")[0].strip()
            else:
                vendor_clean = "Unknown"

            phone_to_use = food_phone if food_phone and food_phone != purch_phone else purch_phone or main_phone

            if is_self_op:
                next_act = "PRIORITY: Self-operated = direct buyer. Call food service dept."
            elif is_contracted:
                next_act = f"Monitor for rebid. Current vendor: {vendor_clean}"
            else:
                next_act = "Call to determine food service model (self-op vs contracted)"

            # Extract named contact if available
            name = "[TBD — Call Facility]"
            title = "Food Service / Purchasing Contact"
            if food_contact and "Barry Martin" in food_contact:
                name = "Barry Martin"
                title = "Food Services Administrator"
            elif food_contact and "Joseph DeMore" in food_contact:
                name = "Joseph DeMore"
                title = "Corrections Director"

            notes = f"~{pop} daily inmates. Model: {model.split('(')[0].strip() if model else 'Unknown'}."

            contacts.append({
                "name": name,
                "title": title,
                "organization": f"{county} County — {agency}",
                "org_type": "Local — County Jail",
                "role_type": "Food Service / Purchasing",
                "tier": tier,
                "influence": influence,
                "geography": f"{county} County, FL",
                "source": "County Website / Sheriff Office",
                "email_available": "Yes" if county_purch_email and county_purch_email != "N/A" else "No",
                "phone_available": "Yes" if phone_to_use else "No",
                "contact_status": "Not Started",
                "last_contact": "",
                "next_action": next_act,
                "current_vendor": vendor_clean,
                "notes": notes,
                "email": county_purch_email if county_purch_email != "N/A" else "",
                "phone": phone_to_use,
            })

    print(f"  County jails: {len(contacts)} contacts")
    return contacts


def main():
    CONTACTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Compiling FL decision maker contacts...")
    all_contacts = []
    all_contacts.extend(load_school_districts())
    all_contacts.extend(load_federal_contacts())
    all_contacts.extend(load_county_jails())

    # Sort: Tier 1 first, then by org_type
    tier_order = {"Tier 1": 0, "Tier 2": 1, "Tier 3": 2}
    all_contacts.sort(key=lambda c: (tier_order.get(c["tier"], 9), c["org_type"], c["organization"]))

    # Write unified CSV (dashboard format — 16 standard columns + 2 extra)
    output_path = CONTACTS_DIR / "fl_decision_makers.csv"
    fieldnames = [
        "name", "title", "organization", "org_type",
        "role_type", "tier", "influence", "geography",
        "source", "email_available", "phone_available",
        "contact_status", "last_contact", "next_action",
        "current_vendor", "notes", "email", "phone",
    ]
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_contacts)

    print(f"\nTotal contacts: {len(all_contacts)}")
    print(f"  Tier 1: {sum(1 for c in all_contacts if c['tier'] == 'Tier 1')}")
    print(f"  Tier 2: {sum(1 for c in all_contacts if c['tier'] == 'Tier 2')}")
    print(f"  Tier 3: {sum(1 for c in all_contacts if c['tier'] == 'Tier 3')}")
    print(f"  Named contacts: {sum(1 for c in all_contacts if not c['name'].startswith('['))}")
    print(f"  With email: {sum(1 for c in all_contacts if c['email_available'] == 'Yes')}")
    print(f"  With phone: {sum(1 for c in all_contacts if c['phone_available'] == 'Yes')}")
    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
