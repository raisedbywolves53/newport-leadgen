# Newport Wholesalers — Architecture

> **Last Updated**: February 23, 2026
> **Status**: Draft
> **Depends On**: [01-VISION.md](./01-VISION.md), [02-REQUIREMENTS.md](./02-REQUIREMENTS.md)

## Overview

This document defines the technical architecture for the Newport engagement. Unlike a typical SaaS application, this system is a consulting intelligence platform with three layers: (1) data collection and analysis (Python), (2) client-facing deliverables (React/Vite interactive web presentation), and (3) operational automation (daily monitoring, pipeline tracking, outreach). All components live in a single monorepo organized by channel.

---

## Tech Stack

| Layer | Technology | Version | Why This Choice |
|-------|-----------|---------|-----------------|
| **Core Language** | Python | 3.10+ | All API clients, scrapers, scoring, data pipelines. Widely supported by Claude CLI. |
| **Web Presentation** | React 19 + Vite 7 | Latest | Interactive client-facing GovCon presentation. Primary deliverable. |
| **Styling** | Tailwind CSS 4 | Latest | Utility-first CSS framework for slide layouts. |
| **Data Visualization** | ECharts 6 | Latest | Charts and graphs in web slides. |
| **Animation** | Motion (Framer) 12 | Latest | Slide transitions and data animations. |
| **Data Storage** | CSV files + JSON configs | N/A | Flat files in `data/` directory. No database needed — this is a pipeline tool, not a web app. |
| **Pipeline Tracking** | Google Sheets API | v4 | Newport can view and interact with pipeline data in a familiar tool. `gspread` Python library. |
| **Notifications** | Slack webhooks + Resend email | N/A | Daily monitor alerts. Slack for real-time, email for formal notifications. |
| **Scheduling** | GitHub Actions | N/A | Daily SAM.gov monitor runs at 6 AM ET via cron. Free for public repos. |
| **Contact Enrichment** | Apollo.io API | v1 | People search, email/phone enrichment for ICP segments. Free search, 1 credit per email reveal. |
| **Federal Data APIs** | SAM.gov, USASpending, FPDS, Grants.gov | v2/v1 | Free government APIs. SAM.gov requires API key (free, 1,000 req/day). Others require no auth. |
| **Outreach (Future)** | Instantly + Twilio + Retell AI | N/A | Email sequences, SMS, AI voice. Not yet implemented for Newport. |
| **Version Control** | Git + GitHub | N/A | Single repo, main branch. |
| **Development** | Claude CLI in VS Code + Claude Desktop | N/A | CLI for code changes, Desktop for iterative document/model work. |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT DELIVERABLES                          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ GovCon Web Presentation (React 19 + Vite 7)                 │   │
│  │ 20 interactive slides — web/src/components/slides/          │   │
│  │ Data: web/src/data/{market,strategy,financials}.js          │   │
│  │ Design: web/DESIGN-SYSTEM.md                                │   │
│  └──────────────────────────┬───────────────────────────────────┘   │
│                              │                                       │
│           market_data.json ◄── collect_market_data.py                │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ ARCHIVED: PPTX builders + Excel models → archive/           │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────┼──────────────────────────────────────────────────┘
                   │
┌──────────────────┼──────────────────────────────────────────────────┐
│              INTELLIGENCE LAYER (Python)                             │
│                                                                      │
│  ┌─────────────────────────────────┐  ┌────────────────────────┐    │
│  │ GOVCON CHANNEL                  │  │ COMMERCIAL CHANNEL     │    │
│  │                                  │  │                        │    │
│  │  scrapers/                       │  │  scrapers/             │    │
│  │  ├─ contract_scanner.py (10 rpt) │  │  └─ apollo_prospector  │    │
│  │  └─ daily_monitor.py             │  │                        │    │
│  │                                  │  │  enrichment/           │    │
│  │  scoring/                        │  │  ├─ apollo_client.py   │    │
│  │  ├─ bid_scorer.py                │  │  ├─ enricher.py        │    │
│  │  └─ bid_no_bid.py                │  │  └─ re_enrich.py       │    │
│  │                                  │  │                        │    │
│  │  tracking/                       │  │  (outreach/ — FUTURE)  │    │
│  │  └─ sheets_pipeline.py           │  │  ├─ instantly_client   │    │
│  │                                  │  │  ├─ twilio_client      │    │
│  │  notifications/                  │  │  └─ retell_client       │    │
│  │  └─ notify.py                    │  │                        │    │
│  └─────────────────────────────────┘  └────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ SHARED: enrichment/ (API clients)                            │    │
│  │  sam_client.py │ sam_entity_client.py │ usaspending_client.py│    │
│  │  fpds_client.py │ grants_client.py                           │    │
│  └─────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
                   │
┌──────────────────┼──────────────────────────────────────────────────┐
│              CONFIGURATION LAYER                                     │
│                                                                      │
│  config/                                                             │
│  ├─ icp_definitions.json        # 5 segments, Apollo search params   │
│  ├─ exclusions.json              # Company/title exclusion lists     │
│  └─ government_contracts.json    # NAICS/PSC codes, scoring params   │
│                                                                      │
│  .env                            # API keys (gitignored)             │
└──────────────────────────────────────────────────────────────────────┘
                   │
┌──────────────────┼──────────────────────────────────────────────────┐
│              DATA LAYER (gitignored runtime data)                    │
│                                                                      │
│  data/                                                               │
│  ├─ raw/          # API responses                                    │
│  ├─ enriched/     # Post-processing output                           │
│  ├─ final/        # Timestamped CSV deliverables                     │
│  ├─ cache/        # API response caching                             │
│  └─ contacts/     # FL decision maker list, Apollo prospects         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: GovCon Intelligence Pipeline

```
1. DAILY MONITOR (automated, 6 AM ET)
   SAM.gov API → daily_monitor.py → bid_no_bid.py (score) → sheets_pipeline.py → Slack/email
   
2. ON-DEMAND SCANNER (manual, when doing market research)
   SAM.gov + USASpending + FPDS + Grants.gov → contract_scanner.py → 10 CSV reports → data/final/

3. DELIVERABLES PIPELINE (manual, for Newport presentation)
   collect_market_data.py → market_data.json → web/src/data/*.js → React slide components
   Dev: cd web && npm run dev    Build: cd web && npm run build

4. BID SCORING (manual, when evaluating specific opportunities)
   CSV of opportunities → bid_no_bid.py → scored + ranked output → decision support
```

## Data Flow: Commercial SDR Pipeline

```
1. PROSPECTING (manual, segment by segment)
   config/icp_definitions.json → apollo_prospector.py → raw prospect CSVs → data/raw/

2. ENRICHMENT (manual, after prospecting)
   raw prospects → enricher.py (Apollo reveal) → enriched CSVs → data/enriched/
   enriched CSVs → re_enrich.py (refresh) → updated enriched CSVs

3. OUTREACH (FUTURE — not yet built)
   enriched contacts → campaign_orchestrator.py → Instantly (email) → Twilio (SMS) → Retell (voice)
   responses → CRM (Google Sheets) → follow-up sequences
```

---

## Key Architecture Decisions

### Decision 1: Monorepo with Channel Separation

- **Context**: Two distinct channels (GovCon and Commercial) with shared config and overlapping tooling
- **Decision**: Single repo with top-level `govcon/` and `commercial/` directories, shared `config/`
- **Rationale**: Shared API clients (Apollo is used by both channels), shared exclusion lists, single CLAUDE.md, single CI/CD configuration. Channel directories are self-contained enough to work independently.
- **Trade-offs**: Repo size grows. Someone working on only one channel still clones everything.
- **Alternatives Considered**: Separate repos per channel — rejected because of shared config duplication and loss of cross-channel context for Claude CLI.

### Decision 2: Flat Files Over Database

- **Context**: Pipeline data, prospect lists, and market research all need persistence
- **Decision**: CSV files in `data/` (gitignored) + Google Sheets for operational tracking
- **Rationale**: No web app = no need for a database. CSVs are readable by pandas, Excel, and humans. Google Sheets gives Newport a collaborative view without requiring database access. Solo operator doesn't need PostgreSQL overhead.
- **Trade-offs**: No query optimization, no relationships, no concurrent write safety
- **Alternatives Considered**: Supabase/Postgres — premature for a pipeline tool used by one person

### Decision 3: Web-Based Interactive Presentation

- **Context**: Presentation decks and financial models need to be iterated as data and assumptions change. PPTX generation was limiting in design flexibility.
- **Decision**: React 19 + Vite 7 web application with Tailwind CSS 4, ECharts 6, and Motion 12 for the GovCon presentation. Data separated into JS modules (`market.js`, `strategy.js`, `financials.js`). Legacy PPTX builders and Excel scripts archived.
- **Rationale**: Web app enables interactive data visualizations, animated transitions, responsive design, and instant iteration via hot reload. Shareable via URL (Netlify-deployed, password-gated). The `market_data.json` intermediate file still decouples data collection from presentation.
- **Trade-offs**: Requires Node.js toolchain. Offline viewing requires a build step. Excel model no longer directly editable by Newport — financial data is presentation-only.
- **Alternatives Considered**: PPTX generation (pptxgenjs) — completed and archived, but design flexibility was too constrained. The web app delivers a materially better client experience.

### Decision 4: Claude Desktop for Financial Models, CLI for Everything Else

- **Context**: The financial model went through 7 iterations (v1 → v7) requiring conversational refinement
- **Decision**: Use Claude Desktop for iterative document/model work, Claude CLI for code changes
- **Rationale**: Desktop excels at "help me think through this model structure" conversations. CLI excels at "create this Python file, run this command, fix this bug" workflows. The v7 model is demonstrably better than what `build_proforma.py` generates.
- **Trade-offs**: v7 model is not reproducible from code — it was accepted as canonical and key data extracted to `web/src/data/financials.js`. The archived .xlsx at `archive/govcon-financials-openpyxl/` serves as the reference.
- **Alternatives Considered**: CLI-only — resulted in v4-quality output. Desktop-only — can't run Python scripts or manage the codebase.

### Decision 5: Free APIs First, Paid Platforms as Recommendations

- **Context**: Newport hasn't committed to any paid tools yet
- **Decision**: Build the intelligence system on free APIs (SAM.gov, USASpending, FPDS, Grants.gov) and recommend paid platforms (CLEATUS, HigherGov, GovSpend) as the "paid route" upgrade
- **Rationale**: Proves capability before asking for investment. The "Two Routes" comparison is more credible when we can demonstrate what the free system already does.
- **Trade-offs**: Free APIs cover only ~40–50% of the market. SLED data is nearly invisible without paid tools.
- **Alternatives Considered**: Start with paid tools — rejected because Newport hasn't agreed to any investment yet and we're proving concept first.

---

## Environment Configuration

### Required Environment Variables

| Variable | Service | Channel | Required? | Notes |
|----------|---------|---------|-----------|-------|
| `SAM_API_KEY` | SAM.gov Opportunities + Entity | GovCon | Yes | Free, register at api.data.gov. 1,000 req/day |
| `APOLLO_API_KEY` | Apollo.io people search | Commercial | Yes | Free search, 1 credit/reveal. Get at app.apollo.io |
| `SLACK_WEBHOOK_URL` | Slack notifications | GovCon | Recommended | Create incoming webhook at api.slack.com |
| `RESEND_API_KEY` | Resend email API | GovCon | Optional | Alternative to Slack for notifications |
| `RESEND_TO_EMAIL` | Email recipient | GovCon | If using Resend | Newport contact email |
| `GOOGLE_SHEETS_CREDS_PATH` | Google Sheets API | GovCon | For pipeline | Service account JSON file path |
| `GOOGLE_SHEETS_ID` | Target spreadsheet | GovCon | For pipeline | Spreadsheet ID from URL |
| `INSTANTLY_API_KEY` | Instantly email outreach | Commercial | Future | Not yet implemented |
| `TWILIO_ACCOUNT_SID` | Twilio SMS | Commercial | Future | Not yet implemented |
| `TWILIO_AUTH_TOKEN` | Twilio auth | Commercial | Future | Not yet implemented |
| `RETELL_API_KEY` | Retell AI voice | Commercial | Future | Not yet implemented |

### Development vs. Production

| Aspect | Development | Production |
|--------|-------------|------------|
| Data directory | `data/` (local) | Same (no hosted deployment) |
| API calls | `--dry-run` flag on all scrapers | Live API calls |
| Notifications | Disabled or test channel | Live Slack + email |
| Scheduling | Manual execution | GitHub Actions cron |
| Web presentation | `cd web && npm run dev` | Netlify deployment (password-gated) |

---

## Claude CLI Notes

When working on this codebase:

1. **Path resolution pattern**: All scripts use `_project_root = Path(__file__).resolve().parent.parent.parent` to find repo root. Don't change this convention.
2. **Config loading**: Always load from `_project_root / "config" / "<file>.json"`. Config stays at repo root level.
3. **Data output**: All CSVs go to `data/final/` with timestamped filenames: `{prefix}_{report}_{YYYYMMDD_HHMM}.csv`
4. **API clients**: Follow the existing pattern in `enrichment/` — `__init__` with key from env, `requests.Session`, `_request()` with 429 retry + exponential backoff, `stats` property.
5. **CLI pattern**: All scrapers use argparse with `--dry-run` mode, `load_config()`, `save_results()`.
6. **Never commit API keys** — they go in `.env` (gitignored).
7. **The deliverables pipeline flows**: `collect_market_data.py` → `market_data.json` → `web/src/data/*.js` → React slide components. Don't break this chain.
