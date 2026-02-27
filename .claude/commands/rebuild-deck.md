Modify or rebuild slides in the GovCon web presentation.

The web app lives at `/web/` — React 19 + Vite 7 + Tailwind CSS 4 + ECharts 6 + Motion 12.

Before making changes:
1. Read `/web/DESIGN-SYSTEM.md` — this is the design bible. Follow it exactly.
2. Read `/web/src/data/slides.js` — the slide registry (20 slides, 4 acts)
3. Read the specific slide component in `/web/src/components/slides/`
4. Read data files: `/web/src/data/market.js`, `strategy.js`, `financials.js`

Key rules from the design system:
- Card DNA: `rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)]`
- Two-accent discipline: gold `#C9A84C` + teal `#1B7A8A` only
- Slide container: `w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden`
- Typography: Playfair Display (title only), Inter (everything else)
- Animation sequence < 2 seconds total, use `motion/react`

Reusable components (import from `/web/src/components/ui/`):
- `GoldLine` — animated gold divider after subtitles
- `CompassStar` — 4-pointed decorative star
- `HeroStat` — oversized metric display
- `SourceCitation` — bottom-of-slide citation
- `SlideLayout` — base layout wrapper
- `SectionDivider` — divider slides between acts

Data imports — never hardcode numbers:
- Market data: `import { HEADLINE_STATS, FL_TAM_CHANNELS, ... } from '../../data/market'`
- Strategy data: `import { KEY_QUESTIONS, COMPLIANCE_REQUIRED, ... } from '../../data/strategy'`
- Financial data: `import { FIVE_YEAR_PROJECTIONS, SCENARIO_COMPARISON, ... } from '../../data/financials'`

Development workflow:
- `cd web && npm run dev` — hot reload at localhost:5173
- `cd web && npm run build` — production build (zero errors required)

Reference specs: 02-REQUIREMENTS.md (FR-007), web/DESIGN-SYSTEM.md
