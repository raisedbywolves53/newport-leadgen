# Slide Fixes — Batch 1 (Slides 4, 6, 7)

> **Context**: Newport Wholesalers government contracting pitch deck. React + Vite + Tailwind + Framer Motion + ECharts. Project at `web/`. Dev server runs on localhost:5174.
> **Design system**: `web/DESIGN-SYSTEM.md` governs all visual decisions for slides 3-19.
> **Locked slides**: 1-2 (don't touch), 3 (quality reference), 5 (approved).

---

## CRITICAL RULES

1. Read `DESIGN-SYSTEM.md` thoroughly before writing any code.
2. Read `src/components/slides/WhyNewportSlide.jsx` (slide 3) as the quality reference — match its card DNA, spacing, typography scale, and animation patterns.
3. Only use gold (`#C9A84C`) and teal (`#1B7A8A`) as accent colors. No amber, no other hues.
4. All cards must use canonical surface: `rounded-2xl bg-white/70 backdrop-blur-sm border border-black/[0.06] shadow-[0_1px_3px_rgba(0,0,0,0.04)]`
5. Slide container: `w-full h-full flex flex-col px-16 lg:px-20 pt-6 pb-20 relative overflow-hidden`
6. Import shared components from `../ui/DecorativeElements` and `../ui/SourceCitation`. Import data from `../../data/market.js` and `../../data/strategy.js`. Never hardcode data that exists in those files.
7. After making changes, run `./node_modules/.bin/vite build --outDir /tmp/newport-build` to verify clean build (ignore chunk size warnings).

---

## Fix 1: Slide 4 — FloridaTamSlide.jsx

**File**: `src/components/slides/FloridaTamSlide.jsx`

**Problem**: The concentric ring colors are too washed out and pale. The $87M center text is white on light rings — low contrast, not crispy. The rings look like faded watercolors rather than a confident data visualization.

**What to change**:

### A. Ring opacity/saturation — much darker and more saturated
Replace the current `ringOpacity` function and ring rendering. The rings should be rich and bold — think Bloomberg terminal data vis, not pastel watercolors.

New approach:
- Outermost ring (State, gold): **opacity 0.45** base, **0.65** hover
- Ring 2 (Education, gold): **opacity 0.55** base, **0.75** hover
- Ring 3 (Micro-Purchase, teal): **opacity 0.60** base, **0.80** hover
- Ring 4 (Federal FPDS, teal): **opacity 0.70** base, **0.88** hover
- Ring 5 innermost (Local, teal): **opacity 0.82** base, **0.95** hover

The visual effect should be: progressively darker/richer toward center, with the innermost ring being nearly solid teal.

### B. $87M center text — dark navy, not white
The center is surrounded by the innermost (darkest) ring. But the text doesn't need to sit ON the dark ring — it sits in the CENTER_R gap. Change center text styling:
- `$87M`: Use `fill: '#C9A84C'` (gold) with `fontSize: '48px'`, `fontWeight: 800`, `letterSpacing: '-0.03em'`. Add a subtle dark text-shadow for depth: `filter: 'drop-shadow(0 2px 4px rgba(15,26,46,0.25))'`
- `Total TAM`: Use `fill: '#0F1A2E'` (navy-950) at `opacity: 0.5`, `fontSize: '10px'`, `fontWeight: 700`
- Also add a white circle behind the center text as a "backdrop": a `<circle>` at CX/CY with `r={CENTER_R}` filled `white` at `opacity: 0.92` — this creates a clean light pad for the gold text to sit on.

### C. Ring gap — slightly wider
Increase `RING_GAP` from 3 to 4px for cleaner visual separation between rings now that they're darker.

### D. Legend dots at bottom — match the darker ring opacities
The legend dot `opacity: 0.6` is too faint now. Set each dot's opacity to match its ring's base opacity from the new values above.

**Do NOT change**: header, card layout on the right, tooltip style, animation timing, or the card hover interactivity. Those are approved.

---

## Fix 2: Slide 6 — ConfectioneryGapSlide.jsx

**File**: `src/components/slides/ConfectioneryGapSlide.jsx`

**Problem**: The slide is too plain and white. The donut chart card is a big empty white box with a tiny chart floating in it. The insight cards on the right are flat monotone tiles that don't tell a story. There's no visual energy, no narrative progression, no sense of "this is a huge opportunity."

**What to redesign — make insight cards into rich stat-story cards**:

The right-column insight cards should NOT be plain text tiles. Each should be a **mini data-story card** inspired by yield-card / animated-chart-card patterns — each card has a prominent stat or data point as the visual anchor, with supporting narrative text below.

### New card structure (right column, 4 cards not 5 — tighten to essentials):

**Card 1 — "The Market"** (standard card):
- Stat: `$55M` in gold, `text-2xl font-bold`
- Label: "National Spend" in `text-[11px] text-navy-800/40 uppercase tracking-wide`
- Detail: "Only $412K currently captured in Florida — massive whitespace." in `text-[13px] text-navy-800/65`

**Card 2 — "The Opportunity"** (standard card):
- Stat: `1.6` in teal, `text-2xl font-bold`
- Label: "Avg Offers per Award" in same style
- Detail: "Most solicitations attract one or two bids. Low competition by design."

**Card 3 — "The Advantage"** (hero card — `bg-white` full opacity, gold left accent strip):
- Stat: `Segment E` in gold, `text-xl font-bold`
- Label: "Newport Core Competency"
- Detail: "Existing wholesale pricing and supplier relationships translate directly to government bids."
- This is the hero card because it's the "so what" — why Newport specifically wins here.

**Card 4 — "The Moat"** (standard card):
- Stat: `LPTA` in navy-950, `text-xl font-bold`
- Label: "Evaluation Method"
- Detail: "Lowest Price Technically Acceptable — directly favors wholesale distributors with volume pricing."

### Left column improvements:
- The donut chart card should be taller — give the chart `w-64 h-64` (not w-56 h-56) so it's a more commanding visual anchor
- Center the donut label overlay properly using absolute positioning at the true center of the chart container, not negative margin hacks
- Below the chart in the same card, add a horizontal stat row: "58% Sole Source" (gold, bold) on the left, and "42% Competitive" (navy-800/40, lighter) on the right — like a legend/callout bar. Use a subtle top border to separate from chart.
- The "45 National Awards" card below should have a teal icon pill (use `Award` from lucide-react) to the left of the stat, matching WhyNewportSlide's StatCard icon treatment: `w-9 h-9 rounded-lg bg-[#1B7A8A15] flex items-center justify-center`

### Source citation:
Use inline source at bottom like slide 3 (not `SourceCitation` component — match slide 3's pattern with `motion.p` and `CompassStar`).

---

## Fix 3: Slide 7 — CompetitionSlide.jsx

**File**: `src/components/slides/CompetitionSlide.jsx`

**Problem**: The table needs to be more pronounced with better visual hierarchy. Looking at the reference screenshots (Looker Studio tables, task management tables), the table rows need: clearer column widths, bolder row differentiation, status/tier badges, and a stronger Newport callout.

**What to change**:

### A. Table header — bolder
- Header row: add `bg-navy-950/[0.03]` background for slight contrast
- Header text: keep `text-[11px] font-semibold uppercase tracking-wider text-navy-800/40` but add `py-3.5` for more breathing room

### B. Table rows — more differentiated
- Row height: increase padding to `py-3.5` (from py-3)
- **Top tier rows (Oakes, US Foods)**: Add a subtle gold left border `border-l-[3px]` with `border-l-[#C9A84C]`. Company name in `font-semibold text-navy-950`. Amount in gold bold.
- **Mid tier rows (JNS, Sysco)**: Teal left border. Amount in `text-navy-950 font-semibold`.
- **Target tier rows (#5-8)**: Standard (no colored border or use very subtle navy-800/10). Amount in `text-navy-800/60`.
- Add a **tier badge** after the company name for top-tier companies: a small inline pill `bg-[#C9A84C]/10 text-[#C9A84C] text-[10px] font-semibold px-2 py-0.5 rounded-full ml-2` saying "Top Tier" for ranks 1-2, `bg-[#1B7A8A]/10 text-[#1B7A8A]` saying "Mid Tier" for ranks 3-4.
- Even/odd row striping: even rows `bg-white/40`, odd rows `bg-transparent`

### C. Newport callout row — make it unmissable
Current callout is okay but needs to be stronger:
- Full-width row inside the table (not a separate card below)
- Background: `bg-[#1B7A8A]/[0.06]`
- Left border: gold `#C9A84C` 4px
- Company name "Newport Wholesalers" in bold teal with a gold "Entry Point" badge pill after it
- Amount: "$1-5M" in gold bold
- Notes: "30-year track record · Plantation, FL · Superior cold chain infrastructure" — more detail

### D. Column widths — rebalance
Change grid template to `grid-cols-[48px_1.2fr_110px_1fr]` — slightly narrower rank, wider company name for badges.

### E. Add a compact context line above the table
Between the hero stats and the table card, add a single subtle line: `"8 tracked FL food distributors by federal contract value"` in `text-[12px] text-navy-800/40 mb-3` — frames what the table shows.

---

## Execution order

1. Fix slide 4 (FloridaTamSlide.jsx)
2. Fix slide 6 (ConfectioneryGapSlide.jsx)
3. Fix slide 7 (CompetitionSlide.jsx)
4. Run `./node_modules/.bin/vite build --outDir /tmp/newport-build` to verify clean build
5. Confirm dev server at localhost:5174 reflects changes (hot reload should handle this)

---

## What NOT to touch
- Slides 1, 2, 3, 5 — locked/approved
- Slide 8 (HowItWorksSlide) — already redesigned, no feedback yet
- Navigation, SlideContainer, PasswordGate, App.jsx
- Data files (market.js, strategy.js) — read-only
- DecorativeElements.jsx, SourceCitation.jsx — shared components, don't modify
