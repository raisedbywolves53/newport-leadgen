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

## PENDING RESEARCH

### Win Rates by Tier and Year
- Need to derive from competition density data + past performance accumulation
- Current model uses stepped rates (Y1 H1/H2, Y2, Y3+) — likely needs per-tier differentiation

### Gross Margin
- MODEL_INPUTS says 22% blended (Newport actual)
- Interactive default is 11% (intentionally conservative)
- Need to decide: what's the right default for the presentation?

### Set-Aside Bid Prep Cost
- Micro $250, Simplified $1,500, SLED $1,000
- Set-Aside: ??? — needs a number

### Shared Costs
- Insurance ($265-$3,030/yr), Legal ($1,500-$5,000 one-time), Memberships ($225-$725/yr)
- Decision needed: include in model or keep separate?

### Revenue Ramp / Portfolio Evolution
- Current PORTFOLIO_EVOLUTION percentages may need revision given new universe data
- Year 1 should be almost entirely micro + some simplified
- SLED entry timing depends on portal registration + relationship building

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
- Separate revenue stream with different cost structure
