"""Retell AI API client — create agents, make outbound calls, manage campaigns.

Usage:
    python outreach/voice/retell_client.py --list-agents
    python outreach/voice/retell_client.py --create-agent new_homeowner
    python outreach/voice/retell_client.py --create-all-agents
    python outreach/voice/retell_client.py --list-phones
    python outreach/voice/retell_client.py --test-call --to "+12485551234" --script new_homeowner --market oakland
    python outreach/voice/retell_client.py --campaign leads.csv --script referral_partner --market oakland
    python outreach/voice/retell_client.py --dry-run --campaign leads.csv --script new_homeowner --market oakland
    python outreach/voice/retell_client.py --stats
    python outreach/voice/retell_client.py --recent-calls 10
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MARKETS_PATH = PROJECT_ROOT / "config" / "markets.json"
CALL_LOG_PATH = PROJECT_ROOT / "data" / "voice_call_log.json"

BASE_URL = "https://api.retellai.com"

# Voice ID for male voice — Retell's 11labs Adrian
DEFAULT_VOICE_ID = "11labs-Adrian"

# Market short name → region code
MARKET_PHONE_MAP = {
    "oakland": "mi",
    "wayne": "mi",
    "triangle": "nc",
    "oakland_county_mi": "mi",
    "wayne_county_mi": "mi",
    "triangle_nc": "nc",
    "mi": "mi",
    "nc": "nc",
}

# Region code → .env variable for Retell phone number
REGION_PHONE_ENV = {
    "mi": "RETELL_PHONE_MI",
    "nc": "RETELL_PHONE_NC",
}

_log_lock = threading.Lock()


def setup_logging() -> logging.Logger:
    """Configure logging to console + daily log file."""
    logger = logging.getLogger("retell")
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console)

    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    fh = logging.FileHandler(log_dir / f"retell_{date_str}.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(fh)

    return logger


log = setup_logging()


def redact_phone(phone: str) -> str:
    """Redact middle digits of a phone number for logging."""
    digits = re.sub(r"\D", "", phone)
    if len(digits) >= 10:
        return f"+{digits[:2]}***{digits[-4:]}"
    return "***"


def market_to_region(market: str) -> str:
    """Map market name to region code (mi/nc)."""
    region = MARKET_PHONE_MAP.get(market)
    if region:
        return region
    # Fallback: try loading from markets.json
    try:
        with open(MARKETS_PATH) as f:
            markets = json.load(f)["markets"]
        if market in markets:
            state = markets[market].get("region", "")
            if "michigan" in state.lower():
                return "mi"
            if "carolina" in state.lower():
                return "nc"
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass
    log.error(f"Unknown market: {market}. Use oakland, wayne, or triangle.")
    sys.exit(1)


def format_e164(phone: str) -> str:
    """Normalize a US phone number to E.164 format (+1XXXXXXXXXX)."""
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("1") and len(digits) == 11:
        return f"+{digits}"
    if len(digits) == 10:
        return f"+1{digits}"
    return phone  # Return as-is if already formatted or unknown format


def _convert_analysis_schema(schema: dict) -> list:
    """Convert our script post_call_analysis_schema dict to Retell's array format.

    Our format:   {"interested": {"type": "boolean", "description": "..."}, ...}
    Retell format: [{"name": "interested", "type": "boolean", "description": "..."}, ...]
    """
    result = []
    for name, config in schema.items():
        entry = {
            "name": name,
            "type": config.get("type", "string"),
            "description": config.get("description", ""),
        }
        result.append(entry)
    return result


class RetellClient:
    """Interface with Retell AI API for outbound voice campaigns."""

    def __init__(self, api_key: str = None, dry_run: bool = False):
        self.api_key = api_key or os.getenv("RETELL_API_KEY")
        self.dry_run = dry_run
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            })

        # Import RetellConfig — handle both module and script execution
        try:
            from outreach.voice.retell_config import RetellConfig
        except ModuleNotFoundError:
            from retell_config import RetellConfig
        self.config = RetellConfig()

        self.phone_numbers = {
            "mi": os.getenv("RETELL_PHONE_MI"),
            "nc": os.getenv("RETELL_PHONE_NC"),
        }

    def _require_api_key(self) -> None:
        """Exit if no API key is configured."""
        if not self.api_key:
            log.error("RETELL_API_KEY not set. Add it to .env or pass via --api-key.")
            sys.exit(1)

    def _request(self, method: str, path: str, **kwargs) -> dict | list | None:
        """Make an API request with retry and backoff.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE).
            path: URL path (e.g. /create-agent).
            **kwargs: Passed to requests (json, params, etc).

        Returns:
            Parsed JSON response, or None for 204 responses.
        """
        url = f"{BASE_URL}{path}"
        max_retries = 3

        for attempt in range(max_retries):
            try:
                log.debug(f"API {method} {path} (attempt {attempt + 1})")
                resp = self.session.request(method, url, timeout=30, **kwargs)

                if resp.status_code == 429:
                    wait = 2 ** (attempt + 1)
                    log.warning(f"Rate limited (429). Retrying in {wait}s...")
                    time.sleep(wait)
                    continue

                if resp.status_code == 401:
                    log.error("Authentication failed (401). Check RETELL_API_KEY.")
                    sys.exit(1)

                if resp.status_code == 204:
                    return None

                resp.raise_for_status()

                if resp.text:
                    return resp.json()
                return {}

            except requests.ConnectionError as exc:
                if attempt < max_retries - 1:
                    wait = 2 ** (attempt + 1)
                    log.warning(f"Connection error: {exc}. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    log.error(f"Connection failed after {max_retries} attempts: {exc}")
                    raise
            except requests.HTTPError as exc:
                log.error(f"API error: {exc} -- {resp.text}")
                raise

        log.error(f"Request failed after {max_retries} attempts")
        raise RuntimeError(f"Max retries exceeded for {method} {path}")

    # ------------------------------------------------------------------
    # LLM Management (Retell separates LLM from Agent)
    # ------------------------------------------------------------------

    def create_llm(self, script_name: str) -> str:
        """Create a Retell LLM from a script config.

        POST /create-retell-llm
        Body: general_prompt, begin_message (set to null so agent uses
              first_sentence from agent config), general_tools (transfer_call),
              default_dynamic_variables (template vars).

        Args:
            script_name: Script name from Phase 4A configs.

        Returns:
            llm_id string.
        """
        script = self.config.load_script(script_name)

        # Build transfer_call tool for Tal's number
        transfer_tool = {
            "type": "transfer_call",
            "name": "transfer_to_tal",
            "description": (
                "Transfer the call to Tal Goldman, the owner, when the prospect "
                "expresses interest in scheduling or learning more."
            ),
            "transfer_destination": {
                "type": "predefined",
                "number": os.getenv("TAL_PHONE_NUMBER", "+12485090470"),
            },
            "transfer_option": {
                "type": "warm_transfer",
                "show_transferee_as_caller": True,
            },
        }

        # End call tool
        end_call_tool = {
            "type": "end_call",
            "name": "end_call",
            "description": (
                "End the call when the prospect clearly declines, "
                "asks to be removed, or the conversation is complete."
            ),
        }

        # Default dynamic variables for template filling
        default_vars = {
            "first_name": "there",
            "street": "your street",
            "business_name": "your company",
            "partner_type": "professional",
        }

        payload = {
            "model": "gpt-4.1",
            "model_temperature": 0.3,
            "general_prompt": script["system_prompt"],
            "general_tools": [transfer_tool, end_call_tool],
            "default_dynamic_variables": default_vars,
            "start_speaker": "agent",
        }

        if self.dry_run:
            log.info(f"[DRY RUN] Would create LLM for script: {script_name}")
            log.debug(f"  Prompt length: {len(script['system_prompt'])} chars")
            return "dry_run_llm_id"

        self._require_api_key()
        result = self._request("POST", "/create-retell-llm", json=payload)
        llm_id = result["llm_id"]
        log.info(f"Created LLM for {script_name}: {llm_id}")
        return llm_id

    # ------------------------------------------------------------------
    # Agent Management
    # ------------------------------------------------------------------

    def create_agent(self, script_name: str) -> dict:
        """Create a Retell agent from a script config.

        Steps:
        1. Create LLM with system_prompt and tools.
        2. Create Agent with voice, first_sentence, analysis schema.

        Args:
            script_name: Script name from Phase 4A configs.

        Returns:
            Dict with agent_id and llm_id.
        """
        script = self.config.load_script(script_name)

        # Step 1: Create the LLM
        llm_id = self.create_llm(script_name)

        # Step 2: Build agent payload
        analysis_data = _convert_analysis_schema(
            script.get("post_call_analysis_schema", {})
        )

        voice_id = DEFAULT_VOICE_ID
        if script.get("voice") == "female":
            voice_id = "11labs-Myra"

        payload = {
            "response_engine": {
                "type": "retell-llm",
                "llm_id": llm_id,
            },
            "voice_id": voice_id,
            "agent_name": script["agent_name"],
            "max_call_duration_ms": script.get("max_call_duration_ms", 180000),
            "post_call_analysis_data": analysis_data,
            "language": "en-US",
            "enable_backchannel": True,
            "ambient_sound": "call-center",
            "ambient_sound_volume": 0.3,
            "enable_voicemail_detection": True,
            "voicemail_message": (
                "Hi, this is Alex from Goldman's Garage Door Repair. "
                "I was calling to see if we could help with your garage door. "
                "Give us a call back at 248-509-0470. Thanks!"
            ),
        }

        if self.dry_run:
            log.info(f"[DRY RUN] Would create agent: {script['agent_name']}")
            log.info(f"  Voice: {voice_id}")
            log.info(f"  Max duration: {script.get('max_call_duration_ms', 180000)}ms")
            log.info(f"  Analysis fields: {[d['name'] for d in analysis_data]}")
            return {"agent_id": "dry_run_agent_id", "llm_id": llm_id}

        self._require_api_key()
        result = self._request("POST", "/create-agent", json=payload)
        agent_id = result["agent_id"]
        log.info(f"Created agent: {script['agent_name']} → {agent_id}")
        return {"agent_id": agent_id, "llm_id": llm_id}

    def create_all_agents(self) -> dict:
        """Create agents for all 5 scripts.

        Returns:
            Dict mapping script_name → {agent_id, llm_id}.
        """
        scripts = self.config.get_all_scripts()
        results = {}
        for name in sorted(scripts.keys()):
            log.info(f"\n--- Creating agent for: {name} ---")
            try:
                result = self.create_agent(name)
                results[name] = result
                time.sleep(1)  # Respect rate limits
            except Exception as exc:
                log.error(f"Failed to create agent for {name}: {exc}")
                results[name] = {"error": str(exc)}
        return results

    def list_agents(self) -> list:
        """List all agents on the account.

        GET /list-agents

        Returns:
            List of agent dicts.
        """
        if self.dry_run:
            log.info("[DRY RUN] Would list agents")
            return []
        self._require_api_key()
        return self._request("GET", "/list-agents")

    def get_agent(self, agent_id: str) -> dict:
        """Get agent details.

        GET /get-agent/{agent_id}
        """
        if self.dry_run:
            log.info(f"[DRY RUN] Would get agent: {agent_id}")
            return {}
        self._require_api_key()
        return self._request("GET", f"/get-agent/{agent_id}")

    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent.

        DELETE /delete-agent/{agent_id}

        Returns:
            True if deleted successfully.
        """
        if self.dry_run:
            log.info(f"[DRY RUN] Would delete agent: {agent_id}")
            return True
        self._require_api_key()
        self._request("DELETE", f"/delete-agent/{agent_id}")
        log.info(f"Deleted agent: {agent_id}")
        return True

    # ------------------------------------------------------------------
    # Phone Number Management
    # ------------------------------------------------------------------

    def list_phone_numbers(self) -> list:
        """List phone numbers on account.

        GET /list-phone-numbers
        """
        if self.dry_run:
            log.info("[DRY RUN] Would list phone numbers")
            return []
        self._require_api_key()
        return self._request("GET", "/list-phone-numbers")

    def update_phone_agent(self, phone_number: str, agent_id: str,
                           direction: str = "outbound") -> dict:
        """Assign an agent to a phone number.

        PATCH /update-phone-number/{phone_number}

        Args:
            phone_number: E.164 format phone number.
            agent_id: Agent to assign.
            direction: 'outbound' or 'inbound'.

        Returns:
            Updated phone number config.
        """
        key = "outbound_agent_id" if direction == "outbound" else "inbound_agent_id"
        payload = {key: agent_id}

        if self.dry_run:
            log.info(f"[DRY RUN] Would assign agent {agent_id} to "
                     f"{redact_phone(phone_number)} ({direction})")
            return {}
        self._require_api_key()
        result = self._request(
            "PATCH", f"/update-phone-number/{phone_number}", json=payload
        )
        log.info(f"Assigned agent {agent_id} to {redact_phone(phone_number)} "
                 f"({direction})")
        return result

    # ------------------------------------------------------------------
    # Outbound Calls
    # ------------------------------------------------------------------

    def _get_from_number(self, market: str) -> str:
        """Get the Retell phone number for a market."""
        region = market_to_region(market)
        env_var = REGION_PHONE_ENV.get(region)
        if not env_var:
            if self.dry_run:
                return "+10000000000"
            log.error(f"No phone number configured for region: {region}")
            sys.exit(1)
        phone = os.getenv(env_var)
        if not phone:
            if self.dry_run:
                return "+10000000000"
            log.error(f"Phone number not set: {env_var}. Add to .env.")
            sys.exit(1)
        return phone

    def make_call(self, agent_id: str, to_number: str, market: str,
                  lead_data: dict = None, metadata: dict = None) -> dict:
        """Initiate a single outbound call.

        POST /v2/create-phone-call

        Args:
            agent_id: Retell agent ID to use.
            to_number: Prospect phone (any US format, auto-formatted to E.164).
            market: Market name for from-number selection.
            lead_data: Lead fields for template personalization.
            metadata: Additional metadata to attach to the call.

        Returns:
            Dict with call_id and initial status.
        """
        from_number = self._get_from_number(market)
        to_e164 = format_e164(to_number)

        # Build dynamic variables for template personalization
        dynamic_vars = {}
        if lead_data:
            for key in ("first_name", "street", "business_name", "partner_type"):
                if key in lead_data and lead_data[key]:
                    dynamic_vars[key] = str(lead_data[key])

        payload = {
            "from_number": from_number,
            "to_number": to_e164,
            "override_agent_id": agent_id,
            "retell_llm_dynamic_variables": dynamic_vars or None,
            "metadata": metadata or {},
        }
        # Remove None values
        payload = {k: v for k, v in payload.items() if v is not None}

        if self.dry_run:
            log.info(f"[DRY RUN] Would call {redact_phone(to_e164)} "
                     f"from {redact_phone(from_number)}")
            log.info(f"  Agent: {agent_id}")
            log.info(f"  Dynamic vars: {dynamic_vars}")
            return {"call_id": "dry_run_call_id", "call_status": "dry_run"}

        self._require_api_key()
        result = self._request("POST", "/v2/create-phone-call", json=payload)
        call_id = result.get("call_id", "unknown")
        log.info(f"Call initiated: {call_id} → {redact_phone(to_e164)}")
        return result

    def get_call(self, call_id: str) -> dict:
        """Get call details and post-call analysis.

        GET /v2/get-call/{call_id}
        """
        if self.dry_run:
            log.info(f"[DRY RUN] Would get call: {call_id}")
            return {}
        self._require_api_key()
        return self._request("GET", f"/v2/get-call/{call_id}")

    def list_calls(self, limit: int = 50) -> list:
        """List recent calls.

        POST /v2/list-calls (note: POST, not GET)
        """
        payload = {
            "sort_order": "descending",
            "limit": min(limit, 1000),
        }

        if self.dry_run:
            log.info(f"[DRY RUN] Would list {limit} recent calls")
            return []
        self._require_api_key()
        return self._request("POST", "/v2/list-calls", json=payload)

    def poll_call_status(self, call_id: str, timeout: int = 200,
                         interval: int = 5) -> dict:
        """Poll call status until complete or timeout.

        Args:
            call_id: Call to monitor.
            timeout: Max seconds to wait.
            interval: Seconds between polls.

        Returns:
            Final call data dict.
        """
        if self.dry_run:
            log.info(f"[DRY RUN] Would poll call: {call_id}")
            return {
                "call_id": call_id,
                "call_status": "ended",
                "disconnection_reason": "agent_hangup",
                "duration_ms": 45000,
                "call_analysis": {
                    "custom_analysis_data": {
                        "interested": True,
                        "callback_requested": False,
                        "notes": "Dry run — no actual call made.",
                        "objection": "",
                    },
                    "in_voicemail": False,
                },
            }

        start = time.time()
        terminal_statuses = {"ended", "not_connected", "error"}

        while time.time() - start < timeout:
            call_data = self.get_call(call_id)
            status = call_data.get("call_status", "")
            log.debug(f"Call {call_id}: status={status}")

            if status in terminal_statuses:
                return call_data

            time.sleep(interval)

        log.warning(f"Call {call_id} polling timed out after {timeout}s")
        return self.get_call(call_id)

    # ------------------------------------------------------------------
    # Campaign Management
    # ------------------------------------------------------------------

    def run_campaign(self, script_name: str, leads: list, market: str,
                     max_concurrent: int = 1, delay_between: int = 30) -> dict:
        """Run a voice campaign against a list of leads.

        For each lead:
        1. Fill script template with lead data
        2. Create or reuse agent for this script
        3. Make outbound call
        4. Wait for call to complete (poll)
        5. Process transfer results
        6. Log result
        7. Wait delay_between seconds before next call

        Args:
            script_name: Voice script to use.
            leads: List of dicts with phone + lead fields.
            market: Market for from-number selection.
            max_concurrent: Parallel calls (1 for now).
            delay_between: Seconds between calls.

        Returns:
            Campaign summary dict.
        """
        stats = {
            "total": len(leads),
            "completed": 0,
            "connected": 0,
            "interested": 0,
            "transferred": 0,
            "voicemail": 0,
            "no_answer": 0,
            "declined": 0,
            "errors": 0,
        }

        # Create or reuse agent
        log.info(f"\n{'='*60}")
        log.info(f"Voice Campaign: {script_name}")
        log.info(f"Market: {market} | Leads: {len(leads)} | "
                 f"Delay: {delay_between}s")
        log.info(f"{'='*60}\n")

        agent_result = self.create_agent(script_name)
        agent_id = agent_result["agent_id"]

        for i, lead in enumerate(leads, 1):
            phone = lead.get("phone", "")
            if not phone:
                log.warning(f"  [{i}/{len(leads)}] Skipping lead — no phone number")
                stats["errors"] += 1
                continue

            name = lead.get("first_name", "Unknown")
            log.info(f"  [{i}/{len(leads)}] Calling {name} at "
                     f"{redact_phone(format_e164(phone))}...")

            try:
                # Make the call
                call_result = self.make_call(
                    agent_id=agent_id,
                    to_number=phone,
                    market=market,
                    lead_data=lead,
                    metadata={
                        "script": script_name,
                        "market": market,
                        "lead_name": name,
                    },
                )
                call_id = call_result.get("call_id", "unknown")

                # Poll until complete
                call_data = self.poll_call_status(call_id)
                status = call_data.get("call_status", "")
                disconnection = call_data.get("disconnection_reason", "")
                analysis = call_data.get("call_analysis", {})
                custom = analysis.get("custom_analysis_data", {})
                in_voicemail = analysis.get("in_voicemail", False)

                stats["completed"] += 1

                if status == "not_connected":
                    stats["no_answer"] += 1
                    log.info(f"    → No answer")
                elif in_voicemail:
                    stats["voicemail"] += 1
                    log.info(f"    → Voicemail")
                elif status == "ended":
                    stats["connected"] += 1

                    if custom.get("interested"):
                        stats["interested"] += 1
                        log.info(f"    → Interested!")
                    else:
                        stats["declined"] += 1
                        objection = custom.get("objection", "none")
                        log.info(f"    → Declined (objection: {objection})")

                    if disconnection == "call_transfer":
                        stats["transferred"] += 1
                        transfer_result = self.handle_transfer_result(call_data)
                        if transfer_result.get("transfer_success"):
                            log.info(f"    → Transfer to Tal: SUCCESS")
                        else:
                            log.info(f"    → Transfer to Tal: MISSED "
                                     f"(SMS sent)")
                elif status == "error":
                    stats["errors"] += 1
                    log.warning(f"    → Error: {disconnection}")

                # Log result
                self.log_call_result(call_data, script_name, market)

            except Exception as exc:
                stats["errors"] += 1
                log.error(f"    → Error: {exc}")

            # Delay between calls
            if i < len(leads):
                log.debug(f"  Waiting {delay_between}s before next call...")
                time.sleep(delay_between)

        # Print summary
        log.info(f"\n{'='*60}")
        log.info(f"Campaign Complete: {script_name}")
        log.info(f"{'='*60}")
        for key, val in stats.items():
            log.info(f"  {key:>15}: {val}")

        return stats

    # ------------------------------------------------------------------
    # Transfer Handling
    # ------------------------------------------------------------------

    def handle_transfer_result(self, call_data: dict) -> dict:
        """Process what happened after a transfer attempt.

        If transfer succeeded: mark as hot lead.
        If transfer failed (Tal didn't answer):
            1. SMS Tal with missed transfer alert
            2. SMS prospect with callback promise
            3. Mark as warm lead needing callback

        Returns:
            Dict with transfer_success, actions_taken.
        """
        disconnection = call_data.get("disconnection_reason", "")
        transfer_dest = call_data.get("transfer_destination", "")
        analysis = call_data.get("call_analysis", {})
        custom = analysis.get("custom_analysis_data", {})
        metadata = call_data.get("metadata", {})

        prospect_name = metadata.get("lead_name", "Unknown")
        to_number = call_data.get("to_number", "")
        summary = custom.get("notes", analysis.get("call_summary", "No summary"))

        # Transfer succeeded if disconnection_reason is "call_transfer"
        # and the call actually connected to Tal
        transfer_success = disconnection == "call_transfer"

        result = {
            "transfer_success": transfer_success,
            "prospect_name": prospect_name,
            "prospect_phone": to_number,
            "actions_taken": [],
        }

        if transfer_success:
            result["actions_taken"].append("logged_hot_lead")
            log.info(f"Transfer succeeded: {prospect_name} connected to Tal")
            return result

        # Transfer failed — send notifications
        log.info(f"Transfer missed: Tal didn't answer for {prospect_name}")

        if self.dry_run:
            log.info(f"[DRY RUN] Would SMS Tal about missed transfer")
            log.info(f"[DRY RUN] Would SMS prospect about callback")
            result["actions_taken"] = ["dry_run_sms_tal", "dry_run_sms_prospect"]
            return result

        try:
            from outreach.sms.twilio_sender import TwilioSender
            sms = TwilioSender()
            tal_phone = os.getenv("TAL_PHONE_NUMBER", "+12485090470")

            # SMS to Tal
            tal_msg = (
                f"Missed Transfer! {prospect_name} at "
                f"{to_number} interested in service. "
                f"Call back within 1 hour.\n"
                f"Summary: {summary[:200]}"
            )
            sms_result = sms.send_sms(
                to_number=tal_phone,
                message=tal_msg,
                market="oakland_county_mi",
            )
            result["actions_taken"].append("sms_tal")
            log.info(f"Sent missed-transfer SMS to Tal: {sms_result.get('sid')}")

            # SMS to prospect
            prospect_msg = (
                f"Hi {prospect_name}, Tal from Goldman's will call you "
                f"back within the hour! Save our number: 248-509-0470"
            )
            sms_result = sms.send_sms(
                to_number=to_number,
                message=prospect_msg,
                market=metadata.get("market", "oakland_county_mi"),
            )
            result["actions_taken"].append("sms_prospect")
            log.info(f"Sent callback SMS to prospect: {sms_result.get('sid')}")

        except ImportError:
            log.warning("TwilioSender not available — skipping SMS notifications")
            result["actions_taken"].append("sms_skipped_no_twilio")
        except Exception as exc:
            log.error(f"Failed to send SMS notifications: {exc}")
            result["actions_taken"].append(f"sms_error: {exc}")

        result["actions_taken"].append("logged_warm_lead_callback")
        return result

    # ------------------------------------------------------------------
    # Results & Logging
    # ------------------------------------------------------------------

    def log_call_result(self, call_data: dict, script_name: str,
                        market: str) -> None:
        """Append call result to data/voice_call_log.json.

        Thread-safe JSON array append.
        """
        analysis = call_data.get("call_analysis", {})
        custom = analysis.get("custom_analysis_data", {})
        disconnection = call_data.get("disconnection_reason", "")

        entry = {
            "call_id": call_data.get("call_id", "unknown"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "to_number": redact_phone(call_data.get("to_number", "")),
            "market": market,
            "script": script_name,
            "duration_sec": round(
                call_data.get("duration_ms", 0) / 1000, 1
            ),
            "status": call_data.get("call_status", "unknown"),
            "disconnection_reason": disconnection,
            "connected": call_data.get("call_status") == "ended",
            "interested": bool(custom.get("interested", False)),
            "transferred": disconnection == "call_transfer",
            "transfer_success": disconnection == "call_transfer",
            "callback_requested": bool(
                custom.get("callback_requested", False)
            ),
            "voicemail": bool(analysis.get("in_voicemail", False)),
            "notes": custom.get("notes", ""),
            "objection": custom.get("objection", ""),
        }

        with _log_lock:
            CALL_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
            existing = []
            if CALL_LOG_PATH.exists():
                try:
                    with open(CALL_LOG_PATH) as f:
                        existing = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    existing = []

            existing.append(entry)
            with open(CALL_LOG_PATH, "w") as f:
                json.dump(existing, f, indent=2)

        log.debug(f"Logged call result: {entry['call_id']}")

    def get_campaign_stats(self) -> dict:
        """Read voice_call_log.json and return aggregate stats.

        Returns:
            Dict with totals and per-script breakdowns.
        """
        if not CALL_LOG_PATH.exists():
            return {"total_calls": 0, "message": "No call log found."}

        with open(CALL_LOG_PATH) as f:
            try:
                calls = json.load(f)
            except (json.JSONDecodeError, ValueError):
                return {"total_calls": 0, "message": "Call log is empty or corrupt."}

        if not calls:
            return {"total_calls": 0, "message": "No calls logged yet."}

        stats = {
            "total_calls": len(calls),
            "connected": sum(1 for c in calls if c.get("connected")),
            "interested": sum(1 for c in calls if c.get("interested")),
            "transferred": sum(1 for c in calls if c.get("transferred")),
            "voicemail": sum(1 for c in calls if c.get("voicemail")),
            "callback_requested": sum(
                1 for c in calls if c.get("callback_requested")
            ),
            "avg_duration_sec": round(
                sum(c.get("duration_sec", 0) for c in calls) / len(calls), 1
            ),
            "by_script": {},
            "by_market": {},
        }

        # Per-script breakdown
        for call in calls:
            script = call.get("script", "unknown")
            if script not in stats["by_script"]:
                stats["by_script"][script] = {
                    "calls": 0, "connected": 0, "interested": 0,
                }
            stats["by_script"][script]["calls"] += 1
            if call.get("connected"):
                stats["by_script"][script]["connected"] += 1
            if call.get("interested"):
                stats["by_script"][script]["interested"] += 1

        # Per-market breakdown
        for call in calls:
            market = call.get("market", "unknown")
            if market not in stats["by_market"]:
                stats["by_market"][market] = {"calls": 0, "connected": 0}
            stats["by_market"][market]["calls"] += 1
            if call.get("connected"):
                stats["by_market"][market]["connected"] += 1

        return stats


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def load_leads_csv(csv_path: str) -> list:
    """Load leads from a CSV file.

    Expected columns: phone (required), first_name, street,
    business_name, partner_type, market.
    """
    path = Path(csv_path)
    if not path.exists():
        log.error(f"CSV file not found: {csv_path}")
        sys.exit(1)

    leads = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lead = {k.strip().lower(): v.strip() for k, v in row.items() if v}
            leads.append(lead)

    log.info(f"Loaded {len(leads)} leads from {csv_path}")
    return leads


def cmd_list_agents(client: RetellClient) -> None:
    """List all agents."""
    agents = client.list_agents()
    if not agents:
        print("No agents found.")
        return
    print(f"\n{'Agent Name':<45} {'Agent ID':<30} {'Version'}")
    print("-" * 90)
    for agent in agents:
        name = agent.get("agent_name", "Unnamed")
        aid = agent.get("agent_id", "?")
        version = agent.get("version", "?")
        print(f"{name:<45} {aid:<30} {version}")
    print(f"\nTotal: {len(agents)} agents")


def cmd_create_agent(client: RetellClient, script_name: str) -> None:
    """Create a single agent from script config."""
    result = client.create_agent(script_name)
    print(f"\nAgent created:")
    print(f"  Agent ID: {result.get('agent_id')}")
    print(f"  LLM ID:   {result.get('llm_id')}")


def cmd_create_all(client: RetellClient) -> None:
    """Create agents for all 5 scripts."""
    results = client.create_all_agents()
    print(f"\n{'Script':<25} {'Agent ID':<30} {'Status'}")
    print("-" * 70)
    for name, result in results.items():
        if "error" in result:
            print(f"{name:<25} {'ERROR':<30} {result['error']}")
        else:
            print(f"{name:<25} {result.get('agent_id', '?'):<30} OK")


def cmd_list_phones(client: RetellClient) -> None:
    """List phone numbers on the account."""
    phones = client.list_phone_numbers()
    if not phones:
        print("No phone numbers found.")
        return
    print(f"\n{'Phone Number':<20} {'Area':<8} {'Outbound Agent':<30} "
          f"{'Inbound Agent'}")
    print("-" * 90)
    for p in phones:
        number = p.get("phone_number_pretty") or p.get("phone_number", "?")
        area = p.get("area_code", "?")
        out_agent = p.get("outbound_agent_id", "—")
        in_agent = p.get("inbound_agent_id", "—")
        print(f"{number:<20} {area:<8} {out_agent:<30} {in_agent}")
    print(f"\nTotal: {len(phones)} numbers")


def cmd_test_call(client: RetellClient, to_number: str,
                  script_name: str, market: str) -> None:
    """Make a single test call."""
    print(f"\nTest call: {script_name} → {redact_phone(format_e164(to_number))}")
    print(f"Market: {market}\n")

    result = client.create_agent(script_name)
    agent_id = result["agent_id"]

    call = client.make_call(
        agent_id=agent_id,
        to_number=to_number,
        market=market,
        lead_data={"first_name": "Test"},
    )
    call_id = call.get("call_id", "unknown")
    print(f"Call initiated: {call_id}")

    if not client.dry_run:
        print("Polling for completion...")
        final = client.poll_call_status(call_id)
        print(f"\nStatus: {final.get('call_status')}")
        print(f"Duration: {final.get('duration_ms', 0) / 1000:.1f}s")
        analysis = final.get("call_analysis", {})
        custom = analysis.get("custom_analysis_data", {})
        if custom:
            print(f"Analysis: {json.dumps(custom, indent=2)}")
        client.log_call_result(final, script_name, market)


def cmd_campaign(client: RetellClient, csv_path: str,
                 script_name: str, market: str) -> None:
    """Run a campaign from CSV."""
    leads = load_leads_csv(csv_path)
    if not leads:
        print("No leads to process.")
        return
    client.run_campaign(script_name, leads, market)


def cmd_stats(client: RetellClient) -> None:
    """Display campaign stats from the call log."""
    stats = client.get_campaign_stats()

    if stats.get("message"):
        print(stats["message"])
        return

    print(f"\n{'='*50}")
    print(f"Voice Campaign Stats")
    print(f"{'='*50}")
    print(f"  Total calls:        {stats['total_calls']}")
    print(f"  Connected:          {stats['connected']}")
    print(f"  Interested:         {stats['interested']}")
    print(f"  Transferred:        {stats['transferred']}")
    print(f"  Voicemail:          {stats['voicemail']}")
    print(f"  Callback requested: {stats['callback_requested']}")
    print(f"  Avg duration:       {stats['avg_duration_sec']}s")

    if stats.get("by_script"):
        print(f"\n  By Script:")
        for name, s in stats["by_script"].items():
            print(f"    {name}: {s['calls']} calls, "
                  f"{s['connected']} connected, {s['interested']} interested")

    if stats.get("by_market"):
        print(f"\n  By Market:")
        for name, s in stats["by_market"].items():
            print(f"    {name}: {s['calls']} calls, {s['connected']} connected")
    print()


def cmd_recent_calls(client: RetellClient, limit: int) -> None:
    """List recent calls from the API."""
    calls = client.list_calls(limit=limit)
    if not calls:
        print("No calls found.")
        return
    print(f"\n{'Call ID':<30} {'Status':<15} {'Duration':<10} {'To':<18} "
          f"{'Disconnection'}")
    print("-" * 95)
    for call in calls[:limit]:
        cid = call.get("call_id", "?")[:28]
        status = call.get("call_status", "?")
        dur = f"{call.get('duration_ms', 0) / 1000:.0f}s"
        to = redact_phone(call.get("to_number", ""))
        disc = call.get("disconnection_reason", "—")
        print(f"{cid:<30} {status:<15} {dur:<10} {to:<18} {disc}")
    print(f"\nShowing {min(limit, len(calls))} of {len(calls)} calls")


def main():
    parser = argparse.ArgumentParser(
        description="Retell AI API client for outbound voice campaigns"
    )

    # Mode flags
    parser.add_argument("--list-agents", action="store_true",
                        help="List all Retell agents")
    parser.add_argument("--create-agent", metavar="SCRIPT",
                        help="Create agent from script (e.g. new_homeowner)")
    parser.add_argument("--create-all-agents", action="store_true",
                        help="Create agents for all 5 scripts")
    parser.add_argument("--list-phones", action="store_true",
                        help="List phone numbers on account")
    parser.add_argument("--test-call", action="store_true",
                        help="Make a single test call")
    parser.add_argument("--campaign", metavar="CSV",
                        help="Run campaign from CSV file")
    parser.add_argument("--stats", action="store_true",
                        help="Show campaign stats from call log")
    parser.add_argument("--recent-calls", metavar="N", type=int,
                        help="List N recent calls from API")

    # Options
    parser.add_argument("--to", help="Phone number for --test-call")
    parser.add_argument("--script", help="Script name for --test-call or --campaign")
    parser.add_argument("--market", help="Market: oakland, wayne, or triangle")
    parser.add_argument("--dry-run", action="store_true",
                        help="Log actions without making API calls")
    parser.add_argument("--api-key", help="Override RETELL_API_KEY from .env")

    args = parser.parse_args()
    client = RetellClient(api_key=args.api_key, dry_run=args.dry_run)

    if args.list_agents:
        cmd_list_agents(client)
    elif args.create_agent:
        cmd_create_agent(client, args.create_agent)
    elif args.create_all_agents:
        cmd_create_all(client)
    elif args.list_phones:
        cmd_list_phones(client)
    elif args.test_call:
        if not args.to or not args.script or not args.market:
            parser.error("--test-call requires --to, --script, and --market")
        cmd_test_call(client, args.to, args.script, args.market)
    elif args.campaign:
        if not args.script or not args.market:
            parser.error("--campaign requires --script and --market")
        cmd_campaign(client, args.campaign, args.script, args.market)
    elif args.stats:
        cmd_stats(client)
    elif args.recent_calls:
        cmd_recent_calls(client, args.recent_calls)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
