"""Retell AI agent configuration manager — loads, fills, validates voice scripts.

Usage:
    python outreach/voice/retell_config.py --validate
    python outreach/voice/retell_config.py --show new_homeowner
    python outreach/voice/retell_config.py --fill new_homeowner --first-name "Sarah" --street "123 Oak Dr"
"""

import argparse
import json
import re
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"

# ICP type → script name mapping
ICP_TO_SCRIPT = {
    "new_homeowners": "new_homeowner",
    "real_estate_agents": "referral_partner",
    "property_managers": "referral_partner",
    "home_inspectors": "referral_partner",
    "insurance_agents": "referral_partner",
    "builders_contractors": "referral_partner",
    "adjacent_trades": "referral_partner",
    "storm_damage": "storm_damage",
    "commercial_properties": "commercial",
    "aging_neighborhoods": "aging_neighborhood",
}

REQUIRED_FIELDS = [
    "agent_name",
    "voice",
    "first_sentence",
    "system_prompt",
    "max_call_duration_ms",
    "post_call_analysis_schema",
]

ANALYSIS_REQUIRED_KEYS = ["interested", "callback_requested", "notes", "objection"]


class RetellConfig:
    """Manages Retell AI agent configurations and script loading."""

    def __init__(self, scripts_dir: Path = None):
        self.scripts_dir = scripts_dir or SCRIPTS_DIR
        self.agents = {}

    def load_script(self, script_name: str) -> dict:
        """Load a script config by name (without .json extension).

        Args:
            script_name: Script filename without extension (e.g. 'new_homeowner').

        Returns:
            Parsed JSON dict of the script configuration.
        """
        if script_name in self.agents:
            return self.agents[script_name]

        path = self.scripts_dir / f"{script_name}.json"
        if not path.exists():
            available = [f.stem for f in self.scripts_dir.glob("*.json")]
            raise FileNotFoundError(
                f"Script not found: {script_name}. "
                f"Available: {', '.join(available)}"
            )

        with open(path) as f:
            data = json.load(f)

        self.agents[script_name] = data
        return data

    def fill_script(self, script_name: str, lead_data: dict) -> dict:
        """Fill template variables in first_sentence with lead data.

        Template variables: {first_name}, {street}, {business_name}, {partner_type}

        Args:
            script_name: Script name to load and fill.
            lead_data: Dict with lead fields to substitute.

        Returns:
            Copy of the script config with first_sentence variables filled.
        """
        script = self.load_script(script_name)
        filled = script.copy()

        values = {
            "first_name": str(lead_data.get("first_name", "")).strip() or "there",
            "street": str(lead_data.get("street", "")).strip() or "your street",
            "business_name": str(lead_data.get("business_name",
                                 lead_data.get("company_name", ""))).strip()
                             or "your company",
            "partner_type": str(lead_data.get("partner_type",
                                lead_data.get("trade_type", ""))).strip()
                            or "professional",
        }

        try:
            filled["first_sentence"] = script["first_sentence"].format(**values)
        except KeyError:
            # Fill what we can with regex fallback
            result = script["first_sentence"]
            for key, val in values.items():
                result = result.replace(f"{{{key}}}", val)
            filled["first_sentence"] = result

        return filled

    def get_all_scripts(self) -> dict:
        """Return all available script configs, keyed by script name.

        Returns:
            Dict mapping script_name → parsed JSON config.
        """
        scripts = {}
        for path in sorted(self.scripts_dir.glob("*.json")):
            name = path.stem
            scripts[name] = self.load_script(name)
        return scripts

    def validate_script(self, script_data: dict) -> tuple:
        """Validate a script has all required fields.

        Args:
            script_data: Parsed script JSON dict.

        Returns:
            Tuple of (is_valid: bool, errors: list[str]).
        """
        errors = []

        for field in REQUIRED_FIELDS:
            if field not in script_data:
                errors.append(f"Missing required field: {field}")
            elif not script_data[field]:
                errors.append(f"Empty required field: {field}")

        # Validate voice
        if script_data.get("voice") not in ("male", "female"):
            errors.append(f"Invalid voice: {script_data.get('voice')} (must be 'male' or 'female')")

        # Validate max_call_duration_ms is a positive number
        duration = script_data.get("max_call_duration_ms")
        if not isinstance(duration, (int, float)) or duration <= 0:
            errors.append(f"Invalid max_call_duration_ms: {duration}")

        # Validate first_sentence has template variables (braces)
        first = script_data.get("first_sentence", "")
        if not first:
            errors.append("first_sentence is empty")

        # Validate system_prompt contains transfer protocol
        prompt = script_data.get("system_prompt", "")
        if "transfer_to" not in prompt:
            errors.append("system_prompt missing transfer_to function call reference")
        if "notify_missed_transfer" not in prompt:
            errors.append("system_prompt missing notify_missed_transfer reference")
        if "248-509-0470" not in prompt and "12485090470" not in prompt:
            errors.append("system_prompt missing Tal's phone number")

        # Validate post_call_analysis_schema
        schema = script_data.get("post_call_analysis_schema", {})
        if isinstance(schema, dict):
            for key in ANALYSIS_REQUIRED_KEYS:
                if key not in schema:
                    errors.append(f"post_call_analysis_schema missing key: {key}")
        else:
            errors.append("post_call_analysis_schema must be a dict")

        return (len(errors) == 0, errors)

    def get_script_for_icp(self, icp_type: str) -> str:
        """Map ICP type to script name.

        Args:
            icp_type: ICP type string from icp_definitions.json.

        Returns:
            Script name (without .json extension).

        Raises:
            ValueError: If ICP type has no script mapping.
        """
        script = ICP_TO_SCRIPT.get(icp_type)
        if not script:
            raise ValueError(
                f"No script mapping for ICP: {icp_type}. "
                f"Known ICPs: {', '.join(ICP_TO_SCRIPT.keys())}"
            )
        return script


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def cmd_validate(config: RetellConfig) -> None:
    """Validate all scripts and print results."""
    scripts = config.get_all_scripts()
    all_pass = True

    print(f"\nValidating {len(scripts)} scripts...\n")

    for name, data in scripts.items():
        valid, errors = config.validate_script(data)
        status = "PASS" if valid else "FAIL"
        print(f"  [{status}] {name}")
        if errors:
            all_pass = False
            for err in errors:
                print(f"         - {err}")

    print()
    if all_pass:
        print(f"All {len(scripts)} scripts passed validation.")
    else:
        print("Some scripts have validation errors.")
        sys.exit(1)


def cmd_show(config: RetellConfig, script_name: str) -> None:
    """Pretty-print a script config."""
    try:
        data = config.load_script(script_name)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Script: {script_name}")
    print(f"{'='*60}")
    print(f"Agent Name:    {data['agent_name']}")
    print(f"Voice:         {data['voice']}")
    print(f"Max Duration:  {data['max_call_duration_ms']}ms "
          f"({data['max_call_duration_ms'] // 1000}s)")
    print(f"\nFirst Sentence:")
    print(f"  {data['first_sentence']}")
    print(f"\nSystem Prompt ({len(data['system_prompt'])} chars):")
    # Print first 500 chars with indent
    prompt_preview = data["system_prompt"][:500]
    for line in prompt_preview.split("\n"):
        print(f"  {line}")
    if len(data["system_prompt"]) > 500:
        print(f"  ... ({len(data['system_prompt']) - 500} more chars)")
    print(f"\nPost-Call Analysis Schema:")
    for key, schema in data["post_call_analysis_schema"].items():
        print(f"  {key} ({schema['type']}): {schema['description']}")
    print()


def cmd_fill(config: RetellConfig, script_name: str, lead_data: dict) -> None:
    """Show a script with template variables filled."""
    try:
        filled = config.fill_script(script_name, lead_data)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Filled Script: {script_name}")
    print(f"Lead Data: {lead_data}")
    print(f"{'='*60}")
    print(f"\nFirst Sentence (filled):")
    print(f"  {filled['first_sentence']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Retell AI voice agent configuration manager"
    )
    parser.add_argument(
        "--validate", action="store_true",
        help="Validate all script configurations"
    )
    parser.add_argument(
        "--show", metavar="SCRIPT",
        help="Pretty-print a script config (e.g. new_homeowner)"
    )
    parser.add_argument(
        "--fill", metavar="SCRIPT",
        help="Show filled script with template variables replaced"
    )
    parser.add_argument("--first-name", help="Lead first name for --fill")
    parser.add_argument("--street", help="Lead street address for --fill")
    parser.add_argument("--business-name", help="Business name for --fill")
    parser.add_argument("--partner-type", help="Partner type for --fill")

    args = parser.parse_args()
    config = RetellConfig()

    if args.validate:
        cmd_validate(config)
    elif args.show:
        cmd_show(config, args.show)
    elif args.fill:
        lead_data = {}
        if args.first_name:
            lead_data["first_name"] = args.first_name
        if args.street:
            lead_data["street"] = args.street
        if args.business_name:
            lead_data["business_name"] = args.business_name
        if args.partner_type:
            lead_data["partner_type"] = args.partner_type
        cmd_fill(config, args.fill, lead_data)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
