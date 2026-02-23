# Reference: Original Technical Requirements

> **IMPORTANT**: This is a placeholder. Replace this file with the actual `REQUIREMENTS-newport-govcon-command-center.md` that already exists in your project.

## Where to Find It
The authoritative requirements document is already written and should be in your VS Code project. It contains:

- **Build Spec 1**: SAM.gov Federal Opportunity Monitor (API client, filters, Google Sheets output)
- **Build Spec 2**: USASpending Competitive Intelligence Dashboard (TAM analysis, competitor tracking, expiring contracts)
- **Build Spec 3**: Notion/Sheets Master Pipeline Tracker (lifecycle stages, views, linked databases)
- **Build Spec 4**: Bid/No-Bid Scoring Framework (9-factor weighted matrix)
- **Build Spec 5**: Monthly Reporting Template (ROI demonstration, pipeline metrics)

## Status vs. This Project

| Build Spec | Status | Where |
|-----------|--------|-------|
| Spec 1 (SAM.gov Monitor) | ✅ BUILT | `enrichment/sam_client.py` |
| Spec 2 (USASpending Intel) | ✅ BUILT | `enrichment/usaspending_client.py` + `enrichment/fpds_client.py` (FPDS is better than original spec) |
| Spec 3 (Pipeline Tracker) | ❌ Phase 2 builds this | `pipeline/sheets_pipeline.py` |
| Spec 4 (Bid/No-Bid Scoring) | ❌ Phase 2 builds this | `scoring/bid_no_bid.py` |
| Spec 5 (Monthly Reporting) | ❌ Addressed in Phase 2 dashboard sheet | Part of pipeline tracker |

## CLI Instruction
Copy your existing `REQUIREMENTS-newport-govcon-command-center.md` file here. The Phase 2 builds reference it for detailed specifications. If it's not available, Phase 2 docs contain sufficient detail to build everything.
