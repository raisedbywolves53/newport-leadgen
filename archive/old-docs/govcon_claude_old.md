# Newport Government Contracting Command Center

## Project Overview
Government contract intelligence, scoring, and pipeline management system for Newport Wholesalers — a 30-year South Florida grocery wholesaler (NAICS 424410/424450/424490) entering government contracting. Target: $10K–$350K micro and small contracts across federal, state, local, and education buyers.

## How This Repo Works
This project is built in phases. Each phase has its own requirements document in `/docs/`. Execute phases in order. Do NOT skip ahead.

### Phase Execution Order
1. **PHASE-1-REPO-SETUP.md** — Organize repo structure, migrate files from newport-leadgen, clean up
2. **PHASE-2-OPERATIONAL-SYSTEM.md** — Build the 3 missing operational components (bid/no-bid scoring, pipeline lifecycle, daily automation)
3. **PHASE-3-PRESENTATION.md** — Generate the client-facing PPT proposal deck
4. **PHASE-4-FINANCIALS.md** — Generate the pro forma Excel with 3-scenario projections

### Reference Documents (read but don't execute)
- `docs/REFERENCE-requirements.md` — Original technical build specs (Build Specs 1-5). API clients from Specs 1-2 are ALREADY BUILT. Specs 3-5 are addressed in Phase 2.
- `docs/REFERENCE-strategy.md` — Buyer universe, competitive landscape, FPDS findings, financial assumptions. Used by Phases 3-4 for data.

## What's Already Built (from newport-leadgen migration)
These files exist and work. Do NOT rebuild them:
- `enrichment/sam_client.py` — SAM.gov opportunities API
- `enrichment/usaspending_client.py` — USASpending award data
- `enrichment/fpds_client.py` — FPDS competition density analysis
- `enrichment/grants_client.py` — Grants.gov USDA food grants
- `enrichment/sam_entity_client.py` — SAM entity/competitor lookup
- `tracking/sheets_crm.py` — Google Sheets CRM integration
- `dashboard/generate_dashboard.py` — Dashboard/report generator
- `templates/capability_statement_template.docx` — Capability statement
- `templates/sources_sought_response_template.docx`
- `templates/legitimacy_package_checklist.docx`
- `config/government_contracts.json` — NAICS/PSC filter config

## What Does NOT Belong in This Repo
The following are commercial lead generation tools and belong in `newport-leadgen`:
- Apollo prospecting, enrichment, outreach (email/sms/voice)
- Campaign runner / orchestrator
- Commercial CRM setup
- Pitchbook generator
- Candy/LATAM strategy docs
- ICP definitions, exclusions config

## Tech Stack
- Python 3.11+
- Google Sheets API (via gspread)
- GitHub Actions (automation)
- Resend (email notifications)
- No frontend. No database. Sheets is the operational layer.

## Environment Variables Required
```
SAM_GOV_API_KEY=
USASPENDING_API_KEY=  (optional, public API)
GOOGLE_SHEETS_CREDENTIALS_PATH=
RESEND_API_KEY=
NOTIFICATION_EMAIL=
```
