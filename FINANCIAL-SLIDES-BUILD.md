# Financial Slide Build — Claude CLI Execution Guide

> **Purpose:** Add 1 interactive financial slide to the Newport GovCon web presentation.
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

## Architecture

This is ONE slide with two interconnected halves:

```
┌─────────────────────────────────────────────────────┐
│  TOP HALF: Executive Dashboard                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ Y1 Rev   │ │ Y5 Rev   │ │Breakeven │ │5Y Total│ │
│  │ $XXX,XXX │ │ $X.XM    │ │ Year X   │ │ $X.XM  │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
│  [GovCon % of Rev: X%]  [EBITDA Contribution: $XX] │
├─────────────────────────────────────────────────────┤
│  BOTTOM HALF: 5-Year Pro Forma                      │
│  ┌─ Controls ─────────────────────────────────────┐ │
│  │ [Conservative] [Moderate] [Aggressive]         │ │
│  │ Margin [===o===] Volume [===o===] Win [===o==] │ │
│  └────────────────────────────────────────────────┘ │
│  ┌─ Table (60%) ──────┐ ┌─ Chart (40%) ──────────┐ │
│  │ Metric Y1 Y2 .. Y5 │ │  ███  Stacked area     │ │
│  │ Revenue    ...      │ │  ███  showing all 3    │ │
│  │ COGS       ...      │ │  ███  scenarios with   │ │
│  │ Net Income ...      │ │  ██   component layers │ │
│  │ Cash Flow  ...      │ │  █                     │ │
│  │ ...                 │ │                        │ │
│  └─────────────────────┘ └────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

**Key interaction:** When the user toggles scenarios or adjusts sliders, BOTH halves update simultaneously — KPI cards animate to new values, the table recalculates, and the chart redraws.

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
| DSO (days sales outstanding) | 45 | 45 | 45 |

**Overrides (sliders):**
- `grossMargin`: 0.08–0.15, default 0.11
- `bidVolumeMultiplier`: 0.5–2.0, default 1.0
- `winRateAdjustment`: -0.10 to +0.10, default 0.0

**Key assumptions (hardcoded from research):**
- 70% contract renewal rate (compounds yearly)
- Contract tiers: Micro $8K avg, Simplified $50K, SLED $75K, Sealed Bid $150K
- Platform costs breakdown: CLEATUS $3K + HigherGov $3.5K + GovSpend $6.5K = $13K/yr
- COGS = revenue × (1 - grossMargin)
- Newport baseline revenue: $50M (for revenue concentration % calculation)
- Cash flow impact: revenue delayed by DSO days; approximate as (revenue / 12) × (DSO / 30) for working capital tied up

### Export: `computeAllScenarios(overrides)`

Runs `computeProForma` for ALL THREE scenarios with the same overrides. Returns `{ conservative: {...}, moderate: {...}, aggressive: {...} }`. This is needed for the stacked area chart that compares all scenarios simultaneously.

**Return shape (per scenario):**
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
      totalOperatingCosts: 28000,
      netIncome: -3250,
      cumulativeRevenue: 225000,
      roi: -0.12,
      workingCapitalTiedUp: 28125,    // cash flow: revenue/12 * DSO/30
      revenueConcentration: 0.0045,   // revenue / 50M baseline
      ebitdaContribution: -3250,      // netIncome (simplified; no depreciation/amortization for this model)
    },
    // ... years 2-5
  ],
  summary: {
    breakevenYear: 2,
    y5Revenue: 850000,
    y5CumulativeRevenue: 2750000,
    y5ActiveContracts: 35,
    peakWorkingCapital: 106250,       // max workingCapitalTiedUp across 5 years
    y5RevenueConcentration: 0.017,    // Y5 revenue / baseline
    y5EbitdaContribution: 93500,
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

## Step 3 — Create Slide 18: `FinancialOutlookSlide.jsx`

**File:** `/web/src/components/slides/FinancialOutlookSlide.jsx`

This is ONE slide with two interconnected halves sharing the same state. The controls sit between the halves and drive everything.

### Shared State (at component root level)

```js
const [scenario, setScenario] = useState('moderate')
const [overrides, setOverrides] = useState({
  grossMargin: 0.11,
  bidVolumeMultiplier: 1.0,
  winRateAdjustment: 0,
})

// Active scenario model (for KPI cards + table)
const model = useMemo(() => computeProForma(scenario, overrides), [scenario, overrides])

// All scenarios (for stacked area chart comparison)
const allModels = useMemo(() => computeAllScenarios(overrides), [overrides])
```

### TOP HALF — Executive Dashboard KPIs

**Layout:** Slide title → KPI cards row → strategic metrics row

**Title:** "Financial Outlook" — small, left-aligned, text-zinc-500 subtitle "Five-year GovCon revenue projections"

**KPI Cards (4 across, equal width):**
| Card | Value | Subtitle |
|---|---|---|
| Year 1 Revenue | AnimatedNumber (currency) | "First-year projected" |
| Year 5 Revenue | AnimatedNumber (compact) | "Fifth-year projected" |
| Breakeven | "Year X" | "First profitable year" |
| 5-Year Cumulative | AnimatedNumber (compact) | "Total five-year revenue" |

Each card: white bg, `rounded-xl border border-zinc-200 shadow-sm`, colored left border or top border using scenario color.

**Strategic Metrics Row (smaller, secondary emphasis):**
Two compact inline metrics below the KPI cards:
- "GovCon % of Revenue: X.X%" — `revenueConcentration` from Y5, formatted as percent
- "Y5 EBITDA Contribution: $XXK" — `y5EbitdaContribution`, compact currency

These use AnimatedNumber but smaller text (text-sm), zinc-600 color. Think of these as contextual footnotes that answer "how meaningful is this to the overall business?"

### DIVIDER — Controls Strip

Between top and bottom halves. Visually distinct row that contains:
- **ScenarioToggle** (left side)
- **3 Sliders** (right side, compact inline)
  - Gross Margin (8%–15%, step 0.5%, default 11%)
  - Bid Volume (0.5×–2.0×, step 0.1×, default 1.0×)
  - Win Rate Adj (-10% to +10%, step 1%, default 0%)

Style: `bg-zinc-50 rounded-lg px-4 py-2` — subtle background to visually separate from the white card areas above and below. Compact vertical height.

### BOTTOM HALF — 5-Year Pro Forma

**Two-column layout:**
- **LEFT (60%):** Interactive data table
- **RIGHT (40%):** Stacked area chart comparing all 3 scenarios

#### Table

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
| Working Capital Req | | | | | |
| Cumulative Revenue | | | | | |
| ROI | | | | | |

- The table shows data for the ACTIVE SCENARIO only (whichever toggle is selected)
- Row labels: left column, text-zinc-700
- Values: AnimatedNumber for smooth transitions on scenario/slider change
- Revenue, Gross Profit, Net Income rows are **bold**
- Net Income row: `text-emerald-600` if positive, `text-red-500` if negative
- Subtle zebra striping: `bg-zinc-50` on alternate rows
- Compact: `text-sm` for values, `text-xs` for row labels

#### Stacked Area Chart (THE KEY VISUAL)

This chart shows ALL THREE scenarios simultaneously so the viewer can visually compare them. This is different from the table which only shows the active scenario.

**Chart type:** ECharts stacked area chart
**X-axis:** Year 1 → Year 5
**Y-axis:** Revenue (dollar amounts)

**Three stacked area series:**
1. **Conservative** (bottom layer): zinc-300 fill, zinc-400 line
2. **Moderate** (middle layer): teal fill (#1B7A8A, 40% opacity), teal line
3. **Aggressive** (top layer): gold fill (#C9A84C, 30% opacity), gold line

**Stacking behavior:** Each series shows its own revenue value stacked on top of the one below. This creates a visual "fan" that widens over 5 years, showing the growing gap between scenarios. The area between layers represents the incremental revenue from moving to a more aggressive approach.

**Active scenario highlight:** The currently selected scenario's area should have FULL opacity and a thicker border line (lineWidth: 3), while the other two fade to lower opacity (0.15). This creates a visual "spotlight" on the active scenario while maintaining the comparison context.

**Tooltip:** On hover, show all 3 scenario values for that year in a formatted tooltip:
```
Year 3
Conservative: $180,000
Moderate: $425,000      ← (highlighted if active)
Aggressive: $780,000
```

**Animate on change:** When scenario toggle or sliders change, use `chart.setOption()` with animation enabled. The areas should smoothly morph to new values.

**Compact styling:** No external legend (the colors are self-evident from the toggle above). Minimal axis labels. The chart should feel like part of the slide, not a standalone visualization.

---

## Step 4 — Register New Slide

### Modify `/web/src/data/slides.js`

Add ONE entry before the 'blueprint' entry (currently last):
```js
{ id: 'financial-outlook', label: 'Financial Outlook', section: 'execution' },
```

### Modify `/web/src/App.jsx`

Add import:
```js
import FinancialOutlookSlide from './components/slides/FinancialOutlookSlide'
```

Add to `SLIDE_COMPONENTS` object:
```js
'financial-outlook': FinancialOutlookSlide,
```

---

## Verification Checklist

After building, verify all of these:

- [ ] Dev server runs without errors (`npm run dev`)
- [ ] Navigate to slide 18 (Financial Outlook) — displays correctly
- [ ] TOP HALF: KPI cards show correct values for selected scenario
- [ ] BOTTOM HALF table: shows data for selected scenario, updates on toggle/slider
- [ ] BOTTOM HALF chart: shows ALL 3 scenarios as stacked areas, highlights active one
- [ ] Toggle between scenarios — KPIs, table, AND chart all update smoothly together
- [ ] Adjust each slider — everything recalculates in real time
- [ ] Strategic metrics (GovCon % of Rev, EBITDA) update with scenario changes
- [ ] Numbers align with research ranges:
  - Conservative Y1 revenue: ~$50K–$150K
  - Moderate Y1 revenue: ~$150K–$350K
  - Aggressive Y1 revenue: ~$350K–$750K
- [ ] Stacked area chart "fans out" over 5 years showing growing scenario gap
- [ ] All content clears the progress bar (pb-14 bottom padding)
- [ ] No regressions on existing 17 slides
- [ ] Production build succeeds (`npm run build`)

---

## File Checklist

**Create (5 files):**
- [ ] `web/src/data/financials.js`
- [ ] `web/src/components/ui/ScenarioToggle.jsx`
- [ ] `web/src/components/ui/AnimatedNumber.jsx`
- [ ] `web/src/components/ui/Slider.jsx`
- [ ] `web/src/components/slides/FinancialOutlookSlide.jsx`

**Modify (2 files):**
- [ ] `web/src/data/slides.js` — add 1 slide entry
- [ ] `web/src/App.jsx` — import + register 1 component
