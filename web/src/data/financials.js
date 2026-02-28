/**
 * Newport GovCon Financial Model — Computation Engine
 *
 * Source: Validated research (Feb 28, 2026) — govcon/docs/
 * All inputs from 12 locked research variables.
 *   Win rates: FPDS FY2024 (537 awards, 32 NAICS/agency combos)
 *   Contract values: USASpending FL food procurement
 *   Retention: Fed-Spend 2025, food industry benchmarks
 *   Tool pricing: cleat.ai, highergov.com, govspend.com (Feb 2026)
 *   Costs: BD/marketing benchmarks, consultant retainer, fulfillment overhead
 *
 * Architecture:
 *   10 contract tiers × 6 computation periods (Y1H1, Y1H2, Y2, Y3, Y4, Y5)
 *   2 routes: Free ($0 tools) vs Paid ($13.9K/yr tools)
 *   3 scenarios: Conservative (65%) / Moderate (70%) / Aggressive (85% renewal)
 *   Mechanical: bids × winRate = wins, priorActive × renewal = renewals
 *   Sliders adjust proportionally from research baselines
 */

// ═══════════════════════════════════════════════════════════════════════════════
// TIER DEFINITIONS — 10 internal tiers
// Source: govcon/docs/revenue-ramp-model.md (locked ACVs)
// ═══════════════════════════════════════════════════════════════════════════════

const TIERS = [
  { key: 'fedMicro',       acv: 7500,    group: 'fedMicro',      isSub: false },
  { key: 'fedSimplified',  acv: 85000,   group: 'fedSimplified', isSub: false },
  { key: 'schoolDistrict', acv: 500000,  group: 'sled',          isSub: false },
  { key: 'countyJail',     acv: 3000000, group: 'sled',          isSub: false },
  { key: 'dlaSub',         acv: 625000,  group: 'sub',           isSub: true },
  { key: 'fsmcSub',        acv: 2750000, group: 'sub',           isSub: true },
  { key: 'cooperative',    acv: 150000,  group: 'sled',          isSub: false },
  { key: 'mentorProtege',  acv: 2000000, group: 'setAside',      isSub: false },
  { key: 'fedSetAside',    acv: 500000,  group: 'setAside',      isSub: false },
  { key: 'fedLarge',       acv: 750000,  group: 'setAside',      isSub: false },
]

// ═══════════════════════════════════════════════════════════════════════════════
// GROUPED TIER CONFIGS — 5 display tiers for chart
// Source: govcon/docs/revenue-ramp-model.md "Portfolio Evolution (Grouped)"
// ═══════════════════════════════════════════════════════════════════════════════

export const TIER_CONFIGS = [
  { key: 'fedMicro',      label: 'Federal Micro',      color: '#C9A84C' },
  { key: 'fedSimplified', label: 'Federal Simplified',  color: '#1B7A8A' },
  { key: 'sled',          label: 'SLED',                color: '#239BAD' },
  { key: 'sub',           label: 'Subcontracting',      color: '#10b981' },
  { key: 'setAside',      label: 'Set-Aside / JV',      color: '#E8913A' },
]

// ═══════════════════════════════════════════════════════════════════════════════
// SCENARIO PARAMS — labels + colors for ScenarioToggle, renewal rates for engine
// Scenarios differ by renewal rate (primary long-term revenue driver)
// Source: Fed-Spend 2025 (70% incumbent), food industry benchmarks (85-90%+)
// ═══════════════════════════════════════════════════════════════════════════════

export const SCENARIO_PARAMS = {
  conservative: {
    label: 'Conservative',
    color: '#71717a',
    renewalRate: 0.65,
  },
  moderate: {
    label: 'Moderate',
    color: '#1B7A8A',
    renewalRate: 0.70,
  },
  aggressive: {
    label: 'Aggressive',
    color: '#C9A84C',
    renewalRate: 0.85,
  },
}

// Sub-tier renewal rate — relationship-based, always 85%+
const SUB_RENEWAL_RATE = 0.85

// ═══════════════════════════════════════════════════════════════════════════════
// ROUTE PARAMS — cost structures for Free vs Paid tool routes
// Source: govcon/docs/tool-capabilities.md (corrected pricing Feb 28, 2026)
//   CLEATUS: $3,360/yr | HigherGov: $500/yr (Starter) | GovSpend: ~$10,000/yr
// Source: govcon/docs/bd-marketing-personnel-costs.md
//   Consultant: $42-60K free, $90-120K paid | BD/Marketing: $13K Y1 recommended
// ═══════════════════════════════════════════════════════════════════════════════

const ROUTE_PARAMS = {
  free: {
    annualToolCost: 0,
    annualConsultantCost: 51000,   // Midpoint $42-60K (Foundation tier)
    annualBdCost: 13060,           // Recommended Y1 minimum
  },
  paid: {
    annualToolCost: 13860,         // CLEATUS $3,360 + HigherGov $500 + GovSpend $10,000
    annualConsultantCost: 105000,  // Midpoint $90-120K (Growth tier)
    annualBdCost: 13060,
  },
}

// ═══════════════════════════════════════════════════════════════════════════════
// SLIDER CONFIGS — adjustable inputs for presentation controls
// ═══════════════════════════════════════════════════════════════════════════════

export const SLIDER_CONFIGS = [
  { key: 'grossMargin',        label: 'Gross Margin',  min: 0.08, max: 0.25, step: 0.005, default: 0.11, format: 'percent' },
  { key: 'bidVolumeMultiplier', label: 'Bid Volume',   min: 0.5,  max: 2.0,  step: 0.1,   default: 1.0,  format: 'multiplier' },
  { key: 'winRateAdjustment',  label: 'Win Rate Adj.', min: -0.10, max: 0.10, step: 0.01,  default: 0,    format: 'percentSigned' },
]

// ═══════════════════════════════════════════════════════════════════════════════
// BID ALLOCATIONS — per tier, per period, per route
// Source: govcon/docs/revenue-ramp-model.md Tables 1 (Paid & Free)
// Periods: [Y1H1, Y1H2, Y2, Y3, Y4, Y5]
// ═══════════════════════════════════════════════════════════════════════════════

const BID_ALLOCATIONS = {
  paid: {
    fedMicro:       [100, 80, 60, 30, 15, 10],
    fedSimplified:  [15,  30, 50, 40, 35, 30],
    schoolDistrict: [0,   5,  8,  6,  5,  4],
    countyJail:     [0,   0,  3,  2,  2,  2],
    dlaSub:         [3,   3,  3,  2,  2,  2],
    fsmcSub:        [0,   2,  2,  3,  3,  3],
    cooperative:    [0,   0,  7,  3,  4,  5],
    mentorProtege:  [0,   0,  0,  3,  4,  5],
    fedSetAside:    [0,   0,  0,  5,  6,  8],
    fedLarge:       [0,   0,  0,  0,  0,  3],
  },
  free: {
    fedMicro:       [8,  10, 12, 8,  5,  3],
    fedSimplified:  [12, 15, 20, 18, 15, 12],
    schoolDistrict: [0,  3,  4,  4,  3,  3],
    countyJail:     [0,  0,  2,  2,  2,  1],
    dlaSub:         [2,  2,  2,  2,  1,  1],
    fsmcSub:        [0,  1,  1,  2,  2,  2],
    cooperative:    [0,  0,  3,  2,  3,  3],
    mentorProtege:  [0,  0,  0,  2,  3,  3],
    fedSetAside:    [0,  0,  0,  3,  4,  5],
    fedLarge:       [0,  0,  0,  0,  0,  0],
  },
}

// ═══════════════════════════════════════════════════════════════════════════════
// WIN RATES — per tier, per period (shared across routes)
// Source: govcon/docs/win-rates-progression.md
// Used for slider adjustments: winRateScale = (baseRate + adjustment) / baseRate
// Periods: [Y1H1, Y1H2, Y2, Y3, Y4, Y5]
// ═══════════════════════════════════════════════════════════════════════════════

const WIN_RATES = {
  fedMicro:       [0.20,  0.38,  0.48,  0.55,  0.55,  0.55],
  fedSimplified:  [0.08,  0.18,  0.30,  0.40,  0.40,  0.40],
  schoolDistrict: [0,     0.40,  0.42,  0.42,  0.42,  0.42],
  countyJail:     [0,     0,     0.38,  0.42,  0.42,  0.42],
  dlaSub:         [0,     0,     0.22,  0.50,  0.50,  0.50],
  fsmcSub:        [0,     0,     0.50,  0.60,  0.60,  0.60],
  cooperative:    [0,     0,     1.00,  1.00,  1.00,  1.00],
  mentorProtege:  [0,     0,     0,     0.25,  0.30,  0.35],
  fedSetAside:    [0,     0,     0,     0.30,  0.35,  0.40],
  fedLarge:       [0,     0,     0,     0,     0,     0.20],
}

// ═══════════════════════════════════════════════════════════════════════════════
// RESEARCH WINS — exact validated win counts from research Table 2
// Source: govcon/docs/revenue-ramp-model.md Table 2 (Paid & Free)
// These are the ground truth. At default slider positions, the engine uses
// these directly. Slider adjustments scale proportionally from these baselines.
// This avoids rounding artifacts on high-ACV tiers (e.g., 1 FSMC win = $2.75M).
// Periods: [Y1H1, Y1H2, Y2, Y3, Y4, Y5]
// ═══════════════════════════════════════════════════════════════════════════════

const RESEARCH_WINS = {
  paid: {
    fedMicro:       [20, 30, 28, 16, 8,  6],
    fedSimplified:  [1,  5,  15, 16, 14, 12],
    schoolDistrict: [0,  2,  3,  3,  2,  2],
    countyJail:     [0,  0,  1,  1,  1,  1],
    dlaSub:         [0,  0,  1,  1,  1,  1],
    fsmcSub:        [0,  0,  1,  2,  2,  2],
    cooperative:    [0,  0,  7,  3,  4,  5],
    mentorProtege:  [0,  0,  0,  1,  1,  2],
    fedSetAside:    [0,  0,  0,  2,  2,  3],
    fedLarge:       [0,  0,  0,  0,  0,  1],
  },
  free: {
    fedMicro:       [2, 4, 6,  4, 3, 2],
    fedSimplified:  [1, 3, 6,  7, 6, 5],
    schoolDistrict: [0, 1, 2,  2, 1, 1],
    countyJail:     [0, 0, 1,  1, 1, 0],
    dlaSub:         [0, 0, 0,  1, 0, 0],
    fsmcSub:        [0, 0, 0,  1, 1, 1],
    cooperative:    [0, 0, 3,  2, 3, 3],
    mentorProtege:  [0, 0, 0,  0, 1, 1],
    fedSetAside:    [0, 0, 0,  1, 1, 2],
    fedLarge:       [0, 0, 0,  0, 0, 0],
  },
}

// Period configs: factor is 0.5 for half-year periods, 1.0 for annual
const PERIODS = [
  { factor: 0.5 },  // Y1H1
  { factor: 0.5 },  // Y1H2
  { factor: 1.0 },  // Y2
  { factor: 1.0 },  // Y3
  { factor: 1.0 },  // Y4
  { factor: 1.0 },  // Y5
]

// Model constants
const FULFILLMENT_OH_RATE = 0.05   // 5% of revenue — gov compliance overhead
const DSO_DAYS = 25                // Blended: federal food 7-15 + SLED 30-45

// ═══════════════════════════════════════════════════════════════════════════════
// COMPUTATION ENGINE
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Compute 5-year pro forma for a single scenario × route combination.
 *
 * Uses research-validated win counts as baseline. At default slider positions,
 * output exactly matches govcon/docs/revenue-ramp-model.md. Slider adjustments
 * scale proportionally from these baselines:
 *   - bidVolumeMultiplier: scales wins linearly (more bids → more wins)
 *   - winRateAdjustment: scales wins by (baseRate + adj) / baseRate
 *   - grossMargin: only affects cost side, not revenue
 *
 * Renewals are computed mechanically: priorActive × scenarioRenewalRate.
 * This means scenarios (65/70/85% renewal) produce properly compounded
 * differences across the 5-year horizon.
 *
 * @param {string} scenarioKey - 'conservative' | 'moderate' | 'aggressive'
 * @param {string} routeKey - 'free' | 'paid'
 * @param {object} overrides - { grossMargin, bidVolumeMultiplier, winRateAdjustment }
 * @returns {{ years: Array, summary: object }}
 */
export function computeProForma(scenarioKey = 'moderate', routeKey = 'free', overrides = {}) {
  const scenario = SCENARIO_PARAMS[scenarioKey]
  const route = ROUTE_PARAMS[routeKey]
  const bidAlloc = BID_ALLOCATIONS[routeKey]
  const researchWins = RESEARCH_WINS[routeKey]

  const grossMargin = overrides.grossMargin ?? 0.11
  const bidVolumeMultiplier = overrides.bidVolumeMultiplier ?? 1.0
  const winRateAdjustment = overrides.winRateAdjustment ?? 0

  // Track prior active contracts per tier for renewal computation
  const priorActive = {}
  TIERS.forEach(t => { priorActive[t.key] = 0 })

  // ── Phase 1: Compute all 6 periods at tier level ──
  const periodResults = PERIODS.map((period, pi) => {
    const tierData = {}
    let totalBids = 0
    let totalNewWins = 0
    let totalRenewals = 0
    let totalActive = 0
    let totalRevenue = 0

    TIERS.forEach(tier => {
      const baseBids = bidAlloc[tier.key][pi]
      const adjustedBids = Math.round(baseBids * bidVolumeMultiplier)

      // New wins: scale from research baseline
      const baseWins = researchWins[tier.key][pi]
      const baseWinRate = WIN_RATES[tier.key][pi]
      let newWins
      if (baseWins === 0 || baseBids === 0) {
        // Research says 0 wins for this tier/period — respect that baseline.
        // Only deviate if user actively adjusted sliders (bid volume or win rate).
        if (baseWinRate === 0 || baseBids === 0) {
          newWins = 0  // Channel locked or no bids — always zero
        } else if (bidVolumeMultiplier === 1.0 && winRateAdjustment === 0) {
          newWins = 0  // Sliders at defaults — use research baseline (0)
        } else {
          // User adjusted sliders — recompute, may cross threshold
          const adjustedWinRate = Math.max(0, Math.min(1, baseWinRate + winRateAdjustment))
          newWins = Math.max(0, Math.round(adjustedBids * adjustedWinRate))
        }
      } else {
        // Scale research wins proportionally by slider adjustments
        const adjustedWinRate = Math.max(0, Math.min(1, baseWinRate + winRateAdjustment))
        const winScale = bidVolumeMultiplier * (adjustedWinRate / baseWinRate)
        newWins = Math.max(0, Math.round(baseWins * winScale))
      }

      // Sub tiers always renew at SUB_RENEWAL_RATE; others use scenario rate
      const renewalRate = tier.isSub
        ? Math.max(scenario.renewalRate, SUB_RENEWAL_RATE)
        : scenario.renewalRate
      const renewals = Math.round(priorActive[tier.key] * renewalRate)

      const active = newWins + renewals
      const revenue = active * tier.acv * period.factor

      tierData[tier.key] = { bids: adjustedBids, newWins, renewals, active, revenue }

      totalBids += adjustedBids
      totalNewWins += newWins
      totalRenewals += renewals
      totalActive += active
      totalRevenue += revenue

      // Update prior active for next period
      priorActive[tier.key] = active
    })

    return { totalBids, totalNewWins, totalRenewals, totalActive, totalRevenue, tierData }
  })

  // ── Phase 2: Consolidate into 5 annual years ──
  let cumulativeRevenue = 0
  const years = []

  for (let yr = 1; yr <= 5; yr++) {
    let bidsSubmitted, newWins, renewals, activeContracts, revenue, annualTierData

    if (yr === 1) {
      // Combine Y1H1 (period 0) and Y1H2 (period 1)
      const h1 = periodResults[0]
      const h2 = periodResults[1]
      bidsSubmitted = h1.totalBids + h2.totalBids
      newWins = h1.totalNewWins + h2.totalNewWins
      renewals = h1.totalRenewals + h2.totalRenewals
      activeContracts = h2.totalActive  // End-of-year = end of H2
      revenue = h1.totalRevenue + h2.totalRevenue

      // Merge tier data across half-years
      annualTierData = {}
      TIERS.forEach(tier => {
        const t1 = h1.tierData[tier.key]
        const t2 = h2.tierData[tier.key]
        annualTierData[tier.key] = {
          bids: t1.bids + t2.bids,
          newWins: t1.newWins + t2.newWins,
          renewals: t1.renewals + t2.renewals,
          active: t2.active,  // End-of-year
          revenue: t1.revenue + t2.revenue,
        }
      })
    } else {
      // Years 2-5 map to periods 2-5
      const p = periodResults[yr]
      bidsSubmitted = p.totalBids
      newWins = p.totalNewWins
      renewals = p.totalRenewals
      activeContracts = p.totalActive
      revenue = p.totalRevenue
      annualTierData = p.tierData
    }

    // ── Financial computations ──
    const cogs = Math.round(revenue * (1 - grossMargin))
    const grossProfit = Math.round(revenue * grossMargin)
    const fulfillmentOH = Math.round(revenue * FULFILLMENT_OH_RATE)
    const toolCost = route.annualToolCost
    // Admin cost = consultant + BD/marketing + fulfillment overhead
    const adminCost = route.annualConsultantCost + route.annualBdCost + fulfillmentOH
    const netIncome = grossProfit - toolCost - adminCost

    cumulativeRevenue += revenue
    const workingCapital = Math.round((revenue / 12) * (DSO_DAYS / 30))
    const totalInvestment = toolCost + route.annualConsultantCost + route.annualBdCost
    const roi = totalInvestment > 0
      ? netIncome / totalInvestment
      : (netIncome > 0 ? Infinity : 0)

    // ── Build grouped tier breakdown for chart ──
    const tiers = TIER_CONFIGS.map(tc => {
      let contracts = 0
      let tierRevenue = 0
      TIERS.filter(t => t.group === tc.key).forEach(t => {
        contracts += annualTierData[t.key].active
        tierRevenue += annualTierData[t.key].revenue
      })
      return {
        key: tc.key,
        label: tc.label,
        color: tc.color,
        contracts,
        avgValue: contracts > 0 ? Math.round(tierRevenue / contracts) : 0,
        revenue: Math.round(tierRevenue),
      }
    })

    years.push({
      year: yr,
      bidsSubmitted,
      newWins,
      renewals,
      activeContracts,
      revenue: Math.round(revenue),
      cogs,
      grossProfit,
      toolCost,
      adminCost,
      netIncome,
      cumulativeRevenue: Math.round(cumulativeRevenue),
      roi,
      workingCapital,
      tiers,
    })
  }

  // ── Summary ──
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

/**
 * Compute all 3 scenarios for chart comparison.
 *
 * @param {string} routeKey - 'free' | 'paid'
 * @param {object} overrides - slider values
 * @returns {{ conservative: object, moderate: object, aggressive: object }}
 */
export function computeAllScenarios(routeKey = 'free', overrides = {}) {
  return {
    conservative: computeProForma('conservative', routeKey, overrides),
    moderate: computeProForma('moderate', routeKey, overrides),
    aggressive: computeProForma('aggressive', routeKey, overrides),
  }
}
