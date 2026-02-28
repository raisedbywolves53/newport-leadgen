# Newport Presentation Design System

> **Purpose**: Single source of truth for every visual decision in the Newport web presentation (slides 3–19). Written so an AI coding assistant can mechanically produce slides that match the [shadcn/ui dashboard-01 block](https://ui.shadcn.com/blocks).
>
> **Slides 1–2 are EXCLUDED** from these guidelines.
>
> **Visual north star:** The `dashboard-01` block from [shadcn/ui](https://ui.shadcn.com/blocks). The actual source is at `apps/v4/app/(examples)/dashboard/` in the shadcn-ui/ui repo. The defining characteristics: **stat cards in a horizontal row on top → chart full-width below → optional table below that.** Every data slide MUST follow this vertical flow.

---

## 1. THE ONE RULE (Read This First)

Previous versions of this system offered 6 layout patterns (A–F). That created too much variation. **There is now ONE layout.**

It is the shadcn `dashboard-01` layout:

```
┌──────────┬──────────┬──────────┬──────────┐
│ StatCard │ StatCard │ StatCard │ StatCard │  ← HORIZONTAL ROW of stat cards
└──────────┴──────────┴──────────┴──────────┘
┌────────────────────────────────────────────┐
│                                            │
│   ChartCard (FULL WIDTH)                   │  ← Chart BELOW the stat row
│                                            │
└────────────────────────────────────────────┘
┌────────────────────────────────────────────┐
│   Optional: TableCard or InsightCard       │  ← Optional third row
└────────────────────────────────────────────┘
```

**This is the ONLY layout. Every data slide uses it.**

The vertical flow is always:
1. **Slide header** (eyebrow → headline → subtitle → gold line)
2. **Stat card row** — 3 or 4 cards in `grid-cols-3` or `grid-cols-4`, horizontal
3. **Chart card** — full width, always BELOW the stat row
4. **Optional bottom row** — table, insight, or additional stat cards
5. **Source citation**

**What this means for existing slides:**
- NO `grid-cols-[3fr_2fr]` layouts (chart beside stats)
- NO vertical stat tile stacks
- NO bento grids (hero card spanning rows)
- Stats are ALWAYS in a horizontal row. Charts are ALWAYS below them.

---

## 2. StatCard — The Core Building Block

This is extracted from shadcn's actual `section-cards.tsx` source code (`apps/v4/app/(examples)/dashboard/components/section-cards.tsx`).

**shadcn's actual card anatomy:**
```
CardHeader
  ├── CardDescription  (muted label — "Total Revenue")
  ├── CardTitle        (big bold number — "$1,250.00")
  └── CardAction       (Badge with trend icon + percentage — "↑ +12.5%")
CardFooter
  ├── Trend line       (font-medium text + icon — "Trending up this month ↑")
  └── Description      (muted — "Visitors for the last 6 months")
```

**Newport translation** (no shadcn Card primitives — we use plain divs):

```jsx
{/* StatCard — use for EVERY stat tile */}
<motion.div
  whileHover={{ y: -2 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm
             hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out
             flex flex-col gap-6 py-6 cursor-default"
>
  {/* CardHeader zone */}
  <div className="px-6 flex flex-col gap-2">
    {/* Row 1: muted label (left) + trend badge (right) */}
    <div className="flex items-center justify-between">
      <span className="text-sm text-zinc-500">{label}</span>
      <span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-zinc-700">
        {trendIcon} {trendText}
      </span>
    </div>
    {/* Row 2: big bold number */}
    <span className="text-2xl font-semibold tabular-nums tracking-tight" style={{ color: accentColor }}>
      {value}
    </span>
  </div>

  {/* CardFooter zone — separated by border */}
  <div className="border-t border-zinc-100 px-6 pt-4 flex flex-col gap-1.5 text-sm">
    <div className="flex items-center gap-2 font-medium text-zinc-900">
      {footerHighlight} {footerIcon}
    </div>
    <div className="text-zinc-500 text-xs">
      {footerDescription}
    </div>
  </div>
</motion.div>
```

**Rules:**
- Label is `text-sm text-zinc-500` — muted, top-left. This is the card's title (e.g., "FL Confectionery Spend", "Sole-Source Rate").
- Value is `text-2xl font-semibold tabular-nums` — the big number. Primary metric gold `#C9A84C`, secondary metrics `text-zinc-950` or teal `#1B7A8A`.
- Trend badge sits top-right: `border border-zinc-200 rounded-md px-2 py-0.5`. Contains an up/down arrow icon + percentage or keyword.
- Footer has `border-t border-zinc-100` separator. Two lines: a bold summary line with icon, and a muted description line.
- **EVERY StatCard MUST have all 4 zones**: label, value, trend badge, footer. This is what creates the shadcn density. Empty-looking cards = not enough content.

**Trend badge variants:**
```jsx
{/* Positive trend */}
<span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-emerald-700">
  <TrendingUp className="w-3 h-3" /> +12.5%
</span>

{/* Negative trend */}
<span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-red-600">
  <TrendingDown className="w-3 h-3" /> -20%
</span>

{/* Neutral / label-only (for non-trend data like "HIGH confidence") */}
<span className="inline-flex items-center gap-1 text-xs font-medium border border-zinc-200 rounded-md px-2 py-0.5 text-zinc-600">
  <Shield className="w-3 h-3" /> HIGH
</span>
```

**What makes this different from the old MetricCard:**
| Old MetricCard | New StatCard (shadcn) |
|---|---|
| Title + big number + 1 detail line | Label + big number + trend badge + 2-line footer |
| No trend indicator | Always has trend badge top-right |
| No footer border separator | Always has `border-t` footer zone |
| 3 pieces of content | 5+ pieces of content per card |
| Looks sparse | Looks dense and informational |

---

## 3. ChartCard — Wraps Every Visualization

Every ECharts visualization MUST be inside this wrapper. No exceptions.

```jsx
{/* ChartCard — wraps every ECharts visualization */}
<div className="rounded-xl bg-white border border-zinc-200 shadow-sm flex flex-col">
  {/* CardHeader */}
  <div className="p-6 pb-0">
    <h3 className="text-lg font-semibold text-zinc-950">{chartTitle}</h3>
    <p className="text-sm text-zinc-500 mt-1">{chartDescription}</p>
  </div>

  {/* CardContent — the chart */}
  <div className="p-6 pt-4 flex-1 min-h-0">
    <div ref={chartRef} className="w-full h-full" />
  </div>

  {/* CardFooter — legend, always present */}
  <div className="px-6 py-3 border-t border-zinc-100 flex items-center gap-4">
    {legendItems.map(item => (
      <div key={item.label} className="flex items-center gap-1.5">
        <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
        <span className="text-xs text-zinc-500">{item.label}</span>
      </div>
    ))}
  </div>
</div>
```

**Rules:**
- `CardHeader`: title (`text-lg font-semibold text-zinc-950`) + description (`text-sm text-zinc-500`)
- `CardContent`: chart renders here. `flex-1 min-h-0`
- `CardFooter`: **ALWAYS present**. Separated by `border-t border-zinc-100`. Color-dot legend.
- For the hero chart on a slide, add gold accent strip: `<div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />`
- Chart height: set via parent container, 240–320px
- Chart background: always `transparent`

---

## 4. TableCard

```jsx
{/* TableCard */}
<div className="rounded-xl bg-white border border-zinc-200 shadow-sm">
  <div className="p-6 pb-0">
    <h3 className="text-lg font-semibold text-zinc-950">{tableTitle}</h3>
    <p className="text-sm text-zinc-500 mt-1">{tableDescription}</p>
  </div>
  <div className="p-6 pt-4">
    {/* Header row */}
    <div className="grid grid-cols-[...] border-b border-zinc-200 pb-3 mb-1">
      <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Column</span>
    </div>
    {/* Data rows */}
    {rows.map((row, i) => (
      <div key={i} className={`grid grid-cols-[...] py-3 ${i % 2 === 0 ? 'bg-zinc-50/50' : ''}`}>
        <span className="text-sm text-zinc-900">{row.name}</span>
        <span className="text-sm text-zinc-600 text-right font-medium">{row.value}</span>
      </div>
    ))}
  </div>
</div>
```

---

## 5. InsightCard (max 1 per slide)

```jsx
{/* InsightCard — max 1 per slide */}
<div className="rounded-xl bg-amber-50/50 border border-amber-200/50 shadow-sm p-6">
  <div className="flex items-start gap-3">
    <div className="w-8 h-8 rounded-md bg-amber-100 flex items-center justify-center shrink-0">
      <Lightbulb className="w-4 h-4 text-amber-600" strokeWidth={1.5} />
    </div>
    <div>
      <h4 className="text-sm font-semibold text-zinc-950 mb-1">{insightTitle}</h4>
      <p className="text-sm text-zinc-600 leading-relaxed">{insightText}</p>
    </div>
  </div>
</div>
```

---

## 6. THE LAYOUT — Two Simple Rules

### 6.1 The Two Layout Rules

**Rule 1 — SPLIT LAYOUT (default for most slides):**
Visual asset (chart, graph, donut, rings, process flow) on the LEFT → stat tiles on the RIGHT.

**Rule 2 — TABLE LAYOUT (exception):**
When the slide's main content is a TABLE, use: stat tiles in a horizontal row on TOP → full-width table BELOW.

That's it. Every data slide uses one of these two.

```
RULE 1 — SPLIT (default):                 RULE 2 — TABLE (exception):

┌────────────────────┬───────────┐         ┌──────┬──────┬──────┬──────┐
│                    │ StatCard  │         │ Stat │ Stat │ Stat │ Stat │
│   ChartCard        ├───────────┤         └──────┴──────┴──────┴──────┘
│   (visual asset)   │ StatCard  │         ┌────────────────────────────┐
│                    ├───────────┤         │                            │
│                    │ StatCard  │         │   TableCard (full width)   │
│                    ├───────────┤         │                            │
│                    │ StatCard  │         └────────────────────────────┘
└────────────────────┴───────────┘
```

### 6.2 Split Layout — Full Structure

```jsx
export default function SomeSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden">

      {/* ZONE 1: Header */}
      <div className="mb-4 relative z-10">
        <span className="inline-block text-xs font-medium uppercase tracking-widest text-zinc-400 mb-3">
          {eyebrowLabel}
        </span>
        <h2 className="text-3xl font-semibold tracking-tight text-zinc-950 mb-2">
          {headline}
        </h2>
        <p className="text-sm text-zinc-600 max-w-2xl">
          {subtitle}
        </p>
        <GoldLine width={48} className="mt-3" />
      </div>

      {/* ZONE 2: Split — visual LEFT, tiles RIGHT */}
      <div className="grid grid-cols-5 gap-4 relative z-10 flex-1 min-h-0">

        {/* LEFT: ChartCard — 3 of 5 columns */}
        <div className="col-span-3">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="rounded-xl bg-white border border-zinc-200 shadow-sm
                       hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out
                       relative overflow-hidden h-full flex flex-col"
          >
            {/* Gold accent strip */}
            <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />

            {/* CardHeader */}
            <div className="p-6 pb-0 pl-8">
              <h3 className="text-lg font-semibold text-zinc-950">{chartTitle}</h3>
              <p className="text-sm text-zinc-500 mt-1">{chartDescription}</p>
            </div>

            {/* CardContent — chart/graph/visual fills remaining space */}
            <div className="flex-1 p-6 pt-4 pl-8 min-h-0">
              <ResponsiveContainer width="100%" height="100%">
                {/* Recharts chart or custom SVG */}
              </ResponsiveContainer>
            </div>

            {/* CardFooter */}
            <div className="px-6 pl-8 py-3 border-t border-zinc-100 flex items-center gap-4">
              {/* Legend dots */}
            </div>
          </motion.div>
        </div>

        {/* RIGHT: Stat tiles — 2 of 5 columns, stacked vertically */}
        <div className="col-span-2 flex flex-col gap-4">
          {STATS.map((stat, i) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              whileHover={{ y: -2 }}
              transition={{ duration: 0.4, delay: 0.35 + i * 0.08 }}
              className="rounded-xl bg-white border border-zinc-200 shadow-sm
                         hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out
                         flex flex-col gap-3 py-4 cursor-default"
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
          ))}
        </div>
      </div>

      {/* ZONE 3 (optional): Bottom row — InsightCard or additional context */}

      {/* ZONE 4: Source */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <p className="text-[10px] text-zinc-300">{sourceCitation}</p>
        <CompassStar size={14} opacity={0.2} />
      </div>
    </div>
  )
}
```

**Split layout rules:**
- `grid-cols-5` — visual `col-span-3` (60%) LEFT, tiles `col-span-2` (40%) RIGHT
- Visual card gets gold accent strip + `pl-8` on all content
- Stat tiles use the **compact variant** (see section 6.3) — they stack vertically
- 3 or 4 stat tiles. If 3, they fill nicely. If 4, spacing is tighter.
- The visual card is `h-full` — it stretches to match the total height of stacked tiles
- Optional InsightCard or bottom row below the split (full width)

### 6.3 Compact StatCard (Used in Split Layout)

Stat tiles in the split layout use compact sizing so 3–4 can stack vertically.

```jsx
{/* Compact StatCard — used in split layout RIGHT column */}
<motion.div
  whileHover={{ y: -2 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm
             hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out
             flex flex-col gap-3 py-4 cursor-default"
>
  <div className="px-4 flex flex-col gap-1.5">
    <div className="flex items-center justify-between">
      <span className="text-xs text-zinc-500">{label}</span>
      <span className="inline-flex items-center gap-1 text-[11px] font-medium border border-zinc-200 rounded-md px-1.5 py-0.5 text-zinc-700">
        {trendIcon} {trendText}
      </span>
    </div>
    <span className="text-xl font-semibold tabular-nums tracking-tight" style={{ color: accentColor }}>
      {value}
    </span>
  </div>
  <div className="border-t border-zinc-100 px-4 pt-3 flex flex-col gap-1 text-xs">
    <div className="flex items-center gap-1.5 font-medium text-zinc-900">{footerHighlight}</div>
    <div className="text-zinc-500 text-[11px]">{footerDescription}</div>
  </div>
</motion.div>
```

**Compact vs standard sizing:**
| Property | Standard (old) | Compact (split layout) |
|---|---|---|
| Outer padding | `py-6` | `py-4` |
| Inner padding | `px-6` | `px-4` |
| Gap between zones | `gap-6` | `gap-3` |
| Label size | `text-sm` | `text-xs` |
| Value size | `text-2xl` | `text-xl` |
| Badge size | `text-xs` | `text-[11px]` |
| Footer text | `text-sm` / `text-xs` | `text-xs` / `text-[11px]` |

### 6.4 Table Layout — Full Structure

Use when the slide's main content is a data table.

```jsx
export default function TableSlide() {
  return (
    <div className="w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden">

      {/* ZONE 1: Header (same as split) */}
      <div className="mb-4 relative z-10">
        {/* eyebrow → headline → subtitle → GoldLine */}
      </div>

      {/* ZONE 2: Stat card row — HORIZONTAL on top */}
      <div className="grid grid-cols-3 gap-4 mb-4 relative z-10">
        <StatCard ... />  {/* Standard size — NOT compact */}
        <StatCard ... />
        <StatCard ... />
      </div>

      {/* ZONE 3: TableCard — FULL WIDTH below */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.5 }}
        className="rounded-xl bg-white border border-zinc-200 shadow-sm
                   hover:shadow-md hover:border-zinc-300 transition-all duration-200 ease-out
                   relative overflow-hidden flex-1"
      >
        {/* Gold accent strip */}
        <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />
        {/* CardHeader + Table content + CardFooter */}
      </motion.div>

      {/* ZONE 4: Source */}
      <div className="flex items-center justify-between mt-4 relative z-10">
        <p className="text-[10px] text-zinc-300">{sourceCitation}</p>
      </div>
    </div>
  )
}
```

**Table layout rules:**
- Stat cards on top use `grid-cols-3` or `grid-cols-4`, **standard** size (not compact)
- Standard StatCard: `py-6 px-6 gap-6 text-sm text-2xl` (the template from section 2)
- Table card is full-width below
- Table rows have `hover:bg-zinc-50 transition-colors duration-150`

### 6.5 Which Slides Use Which Layout

| Layout | Slides |
|---|---|
| **Split** (visual LEFT + tiles RIGHT) | 3, 4, 5, 6, 7, 8, 9, 11, 12, 14, 15, 16, 17 |
| **Table** (tiles top + table below) | 10, 13 |

### 6.6 Optional Bottom Row

After either layout, you can add ONE optional element below:

```jsx
{/* InsightCard — max 1 per slide */}
<div className="mt-4">
  <InsightCard ... />
</div>
```

### 6.7 Slides Without Charts or Tables

Some slides are text/process-focused (like slide 8's pipeline). They still use the **split layout** — the LEFT card contains the process flow or content instead of a chart. Same `grid-cols-5` structure, same ChartCard wrapper.

---

## 7. Color System

### 7.1 Slide Background
`#f4f4f5` (zinc-100) — set by `SlideBackground`, never override.

### 7.2 Text Hierarchy

| Role | Tailwind | Hex |
|---|---|---|
| Headline | `text-zinc-950` | `#09090b` |
| Card title (chart/table) | `text-zinc-950` | `#09090b` |
| StatCard label | `text-zinc-500` | `#71717a` |
| Body text | `text-zinc-600` | `#52525b` |
| StatCard footer description | `text-zinc-500` | `#71717a` |
| Detail / caption | `text-zinc-400` | `#a1a1aa` |
| Source | `text-zinc-300` | `#d4d4d8` |

### 7.3 Accent Colors (strict — never add more)

| Role | Name | Hex |
|---|---|---|
| Primary accent | Gold | `#C9A84C` |
| Secondary accent | Teal | `#1B7A8A` |
| 3rd data series only | Light teal | `#3CC0D4` |
| 4th data series only | Amber | `#E8913A` |

**StatCard value color rules:**
- Primary metric of the slide → gold `#C9A84C`
- Secondary metrics → `text-zinc-950` or teal `#1B7A8A`

### 7.4 Card Surface (ONE surface — no variants)

```
rounded-xl bg-white border border-zinc-200 shadow-sm
```

Every card uses this. No `bg-white/70`, no `backdrop-blur`. Solid white, zinc-200 border, shadow-sm.

### 7.5 Card Accent Variants

| Variant | How | When |
|---|---|---|
| Gold accent strip | `absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]` | Hero chart card only (1 per slide max) |
| Insight card | `bg-amber-50/50 border-amber-200/50` | InsightCard component (1 per slide max) |

---

## 8. Typography

### 8.1 Font Stack
- **Display**: `Playfair Display` — ONLY slide 1 title
- **Everything else**: `Inter` (`font-body` class)

### 8.2 Scale

| Element | Classes |
|---|---|
| Slide headline | `text-3xl font-semibold tracking-tight text-zinc-950` |
| Eyebrow | `text-xs font-medium uppercase tracking-widest text-zinc-400` |
| ChartCard title | `text-lg font-semibold text-zinc-950` |
| ChartCard description | `text-sm text-zinc-500` |
| StatCard label | `text-sm text-zinc-500` |
| StatCard value | `text-2xl font-semibold tabular-nums tracking-tight` |
| StatCard trend badge | `text-xs font-medium` |
| StatCard footer highlight | `text-sm font-medium text-zinc-900` |
| StatCard footer description | `text-xs text-zinc-500` |
| Body text | `text-sm text-zinc-600 leading-relaxed` |
| Table header | `text-xs font-medium text-zinc-500 uppercase tracking-wider` |
| Table cell | `text-sm text-zinc-700` |
| Source | `text-[10px] text-zinc-300` |
| Legend item | `text-xs text-zinc-500` |

---

## 9. Charts (ECharts)

### 9.1 Setup

```jsx
import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([BarChart, GridComponent, TooltipComponent, CanvasRenderer])
```

### 9.2 Lifecycle

```jsx
const chartRef = useRef(null)

useEffect(() => {
  if (!chartRef.current) return
  const chart = echarts.init(chartRef.current, null, { renderer: 'canvas' })
  chart.setOption({ /* ... */ })

  const handleResize = () => chart.resize()
  window.addEventListener('resize', handleResize)
  return () => {
    window.removeEventListener('resize', handleResize)
    chart.dispose()
  }
}, [])
```

### 9.3 Universal Chart Options

```jsx
{
  backgroundColor: 'transparent',
  animation: false,
  tooltip: {
    trigger: 'axis',
    backgroundColor: '#18181b',
    borderColor: '#27272a',
    borderWidth: 1,
    textStyle: {
      color: '#fafafa',
      fontFamily: 'Inter, system-ui, sans-serif',
      fontSize: 12,
    },
    padding: [8, 12],
  },
}
```

### 9.4 Chart Types

| Data story | Chart type | Key settings |
|---|---|---|
| Part-to-whole | Donut | `radius: ['52%', '78%']`, center label |
| Ranking | Horizontal bar | Sorted desc, `barWidth: 18`, labels right |
| Trend | Line/Area | `smooth: true`, area fill 8% opacity |
| Composition over time | Stacked bar | `barWidth: 28`, 4 series max |

### 9.5 Chart Color Series

| Series | Color |
|---|---|
| 1st | `#C9A84C` (gold) |
| 2nd | `#1B7A8A` (teal) |
| 3rd | `#3CC0D4` (light teal) |
| 4th | `#E8913A` (amber) |

### 9.6 Axis Styling

```jsx
xAxis: {
  axisLine: { lineStyle: { color: '#e5e5e5' } },
  axisTick: { show: false },
  axisLabel: { fontSize: 11, fontFamily: 'Inter, system-ui, sans-serif', color: '#71717a' },
},
yAxis: {
  splitLine: { lineStyle: { color: '#e5e5e5', opacity: 0.5 } },
  axisLabel: { fontSize: 11, fontFamily: 'Inter, system-ui, sans-serif', color: '#71717a' },
}
```

### 9.7 CRITICAL: Charts Always Inside ChartCard

Never render ECharts without the ChartCard wrapper from section 3.

---

## 10. Visual Polish (Required)

These polish details close the gap between "functional dashboard" and "production shadcn quality." **Every card and chart MUST include these treatments.**

### 10.1 StatCard Hover State

Every StatCard gets an interactive hover treatment:

```jsx
<motion.div
  whileHover={{ y: -2 }}
  transition={{ duration: 0.15 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm
             hover:shadow-md hover:border-zinc-300
             transition-all duration-200 ease-out
             flex flex-col gap-6 py-6 cursor-default"
>
```

**Rules:**
- `hover:shadow-md` — subtle depth increase on hover
- `hover:border-zinc-300` — border darkens slightly
- `transition-all duration-200 ease-out` — smooth CSS transition for shadow + border
- `whileHover={{ y: -2 }}` via Motion — card lifts 2px
- `cursor-default` — cards are informational, not clickable

### 10.2 ChartCard Hover State

```jsx
<motion.div
  initial={{ opacity: 0, y: 12 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, delay: 0.3 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm
             hover:shadow-md hover:border-zinc-300
             transition-all duration-200 ease-out
             relative overflow-hidden"
>
```

Same hover pattern as StatCards — `hover:shadow-md hover:border-zinc-300 transition-all duration-200`.

### 10.3 Trend Badge Color System

Use specific badge colors to convey meaning at a glance:

```jsx
{/* Positive / growth */}
className="text-emerald-700 bg-emerald-50"

{/* Warning / caution */}
className="text-amber-700 bg-amber-50"

{/* Negative / risk */}
className="text-red-700 bg-red-50"

{/* Neutral / informational (default) */}
className="text-zinc-600"
```

**Enhanced badge template with subtle background fill:**
```jsx
<span className="inline-flex items-center gap-1 text-xs font-medium
                 border border-emerald-200 rounded-md px-2 py-0.5
                 text-emerald-700 bg-emerald-50">
  <TrendingUp className="w-3 h-3" /> +12.5%
</span>
```

The key difference: add `bg-{color}-50` and change `border-zinc-200` to `border-{color}-200` for colored badges. Use sparingly — max 1 colored badge per stat row, rest should be neutral `text-zinc-600 border-zinc-200`.

### 10.4 Gold Accent Strip (Hero Card)

The main chart card gets a gold left-border accent:

```jsx
{/* Inside ChartCard, first child */}
<div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />
```

- Apply to the PRIMARY chart card only (1 per slide max)
- Requires `relative` on the parent
- Adds `pl-8` to CardHeader and CardContent (instead of `pl-6`) to clear the strip

### 10.5 Subtle Card Top Gradient (Optional Enhancement)

For the hero stat card on a slide (typically Card 1), add a subtle top gradient:

```jsx
<div className="rounded-xl bg-white border border-zinc-200 shadow-sm
                flex flex-col gap-6 py-6 relative overflow-hidden">
  {/* Subtle gradient overlay — hero card only */}
  <div className="absolute inset-0 bg-gradient-to-b from-amber-50/30 to-transparent pointer-events-none" />
  {/* ... card content ... */}
</div>
```

**Rules:**
- Maximum 1 gradient-highlighted card per slide
- Use `from-amber-50/30` (gold family) for Tier 1 / primary metrics
- Use `from-sky-50/30` (teal family) for secondary emphasis
- Always `to-transparent`, always `pointer-events-none`
- Card content must have `relative z-10` to sit above the gradient

### 10.6 Table Row Hover

TableCard rows should have subtle hover states:

```jsx
<div className={`grid grid-cols-[...] py-3 transition-colors duration-150
                 hover:bg-zinc-50
                 ${i % 2 === 0 ? 'bg-zinc-50/50' : ''}`}>
```

### 10.7 Chart Tooltip Polish

ECharts tooltips should feel native to the card system:

```jsx
tooltip: {
  backgroundColor: '#18181b',
  borderColor: '#27272a',
  borderWidth: 1,
  borderRadius: 8,              // ← match card radius
  padding: [10, 14],
  textStyle: {
    color: '#fafafa',
    fontFamily: 'Inter, system-ui, sans-serif',
    fontSize: 12,
    lineHeight: 18,
  },
  extraCssText: 'box-shadow: 0 8px 24px rgba(0,0,0,0.25);',  // ← elevated shadow
}
```

### 10.8 Polish Checklist

Add to the quality checklist for every slide:

- [ ] StatCards have `hover:shadow-md hover:border-zinc-300 transition-all duration-200`
- [ ] ChartCard has `hover:shadow-md hover:border-zinc-300 transition-all duration-200`
- [ ] Hero chart card has gold accent strip + `pl-8`
- [ ] At most 1 colored trend badge per stat row (rest neutral)
- [ ] Table rows have `hover:bg-zinc-50` if TableCard is present
- [ ] Chart tooltip has `borderRadius: 8` and `extraCssText` shadow

---

## 11. Charts — Recharts (Preferred for New Slides)

**Recharts** is now the preferred charting library for new slides. It produces cleaner, more polished output with less configuration than ECharts and integrates natively with React (declarative JSX instead of imperative options objects).

**ECharts remains supported** for existing slides. Do NOT refactor working ECharts slides to Recharts unless specifically asked. But all NEW slides should use Recharts.

### 11.1 Setup

```jsx
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell
} from 'recharts'
```

### 11.2 Horizontal Bar Chart (Most Common)

```jsx
<ResponsiveContainer width="100%" height="100%">
  <BarChart
    data={data}
    layout="vertical"
    margin={{ top: 0, right: 80, left: 0, bottom: 0 }}
    barSize={18}
  >
    <CartesianGrid
      horizontal={false}
      stroke="#e5e5e5"
      strokeOpacity={0.5}
      strokeDasharray="4 4"
    />
    <XAxis type="number" hide />
    <YAxis
      type="category"
      dataKey="name"
      axisLine={false}
      tickLine={false}
      tick={{ fontSize: 12, fontFamily: 'Inter, system-ui, sans-serif', fill: '#18181b' }}
      width={140}
    />
    <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0,0,0,0.03)' }} />
    <Bar dataKey="value" radius={[0, 4, 4, 0]}>
      {data.map((entry, i) => (
        <Cell key={i} fill={entry.tier === 1 ? 'rgba(201,168,76,0.80)' : 'rgba(27,122,138,0.70)'} />
      ))}
    </Bar>
  </BarChart>
</ResponsiveContainer>
```

### 11.3 Donut Chart

```jsx
import { PieChart, Pie, Cell } from 'recharts'

<ResponsiveContainer width="100%" height="100%">
  <PieChart>
    <Pie
      data={donutData}
      cx="50%"
      cy="50%"
      innerRadius="52%"
      outerRadius="78%"
      paddingAngle={2}
      dataKey="value"
      stroke="none"
    >
      {donutData.map((entry, i) => (
        <Cell key={i} fill={COLORS[i]} />
      ))}
    </Pie>
    <Tooltip content={<CustomTooltip />} />
  </PieChart>
</ResponsiveContainer>
```

### 11.4 Stacked Bar Chart (Portfolio Evolution)

```jsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

<ResponsiveContainer width="100%" height="100%">
  <BarChart data={yearData} barSize={28}>
    <CartesianGrid vertical={false} stroke="#e5e5e5" strokeOpacity={0.5} />
    <XAxis dataKey="year" axisLine={false} tickLine={false}
           tick={{ fontSize: 12, fontFamily: 'Inter, system-ui, sans-serif', fill: '#71717a' }} />
    <YAxis axisLine={false} tickLine={false}
           tick={{ fontSize: 11, fontFamily: 'Inter, system-ui, sans-serif', fill: '#71717a' }} />
    <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(0,0,0,0.03)' }} />
    <Bar dataKey="tier1" stackId="a" fill="#C9A84C" radius={[0, 0, 0, 0]} />
    <Bar dataKey="tier2" stackId="a" fill="#1B7A8A" radius={[0, 0, 0, 0]} />
    <Bar dataKey="tier3" stackId="a" fill="#3CC0D4" radius={[0, 0, 0, 0]} />
    <Bar dataKey="micro" stackId="a" fill="#E8913A" radius={[4, 4, 0, 0]} />
  </BarChart>
</ResponsiveContainer>
```

### 11.5 Custom Tooltip (Matches Card System)

```jsx
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-lg px-4 py-3 shadow-lg"
         style={{ backgroundColor: '#18181b', border: '1px solid #27272a' }}>
      <p className="text-[13px] font-semibold text-zinc-50">{label}</p>
      {payload.map((p, i) => (
        <p key={i} className="text-xs text-zinc-300 mt-0.5">
          {p.name}: <span className="font-medium text-zinc-50">{p.value}</span>
        </p>
      ))}
    </div>
  )
}
```

### 11.6 Color Series (Same as ECharts)

| Series | Color |
|---|---|
| 1st | `#C9A84C` (gold) |
| 2nd | `#1B7A8A` (teal) |
| 3rd | `#3CC0D4` (light teal) |
| 4th | `#E8913A` (amber) |

### 11.7 Recharts Inside ChartCard

Same ChartCard wrapper from section 3. The only difference: `<ResponsiveContainer>` replaces the `ref={chartRef}` div:

```jsx
{/* CardContent: Recharts */}
<div className="p-6 pt-4 pl-8 flex-1 min-h-0">
  <ResponsiveContainer width="100%" height="100%">
    <BarChart ... />
  </ResponsiveContainer>
</div>
```

No `useEffect`, no `useRef`, no manual `dispose()`. Recharts handles all of this declaratively.

### 11.8 When to Use Which

| Scenario | Library |
|---|---|
| Existing slides (3–5) already using ECharts | Keep ECharts |
| New slides (6–17) with standard charts | Use Recharts |
| Custom SVG visualizations (concentric rings, etc.) | Keep custom SVG |
| Any chart inside ChartCard | Either library works |

---

## 12. Animation System (unchanged)

| Element | Initial | Animate | Duration | Delay |
|---|---|---|---|---|
| Eyebrow | `opacity: 0` | `opacity: 1` | 0.3s | 0.05s |
| Headline | `opacity: 0, y: 8` | `opacity: 1, y: 0` | 0.35s | 0.1s |
| Subtitle | `opacity: 0` | `opacity: 1` | 0.35s | 0.2s |
| GoldLine | `width: 0` | `width: target` | 0.6s | 0.25s |
| Stat cards (staggered) | `opacity: 0, y: 12` | `opacity: 1, y: 0` | 0.4s | 0.3 + i × 0.08 |
| Chart card | `opacity: 0, y: 12` | `opacity: 1, y: 0` | 0.5s | 0.5s |
| Bottom row | `opacity: 0, y: 12` | `opacity: 1, y: 0` | 0.4s | 0.6s |
| Source | `opacity: 0` | `opacity: 1` | 0.35s | last |

Total budget: under 1.5 seconds. `useCountUp` for animated numbers.

---

## 13. Decorative Elements

| Element | Component | Rules |
|---|---|---|
| Gold line | `GoldLine` | Below subtitle. Width 48px. |
| Compass star | `CompassStar` | Bottom-right. Max 1 in 3 slides. Size 14, opacity 0.2. |
| Background ring | `BackgroundRing` | Max 1 per slide. Corner, half off-screen. Opacity 0.03. |

---

## 14. Spacing Rules

| Context | Value |
|---|---|
| Gap between cards | `gap-4` (16px) |
| Stat row to chart | `mb-4` on stat row |
| Chart to bottom row | `mt-4` on bottom row |
| Header to content | `mb-4` |
| Card internal padding | `p-6` (stat cards use `py-6 px-6`) |
| Slide horizontal padding | `px-16 lg:px-20` |
| Content to source | `mt-4` |

---

## 15. Slide-by-Slide Instructions

**Every slide uses one of two layouts (see section 6):**
- **SPLIT** = visual LEFT (col-span-3) + stat tiles RIGHT (col-span-2)
- **TABLE** = stat tiles horizontal on TOP + full-width table BELOW

---

### Slide 3: Why Newport — SPLIT

**Data:** hardcoded pillars
**LEFT:** InsightCard with narrative about Newport's competitive moat (30 years, real infrastructure, post-fraud positioning). CardHeader "The Verifiable History Agencies Now Require".
**RIGHT:** 4 stacked compact tiles:
- "30 Years" (gold), badge "Since 1996", footer "Real warehouse, fleet, W-2 workforce" / "Plantation, FL"
- "1,091" (gold), badge "↓ 25% of 8(a)", footer "SBA cleared Jan 2026" / "DOJ prosecuted $550M"
- "83%" (teal), badge "Below $15K", footer "No bid, no past performance needed" / "Fastest path to first contract"
- "$1–5M" (teal), badge "Entry Tier", footer "FL competitors #5–10" / "Less capability than Newport"

---

### Slide 4: Florida TAM — SPLIT

**Data:** RING_CONFIG from FloridaTamSlide
**LEFT:** ChartCard with concentric rings SVG. CardHeader "TAM by Channel" / "$87M Total". SVG fills available space (min 320px diameter). CardFooter with 5-color legend.
**RIGHT:** 4 stacked compact tiles:
- "State Procurement" → "$20–30M" (gold), badge "MEDIUM"
- "Education / NSLP" → "$10–20M" (gold), badge "MEDIUM"
- "Micro-Purchase" → "$8–15M" (teal), badge "HIGH ↑"
- "Federal + Local" → "$9.4M" (teal), badge "HIGH"

---

### Slide 5: Product Matrix — SPLIT

**Data:** `PRODUCT_TIERS` from `market.js`
**LEFT:** ChartCard with horizontal bar chart. CardHeader "FL Spend by Product Category" / "Gold = Tier 1, Teal = Tier 2, Gray = Avoid". CardFooter with tier legend.
**RIGHT:** 3 stacked compact tiles:
- "Confectionery & Nuts" → "$55M" (gold), badge "Highest Fit"
- "Sole-Source Rate" → "58%" (gold), badge "↑ No competition"
- "Evaluation Method" → "LPTA" (teal), badge "Price wins"

---

### Slide 6: The Confectionery Gap — SPLIT

**Data:** `PRODUCT_TIERS.tier1[0]` from `market.js`
**LEFT:** ChartCard with donut chart. Gold = sole-source (58%), zinc = competitive. Center label "58%". CardHeader "Competition Density" / "PSC 8925 — Confectionery & Nuts".
**RIGHT:** 3 stacked compact tiles:
- "National Spend" → "$55M" (gold), badge "Tier 1"
- "FL Awards" → "45" (teal), badge "FY2024"
- "Avg. Offers per Award" → "1.6" (teal), badge "Low competition"

**Bottom row (optional):** InsightCard about Segment E pricing advantage.

---

### Slide 7: Competition Landscape — SPLIT

**Data:** `COMPETITORS` from `market.js`
**LEFT:** ChartCard with horizontal bar chart of 8 competitors. Newport highlighted in teal. CardHeader "FL Food Procurement by Vendor" / "FPDS FY2024 Award Volume".
**RIGHT:** 4 stacked compact tiles:
- "Top Competitor" → "$26.1M" (gold), badge "Dominant"
- "Active Competitors" → "8" (teal), badge "Moderate"
- "Newport Target" → "#6" (teal), badge "Entry point"
- "Gap to #5" → "$5M+" (gold), badge "↑ Opportunity"

---

### Slide 8: How It Works (Pipeline) — SPLIT

**Data:** `PIPELINE_STAGES`, `SOURCING_CHANNELS` from `strategy.js`
**LEFT:** ChartCard with 5-step pipeline process flow (horizontal chevron steps). CardHeader "Procurement Pipeline" / "From registration to recurring revenue".
**RIGHT:** 4 stacked compact tiles (sourcing channels):
- "SAM.gov" → "Free" (gold), badge "Primary"
- "MFMP / MyFL" → "Free" (gold), badge "State"
- "BidNet / DemandStar" → "$5–13K/yr" (teal), badge "Paid"
- "Direct Outreach" → "Free" (teal), badge "Proactive"

---

### Slide 9: Target Agencies — SPLIT

**Data:** `TARGET_AGENCIES` from `market.js`
**LEFT:** ChartCard with horizontal bar chart of agency values. DOJ bar in gold. CardHeader "FL Contract Value by Agency" / "Annual addressable opportunity".
**RIGHT:** 4 stacked compact tiles (one per agency):
- "DOJ / BOP" → value from data (gold), badge "Primary"
- "USDA" → value from data (teal), badge "Secondary"
- "VA Medical" → value from data (teal), badge "Steady"
- "DoD Commissary" → value from data (teal), badge "Volume"

---

### Slide 10: Real Contracts — TABLE

**Data:** `CONTRACT_EXAMPLES` from `strategy.js`
**TOP ROW:** `grid-cols-3` standard stat cards:
- "Active Opportunities" → "8" (gold), badge "Qualified"
- "Combined Value" → "$155K+" (teal), badge "Addressable"
- "High Fit Rating" → "75%" (teal), badge "Strong"

**BELOW:** Full-width TableCard. CardHeader "Contract Pipeline" / "Scored by product fit, size, and competition". Table with columns: Contract, Agency, Value, Fit Rating. Fit badges: HIGH = amber, MEDIUM = teal, LOW = zinc. Table rows have `hover:bg-zinc-50`.

---

### Slide 11: Portfolio Evolution — SPLIT

**Data:** `PORTFOLIO_EVOLUTION` from `financials.js`
**LEFT:** ChartCard with stacked bar chart Y1–Y5, 4 series. CardHeader "Contract Portfolio Growth" / "Projected 5-year build across contract tiers".
**RIGHT:** 3 stacked compact tiles:
- "Year 5 Contracts" → "78" (gold), badge "↑ Cumulative"
- "Renewal Rate" → "70%" (teal), badge "Industry avg"
- "Year 5 Revenue" → "$1.2M" (teal), badge "↑ Projected"

---

### Slide 12: Relationship Strategy — SPLIT

**Data:** `INFLUENCE_LAYERS`, `BD_PROCESS_STEPS` from `strategy.js`
**LEFT:** ChartCard with numbered vertical timeline (5 BD steps). CardHeader "Business Development Process" / "5-step relationship building".
**RIGHT:** 3 stacked compact tiles (influence layers):
- "Front-Line Buyers" → "Micro-Purchase" (gold), badge "Primary"
- "Program Managers" → "Requirements" (teal), badge "Influence"
- "Contracting Officers" → "Authority" (teal), badge "Decision"

---

### Slide 13: Risk & Compliance — TABLE

**Data:** `COMPLIANCE_REQUIRED`, `COMPLIANCE_NOT_NEEDED` from `strategy.js`
**TOP ROW:** `grid-cols-3` standard stat cards:
- "Total Entry Cost" → "$4K–$31.5K" (gold), badge "One-time"
- "Complexity Avoided" → "$120–360K" (teal), badge "Saved"
- "Registrations Needed" → "6" (teal), badge "Straightforward"

**BELOW:** Full-width TableCard with two-column comparison. Left = Required items (Check icon, teal), Right = Not Required items (X icon, zinc, line-through). CardHeader "Requirements Checklist" / "What Newport needs vs. what it skips".

---

### Slide 14: Our Recommendation — SPLIT

**Data:** `ROUTE_COMPARISON` from `strategy.js`
**LEFT:** ChartCard with side-by-side route comparison visual (two columns inside the card, or a grouped bar chart). CardHeader "Route Comparison" / "Free vs. paid market access".
**RIGHT:** 4 stacked compact tiles:
- "Free Route Cost" → "$0" (zinc-950), badge "No cost"
- "Paid Route Cost" → "$13K/yr" (gold), badge "★ Recommended"
- "Visibility Gap" → "2x" (gold), badge "↑ Critical"
- "Break-Even" → "1 Win" (teal), badge "Low bar"

---

### Slide 15: Key Questions — SPLIT

**Data:** `KEY_QUESTIONS` from `strategy.js`
**LEFT:** ChartCard with grouped question list and priority badges. CardHeader "Discussion Points" / "Key questions for Newport leadership".
**RIGHT:** 3 stacked compact tiles (question categories with count per category)

---

### Slide 16: B2B Fast Track — SPLIT

**Data:** `B2B_TARGETS` from `market.js`
**LEFT:** ChartCard with horizontal bar chart of 5 targets. GEO Group highlighted. CardHeader "B2B Target Revenue" / "Near-term commercial opportunities".
**RIGHT:** 3 stacked compact tiles:
- "Targets" → "5" (gold), badge "Qualified"
- "Sales Cycle" → "2–8 wks" (teal), badge "Fast"
- "Combined Revenue" → "$2M+" (teal), badge "Addressable"

---

### Slide 17: The Blueprint (Final) — SPLIT

**Data:** `RESPONSIBILITIES.partnership` from `strategy.js`
**LEFT:** ChartCard with two-column responsibilities card. Left column = Newport (teal accent), Right column = Still Mind (gold accent). Handshake icon center. CardHeader "Partnership Structure".
**RIGHT:** 4 stacked compact tiles (key partnership metrics)

---

### Section Divider Slides

No split layout. No stat cards. Just:
- Centered layout
- Title: `text-4xl font-semibold text-zinc-950`
- Subtitle: `text-base text-zinc-500`
- GoldLine centered (64px)
- BackgroundRing large, centered, 2% opacity

---

## 16. Quality Checklist

Before any slide is complete, verify ALL of these:

- [ ] **Split or Table layout**: SPLIT = visual LEFT + tiles RIGHT (default), TABLE = tiles top + table below (slides 10, 13 only)
- [ ] **Split uses grid-cols-5**: visual `col-span-3` LEFT, tiles `col-span-2` RIGHT stacked vertically
- [ ] **StatCard density**: Every stat card has: muted label, big number, trend badge (top-right), footer with border-t and 2 lines
- [ ] **ChartCard anatomy**: CardHeader (title + desc) → CardContent (chart) → CardFooter (border-t + legend)
- [ ] **Card surface**: ALL cards use `rounded-xl bg-white border border-zinc-200 shadow-sm`
- [ ] **Tile count**: 3 or 4 compact tiles stacked RIGHT (split), or 3–4 standard tiles horizontal TOP (table)
- [ ] **Two-accent rule**: Only gold `#C9A84C` and teal `#1B7A8A` as accent colors
- [ ] **Data from imports**: Numbers from `market.js`, `strategy.js`, or `financials.js`
- [ ] **Typography scale**: No mushy middle sizes. Use the exact classes from section 8.2.
- [ ] **Source citation**: Every data slide has a source line
- [ ] **Animation budget**: Under 1.5 seconds total
- [ ] **Container pattern**: Root div uses `justify-center px-16 lg:px-20 pb-16`
- [ ] **Hover states**: All cards have `hover:shadow-md hover:border-zinc-300 transition-all duration-200`
- [ ] **Gold accent strip**: Hero ChartCard has `absolute left-0 ... bg-[#C9A84C]` + content `pl-8`
- [ ] **Chart tooltip radius**: `borderRadius: 8` + `extraCssText: 'box-shadow: ...'`
- [ ] **Table hover**: TableCard rows have `hover:bg-zinc-50` if present
- [ ] **New slides use Recharts**: Slides 6–17 use `recharts` (not ECharts) for standard charts

---

## 17. Component Reference

| Component | Import | Purpose |
|---|---|---|
| `GoldLine` | `../ui/DecorativeElements` | Animated gold divider |
| `CompassStar` | `../ui/DecorativeElements` | 4-pointed star |
| `BackgroundRing` | `../ui/DecorativeElements` | Circular decoration |
| `SourceCitation` | `../ui/SourceCitation` | Source line |
| `useCountUp` | `../../hooks/useCountUp` | Animated counter |
| `TrendingUp` | `lucide-react` | Trend badge icon |
| `TrendingDown` | `lucide-react` | Trend badge icon |

Data files: `src/data/market.js`, `src/data/strategy.js`, `src/data/financials.js`

---

*This system enforces the shadcn/ui dashboard-01 layout as the ONLY layout for data slides. The key structural rules: stat cards always in a horizontal row (grid-cols-3 or grid-cols-4), chart card always full-width below, every stat card has 5+ pieces of content (label, value, trend badge, footer highlight, footer description). No bento grids, no side-by-side chart+stats, no vertical stacking.*
