#!/usr/bin/env python3
"""One-time CRM setup: load all leads + apply professional formatting.

Usage:
    python crm/setup_crm.py
    python crm/setup_crm.py --format-only   # Skip data load, just format
"""

import argparse
import sys
import time
from pathlib import Path

import pandas as pd

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import google.auth
import google.auth.transport.requests
import gspread
from gspread.utils import rowcol_to_a1
from dotenv import load_dotenv
import os

load_dotenv()

SPREADSHEET_ID = os.getenv("GOOGLE_SHEETS_ID")
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Market display names
MARKET_LABELS = {
    "oakland_county_mi": "oakland",
    "wayne_county_mi": "wayne",
    "triangle_nc": "triangle",
}

# ICP type mapping from scraper categories to CRM icp_type
ICP_MAP = {
    "real_estate_agents": ("real_estate_agent", "referral_partner"),
    "property_managers": ("property_manager", "referral_partner"),
    "home_inspectors": ("home_inspector", "referral_partner"),
    "insurance_agents": ("insurance_agent", "referral_partner"),
    "home_builders": ("home_builder", "referral_partner"),
    "adjacent_trades": ("adjacent_trade", "referral_partner"),
    "commercial_properties": ("commercial", "direct_customer"),
}

# Brand colors
NAVY = {"red": 0.11, "green": 0.15, "blue": 0.27}       # #1C2745
GOLD = {"red": 0.85, "green": 0.65, "blue": 0.13}        # #D9A521
WHITE = {"red": 1, "green": 1, "blue": 1}
LIGHT_GRAY = {"red": 0.95, "green": 0.95, "blue": 0.95}  # #F2F2F2
LIGHT_GOLD = {"red": 0.98, "green": 0.94, "blue": 0.82}  # #FAF0D1
GREEN = {"red": 0.22, "green": 0.66, "blue": 0.36}       # #38A85C
RED = {"red": 0.84, "green": 0.18, "blue": 0.18}         # #D62D2D
BLUE = {"red": 0.16, "green": 0.47, "blue": 0.81}        # #2878CF
MEDIUM_GRAY = {"red": 0.80, "green": 0.80, "blue": 0.80}


def connect():
    """Connect to Google Sheets via ADC."""
    creds, _ = google.auth.default(scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ])
    creds.refresh(google.auth.transport.requests.Request())
    gc = gspread.authorize(creds)
    return gc.open_by_key(SPREADSHEET_ID)


def rate_limit():
    """Respect Sheets API rate limits."""
    time.sleep(1.2)


# ──────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────

def load_enriched_leads(sh):
    """Load all enriched referral partner / business leads into the Leads tab."""
    ws = sh.worksheet("Leads")
    rate_limit()

    enriched_files = [
        ("real_estate_agents", "enriched/real_estate_agents_20260214.csv"),
        ("property_managers", "enriched/property_managers_20260214.csv"),
        ("home_inspectors", "enriched/home_inspectors_20260214.csv"),
        ("insurance_agents", "enriched/insurance_agents_20260214.csv"),
        ("home_builders", "enriched/home_builders_20260214.csv"),
        ("adjacent_trades", "enriched/adjacent_trades_20260214.csv"),
        ("commercial_properties", "enriched/commercial_properties_20260214.csv"),
    ]

    all_rows = []
    lead_counter = 1

    for icp_cat, csv_rel in enriched_files:
        csv_path = DATA_DIR / csv_rel
        if not csv_path.exists():
            print(f"  Skipping {icp_cat} — file not found")
            continue

        df = pd.read_csv(csv_path)
        icp_type, pipeline = ICP_MAP.get(icp_cat, (icp_cat, "referral_partner"))
        market_key = ""

        for _, row in df.iterrows():
            raw_market = str(row.get("market", "")).strip()
            market = MARKET_LABELS.get(raw_market, raw_market)

            # Parse name fields
            first_name = str(row.get("dm_first_name", "")).strip()
            last_name = str(row.get("dm_last_name", "")).strip()
            if first_name.lower() in ("nan", ""): first_name = ""
            if last_name.lower() in ("nan", ""): last_name = ""

            email = str(row.get("dm_email", "")).strip()
            if email.lower() in ("nan", ""): email = ""
            phone = str(row.get("phone", "")).strip()
            if phone.lower() in ("nan", ""): phone = ""

            # Skip if no contact info
            if not email and not phone:
                continue

            company = str(row.get("name", "")).strip()
            if company.lower() in ("nan", ""): company = ""
            address = str(row.get("formatted_address", "")).strip()
            if address.lower() in ("nan", ""): address = ""
            city = str(row.get("city", "")).strip()
            if city.lower() in ("nan", ""): city = ""
            zipcode = str(row.get("zip", "")).strip()
            if zipcode.lower() in ("nan", ""): zipcode = ""

            rating = row.get("rating", "")
            reviews = row.get("user_ratings_total", "")
            score = ""
            try:
                r = float(rating)
                rv = int(reviews) if pd.notna(reviews) else 0
                if r >= 4.5 and rv >= 20: score = "5"
                elif r >= 4.0 and rv >= 10: score = "4"
                elif r >= 4.0: score = "3"
                elif r >= 3.5: score = "2"
                else: score = "1"
            except (ValueError, TypeError):
                pass

            lead_id = f"L{lead_counter:05d}"
            lead_counter += 1

            crm_row = [
                lead_id,            # lead_id
                "2026-02-14",       # created_date
                "gmaps_scraper",    # source
                icp_type,           # icp_type
                pipeline,           # pipeline
                market,             # market
                first_name,         # first_name
                last_name,          # last_name
                company,            # company
                email,              # email
                phone,              # phone
                address,            # address
                city,               # city
                zipcode,            # zip
                "new",              # status
                score,              # score
                "",                 # notes
                "2026-02-14",       # last_activity
            ]
            all_rows.append(crm_row)

        print(f"  {icp_cat}: {len(df)} records processed")

    # Load listing agents
    listing_agent_files = [
        ("oakland_county_mi", "raw/listing_agents_oakland_county_mi_20260214.csv"),
        ("wayne_county_mi", "raw/listing_agents_wayne_county_mi_20260214.csv"),
        ("triangle_nc", "raw/listing_agents_triangle_nc_20260214.csv"),
    ]

    for market_key, csv_rel in listing_agent_files:
        csv_path = DATA_DIR / csv_rel
        if not csv_path.exists():
            print(f"  Skipping listing agents {market_key} — file not found")
            continue

        df = pd.read_csv(csv_path)
        market = MARKET_LABELS.get(market_key, market_key)

        for _, row in df.iterrows():
            name = str(row.get("agent_name", "")).strip()
            email = str(row.get("agent_email", "")).strip()
            phone = str(row.get("agent_phone", "")).strip()

            if name.lower() in ("nan", ""): name = ""
            if email.lower() in ("nan", ""): email = ""
            if phone.lower() in ("nan", ""): phone = ""

            if not email and not phone:
                continue

            # Split name
            parts = name.split(None, 1)
            first_name = parts[0] if parts else ""
            last_name = parts[1] if len(parts) > 1 else ""

            broker = str(row.get("broker_name", "")).strip()
            if broker.lower() in ("nan", ""): broker = ""
            city = str(row.get("city", "")).strip()
            if city.lower() in ("nan", ""): city = ""
            state = str(row.get("state", "")).strip()
            if state.lower() in ("nan", ""): state = ""

            listings = row.get("active_listing_count", 0)
            try:
                listings = int(listings)
            except (ValueError, TypeError):
                listings = 0

            score = ""
            if listings >= 10: score = "5"
            elif listings >= 5: score = "4"
            elif listings >= 3: score = "3"
            else: score = "2"

            lead_id = f"L{lead_counter:05d}"
            lead_counter += 1

            crm_row = [
                lead_id,
                "2026-02-14",
                "active_listing_agent",
                "real_estate_agent",
                "referral_partner",
                market,
                first_name,
                last_name,
                broker,
                email,
                phone,
                "",
                city,
                "",
                "new",
                score,
                f"{listings} active listings",
                "2026-02-14",
            ]
            all_rows.append(crm_row)

        print(f"  listing_agents ({market_key}): {len(df)} records processed")

    if not all_rows:
        print("  No leads to load!")
        return 0

    # Deduplicate by email (keep first occurrence)
    seen_emails = set()
    unique_rows = []
    for row in all_rows:
        email = row[9].lower().strip()  # email is column index 9
        if email and email in seen_emails:
            continue
        if email:
            seen_emails.add(email)
        unique_rows.append(row)

    # Batch append (Sheets API allows up to ~40k cells per request)
    batch_size = 500
    total = len(unique_rows)
    for i in range(0, total, batch_size):
        batch = unique_rows[i:i + batch_size]
        ws.append_rows(batch, value_input_option="USER_ENTERED")
        print(f"  Loaded {min(i + batch_size, total)}/{total} leads...")
        rate_limit()

    print(f"\n  Total leads loaded: {total} (deduplicated from {len(all_rows)})")
    return total


# ──────────────────────────────────────────────
# PROFESSIONAL FORMATTING
# ──────────────────────────────────────────────

def format_sheet(sh):
    """Apply professional formatting to all tabs."""

    # ── Helper to build requests ──
    def header_format_req(sheet_id, num_cols):
        """Bold white text on navy background for header row."""
        return [
            # Header background
            {
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1,
                              "startColumnIndex": 0, "endColumnIndex": num_cols},
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": NAVY,
                            "textFormat": {"bold": True, "foregroundColor": WHITE, "fontSize": 10,
                                           "fontFamily": "Inter"},
                            "horizontalAlignment": "CENTER",
                            "verticalAlignment": "MIDDLE",
                            "padding": {"top": 4, "bottom": 4, "left": 6, "right": 6},
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment,padding)",
                }
            },
            # Freeze header row
            {
                "updateSheetProperties": {
                    "properties": {"sheetId": sheet_id, "gridProperties": {"frozenRowCount": 1}},
                    "fields": "gridProperties.frozenRowCount",
                }
            },
            # Set default font for data rows
            {
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": 5000,
                              "startColumnIndex": 0, "endColumnIndex": num_cols},
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {"fontSize": 10, "fontFamily": "Inter"},
                            "verticalAlignment": "MIDDLE",
                            "padding": {"top": 2, "bottom": 2, "left": 4, "right": 4},
                        }
                    },
                    "fields": "userEnteredFormat(textFormat,verticalAlignment,padding)",
                }
            },
            # Alternating row colors
            {
                "addBanding": {
                    "bandedRange": {
                        "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 5000,
                                  "startColumnIndex": 0, "endColumnIndex": num_cols},
                        "rowProperties": {
                            "headerColor": NAVY,
                            "firstBandColor": WHITE,
                            "secondBandColor": LIGHT_GRAY,
                        },
                    }
                }
            },
        ]

    def auto_resize_req(sheet_id, num_cols):
        """Auto-resize columns to fit content."""
        return {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": num_cols,
                }
            }
        }

    def set_col_width(sheet_id, col_idx, px):
        return {
            "updateDimensionProperties": {
                "range": {"sheetId": sheet_id, "dimension": "COLUMNS",
                          "startIndex": col_idx, "endIndex": col_idx + 1},
                "properties": {"pixelSize": px},
                "fields": "pixelSize",
            }
        }

    def set_row_height(sheet_id, row_idx, px):
        return {
            "updateDimensionProperties": {
                "range": {"sheetId": sheet_id, "dimension": "ROWS",
                          "startIndex": row_idx, "endIndex": row_idx + 1},
                "properties": {"pixelSize": px},
                "fields": "pixelSize",
            }
        }

    # Get sheet IDs
    sheets = {ws.title: ws for ws in sh.worksheets()}
    sheet_ids = {ws.title: ws.id for ws in sh.worksheets()}

    requests = []

    # ── TAB COLORS ──
    tab_colors = {
        "Leads": BLUE,
        "Outreach Log": GREEN,
        "Referral Partners": GOLD,
        "Campaigns": {"red": 0.56, "green": 0.27, "blue": 0.68},  # Purple
        "Dashboard": NAVY,
    }
    for tab_name, color in tab_colors.items():
        if tab_name in sheet_ids:
            requests.append({
                "updateSheetProperties": {
                    "properties": {"sheetId": sheet_ids[tab_name], "tabColor": color},
                    "fields": "tabColor",
                }
            })

    # ── LEADS TAB (18 columns) ──
    sid = sheet_ids.get("Leads")
    if sid is not None:
        requests.extend(header_format_req(sid, 18))
        requests.append(auto_resize_req(sid, 18))
        # Set specific column widths
        col_widths = {
            0: 80,    # lead_id
            1: 100,   # created_date
            2: 130,   # source
            3: 140,   # icp_type
            4: 120,   # pipeline
            5: 90,    # market
            6: 100,   # first_name
            7: 100,   # last_name
            8: 200,   # company
            9: 220,   # email
            10: 130,  # phone
            11: 250,  # address
            12: 120,  # city
            13: 70,   # zip
            14: 90,   # status
            15: 50,   # score
            16: 200,  # notes
            17: 130,  # last_activity
        }
        for col, px in col_widths.items():
            requests.append(set_col_width(sid, col, px))

        # Header row height
        requests.append(set_row_height(sid, 0, 36))

        # Conditional formatting: status colors
        status_colors = {
            "new": {"red": 0.88, "green": 0.93, "blue": 1.0},         # Light blue
            "contacted": {"red": 1.0, "green": 0.95, "blue": 0.80},   # Light orange
            "responded": {"red": 0.85, "green": 0.95, "blue": 0.85},  # Light green
            "qualified": {"red": 0.80, "green": 0.92, "blue": 0.80},  # Green
            "scheduled": {"red": 0.78, "green": 0.85, "blue": 0.97},  # Blue
            "closed_won": {"red": 0.22, "green": 0.66, "blue": 0.36}, # Dark green
            "closed_lost": {"red": 0.93, "green": 0.87, "blue": 0.87},# Light red
            "unsubscribed": {"red": 0.85, "green": 0.85, "blue": 0.85},
        }
        for status, bg_color in status_colors.items():
            text_color = WHITE if status == "closed_won" else {"red": 0.2, "green": 0.2, "blue": 0.2}
            requests.append({
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [{"sheetId": sid, "startRowIndex": 1, "endRowIndex": 5000,
                                    "startColumnIndex": 14, "endColumnIndex": 15}],
                        "booleanRule": {
                            "condition": {"type": "TEXT_EQ", "values": [{"userEnteredValue": status}]},
                            "format": {"backgroundColor": bg_color, "textFormat": {"foregroundColor": text_color, "bold": status in ("closed_won", "scheduled")}},
                        }
                    },
                    "index": 0,
                }
            })

        # Score column: gold stars effect
        for score_val in range(1, 6):
            intensity = 0.6 + (score_val * 0.08)
            requests.append({
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [{"sheetId": sid, "startRowIndex": 1, "endRowIndex": 5000,
                                    "startColumnIndex": 15, "endColumnIndex": 16}],
                        "booleanRule": {
                            "condition": {"type": "NUMBER_EQ", "values": [{"userEnteredValue": str(score_val)}]},
                            "format": {
                                "backgroundColor": {"red": intensity, "green": intensity * 0.78, "blue": 0.15},
                                "textFormat": {"foregroundColor": WHITE, "bold": True},
                            },
                        }
                    },
                    "index": 0,
                }
            })

    # ── OUTREACH LOG TAB (9 columns) ──
    sid = sheet_ids.get("Outreach Log")
    if sid is not None:
        requests.extend(header_format_req(sid, 9))
        requests.append(auto_resize_req(sid, 9))
        requests.append(set_row_height(sid, 0, 36))

    # ── REFERRAL PARTNERS TAB (12 columns) ──
    sid = sheet_ids.get("Referral Partners")
    if sid is not None:
        requests.extend(header_format_req(sid, 12))
        requests.append(auto_resize_req(sid, 12))
        requests.append(set_row_height(sid, 0, 36))

    # ── CAMPAIGNS TAB (17 columns) ──
    sid = sheet_ids.get("Campaigns")
    if sid is not None:
        requests.extend(header_format_req(sid, 17))
        requests.append(auto_resize_req(sid, 17))
        requests.append(set_row_height(sid, 0, 36))

    # ── DASHBOARD TAB ──
    sid = sheet_ids.get("Dashboard")
    if sid is not None:
        ws = sheets["Dashboard"]
        rate_limit()

        # Clear existing dashboard content
        ws.clear()
        rate_limit()

        # Write new dashboard layout
        dashboard_data = [
            # Row 1: Title
            ["GOLDMAN'S GARAGE DOOR REPAIR", "", "", ""],
            # Row 2: Subtitle
            ["Lead Generation Command Center", "", "", ""],
            # Row 3: blank
            ["", "", "", ""],
            # Row 4: Section - Pipeline
            ["PIPELINE OVERVIEW", "", "LEAD SOURCES", ""],
            # Row 5
            ["Total Leads", '=COUNTA(Leads!A2:A)', "Google Maps (Referral Partners)", '=COUNTIF(Leads!C2:C,"gmaps_scraper")'],
            # Row 6
            ["New", '=COUNTIF(Leads!O2:O,"new")', "Active Listing Agents", '=COUNTIF(Leads!C2:C,"active_listing_agent")'],
            # Row 7
            ["Contacted", '=COUNTIF(Leads!O2:O,"contacted")', "Storm Alerts", '=COUNTIF(Leads!C2:C,"storm_alert")'],
            # Row 8
            ["Responded", '=COUNTIF(Leads!O2:O,"responded")', "Manual / Other", '=COUNTIF(Leads!C2:C,"manual")'],
            # Row 9
            ["Qualified", '=COUNTIF(Leads!O2:O,"qualified")', "", ""],
            # Row 10
            ["Scheduled", '=COUNTIF(Leads!O2:O,"scheduled")', "", ""],
            # Row 11
            ["Closed Won", '=COUNTIF(Leads!O2:O,"closed_won")', "", ""],
            # Row 12: blank
            ["", "", "", ""],
            # Row 13: Section - Markets
            ["BY MARKET", "", "BY ICP TYPE", ""],
            # Row 14
            ["Oakland County, MI", '=COUNTIF(Leads!F2:F,"oakland")', "Real Estate Agents", '=COUNTIF(Leads!D2:D,"real_estate_agent")'],
            # Row 15
            ["Wayne County, MI", '=COUNTIF(Leads!F2:F,"wayne")', "Property Managers", '=COUNTIF(Leads!D2:D,"property_manager")'],
            # Row 16
            ["Triangle, NC", '=COUNTIF(Leads!F2:F,"triangle")', "Home Builders", '=COUNTIF(Leads!D2:D,"home_builder")'],
            # Row 17
            ["", "", "Home Inspectors", '=COUNTIF(Leads!D2:D,"home_inspector")'],
            # Row 18
            ["", "", "Insurance Agents", '=COUNTIF(Leads!D2:D,"insurance_agent")'],
            # Row 19
            ["", "", "Adjacent Trades", '=COUNTIF(Leads!D2:D,"adjacent_trade")'],
            # Row 20
            ["", "", "Commercial", '=COUNTIF(Leads!D2:D,"commercial")'],
            # Row 21: blank
            ["", "", "", ""],
            # Row 22: Outreach section
            ["OUTREACH ACTIVITY", "", "CONVERSION", ""],
            # Row 23
            ["Emails Sent", '=COUNTIF(\'Outreach Log\'!D2:D,"email")', "Response Rate", '=IFERROR(COUNTIF(Leads!O2:O,"responded")/COUNTIF(Leads!O2:O,"contacted"),"—")'],
            # Row 24
            ["SMS Sent", '=COUNTIF(\'Outreach Log\'!D2:D,"sms")', "Qualification Rate", '=IFERROR(COUNTIF(Leads!O2:O,"qualified")/COUNTIF(Leads!O2:O,"responded"),"—")'],
            # Row 25
            ["Calls Made", '=COUNTIF(\'Outreach Log\'!D2:D,"voice")', "Close Rate", '=IFERROR(COUNTIF(Leads!O2:O,"closed_won")/(COUNTIF(Leads!O2:O,"closed_won")+COUNTIF(Leads!O2:O,"closed_lost")),"—")'],
            # Row 26
            ["Total Touches", '=COUNTA(\'Outreach Log\'!A2:A)', "", ""],
            # Row 27: blank
            ["", "", "", ""],
            # Row 28
            ["Active Referral Partners", '=COUNTIF(\'Referral Partners\'!H2:H,"active")', "", ""],
            # Row 29
            ["Last Updated", '=NOW()', "", ""],
        ]

        ws.update(values=dashboard_data, range_name="A1:D29", value_input_option="USER_ENTERED")
        rate_limit()

        # Dashboard formatting requests
        requests.extend([
            # Title: large, bold, navy
            {
                "repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1,
                              "startColumnIndex": 0, "endColumnIndex": 4},
                    "cell": {"userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 18, "foregroundColor": NAVY, "fontFamily": "Inter"},
                    }},
                    "fields": "userEnteredFormat(textFormat)",
                }
            },
            # Subtitle
            {
                "repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": 2,
                              "startColumnIndex": 0, "endColumnIndex": 4},
                    "cell": {"userEnteredFormat": {
                        "textFormat": {"fontSize": 12, "foregroundColor": {"red": 0.5, "green": 0.5, "blue": 0.5}, "fontFamily": "Inter"},
                    }},
                    "fields": "userEnteredFormat(textFormat)",
                }
            },
            # Section headers (rows 4, 13, 22): bold, gold underline
            *[{
                "repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": r, "endRowIndex": r + 1,
                              "startColumnIndex": c, "endColumnIndex": c + 2},
                    "cell": {"userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 11, "foregroundColor": NAVY, "fontFamily": "Inter"},
                        "backgroundColor": LIGHT_GOLD,
                        "borders": {"bottom": {"style": "SOLID", "width": 2, "color": GOLD}},
                        "padding": {"top": 6, "bottom": 6, "left": 8, "right": 8},
                    }},
                    "fields": "userEnteredFormat(textFormat,backgroundColor,borders,padding)",
                }
            } for r, c in [(3, 0), (3, 2), (12, 0), (12, 2), (21, 0), (21, 2)]],
            # Metric labels: left-aligned, medium gray
            {
                "repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": 4, "endRowIndex": 29,
                              "startColumnIndex": 0, "endColumnIndex": 1},
                    "cell": {"userEnteredFormat": {
                        "textFormat": {"fontSize": 10, "fontFamily": "Inter"},
                        "padding": {"left": 12},
                    }},
                    "fields": "userEnteredFormat(textFormat,padding)",
                }
            },
            {
                "repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": 4, "endRowIndex": 29,
                              "startColumnIndex": 2, "endColumnIndex": 3},
                    "cell": {"userEnteredFormat": {
                        "textFormat": {"fontSize": 10, "fontFamily": "Inter"},
                        "padding": {"left": 12},
                    }},
                    "fields": "userEnteredFormat(textFormat,padding)",
                }
            },
            # Metric values: bold, right-aligned
            {
                "repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": 4, "endRowIndex": 29,
                              "startColumnIndex": 1, "endColumnIndex": 2},
                    "cell": {"userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 11, "foregroundColor": NAVY, "fontFamily": "Inter"},
                        "horizontalAlignment": "RIGHT",
                        "padding": {"right": 12},
                    }},
                    "fields": "userEnteredFormat(textFormat,horizontalAlignment,padding)",
                }
            },
            {
                "repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": 4, "endRowIndex": 29,
                              "startColumnIndex": 3, "endColumnIndex": 4},
                    "cell": {"userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 11, "foregroundColor": NAVY, "fontFamily": "Inter"},
                        "horizontalAlignment": "RIGHT",
                        "padding": {"right": 12},
                    }},
                    "fields": "userEnteredFormat(textFormat,horizontalAlignment,padding)",
                }
            },
            # Total Leads row: larger
            {
                "repeatCell": {
                    "range": {"sheetId": sid, "startRowIndex": 4, "endRowIndex": 5,
                              "startColumnIndex": 0, "endColumnIndex": 2},
                    "cell": {"userEnteredFormat": {
                        "textFormat": {"bold": True, "fontSize": 14, "foregroundColor": NAVY, "fontFamily": "Inter"},
                        "backgroundColor": {"red": 0.92, "green": 0.94, "blue": 0.98},
                        "padding": {"top": 6, "bottom": 6, "left": 12, "right": 12},
                    }},
                    "fields": "userEnteredFormat(textFormat,backgroundColor,padding)",
                }
            },
            # Column widths
            set_col_width(sid, 0, 220),
            set_col_width(sid, 1, 100),
            set_col_width(sid, 2, 220),
            set_col_width(sid, 3, 100),
            # Row heights
            set_row_height(sid, 0, 40),
            set_row_height(sid, 1, 28),
            # Freeze nothing on dashboard
            {
                "updateSheetProperties": {
                    "properties": {"sheetId": sid, "gridProperties": {"frozenRowCount": 0}},
                    "fields": "gridProperties.frozenRowCount",
                }
            },
            # Hide gridlines on dashboard
            {
                "updateSheetProperties": {
                    "properties": {"sheetId": sid, "gridProperties": {"hideGridlines": True}},
                    "fields": "gridProperties.hideGridlines",
                }
            },
        ])

    # ── EXECUTE ALL FORMATTING ──
    print(f"  Applying {len(requests)} formatting rules...")

    # Batch in chunks to avoid API limits
    batch_size = 50
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]
        sh.batch_update({"requests": batch})
        rate_limit()
        print(f"  Applied {min(i + batch_size, len(requests))}/{len(requests)} rules")

    print("  Formatting complete!")


def main():
    parser = argparse.ArgumentParser(description="Set up Goldman's CRM with data and formatting")
    parser.add_argument("--format-only", action="store_true", help="Skip data load, just format")
    args = parser.parse_args()

    print("Connecting to Google Sheets...")
    sh = connect()
    print(f"Connected: {sh.title}\n")

    if not args.format_only:
        print("Loading leads into CRM...")
        total = load_enriched_leads(sh)
        print(f"\nLead loading complete: {total} leads\n")

    print("Applying professional formatting...")
    format_sheet(sh)

    print(f"\nCRM is ready!")
    print(f"  https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")


if __name__ == "__main__":
    main()
