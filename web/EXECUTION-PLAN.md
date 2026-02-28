# Execution Plan: Presentation Rebuild

> **Goal**: Rebuild slides 3–17 to match the shadcn-aligned DESIGN-SYSTEM.md in 5 batches of 3 slides.
> **Executor**: Claude CLI in VSCode
> **Reviewer**: Cowork (visual QA via screenshots)

---

## Pre-Build: Foundation Work (Run FIRST)

Before touching any slides, these global changes must be applied:

### Step 1: Replace the design system file
- Delete the old `web/DESIGN-SYSTEM.md`
- Copy the new version from `web/DESIGN-SYSTEM-SHADCN.md` (or overwrite with the uploaded content)
- The new file is the ONLY design authority going forward

### Step 2: Update CSS tokens in `web/src/index.css`
The `@theme` block needs these changes to align with the new system:

**Slide background**: `#e6e6ec` → `#f4f4f5` (zinc-100)

**Add zinc scale tokens** (if not present):
```css
--color-zinc-50: #fafafa;
--color-zinc-100: #f4f4f5;
--color-zinc-200: #e4e4e7;
--color-zinc-300: #d4d4d8;
--color-zinc-400: #a1a1aa;
--color-zinc-500: #71717a;
--color-zinc-600: #52525b;
--color-zinc-700: #3f3f46;
--color-zinc-800: #27272a;
--color-zinc-900: #18181b;
--color-zinc-950: #09090b;
```

Keep existing navy/teal/amber/gold tokens — they're still used for accent colors. The zinc scale handles all neutral surfaces and text.

### Step 3: Update shared components
- **SourceCitation.jsx**: Change `text-navy-800/35` → `text-zinc-300`
- **DecorativeElements.jsx**: No changes needed (gold accents stay)
- **SlideBackground** (wherever it sets `#e6e6ec`): Change to `#f4f4f5`

### Step 4: Add missing data to strategy.js
Slide 12 (BD Strategy) needs influence layers and process steps that don't exist yet. Add to `strategy.js`:

```javascript
export const INFLUENCE_LAYERS = [
  {
    role: 'Contracting Officers',
    description: 'Control the formal procurement process — RFQs, evaluations, awards.',
    stat: 'Decision authority',
    color: 'teal',
  },
  {
    role: 'Program Managers',
    description: 'Define requirements and evaluate vendor capability. Budget owners.',
    stat: 'Requirement setters',
    color: 'teal',
  },
  {
    role: 'Front-Line Influencers',
    description: 'Kitchen managers, food service directors, nutrition staff. They know what they need and recommend vendors.',
    stat: 'Newport\'s entry point',
    color: 'gold',
  },
]

export const BD_PROCESS_STEPS = [
  { step: 1, title: 'Identify Facilities', description: 'Map federal and state facilities within delivery range.' },
  { step: 2, title: 'Research Requirements', description: 'Pull current contracts, expiration dates, incumbent vendors.' },
  { step: 3, title: 'Engage Front-Line', description: 'Visit food service directors. Bring samples. Build relationships.' },
  { step: 4, title: 'Position for Recompete', description: 'When contracts expire, Newport is already a known quantity.' },
  { step: 5, title: 'Win & Expand', description: 'Win first micro-purchase. Use past performance to bid larger contracts.' },
]
```

---

## Data Clarifications (hardcode these values)

| Slide | Issue | Resolution |
|-------|-------|------------|
| 11 (Portfolio Evolution) | Hero stat "78" vs data showing "255" | Use **78** — this is the conservative model from the original v7 Excel. The 255 figure is the aggressive scenario. |
| 13 (Risk & Compliance) | Entry cost "$4K" vs sum "$4-31.5K" | Use **"$4K–$31.5K"** as the range. "$4K" is the minimum (SAM + MFMP only). |
| 16 (B2B Fast Track) | Sales cycle "2–8 weeks" not in data | Hardcode as hero stat — it's from industry research, not a database field. |

---

## Batch Execution Order

### Batch 1: Slides 3–5 (Global Refresh)
**What changes**: Migrate from old card/color system to shadcn-aligned system.
- Card surfaces: `rounded-2xl bg-white/70 backdrop-blur-sm border-black/[0.06]` → `rounded-xl bg-white border-zinc-200 shadow-sm`
- Text colors: `navy-800/XX` → zinc scale
- Padding: `p-5` → `p-6`
- Grid gap: `gap-5` → `gap-4`
- Headlines: `font-bold` → `font-semibold`
- Stat sizes: `text-7xl` → `text-6xl`, `text-3xl` → `text-2xl`
- Icon containers: `rounded-lg bg-[accent]15` → `rounded-md bg-zinc-100`
- Slide container: Add `justify-center`, use `pb-16` not `pb-20`
- Slides 4 and 5 already have charts — keep those, just update surface styling
- Slide 4: Confirm hover interactivity on concentric rings works after migration

### Batch 2: Slides 6–8
**Slide 6 (Confectionery Gap)**: Dashboard Pattern A — donut chart (hero card, left) + 3 stat tiles (right). Use template 6.2.2 from design system. Data: `PRODUCT_TIERS.tier1[0]`.
**Slide 7 (Competition)**: Dashboard Pattern C — horizontal bar chart (hero card) + hero stat card top, full-width table below. Data: `COMPETITORS`.
**Slide 8 (How It Works)**: Process flow — pipeline badges in hero card + 4 sourcing channel cards below. Data: `PIPELINE_STAGES`, `SOURCING_CHANNELS`.

### Batch 3: Slides 9–11
**Slide 9 (Target Agencies)**: Dashboard Pattern A — horizontal bar chart (hero) + 4 stat tiles. Data: `TARGET_AGENCIES`.
**Slide 10 (Real Contracts)**: Dashboard Pattern C — 3 compact stat tiles top + full-width table. Data: `CONTRACT_EXAMPLES`.
**Slide 11 (Portfolio Evolution)**: Dashboard Pattern A — stacked bar chart (hero, template 6.2.5) + 3 stat tiles. Data: `PORTFOLIO_EVOLUTION` from financials.js. Hero stat: 78.

### Batch 4: Slides 12–14
**Slide 12 (BD Strategy)**: Two-column — 3 influence layer cards with chevron connectors (left) + numbered timeline (right) + insight callout. Data: `INFLUENCE_LAYERS`, `BD_PROCESS_STEPS` (added in Step 4).
**Slide 13 (Risk & Compliance)**: Dashboard stat comparison — 2 hero stat cards top + two-column required vs not-required. Data: `COMPLIANCE_REQUIRED`, `COMPLIANCE_NOT_NEEDED`.
**Slide 14 (Recommendation)**: Two recommendation cards + comparison table. Data: `ROUTE_COMPARISON`.

### Batch 5: Slides 15–17 + Dividers
**Slide 15 (Key Questions)**: Category groups — 3 category cards containing question rows. Data: `KEY_QUESTIONS`.
**Slide 16 (B2B Fast Track)**: Dashboard Pattern C — horizontal bar chart + hero stat + table. Data: `B2B_TARGETS`.
**Slide 17 (Blueprint)**: Split narrative — teal panel (Newport) + gold panel (Still Mind) + center connector. Data: `RESPONSIBILITIES.partnership`.
**Divider slides**: Update to match new zinc text colors and GoldLine width (48px).

---

## Quality Gate (after each batch)

Run this checklist before moving to the next batch:

1. `npm run build` — zero errors
2. Visual asset present on every data slide (6+)
3. Only gold and teal accents — no stray colors
4. All cards use `rounded-xl bg-white border-zinc-200 shadow-sm`
5. Charts inside cards with compact legend below
6. Text hierarchy: zinc-950 headlines, zinc-600 body, zinc-400 captions
7. Source citation on every data slide
8. Animation budget under 1.5 seconds
9. Slide background is `#f4f4f5`
10. No text smaller than 11px

---

## File Cleanup (after all batches complete)

- Delete `SLIDE-FIXES-BATCH1.md`
- Delete `SLIDE-FIXES-BATCH2.md`
- Delete `EXECUTION-PLAN.md` (this file)
- Delete any duplicate design system files (keep only `DESIGN-SYSTEM.md`)
- Run final `npm run build` to confirm clean output
