Run the contract scanner to generate market intelligence reports.

Steps:
1. Verify .env has SAM_API_KEY set
2. Run: `python govcon/scrapers/contract_scanner.py`
3. This generates up to 10 CSV reports in data/final/ covering:
   - Active opportunities by NAICS code
   - Competition density analysis
   - Set-aside opportunities
   - FL-specific opportunities
   - Agency breakdown

After running:
- Check data/final/ for timestamped output files
- Run `python govcon/deliverables/collect_market_data.py` to update market_data.json
- If market_data.json changed significantly, flag for deck/model update

Known issues:
- SAM.gov API has intermittent outages — check error logs
- FPDS ezSearch decommissioned Feb 24, 2026 — ATOM feed still works but will sunset later FY2026
- Rate limits: 1,000 requests/day on SAM.gov API

Reference specs: 03-ARCHITECTURE.md, 09-INTEGRATIONS.md
