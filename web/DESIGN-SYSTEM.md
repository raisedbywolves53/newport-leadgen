# Newport Presentation Design System

> **Purpose**: Single source of truth for every visual decision in the Newport web presentation (slides 3–19). Written so an AI coding assistant can mechanically produce slides that meet Fortune 500 executive-presentation standards.
>
> **Slides 1–2 are EXCLUDED** from these guidelines. They have their own visual treatment.
>
> **Visual reference standard:** [shadcn/ui blocks](https://ui.shadcn.com/blocks) — dashboard layouts with charts inside cards, KPI stat tiles with trend indicators, clean data tables. Every data slide (6+) MUST include at least one chart or data visualization.

---

## 1. Design Philosophy

The presentation tells one story: *Newport is the right partner for government food procurement.* Every slide is a scene. The visual language is **quiet, confident, and editorial** — the way a shadcn/ui dashboard communicates data.

**Visual North Star: shadcn/ui Dashboard Aesthetic**

Study [shadcn/ui blocks](https://ui.shadcn.com/blocks). Key principles that apply to EVERY data slide (6+):

- **Charts live inside cards** — a donut, bar chart, or area chart sits inside a white card with a compact legend. Charts are never floating or unstyled.
- **KPI stat tiles** — small cards showing a big number, a label, and optionally a trend indicator. These sit alongside or below chart cards.
- **Data tables are clean** — minimal borders, alternating backgrounds, right-aligned numbers, no heavy styling. Tables live inside card surfaces.
- **Layout is grid-based** — typically 2 columns: one large chart card (60%) + stacked stat tiles (40%). Or full-width chart above + row of stat tiles below.
- **Every data slide MUST have at least one visual asset** — chart, data table, or styled metric tile. Pure text-card slides are forbidden for slides 6+.

**Four governing principles:**

1. **Unified surface** — Every slide reads as one cohesive dashboard panel, not a collection of independent elements. White space is a design element.
2. **Two-accent discipline** — Gold and teal carry all visual weight. No other hue appears in data, accents, or highlights.
3. **Let the data breathe** — If a number is important, give it size. If text is supporting, make it smaller and lighter. Never let two elements compete.
4. **Chart-first storytelling** — If a slide has quantitative data, show it as a chart FIRST, then support with stat cards. The chart is the hero; stat cards provide context.

---

## 2. Color System

### 2.1 Foundations

The color system follows a **hybrid approach**: shadcn-style neutral surfaces (clean whites, subtle zinc borders) with Newport's gold and teal as accent/data colors. This gives the polished modern feel of shadcn while maintaining brand identity.

**shadcn/ui reference values (OKLCH):**

| shadcn Token | OKLCH Value | Approximate Hex | Our Usage |
|---|---|---|---|
| `--background` | `oklch(1 0 0)` | `#ffffff` | Page/app background |
| `--foreground` | `oklch(0.145 0 0)` | `#0a0a0a` | Primary text |
| `--card` | `oklch(1 0 0)` | `#ffffff` | Card backgrounds |
| `--card-foreground` | `oklch(0.145 0 0)` | `#0a0a0a` | Card text |
| `--muted` | `oklch(0.97 0 0)` | `#f5f5f5` | Muted backgrounds |
| `--muted-foreground` | `oklch(0.556 0 0)` | `#737373` | Secondary text |
| `--border` | `oklch(0.922 0 0)` | `#e5e5e5` | Border color |
| `--radius` | `0.625rem` | `10px` | Base border-radius |

### 2.2 Slide Background

| Token | Value | Usage |
|---|---|---|
| `slide-bg` | `#f4f4f5` (zinc-100) | Slide canvas — applied by `SlideBackground`, never override |
| `app-chrome` | `#0F1A2E` (navy-950) | Password gate, HTML body only. Never on slide surfaces |

> **Change from previous**: Shifted from `#e6e6ec` to zinc-100 (`#f4f4f5`) to align with shadcn's neutral palette. This is warmer and more contemporary.

### 2.3 Text Hierarchy

| Role | Color | Tailwind | Notes |
|---|---|---|---|
| Primary headline | `#0a0a0a` | `text-zinc-950` | Near-black, maximum contrast |
| Secondary headline / card title | `#18181b` | `text-zinc-900` | Slightly lighter |
| Body text | `#52525b` | `text-zinc-600` | Comfortable reading weight |
| Caption / detail / footnote | `#a1a1aa` | `text-zinc-400` | Recedes clearly |
| Kicker / eyebrow label | `#a1a1aa` or `#1B7A8A` | `text-zinc-400` or `text-teal-500` | Uppercase, tracked |
| Source citation | `#d4d4d8` | `text-zinc-300` | Nearly invisible |

> **Change from previous**: Moved from custom `navy-800/XX` opacity values to standard zinc scale. This matches shadcn's text hierarchy exactly and eliminates the need for custom color definitions.

### 2.4 Accent Palette (strict — no exceptions)

| Role | Name | Hex | When to use |
|---|---|---|---|
| **Primary accent** | Gold | `#C9A84C` | Hero stats, accent strips, primary KPI values, chart emphasis, icon tints on lead cards |
| **Secondary accent** | Teal | `#1B7A8A` | Supporting KPI values, secondary data series, icon tints on supporting cards |
| **Tertiary (data only)** | Light teal | `#3CC0D4` | Third data series in multi-series charts ONLY |
| **Tertiary (data only)** | Amber | `#E8913A` | Fourth data series in multi-series charts ONLY, or a single highlight callout per slide |

### 2.5 Chart Colors

Aligned with shadcn's `--chart-*` token pattern:

| Series | Our Color | shadcn Equivalent |
|---|---|---|
| 1st (primary) | Gold `#C9A84C` | `--chart-1` |
| 2nd | Teal `#1B7A8A` | `--chart-2` |
| 3rd | Light teal `#3CC0D4` | `--chart-3` |
| 4th | Amber `#E8913A` | `--chart-4` |

### 2.6 Forbidden Colors

These **must not** appear as accents, borders, icon tints, or data colors on slides 3–19:

- Any red, green, purple, pink, or blue outside the accent palette
- Raw amber as a card border or background
- Any color at full opacity over large card-sized areas
- Gray tones outside the zinc scale

---

## 3. Card System

This is the biggest alignment change. Cards now follow shadcn's exact treatment.

### 3.1 Base Card Surface

```
rounded-xl bg-white border border-zinc-200 shadow-sm
```

**Key differences from previous system:**

| Property | Previous | shadcn-aligned |
|---|---|---|
| Border radius | `rounded-2xl` (16px) | `rounded-xl` (12px) |
| Background | `bg-white/70 backdrop-blur-sm` | `bg-white` (solid) |
| Border | `border-black/[0.06]` | `border-zinc-200` |
| Shadow | `shadow-[0_1px_3px_rgba(0,0,0,0.04)]` | `shadow-sm` |

> **Why**: shadcn uses solid white cards with a clear `border-zinc-200` border — no frosted glass, no backdrop blur, no custom shadow values. This is cleaner and renders more consistently.

### 3.2 Card Variants

| Variant | Classes | When |
|---|---|---|
| **Standard** | `rounded-xl bg-white border border-zinc-200 shadow-sm` | Default for all cards |
| **Hero** (1 per slide max) | Base + `relative overflow-hidden` with left gold accent strip: `absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]` | The single most important card on the slide |
| **Muted / stat tile** | `rounded-xl bg-zinc-50 border border-zinc-200` | Supporting KPI tiles |
| **Emphasized** | `rounded-xl bg-teal-50/50 border border-teal-200/50` | One secondary callout per slide, max |
| **Highlighted** | `rounded-xl bg-amber-50/50 border border-amber-200/50` | One per slide max, for a key insight |

**Rules:**

- Never more than **1 hero card** per slide
- Never more than **1 emphasized + 1 highlighted** card per slide
- If a slide has 4+ cards, they should ALL be standard — differentiate with accent-colored stat values, not card backgrounds
- No drop shadow heavier than `shadow-sm`

### 3.3 Card Padding

Following shadcn's Card component:

| Size | Padding | Usage |
|---|---|---|
| Default | `p-6` | Standard cards |
| Compact | `p-4` | Stat tiles, tight layouts |
| Hero | `p-6` to `p-8` | Hero cards with more breathing room |

> **Change from previous**: Standardized to `p-6` default (was `p-5`). shadcn's CardContent uses `p-6 pt-0` with `CardHeader` providing top padding.

### 3.4 Card Anatomy (shadcn pattern)

```
┌─────────────────────────────────────┐
│ CardHeader: p-6                     │
│   CardTitle: text-lg font-semibold  │
│   CardDescription: text-sm text-zinc-600 │
├─────────────────────────────────────│
│ CardContent: p-6 pt-0              │
│   [chart / stats / table content]  │
├─────────────────────────────────────│
│ CardFooter: p-6 pt-0 (optional)   │
│   [legend / actions / metadata]    │
└─────────────────────────────────────┘
```

When building chart cards:

- Title + description in the card header area
- Chart occupies the content area
- Legend sits in the footer area, separated by `border-t border-zinc-100`

---

## 4. Typography

### 4.1 Font Stack

| Role | Family | Weight | Tracking |
|---|---|---|---|
| **Display** | `Playfair Display` | — | — |
| **Body** | `Inter` | 400–700 | `tracking-tight` on stats, normal on body |

> shadcn uses `font-sans` which maps to the system font stack. We keep Inter as our explicit choice — it's close to Geist (shadcn's preferred font) and already installed.

### 4.2 Usage Rules

- **Playfair Display is used ONLY on slide 1 (title).** Slides 2–19 use `Inter` for everything.
- Headlines: `text-3xl font-semibold tracking-tight` (or `text-2xl` on dense slides)
- Kicker/eyebrow: `text-xs font-medium uppercase tracking-widest`
- Hero stat: `text-5xl md:text-6xl font-bold tracking-tighter leading-none`
- Card stat: `text-2xl font-semibold tracking-tight leading-none`
- Card title: `text-sm font-medium`
- Card description: `text-sm text-zinc-600`
- Card body: `text-sm leading-relaxed`
- Detail/caption: `text-xs text-zinc-400`
- Source line: `text-[10px] text-zinc-300`

> **Changes from previous**: Reduced headline weight from `font-bold` to `font-semibold` (shadcn convention). Reduced hero stat from 7xl to 6xl. Card stats from 3xl to 2xl. These are subtler, more restrained — the shadcn way.

### 4.3 Hierarchy Pattern (every slide follows this)

```
Eyebrow label (xs, uppercase, tracking-widest, teal or zinc-400)
Headline (2xl–3xl, semibold, zinc-950)
Subtitle (sm, zinc-600, max-w-2xl)
GoldLine (48px, animated)
—— content area ——
Source citation (10px, zinc-300, bottom of slide)
```

---

## 5. Layout System

### 5.1 Slide Container

Every slide's root `<div>`:

```
w-full h-full flex flex-col justify-center px-16 lg:px-20 pb-16 relative overflow-hidden
```

- `justify-center` vertically centers the content block
- `px-16 lg:px-20` gives generous horizontal margins
- `pb-16` ensures content clears the fixed navigation bar
- `relative overflow-hidden` enables decorative elements

> **CRITICAL**: Do NOT use `pt-6 pb-20` — this causes layout issues. The validated pattern is `justify-center` with horizontal padding.

### 5.2 Content Layouts

| Layout | Grid | Best for |
|---|---|---|
| **Dashboard: Chart + Stats** | `grid-cols-[3fr_2fr] gap-4` | 1 chart + 2–4 stat tiles (most common) |
| **Dashboard: Full-width Chart** | Full-width chart + `grid-cols-3 gap-4` stat row below | Chart hero + compact stats |
| **Dashboard: Chart + Table** | Chart top (50%) + table below (50%) | Visual summary + detailed breakdown |
| **Bento** | `grid-cols-2 grid-rows-3` with hero `row-span-2` | 1 hero metric + supporting stats |
| **Two-column** | `grid-cols-2 gap-4` | Side-by-side comparison |
| **Card grid** | `grid-cols-2 gap-4` | 4 equal-weight cards |
| **Table** | `grid-cols-[...explicit widths...]` | Data tables with row striping |
| **Process flow** | Flex row + grid below | Sequential steps |
| **Split narrative** | `grid-cols-[1fr_auto_1fr]` | Two-side comparison |

**Dashboard Layout Patterns (shadcn-style):**

**Pattern A — Chart + Stat Tiles (most common)**
```
┌─────────────────────────┬──────────────┐
│                         │  Stat Tile 1 │
│   Chart Card            │──────────────│
│   (ECharts inside       │  Stat Tile 2 │
│    white card)          │──────────────│
│                         │  Stat Tile 3 │
└─────────────────────────┴──────────────┘
```
Grid: `grid-cols-[3fr_2fr] gap-4`. Chart card = hero card (gold accent strip).

**Pattern B — Full-width Chart + Stat Row**
```
┌────────────────────────────────────────┐
│   Chart Card (ECharts)                 │
│   height: 260–320px                    │
└────────────────────────────────────────┘
┌──────────┬──────────┬──────────────────┐
│ Stat 1   │ Stat 2   │ Insight Card     │
└──────────┴──────────┴──────────────────┘
```

**Pattern C — Chart + Table**
```
┌─────────────────────┬──────────────────┐
│   Chart Card        │  Hero Stat Card  │
└─────────────────────┴──────────────────┘
┌────────────────────────────────────────┐
│   Table Card (full width)              │
└────────────────────────────────────────┘
```

### 5.3 Spacing Rules

| Context | Value | Notes |
|---|---|---|
| Gap between cards | `gap-4` (16px) | Standard. shadcn uses `gap-4` consistently |
| Header to content | `mb-3` after GoldLine | Tighter than before |
| Card internal padding | `p-6` standard, `p-4` compact | shadcn CardContent convention |
| Icon to text in cards | `gap-2` or `gap-3` | Compact |
| Slide horizontal padding | `px-16 lg:px-20` | Content never touches edges |

> **Change from previous**: Standardized to `gap-4` everywhere (was `gap-5`). shadcn uses tighter spacing consistently — `gap-4` (16px) is the standard gap between dashboard cards.

---

## 6. Visual Assets

### 6.1 KPI Tiles / Stat Cards

The **StatCard** is the primary visual unit. shadcn-style anatomy:

```
┌──────────────────────────────────┐
│ [Icon]  Label (xs, font-medium)  │  ← zinc-600 text
│                                  │
│  $87M  (2xl, semibold, accent)   │  ← gold or teal
│                                  │
│  +12% from last year (xs)        │  ← zinc-400, optional trend
└──────────────────────────────────┘
```

**Icon treatment:**

- Icon inside a `w-8 h-8 rounded-md` container with `bg-zinc-100` (or `bg-[accent]/10` for accent cards)
- Icon itself: `w-4 h-4` in zinc-600 (or accent color)
- `strokeWidth={1.5}`
- Use `lucide-react` icons only

> **Change from previous**: `rounded-md` instead of `rounded-lg`. `bg-zinc-100` default instead of always accent-tinted. This matches shadcn's subtler icon containers.

**Accent color rules for stat values:**

- The **single most important stat** on the slide gets gold (`#C9A84C`)
- All other stats use either `zinc-950` (dark, neutral) or teal (`#1B7A8A`)
- Never use amber or light teal for stat values in cards

**Hero stat (standalone):**

- `text-5xl md:text-6xl font-bold tracking-tighter`
- Gold accent color
- Maximum one per slide

### 6.2 Charts

**General chart rules:**

- Use ECharts with canvas renderer (modular imports)
- Chart backgrounds: `transparent` — the card provides the surface
- Grid lines: `#e5e5e5` (zinc-200) at 0.5 opacity, horizontal only
- Axis labels: Inter, 11px, `#71717a` (zinc-500)
- No chart borders or outlines
- Maximum 4 data series per chart
- Charts ALWAYS live inside a card surface
- Every chart card includes a compact legend below, separated by `border-t border-zinc-100`

**Color assignment for data series:**

| Series | Color | Opacity |
|---|---|---|
| 1st (primary) | Gold `#C9A84C` | 100% |
| 2nd | Teal `#1B7A8A` | 100% |
| 3rd | Light teal `#3CC0D4` | 100% |
| 4th | Amber `#E8913A` | 100% |

**Chart type guidance:**

| Data story | Chart type | Notes |
|---|---|---|
| Part-to-whole | Donut (not pie) | Max 4 segments. Center label. `radius: ['52%', '78%']` |
| Composition over time | Stacked bar | Horizontal axis = time |
| Ranking / comparison | Horizontal bar | Sorted descending. Single color |
| Trend | Line / Area | Gold primary, teal secondary. 8% opacity area fill |

**Chart sizing:**

- Charts take 50–60% of content area width
- Minimum height: 200px, recommended 240–300px
- Legend always below or beside (not overlaid)

**Tooltip styling (shadcn-aligned):**

```jsx
tooltip: {
  trigger: 'axis',
  backgroundColor: '#18181b',    // zinc-900
  borderColor: '#27272a',        // zinc-800
  borderWidth: 1,
  textStyle: {
    color: '#fafafa',            // zinc-50
    fontFamily: 'Inter, system-ui, sans-serif',
    fontSize: 12
  },
  padding: [8, 12],
}
```

> **Change from previous**: Tooltip background changed from `rgba(36,51,86,0.95)` to zinc-900. This matches shadcn's popover/tooltip aesthetic.

---

#### 6.2.1 ECharts Setup (required for every chart slide)

**Imports — always use modular imports:**

```jsx
import { useEffect, useRef } from 'react'
import * as echarts from 'echarts/core'
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([BarChart, GridComponent, TooltipComponent, CanvasRenderer])
```

**Chart lifecycle pattern:**

```jsx
const chartRef = useRef(null)

useEffect(() => {
  if (!chartRef.current) return
  const chart = echarts.init(chartRef.current, null, { renderer: 'canvas' })
  chart.setOption({ /* config */ })

  const handleResize = () => chart.resize()
  window.addEventListener('resize', handleResize)
  return () => {
    window.removeEventListener('resize', handleResize)
    chart.dispose()
  }
}, [])
```

**Chart container (inside a card):**

```jsx
<div ref={chartRef} className="w-full h-full" />
```

---

#### 6.2.2 Template: Donut Chart

**Use for:** Part-to-whole data

```jsx
import { PieChart } from 'echarts/charts'
import { GraphicComponent, TooltipComponent } from 'echarts/components'
echarts.use([PieChart, GraphicComponent, TooltipComponent, CanvasRenderer])

chart.setOption({
  backgroundColor: 'transparent',
  animation: false,
  tooltip: {
    trigger: 'item',
    backgroundColor: '#18181b',
    borderColor: '#27272a',
    borderWidth: 1,
    textStyle: { color: '#fafafa', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 12 },
    padding: [8, 12],
  },
  graphic: [{
    type: 'group', left: 'center', top: 'center',
    children: [
      { type: 'text', style: { text: '58%', textAlign: 'center', fill: '#C9A84C', fontSize: 32, fontWeight: 600, fontFamily: 'Inter, system-ui, sans-serif' } },
      { type: 'text', style: { text: 'Sole Source', textAlign: 'center', fill: '#71717a', fontSize: 12, fontFamily: 'Inter, system-ui, sans-serif' }, top: 26 },
    ],
  }],
  series: [{
    type: 'pie', radius: ['52%', '78%'], center: ['50%', '50%'],
    avoidLabelOverlap: false, label: { show: false }, labelLine: { show: false }, emphasis: { scale: false },
    data: [
      { value: 58, name: 'Sole Source', itemStyle: { color: '#C9A84C' } },
      { value: 42, name: 'Competitive', itemStyle: { color: '#e5e5e5' } },
    ],
  }],
})
```

> **Change**: Secondary donut slice color changed from `rgba(15,26,46,0.08)` to `#e5e5e5` (zinc-200) for better visibility on white cards.

**Hero chart card wrapper:**

```jsx
<motion.div
  initial={{ opacity: 0, y: 16 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, delay: 0.3 }}
  className="rounded-xl bg-white border border-zinc-200 shadow-sm p-6 relative overflow-hidden"
>
  {/* Gold accent strip */}
  <div className="absolute left-0 top-3 bottom-3 w-1 rounded-full bg-[#C9A84C]" />

  <div className="flex flex-col h-full">
    <div className="flex-1 min-h-0">
      <div ref={chartRef} className="w-full h-full" />
    </div>
    {/* Compact legend */}
    <div className="flex items-center gap-4 pt-3 mt-3 border-t border-zinc-100">
      <div className="flex items-center gap-1.5">
        <div className="w-2 h-2 rounded-full bg-[#C9A84C]" />
        <span className="text-xs text-zinc-500">Sole Source</span>
      </div>
      <div className="flex items-center gap-1.5">
        <div className="w-2 h-2 rounded-full bg-zinc-200" />
        <span className="text-xs text-zinc-500">Competitive</span>
      </div>
    </div>
  </div>
</motion.div>
```

---

#### 6.2.3 Template: Horizontal Bar Chart

**Use for:** Rankings, comparisons

```jsx
import { BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent } from 'echarts/components'
echarts.use([BarChart, GridComponent, TooltipComponent, CanvasRenderer])

chart.setOption({
  backgroundColor: 'transparent',
  animation: false,
  tooltip: {
    trigger: 'axis', axisPointer: { type: 'shadow' },
    backgroundColor: '#18181b', borderColor: '#27272a', borderWidth: 1,
    textStyle: { color: '#fafafa', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 12 },
    padding: [8, 12],
  },
  grid: { left: 16, right: 90, top: 16, bottom: 16, containLabel: true },
  xAxis: { type: 'value', show: false, splitLine: { show: false } },
  yAxis: {
    type: 'category',
    data: REVERSED_DATA.map(d => d.label),
    axisLine: { show: false }, axisTick: { show: false },
    splitLine: { show: true, lineStyle: { color: '#e5e5e5', opacity: 0.3, type: 'dashed' } },
    axisLabel: { fontSize: 12, fontFamily: 'Inter, system-ui, sans-serif', color: '#18181b' },
  },
  series: [{
    type: 'bar',
    data: REVERSED_DATA.map(d => ({
      value: d.amount,
      itemStyle: { color: d.isPrimary ? '#C9A84C' : 'rgba(27,122,138,0.70)', borderRadius: [0, 4, 4, 0] },
    })),
    barWidth: 18,
    label: {
      show: true, position: 'right', fontSize: 11,
      fontFamily: 'Inter, system-ui, sans-serif', fontWeight: 600, color: '#71717a',
      formatter: (p) => formatCurrency(p.value),
    },
  }],
})
```

---

#### 6.2.4 Template: Area/Line Chart

**Use for:** Trends, growth projections

```jsx
import { LineChart } from 'echarts/charts'
echarts.use([LineChart, GridComponent, TooltipComponent, CanvasRenderer])

chart.setOption({
  backgroundColor: 'transparent',
  animation: false,
  tooltip: { trigger: 'axis', backgroundColor: '#18181b', borderColor: '#27272a', borderWidth: 1,
    textStyle: { color: '#fafafa', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 12 }, padding: [8, 12] },
  grid: { left: 60, right: 20, top: 20, bottom: 40, containLabel: false },
  xAxis: {
    type: 'category', data: ['Y1', 'Y2', 'Y3', 'Y4', 'Y5'],
    axisLine: { lineStyle: { color: '#e5e5e5' } }, axisTick: { show: false },
    axisLabel: { fontSize: 11, fontFamily: 'Inter, system-ui, sans-serif', color: '#71717a' },
  },
  yAxis: {
    type: 'value', axisLine: { show: false }, axisTick: { show: false },
    splitLine: { lineStyle: { color: '#e5e5e5', opacity: 0.5 } },
    axisLabel: { fontSize: 11, fontFamily: 'Inter, system-ui, sans-serif', color: '#71717a' },
  },
  series: [{
    type: 'line', data: [10, 25, 45, 65, 78],
    smooth: true, symbol: 'circle', symbolSize: 6,
    lineStyle: { color: '#C9A84C', width: 2 },
    itemStyle: { color: '#C9A84C', borderColor: '#fff', borderWidth: 2 },
    areaStyle: { color: 'rgba(201,168,76,0.08)' },
  }],
})
```

---

#### 6.2.5 Template: Stacked Bar Chart (Vertical)

**Use for:** Composition over time

```jsx
chart.setOption({
  backgroundColor: 'transparent',
  animation: false,
  tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' },
    backgroundColor: '#18181b', borderColor: '#27272a', borderWidth: 1,
    textStyle: { color: '#fafafa', fontFamily: 'Inter, system-ui, sans-serif', fontSize: 12 }, padding: [8, 12] },
  grid: { left: 60, right: 20, top: 20, bottom: 40 },
  xAxis: {
    type: 'category', data: ['Y1', 'Y2', 'Y3', 'Y4', 'Y5'],
    axisLine: { lineStyle: { color: '#e5e5e5' } }, axisTick: { show: false },
    axisLabel: { fontSize: 11, fontFamily: 'Inter, system-ui, sans-serif', color: '#71717a' },
  },
  yAxis: {
    type: 'value',
    splitLine: { lineStyle: { color: '#e5e5e5', opacity: 0.5 } },
    axisLabel: { fontSize: 11, fontFamily: 'Inter, system-ui, sans-serif', color: '#71717a' },
  },
  series: [
    { name: 'Micro', type: 'bar', stack: 'total', data: [5, 12, 18, 22, 25], itemStyle: { color: '#C9A84C' }, barWidth: 28 },
    { name: 'Simplified', type: 'bar', stack: 'total', data: [0, 3, 8, 15, 22], itemStyle: { color: '#1B7A8A' } },
    { name: 'Larger', type: 'bar', stack: 'total', data: [0, 0, 3, 8, 16], itemStyle: { color: '#3CC0D4' } },
    { name: 'Renewed', type: 'bar', stack: 'total', data: [0, 0, 2, 8, 15], itemStyle: { color: '#E8913A' } },
  ],
})
```

---

### 6.3 Tables

**Table styling (shadcn-aligned):**

```
Header row: text-xs font-medium text-zinc-500 uppercase tracking-wider
            border-b border-zinc-200 pb-3
Data rows:  text-sm text-zinc-700
            Even rows: bg-zinc-50/50
            Odd rows: bg-transparent
            Row padding: py-3 px-4
```

- Use CSS Grid for table layout (not `<table>`) — allows precise column widths
- First column left-aligned, number columns right-aligned
- Currency values: `font-medium`, accent-colored (gold for highest, teal for others)
- No row hover (presentation, not app)

> **Change from previous**: Header changed from `text-[11px]` to `text-xs`. Row background from `bg-white/40` to `bg-zinc-50/50`. Border color from `border-black/[0.08]` to `border-zinc-200`.

**Badge system for categorical data:**

| Category | Style |
|---|---|
| Highest priority | `bg-amber-50 text-amber-700 border border-amber-200/50 rounded-md px-2 py-0.5 text-xs font-medium` |
| High / good | `bg-teal-50 text-teal-700 border border-teal-200/50 rounded-md px-2 py-0.5 text-xs font-medium` |
| Moderate | `bg-zinc-100 text-zinc-600 rounded-md px-2 py-0.5 text-xs font-medium` |
| Low / avoid | `bg-zinc-50 text-zinc-400 rounded-md px-2 py-0.5 text-xs font-medium line-through` |

> **Change from previous**: Badges changed from `rounded-full px-3` (pill) to `rounded-md px-2` (rounded rectangle). This matches shadcn's Badge component styling exactly.

### 6.4 Process Flows / Pipelines

- Horizontal flex row with icon badges connected by subtle connectors
- Badge: `w-10 h-10 rounded-lg bg-zinc-100` with icon centered (or accent bg at 10% for highlighted steps)
- Connector: `ChevronRight` icon at `text-zinc-300` between badges
- Label below: `text-xs font-medium text-zinc-900`
- Sub-label: `text-[10px] text-zinc-400`
- Maximum 5 stages per pipeline row

> **Change from previous**: Badge shape from `rounded-full` to `rounded-lg`. Background from accent at 15% to `bg-zinc-100` default. Connector icon changed to ChevronRight.

### 6.5 Decorative Elements

Use sparingly — decoration should never compete with data.

| Element | Component | Placement | Frequency |
|---|---|---|---|
| Gold line | `GoldLine` | Below subtitle, before content | Every slide |
| Compass star | `CompassStar` | Bottom-right, next to source | 1 in 3 slides max |
| Background ring | `BackgroundRing` | Corner, half off-screen | Max 1 per slide |

- Background rings: `opacity-[0.02]`, gold color
- CompassStar: `opacity-20`, size 14px
- GoldLine: 48px wide, gold `#C9A84C`

---

## 7. Animation System

All animations use `motion/react` (Framer Motion).

### 7.1 Standard Patterns

| Element | Initial | Animate | Duration | Delay |
|---|---|---|---|---|
| Headline | `opacity: 0, y: 8` | `opacity: 1, y: 0` | 0.35s | 0.1s |
| Subtitle | `opacity: 0` | `opacity: 1` | 0.35s | 0.2s |
| GoldLine | `width: 0` | `width: target` | 0.6s | 0.25s |
| Cards (staggered) | `opacity: 0, y: 12` | `opacity: 1, y: 0` | 0.4s | 0.35 + i × 0.08 |
| Hero stat / chart | `opacity: 0, scale: 0.97` | `opacity: 1, scale: 1` | 0.5s | 0.3s |
| Source citation | `opacity: 0` | `opacity: 1` | 0.35s | last |

> **Changes from previous**: Reduced all animation distances (`y: 12` → `y: 8`, scale `0.95` → `0.97`). Shortened durations. shadcn animations are subtle and quick — they communicate responsiveness, not drama.

### 7.2 Rules

- Total animation sequence per slide: **under 1.5 seconds**
- Header always animates first
- Content follows header
- Source citation last
- `useCountUp` hook for stats: `duration: 1000, delay: 500 + index * 150`
- Never animate decorative elements with attention-grabbing motion

---

## 8. Slide-by-Slide Instructions

> **Legend:**
> Layout = CSS Grid / Flex structure
> Hero = single most prominent visual element
> Cards = StatCard-style tiles
> Source = bottom-line citation

---

### Slides 3–5: LOCKED — Do Not Modify

Slides 3 (WhyNewportSlide), 4 (FloridaTamSlide), and 5 (ProductMatrixSlide) are approved and locked. Study their patterns but do not modify.

---

### Slide 6: The Confectionery Gap

**Content:** PSC 8925 deep dive — Newport's Segment E advantage
**Data source:** `PRODUCT_TIERS.tier1[0]` from `market.js`
**Layout:** Dashboard Pattern A — Chart + Stat Tiles (`grid-cols-[3fr_2fr] gap-4`)
**Required visual:** ECharts donut chart (Template 6.2.2)

**Structure:**
- Eyebrow: "Category Deep Dive" (zinc-400)
- Headline: "The Confectionery Gap" (3xl)
- Subtitle + GoldLine
- **Left (3fr):** Hero chart card — donut: 58% sole-source (gold) vs 42% competitive (zinc-200). Center label: "58%" gold 32px semibold. Chart height ~240px. Hero card with gold accent strip.
- **Right (2fr):** 3 stat tiles stacked (`gap-3`):
  - `$55M` (gold) + "National Spend"
  - `45` (teal) + "National Awards"
  - `1.6` (teal) + "Avg Offers per Award"
- Source: "FPDS FY2024, PSC 8925"

---

### Slide 7: Competition Landscape

**Content:** Top 8 FL food distributors
**Data source:** `COMPETITORS` from `market.js`
**Layout:** Dashboard Pattern C
**Required visual:** Horizontal bar chart (Template 6.2.3)

**Structure:**
- Eyebrow + Headline + GoldLine
- **Top:** `grid-cols-[3fr_2fr] gap-4` — chart card (hero) + stat card ("$26.1M" gold, "$1–5M" teal entry tier)
- **Bottom:** Full-width table card. 8 rows, alternating `bg-zinc-50/50`. Newport callout row: `bg-teal-50/50`
- Source

---

### Slide 8: How It Works (Pipeline)

**Content:** 5-stage pipeline + 4 sourcing channels
**Data source:** `PIPELINE_STAGES`, `SOURCING_CHANNELS` from `strategy.js`
**Layout:** Process flow + card grid

**Structure:**
- Eyebrow + Headline + GoldLine
- **Pipeline row:** 5 badges in hero card, connected by chevrons
- **Channels:** `grid-cols-4 gap-3`, standard cards with top accent bar (2px)
- Source

---

### Slide 9: Target Agencies

**Content:** 4 priority targets
**Data source:** `TARGET_AGENCIES` from `market.js`
**Layout:** Dashboard Pattern A
**Required visual:** Horizontal bar chart

**Structure:**
- Left: Hero chart card — 4 agencies by value
- Right: 4 stat tiles (DOJ gold, others teal)
- Source

---

### Slide 10: Real Contracts

**Content:** 8 contract examples
**Data source:** `CONTRACT_EXAMPLES` from `strategy.js`
**Layout:** Dashboard Pattern C — stat row + table

**Structure:**
- 3 compact stat tiles: "8" opportunities, "$155K+" value, "75%" high fit
- Full-width table with badge system
- Source

---

### Slide 11: Portfolio Evolution

**Content:** 5-year stacked bar
**Data source:** Projection data (hardcoded)
**Layout:** Dashboard Pattern A
**Required visual:** Stacked bar (Template 6.2.5)

**Structure:**
- Left: Hero chart card — 4-series stacked bars Y1–Y5
- Right: 3 stat tiles ("78" contracts gold, "70%" renewal teal, "$1.2M" revenue teal)
- Source

---

### Slide 12: Relationship Strategy

**Content:** 3 influence layers + 5-step process
**Layout:** Two-column (`grid-cols-2 gap-4`)

**Structure:**
- Left: 3 stacked cards with chevron connectors. Card 3 (Front-Line) gets gold accent
- Right: Numbered vertical timeline (5 steps) inside a card
- Insight callout card (full width, emphasized)
- Source

---

### Slide 13: Risk & Compliance

**Content:** $4K entry cost vs. $360K avoided
**Data source:** `COMPLIANCE_REQUIRED`, `COMPLIANCE_NOT_NEEDED` from `strategy.js`
**Layout:** Dashboard — stat row + two-column comparison

**Structure:**
- 2 hero stat cards: "$4K" (teal) vs "$120–360K" (gold)
- Two-column: "Required" (teal) vs "Not Required" (gold, line-through)
- Source

---

### Slide 14: Our Recommendation

**Content:** Free vs. Paid route comparison
**Data source:** `ROUTE_COMPARISON` from `strategy.js`
**Layout:** Two recommendation cards + comparison table

**Structure:**
- Left card (Free): standard, muted. "$0", "40–50%" visibility
- Right card (Paid): hero card, gold accent. "$13K/yr", "90%+", "Recommended" badge
- Comparison table below
- Source

---

### Slide 15: Key Questions

**Content:** 10 decision questions
**Data source:** `KEY_QUESTIONS` from `strategy.js`
**Layout:** Category groups

**Structure:**
- 3 category cards, each containing questions as rows (not individual cards)
- Priority badges per question
- Decorative "10" watermark
- Source

---

### Slide 16: B2B Fast Track

**Content:** 5 institutional buyer targets
**Data source:** `B2B_TARGETS` from `market.js`
**Layout:** Dashboard Pattern C
**Required visual:** Horizontal bar chart

**Structure:**
- Top: chart card + stat card ("2–8 weeks" gold)
- Table: 5 targets, GEO Group highlighted
- Source

---

### Slide 17: The Blueprint (Final)

**Content:** Partnership responsibilities
**Data source:** `RESPONSIBILITIES.partnership` from `strategy.js`
**Layout:** Split narrative (`grid-cols-[1fr_auto_1fr]`)

**Structure:**
- Left panel: Newport (teal accent strip)
- Center: Vertical gradient connector with Handshake icon
- Right panel: Still Mind (gold accent strip)
- Source

---

### Divider Slides

**Layout:** Centered, minimal

**Structure:**
- Section title: `text-4xl font-semibold text-zinc-950` centered
- Subtitle: `text-base text-zinc-500` centered
- GoldLine centered (64px)
- BackgroundRing large, centered, 2% opacity
- No cards, no data

---

## 9. Quality Checklist

Before any slide is complete:

- [ ] **Visual asset present**: Every data slide (6+) has a chart, table, or styled metric
- [ ] **Two-accent rule**: Only gold and teal as accent colors
- [ ] **One hero**: Max one hero card or stat per slide
- [ ] **Card DNA**: All cards use `rounded-xl bg-white border border-zinc-200 shadow-sm` or an approved variant
- [ ] **Chart inside card**: ECharts visualizations sit inside card surfaces with compact legend below
- [ ] **Data from imports**: Quantitative data from `market.js` or `strategy.js`
- [ ] **Typography scale**: Headlines 2xl–3xl, card stats 2xl, hero stats 5xl–6xl. No mushy middle
- [ ] **Breathing room**: Minimum `px-16` horizontal. Cards have `p-4` to `p-6` internal padding
- [ ] **Container pattern**: Root div uses `justify-center px-16 lg:px-20 pb-16`
- [ ] **Source citation**: Every data slide has a source line
- [ ] **Animation budget**: Under 1.5 seconds total
- [ ] **No competing weight**: Squint test — one element dominates
- [ ] **Consistent with slides 3–5**: Same card DNA, same accent discipline
- [ ] **shadcn aesthetic**: Looks like a shadcn/ui dashboard panel

---

## 10. Component Reference

| Component | Import | Purpose |
|---|---|---|
| `GoldLine` | `../ui/DecorativeElements` | Animated gold divider after subtitles |
| `CompassStar` | `../ui/DecorativeElements` | 4-pointed decorative star |
| `HeroStat` | `../ui/DecorativeElements` | Oversized metric display |
| `BackgroundRing` | `../ui/DecorativeElements` | Subtle circular decoration |
| `SourceCitation` | `../ui/SourceCitation` | Bottom-of-slide source line |
| `useCountUp` | `../../hooks/useCountUp` | Animated number counter |

All slide data lives in `/src/data/market.js` and `/src/data/strategy.js`.

---

## Appendix: Migration Summary

Key changes from the previous design system to align with shadcn/ui:

| Area | Previous | shadcn-aligned |
|---|---|---|
| Card radius | `rounded-2xl` (16px) | `rounded-xl` (12px) |
| Card bg | `bg-white/70 backdrop-blur-sm` | `bg-white` (solid) |
| Card border | `border-black/[0.06]` | `border-zinc-200` |
| Card shadow | Custom `rgba(0,0,0,0.04)` | `shadow-sm` |
| Card padding | `p-5` | `p-6` (standard), `p-4` (compact) |
| Grid gap | `gap-5` | `gap-4` |
| Slide bg | `#e6e6ec` | `#f4f4f5` (zinc-100) |
| Text colors | `navy-800/XX` opacity system | Zinc scale (950/900/600/400/300) |
| Headline weight | `font-bold` | `font-semibold` |
| Hero stat size | `text-7xl` | `text-6xl` |
| Card stat size | `text-3xl` | `text-2xl` |
| Badge shape | `rounded-full` (pill) | `rounded-md` (rect) |
| Icon container | `rounded-lg` accent bg | `rounded-md` zinc-100 bg |
| Tooltip bg | Navy `rgba(36,51,86,0.95)` | `#18181b` (zinc-900) |
| Donut secondary | `rgba(15,26,46,0.08)` | `#e5e5e5` (zinc-200) |
| Animation distance | `y: 16–20` | `y: 8–12` |
| Animation budget | 2 seconds | 1.5 seconds |
| Process badge | `rounded-full` | `rounded-lg` |

---

*This system fuses shadcn/ui's clean, component-driven aesthetic with Newport's gold-and-teal brand identity. Follow it precisely — every rule exists to maintain the quiet confidence of a well-designed dashboard.*
