# Newport Wholesalers Lead Generation

## Project Overview

Automated lead generation and competitive intelligence pipeline for Newport Wholesalers — a food wholesale distributor. Targets enterprise grocery buyers, food suppliers/manufacturers, government food procurement, corrections food service, and candy wholesalers.

## Architecture

```
config/              # JSON configs: ICP definitions, exclusions, government contracts
enrichment/          # API clients: Apollo.io, SAM.gov, USASpending.gov
scrapers/            # CLI tools: apollo_prospector.py, contract_scanner.py
crm/                 # Google Sheets CRM integration
orchestrator/        # Campaign runner
outreach/            # Email (Instantly), SMS (Twilio), Voice (Retell AI)
tracking/            # Dashboard and CRM tracking
data/                # Gitignored: raw/, enriched/, final/, cache/
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
Federal food procurement intelligence from SAM.gov + USASpending.gov.
```
python scrapers/contract_scanner.py --report all --dry-run
python scrapers/contract_scanner.py --report market-size --fiscal-years 2024,2025
python scrapers/contract_scanner.py --report expiring --months-ahead 12 --max-pages 3
python scrapers/contract_scanner.py --report opportunities --max-pages 2
python scrapers/contract_scanner.py --report incumbents --max-pages 5
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
- `SAM_API_KEY` — SAM.gov for federal contract data (free, 1,000 req/day)
- USASpending.gov — no key needed

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
- Government contract intelligence pipeline with 4 reports:
  - **Expiring contracts** — SAM.gov awards expiring in N months
  - **Incumbent analysis** — vendor aggregation (contracts, value, competition %)
  - **Opportunity pipeline** — active solicitations/pre-sols/sources sought
  - **Market sizing** — USASpending spending by NAICS + agency per FY
- Cache layer for SAM.gov rate limit management (24hr TTL, `data/cache/`)
- 10 primary NAICS codes (food wholesale 4244xx + food service 722310), 42 secondary (food manufacturing 311xxx)

### Not Yet Verified Against Live APIs
- Contract scanner reports (expiring, incumbents, opportunities) require SAM_API_KEY to test
- Market-size report runs without a key (USASpending is free) — test with: `python scrapers/contract_scanner.py --report market-size --fiscal-years 2024,2025`
- After getting SAM key, verify all reports produce valid CSV output and cache works

### Remaining Backlog
- CRM integration (Google Sheets push)
- Outreach automation (Instantly email, Twilio SMS, Retell voice)
- Campaign orchestrator
- Dashboard/tracking
