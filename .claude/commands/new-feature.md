I want to add a new feature: $ARGUMENTS

Before writing any code:
1. Check /specs/02-REQUIREMENTS.md to see if this feature is already spec'd (look for the FR-### ID)
2. Check /specs/03-ARCHITECTURE.md for relevant data flows and patterns
3. Check /specs/04-USER-STORIES.md for the expected workflow
4. Check /specs/GLOSSARY.md for any domain-specific terms you need to understand
5. Propose your implementation approach and wait for approval

When implementing:
- Follow the coding conventions in /CLAUDE.md (path resolution, config loading, data output patterns)
- Follow the existing API client pattern if adding a new integration
- Use `--dry-run` mode for any new scripts that make API calls
- Add timestamped output filenames for any new CSV outputs
- Never hardcode Newport's business data — use config or input variables
- Mark confidence levels on any new market data: HIGH/MEDIUM/LOW

After implementing:
- Update /CLAUDE.md's "Current Phase" section if this completes a milestone
- Note any new environment variables in .env.example

Reference specs: 02-REQUIREMENTS.md, 03-ARCHITECTURE.md, 04-USER-STORIES.md
