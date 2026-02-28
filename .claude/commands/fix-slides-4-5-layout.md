# Fix Slides 4 & 5 Layout

Read `web/DESIGN-SYSTEM.md` sections 6.3 (Hero Visual Layout), 6.4 (Compact StatCard), and 10 (Visual Polish) before starting.

---

## Slide 4: FloridaTamSlide.jsx → Hero Visual Layout

**File:** `web/src/components/slides/FloridaTamSlide.jsx`

**CURRENT PROBLEM:** Stat cards sit in a horizontal row on top → concentric rings chart squeezed into a short band below. The circular rings visualization needs square space to breathe.

**FIX:** Switch to the Hero Visual Layout (DESIGN-SYSTEM.md section 6.3). Visual LEFT (60%), stat cards RIGHT (40%).

### New Layout Structure:

```jsx
{/* Replace the current ZONE 2 + ZONE 3 with this: */}

{/* HERO VISUAL LAYOUT: visual LEFT, stats RIGHT */}
<div className="grid grid-cols-5 gap-4 relative z-10" style={{ minHeight: '420px' }}>

  {/* LEFT: Concentric rings visualization — 3 of 5 columns */}
  <div className="col-span-3">
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out relative overflow-hidden h-full flex flex-col"
    >
      {/* Gold accent strip */}
      <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />

      {/* CardHeader */}
      <div className="p-6 pb-0 pl-8">
        <h3 className="text-lg font-semibold text-zinc-950">TAM by Channel</h3>
        <p className="text-sm text-zinc-500 mt-1">FL Government Food Procurement — $87M Total</p>
      </div>

      {/* CardContent — rings get ALL the space */}
      <div className="flex-1 flex items-center justify-center p-6 pl-8 min-h-0">
        {/* EXISTING concentric rings SVG goes here */}
        {/* Increase the SVG viewBox / container to fill available space */}
        {/* Target: at least 320px diameter for the rings */}
      </div>

      {/* CardFooter */}
      <div className="px-6 pl-8 py-3 border-t border-zinc-100 flex items-center gap-4 flex-wrap">
        {/* Color-dot legend: State, Education, Micro-Purchase, Federal FPDS, Local/Municipal */}
        {RING_CONFIG.map(ring => (
          <div key={ring.label} className="flex items-center gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: ring.color }} />
            <span className="text-xs text-zinc-500">{ring.label}</span>
          </div>
        ))}
      </div>
    </motion.div>
  </div>

  {/* RIGHT: 2×2 compact stat card grid — 2 of 5 columns */}
  <div className="col-span-2 grid grid-cols-2 gap-4">
    {STAT_CARDS.map((stat, i) => (
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
              {stat.badge.icon} {stat.badge.text}
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
    ))}
  </div>
</div>
```

### Key Changes:
1. **Delete** the current `grid-cols-4` stat row above the chart
2. **Delete** the current full-width ChartCard wrapper below the stat row
3. **Replace** with a single `grid-cols-5` container: visual LEFT (`col-span-3`), stats RIGHT (`col-span-2`)
4. **Stat cards** use the COMPACT variant: `py-4 px-4 gap-3`, `text-xs` labels, `text-xl` values, `text-[11px]` badges/footers
5. **SVG rings** should expand to fill available space — increase the container or SVG viewBox so rings are at least 320px diameter
6. **Move legend** from wherever it currently is into the ChartCard footer
7. Set `minHeight: '420px'` on the grid container so the visual gets tall space

### What NOT to change:
- Keep the header (eyebrow, headline, subtitle, gold line) exactly as-is
- Keep the source citation at the bottom
- Keep all 4 stat card data values the same
- Keep the concentric rings SVG and RING_CONFIG data

---

## Slide 5: ProductMatrixSlide.jsx → Compact Stat Cards + Taller Chart

**File:** `web/src/components/slides/ProductMatrixSlide.jsx`

**CURRENT PROBLEM:** Standard-size stat cards eat too much vertical space, leaving the horizontal bar chart cramped with limited room for bar labels and values.

**FIX:** Switch stat cards to COMPACT variant. Give chart more height.

### Changes to make:

**1. Compact the stat cards:**

Replace the current stat card styles:
```
py-6 → py-4
px-6 → px-4
gap-6 → gap-3
text-sm (label) → text-xs
text-2xl (value) → text-xl
text-xs (badge) → text-[11px]
text-sm (footer highlight) → text-xs
text-xs (footer description) → text-[11px]
```

**2. Increase chart height:**

Find the ChartCard container height (probably `style={{ height: '280px' }}` or similar) and change to:
```jsx
style={{ height: '340px' }}
```

**3. Add hover polish (if not already present):**
- Stat cards: `whileHover={{ y: -2 }}` + `hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out cursor-default`
- ChartCard: `hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out`

### What NOT to change:
- Keep `grid-cols-3 gap-4` for the stat row (3 cards horizontal)
- Keep all stat card data values the same
- Keep the chart type (horizontal bar, ECharts) and data
- Keep the header and source citation

---

## AFTER BOTH SLIDES:

1. Run `cd web && npm run build` — zero errors
2. Run `cd web && npm run dev` and verify:
   - Slide 4: Rings are large and prominent on the LEFT, 4 compact stat cards on the RIGHT in a 2×2 grid
   - Slide 5: Stat cards are more compact, bar chart has more vertical room

## Checklist:
- [ ] Slide 4 uses `grid-cols-5` Hero Visual Layout (visual LEFT, stats RIGHT)
- [ ] Slide 4 rings are at least 320px diameter
- [ ] Slide 4 stat cards use compact variant (`py-4 px-4 gap-3 text-xs`)
- [ ] Slide 5 stat cards use compact variant
- [ ] Slide 5 chart height is 340px (not 280px)
- [ ] Both slides have hover states on all cards
- [ ] Build passes with zero errors
