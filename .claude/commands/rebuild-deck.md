Rebuild the GovCon presentation deck: $ARGUMENTS

Steps:
1. Read /specs/02-REQUIREMENTS.md FR-007 for deck acceptance criteria
2. Read /specs/05-DEVELOPMENT-PLAN.md Phase 2 for the slide outline
3. Ensure market_data.json is current: run `python govcon/deliverables/collect_market_data.py`
4. Review the v7 Excel model for current financial figures — deck numbers must match exactly
5. Rebuild govcon/deliverables/presentation/build_presentation.js to match the Phase 2 slide outline
6. Apply ocean gradient palette: #065A82 (primary), #1C7293 (secondary), #21295C (accent)
7. Generate: `cd govcon/deliverables/presentation && node build_presentation.js`
8. Verify: open output .pptx, check all slides render, charts display, data matches v7 model

Critical narrative requirements:
- Opening slide leads with Newport's 30-year competitive advantage, NOT generic market stats
- "How It Works" section proves operational capability (sourcing, scoring, pipeline, relationships)
- Two Routes comparison with clear recommendation
- Financial projections match v7 Excel exactly
- Tone: professional assessment, research-backed optimism, honest about unknowns. Never hard-sell.

Reference specs: 02-REQUIREMENTS.md (FR-007), 05-DEVELOPMENT-PLAN.md (Phase 2)
