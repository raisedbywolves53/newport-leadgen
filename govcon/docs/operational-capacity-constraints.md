# Operational Capacity Constraints & Readiness Assessment — Feb 28, 2026

> **Purpose:** Reality check on the revenue ramp model. The market opportunity model shows what's available to win. This document addresses what Newport can actually deliver — and what we don't yet know.
>
> **Key finding:** The revenue ramp model mechanism is sound but magnitude is likely 2-3x overstated. Operational capacity, not win rates, is the binding constraint.

---

## Critical Assumption Corrections

### Newport's Business Model — UNKNOWN, MUST CONFIRM

**We do not know Newport's operational model.** Early research assumed a vertically integrated distributor (owns warehouse, operates fleet, employs drivers). This may be wrong.

Newport may operate as a **brokerage/arbitrage model**:
- Buys truckloads at price A, routes to buyers at price B
- Uses contract haulers rather than owned fleet
- Minimal or no owned warehouse (or third-party cold storage)
- ~10 employees total (estimated)
- Value-add is sourcing, logistics coordination, and relationships — not physical distribution

**This fundamentally changes the operational capacity analysis.** A broker model:
- Has lower fixed costs, higher variable costs
- Scales through deal flow and coordination, not physical infrastructure
- May have different capacity constraints than a fleet-owning distributor
- May need different compliance infrastructure for government (who controls the cold chain?)

### Newport's Liquidity — UNKNOWN, DO NOT ASSUME

A 35-year business owner who lives modestly may have substantial reserves. Do not project liquidity constraints without data. Present requirements as inputs, not limitations.

---

## What We Know: Government Requirements (These Apply Regardless of Business Model)

### Compliance Documentation (non-negotiable for government food contracts)
- Temperature logs per delivery (who provides these if using contract haulers?)
- Buy American documentation (country of origin tracking)
- Lot-level traceability (FSMA Section 204, effective Jan 2026)
- WAWF electronic invoicing for federal contracts (free, training required)
- Per-district reporting for school contracts
- CPARS monitoring and response for contracts >$350K
- HACCP plan for corrections contracts

### Insurance Requirements
| Coverage | Minimum | Typical Gov Requirement | Est. Annual Cost |
|---|---|---|---|
| General Liability | $1M/$2M | $1M-$5M per occurrence | $3K-$8K |
| Product Liability | $1M | $1M-$5M | $5K-$15K |
| Commercial Auto | $1M | $1M + additional insured | $8K-$20K/truck |
| Umbrella/Excess | $5M recommended | $5M-$10M for large contracts | $5K-$15K |
| Workers' Comp | FL statutory | Required by FL law | Rate: $2.91/$100 payroll (wholesale) |

### Bonding (mostly NOT required for food supply)
- NSLP (school lunch) — **no bonding requirement**
- SFSP contracts >$250K — 10-25% of contract value
- Federal non-construction — at CO's discretion (rare for food)
- SBA bond program: 20x working capital (includes unused credit lines)

### Payment Terms (actually favorable for food)
| Product | Payment Due | Source |
|---|---|---|
| Meat, poultry, fish, eggs | **7 days** after delivery | FAR 52.232-25 (Prompt Payment Act) |
| Perishable agricultural commodities | **10 days** after delivery | FAR 52.232-25 |
| Dairy, edible fats/oils | **10 days** after invoice receipt | FAR 52.232-25 |
| All other goods/services | **30 days** after invoice receipt | FAR 52.232-25 |
| SLED (schools, counties) | **30-45 days** typical | State/local policy |
| Late payment | Government must pay interest | Prompt Payment Act |

**Federal food payment is faster than most commercial customers.** This is a genuine advantage.

---

## What We Don't Know: Newport Readiness Questions

### Operations Model (CRITICAL — shapes entire capacity analysis)

1. **How does a typical Newport transaction work?**
   - Buy truckload at price A → redirect to buyer at price B (pure arbitrage)?
   - Buy → warehouse → break bulk → deliver (distributor)?
   - Some hybrid of both?
   - What % of transactions touch a Newport-controlled facility?

2. **What physical infrastructure does Newport have?**
   - Warehouse: owned, leased, third-party, or none?
   - Square footage and temperature zones (dry, refrigerated, frozen)?
   - Current utilization — how much slack capacity?
   - Cold chain: who controls temperature from purchase to delivery?

3. **Fleet situation:**
   - Owned vehicles: how many, what type?
   - Contract haulers: how many relationships, what capacity?
   - If using contract haulers for government — who provides temperature logs and chain of custody documentation?
   - DOT compliance: on Newport or on the carrier?

4. **Current headcount (~10 employees estimated):**
   - Who does what? (sales, logistics, warehouse, admin, accounting, ownership)
   - Who would handle government compliance documentation?
   - What's the bandwidth for adding government as a channel without hiring?

### Financial Position (present as inputs, not assumptions)

5. **Current liquidity / reserves:**
   - Available credit facility size?
   - Cash reserves or willingness to fund government ramp?
   - Risk tolerance for 30-45 day SLED payment cycles?
   - Current commercial DSO (how fast do current customers pay)?

6. **Current gross margin:**
   - Blended across all products/customers?
   - Does it vary by product category (fresh vs frozen vs dry)?
   - What margin would they target on government contracts?
   - Owner input field in model — they set this number

### Systems & Compliance

7. **ERP / inventory system:**
   - What system do they use today?
   - Does it support lot-level traceability?
   - Can it handle WAWF invoicing (or is that a manual process)?
   - EDI capability for large institutional buyers?

8. **Existing food safety infrastructure:**
   - HACCP plan: current and documented?
   - FDA facility registration: current?
   - Florida FDACS permit: current?
   - Temperature monitoring: automated or manual?
   - Recall/traceability procedures in place?

9. **Insurance:**
   - Current coverage limits (GL, product liability, auto, umbrella)?
   - Willingness to increase for government contract requirements?

### Strategic

10. **Risk tolerance and commitment level:**
    - Comfortable with 1+4 year contracts they cannot decline option years on?
    - Willing to invest 12-18 months before meaningful returns?
    - How much of their management attention can go to government vs commercial?
    - Is this a "try it and see" or a strategic commitment?

---

## Operational Scaling Thresholds (Validated Research)

These thresholds hold regardless of Newport's specific model, though the specifics change based on broker vs distributor.

### Working Capital Requirements
- Per $1M in food wholesale revenue: ~$56K net working capital tied up (Damodaran/NYU Stern, 2026)
- Credit line should be 2-4x theoretical working capital need
- Government contract factoring available at 1-3% (cheaper than commercial — government never defaults)
- SBA 7(a) revolving line up to $5M at Prime + 2-3%

| GovCon Revenue | Working Capital Needed | Recommended Credit Line |
|---|---|---|
| $500K | $28K | $75-150K |
| $2M | $112K | $300-500K |
| $5M | $280K | $750K-1.25M |
| $10M | $560K | $1.5-2.5M |

### Staffing Benchmarks (IFDA — applies to integrated distributors, NOT brokers)
- Industry median revenue per employee: $757K
- Industry mix: 42% warehouse, 31% drivers, 27% admin
- **These benchmarks do NOT apply to a brokerage model** — a 10-person broker operation has a completely different ratio
- Government compliance coordinator becomes necessary at ~$2M in gov revenue regardless of model

### Technology Requirements
| System Level | Monthly Cost | What It Provides | When Needed |
|---|---|---|---|
| Existing system + manual tracking | $0-200 | Basic invoicing | $0-500K GovCon |
| WMS with lot tracking | $750-1,800 | FSMA traceability, FEFO | $500K-5M GovCon |
| Mid-tier food ERP + EDI | $2K-10K | Full compliance, EDI, WAWF | $5M+ GovCon |

### Learning Curve
- Registration & setup: Months 1-2
- First bids submitted: Months 2-4
- First win (micro): Months 4-6
- Operational shakedown: Months 6-12
- Competent execution: Months 12-18
- **Total time to operational proficiency: 12-18 months**

---

## Failure Modes to Watch For

### Top 5 (from Federal Compass, UC Berkeley CMR, SBDC Tampa Bay)

1. **Documentation/compliance failures** — government requires far more paperwork than commercial. Temperature logs, delivery receipts, lot traceability, Buy American, per-agency reporting. This catches every new vendor.

2. **Cash flow mismanagement** — upfront fulfillment costs before payment. Mitigated for Newport by Prompt Payment Act (7-15 days for food) but SLED is 30-45 days.

3. **Underpricing to win** — food wholesale operates at 1-3% net margin (Damodaran). Bidding too aggressively to build past performance, then losing money every delivery.

4. **Admin overload** — ten $500K contracts are operationally harder than one $5M contract. Each has separate invoicing, compliance docs, CPARS, and relationship management.

5. **Option year trap** — once contracted, you CANNOT decline option years (FAR 17.2). If you win 3 contracts in Y2, you're committed to all of them through Y5+. Capacity planning must model worst case = all options exercised simultaneously.

### The CPARS risk
One negative CPARS rating — even a single "Marginal" on one factor — "can stall your pipeline for years." For a new entrant with no track record, the first CPARS-eligible contract (>$350K) is high stakes.

### Base rates for new GovCon entrants
- 97.5% of small businesses fail to transition from small to mid-size in GovCon (GAO-19-523)
- 35% of 8(a) participants graduate successfully (with dedicated SBA support)
- ~15% of 400K+ SAM-registered businesses actually receive awards
- Newport has genuine advantages (35yr operation, infrastructure, FL location) but these numbers inform confidence intervals

---

## Revenue Model Adjustment: Market Opportunity vs Operational Capacity

The revenue ramp model (revenue-ramp-model.md) shows **market opportunity** — what's available to win.

This document establishes that **operational capacity is the binding constraint**, not win rates.

### Capacity-Constrained Projections (pending Newport readiness answers)

| Year | Market Opportunity (Paid) | Capacity-Constrained Range | Limiting Factor |
|---|---|---|---|
| Y1 | $1.04M | $100K-$500K | Learning curve, first wins |
| Y2 | $11.48M | $500K-$2M | Admin capacity, compliance ramp |
| Y3 | $25.59M | $2M-$5M | Dedicated staff, systems investment |
| Y4 | $34.88M | $4M-$8M | Working capital, route capacity |
| Y5 | $42.41M | $6M-$12M | Government division buildout |

**The real projection = minimum of market opportunity and operational capacity.**

$6-12M in government revenue by Year 5 on top of existing commercial business = 12-24% increase in total company revenue from a channel that didn't exist. That's still a transformative outcome.

### These ranges will tighten significantly once Newport answers the readiness questions.

---

## Data Sources

- NYU Stern/Damodaran — Working capital ratios, operating margins (Jan 2026)
- IFDA — Revenue per employee, warehouse benchmarks (2023)
- FAR 52.232-25 — Prompt Payment Act (meat 7 days, perishables 10 days)
- FAR 17.2 — Option year obligations
- FAR 49.4 — Termination for default procedures
- GAO-19-523 — Small business transition rates (2.5% success from small to mid-size)
- UC Berkeley CMR — Why suppliers struggle with government (Jan 2025)
- Federal Compass — Government contractor failure modes
- SBA — 8(a) program graduation rates, surety bond program
- HigherGov — Small business trends 2022 ($2.7M avg award)
- Hinge Marketing — GovCon growth rates (12% avg, 38% high-growth)
- CreditPulse — DSO benchmarks by industry (2025)
- Florida FDACS — Food establishment permit requirements
- FDA/FSMA — Facility registration, traceability, sanitary transport
