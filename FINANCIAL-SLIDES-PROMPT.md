# Financial Slide — Strategic Brief

> **How to use:** Read this FIRST for the business context and model logic. Then read `FINANCIAL-SLIDES-BUILD.md` for the technical implementation spec. Both documents must be read before writing any code.

---

## Role

You are a managing director in Goldman Sachs' Investment Banking division. Still Mind Creative LLC has retained you to build a web-based interactive pro forma that helps Newport Wholesalers' owners evaluate whether to pursue a government contracting channel.

**Calibration:** Mid-level fidelity. Not so high-level it's generic, not so granular it implies false precision. Every number should be defensible from the research. Where we don't have data, we expose the variable as an adjustable input and let management tune it.

---

## The Business Situation

Newport Wholesalers is a 35-year, $25M-$100M grocery wholesaler in Plantation, FL. Zero government contracting history. They want to know: **is pursuing government food contracts worth it, and if so, how much should they invest?**

Still Mind Creative is Newport's strategic partner. Still Mind handles ALL business development, opportunity monitoring, bid identification, proposal support, compliance frameworks, and admin. Newport's only responsibilities are relationship management and physical delivery of product. This is a critical distinction — Newport's operational burden is minimal. The cost to Newport is platform tools + insurance + Newport's own delivery/fulfillment costs.

**Still Mind's consulting fee is intentionally excluded from this model.** That's a separate conversation. This model shows Newport's direct P&L from pursuing the channel.

---

## What the Model Must Answer

Two questions, in order:

1. **"Is this worth pursuing at all?"** — Even the conservative case should show a credible path to positive ROI. If it doesn't, the answer is "don't do it."
2. **"How much should we invest?"** — The difference between the free route and paid route shows what they get for a $13K/yr platform investment. The scenarios then show what different commitment levels produce.

---

## Model Architecture: Two Axes

### Axis 1: Route (Free vs Paid)

This is a binary toggle. It determines the biddable universe and platform costs.

| | Free Route ($0-$3.6K/yr) | Paid Route ($13K/yr) |
|---|---|---|
| Market coverage | ~40-50% (SAM.gov, FPDS, manual) | ~90%+ (CLEATUS + HigherGov + GovSpend) |
| Max bids/month | ~2-3 (limited visibility) | ~5-8 (full pipeline visibility) |
| Platform cost | $0 | $13,000/yr |
| Insurance/compliance | ~$265-$810/yr | ~$810-$3,030/yr |
| Conference/membership | $0 (optional) | $1,725-$3,725/yr |
| Total annual fixed cost | ~$1,272-$3,600 | ~$16,000-$20,000 |

### Axis 2: Scenario (Conservative / Moderate / Aggressive)

Within each route, three scenarios reflect different levels of effort and ambition.

**Free Route scenarios:**
| | Conservative | Moderate | Aggressive |
|---|---|---|---|
| Bids/month | 1 | 1.5 | 2.5 |
| Target contracts | Micro only (<$15K) | Micro + some simplified | Micro + simplified + set-aside |
| Avg contract value | $8K | $12K | $18K |
| Win rate Y1 | 15% | 20% | 25% |

**Paid Route scenarios:**
| | Conservative | Moderate | Aggressive |
|---|---|---|---|
| Bids/month | 2 | 4 | 6 |
| Target contracts | Micro + simplified | All tiers including SLED | All tiers + B2B sub-contracts |
| Avg contract value | $15K | $30K | $45K |
| Win rate Y1 | 18% | 22% | 28% |

**Win rate progression (both routes):**
- Year 1 (months 1-6): Base rate (buying a track record)
- Year 1 (months 7-12): +8-10% (early references)
- Year 2: +5% (established, CPARS history)
- Year 3-5: +5% (preferred vendor, renewal flywheel)

---

## Portfolio Evolution Narrative

The model must reflect HOW the contract portfolio changes over time, not just total revenue:

**Year 1 — "Buying a Track Record"**
Almost entirely micro-purchases (<$15K, 83% of all FL food awards). These are low-barrier, low-competition, low-margin. The goal is past performance documentation, not profit. Some set-asides for small business. Maybe 1 B2B sub-contract if GEO Group or similar opportunity arises. This year may be net negative after costs.

**Year 2 — "Graduating Up"**
Track record from Y1 unlocks simplified acquisitions ($15K-$250K). Win rates improve meaningfully. 70% of Y1 contracts renew, creating recurring base revenue. Revenue roughly 3-5x Year 1. This is where breakeven likely happens.

**Year 3-5 — "The Flywheel"**
Renewals compound (70%/yr). Portfolio shifts: SLED contracts, sealed bids ($250K+), multi-year awards. By Year 3, renewals are the dominant revenue source. New wins add on top. The owner starts seeing real earnings.

**This evolution should be visible in the chart** — not just total revenue growing, but the composition changing. Year 1 is mostly micro. Year 5 is mostly renewals and larger contracts.

---

## Two Categories of Variables

### Category A: Research-Validated (hardcoded, shown as line items)

These come from FPDS, USASpending, SAM.gov data — we can cite the source:

- Florida TAM: $85M addressable, $6.4M visible (117 contracts)
- Contract tier distribution: 83% micro (<$15K), 12% simplified, 5% SLED/sealed
- Average values by tier: Micro $8K, Simplified $50K, SLED $75K, Sealed Bid $150K
- 93% sole source rate for NAICS 424490 @ DoD
- 70% contract renewal/recompete rate
- Win rates by competition density: Low 25-40%, Moderate 12-18%, High 5-8%
- Platform costs: CLEATUS $3K + HigherGov $3.5K + GovSpend $6.5K = $13K/yr
- Insurance range: $265-$3,030/yr depending on coverage
- Post-fraud environment tailwind: +5-10% win rate for clean-history vendors

### Category B: Management Inputs (adjustable sliders)

Only the owner knows these — make them adjustable with sensible defaults:

- **Gross margin %** (8%-15%, default 11%) — Their margin on products sold into government. May differ from commercial margin.
- **Delivery/logistics cost %** (2%-8%, default 4%) — Incremental cost of government delivery routes, base access, special packaging. Could be near-zero if piggyback on existing routes.
- **Admin overhead $/yr** ($0-$50K, default $5K) — Newport's internal time cost for relationship management, paperwork, warehouse coordination. NOT Still Mind's fee.

---

## Tooltip / "Show the Math" Requirement

When a viewer hovers over any data point, the tooltip must break down the arithmetic. This is critical for credibility — these are business owners evaluating a six-figure decision, not analysts who take the model on faith.

Example hover on Year 2, Paid Route, Moderate scenario showing $420K revenue:

```
Year 2 — Moderate (Paid Route)
───────────────────────────────
Bids submitted:  4/mo × 12 = 48
Win rate:        27% (Y2 moderate)
New contracts:   13
Renewals:        7 (10 Y1 contracts × 70%)
Active total:    20 contracts

Revenue by tier:
  Micro (11):    11 × $8K   = $88K
  Simplified (6): 6 × $50K  = $300K
  SLED (3):       3 × $75K  = $225K
  ─────────────────────────────
  Total:  $420K  (gross margin: $46K at 11%)
```

Simple enough to follow: bids × win rate = wins, wins × avg value = revenue. If we claim a number, the hover proves it.

---

## Design: Simple Dashboard

One slide, two interconnected halves. Think Bloomberg terminal meets Looker Studio — clean, dense, functional.

**TOP:** KPI summary cards that update when any input changes
**MIDDLE:** Route toggle (Free/Paid) + Scenario toggle (Conservative/Moderate/Aggressive) + 3 adjustment sliders
**BOTTOM:** Pro forma table (active selection) alongside 1-2 charts

**Charts:** Your call as the builder, but my recommendation:
1. **Primary:** Stacked/overlapping area chart showing all 3 scenarios for the selected route — lets the viewer see the gap between commitment levels
2. **Optional second:** Small stacked bar showing contract type composition shifting Y1→Y5 — makes the portfolio evolution story visual

Every input change must cascade through the entire dashboard — KPIs, table, and charts all update together, smoothly.

---

## Technical Implementation

Read `FINANCIAL-SLIDES-BUILD.md` for the complete technical spec. Start with the Pre-Read files listed there, then follow the step-by-step build instructions.
