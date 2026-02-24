# Newport Wholesalers — User Stories

> **Last Updated**: February 23, 2026
> **Status**: Draft
> **Depends On**: [01-VISION.md](./01-VISION.md), [02-REQUIREMENTS.md](./02-REQUIREMENTS.md)

## Overview

User stories for this engagement cover two types of flows: (1) deliverable creation workflows where Still Mind builds and presents the proposal packages, and (2) operational workflows where Still Mind runs the intelligence system day-to-day after Newport says "go." The "users" are Still Mind (operator) and Newport ownership (decision maker).

---

## Flow 1: GovCon Proposal Delivery

**Actor**: Still Mind
**Trigger**: Research, financial model, and system components are ready for presentation
**Preconditions**: v7 financial model finalized, market data validated from live APIs, codebase operational

### Happy Path

1. Still Mind runs `collect_market_data.py` → generates fresh `market_data.json` with latest FPDS/USASpending data
2. Still Mind reviews and finalizes the Excel model (5 sheets). Validates: formulas resolve, charts render, blue cells are clearly editable, Key Questions tab complete
3. Still Mind generates or finalizes the PowerPoint deck (~17–20 slides). Validates: narrative arc (Newport's Advantage → Market Opportunity → How It Works → Two Routes → Projections → Key Questions → Next Steps), data matches Excel, tone is professional assessment not sales pitch
4. Still Mind sends Key Questions as a pre-read to Newport ownership — "answer these before the meeting so we can discuss with your numbers"
5. Still Mind presents deck in person or video. Deck is the sell, Excel is the brass tacks. Walk through the Two Routes decision together.
6. Newport takes the Excel model, plugs in their actual numbers (COGS, margin, delivery radius, certifications, order minimums)
7. Still Mind recalibrates projections based on Newport's answers and delivers updated model
8. **End State**: Newport makes a go/no-go decision. If go, Still Mind begins operational phase immediately (registrations, first bids).

### Error Paths

- **If market data is stale**: Use hardcoded fallback values (built into `build_presentation.js`). Note data date in footnotes. All core research was validated Feb 2026 and federal food markets don't shift dramatically quarter to quarter.
- **If Newport can't answer a Key Question immediately**: Show the sensitivity — "if yes, the model looks like X. If no, it looks like Y. Take your time, we'll update when you decide."
- **If Newport pushes back on win rates**: Point to the data — 93% sole source for NAICS 424490 @ DoD, 15 low-competition NAICS/agency combos worth $64.8M. Then the DOGE/fraud context: agencies are actively losing vendors to fraud investigations and need replacements with auditable histories. Newport isn't a stranger knocking on doors — they're a 30-year answer to a problem agencies are having right now. With the right capability statement and collateral, doors will open.
- **If Newport wants to start free and upgrade later**: Model supports both paths. Show Year 2 upgrade scenario.

### UI Notes (Deliverable Design)

- **Deck**: 16:9, ocean gradient palette (#065A82, #1C7293, #21295C). Charts and tables primary, text supplemental. Short sentences, Buffett tone.
- **Excel**: Standard financial model color coding. Simplicity over complexity — if Newport needs a tutorial, it's too complicated.
- **Opening slide must hit immediately**: Newport's competitive advantage is the headline. "30 years. Clean books. Real infrastructure. The exact vendor agencies need right now." Then back it with the research.

---

## Flow 2: Commercial SDR Proposal Delivery

**Actor**: Still Mind
**Trigger**: GovCon package is delivered (or in parallel)
**Preconditions**: ICP segments validated, Apollo search configs tested, candy/LATAM research complete

### Happy Path

1. Still Mind prepares commercial deck showing the 5 ICP segments with rationale
2. Still Mind demonstrates proof of capability: "here's a sample enriched prospect list for Segment A — names, titles, companies, contact info, all accurate"
3. Still Mind builds commercial financial model showing: tool costs, cost per lead, funnel economics (prospects → enriched → outreach → replies → meetings → deals)
4. Deck positions the SDR as a growth accelerator for a business that's already successful — not a fix for something broken, but a way to systematically find more of what's already working
5. Newport provides input on: what messaging resonates with their buyers, what deal sizes look like, what their current close rate is on warm introductions
6. Still Mind refines the outreach framework and automates
7. **End State**: Newport sales team has a consistent flow of qualified prospects. They focus on relationships and closing. The system runs.

### Key Narrative Point

Newport's uncle built a rich business through relationships and reputation over 30 years. He's not looking to replace what works — he's excited about what technology can add on top. The commercial SDR story is: "you've been doing this manually with great results. Imagine doing it at 10x the volume with the same personal touch, because the AI handles the sourcing and the outreach, and your team handles the conversations."

### Error Paths

- **If Apollo coverage for a segment is thin**: Supplement with manual research (trade directories, conference attendee lists, LinkedIn Sales Navigator). Document coverage gaps per segment.
- **If Newport's existing sales process is more sophisticated than assumed**: Adapt — the SDR slots in alongside whatever they're doing, it doesn't replace it.
- **If deal sizes vary wildly by segment**: Model each segment separately in the financial model. Don't blend averages that hide the real economics.

---

## Flow 3: Daily Opportunity Monitoring (Post Go-Decision)

**Actor**: Still Mind (automated + manual review)
**Trigger**: GitHub Actions cron at 6 AM ET
**Preconditions**: SAM.gov API key configured, Slack webhook active, Google Sheets connected

### Happy Path

1. GitHub Actions triggers `daily_monitor.py` at 6 AM ET
2. Script queries SAM.gov for Newport's NAICS codes across 10 target states
3. Filters applied: active + presolicitation, response within 90 days, relevant set-asides
4. Each opportunity scored through `bid_no_bid.py` (9 factors, weighted)
5. Deduplicates against previously seen solicitations
6. Opportunities scoring ≥ 50 pushed to Google Sheets pipeline tracker
7. Slack alert: "[X] new opportunities. Top: [title] ([score]/100)"
8. Still Mind reviews during morning check → makes bid/no-bid decisions
9. **End State**: No relevant solicitation goes unseen. Pipeline stays current.

### Error Paths

- **SAM.gov API down**: Script logs unavailability, sends Slack alert, exits clean. Resume next day.
- **No new opportunities**: Normal. Script sends "no new matches" to Slack. Not every day has new solicitations.
- **Google Sheets API fails**: Data still saved as local CSV. Sheets is convenience, not dependency.

---

## Flow 4: Bid Preparation (Micro-Purchase)

**Actor**: Still Mind
**Trigger**: Micro-purchase opportunity identified (< $15K, no formal proposal required)
**Preconditions**: Newport registered on SAM.gov, capability statement ready

### Happy Path

1. Still Mind identifies opportunity (daily monitor or direct portal notification)
2. Still Mind prepares: quote with Newport pricing, capability statement, any required certifications
3. Still Mind confirms with Newport: "Can you deliver [product] to [location] by [date] at [price]? Y/N"
4. Newport confirms delivery capability and pricing
5. Still Mind submits via SAM.gov, email to contracting officer, or portal
6. If awarded: Newport fulfills. Still Mind handles paperwork.
7. **End State**: Contract win added to past performance record. One more step toward simplified-acquisition eligibility.

### Critical Context

Micro-purchases are credibility currency, not a business line. Newport needs enough of them to establish past performance references — the #1 factor in winning larger contracts. Once we have 5–10 successful micro deliveries with strong performance ratings, we're eligible to compete for simplified acquisitions ($15K–$350K) where the real revenue lives. In the current post-fraud environment, agencies replacing disqualified vendors are especially receptive to new suppliers with verifiable track records — even a few successful micros from a 30-year wholesaler carry more weight than years of past performance from a vendor under investigation.

The model should show micro bid volume high in months 1–6, declining through months 7–12, and near zero by Year 2. They're the on-ramp. Simplified and SLED bids ramp simultaneously because Newport's commercial track record + even a handful of micro wins creates a credible proposal.

---

## Flow 5: Bid Preparation (Simplified Acquisition / SLED)

**Actor**: Still Mind
**Trigger**: Simplified or SLED opportunity scored high (≥ 65) and bid decision = "Bid"
**Preconditions**: Newport has some past performance (even 3–5 micro wins), capability statement, relevant certifications

### Happy Path

1. Still Mind downloads the full solicitation package (RFQ/RFP/ITB)
2. Still Mind parses requirements: delivery schedule, product specs, required certifications, evaluation criteria, small business set-aside status
3. Still Mind prepares proposal components: technical approach (how Newport fulfills), pricing (competitive based on wholesale margins), past performance citations, required forms/certifications
4. If using CLEATUS (paid route): upload solicitation → AI shreds requirements → compliance matrix generated → proposal drafted with AI assistance
5. Still Mind reviews proposal with Newport for pricing sign-off and delivery commitment
6. Still Mind submits by deadline
7. If awarded: Newport begins fulfillment. Still Mind tracks performance milestones, handles reporting.
8. **End State**: Simplified/SLED contract won. Larger revenue, longer term, recurring potential.

### Error Paths

- **If Newport lacks a required certification**: Evaluate cost/time to obtain vs. skipping this opportunity. Some certs (SQF/GFSI) take months — flag early.
- **If pricing is not competitive**: Newport's wholesale pricing + 18–25% margin should be competitive against smaller FL distributors. If not, the opportunity may have requirements that favor a different vendor type.
- **If timeline is too tight for a quality proposal**: No-bid. A rushed bad proposal wastes credibility. Better to wait for the next one.

### Key Insight

Simplified and SLED bids should NOT wait until micro past performance is fully established. Newport has 30 years of commercial delivery excellence. Combined with even 2–3 successful micro deliveries plus the capability statement highlighting their infrastructure, fleet, workforce stability, and clean history — that's a stronger proposal than most new entrants have. The post-DOGE environment amplifies this: evaluators are looking for reasons to trust a vendor, and Newport gives them plenty. Bid on simplified/SLED from the beginning, while micro wins accumulate in parallel.

---

## Flow 6: Account-Based Decision Maker Outreach (GovCon)

**Actor**: Still Mind
**Trigger**: Target agency identified, no active solicitation but relationship building needed
**Preconditions**: Contact data sourced (Apollo, manual research, FL decision maker list), outreach collateral ready

### Happy Path

1. Still Mind identifies target agency + specific decision makers (e.g., FCI Coleman Food Service Administrator, Broward Schools Food Service Director)
2. Two tiers of contacts identified:
   - **Front-line operators** who write requirements and evaluate vendors (kitchen managers, food service administrators, nutrition directors)
   - **Senior decision makers** who approve contracts (procurement directors, contracting officers, wardens/principals)
3. Still Mind prepares personalized outreach: intro email/letter with capability statement, specific reference to the agency's food procurement needs, offer to be a responsive local vendor
4. Newport (or Still Mind on behalf) makes introductory contact — phone call, email, or in-person visit
5. Relationship nurtured over weeks/months: follow-up touches, industry event meetings, response to sources-sought notices
6. When solicitation drops (or recompete approaches), Newport is already a known quantity
7. **End State**: Newport is on the agency's "call for quotes" list. When they need a food vendor, Newport is top of mind.

### Why This Matters

Government procurement isn't just about responding to posted solicitations. Especially at the micro-purchase and local levels, contracting officers have discretion. They call vendors they trust. The front-line people (head of the prison kitchen, school nutrition director) are the ones who actually specify what they need and influence who gets the call. Finding and building relationships with these people — before a formal bid even exists — is how you win the invisible 83% of the market that never hits a portal.

The system already has a foundation: `data/contacts/fl_decision_makers.csv` with FL BOP, VA, school district, and county contacts. Apollo Segments C and D provide additional government and corrections contacts.

---

## Flow 7: Commercial Prospect Enrichment and Outreach

**Actor**: Still Mind
**Trigger**: Segment-based prospecting cycle (weekly/biweekly)
**Preconditions**: Apollo API configured, ICP definitions in `config/icp_definitions.json`

### Happy Path

1. Still Mind runs `apollo_prospector.py --segment [A-E] --region united_states --max-pages 10`
2. Prospects matching segment criteria returned: name, title, company, industry, employee count, revenue
3. Still Mind runs `enricher.py` on raw prospects → reveals email/phone for top-priority contacts (1 Apollo credit per reveal)
4. Enriched contacts reviewed for accuracy and relevance → bad matches filtered out
5. Still Mind prepares personalized outreach messaging with Newport input on value proposition
6. (Future) Campaign orchestrator sequences: personalized email → wait → follow-up → SMS → AI voice call for high-priority
7. Responses routed to Newport sales team for human follow-up
8. **End State**: Newport salespeople receive warm, qualified leads with context on who the contact is, what their company does, and why Newport is relevant to them.

### Segment-Specific Value Props (Need Newport Input)

- **Segment A (Buyers)**: "We're your local South Florida distribution partner. Confectionery, snacks, dry goods — next-day delivery, competitive wholesale pricing."
- **Segment B (Suppliers)**: "We move [X] units/month through our distribution network. Looking to add brands that our retail and institutional buyers are asking for."
- **Segment C/D (Government/Corrections)**: Overlaps with GovCon channel — coordinate messaging
- **Segment E (Candy)**: "Miami port access, LATAM supply chain, 30 years in confectionery wholesale. Let's talk distribution."

These are starter frameworks. Newport's input on what actually resonates with their buyers is essential.

---

## Claude CLI Notes

When implementing any of these flows:
- Flows 1–2 are deliverable workflows. Reference [02-REQUIREMENTS.md](./02-REQUIREMENTS.md) FR-001 through FR-011 for acceptance criteria.
- Flows 3–6 are operational workflows. The code for these is largely built. Reference the existing `govcon/scrapers/`, `govcon/scoring/`, and `govcon/tracking/` modules.
- Flow 7 is partially built (`commercial/scrapers/`, `commercial/enrichment/`). The outreach automation (Instantly/Twilio/Retell) is not yet implemented.
- Never hard-sell in any client-facing output. Tone is always: professional assessment, research-backed optimism, honest about unknowns.
- Remember: micro-purchases are loss leaders for credibility. The model and narrative should show them declining as simplified/SLED ramp. Newport should be bidding on simplified and SLED from the start — they don't need to wait until micro past performance is "complete."
