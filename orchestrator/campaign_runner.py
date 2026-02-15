"""Orchestrate end-to-end lead gen campaigns.

Automated pipeline: scrape -> enrich (Apollo) -> outreach -> CRM

Usage:
    python -m orchestrator.campaign_runner homeowner --market oakland_county_mi
    python -m orchestrator.campaign_runner homeowner --market all --days 30
    python -m orchestrator.campaign_runner referral --market oakland_county_mi --icp-type real_estate_agents
    python -m orchestrator.campaign_runner referral --market all --icp-type real_estate_agents --enrich
    python -m orchestrator.campaign_runner outreach --csv data/enriched/real_estate_agents_20260214.csv --icp-type real_estate_agents --market oakland_county_mi
    python -m orchestrator.campaign_runner enrich --input data/raw/businesses_real_estate_agents_20260214.csv --icp-type real_estate_agents
    python -m orchestrator.campaign_runner storm --market oakland_county_mi
    python -m orchestrator.campaign_runner storm --market all --test
    python -m orchestrator.campaign_runner storm-monitor
    python -m orchestrator.campaign_runner schedule
    python -m orchestrator.campaign_runner status
    python -m orchestrator.campaign_runner --dry-run homeowner --market all
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import schedule as schedule_lib
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
ENRICHED_DIR = DATA_DIR / "enriched"
CLAY_READY_DIR = DATA_DIR / "clay_ready"

# Add project root to sys.path so sibling packages import cleanly
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scrapers import homeowner_scraper, gmaps_scraper, weather_monitor, clay_formatter
from enrichment.apollo_client import ApolloClient
from enrichment.enricher import enrich_businesses, save_enriched, print_enrichment_summary
from outreach.email.instantly_client import InstantlyClient
from outreach.sms.twilio_sender import TwilioSender
from outreach.voice.retell_client import RetellClient, load_leads_csv
from outreach.voice.retell_config import RetellConfig
from crm.sheets_manager import SheetsManager

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

log = logging.getLogger("campaign_runner")
log.setLevel(logging.DEBUG)

if not log.handlers:
    _console = logging.StreamHandler()
    _console.setLevel(logging.INFO)
    _console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S"))
    log.addHandler(_console)

    _fh = logging.FileHandler(LOG_DIR / f"campaign_runner_{datetime.now():%Y%m%d}.log")
    _fh.setLevel(logging.DEBUG)
    _fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    log.addHandler(_fh)

# ---------------------------------------------------------------------------
# Mappings
# ---------------------------------------------------------------------------

# icp_definitions.json "email_campaign" field -> actual template filename
EMAIL_TEMPLATE_MAP = {
    "agent_partner": "agent_partner.json",
    "pm_partner": "pm_partner.json",
    "inspector_partner": "inspector_partner.json",
    "insurance_partner": "insurance_partner.json",
    "builder_partner": "builder_partner.json",
    "trades_partner": "trade_swap.json",
    "new_homeowner": "welcome_home.json",
    "aging_home": "aging_neighborhood.json",
    "storm_response": "storm_response.json",
    "commercial": "commercial.json",
}

# ICP type -> SMS template name (matches filenames in outreach/sms/templates/)
SMS_TEMPLATE_MAP = {
    "new_homeowners": "new_homeowner",
    "storm_damage": "storm_damage",
    "real_estate_agents": "referral_partner",
    "property_managers": "referral_partner",
    "home_builders": "referral_partner",
}

SENDING_ACCOUNT = os.getenv(
    "INSTANTLY_SENDING_ACCOUNT", "tal@goldmansgaragedoorrepair.com"
)


# ===================================================================
# CampaignRunner
# ===================================================================

class CampaignRunner:
    """Run and coordinate multi-channel lead gen campaigns."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.markets = self._load_markets()
        self.icp_defs = self._load_icp_definitions()
        self.crm = SheetsManager(dry_run=dry_run)
        self._crm_connected = False

    # ------------------------------------------------------------------
    # Config helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_markets() -> dict:
        return homeowner_scraper.load_markets()

    @staticmethod
    def _load_icp_definitions() -> dict:
        return clay_formatter.load_icp_config()

    def _ensure_crm(self) -> bool:
        if not self._crm_connected:
            self._crm_connected = self.crm.connect()
            if self._crm_connected:
                self.crm.initialize_sheets()
        return self._crm_connected

    def _get_icp(self, icp_type: str) -> dict:
        icp = self.icp_defs.get(icp_type)
        if not icp:
            raise ValueError(
                f"Unknown ICP type: {icp_type}. "
                f"Valid: {', '.join(self.icp_defs.keys())}"
            )
        return icp

    def _resolve_markets(self, market: str) -> list[str]:
        """Return list of market keys for 'all' or a single key."""
        if market == "all":
            return list(self.markets.keys())
        if market not in self.markets:
            raise ValueError(
                f"Unknown market: {market}. "
                f"Valid: {', '.join(self.markets.keys())}, all"
            )
        return [market]

    # ------------------------------------------------------------------
    # Phase 1: Homeowner scrape campaign
    # ------------------------------------------------------------------

    def run_homeowner_campaign(self, market: str, days: int = 14) -> dict:
        """Scrape recently sold homes, format for Clay, and output clay-ready CSVs.

        Returns dict with per-ICP results including row counts and output paths.
        """
        log.info(f"=== Homeowner campaign: {market}, days={days} ===")
        market_cfg = self.markets[market]

        # Step 1: Scrape
        log.info(f"Scraping {market}...")
        df = homeowner_scraper.scrape_market(market, market_cfg, days)
        if df.empty:
            log.warning(f"No homes found for {market}")
            return {"market": market, "status": "empty", "rows": 0, "icps": {}}

        raw_path = homeowner_scraper.save(df, market, RAW_DIR)
        log.info(f"Raw data: {raw_path} ({len(df)} rows)")

        # Step 2: Split into ICP segments and format for Clay
        icp_config = self.icp_defs
        segments = {}

        # New homeowners: sold within last 30 days
        if "days_since_sold" in df.columns:
            new_df = df[df["days_since_sold"].notna() & (df["days_since_sold"] <= 30)]
            if not new_df.empty:
                segments["new_homeowners"] = new_df

        # Aging neighborhoods: older garage doors
        if "aging_door" in df.columns:
            aging_df = df[df["aging_door"] == True]
            if not aging_df.empty:
                segments["aging_neighborhoods"] = aging_df

        results = {"market": market, "status": "success", "rows": len(df), "icps": {}}

        for icp_type, segment_df in segments.items():
            channels = clay_formatter.get_outreach_channels(icp_type, icp_config)
            formatted = clay_formatter.format_homeowner(segment_df, icp_type, channels)

            CLAY_READY_DIR.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d")
            csv_path = CLAY_READY_DIR / f"{icp_type}_{market}_{date_str}.csv"
            formatted.to_csv(csv_path, index=False)

            instructions = clay_formatter.generate_instructions(icp_type, icp_config)
            md_path = CLAY_READY_DIR / f"clay_instructions_{icp_type}.md"
            md_path.write_text(instructions)

            results["icps"][icp_type] = {
                "rows": len(formatted),
                "clay_csv": str(csv_path),
                "instructions": str(md_path),
            }
            log.info(f"  {icp_type}: {len(formatted)} rows -> {csv_path}")

        # Print next steps
        log.info("")
        log.info("NEXT STEPS:")
        log.info("  1. Upload clay-ready CSVs to Clay for enrichment")
        log.info("  2. Follow the instructions in each clay_instructions_*.md file")
        log.info("  3. Export enriched CSVs to data/clay_enriched/")
        log.info("  4. Run: python -m orchestrator.campaign_runner outreach "
                 "--csv <enriched.csv> --icp-type <type> --market " + market)
        return results

    # ------------------------------------------------------------------
    # Phase 1: Referral partner scrape campaign
    # ------------------------------------------------------------------

    def run_referral_campaign(self, market: str, icp_type: str) -> dict:
        """Scrape referral partner businesses via Google Maps, format for Clay.

        Returns dict with row counts and output paths.
        """
        log.info(f"=== Referral campaign: {icp_type} in {market} ===")

        api_key = os.getenv("GOOGLE_PLACES_API_KEY")
        if not api_key:
            log.error("GOOGLE_PLACES_API_KEY not set — cannot scrape Google Maps")
            return {"status": "error", "reason": "missing_api_key"}

        all_queries = gmaps_scraper.load_queries()
        if icp_type not in all_queries:
            raise ValueError(
                f"No queries defined for ICP: {icp_type}. "
                f"Valid: {', '.join(all_queries.keys())}"
            )

        cat_cfg = all_queries[icp_type]

        # Filter queries to target market
        if market != "all":
            filtered_queries = [q for q in cat_cfg["queries"] if q["market"] == market]
            if not filtered_queries:
                log.warning(f"No queries match market={market} for {icp_type}")
                return {"status": "empty", "icp_type": icp_type, "market": market, "rows": 0}
            cat_cfg = dict(cat_cfg)
            cat_cfg["queries"] = filtered_queries

        log.info(f"Running {len(cat_cfg['queries'])} queries...")
        df = gmaps_scraper.scrape_category(icp_type, cat_cfg, api_key)

        if df.empty:
            log.warning(f"No businesses found for {icp_type}")
            return {"status": "empty", "icp_type": icp_type, "market": market, "rows": 0}

        raw_path = gmaps_scraper.save(df, icp_type, RAW_DIR)
        log.info(f"Raw data: {raw_path} ({len(df)} rows)")

        # Auto-enrich via Apollo if API key is configured
        apollo_key = os.getenv("APOLLO_API_KEY", "")
        enriched_csv = None

        if apollo_key and not self.dry_run:
            log.info("Enriching via Apollo.io...")
            try:
                client = ApolloClient(api_key=apollo_key)
                df = enrich_businesses(df, icp_type, client)
                enriched_path = save_enriched(df, icp_type, ENRICHED_DIR)
                print_enrichment_summary(df, icp_type)
                enriched_csv = str(enriched_path)
                log.info(f"Enriched data: {enriched_path}")
            except Exception as e:
                log.warning(f"Apollo enrichment failed ({e}), falling back to Clay workflow")

        if not enriched_csv:
            # Fallback: format for manual Clay enrichment
            icp_config = self.icp_defs
            channels = clay_formatter.get_outreach_channels(icp_type, icp_config)
            formatted = clay_formatter.format_business(df, icp_type, channels)

            CLAY_READY_DIR.mkdir(parents=True, exist_ok=True)
            date_str = datetime.now().strftime("%Y%m%d")
            csv_path = CLAY_READY_DIR / f"{icp_type}_{market}_{date_str}.csv"
            formatted.to_csv(csv_path, index=False)

            instructions = clay_formatter.generate_instructions(icp_type, icp_config)
            md_path = CLAY_READY_DIR / f"clay_instructions_{icp_type}.md"
            md_path.write_text(instructions)

            log.info(f"Clay-ready: {csv_path} ({len(formatted)} rows)")
            log.info("")
            log.info("NEXT STEPS (no Apollo key — manual Clay enrichment):")
            log.info("  1. Upload to Clay and run enrichment (see instructions)")
            log.info("  2. Export enriched CSV to data/enriched/")
            log.info("  3. Run: python -m orchestrator.campaign_runner outreach "
                     f"--csv <enriched.csv> --icp-type {icp_type} --market {market}")

        result = {
            "status": "success",
            "icp_type": icp_type,
            "market": market,
            "rows": len(df),
        }
        if enriched_csv:
            result["enriched_csv"] = enriched_csv
            log.info("")
            log.info("NEXT STEP:")
            log.info(f"  Run: python -m orchestrator.campaign_runner outreach "
                     f"--csv {enriched_csv} --icp-type {icp_type} --market {market}")
        return result

    # ------------------------------------------------------------------
    # Phase 2: Multi-channel outreach
    # ------------------------------------------------------------------

    def run_outreach(self, csv_path: str, icp_type: str, market: str,
                     channels_override: list[str] | None = None) -> dict:
        """Send outreach via all configured channels for an ICP type.

        Args:
            csv_path: Path to Clay-enriched CSV.
            icp_type: ICP type for template/channel selection.
            market: Market key for from-number selection and CRM.
            channels_override: Override ICP's default channels.

        Returns dict with per-channel results and CRM campaign ID.
        """
        log.info(f"=== Outreach: {icp_type} in {market} ===")
        log.info(f"Source CSV: {csv_path}")

        if not Path(csv_path).exists():
            log.error(f"CSV not found: {csv_path}")
            return {"status": "error", "reason": "csv_not_found"}

        icp = self._get_icp(icp_type)
        channels = channels_override or icp.get("outreach_channels", [])
        log.info(f"Channels: {', '.join(channels)}")

        # CRM: create campaign + import leads
        campaign_id = None
        if self._ensure_crm():
            try:
                campaign_id = self.crm.create_campaign({
                    "name": f"{icp_type}_{market}_{datetime.now():%Y%m%d}",
                    "channel": ", ".join(channels),
                    "icp_type": icp_type,
                    "market": market,
                    "status": "active",
                })
                log.info(f"CRM campaign: {campaign_id}")

                import_result = self.crm.import_leads_from_csv(
                    csv_path, "clay", icp_type, market
                )
                log.info(f"CRM import: {import_result}")
            except Exception as exc:
                log.error(f"CRM error: {exc}")

        # Send via each channel
        results = {"status": "success", "campaign_id": campaign_id, "channels": {}}
        total_sent = 0

        for channel in channels:
            try:
                if channel == "email":
                    ch_result = self._send_email(csv_path, icp_type)
                elif channel == "sms":
                    ch_result = self._send_sms(csv_path, icp_type)
                elif channel == "ai_call":
                    ch_result = self._send_voice(csv_path, icp_type, market)
                else:
                    log.warning(f"Unknown channel: {channel}")
                    continue

                results["channels"][channel] = ch_result
                total_sent += ch_result.get("sent", ch_result.get("leads_added", 0))
                log.info(f"  {channel}: {ch_result}")

            except Exception as exc:
                log.error(f"  {channel} error: {exc}")
                results["channels"][channel] = {"status": "error", "reason": str(exc)}

        # Update CRM campaign stats
        if campaign_id and self._crm_connected:
            try:
                self.crm.update_campaign_stats(campaign_id, {
                    "sent": str(total_sent),
                    "status": "active",
                })
            except Exception as exc:
                log.error(f"CRM stats update error: {exc}")

        return results

    def _send_email(self, csv_path: str, icp_type: str) -> dict:
        """Send email outreach via Instantly.ai."""
        icp = self._get_icp(icp_type)
        template_key = icp.get("email_campaign", "")
        template_file = EMAIL_TEMPLATE_MAP.get(template_key, f"{template_key}.json")
        template_path = str(
            PROJECT_ROOT / "outreach" / "email" / "templates" / template_file
        )

        if self.dry_run:
            out_dir = str(DATA_DIR / "instantly_ready")
            out_path = InstantlyClient.export_for_manual_upload(
                csv_path, template_key, out_dir
            )
            log.info(f"  [DRY RUN] Email exported: {out_path}")
            return {"mode": "export", "exported_csv": str(out_path)}

        client = InstantlyClient()
        campaign_id = client.create_campaign(template_path, SENDING_ACCOUNT)
        leads_added = client.add_leads_to_campaign(campaign_id, csv_path)
        return {"mode": "api", "campaign_id": campaign_id, "leads_added": leads_added}

    def _send_sms(self, csv_path: str, icp_type: str) -> dict:
        """Send SMS outreach via Twilio."""
        template_name = SMS_TEMPLATE_MAP.get(icp_type)
        if not template_name:
            log.info(f"  No SMS template for {icp_type}, skipping")
            return {"skipped": True, "reason": "no_template"}

        if self.dry_run:
            df = pd.read_csv(csv_path)
            log.info(f"  [DRY RUN] Would send SMS to {len(df)} leads, "
                     f"template={template_name}")
            return {"mode": "dry_run", "would_send": len(df), "template": template_name}

        sender = TwilioSender()
        return sender.send_campaign(csv_path, template_name)

    def _send_voice(self, csv_path: str, icp_type: str, market: str) -> dict:
        """Send voice outreach via Retell AI."""
        config = RetellConfig()
        try:
            script_name = config.get_script_for_icp(icp_type)
        except ValueError:
            log.info(f"  No voice script for {icp_type}, skipping")
            return {"skipped": True, "reason": "no_script"}

        leads = load_leads_csv(csv_path)
        if not leads:
            return {"skipped": True, "reason": "no_leads_with_phone"}

        client = RetellClient(dry_run=self.dry_run)
        return client.run_campaign(
            script_name=script_name,
            leads=leads,
            market=market,
            max_concurrent=1,
            delay_between=30,
        )

    # ------------------------------------------------------------------
    # Storm campaigns (reactive)
    # ------------------------------------------------------------------

    def run_storm_campaign(self, market: str, event: dict | None = None) -> dict:
        """Check weather and run storm damage scrape campaign.

        If event is None, checks live weather first. If severe weather found
        (or event provided), scrapes recent homeowners and outputs clay-ready CSV.

        Returns dict with alert info and scrape results.
        """
        log.info(f"=== Storm campaign: {market} ===")
        market_cfg = self.markets[market]

        # Step 1: Get or check for storm event
        if event is None:
            api_key = os.getenv("OPENWEATHER_API_KEY")
            if not api_key:
                log.error("OPENWEATHER_API_KEY not set")
                return {"status": "error", "reason": "missing_api_key"}

            event = weather_monitor.check_market(market, market_cfg, api_key, 50.0)
            if event is None:
                log.info(f"No severe weather in {market} -- all clear")
                return {"status": "clear", "market": market, "alert": None}

            weather_monitor.save_alert(event)

        log.info(f"Storm alert: {event.get('severity', 'unknown')} in {market}")
        weather_monitor.print_alert(event)

        # Step 2: Scrape recent homeowners (short lookback for urgency)
        log.info(f"Scraping recent homeowners in {market} (7-day lookback)...")
        df = homeowner_scraper.scrape_market(market, market_cfg, days=7)

        if df.empty:
            log.warning(f"No recent homes found in {market}")
            return {"status": "alert_only", "market": market, "alert": event, "rows": 0}

        raw_path = homeowner_scraper.save(df, market, RAW_DIR)

        # Step 3: Format for Clay as storm_damage ICP
        icp_config = self.icp_defs
        channels = clay_formatter.get_outreach_channels("storm_damage", icp_config)
        formatted = clay_formatter.format_homeowner(df, "storm_damage", channels)

        CLAY_READY_DIR.mkdir(parents=True, exist_ok=True)
        date_str = datetime.now().strftime("%Y%m%d")
        csv_path = CLAY_READY_DIR / f"storm_damage_{market}_{date_str}.csv"
        formatted.to_csv(csv_path, index=False)

        instructions = clay_formatter.generate_instructions("storm_damage", icp_config)
        md_path = CLAY_READY_DIR / "clay_instructions_storm_damage.md"
        md_path.write_text(instructions)

        log.info(f"Clay-ready: {csv_path} ({len(formatted)} rows)")
        log.info("")
        log.info("NEXT STEPS (URGENT -- storm damage is time-sensitive):")
        log.info("  1. Enrich in Clay immediately")
        log.info("  2. Run: python -m orchestrator.campaign_runner outreach "
                 f"--csv <enriched.csv> --icp-type storm_damage --market {market}")

        return {
            "status": "success",
            "market": market,
            "alert": event,
            "rows": len(formatted),
            "clay_csv": str(csv_path),
        }

    def check_and_run_storms(self) -> list[dict]:
        """Check all markets for severe weather and trigger storm campaigns."""
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            log.error("OPENWEATHER_API_KEY not set, cannot check storms")
            return []

        alerts = weather_monitor.check_all(self.markets, api_key, 50.0)
        results = []

        for alert in alerts:
            weather_monitor.print_alert(alert)
            weather_monitor.save_alert(alert)
            market_key = alert.get("market", "")
            try:
                result = self.run_storm_campaign(market_key, event=alert)
                results.append(result)
            except Exception as exc:
                log.error(f"Storm campaign error for {market_key}: {exc}")
                results.append({"status": "error", "market": market_key, "reason": str(exc)})

        if not alerts:
            log.info("All clear -- no severe weather in any market")

        return results

    # ------------------------------------------------------------------
    # Scheduling
    # ------------------------------------------------------------------

    def schedule_campaigns(self) -> None:
        """Set up recurring campaign schedules and enter the run loop.

        Schedule:
            Homeowner scrape:  Monday 06:00 (weekly, all markets)
            Storm check:       Every 6 hours
            Status report:     Daily 20:00
        """
        log.info("Starting campaign scheduler")
        log.info(f"  Dry run: {self.dry_run}")

        schedule_lib.every().monday.at("06:00").do(self._job_homeowner_scrape)
        log.info("  Scheduled: Homeowner scrape -- Monday 06:00")

        schedule_lib.every(6).hours.do(self._job_storm_check)
        log.info("  Scheduled: Storm check -- every 6 hours")

        schedule_lib.every().day.at("20:00").do(self._job_status_report)
        log.info("  Scheduled: Status report -- daily 20:00")

        # Run storm check immediately on startup
        self._job_storm_check()

        log.info("\nScheduler running (Ctrl+C to stop)")
        try:
            while True:
                schedule_lib.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            log.info("\nScheduler stopped.")

    def _job_homeowner_scrape(self) -> None:
        log.info(f"\n{'=' * 60}")
        log.info(f"Scheduled homeowner scrape: {datetime.now():%Y-%m-%d %H:%M}")
        log.info(f"{'=' * 60}")
        for market_key in self.markets:
            try:
                result = self.run_homeowner_campaign(market_key, days=14)
                log.info(f"  {market_key}: {result.get('rows', 0)} rows")
            except Exception as exc:
                log.error(f"  {market_key}: ERROR -- {exc}")

    def _job_storm_check(self) -> None:
        log.info(f"\n{'=' * 60}")
        log.info(f"Storm check: {datetime.now():%Y-%m-%d %H:%M}")
        log.info(f"{'=' * 60}")
        try:
            results = self.check_and_run_storms()
            if results:
                log.info(f"  {len(results)} storm campaign(s) triggered")
        except Exception as exc:
            log.error(f"  Storm check error: {exc}")

    def _job_status_report(self) -> None:
        log.info(f"\n{'=' * 60}")
        log.info(f"Status report: {datetime.now():%Y-%m-%d %H:%M}")
        log.info(f"{'=' * 60}")
        try:
            status = self.get_status()
            _print_status(status)
        except Exception as exc:
            log.error(f"  Status report error: {exc}")

    # ------------------------------------------------------------------
    # Status / dashboard
    # ------------------------------------------------------------------

    def get_status(self) -> dict:
        """Get pipeline status from CRM dashboard."""
        if not self._ensure_crm():
            log.warning("Cannot connect to CRM -- returning empty status")
            return {}
        return self.crm.get_dashboard_summary()


# ===================================================================
# CLI
# ===================================================================

def _print_status(status: dict) -> None:
    """Pretty-print status dict to console."""
    if not status:
        print("No status data available.")
        return
    for key, value in status.items():
        if isinstance(value, dict):
            print(f"\n{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Goldman's Lead Gen Campaign Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape homeowners (Phase 1 -- outputs clay-ready CSV)
  python -m orchestrator.campaign_runner homeowner --market oakland_county_mi
  python -m orchestrator.campaign_runner homeowner --market all --days 30

  # Scrape referral partners (Phase 1)
  python -m orchestrator.campaign_runner referral --market triangle_nc --icp-type real_estate_agents

  # Run outreach on enriched data (Phase 2)
  python -m orchestrator.campaign_runner outreach --csv data/clay_enriched/agents.csv --icp-type real_estate_agents --market oakland_county_mi

  # Storm campaign (check weather + scrape)
  python -m orchestrator.campaign_runner storm --market oakland_county_mi

  # Run scheduled campaigns (blocking loop)
  python -m orchestrator.campaign_runner schedule

  # Show status
  python -m orchestrator.campaign_runner status
        """,
    )

    parser.add_argument(
        "--dry-run", action="store_true",
        help="Log actions without calling external APIs",
    )

    sub = parser.add_subparsers(dest="command", help="Campaign commands")

    # --- homeowner ---
    p = sub.add_parser("homeowner",
                       help="Scrape recently sold homes -> clay-ready CSVs")
    p.add_argument("--market", required=True,
                   help='Market key (oakland_county_mi, etc.) or "all"')
    p.add_argument("--days", type=int, default=14,
                   help="Days back to search (default: 14)")

    # --- referral ---
    p = sub.add_parser("referral",
                       help="Scrape referral partner businesses -> clay-ready CSVs")
    p.add_argument("--market", required=True,
                   help='Market key or "all"')
    p.add_argument("--icp-type", required=True,
                   help='ICP type (real_estate_agents, etc.) or "all"')

    # --- outreach ---
    p = sub.add_parser("outreach",
                       help="Run multi-channel outreach on enriched CSV")
    p.add_argument("--csv", required=True,
                   help="Path to Clay-enriched CSV file")
    p.add_argument("--icp-type", required=True,
                   help="ICP type for template/channel selection")
    p.add_argument("--market", required=True,
                   help="Market for from-number selection and CRM tagging")
    p.add_argument("--channels", default=None,
                   help="Override channels (comma-separated: email,sms,ai_call)")

    # --- enrich ---
    p = sub.add_parser("enrich",
                       help="Enrich a raw CSV via Apollo.io (standalone)")
    p.add_argument("--input", required=True,
                   help="Path to raw CSV from gmaps_scraper")
    p.add_argument("--icp-type", required=True,
                   help="ICP type for decision-maker title matching")
    p.add_argument("--output-dir", default=None,
                   help="Output directory (default: data/enriched/)")

    # --- storm ---
    p = sub.add_parser("storm",
                       help="Check weather and run storm damage campaign")
    p.add_argument("--market", required=True,
                   help='Market key or "all"')
    p.add_argument("--test", action="store_true",
                   help="Simulate storm alert without weather API call")

    # --- storm-monitor ---
    sub.add_parser("storm-monitor",
                   help="Continuous storm monitoring (checks every 6 hours)")

    # --- schedule ---
    sub.add_parser("schedule",
                   help="Start the recurring campaign scheduler (blocking)")

    # --- status ---
    sub.add_parser("status", help="Show pipeline status from CRM")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    runner = CampaignRunner(dry_run=args.dry_run)

    if args.command == "homeowner":
        market_keys = runner._resolve_markets(args.market)
        for mk in market_keys:
            try:
                result = runner.run_homeowner_campaign(mk, days=args.days)
                for icp, info in result.get("icps", {}).items():
                    print(f"  {icp}: {info['rows']} rows -> {info['clay_csv']}")
            except Exception as exc:
                log.error(f"{mk}: {exc}")

    elif args.command == "referral":
        queries = gmaps_scraper.load_queries()
        icp_targets = (
            list(queries.keys()) if args.icp_type == "all"
            else [args.icp_type]
        )
        market_keys = runner._resolve_markets(args.market)

        for icp_type in icp_targets:
            for mk in market_keys:
                try:
                    result = runner.run_referral_campaign(mk, icp_type)
                    print(f"  {icp_type}/{mk}: {result.get('rows', 0)} rows")
                except Exception as exc:
                    log.error(f"{icp_type}/{mk}: {exc}")

    elif args.command == "enrich":
        input_path = Path(args.input)
        if not input_path.exists():
            log.error(f"File not found: {input_path}")
            sys.exit(1)
        df = pd.read_csv(input_path)
        print(f"Loaded {len(df)} rows from {input_path}")
        if args.dry_run:
            has_web = (df.get("website", pd.Series(dtype=str)).fillna("").str.len() > 0).sum()
            print(f"Would enrich {len(df)} businesses ({has_web} with websites)")
            print(f"Estimated: {len(df)} email credits, ~{len(df)*2//60} min")
        else:
            client = ApolloClient()
            df = enrich_businesses(df, args.icp_type, client)
            out_dir = Path(args.output_dir) if args.output_dir else ENRICHED_DIR
            path = save_enriched(df, args.icp_type, out_dir)
            print_enrichment_summary(df, args.icp_type)
            print(f"\nSaved to {path}")

    elif args.command == "outreach":
        channels_override = (
            [c.strip() for c in args.channels.split(",")]
            if args.channels else None
        )
        result = runner.run_outreach(
            args.csv, args.icp_type, args.market,
            channels_override=channels_override,
        )
        print(f"\nOutreach complete: campaign_id={result.get('campaign_id')}")
        for ch, info in result.get("channels", {}).items():
            print(f"  {ch}: {info}")

    elif args.command == "storm":
        market_keys = runner._resolve_markets(args.market)
        for mk in market_keys:
            if args.test:
                event = weather_monitor.build_simulated_alert(
                    mk, runner.markets[mk]
                )
            else:
                event = None
            try:
                result = runner.run_storm_campaign(mk, event=event)
                status = result.get("status", "")
                if status == "clear":
                    print(f"  {mk}: No severe weather")
                else:
                    print(f"  {mk}: {result.get('rows', 0)} rows scraped "
                          f"(alert: {result.get('alert', {}).get('severity', 'N/A')})")
            except Exception as exc:
                log.error(f"{mk}: {exc}")

    elif args.command == "storm-monitor":
        log.info("Starting storm monitor (checking every 6 hours)...")
        runner.check_and_run_storms()
        schedule_lib.every(6).hours.do(runner.check_and_run_storms)
        try:
            while True:
                schedule_lib.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            log.info("\nStorm monitor stopped.")

    elif args.command == "schedule":
        runner.schedule_campaigns()

    elif args.command == "status":
        status = runner.get_status()
        _print_status(status)


if __name__ == "__main__":
    main()
