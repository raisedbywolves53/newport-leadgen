# Phase 2: Operational System — Scoring, Pipeline, Automation

## Objective
Build the 3 missing components that turn raw API data into an operational system Newport can work out of daily. After this phase, the command center is functional.

## Prerequisites
- Phase 1 complete (repo organized, files migrated)
- Google Sheets API credentials configured
- Resend API key configured

---

## Build 1: Bid/No-Bid Scoring Framework

### File: `scoring/bid_no_bid.py`

### Purpose
Systematically evaluate every government opportunity on 9 weighted factors. Returns a numeric score (0-100) and a recommendation (Strong Bid / Bid / Review / No-Bid). This is how Newport decides what to pursue vs. skip.

### Scoring Matrix (9 Factors)

| Factor | Weight | Description | Scoring Criteria |
|--------|--------|-------------|-----------------|
| NAICS Alignment | 15% | Does the opportunity match Newport's NAICS codes? | 100: Primary NAICS exact match (424410, 424450, 424490). 75: Adjacent NAICS (722310 food service, 311 food manufacturing). 25: Tangentially related. 0: No match. |
| Geography | 15% | Is it in Newport's delivery radius? | 100: South Florida (Miami-Dade, Broward, Palm Beach). 80: Florida statewide. 60: Southeast US (GA, SC, NC, AL, TN, MS, LA). 40: Mid-Atlantic (VA, DC, MD). 20: National/other. 0: International. |
| Contract Size | 10% | Does the value fit Newport's sweet spot? | 100: $25K-$75K (ideal first-year target). 80: $75K-$150K. 60: $150K-$350K. 40: $10K-$25K (small but worth it for past performance). 20: >$350K (stretch). 0: <$10K (not worth effort). |
| Competition Level | 10% | How many bidders are expected? | 100: Sole-source or single bid expected. 80: 2-3 expected bidders. 60: 4-6 expected bidders. 40: 7-10 expected bidders. 20: >10 expected bidders. 0: Incumbent-locked/wired. |
| Past Performance Requirement | 15% | Does Newport meet the experience requirements? | 100: No past performance required or self-certification only. 75: 1-2 references required, commercial experience accepted. 50: 2-3 government references required (Newport has some by mid-Year 1). 25: 3+ government references required. 0: Specific government contract past performance mandatory. |
| Evaluation Criteria Fit | 10% | How does the agency evaluate bids? | 100: Lowest Price Technically Acceptable (LPTA) — price wins. 80: Best value with price as primary factor. 50: Best value with technical/management weighted equally to price. 25: Technical/management dominant. 0: Subjective oral presentations required. |
| Relationship Status | 10% | Does Newport have any connection to the buying agency? | 100: Active relationship with contracting officer or end user. 75: Previous communication or introduction. 50: Know someone who can make an introduction. 25: No relationship but agency is accessible. 0: Agency is opaque/difficult to reach. |
| Timeline Feasibility | 10% | Can Newport respond in time? | 100: 30+ days until deadline. 80: 15-30 days. 60: 7-14 days. 30: 3-7 days. 0: <3 days or already passed. |
| Strategic Value | 5% | Does winning open doors beyond this contract? | 100: FEMA advance contract, cooperative purchasing vehicle, or large agency relationship. 75: Recompete opportunity or multi-year contract. 50: Builds past performance in target buyer category. 25: One-off contract, limited strategic value. 0: No strategic benefit. |

### Score Thresholds

| Score Range | Recommendation | Action |
|-------------|---------------|--------|
| 80-100 | **Strong Bid** | Bid aggressively. Dedicate full effort. |
| 65-79 | **Bid** | Bid with standard effort. Worth pursuing. |
| 50-64 | **Review** | Discuss with Newport. May bid if capacity allows. |
| 0-49 | **No-Bid** | Skip. Log reason. Move on. |

### Implementation Requirements

```python
class BidNoBidScorer:
    """
    Score government opportunities for Newport Wholesalers.
    
    Usage:
        scorer = BidNoBidScorer()
        result = scorer.score(opportunity_data)
        # result = {
        #     "total_score": 78,
        #     "recommendation": "Bid",
        #     "factor_scores": { ... },
        #     "reasoning": "Strong NAICS match and geographic fit. No past performance required..."
        # }
    """
```

The scorer must:
1. Accept a dictionary of opportunity data (from any source — SAM.gov, manual entry, CLEATUS export)
2. Return total score, recommendation, per-factor scores, and human-readable reasoning
3. Handle missing data gracefully (use conservative defaults — assume worst case for unknown factors)
4. Be callable from the daily monitor (Phase 2 Build 3) to auto-score new opportunities
5. Log all scoring decisions for monthly reporting

### Newport-Specific NAICS Codes
Primary: 424410 (General Line Grocery Merchant Wholesalers), 424450 (Confectionery Merchant Wholesalers), 424490 (Other Grocery and Related Products Merchant Wholesalers)
Adjacent: 722310 (Food Service Contractors), 311 (Food Manufacturing), 424420 (Packaged Frozen Food), 424430 (Dairy Product), 424440 (Poultry and Poultry Product), 424460 (Fish and Seafood), 424470 (Meat and Meat Product), 424480 (Fresh Fruit and Vegetable)

### Newport Target Geography (priority order)
1. South Florida: Miami-Dade, Broward, Palm Beach counties
2. Florida statewide
3. Southeast: GA, SC, NC, AL, TN, MS, LA
4. Mid-Atlantic: VA, DC, MD
5. Extended: TX, AR, KY

---

## Build 2: Pipeline Lifecycle Tracker

### File: `pipeline/sheets_pipeline.py`

### Purpose
Replace the generic lead tracking in `tracking/sheets_crm.py` with government contracting lifecycle stages, buyer category tagging, and deadline management. This is the operational hub — where Newport sees every opportunity and its status.

### Google Sheet Structure

#### Sheet 1: "Pipeline" (Main Tracking)

| Column | Field | Type | Notes |
|--------|-------|------|-------|
| A | Opportunity ID | Text | Auto-generated or from SAM.gov notice ID |
| B | Title | Text | Opportunity title |
| C | Agency | Text | Buying agency name |
| D | Buyer Category | Dropdown | School District, Corrections, Military/DoD, FEMA/Emergency, VA/Healthcare, University/College, State Agency, County/Municipal, Federal Civilian, Food Bank/Nonprofit |
| E | Tier | Dropdown | Federal, State, Local, Education |
| F | NAICS Code | Text | Primary NAICS from solicitation |
| G | Contract Value | Currency | Estimated or stated value |
| H | State | Text | State abbreviation |
| I | Stage | Dropdown | See lifecycle stages below |
| J | Bid/No-Bid Score | Number | From scoring framework (0-100) |
| K | Recommendation | Text | Strong Bid / Bid / Review / No-Bid |
| L | Source | Text | SAM.gov, MFMP, BidSync, HigherGov, GovSpend, Manual |
| M | Response Deadline | Date | Proposal submission deadline |
| N | Days Until Deadline | Formula | =M[row]-TODAY() |
| O | Award Date | Date | When contract was awarded (blank until decided) |
| P | Outcome | Dropdown | Pending, Won, Lost, No-Bid, Cancelled |
| Q | Contract Number | Text | Assigned after award |
| R | Contracting Officer | Text | Name of CO |
| S | CO Email | Text | CO email for follow-up |
| T | Notes | Text | Free-form notes, debrief feedback |
| U | Date Added | Date | When opportunity entered pipeline |
| V | Last Updated | Date | Auto-updated on any change |
| W | Solicitation URL | URL | Link to full solicitation document |

#### Lifecycle Stages (Column I)

```
Identified → Qualifying → Bid Decision → Capture → Drafting Proposal → 
Internal Review → Submitted → Under Evaluation → Awarded → Lost → No-Bid → Cancelled
```

Stage definitions:
- **Identified**: Opportunity found via API monitor, manual search, or alert. Not yet evaluated.
- **Qualifying**: Reviewing solicitation. Gathering info to score.
- **Bid Decision**: Scored. Awaiting go/no-go decision from Newport.
- **Capture**: Decided to bid. Building relationships, gathering intel on agency needs.
- **Drafting Proposal**: Actively writing technical response, pricing, compliance matrix.
- **Internal Review**: Proposal complete, under internal review before submission.
- **Submitted**: Proposal submitted. Awaiting evaluation.
- **Under Evaluation**: Agency confirmed receipt, evaluation in progress.
- **Awarded**: Newport won the contract.
- **Lost**: Another vendor won. Request debrief.
- **No-Bid**: Decided not to bid. Reason logged in Notes.
- **Cancelled**: Agency cancelled the solicitation.

#### Sheet 2: "Agencies" (Relationship Tracker)

| Column | Field | Notes |
|--------|-------|-------|
| A | Agency Name | |
| B | Buyer Category | |
| C | Tier | |
| D | State | |
| E | Primary Contact | |
| F | Contact Email | |
| G | Contact Phone | |
| H | Relationship Status | Cold, Warm, Active, Past Winner |
| I | Last Contact Date | |
| J | Total Opportunities | Count from Pipeline sheet |
| K | Total Bids | Count from Pipeline sheet |
| L | Total Wins | Count from Pipeline sheet |
| M | Notes | |

#### Sheet 3: "Dashboard" (Summary Views)

Auto-calculated from Pipeline data:
- Opportunities by Stage (count)
- Opportunities by Buyer Category (count + total value)
- Win Rate (Awarded / (Awarded + Lost))
- Active Pipeline Value (sum of Contract Value where Stage is Capture through Under Evaluation)
- Upcoming Deadlines (next 14 days)
- Monthly Activity (opportunities added, bids submitted, wins/losses)

### Implementation Requirements

```python
class GovConPipeline:
    """
    Government contracting pipeline tracker using Google Sheets.
    
    Methods:
        setup_sheets() — Create Pipeline, Agencies, Dashboard sheets with headers and formatting
        add_opportunity(data) — Add new opportunity to Pipeline
        update_stage(opp_id, new_stage) — Move opportunity to new stage
        score_opportunity(opp_id) — Run bid/no-bid scorer and update columns J-K
        get_active_pipeline() — Return all opportunities not in terminal states
        get_upcoming_deadlines(days=14) — Return opportunities with deadlines within N days
        get_dashboard_data() — Return summary metrics for Dashboard sheet
        sync_agencies() — Update Agencies sheet from Pipeline data
    """
```

Must:
1. Create the Google Sheet structure on first run (idempotent — don't recreate if exists)
2. Apply data validation (dropdowns) for Buyer Category, Tier, Stage, Outcome columns
3. Apply conditional formatting: Red for deadlines <7 days, Yellow for <14 days, Green for >14 days
4. Auto-populate Date Added and Last Updated
5. Integrate with bid/no-bid scorer from Build 1

---

## Build 3: Daily Automation & Notifications

### Files:
- `automation/daily_monitor.py` — Main script
- `.github/workflows/daily-monitor.yml` — GitHub Actions cron

### Purpose
Run the SAM.gov monitor every day at 6:00 AM ET. When new opportunities matching Newport's NAICS codes appear, auto-score them, add to pipeline, and send email notification.

### daily_monitor.py Logic

```
1. Call sam_client.py with Newport NAICS filters
2. Compare results against existing Pipeline sheet (by notice ID) to find NEW opportunities
3. For each new opportunity:
   a. Run bid/no-bid scorer with available data
   b. Add to Pipeline sheet with Stage = "Identified"
   c. Collect for notification digest
4. Check Pipeline for deadlines in next 7 days → add to digest
5. Send email digest via Resend API
```

### Email Digest Format

```
Subject: Newport GovCon Daily Brief — [DATE]

NEW OPPORTUNITIES ([count])
━━━━━━━━━━━━━━━━━━━━━━━━━
[For each new opportunity:]
📋 [Title]
   Agency: [Agency Name] | Value: [Contract Value] | NAICS: [Code]
   Deadline: [Response Deadline]
   Score: [XX]/100 — [Recommendation]
   Link: [Solicitation URL]

UPCOMING DEADLINES (Next 7 Days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[For each:]
⏰ [Title] — Due [Date] ([X days])
   Stage: [Current Stage]

PIPELINE SNAPSHOT
━━━━━━━━━━━━━━━━
Active Opportunities: [count]
Proposals in Progress: [count]  
Submitted & Awaiting: [count]
Pipeline Value: $[total]
```

### GitHub Actions Workflow: `.github/workflows/daily-monitor.yml`

```yaml
name: Daily GovCon Monitor
on:
  schedule:
    - cron: '0 11 * * *'  # 6:00 AM ET (11:00 UTC)
  workflow_dispatch:         # Manual trigger for testing

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python automation/daily_monitor.py
        env:
          SAM_GOV_API_KEY: ${{ secrets.SAM_GOV_API_KEY }}
          GOOGLE_SHEETS_CREDENTIALS_PATH: ${{ secrets.GOOGLE_SHEETS_CREDENTIALS_PATH }}
          RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
          NOTIFICATION_EMAIL: ${{ secrets.NOTIFICATION_EMAIL }}
```

Note on Google Sheets credentials for GitHub Actions: The credentials JSON needs to be stored as a GitHub secret and written to a file at runtime. Add a step:
```yaml
      - name: Setup Google credentials
        run: echo '${{ secrets.GOOGLE_CREDENTIALS_JSON }}' > config/google_credentials.json
```

### SAM.gov NAICS Filters

Use these NAICS codes in the daily query:
```python
NEWPORT_NAICS = [
    "424410",  # General Line Grocery Merchant Wholesalers
    "424450",  # Confectionery Merchant Wholesalers  
    "424490",  # Other Grocery and Related Products
    "722310",  # Food Service Contractors
    "424420",  # Packaged Frozen Food
    "424430",  # Dairy Product
    "424440",  # Poultry and Poultry Product
    "424460",  # Fish and Seafood
    "424470",  # Meat and Meat Product
    "424480",  # Fresh Fruit and Vegetable
]
```

---

## Completion Criteria
- [ ] `scoring/bid_no_bid.py` — Scores opportunities on 9 factors, returns score + recommendation
- [ ] `pipeline/sheets_pipeline.py` — Creates and manages 3-sheet Google Sheet with lifecycle stages
- [ ] `automation/daily_monitor.py` — Pulls SAM.gov, scores, adds to pipeline, sends digest
- [ ] `.github/workflows/daily-monitor.yml` — Cron job configured for 6 AM ET daily
- [ ] All 3 components integrate (monitor calls scorer, scorer feeds pipeline)
- [ ] Manual test: run `python automation/daily_monitor.py` and verify email arrives with data

## Next Phase
Read `docs/PHASE-3-PRESENTATION.md`
