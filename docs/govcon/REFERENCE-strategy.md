# Reference: Newport GovCon Strategy & Intelligence

> This document is READ-ONLY reference material for CLI. It provides strategic context used across all phases. Do not execute this document — reference it when building components in Phases 2-4.

---

## Newport Wholesalers — Company Profile

- **Company**: Newport Wholesalers
- **Business**: Grocery/food wholesale distribution
- **Age**: 30+ years operating
- **Location**: South Florida (warehouse in Miami-Dade/Broward area)
- **NAICS Codes**: 424410 (General Line Grocery), 424450 (Confectionery), 424490 (Other Grocery)
- **Capabilities**: Warehousing, cold chain, delivery fleet, established supplier relationships
- **Government Experience**: None (new entrant)
- **Consultant**: Still Mind Creative LLC (Zack) — building the intelligence system and managing the go-to-market

---

## Target Buyer Universe

### Buyer Categories (priority order)

1. **School Districts** — Largest addressable market. Recurring annual contracts. Lowest-price-wins evaluation. Massive volume (Florida alone: 67 districts, 2.8M+ students).
2. **Corrections** — Consistent demand, multi-year contracts, price-sensitive. FL DOC: 80,000+ inmates across 50+ facilities. County jails throughout Southeast.
3. **FEMA / Emergency Management** — Newport's South FL warehouse is a strategic asset for disaster staging. FL is #1 state for federal emergency declarations. FEMA advance contracts pre-position vendors before disasters hit.
4. **Military / DoD** — Base commissaries, dining facilities. Homestead ARB, MacDill AFB, NAS Jacksonville, Fort Liberty (NC), Fort Stewart (GA).
5. **Universities & Colleges** — Campus dining services, food supply. 12 FL state universities, 28 FL community colleges. Large public universities throughout Southeast.
6. **VA Hospitals / Healthcare** — Patient meals, cafeteria supply. VA facilities throughout Southeast.
7. **State Agencies** — General food procurement for state-run facilities.
8. **County/Municipal** — County government buildings, community centers, meal programs.
9. **Food Banks / Nonprofits** — USDA commodity distribution, TEFAP, LFPA programs.

### Target Tiers

| Tier | Examples | Entry Difficulty | Contract Size |
|------|----------|-----------------|---------------|
| Federal | USDA, DoD, FEMA, VA, BOP | Medium (SAM.gov required, more formal) | $25K-$350K+ |
| State | FL DOC, FL Dept of Education, state universities | Medium (MFMP registration) | $10K-$250K |
| Local | County governments, sheriff offices, city agencies | Low (portal registration) | $5K-$100K |
| Education | School districts (K-12), community colleges | Low-Medium (BidSync/Bonfire) | $25K-$500K+ |

### Geographic Priority (ranked)

1. **South Florida** (home market): Miami-Dade, Broward, Palm Beach
2. **Florida statewide**: Orlando, Tampa, Jacksonville, Tallahassee
3. **Southeast US**: Georgia, South Carolina, North Carolina, Alabama, Tennessee
4. **Extended Southeast**: Mississippi, Louisiana, Virginia
5. **National expansion**: Texas, Arkansas, Kentucky (Year 2+)

---

## FPDS Competition Intelligence (Real Data from CLI Analysis)

### Summary Findings — FY2025
- **Total transactions analyzed**: 1,664 across 10 food NAICS codes
- **Sole-source rate**: 64.8% of contracts received only one bid
- **Key insight**: The federal food contracting market is massively undercontested

### By NAICS Code (from FPDS API output)

| NAICS | Description | Awards | Avg Value | Avg Offers | Sole Source % |
|-------|-------------|--------|-----------|------------|---------------|
| 722310 | Food Service Contractors | 98 | $43M | 1.0 | ~100% |
| 424410 | Grocery Wholesalers | [pull from data] | [pull from data] | [pull from data] | [pull from data] |
| 424490 | Other Grocery | [pull from data] | [pull from data] | [pull from data] | [pull from data] |
| 424420 | Packaged Frozen Food | [pull from data] | [pull from data] | [pull from data] | [pull from data] |
| 424430 | Dairy Product | [pull from data] | [pull from data] | [pull from data] | [pull from data] |
| 424440 | Poultry & Poultry Product | [pull from data] | [pull from data] | [pull from data] | [pull from data] |
| 424450 | Confectionery | [pull from data] | [pull from data] | [pull from data] | [pull from data] |
| 424460 | Fish & Seafood | [pull from data] | [pull from data] | [pull from data] | [pull from data] |
| 424470 | Meat & Meat Product | [pull from data] | [pull from data] | [pull from data] | [pull from data] |
| 424480 | Fresh Fruit & Vegetable | [pull from data] | [pull from data] | [pull from data] | [pull from data] |

> **CLI Instruction**: Run `python enrichment/fpds_client.py` to get current data. Replace "[pull from data]" cells with actual output. If unable to run, use the summary data (1,664 transactions, 64.8% sole-source, 722310 at 98 awards/$43M avg/1.0 offers).

### What This Means for Newport
- Most food contracts get 1 bid (or none). Newport isn't fighting 20 competitors.
- The barrier to entry is VISIBILITY (knowing contracts exist) and SHOWING UP (submitting a compliant bid).
- Small wholesalers don't have systems to find these opportunities. Newport will.
- Past performance compounds: first 3-5 wins are hardest, then gets exponentially easier.

---

## Competitive Landscape

### Newport's Advantages
- 30-year wholesale distribution track record (commercial past performance)
- South Florida warehouse = FEMA disaster staging asset
- Existing cold chain, delivery fleet, supplier relationships
- Full distribution infrastructure already operational
- Small enough to pursue micro/small contracts profitably (large distributors skip these)

### Newport's Gaps
- Zero government past performance references
- No existing agency relationships
- No set-aside certifications (SBA small business, HUBZone, 8(a), SDVOSB)
- No experience with government proposal formats
- No prior SAM.gov registration

### Certification Recommendations (Future — Not Required for Phase 1)
- **SBA Small Business**: Self-certify in SAM.gov during registration
- **HUBZone**: If warehouse qualifies based on census tract (check SBA HUBZone map)
- **SBA 8(a)**: Only if ownership qualifies (socially/economically disadvantaged)
- **SDVOSB/VOSB**: Only if applicable based on ownership

---

## Financial Assumptions

### Newport's Business Economics
- **Wholesale gross margin**: 10-12% (use 11% as baseline)
- **Delivery costs**: Included in margin (existing routes)
- **Incremental cost of government channel**: Primarily administrative (proposal writing, compliance)

### Contract Size Targets
- **Sweet spot Year 1**: $25K-$75K per contract
- **Micro-purchases** (<$10K): No formal bid required, but low value individually
- **Small contracts** ($10K-$250K): Simplified acquisition, often LPTA evaluation
- **Upper range** ($250K-$350K): More formal, may require past performance

### Platform Investment Options
| Platform | Annual Cost | What It Does |
|----------|------------|--------------|
| Free (built tools) | $0 | SAM.gov + FPDS + USASpending monitoring. ~40-50% market visibility. |
| CLEATUS | $2,400-$3,600/yr | Federal + state + local monitoring with AI proposal writing |
| HigherGov | $2,000-$5,000/yr | 40,000+ SLED agencies with NAICS-mapped alerts |
| GovSpend | $3,000-$10,000/yr | Micro-purchases and P-card data (invisible market) |
| **Optimal Total** | **$7,400-$18,600/yr** | **~90%+ market coverage** |

### Revenue Scenarios

| Scenario | Contracts Won Y1 | Avg Value | Revenue | Gross Profit | Net After Platform |
|----------|-----------------|-----------|---------|-------------|-------------------|
| Conservative | 5 | $50K | $250K | $25K-$30K | $6.4K-$30K |
| Moderate | 10 | $75K | $750K | $75K-$90K | $56.4K-$82.6K |
| Aggressive | 15+ | $100K | $1.5M+ | $150K-$180K | $131.4K-$172.6K |

### Key Financial Insight
Even the conservative scenario (5 wins at $50K) generates enough gross profit ($25K-$30K) to pay for the optimal platform ($7.4K-$18.6K) and consulting fees in Year 1. Government contracting is net-positive from Year 1 for Newport.

---

## Registration Requirements (Step 1 Checklist)

### Federal
- [ ] SAM.gov registration (UEI number) — 2-4 weeks for validation
- [ ] Opt into FEMA Disaster Response Registry during SAM.gov registration
- [ ] Obtain SAM.gov public API key for automated monitoring

### State (Florida)
- [ ] MyFloridaMarketPlace (MFMP) vendor registration — 1-2 weeks

### Local (South Florida)
- [ ] Miami-Dade County procurement portal
- [ ] Broward County purchasing portal
- [ ] Palm Beach County procurement portal
- [ ] Miami-Dade County Public Schools (BidSync/Bonfire)
- [ ] Broward County Public Schools
- [ ] Palm Beach County School District

### Documentation Required
- [ ] Florida business license (current)
- [ ] General liability insurance certificate
- [ ] Workers compensation certificate
- [ ] Food safety certifications (FDA registration, any applicable HACCP)
- [ ] W-9 form
- [ ] Banking information for ACH payment setup

---

## Cooperative Purchasing Vehicles (Year 2 Target)

These are contracts that, once awarded, allow ANY member agency to purchase from Newport without a separate RFP:

- **TIPS (The Interlocal Purchasing System)**: 5,000+ member agencies
- **Sourcewell** (formerly NJPA): National cooperative
- **OMNIA Partners**: Largest purchasing cooperative in US
- **Florida Sheriffs Association**: Statewide cooperative

Getting on one cooperative vehicle = access to thousands of agencies simultaneously.
