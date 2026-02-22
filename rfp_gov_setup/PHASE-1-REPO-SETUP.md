# Phase 1: Repository Setup & File Migration

## Objective
Split `newport-leadgen` into two repos. This repo (`newport-govcon`) gets all government contracting assets. `newport-leadgen` keeps commercial lead gen.

## Prerequisites
- Access to `newport-leadgen` project directory
- Git initialized in new `newport-govcon` directory

## Step 1: Create Directory Structure

```
newport-govcon/
├── CLAUDE.md
├── README.md
├── docs/
│   ├── PHASE-1-REPO-SETUP.md          (this file)
│   ├── PHASE-2-OPERATIONAL-SYSTEM.md
│   ├── PHASE-3-PRESENTATION.md
│   ├── PHASE-4-FINANCIALS.md
│   ├── REFERENCE-requirements.md
│   └── REFERENCE-strategy.md
├── enrichment/                         ← API clients (migrate from newport-leadgen)
│   ├── __init__.py
│   ├── sam_client.py
│   ├── usaspending_client.py
│   ├── fpds_client.py
│   ├── grants_client.py
│   └── sam_entity_client.py
├── scoring/                            ← NEW (Phase 2 builds this)
│   ├── __init__.py
│   └── bid_no_bid.py
├── pipeline/                           ← NEW (Phase 2 builds this)
│   ├── __init__.py
│   └── sheets_pipeline.py
├── automation/                         ← NEW (Phase 2 builds this)
│   └── daily_monitor.py
├── dashboard/                          ← Migrate from newport-leadgen
│   └── generate_dashboard.py
├── templates/                          ← Migrate from newport-leadgen
│   ├── capability_statement_template.docx
│   ├── sources_sought_response_template.docx
│   └── legitimacy_package_checklist.docx
├── config/
│   └── government_contracts.json
├── strategy/                           ← Migrate gov-specific strategy docs only
│   ├── government_contract_strategy.md
│   ├── government_contact_sourcing_playbook.md
│   └── intelligence_assessment_feb2026.md
├── deliverables/                       ← Phase 3-4 output goes here
│   ├── presentation/
│   └── financials/
├── .github/
│   └── workflows/
│       └── daily-monitor.yml           ← Phase 2 builds this
├── .env.example
├── requirements.txt
└── .gitignore
```

## Step 2: Migrate Files from newport-leadgen

Copy these files FROM `newport-leadgen` TO `newport-govcon`:

### Enrichment (copy entire files)
```
newport-leadgen/enrichment/sam_client.py        → newport-govcon/enrichment/sam_client.py
newport-leadgen/enrichment/usaspending_client.py → newport-govcon/enrichment/usaspending_client.py
newport-leadgen/enrichment/fpds_client.py       → newport-govcon/enrichment/fpds_client.py
newport-leadgen/enrichment/grants_client.py     → newport-govcon/enrichment/grants_client.py
newport-leadgen/enrichment/sam_entity_client.py → newport-govcon/enrichment/sam_entity_client.py
```

### Dashboard
```
newport-leadgen/dashboard/generate_dashboard.py → newport-govcon/dashboard/generate_dashboard.py
```

### Templates
```
newport-leadgen/templates/capability_statement_template.docx     → newport-govcon/templates/
newport-leadgen/templates/sources_sought_response_template.docx  → newport-govcon/templates/
newport-leadgen/templates/legitimacy_package_checklist.docx      → newport-govcon/templates/
```

### Config
```
newport-leadgen/config/government_contracts.json → newport-govcon/config/government_contracts.json
```

### Strategy (gov-specific only)
```
newport-leadgen/strategy/government_contract_strategy.md           → newport-govcon/strategy/
newport-leadgen/strategy/government_contact_sourcing_playbook.md   → newport-govcon/strategy/
newport-leadgen/strategy/intelligence_assessment_feb2026.md        → newport-govcon/strategy/
```

### DO NOT migrate these (they stay in newport-leadgen):
- enrichment/apollo_client.py
- enrichment/enricher.py
- scrapers/ (entire folder)
- crm/setup_crm.py, crm/sheets_manager.py
- orchestrator/ (entire folder)
- outreach/ (entire folder)
- pitchbook/ (entire folder)
- tracking/dashboard.py
- config/icp_definitions.json, config/exclusions.json
- strategy/candy_latam_trade_assessment.md
- Any research docs about non-government topics

## Step 3: Update Imports

After migration, scan all Python files for imports that reference modules left behind in `newport-leadgen`. Fix broken imports. The enrichment clients should be self-contained — if they import from `enricher.py` or `apollo_client.py`, remove those dependencies.

## Step 4: Create requirements.txt

```
requests>=2.31.0
gspread>=5.12.0
google-auth>=2.25.0
google-auth-oauthlib>=1.2.0
python-dotenv>=1.0.0
resend>=0.7.0
openpyxl>=3.1.0
python-docx>=1.1.0
```

## Step 5: Create .env.example

```
SAM_GOV_API_KEY=your_sam_gov_api_key
GOOGLE_SHEETS_CREDENTIALS_PATH=./config/google_credentials.json
RESEND_API_KEY=your_resend_api_key
NOTIFICATION_EMAIL=zack@stillmindcreative.com
```

## Step 6: Create .gitignore

```
.env
__pycache__/
*.pyc
config/google_credentials.json
data/
logs/
deliverables/**/*.pptx
deliverables/**/*.xlsx
.DS_Store
```

## Step 7: Create README.md

Write a README that explains:
- What this project does (government contract intelligence for Newport Wholesalers)
- How to set up (clone, install deps, configure .env)
- How to run each enrichment client manually
- That automation runs via GitHub Actions daily at 6 AM ET
- Link to docs/ folder for full system documentation

## Step 8: Git Init & Initial Commit

```bash
cd newport-govcon
git init
git add .
git commit -m "Initial commit: Newport GovCon Command Center - migrated from newport-leadgen"
```

## Completion Criteria
- [ ] All files migrated and in correct directories
- [ ] No broken imports in any Python file
- [ ] requirements.txt includes all dependencies
- [ ] .env.example has all required variables
- [ ] README.md is written
- [ ] Git repo initialized with clean first commit
- [ ] newport-leadgen still works independently (don't delete files from it, just copy)

## Next Phase
Read `docs/PHASE-2-OPERATIONAL-SYSTEM.md`
