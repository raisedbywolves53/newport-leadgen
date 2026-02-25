# Newport GovCon Presentation — Visual Design Reference

**Theme Name:** Midnight Executive
**Last Updated:** February 25, 2026
**Applies to:** Web presentation at `/web/` (Vite + React + Tailwind v4)

---

## 1. Color Palette

### Primary Colors

| Token | Hex | Usage |
|---|---|---|
| `navy-950` | `#0F1A2E` | Slide background (dark mode), primary heading text (light mode), deepest layer |
| `navy-900` | `#1A2744` | Navigation bar background, secondary dark surfaces |
| `navy-800` | `#243356` | Body text (with opacity), used at `/60` or `/70` for readable-but-quiet copy |
| `navy-700` | `#2E4068` | Borders in dark contexts, scrollbar thumb, subtle dividers |
| `navy-600` | `#3A5080` | Lighter navy accents (rarely used) |

### Accent Colors

| Token | Hex | Role |
|---|---|---|
| `teal-500` | `#1B7A8A` | **Primary accent.** Section labels, stat accents, highlighted data, "opportunity" section color |
| `teal-400` | `#239BAD` | Lighter teal for hover states, secondary teal highlights, competitor callouts |
| `teal-300` | `#3CC0D4` | Lightest teal — callout text on teal-tinted backgrounds |
| `amber-500` | `#E8913A` | **Secondary accent.** "Strategy" section color, chart segments, warm emphasis |
| `amber-400` | `#F0A85C` | "Execution" section color, chart elements, lighter warm accent |
| `amber-300` | `#F5C080` | Lightest amber — icon backgrounds at low opacity |

### Signature Colors

| Hex | Name | Usage |
|---|---|---|
| `#C9A84C` | **Gold** | Premium accent. Title slide subtitle, section divider accent lines, hero stat numbers, icon tints on hero cards. This is the presentation's signature "editorial" color. |
| `#9CA0A4` | Footer gray | Credit/attribution text on dark backgrounds |

### Neutrals

| Token | Hex | Usage |
|---|---|---|
| `offwhite` | `#F5F6FA` | Default text on dark backgrounds, base body color |
| `slate-300` | `#CBD5E1` | Light text accents |
| `slate-400` | `#94A3B8` | Navigation counter text, muted labels |
| `slate-500` | `#64748B` | Inactive navigation dots |
| `white` | `#FFFFFF` | Card backgrounds (often at `/70` opacity for glass effect) |
| `black` | `#000000` | Used only at very low opacity for borders (`/[0.04]`, `/[0.06]`) and shadows |

### Background Contexts

The presentation has two distinct background modes:

**Dark mode** (Title slide only): `navy-950` (`#0F1A2E`) with 80% overlay on photography. Text is white/offwhite. Subtitle is gold.

**Light mode** (All other slides): A warm gray approximately `#E2E2E8` to `#E6E6EC`. This is not a named token — it comes from the slide container's visual treatment. Text is `navy-950` for headings, `navy-800/60` for body copy. Cards are white.

---

## 2. Typography

### Font Stack

| Role | Font | Weights Loaded | Tailwind Class |
|---|---|---|---|
| **Display / Decorative** | Playfair Display | 400, 500, 600, 700 | `font-display` |
| **Body / UI** | Inter | 300, 400, 500, 600, 700 | `font-body` |

**Important:** The presentation uses Inter (`font-body`) for almost everything — headings, body, stats, labels. Playfair Display (`font-display`) is available but reserved. The overall look is clean sans-serif with tight tracking, not decorative serif.

### Type Scale (as rendered)

| Element | Size | Weight | Tracking | Line Height | Color |
|---|---|---|---|---|---|
| **Title slide H1** | `text-7xl` / `text-9xl` | 700 (bold) | `tracking-tight` | `leading-none` | White `#FFFFFF` |
| **Title slide subtitle** | `text-base` (16px) | 400 | `tracking-[0.2em]` | Normal | Gold `#C9A84C`, uppercase |
| **Slide heading (H2)** | `text-3xl` / `text-4xl` | 700 (bold) | `tracking-tight` | 1.25 | `navy-950` |
| **Section divider heading** | `text-4xl` / `text-5xl` | 700 (bold) | `tracking-tight` | 1.25 | `navy-950` |
| **Slide subtitle** | `text-base` (16px) | 400 | Normal | 1.625 | `navy-800/60` |
| **Category label** | `text-xs` (12px) | 600 | `tracking-widest` | Normal | `teal-500`, uppercase |
| **Card headline** | `text-base` to `text-xl` | 600 | Normal | 1.4 | `navy-950` |
| **Card body** | `text-sm` to `text-[15px]` | 400 | Normal | `leading-relaxed` | `navy-800/65` to `/70` |
| **Hero stat number** | `text-4xl` to `text-7xl` | 700 (bold) | `tracking-tighter` to `tracking-tight` | `leading-none` | Gold `#C9A84C` or accent color |
| **Stat unit label** | `text-[11px]` to `text-lg` | 500 | `tracking-wide`, uppercase | Normal | `navy-800/35` to `/40` |
| **Table header** | `text-xs` (12px) | 600 | Normal | Normal | `navy-800/60` |
| **Table cell** | `text-sm` (14px) | 400 | Normal | Normal | `navy-800` or accent |
| **Source citation** | `text-[10px]` | 400 | Normal | Normal | `navy-800/35` to `/40` |
| **Nav counter** | `text-xs` | 400 | `tabular-nums` | Normal | `slate-400` |
| **Footer credit** | `text-sm` | 400 | `tracking-[0.2em]`, uppercase | Normal | `#9CA0A4` |

### Typography Rules

1. **Headings never use serif.** All headings are Inter bold with tight tracking.
2. **Uppercase is reserved** for category labels (`tracking-widest`), unit labels (`tracking-wide`), the title subtitle (`tracking-[0.2em]`), and footer credits.
3. **Opacity controls hierarchy.** Rather than using lighter font weights or gray colors, the system uses navy-800 at varying opacities: `/70` for readable body, `/60` for subtitles, `/50` for supporting detail, `/40` for metadata, `/35` for source citations.
4. **Stat numbers are oversized.** They break the normal type scale intentionally — `text-3xl` minimum, up to `text-7xl` for hero stats. Always bold, always accent-colored.
5. **No italic text** anywhere in the presentation.
6. **Antialiasing is always on:** `-webkit-font-smoothing: antialiased`.

---

## 3. Spacing & Layout

### Slide Container

- **Max width:** `max-w-7xl` (80rem / 1280px) centered with `mx-auto`
- **Horizontal padding:** Responsive — `px-8` (mobile) → `px-16` (md) → `px-24` (lg) for standard slides. Some custom slides use `px-20` or `px-16`.
- **Vertical padding:** `py-12`
- **Content alignment:** `flex flex-col justify-center` — content is vertically centered in the viewport

### Common Spacing Values

| Use Case | Value | Tailwind |
|---|---|---|
| Gap between cards in a grid | 16-20px | `gap-4` to `gap-5` |
| Heading to subtitle | 8px | `mb-2` |
| Subtitle to content block | 32px | `mb-8` |
| Inside cards (padding) | 16-40px | `p-4` to `p-10` (varies by card importance) |
| Icon container to label | 12px | `gap-3` |
| Stat number to description | 8-12px | `mb-2` to `mb-3` |
| Source citation from bottom | 16px | `bottom-4` |
| Between stacked items | 4-8px | `gap-1` to `gap-2` |
| Section divider bottom padding | 96px | `pb-24` |

### Grid Patterns

**Bento grid (WhyNewport slide):** `grid-cols-[1fr_1fr] grid-rows-[1fr_1fr_1fr]` — hero card spans 2 rows on left, 3 smaller cards stack on right. Height fixed at 460px.

**2×2 stat grid (Executive Summary):** `grid-cols-2 gap-4`

**4-column pipeline (How It Works):** 5 step indicators in a row with arrow separators, then 4 content cards below

**2-column comparison (Risk, Recommendation, Blueprint):** Side-by-side columns with distinct visual treatments per column

**Split layout (Executive Summary):** `grid grid-cols-[45%_55%]` — illustration left, content right

---

## 4. Card & Surface Styles

### Standard Content Card

```
rounded-2xl bg-white/70 backdrop-blur-sm
border border-black/[0.06]
shadow-[0_1px_3px_rgba(0,0,0,0.04)]
p-5
```

This is the workhorse card. White at 70% opacity with a hair-thin border and almost imperceptible shadow. The glass effect (`backdrop-blur-sm`) is subtle — it reads as a clean white card on the warm gray background.

### Hero Card

```
rounded-2xl bg-white p-10
shadow-[0_2px_8px_rgba(0,0,0,0.06)]
border border-black/[0.04]
```

Bigger padding, slightly stronger shadow, fully opaque white. Used for the most important stat on a slide. Often includes a **gold accent strip** on the left edge: `w-1 rounded-full` in `#C9A84C`.

### Accent-Tinted Card (Callout)

```
rounded-xl border border-teal-500/30 bg-teal-500/8 p-4
```

Used for callout boxes and highlighted recommendations. The tint is extremely subtle (8% opacity). Also appears in amber: `border-amber-500/20 bg-amber-500/5`.

### Table Container

```
rounded-xl border border-black/[0.06] overflow-hidden
```

Header row: `bg-white/70 px-4 py-2.5`
Body rows: `px-4 py-2 border-t border-black/[0.06]`
Highlighted rows (competitors): `bg-teal-500/8` with teal-colored text

### Card Rules

1. **Border radius is always `rounded-xl` (12px) or `rounded-2xl` (16px).** Never sharp corners, never full-round except pills/badges.
2. **Borders are black at 4-6% opacity** — barely visible but structurally defining.
3. **Shadows are minimal.** The strongest shadow in the system is `0_2px_8px_rgba(0,0,0,0.06)`. Most cards use `0_1px_3px_rgba(0,0,0,0.04)` or no shadow at all.
4. **No colored borders on standard cards.** Color borders only appear on accent-tinted callout cards.
5. **Cards never have colored backgrounds** (other than white or very subtle accent tints at 5-8% opacity).

---

## 5. Icon System

### Library
**Lucide React** (`lucide-react` v0.575.0) — line-style icons with consistent stroke weight.

### Icon Styling Rules

| Context | Size | Stroke Width | Container | Color |
|---|---|---|---|---|
| Stat card icon | `w-5 h-5` | 1.5 | `w-7 h-7 rounded-lg` with accent at 15% opacity bg | Accent color or `navy-950/50` |
| Hero card icon | `w-6 h-6` | 1.8 | `w-12 h-12 rounded-xl` with accent at ~8% opacity bg | Gold `#C9A84C` |
| Category/label icon | `w-4 h-4` | 1.5 | None | Same as label text color |
| Pipeline step icon | `w-5 h-5` to `w-6 h-6` | 1.5 | Full circle or rounded-xl container | Section accent color |

### Icon Rules

1. **Always line-style** (never filled/solid variants).
2. **Always inside a tinted container** when appearing at the start of a card or stat. The container background is the accent color at 8-15% opacity.
3. **Icon containers use `rounded-lg` (8px) or `rounded-xl` (12px)** — matching the card radius but smaller.
4. **Color matches the stat or section accent** — gold for hero elements, teal for data/opportunity, amber for strategy.

---

## 6. Data Visualization

### Chart Library
**ECharts** (`echarts-for-react` v6.0.0)

### Chart Color Sequence
Charts use the same accent palette: navy-950 (darkest bars), teal-500/400 (mid values), amber-500/400 (highlights/renewals).

### Bar Chart Rules (Portfolio Evolution, Florida TAM)
- Bars have no border/outline
- Stacked bar segments use the 4-color sequence: navy-950 → teal-500 → teal-400 → amber-500
- Axis labels are small (`text-xs`), slate-colored
- Grid lines are minimal or absent
- The chart sits directly in the slide with no card wrapper

### Donut/Ring Chart (Confectionery Gap)
- Single-value ring with amber-500 fill and transparent remainder
- Stat value displayed below in accent color

---

## 7. Animation & Motion

### Library
**Motion** (Framer Motion v12.34.3, imported as `motion/react`)

### Slide Transitions

```javascript
// Slide enter/exit
x: direction > 0 ? '8%' : '-8%'  // Horizontal shift
opacity: 0 → 1
duration: 0.4s
ease: [0.25, 0.1, 0.25, 1]  // Cubic bezier (smooth deceleration)
```

### Element Entrance Animations

| Element | Animation | Duration | Delay |
|---|---|---|---|
| Slide heading | Fade up (`y: 15 → 0`) | 0.4s | 0.1s |
| Subtitle | Fade in | 0.4s | 0.2s |
| Cards (staggered) | Fade up (`y: 16-20 → 0`) | 0.45-0.5s | Base 0.3s + `index * 0.1-0.12s` |
| Table rows (staggered) | Fade from left (`x: -10 → 0`) | 0.3s | Base 0.4s + `index * 0.06s` |
| Source citations | Fade in | 0.4s | 0.8-1.4s (last element) |
| Section divider accent line | Width expand (`width: 0 → 60px`) | 0.8s | 0.2s |
| Background images | Fade in | 1.2s | 0.1s |
| Number counters | Count up animation | 1.2s | 0.6s + stagger |

### Motion Rules

1. **Everything fades in** — no element appears instantly.
2. **Vertical movement is subtle** — 15-20px maximum. Never bouncy or overshooting.
3. **Stagger creates reading order** — heading first, then subtitle, then content cards left-to-right/top-to-bottom, then source citations last.
4. **No exit animations on individual elements** — only the slide-level transition handles exit.
5. **Easing is always smooth deceleration** — content "settles into place."
6. **Count-up numbers** are used on stat slides to add dynamism without being flashy.

---

## 8. Navigation

### Progress Bar
- **Position:** Fixed, bottom-center (`bottom-6`), full z-index (`z-50`)
- **Container:** `rounded-full bg-navy-900/80 backdrop-blur-md border border-navy-700/50`
- **Padding:** `px-4 py-2.5`

### Dot Indicators
- **Inactive:** `w-2 h-2 rounded-full bg-slate-500/50`
- **Active:** `w-8 h-2.5 rounded-full` in section color (see below)
- **Hover:** `bg-slate-400/70`
- **Transition:** `transition-all duration-300`

### Section Colors in Navigation

| Section | Color | Slides |
|---|---|---|
| Opportunity | `bg-teal-500` | Slides 3-9 |
| Strategy | `bg-amber-500` | Slides 10-14 |
| Execution | `bg-amber-400` | Slides 15-18 |
| Unsectioned | `bg-slate-400` | Slides 1-2, 19 |

### Section Dividers (between acts)
- Extra margin on dots: `mx-1`
- Slide type: Centered text at bottom of viewport
- Gold accent line above title: 60px wide, 1px height, `#C9A84C`
- Gradient overlay on background images: `from-[#e6e6ec] via-[#e6e6ec]/60 to-[#e6e6ec]/30` (bottom to top)

---

## 9. Photography & Illustration

### Title Slide Background
- Full-bleed aerial photograph of port/warehouse operations with Newport Wholesalers branding visible
- **Heavy overlay:** `bg-navy-950/80` — the image is visible but dark, reading as texture not content
- Image positioned with `object-cover object-bottom`

### Illustration (Executive Summary)
- Pencil-sketch style tree illustration (roots visible — symbolizing deep history/foundation)
- Positioned on left 45% of slide at 90% height
- Offset: `-left-[15%]` to bleed off the edge
- Fades in slowly (1.2s)

### Image Rules

1. **Photography is used exactly once** (title slide) and is heavily overlaid to avoid competing with text.
2. **Illustrations are editorial, hand-drawn style** — not stock vector art, not photographic.
3. **All images have `alt=""`** — they are decorative, not informational.
4. **Background images on section dividers** are optional and receive a heavy gradient overlay (`from-[#e6e6ec]`) so text remains readable.
5. **No inline images, logos, or diagrams** in content slides. Data is presented through cards, tables, and charts — never infographics or decorative illustrations.

---

## 10. Badge & Tag Patterns

### Priority Badges (Key Questions slide)

| Level | Style |
|---|---|
| HIGHEST | Solid amber/orange fill, white text, `rounded-md`, `text-[10px] font-bold uppercase` |
| HIGH | Solid teal fill, white text |
| MEDIUM | Outlined/lighter fill, muted text |

### Type Tags (Contract Examples)

Small pill badges: `rounded-md` or `rounded-full`, teal or amber background at low opacity with matching text. Example: "Micro-purchase", "Simplified / SLED", "B2B sub-supply".

### "RECOMMENDED" Badge

Appears on the Recommendation slide: solid teal-500 pill with white text, positioned top-right of the recommended card.

---

## 11. Writing & Content Style

### Headline Pattern
Slide headings are direct and declarative: "Why Newport Wins", "The B2B Fast Track", "The Blueprint Is Yours". No questions, no jargon, no filler.

### Subtitle Pattern
One-line summaries that set context: always plain language, often with an em dash for a subordinate clause. Example: "Top FL food distributors — Newport enters at the #5-10 tier with superior infrastructure."

### Stat Presentation
Large number + small unit label + one-line explanation. The number is always the visual anchor. Example:
```
$87M          ← accent-colored, oversized
Florida Federal Food TAM   ← label, semibold, small
Annual addressable market, all PSC 89xx categories under $350K   ← detail, muted
```

### Source Citations
Every data slide has a source citation pinned to the bottom-left. Format: `API/Source Name (date) | Second Source | Third Source`. Font size 10px, nearly invisible (`navy-800/35`).

### Callout Boxes
Short insight paragraph in an accent-tinted card. Usually start with a bold lead-in like "The creative insight:" or "Why this matters:" followed by one to two sentences.

---

## 12. Do's and Don'ts

### DO
- Use navy-950 for headings on light backgrounds
- Use opacity variants of navy-800 for text hierarchy (not different gray colors)
- Keep cards white with barely-visible borders
- Stagger entrance animations in reading order
- Use gold (#C9A84C) sparingly for premium moments
- Source-cite every data point
- Let stat numbers be the biggest element on any card

### DON'T
- Use colored card backgrounds (keep cards white/near-white)
- Add drop shadows stronger than `rgba(0,0,0,0.06)`
- Use serif fonts for headings or body copy
- Add decorative borders, gradients, or patterns to cards
- Make icons larger than their containers suggest
- Use italic, underline, or strikethrough text
- Add more than one illustration per slide
- Skip the entrance animation — every element should fade in

---

## Appendix: Tailwind Theme Block (Source of Truth)

```css
@theme {
  --color-navy-950: #0F1A2E;
  --color-navy-900: #1A2744;
  --color-navy-800: #243356;
  --color-navy-700: #2E4068;
  --color-navy-600: #3A5080;
  --color-teal-500: #1B7A8A;
  --color-teal-400: #239BAD;
  --color-teal-300: #3CC0D4;
  --color-amber-500: #E8913A;
  --color-amber-400: #F0A85C;
  --color-amber-300: #F5C080;
  --color-offwhite: #F5F6FA;
  --color-slate-300: #CBD5E1;
  --color-slate-400: #94A3B8;
  --color-slate-500: #64748B;

  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'Inter', system-ui, sans-serif;
}
```

### Non-Token Colors (hardcoded in components)

| Hex | Where Used |
|---|---|
| `#C9A84C` | Gold accent — title subtitle, section divider lines, hero stat numbers, hero card accent strips |
| `#9CA0A4` | Footer credit text on dark background |
| `#E6E6EC` | Section divider gradient overlay base |
