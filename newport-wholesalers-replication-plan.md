# Newport Wholesalers — AI SDR Replication Plan

> Replicating the Goldman's Garage Door leadgen system for Newport Wholesalers, Inc.
> Wholesale grocery distribution → B2B outreach to grocery stores, supermarkets, convenience stores, and independent retailers.

---

## Architecture Overview

The Goldman's system has 3 layers. Here's what happens to each:

| Layer | Goldman's | Newport | Action |
|-------|-----------|---------|--------|
| **Core Engine** | Instantly, Twilio, Retell, Apollo, CRM, Orchestrator | Same tools | **Copy as-is** |
| **Config** | Garage door ICPs, MI/NC markets, home service queries | Wholesale ICPs, new markets, grocery queries | **Rebuild** |
| **Data/Templates** | Storm leads, homeowner scraping, garage door messaging | Grocery store leads, wholesale messaging | **Rebuild** |

---

## Step-by-Step Execution Plan

### PHASE 1: Scaffold the New Repo

**Step 1 — Clone the structure (strip Goldman's data)**

Open your VS Code terminal and run:

```powershell
# Create the new project folder
New-Item -ItemType Directory -Path "C:\Users\USER\newport-leadgen" -Force

# Copy the full structure
Copy-Item -Path "C:\Users\USER\goldmans-leadgen\*" -Destination "C:\Users\USER\newport-leadgen\" -Recurse -Force

# Remove Goldman's-specific data files
Remove-Item -Path "C:\Users\USER\newport-leadgen\data\*" -Recurse -Force
Remove-Item -Path "C:\Users\USER\newport-leadgen\logs\*" -Recurse -Force

# Recreate empty data folders
New-Item -ItemType Directory -Path "C:\Users\USER\newport-leadgen\data\raw" -Force
New-Item -ItemType Directory -Path "C:\Users\USER\newport-leadgen\data\enriched" -Force
New-Item -ItemType Directory -Path "C:\Users\USER\newport-leadgen\data\clay_ready" -Force
New-Item -ItemType Directory -Path "C:\Users\USER\newport-leadgen\data\competitor_intel" -Force
New-Item -ItemType Directory -Path "C:\Users\USER\newport-leadgen\logs" -Force

# Remove storm-specific folders (not needed)
Remove-Item -Path "C:\Users\USER\newport-leadgen\data\storm_leads" -Recurse -Force -ErrorAction SilentlyContinue

# Remove Goldman's credentials and env
Remove-Item -Path "C:\Users\USER\newport-leadgen\.env" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Users\USER\newport-leadgen\credentials.json" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Users\USER\newport-leadgen\twilio_2FA_recovery_code.txt" -Force -ErrorAction SilentlyContinue
```

**Step 2 — Open the new project in VS Code**

```powershell
code "C:\Users\USER\newport-leadgen"
```

---

### PHASE 2: Rebuild Config Files

These are the 3 files that define WHO you target, WHERE, and HOW you find them. Give each of the following prompts to Claude CLI inside the newport-leadgen project.

**Step 3 — New .env.example**

> Claude CLI Prompt:
```
Replace the contents of .env.example with a new version for Newport Wholesalers, Inc. — a wholesale grocery distributor. Keep the same API service structure (Instantly, Twilio, Retell, Apollo, Google Places, Google Sheets) but:
- Change INSTANTLY_SENDING_ACCOUNT to a placeholder for Newport
- Remove OPENWEATHER_API_KEY (no storm monitoring needed)
- Remove TAL_PHONE_NUMBER, replace with NEWPORT_SALES_PHONE
- Keep TWILIO and RETELL phone vars but rename from MI/NC to match Newport's actual markets (we'll define markets next)
- Add any notes as comments
```

**Step 4 — New markets.json**

> ⚠️ IMPORTANT: Before running this prompt, you need to know Newport Wholesalers' service areas/markets. Answer these questions first:
> - What geographic areas does Newport serve? (states, metro areas, counties)
> - Do they have warehouses or distribution centers in specific locations?
> - What's their delivery radius?

> Claude CLI Prompt (fill in the blanks):
```
Replace config/markets.json for Newport Wholesalers, Inc. Follow the exact same JSON structure as the current file but with Newport's markets:

Markets to define: [FILL IN — e.g., "Greater Philadelphia PA", "Central New Jersey", "Delaware Valley"]

For each market include:
- name, state, region
- phone_area_code (for Twilio/Retell)
- major_cities (where grocery stores and supermarkets are concentrated)
- zip_codes (key commercial zip codes in the territory)
```

**Step 5 — New icp_definitions.json**

> Claude CLI Prompt:
```
Replace config/icp_definitions.json for Newport Wholesalers, Inc. — a wholesale distributor of grocery products (dry goods, confectionery, national brands).

Newport sells in bulk to retail buyers. Define these ICP types:

1. "independent_grocery_stores" — Priority 1, email + ai_call
   Small/mid-size independent grocery stores that buy from distributors rather than direct from manufacturers

2. "convenience_stores" — Priority 1, email + ai_call
   Corner stores, bodegas, c-stores that need reliable wholesale supply

3. "supermarkets" — Priority 1, email + ai_call
   Regional supermarket chains and larger grocery retailers

4. "dollar_stores" — Priority 2, email
   Dollar stores and discount retailers that carry grocery/confectionery items

5. "gas_station_marts" — Priority 2, email
   Gas station convenience shops that stock snacks, candy, dry goods

6. "specialty_food_stores" — Priority 2, email
   Ethnic grocery stores, international food markets, specialty shops

7. "food_service_distributors" — Priority 3, email
   Potential B2B partnerships with other distributors for cross-selling

8. "restaurant_supply" — Priority 3, email
   Restaurant supply companies that might add grocery wholesale lines

Follow the exact JSON structure from the current file. For each ICP include:
- icp_type, display_name, pipeline (either "direct_to_customer" or "referral_partner")
- why (business rationale)
- outreach_channels, priority, email_campaign name
- value_prop (what Newport offers — bulk pricing, reliable delivery, national brands, flexible minimums, dedicated account rep, weekly delivery routes)
```

**Step 6 — New search_queries.json**

> Claude CLI Prompt (fill in market names from Step 4):
```
Replace config/search_queries.json for Newport Wholesalers. Use the markets defined in config/markets.json.

For each ICP type, create Google Maps search queries to find these businesses in each market city:

- independent_grocery_stores: "grocery store", "supermarket", "food market"
- convenience_stores: "convenience store", "corner store", "bodega", "mini mart"
- supermarkets: "supermarket", "grocery chain"
- dollar_stores: "dollar store", "discount store"
- gas_station_marts: "gas station", "fuel station"
- specialty_food_stores: "international grocery", "ethnic food store", "specialty food market", "Asian grocery", "Hispanic grocery"
- food_service_distributors: "food distributor", "wholesale food"
- restaurant_supply: "restaurant supply store"

Follow the exact JSON structure. Set appropriate min_rating and min_reviews thresholds (lower for convenience/dollar stores, higher for specialty).
```

---

### PHASE 3: Rebuild Templates

**Step 7 — New email templates**

> Claude CLI Prompt:
```
Replace ALL files in outreach/email/templates/ with new templates for Newport Wholesalers, Inc.

Newport is a wholesale grocery distributor selling national brand dry goods and confectionery in bulk. Create these email campaign templates (JSON format matching the current template structure):

1. independent_grocery.json — "Tired of unreliable suppliers?" angle. Emphasize: competitive pricing, consistent stock, weekly delivery, flexible order minimums.

2. convenience_store.json — "Stock what sells" angle. Emphasize: top-selling national brands, candy/snack variety packs, fast restock, no minimum headaches.

3. supermarket.json — "Volume pricing that makes sense" angle. Emphasize: bulk discounts, full catalog of national brands, dedicated account manager, reliable logistics.

4. dollar_discount.json — "Wholesale prices that protect your margins" angle. Emphasize: lowest wholesale cost on confectionery and dry goods, case-break options, consistent supply.

5. specialty_food.json — "Expand your selection with national brands" angle. Emphasize: complement their specialty items with recognizable national brands customers expect.

6. gas_station.json — "Keep your shelves full between deliveries" angle. Emphasize: snacks, candy, impulse buys, fast turnaround.

7. partner_distributor.json — B2B partnership angle for cross-selling with other distributors.

8. restaurant_supply.json — Partnership angle for restaurant supply companies.

Each template should have 3-step email sequence (initial, follow_up_1, follow_up_2) with subject lines and body text. Keep copy punchy and benefit-driven — no fluff.

Remove all old Goldman's templates (storm_response.json, agent_partner.json, etc.)
```

**Step 8 — New SMS templates**

> Claude CLI Prompt:
```
Replace ALL files in outreach/sms/templates/ with new templates for Newport Wholesalers.

Create:
1. new_prospect.json — First touch SMS to a grocery/convenience store owner
2. follow_up.json — Follow-up after email with no response
3. reorder_reminder.json — For existing customers (future use)
4. partner_intro.json — For distributor partnership outreach

Keep messages under 160 characters where possible. Professional but conversational tone. Include a clear CTA in each.

Remove all old Goldman's SMS templates.
```

**Step 9 — New voice scripts**

> Claude CLI Prompt:
```
Replace ALL files in outreach/voice/scripts/ with new Retell AI voice call scripts for Newport Wholesalers.

Create:
1. independent_grocery.json — Cold call script for independent grocery store owners/managers
2. convenience_store.json — Cold call to c-store owners
3. supermarket.json — Call to supermarket purchasing managers
4. partner_intro.json — Partnership call to other distributors

Each script should include:
- Opening (who we are, why we're calling)
- Value prop (2-3 key benefits)
- Qualifying questions (current supplier satisfaction, order volume, pain points)
- Close (schedule a catalog review / sample delivery)
- Objection handling (already have a supplier, pricing concerns, minimum orders)
- Warm transfer trigger (when to transfer to Newport's sales team)

Remove all old Goldman's voice scripts.
```

---

### PHASE 4: Update Scrapers

**Step 10 — Remove Goldman's-specific scrapers**

> Claude CLI Prompt:
```
In the scrapers/ directory:
1. Delete weather_monitor.py (no storm targeting needed)
2. Delete storm_lead_scraper.py (no storm leads)
3. Delete homeowner_scraper.py (no homeowner targeting)
4. Delete active_listings_scraper.py (no real estate listings)

Keep:
- gmaps_scraper.py (we still scrape Google Maps for business leads)
- clay_formatter.py (still format for Clay enrichment)
- competitor_review_scraper.py (useful for competitive intel on other distributors)
- __init__.py

Update __init__.py to remove imports for deleted scrapers.
```

**Step 11 — Update gmaps_scraper.py references**

> Claude CLI Prompt:
```
Review scrapers/gmaps_scraper.py and update any Goldman's-specific references:
- Update any hardcoded business names or categories
- Make sure it reads from the new config/search_queries.json structure
- Ensure the ICP type field names match our new icp_definitions.json
- If there are any garage-door-specific filtering logic, generalize it for wholesale grocery targets
```

---

### PHASE 5: Update Supporting Files

**Step 12 — Update README.md**

> Claude CLI Prompt:
```
Rewrite README.md for Newport Wholesalers, Inc. Lead Generation System.

Same structure as current but updated for:
- Company: Newport Wholesalers, Inc. — wholesale grocery distribution
- Pipelines: Direct-to-Customer (grocery stores, c-stores, supermarkets, etc.) and B2B Partners (other distributors, restaurant supply)
- Tech stack: Same tools (Google Places, Clay, Instantly, Twilio, Retell, Google Sheets)
- Remove HomeHarvest and OpenWeather references
- Update project structure description
```

**Step 13 — Update orchestrator references**

> Claude CLI Prompt:
```
Review orchestrator/campaign_runner.py and orchestrator/__main__.py:
- Remove any storm-monitoring logic or weather-triggered campaign launches
- Update ICP type references to match our new icp_definitions.json
- Make sure campaign routing logic works with the new email/sms/voice template names
- Keep the general campaign orchestration flow intact
```

**Step 14 — Update outreach client references**

> Claude CLI Prompt:
```
Review these files and update Goldman's-specific references:
- outreach/email/instantly_client.py — update any hardcoded sender names or campaign references
- outreach/sms/twilio_sender.py — update any Goldman's references
- outreach/voice/retell_config.py — update agent name, company info, greeting scripts
- outreach/voice/retell_client.py — update any hardcoded references

Replace "Goldman's" / "Goldman's Garage Door" with "Newport Wholesalers" throughout. Replace "Tal" with a generic sales contact placeholder.
```

**Step 15 — Update CRM and tracking**

> Claude CLI Prompt:
```
Review crm/sheets_manager.py, crm/setup_crm.py, tracking/sheets_crm.py, and tracking/dashboard.py:
- Update any Goldman's-specific column names or sheet references
- Update ICP category labels to match new icp_definitions.json
- Update any status labels (e.g., "storm_response" → remove)
- Keep the Google Sheets CRM structure intact, just adapt labels
```

---

### PHASE 6: Final Setup

**Step 16 — Create new .env file**

Copy `.env.example` to `.env` and fill in your actual API keys. You'll need:
- New Instantly.ai sending account for Newport
- Twilio phone numbers for Newport's markets
- Retell AI phone numbers for Newport's markets
- Newport sales team phone number for warm transfers
- Google Places API key (can reuse if on same account)
- Apollo API key (can reuse if on same account)
- Google Sheets credentials for Newport's CRM

**Step 17 — Test the pipeline**

> Claude CLI Prompt:
```
Run a dry-run test of the full pipeline:
1. Run the gmaps_scraper for one market, one ICP type (e.g., convenience_stores in one city) — verify it finds and formats results
2. Check that clay_formatter.py outputs correctly for the new ICP structure
3. Verify the orchestrator can load all new configs without errors
4. Send a test email through Instantly with the new template
5. Send a test SMS through Twilio
6. Make a test Retell call with the new script

Report any errors or config mismatches.
```

---

## Before You Start Checklist

Before running Phase 2, gather this info about Newport Wholesalers:

- [ ] **Markets/territories** — What geographic areas do they serve? Cities, counties, states?
- [ ] **Warehouse locations** — Where do they ship from?
- [ ] **Delivery radius** — How far do they deliver?
- [ ] **Product catalog highlights** — Key brands, best sellers, product categories
- [ ] **Sales contact** — Name and phone number for warm transfers
- [ ] **Sending domain** — Email domain for Instantly (e.g., sales@newportwholesalers.com)
- [ ] **Differentiators** — What makes them better than competing distributors? (pricing, delivery speed, minimums, service, catalog breadth)
- [ ] **Current customers** — Any example customer types to inform messaging?

---

## File Change Summary

| File/Folder | Action |
|---|---|
| `.env` / `.env.example` | Rebuild for Newport |
| `config/icp_definitions.json` | Rebuild — new ICPs |
| `config/markets.json` | Rebuild — new markets |
| `config/search_queries.json` | Rebuild — new search queries |
| `outreach/email/templates/*` | Rebuild — all new templates |
| `outreach/sms/templates/*` | Rebuild — all new templates |
| `outreach/voice/scripts/*` | Rebuild — all new scripts |
| `scrapers/weather_monitor.py` | Delete |
| `scrapers/storm_lead_scraper.py` | Delete |
| `scrapers/homeowner_scraper.py` | Delete |
| `scrapers/active_listings_scraper.py` | Delete |
| `scrapers/__init__.py` | Update imports |
| `scrapers/gmaps_scraper.py` | Update references |
| `orchestrator/*` | Update ICP/campaign references |
| `outreach/*/client files` | Find-replace Goldman's → Newport |
| `crm/*` | Update labels |
| `tracking/*` | Update labels |
| `README.md` | Rewrite |
| `data/*` | Cleared — fresh start |
| `data/storm_leads/` | Deleted entirely |
| Core engine files | **No changes needed** |
