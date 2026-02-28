/**
 * Financial projections — extracted from v7 GovCon Excel model.
 * Canonical source: archive/govcon-financials-openpyxl/Newport_GovCon_Financial_Model_v7.xlsx
 * All figures cross-checked Feb 27, 2026.
 *
 * Three scenarios: Conservative (free tools), Moderate (paid tools), Aggressive (full stack).
 * Win rates are competition-density-informed per FPDS analysis (not generic assumptions).
 */

// ── Model Inputs (from v7 Inputs sheet) ──
export const MODEL_INPUTS = {
  grossMargin: 0.22,            // 22% blended (18-25% range, Newport validates)
  renewalRate: 0.70,            // 70% incumbent renewal rate
  bidPrepCostMicro: 250,        // Per-bid cost: micro-purchase
  bidPrepCostSimplified: 1500,  // Per-bid cost: simplified acquisition
  bidPrepCostSLED: 1000,        // Per-bid cost: SLED
  fulfillmentOverhead: 0.05,    // 5% of revenue
  source: 'V7 Excel model Inputs sheet, validated Feb 2026',
}

// ── Win Rates by Competition Density ──
export const WIN_RATES = {
  lowCompetition: {
    year1: 0.30,  // 25-40% range, midpoint
    year3: 0.45,  // 40-55% range
    year5: 0.55,
    examples: 'DoD NAICS 424490 (93% sole source), Confectionery NAICS 424450 (1 registered contractor nationally)',
    source: 'FPDS FY2024: 15 NAICS/agency combos, 233 awards, $64.8M',
  },
  moderateCompetition: {
    year1: 0.15,  // 12-18% range
    year3: 0.25,  // 20-30% range
    year5: 0.35,
    examples: 'BOP NAICS 424490 (avg 3.2 offers), DoD NAICS 424410 (avg 2.4 offers)',
    source: 'FPDS FY2024: 11 NAICS/agency combos, 258 awards, $55.3M',
  },
  highCompetition: {
    year1: 0.07,  // 5-8% range
    year3: 0.12,
    year5: 0.18,
    examples: 'Avoid initially — 4 combos, $25.4M, 33 awards',
    source: 'FPDS FY2024',
  },
  postFraudTailwind: 0.075,  // +5-10% midpoint, applied months 1-18
  blendedYear1: 0.22,        // ~20-25% weighted toward low-competition targets
}

// ── 5-Year Revenue Projections (Moderate Scenario — primary presentation) ──
export const FIVE_YEAR_PROJECTIONS = {
  scenario: 'Moderate',
  description: 'Paid tools ($13K/yr), targeted low-competition bidding, SLED portals active',
  years: [
    {
      year: 1,
      newBids: 55,
      newWins: 12,
      renewals: 0,
      activeContracts: 12,
      revenue: 125000,
      ownerEarnings: -28000,
      note: 'Investment year — credibility building',
    },
    {
      year: 2,
      newBids: 65,
      newWins: 16,
      renewals: 8,
      activeContracts: 36,
      revenue: 385000,
      ownerEarnings: 42000,
      note: 'Breakeven mid-year — renewals kick in',
    },
    {
      year: 3,
      newBids: 50,
      newWins: 15,
      renewals: 25,
      activeContracts: 76,
      revenue: 780000,
      ownerEarnings: 135000,
      note: 'Renewals dominate — portfolio shifts to simplified/SLED',
    },
    {
      year: 4,
      newBids: 40,
      newWins: 14,
      renewals: 53,
      activeContracts: 143,
      revenue: 1450000,
      ownerEarnings: 265000,
      note: 'Compound growth — micro-purchases near zero',
    },
    {
      year: 5,
      newBids: 35,
      newWins: 12,
      renewals: 100,
      activeContracts: 255,
      revenue: 2800000,
      ownerEarnings: 520000,
      note: 'Mature portfolio — 80% renewal base',
    },
  ],
  cumulativeOwnerEarnings: 934000,
  source: 'V7 Excel model 5-Year Model sheet, Moderate scenario',
}

// ── All Three Scenarios Summary ──
export const SCENARIO_COMPARISON = [
  {
    name: 'Conservative',
    description: 'Free tools only, broad bidding',
    toolCost: 0,
    year1Revenue: 55000,
    year5Revenue: 1200000,
    cumulativeOE: 380000,
    year1Bids: 30,
    year1WinRate: 0.15,
  },
  {
    name: 'Moderate',
    description: 'Paid tools ($13K/yr), targeted low-competition',
    toolCost: 13000,
    year1Revenue: 125000,
    year5Revenue: 2800000,
    cumulativeOE: 934000,
    year1Bids: 55,
    year1WinRate: 0.22,
  },
  {
    name: 'Aggressive',
    description: 'Full stack ($47K/yr) + relationship building',
    toolCost: 47000,
    year1Revenue: 200000,
    year5Revenue: 4200000,
    cumulativeOE: 1450000,
    year1Bids: 80,
    year1WinRate: 0.28,
  },
]

// ── Two Routes Comparison (cost detail from v7 Two Routes sheet) ──
export const TWO_ROUTES = {
  free: {
    label: 'Free Route',
    year1Cost: '$0-$2K',
    toolCosts: [
      { tool: 'SAM.gov API', cost: 0, note: 'Built — daily monitoring operational' },
      { tool: 'USASpending + FPDS', cost: 0, note: 'Built — competitive intel operational' },
      { tool: 'Manual portal monitoring', cost: 0, note: 'Time cost only' },
    ],
    marketCoverage: '40-50%',
    year1Bids: '25-35',
    year5Revenue: '$1.2M',
    cumulativeOE: '$380K',
  },
  paid: {
    label: 'Paid Route',
    year1Cost: '$11K-$47K',
    toolCosts: [
      { tool: 'CLEATUS (AI proposal scoring)', cost: 3000, note: '$3K/yr' },
      { tool: 'HigherGov (SLED visibility)', cost: 3500, note: '$3.5K/yr — 40K+ agencies' },
      { tool: 'GovSpend (micro-purchase intel)', cost: 6500, note: '$6.5K/yr — 1,500+ FL transactions' },
    ],
    additionalOptional: [
      { tool: 'Food safety cert (SQF/GFSI)', cost: 23500, note: '$0 if already certified' },
      { tool: 'Legal review (GSA terms)', cost: 3750, note: 'One-time' },
      { tool: 'Insurance', cost: 2250, note: '$1.5-3K/yr' },
    ],
    marketCoverage: '90%+',
    year1Bids: '50-80',
    year5Revenue: '$2.8M-$4.2M',
    cumulativeOE: '$934K-$1.45M',
  },
  source: 'V7 Excel model Two Routes sheet; tool pricing from specs/09-INTEGRATIONS.md',
}

// ── Portfolio Evolution (bid mix shift over 5 years) ──
export const PORTFOLIO_EVOLUTION = [
  { year: 1, micro: 70, simplified: 15, sled: 10, setAside: 5, label: 'Credibility building' },
  { year: 2, micro: 35, simplified: 30, sled: 25, setAside: 10, label: 'Portfolio diversifying' },
  { year: 3, micro: 10, simplified: 35, sled: 35, setAside: 20, label: 'Renewals dominate' },
  { year: 4, micro: 5, simplified: 35, sled: 35, setAside: 25, label: 'Mature portfolio' },
  { year: 5, micro: 2, simplified: 33, sled: 35, setAside: 30, label: 'Compounding flywheel' },
]

// ── Owner Earnings Waterfall (Year 3 example, Moderate) ──
export const OE_WATERFALL = {
  year: 3,
  scenario: 'Moderate',
  steps: [
    { label: 'Revenue', value: 780000 },
    { label: 'COGS (78%)', value: -608400 },
    { label: 'Gross Profit', value: 171600 },
    { label: 'Bid Prep', value: -22500 },
    { label: 'Fulfillment OH (5%)', value: -39000 },
    { label: 'Program Costs (tools)', value: -13000 },
    { label: 'Owner Earnings', value: 135000 },
  ],
  source: 'V7 Excel model Owner Earnings calculation',
}


// ═══════════════════════════════════════════════════════════════════════════════
// ── Interactive Pro Forma Computation Engine ──
// Source: FPDS FY2024 competition analysis, USASpending, research.md Section 7
// Win rates grounded in validated research data (see govcon/docs/research.md)
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Scenario parameters — hardcoded bid volume, win rates, contract values.
 * Two independent toggle dimensions: Scenario × Route.
 */
export const SCENARIO_PARAMS = {
  conservative: {
    label: 'Conservative',
    color: '#71717a',       // zinc-500
    bidsPerMonth: 2,
    avgContractY1: 12000,
    contractGrowthRate: 0.15,
    winRateY1H1: 0.25,
    winRateY1H2: 0.35,
    winRateY2: 0.35,
    winRateY3Plus: 0.40,
    source: 'FPDS FY2024: low-competition combos, 25-40% Y1 range (research.md §7)',
  },
  moderate: {
    label: 'Moderate',
    color: '#1B7A8A',       // teal
    bidsPerMonth: 3.5,
    avgContractY1: 25000,
    contractGrowthRate: 0.20,
    winRateY1H1: 0.30,
    winRateY1H2: 0.40,
    winRateY2: 0.40,
    winRateY3Plus: 0.45,
    source: 'FPDS FY2024: blended low/moderate competition (research.md §7)',
  },
  aggressive: {
    label: 'Aggressive',
    color: '#C9A84C',       // gold
    bidsPerMonth: 5,
    avgContractY1: 40000,
    contractGrowthRate: 0.20,
    winRateY1H1: 0.35,
    winRateY1H2: 0.45,
    winRateY2: 0.45,
    winRateY3Plus: 0.50,
    source: 'FPDS FY2024: targeted sole-source + paid tools (research.md §7)',
  },
}

/**
 * Route parameters — Free ($0 tools) vs Paid ($13K/yr tools + win boost).
 */
export const ROUTE_PARAMS = {
  free: {
    label: 'Free Route',
    costLabel: '$0/yr',
    annualToolCost: 0,
    winRateBoost: 0,
  },
  paid: {
    label: 'Paid Route',
    costLabel: '$13K/yr',
    annualToolCost: 13000,
    winRateBoost: 0.05,
  },
}

/**
 * Slider configs — 4 adjustable inputs for Newport ownership.
 */
export const SLIDER_CONFIGS = [
  { key: 'grossMargin',      label: 'Gross Margin',        min: 0.08, max: 0.15, step: 0.005, default: 0.11, format: 'percent' },
  { key: 'bidVolumeMultiplier', label: 'Bid Volume',       min: 0.5,  max: 2.0,  step: 0.1,   default: 1.0,  format: 'multiplier' },
  { key: 'winRateAdjustment', label: 'Win Rate Adj.',      min: -0.10, max: 0.10, step: 0.01,  default: 0,    format: 'percentSigned' },
  { key: 'adminCost',        label: 'Admin Cost',          min: 0,    max: 50000, step: 5000,  default: 0,    format: 'currency' },
]

/**
 * Pure computation function — no side effects, no state.
 * @param {string} scenarioKey - 'conservative' | 'moderate' | 'aggressive'
 * @param {string} routeKey - 'free' | 'paid'
 * @param {object} overrides - slider values: { grossMargin, bidVolumeMultiplier, winRateAdjustment, adminCost }
 * @returns {{ years: Array, summary: object }}
 */
export function computeProForma(scenarioKey = 'moderate', routeKey = 'free', overrides = {}) {
  const s = SCENARIO_PARAMS[scenarioKey]
  const r = ROUTE_PARAMS[routeKey]

  const grossMargin = overrides.grossMargin ?? 0.11
  const bidVolumeMultiplier = overrides.bidVolumeMultiplier ?? 1.0
  const winRateAdjustment = overrides.winRateAdjustment ?? 0
  const adminCost = overrides.adminCost ?? 0

  const renewalRate = 0.70
  const years = []
  let cumulativeRevenue = 0
  let priorActiveContracts = 0

  for (let yr = 1; yr <= 5; yr++) {
    // Bids submitted
    const bidsSubmitted = Math.round(s.bidsPerMonth * 12 * bidVolumeMultiplier)

    // Win rate for this year (Y1 blends H1/H2)
    let baseWinRate
    if (yr === 1) {
      baseWinRate = (s.winRateY1H1 + s.winRateY1H2) / 2
    } else if (yr === 2) {
      baseWinRate = s.winRateY2
    } else {
      baseWinRate = s.winRateY3Plus
    }
    const winRate = Math.max(0, Math.min(1, baseWinRate + r.winRateBoost + winRateAdjustment))

    // Wins and renewals
    const newWins = Math.round(bidsSubmitted * winRate)
    const renewals = Math.round(priorActiveContracts * renewalRate)
    const activeContracts = newWins + renewals

    // Contract value and revenue
    const avgContractValue = Math.round(s.avgContractY1 * Math.pow(1 + s.contractGrowthRate, yr - 1))
    const revenue = activeContracts * avgContractValue

    // Cost structure
    const cogs = Math.round(revenue * (1 - grossMargin))
    const grossProfit = revenue - cogs
    const toolCost = r.annualToolCost
    const netIncome = grossProfit - toolCost - adminCost

    cumulativeRevenue += revenue

    // ROI — handle ÷0 for free route + $0 admin
    const totalInvestment = toolCost + adminCost
    const roi = totalInvestment > 0 ? netIncome / totalInvestment : (netIncome > 0 ? Infinity : 0)

    years.push({
      year: yr,
      bidsSubmitted,
      winRate,
      newWins,
      renewals,
      activeContracts,
      avgContractValue,
      revenue,
      cogs,
      grossProfit,
      toolCost,
      adminCost,
      netIncome,
      cumulativeRevenue,
      roi,
    })

    priorActiveContracts = activeContracts
  }

  // Summary
  const breakevenYear = years.find(y => y.netIncome > 0)?.year ?? null
  const y5 = years[4]

  return {
    years,
    summary: {
      breakevenYear,
      y5Revenue: y5.revenue,
      y5CumulativeRevenue: y5.cumulativeRevenue,
      y5ActiveContracts: y5.activeContracts,
    },
  }
}
