# Financial Slide Build — Claude CLI Technical Spec

> **Purpose:** Add 1 interactive financial slide to the Newport GovCon web presentation.
> **Context:** Read `FINANCIAL-SLIDES-PROMPT.md` FIRST for business logic and model architecture.
> **Stack:** React 19 + Vite 7.3 + Tailwind CSS 4.2 + ECharts 6 + Motion
> **Working directory:** `newport-leadgen/web/`

---

## Design Reference

Use https://ui.shadcn.com/blocks as visual inspiration — particularly dashboard blocks with KPI cards, charts, and tables. We are NOT installing shadcn/ui. Replicate the design patterns (spacing, card proportions, typography hierarchy) using existing Tailwind classes.

---

## Pre-Read (Do This First)

Before writing ANY code, read these files:

```
FINANCIAL-SLIDES-PROMPT.md               — Business context, model logic, variable definitions (READ THIS FIRST)
govcon/docs/research.md                  — TAM, win rates, competition density, contract values
govcon/docs/strategy.md                  — cost breakdowns, company profile, two routes
govcon/docs/phases/PHASE-4-FINANCIALS.md — financial model spec
.claude/commands/rebuild-proforma.md     — scenario definitions, win rate methodology
web/src/data/market.js                   — existing data export pattern
web/src/data/strategy.js                 — existing data export pattern
web/src/data/slides.js                   — slide registry (you'll modify this)
web/src/App.jsx                          — component registration (you'll modify this)
web/src/components/slides/PortfolioEvolutionSlide.jsx — ECharts integration pattern
web/src/components/ui/DecorativeElements.jsx          — reusable UI components
```

---

## Design System

- **Palette:** zinc base + Gold `#C9A84C`, Teal `#1B7A8A`, Light Teal `#239BAD`, Orange `#E8913A`
- **Card pattern:** `rounded-xl bg-white border border-zinc-200 shadow-sm`
- **Bottom padding:** Always `pb-14` on slide outer container (progress bar clearance)
- **ECharts pattern:** `useRef` for DOM, `useEffect` for init/update, resize handler, `chart.setOption()` for reactive updates

---

## Step 1 — Create `/web/src/data/financials.js`

Pure computation engine. No React, no UI — just math.

### Two Axes

**Axis 1 — Route** (`routeKey = 'free' | 'paid'`):

| Parameter | Free | Paid |
|---|---|---|
| Platform cost/yr | $0 | $13,000 |
| Insurance/compliance/yr | $500 | $1,500 |
| Conference/membership/yr | $0 | $2,000 |
| Market coverage | ~45% | ~90% |
| Bid capacity multiplier | 1.0× | 2.5× |

**Axis 2 — Scenario** (`scenarioKey = 'conservative' | 'moderate' | 'aggressive'`):

Base bid volumes (before route multiplier):
| Parameter | Conservative | Moderate | Aggressive |
|---|---|---|---|
| Base bids/month | 1 | 2 | 3 |
| Win rate Y1 (mo 1-6) | 15% | 20% | 25% |
| Win rate Y1 (mo 7-12) | 23% | 28% | 33% |
| Win rate Y2 | 28% | 33% | 38% |
| Win rate Y3-5 | 33% | 38% | 43% |

Actual bids/month = base × route bid capacity multiplier

**Contract tier mix evolves by year:**
| Tier | Avg Value | Y1 Mix | Y2 Mix | Y3 Mix | Y4-5 Mix |
|---|---|---|---|---|---|
| Micro (<$15K) | $8K | 80% | 55% | 35% | 25% |
| Simplified ($15K-$250K) | $50K | 15% | 30% | 35% | 30% |
| SLED | $75K | 5% | 10% | 20% | 25% |
| Sealed Bid ($250K+) | $150K | 0% | 5% | 10% | 20% |

Weighted avg contract value = sum(tierMix × tierAvgValue) per year.

### Overrides (management input sliders)

- `grossMargin`: 0.08–0.15, step 0.005, default 0.11
- `deliveryCostPct`: 0.02–0.08, step 0.005, default 0.04
- `adminOverhead`: 0–50000, step 1000, default 5000

### Exports

**`ROUTE_CONFIGS`** — Object with 'free' and 'paid' keys, each containing { label, platformCost, insuranceCost, conferenceCost, bidMultiplier, color }

**`SCENARIO_CONFIGS`** — Object with scenario keys, each containing { label, baseBidsPerMonth, winRates: { y1h1, y1h2, y2, y3to5 }, color }

**`SLIDER_CONFIGS`** — Array of { key, label, min, max, step, default, format }

**`computeProForma(routeKey, scenarioKey, overrides)`** — Returns:

```js
{
  route: 'paid',
  scenario: 'moderate',
  overrides: { grossMargin: 0.11, deliveryCostPct: 0.04, adminOverhead: 5000 },
  years: [
    {
      year: 1,
      bidsPerMonth: 5,           // base 2 × paid multiplier 2.5
      bidsSubmitted: 60,         // bidsPerMonth × 12
      winRate: 0.24,             // weighted avg of H1 and H2
      newWins: 14,               // bidsSubmitted × winRate
      renewals: 0,               // prior year active × 0.70
      activeContracts: 14,

      // Revenue breakdown by tier
      tierBreakdown: [
        { tier: 'Micro', count: 11, avgValue: 8000, revenue: 88000 },
        { tier: 'Simplified', count: 2, avgValue: 50000, revenue: 100000 },
        { tier: 'SLED', count: 1, avgValue: 75000, revenue: 75000 },
      ],
      revenue: 263000,

      // Costs
      cogs: 234070,              // revenue × (1 - grossMargin)
      grossProfit: 28930,
      deliveryCost: 10520,       // revenue × deliveryCostPct
      platformCost: 13000,       // from route config
      insuranceCost: 1500,
      conferenceCost: 2000,
      adminOverhead: 5000,
      totalCosts: 266090,

      // Bottom line
      netIncome: -3090,
      cumulativeRevenue: 263000,
      cumulativeNetIncome: -3090,
      roi: -0.01,               // netIncome / totalCosts (excl COGS)
    },
    // ... years 2-5
  ],
  summary: {
    breakevenYear: 2,
    y5Revenue: 0,               // computed
    y5CumulativeRevenue: 0,     // computed
    y5ActiveContracts: 0,       // computed
    y5NetIncome: 0,             // computed
    totalInvestment: 0,         // sum of all non-COGS costs over 5 years
    totalReturn: 0,             // cumulative net income
  }
}
```

**`computeAllScenarios(routeKey, overrides)`** — Runs `computeProForma` for all 3 scenarios with same route + overrides. Returns `{ conservative: {...}, moderate: {...}, aggressive: {...} }`.

### Implementation Notes

- renewals = prior year activeContracts × 0.70
- activeContracts = newWins + renewals
- newWins by tier: distribute newWins across tiers using that year's tier mix %
- revenue = sum of (tier count × tier avg value) across all tiers
- For Y1 win rate: use weighted average of H1 (months 1-6) and H2 (months 7-12)
- Aggressive scenario win rates are capped at 45% (max credible for new entrant by Y5)
- tier counts should be whole numbers (Math.round), ensure they sum to total newWins

---

## Step 2 — Create Shared UI Components

### `/web/src/components/ui/RouteToggle.jsx`

Two-button toggle: Free Route / Paid Route. Props: `{ active, onChange }`

- Free: zinc/slate styling, show "$0/yr" subtitle
- Paid: teal styling, show "$13K/yr" subtitle
- Active gets filled bg, inactive gets outline

### `/web/src/components/ui/ScenarioToggle.jsx`

Three pill buttons. Props: `{ active, onChange }`

- Conservative: zinc color
- Moderate: teal (#1B7A8A)
- Aggressive: gold (#C9A84C)

### `/web/src/components/ui/AnimatedNumber.jsx`

Smooth number transitions. Props: `{ value, format, duration, className }`
Formats: 'currency' ($XXX,XXX), 'compact' ($850K, $2.7M), 'percent' (XX.X%), 'number' (plain)

### `/web/src/components/ui/Slider.jsx`

Range input. Props: `{ label, value, onChange, min, max, step, format }`
Label left, formatted value right. Teal thumb on zinc track. Compact.

---

## Step 3 — Create Slide 18: `FinancialOutlookSlide.jsx`

Single slide, two interconnected halves sharing state. Every input change cascades through the entire dashboard.

### State

```js
const [route, setRoute] = useState('free')
const [scenario, setScenario] = useState('moderate')
const [overrides, setOverrides] = useState({
  grossMargin: 0.11,
  deliveryCostPct: 0.04,
  adminOverhead: 5000,
})

const model = useMemo(
  () => computeProForma(route, scenario, overrides),
  [route, scenario, overrides]
)

const allScenarios = useMemo(
  () => computeAllScenarios(route, overrides),
  [route, overrides]
)
```

### Layout

```
┌─────────────────────────────────────────────────────────┐
│ FINANCIAL PROJECTIONS                                   │
│ Financial Outlook                                       │
│                                                         │
│ [Free Route] [Paid Route]  [Cons] [Mod] [Agg]          │
│ Margin [===o===]  Delivery [===o===]  Admin [===o===]   │
│                                                         │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐  │
│ │ Y1 Rev   │ │ Y5 Rev   │ │Breakeven │ │ 5Y Net Inc │  │
│ │ $263K    │ │ $2.1M    │ │ Year 2   │ │ $485K      │  │
│ └──────────┘ └──────────┘ └──────────┘ └────────────┘  │
│                                                         │
│ ┌─ Table (55%) ────────────┐ ┌─ Chart (45%) ─────────┐ │
│ │ Metric   Y1  Y2 .. Y5   │ │  Overlapping area      │ │
│ │ Revenue       ...        │ │  3 scenarios            │ │
│ │ COGS          ...        │ │  active highlighted     │ │
│ │ Gross Profit  ...        │ │                         │ │
│ │ Platform      ...        │ │  ┌── opt. 2nd chart ──┐│ │
│ │ Delivery      ...        │ │  │ Stacked bar: tier  ││ │
│ │ Admin         ...        │ │  │ composition Y1→Y5  ││ │
│ │ Net Income    ...        │ │  └────────────────────┘│ │
│ └──────────────────────────┘ └────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### TOP — Controls + KPI Cards

**Controls row:** RouteToggle (left) → ScenarioToggle (center) → 3 Sliders (right, compact)

**KPI Cards (4 across):**
| Card | Value | Source |
|---|---|---|
| Year 1 Revenue | AnimatedNumber (currency) | `model.years[0].revenue` |
| Year 5 Revenue | AnimatedNumber (compact) | `model.years[4].revenue` |
| Breakeven Year | "Year X" or "Year 1" | `model.summary.breakevenYear` |
| 5-Year Net Income | AnimatedNumber (compact) | `model.summary.totalReturn` |

Cards: white bg, rounded-xl, border, shadow-sm. Net Income card: green border if positive, red if negative.

### BOTTOM LEFT — Pro Forma Table

Shows data for the ACTIVE route + scenario combination only.

| Row | Y1 | Y2 | Y3 | Y4 | Y5 | Notes |
|---|---|---|---|---|---|---|
| Bids Submitted | | | | | | number |
| New Wins | | | | | | number |
| Renewals | | | | | | number |
| Active Contracts | | | | | | number |
| **Revenue** | | | | | | **bold**, currency |
| COGS | | | | | | currency, zinc-400 |
| **Gross Profit** | | | | | | **bold** |
| Platform & Insurance | | | | | | currency |
| Delivery Costs | | | | | | currency |
| Admin Overhead | | | | | | currency |
| **Net Income** | | | | | | **bold**, green/red |
| Cumulative Net Income | | | | | | currency |

- AnimatedNumber on all value cells for smooth transitions
- Zebra striping: bg-zinc-50 on alternate rows
- Compact: text-sm values, text-xs labels

### BOTTOM RIGHT — Chart(s)

**Primary: 3-Scenario Overlapping Area Chart**

Shows all 3 scenarios for the selected route. NOT additive stacking — each series shows absolute revenue. Render order: Aggressive (back), Moderate (middle), Conservative (front).

- Conservative: zinc (#71717a) line + fill
- Moderate: teal (#1B7A8A) line + fill
- Aggressive: gold (#C9A84C) line + fill
- Active scenario: full opacity (0.35), thick line (3px), dot markers
- Inactive: faded (0.08 opacity), thin line (1.5px), no markers

**Tooltip (critical — must show the math):**

```
Year 2 — Moderate (Paid Route)
───────────────────────────────
  Aggressive:    $780K
▸ Moderate:      $420K   ← active, bold
  Conservative:  $145K

Bids: 60 | Wins: 16 | Renewals: 10
  Micro (8):       8 × $8K  = $64K
  Simplified (5):  5 × $50K = $250K
  SLED (3):        3 × $75K = $225K
```

Tooltip data comes from `model.years[yearIndex].tierBreakdown` for the active scenario. The 3-scenario comparison values come from `allScenarios`.

**Optional secondary chart (if space permits):**

Small stacked bar chart showing contract tier composition shifting Y1→Y5. Each bar is one year, segments are tier percentages. This makes the "buying a track record → graduating up → flywheel" narrative visual. Place below the area chart or as a toggle view.

---

## Step 4 — Register Slide

### `/web/src/data/slides.js`

Add before 'blueprint' (currently last):
```js
{ id: 'financial-outlook', label: 'Financial Outlook', section: 'execution' },
```

### `/web/src/App.jsx`

```js
import FinancialOutlookSlide from './components/slides/FinancialOutlookSlide'
// in SLIDE_COMPONENTS:
'financial-outlook': FinancialOutlookSlide,
```

---

## Verification Checklist

- [ ] Dev server runs without errors (`npm run dev`)
- [ ] Slide 18 renders with all components visible
- [ ] Route toggle switches between Free and Paid — all values update
- [ ] Scenario toggle switches — KPIs, table, chart highlight all update
- [ ] Each slider adjusts values in real time across all components
- [ ] Tooltip on chart hover shows tier breakdown math
- [ ] Numbers are credible:
  - Free/Conservative Y1: ~$15K-$40K revenue
  - Free/Moderate Y1: ~$40K-$100K revenue
  - Paid/Conservative Y1: ~$80K-$180K revenue
  - Paid/Moderate Y1: ~$200K-$400K revenue
  - Paid/Aggressive Y1: ~$400K-$750K revenue
- [ ] Net Income row is red when negative, green when positive
- [ ] Year 1 shows mostly micro contracts, Year 5 shows larger mix
- [ ] All content clears progress bar (pb-14)
- [ ] No regressions on existing 17 slides
- [ ] Production build succeeds (`npm run build`)

---

## File Checklist

**Create (6 files):**
- [ ] `web/src/data/financials.js`
- [ ] `web/src/components/ui/RouteToggle.jsx`
- [ ] `web/src/components/ui/ScenarioToggle.jsx`
- [ ] `web/src/components/ui/AnimatedNumber.jsx`
- [ ] `web/src/components/ui/Slider.jsx`
- [ ] `web/src/components/slides/FinancialOutlookSlide.jsx`

**Modify (2 files):**
- [ ] `web/src/data/slides.js` — add 1 entry
- [ ] `web/src/App.jsx` — import + register 1 component
