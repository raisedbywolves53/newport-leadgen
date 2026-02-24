Something is broken: $ARGUMENTS

Diagnostic steps:
1. Read the error message carefully and identify the file and line
2. Check /specs/03-ARCHITECTURE.md to understand how the affected components connect
3. Check if this is a known gotcha listed in /CLAUDE.md's Guardrails section
4. Check /specs/09-INTEGRATIONS.md if the error involves an external API
5. Propose a fix and explain what caused the issue before making changes

Do not make changes until you've explained the root cause.

Common issues:
- SAM.gov API outages (Feb 2026) — check if system degraded gracefully
- Path resolution: all scripts should use `Path(__file__).resolve().parent.parent.parent` for repo root
- Google Sheets requires service account JSON at GOOGLE_SHEETS_CREDS_PATH
- Apollo free tier has limited reveal credits — check budget

Reference specs: 03-ARCHITECTURE.md, 09-INTEGRATIONS.md, CLAUDE.md
