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
- Renewal rate: 70% (federal incumbent rate)
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

### Cost of Entry (One-Time / Annual)
- SAM.gov, E-Verify, FDACS, MFMP: $0
- Insurance ($1M/$2M CGL): $2,000-$5,000/yr
- Background checks: $50-$100/person
- HACCP documentation: $1,000-$3,000
- GFSI certification (SQF): $5,000-$15,000
- SBA 8(a) application: $0
- Bonding: 1-3% of bond amount (when needed)

## PENDING RESEARCH

### Win Rates by Tier and Year
- Need to derive from competition density data + past performance accumulation
- Current model uses stepped rates (Y1 H1/H2, Y2, Y3+) — likely needs per-tier differentiation
- Now informed by channel requirements: micro has no past performance eval, simplified is neutral, large requires 3+ refs

### Gross Margin
- MODEL_INPUTS says 22% blended (Newport actual)
- Interactive default is 11% (intentionally conservative)
- Need to decide: what's the right default for the presentation?

### Set-Aside Bid Prep Cost
- Micro $250, Simplified $1,500, SLED $1,000
- Set-Aside: ??? — needs a number

### Shared Costs
- Insurance ($265-$3,030/yr), Legal ($1,500-$5,000 one-time), Memberships ($225-$725/yr)
- Now partially informed by channel requirements cost-of-entry data
- Decision needed: include in model or keep separate?

### Revenue Ramp / Portfolio Evolution
- Current PORTFOLIO_EVOLUTION percentages may need revision given new universe data
- Now informed by realistic access timeline from channel requirements
- Year 1 should be almost entirely micro + some simplified + DLA subs
- SLED entry timing: school districts Y1 H2, county jails Y2, cooperatives Y2

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
- Now informed by channel requirements: DLA subs ($250K-$1M), FSMC subs ($500K-$5M), Mentor-Protege JV ($1M-$5M)
- Separate revenue stream with different cost structure
