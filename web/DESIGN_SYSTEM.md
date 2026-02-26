# Newport GovCon Presentation — Visual Design System

**Theme:** Midnight Executive
**Updated:** February 25, 2026
**Platform:** Vite + React 19 + Tailwind CSS v4 + Motion (Framer Motion) + ECharts
**Quality Baseline:** Slides 1 (Title) and 2 (The Opportunity) — every slide must match this bar

---

## 0. The Quality Bar — What "Good" Looks Like

Slides 1 and 2 are the standard. Every new slide must be evaluated against them before shipping.

### What Makes Slides 1–2 Work

**Slide 1 (Title)** succeeds because it is *cinematic*. A full-bleed aerial photograph creates immediate emotional weight — this is a real business with real infrastructure. The navy overlay at 80% makes the image feel like texture, not decoration. The typography is massive and confident (9xl bold, tracking-tight). The gold subtitle in small uppercase tracking says "premium editorial." The footer credit in wide-tracked uppercase says "this was crafted." Every element has intentional breathing room. There are only four things on the slide.

**Slide 2 (The Opportunity)** succeeds because it pairs *art with data*. The pencil-sketch tree illustration (roots = 30-year foundation) is emotionally resonant and hand-crafted — it immediately separates this from a template. The illustration occupies the full left 45% and bleeds off-edge, treating the slide like a magazine spread. The stat cards on the right are clean but warm (white glass, gold hero accent, count-up animations). The decorative compass/star element at the bottom adds a finishing touch. There are only two "zones" — art and content — and they don't compete.

### What Slides 3–19 Get Wrong

The remaining slides fail the quality bar in two ways:

**1. Visual storytelling disappears.** After slide 2, the presentation becomes a data-card layout engine. Every slide is the same pattern: heading, subtitle, grid of white rounded cards on warm-gray background. There are no illustrations, no photography, no visual metaphors, no emotional moments. The slides read as "dashboard UI" instead of "editorial presentation."

**2. The cards feel generic.** White rounded rectangles with tiny icons and small text are the default output of any AI coding tool. They're functional but they're not designed. Slide 2's cards work because they sit alongside a dramatic illustration — they're the "data" half of an art-data pairing. When cards exist alone on a blank warm-gray background (slides 3–19), they read as wireframes.

### The Fix: Every Slide Needs a Visual Anchor

A **visual anchor** is the element that makes someone pause and look. It's the thing that separates a designed slide from a data layout. On slide 1, it's the photograph. On slide 2, it's the tree illustration.

For slides 3–19, visual anchors could be:

- A curated illustration or artistic element (hand-drawn, editorial style — NOT stock icons, NOT AI-generated clip art)
- A hero data visualization that is beautiful on its own (a well-designed chart IS art when done right)
- A dramatic layout asymmetry (split compositions, oversized numbers that bleed, intentional negative space)
- Photography used as texture (heavily overlaid, cropped dramatically, never "stock photo on a slide")
- Subtle decorative elements (the compass star from slide 2, gold accent lines, fine typographic details)

**The rule: if you remove the data from a slide and there's nothing interesting left to look at, the slide needs a visual anchor.**

---

## 1. Color Palette

### Core Tokens (defined in `index.css` @theme block)

```css
@theme {
  /* Navy — the foundation */
  --color-navy-950: #0F1A2E;   /* Deepest: dark backgrounds, heading text on light */
  --color-navy-900: #1A2744;   /* Navigation bar, secondary dark surfaces */
  --color-navy-800: #243356;   /* Body text via opacity: /70 readable, /60 quiet, /40 metadata */
  --color-navy-700: #2E4068;   /* Dark borders, scrollbar, nav borders */
  --color-navy-600: #3A5080;   /* Rarely used — lighter navy accent */

  /* Teal — primary accent (opportunity, data, trust) */
  --color-teal-500: #1B7A8A;   /* Section labels, primary highlights, nav "opportunity" color */
  --color-teal-400: #239BAD;   /* Competitor callouts, lighter teal emphasis */
  --color-teal-300: #3CC0D4;   /* Callout text on teal-tinted cards */

  /* Amber — secondary accent (strategy, warmth, action) */
  --color-amber-500: #E8913A;  /* "Strategy" nav color, chart segments, warm emphasis */
  --color-amber-400: #F0A85C;  /* "Execution" nav color, lighter warm highlights */
  --color-amber-300: #F5C080;  /* Icon backgrounds at low opacity */

  /* Neutrals */
  --color-offwhite: #F5F6FA;   /* Default text on dark backgrounds */
  --color-slate-300: #CBD5E1;
  --color-slate-400: #94A3B8;  /* Nav counter text, muted labels */
  --color-slate-500: #64748B;  /* Inactive nav dots */

  /* Fonts */
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'Inter', system-ui, sans-serif;
}
```

### Signature Colors (hardcoded, not in @theme)

| Hex | Name | Usage |
|---|---|---|
| `#C9A84C` | **Gold** | The editorial signature. Title subtitle, section divider accent lines, hero stat numbers, hero card left-edge accent strips, icon tints on premium cards. Use sparingly — it signals "this is the most important thing." |
| `#9CA0A4` | Footer gray | Credit/attribution text on dark backgrounds only |
| `#E6E6EC` | Warm gray | Section divider gradient overlay base. Approximates the light-mode slide background. |

### Background Modes

**Dark (Title slide, password gate):** `navy-950` base. Photography or imagery with `bg-navy-950/80` overlay. Text is white/offwhite. Gold for accent text.

**Light (Content slides):** Warm gray ~`#E2E2E8` to `#E6E6EC`. Headings are `navy-950`. Body copy is `navy-800` at varying opacity. Cards are white.

### Opacity-Based Hierarchy

Instead of multiple gray tokens, this system controls text hierarchy through a single base color (`navy-800`) at different opacities:

| Opacity | Role | Example |
|---|---|---|
| `/70` | Readable body copy | Card descriptions, detail paragraphs |
| `/65` | Slightly quieter body | Secondary card text |
| `/60` | Slide subtitles | One-line context setters below headings |
| `/50` | Supporting detail | Supplementary info, less-important stats |
| `/40` | Metadata | Source citations, timestamps, unit labels |
| `/35` | Nearly invisible | Footnote-level citations |

---

## 2. Typography

### Fonts (loaded from Google Fonts in `index.html`)

| Role | Font | Weights | Tailwind | Notes |
|---|---|---|---|---|
| **Body / Everything** | Inter | 300, 400, 500, 600, 700 | `font-body` | Used for all headings, body, stats, labels. This is the voice of the presentation. |
| **Display / Reserved** | Playfair Display | 400, 500, 600, 700 | `font-display` | Available but currently unused. Reserved for future editorial moments where serif warmth is needed. |

### Type Scale

| Element | Size | Weight | Tracking | Color | Notes |
|---|---|---|---|---|---|
| Title H1 | `text-7xl` / `text-9xl` | 700 | `tracking-tight` | White | Only on title slide. Massive, confident. |
| Title subtitle | `text-base` | 400 | `tracking-[0.2em]` | Gold `#C9A84C` | Uppercase. Small and spaced = editorial luxury. |
| Slide heading H2 | `text-3xl` / `text-4xl` | 700 | `tracking-tight` | `navy-950` | Every content slide starts here. |
| Section divider H2 | `text-4xl` / `text-5xl` | 700 | `tracking-tight` | `navy-950` | Larger for act breaks. |
| Slide subtitle | `text-base` | 400 | Normal | `navy-800/60` | One line. Sets context. Always under heading. |
| Category label | `text-xs` | 600 | `tracking-widest` | `teal-500` | Uppercase. Appears above headings ("COMPETITIVE MOAT"). |
| Hero stat number | `text-4xl` to `text-7xl` | 700 | `tracking-tighter` | Gold or accent | The visual anchor of stat cards. Intentionally oversized. |
| Stat unit label | `text-[11px]` to `text-lg` | 500 | `tracking-wide` | `navy-800/35` | Uppercase. Sits next to big numbers. |
| Card headline | `text-base` to `text-xl` | 600 | Normal | `navy-950` | Clear, scannable. |
| Card body | `text-sm` to `text-[15px]` | 400 | Normal | `navy-800/65-70` | `leading-relaxed` for readability. |
| Table header | `text-xs` | 600 | Normal | `navy-800/60` | Uppercase optional. |
| Table cell | `text-sm` | 400 | Normal | `navy-800` or accent | Monospace for numbers (`font-mono`). |
| Source citation | `text-[10px]` | 400 | Normal | `navy-800/35-40` | Bottom-left, nearly invisible. Every data slide. |
| Footer credit | `text-sm` | 400 | `tracking-[0.2em]` | `#9CA0A4` | Uppercase. Title slide only. |

### Typography Rules

1. **No serif headings.** All headings are Inter bold with tight tracking.
2. **Uppercase is a design tool, not a default.** Reserved for: category labels, unit labels, title subtitle, footer credits. Never on headings or body.
3. **Opacity is hierarchy.** Navy-800 at `/70` → `/60` → `/50` → `/40` → `/35`. Never introduce new gray colors.
4. **Stat numbers break the scale.** `text-3xl` minimum, `text-7xl` for hero stats. Always bold, always accent-colored. They should be the first thing your eye hits.
5. **No italic. No underline. No strikethrough.** Anywhere.
6. **Antialiasing always on:** `-webkit-font-smoothing: antialiased`.

---

## 3. Layout & Spacing

### Slide Container (`SlideLayout.jsx`)

```
max-w-7xl mx-auto
px-8 md:px-16 lg:px-24
py-12
flex flex-col justify-center    /* vertically centered */
```

### Slide Transitions (`SlideContainer.jsx`)

```javascript
enter:  { x: '8%',  opacity: 0 }
center: { x: 0,     opacity: 1 }
exit:   { x: '-8%', opacity: 0 }
duration: 0.4s
ease: [0.25, 0.1, 0.25, 1]
```

### Key Spacing Values

| Relationship | Value | Why |
|---|---|---|
| Heading → subtitle | `mb-2` (8px) | Tight — they're a unit. |
| Subtitle → content | `mb-8` (32px) | Clear separation between setup and payload. |
| Cards in grid | `gap-4` to `gap-5` (16-20px) | Breathable but connected. |
| Card internal padding | `p-4` (standard) to `p-10` (hero) | Hero cards need room. Standard cards are compact. |
| Source citation → bottom | `bottom-4` (16px) | Pinned, out of the way. |
| Section divider → bottom | `pb-24` (96px) | Generous — the divider title sits low, leaving room for an illustration above. |

### Layout Patterns

**Magazine split** (Slide 2 — THE GOLD STANDARD): `grid-cols-[45%_55%]`. Art on left bleeds off-edge. Content on right is self-contained. This is the pattern that should be used more.

**Bento grid** (Slide 3): Hero card spans 2 rows left, 3 smaller cards stack right. Height fixed at 460px.

**Equal grid**: `grid-cols-2 gap-4` (stats), `grid-cols-4` (pipeline steps), `grid-cols-3` (tier 2 products).

**Two-column compare**: Side-by-side with distinct visual treatments per column (Risk: required vs. not required; Blueprint: Newport vs. Still Mind).

---

## 4. Cards & Surfaces

### The Three Card Types

**Standard Card** — workhorse data container:
```
rounded-2xl bg-white/70 backdrop-blur-sm
border border-black/[0.06]
shadow-[0_1px_3px_rgba(0,0,0,0.04)]
p-5
```

**Hero Card** — most important element on the slide:
```
rounded-2xl bg-white p-10
shadow-[0_2px_8px_rgba(0,0,0,0.06)]
border border-black/[0.04]
/* Often includes a gold accent strip: */
/* absolute left-0 top-8 bottom-8 w-1 rounded-full bg-[#C9A84C] */
```

**Callout Card** — accent-tinted insight box:
```
rounded-xl border border-teal-500/30 bg-teal-500/8 p-4
/* Or amber variant: */
rounded-xl border border-amber-500/20 bg-amber-500/5 p-4
```

### Table Container
```
rounded-xl border border-black/[0.06] overflow-hidden
```
- Header: `bg-white/70 px-4 py-2.5`
- Rows: `px-4 py-2 border-t border-black/[0.06]`
- Highlighted rows: `bg-teal-500/8` with teal text

### Card Rules

1. Border radius: `rounded-xl` (12px) or `rounded-2xl` (16px). Never sharp. Never fully round.
2. Borders: black at 4-6% opacity. Structurally defining but invisible.
3. Shadows: max `rgba(0,0,0,0.06)`. Most use `rgba(0,0,0,0.04)`.
4. No colored backgrounds on standard cards. White only. Accent tints at 5-8% only on callout cards.
5. No colored borders on standard cards. Color borders only on callouts.

### ⚠️ Card Anti-Pattern (The Quality Gap)

**The problem with slides 3–19:** Cards on a blank warm-gray background read as "generic dashboard component." The cards themselves are fine — the issue is that there's nothing else on the slide to create visual interest.

**The fix:** Pair card grids with at least one of:
- An illustration or editorial image (like slide 2's tree)
- A dramatic asymmetric layout (hero card 2x size, dramatic negative space)
- A gold accent element (accent strip, decorative line, compass star)
- An oversized stat number that breaks the card boundary
- A subtle textured or photographic background treatment

---

## 5. Icons

### Library
**Lucide React** v0.575.0 — line-style only.

| Context | Size | Stroke | Container | Color |
|---|---|---|---|---|
| Stat card | `w-5 h-5` | 1.5 | `w-7 h-7 rounded-lg` bg at 15% | Accent or `navy-950/50` |
| Hero card | `w-6 h-6` | 1.8 | `w-12 h-12 rounded-xl` bg at ~8% | Gold `#C9A84C` |
| Label/inline | `w-4 h-4` | 1.5 | None | Same as text |
| Pipeline step | `w-5-6 h-5-6` | 1.5 | Circle or rounded-xl | Section accent |

Rules: Always line-style. Always in a tinted container when leading a card. Container bg = accent at 8-15% opacity.

---

## 6. Data Visualization (ECharts)

### Library
**ECharts** via `echarts-for-react` v6.0.0

### Current Chart Types
- **Stacked bar** (Portfolio Evolution): navy-950 → teal-500 → teal-400 → amber-500
- **Horizontal bar** (Florida TAM): navy/teal/amber by channel type
- **Donut ring** (Confectionery Gap): amber-500 arc, value below

### Chart Styling Rules (Current)
- No borders on bar segments
- Minimal/no grid lines
- Axis labels: `text-xs`, slate-colored
- Charts sit directly on slide — no card wrapper

### Interactive Financial Dashboard (Pro Forma) — Direction

The financial dashboard should follow a **light editorial** direction, consistent with slides 1-2's quality bar. Reasoning: the warm-gray content slides are where the user's data-heavy content lives, and slides 1-2 proved that the light palette with selective accent color creates the most premium feel.

**Visual Principles for the Dashboard:**

1. **The chart IS the visual anchor.** Unlike content slides where we need an illustration to break up cards, a well-designed interactive chart can be the centerpiece. It needs to be *beautiful on its own* — thoughtful color, generous whitespace, smooth transitions.

2. **Light base, selective color.** Background matches the warm gray slide treatment. Charts use the navy/teal/amber palette. The key stat or insight gets gold `#C9A84C` treatment.

3. **Glass card containers for controls.** Input controls (scenario toggles, sliders) live in the same `bg-white/70 backdrop-blur-sm` cards. Interactive elements get the teal accent for affordance.

4. **Generous chart sizing.** Charts should occupy at least 50-60% of the viewport. Don't shrink charts to fit more cards around them. Let the visualization breathe.

5. **Animated transitions.** When inputs change, chart values should animate smoothly (ECharts supports this natively). Count-up numbers for key stats (reuse `useCountUp` hook).

6. **One "hero number" per view.** Whatever the user is looking at — Year 5 revenue, cumulative owner earnings, ROI — one number should be oversized in gold or teal, anchoring the whole layout.

7. **Scenario toggling.** Free / Moderate / Aggressive scenarios should use a clean tab or segmented control (not dropdown). Active scenario gets teal accent, inactive gets slate.

**ECharts Theme Configuration:**
```javascript
const CHART_THEME = {
  backgroundColor: 'transparent',
  color: ['#0F1A2E', '#1B7A8A', '#239BAD', '#3CC0D4', '#E8913A', '#F0A85C'],
  textStyle: {
    fontFamily: 'Inter, system-ui, sans-serif',
    color: '#243356',  // navy-800
  },
  title: {
    textStyle: { fontWeight: 700, fontSize: 16, color: '#0F1A2E' }
  },
  grid: { containLabel: true, left: 20, right: 20, top: 40, bottom: 20 },
  xAxis: {
    axisLine: { lineStyle: { color: '#CBD5E1' } },  // slate-300
    axisLabel: { fontSize: 11, color: '#94A3B8' },   // slate-400
    splitLine: { show: false }
  },
  yAxis: {
    axisLine: { show: false },
    axisLabel: { fontSize: 11, color: '#94A3B8' },
    splitLine: { lineStyle: { color: '#0F1A2E', opacity: 0.06 } }
  },
  tooltip: {
    backgroundColor: '#0F1A2E',
    borderColor: '#2E4068',
    textStyle: { color: '#F5F6FA', fontSize: 12 },
    borderRadius: 8
  },
  legend: {
    textStyle: { fontSize: 11, color: '#64748B' }  // slate-500
  }
}
```

---

## 7. Animation & Motion

### Library
**Motion** (Framer Motion v12.34.3) — imported as `motion/react`

### Element Entrances

| Element | Animation | Duration | Delay |
|---|---|---|---|
| Slide heading | `y: 15 → 0`, opacity | 0.4s | 0.1s |
| Subtitle | opacity only | 0.4s | 0.2s |
| Cards (staggered) | `y: 16-20 → 0`, opacity | 0.45-0.5s | 0.3s + `i × 0.1-0.12s` |
| Table rows | `x: -10 → 0`, opacity | 0.3s | 0.4s + `i × 0.06s` |
| Illustrations / images | opacity | 1.2s | 0.1s |
| Divider accent line | `width: 0 → 60px` | 0.8s | 0.2s |
| Number counters | count-up | 1.2s | 0.6s + stagger |
| Source citations | opacity | 0.4s | 0.8-1.4s (last) |

### Motion Rules

1. Everything fades in. Nothing appears instantly.
2. Vertical movement: 15-20px max. Subtle. Content settles into place.
3. Stagger = reading order. Heading → subtitle → content (L→R, top→bottom) → citations last.
4. No exit animations on individual elements. Only slide-level transition.
5. Easing: smooth deceleration. `[0.25, 0.1, 0.25, 1]` for slides, spring-free for elements.
6. Count-up numbers on stat slides add polish without being flashy.

---

## 8. Navigation

### Progress Bar (bottom-center, fixed)
```
rounded-full bg-navy-900/80 backdrop-blur-md border border-navy-700/50
px-4 py-2.5, z-50
```

### Dots
- Inactive: `w-2 h-2 bg-slate-500/50`
- Active: `w-8 h-2.5` in section color
- Hover: `bg-slate-400/70`
- Transition: `duration-300`

### Section Colors
| Section | Color | Slides |
|---|---|---|
| Opportunity | `teal-500` | 3-9 |
| Strategy | `amber-500` | 10-14 |
| Execution | `amber-400` | 15-18 |
| Unsectioned | `slate-400` | 1-2, 19 |

### Section Dividers
- Gold accent line: 60px wide, 1px, `#C9A84C`
- Title at bottom third of viewport, centered
- Optional background image with heavy gradient: `from-[#e6e6ec] via-[#e6e6ec]/60 to-[#e6e6ec]/30`

---

## 9. Visual Assets — Photography & Illustration

### The Role of Visual Assets

This is the most important section of the design system because it addresses the core quality gap. Slides 1-2 work because they have *curated visual storytelling*. Slides 3-19 fail because they don't.

### Photography Rules
- Used on title slide only (so far). Full-bleed with `bg-navy-950/80` overlay.
- Image reads as texture/atmosphere, not as content to study.
- `object-cover object-bottom` positioning.
- Can be used on section dividers with the warm-gray gradient overlay.

### Illustration Rules
- **Style: hand-drawn / pencil-sketch / editorial.** The tree on slide 2 is the reference. It looks like it belongs in a premium magazine or book, not in a SaaS product.
- **NOT:** stock vector icons, flat illustration, AI-generated generic imagery, clip art, photo collages.
- **Placement:** Large and confident. Minimum 40% of slide width. Bleeds off edge when possible (`-left-[15%]`).
- **One per slide maximum.** Illustrations are visual anchors, not decorations.
- **Conceptually resonant.** The tree = roots = 30-year foundation. Every illustration should carry narrative weight, not just fill space.

### Decorative Elements
- **Compass/star mark:** Appears at bottom of slide 2 as a subtle brand touch. Can be reused as a decorative element.
- **Gold accent lines:** 1px, 40-60px wide, `#C9A84C`. Used on section dividers. Can be used as separators or decorative elements in editorial layouts.
- **All decorative images:** `alt=""` — they are decorative, not informational.

### When a Slide Needs a Visual Anchor (Checklist)

Ask: "If I remove all the data cards, is there anything visually interesting left?"

If no, add one of:
- [ ] An editorial illustration paired with the content (magazine split layout)
- [ ] A hero chart that's beautiful enough to be the centerpiece
- [ ] A dramatically asymmetric layout with oversized typography
- [ ] A subtle photographic texture treatment on the background
- [ ] A gold-accent decorative element that adds editorial polish

---

## 10. Badges, Tags & Status Indicators

### Priority Badges
| Level | Fill | Text | Radius |
|---|---|---|---|
| HIGHEST | Solid amber/orange | White | `rounded-md` |
| HIGH | Solid teal | White | `rounded-md` |
| MEDIUM | Lighter/outlined | Muted | `rounded-md` |

All badges: `text-[10px] font-bold uppercase`

### Type Tags
Small pills: `rounded-md` or `rounded-full`, accent bg at low opacity with matching text. Examples: "Micro-purchase" (teal), "B2B sub-supply" (amber).

### RECOMMENDED Badge
Solid `teal-500`, white text, positioned top-right of the recommended card.

---

## 11. Writing & Content Voice

### Tone
Professional assessment. Buffett-style: direct, no fluff, no hard sell. We present research and let the data make the case. We're honest about what we don't know (Key Questions exist for a reason).

### Headlines
Direct and declarative. "Why Newport Wins", "The B2B Fast Track", "The Blueprint Is Yours". No questions in headlines. No jargon. No filler words.

### Subtitles
One line, plain language, often with an em dash subordinate clause: "Top FL food distributors — Newport enters at the #5-10 tier with superior infrastructure."

### Stat Presentation
The number is always the biggest visual element:
```
$87M                        ← gold/accent, text-4xl+, bold
Florida Federal Food TAM    ← navy-950, semibold, text-xs
Annual addressable market   ← navy-800/50, text-[11px]
```

### Source Citations
Every data slide. Bottom-left. Format: `Source (date) | Source | Source`. `text-[10px] navy-800/35-40`. Nearly invisible but always present.

### Callout Boxes
One to two sentences in an accent-tinted card. Lead with a bold hook: "The creative insight:", "Why this matters:", "Total Entry Cost:".

---

## 12. Using 21st.dev for Visual Inspiration

### Purpose
21st.dev is a reference library for finding premium React component patterns that match the quality bar of slides 1-2. It is NOT a component library to import — it's a visual dictionary for communicating design intent.

### Workflow

1. **Browse 21st.dev** for components or layouts that capture the feel you want
2. **Screenshot or link** the specific component
3. **Share with Claude** alongside the instruction: "This is the visual quality I want for [slide/section]. Match this feel using our design tokens."
4. Claude translates the visual pattern into components using our existing Tailwind tokens, Motion animations, and ECharts config — no external dependencies added

### What to Look For on 21st.dev

- **Dashboard cards** with subtle glass effects, generous whitespace, and premium typography (→ reference for upgrading our stat cards)
- **Data visualization layouts** where the chart is the hero element, not crammed into a small card (→ reference for the financial dashboard)
- **Hero sections** with dramatic typography, editorial layouts, and intentional negative space (→ reference for slides that currently feel like data dumps)
- **Comparison tables** with visual polish beyond basic alternating-row styling (→ reference for competition/risk/recommendation slides)

### What to Avoid on 21st.dev

- Neon/dark-mode SaaS dashboards (too techy for Newport's audience)
- Overly animated components (motion should be subtle per our rules)
- Components with heavy colored gradients (our palette is restrained)
- Anything that feels like a developer tool rather than an editorial presentation

---

## 13. Comprehensive Do's and Don'ts

### DO — Visual Quality
- Pair data with a visual anchor on every slide (illustration, hero chart, dramatic layout)
- Use the magazine split layout (45/55 or 40/60) when a slide has an illustration
- Let hero stats be massive — they should be the first thing the eye hits
- Use gold `#C9A84C` for the single most important element per slide
- Add decorative finishing touches (accent lines, compass star, fine typography details)
- Test: "would this slide look good in a premium business magazine?"

### DO — Technical
- Use navy-950 for headings on light backgrounds
- Use opacity variants of navy-800 for text hierarchy
- Keep cards white with barely-visible borders
- Stagger entrance animations in reading order
- Source-cite every data point
- Use `font-body` (Inter) for everything

### DON'T — Visual Quality
- Leave slides as "heading + grid of white cards on gray" — this is the anti-pattern
- Use stock icons, clip art, or generic AI illustrations as visual anchors
- Treat every slide the same way — the deck needs rhythm (quiet slides, dramatic slides, data slides)
- Add visual interest through color (colored cards, gradients) — add it through layout, imagery, and typography instead
- Skip the visual anchor because "this is just a data slide" — the data IS the story, present it beautifully

### DON'T — Technical
- Add shadows stronger than `rgba(0,0,0,0.06)`
- Use serif fonts for headings
- Use italic, underline, or strikethrough
- Add colored backgrounds to standard cards
- Use more than one illustration per slide
- Skip entrance animations

---

## 14. Slide Structure Reference

### Act 1: The Anchor (Slides 1-2)
- **Slide 1 — Title:** Dark. Full-bleed photo. Massive typography. Gold subtitle. ✅ Quality bar.
- **Slide 2 — The Opportunity:** Light. Magazine split. Tree illustration. Stat cards. Compass star. ✅ Quality bar.

### Act 2: The Market (Slides 3-9)
- Slides 3-9: Data-heavy. Currently cards-only. **Needs visual anchors.**

### Act 3: The Strategy (Slides 10-14)
- Slide 10: Section divider (gold line, centered title). Works well.
- Slides 11-14: Process and relationship content. Currently cards-only. **Needs visual anchors.**

### Act 4: Making It Real (Slides 15-19)
- Slide 15: Section divider. Works well.
- Slides 16-18: Compliance, recommendation, questions. Currently cards-only. **Needs visual anchors.**
- Slide 19: Closing/blueprint. Two-column with subtle accent cards. Close to quality bar but could be elevated.

### Future: Financial Dashboard
- Interactive pro forma model. Light editorial direction. Chart is the visual anchor. Scenario toggling. One hero number per view.

---

## Appendix: Dependencies

```json
{
  "react": "19.2.0",
  "motion": "12.34.3",
  "echarts": "6.0.0",
  "echarts-for-react": "latest",
  "lucide-react": "0.575.0",
  "tailwindcss": "4.2.1",
  "@tailwindcss/vite": "4.2.1",
  "vite": "7.3.1"
}
```

Fonts: Google Fonts — `Playfair Display` (400-700) + `Inter` (300-700), preconnected in `index.html`.
