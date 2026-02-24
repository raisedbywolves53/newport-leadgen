Rebuild the GovCon presentation deck.

Before building:
1. Read /specs/02-REQUIREMENTS.md FR-007 for deck acceptance criteria
2. Read /specs/05-DEVELOPMENT-PLAN.md Phase 2 for the slide-by-slide outline
3. Read /specs/04-USER-STORIES.md Flow 1 for the delivery narrative and error paths
4. Run `python govcon/deliverables/collect_market_data.py` to generate fresh market_data.json
5. Verify the v7 Excel model data matches what will go into the deck

Slide outline is in /specs/05-DEVELOPMENT-PLAN.md Phase 2 (19 slides).

Key requirements:
- 16:9 widescreen, ocean gradient palette: #065A82, #1C7293, #21295C
- Opening slide leads with Newport's competitive advantage + DOGE/fraud receipts
- Three headline competition stats: DoD 93% sole source, confectionery 1 contractor nationally, 15 low-competition combos worth $64.8M
- TAM waterfall: $87M → filters → $17-20M SAM
- All financial data must match v7 Excel model exactly
- Professional, grounded — never hard-sell
- Charts from market_data.json with hardcoded fallbacks

Build path: cd govcon/deliverables/presentation && node build_presentation.js
Or build manually in Claude Desktop if iterative refinement needed.

Reference specs: 02-REQUIREMENTS.md (FR-007), 05-DEVELOPMENT-PLAN.md (Phase 2), 04-USER-STORIES.md (Flow 1)
