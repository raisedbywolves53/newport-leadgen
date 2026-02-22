"""Notification dispatchers for GovCon daily monitor alerts.

Supports Slack (incoming webhook) and email (Resend API). Both fail
gracefully — a missing credential logs a warning and returns False.

Usage:
    from notifications.notify import send_slack_notification, send_email_notification
"""

import logging
import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)


# -- Slack -------------------------------------------------------------------

def send_slack_notification(webhook_url: str, text: str, blocks: list | None = None) -> bool:
    """POST a message to a Slack incoming webhook."""
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
    deadlines: list[dict] | None = None,
    pipeline_stats: dict | None = None,
) -> tuple[str, list]:
    """Build Slack Block Kit formatted message for the daily digest."""
    fallback = f"Newport GovCon Daily Brief: {len(new_opps)} new opportunities ({total_count} total)"

    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"Newport GovCon Daily Brief — {datetime.now():%b %d, %Y}"},
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{len(new_opps)} new* opportunities detected ({total_count} total in pipeline)",
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

    # Deadline summary
    if deadlines:
        blocks.append({"type": "divider"})
        deadline_lines = []
        for d in deadlines[:5]:
            title = (d.get("title") or "?")[:50]
            days = d.get("_days_until", "?")
            deadline_lines.append(f"• *{title}* — {days} days")
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Upcoming Deadlines (7 days)*\n" + "\n".join(deadline_lines),
            },
        })

    # Pipeline snapshot
    if pipeline_stats:
        active = pipeline_stats.get("active_count", 0)
        value = pipeline_stats.get("pipeline_value", 0)
        blocks.append({
            "type": "context",
            "elements": [
                {"type": "mrkdwn", "text": f"Pipeline: {active} active | ${value:,.0f} total value"},
            ],
        })

    return fallback, blocks


# -- Email (Resend API) ------------------------------------------------------

def send_email_notification(api_key: str, to: str, subject: str, html_body: str) -> bool:
    """Send an email via the Resend API."""
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


def format_email_digest(
    new_opps: list[dict],
    total_count: int,
    deadlines: list[dict] | None = None,
    pipeline_stats: dict | None = None,
) -> tuple[str, str]:
    """Build the daily digest email (subject + HTML body).

    Format per Phase 2 spec:
      - NEW OPPORTUNITIES section with score/recommendation
      - UPCOMING DEADLINES section
      - PIPELINE SNAPSHOT section
    """
    today = datetime.now().strftime("%b %d, %Y")
    subject = f"Newport GovCon Daily Brief — {today}"

    # --- New Opportunities ---
    opp_rows = ""
    for opp in new_opps[:20]:
        title = (opp.get("title") or "Untitled")[:80]
        agency = opp.get("agency", "")[:50]
        value = opp.get("contract_value", opp.get("contract_size_est", ""))
        naics = opp.get("naics_code", "")
        deadline = opp.get("response_deadline", "N/A")
        score = opp.get("bid_score", "")
        decision = opp.get("bid_decision", "")
        score_cell = f"{score}/100 — {decision}" if score else "Not scored"
        ui_link = opp.get("ui_link", "")
        sol = opp.get("solicitation_number", "")

        title_html = f'<a href="{ui_link}" style="color:#1C7293">{title}</a>' if ui_link else title

        opp_rows += f"""<tr>
            <td style="padding:8px;border-bottom:1px solid #eee">
                <strong>{title_html}</strong><br>
                <span style="color:#666;font-size:13px">
                    Agency: {agency} | Value: {value} | NAICS: {naics}<br>
                    Deadline: {deadline} | {sol}<br>
                    <strong>Score: {score_cell}</strong>
                </span>
            </td>
        </tr>"""

    more_text = ""
    if len(new_opps) > 20:
        more_text = f'<p style="color:#888;font-size:13px">Showing first 20 of {len(new_opps)} new opportunities.</p>'

    # --- Upcoming Deadlines ---
    deadline_rows = ""
    if deadlines:
        for d in deadlines[:10]:
            title = (d.get("title") or "?")[:60]
            dl_date = d.get("response_deadline", "N/A")
            days = d.get("_days_until", "?")
            stage = d.get("stage", "")
            color = "#dc3545" if isinstance(days, int) and days <= 3 else "#ffc107" if isinstance(days, int) and days <= 7 else "#666"
            deadline_rows += f"""<tr>
                <td style="padding:6px;border-bottom:1px solid #eee">
                    <strong style="color:{color}">{title}</strong> — Due {dl_date} ({days} days)<br>
                    <span style="color:#888;font-size:13px">Stage: {stage}</span>
                </td>
            </tr>"""

    # --- Pipeline Snapshot ---
    snapshot_html = ""
    if pipeline_stats:
        active = pipeline_stats.get("active_count", 0)
        proposals = pipeline_stats.get("proposals_in_progress", 0)
        submitted = pipeline_stats.get("submitted_awaiting", 0)
        value = pipeline_stats.get("pipeline_value", 0)
        snapshot_html = f"""
        <h3 style="color:#065A82;margin-top:24px">PIPELINE SNAPSHOT</h3>
        <table style="width:100%">
            <tr><td style="padding:4px">Active Opportunities:</td><td style="padding:4px"><strong>{active}</strong></td></tr>
            <tr><td style="padding:4px">Proposals in Progress:</td><td style="padding:4px"><strong>{proposals}</strong></td></tr>
            <tr><td style="padding:4px">Submitted &amp; Awaiting:</td><td style="padding:4px"><strong>{submitted}</strong></td></tr>
            <tr><td style="padding:4px">Pipeline Value:</td><td style="padding:4px"><strong>${value:,.0f}</strong></td></tr>
        </table>"""

    html_body = f"""<html><body style="font-family:Arial,sans-serif;max-width:700px;margin:0 auto">
    <div style="background:#065A82;padding:20px;color:#fff">
        <h1 style="margin:0">Newport GovCon Daily Brief</h1>
        <p style="margin:4px 0 0">{today}</p>
    </div>
    <div style="padding:16px">
        <h3 style="color:#065A82">NEW OPPORTUNITIES ({len(new_opps)})</h3>
        <table style="width:100%">{opp_rows}</table>
        {more_text}

        {"<h3 style='color:#065A82;margin-top:24px'>UPCOMING DEADLINES (Next 7 Days)</h3><table style='width:100%'>" + deadline_rows + "</table>" if deadline_rows else ""}

        {snapshot_html}
    </div>
    <hr style="border:none;border-top:1px solid #ddd;margin-top:24px">
    <p style="color:#888;font-size:12px;padding:0 16px">Newport GovCon Command Center — automated daily scan</p>
    </body></html>"""

    return subject, html_body
