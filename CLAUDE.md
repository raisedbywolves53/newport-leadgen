# CLAUDE.md

## Project Overview

Newport Wholesalers is a 35-year American-owned grocery wholesaler based in Plantation, FL (founded 1991). Still Mind Creative LLC is building a two-channel growth strategy: (1) Government contracting — entering federal/state/local food procurement, and (2) Commercial SDR — AI-powered outbound prospecting for their core wholesale business. This repo contains the intelligence system, client deliverables, and operational tooling for both channels.

Newport's competitive advantage: 35 years of continuous Florida operations, real warehouse/fleet infrastructure, W-2 American workforce, clean audit history. In the current post-DOGE/fraud-crackdown environment, agencies actively need vendors with auditable, transparent histories. Newport is the exact type of company these agencies need — a competitive moat that took decades to build and can't be manufactured.

## Tech Stack

- **Core Language**: Python 3.10+
- **Web Presentation**: React 19.2 + Vite 7.3 + Tailwind CSS 4.2 (primary client deliverable)
- **Data Visualization**: ECharts 6.0 (charts) + Motion 12 (animations)
- **Data Storage**: Flat CSV files + JSON configs (no database)
- **Pipeline Tracking**: Google Sheets API v4 (gspread)
- **Notifications**: Slack webhooks + Resend email
- **Scheduling**: GitHub Actions (daily SAM.gov monitor, 6 AM ET)
- **Contact Enrichment**: Apollo.io API v1
- **Federal Data**: SAM.gov, USASpending, FPDS, Grants.gov (all free APIs)

## Key Commands

```bash
# Web Presentation (primary deliverable)
cd web && npm run dev                                        # Dev server at localhost:5173
cd web && npm run build                                      # Production build → web/dist/

# GovCon Intelligence
python govcon/scrapers/daily_monitor.py --dry-run           # Test daily monitor
python govcon/scrapers/daily_monitor.py --score --push-to-sheet --max-pages 3  # Live run
python govcon/scrapers/contract_scanner.py                   # Full market scan (10 reports)
python govcon/deliverables/collect_market_data.py            # Generate market_data.json

# Commercial Prospecting
python commercial/scrapers/apollo_prospector.py --segment A --max-pages 5  # Prospect by segment
python commercial/enrichment/enricher.py --input data/raw/segment_a.csv    # Enrich contacts

# Bid Scoring
python govcon/scoring/bid_no_bid.py --input data/final/opportunities.csv   # Score opportunities
```

## Project Structure

```
web/             # Primary client deliverable: React/Vite interactive GovCon presentation (17 slides, 1 financial slide planned)
govcon/          # Channel 1: Government contracting (enrichment, scrapers, scoring, tracking, deliverables)
commercial/      # Channel 2: Commercial SDR (enrichment, scrapers, outreach [future])
config/          # Shared: ICP definitions, exclusions, government contract params
specs/           # Blueprint specifications (this project's documentation)
data/            # Runtime data — gitignored (raw/, enriched/, final/, cache/, contacts/)
assets/          # Brand assets (backgrounds, logos)
archive/         # Superseded files: legacy PPTX builders, openpyxl scripts, v7 Excel model, old docs
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
- **Data flow**: `collect_market_data.py` → `market_data.json` → `web/src/data/*.js` → React slide components

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
- The GovCon web presentation (`web/`) is the primary client deliverable. 17 interactive slides (1 financial slide planned), React 19.2 + Vite 7.3 + Tailwind CSS 4.2 + ECharts 6 + Motion 12, deployed via Netlify. Design rules are in `web/DESIGN-SYSTEM.md` — read it before modifying any slide.
- Market data in `web/src/data/market.js`, strategy data in `web/src/data/strategy.js`. Financial computation engine planned for `web/src/data/financials.js` (see `FINANCIAL-SLIDES-BUILD.md` for full build spec).
- Legacy PPTX and Excel builders are archived in `archive/` subdirectories. The v7 .xlsx (`data/Newport_GovCon_Financial_Model_v7.xlsx`) remains as reference but financial slides are being rebuilt from scratch using research data.
- Slide design system: zinc palette + brand accents (Gold #C9A84C, Teal #1B7A8A, Light Teal #239BAD, Orange #E8913A). Card pattern: `rounded-xl bg-white border border-zinc-200 shadow-sm`. Always use `pb-14` for progress bar clearance.
- Google Sheets API requires a service account JSON file at the path specified in `GOOGLE_SHEETS_CREDS_PATH`. The spreadsheet must be shared with the service account email.
- Apollo.io free tier has unlimited search but limited reveal credits. Budget reveals per segment.

## Current Phase

**Phase 0: Spec Finalization & Repo Cleanup** — COMPLETE
- [x] Blueprint specs created (VISION, REQUIREMENTS, ARCHITECTURE, USER-STORIES, DEVELOPMENT-PLAN, REPO-STRUCTURE, INTEGRATIONS, GLOSSARY)
- [x] CLAUDE.md updated
- [x] .claude/commands/ created
- [x] Verify all existing scripts run without errors
- [x] Confirm market_data.json generation

**Phase 1: GovCon Excel Model Validation** — COMPLETE
- [x] V7 .xlsx validated: 5 sheets, 176 formulas, zero errors, 7 charts
- [x] FR-003 met: five tiers, bid volumes, win rates, renewals at 70%, owner earnings, portfolio shift
- [x] FR-008 met: 5 sheets, color coding, formula-driven, charts, zero formula errors
- [x] Win rates cross-checked against research: Yr1 micro 15% matches FR-003; conservative vs research's 35-45% but defensible for zero past performance
- [x] Market data validated: $7.17B national TAM, $85M FL, 117 FL contracts / $6.4M, 537 FPDS awards / 32 combos, 93% sole source NAICS 424490 @ DoD
- [x] WIP build_proforma.py v7 rewrite restored from stash (~95% complete, runs successfully, deferred to Phase 5)
- [x] Decision: v7 .xlsx accepted as canonical model (Option A from dev plan)

**Phase 2: GovCon Deck Rebuild** — COMPLETE (PPTX ARCHIVED → superseded by web app)
- [x] Full rewrite of build_presentation.js: 17 slides → 18 slides, v7 narrative arc
- [x] All slides implemented with v7 data and narrative
- [x] PPTX builder and output archived to `archive/govcon-presentation-pptx/`

**Phase 2.5: GovCon Web Presentation** — COMPLETE (17 slides live, 2 financial slides in progress)
- [x] React 19.2 + Vite 7.3 + Tailwind CSS 4.2 + ECharts 6.0 + Motion 12
- [x] 17 interactive slides across 4 sections (null/title, opportunity, strategy, execution)
- [x] Design system: editorial tone, gold + teal accents, card-based layouts, zinc palette
- [x] Market data from `web/src/data/market.js`, strategy from `strategy.js`
- [x] Password-gated, Netlify-deployed
- [x] This is now the primary client-facing deliverable
- [x] Multiple rounds of visual polish (font sizing, spacing, progress bar clearance)
- [ ] **IN PROGRESS**: 1 interactive financial slide (Slide 18: Financial Outlook)
  - Strategic brief: `FINANCIAL-SLIDES-PROMPT.md` — business context, Goldman Sachs IB framing, model logic
  - Technical spec: `FINANCIAL-SLIDES-BUILD.md` — component architecture, data model, verification checklist
  - Two-axis model: Route (Free $0/yr vs Paid $13K/yr) × Scenario (Conservative/Moderate/Aggressive)
  - `computeProForma(routeKey, scenarioKey, overrides)` — pure computation engine
  - Still Mind handles all BD/bidding/admin; Newport only handles relationship mgmt + delivery
  - Still Mind consulting fee intentionally excluded from model (separate conversation)
  - Management input sliders: Gross Margin, Delivery Cost %, Admin Overhead
  - Portfolio evolution: Y1 micro-purchases → Y2 simplified → Y3-5 SLED/sealed bid + renewal flywheel
  - Chart tooltips must show tier breakdown math (bids × win rate = wins, per-tier revenue)
  - Research data sources: `govcon/docs/research.md`, `govcon/docs/strategy.md`, `govcon/docs/phases/PHASE-4-FINANCIALS.md`

**Phase 3: Commercial Financial Model** — COMPLETE (ARCHIVED)
- [x] `build_commercial_model.py`: 5 sheets, 3 scenarios, 3 charts — v1 complete
- [x] Script and output archived to `archive/commercial-financials-openpyxl/`
- [x] Commercial web slides are a future item (GovCon web presentation is the current priority)

**Phase 4: Commercial Deck + Reference Docs** — COMPLETE (PPTX ARCHIVED)
- [x] Commercial PPTX deck (12 slides) and financial model built and archived
- [x] Specs updated with post-fraud crisis data, competition density, procurement platforms
- [x] PPTX builder and output archived to `archive/commercial-presentation-pptx/`
- [x] Commercial web integration is a future item

**Next**: Complete financial slides (Slide 18 + 19), then Phase 5 (Operational Hardening)
- Fine-tune daily monitor scoring weights
- Prepare bid template library
- Set up direct portal monitoring for top FL school districts
- Build Notion pipeline tracker
- FPDS migration (ezSearch decommissioned Feb 24, 2026)
- Platform registrations (Unison Marketplace, BidNet, DemandStar, VendorLink)

See `/specs/05-DEVELOPMENT-PLAN.md` for full phase details and completion criteria.
