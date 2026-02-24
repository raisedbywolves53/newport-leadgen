Something is broken: $ARGUMENTS

Diagnostic steps:
1. Read the error message carefully and identify the file and line
2. Check /specs/03-ARCHITECTURE.md to understand how the affected components connect
3. Check /CLAUDE.md's "Known gotchas" section — common issues are documented there
4. Check if this is an API issue:
   - SAM.gov has intermittent outages (experienced Feb 2026) — check if API is responding
   - Apollo.io may have rate limits or credit exhaustion
   - Google Sheets requires service account auth — verify credentials path
5. Check the data flow: collect_market_data.py → market_data.json → build_proforma.py / build_presentation.js
   If a deliverable is wrong, the issue may be upstream in the data collection
6. Propose a fix and explain what caused the issue before making changes

Do not make changes until you've explained the root cause.

Reference specs: 03-ARCHITECTURE.md, 09-INTEGRATIONS.md
