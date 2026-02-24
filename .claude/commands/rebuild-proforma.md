Rebuild the GovCon financial model: $ARGUMENTS

Steps:
1. Read /specs/02-REQUIREMENTS.md FR-008 for Excel model acceptance criteria
2. Read /specs/05-DEVELOPMENT-PLAN.md Phase 1 for validation checklist
3. The v7 model (built in Claude Desktop) is the canonical version with 5 sheets:
   - Inputs: Newport-editable variables (blue on yellow), win rates by tier, cost assumptions
   - Two Routes: Free vs. Paid side-by-side with costs and expected outcomes
   - 5-Year Model: Bids → Wins → Active Contracts → Revenue → Owner Earnings
   - Market Analysis: TAM waterfall, contract examples, category gaps, competition
   - Key Questions: 10 prioritized questions with if-yes/if-no impact
4. If updating build_proforma.py to match v7:
   - Use openpyxl with Excel formulas (not Python math)
   - Color coding: blue text = editable, yellow background = Newport provides, black = calculated, green = linked
   - Include charts: revenue step-up (stacked), owner earnings, active contracts, portfolio shift
   - Zero formula errors when opened in Excel
5. Key model points:
   - Micro bids peak early, decline sharply — they're credibility currency, not a business line
   - Simplified and SLED bids start Year 1 and ramp — Newport's 30-year track record plus post-fraud environment means they don't wait
   - Win rates should NOT be overly conservative — the DOGE/fraud tailwind means agencies actively need clean vendors
   - Renewals compound at 70% and dominate revenue by Year 3
   - Owner Earnings (Buffett metric): Revenue - COGS - Bid Prep - Fulfillment - Program Costs

Reference specs: 02-REQUIREMENTS.md (FR-003, FR-008), 05-DEVELOPMENT-PLAN.md (Phase 1)
