# Newport Wholesalers — Requirements

> **Last Updated**: February 24, 2026
> **Status**: Draft
> **Depends On**: [01-VISION.md](./01-VISION.md)

## Overview

This document specifies every deliverable, capability, and output required for the Newport engagement. Requirements are organized by channel (GovCon, Commercial SDR, Cross-Channel) and prioritized by delivery order. Each requirement includes acceptance criteria that remove ambiguity about what "done" looks like.

---

## Functional Requirements

### P0 — Must Have (GovCon Proposal Package)

These requirements must be complete before presenting to Newport ownership.

---

#### FR-001: Two-Routes Analysis (Free vs. Paid)

**As** Newport ownership, **I need to** understand the two investment paths for entering government contracting, **so that** I can make an informed decision about how much to invest upfront.

**Acceptance Criteria:**
- [ ] Side-by-side comparison showing: cost (Year 1 and ongoing), market coverage (% of TAM visible), bid capacity (bids/year), expected win rate, time to first simplified-acquisition eligibility
- [ ] Free route shows: SAM.gov + FPDS + USASpending (free APIs), manual portal monitoring, DIY bid prep — covers ~40–50% of market
- [ ] Paid route shows: CLEATUS + HigherGov + GovSpend + free APIs — covers ~90% of market, 2–3x bid volume, higher win rates from better intelligence
- [ ] Expected outcomes table: Year 1 contracts won, Year 1 revenue, 5-year cumulative revenue, 5-year owner earnings — for each route
- [ ] Recommendation with clear rationale (paid route pays for itself by mid-Year 2)
- [ ] Appears in both the Excel model ("Two Routes" sheet) and the presentation deck

**Notes:** The v7 financial model already has a "Two Routes" sheet. Validate it matches the current research data. The deck needs a dedicated slide for this comparison.

---

#### FR-002: Total Addressable Market Analysis

**As** Newport ownership, **I need to** see defensible market sizing for government food procurement in Florida and the Southeast, **so that** I can evaluate whether the opportunity justifies the investment.

**Acceptance Criteria:**
- [ ] Market waterfall from national → Florida → Newport's serviceable addressable market (SAM), with dollar values and award counts at each level
- [ ] TAM waterfall slide: $87M (FL federal food under $350K, all PSC 89xx, USASpending confirmed) → filter locked SPV contracts → filter product categories outside Newport's range → filter unreachable geographies → **$17–20M biddable by Newport**
- [ ] Breakdown by contract tier: micro-purchase (<$15K, 83% of awards), simplified ($15K–$350K, 14.4%), sealed bid (>$350K, 2.2%)
- [ ] Florida federal food TAM: **$87M / 39,857 awards** (USASpending API, FY2024, re-confirmed Feb 24, 2026)
- [ ] Southeast regional TAM: $179M (if multi-state delivery — depends on Newport's answer to delivery radius question)
- [ ] SLED estimate upgraded to **MEDIUM confidence**: FL school districts **$1.04B/yr** (USDA-derived: $358/student × 2.9M students, top 10 districts individually sized — Miami-Dade $82.25M, Broward $56.1M, etc.), FL county/municipal $45M/yr, FL DOC **explicitly excluded** (Aramark Contract C3021, $86.7M/yr through April 2027, not biddable)
- [ ] BOP facility-level breakdown: FCC Coleman $2.0–2.5M, FCI Miami $800K–1.2M, FCI Marianna $800K–1.0M, FCI Tallahassee $500–700K, FPC Pensacola $500–700K, FDC Miami $300–500K — **total FL BOP $5–7M/yr**
- [ ] VA entry vector specified: national SPV (US Foods, $263M) **excludes fresh bread, fresh milk, and fresh produce** — these categories purchased locally through BPAs/micro-purchases, estimated **$3–5M/yr across FL's 7 VA medical centers**
- [ ] Category breakdown by PSC code showing Newport's fit (HIGHEST: Confectionery 8925, HIGH: Produce 8915, MODERATE: Dairy 8910, etc.)
- [ ] Confectionery gap highlighted: **$55.5M national** (USASpending API, re-confirmed Feb 24, 2026), only **$412K** in FL competition, **1 registered federal contractor nationally under NAICS 424450** — Newport's beachhead
- [ ] All data points cite source and date (e.g., "USASpending API, FY2024, confirmed Feb 24, 2026")
- [ ] Confidence levels marked on every estimate (HIGH = live API data, MEDIUM = extrapolated from verified formula, LOW = industry estimates)
- [ ] Appears in Excel ("Market Analysis" sheet) and deck (2–3 slides including TAM waterfall)

**Notes:** Most data exists in `govcon/docs/research.md`. The $87M and $17–20M SAM are both defensible — present both as the honest waterfall shows disciplined market sizing, not pie-in-the-sky claims. SLED school district numbers now have a per-student formula ($358/yr from USDA NSLP data) that makes them verifiable. FL DOC must be in "Not Addressable" column with clear explanation. BOP Unison Marketplace registration is a prerequisite for bidding on BOP food POs — see [INTEGRATIONS.md](./09-INTEGRATIONS.md).

---

#### FR-003: Contract Pipeline Projections (5-Year Model)

**As** Newport ownership, **I need to** see a 5-year projection of bids, wins, revenue, and owner earnings, **so that** I can evaluate the financial trajectory and decide which scenario fits my risk appetite.

**Acceptance Criteria:**
- [ ] Five tiers modeled separately: Micro (<$15K), Simplified ($15K–$250K), Set-Aside (SDB/HUBZone), SLED (State/Local/Ed), Sealed Bid ($250K+)
- [ ] Bid volume per tier per year, with strategic narrative (micro phases OUT, simplified/SLED phase IN)
- [ ] Win rates by tier AND by competition density, escalating over 5 years as past performance accumulates. Win rates must be justified by FPDS competition data, not assumed generically:
  - **Low-competition categories** (15 NAICS/agency combos, $64.8M, 233 awards): DoD NAICS 424490 = 93% sole source, avg 1.2 offers/award. Confectionery NAICS 424450 = 58% sole source, avg 1.6 offers, **1 registered federal contractor nationally**. Forest Service NAICS 722310 = 100% sole source. Win rates in these categories should be **25–40% Year 1, 40–55% Year 3** — agencies posting requirements and receiving zero or one bid.
  - **Moderate-competition categories** (11 combos, $55.3M, 258 awards): DoD NAICS 424410 avg 2.4 offers, BOP NAICS 424490 avg 3.2 offers. Win rates: **12–18% Year 1, 20–30% Year 3**.
  - **High-competition categories** (4 combos, $25.4M, 33 awards): Avoid initially. Win rates: **5–8% Year 1**.
  - **Post-fraud tailwind adjustment**: 1,091 firms suspended (25% of 8(a) program, Jan 2026), multi-agency audits ongoing. Agencies with recurring food contracts are actively losing vendors — Newport's 30-year clean history is a warm introduction, not a cold bid. Apply a **+5–10% tailwind adjustment** to all categories for the first 12–18 months while the enforcement wave plays out. This is not speculative — it's the documented result of SBA, DoW, Treasury, and GSA actions taken in December 2025–January 2026 (sources: SBA.gov, Holland & Knight).
  - Blended Year 1 win rate across all categories: ~20–25% (weighted by bid volume toward low-competition targets). This is higher than the generic 15% "new entrant" assumption because Newport is deliberately targeting low-competition categories first, not bidding randomly.
- [ ] Renewal/recompete rate: 70% of contracts renew to incumbent — this is the compounding flywheel
- [ ] Revenue split: new wins vs. renewal base — must show renewals becoming dominant by Year 3
- [ ] Owner earnings calculation: Revenue → COGS → Gross Profit → Bid Prep → Fulfillment Overhead → Program Costs → Owner Earnings
- [ ] Cumulative owner earnings: negative Year 1 (investment), breakeven mid-Year 2, $500K–$840K cumulative by Year 5
- [ ] Portfolio shift visualization: Year 1 = mostly micro, Year 5 = mostly simplified/SLED/renewals
- [ ] All calculations driven by editable inputs (not hardcoded)
- [ ] Three scenarios tied to investment path AND competition targeting:
  - **Conservative** (free tools, broad bidding): Lower bid volume, generic win rates (15% micro, 10% simplified), limited market visibility. ~$50K Year 1 revenue.
  - **Moderate** (paid tools, targeted bidding): Higher bid volume focused on low-competition categories, competition-informed win rates (25% micro in low-competition, 15% simplified), SLED portals active. ~$100K–$150K Year 1 revenue.
  - **Aggressive** (full paid stack, active relationship building): Maximum bid volume, low-competition targeting + account-based outreach to contracting officers, post-fraud tailwind fully leveraged. ~$150K–$250K Year 1 revenue.

**Notes:** The v7 Excel model implements most of this. Key refinements needed: (1) **differentiate win rates by competition density** — the 93% sole source rate at DoD and 1 registered contractor nationally in confectionery justify materially higher rates than generic "new entrant" assumptions, (2) model should have a "Competition Density" input section where each NAICS/agency combo's avg offers and sole source % feed into win rate calculations, (3) ensure the "phase out micro" narrative is clear in the numbers, (4) confirm the compounding renewal math is correct. The three scenarios should reflect not just tool investment but **how aggressively Newport targets low-competition categories** — this is the primary lever, not just spending on platforms.

---

#### FR-004: Key Questions for Newport Ownership

**As** Newport ownership, **I need to** see the specific questions whose answers change every number in the model, **so that** I feel respected (you didn't assume you know my business) and understand what information I need to provide.

**Acceptance Criteria:**
- [ ] 10 questions, prioritized by impact (HIGHEST → INFO)
- [ ] Each question shows: what changes if YES, what changes if NO
- [ ] Critical questions include: minimum profitable order size, set-aside eligibility, delivery radius, food safety certifications, willingness to invest
- [ ] Questions are phrased in plain business English (not government procurement jargon)
- [ ] Appears as dedicated sheet in Excel model AND as a section in the presentation deck
- [ ] Space/cells for Newport to write their answers directly in the Excel file

**Notes:** v7 "Key Questions" sheet is excellent. Ensure the deck mirrors these questions so they can be discussed in person.

---

#### FR-005: Real Contract Examples

**As** Newport ownership, **I need to** see examples of actual government food contracts that Newport would bid on, **so that** the opportunity feels concrete rather than abstract.

**Acceptance Criteria:**
- [ ] 8–12 example contracts spanning all tiers (micro through sealed bid)
- [ ] Each example includes: buyer/agency, description, NAICS code, value range, location, product type, frequency
- [ ] Examples are representative composites based on real USASpending/FPDS award data (cited)
- [ ] Include at least 2 FL-specific examples (BOP, VA, school district, military base)
- [ ] Include at least 1 FEMA/disaster example (leveraging FL warehouse in hurricane zone)
- [ ] Include at least 1 confectionery-specific example (Newport's core strength)
- [ ] Appears in Excel ("Example Contracts" or within "Market Analysis" sheet) and referenced in deck

**Notes:** v7 Market Analysis sheet has a solid contract examples section. The deck should feature 3–4 of the most compelling examples with enough detail to feel real.

---

#### FR-006: Competitive Landscape

**As** Newport ownership, **I need to** understand who Newport would compete against and why we can win, **so that** I'm confident this isn't a market dominated by players we can't beat.

**Acceptance Criteria:**
- [ ] Top 10 FL food contract holders with government revenue and category focus
- [ ] Clear positioning: competitors #5–10 are small FL companies doing $1–5M — Newport's infrastructure and pricing are competitive in this tier
- [ ] **Full low-competition universe**: 15 NAICS/agency combos rated LOW competition covering 233 awards worth $64.8M — nearly half the biddable universe by award count. This is Newport's primary target zone.
- [ ] **Three headline competition stats** (must appear in deck):
  1. **DoD food purchasing (NAICS 424490)**: 93% sole source, avg 1.2 offers/award, $9.1M across 117 awards. Military bases are posting food requirements and getting zero or one bid. Newport shows up = Newport wins.
  2. **Confectionery (NAICS 424450)**: 1 registered federal contractor nationally, 58% sole source, avg 1.6 offers, $55.5M national market. Newport's beachhead — virtually zero competition.
  3. **Forest Service (NAICS 722310)**: 100% sole source, $43.1M, 98 awards. Remote food delivery — geographically challenging but high value if Newport's delivery radius reaches North FL.
- [ ] Competition density breakdown by level: LOW (15 combos, $64.8M) → MODERATE (11 combos, $55.3M) → HIGH (4 combos, $25.4M) → VERY HIGH (2 combos, $818K, avoid)
- [ ] Big players (Sysco, US Foods) don't compete for micro-purchases — structural advantage for Newport
- [ ] Post-fraud-crackdown narrative backed by hard data: 1,091 8(a) firms suspended Jan 2026 (25% of program), $550M DOJ fraud case, DoW auditing $80B+ in set-asides with results due to DOGE by Feb 28, 2026. Agencies need replacement vendors for recurring food supply contracts — these are perishable goods, procurement can't pause. (Cite: SBA.gov Jan 28, 2026; Holland & Knight Jan 21, 2026)
- [ ] Appears in Excel ("Market Analysis" competitive section) and deck (1–2 slides)

---

#### FR-007: GovCon Presentation — Interactive Web App ✅ COMPLETE

**As** Newport ownership, **I need to** see a professionally designed interactive presentation that tells the complete GovCon story, **so that** I can evaluate the opportunity and make a go/no-go decision.

**Acceptance Criteria:**
- [x] 20 interactive slides, responsive web app (React 19 + Vite 7)
- [x] Professional design: editorial tone per `web/DESIGN-SYSTEM.md` — gold + teal accents, card-based layouts, Playfair Display + Inter typography
- [x] Opening slides immediately highlight Newport's competitive advantage — 30-year track record as a moat in the post-fraud-crackdown era
- [x] Visual-first design: ECharts 6 for data visualization, Motion 12 for animations, Tailwind CSS 4 for layout
- [x] 4-act narrative: Anchor (title + executive summary) → Market (opportunity, TAM, products, agencies, competition) → Strategy (how it works, examples, portfolio, BD) → Execution (risk, recommendation, key questions, blueprint)
- [x] "How It Works" section shows sourcing, pipeline, bid scoring, relationship building
- [x] Risk & Compliance section with required vs. avoided costs
- [x] No hard-sell language. Tone: professional assessment of an exceptional opportunity
- [x] All data from `web/src/data/{market,strategy,financials}.js` — sourced from live API data with citations
- [x] Password-gated, Netlify-deployed, shareable via URL

**Notes:** The PPTX builder (`build_presentation.js`) has been archived to `archive/govcon-presentation-pptx/`. The web app supersedes it as the primary client deliverable.

---

#### FR-008: GovCon Financial Model — ARCHIVED (data extracted to web app)

**Status:** v7 Excel model COMPLETE and validated (5 sheets, 176 formulas, zero errors, 7 charts). Key financial projections extracted to `web/src/data/financials.js` for the web presentation. The v7 .xlsx is archived at `archive/govcon-financials-openpyxl/Newport_GovCon_Financial_Model_v7.xlsx` for reference and validation.

**What was delivered:**
- [x] 5 sheets: Inputs, Two Routes, 5-Year Model, Market Analysis, Key Questions
- [x] Three scenarios (Conservative/Moderate/Aggressive) with competition-density-informed win rates
- [x] Owner Earnings calculation, compounding renewal flywheel, portfolio evolution
- [x] Zero formula errors

**Notes:** The `build_proforma.py` script (WIP v7 rewrite) is also archived. Financial data is now consumed from `web/src/data/financials.js` by the web presentation. If Newport needs to manipulate inputs directly, the archived v7 .xlsx remains functional.

---

### P0 — Must Have (Commercial SDR Proposal Package)

These requirements must be complete before presenting the commercial channel to Newport.

---

#### FR-009: Commercial ICP Validation & Segment Analysis

**As** Newport ownership, **I need to** see the five target segments for our outbound prospecting, **so that** I understand who we're going after and why.

**Acceptance Criteria:**
- [ ] 5 segments defined with clear qualification criteria: A (Enterprise Grocery Buyers), B (Suppliers/Manufacturers), C (Government Food Buyers), D (Corrections), E (Candy Wholesalers)
- [ ] Each segment includes: target company profile, target title/role, geographic focus, company size thresholds
- [ ] For each segment: estimated universe size (how many companies/contacts fit the criteria)
- [ ] Buyer segments (A, E) vs. supplier segments (B) clearly distinguished — different value propositions
- [ ] Segment C/D overlap with GovCon channel acknowledged and leveraged
- [ ] Candy/LATAM opportunity (Segment E) positioned as unique competitive advantage via Miami port access
- [ ] Appears in both the commercial deck and referenced in the commercial financial model

**Notes:** ICP definitions exist in `config/icp_definitions.json` and `commercial/docs/icp_segments.md`. Candy research exists in `commercial/docs/`. Key gap: no financial model or deck exists for commercial yet.

---

#### FR-010: Commercial SDR Financial Model — v1 COMPLETE, ARCHIVED

**Status:** v1 complete. Script and output archived at `archive/commercial-financials-openpyxl/`.

**What was delivered:**
- [x] 5 sheets: Inputs, ICP Segments, Funnel Model, Market Analysis, Key Questions
- [x] Three scenarios (Free/Moderate/Aggressive) with 12-month projections
- [x] Same design language as GovCon model

**Notes:** Commercial web integration is a future item. The archived .xlsx remains functional for standalone use.

---

#### FR-011: Commercial SDR Presentation Deck — v1 COMPLETE (PPTX), ARCHIVED

**Status:** v1 PPTX deck complete (12 slides). Archived at `archive/commercial-presentation-pptx/`. Commercial web integration is a future item.

**What was delivered:**
- [x] 12 slides, same design language as GovCon deck
- [x] 5 ICP segments with priority indicators
- [x] How It Works: Find → Enrich → Reach → Convert
- [x] Three scenarios side-by-side with economics
- [x] Two Channels, One Strategy slide linking GovCon + Commercial

**Notes:** When commercial slides are added to the web app, they should follow the same design system in `web/DESIGN-SYSTEM.md`.

---

### P1 — Should Have (Post-Presentation)

These requirements improve the operational system but aren't needed for the initial presentation.

---

#### FR-012: GovCon Deck Rebuild — SUPERSEDED by Web App

**Status:** SUPERSEDED. The GovCon presentation is now a React/Vite web app (`web/`). The PPTX builder has been archived to `archive/govcon-presentation-pptx/`. Iteration happens by editing React components in `web/src/components/slides/` and data in `web/src/data/`. Run `cd web && npm run dev` to preview changes instantly.

---

#### FR-013: Pro Forma Rebuild — SUPERSEDED, Script Archived

**Status:** SUPERSEDED. The v7 Excel model was accepted as canonical (Option A from dev plan). Key financial data has been extracted to `web/src/data/financials.js` for the web presentation. The `build_proforma.py` script (WIP v7 rewrite, ~95% complete) is archived at `archive/govcon-financials-openpyxl/`. To update financial projections, edit `web/src/data/financials.js` directly.

---

#### FR-014: Commercial Outreach Automation Pipeline

**As** Still Mind, **I need to** automate the outreach sequence (email → SMS → voice) for enriched prospects, **so that** the SDR system can run on autopilot with minimal intervention.

**Acceptance Criteria:**
- [ ] Email sequences via Instantly (multi-step, personalized from enrichment data)
- [ ] SMS follow-up via Twilio (for contacts with mobile numbers)
- [ ] AI voice outreach via Retell AI (for high-priority prospects)
- [ ] Campaign orchestrator that sequences: email → wait → email → SMS → voice
- [ ] Integration with CRM (Google Sheets initially, Notion later) for tracking
- [ ] Respects opt-out and compliance requirements (CAN-SPAM, TCPA)

**Notes:** This is the `goldmans-leadgen` extraction. Needs to be rebuilt/adapted for Newport's segments and messaging.

---

### P2 — Future Consideration

#### FR-015: Notion Master Pipeline Tracker
Central CRM that aggregates opportunities from CLEATUS, HigherGov, GovSpend, SAM.gov monitor, and direct portals into a single operational dashboard.

#### FR-016: Monthly Automated Reporting
Template-driven monthly report showing pipeline health, win rate, competitive positioning, and recommendations. Generated from pipeline data.

#### FR-017: Multi-Client Template Extraction
When Newport proves the model, extract a reusable framework for other wholesale distributors. Separate the Newport-specific content from the methodology.

---

## Non-Functional Requirements

### Data Integrity
- All market data cited with source and date
- Confidence levels (HIGH/MEDIUM/LOW) on every estimate
- Clear separation between confirmed API data and industry estimates
- Financial model formulas must be auditable (no hidden calculations)

### Design Standards
- Presentation decks: 16:9, ocean gradient palette (#065A82, #1C7293, #21295C)
- Charts and tables: clean, professional, no 3D effects or gratuitous animations
- Text style: short sentences, bullet points, Buffett tone (direct, no fluff)
- Financial models: standard color coding (blue = input, black = formula, green = linked)

### Reproducibility
- Every deliverable can be regenerated from source data + scripts
- Excel models use formulas, not hardcoded values
- Deck reads from `market_data.json` or equivalent data source
- Changes to assumptions propagate automatically through all dependent outputs

### Security & Privacy
- No API keys committed to repo (`.env` file, gitignored)
- Contact data (FL decision makers, Apollo prospects) gitignored
- Newport's proprietary business information (exact revenue, margins) never hardcoded — always input variables

---

## Claude CLI Notes

When implementing any requirement:
1. Check this document first for the acceptance criteria
2. Cross-reference [ARCHITECTURE.md](./03-ARCHITECTURE.md) for technical approach
3. Cross-reference [01-VISION.md](./01-VISION.md) to ensure alignment with strategic intent
4. Flag any acceptance criteria that can't be met and explain why before proceeding
