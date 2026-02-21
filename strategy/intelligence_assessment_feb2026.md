# Newport Wholesalers — Intelligence Assessment Summary

**Date:** February 20, 2026
**Status:** Phase 1 Complete

---

## Executive Summary

This assessment answers the gating question: **Can we identify the right decision makers and get valid contact info for government food procurement and candy wholesale?**

**Answer: Yes, with caveats.**

- **Government:** Decision makers are identifiable through a multi-source approach (Apollo + FPDS + agency directories + industry associations). Apollo alone is insufficient for government contacts — expect 15-25% hit rate on government employees vs. 40-60% for private sector. The recommended approach combines 8 different sourcing channels to build a validated database of 275-925 contacts at an estimated cost of $300-$1,000 plus 40-80 hours of research time
- **Candy (US):** Apollo coverage of US candy distributors is good. Decision makers at companies like Nassau Candy, Redstone, B.A. Sweetie are findable with standard Apollo search
- **Candy (LATAM):** Apollo coverage drops significantly for Central America and Caribbean. Mexico and South America (Brazil, Colombia) have moderate coverage. Supplementary sources needed for comprehensive LATAM targeting
- **Government is the higher-value play.** A single government contract can generate $100K-$5M+ in annual revenue. The investment to identify and reach decision makers ($1K-$2K) has trivial cost relative to contract value

---

## Live Data Results

### USASpending Market-Size Report (FY2023-2025)

Federal food procurement spending tracked through USASpending.gov for Newport's target NAICS codes:

| Fiscal Year | Total Federal Food Spend | YoY Growth |
|---|---|---|
| FY2023 | **$1.276 billion** | — |
| FY2024 | **$1.322 billion** | +3.6% |
| FY2025 | **$1.467 billion** | +10.9% |

**Spending by NAICS Code (FY2025):**

| NAICS | Category | FY2025 Spend |
|---|---|---|
| 722310 | Food Service Contractors | $1.379B (94%) |
| 424410 | General Line Grocery Wholesalers | $29.0M |
| 424490 | Other Grocery Wholesalers | $16.4M |
| 424440 | Poultry Wholesalers | $2.4M |
| 722330 | Mobile Food Services | $1.3M |
| 424480 | Fresh Fruit/Vegetable Wholesalers | $938K |
| 424470 | Meat Wholesalers | $865K |
| 424430 | Dairy Wholesalers | $776K |
| 424460 | Fish/Seafood Wholesalers | $324K |
| 424420 | Packaged Frozen Food Wholesalers | $95K |
| 424450 | Confectionery Wholesalers | $16K |

**Spending by Agency (Top 5, FY2025):**

| Agency | FY2025 Spend | % of Total |
|---|---|---|
| Department of Defense | $1.193B | 81.4% |
| Department of Agriculture | $117.1M | 8.0% |
| Department of Homeland Security | $90.2M | 6.1% |
| Department of Justice (incl. BOP) | $19.7M | 1.3% |
| Department of State | $12.4M | 0.8% |

**Key Insights:**
1. **Food Service Contractors (722310) dominate at 94% of tracked spending.** This confirms that the FSMC channel (Aramark, Compass, Sodexo, Trinity) is the primary path to federal food dollars — Newport needs to become an approved FSMC vendor
2. **General Line Grocery Wholesale (424410) — Newport's primary NAICS — shows $29M in FY2025, up from $17M in FY2023.** This 70% growth indicates expanding direct-supply opportunities
3. **DoD accounts for 81% of spending.** Military food service is the largest single market, but accessed through prime vendors (Sysco, US Foods), not direct federal contracts
4. **USDA is growing fast** ($66M → $117M, +77% FY2023→FY2025). USDA AMS commodity procurement is an accessible entry point for Newport
5. **DOJ (BOP) spending at $19.7M** represents the most accessible direct federal market for Newport — BOP institutions procure locally

**Important caveat:** USASpending tracks federal spending only. State and local government food spending ($25-40B+ annually) is not captured here. The federal numbers represent the floor of the opportunity, not the ceiling.

**Output files:**
- `data/final/govt_market_size_by_naics_20260220_2132.csv` — 34 records
- `data/final/govt_market_size_by_agency_20260220_2132.csv` — 73 records

---

## Apollo Dry Run Assessment

### Segment C — Government Food Buyers

**Configuration validated.** Key parameters:
- 14 title keywords covering procurement, food service, nutrition, dietary, commissary, subsistence
- 13 org keywords covering government, federal, state, county, school district, BOP, VA, military
- Seniority: Director+ (appropriate for decision makers)
- Employee minimum: 101+ (filters small agencies appropriately)
- Exclusions: IT, HR, engineering, marketing roles filtered out
- Government-only — no private sector noise

**Assessment:** Config is well-targeted but Apollo's coverage of government employees is inherently limited. Expected results: 20-100 contacts from private-sector government contractors and larger agencies. Direct government employee coverage (actual BOP food service administrators, VA nutrition managers) will be sparse. **This is expected and why the multi-source playbook is essential.**

### Segment D — Corrections & Prison Food

**Configuration validated.** Key parameters:
- 11 title keywords focused on food service, commissary, procurement, operations, nutrition
- 18 org keywords including corrections, prison, detention, commissary, institutional food, facility services
- 8 priority companies: CoreCivic, GEO Group, Aramark, Trinity, Keefe, Summit, MTC, LaSalle
- Employee minimum: 51+ with revenue floors ($10M+)
- Warden, guard, correctional officer roles correctly excluded

**Assessment:** This is the strongest government-adjacent segment for Apollo because it targets private companies (CoreCivic, GEO Group, Aramark Corrections, Trinity, Keefe Group) that are well-indexed in Apollo. Expected results: 50-200 contacts at private corrections companies. State DOC contacts will be weaker. **Recommend running this live search first.**

### Segment E — Candy Wholesalers

**Configuration validated.** Key parameters:
- 14 title keywords covering purchasing, sales, commercial, wholesale, export, trading
- 17 org keywords including English (wholesale candy, confectionery distributor) and Spanish (distribuidora, mayorista, dulces, golosinas)
- 24 LATAM country locations
- Employee minimum: 11+ (captures small specialty distributors)
- Revenue minimum: $5M+ (appropriate for wholesale)
- Manufacturers (Hershey, Mars, Mondelez), retailers (Walmart, Costco), and irrelevant industries correctly excluded

**Assessment:** Well-configured for US market. LATAM coverage will vary — Mexico moderate, Central America/Caribbean weak. Spanish org keywords are a smart addition. **Recommend running US-only first, then LATAM separately to assess coverage gap.**

**Suggested refinements for next iteration:**
- Add "confitería" and "importador"/"importadora" to org keywords for LATAM
- Consider adding "broker" as a title keyword for LATAM markets where candy brokers are common intermediaries

---

## Decision Maker Identification — Can We Find Them?

### Government Contacts: Multi-Source Required

| Source | Expected Contacts | Quality | Cost | Best For |
|---|---|---|---|---|
| Apollo Segments C+D | 70-300 | Mixed | $5-$30 | Private corrections, FSMCs |
| FPDS Contract Awards | 20-50 | High | Free | Named contracting officers |
| Agency Directories | 30-80 | High | Free | Current facility staff |
| SAM.gov Entity Search | 50-200 | Moderate | Free | Federal entity POCs |
| LinkedIn | 50-150 | Moderate | Free-$99/mo | Individual profiles |
| State Procurement Portals | 10-30 | High | $50/yr | State buyers |
| Industry Associations (ACFSA, SNA) | 40-100 | Very High | $225-$725/yr | Engaged professionals |
| USDA AMS / Specialized | 5-15 | High | Free | Specific federal roles |
| **Total** | **275-925** | | **$300-$1,000/yr** | |

**Cost per validated government contact: $0.50-$5.00** (excluding time)
**ROI justification:** One government contract win ($100K-$5M+) pays for the entire contact sourcing effort 100x over

### Candy Contacts: Apollo-Centered

| Source | Expected Contacts | Quality | Cost |
|---|---|---|---|
| Apollo Segment E (US) | 100-400 | Good | Free search, $3-$40 for reveals |
| Apollo Segment E (LATAM) | 50-200 | Moderate | Free search |
| Trade show exhibitor lists | 50-100 | High | Conference attendance cost |
| Local trade directories (LATAM) | 20-80 | Variable | Mostly free |
| **Total** | **220-780** | | **$3-$200** |

---

## LATAM Trade Assessment — Key Findings

### Go / No-Go Decision: **GO** (with compliance investment)

**No regulatory show-stoppers for candy imports from LATAM.** However, three compliance requirements need investment before first import:

1. **FSVP compliance** — $10K-$20K setup, mandatory, 3-6 month lead time
2. **Lead testing protocol** — Critical for Mexican/Central American candy. Budget $50-$150/sample
3. **Color additive audit** — Several LATAM-common colors are banned in the US. Must audit before import

**Tariff situation is very favorable:**
- Mexico: Free under USMCA
- CAFTA-DR countries (Costa Rica, DR, Guatemala, Honduras, El Salvador, Nicaragua): Free or near-free
- Colombia: Free under bilateral TPA
- Sugar TRQs do NOT apply to finished confectionery (common misconception)

**Startup investment: $20K-$45K** for FSVP program, training, labels, customs, testing, and first supplier audits. This is modest relative to the import margins available.

**Miami port advantage:** #1 US gateway for LATAM trade, extensive cold chain, experienced FDA inspectors, short transit times (DR: 2-4 days, Central America: 3-7 days)

---

## Deliverables Produced

| Document | Location | Purpose |
|---|---|---|
| Government Contract Strategy | `strategy/government_contract_strategy.md` | 10-section comprehensive strategy, competitive landscape, entry playbook, 12-month roadmap |
| Government Contact Sourcing Playbook | `strategy/government_contact_sourcing_playbook.md` | 9 sourcing channels, expected hit rates, costs, recommended workflow |
| Candy & LATAM Trade Assessment | `strategy/candy_latam_trade_assessment.md` | Regulatory requirements, tariff analysis, startup costs, compliance checklist |
| Intelligence Assessment Summary | `strategy/intelligence_assessment_feb2026.md` | This document — consolidated findings |
| Market Size by NAICS (CSV) | `data/final/govt_market_size_by_naics_20260220_2132.csv` | USASpending FY2023-2025, 34 records |
| Market Size by Agency (CSV) | `data/final/govt_market_size_by_agency_20260220_2132.csv` | USASpending FY2023-2025, 73 records |

---

## Recommended Immediate Actions

### This Week
1. Run Apollo Segment D (corrections) live search — highest expected hit rate
2. Run Apollo Segment E (candy, US only) live search — validate distributor coverage
3. Run Apollo Segment C (government) live search — baseline assessment

### This Month
1. Register on SAM.gov (30-45 day process — start now)
2. Register on MyFloridaMarketPlace (MFMP)
3. Join ACFSA ($150/year) — corrections food service networking
4. Begin compiling FL school district Food Service Director contacts from district websites
5. Search FPDS for FL-based food contract Contracting Officers

### Next 90 Days
1. Create government capability statement
2. Submit USDA AMS Qualified Bidders List application
3. Attend FL School Nutrition Association conference
4. Contact FL BOP food service administrators at Coleman, Marianna, Miami, Tallahassee
5. Begin FSVP program development for LATAM candy imports
6. Run Apollo Segment E (LATAM) and assess coverage gaps

---

## Bug Fix Applied

During this session, fixed a `ModuleNotFoundError` in `scrapers/apollo_prospector.py` — the script was missing the `sys.path` insert that `contract_scanner.py` already had. Added the same pattern:

```python
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
```

This ensures `from enrichment.apollo_client import ApolloClient` resolves correctly when running the script from any directory.

---

*Assessment prepared from live USASpending.gov API data, Apollo.io dry run validation, federal regulatory research, and comprehensive source material analysis.*
