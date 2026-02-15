# Goldman's Garage Door Repair — Agentic Lead Gen System

## Development Plan

**Owner:** Tal Goldman, phone (248) 509-0470
**Website:** goldmansgaragedoorrepair.com
**Markets:** Oakland County MI, Wayne County MI, Triangle NC (Raleigh-Durham-Chapel Hill)

---

## System Overview

Two pipelines:

1. **Direct-to-customer:** new homeowners, aging neighborhoods, storm damage, commercial properties.
2. **Referral partners:** real estate agents, property managers, home inspectors, insurance agents, home builders/GCs, adjacent trades (HVAC, electricians, plumbers, painters, handymen, locksmiths, landscapers).

## Tech Stack

| Tool | Purpose | Integration |
|------|---------|-------------|
| HomeHarvest | Scrape recently sold homes from Realtor.com | Python, `pip install homeharvest` |
| Google Places API | Scrape local businesses for referral partners | REST API |
| Clay | Enrich scraped data with emails, phones, decision-maker names | Manual platform (not code) |
| Instantly.ai | Cold email campaigns with domain warmup | API |
| Twilio | SMS outreach + inbound reply handling | Python SDK |
| Retell AI | AI voice calls that warm-transfer to Tal's phone | Python SDK |
| Google Sheets (gspread) | Lightweight CRM and tracking | Python SDK |

## Phase 0: Project Setup

### Prompt 0A — Create Project Scaffold

Create the complete folder structure with placeholder files:

```
goldmans-leadgen/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config/
│   ├── markets.json          (full zip codes for all 3 markets)
│   ├── search_queries.json   (Google Maps queries per ICP)
│   └── icp_definitions.json  (ICP metadata)
├── scrapers/
│   ├── __init__.py
│   ├── homeowner_scraper.py
│   ├── gmaps_scraper.py
│   ├── weather_monitor.py
│   └── clay_formatter.py
├── outreach/
│   ├── __init__.py
│   ├── email/
│   │   ├── __init__.py
│   │   ├── instantly_client.py
│   │   └── templates/
│   ├── sms/
│   │   ├── __init__.py
│   │   ├── twilio_sender.py
│   │   └── webhook_handler.py
│   └── voice/
│       ├── __init__.py
│       ├── retell_client.py
│       └── agent_configs/
├── tracking/
│   ├── __init__.py
│   ├── sheets_crm.py
│   └── dashboard.py
├── orchestrator/
│   ├── __init__.py
│   └── campaign_runner.py
└── assets/
    └── email_templates/
```

**requirements.txt:** homeharvest, pandas, requests, python-dotenv, twilio, retell-sdk, gspread, oauth2client, flask, schedule

**.env.example placeholders:** INSTANTLY_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_MI, TWILIO_PHONE_NC, RETELL_API_KEY, RETELL_PHONE_MI, RETELL_PHONE_NC, TAL_PHONE_NUMBER, OPENWEATHER_API_KEY, GOOGLE_SHEETS_CREDS_PATH, GOOGLE_PLACES_API_KEY

**config/markets.json** — include full zip code lists:
- **Oakland County MI:** 48009, 48017, 48025, 48030, 48034, 48067, 48069, 48071, 48073, 48075, 48076, 48083, 48084, 48085, 48098, 48301, 48302, 48304, 48306, 48307, 48309, 48322-48329, 48331, 48334-48336, 48340-48342, 48346, 48348, 48350, 48356, 48357, 48359, 48360, 48362, 48363, 48367, 48370, 48371, 48374-48377, 48380-48383, 48386, 48390, 48393
- **Wayne County MI:** 48101, 48111, 48120, 48122, 48124-48128, 48134, 48135, 48138, 48141, 48146, 48150, 48152, 48154, 48164, 48167, 48168, 48170, 48173, 48174, 48180, 48183-48188, 48192, 48193, 48195
- **Triangle NC:** 27502, 27510, 27511, 27513, 27514, 27516, 27517, 27519, 27520, 27523, 27526, 27529, 27539-27541, 27545, 27560, 27562, 27571, 27587, 27591, 27596, 27601, 27603-27617, 27695, 27701, 27703-27705, 27707-27709

**Acceptance Criteria:**
- All directories and files exist per tree structure
- `markets.json` contains expanded zip code lists (no unexpanded ranges)
- `requirements.txt` lists all packages
- `.env.example` has all placeholder keys
- All config JSON files are valid
- Git commit on `phase-0/setup` branch
