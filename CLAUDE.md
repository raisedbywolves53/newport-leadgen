# Newport Wholesalers Lead Generation

## Project Overview

Automated lead generation and competitive intelligence pipeline for Newport Wholesalers — a food wholesale distributor. Targets enterprise grocery buyers, food suppliers/manufacturers, and candy wholesalers.

> **Note**: Government contracting assets (scoring, pipeline tracker, daily monitor, enrichment clients) have been migrated to the dedicated **`newport-govcon`** repo (`C:\Users\USER\newport-govcon`). This repo retains the original copies for reference but active government contracting development happens in `newport-govcon`.

## Architecture

```
config/              # JSON configs: ICP definitions, exclusions, government contracts
enrichment/          # API clients: Apollo.io, SAM.gov (Opps + Entity), USASpending.gov, Grants.gov, FPDS
scoring/             # Bid/no-bid scoring framework (9-factor weighted model)
scrapers/            # CLI tools: apollo_prospector.py, contract_scanner.py, daily_monitor.py
notifications/       # Slack + email notification dispatchers
crm/                 # Google Sheets CRM integration (Goldman's)
tracking/            # GovCon Pipeline Tracker (Google Sheets)
orchestrator/        # Campaign runner
outreach/            # Email (Instantly), SMS (Twilio), Voice (Retell AI)
data/                # Gitignored: raw/, enriched/, final/, cache/
.github/workflows/   # GitHub Actions: daily-scan.yml
```

## Key Tools

### Apollo Prospector (`scrapers/apollo_prospector.py`)
Enterprise people search via Apollo.io. Free search, 1 credit per email reveal.
```
python scrapers/apollo_prospector.py --segment segment_a_buyers --dry-run
python scrapers/apollo_prospector.py --segment all --region united_states --max-pages 10
python scrapers/apollo_prospector.py --segment all --reveal-emails --max-reveals 100
```

### Government Contract Scanner (`scrapers/contract_scanner.py`)
Federal food procurement intelligence from SAM.gov + USASpending.gov + Grants.gov + FPDS. 10 reports.
```
python scrapers/contract_scanner.py --report all --dry-run
python scrapers/contract_scanner.py --report market-size --fiscal-years 2024,2025
python scrapers/contract_scanner.py --report expiring --months-ahead 12 --max-pages 3
python scrapers/contract_scanner.py --report opportunities --max-pages 2
python scrapers/contract_scanner.py --report opportunities --max-pages 2 --score
python scrapers/contract_scanner.py --report incumbents --max-pages 5
python scrapers/contract_scanner.py --report competitors --states FL,GA,AL
python scrapers/contract_scanner.py --report analytics --fiscal-years 2023,2024,2025
python scrapers/contract_scanner.py --report grants
python scrapers/contract_scanner.py --report competition-density --fiscal-years 2024,2025
```

### Bid/No-Bid Scorer (`scoring/bid_scorer.py`)
9-factor weighted scoring (0-100) → Strong Bid / Bid / Review / No-Bid decisions.
```
python scoring/bid_scorer.py --csv data/final/govt_opportunity_pipeline_*.csv
python scoring/bid_scorer.py --csv FILE --overrides '{"past_performance": 1}'
python scoring/bid_scorer.py --csv FILE --top 10
```

### Daily SAM.gov Monitor (`scrapers/daily_monitor.py`)
Automated change detection with Slack/email notifications. Runs via GitHub Actions at 6 AM ET.
```
python scrapers/daily_monitor.py --dry-run
python scrapers/daily_monitor.py --score --dry-run
python scrapers/daily_monitor.py --score --push-to-sheet --dry-run
python scrapers/daily_monitor.py --max-pages 3
```

### GovCon Pipeline Tracker (`tracking/sheets_crm.py`)
Google Sheets pipeline tracker: 12 stages, 11 buyer categories, 4 tabs (Opportunities/Agencies/Contacts/Dashboard).
```
python tracking/sheets_crm.py --dry-run --init
python tracking/sheets_crm.py --dry-run --add-opp --solicitation W51YHZ-24-R-0001 --title "Fresh Produce" --agency "DEPT OF DEFENSE" --state FL --naics 424480 --category military_dla --tier federal
python tracking/sheets_crm.py --dry-run --update-stage OPP_ID qualifying
python tracking/sheets_crm.py --dry-run --import-csv data/final/govt_opportunity_pipeline_*.csv
python tracking/sheets_crm.py --dry-run --dashboard
python tracking/sheets_crm.py --dry-run --deadlines --days-ahead 14
```

## Segments

| Segment | Target | Geography |
|---------|--------|-----------|
| A — Buyers | Enterprise grocery/retail chains (200+ emp, $50M+ rev) | US, UK, EU |
| B — Suppliers | Food manufacturers/distributors (100+ emp, $25M+ rev) | US, UK, EU |
| C — Government | Federal/state food procurement agencies | US only |
| D — Corrections | Prison food service & commissary | US only |
| E — Candy | Candy wholesalers & distributors (11+ emp, $5M+ rev) | US + LATAM |

## API Keys Required

- `APOLLO_API_KEY` — Apollo.io for people search and enrichment
- `SAM_API_KEY` — SAM.gov for opportunities + entity data (free, 1,000 req/day)
- `SLACK_WEBHOOK_URL` — Slack incoming webhook for daily monitor alerts
- `RESEND_API_KEY` + `RESEND_TO_EMAIL` — Resend for email notifications (optional)
- USASpending.gov — no key needed
- Grants.gov — no key needed
- FPDS — no key needed

## Config Files

- `config/icp_definitions.json` — Segment definitions, Apollo search params, geography
- `config/exclusions.json` — Company/title exclusion lists per segment
- `config/government_contracts.json` — NAICS/PSC codes, API settings, analysis params, cache config

## Code Patterns

- **API clients** (`enrichment/`): `__init__` with key from env, `requests.Session`, `_request()` with 429 retry + exponential backoff, `stats` property for usage tracking
- **CLI scrapers** (`scrapers/`): argparse, `load_config()`, `--dry-run` mode, `save_results()` to CSV with timestamp (`YYYYMMDD_HHMM`), `print_summary()` with breakdowns
- **Data flow**: Config → API client → flat dicts → `pd.DataFrame` → dedup → filter → CSV to `data/final/`
- **Output naming**: `{prefix}_{report}_{YYYYMMDD_HHMM}.csv`

## Current State (Feb 2026)

### Completed
- Full Apollo prospector pipeline (segments A-E) with enterprise people search, email reveal, exclusion filters, geographic filtering
- Government contract intelligence pipeline with 10 reports:
  - **Expiring contracts** — USASpending awards expiring in N months
  - **Incumbent analysis** — vendor aggregation (contracts, value, competition %)
  - **Small contracts** — $10K-$350K simplified acquisition range
  - **FEMA procurement** — disaster food contracts
  - **Opportunity pipeline** — active solicitations/pre-sols/sources sought (7 ptypes)
  - **Market sizing** — USASpending spending by NAICS + agency per FY
  - **Competitor registry** — SAM.gov registered vendors by NAICS/state
  - **Computed analytics** — trends, geography heatmap, recipient concentration
  - **Grants pipeline** — Grants.gov USDA food grants
  - **Competition density** — FPDS avg offers per award by NAICS/agency (NEW)
- API clients: `sam_client.py` (opportunities), `sam_entity_client.py` (entity registry), `usaspending_client.py` (awards + enhanced endpoints), `grants_client.py` (grants), `fpds_client.py` (competition density)
- USASpending enhanced endpoints: `spending_by_recipient`, `spending_by_county`, `spending_by_geography`, `recipient_profile`, `new_awards_over_time`, `search_subawards`
- Cache layer for SAM.gov rate limit management (24hr TTL, `data/cache/`)
- 10 primary NAICS codes (food wholesale 4244xx + food service 722310), 42 secondary (food manufacturing 311xxx)
- 10 target states: FL, GA, AL, SC, NC, TN, MS, LA, VA, TX
- **Bid/No-Bid Scoring Framework** (`scoring/bid_scorer.py`):
  - 9-factor weighted model (NAICS 15%, Geography 15%, Size 10%, Competition 10%, Past Performance 15%, Eval Criteria 10%, Relationship 10%, Timeline 10%, Strategic 5%)
  - 5 auto-scored factors from opportunity data, 4 manual override factors (default 3)
  - Decision thresholds: 80=Strong Bid, 65=Bid, 50=Review, <50=No-Bid
  - Standalone CLI + integrated `--score` flag in contract_scanner.py
- **Daily SAM.gov Monitor** (`scrapers/daily_monitor.py`):
  - State persistence via `data/cache/last_opportunities.json`
  - Change detection (new/removed notice_ids across runs)
  - Optional bid scoring of new opportunities
  - Slack (Block Kit) + email (Resend API) notifications
  - GitHub Actions workflow (daily at 6 AM ET) with artifact upload
- **GovCon Pipeline Tracker** (`tracking/sheets_crm.py`):
  - 12 pipeline stages: identified → qualifying → bid_decision → capture → drafting_proposal → review → submitted → under_evaluation → awarded/lost/no_bid/cancelled
  - 11 buyer categories (K-12, corrections, military/DLA, VA, FEMA, county, city, university, food bank, state agency, other)
  - 4 tabs: Opportunities (29 cols), Agencies (11 cols), Contacts (11 cols), Dashboard (formulas)
  - Import from contract_scanner CSV or direct API dicts (daily_monitor integration)
  - Deadline reports, pipeline analytics, CSV export
- **Integration chain**: daily_monitor → bid_scorer → pipeline_tracker (optional `--push-to-sheet` flag)

### Verified Against Live APIs
- USASpending endpoints: market-size, small-contracts, fema, spending_by_recipient, spending_by_geography, new_awards_over_time — all confirmed working
- Grants.gov: search_grants confirmed working (136 food-related results)
- FPDS: fpds library confirmed working (111 records for NAICS 424410, 2-month window)
- SAM.gov Opportunities: requires SAM_API_KEY (key is set in .env)
- SAM.gov Entity API: requires SAM_API_KEY (same key, shares 1,000/day limit)

### Repo Split (Feb 2026)
- Government contracting assets migrated to `newport-govcon` repo
- This repo (`newport-leadgen`) retains: Apollo prospector, commercial CRM, outreach, orchestrator, pitchbook, candy/LATAM strategy
- Enrichment clients (SAM, USASpending, FPDS, Grants, SAM Entity) exist in both repos — `newport-govcon` is the active copy for gov work

### Remaining Backlog
- Outreach automation (Instantly email, Twilio SMS, Retell voice)
- Campaign orchestrator
- Pitchbook generator update to pull live data from API outputs
