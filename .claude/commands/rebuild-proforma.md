Update financial projections in the web presentation.

Financial data lives in `/web/src/data/financials.js` — extracted from the v7 Excel model.
The archived v7 .xlsx at `archive/govcon-financials-openpyxl/Newport_GovCon_Financial_Model_v7.xlsx` is the canonical reference for validation.

Data modules:
- `financials.js` — 5-year projections, scenario comparison, win rates, portfolio evolution, owner earnings
- `market.js` — TAM, agencies, competitors, product tiers (don't duplicate here)
- `strategy.js` — compliance costs, key questions, route comparison (don't duplicate here)

What's in financials.js:
- `MODEL_INPUTS` — gross margin, renewal rate, bid prep costs, fulfillment overhead
- `WIN_RATES` — competition-density-informed rates (low/moderate/high + post-fraud tailwind)
- `FIVE_YEAR_PROJECTIONS` — Moderate scenario: bids, wins, renewals, revenue, owner earnings per year
- `SCENARIO_COMPARISON` — Conservative/Moderate/Aggressive summary
- `TWO_ROUTES` — Free vs. Paid route cost detail
- `PORTFOLIO_EVOLUTION` — bid mix shift (micro → simplified → SLED) over 5 years
- `OE_WATERFALL` — Owner Earnings calculation breakdown

Critical: Win rates must be competition-density-informed (NOT generic assumptions):
- Low-competition (DoD 424490, confectionery 424450): 25-40% Year 1
- Moderate-competition (BOP 424490, DoD 424410): 12-18% Year 1
- Post-fraud tailwind: +5-10% adjustment for months 1-18
- Blended Year 1: ~20-25% (weighted toward low-competition targets)

The competition density data is in /govcon/docs/research.md Section 3 (FPDS analysis).

To refresh market data upstream:
- `python govcon/deliverables/collect_market_data.py` → generates `market_data.json`
- Then update `web/src/data/market.js` with any new figures

After updating financials.js, verify:
- `cd web && npm run build` — zero build errors
- `cd web && npm run dev` — check affected slides render correctly

Reference specs: 02-REQUIREMENTS.md (FR-003, FR-008), web/src/data/financials.js
