# Build Slides 9–11 — Split Layout + Table Layout

Read `web/DESIGN-SYSTEM.md` completely before starting. Follow it exactly.

## TWO LAYOUTS

**SPLIT** (slides 9, 11) = visual LEFT (col-span-3) + tiles RIGHT (col-span-2)
**TABLE** (slide 10) = tiles horizontal TOP + full-width table BELOW

See DESIGN-SYSTEM.md sections 6.2–6.4 for templates and 11 for Recharts.

---

## Slide 9: TargetAgenciesSlide.jsx — SPLIT

**Data:** `import { TARGET_AGENCIES } from '../../data/market'`

**Header:** Eyebrow "Priority Targets" → Headline "Four Agencies, One Strategy" → Subtitle "Ranked by FL food procurement volume and Newport fit."

**LEFT (col-span-3):** ChartCard with Recharts horizontal bar chart. 4 agencies sorted descending. DOJ bar in gold, others teal. CardHeader "FL Contract Value by Agency" / "Annual addressable opportunity". CardFooter with targeting context.

**RIGHT (col-span-2):** 4 stacked compact tiles (one per agency):
1. label "DOJ / BOP", value from data (gold), badge "Primary", footer "Federal Bureau of Prisons" / "Largest FL food buyer"
2. label "USDA", value from data (teal), badge "Secondary", footer "NSLP and commodity programs" / "Education distribution"
3. label "VA Medical", value from data (teal), badge "Steady", footer "Veterans Affairs hospitals" / "Consistent annual procurement"
4. label "DoD Commissary", value from data (teal), badge "Volume", footer "Military base food service" / "Sole-source NAICS 424490"

**Source:** "USASpending FY2024 | FPDS FL Awards"

---

## Slide 10: ContractsSlide.jsx — TABLE LAYOUT

**Data:** `import { CONTRACT_EXAMPLES } from '../../data/strategy'`

**Header:** Eyebrow "Opportunities" → Headline "Real Contracts Newport Can Win" → Subtitle "Active and upcoming opportunities matched to Newport's capabilities."

**TOP ROW:** `grid-cols-3 gap-4` — **standard** (NOT compact) stat cards:
1. label "Active Opportunities", value "8" (gold), badge "Qualified", footer "Matched to Newport's capabilities" / "Product fit + contract size"
2. label "Combined Value", value "$155K+" (teal), badge "Addressable", footer "Within micro + simplified thresholds" / "First-year target range"
3. label "High Fit Rating", value "75%" (teal), badge "Strong", footer "Based on product match" / "Competition level confirmed"

**BELOW:** Full-width TableCard with gold accent strip. CardHeader "Contract Pipeline" / "Scored by product fit, size, and competition". Table from CONTRACT_EXAMPLES. Columns: Contract, Agency, Value, Fit Rating. Fit badges: HIGH = amber bg, MEDIUM = teal, LOW = zinc. Table rows `hover:bg-zinc-50`. CardFooter with context.

**Source:** "SAM.gov | FPDS | Agency procurement forecasts FY2024–2025"

---

## Slide 11: PortfolioSlide.jsx — SPLIT

**Data:** `import { PORTFOLIO_EVOLUTION } from '../../data/financials'`

**Header:** Eyebrow "Growth Model" → Headline "Year 1 to Year 5" → Subtitle "Conservative projection — 15% win rate Year 1, scaling with past performance."

**LEFT (col-span-3):** ChartCard with Recharts stacked bar chart. X-axis Y1–Y5. 4 series: Micro (gold), Simplified (teal), Larger (light teal), Renewed (amber). barSize 28. CardHeader "Contract Portfolio Growth" / "Projected 5-year build across contract tiers". CardFooter with 4-color legend.

**RIGHT (col-span-2):** 3 stacked compact tiles:
1. label "Year 5 Contracts", value "78" (gold), badge "↑ Cumulative", footer "Active contracts across all tiers" / "Starting from 3–5 in Year 1"
2. label "Renewal Rate", value "70%" (teal), badge "Industry avg", footer "Incumbent vendor retention" / "Key driver of portfolio growth"
3. label "Year 5 Revenue", value "$1.2M" (teal), badge "↑ Projected", footer "Annual contract revenue" / "Conservative baseline estimate"

**Source:** "Newport projection model | Industry benchmarks | FAR thresholds"

---

## AFTER BUILDING ALL 3:

1. Register new slides in `web/src/data/slides.js` if they don't exist
2. Run `cd web && npm run build` — zero errors

## Checklist:
- [ ] Slides 9, 11: `grid-cols-5 gap-4` split layout (visual LEFT, tiles RIGHT)
- [ ] Slide 10: standard stat row TOP + full-width table BELOW
- [ ] Charts use Recharts with `<ResponsiveContainer>`
- [ ] Table rows have `hover:bg-zinc-50`
- [ ] All cards have hover states
- [ ] Source citations present
- [ ] Build passes
