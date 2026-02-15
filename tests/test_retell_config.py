"""Tests for Retell AI voice agent configuration manager."""

import json
import tempfile
from pathlib import Path

import pytest

from outreach.voice.retell_config import RetellConfig, ICP_TO_SCRIPT, REQUIRED_FIELDS


SCRIPT_NAMES = [
    "new_homeowner",
    "referral_partner",
    "storm_damage",
    "commercial",
    "aging_neighborhood",
]


# ------------------------------------------------------------------
# Loading tests
# ------------------------------------------------------------------

class TestLoadScript:
    """Test loading each of the 5 scripts."""

    @pytest.fixture
    def config(self):
        return RetellConfig()

    @pytest.mark.parametrize("name", SCRIPT_NAMES)
    def test_load_each_script(self, config, name):
        data = config.load_script(name)
        assert isinstance(data, dict)
        assert "agent_name" in data
        assert "Goldman's" in data["agent_name"]

    @pytest.mark.parametrize("name", SCRIPT_NAMES)
    def test_script_has_all_required_fields(self, config, name):
        data = config.load_script(name)
        for field in REQUIRED_FIELDS:
            assert field in data, f"Script {name} missing field: {field}"

    def test_load_nonexistent_script(self, config):
        with pytest.raises(FileNotFoundError):
            config.load_script("nonexistent_script")

    def test_get_all_scripts(self, config):
        scripts = config.get_all_scripts()
        assert len(scripts) == 5
        for name in SCRIPT_NAMES:
            assert name in scripts

    def test_load_caches_result(self, config):
        data1 = config.load_script("new_homeowner")
        data2 = config.load_script("new_homeowner")
        assert data1 is data2  # Same object reference = cached


# ------------------------------------------------------------------
# Fill tests
# ------------------------------------------------------------------

class TestFillScript:
    """Test fill_script with various lead data."""

    @pytest.fixture
    def config(self):
        return RetellConfig()

    def test_fill_new_homeowner(self, config):
        lead = {"first_name": "Sarah", "street": "123 Oak Dr"}
        filled = config.fill_script("new_homeowner", lead)
        assert "Sarah" in filled["first_sentence"]
        assert "123 Oak Dr" in filled["first_sentence"]
        assert "{first_name}" not in filled["first_sentence"]
        assert "{street}" not in filled["first_sentence"]

    def test_fill_referral_partner(self, config):
        lead = {
            "first_name": "Mike",
            "business_name": "RE/MAX Premier",
            "partner_type": "real estate agent",
        }
        filled = config.fill_script("referral_partner", lead)
        assert "Mike" in filled["first_sentence"]
        assert "RE/MAX Premier" in filled["first_sentence"]
        assert "real estate agent" in filled["first_sentence"]

    def test_fill_storm_damage(self, config):
        lead = {"first_name": "John"}
        filled = config.fill_script("storm_damage", lead)
        assert "John" in filled["first_sentence"]

    def test_fill_commercial_with_business_name(self, config):
        lead = {"business_name": "Metro Storage LLC"}
        filled = config.fill_script("commercial", lead)
        assert "Metro Storage LLC" in filled["first_sentence"]

    def test_fill_aging_neighborhood(self, config):
        lead = {"first_name": "Linda"}
        filled = config.fill_script("aging_neighborhood", lead)
        assert "Linda" in filled["first_sentence"]

    def test_fill_missing_first_name_uses_default(self, config):
        lead = {}
        filled = config.fill_script("new_homeowner", lead)
        assert "there" in filled["first_sentence"]
        assert "{first_name}" not in filled["first_sentence"]

    def test_fill_missing_street_uses_default(self, config):
        lead = {"first_name": "Sarah"}
        filled = config.fill_script("new_homeowner", lead)
        assert "your street" in filled["first_sentence"]

    def test_fill_company_name_fallback(self, config):
        """company_name should work as fallback for business_name."""
        lead = {"first_name": "Dave", "company_name": "Acme Plumbing"}
        filled = config.fill_script("referral_partner", lead)
        assert "Acme Plumbing" in filled["first_sentence"]

    def test_fill_does_not_modify_original(self, config):
        original = config.load_script("new_homeowner")
        original_sentence = original["first_sentence"]
        lead = {"first_name": "Sarah", "street": "123 Oak Dr"}
        config.fill_script("new_homeowner", lead)
        assert original["first_sentence"] == original_sentence


# ------------------------------------------------------------------
# ICP mapping tests
# ------------------------------------------------------------------

class TestICPMapping:
    """Test ICP-to-script mapping for all 10 ICPs."""

    @pytest.fixture
    def config(self):
        return RetellConfig()

    @pytest.mark.parametrize("icp,expected_script", [
        ("new_homeowners", "new_homeowner"),
        ("real_estate_agents", "referral_partner"),
        ("property_managers", "referral_partner"),
        ("home_inspectors", "referral_partner"),
        ("insurance_agents", "referral_partner"),
        ("builders_contractors", "referral_partner"),
        ("adjacent_trades", "referral_partner"),
        ("storm_damage", "storm_damage"),
        ("commercial_properties", "commercial"),
        ("aging_neighborhoods", "aging_neighborhood"),
    ])
    def test_icp_maps_to_correct_script(self, config, icp, expected_script):
        assert config.get_script_for_icp(icp) == expected_script

    def test_unknown_icp_raises_error(self, config):
        with pytest.raises(ValueError):
            config.get_script_for_icp("unknown_icp_type")

    def test_all_10_icps_have_mappings(self):
        assert len(ICP_TO_SCRIPT) == 10

    def test_all_mapped_scripts_exist(self, config):
        """Every script referenced in the ICP mapping must exist as a file."""
        unique_scripts = set(ICP_TO_SCRIPT.values())
        for script_name in unique_scripts:
            data = config.load_script(script_name)
            assert data is not None


# ------------------------------------------------------------------
# Validation tests
# ------------------------------------------------------------------

class TestValidation:
    """Test validation catches missing fields and all scripts pass."""

    @pytest.fixture
    def config(self):
        return RetellConfig()

    @pytest.mark.parametrize("name", SCRIPT_NAMES)
    def test_all_scripts_pass_validation(self, config, name):
        data = config.load_script(name)
        valid, errors = config.validate_script(data)
        assert valid, f"Script {name} failed validation: {errors}"

    def test_missing_agent_name(self, config):
        data = {"voice": "male", "first_sentence": "Hi",
                "system_prompt": "transfer_to(+12485090470) notify_missed_transfer 248-509-0470",
                "max_call_duration_ms": 180000,
                "post_call_analysis_schema": {
                    "interested": {"type": "boolean", "description": "x"},
                    "callback_requested": {"type": "boolean", "description": "x"},
                    "notes": {"type": "string", "description": "x"},
                    "objection": {"type": "string", "description": "x"},
                }}
        valid, errors = config.validate_script(data)
        assert not valid
        assert any("agent_name" in e for e in errors)

    def test_missing_system_prompt(self, config):
        data = {"agent_name": "Test", "voice": "male", "first_sentence": "Hi",
                "max_call_duration_ms": 180000,
                "post_call_analysis_schema": {
                    "interested": {"type": "boolean", "description": "x"},
                    "callback_requested": {"type": "boolean", "description": "x"},
                    "notes": {"type": "string", "description": "x"},
                    "objection": {"type": "string", "description": "x"},
                }}
        valid, errors = config.validate_script(data)
        assert not valid
        assert any("system_prompt" in e for e in errors)

    def test_invalid_voice(self, config):
        data = {"agent_name": "Test", "voice": "robot", "first_sentence": "Hi",
                "system_prompt": "transfer_to(+12485090470) notify_missed_transfer 248-509-0470",
                "max_call_duration_ms": 180000,
                "post_call_analysis_schema": {
                    "interested": {"type": "boolean", "description": "x"},
                    "callback_requested": {"type": "boolean", "description": "x"},
                    "notes": {"type": "string", "description": "x"},
                    "objection": {"type": "string", "description": "x"},
                }}
        valid, errors = config.validate_script(data)
        assert not valid
        assert any("voice" in e for e in errors)

    def test_missing_analysis_key(self, config):
        data = {"agent_name": "Test", "voice": "male", "first_sentence": "Hi",
                "system_prompt": "transfer_to(+12485090470) notify_missed_transfer 248-509-0470",
                "max_call_duration_ms": 180000,
                "post_call_analysis_schema": {
                    "interested": {"type": "boolean", "description": "x"},
                    # missing callback_requested, notes, objection
                }}
        valid, errors = config.validate_script(data)
        assert not valid
        assert any("callback_requested" in e for e in errors)

    def test_missing_transfer_protocol(self, config):
        data = {"agent_name": "Test", "voice": "male", "first_sentence": "Hi",
                "system_prompt": "Just a normal prompt without transfer instructions.",
                "max_call_duration_ms": 180000,
                "post_call_analysis_schema": {
                    "interested": {"type": "boolean", "description": "x"},
                    "callback_requested": {"type": "boolean", "description": "x"},
                    "notes": {"type": "string", "description": "x"},
                    "objection": {"type": "string", "description": "x"},
                }}
        valid, errors = config.validate_script(data)
        assert not valid
        assert any("transfer_to" in e for e in errors)

    def test_invalid_duration(self, config):
        data = {"agent_name": "Test", "voice": "male", "first_sentence": "Hi",
                "system_prompt": "transfer_to(+12485090470) notify_missed_transfer 248-509-0470",
                "max_call_duration_ms": -1,
                "post_call_analysis_schema": {
                    "interested": {"type": "boolean", "description": "x"},
                    "callback_requested": {"type": "boolean", "description": "x"},
                    "notes": {"type": "string", "description": "x"},
                    "objection": {"type": "string", "description": "x"},
                }}
        valid, errors = config.validate_script(data)
        assert not valid
        assert any("max_call_duration_ms" in e for e in errors)
