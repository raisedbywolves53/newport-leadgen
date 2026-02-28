# Financial Slide Build Prompt

> **How to use:** Paste this into Claude CLI in VSCode as your initial prompt. It references `FINANCIAL-SLIDES-BUILD.md` for technical specs — this document provides the strategic framing and business logic.

---

## Role

You are a managing director at Goldman Sachs building an interactive financial report for Newport Wholesalers, a 35-year Florida grocery wholesaler evaluating a government contracting channel. The report needs to help the owners make a realistic, educated decision about whether to pursue this opportunity.

**Calibration:** Mid-level fidelity. Not so high-level it's generic, not so granular it implies false precision. Every number should offer reasonable signal with honest buffer. Think "here's what the research tells us and here's where you fill in what only you know."

---

## What This Slide Must Communicate

**Story arc in 3 beats:**

1. **"Here's what we know about your opportunity."** The total universe of contracts Newport could realistically bid on (and win) in Florida — based on their infrastructure, track record, competitive landscape, and the requirements to win. This is grounded in FPDS/USASpending/SAM.gov research already collected.

2. **"Here's what a realistic path looks like."** Three scenario projections (Conservative / Moderate / Aggressive) showing how revenue builds over 5 years — driven by whether they invest in paid tools or go free, which determines biddable universe size, bid volume, and win rates. The chart should show portfolio evolution: Year 1 focused on micro-purchases and set-asides ("buying a track record"), gradually shifting toward larger contracts, B2B subcontracts (GEO Group etc.), and longer-term recurring revenue.

3. **"Here's where you dial in what only you know."** Adjustable sliders for variables we can't research — product margins, logistics costs, servicing overhead. The fixed costs we DO know (tech stack, cost per bid, BD costs) are line items. The owner fills in their side and sees feasibility update in real time.

---

## Chart Requirements: Show the Math

The stacked area chart comparing all 3 scenarios is the centerpiece. It must show portfolio evolution compounded across contract channels over time.

**Critical UX requirement — tooltips must show the work:**

When a user hovers over any data point in the chart, the tooltip must break down HOW that number was derived. For example:

If Conservative + Paid is selected and Year 1 shows 35 contracts won / $500K revenue, the tooltip should show:

```
Year 1 — Conservative (Paid Tools)
─────────────────────────────────
Bids submitted:    18/mo × 12 = 216
Win rate:          ~16% (weighted avg)
Contracts won:     35
  ├─ Micro (<$15K):     28 @ $8K avg = $224K
  ├─ Simplified:         5 @ $50K avg = $250K
  └─ Set-aside:          2 @ $13K avg = $26K
Total revenue:     $500K
```

The math should be simple enough to follow — "submit X bids per month, at Y win rate, based on Z average contract value = the result shown." If we claim a number, the hover proves it.

---

## Two Categories of Variables

### Fixed (we researched these — display as line items, not sliders):
- Platform/tech stack costs: CLEATUS $3K + HigherGov $3.5K + GovSpend $6.5K = $13K/yr (paid path) or $0 (free path)
- Estimated cost per bid (time + materials)
- Business development costs (reasonable estimate from research)
- Win rates by competition density (from FPDS data)
- Contract tier distribution and average values (from USASpending data)
- Renewal/recompete rate: 70% (from research)

### Adjustable (only the business owner knows these — make them sliders):
- Gross margin on specific product categories (8%–15% range)
- Logistics/delivery costs
- Servicing and relationship management overhead
- Bid volume multiplier (how aggressively they want to pursue)
- Any additional headcount or operational costs

---

## Portfolio Evolution Logic (Year 1 → Year 5)

**Year 1:** "Buying a track record." Almost entirely micro-purchases (<$15K), some set-asides for small businesses, maybe 1-2 B2B subcontracts. Win rates are lowest. The goal is past performance, not profit.

**Year 2:** Track record enables simplified acquisitions ($15K-$250K). Win rates improve. Some Year 1 contracts renew (70% renewal rate). Revenue roughly doubles.

**Year 3-5:** Portfolio shifts toward larger contracts (SLED, sealed bid). Renewals compound — by Year 3 they become the dominant revenue source. Win rates peak. The "flywheel" is spinning.

The chart should visually show this evolution — the composition of each year's revenue changes, not just the total.

---

## Scope: Florida Only (for now)

All projections are Florida-only, even though Newport can operate nationwide. The model should make this clear in labeling. This is a deliberate constraint — prove the concept in the home state first.

---

## Technical Implementation

Read `FINANCIAL-SLIDES-BUILD.md` in the repo root for the complete technical spec including:
- File structure and component architecture
- Data model and return shapes
- ECharts configuration for the stacked area chart
- UI component specs (ScenarioToggle, AnimatedNumber, Slider)
- Design system colors, patterns, and spacing
- Slide registration instructions
- Verification checklist

Start by reading the Pre-Read files listed in that document, then follow the step-by-step build instructions.
