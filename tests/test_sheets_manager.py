"""
Tests for crm/sheets_manager.py

All tests use dry-run mode — no Google API credentials needed.
"""

import csv
import json
import os
import sys
from pathlib import Path

import pytest

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from crm.sheets_manager import (
    SheetsManager,
    TAB_DEFINITIONS,
    VALID_STATUSES,
    VALID_CHANNELS,
    VALID_MARKETS,
    _generate_id,
    _now_iso,
    _today_iso,
    DASHBOARD_LAYOUT,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def mgr():
    """Create a dry-run SheetsManager with initialized tabs."""
    m = SheetsManager(dry_run=True)
    m.connect()
    m.initialize_sheets()
    return m


@pytest.fixture
def sample_lead():
    return {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@example.com",
        "phone": "+12485551234",
        "market": "oakland",
        "icp_type": "new_homeowner",
        "pipeline": "direct_customer",
        "address": "123 Main St",
        "city": "Oakland",
        "zip": "48363",
    }


@pytest.fixture
def sample_lead_2():
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "phone": "+19195559876",
        "market": "triangle",
        "icp_type": "real_estate_agent",
        "pipeline": "referral_partner",
    }


@pytest.fixture
def sample_csv(tmp_path):
    """Create a sample CSV file for import testing."""
    csv_path = tmp_path / "test_leads.csv"
    rows = [
        {"first_name": "Alice", "last_name": "Wong", "email": "alice@test.com",
         "phone": "+12485550001", "address": "10 Oak Dr", "city": "Rochester", "zip": "48306"},
        {"first_name": "Bob", "last_name": "Chen", "email": "bob@test.com",
         "phone": "+12485550002", "address": "20 Elm St", "city": "Troy", "zip": "48083"},
        {"first_name": "Carol", "last_name": "Davis", "email": "carol@test.com",
         "phone": "+12485550003", "address": "30 Pine Ln", "city": "Auburn Hills", "zip": "48326"},
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return str(csv_path)


@pytest.fixture
def sample_csv_alt_columns(tmp_path):
    """CSV with alternative column naming conventions."""
    csv_path = tmp_path / "alt_leads.csv"
    rows = [
        {"firstname": "Dan", "lastname": "Miller", "email_address": "dan@test.com",
         "telephone": "+19195550004", "street_address": "40 Maple Ave"},
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return str(csv_path)


@pytest.fixture
def sample_csv_no_contact(tmp_path):
    """CSV with rows missing both email and phone."""
    csv_path = tmp_path / "bad_leads.csv"
    rows = [
        {"first_name": "NoContact", "last_name": "Person", "address": "50 Nowhere St"},
    ]
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return str(csv_path)


# ---------------------------------------------------------------------------
# Sheet Initialization Tests
# ---------------------------------------------------------------------------

class TestInitialization:

    def test_creates_all_tabs(self, mgr):
        tab_names = [ws.title for ws in mgr.spreadsheet.worksheets()]
        for tab in TAB_DEFINITIONS:
            assert tab in tab_names, f"Tab '{tab}' not created"

    def test_leads_tab_has_correct_headers(self, mgr):
        ws = mgr.spreadsheet.worksheet("Leads")
        headers = ws.row_values(1)
        assert headers == TAB_DEFINITIONS["Leads"]

    def test_outreach_log_tab_has_correct_headers(self, mgr):
        ws = mgr.spreadsheet.worksheet("Outreach Log")
        headers = ws.row_values(1)
        assert headers == TAB_DEFINITIONS["Outreach Log"]

    def test_referral_partners_tab_has_correct_headers(self, mgr):
        ws = mgr.spreadsheet.worksheet("Referral Partners")
        headers = ws.row_values(1)
        assert headers == TAB_DEFINITIONS["Referral Partners"]

    def test_campaigns_tab_has_correct_headers(self, mgr):
        ws = mgr.spreadsheet.worksheet("Campaigns")
        headers = ws.row_values(1)
        assert headers == TAB_DEFINITIONS["Campaigns"]

    def test_dashboard_has_title(self, mgr):
        ws = mgr.spreadsheet.worksheet("Dashboard")
        val = ws.row_values(1)
        assert "Goldman's Garage Door Repair" in val[0]

    def test_dashboard_has_formulas(self, mgr):
        ws = mgr.spreadsheet.worksheet("Dashboard")
        # Check a known formula cell (B6 = Total Leads formula)
        all_vals = ws.get_all_values()
        # Row 6, Col 2 should have COUNTA formula
        assert "COUNTA" in all_vals[5][1] or "=" in all_vals[5][1]

    def test_idempotent_init(self, mgr):
        """Running initialize_sheets twice should not duplicate tabs."""
        mgr.initialize_sheets()
        tab_names = [ws.title for ws in mgr.spreadsheet.worksheets()]
        # Count occurrences of each tab
        for tab in TAB_DEFINITIONS:
            assert tab_names.count(tab) == 1, f"Tab '{tab}' duplicated"


# ---------------------------------------------------------------------------
# Lead Management Tests
# ---------------------------------------------------------------------------

class TestLeadManagement:

    def test_add_lead_returns_id(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        assert lead_id is not None
        assert len(lead_id) == 8

    def test_add_lead_sets_defaults(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        lead = mgr.get_lead(lead_id)
        assert lead["status"] == "new"
        assert lead["created_date"] == _today_iso()
        assert lead["last_activity"] != ""

    def test_add_lead_stores_all_fields(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        lead = mgr.get_lead(lead_id)
        assert lead["first_name"] == "John"
        assert lead["last_name"] == "Smith"
        assert lead["email"] == "john@example.com"
        assert lead["phone"] == "+12485551234"
        assert lead["market"] == "oakland"
        assert lead["icp_type"] == "new_homeowner"

    def test_get_lead_not_found(self, mgr):
        lead = mgr.get_lead("nonexistent")
        assert lead == {}

    def test_dedup_by_email(self, mgr, sample_lead):
        """Adding a lead with same email should update, not duplicate."""
        lead_id_1 = mgr.add_lead(sample_lead)

        dup_lead = {
            "first_name": "Johnny",
            "email": "john@example.com",
            "phone": "+10000000000",  # Different phone
            "market": "wayne",
        }
        lead_id_2 = mgr.add_lead(dup_lead)

        assert lead_id_1 == lead_id_2
        # Verify updated fields
        lead = mgr.get_lead(lead_id_1)
        assert lead["first_name"] == "Johnny"
        assert lead["market"] == "wayne"

    def test_dedup_by_phone(self, mgr, sample_lead):
        """Adding a lead with same phone should update, not duplicate."""
        lead_id_1 = mgr.add_lead(sample_lead)

        dup_lead = {
            "first_name": "Jonathan",
            "email": "different@example.com",
            "phone": "+12485551234",  # Same phone
        }
        lead_id_2 = mgr.add_lead(dup_lead)

        assert lead_id_1 == lead_id_2

    def test_no_dedup_different_contact(self, mgr, sample_lead, sample_lead_2):
        """Different email and phone should create separate leads."""
        lead_id_1 = mgr.add_lead(sample_lead)
        lead_id_2 = mgr.add_lead(sample_lead_2)
        assert lead_id_1 != lead_id_2

    def test_update_lead(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        mgr.update_lead(lead_id, {"notes": "Hot lead!", "score": "5"})
        lead = mgr.get_lead(lead_id)
        assert lead["notes"] == "Hot lead!"
        assert lead["score"] == "5"

    def test_update_lead_not_found(self, mgr):
        result = mgr.update_lead("nonexistent", {"notes": "test"})
        assert result is False

    def test_update_lead_status(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        result = mgr.update_lead_status(lead_id, "contacted")
        assert result is True
        lead = mgr.get_lead(lead_id)
        assert lead["status"] == "contacted"

    def test_update_lead_status_invalid(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        result = mgr.update_lead_status(lead_id, "invalid_status")
        assert result is False

    def test_find_leads_by_market(self, mgr, sample_lead, sample_lead_2):
        mgr.add_lead(sample_lead)
        mgr.add_lead(sample_lead_2)

        oakland_leads = mgr.find_leads({"market": "oakland"})
        assert len(oakland_leads) == 1
        assert oakland_leads[0]["first_name"] == "John"

        triangle_leads = mgr.find_leads({"market": "triangle"})
        assert len(triangle_leads) == 1
        assert triangle_leads[0]["first_name"] == "Jane"

    def test_find_leads_by_status(self, mgr, sample_lead, sample_lead_2):
        id1 = mgr.add_lead(sample_lead)
        mgr.add_lead(sample_lead_2)
        mgr.update_lead_status(id1, "contacted")

        new_leads = mgr.find_leads({"status": "new"})
        assert len(new_leads) == 1

        contacted_leads = mgr.find_leads({"status": "contacted"})
        assert len(contacted_leads) == 1

    def test_find_leads_by_icp_type(self, mgr, sample_lead, sample_lead_2):
        mgr.add_lead(sample_lead)
        mgr.add_lead(sample_lead_2)

        homeowners = mgr.find_leads({"icp_type": "new_homeowner"})
        assert len(homeowners) == 1

    def test_find_leads_multiple_filters(self, mgr, sample_lead, sample_lead_2):
        mgr.add_lead(sample_lead)
        mgr.add_lead(sample_lead_2)

        results = mgr.find_leads({"market": "oakland", "status": "new"})
        assert len(results) == 1
        assert results[0]["first_name"] == "John"

    def test_find_leads_no_match(self, mgr, sample_lead):
        mgr.add_lead(sample_lead)
        results = mgr.find_leads({"market": "wayne"})
        assert len(results) == 0


# ---------------------------------------------------------------------------
# Outreach Logging Tests
# ---------------------------------------------------------------------------

class TestOutreachLogging:

    def test_log_activity_returns_id(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        activity_id = mgr.log_activity(
            lead_id=lead_id,
            channel="email",
            direction="outbound",
            campaign_name="oakland_homeowner_q1",
            subject_or_message="Garage door inspection offer",
            status="sent",
        )
        assert activity_id is not None
        assert len(activity_id) == 8

    def test_log_activity_correct_fields(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        mgr.log_activity(
            lead_id=lead_id,
            channel="sms",
            direction="outbound",
            campaign_name="sms_intro",
            subject_or_message="Hi John, free inspection for your new home!",
            status="delivered",
            notes="First touch",
        )

        history = mgr.get_lead_history(lead_id)
        assert len(history) == 1
        assert history[0]["channel"] == "sms"
        assert history[0]["direction"] == "outbound"
        assert history[0]["status"] == "delivered"
        assert history[0]["notes"] == "First touch"

    def test_log_activity_truncates_message(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        long_msg = "A" * 300
        mgr.log_activity(
            lead_id=lead_id,
            channel="email",
            direction="outbound",
            campaign_name="test",
            subject_or_message=long_msg,
            status="sent",
        )

        history = mgr.get_lead_history(lead_id)
        assert len(history[0]["subject_or_message"]) <= 200

    def test_get_lead_history_sorted(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)

        mgr.log_activity(lead_id, "email", "outbound", "camp1", "Email 1", "sent")
        mgr.log_activity(lead_id, "sms", "outbound", "camp1", "SMS 1", "delivered")
        mgr.log_activity(lead_id, "voice", "outbound", "camp1", "Call 1", "connected")

        history = mgr.get_lead_history(lead_id)
        assert len(history) == 3

        # Verify timestamps are in order
        timestamps = [h["timestamp"] for h in history]
        assert timestamps == sorted(timestamps)

    def test_get_lead_history_empty(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        history = mgr.get_lead_history(lead_id)
        assert history == []

    def test_log_activity_updates_last_activity(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        lead_before = mgr.get_lead(lead_id)

        mgr.log_activity(lead_id, "email", "outbound", "test", "Hello", "sent")

        lead_after = mgr.get_lead(lead_id)
        # last_activity should have been updated
        assert lead_after["last_activity"] != ""


# ---------------------------------------------------------------------------
# Referral Partner Tests
# ---------------------------------------------------------------------------

class TestReferralPartners:

    def test_add_partner(self, mgr, sample_lead_2):
        lead_id = mgr.add_lead(sample_lead_2)
        mgr.add_partner(lead_id, {
            "business_name": "Jane Doe Realty",
            "contact_name": "Jane Doe",
            "partner_type": "real_estate_agent",
            "market": "triangle",
            "phone": "+19195559876",
            "email": "jane@example.com",
            "status": "active",
        })

        partners = mgr.get_active_partners()
        assert len(partners) == 1
        assert partners[0]["business_name"] == "Jane Doe Realty"

    def test_get_active_partners_by_market(self, mgr, sample_lead, sample_lead_2):
        id1 = mgr.add_lead(sample_lead)
        id2 = mgr.add_lead(sample_lead_2)

        mgr.add_partner(id1, {
            "business_name": "Oakland Realty",
            "partner_type": "real_estate_agent",
            "market": "oakland",
            "status": "active",
        })
        mgr.add_partner(id2, {
            "business_name": "Triangle Props",
            "partner_type": "property_manager",
            "market": "triangle",
            "status": "active",
        })

        oakland = mgr.get_active_partners(market="oakland")
        assert len(oakland) == 1
        assert oakland[0]["business_name"] == "Oakland Realty"

        all_active = mgr.get_active_partners()
        assert len(all_active) == 2

    def test_get_active_partners_excludes_inactive(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        mgr.add_partner(lead_id, {
            "business_name": "Inactive Realty",
            "status": "inactive",
            "market": "oakland",
        })

        active = mgr.get_active_partners()
        assert len(active) == 0

    def test_log_referral_sent(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        mgr.add_partner(lead_id, {
            "business_name": "Test Realty",
            "status": "active",
            "market": "oakland",
        })

        mgr.log_referral(lead_id, "sent")

        ws = mgr.spreadsheet.worksheet("Referral Partners")
        records = ws.get_all_records()
        assert len(records) == 1
        assert int(records[0]["referrals_sent"]) == 1

    def test_log_referral_received(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        mgr.add_partner(lead_id, {
            "business_name": "Test Realty",
            "status": "active",
        })

        mgr.log_referral(lead_id, "received")
        mgr.log_referral(lead_id, "received")

        ws = mgr.spreadsheet.worksheet("Referral Partners")
        records = ws.get_all_records()
        assert int(records[0]["referrals_received"]) == 2

    def test_log_referral_partner_not_found(self, mgr):
        # Should not raise, just log warning
        mgr.log_referral("nonexistent", "sent")

    def test_add_partner_update_existing(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        mgr.add_partner(lead_id, {
            "business_name": "Old Name",
            "status": "prospecting",
        })
        # Update existing
        mgr.add_partner(lead_id, {
            "business_name": "New Name",
            "status": "active",
        })

        ws = mgr.spreadsheet.worksheet("Referral Partners")
        records = ws.get_all_records()
        # Should still be one record, not two
        assert len(records) == 1
        assert records[0]["business_name"] == "New Name"
        assert records[0]["status"] == "active"


# ---------------------------------------------------------------------------
# Campaign Tests
# ---------------------------------------------------------------------------

class TestCampaigns:

    def test_create_campaign_returns_id(self, mgr):
        campaign_id = mgr.create_campaign({
            "name": "Oakland Homeowners Q1",
            "channel": "email",
            "icp_type": "new_homeowner",
            "market": "oakland",
        })
        assert campaign_id is not None
        assert len(campaign_id) == 8

    def test_create_campaign_sets_defaults(self, mgr):
        campaign_id = mgr.create_campaign({
            "name": "Test Campaign",
            "channel": "sms",
        })
        campaign = mgr.get_campaign(campaign_id)
        assert campaign["status"] == "draft"
        assert campaign["start_date"] == _today_iso()
        assert campaign["sent"] == "0"

    def test_update_campaign_stats(self, mgr):
        campaign_id = mgr.create_campaign({
            "name": "Email Blast",
            "channel": "email",
        })

        mgr.update_campaign_stats(campaign_id, {
            "status": "active",
            "total_leads": "100",
            "sent": "95",
            "delivered": "90",
            "opened": "45",
            "replied": "10",
        })

        campaign = mgr.get_campaign(campaign_id)
        assert campaign["status"] == "active"
        assert campaign["sent"] == "95"
        assert campaign["opened"] == "45"
        assert campaign["replied"] == "10"

    def test_get_campaign_not_found(self, mgr):
        result = mgr.get_campaign("nonexistent")
        assert result == {}

    def test_update_campaign_stats_not_found(self, mgr):
        # Should not raise
        mgr.update_campaign_stats("nonexistent", {"sent": "10"})


# ---------------------------------------------------------------------------
# Bulk Operations Tests
# ---------------------------------------------------------------------------

class TestBulkOperations:

    def test_import_leads_from_csv(self, mgr, sample_csv):
        results = mgr.import_leads_from_csv(
            sample_csv, "homeowner_scraper", "new_homeowner", "oakland",
        )
        assert results["imported"] == 3
        assert results["duplicates"] == 0
        assert results["errors"] == 0

        # Verify leads exist
        all_leads = mgr.find_leads({"market": "oakland"})
        assert len(all_leads) == 3

    def test_import_csv_sets_source_and_icp(self, mgr, sample_csv):
        mgr.import_leads_from_csv(
            sample_csv, "clay", "real_estate_agent", "wayne",
        )
        leads = mgr.find_leads({"source": "clay"})
        assert len(leads) == 3
        for lead in leads:
            assert lead["icp_type"] == "real_estate_agent"
            assert lead["market"] == "wayne"

    def test_import_csv_dedup(self, mgr, sample_csv):
        """Importing the same CSV twice should show duplicates."""
        results1 = mgr.import_leads_from_csv(
            sample_csv, "homeowner_scraper", "new_homeowner", "oakland",
        )
        assert results1["imported"] == 3

        results2 = mgr.import_leads_from_csv(
            sample_csv, "homeowner_scraper", "new_homeowner", "oakland",
        )
        assert results2["duplicates"] == 3
        assert results2["imported"] == 0

    def test_import_csv_alt_columns(self, mgr, sample_csv_alt_columns):
        """CSV with alternative column names should still import."""
        results = mgr.import_leads_from_csv(
            sample_csv_alt_columns, "gmaps_scraper", "real_estate_agent", "triangle",
        )
        assert results["imported"] == 1
        assert results["errors"] == 0

        leads = mgr.find_leads({"market": "triangle"})
        assert len(leads) == 1
        assert leads[0]["first_name"] == "Dan"

    def test_import_csv_no_contact_info(self, mgr, sample_csv_no_contact):
        """Rows without email or phone should be skipped."""
        results = mgr.import_leads_from_csv(
            sample_csv_no_contact, "manual", "new_homeowner", "oakland",
        )
        assert results["imported"] == 0
        assert results["errors"] == 1

    def test_import_csv_file_not_found(self, mgr):
        results = mgr.import_leads_from_csv(
            "/nonexistent/path.csv", "manual", "new_homeowner", "oakland",
        )
        assert results["errors"] >= 1

    def test_export_leads_to_csv(self, mgr, sample_lead, sample_lead_2, tmp_path):
        mgr.add_lead(sample_lead)
        mgr.add_lead(sample_lead_2)

        output_path = str(tmp_path / "export.csv")
        result = mgr.export_leads_to_csv({}, output_path)
        assert result == output_path

        # Verify CSV content
        with open(output_path, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 2

        # Check headers match
        assert set(reader.fieldnames) == set(TAB_DEFINITIONS["Leads"])

    def test_export_leads_filtered(self, mgr, sample_lead, sample_lead_2, tmp_path):
        mgr.add_lead(sample_lead)
        mgr.add_lead(sample_lead_2)

        output_path = str(tmp_path / "export_filtered.csv")
        mgr.export_leads_to_csv({"market": "oakland"}, output_path)

        with open(output_path, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 1
        assert rows[0]["first_name"] == "John"

    def test_export_no_leads(self, mgr, tmp_path):
        output_path = str(tmp_path / "empty_export.csv")
        result = mgr.export_leads_to_csv({"market": "wayne"}, output_path)
        assert result == ""


# ---------------------------------------------------------------------------
# Dashboard Tests
# ---------------------------------------------------------------------------

class TestDashboard:

    def test_dashboard_summary_empty(self, mgr):
        summary = mgr.get_dashboard_summary()
        assert summary["total_leads"] == 0
        assert summary["active_referral_partners"] == 0

    def test_dashboard_summary_with_leads(self, mgr, sample_lead, sample_lead_2):
        id1 = mgr.add_lead(sample_lead)
        mgr.add_lead(sample_lead_2)
        mgr.update_lead_status(id1, "contacted")

        summary = mgr.get_dashboard_summary()
        assert summary["total_leads"] == 2
        assert summary["by_status"].get("contacted", 0) == 1
        assert summary["by_status"].get("new", 0) == 1
        assert summary["by_market"].get("oakland", 0) == 1
        assert summary["by_market"].get("triangle", 0) == 1

    def test_dashboard_summary_with_activities(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        mgr.log_activity(lead_id, "email", "outbound", "test", "Hello", "sent")
        mgr.log_activity(lead_id, "sms", "outbound", "test", "Hi", "delivered")
        mgr.log_activity(lead_id, "voice", "outbound", "test", "Call", "connected")

        summary = mgr.get_dashboard_summary()
        assert summary["by_channel"].get("email", 0) == 1
        assert summary["by_channel"].get("sms", 0) == 1
        assert summary["by_channel"].get("voice", 0) == 1

    def test_dashboard_summary_with_partners(self, mgr, sample_lead):
        lead_id = mgr.add_lead(sample_lead)
        mgr.add_partner(lead_id, {
            "business_name": "Active Partner",
            "status": "active",
        })

        summary = mgr.get_dashboard_summary()
        assert summary["active_referral_partners"] == 1


# ---------------------------------------------------------------------------
# Utility Tests
# ---------------------------------------------------------------------------

class TestUtilities:

    def test_generate_id_length(self):
        id_val = _generate_id()
        assert len(id_val) == 8
        assert id_val.isalnum()

    def test_generate_id_unique(self):
        ids = {_generate_id() for _ in range(100)}
        assert len(ids) == 100  # All unique

    def test_now_iso_format(self):
        ts = _now_iso()
        # Should be YYYY-MM-DD HH:MM:SS
        assert len(ts) == 19
        assert ts[4] == "-"
        assert ts[10] == " "

    def test_today_iso_format(self):
        d = _today_iso()
        assert len(d) == 10
        assert d[4] == "-"


# ---------------------------------------------------------------------------
# Dry-Run Mode Tests
# ---------------------------------------------------------------------------

class TestDryRunMode:

    def test_dry_run_flag(self):
        mgr = SheetsManager(dry_run=True)
        assert mgr.dry_run is True

    def test_dry_run_connect_succeeds(self):
        mgr = SheetsManager(dry_run=True)
        assert mgr.connect() is True

    def test_dry_run_full_workflow(self):
        """End-to-end test in dry-run mode."""
        mgr = SheetsManager(dry_run=True)
        mgr.connect()
        mgr.initialize_sheets()

        # Add leads
        id1 = mgr.add_lead({
            "first_name": "Test",
            "email": "test@dry.run",
            "market": "oakland",
            "icp_type": "new_homeowner",
        })

        # Log activity
        act_id = mgr.log_activity(
            id1, "email", "outbound", "dry_test", "Test email", "sent",
        )

        # Create campaign
        camp_id = mgr.create_campaign({"name": "Dry Campaign", "channel": "email"})

        # Dashboard
        summary = mgr.get_dashboard_summary()
        assert summary["total_leads"] == 1
        assert summary["by_channel"].get("email", 0) == 1

        # Update status
        mgr.update_lead_status(id1, "contacted")
        lead = mgr.get_lead(id1)
        assert lead["status"] == "contacted"


# ---------------------------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_add_lead_empty_optional_fields(self, mgr):
        """Lead with only required fields should work."""
        lead_id = mgr.add_lead({"email": "minimal@test.com"})
        lead = mgr.get_lead(lead_id)
        assert lead["email"] == "minimal@test.com"
        assert lead["first_name"] == ""
        assert lead["status"] == "new"

    def test_find_leads_empty_filters(self, mgr, sample_lead):
        """Empty filters should return all leads."""
        mgr.add_lead(sample_lead)
        all_leads = mgr.find_leads({})
        assert len(all_leads) == 1

    def test_case_insensitive_dedup(self, mgr):
        """Email dedup should be case-insensitive."""
        id1 = mgr.add_lead({"email": "John@Example.COM", "first_name": "John"})
        id2 = mgr.add_lead({"email": "john@example.com", "first_name": "Updated"})
        assert id1 == id2

    def test_case_insensitive_filter(self, mgr, sample_lead):
        """Filters should be case-insensitive."""
        mgr.add_lead(sample_lead)
        results = mgr.find_leads({"market": "OAKLAND"})
        assert len(results) == 1
