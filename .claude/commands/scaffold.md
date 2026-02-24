Set up this project from the current repo state.

1. Read /specs/06-REPO-STRUCTURE.md for the complete file tree
2. Read /specs/03-ARCHITECTURE.md for tech stack and dependencies
3. Install Python dependencies: `pip install -r requirements.txt`
4. Install Node dependencies: `cd govcon/deliverables/presentation && npm install`
5. Verify .env.example exists with all variables listed in /specs/09-INTEGRATIONS.md
6. Create any missing directories from the repo structure (data/raw, data/enriched, data/final, data/cache, data/contacts, specs/, .claude/commands/)
7. Copy spec files from /specs/ into the repo's /specs/ directory
8. Copy CLAUDE.md from /specs/CLAUDE.md to repo root
9. Verify: `python govcon/scrapers/daily_monitor.py --dry-run` completes without errors
10. Verify: `python govcon/deliverables/collect_market_data.py --dry-run` completes without errors

Reference specs: 03-ARCHITECTURE.md, 06-REPO-STRUCTURE.md, 09-INTEGRATIONS.md
