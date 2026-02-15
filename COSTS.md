# Goldman's Garage Door Lead Gen — Cost Breakdown

Last updated: 2026-02-14

---

## Current Monthly Subscriptions

| Service | Plan | Monthly Cost | What You Get | Status |
|---------|------|-------------|--------------|--------|
| Apollo.io | Basic | $49/mo | 2,520 email credits/mo, 75 mobile credits/mo, unlimited search | ACTIVE — ~600 credits used so far |
| Instantly.ai | Growth | $37/mo | 5,000 emails/mo, unlimited accounts + warmup, 1,000 contacts | ACTIVE — not yet sending |
| Retell AI | Pay-as-you-go | $0/mo base | Per-minute billing (see usage costs below) | ACTIVE — not yet calling |
| Twilio | Pay-as-you-go | $0/mo base | Per-SMS + per-number billing (see below) | ACTIVE — not yet sending |
| Google Cloud | Pay-as-you-go | $0/mo base | Places API (see usage costs below) | ACTIVE |
| OpenWeatherMap | Free tier | $0/mo | Weather alerts for storm monitoring | ACTIVE |
| Google Sheets | Free | $0/mo | CRM / lead tracking | ACTIVE |

**Current fixed monthly total: $86/mo** (Apollo + Instantly)

---

## Usage-Based Costs (Variable)

### Google Places API (Referral Partner Scraping)

Our field mask includes `nationalPhoneNumber`, `websiteUri`, `rating`, `userRatingCount` — these
are Enterprise-tier fields.

| SKU | Rate | Free Allowance |
|-----|------|----------------|
| Text Search Enterprise | $0.035/request | 1,000 free requests/mo |

**What we used:** ~350 API requests for the initial full scrape (all 7 ICP categories across 3 markets).
That's within the 1,000/mo free tier = **$0 for the first run**.

Re-running monthly: ~350 requests/mo stays within free tier.

### Apollo.io Credits (Lead Enrichment)

| Action | Credit Cost | Volume So Far |
|--------|------------|---------------|
| People Search | 0 (free) | ~1,011 searches |
| Email Reveal | 1 credit | ~600 reveals |
| Organization Enrich | 1 credit | Not used |
| Additional credits (if you exceed 2,520/mo) | $0.20 each | N/A yet |

**What we used:** ~600 of 2,520 monthly credits = **$0 extra** (included in $49/mo).
Remaining: 1,920 credits this billing cycle.

### Twilio (SMS Outreach)

| Item | Cost |
|------|------|
| Local phone number (MI) | $1.15/mo |
| Local phone number (NC) | $1.15/mo |
| Outbound SMS | ~$0.0079/segment + carrier surcharge |
| Inbound SMS (replies) | ~$0.0079/segment |

**Not yet purchased.** Two numbers needed = $2.30/mo.

Estimated SMS campaign cost (1,000 leads):
- 1,000 outbound texts x $0.0079 = ~$8
- Plus carrier surcharges (~$0.003-0.006/msg) = ~$3-6
- **Total for 1,000 SMS: ~$11-14**

### Retell AI (Voice Outreach)

| Component | Cost/Minute |
|-----------|-------------|
| Voice engine (ElevenLabs) | $0.07-0.08 |
| LLM (GPT-4.1) | ~$0.04-0.06 |
| Knowledge base | $0.005 |
| Batch calling | $0.005/dial |
| Branded caller ID | $0.10/call |
| **Estimated total per minute** | **$0.15-0.25** |

Estimated voice campaign cost (100 calls, avg 2 min each):
- 200 minutes x $0.20/min = ~$40
- Plus per-dial fees = ~$1
- **Total for 100 voice calls: ~$41**

### Instantly.ai (Email Outreach)

Growth plan includes 5,000 emails/mo. At pilot scale this is sufficient.
No per-email overage expected during pilot.

**Cost: $0 extra** (included in $37/mo subscription).

---

## Lead Sourcing Costs by Channel

### Channel 1: Google Maps Referral Partners (1,011 leads sourced)

| Step | Tool | Cost |
|------|------|------|
| Scrape businesses | Google Places API | $0 (within free tier) |
| Enrich with decision-maker email | Apollo.io | $0 (within $49/mo plan) |
| **Total cost to source 1,011 referral leads** | | **$0 variable** |

Results: 514 emails (51%), 992 phones (98%), 996 reachable (99%)

### Channel 2: Active Home Listings / Warranty Leads (9,049 listings, 6,014 warranty leads)

| Step | Tool | Cost |
|------|------|------|
| Scrape active listings | HomeHarvest (Realtor.com) | $0 (free library) |
| Extract listing agents | Built into scraper | $0 |
| Warranty classification | Built into scraper | $0 |
| **Total cost to source** | | **$0** |

Results: 4,339 listing agents (91% with email), 6,014 warranty-risk properties

### Channel 3: Storm Leads (6,313 leads in test run)

| Step | Tool | Cost |
|------|------|------|
| Weather monitoring | OpenWeatherMap | $0 (free tier) |
| Scrape storm-zone listings | HomeHarvest | $0 |
| Scrape recent buyers | HomeHarvest | $0 |
| Insurance agent data | Pre-enriched via Apollo | Already counted above |
| **Total cost to source** | | **$0** |

### Channel 4: Competitor Review Mining (139 competitors, 36 negative reviews)

| Step | Tool | Cost |
|------|------|------|
| Find competitors | Google Places API | $0 (within free tier) |
| Pull reviews | Google Places API | $0 (within free tier) |
| Analyze complaint themes | Built into scraper | $0 |
| **Total cost to source** | | **$0** |

### Channel 5: Homeowner Seller Contact Info (NOT YET BUILT)

| Step | Tool | Cost |
|------|------|------|
| Get addresses | Already have from active listings | $0 |
| Match to county assessor records | Free county data downloads | $0 |
| Skip trace for phone + email | Tracerfy API | $0.02/record |
| DNC scrub | Tracerfy add-on | $0.02/phone |
| **Cost per lead** | | **~$0.04/lead** |

Estimated cost for 9,049 active listings:
- Skip trace: 9,049 x $0.02 = $181
- DNC scrub: 9,049 x $0.02 = $181
- **Total: ~$362 one-time**

Monthly ongoing (~2,000 new listings/mo): **~$80/mo**

---

## Outreach Costs per Lead (Estimated)

| Channel | Cost/Lead | Notes |
|---------|-----------|-------|
| Email only (Instantly) | ~$0.007 | 5,000 emails included in $37/mo |
| SMS only (Twilio) | ~$0.011-0.014 | Per-segment + carrier fees |
| Voice call (Retell, 2 min avg) | ~$0.40-0.50 | Most expensive channel |
| Email + SMS combo | ~$0.02 | Recommended for most ICPs |
| Email + Voice (high-priority) | ~$0.41-0.51 | Reserve for P1 referral partners |

---

## Pilot Month Budget Estimate

Assuming pilot focuses on the leads already sourced (no skip tracing yet):

### Fixed Costs
| Item | Cost |
|------|------|
| Apollo.io Basic | $49 |
| Instantly.ai Growth | $37 |
| Twilio phone numbers (2) | $2.30 |
| **Fixed subtotal** | **$88.30/mo** |

### Variable Costs (Pilot Outreach Volume)
| Activity | Volume | Cost |
|----------|--------|------|
| Email campaign to referral partners | 500 emails | $0 (in plan) |
| SMS to new homeowners / warranty leads | 500 texts | ~$7 |
| AI voice calls to top agents + builders | 50 calls (2 min avg) | ~$20 |
| Google Places API (re-scrape) | ~350 requests | $0 (free tier) |
| **Variable subtotal** | | **~$27** |

### Pilot Month Total: ~$115

---

## Scale Scenario: Full Market Operation

Running all channels monthly across all 3 markets:

### Fixed Costs
| Item | Monthly |
|------|---------|
| Apollo.io Basic | $49 |
| Instantly.ai Growth | $37 |
| Twilio numbers (2) | $2.30 |
| DNC Registry (3 area codes) | ~$19 ($225/yr) |
| **Fixed subtotal** | **$107/mo** |

### Variable Costs (Full Volume)
| Activity | Volume | Monthly Cost |
|----------|--------|-------------|
| Email campaigns | 5,000/mo | $0 (in plan) |
| SMS campaigns | 2,000/mo | ~$22 |
| AI voice calls | 200 calls/mo | ~$80 |
| Apollo enrichment (new leads) | 500 reveals/mo | $0 (in plan) |
| Skip tracing (homeowner sellers) | 2,000/mo | $40 |
| DNC scrub | 2,000/mo | $40 |
| Google Places re-scrape | ~350/mo | $0 (free tier) |
| **Variable subtotal** | | **~$182/mo** |

### Full Operation Total: ~$289/mo

---

## What's Free

| Tool | What It Does | Why It's Free |
|------|-------------|---------------|
| HomeHarvest | Scrapes Realtor.com listings | Open-source Python library |
| County assessor data | Owner names + mailing addresses | Public records (all 5 counties) |
| OpenWeatherMap | Storm alerts | Free API tier |
| Google Sheets | CRM / tracking | Google free tier |
| Apollo People Search | Find decision makers | 0-credit searches |
| Google Places API | Business discovery | 1,000 free Enterprise requests/mo |

---

## Not Yet Purchased (Pending)

| Item | Cost | When Needed |
|------|------|-------------|
| Twilio MI phone number | $1.15/mo | Before SMS/voice outreach |
| Twilio NC phone number | $1.15/mo | Before SMS/voice outreach |
| Retell MI phone number | TBD (may use Twilio number) | Before AI voice calls |
| Retell NC phone number | TBD (may use Twilio number) | Before AI voice calls |
| Skip tracing credits (Tracerfy) | ~$0.02/record | When homeowner seller pipeline is built |
| DNC Registry access | $75/yr per area code | Before any cold calling |

---

## Credit/Usage Tracking

### Apollo.io (resets each billing cycle)
- Plan: Basic (2,520 email credits/mo)
- Used this cycle: ~600
- Remaining: ~1,920

### Instantly.ai (resets monthly)
- Plan: Growth (5,000 emails/mo, 1,000 contacts)
- Used: 0
- Remaining: 5,000 emails, 1,000 contacts

### Google Places API (resets monthly)
- Free tier: 1,000 Enterprise requests/mo
- Used this month: ~350
- Remaining: ~650

---

## Sources

- [Apollo.io Pricing](https://www.apollo.io/pricing)
- [Instantly.ai Pricing](https://instantly.ai/pricing)
- [Retell AI Pricing](https://www.retellai.com/pricing)
- [Twilio SMS Pricing](https://www.twilio.com/en-us/sms/pricing/us)
- [Twilio Phone Number Pricing](https://help.twilio.com/articles/223182908-How-much-does-a-phone-number-cost-)
- [Google Maps Platform Pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- [Google Places API Usage & Billing](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing)
- [Tracerfy Skip Tracing Pricing](https://www.tracerfy.com/pricing)
