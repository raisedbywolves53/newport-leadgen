# Newport Wholesalers — Repository Structure

> **Last Updated**: February 23, 2026
> **Status**: Draft
> **Depends On**: [03-ARCHITECTURE.md](./03-ARCHITECTURE.md)

## Overview

The `newport-leadgen` monorepo contains the complete intelligence system for both channels (GovCon + Commercial SDR), the interactive web presentation (primary client deliverable), research documentation, and operational tooling. Top-level directories separate concerns by channel, with shared configuration at the root. Legacy PPTX and Excel builders are archived.

---

## Directory Tree

```
newport-leadgen/
│
├── CLAUDE.md                              # Claude CLI project context (MOST IMPORTANT FILE)
├── requirements.txt                       # Python dependencies
├── .gitignore                             # Excludes data/, .env, node_modules/
├── .env.example                           # Environment variable template (NEVER actual values)
│
├── web/                                   # PRIMARY CLIENT DELIVERABLE: GovCon Web Presentation
│   ├── package.json                       # React 19, Vite 7, ECharts 6, Motion 12, Tailwind 4
│   ├── vite.config.js                     # Vite build configuration
│   ├── netlify.toml                       # Netlify deployment config
│   ├── index.html                         # HTML template
│   ├── DESIGN-SYSTEM.md                   # Core design rules (THE BIBLE for slide design)
│   ├── src/
│   │   ├── App.jsx                        # Root component
│   │   ├── main.jsx                       # Entry point
│   │   ├── index.css                      # Tailwind + custom styles
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Navigation.jsx         # Slide navigation bar
│   │   │   │   ├── PasswordGate.jsx       # Authentication wrapper
│   │   │   │   └── SlideContainer.jsx     # Slide wrapper/viewport
│   │   │   ├── slides/                    # 20 individual slide components
│   │   │   │   ├── TitleSlide.jsx
│   │   │   │   ├── ExecutiveSummarySlide.jsx
│   │   │   │   ├── WhyNewportSlide.jsx
│   │   │   │   ├── FloridaTamSlide.jsx
│   │   │   │   ├── ProductMatrixSlide.jsx
│   │   │   │   ├── ConfectioneryGapSlide.jsx
│   │   │   │   ├── TargetAgenciesSlide.jsx
│   │   │   │   ├── CompetitionSlide.jsx
│   │   │   │   ├── B2bFastTrackSlide.jsx
│   │   │   │   ├── HowItWorksSlide.jsx
│   │   │   │   ├── ContractExamplesSlide.jsx
│   │   │   │   ├── PortfolioEvolutionSlide.jsx
│   │   │   │   ├── BdStrategySlide.jsx
│   │   │   │   ├── RiskComplianceSlide.jsx
│   │   │   │   ├── RecommendationSlide.jsx
│   │   │   │   ├── KeyQuestionsSlide.jsx
│   │   │   │   ├── BlueprintSlide.jsx
│   │   │   │   └── PlaceholderSlide.jsx
│   │   │   └── ui/                        # Reusable UI components
│   │   │       ├── DecorativeElements.jsx # GoldLine, CompassStar, HeroStat, BackgroundRing
│   │   │       ├── SectionDivider.jsx     # Divider slides (strategy, execution)
│   │   │       ├── SlideLayout.jsx        # Base layout wrapper
│   │   │       └── SourceCitation.jsx     # Bottom-of-slide citations
│   │   ├── data/
│   │   │   ├── slides.js                  # Slide registry (20 slides, 4 acts)
│   │   │   ├── market.js                  # Market data constants (TAM, agencies, competitors)
│   │   │   ├── strategy.js                # Strategy data (pipeline, contracts, compliance, questions)
│   │   │   └── financials.js              # Financial projections (from v7 Excel model)
│   │   └── hooks/
│   │       ├── useCountUp.js              # Animated number counter
│   │       └── useSlideNavigation.js      # Slide navigation logic
│   ├── public/                            # Static assets
│   │   ├── newport_background.jpg
│   │   └── animated_under_tree.png
│   └── dist/                              # Production build output
│
├── .github/
│   └── workflows/
│       └── daily-scan.yml                 # GitHub Actions: SAM.gov daily monitor at 6 AM ET
│
├── .claude/
│   └── commands/                          # Claude CLI reusable task prompts
│       ├── scaffold.md                    # Set up project from scratch
│       ├── new-feature.md                 # Spec-first feature implementation
│       ├── debug.md                       # Diagnose-before-fix debugging
│       ├── rebuild-deck.md                # Web presentation development guide
│       ├── rebuild-proforma.md            # Financial data update guide
│       └── run-scanner.md                 # Execute contract scanner with reports
│
├── config/                                # Shared configuration (both channels)
│   ├── icp_definitions.json               # 5 ICP segment definitions with Apollo search params
│   ├── exclusions.json                    # Company/title exclusion lists for enrichment
│   └── government_contracts.json          # NAICS codes, PSC codes, scoring parameters
│
├── specs/                                 # Blueprint specification files
│   ├── 01-VISION.md
│   ├── 02-REQUIREMENTS.md
│   ├── 03-ARCHITECTURE.md
│   ├── 04-USER-STORIES.md
│   ├── 05-DEVELOPMENT-PLAN.md
│   ├── 06-REPO-STRUCTURE.md              # This file
│   ├── 09-INTEGRATIONS.md
│   └── GLOSSARY.md
│
├── govcon/                                # Channel 1: Government Contracting
│   ├── __init__.py
│   │
│   ├── enrichment/                        # Federal data API clients
│   │   ├── __init__.py
│   │   ├── sam_client.py                  # SAM.gov Opportunities API v2
│   │   ├── sam_entity_client.py           # SAM.gov Entity (vendor registry) API
│   │   ├── usaspending_client.py          # USASpending.gov award data API
│   │   ├── fpds_client.py                 # FPDS competition density (ATOM feed)
│   │   └── grants_client.py              # Grants.gov opportunity API
│   │
│   ├── scrapers/                          # Data collection scripts
│   │   ├── __init__.py
│   │   ├── contract_scanner.py            # On-demand: 10 CSV reports across all APIs
│   │   └── daily_monitor.py               # Automated: daily SAM.gov opportunity scan
│   │
│   ├── scoring/                           # Bid evaluation
│   │   ├── __init__.py
│   │   ├── bid_scorer.py                  # Procedural bid scoring (legacy)
│   │   └── bid_no_bid.py                  # OOP bid scoring: 9 factors, weighted, thresholds
│   │
│   ├── tracking/                          # Pipeline management
│   │   ├── __init__.py
│   │   └── sheets_pipeline.py             # Google Sheets v2: 3 tabs, 12 stages
│   │
│   ├── notifications/                     # Alert delivery
│   │   ├── __init__.py
│   │   └── notify.py                      # Slack webhooks + Resend email
│   │
│   ├── templates/                         # Bid document templates
│   │   ├── generate_templates.py          # Template generation script
│   │   ├── capability_statement_template.docx
│   │   ├── sources_sought_response_template.docx
│   │   └── legitimacy_package_checklist.docx
│   │
│   ├── deliverables/                      # Data collection for web presentation
│   │   └── collect_market_data.py         # Aggregates API data → market_data.json
│   │
│   └── docs/                              # Research and strategy documentation
│       ├── strategy.md                    # Buyer universe, platforms, entry strategy (31K)
│       ├── research.md                    # TAM analysis, competition, live API validation (26K)
│       ├── requirements.md                # Command Center technical spec (37K)
│       └── phases/
│           ├── PHASE-2-OPERATIONAL-SYSTEM.md
│           ├── PHASE-3-PRESENTATION.md
│           └── PHASE-4-FINANCIALS.md
│
├── commercial/                            # Channel 2: Commercial SDR
│   ├── __init__.py
│   │
│   ├── enrichment/                        # Contact data enrichment
│   │   ├── __init__.py
│   │   ├── apollo_client.py               # Apollo.io API: search + reveal
│   │   ├── enricher.py                    # Bulk enrichment pipeline
│   │   └── re_enrich.py                   # Refresh previously enriched contacts
│   │
│   ├── scrapers/                          # Prospect sourcing
│   │   ├── __init__.py
│   │   └── apollo_prospector.py           # Enterprise people search by ICP segment
│   │
│   ├── outreach/                          # (FUTURE) Automated outreach
│   │   ├── __init__.py                    # Placeholder
│   │   ├── instantly_client.py            # (FUTURE) Email sequences via Instantly
│   │   ├── twilio_client.py              # (FUTURE) SMS via Twilio
│   │   ├── retell_client.py              # (FUTURE) AI voice via Retell AI
│   │   └── campaign_orchestrator.py       # (FUTURE) Multi-channel sequence manager
│   │
│   ├── deliverables/                      # (empty — scripts archived)
│   │
│   └── docs/                              # Market research
│       ├── icp_segments.md                # 5 segment definitions and rationale
│       ├── candy_wholesaler_research.md   # US + LATAM candy market (40K)
│       └── candy_latam_assessment.md      # Import viability, regulatory, Apollo coverage
│
├── assets/                                # Shared media assets
│   └── newport_background.jpg             # Brand asset for presentations
│
├── data/                                  # Runtime data (GITIGNORED)
│   ├── raw/                               # Direct API response dumps
│   ├── enriched/                          # Post-enrichment processed data
│   ├── final/                             # Timestamped CSV deliverables
│   ├── cache/                             # API response caching
│   ├── contacts/                          # FL decision makers, Apollo prospects
│   └── market_data.json                   # Aggregated market data for deliverables
│
└── archive/                               # Superseded files (kept for reference)
    ├── govcon-presentation-pptx/          # GovCon PPTX builder + output (build_presentation.js)
    ├── govcon-financials-openpyxl/        # GovCon Excel builder + v7 model (build_proforma.py, .xlsx)
    ├── commercial-presentation-pptx/      # Commercial PPTX builder + output
    ├── commercial-financials-openpyxl/    # Commercial Excel builder + output
    ├── dashboard/                         # Old dashboard generation scripts
    ├── pitchbook/                         # Early deck iterations
    ├── sheets_crm_v1.py                   # V1 Google Sheets integration
    └── old-docs/                          # Superseded documentation
```

---

## File Descriptions

### Root Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | The first file Claude CLI reads. Project overview, tech stack, conventions, guardrails, current phase. Updated as project progresses. |
| `requirements.txt` | Python dependencies. Key packages: `requests`, `pandas`, `gspread`, `google-auth`, `fpds`, `python-dotenv` |
| `.env.example` | Template for environment variables. Lists every required key with description and where to obtain it. Never contains actual values. |
| `.gitignore` | Excludes: `data/`, `.env`, `node_modules/`, `*.pyc`, `__pycache__/` |

### /config/ — Shared Configuration

| File | Purpose |
|------|---------|
| `icp_definitions.json` | Defines all 5 ICP segments with Apollo search parameters (employee count, revenue, industries, titles, geography). Used by both `apollo_prospector.py` and commercial enrichment. |
| `exclusions.json` | Companies and titles to exclude from enrichment (competitors, irrelevant roles). Shared across channels. |
| `government_contracts.json` | Newport's NAICS codes, PSC codes, target agencies, bid scoring weights, threshold values. Consumed by `contract_scanner.py`, `daily_monitor.py`, `bid_no_bid.py`. |

### /govcon/enrichment/ — Federal Data API Clients

| File | Purpose |
|------|---------|
| `sam_client.py` | SAM.gov Opportunities API v2. Queries active solicitations by NAICS, state, set-aside type. Handles pagination, 429 retry, response parsing. |
| `sam_entity_client.py` | SAM.gov Entity API. Vendor registry lookups for competitor research and Newport's own registration verification. |
| `usaspending_client.py` | USASpending.gov API. Award data for TAM sizing, competitor revenue analysis, contract examples. |
| `fpds_client.py` | FPDS ATOM feed parser. Competition density analysis across NAICS/agency combinations. Uses `fpds` library. |
| `grants_client.py` | Grants.gov API. Federal grant opportunity monitoring for food-related programs. |

### /govcon/scrapers/

| File | Purpose |
|------|---------|
| `contract_scanner.py` | On-demand comprehensive scan. Generates 10 CSV reports: opportunities by NAICS, by state, by set-aside, by agency, competition analysis, etc. Entry point for market research refreshes. |
| `daily_monitor.py` | Automated (GitHub Actions 6 AM ET). Queries SAM.gov, scores via `bid_no_bid.py`, deduplicates, pushes to Google Sheets, sends Slack/email alerts. |

### /govcon/scoring/

| File | Purpose |
|------|---------|
| `bid_scorer.py` | Legacy procedural scoring. Kept for reference. |
| `bid_no_bid.py` | Primary scoring engine. OOP, 9 weighted factors (NAICS 15%, Geography 15%, Size 10%, Competition 10%, Past Performance 15%, Evaluation 10%, Relationship 10%, Timeline 10%, Strategic 5%). Thresholds: 80=Strong Bid, 65=Bid, 50=Review, <50=No-Bid. |

### /govcon/deliverables/

| File | Purpose |
|------|---------|
| `collect_market_data.py` | Aggregates data from all API clients into `market_data.json`. This is the data source consumed by `web/src/data/*.js` for the web presentation. |

**Note:** The PPTX builder and Excel builder have been archived to `archive/govcon-presentation-pptx/` and `archive/govcon-financials-openpyxl/` respectively. The web app (`web/`) supersedes them.

### /commercial/enrichment/

| File | Purpose |
|------|---------|
| `apollo_client.py` | Apollo.io API wrapper. Free search (people/org) + paid reveal (1 credit per email). Session-based with retry logic. |
| `enricher.py` | Bulk enrichment pipeline. Takes raw prospect CSVs, reveals emails/phones for priority contacts, outputs enriched CSVs. |
| `re_enrich.py` | Refreshes previously enriched contacts. Useful when Apollo data updates or when previously unrevealed contacts become priority. |

### /commercial/scrapers/

| File | Purpose |
|------|---------|
| `apollo_prospector.py` | Enterprise people search by ICP segment. Reads segment definitions from `config/icp_definitions.json`, queries Apollo, deduplicates, filters by exclusions, outputs to `data/raw/`. |

---

## Configuration Files Detail

### .env.example

```bash
# === REQUIRED (GovCon) ===
SAM_API_KEY=                    # Free. Register at https://api.data.gov/signup/
SLACK_WEBHOOK_URL=              # Create at https://api.slack.com/messaging/webhooks

# === REQUIRED (Commercial) ===
APOLLO_API_KEY=                 # Free tier at https://app.apollo.io/

# === OPTIONAL (GovCon Notifications) ===
RESEND_API_KEY=                 # https://resend.com — email notifications
RESEND_TO_EMAIL=                # Recipient for email alerts

# === OPTIONAL (Pipeline Tracking) ===
GOOGLE_SHEETS_CREDS_PATH=       # Path to Google service account JSON
GOOGLE_SHEETS_ID=               # Spreadsheet ID from Google Sheets URL

# === FUTURE (Commercial Outreach) ===
INSTANTLY_API_KEY=              # https://instantly.ai
INSTANTLY_SENDING_ACCOUNT=     # Sending email account for campaigns
TWILIO_ACCOUNT_SID=            # https://twilio.com
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=           # Twilio phone for SMS
RETELL_API_KEY=                # https://retellai.com
```

---

## Files That Need to Be Created

These files are referenced in the specs but don't exist yet:

| File | Phase | Purpose |
|------|-------|---------|
| `/commercial/outreach/instantly_client.py` | Phase 6 | Instantly email integration |
| `/commercial/outreach/twilio_client.py` | Phase 6 | Twilio SMS integration |
| `/commercial/outreach/retell_client.py` | Phase 6 | Retell AI voice integration |
| `/commercial/outreach/campaign_orchestrator.py` | Phase 6 | Multi-channel sequence manager |

---

## Claude CLI Notes

When creating new files:
1. Follow the existing module pattern: `__init__.py` in every directory, imports in `__init__`
2. All scripts use `_project_root = Path(__file__).resolve().parent.parent.parent` for path resolution
3. Config loads from `_project_root / "config" / "filename.json"`
4. Data outputs go to `_project_root / "data" / "{raw|enriched|final}" / "filename.csv"`
5. Timestamped filenames: `{prefix}_{report}_{YYYYMMDD_HHMM}.csv`
6. Every new API client follows the pattern in `/govcon/enrichment/`: Session, `_request()` with retry, `stats` property
