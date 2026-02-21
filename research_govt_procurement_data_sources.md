# Government Food Procurement Data Sources & Intelligence Tools
## For Newport Wholesalers -- Tracking Contracts, Identifying Opportunities
### Research Date: February 20, 2026

---

# TABLE OF CONTENTS

1. [State Procurement Portals (APIs & Bulk Data)](#1-state-procurement-portals)
2. [Open Data Portals (data.gov & State-Level)](#2-open-data-portals)
3. [School District Food Procurement Databases](#3-school-district-food-procurement)
4. [Corrections Food Contract Data](#4-corrections-food-contracts)
5. [USDA Data Sources](#5-usda-data-sources)
6. [Federal Procurement Data (SAM.gov, FPDS, USASpending)](#6-federal-procurement-data)
7. [Commercial Competitive Intelligence Tools](#7-commercial-intelligence-tools)
8. [Recommended Stack for Newport](#8-recommended-stack)
9. [Key NAICS Codes for Searching](#9-naics-codes)
10. [Sources](#10-sources)

---

# 1. STATE PROCUREMENT PORTALS

## Which States Offer APIs or Bulk Data Downloads?

Most state procurement portals are web-searchable but do NOT offer formal APIs. Only a handful provide bulk download or programmatic access. Here is a ranked assessment:

### Tier 1: Most Transparent (Bulk Download + Searchable + Full Contract Text)

**Florida -- FACTS (Florida Accountability Contract Tracking System)**
- URL: https://facts.fldfs.com/
- Mandated by the "Transparency Florida Act" (Section 215.985(16), Florida Statutes)
- Search by vendor name (min 3 letters), agency, commodity/service code, contract ID
- Download commodity/service code lists to Excel
- Full contract text and procurement documents available via "Documents" tab
- Covers all contracts valued at $25,000+
- **Best feature:** Full text of original contracts AND amendments downloadable
- **No formal API** but structured enough for scraping

**California -- Cal eProcure + California Open Data Portal**
- Cal eProcure: https://caleprocure.ca.gov (solicitations and awards)
- Open Data Portal: https://data.ca.gov/dataset/purchase-order-data
- The open data portal publishes **Purchase Order Data** as a downloadable dataset
- California's State Contract and Procurement Registration System (SCPRS) has been a centralized database since 2003, covering contracts and purchases over $5,000
- Search by keyword, contract number, contract type, department, UNSPSC classification, or expiration date
- **Data download available in CSV format**

**New York -- NYS Procurement + Open Data**
- NYS Procurement: https://ogs.ny.gov/procurement
- Open Data: https://catalog.data.gov/dataset/procurement-report-for-state-authorities
- State authorities required to submit annual procurement reports
- Dataset covers 8+ fiscal years of procurement transactions valued $5,000+
- **Downloadable dataset** available on data.gov
- Also operates the NYS Contract Reporter for active bid opportunities

### Tier 2: Good Searchability, Limited Bulk Access

**Texas -- ESBD (Electronic State Business Daily) + Comptroller**
- ESBD: Active solicitations
- Texas Comptroller Statewide Procurement Division manages contracts
- eGrants portal for competitive funding
- Less bulk data download capability than FL/CA/NY

**North Carolina -- NC eProcurement**
- URL: https://eprocurement.nc.gov/
- State agencies, community colleges, school systems, and local governments use the system
- Aggregated purchasing data available
- One of the more data-oriented state procurement systems

**Pennsylvania -- eMarketplace**
- URL: https://www.emarketplace.state.pa.us
- Searchable contract database
- Limited bulk export

**Ohio -- Procurement Portal**
- URL: https://procure.ohio.gov
- Searchable but limited programmatic access

**Michigan -- SIGMA VSS**
- Vendor Self-Service portal
- Michigan Dept. of Education publishes detailed FSMC contract lists (see Section 3)

### Tier 3: Basic Web Search Only

Most other states offer basic searchable portals with no bulk download or API capability. Examples:
- Illinois: BidBuy (https://www.bidbuy.illinois.gov)
- Massachusetts: CommBuys
- Maryland: eMaryland Marketplace Advantage (EMMA)
- South Carolina: SC Procurement (https://procurement.sc.gov)

### Academic Resource: Clemson University Database of State Contract Portals

Patrick Warren at Clemson University has compiled a comprehensive list of state government contract database URLs:
- URL: https://www.sioe.org/online-databases-contracts-us-state-governments
- Covers all 50 states
- Notes which states allow downloading, full-text access, and advanced searching
- **This is the single best starting point for finding any state's contract portal**

---

# 2. OPEN DATA PORTALS

## data.gov Datasets

### Directly Relevant to Food Procurement

**Good Food Purchasing Data**
- URL: https://catalog.data.gov/dataset/good-food-purchasing-data
- Item-by-item list of food items purchased by city agencies
- Fields include: item description, weight, quantity, price, purchasing agency
- Focus on municipal food procurement transparency

**Procurement Report for State Authorities (New York)**
- URL: https://catalog.data.gov/dataset/procurement-report-for-state-authorities
- 8+ fiscal years of procurement data from NY state authorities
- Transactions valued at $5,000+
- Downloadable format

**Federal Procurement Data System (FPDS) API**
- URL: https://catalog.data.gov/dataset/federal-procurement-data-system-fpds-api
- API access to all federal contract data over the micro-purchase threshold
- Can filter by NAICS code (use 4244xx for grocery wholesalers)
- Covers contracts from all federal agencies

**Comprehensive Federal Procurement Dataset (1979-2023)**
- Published in Nature Scientific Data: https://www.nature.com/articles/s41597-025-05714-1
- Nearly 100 million contract actions over 45 years
- Academic dataset, downloadable in bulk
- Useful for historical trend analysis

### General Procurement Tag on data.gov
- URL: https://catalog.data.gov/dataset?tags=procurement
- Browse all datasets tagged "procurement"
- Mix of federal, state, and local datasets
- Quality and completeness varies widely

## State Open Data Portals with Procurement Data

**California Open Data**
- URL: https://data.ca.gov
- Purchase Order Data available as CSV download
- Links to other state portals: https://data.ca.gov/pages/state-portals

**GODORT (Government Documents Round Table) LibGuide**
- URL: https://godort.libguides.com/govfinancedbs
- Maintained by librarians; curated directory of state-level government finance and contracts databases
- Excellent meta-resource for finding state data portals

---

# 3. SCHOOL DISTRICT FOOD PROCUREMENT

## Is There a Centralized National Database?

**No single national database exists.** School food procurement is managed at the state and local level. However, several valuable resources exist:

## State-Level FSMC Contract Lists

Many states publish lists of which school food authorities (SFAs) have contracts with which Food Service Management Companies (FSMCs). These are gold mines for identifying who is serving which districts:

**California**
- 2025-26 SFAs with FSMC Contracts List
- URL: https://www.cde.ca.gov/ls/nu/sn/fsmcrebidlist.asp
- Lists every California school district using an FSMC, with company names
- Also see procurement guidance: https://www.cde.ca.gov/ls/nu/sn/fsmcproc.asp

**Michigan**
- School Year 2025-2026 SFA and FSMC List
- URL: https://www.michigan.gov/mde (search "FSMC contracts")
- Detailed PDF listing: sponsor name, agreement number, contract type (cost reimbursable vs. fixed), FSMC name (Chartwells, SodexoMagic, Taher, Aramark, etc.)

**Wisconsin**
- List of Known FSMCs Operating in Wisconsin for SY 2025-26
- URL: https://dpi.wi.gov/school-nutrition/program-requirements/procurement/required-template-agreements/fsmc

**New York**
- NYSED Child Nutrition FSMC page
- URL: https://www.cn.nysed.gov/fsmc
- SFAs must use state-approved bid specifications; contracts reviewed and approved by NYSED

**Texas**
- Food Service Management Company Contract List
- URL: https://squaremeals.org/Programs/National-School-Lunch-Program/Food-Service-Management-Companies
- Accessible through the Texas Department of Agriculture "Square Meals" system

## USDA-Level Data on School Food

**USDA FNS -- Procurement in Child Nutrition Programs**
- URL: https://www.fns.usda.gov/taxonomy/term/393
- Federal procurement regulations for all child nutrition programs
- Does NOT publish individual contract data but sets the rules all districts must follow

**Study of School Food Authority Procurement Practices**
- URL: https://www.fns.usda.gov/cn/study-school-food-authority-procurement-practices
- First comprehensive USDA study of SFA-level procurement decision-making
- Useful for understanding how districts buy, not for finding specific contracts

**USDA Foods Database (for vendors)**
- URL: https://www.fns.usda.gov/usda-fis/vendor
- Vendor-specific product information for all direct-delivered USDA Foods
- Nutrition and product data for items in the National School Lunch Program
- Relevant if Newport wants to become a USDA Foods vendor/processor

## Key Insight for Newport

The best approach to track school food contracts is:
1. Check the top 10-15 states' Dept. of Education websites for FSMC contract lists
2. Monitor individual large school district procurement pages for RFPs
3. Use the Urban School Food Alliance as a lead source (the largest districts)
4. Search SAM.gov for DoD Fresh Fruit and Vegetable Program contracts (USDA-DLA partnership serving schools)

---

# 4. CORRECTIONS FOOD CONTRACTS

## Public Data Sources

### Prison Policy Initiative -- Correctional Contracts Library
- URL: https://www.prisonpolicy.org/contracts/documents.html
- **The best public database for corrections procurement documents**
- Searchable by state, vendor, service type, and document type
- Includes food service contracts (cafeteria management), though commissary is the larger focus
- Documents come from: FOIA requests, litigation discovery, advocacy groups, anonymous tips
- Filter by "food service" category for relevant contracts
- Food service defined as: management of correctional facility cafeteria and purchasing food for the cafeteria

### The Appeal -- "Locked In, Priced Out" Commissary Database
- URL: https://theappeal.org/commissary-database/
- First national database of prison commissary lists
- Covers the vast majority of U.S. states
- Shows prices for products available in prison commissaries
- Useful for understanding pricing/margins in the commissary channel, NOT for tracking food service contracts per se

### Key Corrections Food Service Vendors (to Track)

The market is highly concentrated:

| Company | Parent | Role |
|---------|--------|------|
| **Trinity Services Group** | TKC Holdings (H.I.G. Capital) | #1 or #2 prison food service contractor |
| **Aramark Correctional Services** | Aramark Corporation | #1 or #2 prison food service contractor |
| **Keefe Group** | TKC Holdings (H.I.G. Capital) | Dominant commissary provider |
| **Summit Food Service** | Elior Group | Growing corrections food service |
| **ABL Management** | Elior Group | Corrections food service |

**Critical dynamic:** TKC Holdings owns BOTH Trinity Services Group (cafeteria food) AND Keefe Group (commissary). This vertical integration means they have structural incentives around food quality and commissary purchasing. Example: Oklahoma's 2025 contract with Trinity allots just over $5/prisoner/day for all food costs, staff wages, and admin.

### State DOC Procurement Portals

For state-level corrections food contracts, search each state's general procurement portal (see Section 1) filtered by the Department of Corrections. Some specific examples:
- **Idaho DOC** -- Dedicated procurement page: https://www.idoc.idaho.gov/content/management-services/contract-services-procurement
- **Pennsylvania DOC** -- Aramark holds the current food procurement contract
- **Oklahoma DOC** -- $74 million Trinity Services Group contract (2025)

### How to Systematically Find Corrections Food Contracts

1. Use the Prison Policy Initiative Contracts Library as a starting point
2. Search each state's procurement portal for "[Department of Corrections] AND [food service]"
3. Monitor SAM.gov for Federal Bureau of Prisons solicitations (BOP solicitations page: https://www.bop.gov/business/solicitations.jsp)
4. Set Google Alerts for "prison food contract" + state names

---

# 5. USDA DATA SOURCES

## USDA Publishes Several Relevant Datasets

### FNS Food Distribution Program Tables
- URL: https://www.fns.usda.gov/pd/food-distribution-program-tables
- **Four types of tables available:**
  1. Historical summaries (national trends)
  2. Annual state-level data for key metrics
  3. Monthly national-level data for major programs
  4. Latest month state-level participation data
- Covers: Schools, TEFAP, FDPIR, CSFP, Nutrition for the Elderly, Charitable Institutions
- **Downloadable** -- useful for sizing the market by state

### FNS Program Data Overview
- URL: https://www.fns.usda.gov/pd/overview
- Statistical information across all FNS programs
- Interactive FNS Program Participation Dashboard
- Good for understanding total program scale

### AMS Commodity Procurement -- Solicitations & Awards
- URL: https://www.ams.usda.gov/selling-food/solicitations
- Live and historical solicitations for USDA commodity purchases
- Covers 200+ food products
- Shows awarded vendors and prices
- **This is the closest thing to a "vendor contract database" USDA publishes**

### AMS Qualified Bidders List (QBL)
- URL: https://www.ams.usda.gov/selling-food/becoming-approved (then navigate to vendor resources)
- Lists which vendors are already approved to bid on which USDA Foods products
- The QBL/QPL (Qualified Bidders List / Qualified Products List) shows who the existing approved vendors are
- **Key competitive intelligence:** shows exactly who Newport would compete against for USDA commodity contracts

### AMS Purchase Announcements
- URL: https://www.ams.usda.gov/selling-food/purchase-announcements
- Advance notice of upcoming USDA commodity purchases
- Published before formal solicitations
- Useful for pipeline planning

### USDA -- Trends in Procurement Report (CRS R48141)
- URL: https://www.congress.gov/crs-product/R48141
- Congressional Research Service report on trends in USDA procurement of U.S. food and agricultural products
- High-level policy analysis, not granular contract data
- Useful for understanding program direction

### GAO -- Federal Food Purchases Report (GAO-24-106602)
- URL: https://www.gao.gov/assets/gao-24-106602.pdf
- GAO audit of federal food purchasing from small businesses
- Key finding: AMS and DLA account for >90% of all federal food purchases
- Shows breakdown of purchasing by agency, useful for prioritization

### Farmers to Families Food Box -- Previous Approved Vendors
- URL: https://www.ams.usda.gov/selling-food-to-usda/farmers-to-families-food-box/approved-contractors
- List of vendors approved during the COVID-era food box program
- Shows which distributors/wholesalers have USDA approval history
- Program has ended but the vendor list provides competitive intelligence

### What USDA Does NOT Publish
- **No centralized database of all vendor contracts** across all programs
- **No differentiation by vendor business type** (farm vs. distributor vs. wholesaler) in aggregate data
- **No real-time contract tracking** -- you must monitor solicitations and awards separately
- **Individual state-level USDA Foods distribution data** is managed by State Distributing Agencies, not published centrally at the contract level

---

# 6. FEDERAL PROCUREMENT DATA

## SAM.gov

### Contract Opportunities (Active Solicitations)
- URL: https://sam.gov/contracting
- Free to search, free to register
- Search by keyword, agency, NAICS code, PSC code, set-aside status
- **API access:** Public = 10 requests/day; Registered entities = 1,000/day
- API documentation: https://open.gsa.gov/api/ and https://govconapi.com/sam-gov-api-guide

### Contract Data (Historical Awards)
- URL: https://sam.gov/contract-data
- Search awarded contracts
- Contract Awards API: https://open.gsa.gov/api/contract-awards/
- Supports both revealed and unrevealed contract data based on user access level

### Entity Registration
- Required for any business wanting to bid on federal contracts
- Free registration
- Newport should register under NAICS 424410 (General Line Grocery Wholesalers) and related codes

### Bulk Data Downloads
- SAM.gov offers bulk data extracts
- Useful for large-scale analysis
- Documentation at GSA Open Technology portal

## FPDS (Federal Procurement Data System)
- URL: https://www.fpds.gov/
- Repository of ALL federal contracting data for contracts over $25,000
- Can search by agency, NAICS, PSC, vendor name, dollar amount, date range
- **Free, no registration required to search**
- Shows which agencies buy what, from whom, for how much
- FPDS-NG (Next Generation) is the current version
- API available via data.gov: https://catalog.data.gov/dataset/federal-procurement-data-system-fpds-api

### Recommended FPDS Searches for Newport
Search FPDS with these parameters to find food procurement contracts:
- NAICS: 424410 (General Line Grocery Wholesalers)
- NAICS: 424490 (Other Grocery Products Wholesalers)
- PSC: 89xx (Subsistence/Food category)
- Agency: Department of Agriculture, Department of Veterans Affairs, Department of Defense, Department of Justice (BOP)

## USASpending.gov
- URL: https://www.usaspending.gov/
- Tracks all federal spending including contracts, grants, loans
- **Full API:** https://api.usaspending.gov/
- Advanced Search allows filtering by NAICS, agency, recipient, location, date range
- Bulk download via Award Data Archive (historical data back to FY2001)
- Custom Award Download for filtered exports
- API supports spending-by-category/NAICS endpoint for aggregated analysis
- **API documentation:** https://api.usaspending.gov/docs/endpoints

### USASpending API -- Key Endpoints for Food Procurement
- `/api/v2/search/spending_by_category/naics/` -- Aggregate spending by NAICS code
- `/api/v2/search/spending_by_award_count/` -- Count of awards by filter criteria
- `/api/v2/bulk_download/` -- Bulk download with filters
- Filter by NAICS 424410, 424420-424490, 311xxx, 722310 for food-related contracts

---

# 7. COMMERCIAL INTELLIGENCE TOOLS

## Comparison of Paid Platforms

### Tier 1: Enterprise Platforms (Best Data, Highest Cost)

**Deltek GovWin IQ**
- URL: https://www.deltek.com/en/government-contracting/govwin
- Coverage: $700B+ in annual federal spending, 1.2M+ opportunities
- Features: Pre-RFP intelligence, analyst-curated opportunity reports, competitive landscape, pipeline management
- Pricing: ~$417-$2,083/month (varies by tier)
- Best for: Large government contractors with dedicated BD teams
- Food-specific: Can filter by NAICS/PSC codes for food procurement
- **Verdict for Newport: Too expensive and over-featured for a small wholesaler. Skip.**

**Bloomberg Government (BGOV)**
- URL: https://about.bgov.com/
- Coverage: Federal policy intelligence + procurement data
- Features: Policy analysis, contract data, agency spending analysis, regulatory tracking
- Pricing: ~$500-$1,250/month
- Best for: Companies that need policy intelligence alongside procurement data
- Unique advantage: Major reporting on policy changes that affect upcoming contracts
- **Verdict for Newport: Overkill. This is for policy analysts and defense contractors. Skip.**

### Tier 2: Mid-Range Platforms (Good Value)

**GovTribe**
- URL: https://govtribe.com/
- Coverage: Federal, state, and local contracting opportunities
- Features: NAICS/PSC filtering, contracting officer info, vehicle tracking, collaboration tools
- Pricing: Starts at ~$60/month; Standard Plan ~$5,500/year (5 seats)
- Free trial: 14 days, no credit card required
- Best for: Small-to-mid-size businesses doing federal contracting
- **Verdict for Newport: Worth the free trial. If Newport pursues federal contracts actively, the ~$60/month tier could be worthwhile.**

**GovSpend (formerly SmartProcure)**
- URL: https://govspend.com/
- Also see legacy brand: https://smartprocure.us/
- Coverage: **State, Local, and Education (SLED) + Federal** -- 85M+ purchase orders
- Features:
  - Historical purchase order data down to line-item level
  - Search by product, vendor, agency, location, quantity, price
  - Meeting Intelligence: AI transcription of public government meetings (identifies upcoming spending discussions)
  - Bid & RFP tracking
  - Full lifecycle view from planning discussion to PO issuance
- Pricing: Custom/quote-based (not publicly listed)
- Free tier: Available to government agencies only (they share their PO data in exchange)
- **Best for: Exactly Newport's use case** -- finding which government agencies buy food/grocery products, from whom, at what prices, in what quantities
- **Verdict for Newport: This is the #1 commercial tool to evaluate. Request a demo. The SLED-level purchase order data is precisely what Newport needs to identify prospects and understand competitive pricing.**

### Tier 3: Budget-Friendly / Free Options

**SAM.gov (Free)**
- Already covered in Section 6
- Free search, free API access
- Best free resource for federal opportunities
- Limitation: federal only, no state/local

**FPDS-NG (Free)**
- Already covered in Section 6
- Free historical federal contract search
- Best for competitive analysis (who won what contracts)

**USASpending.gov (Free)**
- Already covered in Section 6
- Free API, bulk downloads
- Best for spending analysis and trend identification

**HigherGov**
- URL: https://www.highergov.com/
- Free tier for basic federal contract search
- NAICS-based browsing (e.g., https://www.highergov.com/naics/424490-other-grocery-and-related-products-merchant-wholesalers/)
- Shows contract counts, award amounts, top agencies, top contractors by NAICS code
- **Verdict for Newport: Use the free tier for quick competitive lookups.**

**DemandStar**
- URL: https://network.demandstar.com/
- Free eProcurement platform focused on government contracting
- Covers state and local bid opportunities
- **Verdict for Newport: Worth signing up (free) for state/local bid notifications.**

**BidNet Direct**
- URL: https://www.bidnetdirect.com
- Coverage: State and local government bids
- Pricing: ~$9/state/month (Group Agencies), ~$36/state/month (State & Local), ~$45/state/month (Federal + State + Local)
- **Verdict for Newport: Affordable for targeted state monitoring. Start with 2-3 key states at $9-36/month each.**

**FindRFP**
- URL: https://www.findrfp.com/
- Government RFP aggregator
- Basic search functionality

**GovCon Contract Finder**
- URL: https://govcontractfinder.com/contracts
- Free search of 261K+ federal opportunities
- Basic but functional

### Tier 4: Niche / Specialized

**CDC Food Service Guidelines Toolkit -- Procurement Data**
- URL: https://www.cdc.gov/food-service-guidelines-toolkit/php/monitor-evaluate/procurement-data.html
- Guidance on tracking food procurement data for government wellness programs
- Not a data source per se, but useful for understanding what government buyers track

---

# 8. RECOMMENDED STACK FOR NEWPORT

## Free Tier (Start Here -- $0/month)

| Tool | Use Case | Action |
|------|----------|--------|
| **SAM.gov** | Federal contract opportunities + entity registration | Register Newport, set up saved searches for food NAICS codes |
| **FPDS.gov** | Competitive analysis (who wins federal food contracts) | Search by NAICS 4244xx to see current contract holders |
| **USASpending.gov** | Federal spending trends by agency and vendor | Run NAICS-based queries to size the federal food market |
| **HigherGov** (free tier) | Quick NAICS lookups, top contractors | Browse 424410/424490 pages for competitive landscape |
| **DemandStar** (free) | State/local bid notifications | Sign up for food-related bid alerts |
| **Florida FACTS** | Florida state contract research | Search food service contracts, download vendor data |
| **California Open Data** | California purchase order data | Download CSV of state purchases |
| **USDA AMS Solicitations** | USDA commodity procurement opportunities | Monitor for food commodity purchase announcements |
| **Prison Policy Contracts Library** | Corrections food contract intelligence | Search for food service contracts by state |

## Paid Tier (When Ready to Invest -- ~$100-500/month)

| Tool | Cost | Use Case |
|------|------|----------|
| **GovSpend** | Custom (request quote) | SLED purchase order data -- find exactly which agencies buy food, from whom, at what price |
| **BidNet Direct** | ~$9-45/state/month | State/local bid monitoring for target states |
| **GovTribe** | ~$60/month | Federal opportunity tracking with better filtering than free SAM.gov |

## Priority Actions

1. **Register on SAM.gov immediately** (free, takes ~10 days, required for federal contracts)
2. **Run FPDS searches** for NAICS 424410/424490 to understand competitive landscape
3. **Download Florida FACTS and California Open Data** food procurement records
4. **Check top 5 state FSMC lists** (CA, MI, TX, NY, WI) to identify school food contract holders
5. **Request a GovSpend demo** -- this is the single most valuable paid tool for Newport's use case
6. **Set up DemandStar alerts** for food procurement bids
7. **Monitor USDA AMS purchase announcements** weekly

---

# 9. KEY NAICS CODES FOR SEARCHING

When searching any of the above tools, use these NAICS codes:

| Code | Description | Relevance to Newport |
|------|-------------|---------------------|
| **424410** | General Line Grocery Merchant Wholesalers | **Primary code** -- covers Newport's core business |
| **424490** | Other Grocery and Related Products Merchant Wholesalers | **Primary code** -- broad grocery wholesale |
| **424420** | Packaged Frozen Food Merchant Wholesalers | If Newport distributes frozen |
| **424430** | Dairy Product Merchant Wholesalers | If Newport distributes dairy |
| **424440** | Poultry and Poultry Product Merchant Wholesalers | If Newport distributes poultry |
| **424450** | Confectionery Merchant Wholesalers | **Candy/confection specialty** |
| **424460** | Fish and Seafood Merchant Wholesalers | If applicable |
| **424470** | Meat and Meat Product Merchant Wholesalers | If applicable |
| **424480** | Fresh Fruit and Vegetable Merchant Wholesalers | If applicable |
| **722310** | Food Service Contractors | For finding FSMCs (competitors/partners) |

**SBA Size Standard for NAICS 424410:** $200M annual revenue (Newport likely qualifies as small business)
**SBA Size Standard for NAICS 424490:** 250 employees

PSC (Product Service Code) for food: **89xx** series (Federal Supply Group 89 -- Subsistence)

---

# 10. SOURCES

## State Procurement Portals
- [Florida FACTS](https://facts.fldfs.com/)
- [Florida DMS Contract Search](https://www.dms.myflorida.com/contract_search)
- [California Open Data -- Purchase Order Data](https://data.ca.gov/dataset/purchase-order-data)
- [California State Portals Directory](https://data.ca.gov/pages/state-portals)
- [Cal eProcure](https://caleprocure.ca.gov)
- [New York Procurement Report for State Authorities (data.gov)](https://catalog.data.gov/dataset/procurement-report-for-state-authorities)
- [NC eProcurement](https://eprocurement.nc.gov/)
- [Clemson University -- Online Databases of Contracts with US State Governments](https://www.sioe.org/online-databases-contracts-us-state-governments)
- [GODORT LibGuide -- Government Finances & Contracts Sources](https://godort.libguides.com/govfinancedbs)

## Open Data / data.gov
- [data.gov Procurement Datasets](https://catalog.data.gov/dataset?tags=procurement)
- [Good Food Purchasing Data](https://catalog.data.gov/dataset/good-food-purchasing-data)
- [Comprehensive Federal Procurement Dataset 1979-2023 (Nature)](https://www.nature.com/articles/s41597-025-05714-1)
- [FPDS API on data.gov](https://catalog.data.gov/dataset/federal-procurement-data-system-fpds-api)

## School Food Procurement
- [California Dept. of Education -- 2025-26 SFAs with FSMC Contracts](https://www.cde.ca.gov/ls/nu/sn/fsmcrebidlist.asp)
- [California Dept. of Education -- Procurement in School Nutrition](https://www.cde.ca.gov/ls/nu/sn/fsmcproc.asp)
- [Michigan Dept. of Education -- SY 2025-26 FSMC Contracts](https://www.michigan.gov/mde)
- [Wisconsin DPI -- FSMC Resources](https://dpi.wi.gov/school-nutrition/program-requirements/procurement/required-template-agreements/fsmc)
- [NYSED Child Nutrition -- FSMC](https://www.cn.nysed.gov/fsmc)
- [Texas Agriculture -- FSMC Contract List](https://squaremeals.org/Programs/National-School-Lunch-Program/Food-Service-Management-Companies)
- [USDA FNS -- Study of SFA Procurement Practices](https://www.fns.usda.gov/cn/study-school-food-authority-procurement-practices)
- [USDA FNS -- USDA Foods Vendor/Processor](https://www.fns.usda.gov/usda-fis/vendor)
- [USDA FNS -- Procurement in Child Nutrition](https://www.fns.usda.gov/taxonomy/term/393)
- [USDA FNS -- FSMC Contracts](https://www.fns.usda.gov/sfsp/food-service-management-company-contracts)

## Corrections Procurement
- [Prison Policy Initiative -- Correctional Contracts Library](https://www.prisonpolicy.org/contracts/documents.html)
- [The Appeal -- Commissary Database](https://theappeal.org/commissary-database/)
- [PESP -- H.I.G. Capital Prison Food and Commissary Report](https://pestakeholder.org/wp-content/uploads/2019/10/HIG-Capital-Prison-Food-Commissary-PESP-103019.pdf)
- [Idaho DOC -- Contract Services & Procurement](https://www.idoc.idaho.gov/content/management-services/contract-services-procurement)
- [Oklahoma Watch -- $74M Prison Food Contract](https://oklahomawatch.org/2025/06/09/oklahoma-inks-74-million-deal-to-privatize-prison-food-service/)

## USDA Data
- [USDA FNS -- Food Distribution Program Tables](https://www.fns.usda.gov/pd/food-distribution-program-tables)
- [USDA FNS -- Program Data Overview](https://www.fns.usda.gov/pd/overview)
- [USDA AMS -- Solicitations & Awards](https://www.ams.usda.gov/selling-food/solicitations)
- [USDA AMS -- Purchase Announcements](https://www.ams.usda.gov/selling-food/purchase-announcements)
- [USDA AMS -- Commodity Procurement Program](https://www.ams.usda.gov/about-ams/programs-offices/commodity-procurement)
- [USDA AMS -- Become an Approved Vendor](https://www.ams.usda.gov/selling-food/becoming-approved)
- [USDA AMS -- New Vendor Qualification Requirements (PDF)](https://www.ams.usda.gov/sites/default/files/media/CPPNewVendorQualificationRequirements.pdf)
- [USDA AMS -- Farmers to Families Food Box Approved Vendors](https://www.ams.usda.gov/selling-food-to-usda/farmers-to-families-food-box/approved-contractors)
- [USDA FNS -- Doing Business with FNS](https://www.fns.usda.gov/contracts)
- [GAO -- Federal Food Purchases (GAO-24-106602)](https://www.gao.gov/assets/gao-24-106602.pdf)
- [CRS -- Trends in USDA Procurement (R48141)](https://www.congress.gov/crs-product/R48141)

## Federal Procurement Systems
- [SAM.gov](https://sam.gov/)
- [SAM.gov Contracting](https://sam.gov/contracting)
- [SAM.gov Contract Data](https://sam.gov/contract-data)
- [SAM.gov API Guide (GovCon API)](https://govconapi.com/sam-gov-api-guide)
- [GSA Open Technology APIs](https://open.gsa.gov/api/)
- [GSA Contract Awards API](https://open.gsa.gov/api/contract-awards/)
- [FPDS-NG](https://www.fpds.gov/)
- [USASpending.gov](https://www.usaspending.gov/)
- [USASpending API](https://api.usaspending.gov/)
- [USASpending API Training (PDF)](https://www.usaspending.gov/data/Basic-API-Training.pdf)
- [USASpending Analyst Guide (PDF)](https://www.usaspending.gov/data/analyst-guide-download.pdf)
- [USASpending GitHub -- NAICS Endpoint](https://github.com/fedspendingtransparency/usaspending-api/blob/master/usaspending_api/api_contracts/contracts/v2/search/spending_by_category/naics.md)

## Commercial Intelligence Tools
- [Deltek GovWin IQ](https://www.deltek.com/en/government-contracting/govwin)
- [GovTribe](https://govtribe.com/)
- [GovSpend](https://govspend.com/)
- [SmartProcure (legacy)](https://smartprocure.us/)
- [BidNet Direct](https://www.bidnetdirect.com)
- [DemandStar](https://network.demandstar.com/)
- [HigherGov](https://www.highergov.com/)
- [HigherGov -- NAICS 424490](https://www.highergov.com/naics/424490-other-grocery-and-related-products-merchant-wholesalers/)
- [FindRFP](https://www.findrfp.com/)
- [GovCon Contract Finder](https://govcontractfinder.com/contracts)
- [SamSearch -- NAICS 4244](https://samsearch.co/naics-ai-lookup/4244)
- [NAICS Association](https://www.naics.com/search/)
- [CDC Food Service Guidelines -- Procurement Data](https://www.cdc.gov/food-service-guidelines-toolkit/php/monitor-evaluate/procurement-data.html)

## NAICS / Classification References
- [NAICS Code 4244 Description](https://www.naics.com/naics-code-description/?code=4244)
- [NAICS 424490 -- IBISWorld](https://www.ibisworld.com/classifications/naics/424490/other-grocery-and-related-products-merchant-wholesalers/)
- [Census Bureau -- NAICS 424490](https://www.census.gov/naics/?year=2007&input=424490&details=424490)
- [GSA Federal Schedules -- NAICS Codes in Government Contracting](https://gsa.federalschedules.com/resources/naics-codes-in-government-contracting/)
- [FY 2024 Government Contract Awards by NAICS Code](https://gsa.federalschedules.com/resources/naics-code-government-spending-report/)
