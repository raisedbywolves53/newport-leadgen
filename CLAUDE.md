# Newport Wholesalers — Lead Generation Platform

## Company
Newport Wholesalers is a 30-year grocery wholesaler based in South Florida (Plantation, FL). NAICS 424410/424450/424490. Core products: confectionery, snacks, shelf-stable food, dry goods. Two growth channels managed from this repo.

## Two Channels

### Channel 1: Government Contracting (`govcon/`)
Federal, state, and local food procurement intelligence. Target: $10K-$350K contracts. Geographic focus: FL + Southeast US (GA, AL, SC, NC, TN, MS, LA, VA, TX). Buyer categories: military/DoD, BOP prisons, school districts, state corrections, FEMA, VA hospitals, county/city agencies.

### Channel 2: Commercial SDR (`commercial/`)
Outbound prospecting targeting enterprise grocery buyers, food suppliers/manufacturers, and candy wholesalers via Apollo.io. Five segments (A-E) with geographic and firmographic filters.

## Architecture

```
newport-leadgen/
├── CLAUDE.md                              # This file — master context
├── config/                                # Shared config (both channels)
│   ├── icp_definitions.json               # Segment definitions + Apollo search params
│   ├── exclusions.json                    # Company/title exclusion lists
│   └── government_contracts.json          # NAICS/PSC codes, API settings, scoring params
│
├── govcon/                                # CHANNEL 1: Government Contracting
│   ├── enrichment/                        # API clients
│   │   ├── sam_client.py                  # SAM.gov Opportunities (needs SAM_API_KEY)
│   │   ├── sam_entity_client.py           # SAM.gov Entity Registry (needs SAM_API_KEY)
│   │   ├── usaspending_client.py          # USASpending.gov (no key)
│   │   ├── fpds_client.py                 # FPDS competition density (no key)
│   │   └── grants_client.py              # Grants.gov USDA grants (no key)
│   ├── scrapers/
│   │   ├── contract_scanner.py            # 10-report intelligence pipeline
│   │   └── daily_monitor.py               # Daily SAM.gov monitor + notifications
│   ├── scoring/
│   │   ├── bid_scorer.py                  # Procedural 9-factor scorer (used by scanner)
│   │   └── bid_no_bid.py                  # OOP BidNoBidScorer (used by monitor + tracker)
│   ├── tracking/
│   │   └── sheets_pipeline.py             # Google Sheets pipeline tracker (v2, 3 tabs)
│   ├── notifications/
│   │   └── notify.py                      # Slack + email dispatchers
│   ├── deliverables/                      # Client-facing outputs
│   │   ├── collect_market_data.py         # FPDS + USASpending → market_data.json
│   │   ├── financials/
│   │   │   └── build_proforma.py          # Excel pro forma model (openpyxl)
│   │   └── presentation/
│   │       └── build_presentation.js      # PowerPoint proposal deck (pptxgenjs)
│   ├── templates/
│   │   ├── generate_templates.py          # Capability statement + sources sought (python-docx)
│   │   └── *.docx                         # Generated Word templates
│   └── docs/                              # Consolidated reference docs
│       ├── strategy.md                    # Buyer universe, platform stack, entry strategy
│       ├── research.md                    # TAM, competition, data sources, live validation
│       ├── requirements.md                # Command Center build spec (authoritative)
│       └── phases/                        # Phase execution specs
│
├── commercial/                            # CHANNEL 2: SDR / Outbound Prospecting
│   ├── enrichment/
│   │   ├── apollo_client.py               # Apollo.io API wrapper (free search + paid reveal)
│   │   ├── enricher.py                    # Bulk enrichment pipeline
│   │   └── re_enrich.py                   # Re-enrich revealed prospects (no extra credits)
│   ├── scrapers/
│   │   └── apollo_prospector.py           # Enterprise people search by segment
│   └── docs/
│       ├── icp_segments.md                # 5 segment definitions with Apollo filters
│       ├── candy_latam_assessment.md      # LATAM candy import viability
│       └── candy_wholesaler_research.md   # Candy distributor market research
│
├── data/                                  # Gitignored runtime data (raw/enriched/final/cache)
├── assets/                                # Images (newport_background.jpg)
├── archive/                               # Superseded files (reference only)
│   ├── pitchbook/                         # Old pitchbook (superseded by deliverables/)
│   ├── dashboard/                         # Old dashboard (superseded)
│   └── old-docs/                          # Pre-consolidation research/strategy docs
└── .github/workflows/daily-scan.yml       # GitHub Actions: daily SAM.gov monitor at 6 AM ET
```

## Key Commands

### GovCon — Contract Intelligence
```bash
# 10-report scanner
python govcon/scrapers/contract_scanner.py --report all --dry-run
python govcon/scrapers/contract_scanner.py --report opportunities --max-pages 2 --score
python govcon/scrapers/contract_scanner.py --report small-contracts --state FL --fiscal-years 2024,2025
python govcon/scrapers/contract_scanner.py --report expiring --months-ahead 12
python govcon/scrapers/contract_scanner.py --report competition-density --fiscal-years 2024,2025

# Daily monitor
python govcon/scrapers/daily_monitor.py --dry-run
python govcon/scrapers/daily_monitor.py --score --push-to-sheet --max-pages 3

# Bid scoring
python govcon/scoring/bid_no_bid.py --csv data/final/govt_opportunity_pipeline_*.csv --top 10
python govcon/scoring/bid_scorer.py --csv data/final/govt_opportunity_pipeline_*.csv

# Pipeline tracker
python govcon/tracking/sheets_pipeline.py --dry-run --init
python govcon/tracking/sheets_pipeline.py --dry-run --import-csv data/final/govt_opportunity_pipeline_*.csv
python govcon/tracking/sheets_pipeline.py --dry-run --dashboard

# Deliverables
python govcon/deliverables/collect_market_data.py
python govcon/deliverables/financials/build_proforma.py
cd govcon/deliverables/presentation && npm install && node build_presentation.js
```

### Commercial — Apollo Prospecting
```bash
python commercial/scrapers/apollo_prospector.py --segment segment_a_buyers --dry-run
python commercial/scrapers/apollo_prospector.py --segment all --region united_states --max-pages 10
python commercial/scrapers/apollo_prospector.py --segment all --reveal-emails --max-reveals 100
```

## API Keys

| Key | Service | Channel | Notes |
|-----|---------|---------|-------|
| `SAM_API_KEY` | SAM.gov Opportunities + Entity | GovCon | Free, 1,000 req/day |
| `APOLLO_API_KEY` | Apollo.io people search | Commercial | Free search, 1 credit/reveal |
| `SLACK_WEBHOOK_URL` | Slack notifications | GovCon | Daily monitor alerts |
| `RESEND_API_KEY` | Resend email API | GovCon | Optional email notifications |
| `NOTIFICATION_EMAIL` | Email recipient | GovCon | Required if using Resend |
| `GOOGLE_SHEETS_CREDENTIALS_PATH` | Google Sheets API | GovCon | Pipeline tracker |
| `GOOGLE_SHEETS_ID` | Target spreadsheet | GovCon | Pipeline tracker |

USASpending, FPDS, and Grants.gov require no API keys.

## Segments (Commercial)

| Segment | Target | Filters | Geography |
|---------|--------|---------|-----------|
| A — Buyers | Enterprise grocery/retail chains | 200+ emp, $50M+ rev | US, UK, EU |
| B — Suppliers | Food manufacturers/distributors | 100+ emp, $25M+ rev | US, UK, EU |
| C — Government | Federal/state food procurement | 100+ emp | US only |
| D — Corrections | Prison food service & commissary | 51+ emp, $10M+ rev | US only |
| E — Candy | Candy wholesalers & distributors | 11+ emp, $5M+ rev | US + LATAM |

## Code Patterns

- **Path resolution**: Scripts use `_project_root = Path(__file__).resolve().parent.parent.parent` to find repo root, then `sys.path.insert(0, str(_project_root / "govcon"))` (or `"commercial"`) to resolve internal package imports
- **API clients** (`enrichment/`): `__init__` with key from env, `requests.Session`, `_request()` with 429 retry + exponential backoff, `stats` property
- **CLI scrapers** (`scrapers/`): argparse, `load_config()`, `--dry-run` mode, `save_results()` to timestamped CSV in `data/final/`
- **Config loading**: `_project_root / "config" / "government_contracts.json"` — config stays at repo root, shared by both channels
- **Data flow**: Config → API client → flat dicts → `pd.DataFrame` → dedup → filter → CSV to `data/final/`
- **Output naming**: `{prefix}_{report}_{YYYYMMDD_HHMM}.csv`
- **Deliverables pipeline**: `collect_market_data.py` → `market_data.json` → consumed by `build_proforma.py` + `build_presentation.js`

## Confirmed Live Data (Feb 22, 2026)

All verified from live USASpending + FPDS API runs:
- **FL small contracts**: 117 contracts, $6.4M (DOJ/BOP #1 at $3.7M, DoD #2 at $2.3M)
- **FPDS competition density**: 537 awards, 32 NAICS/agency combos; 93% sole source for NAICS 424490 @ DoD
- **FEMA**: 11 contracts, $69.3M but 2 vendors = 97%; play = disaster registry + micro-purchases
- **TAM**: $7.17B national, $85M FL under $350K, 83% micro-purchases under $15K

## What's Done

### GovCon (Fully Built)
- 5 API clients: SAM.gov Opps, SAM.gov Entity, USASpending (enhanced), FPDS, Grants.gov
- 10-report contract scanner (expiring, incumbents, small-contracts, fema, opportunities, market-size, competitors, analytics, grants, competition-density)
- Bid/no-bid scoring: procedural (`bid_scorer.py`) + OOP (`bid_no_bid.py`), 9-factor weighted model (NAICS 15%, Geography 15%, Size 10%, Competition 10%, Past Performance 15%, Eval 10%, Relationship 10%, Timeline 10%, Strategic 5%)
- Decision thresholds: 80=Strong Bid, 65=Bid, 50=Review, <50=No-Bid
- Daily SAM.gov monitor with change detection, scoring, Slack/email notifications
- Google Sheets pipeline tracker v2 (3 tabs, 12 stages, 10 buyer categories)
- Deliverables: 17-slide PowerPoint deck, 4-sheet Excel pro forma, market data collector
- Templates: capability statement, sources sought response, legitimacy checklist
- GitHub Actions: daily monitor at 6 AM ET
- Integration chain: daily_monitor → bid_no_bid → sheets_pipeline → Slack/email

### Commercial (Partial)
- Apollo.io API client with people search, enrichment, bulk operations
- Apollo prospector for 5 segments (A-E) with enterprise filters
- Enrichment pipeline (enricher + re_enrich)
- ICP definitions + exclusion lists configured

## What's NOT Done

### GovCon — Remaining
- [ ] Rebuild pro forma to match v3 planning tool (`data/newport-govcon-planning-tool-v3.xlsx`)
  - 5 sheets: Executive Summary, Inputs (Free/Paid toggle), Revenue Model (3 tiers + retention), Example Contracts, Market Data
  - Charts, data validation dropdown, conditional formatting
- [ ] Monthly reporting template (automated from pipeline data)
- [ ] Notion pipeline tracker (master CRM across all sources)
- [ ] Direct portal registration tracking
- [ ] Cooperative purchasing vehicle applications

### Commercial — Remaining
- [ ] Outreach automation (email via Instantly, SMS via Twilio, voice via Retell AI)
  - Goldman's code extracted to separate repo (`goldmans-leadgen/`)
  - Needs to be rebuilt/adapted for Newport's segments
- [ ] Campaign orchestrator for Newport SDR workflow
- [ ] CRM integration for commercial leads

## Reference Documents

| Document | Location | Purpose |
|----------|----------|---------|
| v3 Planning Tool | `data/newport-govcon-planning-tool-v3.xlsx` | Target for pro forma rebuild |
| GovCon Strategy | `govcon/docs/strategy.md` | Buyer universe, platforms, entry strategy |
| GovCon Research | `govcon/docs/research.md` | TAM, competition, data validation |
| Build Specs | `govcon/docs/requirements.md` | Command Center technical spec |
| Phase Docs | `govcon/docs/phases/` | Phase 2-4 execution specs |
| ICP Segments | `commercial/docs/icp_segments.md` | 5 segment definitions |
| Candy Research | `commercial/docs/candy_wholesaler_research.md` | Market research |
| LATAM Assessment | `commercial/docs/candy_latam_assessment.md` | Import viability |
| Archived Docs | `archive/old-docs/` | Pre-consolidation source material |
