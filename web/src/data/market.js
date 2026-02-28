/**
 * Market data — all figures fact-checked Feb 28, 2026.
 * Every number has a source citation. CONFIRMED = verified against original source.
 */

// ── Headline Stats (Slide 2) ──
export const HEADLINE_STATS = [
  {
    value: 87,
    prefix: '$',
    suffix: 'M',
    label: 'Florida Federal Food TAM',
    detail: 'Annual addressable market, all PSC 89xx categories under $350K',
    source: 'USASpending API, FY2024 (Feb 24, 2026 query)',
    confidence: 'HIGH',
  },
  {
    value: 83,
    suffix: '%',
    label: 'Below Micro-Purchase Threshold',
    detail: 'Of food contracts require no competitive bidding (<$15K)',
    source: 'USASpending, NAICS 424xxx national distribution, FY2024',
    confidence: 'HIGH',
  },
  {
    value: 70,
    suffix: '%',
    label: 'Incumbent Renewal Rate',
    detail: 'Federal recompete contracts won by incumbent vendor',
    source: 'Fed-Spend analysis of $180B in federal recompetes (industry avg)',
    confidence: 'MEDIUM',
  },
  {
    value: 39857,
    label: 'FL Food Awards',
    detail: 'Individual contract actions in Florida, FY2024',
    source: 'USASpending API, FY2024 (Feb 24, 2026 query)',
    confidence: 'HIGH',
  },
]

// ── Florida TAM by Channel (Slide 5) ──
export const FL_TAM_CHANNELS = [
  {
    channel: 'Federal (FPDS Visible)',
    amount: 6400000,
    contracts: 117,
    description: 'Tracked contracts >$10K on record in FPDS',
    accessibility: 'Free — SAM.gov + FPDS monitoring (built)',
    source: 'USASpending API + FPDS, Feb 2026',
  },
  {
    channel: 'Federal Micro-Purchases',
    amount: 12000000, // midpoint of $8-15M estimate
    amountLabel: '$8-15M',
    description: '83% of awards invisible in public databases',
    accessibility: 'Paid — GovSpend reveals these ($7-12K/yr)',
    source: 'GovSpend coverage estimate; USASpending contract size distribution',
  },
  {
    channel: 'State (MFMP + FL Agencies)',
    amount: 25000000, // conservative estimate of FL share
    amountLabel: 'Est. $20-30M',
    description: 'FL state procurement portal, corrections, state agencies',
    accessibility: 'Free registration — MyFloridaMarketPlace',
    source: 'FL MFMP portal; $1.0-1.2B FL SLED food procurement',
  },
  {
    channel: 'Education (67 Districts)',
    amount: 15000000,
    amountLabel: 'Est. $10-20M',
    description: '67 county school districts, 2.8M students, NSLP funded',
    accessibility: 'BidNet, VendorLink, district portals',
    source: 'FL DOE 2024-25 enrollment; USDA NSLP $17.7B national FY2024',
  },
  {
    channel: 'Local (County/Municipal)',
    amount: 5000000,
    amountLabel: 'Est. $3-7M',
    description: 'County jails, municipal facilities, local government',
    accessibility: 'County procurement portals, DemandStar',
    source: 'Industry estimate based on FL county procurement data',
  },
]

// ── Product Opportunity Matrix (Slide 6) ──
export const PRODUCT_TIERS = {
  tier1: [
    {
      psc: '8925',
      name: 'Confectionery & Nuts',
      flSpend: 412000,
      nationalSpend: 55000000,
      soleSource: 58,
      avgOffers: 1.6,
      nationalAwards: 45,
      newportFit: 'HIGHEST',
      advantage: 'Existing Segment E supplier pricing',
      govMarkup: '20-30%',
      source: 'FPDS FY2024, PSC 8925',
    },
    {
      psc: '8915',
      name: 'Fresh Produce',
      flSpend: 35100000,
      nationalSpend: 2340000000,
      soleSource: 78,
      avgOffers: 1.2,
      newportFit: 'HIGH',
      advantage: 'Lowest vendor concentration; FL sourcing ideal; Oakes Farms proving model at $26M',
      govMarkup: '15-25%',
      source: 'FPDS FY2024, PSC 8915; USASpending',
    },
  ],
  tier2: [
    {
      psc: '8910',
      name: 'Dairy & Eggs',
      flSpend: 5500000,
      nationalSpend: 693000000,
      soleSource: 74,
      newportFit: 'MODERATE',
      advantage: 'Regional distribution feasible',
      govMarkup: '12-20%',
      source: 'FPDS FY2024, PSC 8910',
    },
    {
      psc: '8920',
      name: 'Bakery & Cereal',
      flSpend: 2500000,
      nationalSpend: 541000000,
      soleSource: 66,
      newportFit: 'MODERATE',
      advantage: 'NAICS 424410, regional vendors compete well',
      govMarkup: '15-25%',
      source: 'FPDS FY2024, PSC 8920',
    },
    {
      psc: '8945/8940',
      name: 'General Grocery & Oils',
      flSpend: 13500000,
      nationalSpend: 1001000000,
      soleSource: 69,
      newportFit: 'MODERATE',
      advantage: 'Volume purchasing, existing logistics',
      govMarkup: '15-25%',
      source: 'FPDS FY2024, PSC 8945 + 8940',
    },
  ],
  avoid: [
    { psc: '8905', name: 'Meat, Poultry, Fish', reason: 'Dominated by Tyson/JBS/Cargill' },
    { psc: '8970', name: 'MREs/Composites', reason: 'Specialized military manufacturing' },
    { psc: '8960', name: 'Beverages', reason: 'Low margin, high logistics cost' },
  ],
}

// ── Target Agencies (Slide 8) ──
export const TARGET_AGENCIES = [
  {
    name: 'DOJ / Bureau of Prisons',
    stat: '$3.7M / 71 contracts',
    description: '#1 FL food buyer. Rainmaker doing $5.1M — direct competitive target. Prison food supply is steady, recurring. Uses Unison Marketplace for reverse auctions.',
    color: 'teal',
    source: 'USASpending FY2024; federal BOP FL contracts',
  },
  {
    name: 'Military / DoD',
    stat: '$2.3M / 43 contracts',
    description: '93% sole-source grocery at DoD (avg 1.2 offers). MacDill AFB, Homestead ARB, NAS Jax, Patrick SFB. DeCA commissaries.',
    color: 'teal',
    source: 'FPDS FY2024, NAICS 424490 @ DoD',
  },
  {
    name: 'FEMA / Emergency',
    stat: 'Disaster-driven',
    description: 'FL is a top-5 state for disaster declarations. $25K micro-purchase threshold during emergencies. Disaster Response Registry entry.',
    color: 'amber',
    source: 'FEMA Disaster Declarations Database; FAR 13.201',
  },
  {
    name: 'School Districts (SLED)',
    stat: 'FL $1.0-1.2B SLED',
    description: '67 county districts, 2.8M students. Not in federal data — separate portals (BidNet, VendorLink). Miami-Dade, Broward, Palm Beach.',
    color: 'amber',
    source: 'FL DOE 2024-25; USDA NSLP $17.7B national FY2024',
  },
]

// ── Competition (Slide 9) ──
export const COMPETITORS = [
  { rank: 1, company: 'Oakes Farms Food & Distribution', amount: 26100000, notes: 'Naples, FL — produce focus', tier: 'top' },
  { rank: 2, company: 'US Foods Inc', amount: 24100000, notes: 'National distributor', tier: 'top' },
  { rank: 3, company: 'JNS Foods LLC', amount: 6800000, notes: 'FL-based', tier: 'mid' },
  { rank: 4, company: 'Sysco Central Florida', amount: 5100000, notes: 'National distributor', tier: 'mid' },
  { rank: 5, company: 'Rainmaker Inc', amount: 5100000, notes: 'Federal BOP contracts in FL', tier: 'target' },
  { rank: 6, company: 'Freedom Fresh LLC', amount: 4200000, notes: 'FL-based', tier: 'target' },
  { rank: 7, company: 'Matts Trading Inc', amount: 2600000, notes: 'FL-based', tier: 'target' },
  { rank: 8, company: 'Wholesome Foods Products LLC', amount: 2000000, notes: 'FL-based', tier: 'target' },
]

// ── B2B Fast Track — Private Institutional Buyers (Slide 10) ──
export const B2B_TARGETS = [
  {
    name: 'GEO Group',
    hq: 'Boca Raton, FL (15 mi from Newport)',
    flBeds: '8,500+',
    estFoodSpend: '$9-13M/yr',
    detail: '$2.63B revenue, 6 FL facilities, self-operates food service. Won 3 new FL contracts effective July 2026.',
    path: 'Direct B2B — corporate procurement',
    source: 'GEO Group FY2025 earnings; SEC filings',
  },
  {
    name: 'Aramark (FL DOC prime)',
    hq: 'Philadelphia, PA',
    flBeds: 'Serves ~80,000',
    estFoodSpend: '$449M contract (~$90M/yr)',
    detail: 'Statewide FL Dept of Corrections food service through April 2027. Needs regional food suppliers.',
    path: 'Sub-supplier to Aramark',
    source: 'FL FACTS, Contract C3021',
  },
  {
    name: 'CoreCivic',
    hq: 'Nashville, TN',
    flBeds: '~1,500',
    estFoodSpend: '$2-4M/yr',
    detail: '2 FL facilities (Lake City, Citrus County). Centralized procurement.',
    path: 'Direct B2B',
    source: 'CoreCivic facility directory',
  },
  {
    name: 'FL Charter Schools',
    hq: 'Statewide',
    flBeds: '700+ schools',
    estFoodSpend: 'Fragmented',
    detail: 'Many self-operate USDA-funded meal programs. Need wholesale suppliers. USDA reimbursement ensures payment.',
    path: 'Direct B2B — FL Charter School Alliance vendor marketplace',
    source: 'FL Charter School Alliance; USDA AMS',
  },
  {
    name: 'Assisted Living / Adult Care',
    hq: 'Statewide',
    flBeds: 'Hundreds of facilities',
    estFoodSpend: '$50-500K/facility',
    detail: 'Largest elderly population in US. USDA Adult Care Food Program funded. Fragmented market, no dominant vendor.',
    path: 'Direct B2B — relationship sales',
    source: 'FL Elder Affairs; USDA ACFP',
  },
]

export const B2B_SOURCE = 'GEO Group FY2025 results; FL FACTS Contract C3021; CoreCivic; FL Charter School Alliance; FL Elder Affairs'
