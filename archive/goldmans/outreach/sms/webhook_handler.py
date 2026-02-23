"""Goldman's Garage Door Repair - SMS Webhook Handler

Handles inbound SMS replies from prospects via Twilio webhooks.
- Opt-out/re-subscribe management
- Real-time notification to Tal via SMS
- Auto-response to prospects
- Delivery status tracking

Setup:
1. pip install flask twilio
2. Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN in .env
3. Run: python outreach/sms/webhook_handler.py
4. Expose via ngrok for dev: ngrok http 5000
5. Set Twilio webhook URL to: https://your-ngrok-url/sms/inbound

Production: Deploy behind gunicorn with proper HTTPS

Usage:
    python outreach/sms/webhook_handler.py                    # Start server on port 5000
    python outreach/sms/webhook_handler.py --port 8080        # Custom port
    python outreach/sms/webhook_handler.py --test-inbound     # Simulate an inbound SMS
    python outreach/sms/webhook_handler.py --test-status      # Simulate a status callback
"""

import argparse
import json
import logging
import os
import re
import sys
import threading
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request, abort
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REPLIES_PATH = DATA_DIR / "sms_replies.json"
DELIVERY_LOG_PATH = DATA_DIR / "sms_delivery_log.json"
OPT_OUT_PATH = DATA_DIR / "sms_opt_outs.csv"

TAL_PHONE = os.environ.get("TAL_PHONE_NUMBER", "+12485090470")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
WEBHOOK_PORT = int(os.environ.get("WEBHOOK_PORT", "5000"))

OPT_OUT_WORDS = {"stop", "unsubscribe", "cancel", "end", "quit"}
RESUBSCRIBE_WORDS = {"start", "subscribe"}

# Thread-safe lock for opt-out file access
_opt_out_lock = threading.Lock()
# Thread-safe lock for JSON log file access
_replies_lock = threading.Lock()
_delivery_lock = threading.Lock()


def setup_logging() -> logging.Logger:
    """Configure logging to console + daily log file."""
    logger = logging.getLogger("webhook")
    if logger.handlers:
        return logger
    logger.setLevel(logging.DEBUG)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console)

    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(log_dir / "webhook.log")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(fh)

    return logger


log = setup_logging()


# ------------------------------------------------------------------
# Phone number helpers
# ------------------------------------------------------------------

def format_e164(phone: str) -> str:
    """Normalize a phone number to E.164 format (+1XXXXXXXXXX)."""
    digits = re.sub(r"\D", "", str(phone))
    if len(digits) == 10:
        return f"+1{digits}"
    if len(digits) == 11 and digits.startswith("1"):
        return f"+{digits}"
    if digits and not digits.startswith("+"):
        return f"+{digits}"
    return phone


def redact_phone(phone: str) -> str:
    """Redact a phone number for logging: +1248***0470."""
    e164 = format_e164(phone)
    if len(e164) >= 8:
        return e164[:4] + "***" + e164[-4:]
    return "***"


# ------------------------------------------------------------------
# Opt-out management (thread-safe, CSV-based — shared with twilio_sender)
# ------------------------------------------------------------------

def load_opt_outs() -> set:
    """Load opted-out numbers from CSV."""
    with _opt_out_lock:
        if not OPT_OUT_PATH.exists():
            return set()
        opt_outs = set()
        with open(OPT_OUT_PATH) as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue  # skip header
                parts = line.strip().split(",")
                if parts and parts[0]:
                    opt_outs.add(format_e164(parts[0]))
        return opt_outs


def add_opt_out(phone: str) -> None:
    """Add a phone number to the opt-out CSV (thread-safe)."""
    e164 = format_e164(phone)
    with _opt_out_lock:
        existing = set()
        if OPT_OUT_PATH.exists():
            with open(OPT_OUT_PATH) as f:
                for i, line in enumerate(f):
                    if i == 0:
                        continue
                    parts = line.strip().split(",")
                    if parts and parts[0]:
                        existing.add(format_e164(parts[0]))

        if e164 in existing:
            log.info(f"Already opted out: {redact_phone(e164)}")
            return

        DATA_DIR.mkdir(parents=True, exist_ok=True)
        write_header = not OPT_OUT_PATH.exists()
        with open(OPT_OUT_PATH, "a") as f:
            if write_header:
                f.write("phone,date_added\n")
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{e164},{date_str}\n")

    log.info(f"Opted out: {redact_phone(e164)}")


def remove_opt_out(phone: str) -> None:
    """Remove a phone number from the opt-out CSV (re-subscribe, thread-safe)."""
    e164 = format_e164(phone)
    with _opt_out_lock:
        if not OPT_OUT_PATH.exists():
            return

        lines = []
        with open(OPT_OUT_PATH) as f:
            lines = f.readlines()

        # Rewrite without the matching number
        with open(OPT_OUT_PATH, "w") as f:
            for i, line in enumerate(lines):
                if i == 0:
                    f.write(line)  # keep header
                    continue
                parts = line.strip().split(",")
                if parts and format_e164(parts[0]) != e164:
                    f.write(line)

    log.info(f"Re-subscribed: {redact_phone(e164)}")


# ------------------------------------------------------------------
# JSON log helpers (thread-safe)
# ------------------------------------------------------------------

def _append_json(filepath: Path, entry: dict, lock: threading.Lock) -> None:
    """Append an entry to a JSON array file (thread-safe)."""
    with lock:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        entries = []
        if filepath.exists():
            try:
                with open(filepath) as f:
                    entries = json.load(f)
            except (json.JSONDecodeError, ValueError):
                entries = []
        entries.append(entry)
        with open(filepath, "w") as f:
            json.dump(entries, f, indent=2)


def log_reply(from_number: str, to_number: str, body: str, message_sid: str) -> None:
    """Log an inbound reply to data/sms_replies.json."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "from": from_number,
        "to": to_number,
        "body": body,
        "message_sid": message_sid,
    }
    _append_json(REPLIES_PATH, entry, _replies_lock)
    log.debug(f"Reply logged: {message_sid}")


def log_delivery(message_sid: str, status: str, to_number: str,
                 error_code: str = None) -> None:
    """Log a delivery status update to data/sms_delivery_log.json."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "message_sid": message_sid,
        "status": status,
        "to": to_number,
    }
    if error_code:
        entry["error_code"] = error_code
    _append_json(DELIVERY_LOG_PATH, entry, _delivery_lock)


# ------------------------------------------------------------------
# Twilio request validation
# ------------------------------------------------------------------

def validate_twilio_request(req) -> bool:
    """Validate that a request actually came from Twilio.

    Returns True if valid or if running in debug mode. Returns False if
    validation fails (spoofed request).
    """
    if os.environ.get("FLASK_DEBUG") == "1":
        return True

    if not TWILIO_AUTH_TOKEN:
        log.warning("TWILIO_AUTH_TOKEN not set — skipping request validation")
        return True

    validator = RequestValidator(TWILIO_AUTH_TOKEN)
    url = req.url
    params = req.form.to_dict()
    signature = req.headers.get("X-Twilio-Signature", "")

    return validator.validate(url, params, signature)


# ------------------------------------------------------------------
# Notification sender (uses Twilio REST API directly to avoid
# circular import with TwilioSender's market-based routing)
# ------------------------------------------------------------------

def send_notification_to_tal(from_number: str, body: str, to_number: str) -> None:
    """Send a notification SMS to Tal about a lead reply.

    Uses Twilio REST API directly. Sends from whichever Goldman's number
    received the original message (the 'to_number' from the inbound webhook).
    """
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        log.warning("Twilio credentials not set — cannot notify Tal")
        return

    from twilio.rest import Client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    notification_body = (
        f"\U0001f514 Lead Reply!\n"
        f"From: {from_number}\n"
        f"Message: {body}\n"
        f"Reply directly to this number to respond."
    )

    try:
        msg = client.messages.create(
            body=notification_body,
            from_=to_number,  # Reply from same Goldman's number that received the SMS
            to=format_e164(TAL_PHONE),
        )
        log.info(f"  Notification sent to Tal: {msg.sid}")
    except Exception as exc:
        log.error(f"  Failed to notify Tal: {exc}")


def send_auto_response(from_number: str, to_number: str) -> str:
    """Build auto-response TwiML for a prospect reply.

    Returns the response message text.
    """
    return (
        "Thanks for reaching out! Tal from Goldman's Garage Door Repair "
        "will call you within the hour. If urgent, call us at 248-509-0470"
    )


# ------------------------------------------------------------------
# Flask app
# ------------------------------------------------------------------

app = Flask(__name__)


@app.route("/sms/inbound", methods=["POST"])
def handle_inbound():
    """Handle incoming SMS replies from prospects."""
    if not validate_twilio_request(request):
        log.warning(f"Invalid Twilio signature — rejecting request")
        abort(403)

    from_number = request.form.get("From", "")
    to_number = request.form.get("To", "")
    body = request.form.get("Body", "").strip()
    message_sid = request.form.get("MessageSid", "")

    log.info(f"Inbound SMS from {redact_phone(from_number)}: {body[:80]}")

    resp = MessagingResponse()
    body_lower = body.lower().strip()

    # Opt-out check
    if body_lower in OPT_OUT_WORDS:
        add_opt_out(from_number)
        resp.message("You've been unsubscribed. Reply START to re-subscribe.")
        log.info(f"  Opt-out processed for {redact_phone(from_number)}")
        return str(resp), 200, {"Content-Type": "text/xml"}

    # Re-subscribe check
    if body_lower in RESUBSCRIBE_WORDS:
        remove_opt_out(from_number)
        resp.message(
            "You've been re-subscribed. You'll hear from us again. "
            "Reply STOP anytime to opt out."
        )
        log.info(f"  Re-subscribe processed for {redact_phone(from_number)}")
        return str(resp), 200, {"Content-Type": "text/xml"}

    # Regular reply — log, notify Tal, auto-respond
    log_reply(from_number, to_number, body, message_sid)

    send_notification_to_tal(from_number, body, to_number)

    auto_msg = send_auto_response(from_number, to_number)
    resp.message(auto_msg)

    log.info(f"  Auto-response sent, Tal notified")
    return str(resp), 200, {"Content-Type": "text/xml"}


@app.route("/sms/status", methods=["POST"])
def handle_status():
    """Handle Twilio delivery status callbacks."""
    if not validate_twilio_request(request):
        log.warning("Invalid Twilio signature on status callback — rejecting")
        abort(403)

    message_sid = request.form.get("MessageSid", "")
    status = request.form.get("MessageStatus", "")
    to_number = request.form.get("To", "")
    error_code = request.form.get("ErrorCode", "")

    log_delivery(message_sid, status, to_number, error_code or None)

    if status in ("failed", "undelivered"):
        log.warning(
            f"Delivery failed: {message_sid} to {redact_phone(to_number)} "
            f"status={status} error={error_code}"
        )
    else:
        log.debug(f"Delivery status: {message_sid} → {status}")

    return "", 204


# ------------------------------------------------------------------
# Test simulation helpers
# ------------------------------------------------------------------

def test_inbound():
    """Simulate an inbound SMS for testing without Twilio."""
    print("\n=== Simulating Inbound SMS ===")
    print("From: +12485559876")
    print("To:   +12485551234")
    print("Body: 'Yes I'm interested in a garage door inspection'\n")

    # Test regular reply
    from_number = "+12485559876"
    to_number = "+12485551234"
    body = "Yes I'm interested in a garage door inspection"
    message_sid = "SM_TEST_" + datetime.now().strftime("%Y%m%d%H%M%S")

    log_reply(from_number, to_number, body, message_sid)
    print(f"[OK] Reply logged to {REPLIES_PATH}")

    auto_msg = send_auto_response(from_number, to_number)
    print(f"[OK] Auto-response: {auto_msg}")

    print(f"[OK] Would notify Tal at {TAL_PHONE}:")
    print(f"     \U0001f514 Lead Reply!")
    print(f"     From: {from_number}")
    print(f"     Message: {body}")
    print(f"     Reply directly to this number to respond.")

    # Test opt-out
    print("\n--- Simulating STOP ---")
    opt_out_phone = "+12485550000"
    add_opt_out(opt_out_phone)
    opt_outs = load_opt_outs()
    print(f"[OK] Opt-out list now has {len(opt_outs)} number(s)")
    assert opt_out_phone in opt_outs, "Opt-out not found!"

    # Test re-subscribe
    print("\n--- Simulating START (re-subscribe) ---")
    remove_opt_out(opt_out_phone)
    opt_outs = load_opt_outs()
    in_list = opt_out_phone in opt_outs
    print(f"[OK] {opt_out_phone} in opt-outs: {in_list}")

    print("\n=== Inbound test complete ===\n")


def test_status():
    """Simulate a delivery status callback for testing."""
    print("\n=== Simulating Delivery Status Callbacks ===")

    # Successful delivery
    sid1 = "SM_TEST_DELIVERED"
    log_delivery(sid1, "delivered", "+12485559876")
    print(f"[OK] Logged 'delivered' for {sid1}")

    # Failed delivery
    sid2 = "SM_TEST_FAILED"
    log_delivery(sid2, "failed", "+12485550000", error_code="30006")
    print(f"[OK] Logged 'failed' for {sid2} (error 30006)")

    # Undelivered
    sid3 = "SM_TEST_UNDELIVERED"
    log_delivery(sid3, "undelivered", "+12485550001", error_code="30003")
    print(f"[OK] Logged 'undelivered' for {sid3} (error 30003)")

    print(f"\n[OK] Delivery log written to {DELIVERY_LOG_PATH}")
    print("\n=== Status test complete ===\n")


# ------------------------------------------------------------------
# CLI
# ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Goldman's SMS Webhook Handler — inbound replies + delivery status"
    )
    parser.add_argument(
        "--port", type=int, default=WEBHOOK_PORT,
        help=f"Port to run the webhook server (default: {WEBHOOK_PORT})"
    )
    parser.add_argument(
        "--test-inbound", action="store_true",
        help="Simulate an inbound SMS (no server, no Twilio needed)"
    )
    parser.add_argument(
        "--test-status", action="store_true",
        help="Simulate delivery status callbacks (no server, no Twilio needed)"
    )

    args = parser.parse_args()

    if args.test_inbound:
        test_inbound()
        return

    if args.test_status:
        test_status()
        return

    # Start the Flask server
    debug = os.environ.get("FLASK_DEBUG") == "1"
    log.info(f"Starting webhook server on port {args.port}")
    log.info(f"  Inbound URL:  http://0.0.0.0:{args.port}/sms/inbound")
    log.info(f"  Status URL:   http://0.0.0.0:{args.port}/sms/status")
    log.info(f"  Debug mode:   {debug}")
    log.info(f"  Tal's phone:  {redact_phone(TAL_PHONE)}")
    log.info(f"  Opt-out file: {OPT_OUT_PATH}")
    log.info("")
    log.info("Expose with ngrok for dev: ngrok http " + str(args.port))
    log.info("Then set Twilio webhook URL to: https://your-ngrok-url/sms/inbound\n")

    app.run(host="0.0.0.0", port=args.port, debug=debug)


if __name__ == "__main__":
    main()
