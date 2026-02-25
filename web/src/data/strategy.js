/**
 * Strategy & execution data — slides 11-20.
 * All figures fact-checked Feb 25, 2026.
 */

// ── How It Works — Pipeline Stages (Slide 12) ──
export const PIPELINE_STAGES = [
  { name: 'Identify', description: 'Daily monitoring surfaces matches', color: 'slate' },
  { name: 'Score', description: 'Bid/no-bid evaluated (0-100)', color: 'teal' },
  { name: 'Pursue', description: 'Proposal in progress', color: 'teal' },
  { name: 'Submit', description: 'Bid delivered', color: 'amber' },
  { name: 'Win', description: 'Contract awarded', color: 'green' },
]

export const SOURCING_CHANNELS = [
  {
    title: 'Federal: SAM.gov',
    description: 'Automated daily monitoring of all food/grocery solicitations. Scores each opportunity, sends daily digests.',
    cost: 'Free (built)',
  },
  {
    title: 'State: MyFloridaMarketPlace',
    description: "FL's state procurement portal. School districts, corrections, state agencies. Separate from federal pipeline.",
    cost: 'Free registration',
  },
  {
    title: 'Micro-Purchases: GovSpend',
    description: '83% of food awards are micro-purchases invisible on SAM.gov. GovSpend reveals $8-15M/yr in FL transactions.',
    cost: '$6.5K/yr (recommended)',
  },
  {
    title: 'Set-Asides & Portals',
    description: 'SDB, HUBZone, 8(a) if eligible. BidNet, DemandStar, Unison Marketplace for BOP reverse auctions.',
    cost: 'Free if eligible',
  },
]

// ── Real Contract Examples (Slide 13) ──
export const CONTRACT_EXAMPLES = [
  {
    agency: 'MacDill AFB (DoD)',
    description: 'Fresh produce delivery, base dining facility',
    estValue: '$8,000-$12,000',
    type: 'Micro-purchase',
    competition: 'Sole-source likely',
    fit: 'HIGH',
  },
  {
    agency: 'Federal BOP — Coleman FCI',
    description: 'Shelf-stable food and snacks, quarterly delivery',
    estValue: '$12,000-$15,000',
    type: 'Micro-purchase',
    competition: '1-2 offers typical',
    fit: 'HIGH',
  },
  {
    agency: 'Homestead ARB (DoD)',
    description: 'Dairy and eggs, weekly delivery to commissary',
    estValue: '$5,000-$8,000',
    type: 'Micro-purchase',
    competition: 'Sole-source likely',
    fit: 'HIGH',
  },
  {
    agency: 'Broward County Schools',
    description: 'Confectionery and snack items, school year supply',
    estValue: '$25,000-$75,000',
    type: 'Simplified / SLED',
    competition: '2-4 vendors',
    fit: 'HIGHEST',
  },
  {
    agency: 'FL Dept of Corrections (via Aramark)',
    description: 'Regional produce and dry goods sub-supply',
    estValue: '$50,000-$200,000',
    type: 'B2B sub-supply',
    competition: 'Relationship-based',
    fit: 'HIGH',
  },
  {
    agency: 'FEMA (hurricane response)',
    description: 'Emergency food supply during declared disaster',
    estValue: '$15,000-$25,000',
    type: 'Disaster micro-purchase',
    competition: 'Local vendor preference (Stafford Act)',
    fit: 'MODERATE',
  },
  {
    agency: 'NAS Jacksonville (DoD)',
    description: 'General grocery and bakery items, base galley',
    estValue: '$10,000-$20,000',
    type: 'Micro / Simplified',
    competition: '93% sole-source at DoD grocery',
    fit: 'HIGH',
  },
  {
    agency: 'GEO Group — South Bay Correctional',
    description: 'Confectionery, snacks, dry goods for facility commissary',
    estValue: '$30,000-$100,000',
    type: 'B2B (private)',
    competition: 'Direct sales',
    fit: 'HIGHEST',
  },
]

export const CONTRACT_EXAMPLES_SOURCE = 'Representative examples based on USASpending FY2024 FL data, FPDS competition analysis, and private operator research'

// ── Risk & Compliance (Slide 17) ──
export const COMPLIANCE_REQUIRED = [
  { item: 'SAM.gov Registration', cost: '$0', timeline: '2-4 weeks', note: 'Federal requirement — free', source: 'SAM.gov' },
  { item: 'MFMP Vendor Registration', cost: '$0', timeline: '1-2 weeks', note: 'FL state portal — free', source: 'MyFloridaMarketPlace' },
  { item: 'Food Safety Cert (SQF/GFSI)', cost: '$0-$23.5K', timeline: '3-6 months', note: '$0 if already certified', source: 'SQF Institute' },
  { item: 'General Liability Insurance', cost: '$1.5-3K/yr', timeline: 'Immediate', note: 'May already have coverage', source: 'Industry standard' },
  { item: 'Legal Review (GSA terms)', cost: '$2.5-5K', timeline: '2-4 weeks', note: 'One-time review', source: 'FAR compliance' },
]

export const COMPLIANCE_NOT_NEEDED = [
  { item: 'DCAA-Compliant Accounting', cost: '$50-150K', note: 'Not required for food supply contracts', source: 'FAR 30/31' },
  { item: 'CMMC Cybersecurity', cost: '$25-100K', note: 'DoD IT only — not food procurement', source: 'CMMC 2.0 rule' },
  { item: 'Cost Accounting Standards', cost: '$20-50K', note: 'Only for $50M+ contracts', source: 'FAR 30.201' },
  { item: 'Performance Bonds', cost: '$10-30K', note: 'Rare for food supply under $250K', source: 'FAR 28.102' },
  { item: 'Facility Clearance', cost: '$15K+', note: 'Classified contracts only', source: 'NISPOM' },
]

// ── Recommendation: Full Visibility (Slide 18) ──
export const ROUTE_COMPARISON = [
  {
    feature: 'Federal Monitoring',
    free: 'SAM.gov API — 117 FL contracts visible',
    paid: '+ CLEATUS AI scoring ($3K/yr)',
  },
  {
    feature: 'State/Local (FL $600M+)',
    free: 'Manual portal checking',
    paid: 'HigherGov — 40K+ agencies ($3.5K/yr)',
  },
  {
    feature: 'Micro-Purchases (83% invisible)',
    free: 'Cannot see $8-15M/yr in FL',
    paid: 'GovSpend — 1,500+ FL transactions ($6.5K/yr)',
  },
  {
    feature: 'Competitive Intel',
    free: 'USASpending + FPDS (built)',
    paid: 'Same — already strong',
  },
  {
    feature: 'Market Coverage',
    free: '~40-50% visible',
    paid: '~90%+ visible',
  },
  {
    feature: 'Cost per Bid',
    free: 'Higher — manual research',
    paid: 'Lower — AI-assisted proposals',
  },
]

export const ROUTE_SOURCE = 'CLEATUS ($3K/yr); HigherGov ($3.5K/yr); GovSpend ($6.5K/yr) — pricing from specs/09-INTEGRATIONS.md'

// ── Key Questions (Slide 19) ──
export const KEY_QUESTIONS = [
  // Will This Work?
  {
    category: 'Will This Work?',
    priority: 'HIGHEST',
    question: 'What geographic areas can your trucks realistically service on a regular schedule?',
    whyItMatters: 'FL only = $87M federal TAM. SE region expands to $179M+. Determines every contract we can bid on.',
  },
  {
    category: 'Will This Work?',
    priority: 'HIGHEST',
    question: 'Which product categories can you deliver against — and where do you have the strongest supplier pricing?',
    whyItMatters: 'Determines which NAICS/PSC codes we target. Your wholesale pricing is the competitive advantage in LPTA evaluations.',
  },
  {
    category: 'Will This Work?',
    priority: 'HIGH',
    question: 'Can you handle NET 30-60 payment terms on government contracts?',
    whyItMatters: 'Federal averages NET 30; state/local can be NET 60-90. Limits contract size until cash position supports the float.',
  },
  {
    category: 'Will This Work?',
    priority: 'HIGH',
    question: 'Do you have refrigerated/cold chain trucks and warehouse capacity for 20-30 additional orders per month?',
    whyItMatters: 'Temperature-controlled delivery required for most food contracts. Capacity determines how fast we can scale.',
  },
  // What Are the Risks?
  {
    category: 'What Are the Risks?',
    priority: 'HIGH',
    question: 'Do you have existing food safety certifications (SQF/GFSI/HACCP)?',
    whyItMatters: 'If yes, Year 1 investment drops by $23.5K. If no, this is the biggest single compliance cost.',
  },
  {
    category: 'What Are the Risks?',
    priority: 'MEDIUM',
    question: 'Who would own government contract administration — an existing employee or a new role?',
    whyItMatters: 'Someone manages deadlines, compliance, reporting. We handle intelligence and bid prep, but fulfillment side needs an owner.',
  },
  {
    category: 'What Are the Risks?',
    priority: 'MEDIUM',
    question: 'What is your current gross margin on wholesale distribution?',
    whyItMatters: 'Determines if government margins (18-25%) are accretive or dilutive to your business. We don\'t assume — we ask.',
  },
  // How Much Bigger Could This Be?
  {
    category: 'How Much Bigger?',
    priority: 'HIGHEST',
    question: 'Do you qualify for any SBA set-aside programs — small business, minority-owned, veteran-owned, HUBZone?',
    whyItMatters: 'Set-aside eligibility could be the single biggest accelerant. Win rates jump to 28%+, less competition by design.',
  },
  {
    category: 'How Much Bigger?',
    priority: 'HIGH',
    question: 'Would you consider subcontracting or partnering to build past performance faster?',
    whyItMatters: 'Supplying a prime contractor (Aramark, GEO Group) builds institutional food supply credentials for future government bids.',
  },
  {
    category: 'How Much Bigger?',
    priority: 'MEDIUM',
    question: 'What is the 3-5 year vision — supplemental revenue channel or meaningful growth engine?',
    whyItMatters: 'Determines investment level, staffing trajectory, and whether we pursue aggressive expansion beyond FL.',
  },
]

// ── Blueprint / Responsibilities (Slide 20) ──
export const RESPONSIBILITIES = {
  diy: [
    'SAM.gov + portal registrations',
    'Daily opportunity monitoring',
    'Bid/no-bid evaluation',
    'Proposal writing & compliance docs',
    'Competitive intelligence research',
    'Pipeline tracking & reporting',
    'Front-line influencer sourcing',
    'Contract administration',
    'Relationship management',
    'Fulfillment & delivery',
  ],
  partnership: {
    newport: [
      'Fulfillment & delivery',
      'Business relationships & face-to-face meetings',
      'Product pricing decisions',
      'Contract administration (with our support)',
      'Strategic direction & go/no-go decisions',
    ],
    stillMind: [
      'Intelligence system & daily monitoring',
      'Bid scoring, proposal prep & compliance',
      'Competitive analysis & market tracking',
      'Front-line influencer identification',
      'Pipeline management & monthly reporting',
      'Strategy calibration & model updates',
    ],
  },
}
