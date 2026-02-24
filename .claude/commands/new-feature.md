I want to add a new feature: $ARGUMENTS

Before writing any code:
1. Check /specs/02-REQUIREMENTS.md to see if this feature is already spec'd
2. Check /specs/03-ARCHITECTURE.md for relevant data models and patterns
3. Check /specs/04-USER-STORIES.md for the expected user flow
4. Check /specs/GLOSSARY.md for any project-specific terminology
5. Propose your implementation approach and wait for approval

When implementing:
- Follow the coding conventions in /CLAUDE.md
- Follow the API client pattern in /govcon/enrichment/ for any new integrations
- Include --dry-run mode for any new scripts
- Timestamp output files: {prefix}_{report}_{YYYYMMDD_HHMM}.csv
- Mark confidence levels on market estimates: HIGH/MEDIUM/LOW
- Update CLAUDE.md's "Current Phase" if this completes a phase milestone

Reference specs: 02-REQUIREMENTS.md, 03-ARCHITECTURE.md, 04-USER-STORIES.md
