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
| GovCon Financial Model (Excel) | ✅ v7 Complete, ARCHIVED | Key data extracted to `web/src/data/financials.js`. v7 .xlsx archived at `archive/govcon-financials-openpyxl/` |
| GovCon Web Presentation | ✅ Complete | 20 interactive slides, React 19 + Vite 7, deployed via Netlify |
| GovCon Intelligence System | ✅ Operational | Daily monitor, bid scoring, pipeline tracker, templates — all working |
| Commercial ICP Definitions | ✅ Complete | 5 segments defined, Apollo configs tested |
| Commercial Market Research | ✅ Complete | Candy/LATAM research, enterprise buyer analysis |
| Commercial Financial Model | ✅ v1 Complete, ARCHIVED | 5 sheets, 3 scenarios. Archived at `archive/commercial-financials-openpyxl/` |
| Commercial Presentation Deck | ✅ v1 Complete (PPTX), ARCHIVED | 12 slides. Archived at `archive/commercial-presentation-pptx/`. Web integration future. |
| Commercial Outreach Automation | ❌ Not Started | Instantly/Twilio/Retell integration — deferred to post-presentation |
| CLAUDE.md + CLI Commands | ✅ Updated | Reflects web-first deliverable, archived legacy builders |

---

## Phase Overview

| Phase | Name | Deliverable | Dependencies |
|-------|------|-------------|--------------|
| 0 | Spec Finalization & Repo Cleanup | Updated CLAUDE.md, CLI commands, repo structure confirmed | None |
| 1 | GovCon Excel Model Validation | Presentation-ready v7 (or v8) Excel file | Phase 0 |
| 2 | GovCon Deck Rebuild | PPTX archived; superseded by web app | Phase 1 |
| 2.5 | GovCon Web Presentation | 20-slide React/Vite web app (COMPLETE) | Phase 1 |
| 3 | Commercial Financial Model | Presentation-ready Excel (5 sheets, same design language as GovCon) | Phase 0 |
| 4 | Commercial Presentation Deck | v1 PPTX complete, archived. Web integration future. | Phase 3 |
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
   - Win rates **must be differentiated by competition density**, not generic per-tier. FPDS data provides the justification:
     - Low-competition targets (DoD 424490: 93% sole source, 1.2 avg offers; Confectionery 424450: 58% sole source, 1 registered contractor nationally): **25–40% Year 1 win rate**
     - Moderate-competition targets (BOP 424490: 3.2 avg offers; DoD 424410: 2.4 avg offers): **12–18% Year 1**
     - Post-fraud tailwind: +5–10% adjustment for first 12–18 months (1,091 firms suspended, multi-agency audits — agencies actively losing vendors for recurring food contracts)
     - Blended Year 1 win rate should land at ~20–25% if Newport targets low-competition categories first (which is the strategy). The old generic 15% assumed random bidding across all competition levels — that's not what we're proposing.
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
Verify win rates are differentiated by competition density:
  - Low-competition (DoD 424490, confectionery 424450): 25-40% Year 1
  - Moderate-competition (BOP 424490, DoD 424410): 12-18% Year 1
  - Post-fraud tailwind: +5-10% adjustment for months 1-18
  - Blended Year 1: ~20-25% (weighted toward low-competition targets)
See /specs/04-USER-STORIES.md Flow 4 and Flow 5 for context.
See /govcon/docs/research.md Section 3 for FPDS competition density data.
List any issues found.
```

### Done When
- [ ] Zero formula errors in v7 model
- [ ] Bid volume trajectory: micro peaks early, declines by Year 2, near zero by Year 3
- [ ] Simplified and SLED bids start Year 1 and ramp aggressively
- [ ] Win rates differentiated by competition density: 25–40% for low-competition targets (DoD, confectionery), 12–18% for moderate, blended ~20–25% Year 1
- [ ] Post-fraud tailwind adjustment (+5–10%) applied for months 1–18 with documented justification
- [ ] All charts render and tell a clear visual story
- [ ] Key Questions tab is complete and formatted for Newport to fill in

---

## Phase 2: GovCon Deck Rebuild — COMPLETE (PPTX ARCHIVED)

> **Status**: The PPTX builder (`build_presentation.js`) generated an 18-slide v7 deck. It has been **superseded by the web application** (Phase 2.5) and archived to `archive/govcon-presentation-pptx/`.

---

## Phase 2.5: GovCon Web Presentation — COMPLETE

### Objective
Interactive web-based presentation that delivers the GovCon story with animated data visualizations, responsive design, and URL-based sharing.

### What Was Built
- React 19 + Vite 7 + Tailwind CSS 4 + ECharts 6 + Motion 12
- 20 interactive slides across 4 acts (Anchor, Market, Strategy, Execution)
- Design system documented in `web/DESIGN-SYSTEM.md`
- Data separated into `web/src/data/{market,strategy,financials}.js`
- Password-gated, Netlify-deployed
- Slide components in `web/src/components/slides/`

### Done
- [x] 20 slides with animated transitions and data visualizations
- [x] Opening slides lead with Newport's competitive advantage
- [x] All financial data from v7 model extracted to `financials.js`
- [x] "How It Works" section demonstrates operational capability
- [x] Risk & Compliance section with required vs. avoided costs
- [x] Key Questions slide with all 10 questions and priority levels
- [x] Professional, grounded tone throughout

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

## Phase 4: Commercial Presentation Deck — v1 COMPLETE (PPTX ARCHIVED)

### What Was Built
- 12-slide PPTX deck using same design system as GovCon deck
- 5 ICP segments, How It Works (Find/Enrich/Reach/Convert), 3-scenario economics, Two Channels One Strategy
- PPTX builder and output archived to `archive/commercial-presentation-pptx/`
- Commercial web integration is a future item (GovCon web presentation is the current priority)

---

## Phase 5: Operational Hardening (Post-Presentation)

### Objective
Tighten the operational system for daily use after Newport gives the go-ahead.

### Tasks
1. Fine-tune daily monitor scoring weights based on initial bidding experience
2. Prepare bid template library: capability statement (customized), sources sought response, RFQ response, simplified proposal
3. Set up direct portal monitoring for top 5 FL school districts and top 3 counties
4. Build Notion pipeline tracker consolidating all opportunity sources
5. **FPDS Migration**: FPDS ezSearch decommissioned Feb 24, 2026. The ATOM feed (used by `fpds_client.py`) survives through later FY2026, but must be migrated to SAM.gov contract awards search API before then. Update competition density analysis scripts accordingly.
6. **Platform Registrations**: Ensure Newport is registered on Unison Marketplace (BOP reverse auction platform), BidNet Direct, DemandStar, and VendorLink (Broward County) — in addition to SAM.gov and MyFloridaMarketPlace.

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
| 1 | v7 Excel model archived. Validated before archival: zero formula errors, all charts render. |
| 2/2.5 | `cd web && npm run build` — zero build errors. `npm run dev` — all 20 slides render in Chrome/Firefox/Safari. |
| 3 | Commercial Excel model archived. Validated before archival. |
| 4 | Commercial PPTX archived. Validated before archival. |
| 5 | End-to-end: mock opportunity → score → pipeline → bid template → submission-ready package. |
| 6 | Pilot test: send 50 outreach emails to Segment E. Measure delivery rate, open rate, reply rate. |

---

## Claude CLI Notes

When working on any phase:
1. Read this plan first to understand dependencies and sequencing
2. Check the "Done When" criteria — don't consider a phase complete until all boxes would check
3. For the deck and Excel work: Claude Desktop may produce better iterative results. CLI is better for code changes, script updates, and repo management.
4. Never rush quality. If a phase needs more iteration, iterate. The timeline is "when it's right," not a calendar date.
