# REQUIREMENTS: Newport Wholesalers — Government Contract Command Center
## Technical Build Specification v1.0
## Author: Still Mind Creative LLC
## Date: February 22, 2026
## Status: AUTHORITATIVE — All technical implementation references this document

---

## DOCUMENT PURPOSE

This document defines the technical requirements for building Newport Wholesalers' Government Contract Command Center — the custom-built components of their government contracting intelligence system. It specifies what to build, what to buy, how they connect, and the exact specifications for each build.

This document is:
- **The source of truth** for all technical implementation via Claude CLI in VS Code
- **Referenced by** the client proposal (PPT) for technology cost line items
- **Separate from** the pro forma financial model (Excel), which models revenue/margin projections

---

## SYSTEM OVERVIEW

### What Newport Wholesalers Is
A 30-year grocery wholesaler (NAICS 424410/424450/424490) based in South Florida, entering government contracting for the first time. Target contract range: $10K–$350K. Primary markets: school districts, corrections facilities, military installations, FEMA disaster response, county/city agencies, VA hospitals, and food banks. Geographic focus: Southeast US (FL, GA, SC, NC, AL, TN, MS, LA, VA, TX), expanding nationally.

### What the Command Center Does
Centralizes all government contract opportunity intelligence into a single operational system. Tracks every relevant solicitation across federal, state, local, and education tiers. Manages the full lifecycle from discovery through bid decision, proposal, submission, and contract fulfillment.

### Architecture: Buy + Build + Connect

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMMAND CENTER (Notion)                       │
│         Master Pipeline Database + Dashboards + Reports         │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ Pipeline  │  │ Contacts │  │ Agencies │  │ Proposals    │   │
│  │ Tracker   │  │ Database │  │ Database │  │ & Documents  │   │
│  └────▲─────┘  └────▲─────┘  └────▲─────┘  └──────▲───────┘   │
│       │              │              │               │           │
└───────┼──────────────┼──────────────┼───────────────┼───────────┘
        │              │              │               │
   ┌────┴────┐    ┌────┴────┐   ┌────┴────┐    ┌─────┴─────┐
   │  DATA   │    │ CONTACT │   │ MARKET  │    │ PROPOSAL  │
   │  FEEDS  │    │ ENRICH  │   │  INTEL  │    │  ENGINE   │
   └────┬────┘    └────┬────┘   └────┬────┘    └─────┬─────┘
        │              │              │               │
  ┌─────┴──────┐  ┌────┴────┐  ┌─────┴─────┐  ┌─────┴─────┐
  │ SAM.gov    │  │Apollo.io│  │USASpending│  │ CLEATUS   │
  │ API Monitor│  │(existing)│ │ Dashboard │  │ (BUY)     │
  │ (BUILD)    │  │         │  │ (BUILD)   │  │           │
  ├────────────┤  └─────────┘  └───────────┘  └───────────┘
  │ HigherGov  │
  │ (BUY)      │
  ├────────────┤
  │ GovSpend   │
  │ (BUY)      │
  ├────────────┤
  │ Direct     │
  │ Portals    │
  │ (FREE)     │
  └────────────┘
```

---

## BUY vs. BUILD DECISION LOG

| Component | Decision | Rationale |
|-----------|----------|-----------|
| **SLED opportunity discovery (40K+ agencies)** | BUY (HigherGov) | Maintaining integrations with 40,000+ agency portals is impossible for a solo operator. HigherGov maps NAICS codes to state/local opps that don't natively use them. $2,000–$5,000/yr |
| **Micro-purchase / P-card intelligence** | BUY (GovSpend) | Purchase order data below formal solicitation thresholds is not publicly available. GovSpend has data-sharing agreements with agencies. Can't be scraped or built. $3,000–$10,000/yr |
| **AI proposal writing + compliance** | BUY (CLEATUS) | Solicitation shredding, compliance matrix generation, AI proposal drafting, pipeline CRM. Purpose-built for small GovCon operators. $2,400–$3,600/yr |
| **Federal opportunity monitoring** | BUILD | SAM.gov API is free, well-documented, 1,000 requests/day. Custom monitor gives independent data feed with exact filters Newport needs |
| **Competitive intelligence / TAM analysis** | BUILD | USASpending API is free, no auth required. Custom analysis answers Newport-specific questions no platform pre-answers |
| **Master pipeline / CRM** | BUILD (Notion) | CLEATUS has a CRM, but Newport needs a master tracker that aggregates across ALL sources (CLEATUS + HigherGov + GovSpend + SAM.gov monitor + direct portals). Notion is the central hub |
| **Bid/no-bid scoring framework** | BUILD | This is Newport-specific IP. No platform scores opportunities against Newport's exact capabilities, geography, and strategic priorities |
| **Reporting templates** | BUILD | Monthly reports to Newport leadership showing pipeline health, win rate, competitive positioning, recommendations |
| **Contact enrichment** | EXISTING (Apollo.io) | Already in the stack. Used for decision-maker identification and outreach |
| **Direct portal registrations** | MANUAL (Free) | 15–20 state, county, school district procurement portals. Must be registered directly |

### Annual Platform Costs (for PPT proposal reference)

| Platform | Tier | Annual Cost | What It Covers |
|----------|------|------------|---------------|
| CLEATUS | Essential | $2,400–$3,600 | AI proposal engine, Fed+State+Local discovery, compliance, CRM, document hub |
| HigherGov | Standard | $2,000–$5,000 | 40,000+ SLED agencies, NAICS-mapped alerts, award data, agency profiles |
| GovSpend | Standard | $3,000–$10,000 | Micro-purchase data, P-card spending, purchase order intelligence |
| Apollo.io | Existing | $0 (existing) | Contact enrichment for decision-maker outreach |
| SAM.gov API | Free | $0 | Federal opportunity feed |
| USASpending API | Free | $0 | Federal award data for competitive intel |
| State/county portals | Free | $0 | Direct registration, no subscription |
| **TOTAL PLATFORM COST** | | **$7,400–$18,600/yr** | |

---

## BUILD SPEC 1: SAM.gov Federal Opportunity Monitor

### Purpose
Automated daily monitor that queries the SAM.gov Opportunities API for solicitations matching Newport's NAICS codes, geography, and contract size range. Outputs new opportunities to a Google Sheet and sends notifications via email or Slack. Provides an independent federal data feed that Newport controls regardless of third-party platform availability.

### Technical Stack
- **Language:** Python 3.10+
- **Dependencies:** `requests`, `pandas`, `gspread`, `google-auth`, `python-dotenv`
- **API:** SAM.gov Contract Opportunities API v2
  - Docs: https://open.gsa.gov/api/get-opportunities-public-api/
  - Auth: Free API key (register at sam.gov, request from api.data.gov)
  - Rate limit: 1,000 requests/day
  - Format: JSON responses
- **Output:** Google Sheet (via Google Sheets API with service account)
- **Notifications:** Slack webhook (preferred) OR email via Resend API (Newport already uses Resend)
- **Scheduling:** GitHub Actions cron (free) OR local cron on always-on machine
- **Environment:** Runs headless. No UI needed. Config via `.env` file

### API Query Parameters

```python
# Primary filters — run daily
NAICS_CODES = ["424410", "424450", "424490"]
TARGET_STATES = ["FL", "GA", "SC", "NC", "AL", "TN", "MS", "LA", "VA", "TX"]
SOLICITATION_STATUS = ["active", "presolicitation"]
RESPONSE_DATE_RANGE = "next 90 days"  # Don't pull opportunities already past deadline

# Secondary filters — applied in post-processing
MIN_AWARD_AMOUNT = 10000
MAX_AWARD_AMOUNT = 350000
SET_ASIDE_CODES = [
    "SBA",      # Small Business Set-Aside
    "8A",       # 8(a) Business Development
    "HZC",      # HUBZone
    "SDVOSBC",  # Service-Disabled Veteran-Owned
    "WOSB",     # Women-Owned Small Business
    "NONE"      # Full and Open (no set-aside)
]
```

### Google Sheet Schema

| Column | Field | Source | Notes |
|--------|-------|--------|-------|
| A | `solicitation_number` | API: `solicitationNumber` | Primary key for dedup |
| B | `title` | API: `title` | Opportunity title |
| C | `agency` | API: `fullParentPathName` | Full agency hierarchy |
| D | `sub_agency` | API: `departmentName` | Sub-agency or office |
| E | `naics_code` | API: `naicsCode` | 6-digit NAICS |
| F | `set_aside` | API: `typeOfSetAside` | Small business preference type |
| G | `contract_type` | API: `typeOfSolicitation` | FFP, IDIQ, BPA, etc. |
| H | `award_floor` | API: `award.floor` | Minimum dollar value |
| I | `award_ceiling` | API: `award.ceiling` | Maximum dollar value |
| J | `posted_date` | API: `postedDate` | When solicitation was posted |
| K | `response_deadline` | API: `responseDeadLine` | Submission due date |
| L | `days_until_deadline` | Calculated | `response_deadline - today` |
| M | `pop_state` | API: `placeOfPerformance.state` | Place of performance state |
| N | `pop_city` | API: `placeOfPerformance.city` | Place of performance city |
| O | `contact_name` | API: `pointOfContact[0].fullName` | Contracting officer name |
| P | `contact_email` | API: `pointOfContact[0].email` | Contracting officer email |
| Q | `contact_phone` | API: `pointOfContact[0].phone` | Contracting officer phone |
| R | `solicitation_url` | Constructed | `https://sam.gov/opp/{solicitationNumber}` |
| S | `status` | Manual | `New` / `Reviewed` / `Bid` / `No-Bid` / `Submitted` / `Awarded` / `Lost` |
| T | `bid_score` | Manual | Score from bid/no-bid matrix (0-100) |
| U | `notes` | Manual | Free text for context |
| V | `first_seen` | Auto | Timestamp when monitor first captured this opportunity |
| W | `last_updated` | Auto | Timestamp of most recent API data change |
| X | `amendments` | Auto | Count of solicitation amendments detected |

### Logic Flow

```
1. Load .env config (API key, Google Sheets credentials, Slack webhook URL)
2. Query SAM.gov API for each NAICS code + active status
   - Paginate through all results (API returns max 1000 per request)
   - Apply state filter
3. Parse JSON responses into flat records
4. Load existing Google Sheet data
5. For each API result:
   a. If solicitation_number NOT in existing sheet → NEW opportunity
      - Append to sheet with status = "New"
      - Add to notification batch
   b. If solicitation_number IS in existing sheet → check for changes
      - Compare response_deadline, title, amendment count
      - If changed → update row, increment amendments column, add to notification batch
   c. If existing sheet row has response_deadline in the past and status = "New" → mark "Expired"
6. Apply dollar range filter (post-processing since API doesn't always have award amounts)
7. Sort sheet by response_deadline ascending (most urgent first)
8. Send notification batch:
   - Slack: Summary message with count of new opps + link to sheet
   - Include top 3 new opportunities with title, agency, deadline, dollar range
9. Log run timestamp and result count
```

### Error Handling
- API rate limit: If 429 response, back off 60 seconds and retry (max 3 retries)
- API timeout: 30 second timeout per request. Log and continue to next NAICS code
- Google Sheets API failure: Write results to local CSV as fallback. Retry sheet upload on next run
- Malformed API data: Skip record, log warning with solicitation number

### File Structure
```
sam-monitor/
├── .env                    # API keys, webhook URLs, sheet ID
├── .env.example            # Template with required vars documented
├── requirements.txt        # Python dependencies
├── monitor.py              # Main script
├── config.py               # NAICS codes, states, filters, column mappings
├── sam_api.py              # SAM.gov API client (auth, pagination, parsing)
├── sheets.py               # Google Sheets read/write operations
├── notify.py               # Slack/email notification functions
├── README.md               # Setup instructions
└── .github/
    └── workflows/
        └── daily-scan.yml  # GitHub Actions cron config (6:00 AM ET daily)
```

### Setup Requirements
1. SAM.gov API key: Register at https://api.data.gov/signup/ (free, instant)
2. Google Cloud service account: Create project → enable Sheets API → create service account → download JSON key → share target Google Sheet with service account email
3. Slack webhook: Create incoming webhook in Slack workspace settings (optional, can use email instead)
4. GitHub repo: For hosting code + GitHub Actions scheduling (free for public repos, or use private with free tier minutes)

### Estimated Build Time
2–3 hours with Claude CLI

---

## BUILD SPEC 2: USASpending Competitive Intelligence Dashboard

### Purpose
Analyzes federal contract award data to answer three critical questions for Newport:
1. **TAM:** How much total federal spending exists in Newport's NAICS codes across target states?
2. **Competitors:** Who is winning these contracts, how much, from which agencies?
3. **Expiring Contracts:** Which current contracts in Newport's space are expiring in the next 6–18 months (recompete opportunities)?

This is a batch analysis tool, not a real-time monitor. Run on-demand or monthly to refresh data.

### Technical Stack
- **Language:** Python 3.10+
- **Dependencies:** `requests`, `pandas`, `matplotlib`, `openpyxl`
- **API:** USASpending.gov API v2
  - Docs: https://api.usaspending.gov/
  - Auth: None required (fully public)
  - Rate limit: Generous (no documented hard limit, but be respectful)
  - Format: JSON (POST requests with filter bodies)
- **Output:** Excel workbook with multiple tabs + PNG charts + Markdown summary

### Analysis 1: Total Addressable Market

**API Endpoint:** `POST /api/v2/search/spending_by_award/`

**Filters:**
```python
{
    "filters": {
        "naics_codes": ["424410", "424450", "424490"],
        "place_of_performance_locations": [
            {"country": "USA", "state": "FL"},
            {"country": "USA", "state": "GA"},
            {"country": "USA", "state": "SC"},
            {"country": "USA", "state": "NC"},
            {"country": "USA", "state": "AL"},
            {"country": "USA", "state": "TN"},
            {"country": "USA", "state": "MS"},
            {"country": "USA", "state": "LA"},
            {"country": "USA", "state": "VA"},
            {"country": "USA", "state": "TX"}
        ],
        "time_period": [
            {"start_date": "2022-10-01", "end_date": "2023-09-30"},
            {"start_date": "2023-10-01", "end_date": "2024-09-30"},
            {"start_date": "2024-10-01", "end_date": "2025-09-30"}
        ]
    }
}
```

**Output (Excel Tab: "TAM Analysis"):**

| Column | Data |
|--------|------|
| Fiscal Year | FY2023, FY2024, FY2025 |
| State | Target state |
| NAICS Code | 424410 / 424450 / 424490 |
| Total Obligated ($) | Sum of all awards |
| Number of Awards | Count |
| Average Award Size | Total / Count |
| Top Awarding Agency | Agency with highest spend |
| YoY Growth (%) | Year-over-year change |

**Output (PNG: "tam_by_state.png"):**
Horizontal bar chart showing total spend by state, color-coded by NAICS code.

### Analysis 2: Competitor Landscape

**API Endpoint:** `POST /api/v2/search/spending_by_award/` with recipient fields

**Output (Excel Tab: "Competitors"):**

| Column | Data |
|--------|------|
| Company Name | Award recipient name |
| UEI / DUNS | Unique identifier |
| Total Awards ($) | Sum across all contracts in scope |
| Number of Contracts | Count of distinct awards |
| Primary Agency | Agency they win most from |
| Average Contract Size | Total / Count |
| States Covered | List of states they perform in |
| Small Business Status | Yes/No |
| Largest Single Award | Max individual contract value |

Sort by Total Awards descending. Flag the top 20 competitors.

**Output (PNG: "competitor_share.png"):**
Pie chart showing market share of top 10 competitors + "Other" category.

### Analysis 3: Expiring Contract Pipeline

**API Endpoint:** `POST /api/v2/search/spending_by_award/` with period of performance filters

**Filters:** Active contracts (current period of performance includes today) in target NAICS + states

**Output (Excel Tab: "Expiring Contracts"):**

| Column | Data |
|--------|------|
| Contract Number | PIID |
| Incumbent | Current awardee name |
| Awarding Agency | Federal agency |
| Sub-Agency | Specific office |
| NAICS Code | Contract NAICS |
| Total Value | Contract ceiling |
| Annual Value (est.) | Total / years |
| Period of Performance End | Contract end date |
| Months Until Expiration | Calculated |
| Urgency Flag | 🔴 < 6 months / 🟡 6-12 months / 🟢 12-18 months |
| State | Place of performance |
| Contracting Officer | If available |

Sort by Period of Performance End ascending (soonest expiration first).

This tab IS the "pre-RFP pipeline" — these contracts will be recompeted, and Newport can begin positioning before the new solicitation drops.

### File Structure
```
usaspending-intel/
├── .env                    # (optional) any config overrides
├── requirements.txt
├── analyze.py              # Main script — runs all 3 analyses
├── api_client.py           # USASpending API client (POST requests, pagination)
├── tam_analysis.py         # TAM calculations + chart generation
├── competitor_analysis.py  # Competitor landscape + chart generation
├── expiration_tracker.py   # Expiring contract identification + flagging
├── config.py               # NAICS codes, states, fiscal year ranges
├── output/                 # Generated files land here
│   ├── newport_intel_report.xlsx
│   ├── tam_by_state.png
│   ├── competitor_share.png
│   └── summary.md          # Markdown summary of key findings
└── README.md
```

### Estimated Build Time
3–4 hours with Claude CLI

---

## BUILD SPEC 3: Master Pipeline Tracker (Notion Database)

### Purpose
Central hub that aggregates ALL opportunities from ALL sources into one pipeline view. This is where bid/no-bid decisions are made, proposals are tracked, and performance is measured. CLEATUS has its own CRM, but the Notion tracker is the master record because it includes opportunities from HigherGov, GovSpend, direct portals, and referrals that CLEATUS may not capture.

### Why Notion (Not Google Sheets)
- Zack already uses Notion for documentation and project management
- Relational databases (opportunities linked to agencies, contacts, proposals)
- Multiple views (pipeline board, deadline calendar, dashboard)
- API available for future automation if needed
- Better for long-term scaling than a spreadsheet

### Database: Opportunities

**Properties:**

| Property | Type | Values / Notes |
|----------|------|---------------|
| `Opportunity Name` | Title | Solicitation title |
| `Solicitation Number` | Text | Official solicitation ID |
| `Source` | Select | `SAM.gov Monitor` / `CLEATUS` / `HigherGov` / `GovSpend` / `BidNet` / `DemandStar` / `Direct Portal` / `Referral` / `Outbound` |
| `Government Tier` | Select | `Federal` / `State` / `County` / `City` / `School District` / `University` / `Special District` / `FEMA` |
| `Buyer Category` | Select | `K-12 School Meals` / `Corrections` / `Military/DLA` / `VA Hospital` / `FEMA Disaster` / `County General` / `City General` / `University Dining` / `Food Bank/LFPA` / `State Agency` / `Other` |
| `Agency` | Relation | → Agencies database |
| `State` | Select | All 50 states |
| `NAICS Code` | Select | `424410` / `424450` / `424490` / `Other` |
| `Contract Size (est.)` | Number (currency) | Estimated total value |
| `Annual Value (est.)` | Number (currency) | Estimated annual if multi-year |
| `Set-Aside` | Select | `None` / `Small Business` / `8(a)` / `HUBZone` / `SDVOSB` / `WOSB` |
| `Posted Date` | Date | When solicitation was published |
| `Response Deadline` | Date | Submission due date |
| `Days Until Deadline` | Formula | `dateBetween(prop("Response Deadline"), now(), "days")` |
| `Stage` | Select | `Identified` → `Qualifying` → `Bid Decision` → `Capture` → `Drafting Proposal` → `Review` → `Submitted` → `Under Evaluation` → `Awarded` → `Lost` → `No-Bid` → `Cancelled` |
| `Bid/No-Bid Score` | Number | 0–100 from scoring matrix |
| `Decision Maker` | Relation | → Contacts database |
| `Contracting Officer` | Relation | → Contacts database |
| `Incumbent` | Text | Current contract holder (for recompetes) |
| `Competition Level` | Select | `Sole Source` / `2-3 Bidders` / `5+ Bidders` / `Unknown` |
| `Evaluation Criteria` | Multi-select | `Lowest Price` / `Best Value` / `Past Performance` / `Technical Approach` / `Small Business Preference` |
| `Proposal Link` | URL | Link to Google Drive folder or CLEATUS proposal |
| `Proposal Status` | Select | `Not Started` / `Outline` / `First Draft` / `Review` / `Final` / `Submitted` |
| `Outcome` | Select | `Won` / `Lost` / `Withdrawn` / `Cancelled` / `Pending` |
| `Win/Loss Notes` | Text | Debrief learnings |
| `Contract Value (actual)` | Number (currency) | If won — actual award amount |
| `Contract Start` | Date | If won |
| `Contract End` | Date | If won |
| `Recompete Alert` | Formula | If won: `dateSubtract(prop("Contract End"), 6, "months")` |
| `Created` | Created time | Auto |
| `Last Updated` | Last edited time | Auto |

### Database: Agencies

| Property | Type | Notes |
|----------|------|-------|
| `Agency Name` | Title | Full name |
| `Tier` | Select | Federal / State / County / City / School District / University |
| `State` | Select | |
| `Procurement Portal URL` | URL | Direct link to their bid portal |
| `Registration Status` | Select | `Not Registered` / `Registered` / `Approved Vendor` |
| `Key Contact` | Relation | → Contacts database |
| `Annual Food Spend (est.)` | Number | If known from GovSpend/USASpending |
| `Current Vendor` | Text | Who currently supplies them |
| `Contract Expiration` | Date | When current food supply contract ends |
| `Notes` | Text | Relationship context, procurement preferences |
| `Opportunities` | Relation | → Opportunities database (reverse) |

### Database: Contacts

| Property | Type | Notes |
|----------|------|-------|
| `Name` | Title | Full name |
| `Title` | Text | Job title |
| `Agency` | Relation | → Agencies database |
| `Email` | Email | |
| `Phone` | Phone | |
| `Role` | Select | `Contracting Officer` / `Food Service Director` / `Procurement Specialist` / `Program Manager` / `Decision Maker` / `SBLO (Small Business Liaison)` / `Emergency Mgmt` |
| `Source` | Select | `Apollo.io` / `CLEATUS` / `GovWin` / `SAM.gov` / `Conference` / `Referral` |
| `Last Contact Date` | Date | When we last reached out |
| `Relationship Status` | Select | `Cold` / `Introduced` / `Active` / `Champion` |
| `Notes` | Text | Conversation history, preferences |

### Views

| View Name | Type | Filter/Sort | Purpose |
|-----------|------|-------------|---------|
| **Active Pipeline** | Board (Kanban) | Group by Stage. Filter: Stage ≠ No-Bid, Lost, Cancelled | Main working view — see all active opportunities by stage |
| **Deadlines This Week** | Table | Filter: Days Until Deadline ≤ 7 AND Stage ∈ {Bid Decision, Capture, Drafting, Review}. Sort: Response Deadline asc | Urgency view — what needs attention now |
| **Bid Decisions Needed** | Table | Filter: Stage = Qualifying OR Stage = Bid Decision. Sort: Bid/No-Bid Score desc | Decision queue — score and decide |
| **Submitted — Awaiting Results** | Table | Filter: Stage = Submitted OR Stage = Under Evaluation. Sort: Response Deadline asc | Tracking submitted bids |
| **Won Contracts** | Table | Filter: Outcome = Won. Sort: Contract End asc | Active contract management + recompete tracking |
| **Recompete Pipeline** | Table | Filter: Outcome = Won AND Recompete Alert ≤ today + 180 days. Sort: Contract End asc | Upcoming recompetes |
| **Monthly Report** | Table | Filter: Last Updated within last 30 days. Sort: Stage | Monthly reporting rollup |
| **By Buyer Category** | Board | Group by Buyer Category | Strategic view — where is the pipeline concentrated? |
| **By State** | Board | Group by State | Geographic distribution |
| **Win/Loss Analysis** | Table | Filter: Outcome = Won OR Outcome = Lost | Win rate analysis, debrief review |

### Estimated Build Time
2–3 hours to set up databases, properties, relations, and views in Notion

---

## BUILD SPEC 4: Bid/No-Bid Scoring Framework

### Purpose
Standardized scoring methodology for evaluating every opportunity. Prevents wasting time on low-probability bids and creates a data-driven decision record that improves over time.

### Scoring Matrix

| Factor | Weight | Score 1 (Poor Fit) | Score 3 (Moderate) | Score 5 (Strong Fit) |
|--------|--------|--------------------|--------------------|---------------------|
| **NAICS Alignment** | 15% | Tangential to Newport's capabilities | Partially aligned | Exact match to core grocery/food distribution |
| **Geography** | 15% | Outside delivery radius, would need partners | Within target 10-state region | Within South Florida direct delivery zone |
| **Contract Size** | 10% | Under $5K or over $500K | $5K–$10K or $350K–$500K | $10K–$350K sweet spot |
| **Competition Level** | 10% | Wired to incumbent, 10+ bidders expected | Moderate competition, 3-5 bidders | Small business set-aside, <3 bidders, new requirement |
| **Past Performance Requirement** | 15% | Requires 3+ government references (Newport has 0) | Requires 1 government reference OR accepts commercial | No PP requirement, or new entrant friendly |
| **Evaluation Criteria Fit** | 10% | Heavy technical/innovation weighting | Balanced technical + price | Lowest Price Technically Acceptable (LPTA) or price-dominant |
| **Relationship Status** | 10% | No contact with agency, unknown buyer | Some awareness, attended industry day | Direct relationship with contracting officer or end user |
| **Timeline Feasibility** | 10% | Deadline < 7 days, complex proposal required | 14–30 days, moderate proposal | 30+ days, or simple quote/price sheet format |
| **Strategic Value** | 5% | One-time purchase, no follow-on potential | Moderate follow-on or relationship value | Opens door to larger contracts, key agency, builds PP |

### Scoring Calculation
```
Total Score = Σ (Factor Score × Factor Weight) / 5 × 100

Example:
  NAICS: 5 × 0.15 = 0.75
  Geography: 5 × 0.15 = 0.75
  Size: 5 × 0.10 = 0.50
  Competition: 3 × 0.10 = 0.30
  Past Perf: 3 × 0.15 = 0.45
  Eval Criteria: 5 × 0.10 = 0.50
  Relationship: 1 × 0.10 = 0.10
  Timeline: 3 × 0.10 = 0.30
  Strategic: 5 × 0.05 = 0.25
  
  Raw = 3.90 / 5 × 100 = 78 → BID
```

### Decision Thresholds
- **80–100:** Strong Bid — pursue aggressively
- **65–79:** Bid — pursue with standard effort
- **50–64:** Review — discuss with Newport, may bid if strategic
- **Below 50:** No-Bid — document reason, move on

### Implementation
This matrix should be implemented as:
1. A Notion template page linked from each Opportunity record
2. A simple Google Sheet calculator (for quick scoring before entering into Notion)
3. Over time, compare scores against actual outcomes to calibrate weights

---

## BUILD SPEC 5: Monthly Reporting Template

### Purpose
Structured monthly report delivered to Newport leadership showing pipeline health, activity, wins/losses, competitive positioning, and strategic recommendations. This is how Still Mind Creative demonstrates ROI.

### Report Sections

**1. Executive Summary** (1 paragraph)
Key highlights: opportunities identified, bids submitted, wins, pipeline value, notable developments.

**2. Pipeline Snapshot**
- Total active opportunities: count + total estimated value
- By stage: Identifying / Qualifying / Proposing / Submitted / Awaiting Result
- By buyer category: School districts / Corrections / Military / FEMA / County / Other
- By state
- New this month vs. carried over

**3. Activity Log**
- Opportunities identified this month: count + list
- Bid/No-bid decisions: count bid + count no-bid + reasons for top no-bids
- Proposals submitted: count + list with agency, value, deadline
- Results received: wins + losses + pending

**4. Win/Loss Report**
- Win rate: (wins / total decisions) trailing 90 days
- Average won contract size
- Debrief summaries on losses (what to improve)
- Past performance library update (new references from wins)

**5. Competitive Intelligence**
- Key competitor movements (from USASpending + GovWin)
- Contracts expiring in next 6 months (recompete pipeline)
- New agencies or programs identified

**6. Recommendations**
- Strategic priorities for next month
- Registration/certification actions needed
- Relationship outreach targets
- Upcoming solicitation cycles (school district RFPs, FEMA pre-hurricane, etc.)

### Format
Markdown document generated monthly. Can be converted to PDF or PPT for Newport presentation.

### Estimated Build Time
1 hour for template creation. ~2 hours monthly to populate with real data.

---

## REGISTRATIONS REQUIRED (Manual — Not Buildable)

These must be completed by Newport (with Still Mind guidance) before any bidding can begin:

### Critical Path (Weeks 1–2)

| Registration | URL | Timeline | Blocker? |
|-------------|-----|----------|----------|
| **SAM.gov** (UEI + entity registration) | sam.gov | 2–4 weeks for validation | YES — cannot bid on any federal contract without this |
| **SAM.gov Disaster Response Registry** | sam.gov (opt-in during registration) | Same as above | No, but critical for FEMA positioning |
| **MyFloridaMarketPlace (MFMP)** | vendor.myfloridamarketplace.com | 1–2 weeks | YES — cannot bid on FL state contracts without this |

### Priority Registrations (Weeks 2–4)

| Registration | System | Notes |
|-------------|--------|-------|
| Miami-Dade County | BidSync / Periscope | Free |
| Broward County | BPRO (Bonfire) | Free |
| Palm Beach County | Vendor Self Service | Free |
| City of Miami | BidSync | Free |
| City of Fort Lauderdale | BidSync | Free |
| Miami-Dade County Public Schools | iSupplier Portal | Free — #1 priority school district |
| Broward County Public Schools | BidNet / direct | Free |
| Palm Beach County School District | VendorLink | Free |

### Expansion Registrations (Month 2+)

| Registration | URL | Notes |
|-------------|-----|-------|
| Georgia Team | teamgeorgia.org | GA state procurement |
| SC Procurement | procurement.sc.gov | SC state |
| NC eProcurement | eprocurement.nc.gov | NC state |
| Alabama Purchasing | purchasing.alabama.gov | AL state |
| Tennessee Procurement | tn.gov/generalservices/procurement | TN state |
| FEMA Vendor Profile | Email to fema-industry@fema.dhs.gov | Free, manual submission |
| TIPS/TAPS Cooperative | tips-usa.com | National co-op vehicle |
| Sourcewell Cooperative | sourcewell-mn.gov | National co-op vehicle |
| OMNIA Partners | omniapartners.com | National co-op vehicle |

### Compliance Prerequisites

| Requirement | Status | Action |
|-------------|--------|--------|
| Food Safety Certification (SQF, HACCP, or equivalent) | Verify with Newport | Many solicitations require this. If not current, budget $2,000–$10,000 |
| General Liability Insurance ($1M–$5M) | Verify coverage | Most RFPs specify minimum coverage |
| Workers Compensation Insurance | Verify current | Required |
| Commercial Auto Insurance | Verify current | Required for delivery contracts |
| Florida Business License | Presumably current | Verify |
| FSMA Compliance | Verify with Newport | FDA Food Safety Modernization Act |
| Buy American Certification | Verify sourcing | Required for school meal contracts |

---

## IMPLEMENTATION SEQUENCE

### Phase 1: Foundation (Weeks 1–4)
1. ☐ Newport begins SAM.gov registration (UEI + entity + Disaster Response Registry)
2. ☐ Newport begins MFMP registration
3. ☐ Start CLEATUS 7-day free trial — load company profile, NAICS, capabilities
4. ☐ Start HigherGov free trial — configure NAICS alerts for all 10 SE states
5. ☐ **BUILD: SAM.gov API Monitor** (Claude CLI, 2–3 hours)
6. ☐ **BUILD: USASpending TAM + Competitor Dashboard** (Claude CLI, 3–4 hours)
7. ☐ **BUILD: Notion Pipeline Tracker** (2–3 hours)
8. ☐ Register on South Florida county + school district portals (manual, ongoing)
9. ☐ Submit FEMA Vendor Profile Form

### Phase 2: Activate (Weeks 5–8)
10. ☐ Evaluate CLEATUS trial → subscribe if validated (Essential tier)
11. ☐ Evaluate HigherGov trial → subscribe if SLED coverage is strong
12. ☐ **BUILD: Bid/No-Bid Scoring Framework** in Notion
13. ☐ **BUILD: Monthly Report Template**
14. ☐ Prepare Newport Capability Statement (using CLEATUS AI or Claude)
15. ☐ Identify first 10 target opportunities across all sources
16. ☐ Begin state portal registrations (GA, SC, NC, AL, TN)
17. ☐ Request GovSpend demo/trial

### Phase 3: First Bids (Weeks 9–16)
18. ☐ Score and make bid/no-bid decisions on first targets
19. ☐ Draft and submit first 3–5 proposals (prioritize: small, FL-based, food supply, low PP barrier)
20. ☐ Activate GovSpend subscription
21. ☐ Begin decision-maker outreach via Apollo.io (school food service directors, county procurement)
22. ☐ Attend Florida PTAC for free GovCon counseling
23. ☐ Apply for cooperative purchasing vehicles (TIPS, Sourcewell, OMNIA)
24. ☐ Deliver first Monthly Report to Newport

### Phase 4: Scale (Month 5+)
25. ☐ Expand state portal registrations nationally based on opportunity flow
26. ☐ Pursue FEMA Advance Contract (next solicitation cycle)
27. ☐ Begin DLA Troop Support subcontracting outreach
28. ☐ Calibrate bid/no-bid scoring based on actual win/loss data
29. ☐ Evaluate Year 2 platform upgrades (GovWin IQ if pipeline justifies $12K+)
30. ☐ Target school district RFP cycle (spring/summer) for next academic year

---

## APPENDIX: NAICS CODES

| Code | Description | Newport Relevance |
|------|-------------|-------------------|
| **424410** | General Line Grocery Merchant Wholesalers | Primary — core business |
| **424450** | Confectionery Merchant Wholesalers | Secondary — if Newport distributes candy/snacks |
| **424490** | Other Grocery and Related Products Merchant Wholesalers | Secondary — catch-all for specialty items |
| 424420 | Packaged Frozen Food Merchant Wholesalers | Monitor if Newport handles frozen |
| 424430 | Dairy Product Merchant Wholesalers | Monitor if Newport handles dairy |
| 424440 | Poultry and Poultry Product Merchant Wholesalers | Monitor if relevant |
| 424470 | Meat and Meat Product Merchant Wholesalers | Monitor if relevant |
| 424480 | Fresh Fruit and Vegetable Merchant Wholesalers | Monitor if Newport handles produce |
| 722310 | Food Service Contractors | Monitor — this is the NAICS for companies like Aramark/Sodexo who Newport could subcontract to |

---

## APPENDIX: KEY URLS

| Resource | URL |
|----------|-----|
| SAM.gov (registration + search) | https://sam.gov |
| SAM.gov Opportunities API docs | https://open.gsa.gov/api/get-opportunities-public-api/ |
| SAM.gov API key signup | https://api.data.gov/signup/ |
| USASpending.gov | https://www.usaspending.gov/ |
| USASpending API docs | https://api.usaspending.gov/ |
| FEMA Doing Business | https://www.fema.gov/business-industry/doing-business |
| FEMA Advance Contracts | https://www.fema.gov/businesses-organizations/doing-business/advanced-contracts |
| Florida MFMP | https://vendor.myfloridamarketplace.com/ |
| CLEATUS | https://www.cleat.ai/ |
| HigherGov | https://www.highergov.com/ |
| GovSpend | https://govspend.com/ |
| DLA Troop Support Subsistence | https://www.dla.mil/Troop-Support/Subsistence/ |
| Florida PTAC | https://flaptac.org/ |
| makegov/awesome-procurement-data (GitHub) | https://github.com/makegov/awesome-procurement-data |