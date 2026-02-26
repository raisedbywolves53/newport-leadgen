# Newport Presentation Design System

> **Purpose**: This document is the single source of truth for every visual decision in the Newport web presentation (slides 3–19). It is written so that an AI coding assistant can mechanically produce slides that meet Fortune 500 executive-presentation standards — the kind of work McKinsey would deliver to a boardroom.
>
> **Slides 1–2 are locked.** Do not modify TitleSlide or ExecutiveSummarySlide. They are the quality reference. Every subsequent slide must feel like it belongs in the same deck.

---

## 1. Design Philosophy

The presentation tells a single story: *Newport is the right partner for government food procurement.* Every slide is a scene in that story. The visual language must be **quiet, confident, and editorial** — the way Bloomberg, McKinsey, or a premium fintech dashboard communicates.

**Three governing principles:**

1. **Unified surface** — Every slide reads as one cohesive card/dashboard, not a collection of independent elements fighting for attention. White space is a design element, not wasted space.
2. **Two-accent discipline** — Gold and teal carry all visual weight. No other hue appears in data, accents, or highlights. Period.
3. **Let the data breathe** — If a number is important, give it size. If text is supporting, make it smaller and lighter. Never let two elements compete at the same visual weight.

---

## 2. Color System

### 2.1 Background

| Token | Hex | Usage |
|-------|-----|-------|
| `slide-bg` | `#e6e6ec` | Slide canvas (applied by `SlideBackground`) — never override |
| `navy-950` | `#0F1A2E` | App chrome only (password gate, HTML body). Never on slide surfaces |

### 2.2 Text Hierarchy (on slide background)

| Role | Color | Tailwind Class |
|------|-------|----------------|
| Primary headline | `navy-950` | `text-navy-950` |
| Secondary headline / card title | `navy-950` | `text-navy-950` |
| Body text | `navy-800/65` | `text-navy-800/65` |
| Caption / detail / footnote | `navy-800/40` | `text-navy-800/40` |
| Kicker / eyebrow label | `navy-800/40` or `teal-500` | `text-navy-800/40` or `text-teal-500` |
| Source citation | `navy-800/35` | `text-navy-800/35` |

### 2.3 Accent Palette (strict — no exceptions)

| Role | Name | Hex | When to use |
|------|------|-----|-------------|
| **Primary accent** | Gold | `#C9A84C` | Hero stats, accent strips, gold lines, primary KPI values, chart emphasis, icon tints on lead cards |
| **Secondary accent** | Teal | `#1B7A8A` | Supporting KPI values, secondary data series, icon tints on supporting cards, subtle accent bars |
| **Tertiary (data only)** | Light teal | `#3CC0D4` | Third data series in multi-series charts ONLY. Never for text or card accents |
| **Tertiary (data only)** | Amber | `#E8913A` | Fourth data series in multi-series charts ONLY, or a single "warning/highlight" callout per slide. Never for general decoration |

### 2.4 Forbidden Colors

These colors exist in the CSS tokens but **must not be used** as accents, borders, icon tints, or data colors on slides 3–19:

- `navy-600` through `navy-800` as card backgrounds or circle fills
- Any red, green, purple, pink, or blue that is not in the accent palette above
- Raw amber (`#E8913A`) as a card border or background — use only as a data-chart fill or a single highlight badge
- Any color at full opacity over large areas — cards are always `white/70` or `white` with backdrop blur

### 2.5 Card Surface

All cards, tiles, and container elements use one canonical surface:

```
rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)]
```

**Variations:**

| Variant | Additional classes | When |
|---------|-------------------|------|
| Hero card (1 per slide max) | `bg-white` (full opacity), left gold accent strip (`w-1 rounded-full bg-[#C9A84C]` absolute left) | The single most important card on the slide — the anchor |
| Emphasized card | `border-teal-500/20 bg-teal-500/[0.04]` | One secondary callout per slide, max |
| Highlighted badge | `border-amber-500/20 bg-amber-500/[0.06]` | One per slide max, for a "key insight" or warning |
| Standard card | Base surface only | Everything else |

**Rules:**

- Never more than **1 hero card** per slide
- Never more than **1 emphasized + 1 highlighted** card per slide
- If a slide has 4+ cards, they should ALL be standard — differentiate with accent-colored stat values, not card backgrounds
- Cards have **no drop shadow heavier** than the base `shadow-[0_1px_3px_rgba(0,0,0,0.04)]`

---

## 3. Typography

### 3.1 Font Stack

| Role | Family | Weight | Tracking |
|------|--------|--------|----------|
| **Display** | `Playfair Display` | — | — |
| **Body** | `Inter` | 400–700 | `tracking-tight` on stats, normal on body |

### 3.2 Usage Rules

- **Playfair Display is used ONLY on slide 1 (title).** Slides 2–19 use `Inter` for everything — headlines, stats, body, captions. No exceptions.
- Headlines: `text-4xl font-bold tracking-tight` (or `text-3xl` on dense slides)
- Kicker/eyebrow: `text-xs font-semibold uppercase tracking-widest`
- Hero stat: `text-6xl md:text-7xl font-bold tracking-tighter leading-none`
- Card stat: `text-3xl font-bold tracking-tight leading-none`
- Card title: `text-base font-semibold` or `text-sm font-semibold`
- Card body: `text-sm leading-relaxed` or `text-[13px] leading-relaxed`
- Detail/caption: `text-[11px]` or `text-[10px]`
- Source line: `text-[10px] text-navy-800/35`

### 3.3 Hierarchy Pattern (every slide follows this)

```
Eyebrow label (xs, uppercase, tracking-widest, teal or navy-800/40)
Headline (3xl–4xl, bold, navy-950)
Subtitle (sm, navy-800/60, max-w-2xl)
GoldLine (60px, animated)
—— content area ——
Source citation (10px, navy-800/35, bottom of slide)
```

---

## 4. Layout System

### 4.1 Slide Container

Every slide's root `<div>`:

```
w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden
```

- `pb-20` ensures content clears the fixed navigation bar
- `px-16 lg:px-20` gives generous horizontal margins (editorial feel)
- `relative overflow-hidden` enables decorative elements and absolute-positioned citations

### 4.2 Content Layouts (choose one per slide)

| Layout | Grid | Best for |
|--------|------|----------|
| **Bento** | `grid-cols-[1fr_1fr] grid-rows-[repeat(3,1fr)]` with hero card `row-span-2` | 1 hero metric + 2–3 supporting stats (slides 3, 5) |
| **Two-column** | `grid-cols-2 gap-5` or `grid-cols-[45%_55%]` | Side-by-side comparison, visual + text (slides 4, 14, 16) |
| **Card grid** | `grid-cols-2 gap-4` | 4 equal-weight cards (slides 9) |
| **Table** | `grid-cols-[...explicit widths...]` | Data tables with row striping (slides 7, 10, 12, 17) |
| **Hero + detail** | Flex column: hero stat top, detail cards below | One big number + supporting context (slides 6, 11) |
| **Process flow** | Flex row (horizontal pipeline) + grid below | Sequential steps (slide 8) |
| **Split narrative** | `grid-cols-[1fr_auto_1fr]` | Two-side comparison with center connector (slide 18 blueprint) |

### 4.3 Spacing Rules

- Gap between cards: `gap-4` (standard) or `gap-5` (bento/hero layouts)
- Header to content: `mb-4` after GoldLine
- Internal card padding: `p-5` (standard) or `p-8 to p-10` (hero card)
- Icon to text inside cards: `gap-3` or `gap-4`
- Never let content touch the slide edges — minimum `px-16`

---

## 5. Visual Assets

### 5.1 KPI Tiles / Stat Cards

The **StatCard** is the primary visual unit. Every data slide uses them.

**Anatomy:**

```
┌──────────────────────────────────┐
│ [Icon]  Label text (xs, semibold)│
│                                  │
│  $87M  (3xl, bold, accent color) │
│                                  │
│  Detail text (11px, navy-800/50) │
└──────────────────────────────────┘
```

**Icon treatment:**

- Icon inside a `w-9 h-9 rounded-lg` pill with `backgroundColor: ${accentColor}15` (15% opacity)
- Icon itself uses the accent color at `strokeWidth={1.5}`
- Use `lucide-react` icons only

**Accent color rules for stat values:**

- The **single most important stat** on the slide gets gold (`#C9A84C`)
- All other stats use either `navy-950` (dark, neutral) or teal (`#1B7A8A`)
- Never use amber or light teal for stat values in cards

**Hero stat (standalone, outside cards):**

- Use the `HeroStat` component from `DecorativeElements.jsx`
- `text-6xl md:text-7xl font-bold tracking-tighter`
- Gold accent color
- Placed at top-left of content area, with unit text beside it at `text-lg`
- Maximum one per slide

### 5.2 Charts

**General chart rules:**

- Use ECharts with canvas renderer
- Chart backgrounds: `transparent` — the card/slide provides the surface
- Grid lines: `#e5e7eb` at 0.5 opacity, horizontal only, no vertical
- Axis labels: Inter, 11px, `#64748B`
- No chart borders or outlines
- Maximum 4 data series per chart

**Color assignment for data series:**

| Series | Color | Opacity |
|--------|-------|---------|
| 1st (primary) | Gold `#C9A84C` | 100% |
| 2nd | Teal `#1B7A8A` | 100% |
| 3rd | Light teal `#3CC0D4` | 100% |
| 4th | Amber `#E8913A` | 100% |

**Chart type guidance:**

| Data story | Chart type | Notes |
|------------|-----------|-------|
| Part-to-whole | Donut (not pie) | Max 4 segments. Center label with total. Use ECharts `radius: ['55%', '80%']` |
| Composition over time | Stacked bar | Horizontal axis = time. Use the 4-color series order above |
| Ranking / comparison | Horizontal bar | Sorted descending. Single color (gold or teal) |
| Relationship / hierarchy | Concentric circles or nested cards | Not a traditional chart — build with divs |
| Trend | Line chart | Gold primary line, teal secondary. Subtle area fill at 10% opacity |

**Chart sizing:**

- Charts sit inside cards or take 50–60% of the content area width
- Minimum chart height: 200px
- Always include a legend below or beside the chart (not overlaid)

### 5.3 Tables

**Table styling:**

```
Header row: font-body text-[11px] font-semibold uppercase tracking-wider text-navy-800/40
            border-b border-black/[0.08] pb-2
Data rows:  font-body text-sm text-navy-800/70
            Even rows: bg-white/40
            Odd rows: bg-transparent
            Row padding: py-3
```

- Use CSS Grid for table layout (not `<table>`) — allows precise column widths
- First column left-aligned, number columns right-aligned
- Currency values: bold, accent-colored (gold for the highest, teal for others, navy-950 for standard)
- Row hover: not needed (this is a presentation, not an app)

**Badge system for categorical data in tables:**

| Category | Style |
|----------|-------|
| Highest priority / best fit | `bg-amber-500/10 text-amber-500 rounded-full px-3 py-0.5 text-[11px] font-semibold` |
| High / good | `bg-teal-500/10 text-teal-500 rounded-full px-3 py-0.5 text-[11px] font-semibold` |
| Moderate | `bg-navy-800/10 text-navy-800/60 rounded-full px-3 py-0.5 text-[11px] font-semibold` |
| Avoid / low | `bg-navy-800/5 text-navy-800/35 rounded-full px-3 py-0.5 text-[11px] font-semibold line-through` |

### 5.4 Process Flows / Pipelines

- Horizontal flex row with icon badges connected by subtle arrows
- Badge: `w-10 h-10 rounded-full` with accent background at 15% opacity, icon centered
- Connector: `ArrowRight` icon at `text-navy-800/20` between badges
- Label below each badge: `text-[11px] font-semibold text-navy-950`
- Sub-label: `text-[10px] text-navy-800/40`
- Maximum 5 stages per pipeline row

### 5.5 Decorative Elements

Use sparingly — decoration should never compete with data.

| Element | Component | Placement | Frequency |
|---------|-----------|-----------|-----------|
| Gold line | `GoldLine` | Below subtitle, before content | Every slide |
| Compass star | `CompassStar` | Bottom-right, next to source | 1 in 3 slides max |
| Background ring | `BackgroundRing` | Top-right or bottom-left, half off-screen | Max 1–2 per slide |

- Background rings: `opacity={0.03}` or `opacity={0.025}`, gold color
- CompassStar: `opacity={0.2}`, size 16px
- GoldLine: 48–60px wide, always gold `#C9A84C`

---

## 6. Animation System

All animations use `motion/react` (Framer Motion).

### 6.1 Standard Patterns

| Element | Initial | Animate | Duration | Delay |
|---------|---------|---------|----------|-------|
| Headline | `opacity: 0, y: 12` | `opacity: 1, y: 0` | 0.4s | 0.1s |
| Subtitle | `opacity: 0` | `opacity: 1` | 0.4s | 0.2s |
| GoldLine | `width: 0` | `width: target` | 0.8s | 0.25s |
| Cards (staggered) | `opacity: 0, y: 16` | `opacity: 1, y: 0` | 0.45s | 0.4 + i × 0.1 |
| Hero stat / chart | `opacity: 0, scale: 0.95` | `opacity: 1, scale: 1` | 0.6s | 0.3s |
| Source citation | `opacity: 0` | `opacity: 1` | 0.4s | last (1.0–1.6s) |

### 6.2 Rules

- Total animation sequence per slide: **under 2 seconds**
- Header always animates first (0.1–0.25s delay)
- Content follows header (0.3–0.5s start)
- Source citation animates last
- `useCountUp` hook for animated numeric stats — use `duration: 1200, delay: 600 + index * 200`
- Never animate background decorative elements with attention-grabbing motion (no scale bouncing, no color shifts)

---

## 7. Slide-by-Slide Instructions

> **Legend:**
> Layout = the CSS Grid / Flex structure
> Hero = the single most prominent visual element
> Cards = StatCard-style tiles
> Source = bottom-line citation

---

### Slide 3: Why Newport Wins

**Content:** 4 competitive advantages (30 years, 1091 firms suspended, 83% micro-purchase, $5M entry tier)

**Layout:** Bento grid — `grid-cols-[1fr_1fr] grid-rows-[1fr_1fr_1fr]`, height ~460px

**Structure:**
- Eyebrow: "Competitive Moat" (teal)
- Headline: "Why Newport Wins" (4xl)
- Subtitle: one line about post-fraud environment
- GoldLine
- Hero card: `row-span-2`, left column — "30 Years" stat in gold 7xl, left accent strip, full white bg. Contains icon, stat, headline, detail, footer ("Since 1996 · Plantation, FL")
- 3 standard StatCards stacked in right column — stats in gold or teal, icon pills
- Source line + CompassStar bottom-right
- BackgroundRing top-right and bottom-right, gold, 3% opacity

**Accent assignment:** "30" and "1,091" in gold. "83%" and "$5M" in teal.

**Status:** This slide is LOCKED as the quality reference. Do not modify.

---

### Slide 4: Florida TAM by Channel (NEEDS COMPLETE REDESIGN)

**Content:** $87M total Florida addressable market broken into 5 procurement channels

**Layout:** Bento grid — same pattern as slide 3: `grid-cols-[1fr_1fr] grid-rows-[1fr_1fr_1fr]`, height ~460px

**Structure:**
- Eyebrow: "Florida Total Addressable Market" (navy-800/40)
- Headline: "Five Channels to Market" (4xl, navy-950)
- Subtitle: "Federal is the entry point — state, education, and local expand the opportunity."
- GoldLine
- **Hero card** (left, `row-span-2`): Contains the concentric-circle visualization centered inside the card. Five nested circles using ONLY gold and teal shades: outermost `#C9A84C` at 15% opacity, each ring progressively darker teal. Center displays "$87M" in gold 5xl bold with "Total TAM" label beneath. Ring labels (`$20-30M`, `$10-20M`, etc.) positioned on each ring in white/80. The hero card has the standard white bg with left gold accent strip.
- **3 StatCards** (right column, stacked): Pick the 3 most narratively important channels (Federal Visible $6.4M, Micro-Purchase $8-15M, State $20-30M). Each card shows channel name, dollar amount as the card stat (teal accent), and 1-line detail. Icon pills using lucide icons.
- **Bottom bar** (below the bento, full width): A subtle single-row strip showing all 5 channels with colored dots and amounts, like a legend. This ensures no channel is lost while keeping the cards focused.
- Source citation + confidence note at bottom

**Accent assignment:** "$87M" hero stat in gold. Channel stats in teal. Micro-purchase callout can use amber badge if needed.

**Key change from current:** Eliminate the 3-zone layout (left legend / center circles / right insights). Replace with the bento pattern from slide 3. The circles move INSIDE the hero card. The insight callouts become standard StatCards.

---

### Slide 5: Product Opportunity Matrix

**Content:** 3-tier product prioritization — Tier 1 (Highest), Tier 2 (Growth), Tier 3 (Avoid)

**Layout:** Hero + detail — hero stat top-left, then tier sections below

**Structure:**
- Eyebrow: "Product Strategy" (navy-800/40)
- Headline: "Where Newport Fits" (4xl)
- Subtitle: one line about PSC category prioritization
- GoldLine
- **Tier 1** section header (gold label "Highest Priority") → 2 cards side-by-side (`grid-cols-2 gap-4`). Each card: product name (sm, semibold), PSC code badge (navy ghost badge), FL Spend stat in gold bold, sole-source %, advantage text, markup range. These are the hero products — cards can use emphasized styling (teal border) for one.
- **Tier 2** section header (teal label "Growth Opportunity") → 3 cards in a row (`grid-cols-3 gap-3`). Compact cards: product name, PSC, FL spend in navy-950, sole-source %, brief advantage. Standard card styling.
- **Tier 3** — not cards. A single subtle line of text listing "Avoid" items with strikethrough styling and brief reason: "Meat (Tyson/JBS dominated) · MREs (military manufacturing) · Beverages (low margin)". Use `text-navy-800/35` with line-through.
- Source citation

**Accent assignment:** Tier 1 FL Spend values in gold. Tier 2 in teal. Tier 3 grayed out.

---

### Slide 6: The Confectionery Gap

**Content:** PSC 8925 deep dive — Newport's Segment E advantage, 58% sole-source, 45 national awards

**Layout:** Two-column — `grid-cols-2 gap-8`

**Structure:**
- Eyebrow: "Category Deep Dive" (navy-800/40)
- Headline: "The Confectionery Gap" (4xl)
- Subtitle: why this category is Newport's beachhead
- GoldLine
- **Left column:** Donut chart inside a card. ECharts donut showing 58% sole-source (gold) vs 42% competitive (navy-800/10 light gray). Center label: "58%" in gold bold, "Sole Source" below. Chart sits inside a standard card surface. Below the chart: `useCountUp` stat for 45 national awards in teal.
- **Right column:** 4–5 bullet-style insight cards (compact, no icons). Each is a mini stat-card: one-line headline ("Newport already supplies Segment E confectionery", "Average 1.6 offers per award", etc.) with detail text. Standard card surface, stacked with `gap-3`.
- Source citation

**Accent assignment:** 58% and donut primary slice in gold. 45 awards in teal. Chart secondary slice in light gray.

---

### Slide 7: Competition Landscape

**Content:** Top 8 FL food distributors ranked by government contract value, with Newport entry positioning

**Layout:** Hero + table

**Structure:**
- Eyebrow: "Competitive Analysis" (navy-800/40)
- Headline: "Competition Landscape" (4xl)
- Subtitle: "Where Newport enters the ranking"
- GoldLine
- **Compact hero stat area** (flex row): "$26.1M" (gold, 3xl) labeled "Top FL Competitor (Oakes Farms)" and "Rank #5-10 tier: $1-5M" (teal) to establish context
- **Table** (full width, inside a card surface): Grid columns — Rank (centered), Company, FL Gov Awards (right-aligned, bold), Notes. 8 rows with tier-based subtle left-border accents: top tier (gold left-border), mid tier (teal left-border), target tier (standard). Newport callout row at bottom with teal background `bg-teal-500/[0.04]` and gold stat showing "$1-5M Entry"
- Source citation

**Accent assignment:** Oakes Farms $26.1M in gold (they're the benchmark). Newport entry range in teal. All other amounts in navy-950.

---

### Slide 8: How It Works (Pipeline)

**Content:** 5-stage deal pipeline + 4 sourcing channel cards

**Layout:** Process flow (top) + card grid (bottom)

**Structure:**
- Eyebrow: "Process" (navy-800/40)
- Headline: "How It Works" (4xl)
- Subtitle: from opportunity identification to contract award
- GoldLine
- **Pipeline row** (flex, centered): 5 circular badges connected by subtle arrows. Each badge: `w-12 h-12 rounded-full bg-[accent]/15` with lucide icon in center. Labels below. Colors: stages 1-2 teal, stages 3-4 gold, stage 5 teal (start and end bookend). Arrow connectors: `text-navy-800/15`.
- **Sourcing channels** (below pipeline, `grid-cols-4 gap-3`): 4 equal cards — each shows channel name, accessibility note, and sourcing tool. Standard card surface. Top accent bar (2px rounded, teal or gold) to differentiate. Icon pills in matching accent.
- Source citation

**Accent assignment:** Pipeline badges alternate gold and teal. Channel cards use teal accent bars for free channels, gold for paid.

---

### Slide 9: Target Agencies

**Content:** 4 priority procurement targets (DOJ/BOP, Military/DoD, FEMA, School Districts)

**Layout:** Card grid — `grid-cols-2 gap-4`

**Structure:**
- Eyebrow: "Target Buyers" (navy-800/40)
- Headline: "Target Agencies" (4xl)
- Subtitle: "Four channels into Florida procurement"
- GoldLine
- **2x2 grid of agency cards**: Each card has a top accent bar (4px, rounded-t, alternating gold/teal), icon pill, agency name (base, semibold), key stat (xl, bold, accent-colored), and 2-3 line description. Cards are all standard surface. Top-left card (DOJ/BOP) gets gold accent bar (primary target). Others get teal.
- BackgroundRing bottom-left, gold, 3% opacity
- Source citation

**Accent assignment:** DOJ/BOP stat in gold (primary target). Others in teal. FEMA stat can use amber badge for "Disaster-driven."

---

### Slide 10: Real Contracts (divider: "The Strategy" comes before this)

**Content:** 6-column contract examples table showing real opportunities

**Layout:** Table (full width)

**Structure:**
- Eyebrow: "Pipeline Examples" (navy-800/40)
- Headline: "Real Contracts" (4xl)
- Subtitle: "Current and recent opportunities matching Newport's profile"
- GoldLine
- **Table** inside a full-width card surface: Columns — Agency, Description, Est. Value (right-aligned), Type (badge), Competition (badge), Fit (badge). Use the badge system from Section 5.3 for Type/Competition/Fit columns. Rows use alternating bg-white/40. Currency values: HIGHEST fit rows get gold amounts, others in navy-950.
- Source citation

**Accent assignment:** Contract values for HIGHEST-fit rows in gold. Type badges use teal for micro-purchase, gold for simplified. Fit badges follow the standard badge color system.

---

### Slide 11: Portfolio Evolution

**Content:** 5-year stacked bar chart showing contract accumulation (micro → simplified → larger → renewed)

**Layout:** Hero + chart (hero left, chart right)

**Structure:**
- Eyebrow: "Growth Trajectory" (navy-800/40)
- Headline: "Portfolio Evolution" (4xl)
- Subtitle: "How the contract base compounds over five years"
- GoldLine
- **Left (35%):** Hero stat — "78" in gold 7xl with "Active Contracts by Year 5" label. Below: a compact legend showing the 4 series with colored dots.
- **Right (65%):** ECharts stacked bar chart inside a card surface. 6 time periods on x-axis. 4 series in this order: Micro (gold), Simplified (teal), Larger (light teal `#3CC0D4`), Renewed (amber `#E8913A`). Chart grid: subtle horizontal lines only.
- Source citation

**Accent assignment:** Series order follows Section 5.2 chart colors. Hero stat "78" in gold.

---

### Slide 12: Relationship Strategy (BD Strategy)

**Content:** 3 influence layers + 5-step front-line sourcing process

**Layout:** Two-column — `grid-cols-2 gap-6`

**Structure:**
- Eyebrow: "Business Development" (navy-800/40)
- Headline: "Relationship Strategy" (4xl)
- Subtitle: "Three layers of influence in government procurement"
- GoldLine
- **Left column: Influence Layers** — 3 stacked cards with downward arrow connectors between them. Card 1 (Contracting Officers): teal accent, icon pill. Card 2 (Program Managers): teal accent. Card 3 (Front-Line Influencers): gold accent (this is Newport's entry point — the hero layer). Each card: role title (sm, semibold), 1-line description, key stat.
- **Right column: Process Flow** — Numbered steps (1-5) as a vertical timeline. Each step: number in a `w-8 h-8 rounded-full bg-teal-500/15` circle, title (sm, semibold), description (text-[13px], navy-800/60). Connecting line between steps: `border-l-2 border-navy-800/10`.
- Key insight callout card at bottom-right: teal emphasized card surface, one-line about why front-line sourcing is Newport's advantage.
- Source citation

**Accent assignment:** Front-Line Influencers card gets gold accent (it's the hero insight). Others teal. Process step numbers in teal.

---

### Slide 13: Risk & Compliance

**Content:** Entry cost ($4K) vs. avoided costs ($360K) — two-column compliance comparison

**Layout:** Hero + two-column comparison

**Structure:**
- Eyebrow: "Compliance" (navy-800/40)
- Headline: "Risk & Compliance" (4xl)
- Subtitle: "What's required vs. what's not"
- GoldLine
- **Compact hero row** (flex): Two stats side-by-side — "$4K Entry Cost" (teal, 3xl) and "$120-360K Avoided" (gold, 3xl) — establishing the contrast immediately
- **Two-column grid** (`grid-cols-2 gap-5`):
  - Left column: "Required" header with `ShieldCheck` icon in teal. 4-5 mini cards listing each requirement (item name, cost, timeline). Bottom summary: teal emphasized card with total.
  - Right column: "Not Required" header with `ShieldOff` icon in gold. 4-5 mini cards listing avoided items (item, cost, note). Bottom summary: gold/amber highlighted card with total avoided.
- BackgroundRing top-right
- Source citation

**Accent assignment:** "Required" column uses teal throughout. "Not Required/Avoided" column uses gold. The contrast between columns IS the visual story.

---

### Slide 14: Our Recommendation

**Content:** Free vs. Paid route comparison — tool visibility levels, recommendation for paid route

**Layout:** Table + two-column cards

**Structure:**
- Eyebrow: "Recommendation" (navy-800/40)
- Headline: "Our Recommendation" (4xl)
- Subtitle: "Two paths to market — visibility defines the difference"
- GoldLine
- **Comparison table** (inside card surface): 3-column grid — Feature, Free Route, Paid Route. Free column uses `EyeOff` icon, muted styling. Paid column uses `Eye` icon, standard styling. Rows: visibility %, tools included, cost, timeline. Free values in navy-800/50 (muted). Paid values in navy-950 (strong).
- **Two recommendation cards** (`grid-cols-2 gap-4`): Left card (Free Route) — standard surface, "$0" stat, bullet list of included tools, "40-50% visibility" callout. Right card (Paid/Recommended) — hero card surface with gold left accent strip, "$13K/yr" stat in gold, bullet list, "90%+ visibility" callout, gold "Recommended" badge top-right.
- Source citation

**Accent assignment:** Paid route values in gold. Free route values muted (navy-800/50). "Recommended" badge in gold.

---

### Slide 15: Key Questions

**Content:** 10 owner decision questions grouped in 3 categories

**Layout:** Category groups — vertical stack with compact question cards

**Structure:**
- Eyebrow: "Decision Framework" (navy-800/40)
- Headline: "Key Questions" (4xl)
- Subtitle: "Ten decisions for Newport's leadership"
- GoldLine
- **3 category sections** stacked vertically with `gap-4` between:
  - Category 1: "Will This Work?" (teal label). Questions listed as compact rows inside a card: priority badge (left), question text (center), "why it matters" (right, lighter). Priority badges use the standard badge system.
  - Category 2: "What Are the Risks?" (gold label). Same format.
  - Category 3: "How Much Bigger?" (navy label). Same format.
- Each category is a single card surface containing its questions as rows, not individual cards per question. This prevents visual fragmentation.
- Large decorative "10" watermark: `text-[12rem] font-bold text-navy-800/[0.03]` positioned absolute right, acting as a subtle background anchor.
- Source citation

**Accent assignment:** Category 1 header teal. Category 2 header gold. Priority badges follow standard badge colors (HIGHEST = amber, HIGH = teal, MEDIUM = navy ghost).

---

### Slide 16: B2B Fast Track

**Content:** 5 institutional buyer targets with table (GEO Group, Aramark, CoreCivic, Charter Schools, Assisted Living)

**Layout:** Hero + table

**Structure:**
- Eyebrow: "Private Sector" (navy-800/40)
- Headline: "B2B Fast Track" (4xl)
- Subtitle: "Institutional buyers with 2-8 week sales cycles"
- GoldLine
- **Hero stat** (left-aligned): "2-8 Weeks" in gold 5xl bold, with `Zap` icon and "Average sales cycle" label
- **Table** (full width, inside card surface): Columns — Organization, FL Scale, Est. Food Spend (right-aligned, bold), Detail, Entry Path. First row (GEO Group) gets highlighted treatment: `bg-amber-500/[0.04]` background, gold spend value, `MapPin` badge showing "15 mi from Newport." Other rows alternate standard. Aramark row can use teal accent for its $90M/yr value (largest contract).
- Source citation

**Accent assignment:** GEO Group spend in gold (closest proximity, best fit). Aramark spend in teal (largest contract). Others in navy-950.

---

### Slide 17: The Blueprint (Final Slide)

**Content:** Partnership responsibilities — what Newport owns vs. what Still Mind delivers

**Layout:** Split narrative — `grid-cols-[1fr_auto_1fr]`

**Structure:**
- Eyebrow: "Partnership" (navy-800/40)
- Headline: "The Blueprint" (4xl)
- Subtitle: "Who does what — clear ownership, measurable outcomes"
- GoldLine
- **Left panel** (Newport card — teal accent): Card with left accent strip in teal. Header: `Truck` icon + "Newport Wholesalers" title. Bulleted list of Newport's responsibilities (4-6 items). Each bullet: `text-sm text-navy-800/65` with teal dot marker.
- **Center connector**: Vertical line (gradient from teal to gold, 1px) with `Handshake` icon centered in a `w-10 h-10 rounded-full bg-white border border-black/[0.06]` badge.
- **Right panel** (Still Mind card — gold accent): Card with left accent strip in gold. Header: `Brain` icon + "Still Mind Creative" title. Bulleted list of Still Mind's responsibilities. Gold dot markers.
- Optional: Bottom bar showing shared success metrics
- Source citation (or CompassStar as final flourish)

**Accent assignment:** Newport side teal. Still Mind side gold. Center connector uses both colors as gradient.

---

### Divider Slides (Slide 9.5 "The Strategy", Slide 14.5 "Making It Real")

**Layout:** Centered, minimal

**Structure:**
- Section title: `text-5xl font-bold text-navy-950` centered
- Subtitle: `text-lg text-navy-800/50` centered, max-w-md
- GoldLine centered (80px)
- BackgroundRing large (600px), centered, 2% opacity
- CompassStar centered below title
- No cards, no data, no content — pure transition moment

---

## 8. Quality Checklist

Before considering any slide complete, verify:

- [ ] **Two-accent rule**: Only gold and teal appear as accent colors. No stray hues.
- [ ] **One hero**: Maximum one hero card or hero stat per slide. Everything else is supporting.
- [ ] **Card DNA**: All card surfaces use the canonical `rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06]` or an approved variant.
- [ ] **Typography scale**: No text between 16px and 30px that isn't a card stat. Headlines jump from body (14-15px) to 3xl+ (30px+). Stats jump from card-level (3xl) to hero-level (6-7xl). Avoid the mushy middle.
- [ ] **Breathing room**: Minimum `px-16` horizontal padding. Content never touches edges. Cards have `p-5` minimum internal padding.
- [ ] **Source citation present**: Every data slide has a `SourceCitation` component at the bottom.
- [ ] **Animation budget**: Total animation sequence under 2 seconds. Header first, content staggered, source last.
- [ ] **Footer clearance**: `pb-20` on slide container to clear fixed navigation.
- [ ] **No competing weight**: Squint test — when you blur your eyes, exactly ONE element dominates. If two elements fight for attention, one needs to shrink or lighten.
- [ ] **Consistent with slide 3**: Would this slide look natural placed immediately after slide 3? Same card DNA, same accent discipline, same editorial calm.

---

## 9. Component Reference

These components exist and should be reused — never recreate them:

| Component | Import | Purpose |
|-----------|--------|---------|
| `GoldLine` | `../ui/DecorativeElements` | Animated gold divider after subtitles |
| `CompassStar` | `../ui/DecorativeElements` | 4-pointed decorative star |
| `HeroStat` | `../ui/DecorativeElements` | Oversized metric display |
| `BackgroundRing` | `../ui/DecorativeElements` | Subtle circular decoration |
| `SourceCitation` | `../ui/SourceCitation` | Bottom-of-slide source line |
| `useCountUp` | `../../hooks/useCountUp` | Animated number counter |

All slide data lives in `/src/data/market.js` and `/src/data/strategy.js`. Import and use these — never hardcode data that exists in these files.

---

*This guide was written as if the presentation were for McKinsey's most important client. Every rule exists because breaking it would make the deck look like it was made by a committee instead of a designer. Follow it precisely.*
