# Financial Slides Build — Claude CLI Execution Guide

> **Purpose:** Add 2 interactive financial slides to the Newport GovCon web presentation.
> **Stack:** React 19 + Vite 7.3 + Tailwind CSS 4.2 + ECharts 6 + Motion
> **Working directory:** `newport-leadgen/web/`

---

## Pre-Read (Do This First)

Before writing ANY code, read these files to understand the data, assumptions, and patterns:

```
govcon/docs/research.md          — TAM, win rates, competition density, contract values
govcon/docs/strategy.md          — cost breakdowns, company profile, entry strategy
govcon/docs/phases/PHASE-4-FINANCIALS.md — financial model spec
.claude/commands/rebuild-proforma.md     — scenario definitions, win rate methodology
web/src/data/market.js           — existing market data exports (pattern reference)
web/src/data/strategy.js         — existing strategy data exports (pattern reference)
web/src/data/slides.js           — slide registry (you'll modify this)
web/src/App.jsx                  — component registration (you'll modify this)
web/src/components/slides/PortfolioEvolutionSlide.jsx — ECharts integration pattern
web/src/components/ui/DecorativeElements.jsx          — reusable UI components
```

---

## Design System Reference

- **Palette:** zinc base + Gold `#C9A84C`, Teal `#1B7A8A`, Light Teal `#239BAD`, Orange `#E8913A`
- **Card pattern:** `rounded-xl bg-white border border-zinc-200 shadow-sm`
- **Bottom padding:** Always use `pb-14` on slide outer container (progress bar clearance)
- **Animations:** Motion for enter/exit transitions, ECharts built-in for chart animations
- **ECharts pattern:** `useRef` for DOM node, `useEffect` for init/update, window resize handler, `chart.setOption()` for reactive updates

---

## Step 1 — Create `/web/src/data/financials.js`

Pure computation engine. No React, no UI — just math.

### Export: `computeProForma(scenarioKey, overrides)`

**Scenarios (scenarioKey = 'conservative' | 'moderate' | 'aggressive'):**

| Parameter | Conservative | Moderate | Aggressive |
|---|---|---|---|
| Annual tool cost | $0 (free only) | $13,000/yr | $13,000/yr |
| Bids per month | 1.5 | 3 | 5 |
| Avg contract value | $8,000 (micro only) | $25,000 (mixed tiers) | $40,000 (mixed + SLED) |
| Win rate Y1 (months 1-6) | 15% | 20% | 25% |
| Win rate Y1 (months 7-12) | 25% | 30% | 35% |
| Win rate Y2 | 30% | 35% | 40% |
| Win rate Y3-5 | 30% | 40% | 45% |
| Admin cost/yr | $0 (DIY) | $15,000 | $25,000 |

**Overrides (sliders):**
- `grossMargin`: 0.08–0.15, default 0.11
- `bidVolumeMultiplier`: 0.5–2.0, default 1.0
- `winRateAdjustment`: -0.10 to +0.10, default 0.0

**Key assumptions (hardcoded from research):**
- 70% contract renewal rate (compounds yearly)
- Contract tiers: Micro $8K avg, Simplified $50K, SLED $75K, Sealed Bid $150K
- Platform costs breakdown: CLEATUS $3K + HigherGov $3.5K + GovSpend $6.5K = $13K/yr
- COGS = revenue × (1 - grossMargin)

**Return shape:**
```js
{
  scenario: 'moderate',
  overrides: { grossMargin: 0.11, bidVolumeMultiplier: 1.0, winRateAdjustment: 0 },
  years: [
    {
      year: 1,
      bidsSubmitted: 36,
      newWins: 9,
      renewals: 0,
      activeContracts: 9,
      revenue: 225000,
      cogs: 200250,
      grossProfit: 24750,
      toolCost: 13000,
      adminCost: 15000,
      netIncome: -3250,
      cumulativeRevenue: 225000,
      roi: -0.12,
    },
    // ... years 2-5
  ],
  summary: {
    breakevenYear: 2,        // first year with positive net income
    y5Revenue: 850000,
    y5CumulativeRevenue: 2750000,
    y5ActiveContracts: 35,
  }
}
```

**Implementation notes:**
- Year-over-year: renewals = prior year activeContracts × 0.70
- activeContracts = newWins + renewals
- revenue = activeContracts × avgContractValue
- Use weighted average win rate across the year (blend months 1-6 and 7-12 rates for Y1)
- Export individual scenario configs as `SCENARIOS` for UI labels/colors
- Export slider configs as `SLIDER_CONFIGS` array with { key, label, min, max, step, default, format }

---

## Step 2 — Create Shared UI Components

### `/web/src/components/ui/ScenarioToggle.jsx`

Three pill buttons in a row. Props: `{ active, onChange, className }`

```
active = 'conservative' | 'moderate' | 'aggressive'
onChange = (scenarioKey) => void
```

- Conservative: zinc/slate color
- Moderate: teal color (#1B7A8A)
- Aggressive: gold color (#C9A84C)
- Active button gets filled bg, inactive gets outline
- Use Motion for smooth background transition

### `/web/src/components/ui/AnimatedNumber.jsx`

Smooth number transitions. Props: `{ value, format, duration, className }`

```
format = 'currency' | 'percent' | 'number' | 'compact'
duration = 0.6 (default)
```

- Use Motion's `useMotionValue` + `useTransform` + `animate` for smooth counting
- Currency: $XXX,XXX format
- Compact: $850K, $2.7M format
- Percent: XX.X% format

### `/web/src/components/ui/Slider.jsx`

Clean range input. Props: `{ label, value, onChange, min, max, step, format, className }`

- Label on left, formatted value on right
- Tailwind-styled track (zinc-200) with teal thumb
- Compact layout — these sit in a row of 3

---

## Step 3 — Create Slide 18: `FinancialDashboardSlide.jsx`

**File:** `/web/src/components/slides/FinancialDashboardSlide.jsx`

**Layout (top to bottom):**
1. Slide title: "Financial Outlook" with subtitle "Five-year revenue projections by scenario"
2. ScenarioToggle (centered)
3. 4 KPI cards in a row (equal width)
4. ECharts area chart showing 5-year revenue trajectory

**KPI Cards:**
| Card | Value | Subtitle |
|---|---|---|
| Year 1 Revenue | AnimatedNumber (currency) | "First-year projected revenue" |
| Year 5 Revenue | AnimatedNumber (currency) | "Fifth-year projected revenue" |
| Breakeven | "Year X" | "First profitable year" |
| 5-Year Total | AnimatedNumber (compact) | "Cumulative five-year revenue" |

Each card: white bg, rounded-xl, border, shadow-sm, colored top border (scenario color)

**Chart:**
- ECharts area chart, 5 data points (Year 1–5)
- Y-axis: dollar amounts
- Smooth curve, gradient fill matching scenario color
- Tooltip showing year, revenue, net income, active contracts
- Animate on scenario change via `chart.setOption()` with `notMerge: false`

**State:** `useState` for scenario key, `useMemo` for computed model

---

## Step 4 — Create Slide 19: `ProFormaSlide.jsx`

**File:** `/web/src/components/slides/ProFormaSlide.jsx`

**Layout (top to bottom):**
1. Slide title: "5-Year Pro Forma" with subtitle
2. Row: ScenarioToggle (left) + 3 Sliders (right, compact)
3. Two-column layout below:
   - LEFT (60%): Interactive data table
   - RIGHT (40%): Companion ECharts chart

**Sliders row:**
- Gross Margin (8%–15%, step 0.5%, default 11%)
- Bid Volume (0.5×–2.0×, step 0.1×, default 1.0×)
- Win Rate Adj (-10% to +10%, step 1%, default 0%)

**Table structure:**
| Metric | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|---|---|---|---|---|---|
| Bids Submitted | | | | | |
| New Wins | | | | | |
| Renewals | | | | | |
| Active Contracts | | | | | |
| **Revenue** | | | | | |
| COGS | | | | | |
| **Gross Profit** | | | | | |
| Tool Costs | | | | | |
| Admin Costs | | | | | |
| **Net Income** | | | | | |
| Cumulative Revenue | | | | | |
| ROI | | | | | |

- Row labels in left column, zinc-700 text
- Values use AnimatedNumber for smooth transitions
- Revenue, Gross Profit, Net Income rows are bold
- Net Income row: green text if positive, red if negative
- Subtle zebra striping (bg-zinc-50 alternate rows)
- Compact font sizes (text-sm for values, text-xs for labels)

**Companion Chart:**
- Stacked bar chart: Revenue (teal) vs Total Costs (zinc) per year
- Net Income line overlay
- Compact, no legend (colors are obvious), axis labels only
- Updates reactively with table

**State:** `useState` for scenario + each slider override, `useMemo` for computed model

---

## Step 5 — Register New Slides

### Modify `/web/src/data/slides.js`

Add before the 'blueprint' entry (currently last):
```js
{ id: 'financial-dashboard', label: 'Financial Dashboard', section: 'execution' },
{ id: 'pro-forma', label: '5-Year Pro Forma', section: 'execution' },
```

### Modify `/web/src/App.jsx`

Add imports:
```js
import FinancialDashboardSlide from './components/slides/FinancialDashboardSlide'
import ProFormaSlide from './components/slides/ProFormaSlide'
```

Add to `SLIDE_COMPONENTS` object:
```js
'financial-dashboard': FinancialDashboardSlide,
'pro-forma': ProFormaSlide,
```

---

## Verification Checklist

After building, verify all of these:

- [ ] Dev server runs without errors (`npm run dev`)
- [ ] Navigate to slide 18 (Financial Dashboard) — displays correctly
- [ ] Navigate to slide 19 (Pro Forma) — displays correctly
- [ ] Toggle between all 3 scenarios on both slides — KPIs/table/charts update smoothly
- [ ] Adjust each slider — table and chart values recalculate in real time
- [ ] Numbers align with research ranges:
  - Conservative Y1 revenue: ~$50K–$150K
  - Moderate Y1 revenue: ~$150K–$350K
  - Aggressive Y1 revenue: ~$350K–$750K
- [ ] All content clears the progress bar (pb-14 bottom padding)
- [ ] No regressions on existing 17 slides
- [ ] Production build succeeds (`npm run build`)

---

## File Checklist

**Create (6 files):**
- [ ] `web/src/data/financials.js`
- [ ] `web/src/components/ui/ScenarioToggle.jsx`
- [ ] `web/src/components/ui/AnimatedNumber.jsx`
- [ ] `web/src/components/ui/Slider.jsx`
- [ ] `web/src/components/slides/FinancialDashboardSlide.jsx`
- [ ] `web/src/components/slides/ProFormaSlide.jsx`

**Modify (2 files):**
- [ ] `web/src/data/slides.js`
- [ ] `web/src/App.jsx`
