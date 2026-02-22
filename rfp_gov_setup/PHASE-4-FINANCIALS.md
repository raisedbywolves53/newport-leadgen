# Phase 4: Pro Forma Financial Model

## Objective
Generate a professional Excel financial model that projects Newport's government contracting revenue across 3 scenarios over 24 months. This supports the PPT proposal with detailed, editable financials Newport leadership can review and adjust.

## Output
- File: `deliverables/financials/newport-govcon-proforma.xlsx`
- Tool: openpyxl (Python)
- Must use Excel formulas, NOT hardcoded Python calculations
- Must pass formula recalculation with zero errors

---

## Workbook Structure (4 Sheets)

### Sheet 1: "Assumptions" (Blue text for all editable inputs)

This sheet contains every assumption that drives the model. All values in blue text (RGB 0,0,255) to indicate they are user-editable.

#### Newport Business Assumptions
| Cell | Label | Value | Notes |
|------|-------|-------|-------|
| B3 | Wholesale Gross Margin | 11% | Newport's estimated margin on government food supply |
| B4 | Average Contract Value — Conservative | $50,000 | |
| B5 | Average Contract Value — Moderate | $75,000 | |
| B6 | Average Contract Value — Aggressive | $100,000 | |
| B7 | Average Contract Duration (months) | 12 | Most small contracts are annual |
| B8 | Revenue Recognition | Monthly | Spread evenly over contract duration |

#### Win Rate Assumptions
| Cell | Label | Value | Notes |
|------|-------|-------|-------|
| B11 | Year 1 Win Rate (Months 1-6) | 15% | New entrant, no past performance |
| B12 | Year 1 Win Rate (Months 7-12) | 25% | Some past performance building |
| B13 | Year 2 Win Rate | 35% | Established past performance |

#### Bid Volume Assumptions
| Cell | Label | Value | Notes |
|------|-------|-------|-------|
| B16 | Bids/Month — Conservative (Free system) | 1.5 | ~18/year |
| B17 | Bids/Month — Moderate (Optimal system) | 3 | ~36/year |
| B18 | Bids/Month — Aggressive (Optimal + dedicated effort) | 5 | ~60/year |

#### Platform Cost Assumptions
| Cell | Label | Value | Notes |
|------|-------|-------|-------|
| B21 | Free System Cost (annual) | $0 | Built-in tools only |
| B22 | CLEATUS (annual) | $3,000 | Mid-range estimate |
| B23 | HigherGov (annual) | $3,500 | Mid-range estimate |
| B24 | GovSpend (annual) | $6,500 | Mid-range estimate |
| B25 | Optimal System Total (annual) | =SUM(B22:B24) | Formula |
| B26 | Consulting Fee — Monthly Retainer | [Leave blank for Newport to discuss] | |

#### Ramp Assumptions
| Cell | Label | Value | Notes |
|------|-------|-------|-------|
| B29 | Months to First Bid | 2 | SAM.gov registration + first opportunity cycle |
| B30 | Months to First Win | 4 | Average award timeline after first submission |

### Sheet 2: "Revenue Model" (24-Month Projection)

#### Layout
- Row 1: Headers
- Row 2: Month numbers (1-24)
- Row 3: Calendar months (Mar 2026 — Feb 2028, assuming start date)
- Rows 5-15: Conservative Scenario
- Rows 17-27: Moderate Scenario  
- Rows 29-39: Aggressive Scenario

#### For Each Scenario (Conservative/Moderate/Aggressive):

| Row | Metric | Formula Logic |
|-----|--------|--------------|
| Row A | Bids Submitted | 0 for months before Assumptions!B29, then Assumptions!B16/B17/B18 per month |
| Row B | Win Rate | Assumptions!B11 for months 1-6, B12 for 7-12, B13 for 13-24 |
| Row C | New Contracts Won | =Row A * Row B (rounded to nearest whole) |
| Row D | Cumulative Contracts Won | Running sum of Row C |
| Row E | Active Contracts | Count of contracts still within their duration period |
| Row F | Monthly Revenue from Active Contracts | =Active Contracts * (Avg Contract Value / 12) |
| Row G | Cumulative Revenue | Running sum of Row F |
| Row H | Monthly Gross Profit | =Row F * Assumptions!B3 |
| Row I | Cumulative Gross Profit | Running sum of Row H |
| Row J | Monthly Platform Cost | =Assumptions!B25 / 12 (or $0 for conservative) |
| Row K | Monthly Net Contribution | =Row H - Row J |
| Row L | Cumulative Net Contribution | Running sum of Row K |

#### Key Formulas Must:
- Reference Assumptions sheet for all inputs (never hardcode)
- Handle the ramp period (no bids before month 2, no wins before month 4)
- Show contracts "rolling off" after their duration expires
- Calculate breakeven month for each scenario

### Sheet 3: "Summary" (Executive View)

| Metric | Conservative | Moderate | Aggressive |
|--------|-------------|----------|------------|
| **Year 1 Results** | | | |
| Total Bids Submitted | Formula | Formula | Formula |
| Contracts Won | Formula | Formula | Formula |
| Total Revenue | Formula | Formula | Formula |
| Gross Profit | Formula | Formula | Formula |
| Platform Investment | Formula | Formula | Formula |
| Net Contribution | Formula | Formula | Formula |
| ROI | Formula | Formula | Formula |
| Breakeven Month | Formula | Formula | Formula |
| **Year 2 Results** | | | |
| (Same metrics) | Formula | Formula | Formula |
| **24-Month Totals** | | | |
| (Same metrics) | Formula | Formula | Formula |

All cells reference Revenue Model sheet. NO hardcoded values.

### Sheet 4: "Platform Comparison"

Side-by-side comparison of Free vs. Optimal platform investment.

| Component | Free | Optimal |
|-----------|------|---------|
| Federal Monitoring | SAM.gov API — $0 | + CLEATUS — $3,000/yr |
| State/Local Monitoring | Manual — $0 | HigherGov — $3,500/yr |
| Micro-Purchase Intel | N/A — $0 | GovSpend — $6,500/yr |
| Competitive Intelligence | FPDS + USASpending — $0 | Same — $0 |
| Proposal Writing | Claude + Templates — $0 | CLEATUS AI — included |
| Pipeline Tracking | Google Sheets — $0 | Same — $0 |
| **Total Annual Cost** | **$0** | **$13,000** |
| **Market Coverage** | ~40-50% | ~90%+ |
| **Bid Capacity/Year** | 12-20 | 40-60 |
| **Estimated Win Rate Uplift** | Baseline | +30-50% more bids = more wins |

This sheet is informational (hardcoded text + values from Assumptions sheet where applicable).

---

## Formatting Requirements

### Color Coding (Financial Model Standard)
- Blue text (0,0,255): All editable assumptions/inputs
- Black text (0,0,0): All formulas and calculations
- Green text (0,128,0): Cross-sheet references
- Yellow background (255,255,0): Key assumptions that Newport should review/adjust

### Number Formatting
- Currency: `$#,##0` with header note "($ amounts)"
- Percentages: `0.0%`
- Counts: `#,##0`
- Years/Months: Text format (not number)

### Visual
- Freeze panes on Row 3 and Column A for Revenue Model
- Bold headers, light gray background on header rows
- Alternating row shading for readability on Summary sheet
- Column widths auto-fit to content

---

## Build Instructions for CLI

1. Use openpyxl (Python) — see `/mnt/skills/public/xlsx/SKILL.md`
2. Create build script: `deliverables/financials/build_proforma.py`
3. All calculations must use Excel formulas (=SUM, =IF, etc.), NOT Python math
4. After building, run formula recalculation:
   ```bash
   python scripts/recalc.py deliverables/financials/newport-govcon-proforma.xlsx
   ```
5. Verify zero formula errors in output
6. Fix any #REF!, #DIV/0!, #VALUE! errors and re-run recalc

## Completion Criteria
- [ ] 4-sheet workbook created
- [ ] All Assumptions in blue text, all formulas in black
- [ ] Revenue Model covers 24 months × 3 scenarios
- [ ] Summary sheet pulls all data from Revenue Model via formulas
- [ ] Formula recalculation passes with zero errors
- [ ] Platform Comparison sheet populated
- [ ] File saved to `deliverables/financials/newport-govcon-proforma.xlsx`

## Project Complete
All 4 phases are done. The system is:
- Organized (Phase 1)
- Operational (Phase 2)
- Presented (Phase 3)
- Financially modeled (Phase 4)
