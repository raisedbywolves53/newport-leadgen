/**
 * Newport GovCon Financial Model — Computation Engine
 * Per FINANCIAL-SLIDES-BUILD.md spec
 *
 * Two-axis model:
 *   Route (Free/Paid) × Scenario (Conservative/Moderate/Aggressive)
 *   + 3 management input sliders (grossMargin, deliveryCostPct, adminOverhead)
 *
 * Data sources: FPDS FY2024, USASpending FL food procurement, Fed-Spend 2025
 */

// ── Tier definitions ──

const TIERS = ['micro', 'simplified', 'sled', 'sealed']

const TIER_AVG_VALUES = {
  micro: 8000,
  simplified: 50000,
  sled: 75000,
  sealed: 150000,
}

const TIER_LABELS = {
  micro: 'Micro (<$15K)',
  simplified: 'Simplified ($15-250K)',
  sled: 'SLED',
  sealed: 'Sealed Bid ($250K+)',
}

const TIER_COLORS = {
  micro: '#d4d4d8',
  simplified: '#1B7A8A',
  sled: '#239BAD',
  sealed: '#C9A84C',
}

// Tier mix evolves by year (Y1-Y5, index 0-4)
// Source: FINANCIAL-SLIDES-BUILD.md contract tier mix table
const TIER_MIX = {
  micro:      [0.80, 0.55, 0.35, 0.25, 0.25],
  simplified: [0.15, 0.30, 0.35, 0.30, 0.30],
  sled:       [0.05, 0.10, 0.20, 0.25, 0.25],
  sealed:     [0.00, 0.05, 0.10, 0.20, 0.20],
}

const RENEWAL_RATE = 0.70

// ── Route configs ──

export const ROUTE_CONFIGS = {
  free: {
    label: 'Free Route',
    platformCost: 0,
    insuranceCost: 500,
    conferenceCost: 0,
    bidMultiplier: 1.0,
    color: '#71717a',
  },
  paid: {
    label: 'Paid Route',
    platformCost: 13000,
    insuranceCost: 1500,
    conferenceCost: 2000,
    bidMultiplier: 2.5,
    color: '#1B7A8A',
  },
}

// ── Scenario configs ──

export const SCENARIO_CONFIGS = {
  conservative: {
    label: 'Conservative',
    baseBidsPerMonth: 1,
    winRates: { y1h1: 0.15, y1h2: 0.23, y2: 0.28, y3to5: 0.33 },
    color: '#71717a',
  },
  moderate: {
    label: 'Moderate',
    baseBidsPerMonth: 2,
    winRates: { y1h1: 0.20, y1h2: 0.28, y2: 0.33, y3to5: 0.38 },
    color: '#1B7A8A',
  },
  aggressive: {
    label: 'Aggressive',
    baseBidsPerMonth: 3,
    winRates: { y1h1: 0.25, y1h2: 0.33, y2: 0.38, y3to5: 0.43 },
    color: '#C9A84C',
  },
}

// ── Slider configs ──

export const SLIDER_CONFIGS = [
  { key: 'grossMargin', label: 'Gross Margin', min: 0.08, max: 0.15, step: 0.005, default: 0.11, format: 'percent' },
  { key: 'deliveryCostPct', label: 'Delivery Cost', min: 0.02, max: 0.08, step: 0.005, default: 0.04, format: 'percent' },
  { key: 'adminOverhead', label: 'Admin / Owner Time', min: 0, max: 50000, step: 1000, default: 5000, format: 'currency' },
  { key: 'bdMarketingCost', label: 'BD / Marketing', min: 0, max: 30000, step: 1000, default: 13000, format: 'currency' },
]

// ── Toggle configs (Newport-specific yes/no inputs) ──

export const TOGGLE_CONFIGS = [
  { key: 'hasInsurance', label: 'Have CGL Insurance?', default: false, description: 'Reduces insurance line if you already carry general liability' },
  { key: 'hasGfsiCert', label: 'GFSI / SQF Certified?', default: false, description: 'Required for FSMC sub-contracting (Aramark, Compass, Sodexo)' },
]

// ── Helpers ──

function getWinRate(scenario, year) {
  const wr = scenario.winRates
  if (year === 2) return wr.y2
  return wr.y3to5
}

/**
 * Distribute total wins across tiers per the year's mix percentages.
 * Uses largest-remainder method to ensure counts sum exactly to total.
 */
function distributeTierWins(totalWins, yearIndex) {
  if (totalWins === 0) return TIERS.map(t => ({ tier: t, count: 0 }))

  const raw = TIERS.map(t => ({
    tier: t,
    exact: totalWins * TIER_MIX[t][yearIndex],
    count: Math.floor(totalWins * TIER_MIX[t][yearIndex]),
  }))

  let remaining = totalWins - raw.reduce((s, r) => s + r.count, 0)

  // Distribute remainder by largest fractional part
  const byRemainder = raw
    .map((r, i) => ({ i, frac: r.exact - r.count }))
    .sort((a, b) => b.frac - a.frac)

  for (let j = 0; j < remaining; j++) {
    raw[byRemainder[j].i].count++
  }

  return raw.map(r => ({ tier: r.tier, count: r.count }))
}

// ── Main computation ──

/**
 * Compute 5-year pro forma for a route × scenario combination.
 *
 * Mechanical model:
 *   bidsSubmitted = baseBidsPerMonth × bidMultiplier × 12 (6 for each half of Y1)
 *   newWins = round(bids × winRate)
 *   renewals per tier = round(priorActive × 0.70)
 *   revenue = sum(activeContracts per tier × tier avg value)
 *
 * @param {string} routeKey - 'free' | 'paid'
 * @param {string} scenarioKey - 'conservative' | 'moderate' | 'aggressive'
 * @param {object} overrides - { grossMargin, deliveryCostPct, adminOverhead }
 */
export function computeProForma(routeKey, scenarioKey, overrides = {}) {
  const route = ROUTE_CONFIGS[routeKey]
  const scenario = SCENARIO_CONFIGS[scenarioKey]

  const grossMargin = overrides.grossMargin ?? 0.11
  const deliveryCostPct = overrides.deliveryCostPct ?? 0.04
  const adminOverhead = overrides.adminOverhead ?? 5000
  const bdMarketingCost = overrides.bdMarketingCost ?? 13000
  const hasInsurance = overrides.hasInsurance ?? false

  const bidsPerMonth = scenario.baseBidsPerMonth * route.bidMultiplier
  // If Newport already carries CGL, reduce insurance cost (they only need riders/upgrades)
  const effectiveInsurance = hasInsurance
    ? Math.round(route.insuranceCost * 0.3) // Just riders/upgrades on existing policy
    : route.insuranceCost
  const fixedCosts = route.platformCost + effectiveInsurance + route.conferenceCost

  // Per-tier active contracts carried forward for renewal calculation
  const priorActive = {}
  TIERS.forEach(t => { priorActive[t] = 0 })

  let cumulativeRevenue = 0
  let cumulativeNetIncome = 0
  const years = []

  for (let yr = 1; yr <= 5; yr++) {
    let bidsSubmitted, newWins, winRate

    if (yr === 1) {
      // Split into H1 and H2 with different win rates
      const h1Bids = Math.round(bidsPerMonth * 6)
      const h2Bids = Math.round(bidsPerMonth * 6)
      const h1Wins = Math.round(h1Bids * scenario.winRates.y1h1)
      const h2Wins = Math.round(h2Bids * scenario.winRates.y1h2)
      bidsSubmitted = h1Bids + h2Bids
      newWins = h1Wins + h2Wins
      winRate = bidsSubmitted > 0 ? newWins / bidsSubmitted : 0
    } else {
      bidsSubmitted = Math.round(bidsPerMonth * 12)
      winRate = getWinRate(scenario, yr)
      newWins = Math.round(bidsSubmitted * winRate)
    }

    // Distribute new wins across tiers per year's mix
    const yearIdx = yr - 1
    const newWinDist = distributeTierWins(newWins, yearIdx)

    // Renewals per tier from prior year active
    let totalRenewals = 0
    const renewalDist = {}
    TIERS.forEach(t => {
      renewalDist[t] = Math.round(priorActive[t] * RENEWAL_RATE)
      totalRenewals += renewalDist[t]
    })

    // Active = new wins + renewals, per tier
    const activeTiers = {}
    let totalActive = 0
    TIERS.forEach(t => {
      const nw = newWinDist.find(d => d.tier === t)?.count ?? 0
      activeTiers[t] = nw + renewalDist[t]
      totalActive += activeTiers[t]
    })

    // Tier breakdown for chart / tooltip
    const tierBreakdown = TIERS.map(t => ({
      tier: TIER_LABELS[t],
      count: activeTiers[t],
      avgValue: TIER_AVG_VALUES[t],
      revenue: activeTiers[t] * TIER_AVG_VALUES[t],
      color: TIER_COLORS[t],
    }))

    const revenue = tierBreakdown.reduce((s, t) => s + t.revenue, 0)

    // Costs
    const cogs = Math.round(revenue * (1 - grossMargin))
    const grossProfit = revenue - cogs
    const deliveryCost = Math.round(revenue * deliveryCostPct)
    const platformCost = fixedCosts
    const netIncome = grossProfit - deliveryCost - platformCost - adminOverhead - bdMarketingCost

    cumulativeRevenue += revenue
    cumulativeNetIncome += netIncome

    years.push({
      year: yr,
      bidsPerMonth,
      bidsSubmitted,
      winRate: Math.round(winRate * 1000) / 1000,
      newWins,
      renewals: totalRenewals,
      activeContracts: totalActive,
      tierBreakdown,
      revenue,
      cogs,
      grossProfit,
      deliveryCost,
      platformCost,
      adminOverhead,
      bdMarketingCost,
      netIncome,
      cumulativeRevenue,
      cumulativeNetIncome,
    })

    // Carry forward for next year's renewal calculation
    TIERS.forEach(t => { priorActive[t] = activeTiers[t] })
  }

  const breakevenYear = years.find(y => y.netIncome > 0)?.year ?? null
  const y5 = years[4]

  return {
    route: routeKey,
    scenario: scenarioKey,
    overrides: { grossMargin, deliveryCostPct, adminOverhead, bdMarketingCost, hasInsurance },
    years,
    summary: {
      breakevenYear,
      y5Revenue: y5.revenue,
      y5CumulativeRevenue: y5.cumulativeRevenue,
      y5ActiveContracts: y5.activeContracts,
      y5NetIncome: y5.netIncome,
      totalReturn: y5.cumulativeNetIncome,
    },
  }
}

/**
 * Compute all 3 scenarios for chart comparison.
 *
 * @param {string} routeKey - 'free' | 'paid'
 * @param {object} overrides - slider values
 */
export function computeAllScenarios(routeKey, overrides = {}) {
  return {
    conservative: computeProForma(routeKey, 'conservative', overrides),
    moderate: computeProForma(routeKey, 'moderate', overrides),
    aggressive: computeProForma(routeKey, 'aggressive', overrides),
  }
}
