Rebuild or validate the GovCon financial model.

Before building:
1. Read /specs/02-REQUIREMENTS.md FR-003 and FR-008 for model acceptance criteria
2. Read /specs/05-DEVELOPMENT-PLAN.md Phase 1 for validation checklist
3. Read /specs/04-USER-STORIES.md Flow 4 and Flow 5 for win rate context

Critical: Win rates must be competition-density-informed (NOT generic assumptions):
- Low-competition (DoD 424490, confectionery 424450): 25-40% Year 1
- Moderate-competition (BOP 424490, DoD 424410): 12-18% Year 1
- Post-fraud tailwind: +5-10% adjustment for months 1-18
- Blended Year 1: ~20-25% (weighted toward low-competition targets)

The competition density data is in /govcon/docs/research.md Section 3 (FPDS analysis).

Three scenarios:
- Conservative (free tools, broad bidding): ~$50K Year 1 revenue
- Moderate (paid tools, low-competition targeting): ~$100-150K Year 1
- Aggressive (full stack + relationship building): ~$150-250K Year 1

5 sheets: Inputs, Two Routes, 5-Year Model, Market Analysis, Key Questions
Color coding: Blue = editable, Yellow = Newport provides, Black = calculated, Green = linked

NOTE: v7 model (built in Claude Desktop) is the canonical deliverable.
build_proforma.py generates a v4-era 4-sheet output that needs updating.
If validating v7, open the Excel file directly. If rebuilding programmatically, update the script.

Reference specs: 02-REQUIREMENTS.md (FR-003, FR-008), 05-DEVELOPMENT-PLAN.md (Phase 1)
