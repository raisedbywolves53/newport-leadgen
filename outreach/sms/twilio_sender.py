"""Twilio SMS sender — targeted SMS campaigns with opt-out management.

Usage:
    python outreach/sms/twilio_sender.py send --leads data/clay_enriched/homeowners.csv --template new_homeowner
    python outreach/sms/twilio_sender.py send-one --to +12485551234 --message "Test message" --market oakland_county_mi
    python outreach/sms/twilio_sender.py opt-outs
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException

load_dotenv()

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
OPT_OUT_PATH = PROJECT_ROOT / "data" / "sms_opt_outs.csv"
MARKETS_PATH = PROJECT_ROOT / "config" / "markets.json"

# Market region → .env variable for the Twilio from-number
REGION_PHONE_ENV = {
    "michigan": "TWILIO_PHONE_MI",
    "north_carolina": "TWILIO_PHONE_NC",
}


def setup_logging() -> logging.Logger:
    """Configure logging to console + daily log file."""
    logger = logging.getLogger("sms")
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)

    # Console — INFO and above
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console)

    # File — DEBUG and above
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    fh = logging.FileHandler(log_dir / f"sms_{date_str}.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(fh)

    return logger


log = setup_logging()


def load_markets() -> dict:
    """Load markets config for region lookup."""
    with open(MARKETS_PATH) as f:
        return json.load(f)["markets"]


def market_to_region(market: str) -> str:
    """Get the region (michigan / north_carolina) for a market key."""
    markets = load_markets()
    if market in markets:
        return markets[market]["region"]
    # Fallback: guess from the market key suffix
    if market.endswith("_mi"):
        return "michigan"
    if market.endswith("_nc"):
        return "north_carolina"
    log.error(f"Unknown market: {market}. Cannot determine region.")
    sys.exit(1)


def format_e164(phone: str) -> str:
    """Normalize a phone number to E.164 format (+1XXXXXXXXXX).

    Handles common US formats:
        (248) 555-1234, 248-555-1234, 2485551234, +12485551234
    """
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    # Already has country code or unusual length — return as-is with +
    if digits and not digits.startswith("+"):
        return f"+{digits}"
    return phone


def fill_template(template_msg: str, lead: dict, goldman_phone: str) -> str:
    """Fill merge tags in a template message with lead data.

    {phone} in the message refers to Goldman's phone number, not the lead's.
    """
    values = {
        "first_name": str(lead.get("first_name", "")).strip() or "there",
        "city": str(lead.get("city", "")).strip() or "your area",
        "phone": goldman_phone,
        "trade_type": str(lead.get("trade_type", "")).strip(),
        "role_type": str(lead.get("role_type", "")).strip(),
        "client_type": str(lead.get("client_type", "")).strip(),
        "topic": str(lead.get("topic", "")).strip() or "garage door service",
        "year_built": str(lead.get("year_built", "")).strip(),
        "street": str(lead.get("street", "")).strip(),
        "company_name": str(lead.get("company_name", "")).strip(),
    }
    try:
        return template_msg.format(**values)
    except KeyError as exc:
        log.warning(f"Missing merge tag {exc} for lead {lead.get('email', 'unknown')}")
        # Fill what we can — replace remaining tags with empty string
        result = template_msg
        for key, val in values.items():
            result = result.replace(f"{{{key}}}", val)
        return result


class TwilioSender:
    """Send and manage SMS outreach through Twilio."""

    def __init__(self, account_sid: str = None, auth_token: str = None):
        self.account_sid = account_sid or os.environ.get("TWILIO_ACCOUNT_SID", "")
        self.auth_token = auth_token or os.environ.get("TWILIO_AUTH_TOKEN", "")

        if not self.account_sid or not self.auth_token:
            log.error(
                "ERROR: Twilio credentials not set. Add to your .env file:\n"
                "  TWILIO_ACCOUNT_SID=your_sid\n"
                "  TWILIO_AUTH_TOKEN=your_token\n"
                "Get credentials at https://console.twilio.com"
            )
            sys.exit(1)

        self.client = TwilioClient(self.account_sid, self.auth_token)

        # Load from-numbers from env
        self.from_numbers = {}
        for region, env_var in REGION_PHONE_ENV.items():
            number = os.environ.get(env_var, "")
            if number:
                self.from_numbers[region] = format_e164(number)

        if not self.from_numbers:
            log.warning(
                "No Twilio phone numbers configured. Set TWILIO_PHONE_MI "
                "and/or TWILIO_PHONE_NC in .env"
            )

    def _get_from_number(self, market: str) -> str:
        """Get the correct Twilio from-number for a market."""
        region = market_to_region(market)
        number = self.from_numbers.get(region)
        if not number:
            env_var = REGION_PHONE_ENV.get(region, "TWILIO_PHONE_??")
            log.error(f"No Twilio number for region '{region}'. Set {env_var} in .env")
            sys.exit(1)
        return number

    def send_sms(self, to_number: str, message: str, market: str) -> dict:
        """Send a single SMS via Twilio.

        Args:
            to_number: Recipient phone (any US format, will be normalized to E.164).
            message: Message body.
            market: Market key (oakland_county_mi, wayne_county_mi, triangle_nc).

        Returns:
            Dict with sid, status, date_sent.
        """
        to_e164 = format_e164(to_number)
        from_number = self._get_from_number(market)

        log.debug(f"Sending SMS: {from_number} → {to_e164}")

        try:
            msg = self.client.messages.create(
                body=message,
                from_=from_number,
                to=to_e164,
            )
            result = {
                "sid": msg.sid,
                "status": msg.status,
                "date_sent": str(msg.date_created),
            }
            log.debug(f"  Sent: {msg.sid} ({msg.status})")
            return result

        except TwilioRestException as exc:
            log.error(f"Twilio error sending to {to_e164}: {exc}")
            raise

    def send_campaign(self, leads_csv: str, template_name: str) -> dict:
        """Send an SMS campaign to leads from a CSV.

        Args:
            leads_csv: Path to enriched CSV (must have 'phone' and 'market' columns).
            template_name: Template filename without .json (e.g. 'new_homeowner').

        Returns:
            Dict with sent, skipped, errors, skipped_reasons.
        """
        # Load template
        template_path = TEMPLATES_DIR / f"{template_name}.json"
        if not template_path.exists():
            log.error(f"Template not found: {template_path}")
            available = [f.stem for f in TEMPLATES_DIR.glob("*.json")]
            log.error(f"Available: {', '.join(available)}")
            sys.exit(1)

        with open(template_path) as f:
            template = json.load(f)

        template_msg = template["message"]
        log.info(f"SMS Campaign: {template_name}")
        log.info(f"  Template: {template_path.name}")

        # Load leads
        csv_path = Path(leads_csv)
        if not csv_path.exists():
            log.error(f"Leads CSV not found: {csv_path}")
            sys.exit(1)

        df = pd.read_csv(csv_path)
        log.info(f"  Loaded {len(df)} leads from {csv_path.name}")

        # Required columns check
        if "phone" not in df.columns:
            log.error("CSV missing required 'phone' column")
            sys.exit(1)
        if "market" not in df.columns:
            log.error("CSV missing required 'market' column")
            sys.exit(1)

        # Load opt-outs
        opt_outs = self.check_opt_outs()
        if opt_outs:
            log.info(f"  Opt-out list: {len(opt_outs)} numbers")

        sent = 0
        skipped = 0
        errors = 0
        skipped_reasons = []

        for idx, row in df.iterrows():
            lead = row.to_dict()
            raw_phone = str(lead.get("phone", "")).strip()

            # Skip if no phone
            if not raw_phone or raw_phone == "nan" or len(re.sub(r"\D", "", raw_phone)) < 7:
                reason = f"Row {idx}: missing/invalid phone"
                skipped_reasons.append(reason)
                log.debug(f"  Skip: {reason}")
                skipped += 1
                continue

            to_e164 = format_e164(raw_phone)

            # Skip if opted out
            if to_e164 in opt_outs:
                reason = f"Row {idx}: opted out ({to_e164})"
                skipped_reasons.append(reason)
                log.debug(f"  Skip: {reason}")
                skipped += 1
                continue

            market = str(lead.get("market", "")).strip()
            if not market:
                reason = f"Row {idx}: missing market"
                skipped_reasons.append(reason)
                log.debug(f"  Skip: {reason}")
                skipped += 1
                continue

            # Get Goldman's phone for this market (the {phone} merge tag)
            goldman_phone = self._get_from_number(market)
            message = fill_template(template_msg, lead, goldman_phone)

            try:
                self.send_sms(to_e164, message, market)
                sent += 1
                if sent % 10 == 0:
                    log.info(f"  Progress: {sent} sent...")
            except Exception as exc:
                log.error(f"  Error row {idx} ({to_e164}): {exc}")
                errors += 1

            # Rate limiting: 3-second delay between sends
            time.sleep(3)

        log.info(f"\nCampaign complete: {sent} sent, {skipped} skipped, {errors} errors")
        if skipped_reasons:
            log.info(f"Skip reasons ({len(skipped_reasons)}):")
            for reason in skipped_reasons[:20]:
                log.info(f"  - {reason}")
            if len(skipped_reasons) > 20:
                log.info(f"  ... and {len(skipped_reasons) - 20} more")

        return {
            "sent": sent,
            "skipped": skipped,
            "errors": errors,
            "skipped_reasons": skipped_reasons,
        }

    @staticmethod
    def check_opt_outs() -> set:
        """Read opt-out numbers from the opt-out CSV.

        Returns:
            Set of E.164 formatted phone numbers that have opted out.
        """
        if not OPT_OUT_PATH.exists():
            return set()

        opt_outs = set()
        df = pd.read_csv(OPT_OUT_PATH)
        if "phone" in df.columns:
            for phone in df["phone"].dropna():
                opt_outs.add(format_e164(str(phone).strip()))
        return opt_outs

    @staticmethod
    def add_opt_out(phone: str) -> None:
        """Add a phone number to the opt-out list.

        Args:
            phone: Phone number in any format (will be normalized to E.164).
        """
        e164 = format_e164(phone)

        # Check if already opted out
        existing = TwilioSender.check_opt_outs()
        if e164 in existing:
            log.info(f"Already opted out: {e164}")
            return

        # Ensure data directory exists
        OPT_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Append to CSV (create with header if new)
        write_header = not OPT_OUT_PATH.exists()
        with open(OPT_OUT_PATH, "a") as f:
            if write_header:
                f.write("phone,date_added\n")
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{e164},{date_str}\n")

        log.info(f"Opted out: {e164}")


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Twilio SMS sender for Goldman's lead gen"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # send (campaign)
    send_p = subparsers.add_parser("send", help="Send SMS campaign to leads CSV")
    send_p.add_argument(
        "--leads", required=True,
        help="Path to enriched leads CSV (must have 'phone' and 'market' columns)"
    )
    send_p.add_argument(
        "--template", required=True,
        help="Template name without .json (e.g. new_homeowner, storm_damage)"
    )

    # send-one
    one_p = subparsers.add_parser("send-one", help="Send a single test SMS")
    one_p.add_argument("--to", required=True, help="Recipient phone number")
    one_p.add_argument("--message", required=True, help="Message body")
    one_p.add_argument(
        "--market", required=True,
        help="Market for from-number (oakland_county_mi, wayne_county_mi, triangle_nc)"
    )

    # opt-outs
    subparsers.add_parser("opt-outs", help="List all opted-out numbers")

    # add-opt-out
    add_p = subparsers.add_parser("add-opt-out", help="Add a number to opt-out list")
    add_p.add_argument("--phone", required=True, help="Phone number to opt out")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "opt-outs":
        opt_outs = TwilioSender.check_opt_outs()
        if not opt_outs:
            print("No opted-out numbers.")
        else:
            print(f"\nOpted-out numbers ({len(opt_outs)}):")
            for number in sorted(opt_outs):
                print(f"  {number}")
            print()
        return

    if args.command == "add-opt-out":
        TwilioSender.add_opt_out(args.phone)
        return

    # Commands below need Twilio credentials
    sender = TwilioSender()

    if args.command == "send":
        result = sender.send_campaign(args.leads, args.template)
        print(f"\nResults: {result['sent']} sent, "
              f"{result['skipped']} skipped, {result['errors']} errors")

    elif args.command == "send-one":
        result = sender.send_sms(args.to, args.message, args.market)
        print(f"\nSent: {result['sid']} ({result['status']})")


if __name__ == "__main__":
    main()
