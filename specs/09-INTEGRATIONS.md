# Newport Wholesalers — Integrations

> **Last Updated**: February 24, 2026
> **Status**: Draft
> **Depends On**: [03-ARCHITECTURE.md](./03-ARCHITECTURE.md)

## Overview

This document catalogs every external service, API, and platform the Newport system integrates with — both the free data APIs already in use and the paid platforms recommended as part of the "Paid Route." For each service: what it does, how to set it up, what it costs, and what happens if it's unavailable.

---

## Free APIs (Currently Integrated)

### SAM.gov Opportunities API v2

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Federal contract opportunity monitoring. Powers the daily monitor and contract scanner. |
| **Auth** | API key (free, register at api.data.gov) |
| **Rate Limit** | 1,000 requests/day |
| **Docs** | https://open.gsa.gov/api/get-opportunities-public-api/ |
| **Our Client** | `govcon/enrichment/sam_client.py` |
| **Env Variable** | `SAM_API_KEY` |
| **Cost** | $0 |
| **Status** | ✅ Built and validated. Note: SAM.gov experienced API outage Feb 2026 — system gracefully degrades. |
| **If Unavailable** | Daily monitor reports "SAM.gov API unavailable" and skips. Historical data in CSVs remains accessible. |

### SAM.gov Entity API

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Vendor registry lookups. Verify competitor registrations, check Newport's own registration status. |
| **Auth** | Same `SAM_API_KEY` |
| **Our Client** | `govcon/enrichment/sam_entity_client.py` |
| **Cost** | $0 |

### USASpending.gov API

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Federal award data for TAM analysis, competitor intelligence, market sizing. Source of all "confirmed HIGH confidence" data. |
| **Auth** | None required |
| **Rate Limit** | Reasonable use (no formal limit published) |
| **Docs** | https://api.usaspending.gov/ |
| **Our Client** | `govcon/enrichment/usaspending_client.py` |
| **Cost** | $0 |
| **Status** | ✅ Built and validated. Confirmed $7.17B national TAM, **$87M FL** (39,857 awards), $55.5M PSC 8925. All figures re-confirmed via live API query Feb 24, 2026. |
| **If Unavailable** | Fallback to cached data in `market_data.json`. Research data doesn't change frequently. |

### FPDS (Federal Procurement Data System)

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Competition density analysis. How many vendors bid on specific NAICS/agency combinations. 537 awards across 32 combos analyzed. |
| **Auth** | None required |
| **Format** | ATOM feed (XML) |
| **Our Client** | `govcon/enrichment/fpds_client.py` (uses `fpds` Python library) |
| **Cost** | $0 |
| **Status** | ⚠️ FPDS ezSearch decommissioned Feb 24, 2026. ATOM feed survives through later FY2026 but will also be retired. Must migrate competition density analysis to SAM.gov contract awards search API before ATOM feed sunset. See Phase 5 in [DEVELOPMENT-PLAN.md](./05-DEVELOPMENT-PLAN.md). |

### Grants.gov API

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Federal grant opportunity monitoring. USDA food-related grants that may be relevant for Newport. |
| **Auth** | None required |
| **Docs** | https://www.grants.gov |
| **Our Client** | `govcon/enrichment/grants_client.py` |
| **Cost** | $0 |
| **Status** | ✅ Built. 136 food-related results validated. Lower priority than contract opportunities. |

### Apollo.io API v1

| Attribute | Detail |
|-----------|--------|
| **Purpose** | People search and contact enrichment for all 5 ICP segments. Free search (unlimited), 1 credit per email reveal. |
| **Auth** | API key (free tier available) |
| **Docs** | https://apolloio.github.io/apollo-api-docs/ |
| **Our Client** | `commercial/enrichment/apollo_client.py` |
| **Env Variable** | `APOLLO_API_KEY` |
| **Cost** | $0 (search) / $49–$119/mo (paid plans for more reveal credits) |
| **Status** | ✅ Built. Prospector for 5 segments, enrichment pipeline, re-enrichment for revealed contacts. |
| **If Unavailable** | Prospecting pauses. Existing enriched contacts remain usable. |

---

## Notification Services (Currently Integrated)

### Slack Incoming Webhooks

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Real-time notifications from daily SAM.gov monitor. New opportunities, scoring alerts. |
| **Setup** | Create incoming webhook at https://api.slack.com/messaging/webhooks |
| **Our Client** | `govcon/notifications/notify.py` |
| **Env Variable** | `SLACK_WEBHOOK_URL` |
| **Cost** | $0 (free Slack workspace) |
| **If Unavailable** | Falls back to email (Resend) or silent operation. Monitor still writes to Google Sheets. |

### Resend Email API

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Email notifications as alternative/supplement to Slack. Formal notification delivery. |
| **Setup** | Register at https://resend.com, get API key |
| **Our Client** | `govcon/notifications/notify.py` |
| **Env Variables** | `RESEND_API_KEY`, `RESEND_TO_EMAIL` |
| **Cost** | Free tier: 3,000 emails/month |
| **If Unavailable** | Slack serves as primary notification channel. |

### Google Sheets API v4

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Pipeline tracker. 3-tab spreadsheet (Pipeline, Dashboard, Contacts) that Newport can view and interact with. |
| **Setup** | Create Google Cloud service account, share spreadsheet with service account email |
| **Library** | `gspread` >= 5.12.0 + `google-auth` >= 2.23.0 |
| **Our Client** | `govcon/tracking/sheets_pipeline.py` |
| **Env Variables** | `GOOGLE_SHEETS_CREDS_PATH`, `GOOGLE_SHEETS_ID` |
| **Cost** | $0 |
| **If Unavailable** | Pipeline data still saved as local CSVs. Sheets is a convenience layer, not a dependency. |

---

## Procurement Platforms (Registration Required — No API)

These are web portals where Newport must register to receive and respond to solicitations. They don't have programmatic APIs — monitoring is manual or via email alert subscriptions.

### Unison Marketplace (BOP)

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Bureau of Prisons reverse auction platform for food procurement. BOP uses this for quarterly subsistence solicitations. **Required for bidding on BOP food POs.** |
| **URL** | https://www.unison.com/marketplace |
| **Setup** | Register as vendor, link to SAM.gov UEI, select NAICS/PSC categories |
| **Cost** | $0 (vendor registration is free) |
| **Status** | ⬜ Not yet registered. Must complete before first BOP bid. |
| **Priority** | HIGH — BOP is #1 FL small contract buyer ($5–7M/yr in FL food) |

### MyFloridaMarketPlace (MFMP)

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Florida state procurement portal. Required for all state agency and most SLED bids. |
| **URL** | https://vendor.myfloridamarketplace.com/ |
| **Cost** | 1% transaction fee on awarded contracts |
| **Status** | ⬜ Registration pending |
| **Priority** | HIGH — gateway to $1.04B FL school district food market |

### BidNet Direct

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Aggregated local/county government bid notifications across FL. Covers municipalities and special districts. |
| **URL** | https://www.bidnetdirect.com/ |
| **Cost** | Free basic tier (paid tiers for broader coverage) |
| **Status** | ⬜ Not yet registered |
| **Priority** | MEDIUM — FL county/municipal food procurement ($45M/yr est.) |

### DemandStar

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Local government bid aggregator. Covers FL counties, cities, and school districts not on MFMP. |
| **URL** | https://www.demandstar.com/ |
| **Cost** | Free basic tier |
| **Status** | ⬜ Not yet registered |
| **Priority** | MEDIUM |

### VendorLink (Broward County)

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Broward County's vendor self-service portal. Newport is based in Broward (Plantation, FL) — home county advantage. |
| **URL** | https://www.broward.org/Purchasing/VendorRegistration/ |
| **Cost** | $0 |
| **Status** | ⬜ Not yet registered |
| **Priority** | MEDIUM — local relationship + geographic proximity |

---

## Recommended Paid Platforms (Not Yet Integrated — Part of "Paid Route")

These platforms are recommended in the Newport proposal but are NOT currently integrated into the codebase. Integration would involve manual use of their web portals and/or API connections built in a future phase.

### CLEATUS

| Attribute | Detail |
|-----------|--------|
| **Purpose** | AI proposal engine, federal+state+local discovery, compliance checking, CRM, document hub |
| **URL** | https://www.cleat.ai/ |
| **Annual Cost** | $2,400–$3,600 (Essential tier) |
| **Integration** | Manual use initially. API integration possible for pipeline sync to Notion. |
| **Value** | Replaces manual bid prep effort. AI-assisted proposal writing. Solicitation "shredding" (parsing requirements). |

### HigherGov

| Attribute | Detail |
|-----------|--------|
| **Purpose** | SLED opportunity discovery across 40,000+ state/local/education agencies with NAICS-mapped alerts |
| **URL** | https://www.highergov.com/ |
| **Annual Cost** | $2,000–$5,000 (Standard tier) |
| **Integration** | Manual use. Email alerts. No current API integration needed. |
| **Value** | Covers the $600M–$1.2B FL SLED market invisible to free federal APIs. |

### GovSpend

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Micro-purchase and P-card spending data. 85M+ purchase orders below formal solicitation thresholds. |
| **URL** | https://govspend.com/ |
| **Annual Cost** | $3,000–$10,000 (Standard tier) |
| **Integration** | Manual use. Buyer contact identification. |
| **Value** | Makes visible the $8–15M/yr FL micro-purchase market that no free API covers. |

---

## Future Integrations (Commercial Outreach — Not Yet Built)

### Instantly

| Attribute | Detail |
|-----------|--------|
| **Purpose** | Automated email outreach sequences for commercial SDR |
| **URL** | https://instantly.ai/ |
| **Annual Cost** | $37–$97/mo ($444–$1,164/yr) |
| **Env Variable** | `INSTANTLY_API_KEY`, `INSTANTLY_SENDING_ACCOUNT` |
| **Status** | ❌ Not yet integrated. Client code from `goldmans-leadgen` repo needs adaptation. |

### Twilio

| Attribute | Detail |
|-----------|--------|
| **Purpose** | SMS follow-up for commercial outreach sequences |
| **URL** | https://twilio.com/ |
| **Annual Cost** | Usage-based (~$0.0079/SMS) |
| **Env Variables** | `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_*` |
| **Status** | ❌ Not yet integrated. |

### Retell AI

| Attribute | Detail |
|-----------|--------|
| **Purpose** | AI voice outreach for high-priority commercial prospects |
| **URL** | https://retellai.com/ |
| **Annual Cost** | Usage-based |
| **Env Variables** | `RETELL_API_KEY`, `RETELL_PHONE_*` |
| **Status** | ❌ Not yet integrated. |

---

## Integration Summary

| Service | Channel | Status | Cost | Priority |
|---------|---------|--------|------|----------|
| SAM.gov API | GovCon | ✅ Built | $0 | Critical |
| USASpending API | GovCon | ✅ Built | $0 | Critical |
| FPDS | GovCon | ⚠️ Sunsetting FY2026 | $0 | Migrate to SAM.gov |
| Grants.gov API | GovCon | ✅ Built | $0 | Medium |
| Apollo.io API | Commercial | ✅ Built | $0–$119/mo | Critical |
| Google Sheets API | GovCon | ✅ Built | $0 | High |
| Slack Webhooks | GovCon | ✅ Built | $0 | Medium |
| Resend Email | GovCon | ✅ Built | $0 | Low |
| Unison Marketplace | GovCon (BOP) | ⬜ Register | $0 | HIGH |
| MyFloridaMarketPlace | GovCon (SLED) | ⬜ Register | 1% tx fee | HIGH |
| BidNet Direct | GovCon (SLED) | ⬜ Register | $0 | MEDIUM |
| DemandStar | GovCon (SLED) | ⬜ Register | $0 | MEDIUM |
| VendorLink (Broward) | GovCon (SLED) | ⬜ Register | $0 | MEDIUM |
| CLEATUS | GovCon | ⬜ Recommended | $2,400–$3,600/yr | Paid Route |
| HigherGov | GovCon | ⬜ Recommended | $2,000–$5,000/yr | Paid Route |
| GovSpend | GovCon | ⬜ Recommended | $3,000–$10,000/yr | Paid Route |
| Instantly | Commercial | ❌ Future | $444–$1,164/yr | P1 |
| Twilio | Commercial | ❌ Future | Usage-based | P1 |
| Retell AI | Commercial | ❌ Future | Usage-based | P2 |

---

## Claude CLI Notes

When adding new integrations:
1. Follow the API client pattern in `govcon/enrichment/` or `commercial/enrichment/`
2. All API keys go in `.env` — never hardcode
3. Every client must have: `__init__` with key from env, `requests.Session`, `_request()` with 429 retry + exponential backoff, `stats` property
4. Add the env variable to `.env.example` with a comment explaining where to get the key
5. Update this document with the new integration details
