# CLAUDE.md

## Project Overview

Newport Wholesalers is a 30-year American-owned grocery wholesaler based in Plantation, FL. Still Mind Creative LLC is building a two-channel growth strategy: (1) Government contracting — entering federal/state/local food procurement, and (2) Commercial SDR — AI-powered outbound prospecting for their core wholesale business. This repo contains the intelligence system, client deliverables, and operational tooling for both channels.

Newport's competitive advantage: 30 years of continuous Florida operations, real warehouse/fleet infrastructure, W-2 American workforce, clean audit history. In the current post-DOGE/fraud-crackdown environment, agencies actively need vendors with auditable, transparent histories. Newport is the exact type of company these agencies need — a competitive moat that took decades to build and can't be manufactured.

## Tech Stack

- **Core Language**: Python 3.10+
- **Presentation Generation**: pptxgenjs (Node.js) for PowerPoint
- **Financial Model Generation**: openpyxl (Python) for Excel
- **Data Storage**: Flat CSV files + JSON configs (no database)
- **Pipeline Tracking**: Google Sheets API v4 (gspread)
- **Notifications**: Slack webhooks + Resend email
- **Scheduling**: GitHub Actions (daily SAM.gov monitor, 6 AM ET)
- **Contact Enrichment**: Apollo.io API v1
- **Federal Data**: SAM.gov, USASpending, FPDS, Grants.gov (all free APIs)

## Key Commands

```bash
# GovCon Intelligence
python govcon/scrapers/daily_monitor.py --dry-run           # Test daily monitor
python govcon/scrapers/daily_monitor.py --score --push-to-sheet --max-pages 3  # Live run
python govcon/scrapers/contract_scanner.py                   # Full market scan (10 reports)
python govcon/deliverables/collect_market_data.py            # Generate market_data.json

# GovCon Deliverables
python govcon/deliverables/financials/build_proforma.py      # Generate Excel model (v4-era, needs update)
cd govcon/deliverables/presentation && node build_presentation.js  # Generate deck (v4-era, needs rebuild)

# Commercial Prospecting
python commercial/scrapers/apollo_prospector.py --segment A --max-pages 5  # Prospect by segment
python commercial/enrichment/enricher.py --input data/raw/segment_a.csv    # Enrich contacts

# Bid Scoring
python govcon/scoring/bid_no_bid.py --input data/final/opportunities.csv   # Score opportunities
```

## Project Structure

```
govcon/          # Channel 1: Government contracting (enrichment, scrapers, scoring, tracking, deliverables)
commercial/      # Channel 2: Commercial SDR (enrichment, scrapers, outreach [future])
config/          # Shared: ICP definitions, exclusions, government contract params
specs/           # Blueprint specifications (this project's documentation)
data/            # Runtime data — gitignored (raw/, enriched/, final/, cache/, contacts/)
assets/          # Brand assets (backgrounds, logos)
archive/         # Superseded files kept for reference
.github/         # GitHub Actions workflows
.claude/         # Claude CLI commands
```

## Coding Conventions

- **Path resolution**: `_project_root = Path(__file__).resolve().parent.parent.parent` — all scripts use this to find repo root
- **Config loading**: `_project_root / "config" / "filename.json"` — config is always at repo root level
- **Data output**: `data/final/{prefix}_{report}_{YYYYMMDD_HHMM}.csv` — timestamped filenames
- **API clients**: Follow `/govcon/enrichment/` pattern — `__init__` with env key, `requests.Session`, `_request()` with 429 retry + exponential backoff, `stats` property
- **CLI scripts**: argparse, `--dry-run` mode, `load_config()`, `save_results()`
- **Modules**: `__init__.py` in every directory with explicit imports
- **Data flow**: `collect_market_data.py` → `market_data.json` → consumed by `build_proforma.py` + `build_presentation.js`

## Spec Files

Reference these for detailed context:
- `/specs/01-VISION.md` — Strategic "why": Newport's story, two channels, success criteria
- `/specs/02-REQUIREMENTS.md` — Every deliverable spec'd with acceptance criteria (FR-001 through FR-017)
- `/specs/03-ARCHITECTURE.md` — System design, data flows, key decisions
- `/specs/04-USER-STORIES.md` — Detailed workflows: proposal delivery, daily monitoring, bid prep, ABM outreach
- `/specs/05-DEVELOPMENT-PLAN.md` — Phased build plan (Phase 0–6) with completion criteria
- `/specs/06-REPO-STRUCTURE.md` — Exact file tree with purpose for every file
- `/specs/09-INTEGRATIONS.md` — All external services: free APIs, paid platforms, future integrations
- `/specs/GLOSSARY.md` — 40+ terms: government procurement, wholesale distribution, project-specific vocabulary

## Guardrails

**NEVER do without asking:**
- Commit API keys or credentials to the repo
- Modify `config/government_contracts.json` scoring weights without explaining the change
- Hardcode Newport's proprietary business data (revenue, exact margins) — these are always input variables
- Change the daily monitor schedule in `.github/workflows/daily-scan.yml`
- Delete anything in `archive/` — it's there for reference even if superseded
- Make financial projections more aggressive without citing the data source that supports the change

**ALWAYS do:**
- Use `--dry-run` when testing scrapers
- Cite data sources (API name + date) when generating market analysis content
- Follow the existing API client pattern when adding new integrations
- Timestamp output files: `{prefix}_{report}_{YYYYMMDD_HHMM}.csv`
- Mark confidence levels on market estimates: HIGH (live API data), MEDIUM (extrapolated), LOW (industry estimates)
- Keep deliverable tone professional and grounded — never hard-sell, never overpromise

**Known gotchas:**
- SAM.gov API has intermittent outages (experienced Feb 2026). System degrades gracefully — check logs.
- `build_proforma.py` generates v4-era 4-sheet output. The v7 model (5 sheets: Inputs, Two Routes, 5-Year Model, Market Analysis, Key Questions) was built in Claude Desktop and is the canonical deliverable. The script needs updating to match.
- `build_presentation.js` also generates v4-era narrative. Needs rebuild per Phase 2 of the development plan.
- Google Sheets API requires a service account JSON file at the path specified in `GOOGLE_SHEETS_CREDS_PATH`. The spreadsheet must be shared with the service account email.
- Apollo.io free tier has unlimited search but limited reveal credits. Budget reveals per segment.

## Current Phase

**Phase 0: Spec Finalization & Repo Cleanup** — IN PROGRESS
- [x] Blueprint specs created (VISION, REQUIREMENTS, ARCHITECTURE, USER-STORIES, DEVELOPMENT-PLAN, REPO-STRUCTURE, INTEGRATIONS, GLOSSARY)
- [x] CLAUDE.md updated
- [ ] .claude/commands/ created
- [ ] Verify all existing scripts run without errors
- [ ] Confirm market_data.json generation

**Next**: Phase 1 (GovCon Excel Model Validation) → Phase 2 (GovCon Deck Rebuild) → Phase 3 (Commercial Financial Model) → Phase 4 (Commercial Deck)

See `/specs/05-DEVELOPMENT-PLAN.md` for full phase details and completion criteria.
