Modify or rebuild slides in the GovCon web presentation.

The web app lives at `/web/` — React 19 + Vite 7 + Tailwind CSS 4 + ECharts 6 + Motion 12.

## Before making ANY changes:

1. Read `/web/DESIGN-SYSTEM.md` COMPLETELY — this is the design bible. It defines the ONE layout pattern (dashboard-01) that every slide must follow.
2. Read `/web/src/data/slides.js` — the slide registry (20 slides, 4 acts)
3. Read the specific slide component(s) in `/web/src/components/slides/`
4. Read data files: `/web/src/data/market.js`, `strategy.js`, `financials.js`

## THE ONE LAYOUT (shadcn dashboard-01)

Every data slide follows this EXACT vertical flow:

```
┌──────────┬──────────┬──────────┬──────────┐
│ StatCard │ StatCard │ StatCard │ StatCard │  ← HORIZONTAL ROW (grid-cols-3 or grid-cols-4)
└──────────┴──────────┴──────────┴──────────┘
┌────────────────────────────────────────────┐
│   ChartCard / TableCard (FULL WIDTH)       │  ← BELOW the stat row
└────────────────────────────────────────────┘
┌────────────────────────────────────────────┐
│   Optional bottom row                      │  ← Table, insight, or more stats
└────────────────────────────────────────────┘
```

**NEVER DO:**
- `grid-cols-[3fr_2fr]` (random chart beside stats)
- `grid-cols-7` with `col-span-4/col-span-3`
- Vertical stat stacking
- Bento grids / row-span
- Side-by-side comparison cards as the main layout

**EXCEPTION — Hero Visual Layout (DESIGN-SYSTEM.md section 6.3):**
When a visualization needs square/tall space (concentric rings, treemaps), use `grid-cols-5` with visual `col-span-3` LEFT + stat cards `col-span-2` RIGHT. Currently approved for: Slide 4 only.

## StatCard (shadcn section-cards.tsx pattern — MUST have all 5 zones + hover)

```jsx
<motion.div
  key={stat.label}
  initial={{ opacity: 0, y: 12 }}
  animate={{ opacity: 1, y: 0 }}
  whileHover={{ y: -2 }}
  transition={{ duration: 0.4, delay: 0.3 + i * 0.08 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out flex flex-col gap-6 py-6 cursor-default"
>
  <div className="px-6 flex flex-col gap-2">
    <div className="flex items-center justify-between">
      <span className="text-sm text-zinc-500">{label}</span>
      <span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-zinc-700">
        {trendIcon} {trendText}
      </span>
    </div>
    <span className="text-2xl font-semibold tabular-nums tracking-tight" style={{ color: accentColor }}>
      {value}
    </span>
  </div>
  <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
    <div className="flex items-center gap-2 font-medium text-zinc-900">{footerHighlight}</div>
    <div className="text-zinc-500 text-xs">{footerDescription}</div>
  </div>
</motion.div>
```

**Key difference from old MetricCard:** StatCard has 5 content zones (label, value, trend badge, footer highlight, footer description) + hover polish (shadow-md, border-zinc-300, y: -2 lift). Old MetricCard only had 3 (label, value, detail). The density + interactivity is what makes it look like shadcn.

## ChartCard (wraps EVERY visualization)

```jsx
<div className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col">
  <div className="p-6 pb-0">
    <h3 className="text-lg font-semibold text-zinc-950">{title}</h3>
    <p className="text-sm text-zinc-500 mt-1">{description}</p>
  </div>
  <div className="p-6 pt-4 flex-1 min-h-0">
    <div ref={chartRef} className="w-full h-full" />
  </div>
  <div className="px-6 py-3 border-t border-zinc-100 flex items-center gap-4">
    {/* legend dots */}
  </div>
</div>
```

## Recharts (New Slides 6–17)

New slides use **Recharts** instead of ECharts. Cleaner defaults, declarative JSX, no useRef/useEffect boilerplate.
```jsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
```
See `web/DESIGN-SYSTEM.md` section 11 for full templates.

## Polish (All Slides)

Every card gets hover states. See `web/DESIGN-SYSTEM.md` section 10.
- StatCards: `whileHover={{ y: -2 }}` + `hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out`
- ChartCards: same hover pattern
- Hero ChartCard: gold accent strip + `pl-8`
- Custom tooltip: dark bg, Inter font, rounded-lg, shadow-lg

## Key Rules:

- Card surface: `rounded-xl bg-white border border-zinc-200 shadow-sm`
- Card hover: `hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out`
- Two-accent only: gold `#C9A84C` + teal `#1B7A8A`
- Slide container: `w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden`
- Typography: Inter everywhere (Playfair Display = slide 1 title only)
- Animation budget < 1.5 seconds total
- Text hierarchy: zinc-950 headlines, zinc-500 muted labels, zinc-600 body, zinc-400 captions, zinc-300 sources
- Data from imports — never hardcode numbers

## Reusable components (`/web/src/components/ui/`):

- `GoldLine` — animated gold divider after subtitles
- `CompassStar` — 4-pointed decorative star (use sparingly)
- `BackgroundRing` — circular decoration (max 1 per slide, opacity 0.03)

## Data imports:

- `import { HEADLINE_STATS, FL_TAM_CHANNELS, PRODUCT_TIERS, TARGET_AGENCIES, COMPETITORS, B2B_TARGETS } from '../../data/market'`
- `import { KEY_QUESTIONS, COMPLIANCE_REQUIRED, COMPLIANCE_NOT_NEEDED, PIPELINE_STAGES, SOURCING_CHANNELS, CONTRACT_EXAMPLES, ROUTE_COMPARISON, RESPONSIBILITIES, INFLUENCE_LAYERS, BD_PROCESS_STEPS } from '../../data/strategy'`
- `import { FIVE_YEAR_PROJECTIONS, PORTFOLIO_EVOLUTION } from '../../data/financials'`

## Workflow:

- `cd web && npm run dev` — hot reload
- `cd web && npm run build` — production build (zero errors required)

## Batch prompts (run in order):

0. `.claude/commands/setup-recharts.md` — Install recharts dependency
1. `.claude/commands/batch-0-slides-3-5.md` — Restructure existing slides 3–5 to dashboard-01
2. `.claude/commands/fix-slides-4-5-layout.md` — Fix slide 4 (hero visual layout) + slide 5 (compact cards + taller chart)
3. `.claude/commands/polish-slides-3-5.md` — Add hover states + polish to slides 3–5
4. `.claude/commands/batch-1-slides-6-8.md` — Build slides 6–8 (Recharts + polish)
5. `.claude/commands/batch-2-slides-9-11.md` — Build slides 9–11 (Recharts + polish)
6. `.claude/commands/batch-3-slides-12-14.md` — Build slides 12–14 (Recharts + polish)
7. `.claude/commands/batch-4-slides-15-17.md` — Build slides 15–17 + dividers (Recharts + polish)
