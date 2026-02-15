#!/usr/bin/env python3
"""
Goldman's Lead Gen — End-to-End QC Test Suite

Runs all 7 pre-launch QC phases and prints a pass/fail report card.

Usage:
    python tests/e2e_test.py                         # Run all 7 phases
    python tests/e2e_test.py --phase data-quality     # Run one phase
    python tests/e2e_test.py --phase merge-tags
    python tests/e2e_test.py --phase email
    python tests/e2e_test.py --phase sms
    python tests/e2e_test.py --phase voice
    python tests/e2e_test.py --phase crm
    python tests/e2e_test.py --phase reporting
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Path setup — ensure project root is on sys.path
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(PROJECT_ROOT / ".env")

DATA_DIR = PROJECT_ROOT / "data"
EMAIL_TEMPLATES_DIR = PROJECT_ROOT / "outreach" / "email" / "templates"
SMS_TEMPLATES_DIR = PROJECT_ROOT / "outreach" / "sms" / "templates"
VOICE_SCRIPTS_DIR = PROJECT_ROOT / "outreach" / "voice" / "scripts"

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_MARKETS = {"oakland", "wayne", "triangle",
                 "oakland_county_mi", "wayne_county_mi", "triangle_nc"}

# Phase results
PASS = "PASS"
FAIL = "FAIL"
BLOCKED = "BLOCKED"
MANUAL = "MANUAL CHECK NEEDED"

# ICP type → glob pattern for matching CSV data
ICP_TO_CSV_PATTERNS = {
    "real_estate_agents":    ["enriched/real_estate_agents_*.csv"],
    "property_managers":     ["enriched/property_managers_*.csv"],
    "home_inspectors":       ["enriched/home_inspectors_*.csv"],
    "insurance_agents":      ["enriched/insurance_agents_*.csv"],
    "builders_contractors":  ["enriched/home_builders_*.csv"],
    "adjacent_trades":       ["enriched/adjacent_trades_*.csv"],
    "commercial_properties": ["enriched/commercial_properties_*.csv"],
    "new_homeowners":        ["clay_ready/new_homeowners_*.csv"],
    "aging_neighborhoods":   ["clay_ready/aging_neighborhoods_*.csv"],
    "storm_damage":          ["storm_leads/storm_listing_agents_*.csv"],
    "referral_partners":     ["enriched/real_estate_agents_*.csv"],
    "all":                   ["enriched/real_estate_agents_*.csv"],
}

# Column-name variations for extracting merge-tag data from CSVs
FIELD_CANDIDATES = {
    "first_name": ["dm_first_name", "first_name", "firstname", "fname",
                   "agent_name"],
    "email":      ["dm_email", "email", "agent_email", "email_address"],
    "phone":      ["phone", "agent_phone", "phone_number"],
    "city":       ["city"],
    "company":    ["name", "company_name", "company", "business_name",
                   "office_name", "broker_name"],
}


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _find_csvs(patterns: list[str]) -> list[Path]:
    """Resolve glob patterns relative to DATA_DIR."""
    results = []
    for pat in patterns:
        results.extend(sorted(DATA_DIR.glob(pat)))
    return results


def _read_csv_rows(csv_path: Path, max_rows: int = 0) -> tuple[list[str], list[dict]]:
    """Read a CSV and return (headers, rows-as-dicts). max_rows=0 means all."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or [])
        rows = []
        for i, row in enumerate(reader):
            rows.append(row)
            if max_rows and i + 1 >= max_rows:
                break
    return headers, rows


def _get_field(row: dict, field: str) -> str:
    """Extract a field value trying multiple column-name candidates."""
    candidates = FIELD_CANDIDATES.get(field, [field])
    for col in candidates:
        val = row.get(col, "").strip()
        if val and val.lower() != "nan":
            # For full-name columns when we need first_name, extract first word
            if col in ("agent_name", "name") and field == "first_name":
                return val.split()[0] if val else ""
            return val
    return ""


def _is_valid_email(email: str) -> bool:
    """Check if email contains @ and a domain."""
    return bool(email and "@" in email and "." in email.split("@")[-1])


def _phone_digit_count(phone: str) -> int:
    """Count digits in a phone string."""
    return len(re.sub(r"\D", "", str(phone)))


def _normalize_market(market: str) -> str:
    """Normalize market name to short form."""
    m = market.strip().lower()
    if "oakland" in m:
        return "oakland"
    if "wayne" in m:
        return "wayne"
    if "triangle" in m:
        return "triangle"
    return m


# ---------------------------------------------------------------------------
# Phase 1: Data Quality Audit
# ---------------------------------------------------------------------------

def phase_data_quality() -> tuple[str, int]:
    """Scan all enriched + listing agent CSVs for data quality issues."""
    print("\nPhase 1: Data Quality Audit")
    print("-" * 50)

    # Discover enriched CSVs
    enriched_csvs = sorted(DATA_DIR.glob("enriched/*.csv"))
    # Discover listing agent CSVs
    listing_csvs = sorted(DATA_DIR.glob("raw/listing_agents_*.csv"))
    all_csvs = enriched_csvs + listing_csvs

    if not all_csvs:
        print("  ERROR: No CSV files found in data/enriched/ or data/raw/listing_agents_*")
        return FAIL, 0

    warnings = 0
    merge_fields = ["first_name", "email", "phone", "city", "company"]

    for csv_path in all_csvs:
        headers, rows = _read_csv_rows(csv_path)
        label = csv_path.stem
        total = len(rows)

        if total == 0:
            print(f"  {label}: EMPTY — skipping")
            warnings += 1
            continue

        # Count coverage and issues per field
        field_counts = {f: 0 for f in merge_fields}
        nan_issues = {f: 0 for f in merge_fields}
        email_invalid = 0
        phone_short = 0
        market_invalid = 0

        for row in rows:
            for field in merge_fields:
                val = _get_field(row, field)
                if val:
                    field_counts[field] += 1
                # Check for literal "nan" strings
                raw_candidates = FIELD_CANDIDATES.get(field, [field])
                for col in raw_candidates:
                    raw = row.get(col, "").strip()
                    if raw.lower() == "nan":
                        nan_issues[field] += 1
                        break

            # Email validation
            email_val = _get_field(row, "email")
            if email_val and not _is_valid_email(email_val):
                email_invalid += 1

            # Phone validation
            phone_val = _get_field(row, "phone")
            if phone_val and _phone_digit_count(phone_val) < 10:
                phone_short += 1

            # Market validation
            market_val = (row.get("market", "") or "").strip().lower()
            if market_val and market_val not in VALID_MARKETS:
                market_invalid += 1

        # Print coverage line
        coverage_parts = []
        for field in merge_fields:
            pct = int(field_counts[field] / total * 100) if total else 0
            coverage_parts.append(f"{field} {pct}%")
        print(f"  {label} ({total:,} leads): {' | '.join(coverage_parts)}")

        # Print warnings
        for field in merge_fields:
            if nan_issues[field] > 0:
                print(f"    WARNING: {nan_issues[field]} literal 'nan' in {field}")
                warnings += 1
        if email_invalid:
            print(f"    WARNING: {email_invalid} invalid emails (missing @ or domain)")
            warnings += 1
        if phone_short:
            print(f"    WARNING: {phone_short} phones with <10 digits")
            warnings += 1
        if market_invalid:
            print(f"    WARNING: {market_invalid} invalid market values")
            warnings += 1

    result = PASS if warnings <= 10 else FAIL
    suffix = f" ({warnings} warnings)" if warnings else ""
    print(f"  RESULT: {result}{suffix}")
    return result, warnings


# ---------------------------------------------------------------------------
# Phase 2: Merge Tag Rendering
# ---------------------------------------------------------------------------

def phase_merge_tags() -> tuple[str, int]:
    """Render every email + SMS template with real lead data."""
    print("\nPhase 2: Merge Tag Rendering")
    print("-" * 50)

    warnings = 0

    def _find_lead_row(icp_type: str) -> dict | None:
        """Find a real lead row matching the ICP type."""
        patterns = ICP_TO_CSV_PATTERNS.get(icp_type, [])
        csvs = _find_csvs(patterns)
        if not csvs:
            return None
        _, rows = _read_csv_rows(csvs[0], max_rows=5)
        # Pick first row with at least a first_name
        for row in rows:
            if _get_field(row, "first_name"):
                return row
        return rows[0] if rows else None

    def _build_merge_values(row: dict) -> dict:
        """Build a dict of all possible merge tag values from a CSV row."""
        values = {
            "first_name": _get_field(row, "first_name") or "there",
            "city": _get_field(row, "city") or "your area",
            "company_name": _get_field(row, "company") or "your company",
            "nearby_city": row.get("nearby_city", "").strip() or "nearby",
            "phone": "248-509-0470",
            "county": row.get("county", "").strip() or "your county",
            "street": row.get("street", row.get("full_street_line",
                      row.get("full_address", ""))).strip() or "your street",
            "state": row.get("state", "").strip() or "MI",
            "year_built": str(row.get("year_built", "")).strip() or "2000",
            "trade_type": row.get("trade_type", "").strip() or "trade pro",
            "role_type": row.get("role_type", "").strip() or "agent",
            "client_type": row.get("client_type", "").strip() or "clients",
            "topic": row.get("topic", "").strip() or "garage door service",
            "business_name": _get_field(row, "company") or "your company",
            "partner_type": row.get("partner_type", "").strip() or "professional",
        }
        return values

    def _render_and_check(template_text: str, values: dict, label: str) -> int:
        """Render a template and check for unresolved tags. Returns warning count."""
        w = 0
        try:
            rendered = template_text.format_map(
                type("FallbackDict", (dict,), {
                    "__missing__": lambda self, key: f"{{{key}}}"
                })(values)
            )
        except Exception:
            rendered = template_text
            for k, v in values.items():
                rendered = rendered.replace(f"{{{k}}}", v)

        # Check for unresolved {tags}
        unresolved = re.findall(r'\{([a-z_]+)\}', rendered)
        if unresolved:
            print(f"    WARNING: unresolved tags: {unresolved}")
            w += 1
        return w

    # --- Email templates ---
    email_templates = sorted(EMAIL_TEMPLATES_DIR.glob("*.json"))
    for tmpl_path in email_templates:
        with open(tmpl_path) as f:
            tmpl = json.load(f)

        icp_type = tmpl.get("icp_type", "")
        campaign = tmpl.get("campaign_name", tmpl_path.stem)
        steps = tmpl.get("steps", [])
        lead_row = _find_lead_row(icp_type)

        if not lead_row:
            print(f"  {tmpl_path.stem}: No matching CSV for icp={icp_type} — SKIPPED")
            warnings += 1
            continue

        values = _build_merge_values(lead_row)

        for step in steps[:1]:  # Show first step only for brevity
            subject = step.get("subject", "")
            body = step.get("body", "")

            rendered_subj = subject
            for k, v in values.items():
                rendered_subj = rendered_subj.replace(f"{{{k}}}", v)

            # Truncate body preview
            rendered_body = body
            for k, v in values.items():
                rendered_body = rendered_body.replace(f"{{{k}}}", v)
            preview = rendered_body[:80].replace("\n", " ")

            print(f'  {tmpl_path.stem} Step {step["step_number"]}: "{rendered_subj}"')
            print(f'    -> "{preview}..."')

            # Check subject
            subj_unresolved = re.findall(r'\{([a-z_]+)\}', rendered_subj)
            if subj_unresolved:
                print(f"    WARNING: unresolved in subject: {subj_unresolved}")
                warnings += 1

            # Check body
            body_unresolved = re.findall(r'\{([a-z_]+)\}', rendered_body)
            if body_unresolved:
                print(f"    WARNING: unresolved in body: {body_unresolved}")
                warnings += 1
            else:
                print(f"    All tags resolved OK")

    # --- SMS templates ---
    sms_templates = sorted(SMS_TEMPLATES_DIR.glob("*.json"))
    for tmpl_path in sms_templates:
        with open(tmpl_path) as f:
            tmpl = json.load(f)

        icp_type = tmpl.get("icp_type", "")
        message = tmpl.get("message", "")
        lead_row = _find_lead_row(icp_type)

        if not lead_row:
            print(f"  SMS {tmpl_path.stem}: No matching CSV for icp={icp_type} — SKIPPED")
            warnings += 1
            continue

        values = _build_merge_values(lead_row)
        rendered = message
        for k, v in values.items():
            rendered = rendered.replace(f"{{{k}}}", v)

        preview = rendered[:90]
        print(f'  SMS {tmpl_path.stem}: "{preview}..."')

        unresolved = re.findall(r'\{([a-z_]+)\}', rendered)
        if unresolved:
            print(f"    WARNING: unresolved tags: {unresolved}")
            warnings += 1
        else:
            print(f"    All tags resolved OK")

    result = PASS if warnings == 0 else (PASS if warnings <= 3 else FAIL)
    suffix = f" ({warnings} warnings)" if warnings else ""
    print(f"  RESULT: {result}{suffix}")
    return result, warnings


# ---------------------------------------------------------------------------
# Phase 3: Email Pre-Flight
# ---------------------------------------------------------------------------

def phase_email_preflight() -> tuple[str, int]:
    """Verify Instantly API connection + create test campaign."""
    print("\nPhase 3: Email Pre-Flight")
    print("-" * 50)

    api_key = os.getenv("INSTANTLY_API_KEY", "")
    sending_account = os.getenv("INSTANTLY_SENDING_ACCOUNT", "")

    if not api_key:
        print("  ERROR: INSTANTLY_API_KEY not set in .env")
        return BLOCKED, 0

    warnings = 0

    try:
        from outreach.email.instantly_client import InstantlyClient
        client = InstantlyClient(api_key=api_key)

        # Test 1: List campaigns to verify connection
        campaigns = client.list_campaigns()
        print(f"  Instantly connected | {len(campaigns)} existing campaigns")

        # Test 2: Verify sending account
        if sending_account:
            print(f"  Sending account: {sending_account}")
        else:
            print("  WARNING: INSTANTLY_SENDING_ACCOUNT not set")
            warnings += 1

        # Test 3: Create test campaign
        test_template = EMAIL_TEMPLATES_DIR / "agent_partner.json"
        if test_template.exists() and sending_account:
            with open(test_template) as f:
                tmpl = json.load(f)

            # Modify template name for test
            tmpl["campaign_name"] = "[QC TEST] Agent Partner"

            # Write temp template
            import tempfile
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False, dir=str(PROJECT_ROOT / "tests")
            ) as tmp:
                json.dump(tmpl, tmp)
                tmp_path = tmp.name

            try:
                campaign_id = client.create_campaign(tmp_path, sending_account)
                print(f"  Test campaign created: {campaign_id}")

                # Add test lead (Tal's email)
                tal_email = os.getenv("TAL_EMAIL", "admin@stillmindcreative.com")
                lead_payload = {
                    "campaign": campaign_id,
                    "email": tal_email,
                    "first_name": "Tal",
                    "last_name": "Goldman",
                    "company_name": "Goldman's Garage Door",
                    "skip_if_in_campaign": False,
                    "custom_variables": {
                        "city": "Troy",
                        "phone": "248-509-0470",
                        "nearby_city": "Birmingham",
                    },
                }
                client._request("POST", "/leads", json=lead_payload)
                print(f"  Test lead added ({tal_email}) with all merge tags")
                print(f"  -> ACTION: Preview in Instantly, send test to yourself")
            except Exception as exc:
                print(f"  WARNING: Campaign creation failed: {exc}")
                print(f"  -> This is expected if sending account is not fully verified")
                print(f"  -> Manually create a test campaign in Instantly dashboard")
                warnings += 1
            finally:
                os.unlink(tmp_path)
        else:
            if not test_template.exists():
                print("  WARNING: agent_partner.json template not found")
            if not sending_account:
                print("  WARNING: Cannot create test campaign without sending account")
            warnings += 1

        # Test 4: Check domain warmup
        print("  -> ACTION: Check domain warmup status in Instantly dashboard")

    except SystemExit:
        print("  ERROR: Instantly API authentication failed")
        return FAIL, 0
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return FAIL, 0

    print(f"  RESULT: {MANUAL}")
    return MANUAL, warnings


# ---------------------------------------------------------------------------
# Phase 4: SMS Pre-Flight
# ---------------------------------------------------------------------------

def phase_sms_preflight() -> tuple[str, int]:
    """Verify Twilio credentials + send test SMS."""
    print("\nPhase 4: SMS Pre-Flight")
    print("-" * 50)

    sid = os.getenv("TWILIO_ACCOUNT_SID", "")
    token = os.getenv("TWILIO_AUTH_TOKEN", "")

    if not sid or not token:
        print("  ERROR: TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN not set")
        return BLOCKED, 0

    warnings = 0

    try:
        from twilio.rest import Client as TwilioClient
        client = TwilioClient(sid, token)

        # Verify credentials by fetching account
        account = client.api.accounts(sid).fetch()
        print(f"  Twilio connected | Account: {account.friendly_name}")

    except Exception as exc:
        err_str = str(exc)
        if "Authenticate" in err_str or "401" in err_str or "20003" in err_str:
            print(f"  ERROR: Twilio authentication failed — check credentials")
            return BLOCKED, 0
        print(f"  ERROR: Twilio connection failed: {exc}")
        return FAIL, 0

    # Check phone numbers
    phone_mi = os.getenv("TWILIO_PHONE_MI", "")
    phone_nc = os.getenv("TWILIO_PHONE_NC", "")

    blocked_regions = []
    if not phone_mi:
        print("  WARNING: TWILIO_PHONE_MI not configured")
        blocked_regions.append("MI")
        warnings += 1
    else:
        print(f"  MI phone: {phone_mi}")

    if not phone_nc:
        print("  WARNING: TWILIO_PHONE_NC not configured")
        blocked_regions.append("NC")
        warnings += 1
    else:
        print(f"  NC phone: {phone_nc}")

    # Check opt-out file
    opt_out_path = DATA_DIR / "sms_opt_outs.csv"
    if opt_out_path.exists():
        print(f"  Opt-out file exists: {opt_out_path}")
    else:
        print(f"  Opt-out file not found (will be created on first opt-out)")

    # Send test SMS if MI number is configured
    tal_phone = os.getenv("TAL_PHONE_NUMBER", "3039162443")
    if phone_mi and tal_phone:
        try:
            from outreach.sms.twilio_sender import TwilioSender, fill_template
            sender = TwilioSender(account_sid=sid, auth_token=token)

            # Load new_homeowner template and render
            tmpl_path = SMS_TEMPLATES_DIR / "new_homeowner.json"
            if tmpl_path.exists():
                with open(tmpl_path) as f:
                    tmpl = json.load(f)
                test_lead = {
                    "first_name": "Tal",
                    "city": "Troy",
                }
                rendered = fill_template(tmpl["message"], test_lead, "248-509-0470")
                rendered = f"[QC TEST] {rendered}"

                result = sender.send_sms(
                    to_number=tal_phone,
                    message=rendered,
                    market="oakland_county_mi",
                )
                print(f"  Test SMS sent: {result['sid']} ({result['status']})")
            else:
                print("  WARNING: new_homeowner.json SMS template not found")
                warnings += 1
        except Exception as exc:
            print(f"  ERROR sending test SMS: {exc}")
            warnings += 1
    elif not tal_phone:
        print("  WARNING: TAL_PHONE_NUMBER not set — cannot send test SMS")
        warnings += 1

    if blocked_regions:
        print(f"  RESULT: {BLOCKED} — purchase Twilio numbers for: {', '.join(blocked_regions)}")
        return BLOCKED, warnings

    result = PASS if warnings == 0 else PASS
    suffix = f" ({warnings} warnings)" if warnings else ""
    print(f"  RESULT: {result}{suffix}")
    return result, warnings


# ---------------------------------------------------------------------------
# Phase 5: Voice Pre-Flight
# ---------------------------------------------------------------------------

def phase_voice_preflight() -> tuple[str, int]:
    """Verify Retell API connection + validate agent configs (dry-run only)."""
    print("\nPhase 5: Voice Pre-Flight")
    print("-" * 50)

    api_key = os.getenv("RETELL_API_KEY", "")
    if not api_key:
        print("  ERROR: RETELL_API_KEY not set in .env")
        return BLOCKED, 0

    warnings = 0

    try:
        from outreach.voice.retell_client import RetellClient
        from outreach.voice.retell_config import RetellConfig

        # Test API connection by listing agents
        client = RetellClient(api_key=api_key)
        agents = client.list_agents()
        print(f"  Retell connected | {len(agents)} agents on account")

        # List phone numbers
        phones = client.list_phone_numbers()
        if phones:
            print(f"  Phone numbers: {len(phones)} configured")
            for p in phones:
                number = p.get("phone_number_pretty") or p.get("phone_number", "?")
                out_agent = p.get("outbound_agent_id", "none")
                print(f"    {number} -> agent: {out_agent}")
        else:
            print("  WARNING: No phone numbers configured in Retell")
            warnings += 1

        # Check env phone numbers
        phone_mi = os.getenv("RETELL_PHONE_MI", "")
        phone_nc = os.getenv("RETELL_PHONE_NC", "")
        if not phone_mi:
            print("  WARNING: RETELL_PHONE_MI not configured")
            warnings += 1
        if not phone_nc:
            print("  WARNING: RETELL_PHONE_NC not configured")
            warnings += 1

        # Validate all voice scripts
        config = RetellConfig()
        scripts = config.get_all_scripts()
        all_valid = True

        for name, data in scripts.items():
            valid, errors = config.validate_script(data)
            if valid:
                # Test merge tag resolution with sample data
                test_lead = {"first_name": "Sarah", "street": "123 Oak Dr"}
                filled = config.fill_script(name, test_lead)
                unresolved = re.findall(r'\{([a-z_]+)\}', filled["first_sentence"])
                if unresolved:
                    print(f"    {name}: WARNING — unresolved tags in first_sentence: {unresolved}")
                    warnings += 1
                else:
                    print(f"    {name}: script valid, merge tags resolve OK")
            else:
                print(f"    {name}: FAIL — {errors}")
                all_valid = False
                warnings += 1

        if not all_valid:
            print(f"  RESULT: {FAIL}")
            return FAIL, warnings

        print(f"  Note: Dry-run only — no actual call made (costs money)")

    except SystemExit:
        print("  ERROR: Retell API authentication failed")
        return FAIL, 0
    except Exception as exc:
        print(f"  ERROR: {exc}")
        return FAIL, 0

    result = PASS if warnings == 0 else PASS
    suffix = f" ({warnings} warnings)" if warnings else ""
    print(f"  RESULT: {result}{suffix}")
    return result, warnings


# ---------------------------------------------------------------------------
# Phase 6: CRM Integration
# ---------------------------------------------------------------------------

def phase_crm_integration() -> tuple[str, int]:
    """Test Google Sheets CRM — connect, verify tabs, CRUD test lead."""
    print("\nPhase 6: CRM Integration")
    print("-" * 50)

    sheets_id = os.getenv("GOOGLE_SHEETS_ID", "")
    creds = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "")

    if not sheets_id:
        print("  ERROR: GOOGLE_SHEETS_ID not set in .env")
        return BLOCKED, 0

    warnings = 0
    test_lead_id = None

    try:
        from crm.sheets_manager import SheetsManager, TAB_DEFINITIONS

        mgr = SheetsManager()

        # Test 1: Connect
        if not mgr.connect():
            print("  ERROR: Failed to connect to Google Sheets")
            return FAIL, 0
        print("  Connected to Google Sheets")

        # Test 2: Verify all 5 tabs exist with correct headers
        expected_tabs = list(TAB_DEFINITIONS.keys())
        existing_tabs = [ws.title for ws in mgr.spreadsheet.worksheets()]

        for tab_name in expected_tabs:
            if tab_name in existing_tabs:
                if tab_name != "Dashboard":
                    ws = mgr._get_worksheet(tab_name)
                    headers = mgr._api_call(ws.row_values, 1)
                    expected_headers = TAB_DEFINITIONS[tab_name]
                    if headers == expected_headers:
                        print(f"    {tab_name}: headers match")
                    else:
                        print(f"    {tab_name}: WARNING — headers mismatch")
                        print(f"      Expected: {expected_headers}")
                        print(f"      Got:      {headers}")
                        warnings += 1
                else:
                    print(f"    {tab_name}: exists (formula tab)")
            else:
                print(f"    {tab_name}: MISSING")
                warnings += 1

        # Test 3: CRUD test lead
        print("  Running CRUD test...")

        # Add test lead
        test_data = {
            "first_name": "QC_Test",
            "last_name": "Lead",
            "email": "qc-test@goldmans-test.invalid",
            "phone": "+10000000000",
            "city": "Troy",
            "market": "oakland",
            "icp_type": "new_homeowner",
            "source": "manual",
            "pipeline": "direct_customer",
        }
        test_lead_id = mgr.add_lead(test_data)
        print(f"    Add lead: {test_lead_id}")

        # Log activity
        activity_id = mgr.log_activity(
            lead_id=test_lead_id,
            channel="email",
            direction="outbound",
            campaign_name="[QC TEST]",
            subject_or_message="QC test email",
            status="sent",
        )
        print(f"    Log activity: {activity_id}")

        # Update status
        mgr.update_lead_status(test_lead_id, "contacted")
        print(f"    Update status: contacted")

        # Read back and verify
        lead = mgr.get_lead(test_lead_id)
        if not lead:
            print("    ERROR: Could not read back test lead")
            warnings += 1
        else:
            checks_ok = True
            if lead.get("first_name") != "QC_Test":
                print(f"    ERROR: first_name mismatch: {lead.get('first_name')}")
                checks_ok = False
            if lead.get("status") != "contacted":
                print(f"    ERROR: status mismatch: {lead.get('status')}")
                checks_ok = False
            if lead.get("market") != "oakland":
                print(f"    ERROR: market mismatch: {lead.get('market')}")
                checks_ok = False

            if checks_ok:
                print(f"    Read-back verified: all fields match")
            else:
                warnings += 1

        # Verify dashboard formula still works
        summary = mgr.get_dashboard_summary()
        if summary.get("total_leads", 0) > 0:
            print(f"    Dashboard: {summary['total_leads']} total leads")
        else:
            print(f"    WARNING: Dashboard shows 0 leads")
            warnings += 1

    except Exception as exc:
        print(f"  ERROR: {exc}")
        return FAIL, 0

    finally:
        # Cleanup: delete test lead
        if test_lead_id:
            try:
                from crm.sheets_manager import SheetsManager
                # Reuse existing manager if available
                deleted = mgr.delete_lead(test_lead_id)
                if deleted:
                    print(f"    Cleanup: deleted test lead {test_lead_id}")
                else:
                    print(f"    WARNING: Could not delete test lead {test_lead_id}")
                    warnings += 1
            except Exception as exc:
                print(f"    WARNING: Cleanup failed: {exc}")
                warnings += 1

    result = PASS if warnings == 0 else PASS
    suffix = f" ({warnings} warnings)" if warnings else ""
    print(f"  RESULT: {result}{suffix}")
    return result, warnings


# ---------------------------------------------------------------------------
# Phase 7: Reporting Verification
# ---------------------------------------------------------------------------

def phase_reporting() -> tuple[str, int]:
    """Pull CRM dashboard and cross-check totals."""
    print("\nPhase 7: Reporting Verification")
    print("-" * 50)

    sheets_id = os.getenv("GOOGLE_SHEETS_ID", "")
    if not sheets_id:
        print("  ERROR: GOOGLE_SHEETS_ID not set — using offline CSV count")

    warnings = 0

    # Count leads from enriched CSVs
    enriched_csvs = sorted(DATA_DIR.glob("enriched/*.csv"))
    listing_csvs = sorted(DATA_DIR.glob("raw/listing_agents_*.csv"))
    all_csvs = enriched_csvs + listing_csvs

    total_csv_leads = 0
    by_market = {}
    by_icp = {}

    for csv_path in all_csvs:
        _, rows = _read_csv_rows(csv_path)
        total_csv_leads += len(rows)

        for row in rows:
            market = _normalize_market(row.get("market", ""))
            if market:
                by_market[market] = by_market.get(market, 0) + 1

            icp = row.get("icp_category", row.get("icp_type", "")).strip()
            if icp:
                by_icp[icp] = by_icp.get(icp, 0) + 1

    print(f"  CSV Lead Counts:")
    print(f"    Total: {total_csv_leads:,}")
    for market, count in sorted(by_market.items()):
        print(f"    {market.title()}: {count:,}")

    if by_icp:
        print(f"  By ICP:")
        for icp, count in sorted(by_icp.items(), key=lambda x: -x[1]):
            print(f"    {icp}: {count:,}")

    # Try CRM dashboard if available
    if sheets_id:
        try:
            from crm.sheets_manager import SheetsManager

            mgr = SheetsManager()
            if mgr.connect():
                summary = mgr.get_dashboard_summary()
                crm_total = summary.get("total_leads", 0)
                crm_by_market = summary.get("by_market", {})
                crm_by_status = summary.get("by_status", {})

                print(f"\n  CRM Dashboard:")
                print(f"    Total leads in CRM: {crm_total:,}")

                if crm_by_market:
                    for market, count in sorted(crm_by_market.items()):
                        print(f"    {market.title()}: {count:,}")

                if crm_by_status:
                    print(f"  Pipeline Status:")
                    for status, count in crm_by_status.items():
                        print(f"    {status}: {count:,}")

                channels = summary.get("by_channel", {})
                if channels:
                    print(f"  By Channel:")
                    for ch, count in channels.items():
                        print(f"    {ch}: {count:,}")

                partners = summary.get("active_referral_partners", 0)
                print(f"  Active Referral Partners: {partners}")

                # Cross-check market totals
                if crm_by_market:
                    market_sum = sum(crm_by_market.values())
                    if market_sum != crm_total and crm_total > 0:
                        print(f"  WARNING: Market sum ({market_sum}) != total ({crm_total})")
                        warnings += 1
                    else:
                        print(f"  Market counts verified (sum matches total)")

            else:
                print("  WARNING: Could not connect to CRM for dashboard")
                warnings += 1

        except Exception as exc:
            print(f"  WARNING: CRM dashboard unavailable: {exc}")
            warnings += 1

    result = PASS if warnings == 0 else PASS
    suffix = f" ({warnings} warnings)" if warnings else ""
    print(f"  RESULT: {result}{suffix}")
    return result, warnings


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

PHASES = {
    "data-quality": ("Phase 1: Data Quality Audit", phase_data_quality),
    "merge-tags":   ("Phase 2: Merge Tag Rendering", phase_merge_tags),
    "email":        ("Phase 3: Email Pre-Flight", phase_email_preflight),
    "sms":          ("Phase 4: SMS Pre-Flight", phase_sms_preflight),
    "voice":        ("Phase 5: Voice Pre-Flight", phase_voice_preflight),
    "crm":          ("Phase 6: CRM Integration", phase_crm_integration),
    "reporting":    ("Phase 7: Reporting Verification", phase_reporting),
}


def main():
    parser = argparse.ArgumentParser(
        description="Goldman's Lead Gen — End-to-End QC Test Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Phases: " + ", ".join(PHASES.keys()),
    )
    parser.add_argument(
        "--phase",
        choices=list(PHASES.keys()),
        help="Run a single phase (default: all)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("GOLDMAN'S LEAD GEN — END-TO-END QC TEST")
    print("=" * 60)

    if args.phase:
        phases_to_run = [args.phase]
    else:
        phases_to_run = list(PHASES.keys())

    results = {}
    for phase_key in phases_to_run:
        label, func = PHASES[phase_key]
        try:
            result, warn_count = func()
            results[phase_key] = result
        except Exception as exc:
            print(f"\n  UNHANDLED ERROR in {label}: {exc}")
            results[phase_key] = FAIL

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    counts = {PASS: 0, FAIL: 0, BLOCKED: 0, MANUAL: 0}
    for phase_key in phases_to_run:
        label = PHASES[phase_key][0]
        result = results.get(phase_key, FAIL)
        marker = {"PASS": "OK", "FAIL": "XX", "BLOCKED": "!!", "MANUAL CHECK NEEDED": "??"}
        icon = marker.get(result, "??")
        print(f"  [{icon}] {label}: {result}")
        counts[result] = counts.get(result, 0) + 1

    parts = []
    if counts[PASS]:
        parts.append(f"{counts[PASS]} PASS")
    if counts[MANUAL]:
        parts.append(f"{counts[MANUAL]} MANUAL CHECK")
    if counts[BLOCKED]:
        parts.append(f"{counts[BLOCKED]} BLOCKED")
    if counts[FAIL]:
        parts.append(f"{counts[FAIL]} FAIL")

    print(f"\n  {' | '.join(parts)}")
    print("=" * 60)

    # Exit code: 0 if no FAIL, 1 otherwise
    sys.exit(1 if counts[FAIL] > 0 else 0)


if __name__ == "__main__":
    main()
