# Goldman's Garage Door Repair — Lead Generation System

Automated lead generation system for Goldman's Garage Door Repair, serving Oakland County MI, Wayne County MI, and the Triangle NC region.

## Pipelines

1. **Direct-to-Customer** — New homeowners, aging neighborhoods, storm damage, commercial properties
2. **Referral Partners** — Real estate agents, property managers, home inspectors, insurance agents, builders, adjacent trades

## Tech Stack

- **HomeHarvest** — Scrape recently sold homes
- **Google Places API** — Find local referral partners
- **Clay** — Data enrichment (manual)
- **Instantly.ai** — Cold email campaigns
- **Twilio** — SMS outreach
- **Retell AI** — AI voice calls with warm transfer
- **Google Sheets** — Lightweight CRM

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your API keys in .env
```

## Project Structure

```
config/         — Market definitions, ICP configs, search queries
scrapers/       — HomeHarvest, Google Maps, weather monitoring, Clay formatting
outreach/       — Email (Instantly), SMS (Twilio), Voice (Retell AI)
tracking/       — Google Sheets CRM, dashboard
orchestrator/   — Campaign runner and scheduling
assets/         — Email templates and static assets
```
