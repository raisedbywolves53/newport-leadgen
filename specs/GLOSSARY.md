# Newport Wholesalers — Glossary

> **Last Updated**: February 24, 2026
> **Status**: Draft
> **Depends On**: None

## Overview

Project-specific terms, abbreviations, and jargon used throughout the specification files. General programming terms are excluded — this covers government procurement, wholesale distribution, and project-specific vocabulary only.

---

## Terms

| Term | Definition | Used In |
|------|-----------|---------|
| **8(a) Program** | SBA's Business Development Program certifying socially and economically disadvantaged small businesses. In Jan 2026, SBA suspended 1,091 of 4,300 participants (25%) for failing to produce financial records during a fraud audit. DoW, Treasury, and GSA launched parallel audits. This creates a vendor vacuum that Newport can fill. | VISION, USER-STORIES |
| **BOP** | Bureau of Prisons (DOJ). Manages 122 federal institutions. One of Newport's top target agencies in FL ($5–7M/yr in food across 6 facilities). Uses Unison Marketplace for food procurement reverse auctions. | VISION, REQUIREMENTS, USER-STORIES, research.md |
| **Capability Statement** | A 1–2 page document that summarizes a company's qualifications, past performance, and differentiators for government buyers. Required for most government introductions. | REQUIREMENTS, requirements.md |
| **CLEATUS** | An AI-powered government contracting platform ($2,400–$3,600/yr) that provides solicitation parsing, compliance checking, proposal drafting, and CRM. Recommended as part of the "paid route." | REQUIREMENTS, ARCHITECTURE, requirements.md |
| **COGS** | Cost of Goods Sold. For Newport, this is the wholesale cost of food products before markup. Government contract margins are typically 18–25% depending on tier. | REQUIREMENTS (FR-003, FR-008) |
| **Competition Density** | FPDS-derived metric measuring how many vendors typically bid on contracts in a specific NAICS/agency combination. 537 awards across 32 combos analyzed. **15 combos rated LOW** (233 awards, $64.8M) — nearly half the biddable universe. LOW means agencies post requirements and get 0–2 bids. This is the primary basis for Newport's win rate projections. | REQUIREMENTS (FR-003, FR-006), research.md |
| **DeCA** | Defense Commissary Agency. Operates 236 military commissary stores ($4B+ resale). A Year 2+ opportunity for Newport as a supplier/distributor partner. | strategy.md |
| **DLA Troop Support** | Defense Logistics Agency division managing military food supply through 55 Prime Vendor contracts ($3.79B). Newport's entry path is subcontracting to existing prime vendors. | strategy.md |
| **DOGE** | Department of Government Efficiency. Coordinating government-wide audits of small business contracting. DoW must report all set-aside contract reviews to DOGE lead by Feb 28, 2026. Newport's clean history is positioned as an advantage in this environment. | VISION, DEVELOPMENT-PLAN |
| **DoW** | Department of War (renamed from Department of Defense under Trump administration). Secretary Hegseth ordered line-by-line review of all small business set-aside contracts >$20M on Jan 16, 2026. DoW has $18B in 8(a) spending and $80B+ in total small business spending — nearly 10x any other agency. | VISION, USER-STORIES |
| **FAR** | Federal Acquisition Regulation. The rules governing all federal procurement. Newport needs attorney review for first bids but does NOT need most complex FAR compliance (no DCAA, no CMMC, no CAS). | requirements.md, strategy.md |
| **FEMA** | Federal Emergency Management Agency. Relevant because Newport's FL warehouse is in a hurricane zone — disaster food supply contracts are event-driven but high-value. | REQUIREMENTS (FR-005), research.md |
| **FPDS** | Federal Procurement Data System. Contains award-level data for federal contracts. Used for competition density analysis (537 awards, 32 NAICS/agency combos analyzed). Free, no auth required. ⚠️ ezSearch decommissioned Feb 24, 2026; ATOM feed sunsetting later FY2026 — migration to SAM.gov contract awards search required. | ARCHITECTURE, INTEGRATIONS, research.md |
| **FSMC** | Food Service Management Company. Companies like Aramark, Compass, Sodexo that manage institutional food service. Newport could subcontract to FSMCs as a food supplier. | strategy.md |
| **GovSpend** | Paid platform ($3,000–$10,000/yr) providing micro-purchase and P-card spending data not available through free APIs. Covers the "invisible" sub-$15K market. | REQUIREMENTS, ARCHITECTURE, requirements.md |
| **HigherGov** | Paid platform ($2,000–$5,000/yr) providing SLED (state/local/education) opportunity data across 40,000+ agencies with NAICS-mapped alerts. | REQUIREMENTS, ARCHITECTURE, requirements.md |
| **HUBZone** | Historically Underutilized Business Zone. An SBA program that provides preferential access to government contracts for businesses in designated areas. Newport's eligibility is one of the Key Questions. | REQUIREMENTS (FR-004), financial models |
| **ICP** | Ideal Customer Profile. Used in the commercial SDR channel to define the 5 target segments (A through E) for outbound prospecting. | REQUIREMENTS (FR-009), icp_segments.md |
| **Key Questions** | The 10 prioritized questions in the financial model that Newport ownership must answer to calibrate all projections. Designed to show credibility ("we don't assume we know your business"). | REQUIREMENTS (FR-004) |
| **MFMP** | MyFloridaMarketPlace. Florida's state procurement portal. Registration is required to bid on FL state contracts. Free, but charged a 1% transaction fee on payments. | requirements.md, strategy.md |
| **Micro-Purchase** | Federal contract under $15,000 (threshold effective Oct 1, 2025). No formal competition required — any SAM-registered vendor can receive one. 83% of all federal food awards are micro-purchases. Newport's Year 1 entry point. | All spec files, financial models |
| **NAICS** | North American Industry Classification System. 6-digit codes classifying businesses. Newport's primary codes: 424410 (Grocery Wholesalers), 424450 (Confectionery), 424490 (Other Grocery). SBA size standard: $200M revenue. | All spec files |
| **Owner Earnings** | Buffett-derived financial metric: net income + depreciation - maintenance capex. Used in the v7 financial model as the primary profitability measure. "The only number that matters." | REQUIREMENTS (FR-003, FR-008), financial models |
| **Paid Route** | The recommended investment path: CLEATUS + HigherGov + GovSpend + free APIs ($7,400–$18,600/yr). Provides ~90% market coverage, 2–3x bid volume, higher win rates. | REQUIREMENTS (FR-001), financial models |
| **Free Route** | The zero-cost entry path: SAM.gov + FPDS + USASpending free APIs + manual portal monitoring. Covers ~40–50% of market, lower bid volume, slower ramp. | REQUIREMENTS (FR-001), financial models |
| **Past Performance** | A vendor's track record of successfully completing government contracts. The #1 evaluation factor in government proposals. Newport has zero government past performance — building it is the core Year 1 strategy. | VISION, REQUIREMENTS, strategy.md |
| **PSC** | Product Service Code. Federal codes for product categories. Newport-relevant: 8905 (Meat), 8910 (Dairy), 8915 (Produce), 8920 (Bakery), 8925 (Confectionery — Newport's strongest), 8940 (Special Dietary), 8945 (Oils), 8950 (Condiments), 8955 (Coffee/Tea), 8960 (Beverages). | research.md, financial models |
| **SAM.gov** | System for Award Management. The federal government's vendor registry. Registration is REQUIRED to bid on any federal contract. Free, but takes 2–4 weeks to validate. | All spec files |
| **SDB** | Small Disadvantaged Business. An SBA designation that qualifies businesses for set-aside contracts with higher win rates (28% vs. 8% open competition). Newport's eligibility is one of the Key Questions. | REQUIREMENTS (FR-004), financial models |
| **SDR** | Sales Development Representative. In the commercial channel, "SDR Agent" refers to the AI-powered system that sources prospects, enriches data, and automates outreach — replacing a human SDR role. | VISION, REQUIREMENTS (FR-009 through FR-011) |
| **Set-Aside** | Government contracts reserved for specific business categories (small business, SDB, HUBZone, SDVOSBC, WOSB). Limited competition = higher win rates. | REQUIREMENTS, financial models, strategy.md |
| **Simplified Acquisition** | Federal contracts between $15,000 and $350,000 (threshold effective Oct 1, 2025). Requires small business set-aside if 2+ qualified vendors exist. Less paperwork than full & open competition. Newport's Year 2–3 growth target. | All spec files, financial models |
| **SLED** | State, Local, and Education government agencies. FL school districts: **$1.04B/yr** (MEDIUM confidence — $358/student × 2.9M students, USDA NSLP data). FL county/municipal: **$45M/yr**. FL DOC: **$86.7M/yr but NOT biddable** (Aramark through April 2027). Requires different procurement portals than federal (MFMP, VendorLink, BidNet, DemandStar). | REQUIREMENTS (FR-002), USER-STORIES, research.md |
| **Sole Source** | A contract awarded without competition to a single vendor. Key stats: 93% sole source for NAICS 424490 at DoD (117 awards, $9.1M — bases literally can't find vendors), 100% sole source for Forest Service NAICS 722310 ($43.1M), 58% sole source for confectionery NAICS 424450 (with only 1 registered federal contractor nationally). These rates are the empirical foundation for Newport's win rate projections — we're not guessing, we're targeting categories where nobody else shows up. | REQUIREMENTS (FR-003, FR-006), research.md |
| **Sources Sought** | A government notice asking vendors to express interest in an upcoming contract. Not a solicitation — it's market research. Low-effort way for Newport to signal capability to contracting officers. | requirements.md, templates/ |
| **Still Mind Creative LLC** | The consulting entity (owned by the project lead) providing strategic and operational support to Newport at no consulting fee. Handling monitoring, bid prep, compliance, and admin. | VISION |
| **TAM** | Total Addressable Market. National federal food: $7.17B. FL federal under $350K: **$87M** (39,857 awards, re-confirmed Feb 24, 2026). Newport's SAM after filtering: $17–20M. FL SLED: school districts **$1.04B/yr** (MEDIUM confidence, USDA-derived), county/municipal $45M/yr, FL DOC excluded (Aramark through 2027). | REQUIREMENTS (FR-002), research.md |
| **Two Routes** | The central decision framework presented to Newport: Free Route (DIY, limited market access) vs. Paid Route (platform investment, full competitive capability). Appears in both the deck and financial model. | REQUIREMENTS (FR-001), financial models |
| **UEI** | Unique Entity Identifier. Replaced DUNS number for SAM.gov registration in April 2022. Required for all federal contracting. | requirements.md |
| **Unison Marketplace** | Reverse auction procurement platform used by BOP for food procurement solicitations. Newport must register (free) to bid on BOP quarterly food POs. Separate from SAM.gov. | INTEGRATIONS, USER-STORIES, DEVELOPMENT-PLAN |
| **USASpending** | USASpending.gov — federal award data. Free API, no auth. Source for TAM analysis, competitor analysis, contract examples. All Newport market data confirmed via live API runs Feb 2026. | ARCHITECTURE, research.md |
| **v7 Model** | The 7th iteration of the GovCon financial model (Excel). 5 sheets: Inputs, Two Routes, 5-Year Model, Market Analysis, Key Questions. Built via Claude Desktop. Current best version for Newport presentation. | REQUIREMENTS (FR-008) |

---

## Abbreviations

| Abbreviation | Meaning |
|-------------|---------|
| ABM | Account-Based Marketing |
| BPA | Blanket Purchase Agreement |
| COI | Certificate of Insurance |
| CRM | Customer Relationship Management |
| DoW | Department of War (formerly Department of Defense) |
| FFP | Firm-Fixed-Price (contract type) |
| GFSI | Global Food Safety Initiative |
| HACCP | Hazard Analysis Critical Control Points |
| IDIQ | Indefinite Delivery/Indefinite Quantity (contract type) |
| ITB | Invitation to Bid |
| NRA | National Restaurant Association |
| OE | Owner Earnings |
| P-card | Purchase Card (government credit card for micro-purchases) |
| RFP | Request for Proposal |
| RFQ | Request for Quotation |
| ROI | Return on Investment |
| SBA | Small Business Administration |
| SDVOSBC | Service-Disabled Veteran-Owned Small Business Concern |
| SKU | Stock Keeping Unit |
| SPV | Subsistence Prime Vendor (e.g., US Foods VA contract, $263M — excludes bread, milk, produce) |
| SQF | Safe Quality Food (certification) |
| WOSB | Women-Owned Small Business |

---

## Claude CLI Notes

When generating any content, use the exact terms defined here. If a term appears in this glossary, never substitute a synonym or abbreviation without the full form on first use. Pay special attention to "Two Routes" (always capitalized as a proper concept), "Owner Earnings" (Buffett-specific meaning), and "Key Questions" (refers specifically to the 10 prioritized questions in the financial model).
