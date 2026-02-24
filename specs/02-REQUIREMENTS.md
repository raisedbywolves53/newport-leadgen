# Newport Wholesalers — Requirements

> **Last Updated**: February 23, 2026
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
- [ ] Market waterfall from national → Florida → Newport's serviceable range, with dollar values and award counts at each level
- [ ] Breakdown by contract tier: micro-purchase (<$15K, 83% of awards), simplified ($15K–$350K, 14.4%), sealed bid (>$350K, 2.2%)
- [ ] Florida federal food TAM: $85M / 39,685 awards (confirmed USASpending data)
- [ ] Southeast regional TAM: $179M (if multi-state delivery — depends on Newport's answer to delivery radius question)
- [ ] SLED estimate: $600M–$1.2B/yr for FL (school districts, corrections, county agencies) — clearly marked as LOW confidence
- [ ] Category breakdown by PSC code showing Newport's fit (HIGHEST: Confectionery 8925, HIGH: Produce 8915, MODERATE: Dairy 8910, etc.)
- [ ] Confectionery gap highlighted: $55M national, only $412K in FL competition — Newport's beachhead
- [ ] All data points cite source and date (e.g., "USASpending API, FY2024, confirmed Feb 2026")
- [ ] Confidence levels marked on every estimate (HIGH = live API data, MEDIUM = extrapolated, LOW = industry estimates)
- [ ] Appears in Excel ("Market Analysis" sheet) and deck (2–3 slides)

**Notes:** Most of this data exists in `govcon/docs/research.md`. The Excel v7 has a solid Market Analysis sheet. Key gap: SLED data requires paid tools (HigherGov, GovSpend) for precision — must be transparent about this.

---

#### FR-003: Contract Pipeline Projections (5-Year Model)

**As** Newport ownership, **I need to** see a 5-year projection of bids, wins, revenue, and owner earnings, **so that** I can evaluate the financial trajectory and decide which scenario fits my risk appetite.

**Acceptance Criteria:**
- [ ] Five tiers modeled separately: Micro (<$15K), Simplified ($15K–$250K), Set-Aside (SDB/HUBZone), SLED (State/Local/Ed), Sealed Bid ($250K+)
- [ ] Bid volume per tier per year, with strategic narrative (micro phases OUT, simplified/SLED phase IN)
- [ ] Win rates by tier, escalating over 5 years as past performance accumulates (Year 1 micro: 15%, Year 5 simplified: 20%)
- [ ] Renewal/recompete rate: 70% of contracts renew to incumbent — this is the compounding flywheel
- [ ] Revenue split: new wins vs. renewal base — must show renewals becoming dominant by Year 3
- [ ] Owner earnings calculation: Revenue → COGS → Gross Profit → Bid Prep → Fulfillment Overhead → Program Costs → Owner Earnings
- [ ] Cumulative owner earnings: negative Year 1 (investment), breakeven mid-Year 2, $500K–$840K cumulative by Year 5
- [ ] Portfolio shift visualization: Year 1 = mostly micro, Year 5 = mostly simplified/SLED/renewals
- [ ] All calculations driven by editable inputs (not hardcoded)
- [ ] Three scenarios tied to investment path: Conservative (free tools) vs. Moderate vs. Aggressive (full paid stack)

**Notes:** The v7 Excel model implements most of this. Key refinements needed: (1) validate bid volumes are defensible, (2) ensure the "phase out micro" narrative is clear in the numbers, (3) confirm the compounding renewal math is correct.

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
- [ ] FPDS competition density data: 15 low-competition NAICS/agency combos worth $64.8M (233 awards)
- [ ] Sole source rates: 93% sole source for NAICS 424490 @ DoD (117 awards, $9.1M)
- [ ] Big players (Sysco, US Foods) don't compete for micro-purchases — structural advantage for Newport
- [ ] Post-DOGE/fraud narrative: agencies shifting toward transparent, auditable vendors
- [ ] Appears in Excel ("Market Analysis" competitive section) and deck (1–2 slides)

---

#### FR-007: GovCon Presentation Deck

**As** Newport ownership, **I need to** see a professionally designed PowerPoint presentation that tells the complete GovCon story, **so that** I can evaluate the opportunity and make a go/no-go decision.

**Acceptance Criteria:**
- [ ] ~17–20 slides, 16:9 widescreen format
- [ ] Professional design (ocean gradient palette: #065A82, #1C7293, #21295C — matching existing brand)
- [ ] Opening slide immediately highlights Newport's competitive advantage backed by research — 30-year track record as a moat in the post-fraud-crackdown era
- [ ] Visual-first design: charts, tables, graphs are primary; text supplements (short sentences, bullet points — Buffett tone)
- [ ] Slide flow: Newport's Advantage → Market Opportunity → How It Works (process) → Two Routes → Financial Projections → Key Questions → Next Steps
- [ ] "How It Works" section shows: how we source opportunities (SAM.gov, state portals, SLED platforms), how we evaluate (bid scoring), how we bid, how pipeline is tracked, how we find decision-makers (account-based approach)
- [ ] Evidence that the operational system exists: we can find opportunities across channels including small-business set-asides and low-competition contracts, generate appropriate documents, track pipeline, source contact points for relationship building
- [ ] Risk mitigation section: compliance requirements, insurance, legal review, food safety — shows we've done our homework
- [ ] No hard-sell language. Tone: professional assessment of an exceptional opportunity
- [ ] Charts pull from market_data.json (live API data) with hardcoded fallbacks
- [ ] Generated programmatically via `build_presentation.js` (pptxgenjs) OR Claude Desktop

**Notes:** The existing `build_presentation.js` generates a 17-slide deck but was built against v4-era data/narrative. It needs to be rebuilt to match v7's "Owner Earnings" narrative arc and the strategic framing described here.

---

#### FR-008: GovCon Financial Model (Excel)

**As** Newport ownership, **I need to** see an interactive financial model where I can adjust my own numbers, **so that** I trust the projections and can evaluate viability based on my actual business metrics.

**Acceptance Criteria:**
- [ ] 5 sheets: Inputs, Two Routes, 5-Year Model, Market Analysis, Key Questions
- [ ] Color coding convention: Blue = editable inputs, Yellow background = Newport needs to provide, Black = calculated, Green = linked from other tabs
- [ ] All calculations use Excel formulas (not hardcoded Python math)
- [ ] Dynamic inputs for: gross margin, delivery radius, food safety cert status, set-aside eligibility, minimum order size, bid prep costs, fulfillment overhead
- [ ] Newport can change any blue cell and all projections update automatically
- [ ] Three scenarios embedded in the model or selectable via toggle (Free vs. Paid route at minimum)
- [ ] Charts: revenue step-up (stacked showing compound growth from renewals), owner earnings (annual + cumulative), active contracts (compounding flywheel), portfolio shift (micro phases out)
- [ ] Simplicity > complexity. Ownership should be able to navigate without a tutorial.
- [ ] Zero formula errors (#REF!, #DIV/0!, #VALUE!) when opened in Excel

**Notes:** v7 is the current best version. Evaluate whether it needs refinement or is ready for presentation. Key question: does the `build_proforma.py` script in the repo need to be updated to generate v7, or was v7 built entirely in Claude Desktop? If Desktop, we may need to document the model spec so it can be reproduced or iterated.

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

#### FR-010: Commercial SDR Financial Model (Excel)

**As** Newport ownership, **I need to** see the economics of adding an AI-powered SDR system to our sales process, **so that** I can evaluate the cost vs. additional revenue generated.

**Acceptance Criteria:**
- [ ] Inputs: cost of tools (Apollo, Instantly, Clay, Twilio, Retell AI), cost per lead, conversion rates by segment
- [ ] Funnel model: prospects sourced → contacts enriched → outreach sent → replies → meetings booked → deals closed
- [ ] Revenue per deal by segment (wholesale deals are larger than government micro-purchases)
- [ ] Comparison: current manual prospecting vs. AI-assisted SDR (volume, accuracy, cost per meeting)
- [ ] Three scenarios (conservative/moderate/aggressive) based on tool investment and outreach volume
- [ ] Dynamic inputs for Newport's actual deal sizes, margins, close rates
- [ ] Key Questions tab mirroring the GovCon model's approach — what do we need from Newport to refine?
- [ ] Simplicity > complexity. Same design language as the GovCon model.

**Notes:** This does not exist yet. It should follow the same design philosophy as v7 GovCon model: Owner Earnings focus, Buffett tone, visual-first.

---

#### FR-011: Commercial SDR Presentation Deck

**As** Newport ownership, **I need to** see how an AI SDR agent would integrate into our existing sales process, **so that** I understand the value without needing to understand the technology.

**Acceptance Criteria:**
- [ ] ~10–15 slides, same design language as GovCon deck (ocean gradient, professional)
- [ ] Opens with Newport's commercial growth opportunity — expanding buyer base and supplier relationships
- [ ] Shows the ICP segments visually (who we're targeting and why)
- [ ] Demonstrates the data pipeline: find prospects → enrich data → personalize outreach → automate → measure
- [ ] Proof of capability: we can show sample enriched prospect lists, sample outreach messaging
- [ ] Economics: cost per lead, meetings per month, expected revenue lift
- [ ] Integration story: this slots into Newport's existing sales process, salespeople focus on relationships and closing
- [ ] Runs in parallel with GovCon — two growth engines simultaneously
- [ ] Same quality standards: no hard sell, professional assessment, research-backed

**Notes:** This does not exist yet. Lower complexity than GovCon deck because the SDR story is more straightforward.

---

### P1 — Should Have (Post-Presentation)

These requirements improve the operational system but aren't needed for the initial presentation.

---

#### FR-012: GovCon Deck Rebuild (Programmatic)

**As** Still Mind, **I need to** regenerate the GovCon presentation deck programmatically from updated data, **so that** I can iterate quickly when Newport provides their inputs and I need to refresh the projections.

**Acceptance Criteria:**
- [ ] `build_presentation.js` updated to match v7 narrative arc
- [ ] Reads `market_data.json` for live API data with hardcoded fallbacks
- [ ] Reads financial model outputs (or a summary JSON) for projection charts
- [ ] Can be regenerated with a single command: `cd govcon/deliverables/presentation && node build_presentation.js`
- [ ] Output matches the quality of a manually designed deck

---

#### FR-013: Pro Forma Rebuild (Programmatic)

**As** Still Mind, **I need to** regenerate the financial model programmatically, **so that** I can update projections when assumptions change without manually editing Excel.

**Acceptance Criteria:**
- [ ] `build_proforma.py` generates v7-equivalent output (5 sheets, all formulas, charts)
- [ ] All assumptions are parameterized (can be overridden via config file or CLI args)
- [ ] Charts are embedded in Excel (not just data tables)
- [ ] Output passes formula recalculation with zero errors
- [ ] Can be run with: `python govcon/deliverables/financials/build_proforma.py`

**Notes:** The current `build_proforma.py` generates a 4-sheet model that doesn't match v7. If v7 was built in Claude Desktop, this script needs a significant rewrite.

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
