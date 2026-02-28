# Rebuild Slides 15–17 to Dashboard-01 Layout

Read `web/DESIGN-SYSTEM.md` completely before starting. Follow it exactly.

## THE RULE
Every slide uses the shadcn dashboard-01 layout:
1. Stat cards in a HORIZONTAL ROW (`grid-cols-3` or `grid-cols-4`)
2. Chart/content card FULL WIDTH below
3. Optional bottom row
4. Source citation

**NO side-by-side layouts. NO vertical stat stacking. NO bento grids. NO grid-cols-7 or grid-cols-[1fr_auto_1fr].**

## StatCard Template (MUST have all 5 zones + hover)
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

## RECHARTS & POLISH

For any chart on slides 15–17, use **Recharts** (not ECharts). See `web/DESIGN-SYSTEM.md` section 11.

Every card and chart MUST include polish (see DESIGN-SYSTEM.md section 10):
- StatCards: `whileHover={{ y: -2 }}` + `hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out cursor-default`
- ChartCards: `hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out`
- Hero ChartCard: gold accent strip + content `pl-8`
- Table rows: `hover:bg-zinc-50` transition

---

## Slide 15: QuestionsSlide.jsx

**Data:** `import { KEY_QUESTIONS } from '../../data/strategy'`

**Header:**
- Eyebrow: "Decision Framework"
- Headline: "Ten Questions Before You Start"
- Subtitle: "Key decisions that shape Newport's government entry strategy."

**Stat row (grid-cols-3 gap-4, mb-4):** 3 category summary cards
1. label "Strategic Questions", value "4" (gold `#C9A84C`), trend badge "Priority", footer "Market positioning and timing" / "Must answer before registration"
2. label "Operational Questions", value "3" (teal `#1B7A8A`), trend badge "Logistics", footer "Fulfillment and capacity" / "Warehouse and fleet readiness"
3. label "Financial Questions", value "3" (teal), trend badge "Budget", footer "Investment and ROI thresholds" / "Break-even analysis inputs"

**Chart card (full width):** Question list card.
- CardHeader: "Decision Checklist" / "Grouped by category with priority ratings"
- CardContent: 3 grouped sections. Each group = category label (text-sm font-semibold text-zinc-950 mb-2) + question rows. Each question row = priority badge (HIGH amber, MEDIUM teal, LOW zinc) + question text (text-sm text-zinc-700). Rows separated by border-b border-zinc-100 py-3.
- CardFooter: border-t + "Address HIGH-priority questions in the first partner meeting."

**Source:** "Internal strategy framework"

---

## Slide 16: B2BSlide.jsx

**Data:** `import { B2B_TARGETS } from '../../data/market'`

**Header:**
- Eyebrow: "Commercial Channel"
- Headline: "Institutional Buyers — Fast Track"
- Subtitle: "Direct B2B sales to high-volume institutional accounts in FL."

**Stat row (grid-cols-3 gap-4, mb-4):**
1. label "Priority Accounts", value "5" (gold), trend badge "Identified", footer "FL institutional food buyers" / "GEO Group leads the list"
2. label "Sales Cycle", value "2–8 wks" (gold), trend badge "↑ Fast", footer "vs. 3–12 months for government" / "No procurement bureaucracy"
3. label "Combined Est. Revenue", value "$2M+" (teal), trend badge "Addressable", footer "Annual food spend across targets" / "Direct wholesale relationship"

**Chart card (full width, height 280px):** Horizontal bar chart with gold accent strip.
- CardHeader: "Target Account Value" / "Top 5 institutional buyers in FL"
- Chart: 5 bars sorted descending. GEO Group in gold, others teal. barWidth 22.
- CardFooter: border-t + "GEO Group = largest private prison food buyer in FL"

**Bottom row:** TableCard full-width.
- CardHeader: "Target Accounts" / "Ranked by estimated annual food spend"
- Table: 5 rows. Columns: Account, Type, Est. Value, Status. GEO Group row bg-amber-50/50.
- Status badges: Active (teal), Prospect (zinc), Priority (amber)

**Source:** "Industry research | FL institutional procurement data"

---

## Slide 17: BlueprintSlide.jsx (Final Slide)

**Data:** `import { RESPONSIBILITIES } from '../../data/strategy'`

**Header:**
- Eyebrow: "Partnership"
- Headline: "The Blueprint"
- Subtitle: "A clear division of responsibilities between Newport and Still Mind Creative."

**Stat row (grid-cols-4 gap-4, mb-4):** Key partnership metrics
1. label "Newport Role", value "Operations" (teal), trend badge "Fulfillment", footer "Warehouse, fleet, delivery" / "30 years of distribution expertise"
2. label "Still Mind Role", value "Strategy" (gold), trend badge "Growth", footer "Market intelligence and positioning" / "AI-powered prospecting"
3. label "Phase 1 Timeline", value "90 Days" (gold), trend badge "Launch", footer "Registration to first micro-purchase" / "Parallel government + B2B tracks"
4. label "Year 1 Target", value "$150K+" (teal), trend badge "Conservative", footer "Combined gov + B2B revenue" / "Building past performance"

**Chart card (full width):** Responsibility split card.
- CardHeader: "Partnership Responsibilities" / "Newport Wholesalers × Still Mind Creative"
- CardContent: Two columns inside the card content area (NOT a grid-cols-2 of separate cards). Use `grid grid-cols-2 gap-8` INSIDE the single card. Left column = "Newport Wholesalers" subheader (teal) + bulleted list of their responsibilities. Right column = "Still Mind Creative" subheader (gold) + bulleted list. Center divider: `border-r border-zinc-200`.
- CardFooter: border-t + "Clear lanes, shared accountability, measurable milestones."

**Source:** "Partnership framework | Still Mind Creative LLC"

---

## SECTION DIVIDERS

Update any section divider slides between acts:
- Centered layout, no stat cards, no chart cards
- Title: `text-4xl font-semibold text-zinc-950` centered
- Subtitle: `text-base text-zinc-500` centered
- GoldLine centered (64px)
- BackgroundRing large, centered, 2% opacity

---

## AFTER BUILDING ALL 3 + DIVIDERS:

1. Register slides in `web/src/data/slides.js` if needed
2. Run `cd web && npm run build` — zero errors
3. This completes the full deck rebuild

## Checklist per slide:
- [ ] Stats in HORIZONTAL ROW on top (grid-cols-3 or grid-cols-4)
- [ ] Every stat card has: label, big number, trend badge, footer with border-t and 2 lines
- [ ] Chart/content FULL WIDTH below the stat row
- [ ] NO separate side-by-side card layouts
- [ ] Card surface: rounded-xl bg-white border border-zinc-200 shadow-sm
- [ ] Source citation present
- [ ] Motion animations: stat cards staggered (0.3 + i * 0.08), chart at 0.5s delay
- [ ] StatCards have `whileHover={{ y: -2 }}` + hover:shadow-md transition
- [ ] ChartCard has hover:shadow-md transition
- [ ] Hero chart card has gold accent strip + `pl-8` padding
- [ ] Table rows have `hover:bg-zinc-50` (if TableCard present)
