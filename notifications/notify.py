"""Notification dispatchers for SAM.gov monitoring alerts.

Supports Slack (incoming webhook) and email (Resend API). Both fail
gracefully — a missing credential logs a warning and returns False.

No new packages required; uses ``requests`` which is already a dependency.

Usage:
    from notifications.notify import send_slack_notification, send_email_notification
"""

import logging
import os

import requests
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)


# ── Slack ─────────────────────────────────────────────────────────────────

def send_slack_notification(webhook_url: str, text: str, blocks: list | None = None) -> bool:
    """POST a message to a Slack incoming webhook.

    Returns True on success, False on failure (logged, not raised).
    """
    if not webhook_url:
        log.warning("Slack webhook URL not configured — skipping notification")
        return False

    payload = {"text": text}
    if blocks:
        payload["blocks"] = blocks

    try:
        resp = requests.post(webhook_url, json=payload, timeout=10)
        if resp.status_code == 200:
            log.info("Slack notification sent successfully")
            return True
        log.warning(f"Slack notification failed: {resp.status_code} {resp.text}")
        return False
    except requests.RequestException as e:
        log.warning(f"Slack notification error: {e}")
        return False


def format_slack_opportunity_summary(
    new_opps: list[dict],
    total_count: int,
    sheet_url: str = "",
) -> tuple[str, list]:
    """Build Slack Block Kit formatted message for new opportunities.

    Returns (fallback_text, blocks_list).
    """
    fallback = f"SAM.gov Monitor: {len(new_opps)} new opportunities found ({total_count} total)"

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "SAM.gov Daily Scan Results"},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*{len(new_opps)} new* opportunities detected "
                    f"({total_count} total in pipeline)"
                ),
            },
        },
        {"type": "divider"},
    ]

    # Top 5 new opportunities
    for opp in new_opps[:5]:
        title = (opp.get("title") or "Untitled")[:80]
        agency = opp.get("agency", "Unknown agency")[:60]
        deadline = opp.get("response_deadline", "N/A")
        naics = opp.get("naics_code", "")
        sol = opp.get("solicitation_number", "")
        score_text = ""
        if opp.get("bid_score") is not None:
            score_text = f"  |  Score: *{opp['bid_score']}* ({opp.get('bid_decision', '')})"

        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": (
                    f"*{title}*\n"
                    f"{agency}  |  NAICS {naics}  |  {sol}\n"
                    f"Deadline: {deadline}{score_text}"
                ),
            },
        })

    if len(new_opps) > 5:
        blocks.append({
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"_...and {len(new_opps) - 5} more_"},
            ],
        })

    if sheet_url:
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"<{sheet_url}|View Pipeline Sheet>"},
        })

    return fallback, blocks


# ── Email (Resend API) ────────────────────────────────────────────────────

def send_email_notification(api_key: str, to: str, subject: str, html_body: str) -> bool:
    """Send an email via the Resend API.

    Returns True on success, False on failure (logged, not raised).
    """
    if not api_key:
        log.warning("Resend API key not configured — skipping email notification")
        return False
    if not to:
        log.warning("Resend recipient not configured — skipping email notification")
        return False

    try:
        resp = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "from": "Newport GovCon Monitor <onboarding@resend.dev>",
                "to": [to],
                "subject": subject,
                "html": html_body,
            },
            timeout=10,
        )
        if resp.status_code in (200, 201):
            log.info(f"Email notification sent to {to}")
            return True
        log.warning(f"Email notification failed: {resp.status_code} {resp.text}")
        return False
    except requests.RequestException as e:
        log.warning(f"Email notification error: {e}")
        return False


def format_email_opportunity_summary(
    new_opps: list[dict],
    total_count: int,
) -> tuple[str, str]:
    """Build email subject and HTML body for new opportunities.

    Returns (subject, html_body).
    """
    subject = f"SAM.gov Monitor: {len(new_opps)} new opportunities found"

    rows = ""
    for opp in new_opps[:20]:
        title = (opp.get("title") or "Untitled")[:80]
        agency = opp.get("agency", "")[:50]
        deadline = opp.get("response_deadline", "N/A")
        naics = opp.get("naics_code", "")
        sol = opp.get("solicitation_number", "")
        score = opp.get("bid_score", "")
        decision = opp.get("bid_decision", "")
        score_cell = f"{score} ({decision})" if score else "N/A"
        ui_link = opp.get("ui_link", "")

        title_html = f'<a href="{ui_link}">{title}</a>' if ui_link else title

        rows += f"""<tr>
            <td style="padding:6px;border:1px solid #ddd">{title_html}</td>
            <td style="padding:6px;border:1px solid #ddd">{agency}</td>
            <td style="padding:6px;border:1px solid #ddd">{naics}</td>
            <td style="padding:6px;border:1px solid #ddd">{sol}</td>
            <td style="padding:6px;border:1px solid #ddd">{deadline}</td>
            <td style="padding:6px;border:1px solid #ddd">{score_cell}</td>
        </tr>"""

    html_body = f"""<html><body style="font-family:Arial,sans-serif">
    <h2>SAM.gov Daily Scan Results</h2>
    <p><strong>{len(new_opps)} new</strong> opportunities detected
       ({total_count} total in pipeline).</p>
    <table style="border-collapse:collapse;width:100%">
        <tr style="background:#f5f5f5">
            <th style="padding:8px;border:1px solid #ddd;text-align:left">Title</th>
            <th style="padding:8px;border:1px solid #ddd;text-align:left">Agency</th>
            <th style="padding:8px;border:1px solid #ddd;text-align:left">NAICS</th>
            <th style="padding:8px;border:1px solid #ddd;text-align:left">Solicitation</th>
            <th style="padding:8px;border:1px solid #ddd;text-align:left">Deadline</th>
            <th style="padding:8px;border:1px solid #ddd;text-align:left">Score</th>
        </tr>
        {rows}
    </table>
    {"<p><em>Showing first 20 of " + str(len(new_opps)) + " new opportunities.</em></p>" if len(new_opps) > 20 else ""}
    <hr>
    <p style="color:#888;font-size:12px">Newport GovCon Command Center — automated daily scan</p>
    </body></html>"""

    return subject, html_body
