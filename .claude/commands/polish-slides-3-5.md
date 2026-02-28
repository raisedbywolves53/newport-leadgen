# Polish Pass: Slides 3–5

Read `web/DESIGN-SYSTEM.md` sections 10 (Visual Polish) and 11 (Recharts) completely before starting.

These 3 slides already have the correct dashboard-01 layout. This pass adds the **visual polish** that separates "functional" from "production shadcn quality."

---

## CHANGES TO APPLY TO ALL 3 SLIDES

### 1. StatCard Hover States

Find every stat card `<motion.div>` that contains stat card content and add:

**Before (current):**
```jsx
<motion.div
  key={stat.label}
  initial={{ opacity: 0, y: 12 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, delay: 0.3 + i * 0.08 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col gap-6 py-6"
>
```

**After (polished):**
```jsx
<motion.div
  key={stat.label}
  initial={{ opacity: 0, y: 12 }}
  animate={{ opacity: 1, y: 0 }}
  whileHover={{ y: -2 }}
  transition={{ duration: 0.4, delay: 0.3 + i * 0.08 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out flex flex-col gap-6 py-6 cursor-default"
>
```

Changes:
- Added `whileHover={{ y: -2 }}`
- Added `hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out`
- Added `cursor-default`

### 2. ChartCard Hover State

Find the main chart card `<motion.div>` and add the same hover treatment:

```
hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out
```

### 3. Chart Tooltip Polish

For any ECharts `tooltip` configuration, ensure these properties are present:

```jsx
tooltip: {
  // ... existing properties ...
  borderRadius: 8,
  extraCssText: 'box-shadow: 0 8px 24px rgba(0,0,0,0.25);',
}
```

### 4. Gold Accent Strip Padding

If the ChartCard has a gold accent strip (`absolute left-0 ... bg-[#C9A84C]`), ensure the CardHeader and CardContent use `pl-8` (not `pl-6` or default `p-6`).

---

## SLIDE-SPECIFIC CHANGES

### Slide 3: WhyNewportSlide.jsx

File: `web/src/components/slides/WhyNewportSlide.jsx`

1. Add hover states to all 4 stat cards (see section 1 above)
2. Add hover state to the InsightCard wrapper `<motion.div>`
3. No chart tooltip to update (this slide has an InsightCard instead of a chart)

### Slide 4: FloridaTamSlide.jsx

File: `web/src/components/slides/FloridaTamSlide.jsx`

1. Add hover states to all 4 stat cards
2. Add hover state to the ChartCard `<motion.div>`
3. The SVG concentric rings already have hover interaction — keep that
4. Ensure the gold accent strip's content siblings use `pl-8`

### Slide 5: ProductMatrixSlide.jsx

File: `web/src/components/slides/ProductMatrixSlide.jsx`

1. Add hover states to all 3 stat cards
2. Add hover state to the ChartCard `<motion.div>`
3. Update ECharts tooltip config: add `borderRadius: 8` and `extraCssText: 'box-shadow: 0 8px 24px rgba(0,0,0,0.25);'`
4. Ensure the gold accent strip's content siblings use `pl-8`

---

## AFTER ALL 3 SLIDES:

1. Run `cd web && npm run build` — zero errors
2. Run `cd web && npm run dev` and visually verify hover states work on each slide
3. Confirm: cards lift slightly on hover, shadow deepens, border darkens

## Checklist per slide:
- [ ] All stat cards have `whileHover={{ y: -2 }}` + `hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out`
- [ ] ChartCard / InsightCard wrapper has `hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out`
- [ ] ECharts tooltip has `borderRadius: 8` + `extraCssText` shadow (if applicable)
- [ ] Gold accent strip content uses `pl-8`
- [ ] Build passes with zero errors
