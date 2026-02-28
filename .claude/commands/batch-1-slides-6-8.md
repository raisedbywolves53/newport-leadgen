# Build Slides 6–8 — Split Layout

Read `web/DESIGN-SYSTEM.md` completely before starting. Follow it exactly.

## THE LAYOUT — SPLIT

Visual asset LEFT (col-span-3) + stat tiles RIGHT (col-span-2), stacked vertically.

```
┌────────────────────┬───────────┐
│                    │ StatCard  │
│   ChartCard        ├───────────┤
│   (visual asset)   │ StatCard  │
│                    ├───────────┤
│                    │ StatCard  │
└────────────────────┴───────────┘
```

Grid: `grid-cols-5 gap-4` → visual `col-span-3 h-full`, tiles `col-span-2 flex flex-col gap-4`

## RECHARTS (not ECharts)

Use **Recharts** for all charts. See `web/DESIGN-SYSTEM.md` section 11.
```jsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, PieChart, Pie } from 'recharts'
```

## Templates

See DESIGN-SYSTEM.md sections 6.2 (Split Layout), 6.3 (Compact StatCard), 10 (Visual Polish), 11 (Recharts).

Key points:
- LEFT card: gold accent strip + `pl-8`, `h-full flex flex-col`, hover:shadow-md
- RIGHT tiles: compact variant (`py-4 px-4 gap-3 text-xs text-xl text-[11px]`), `whileHover={{ y: -2 }}`
- Custom tooltip: dark bg `#18181b`, Inter font, rounded-lg, shadow-lg

---

## Slide 6: ConfectionerySlide.jsx — SPLIT

**Data:** `import { PRODUCT_TIERS } from '../../data/market'` → use `PRODUCT_TIERS.tier1[0]`

**Header:** Eyebrow "Product Deep-Dive" → Headline "The Confectionery Gap" → Subtitle "PSC 8925 — Newport's highest-fit category with minimal competition."

**LEFT (col-span-3):** ChartCard with Recharts donut chart. Gold = sole-source (58%), zinc = competitive. Center label "58%" in gold. CardHeader "Competition Density" / "PSC 8925 — Confectionery & Nuts". CardFooter legend.

**RIGHT (col-span-2):** 3 stacked compact tiles:
1. label "National Spend", value "$55M" (gold), badge "Tier 1", footer "Confectionery & nuts PSC 8925" / "Highest fit product category"
2. label "FL Awards", value "45" (teal), badge "FY2024", footer "FPDS tracked contracts >$10K" / "Steady annual volume"
3. label "Avg. Offers", value "1.6" (teal), badge "Low competition", footer "Most awards go sole-source" / "Limited vendor pool"

**Bottom row (optional):** InsightCard about Segment E pricing advantage.

**Source:** "FPDS FY2024, PSC 8925 | USASpending FL Awards"

---

## Slide 7: CompetitionSlide.jsx — SPLIT

**Data:** `import { COMPETITORS } from '../../data/market'`

**Header:** Eyebrow "Competitive Landscape" → Headline "Who's Already Winning" → Subtitle "8 active FL food procurement competitors — and where Newport fits."

**LEFT (col-span-3):** ChartCard with Recharts horizontal bar chart. 8 competitors sorted descending. Newport row in teal, others in gold. barSize 20. CardHeader "FL Food Procurement by Vendor" / "FPDS FY2024 Award Volume".

**RIGHT (col-span-2):** 4 stacked compact tiles:
1. label "Top Competitor", value "$26.1M" (gold), badge "Dominant", footer "Premier Wholesale" / "Largest FL food distributor"
2. label "Active Competitors", value "8" (teal), badge "Moderate", footer "FL food procurement vendors" / "Mixed capability levels"
3. label "Newport Target", value "#6" (teal), badge "Entry point", footer "Revenue-based ranking" / "Room for growth"
4. label "Gap to #5", value "$5M+" (gold), badge "↑ Opportunity", footer "Between #5 and #10 tiers" / "Newport fills this range"

**Source:** "FPDS FY2024 | SAM.gov Registrations"

---

## Slide 8: PipelineSlide.jsx — SPLIT

**Data:** `import { PIPELINE_STAGES, SOURCING_CHANNELS } from '../../data/strategy'`

**Header:** Eyebrow "Go-to-Market" → Headline "How It Works" → Subtitle "From registration to recurring revenue — the government procurement pipeline."

**LEFT (col-span-3):** ChartCard with process flow. 5 stages as horizontal flex row. Each = rounded-lg bg-zinc-100 icon + label. Connected by ChevronRight. Icons: Search, FileText, Send, CheckCircle, Truck. CardHeader "Procurement Pipeline" / "5 stages from identification to delivery". CardFooter "Typical cycle: 30–180 days depending on contract size".

**RIGHT (col-span-2):** 4 stacked compact tiles (sourcing channels):
1. label "SAM.gov", value "Free" (gold), badge "Primary", footer "Federal opportunity database" / "Required registration"
2. label "MFMP / MyFL", value "Free" (gold), badge "State", footer "FL state procurement portal" / "Largest FL channel"
3. label "BidNet / DemandStar", value "$5–13K/yr" (teal), badge "Paid", footer "Aggregated local bids" / "90%+ visibility"
4. label "Direct Outreach", value "Free" (teal), badge "Proactive", footer "Cold outreach to buyers" / "Relationship-driven"

**Source:** "FAR Subpart 4.11 | SAM.gov | MFMP.com"

---

## AFTER BUILDING ALL 3:

1. Register new slides in `web/src/data/slides.js` if they don't exist
2. Run `cd web && npm run build` — zero errors

## Checklist per slide:
- [ ] Uses `grid-cols-5 gap-4` split layout
- [ ] Visual card `col-span-3` LEFT with `h-full` + gold accent strip + `pl-8`
- [ ] Tiles `col-span-2 flex flex-col gap-4` RIGHT, compact variant
- [ ] Charts use Recharts with `<ResponsiveContainer>`
- [ ] Custom tooltip (dark bg, rounded-lg, shadow-lg)
- [ ] All cards have hover states
- [ ] Source citation present
- [ ] Build passes
