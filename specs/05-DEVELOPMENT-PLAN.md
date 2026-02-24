# Newport Wholesalers — Development Plan

> **Last Updated**: February 23, 2026
> **Status**: Draft
> **Depends On**: [01-VISION.md](./01-VISION.md), [02-REQUIREMENTS.md](./02-REQUIREMENTS.md), [03-ARCHITECTURE.md](./03-ARCHITECTURE.md)

## Overview

This plan sequences the remaining work to get both proposal packages (GovCon + Commercial SDR) to presentation-ready quality. The GovCon package is ~90% complete and is the priority. The commercial package doesn't exist yet and follows after. Quality over speed — we don't trade thoroughness for timeline.

---

## Current State Assessment

| Component | Status | What Remains |
|-----------|--------|-------------|
| GovCon Research | ✅ Complete | TAM, competition, buyer universe, live API validation — all done |
| GovCon Financial Model (Excel) | ✅ v7 Complete | Review for consistency with latest research. May need minor refinements after Newport answers Key Questions |
| GovCon Presentation Deck | ⚠️ Needs Rebuild | Existing `build_presentation.js` generates v4-era deck. Must be rebuilt to match v7 narrative arc |
| GovCon Intelligence System | ✅ Operational | Daily monitor, bid scoring, pipeline tracker, templates — all working |
| Commercial ICP Definitions | ✅ Complete | 5 segments defined, Apollo configs tested |
| Commercial Market Research | ✅ Complete | Candy/LATAM research, enterprise buyer analysis |
| Commercial Financial Model | ❌ Not Started | Needs full build — funnel economics, tool costs, scenario modeling |
| Commercial Presentation Deck | ❌ Not Started | Needs full build — ICP story, proof of capability, SDR economics |
| Commercial Outreach Automation | ❌ Not Started | Instantly/Twilio/Retell integration — deferred to post-presentation |
| CLAUDE.md + CLI Commands | ⚠️ Outdated | Existing CLAUDE.md needs update to reflect current state and specs |

---

## Phase Overview

| Phase | Name | Deliverable | Dependencies |
|-------|------|-------------|--------------|
| 0 | Spec Finalization & Repo Cleanup | Updated CLAUDE.md, CLI commands, repo structure confirmed | None |
| 1 | GovCon Excel Model Validation | Presentation-ready v7 (or v8) Excel file | Phase 0 |
| 2 | GovCon Deck Rebuild | Presentation-ready PowerPoint (~17–20 slides) | Phase 1 (financial numbers must be locked) |
| 3 | Commercial Financial Model | Presentation-ready Excel (5 sheets, same design language as GovCon) | Phase 0 |
| 4 | Commercial Presentation Deck | Presentation-ready PowerPoint (~10–15 slides) | Phase 3 |
| 5 | Operational Hardening | Pipeline tracker, notification tuning, bid templates finalized | Phases 1–2 |
| 6 | Commercial Outreach Automation | Instantly + Twilio + Retell integration | Phase 4 (post-presentation) |

---

## Phase 0: Spec Finalization & Repo Cleanup

### Objective
Ensure the repo is organized, CLAUDE.md is current, and any Claude CLI session can immediately understand the project state and start productive work.

### Tasks
1. Update `/CLAUDE.md` at repo root with current project state, tech stack, conventions, and spec file references
2. Create `/.claude/commands/` with reusable task prompts (scaffold, new-feature, debug, plus project-specific commands)
3. Verify all existing code runs without errors: `daily_monitor.py`, `contract_scanner.py`, `bid_no_bid.py`, `sheets_pipeline.py`, `collect_market_data.py`
4. Confirm `market_data.json` generation produces current, accurate data
5. Verify `.env.example` lists all required environment variables with descriptions
6. Ensure `data/` directory structure exists with appropriate `.gitignore`

### Claude CLI Prompt
```
Read /specs/06-REPO-STRUCTURE.md and /specs/03-ARCHITECTURE.md.
Update /CLAUDE.md to match the current project state described in /specs/01-VISION.md.
Create /.claude/commands/ with the command files specified in /specs/06-REPO-STRUCTURE.md.
Verify: python govcon/scrapers/daily_monitor.py --dry-run completes without errors.
Verify: python govcon/deliverables/collect_market_data.py --dry-run completes without errors.
```

### Done When
- [ ] Fresh Claude CLI session can read CLAUDE.md and understand: what this project is, what's built, what's next
- [ ] All CLI commands exist and reference correct spec files
- [ ] `daily_monitor.py --dry-run` exits cleanly
- [ ] `collect_market_data.py` generates valid `market_data.json`

---

## Phase 1: GovCon Excel Model Validation

### Objective
Confirm the v7 financial model is accurate, complete, and ready to hand to Newport ownership.

### Tasks
1. Open v7 Excel model and verify every formula resolves (no #REF!, #DIV/0!, #VALUE!)
2. Validate Inputs sheet: all blue cells are editable, yellow cells are clearly marked for Newport
3. Validate Two Routes sheet: cost comparison is current, expected outcomes match the research data
4. Validate 5-Year Model: 
   - Bid volumes reflect strategy (micro declining, simplified/SLED/set-aside ramping from Day 1)
   - Win rates reflect the post-fraud tailwind — agencies actively need replacement vendors, Newport's 30-year history opens doors. We should not be overly conservative on micro AND simplified simultaneously.
   - Micro-purchases decline sharply after enough wins for past performance (~5-10). They're on-ramp currency, not a business line.
   - Renewal math: 70% of contracts renew, compounding each year. Renewals should dominate revenue by Year 3.
   - Owner Earnings calculation is clean: Revenue - COGS - Bid Prep - Fulfillment - Program Costs = OE
5. Validate Market Analysis: data matches latest `market_data.json` and research.md
6. Validate Key Questions: all 10 present, prioritized, with if-yes/if-no impact clearly stated
7. Validate charts render correctly and tell the story visually
8. Document any discrepancies between the v7 model and the `build_proforma.py` script output — determine if the script needs to be updated or if v7 is the canonical version going forward

### Decision Point: Desktop vs. Programmatic
The v7 model was built in Claude Desktop through iterative conversation. It's demonstrably better than what `build_proforma.py` generates (which produces a v4-era 4-sheet model). Options:
- **Option A**: Accept v7 as the canonical model. Update `build_proforma.py` later to reproduce it (Phase 5).
- **Option B**: Rebuild v7 in `build_proforma.py` now so it's reproducible from code.
- **Recommendation**: Option A. Ship the v7 model to Newport. Update the script in Phase 5 when there's time and when Newport's actual inputs might require regeneration.

### Claude CLI Prompt
```
Read /specs/02-REQUIREMENTS.md FR-003 and FR-008 for acceptance criteria.
Open the v7 Excel model at data/newport-govcon-financial-model-v7.xlsx.
Check all formulas for errors.
Verify the 5-Year Model bid volumes show micro declining and simplified/SLED ramping simultaneously.
Verify win rates are not overly conservative — see /specs/04-USER-STORIES.md Flow 4 and Flow 5 for context on the post-fraud environment.
List any issues found.
```

### Done When
- [ ] Zero formula errors in v7 model
- [ ] Bid volume trajectory: micro peaks early, declines by Year 2, near zero by Year 3
- [ ] Simplified and SLED bids start Year 1 and ramp aggressively
- [ ] Win rates reflect both new-entrant reality AND post-fraud tailwind
- [ ] All charts render and tell a clear visual story
- [ ] Key Questions tab is complete and formatted for Newport to fill in

---

## Phase 2: GovCon Deck Rebuild

### Objective
Produce a presentation-ready PowerPoint deck that matches the v7 model's narrative arc and positions Newport's 30-year history as the lead story.

### Tasks
1. Define slide-by-slide outline (see below)
2. Rebuild `build_presentation.js` to generate the new deck structure OR build manually in Claude Desktop
3. Ensure all data points in the deck match the v7 Excel model exactly
4. Apply professional design: ocean gradient palette, clean typography, chart-forward layout
5. Test: open in PowerPoint, verify no rendering issues, all charts display correctly

### Slide Outline

| # | Slide Title | Content |
|---|------------|---------|
| 1 | Title Slide | Newport Wholesalers — Government Contracting Growth Strategy |
| 2 | Newport's Competitive Advantage | 30 years. Clean books. Real infrastructure. American workforce. The vendor agencies need now. Backed by data: post-DOGE/fraud environment. |
| 3 | The Opportunity | Federal food procurement = $7.17B. FL = $85M under $350K. Key stat: 93% sole source in Newport's category. |
| 4 | Market Waterfall | Visual: National → FL → Newport's serviceable market. Data from USASpending. |
| 5 | The Confectionery Gap | $55M national, $412K FL competition. Newport's beachhead category. |
| 6 | Who's Buying | Target agencies: BOP, VA, DeCA, school districts, county governments. FL facilities map. |
| 7 | The Competition | Top 10 FL food contractors. Newport slots into the $1–5M tier. Big players don't compete for micro. |
| 8 | How It Works: Sourcing | How we find opportunities: SAM.gov, state portals, SLED platforms, small business set-asides, low-competition contracts. |
| 9 | How It Works: Evaluation & Bidding | Bid scoring, proposal preparation, capability statement, compliance docs. |
| 10 | How It Works: Pipeline & Relationships | Dashboard tracking, decision-maker outreach, account-based approach to contracting officers AND front-line operators (kitchen managers, nutrition directors). |
| 11 | Two Routes | Free ($0–$2K) vs. Paid ($11K–$47K). Side-by-side costs, market coverage, expected outcomes. |
| 12 | The Strategy | Year 1: micro for credibility (loss leader) + simultaneous simplified/SLED bids. Year 2–3: portfolio shifts to larger contracts. Year 4–5: compounding renewal base. |
| 13 | 5-Year Financial Summary | Revenue trajectory chart, owner earnings, cumulative return. From v7 model. |
| 14 | The Compounding Flywheel | Active contracts chart: renewals + new wins = exponential growth. 70% renewal rate = money machine. |
| 15 | Risk & Compliance | What it takes: SAM.gov registration, food safety, insurance, legal review. What it DOESN'T take: DCAA, CMMC, CAS, bonding. Cost-avoided section. |
| 16 | Your Investment | What Newport pays (tools, certs, legal). What Still Mind handles (monitoring, bids, compliance, admin). Newport focuses on relationships and delivery. |
| 17 | Key Questions | The 10 questions that calibrate the model. "We built this on research. Your answers make it real." |
| 18 | Next Steps | Immediate actions: answer Key Questions, register SAM.gov, prepare capability statement, first bids within 30 days. |

### Claude CLI Prompt
```
Read /specs/02-REQUIREMENTS.md FR-007 for deck acceptance criteria.
Read the slide outline in /specs/05-DEVELOPMENT-PLAN.md Phase 2.
Read /govcon/deliverables/presentation/build_presentation.js for the existing structure.
Rebuild the slide generation to match the new outline.
Use market_data.json for data, with hardcoded fallbacks.
Apply ocean gradient palette: #065A82, #1C7293, #21295C.
```

### Done When
- [ ] 17–20 slides, 16:9 format
- [ ] Opening slide leads with Newport's competitive advantage, not generic market stats
- [ ] All financial data matches v7 Excel model
- [ ] "How It Works" section demonstrates operational capability (sourcing, scoring, relationships)
- [ ] Risk section shows we've done our homework on compliance — and that most expensive compliance requirements DON'T apply
- [ ] No hard-sell language. Professional, optimistic, grounded.
- [ ] Charts are clean, readable, match the Buffett visual style

---

## Phase 3: Commercial Financial Model

### Objective
Build an interactive Excel model for the commercial SDR channel, same design philosophy as v7 GovCon model.

### Tasks
1. Define sheet structure: Inputs, ICP Segments (5 segments with economics), Funnel Model, Market Analysis, Key Questions
2. Build in Claude Desktop (proven to produce better iterative results for financial models)
3. Inputs: tool costs (Apollo, Instantly, Clay, Twilio, Retell), outreach volume per segment, response rate, meeting rate, close rate, average deal size
4. Newport provides: current deal sizes by customer type, current close rate on warm intros, gross margins on commercial deals
5. Three scenarios based on tooling investment and outreach volume
6. Key Questions tab: what do we need from Newport to calibrate this model?
7. Same color coding: blue = editable, yellow = Newport provides, black = calculated

### Decision Point: Approach
- **Recommendation**: Build in Claude Desktop first (like v7), then document the model spec so `build_proforma.py` can be extended to generate it later.
- Reason: Desktop produces better models through iterative refinement. The commercial model is simpler than GovCon (straight-line funnel vs. tiered compounding) and should iterate faster.

### Done When
- [ ] 5-sheet model, zero formula errors
- [ ] Newport can adjust inputs and see projected pipeline + revenue
- [ ] Three scenarios: conservative (free Apollo only) / moderate (Apollo + Instantly) / aggressive (full stack)
- [ ] Key Questions capture what Newport needs to provide
- [ ] Design language matches GovCon model — feels like a suite, not two unrelated spreadsheets

---

## Phase 4: Commercial Presentation Deck

### Objective
Professional deck positioning the AI SDR as a growth accelerator for Newport's existing successful business.

### Tasks
1. Define slide outline (10–15 slides)
2. Build deck — either programmatically or Claude Desktop
3. Key narrative: Newport is already successful through relationships. The SDR adds systematic scale to what's already working. The uncle's excitement about tech-enabled growth = the story.
4. Include: ICP visual, sample enriched data (anonymized), funnel economics, integration with existing sales process
5. Same design language as GovCon deck

### Slide Outline (Draft)

| # | Slide Title | Content |
|---|------------|---------|
| 1 | Title | Newport Wholesalers — Commercial Growth Engine |
| 2 | Where Newport Stands | 30 years of relationship-built success. Strong book of business. Now: systematic growth. |
| 3 | The Opportunity | [Segment-specific market sizing — how many companies fit each ICP] |
| 4 | Five Growth Segments | Visual: ICP A through E with company profiles and why they're targets |
| 5 | How It Works: Find | AI-powered prospecting across all 5 segments. Show: volume, accuracy, coverage |
| 6 | How It Works: Enrich | Contact data enrichment. Show: sample prospect card with verified data |
| 7 | How It Works: Reach | Personalized outreach at scale. Show: email sequence example |
| 8 | How It Works: Convert | Qualified meetings delivered to Newport sales team. They do what they're best at. |
| 9 | The Economics | Cost per lead, meetings per month, expected deal pipeline |
| 10 | Two Channels, One Strategy | GovCon + Commercial SDR running in parallel. Long plays that compound. |
| 11 | Key Questions | What we need from Newport to calibrate |
| 12 | Next Steps | Pilot: one segment, 30-day sprint, measure results |

### Done When
- [ ] 10–15 slides, same design language as GovCon deck
- [ ] Positions SDR as growth accelerator, not a replacement for Newport's existing approach
- [ ] Proof of capability: shows we can actually do what we're proposing (sample data, sample outreach)
- [ ] Financial data matches commercial Excel model
- [ ] Feels like a natural companion to the GovCon deck — together they tell a complete growth story

---

## Phase 5: Operational Hardening (Post-Presentation)

### Objective
Tighten the operational system for daily use after Newport gives the go-ahead.

### Tasks
1. Update `build_proforma.py` to generate v7-equivalent output (if needed for regeneration)
2. Fine-tune daily monitor scoring weights based on initial bidding experience
3. Prepare bid template library: capability statement (customized), sources sought response, RFQ response, simplified proposal
4. Set up direct portal monitoring for top 5 FL school districts and top 3 counties
5. Build Notion pipeline tracker consolidating all opportunity sources

### Done When
- [ ] Still Mind can process a new opportunity from detection to submission with no ad-hoc scripting
- [ ] Template library covers 80% of bid types Newport will encounter
- [ ] Pipeline gives real-time visibility into all stages across all sources

---

## Phase 6: Commercial Outreach Automation (Post-Presentation)

### Objective
Build the automated outreach pipeline for commercial SDR.

### Tasks
1. Adapt Instantly email client from `goldmans-leadgen` for Newport's segments and messaging
2. Build Twilio SMS integration for follow-up sequences
3. Build Retell AI voice integration for high-priority prospects
4. Create campaign orchestrator: email → wait → follow-up → SMS → voice
5. Connect to Google Sheets CRM for response tracking
6. Test on one segment (Segment E: Candy Wholesalers — smallest, most defined)

### Done When
- [ ] End-to-end: prospect sourced → enriched → outreach sent → response tracked → Newport salesperson notified
- [ ] Compliance: CAN-SPAM, TCPA, opt-out respected
- [ ] Newport sales team receives qualified leads with context, not cold names

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Newport answers Key Questions in ways that fundamentally change the model (e.g., can't fulfill under $5,200) | HIGH | Model already shows sensitivity. Prepare alternative scenarios before the meeting. |
| SAM.gov API instability continues | MEDIUM | Hardcoded fallbacks, local data caching. System degrades gracefully. |
| v7 Excel model can't be reproduced programmatically | LOW | v7 is the canonical deliverable. Script update can happen in Phase 5. |
| Newport decides on free route only | MEDIUM | Model supports free route. Adjust expectations and timeline accordingly. |
| Apollo credit limits for commercial enrichment | MEDIUM | Budget credits per segment. Prioritize Segment E (smallest) as pilot. |
| Competitive landscape shifts (new entrants, regulation changes) | LOW | Federal food procurement moves slowly. Monitor via daily scanner. |
| Newport ownership loses enthusiasm after initial meeting | MEDIUM | Key Questions tab keeps them engaged. Monthly check-ins with pipeline progress. Early wins (even micro) build momentum. |

---

## Testing Strategy

| Phase | Test Approach |
|-------|--------------|
| 0 | Run all scripts with `--dry-run`. Verify outputs match expected format. |
| 1 | Open Excel in Microsoft Excel (not Google Sheets). Change every input cell. Verify no formula breaks. |
| 2 | Open deck in PowerPoint. Verify rendering on both Windows and Mac. Check all charts display. |
| 3 | Same as Phase 1 for commercial model. |
| 4 | Same as Phase 2 for commercial deck. |
| 5 | End-to-end: mock opportunity → score → pipeline → bid template → submission-ready package. |
| 6 | Pilot test: send 50 outreach emails to Segment E. Measure delivery rate, open rate, reply rate. |

---

## Claude CLI Notes

When working on any phase:
1. Read this plan first to understand dependencies and sequencing
2. Check the "Done When" criteria — don't consider a phase complete until all boxes would check
3. For the deck and Excel work: Claude Desktop may produce better iterative results. CLI is better for code changes, script updates, and repo management.
4. Never rush quality. If a phase needs more iteration, iterate. The timeline is "when it's right," not a calendar date.
