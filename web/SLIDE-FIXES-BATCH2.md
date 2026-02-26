# Slide Fixes — Batch 2 (Slides 6, 7, 8) — REVISED

> **Context**: Newport Wholesalers government contracting pitch deck. React + Vite + Tailwind + Framer Motion + ECharts. Project at `web/`.
> **Design system**: `web/DESIGN-SYSTEM.md` governs all visual decisions.
> **Quality reference**: Read `src/components/slides/WhyNewportSlide.jsx` (slide 3) — match its card DNA, spacing, typography scale, and animation patterns in every slide you build.
> **Also reference**: `src/components/slides/ProductMatrixSlide.jsx` (slide 5) for chart card + insight card pattern.

> **Slide numbering** (from `src/data/slides.js` — the ACTUAL app order):
> 1=Title, 2=ExecSummary, 3=WhyNewport, 4=FloridaTam, 5=ProductMatrix, **6=ConfectioneryGap**, **7=TargetAgencies**, **8=Competition**, 9=B2bFastTrack, 10=divider, 11=HowItWorks …

---

## CRITICAL RULES

1. Read `DESIGN-SYSTEM.md` before writing any code.
2. Read `WhyNewportSlide.jsx` (slide 3) as quality reference — match its patterns exactly.
3. Only gold (`#C9A84C`) and teal (`#1B7A8A`) as accent colors. No amber, no other hues.
4. Card surface: `rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)]`
5. Hero card surface: `bg-white` (full opacity) + left gold accent strip + slightly heavier shadow `shadow-[0_2px_8px_rgba(0,0,0,0.06)]`
6. Slide container: `w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden`
7. Import data from `../../data/market.js` / `../../data/strategy.js`. Never hardcode data that exists there.
8. Import shared components from `../ui/DecorativeElements`: `GoldLine`, `CompassStar`, `BackgroundRing`.
9. Typography: Inter for everything. Hero stat = `text-7xl font-bold tracking-tighter`. Card stat = `text-3xl font-bold tracking-tight`. Body = `text-sm leading-relaxed`.
10. ALL content is **left-aligned** unless specifically noted otherwise. Tables: header text centered, data cells left-aligned (numbers right-aligned).
11. After changes, verify build: `./node_modules/.bin/vite build --outDir /tmp/newport-build`

---

## NARRATIVE CONTEXT

The deck builds momentum through slides 1-5:
- Slides 1-2: The hook (here's a big opportunity)
- Slide 3: Why YOU win (credibility + timing)
- Slide 4: How big ($87M TAM, 5 channels)
- Slide 5: Which products (tier prioritization, confectionery + produce = Tier 1)

**Slides 6-8 must continue building forward momentum:**
- Slide 6: "Here's your easiest first win" (beachhead entry point)
- Slide 7: "Here are your first customers" (who to call Monday morning)
- Slide 8: "Here's why you beat your peers" (competitive positioning)

Each slide must make ONE argument the viewer processes in 3 seconds.

---

## Fix 1: Slide 6 — ConfectioneryGapSlide.jsx

**File**: `src/components/slides/ConfectioneryGapSlide.jsx`

### Narrative reframe

**OLD framing**: "The Confectionery Gap" — shows what's missing, feels negative
**NEW framing**: "Your First Win" — shows why this category is a layup

### What to change

**Title and copy updates:**
- Eyebrow: `"Beachhead Category"` (not "Category Deep Dive")
- Headline: `"Your First Win: Confectionery"` (not "The Confectionery Gap")
- Subtitle: `"The lowest-competition category in government food — and you already have the suppliers."` (not the current PSC-heavy copy)

### Layout: Bento grid — matching slide 3's pattern

Use slide 3's proven bento layout: `grid-cols-[1fr_1fr] grid-rows-[1fr_1fr_1fr]` with `height: '460px'`.

**Remove entirely:**
- The stacked bar chart card (the 2.5% gold sliver visual)
- The three bottom stat-story cards
- All `useCountUp` imports and usage (simplify)

**Replace with:**

#### Hero card (left column, row-span-2) — "The Opportunity"

Model this EXACTLY on slide 3's `HeroCard` component. Same structure, same spacing:

```jsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5, delay: 0.3 }}
  className="row-span-2 rounded-2xl bg-white p-10 shadow-[0_2px_8px_rgba(0,0,0,0.06)] border border-black/[0.04] flex flex-col justify-center relative overflow-hidden"
>
  {/* Gold accent strip — matches slide 3 exactly */}
  <div className="absolute left-0 top-8 bottom-8 w-1 rounded-full" style={{ backgroundColor: '#C9A84C' }} />

  <div className="pl-4">
    {/* Icon pill */}
    <div
      className="w-12 h-12 rounded-xl flex items-center justify-center mb-6"
      style={{ backgroundColor: '#C9A84C15' }}
    >
      <Star className="w-6 h-6" style={{ color: '#C9A84C' }} strokeWidth={1.8} />
    </div>

    {/* Hero stat */}
    <div className="flex items-baseline gap-3 mb-2">
      <span className="font-body text-7xl font-bold tracking-tighter leading-none" style={{ color: '#C9A84C' }}>
        58%
      </span>
      <span className="font-body text-lg font-medium text-navy-800/35 uppercase tracking-wide">
        Sole Source
      </span>
    </div>

    {/* Headline */}
    <h3 className="font-body text-xl font-semibold text-navy-950 mt-4 mb-3">
      Virtually No Competition
    </h3>

    {/* Detail */}
    <p className="font-body text-[15px] leading-relaxed text-navy-800/70">
      PSC 8925 has the lowest vendor competition of any food category. Average 1.6 offers per award — most contracts go to the only bidder. Newport's Segment E pricing wins on day one.
    </p>

    {/* Footer — matches slide 3's "Since 1996 · Plantation, FL" pattern */}
    <div className="flex items-center gap-2 mt-5 pt-5 border-t border-black/[0.06]">
      <span className="font-body text-xs font-medium text-navy-800/45">PSC 8925</span>
      <span className="text-navy-800/25">·</span>
      <span className="font-body text-xs font-medium text-navy-800/45">Confectionery & Nuts</span>
    </div>
  </div>
</motion.div>
```

Import `Star` from `lucide-react`.

#### Three StatCards (right column, stacked) — supporting the argument

Model these EXACTLY on slide 3's `StatCard` component. Same layout, same spacing.

**Card 1 — The Market Size:**
- Icon: `DollarSign` from lucide-react, teal pill
- Stat: `$55M` in teal, text-3xl bold
- Unit: `National` (text-[11px] uppercase)
- Headline: `"Massive, Underserved Market"` (text-base semibold)
- Detail: `"Only $412K currently captured in Florida — 99% of national spend is untouched by regional distributors."` (text-sm)

**Card 2 — The Newport Advantage:**
- Icon: `Package` from lucide-react, gold pill
- Stat: `Segment E` in gold, text-3xl bold
- Unit: `Core Line` (text-[11px] uppercase)
- Headline: `"Existing Supplier Pricing"` (text-base semibold)
- Detail: `"Newport already wholesales confectionery at scale. Same products, same logistics — different buyer."` (text-sm)

**Card 3 — The Evaluation Method:**
- Icon: `Scale` from lucide-react, teal pill
- Stat: `LPTA` in navy-950, text-3xl bold
- Unit: `Method` (text-[11px] uppercase)
- Headline: `"Lowest Price Wins"` (text-base semibold)
- Detail: `"Government uses Lowest Price Technically Acceptable — directly rewards wholesale volume pricing."` (text-sm)

Each StatCard follows slide 3's pattern exactly:
```jsx
<motion.div
  initial={{ opacity: 0, y: 16 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.45, delay: 0.4 + index * 0.1 }}
  className="rounded-2xl bg-white/70 backdrop-blur-sm p-6 shadow-[0_1px_3px_rgba(0,0,0,0.04)] border border-black/[0.06] flex flex-col justify-center"
>
  <div className="flex items-start gap-4">
    <div
      className="w-9 h-9 rounded-lg flex items-center justify-center shrink-0"
      style={{ backgroundColor: `${accent}15` }}
    >
      <Icon className="w-5 h-5" style={{ color: accent }} strokeWidth={1.5} />
    </div>
    <div className="flex-1">
      <div className="flex items-baseline gap-2 mb-1">
        <span
          className="font-body text-3xl font-bold tracking-tight leading-none"
          style={{ color: accent }}
        >
          {stat}
        </span>
        <span className="font-body text-[11px] font-medium text-navy-800/40 uppercase tracking-wide">
          {unit}
        </span>
      </div>
      <h3 className="font-body text-base font-semibold text-navy-950 mb-1.5">
        {headline}
      </h3>
      <p className="font-body text-sm leading-relaxed text-navy-800/65">
        {detail}
      </p>
    </div>
  </div>
</motion.div>
```

#### Source + CompassStar — matching slide 3's pattern

```jsx
<div className="flex items-center justify-between mt-4 relative z-10">
  <motion.p
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ delay: 1.0 }}
    className="text-[10px] text-navy-800/35"
  >
    FPDS FY2024, PSC 8925 | USASpending FL awards | FAR 15.101-2 (LPTA)
  </motion.p>
  <CompassStar size={16} opacity={0.2} delay={1.2} />
</div>
```

#### Imports needed

```jsx
import { motion } from 'motion/react'
import { Star, DollarSign, Package, Scale } from 'lucide-react'
import { GoldLine, CompassStar, BackgroundRing } from '../ui/DecorativeElements'
```

Remove: `useCountUp` import, all ECharts-related imports if any remain.

#### Background decorative elements — matching slide 3

```jsx
<BackgroundRing size={500} className="-top-40 -right-40" opacity={0.03} />
<BackgroundRing size={300} className="bottom-20 -right-20" opacity={0.025} />
```

---

## Fix 2: Slide 7 — TargetAgenciesSlide.jsx

**File**: `src/components/slides/TargetAgenciesSlide.jsx`

### Narrative reframe

**OLD**: Flat 2x2 grid where all agencies look equally important
**NEW**: Hero treatment for primary targets (DOJ, Military) + supporting cards for secondary (FEMA, Schools)

The owner should look at this slide and think: "I know exactly who to call first."

### What to change

**Copy updates:**
- Eyebrow: keep `"Procurement Channels"`
- Headline: `"Your First Customers"` (not "Who's Buying: Target Agencies")
- Subtitle: `"Ranked by contract value and accessibility — your first calls."` (not the current generic copy)

### Layout: Hero row (2 cards) + Supporting row (2 cards)

Replace the current uniform 2x2 grid with a visually hierarchical layout.

**Top row — Primary targets (DOJ + Military):** These have hard dollar data. Larger cards with more prominence.

Use a `grid-cols-2 gap-4` row, but these cards get MORE padding, LARGER stats, and a different visual weight than the bottom row.

**Primary card structure** (DOJ/BOP and Military):
```jsx
<motion.div
  initial={{ opacity: 0, y: 16 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.45, delay: 0.3 + i * 0.1 }}
  className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] p-6 relative overflow-hidden"
>
  {/* Left accent strip */}
  <div
    className="absolute left-0 top-3 bottom-3 w-[3px] rounded-full"
    style={{ backgroundColor: accent }}
  />
  <div className="flex items-start gap-4 pl-2">
    <div
      className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
      style={{ backgroundColor: `${accent}15` }}
    >
      <Icon className="w-5 h-5" style={{ color: accent }} strokeWidth={1.5} />
    </div>
    <div className="flex-1">
      <h3 className="font-body text-lg font-semibold text-navy-950">{agency.name}</h3>
      <span className="font-body text-2xl font-bold block mt-1" style={{ color: accent }}>
        {agency.stat}
      </span>
      <p className="font-body text-sm text-navy-800/60 leading-relaxed mt-2">
        {agency.description}
      </p>
    </div>
  </div>
</motion.div>
```

Note the differences from the current uniform cards:
- `p-6` (not `p-5`) — more breathing room
- `w-10 h-10` icon pill (not `w-9 h-9`) — slightly larger
- `text-lg` agency name (not `text-base`)
- `text-2xl` stat (not `text-xl`)
- `gap-4` (not `gap-3`)

The first card (DOJ/BOP, index 0) gets **gold** accent. The second (Military, index 1) also gets **teal** accent.

**Bottom row — Secondary targets (FEMA + Schools):** These have speculative data ("Disaster-driven", "$500M-$1B FL"). Smaller, more compact cards to visually communicate lower certainty.

**Secondary card structure:**
```jsx
<motion.div
  initial={{ opacity: 0, y: 16 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.45, delay: 0.5 + i * 0.1 }}
  className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] px-5 py-4 relative overflow-hidden"
>
  {/* Left accent strip — thinner for secondary */}
  <div
    className="absolute left-0 top-3 bottom-3 w-[2px] rounded-full"
    style={{ backgroundColor: accent, opacity: 0.5 }}
  />
  <div className="flex items-start gap-3 pl-2">
    <div
      className="w-8 h-8 rounded-lg flex items-center justify-center shrink-0"
      style={{ backgroundColor: `${accent}10` }}
    >
      <Icon className="w-4 h-4" style={{ color: accent }} strokeWidth={1.5} />
    </div>
    <div className="flex-1">
      <div className="flex items-baseline gap-2">
        <h3 className="font-body text-base font-semibold text-navy-950">{agency.name}</h3>
        <span className="font-body text-xs font-semibold uppercase tracking-wide" style={{ color: accent }}>
          {agency.stat}
        </span>
      </div>
      <p className="font-body text-[13px] text-navy-800/50 leading-relaxed mt-1.5">
        {agency.description}
      </p>
    </div>
  </div>
</motion.div>
```

Note the differences from primary cards:
- `px-5 py-4` (tighter padding)
- `w-8 h-8` icon pill (smaller)
- Stat is INLINE with the name at `text-xs` (not a separate big line) — because the stat isn't a hard dollar figure
- Description: `text-[13px]` and `text-navy-800/50` (more muted)
- Accent strip: `w-[2px]` and `opacity: 0.5` (thinner, subtler)

### Full layout structure:

```jsx
export default function TargetAgenciesSlide() {
  const primaryAgencies = TARGET_AGENCIES.slice(0, 2)  // DOJ, Military
  const secondaryAgencies = TARGET_AGENCIES.slice(2)     // FEMA, Schools

  return (
    <div className="w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden">
      <BackgroundRing size={450} className="-bottom-40 -left-40" opacity={0.02} />

      {/* Header */}
      <div className="mb-4 relative z-10">
        {/* ... eyebrow, headline, subtitle, GoldLine — same pattern as other slides ... */}
      </div>

      {/* Primary targets — larger cards */}
      <div className="grid grid-cols-2 gap-4 mb-4 relative z-10">
        {primaryAgencies.map((agency, i) => {
          const Icon = agencyIcons[i]
          const accent = agencyAccent(agency.color)
          return ( /* primary card JSX */ )
        })}
      </div>

      {/* Section label between rows */}
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.55 }}
        className="font-body text-[11px] font-semibold uppercase tracking-widest text-navy-800/30 mb-3 relative z-10"
      >
        Expansion Channels
      </motion.span>

      {/* Secondary targets — compact cards */}
      <div className="grid grid-cols-2 gap-4 relative z-10">
        {secondaryAgencies.map((agency, i) => {
          const Icon = agencyIcons[i + 2]
          const accent = agencyAccent(agency.color)
          return ( /* secondary card JSX */ )
        })}
      </div>

      {/* Source */}
      <div className="flex items-center justify-between mt-auto pt-4 relative z-10">
        {/* ... source + CompassStar ... */}
      </div>
    </div>
  )
}
```

The `mt-auto` on the source pushes it to the bottom, and the primary cards take up more visual space naturally.

### Keep from current file:
- `agencyAccent()` function (already correct)
- `agencyIcons` array
- All imports (already correct after linter update)

---

## Fix 3: Slide 8 — CompetitionSlide.jsx

**File**: `src/components/slides/CompetitionSlide.jsx`

### Narrative reframe

**OLD**: "Competition Landscape / Where Newport enters the ranking" — vague, no argument
**NEW**: "The Competitive Field" — Newport has more infrastructure than anyone in its tier

The owner should look at this and think: "I'm not fighting Oakes or US Foods — I'm competing against smaller players with less capability, and I can beat them."

### What to change

**Copy updates:**
- Eyebrow: keep `"Competitive Analysis"`
- Headline: `"The Competitive Field"` (not "Competition Landscape")
- Subtitle: `"The top is locked — but Newport enters with more infrastructure than anyone in the $1-5M tier."` (not "Where Newport enters the ranking")

### Remove the KPI tiles entirely

Delete the entire `<motion.div>` block containing the two centered KPI tiles ($26.1M and $1-5M). These numbers are already visible in the table and the user flagged them as redundant.

Also delete the centered context line ("8 tracked FL food distributors…").

### Table: the star of this slide

The table should fill the available space. Make it `flex-1` so it stretches.

### Table header — centered text, pronounced styling

Keep the current centered header approach (this was correct). But bump it up:

```jsx
<div
  className="grid grid-cols-[52px_1.4fr_140px_1fr] px-6 py-4 border-b-2 border-black/[0.10]"
  style={{ backgroundColor: 'rgba(15,26,46,0.05)' }}
>
  <span className="font-body text-xs font-bold uppercase tracking-wider text-navy-800/50 text-center">Rank</span>
  <span className="font-body text-xs font-bold uppercase tracking-wider text-navy-800/50 text-center">Company</span>
  <span className="font-body text-xs font-bold uppercase tracking-wider text-navy-800/50 text-center">FL Gov Awards</span>
  <span className="font-body text-xs font-bold uppercase tracking-wider text-navy-800/50 text-center">Notes</span>
</div>
```

Changes: `48px` → `52px` rank column, `120px` → `140px` awards column, `px-5` → `px-6`.

### Table data rows — LEFT-ALIGNED content, larger text, lines + banding

**Critical: All data content is LEFT-ALIGNED (except rank which stays centered).**

Add a visual tier separator. After the top-tier rows (ranks 1-2), insert a subtle divider label. After mid-tier (ranks 3-4), another. This groups the table into the story: nationals → mid-market → beatable peers.

**Tier group labels** — inserted between row groups:
```jsx
{/* After top-tier rows */}
<div className="px-6 py-2 border-b border-black/[0.04]" style={{ backgroundColor: 'rgba(15,26,46,0.02)' }}>
  <span className="font-body text-[10px] font-semibold uppercase tracking-widest text-navy-800/30">
    — National Leaders —
  </span>
</div>

{/* After mid-tier rows */}
<div className="px-6 py-2 border-b border-black/[0.04]" style={{ backgroundColor: 'rgba(15,26,46,0.02)' }}>
  <span className="font-body text-[10px] font-semibold uppercase tracking-widest text-navy-800/30">
    — Regional Mid-Market —
  </span>
</div>

{/* Before target tier */}
<div className="px-6 py-2 border-b border-black/[0.04]" style={{ backgroundColor: 'rgba(15,26,46,0.02)' }}>
  <span className="font-body text-[10px] font-semibold uppercase tracking-widest text-navy-800/30">
    — Newport's Competitive Tier —
  </span>
</div>
```

To do this, don't map COMPETITORS as one flat list. Instead, group them:

```jsx
const topTier = COMPETITORS.filter(c => c.tier === 'top')      // ranks 1-2
const midTier = COMPETITORS.filter(c => c.tier === 'mid')       // ranks 3-4
const targetTier = COMPETITORS.filter(c => c.tier === 'target') // ranks 5-8
```

Then render each group with its label before it.

**Data row structure:**

```jsx
<motion.div
  key={c.rank}
  initial={{ opacity: 0, x: -10 }}
  animate={{ opacity: 1, x: 0 }}
  transition={{ delay: baseDelay + i * 0.06, duration: 0.3 }}
  className={`grid grid-cols-[52px_1.4fr_140px_1fr] px-6 py-4 border-l-[3px] border-b border-black/[0.06] ${
    i % 2 === 0 ? 'bg-navy-950/[0.02]' : 'bg-transparent'
  }`}
  style={{ borderLeftColor: tierLeftBorder(c.tier) }}
>
  {/* Rank — centered */}
  <span className="font-body text-base font-semibold text-center text-navy-800/50">
    #{c.rank}
  </span>

  {/* Company — LEFT-ALIGNED */}
  <span className={`font-body text-base ${
    c.tier === 'top' ? 'font-semibold text-navy-950' : 'text-navy-800/70'
  }`}>
    {c.company}
    <TierBadge tier={c.tier} />
  </span>

  {/* Amount — LEFT-ALIGNED, bold */}
  <span className={`font-body text-base font-bold tracking-tight ${
    c.rank === 1 ? '' : c.tier === 'top' ? 'text-navy-950' : c.tier === 'mid' ? 'text-navy-950' : 'text-navy-800/60'
  }`} style={c.rank === 1 ? { color: '#C9A84C' } : undefined}>
    {fmtM(c.amount)}
  </span>

  {/* Notes — LEFT-ALIGNED */}
  <span className="font-body text-sm text-navy-800/50">
    {c.notes}
  </span>
</motion.div>
```

Key changes from current:
- `text-sm` → `text-base` for company and amount (larger, more readable)
- Removed all `text-center` and `justify-center` from data cells — everything LEFT-ALIGNED
- Rank stays `text-center` (it's a narrow column, centering is natural)
- `px-5` → `px-6` (more breathing room)
- `52px` rank column, `140px` awards column (wider)

### Newport callout row — INLINE in the ranking, not a footer

Instead of a special footer row, Newport appears as a visual break WITHIN the target tier section. It should feel like part of the ranking, not an appendage.

```jsx
<motion.div
  initial={{ opacity: 0, y: 6 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ delay: 0.95, duration: 0.4 }}
  className="grid grid-cols-[52px_1.4fr_140px_1fr] px-6 py-5 border-l-[4px] border-b border-black/[0.06]"
  style={{ backgroundColor: 'rgba(27,122,138,0.06)', borderLeftColor: '#C9A84C' }}
>
  <span className="font-body text-base font-bold text-center" style={{ color: '#1B7A8A' }}>
    →
  </span>
  <span className="font-body text-base font-bold" style={{ color: '#1B7A8A' }}>
    Newport Wholesalers
    <span className="inline-flex items-center ml-2 px-2 py-0.5 rounded-full text-[10px] font-semibold" style={{ backgroundColor: 'rgba(201,168,76,0.10)', color: '#C9A84C' }}>
      Entry
    </span>
  </span>
  <span className="font-body text-base font-bold tracking-tight" style={{ color: '#C9A84C' }}>
    $1-5M
  </span>
  <span className="font-body text-sm text-navy-800/60">
    30-year track record · Cold chain · Plantation, FL
  </span>
</motion.div>
```

Changes: LEFT-ALIGNED company and notes. `text-base` throughout. `py-5` for more prominence. Newport row appears right after rank #5 (Rainmaker) — place it after rendering `targetTier[0]` (Rainmaker) to show Newport entering at the #5-6 range.

### Final structure of the render:

```jsx
{/* Table card */}
<motion.div className="rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)] overflow-hidden relative z-10 flex-1">

  {/* Table header */}
  {/* ... centered headers ... */}

  {/* National Leaders label */}
  {/* topTier rows */}

  {/* Regional Mid-Market label */}
  {/* midTier rows */}

  {/* Newport's Competitive Tier label */}
  {/* targetTier[0] — Rainmaker (the direct competitor) */}
  {/* ===== Newport callout row ===== */}
  {/* targetTier[1..3] — Freedom Fresh, Matts Trading, Wholesome Foods */}

</motion.div>
```

This tells the story visually: "National leaders at the top (you're not fighting them), mid-market in the middle, and HERE — in the $1-5M tier — is where Newport enters with more capability than every other player."

### Source — keep as-is (already correct)

---

## Execution order

1. Fix slide 6 (`ConfectioneryGapSlide.jsx`) — bento grid rewrite
2. Fix slide 7 (`TargetAgenciesSlide.jsx`) — hierarchy with primary/secondary cards
3. Fix slide 8 (`CompetitionSlide.jsx`) — remove KPI tiles, left-align, tier grouping
4. Run `./node_modules/.bin/vite build --outDir /tmp/newport-build` to verify clean build
5. Check localhost:5174 for visual review

## What NOT to touch
- Slides 1-5 — locked/approved
- Slide 9+ — future batch
- Data files (market.js, strategy.js) — read-only
- DecorativeElements.jsx, SourceCitation.jsx — shared, don't modify
- Navigation, SlideContainer, PasswordGate, App.jsx
