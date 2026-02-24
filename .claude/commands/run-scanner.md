Run the contract scanner for market research: $ARGUMENTS

Steps:
1. Read /specs/03-ARCHITECTURE.md for the data flow: API clients → contract_scanner.py → 10 CSV reports → data/final/
2. Ensure SAM_API_KEY is set in .env
3. Run with dry-run first: `python govcon/scrapers/contract_scanner.py --dry-run`
4. If dry-run succeeds, run live: `python govcon/scrapers/contract_scanner.py`
5. Check outputs in data/final/ — should see timestamped CSVs for each report type
6. If you need to refresh market_data.json after scanning: `python govcon/deliverables/collect_market_data.py`

Reports generated (10 total):
- Opportunities by NAICS code
- Opportunities by state
- Opportunities by set-aside type
- Opportunities by agency
- Competition density analysis
- Award history by vendor
- Contract value distribution
- Solicitation timeline
- Active vs. closed opportunities
- SLED opportunity scan (if HigherGov configured)

Common issues:
- SAM.gov API outage: check https://api.data.gov/status. System degrades gracefully.
- Rate limit (1,000/day): use --max-pages to limit requests
- Stale data: FPDS and USASpending update daily-ish. SAM.gov is near real-time.

Reference specs: 03-ARCHITECTURE.md, 09-INTEGRATIONS.md
