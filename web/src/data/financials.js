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

const TIERS = ['micro', 'simplified', 'sled', 'sealed', 'subcontracting']

// Source: FPDS FY2024 ($85K simplified avg), USASpending FL ($200K+ small SLED districts)
// Values below are conservative — below validated research midpoints
const TIER_AVG_VALUES = {
  micro: 8000,            // Research: $7,500 (FPDS). Using $8K.
  simplified: 75000,      // Research: $85K (FPDS). Using $75K (conservative).
  sled: 150000,           // Research: $200K-$3M (small districts). Using $150K (floor).
  sealed: 350000,         // Research: $500K-$1M (federal large). Using $350K (conservative).
  subcontracting: 150000, // FSMC sub avg (Aramark, Compass, Sodexo, PFG/Cheney, GEO)
}

const TIER_LABELS = {
  micro: 'Micro (<$15K)',
  simplified: 'Simplified ($15-350K)',     // FAR threshold updated Oct 1, 2025
  sled: 'SLED',
  sealed: 'Sealed Bid ($350K+)',           // FAR threshold updated Oct 1, 2025
  subcontracting: 'Subcontracting (FSMC)',
}

const TIER_COLORS = {
  micro: '#d4d4d8',
  simplified: '#1B7A8A',
  sled: '#239BAD',
  sealed: '#C9A84C',
  subcontracting: '#E8913A',
}

// Tier mix evolves by year (Y1-Y5, index 0-4)
// Source: FINANCIAL-SLIDES-BUILD.md contract tier mix table
// Base mix (without GFSI/subcontracting) — sums to 1.0 per year
const TIER_MIX_BASE = {
  micro:           [0.80, 0.55, 0.35, 0.25, 0.25],
  simplified:      [0.15, 0.30, 0.35, 0.30, 0.30],
  sled:            [0.05, 0.10, 0.20, 0.25, 0.25],
  sealed:          [0.00, 0.05, 0.10, 0.20, 0.20],
  subcontracting:  [0.00, 0.00, 0.00, 0.00, 0.00],
}

// Subcontracting mix when GFSI certified — other tiers reduced proportionally
const SUB_MIX_GFSI = [0.00, 0.05, 0.10, 0.15, 0.15]

function getTierMix(hasGfsiCert) {
  if (!hasGfsiCert) return TIER_MIX_BASE
  const mix = {}
  for (const t of TIERS) {
    if (t === 'subcontracting') {
      mix[t] = SUB_MIX_GFSI
    } else {
      // Reduce base tiers proportionally to make room for sub mix
      mix[t] = TIER_MIX_BASE[t].map((v, i) => {
        const subShare = SUB_MIX_GFSI[i]
        return v * (1 - subShare)
      })
    }
  }
  return mix
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

// Base bids/month before route multiplier (×2.5 for paid route)
// Research: paid route capacity 29-55 bids/month. Still Mind handles all BD.
// Conservative 3 (paid 7.5), Moderate 5 (paid 12.5), Aggressive 8 (paid 20)
export const SCENARIO_CONFIGS = {
  conservative: {
    label: 'Conservative',
    baseBidsPerMonth: 3,
    winRates: { y1h1: 0.15, y1h2: 0.23, y2: 0.28, y3to5: 0.33 },
    color: '#71717a',
  },
  moderate: {
    label: 'Moderate',
    baseBidsPerMonth: 5,
    winRates: { y1h1: 0.20, y1h2: 0.28, y2: 0.33, y3to5: 0.38 },
    color: '#1B7A8A',
  },
  aggressive: {
    label: 'Aggressive',
    baseBidsPerMonth: 8,
    winRates: { y1h1: 0.25, y1h2: 0.33, y2: 0.38, y3to5: 0.43 },
    color: '#C9A84C',
  },
}

// ── Slider configs ──

export const SLIDER_CONFIGS = [
  { key: 'grossMargin', label: 'Gross Margin', min: 0.10, max: 0.28, step: 0.005, default: 0.18, format: 'percent' },
  { key: 'deliveryCostPct', label: 'Delivery Cost', min: 0.02, max: 0.08, step: 0.005, default: 0.05, format: 'percent' },
  { key: 'adminOverhead', label: 'Admin / Owner Time', min: 0, max: 50000, step: 1000, default: 5000, format: 'currency' },
  { key: 'bdMarketingCost', label: 'BD / Marketing', min: 0, max: 30000, step: 1000, default: 13000, format: 'currency' },
]

// ── Toggle configs (Newport-specific yes/no inputs) ──

export const TOGGLE_CONFIGS = [
  { key: 'hasInsurance', label: 'Have CGL Insurance?', default: false, description: 'Reduces insurance line if you already carry general liability' },
  { key: 'hasGfsiCert', label: 'GFSI / SQF Certified?', default: false, description: 'Required for FSMC sub-contracting (Aramark, Compass, Sodexo)' },
]

// ── SBA Certification reference (data only — UI deferred, multipliers unvalidated) ──
// Note: 8(a) frozen under Trump SBA (97% reduction). HUBZone unlikely for Plantation FL.
// Mentor-Protege works via JV structure, not win rate multiplication.
// Multipliers are directional estimates — validate before building UI.

export const SBA_CERT_CONFIGS = {
  none: { label: 'None', winRateMultiplier: 1.0 },
  hubzone: { label: 'HUBZone', winRateMultiplier: 1.2 },
  mentorProtege: { label: 'Mentor-Protégé', winRateMultiplier: 1.3 },
  wosb: { label: 'WOSB', winRateMultiplier: 1.4 },
  sdvosb: { label: 'SDVOSB', winRateMultiplier: 1.4 },
}

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
function distributeTierWins(totalWins, yearIndex, tierMix) {
  if (totalWins === 0) return TIERS.map(t => ({ tier: t, count: 0 }))

  const raw = TIERS.map(t => ({
    tier: t,
    exact: totalWins * tierMix[t][yearIndex],
    count: Math.floor(totalWins * tierMix[t][yearIndex]),
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
 * @param {object} overrides - { grossMargin, deliveryCostPct, adminOverhead, ... }
 */
export function computeProForma(routeKey, scenarioKey, overrides = {}) {
  const route = ROUTE_CONFIGS[routeKey]
  const scenario = SCENARIO_CONFIGS[scenarioKey]

  const grossMargin = overrides.grossMargin ?? 0.18
  const deliveryCostPct = overrides.deliveryCostPct ?? 0.05
  const adminOverhead = overrides.adminOverhead ?? 5000
  const bdMarketingCost = overrides.bdMarketingCost ?? 13000
  const hasInsurance = overrides.hasInsurance ?? false
  const hasGfsiCert = overrides.hasGfsiCert ?? false

  const tierMix = getTierMix(hasGfsiCert)

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
  let cumulativeInvestment = 0
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
    const newWinDist = distributeTierWins(newWins, yearIdx, tierMix)

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
      tierKey: t,
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
    // Investment = all non-COGS operating costs
    const yearInvestment = deliveryCost + platformCost + adminOverhead + bdMarketingCost
    cumulativeInvestment += yearInvestment

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
      cumulativeInvestment,
    })

    // Carry forward for next year's renewal calculation
    TIERS.forEach(t => { priorActive[t] = activeTiers[t] })
  }

  const breakevenYear = years.find(y => y.netIncome > 0)?.year ?? null
  const y5 = years[4]

  // Owner economics
  const totalInvestment = y5.cumulativeInvestment
  const totalReturn = y5.cumulativeNetIncome
  const fiveYearROI = totalInvestment > 0 ? totalReturn / totalInvestment : 0
  const paybackYear = years.find(y => y.cumulativeNetIncome > 0)?.year ?? null

  return {
    route: routeKey,
    scenario: scenarioKey,
    overrides: { grossMargin, deliveryCostPct, adminOverhead, bdMarketingCost, hasInsurance, hasGfsiCert },
    years,
    summary: {
      breakevenYear,
      y5Revenue: y5.revenue,
      y5CumulativeRevenue: y5.cumulativeRevenue,
      y5ActiveContracts: y5.activeContracts,
      y5NetIncome: y5.netIncome,
      totalReturn,
      totalInvestment,
      fiveYearROI,
      paybackYear,
      cumulativeInvestment: years.map(y => y.cumulativeInvestment),
      cumulativeNetIncome: years.map(y => y.cumulativeNetIncome),
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

// ── Cash Flow Computation ──

// Blended DSO (days sales outstanding) by tier
const TIER_DSO = {
  micro: 10,
  simplified: 15,
  sled: 35,
  sealed: 30,
  subcontracting: 25,
}

const SUPPLIER_TERMS = 20 // avg days to pay suppliers

/**
 * Compute cash flow analysis from pro forma results.
 *
 * @param {object} proFormaResult - Output of computeProForma()
 * @param {number} workingCapital - Available working capital (default $75K)
 * @returns {{ years: object[], peakDeficit: number, paybackYear: number|null, isConstrained: boolean[] }}
 */
export function computeCashFlow(proFormaResult, workingCapital = 75000) {
  const cashYears = []
  let cumulativeCash = 0
  let peakDeficit = 0

  for (const yr of proFormaResult.years) {
    // Compute blended DSO weighted by tier revenue
    const totalRevenue = yr.revenue
    let weightedDSO = 0
    if (totalRevenue > 0) {
      for (const tb of yr.tierBreakdown) {
        const tierKey = tb.tierKey
        const dso = TIER_DSO[tierKey] ?? 20
        weightedDSO += (tb.revenue / totalRevenue) * dso
      }
    }

    // COGS float = cash tied up in inventory/receivables gap
    const cogsFloat = Math.round(yr.cogs * (weightedDSO - SUPPLIER_TERMS) / 365)

    // Cash timing: revenue collected minus lag, expenses paid on schedule
    const cashIn = Math.round(totalRevenue * (1 - weightedDSO / 365))
    const cashOut = yr.cogs + yr.deliveryCost + yr.platformCost + yr.adminOverhead + yr.bdMarketingCost
    const netCashFlow = cashIn - cashOut
    cumulativeCash += netCashFlow

    if (cumulativeCash < peakDeficit) peakDeficit = cumulativeCash

    const isConstrained = Math.abs(cogsFloat) > workingCapital

    cashYears.push({
      year: yr.year,
      blendedDSO: Math.round(weightedDSO),
      cogsFloat,
      cashIn,
      cashOut,
      netCashFlow,
      cumulativeCash,
      isConstrained,
    })
  }

  const paybackYear = cashYears.find(y => y.cumulativeCash > 0)?.year ?? null

  return {
    years: cashYears,
    peakDeficit,
    paybackYear,
    isConstrained: cashYears.map(y => y.isConstrained),
  }
}
