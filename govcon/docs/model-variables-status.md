# Financial Model Variables — Research Status

## LOCKED (researched, validated, ready for model)

### Tool Costs (Paid Route)
- CLEATUS: $3,360/yr ($280/mo annual)
- HigherGov: $500/yr (Starter)
- GovSpend: $7,000-$12,000/yr (negotiated, use $10K for model)
- Total paid route: ~$13,860/yr (using $10K GovSpend)

### Tool Costs (Free Route)
- SAM.gov: $0
- USASpending + FPDS: $0
- Manual portal monitoring: $0 (time cost only)

### Bid Prep Costs Per Bid
- Micro (<$15K): $250/bid
- Simplified ($15K-$350K): $1,500/bid
- SLED: $1,000/bid
- Set-Aside: NOT YET DEFINED — needs number

### Operational Capacity (bids/month)
- Free route: 3-8/month (36-96/yr)
- Paid route: 29-55/month (348-660/yr)
- Breakdown by tier in tool-capabilities.md

### FL Bidding Universe (annual opportunities)
- Federal micro: 1,500-2,000 opps @ avg $7,500
- Federal simplified: 350-500 opps @ avg $85,000
- Federal large: 50-70 opps @ avg $750,000
- SLED school districts: 156-245 opps @ $200K-$100M (varies by district size)
- SLED corrections/jails: 32-54 opps @ $500K-$5M
- SLED higher ed/other: 20-35 opps @ $500K-$37M
- Subcontracting: 10-18 relationships @ $250K-$5M
- TOTAL: 2,100-2,900 opps/yr, $1.1B-$1.3B market

### Competition Density
- Federal micro 424490 @ DoD: 1.2 avg bidders, 93% sole source (FPDS, HIGH)
- Federal simplified BOP: 3.2 avg bidders (FPDS, HIGH)
- Federal simplified DoD 424410: 2.4 avg bidders (FPDS, HIGH)
- Federal confectionery 424450: 1.6 avg bidders, 58% sole source (FPDS, HIGH)
- SLED small districts: 2-3 bidders (MEDIUM)
- SLED large districts: 3-5 bidders (MEDIUM)
- County jails: 2-4 bidders (MEDIUM)
- Government-wide: 4.5 avg, 44% receive only 1 bid (Carnegie Mellon, HIGH)

### Existing Model Constants
- Renewal rate: 70% (federal incumbent rate, validated: Fed-Spend 70-75%, Shipley 70% cap, HIGH confidence)
- Fulfillment overhead: 5% of revenue (in MODEL_INPUTS but NOT wired into computeProForma)

### Channel Requirements & Entry Barriers (by tier)
- Federal micro: SAM.gov (recommended), no certs/insurance/bonding, 3-6 weeks to ready
- Federal simplified: SAM.gov required, FDA+FDACS, $1M/$2M CGL, neutral past performance (FAR 15.305), 4-8 months
- FL school districts: E-Verify, per-district registration, FDACS, $1M/$2M CGL, background checks (Jessica Lunsford Act), Buy American, 3-6 months
- FL corrections (county jails): MFMP, security screening, HACCP, bonding >$100K, 6-12 months
- FL DOC (state prisons): Locked under Aramark/Cheney through 2027+ — sub only
- Federal large/set-aside: 3+ past performance refs, bid/performance/payment bonds, SBA cert critical, 12-24 months
- DLA prime vendor subs: SAM.gov + capability statement + insurance, 3-6 months
- FSMC subs (Aramark/Compass/Sodexo): GFSI certification required (SQF/BRC, $5K-$15K, 3-6 months), 6-12 months total
- SBA Mentor-Protege: ~105 days SBA approval, protege performs 40% of JV work, 6-12 months setup
- Full details in channel-requirements.md

### Realistic Access Timeline
- Y1 H1: Federal micro + DLA subs + USDA/LFPA ($50K-$200K)
- Y1 H2: Federal simplified + small school districts ($200K-$500K)
- Y2: County jails + cooperative purchasing + FSMC subs ($500K-$2M)
- Y3: Medium school districts + Mentor-Protege JV + set-asides ($2M-$5M)
- Y4-5: Large contracts + DOC rebids + federal large ($5M-$15M)

### Cost of Entry & Shared Costs (Separate from Model — Startup Investment Table)

**Decision: Keep separate from recurring revenue model. Present as itemized "startup investment" alongside the pro forma.**

#### Free Registrations ($0)
- SAM.gov — unlocks all federal contracting
- E-Verify — mandatory for all FL public contracts
- FDACS vendor registration — unlocks school districts + USDA programs
- MFMP (MyFloridaMarketPlace) — FL state + county procurement portal
- SBA size self-certification — confirms small business status
- District vendor portals — per-district registration (67 districts, time cost only)

#### Required Insurance ($2,000-$5,000/yr recurring)
- $1M per occurrence / $2M aggregate CGL (commercial general liability)
- Required by: federal simplified, school districts, county jails, FSMC subs, DLA subs
- Newport likely already carries this — verify current policy limits
- Not needed for federal micro-purchases

#### Background Checks ($50-$100/person, one-time per employee)
- Jessica Lunsford Act (FL §1012.465) — Level 2 fingerprint screening for school access
- Security screening for jail/correctional facility delivery drivers
- Estimate: 5-15 drivers × $75 avg = $375-$1,125
- Recurring cost only for new hires

#### HACCP Documentation ($1,000-$3,000 one-time)
- Hazard Analysis Critical Control Points food safety plan
- Required for corrections contracts (county jails, future DOC bids)
- Newport may already have elements of this from commercial food safety compliance
- One-time documentation cost; annual review is minimal

#### GFSI Certification — SQF ($5,000-$15,000 one-time + ~$2,000-$3,000/yr renewal)
- Required for FSMC subcontracting (Aramark/Avendra, Compass/Foodbuy, Sodexo/Entegra)
- SQF Edition 9 (Storage & Distribution) is the most common path for distributors
- Includes consulting + audit fees
- Timeline: 3-6 months to achieve
- **This is the single biggest barrier to FSMC sub revenue ($500K-$5M/yr per FSMC)**
- Can defer until Year 1 H2 or Year 2 if FSMC subs are not immediate priority

#### Legal — Entity & Contract Review ($1,500-$5,000 one-time)
- Review of government contract terms, FAR/DFARS flow-downs
- Entity structure verification for SBA size standards
- Mentor-Protege agreement review (if pursuing JV)
- Can be phased: $1,500 for initial review, additional as contracts grow

#### Memberships ($225-$725/yr recurring)
- BuyBoard cooperative membership — free via FSBA for FL school districts
- Florida Buy cooperative — annual fee varies
- Industry associations (IFDA, FMI, local chambers) — $225-$500/yr
- APEX Accelerator counseling — FREE (federally funded, replaces former PTAC)

#### Bonding (variable, only when needed)
- Bid bond: 5% of bid price (required for some federal >$150K and corrections >$100K)
- Performance bond: 100% of contract value (required for large contracts)
- Payment bond: 100% of contract value
- Cost: 1-3% of bond amount annually
- Not needed until Year 2+ when pursuing larger contracts
- Bonding capacity builds with financial history and contract track record

#### Summary: Startup Investment by Phase

| Phase | Items | Est. Cost | Channels Unlocked |
|---|---|---|---|
| **Immediate (Month 1)** | SAM.gov, E-Verify, FDACS, MFMP, capability statement | $0 + time | Federal micro, DLA subs, USDA |
| **Month 1-3** | Insurance verification, background checks (5-10 drivers) | $375-$1,000 | Federal simplified, school districts, county jails |
| **Month 3-6** | HACCP documentation, legal review, memberships | $2,725-$8,725 | Corrections, cooperatives |
| **Month 6-12** | GFSI certification (SQF) | $5,000-$15,000 | FSMC subs (Aramark/Compass/Sodexo) |
| **Year 2+** | Bonding, Mentor-Protege legal, additional certs | Variable | Large contracts, set-asides |
| **Total Y1 startup** | All of above | **$8,100-$24,725** | All channels except large federal |
| **Annual recurring (Y2+)** | Insurance + GFSI renewal + memberships | **$4,225-$8,725/yr** | Maintaining access |

### Win Rates by Channel and Year
- Federal micro: Y1 H1 15-25%, Y1 H2 30-45%, Y2 40-55%, Y3+ 50-60% (MEDIUM confidence)
- Federal simplified: Y1 H1 5-10%, Y1 H2 15-20%, Y2 25-35%, Y3+ 35-45% (MEDIUM)
- FL school districts (small): Y1 H2 30-50%, Y2 35-50%, Y3+ 35-50% (MEDIUM)
- County jails: Y1 H2 25-50%, Y2 35-50%, Y3+ 35-50% (MEDIUM)
- DLA sub: 15-30% probability of onboarding within 12-18 months (MEDIUM)
- FSMC sub: 40-60% probability of approval within 6-12 months (MEDIUM)
- Cooperative (BuyBoard): Y1 5-15% of districts, Y2 15-25%, Y3+ 20-30% (LOW)
- Key finding: LPTA evaluation treats neutral PP identically to Exceptional — price wins
- Full details in win-rates-progression.md

### Past Performance Accumulation
- CPARS mandatory only above $350K (FAR 42.1502)
- Micro-purchases do NOT generate CPARS entries
- Self-reported references citable immediately upon successful delivery
- Commercial experience (35yr) IS citable on federal bids (FAR 15.305(a)(2)(ii))
- SLED contracts count as federal past performance (same FAR citation)
- Subcontract experience citable under 13 CFR 125.2(g)
- Month 0: 35yr commercial; Month 6-12: 5-10 micro + 1-2 SLED; Month 18-24: approaching $350K threshold

### SBA Certification Strategy
- 8(a): DEPRIORITIZE — 97% reduction in acceptances under Trump SBA (65 firms in 2025 vs 2,100+)
- HUBZone: CHECK IMMEDIATELY — 10% LPTA price preference is devastating in food; Plantation FL likely doesn't qualify but adjacent areas may
- Mentor-Protege: BEST ACCELERATOR — no socioeconomic cert needed, JV uses mentor PP, unlimited contracts in 2yr window
- Plain small business: AUTOMATIC — 23% of federal spending set aside, Newport qualifies now

### Revenue Growth Shape
- S-curve: Foundation (Y1, loss leader phase) → Acceleration (Y2-4, 2-3x YoY) → Maturation (Y5+, 15-25% YoY)
- 5 compounding loops: PP accumulation, renewals (70%), contract value escalation, portfolio diversification, relationship/directed awards
- Minimum time in loss leader phase via: parallel channels, SLED wins for federal PP, HUBZone/Mentor-Protege accelerators

### Paid vs Free Route Impact
- Tools multiply opportunity volume (5-7x), not win rate per bid
- Free: 3-8 bids/month, micro-purchases invisible, SLED invisible
- Paid: 29-55 bids/month, full micro visibility (GovSpend), SLED monitoring (HigherGov), AI proposals (CLEATUS)
- Paid route incremental revenue: $120-400K/yr vs $13,860/yr cost (8.7-29x ROI)

### Gross Margin — OWNER INPUT
- Newport owners will provide actual blended gross margin
- Model default: use as editable NumberInput field so owners can adjust
- MODEL_INPUTS reference: 22% blended (Newport actual), 11% (conservative presentation default)
- Not a research variable — this is proprietary Newport data

## PENDING RESEARCH

### Set-Aside Bid Prep Cost
- Micro $250, Simplified $1,500, SLED $1,000
- Set-Aside: ??? — needs a number

### Revenue Ramp / Portfolio Evolution
- Current PORTFOLIO_EVOLUTION percentages need revision given win rates + access timeline data
- Now informed by: win rates per tier, time-to-first-win per channel, past performance accumulation model
- Year 1: micro + simplified + small school districts + DLA subs
- Year 2: county jails + cooperatives + FSMC subs
- Year 3+: Mentor-Protege JV + set-asides + large

### Contract Duration / Overlap
- No concept of multi-year contracts in current model
- SLED school districts: 1+4 year structure
- DOC: 5-10 year contracts
- Federal: mostly annual with renewal options

### Working Capital / DSO
- Not in model. Revenue recognized immediately.
- Government typically pays Net 30-45

### Subcontracting Revenue
- Not in current model at all
- DLA subs ($250K-$1M), FSMC subs ($500K-$5M), Mentor-Protege JV ($1M-$5M)
- Separate revenue stream with different cost structure
