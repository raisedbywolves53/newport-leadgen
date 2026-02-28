# Rebuild Slides 3–5 to Split Layout

Read `web/DESIGN-SYSTEM.md` completely before starting. Follow it exactly.

## THE LAYOUT

**SPLIT LAYOUT** = visual asset LEFT (col-span-3) + stat tiles RIGHT (col-span-2), stacked vertically.

```
┌────────────────────┬───────────┐
│                    │ StatCard  │
│   ChartCard        ├───────────┤
│   (visual asset)   │ StatCard  │
│                    ├───────────┤
│                    │ StatCard  │
│                    ├───────────┤
│                    │ StatCard  │
└────────────────────┴───────────┘
```

Grid: `grid-cols-5 gap-4` → visual `col-span-3`, tiles `col-span-2 flex flex-col gap-4`

## Compact StatCard Template (for RIGHT column — all 5 zones)
```jsx
<motion.div
  key={stat.label}
  initial={{ opacity: 0, y: 12 }}
  animate={{ opacity: 1, y: 0 }}
  whileHover={{ y: -2 }}
  transition={{ duration: 0.4, delay: 0.35 + i * 0.08 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out flex flex-col gap-3 py-4 cursor-default"
>
  <div className="px-4 flex flex-col gap-1.5">
    <div className="flex items-center justify-between">
      <span className="text-xs text-zinc-500">{stat.label}</span>
      <span className="inline-flex items-center gap-1 text-[11px] font-medium border border-zinc-200 rounded-md px-1.5 py-0.5 text-zinc-700">
        {stat.badgeIcon} {stat.badgeText}
      </span>
    </div>
    <span className="text-xl font-semibold tabular-nums tracking-tight" style={{ color: stat.accent }}>
      {stat.value}
    </span>
  </div>
  <div className="border-t border-zinc-100 px-4 pt-3 flex flex-col gap-1 text-xs">
    <div className="flex items-center gap-1.5 font-medium text-zinc-900">{stat.footerHighlight}</div>
    <div className="text-zinc-500 text-[11px]">{stat.footerDescription}</div>
  </div>
</motion.div>
```

## ChartCard LEFT Template (with gold accent strip)
```jsx
<motion.div
  initial={{ opacity: 0, y: 12 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, delay: 0.3 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out relative overflow-hidden h-full flex flex-col"
>
  <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />
  <div className="p-6 pb-0 pl-8">
    <h3 className="text-lg font-semibold text-zinc-950">{title}</h3>
    <p className="text-sm text-zinc-500 mt-1">{description}</p>
  </div>
  <div className="flex-1 p-6 pt-4 pl-8 min-h-0">
    {/* chart or visual content */}
  </div>
  <div className="px-6 pl-8 py-3 border-t border-zinc-100 flex items-center gap-4">
    {/* legend dots */}
  </div>
</motion.div>
```

---

## Slide 3: WhyNewportSlide.jsx — SPLIT

**LEFT (col-span-3):** InsightCard or narrative card. CardHeader "The Verifiable History Agencies Now Require". Content: the key paragraph about Newport's 30 years, post-fraud positioning, clean audit history as competitive moat.

**RIGHT (col-span-2):** 4 stacked compact tiles:
1. label "Continuous FL Operations", value "30 Years" (gold), badge "Since 1996", footer "Real warehouse, fleet, W-2 workforce" / "Plantation, FL"
2. label "Post-Fraud Vacuum", value "1,091" (gold), badge "↓ 25% cleared", footer "SBA cleared Jan 2026" / "DOJ prosecuted $550M"
3. label "Micro-Purchase Threshold", value "83%" (teal), badge "Below $15K", footer "No bid, no past performance needed" / "Fastest path to first contract"
4. label "Infrastructure Edge", value "$5M" (teal), badge "Entry Tier", footer "FL competitors #5–10 at $1–5M" / "Less capability than Newport"

---

## Slide 4: FloridaTamSlide.jsx — SPLIT

**LEFT (col-span-3):** ChartCard with concentric rings SVG. Gold accent strip. CardHeader "TAM by Channel" / "FL Government Food Procurement — $87M Total". Rings SVG fills available space — increase size to at least 320px diameter. CardFooter with 5-color legend.

**RIGHT (col-span-2):** 4 stacked compact tiles:
1. label "State Procurement", value "$20–30M" (gold), badge "MEDIUM", footer "MFMP + corrections + FL agencies" / "Largest single channel"
2. label "Education / NSLP", value "$10–20M" (gold), badge "MEDIUM", footer "67 county districts, 2.8M students" / "NSLP funded"
3. label "Micro-Purchase", value "$8–15M" (teal), badge "HIGH ↑", footer "83% invisible in databases" / "Below $15K — no bid required"
4. label "Federal + Local", value "$9.4M" (teal), badge "HIGH", footer "117 contracts + county jails" / "Visible tip + municipal"

---

## Slide 5: ProductMatrixSlide.jsx — SPLIT

**LEFT (col-span-3):** ChartCard with horizontal bar chart (ECharts — keep existing). Gold accent strip. CardHeader "FL Spend by Product Category" / "Gold = Tier 1, Teal = Tier 2, Gray = Avoid". CardFooter with tier legend.

**RIGHT (col-span-2):** 3 stacked compact tiles:
1. label "Confectionery & Nuts", value "$55M" (gold), badge "Highest Fit", footer "National spend, PSC 8925" / "Newport's #1 product match"
2. label "Sole-Source Rate", value "58%" (gold), badge "↑ No competition", footer "PSC 8925 sole-source" / "Lowest competition of all categories"
3. label "Evaluation Method", value "LPTA" (teal), badge "Price wins", footer "Lowest Price Technically Acceptable" / "Newport's wholesale pricing advantage"

---

## AFTER ALL 3 SLIDES:

1. Run `cd web && npm run build` — zero errors
2. Verify each slide uses `grid-cols-5` with visual `col-span-3` LEFT and tiles `col-span-2` RIGHT

## Checklist per slide:
- [ ] Uses `grid-cols-5 gap-4` split layout
- [ ] Visual card is `col-span-3` on LEFT with `h-full`
- [ ] Tiles are `col-span-2 flex flex-col gap-4` on RIGHT
- [ ] Visual card has gold accent strip + `pl-8` padding
- [ ] Tiles use compact variant: `py-4 px-4 gap-3 text-xs text-xl text-[11px]`
- [ ] Every tile has: label, value, badge, footer (all 5 zones)
- [ ] Hover states: `whileHover={{ y: -2 }}` + `hover:shadow-md hover:border-zinc-300`
- [ ] Source citation present
- [ ] Build passes
