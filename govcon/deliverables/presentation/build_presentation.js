/**
 * Newport GovCon Proposal Deck — v7 (18-Slide Rebuild)
 *
 * Generates an 18-slide 16:9 PowerPoint proposal for Newport Wholesalers.
 * Ocean Gradient palette: #065A82, #1C7293, #21295C
 *
 * v7 narrative arc: lead with Newport's 30-year moat, use Owner Earnings
 * (not just revenue), expand "How It Works" to 3 slides, add Risk/Compliance
 * and Key Questions slides.
 *
 * Reads deliverables/market_data.json for live FPDS/USASpending data.
 * Falls back to hardcoded values if market_data.json doesn't exist.
 *
 * Run: cd govcon/deliverables/presentation && node build_presentation.js
 * Output: govcon/deliverables/presentation/newport-govcon-proposal.pptx
 */

const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

// ---------------------------------------------------------------------------
// Load market data (with graceful fallback)
// ---------------------------------------------------------------------------
let marketData = null;
const marketDataPath = path.join(__dirname, "..", "market_data.json");
try {
  const raw = fs.readFileSync(marketDataPath, "utf-8");
  marketData = JSON.parse(raw);
  console.log(`Loaded market data from ${marketDataPath}`);
} catch (_) {
  console.log("market_data.json not found — using hardcoded fallback values");
}

// ---------------------------------------------------------------------------
// Financial data — pre-computed from v7 model (build_proforma.py)
// ---------------------------------------------------------------------------
const FALLBACK_FINANCIALS = {
  years: [1, 2, 3, 4, 5],
  bids:     [84, 92, 112, 130, 146],
  wins:     [10, 14, 19, 27, 34],
  active:   [10, 21, 34, 51, 70],
  renewed:  [0, 7, 15, 24, 36],
  revenue:  [99600, 440000, 985400, 1924000, 3004000],
  gross_profit: [21912, 96800, 216788, 423280, 660880],
  bid_prep: [21750, 50250, 76500, 97500, 109500],
  fulfillment: [2988, 13200, 29562, 57720, 90120],
  program:  [11000, 6000, 5000, 4000, 4000],
  owner_earnings: [-13826, 27350, 105726, 264060, 457260],
  cumulative_oe: [-13826, 13524, 119250, 383310, 840570],
};

// Fallback data — confirmed from live FPDS/USASpending reports + research foundation (Feb 2026)
const FALLBACK_NAICS = [
  { naics: "424490", description: "Other Grocery Products", awards: 138, avg_offers: 1.2, sole_source_pct: 93.2, avg_value: 78000 },
  { naics: "722310", description: "Food Service Contractors", awards: 322, avg_offers: 2.4, sole_source_pct: 62.1, avg_value: 168000 },
  { naics: "424430", description: "Dairy Product", awards: 14, avg_offers: 8.4, sole_source_pct: 14.3, avg_value: 49400 },
  { naics: "424440", description: "Poultry & Poultry Product", awards: 19, avg_offers: 5.6, sole_source_pct: 0, avg_value: 105500 },
  { naics: "424470", description: "Meat & Meat Product", awards: 11, avg_offers: 14.2, sole_source_pct: 0, avg_value: 57800 },
  { naics: "424410", description: "Grocery Wholesalers", awards: 14, avg_offers: 5.3, sole_source_pct: 14.3, avg_value: 57400 },
  { naics: "424480", description: "Fresh Fruit & Vegetable", awards: 12, avg_offers: 3.5, sole_source_pct: 83.3, avg_value: 56000 },
  { naics: "424420", description: "Packaged Frozen Food", awards: 2, avg_offers: 1.0, sole_source_pct: 100, avg_value: 33200 },
  { naics: "424460", description: "Fish & Seafood", awards: 2, avg_offers: 3.0, sole_source_pct: 0, avg_value: 55300 },
  { naics: "424450", description: "Confectionery", awards: 1, avg_offers: 1.0, sole_source_pct: 100, avg_value: 30300 },
];

const FALLBACK_TOTALS = { transactions: 537, avg_offers: 2.3, sole_source_pct: 56.2 };

const FALLBACK_PSC = [
  { psc: "8905", description: "Meat, Poultry, Fish", total_spending: 2840000000, avg_offers: 1.5, sole_source_pct: 63, opportunity_tier: "LOW" },
  { psc: "8915", description: "Fruits & Vegetables", total_spending: 2340000000, avg_offers: 1.2, sole_source_pct: 78, opportunity_tier: "HIGH" },
  { psc: "8945", description: "Food Oils & Fats", total_spending: 866000000, avg_offers: 1.3, sole_source_pct: 70, opportunity_tier: "MODERATE" },
  { psc: "8910", description: "Dairy & Eggs", total_spending: 693000000, avg_offers: 1.2, sole_source_pct: 74, opportunity_tier: "MODERATE" },
  { psc: "8970", description: "MREs/Composites", total_spending: 572000000, avg_offers: 1.1, sole_source_pct: 85, opportunity_tier: "NONE" },
  { psc: "8920", description: "Bakery & Cereal", total_spending: 541000000, avg_offers: 1.4, sole_source_pct: 66, opportunity_tier: "MODERATE" },
  { psc: "8940", description: "Special Dietary", total_spending: 135000000, avg_offers: 1.3, sole_source_pct: 68, opportunity_tier: "LOW" },
  { psc: "8960", description: "Beverages", total_spending: 123000000, avg_offers: 1.5, sole_source_pct: 60, opportunity_tier: "LOW" },
  { psc: "8925", description: "Confectionery & Nuts", total_spending: 55000000, avg_offers: 1.6, sole_source_pct: 58, opportunity_tier: "HIGH" },
  { psc: "8950", description: "Condiments", total_spending: 9000000, avg_offers: 1.3, sole_source_pct: 68, opportunity_tier: "LOW" },
];

const FALLBACK_PRODUCTS = {
  priority_products: [
    { psc: "8915", name: "Fresh Produce", tier: 1, annual_spending: 2340000000, rationale: "$35.1M in FL alone. Lowest vendor concentration. USDA actively diversifying vendors. Oakes Farms proving the model at $26M." },
    { psc: "8925", name: "Confectionery & Nuts", tier: 1, annual_spending: 55000000, rationale: "$412K FL, only 45 awards nationally, 58% sole-source. Newport's candy expertise (Segment E) = direct competitive advantage." },
    { psc: "8910", name: "Dairy & Eggs", tier: 2, annual_spending: 693000000, rationale: "$5.5M FL. Regional distribution feasible. Fluid milk/eggs accessible for wholesale distributors." },
    { psc: "8920", name: "Bakery & Cereal Products", tier: 2, annual_spending: 541000000, rationale: "$2.5M FL. Covered by NAICS 424410, regional vendors compete well, lower barriers." },
  ],
  avoid: [
    { psc: "8905", name: "Meat, Poultry, Fish", rationale: "Dominated by Tyson/JBS/Cargill (83% pork, 72% poultry market share)" },
    { psc: "8970", name: "MREs/Composite Food Packages", rationale: "Specialized military manufacturing, requires dedicated production facilities" },
  ],
};

// Top FL government food contractors — confirmed from USASpending FY2024
const FALLBACK_COMPETITORS = [
  { rank: 1, company: "Oakes Farms Food & Distribution", amount: 26100000, notes: "Naples, FL — produce focus" },
  { rank: 2, company: "US Foods Inc", amount: 24100000, notes: "National distributor" },
  { rank: 3, company: "JNS Foods LLC", amount: 6800000, notes: "FL-based" },
  { rank: 4, company: "Sysco Central Florida", amount: 5100000, notes: "National distributor" },
  { rank: 5, company: "Rainmaker Inc", amount: 5100000, notes: "FL DOJ prison contracts" },
  { rank: 6, company: "Freedom Fresh LLC", amount: 4200000, notes: "FL-based" },
  { rank: 7, company: "Matts Trading Inc", amount: 2600000, notes: "FL-based" },
  { rank: 8, company: "Wholesome Foods Products LLC", amount: 2000000, notes: "FL-based" },
  { rank: 9, company: "M&B Products", amount: 1200000, notes: "FL-based" },
  { rank: 10, company: "United Oil Packers", amount: 1200000, notes: "FL-based" },
];

// Compliance requirements — from research + v7 model
const COMPLIANCE_REQUIRED = [
  { item: "SAM.gov Registration", cost: "$0", timeline: "2-4 weeks", note: "Federal requirement — free" },
  { item: "MFMP Vendor Registration", cost: "$0", timeline: "1-2 weeks", note: "FL state portal — free" },
  { item: "Food Safety Cert (SQF/GFSI)", cost: "$0-$23.5K", timeline: "3-6 months", note: "$0 if already certified" },
  { item: "General Liability Insurance", cost: "$1.5-3K/yr", timeline: "Immediate", note: "May already have coverage" },
  { item: "Legal Review (GSA terms)", cost: "$2.5-5K", timeline: "2-4 weeks", note: "One-time review of gov terms" },
];

const COMPLIANCE_NOT_NEEDED = [
  { item: "DCAA-Compliant Accounting", cost: "$50-150K", note: "Not required for food supply contracts" },
  { item: "CMMC Cybersecurity", cost: "$25-100K", note: "DoD IT only — not food procurement" },
  { item: "Cost Accounting Standards (CAS)", cost: "$20-50K", note: "Only for $50M+ contracts" },
  { item: "Performance Bonds", cost: "$10-30K", note: "Rare for food supply under $250K" },
  { item: "Facility Clearance", cost: "$15K+", note: "Classified contracts only" },
];

// Key Questions — from v7 model Key Questions sheet
const KEY_QUESTIONS = [
  { priority: "1 HIGHEST", question: "Can Newport profitably fulfill orders under $5,200?", ifYes: "Micro channel opens (83% of awards). Credibility ramp starts.", ifNo: "Must skip to Simplified — harder, slower entry path" },
  { priority: "2 HIGHEST", question: "Eligible for SDB/HUBZone/8(a) set-aside?", ifYes: "Win rates 28%+, margins 25%. Available from Day 1.", ifNo: "Open competition only — lower win rates, slower ramp" },
  { priority: "3 HIGH", question: "Delivery radius from FL warehouses?", ifYes: "FL only = $85M. SE region = $179M. Determines total addressable.", ifNo: "We right-size model to actual reach" },
  { priority: "4 HIGH", question: "Existing food safety certs (SQF/GFSI)?", ifYes: "Year 1 investment drops by $23,500", ifNo: "Biggest single cost variable" },
  { priority: "5 HIGH", question: "Willing to invest $11K-$47K (Paid Route)?", ifYes: "Full competitive capability from Day 1. ROI positive by mid-Y2.", ifNo: "Free route works but 12-18 months slower to traction" },
  { priority: "6 MEDIUM", question: "How many confectionery/snack/nut SKUs?", ifYes: "Broader catalog = eligible for more bids across categories", ifNo: "We focus on strongest categories only" },
  { priority: "7 MEDIUM", question: "Can add delivery routes to bases/prisons?", ifYes: "DOJ/BOP channel opens ($5M+ FL). Rainmaker Inc. is beatable.", ifNo: "Skip DOJ, focus DeCA commissaries instead" },
  { priority: "8 MEDIUM", question: "Current commercial gross margin?", ifYes: "Calibrates if gov margins (18-25%) are accretive or dilutive", ifNo: "May not be worth pursuing if commercial margins much higher" },
  { priority: "9 INFO", question: "Any prior gov contract experience?", ifYes: "Past performance references accelerate everything", ifNo: "Start from zero — typical for new entrants" },
  { priority: "10 INFO", question: "Goal: supplemental revenue or primary channel?", ifYes: "Aggressive staffing and investment trajectory", ifNo: "Conservative side channel approach" },
];

// ---------------------------------------------------------------------------
// Resolve data sources
// ---------------------------------------------------------------------------
const fpdsNaics = (marketData && marketData.fpds && marketData.fpds.by_naics) || FALLBACK_NAICS;
const fpdsTotals = (marketData && marketData.fpds && marketData.fpds.totals) || FALLBACK_TOTALS;
const fpdsPsc = (marketData && marketData.fpds && marketData.fpds.by_psc) || FALLBACK_PSC;
const tamData = (marketData && marketData.tam) || {};
const productOpp = (marketData && marketData.product_opportunity) || FALLBACK_PRODUCTS;
const dataFY = (marketData && marketData.fiscal_year) ? `FY${marketData.fiscal_year}` : "FY2025";
const fin = FALLBACK_FINANCIALS;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function fmtDollars(n) {
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`;
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`;
  return `$${n.toLocaleString()}`;
}

function fmtDollarsK(n) {
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`;
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`;
  if (n < 0 && Math.abs(n) >= 1e3) return `-$${(Math.abs(n) / 1e3).toFixed(0)}K`;
  if (n < 0) return `-$${Math.abs(n).toLocaleString()}`;
  return `$${n.toLocaleString()}`;
}

// ---------------------------------------------------------------------------
// Build presentation
// ---------------------------------------------------------------------------
const pptx = new pptxgen();
pptx.layout = "LAYOUT_16x9";
pptx.author = "Still Mind Creative";
pptx.company = "Still Mind Creative";
pptx.subject = "Newport Wholesalers Government Contracting Proposal";
pptx.title = "Unlocking Government Revenue for Newport Wholesalers";

// --- Color Palette ---
const C = {
  primary: "065A82",
  secondary: "1C7293",
  accent: "21295C",
  white: "FFFFFF",
  textDark: "1E293B",
  textLight: "FFFFFF",
  lightGray: "F3F4F6",
  medGray: "9CA3AF",
  green: "10B981",
  red: "EF4444",
  yellow: "F59E0B",
  tealLight: "E0F2FE",
};

const FONT_HEADER = "Georgia";
const FONT_BODY = "Calibri";

function addHeadline(slide, text) {
  slide.addText(text, {
    x: 0.6, y: 0.25, w: 8.8, h: 0.9,
    fontSize: 36, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });
}

function addSource(slide, text) {
  slide.addText(text, {
    x: 0.6, y: 7.0, w: 8.8, h: 0.3,
    fontSize: 9, fontFace: FONT_BODY, color: C.medGray, italic: true,
  });
}

function addStatCard(slide, x, y, w, h, value, label, bgColor) {
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.1,
    fill: { color: bgColor || C.tealLight },
  });
  slide.addText(value, {
    x, y: y + 0.2, w, h: h * 0.45,
    fontSize: 40, fontFace: FONT_HEADER, color: C.primary, bold: true, align: "center",
  });
  slide.addText(label, {
    x: x + 0.15, y: y + h * 0.5, w: w - 0.3, h: h * 0.4,
    fontSize: 12, fontFace: FONT_BODY, color: C.textDark, align: "center",
    lineSpacingMultiple: 1.2,
  });
}

// ============================================================================
// SLIDE 1: Title Slide
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.primary };

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: -0.5, y: 5.5, w: 4, h: 4, rotate: 45,
    fill: { color: C.secondary, transparency: 70 },
  });
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 8, y: -1, w: 3, h: 3, rotate: 30,
    fill: { color: C.accent, transparency: 60 },
  });

  slide.addText("Unlocking Government Revenue\nfor Newport Wholesalers", {
    x: 0.8, y: 1.8, w: 8.4, h: 2.0,
    fontSize: 36, fontFace: FONT_HEADER, color: C.white, bold: true,
    lineSpacingMultiple: 1.2,
  });
  slide.addText("30 Years of Wholesale Distribution.\nA New Channel for Predictable Revenue.", {
    x: 0.8, y: 3.8, w: 8.4, h: 1.0,
    fontSize: 16, fontFace: FONT_BODY, color: C.white, transparency: 15,
    lineSpacingMultiple: 1.3,
  });
  slide.addText("Prepared by Still Mind Creative  |  February 2026", {
    x: 0.8, y: 6.6, w: 8.4, h: 0.4,
    fontSize: 11, fontFace: FONT_BODY, color: C.white, transparency: 30,
  });
}

// ============================================================================
// SLIDE 2: Newport's Competitive Advantage (leads with moat)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Why Newport Wins");

  const blocks = [
    {
      title: "30 Years of Continuous Operations",
      body: "Three decades of uninterrupted wholesale distribution in Florida. Real warehouse, real fleet, real W-2 workforce. The kind of audit trail agencies need — and can't be manufactured.",
    },
    {
      title: "Post-DOGE Competitive Moat",
      body: "Federal agencies are under pressure to verify vendor legitimacy after fraud crackdowns. Newport's 30-year history, clean audit trail, and transparent operations are exactly what procurement officers want to see.",
    },
    {
      title: "Infrastructure Already in Place",
      body: "Trucks, routes, cold chain, warehouse — all operating. Government delivery is incremental volume on existing routes. Competitors #5-10 in FL are doing $1-5M with less infrastructure.",
    },
    {
      title: "No Past Performance Required (Year 1)",
      body: "83% of FL food contracts are micro-purchases under $15K — no past performance required. 93% of DoD grocery contracts are sole-source. Commercial experience qualifies for entry.",
    },
  ];

  blocks.forEach((b, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.6;
    const y = 1.5 + row * 2.7;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: 4.2, h: 2.3, rectRadius: 0.1,
      fill: { color: i === 1 ? "FFF8E1" : C.tealLight },
    });
    slide.addText(b.title, {
      x: x + 0.25, y: y + 0.2, w: 3.7, h: 0.5,
      fontSize: 14, fontFace: FONT_HEADER, color: C.accent, bold: true,
    });
    slide.addText(b.body, {
      x: x + 0.25, y: y + 0.75, w: 3.7, h: 1.3,
      fontSize: 11, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
  });
}

// ============================================================================
// SLIDE 3: The Opportunity (stat cards)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "The Opportunity: A $7.2B Federal Food Market");

  const stats = [
    { value: "$7.2B", label: "Annual Federal\nFood Spending (FY2024)" },
    { value: "$85M", label: "FL Food Contracts\nUnder $350K/Year" },
    { value: "93%", label: "Sole-Source Rate\nfor Grocery at DoD" },
  ];

  stats.forEach((s, i) => {
    addStatCard(slide, 0.5 + i * 3.2, 1.6, 2.8, 3.0, s.value, s.label);
  });

  slide.addText("Government food procurement is massive, fragmented, and undercontested.\n117 FL food contracts totaling $6.4M confirmed — most with ZERO competing bids.", {
    x: 0.6, y: 5.0, w: 8.8, h: 0.8,
    fontSize: 13, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });

  addSource(slide, `Source: FPDS ${dataFY}, USASpending API — live data, Feb 2026`);
}

// ============================================================================
// SLIDE 4: Market Waterfall (National → FL → Serviceable)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "From National Market to Newport's Opportunity");

  // Waterfall: 3 stages narrowing down
  const stages = [
    { label: "National TAM", value: "$7.17B", desc: "Total federal food\nprocurement (all PSCs)", w: 6.0, color: C.primary },
    { label: "Florida SAM", value: "$85M", desc: "FL contracts under\n$350K/year", w: 4.0, color: C.secondary },
    { label: "Serviceable", value: "$6.4M", desc: "117 visible contracts\n(>$10K, FPDS-tracked)", w: 2.2, color: C.accent },
  ];

  const baseY = 1.6;
  const barH = 1.2;
  const maxW = 8.0;
  const leftX = 1.0;

  stages.forEach((s, i) => {
    const y = baseY + i * 2.0;
    const barW = s.w;
    const x = leftX + (maxW - barW) / 2;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: barW, h: barH, rectRadius: 0.08,
      fill: { color: s.color },
    });
    slide.addText(s.value, {
      x, y, w: barW, h: barH * 0.55,
      fontSize: 32, fontFace: FONT_HEADER, color: C.white, bold: true, align: "center", valign: "bottom",
    });
    slide.addText(s.label, {
      x, y: y + barH * 0.5, w: barW, h: barH * 0.45,
      fontSize: 13, fontFace: FONT_BODY, color: C.white, align: "center", valign: "top",
    });

    // Description to the right
    slide.addText(s.desc, {
      x: leftX + maxW + 0.3, y: y + 0.1, w: 2.0, h: barH - 0.2,
      fontSize: 10, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.2,
    });

    // Arrow between stages
    if (i < stages.length - 1) {
      slide.addText("\u25BC", {
        x: leftX, y: y + barH + 0.1, w: maxW, h: 0.5,
        fontSize: 18, color: C.medGray, align: "center",
      });
    }
  });

  slide.addText("Micro-purchases (<$15K) account for 83% of awards but are invisible in FPDS.\nTrue serviceable market is estimated at $19-33M with paid monitoring tools.", {
    x: 0.6, y: 7.0, w: 8.8, h: 0.5,
    fontSize: 10, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 5: The Confectionery Gap
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Newport's Edge: The Confectionery Gap");

  // Left: the story
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.5, w: 4.5, h: 5.0, rectRadius: 0.1,
    fill: { color: "FFF8E1" },
  });

  slide.addText("PSC 8925: Confectionery & Nuts", {
    x: 0.75, y: 1.7, w: 4.0, h: 0.5,
    fontSize: 16, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });

  const confPoints = [
    "$55M national spending, $412K in FL alone",
    "Only 45 awards nationally — tiny, fragmented market",
    "58% sole-source — incumbents rarely challenged",
    "Newport's Segment E candy expertise = direct competitive advantage",
    "Existing supplier relationships and wholesale pricing",
    "Few competitors even know this category exists in gov procurement",
  ];

  confPoints.forEach((p, i) => {
    slide.addText(`\u2022  ${p}`, {
      x: 0.75, y: 2.4 + i * 0.55, w: 4.0, h: 0.5,
      fontSize: 11, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.2,
    });
  });

  // Right: stat cards
  addStatCard(slide, 5.5, 1.5, 4.0, 1.8, "58%", "Sole-Source Rate\nfor Confectionery", C.tealLight);
  addStatCard(slide, 5.5, 3.7, 4.0, 1.4, "45", "Total National Awards\n(Lowest of All Food PSCs)", C.tealLight);
  addStatCard(slide, 5.5, 5.5, 4.0, 1.0, "TIER 1", "Priority Category for Newport", "E8F5E9");

  addSource(slide, `Source: FPDS ${dataFY}, PSC 8925 — Confectionery & Nuts`);
}

// ============================================================================
// SLIDE 6: Who's Buying (card layout)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Who's Buying: Target Agencies");

  const buyers = [
    {
      name: "DOJ / Bureau of Prisons",
      stat: "$3.7M / 71 contracts",
      desc: "#1 FL food buyer. Rainmaker doing $5M — direct competitive target. Prison food supply is steady, recurring.",
      color: C.primary,
    },
    {
      name: "Military / DoD",
      stat: "$2.3M / 43 contracts",
      desc: "93% sole-source grocery. MacDill AFB, Homestead ARB, NAS Jax, Patrick SFB. DeCA commissaries.",
      color: C.secondary,
    },
    {
      name: "FEMA / Emergency",
      stat: "Disaster-driven",
      desc: "FL is #1 state for disaster declarations. Pistol Point got $22.7M for Hurricane Helene food delivery. Disaster registry entry.",
      color: C.accent,
    },
    {
      name: "School Districts (SLED)",
      stat: "$500M-$1B FL",
      desc: "State/local, not in federal data. Miami-Dade, Broward, Palm Beach — 67 FL districts. Separate procurement portals.",
      color: "2E7D32",
    },
  ];

  buyers.forEach((b, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.6;
    const y = 1.5 + row * 2.8;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: 4.2, h: 2.5, rectRadius: 0.1,
      fill: { color: C.lightGray },
    });

    // Colored accent bar at top
    slide.addShape(pptx.shapes.RECTANGLE, {
      x, y, w: 4.2, h: 0.08,
      fill: { color: b.color },
    });

    slide.addText(b.name, {
      x: x + 0.25, y: y + 0.2, w: 3.7, h: 0.4,
      fontSize: 14, fontFace: FONT_HEADER, color: C.accent, bold: true,
    });
    slide.addText(b.stat, {
      x: x + 0.25, y: y + 0.6, w: 3.7, h: 0.35,
      fontSize: 13, fontFace: FONT_BODY, color: C.primary, bold: true,
    });
    slide.addText(b.desc, {
      x: x + 0.25, y: y + 1.0, w: 3.7, h: 1.3,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
  });

  addSource(slide, `Source: FPDS ${dataFY}, USASpending API, FL state procurement data`);
}

// ============================================================================
// SLIDE 7: The Competition
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "The Competition: Where Newport Fits");

  const compRows = [
    ["Rank", "Company", "FL Gov Awards", "Notes"],
  ];

  FALLBACK_COMPETITORS.slice(0, 8).forEach(c => {
    compRows.push([
      `#${c.rank}`,
      c.company,
      fmtDollars(c.amount),
      c.notes,
    ]);
  });

  compRows[0] = compRows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 10, align: "center" },
  }));
  for (let i = 1; i < compRows.length; i++) {
    const isTarget = i >= 5; // Ranks 5-8 = Newport's target tier
    const bg = isTarget ? "E8F5E9" : (i % 2 === 0 ? C.lightGray : C.white);
    compRows[i] = compRows[i].map((t, j) => ({
      text: t, options: {
        fill: { color: bg }, fontSize: 10,
        align: j === 0 || j === 2 ? "center" : "left",
        bold: isTarget && j === 1,
        color: isTarget ? "2E7D32" : C.textDark,
      },
    }));
  }

  slide.addTable(compRows, {
    x: 0.4, y: 1.5, w: 9.2,
    colW: [0.6, 3.0, 1.5, 4.1],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: 0.42,
  });

  // Newport positioning callout
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.4, y: 5.5, w: 9.2, h: 1.2, rectRadius: 0.1,
    fill: { color: C.tealLight },
    line: { color: C.secondary, width: 1.5 },
  });
  slide.addText("Newport's Entry Point: $1-5M Tier", {
    x: 0.6, y: 5.6, w: 8.8, h: 0.4,
    fontSize: 14, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });
  slide.addText("Competitors #5-10 are small FL companies with less infrastructure than Newport. The top two (Oakes $26M, US Foods $24M) prove the model works at scale. Newport enters at #5-10 tier with superior distribution infrastructure.", {
    x: 0.6, y: 6.0, w: 8.8, h: 0.6,
    fontSize: 11, fontFace: FONT_BODY, color: C.textDark,
    lineSpacingMultiple: 1.3,
  });

  addSource(slide, `Source: USASpending API, FY2024 FL food contracts`);
}

// ============================================================================
// SLIDE 8: How It Works — Sourcing
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "How It Works: Finding Opportunities");

  slide.addText("1 of 3", {
    x: 8.5, y: 0.35, w: 1.2, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.medGray, align: "right",
  });

  const channels = [
    {
      title: "Federal: SAM.gov",
      desc: "Automated daily monitoring of all food/grocery solicitations. 117 FL contracts identified. Our system scores each opportunity and sends daily digests.",
      cost: "Free (built)",
    },
    {
      title: "State: MyFloridaMarketPlace",
      desc: "FL's $600M-$1.2B state procurement portal. School districts, corrections, state agencies. Separate from federal pipeline — massive opportunity.",
      cost: "Free registration",
    },
    {
      title: "Micro-Purchases: GovSpend",
      desc: "83% of food awards are micro-purchases (<$15K) invisible on SAM.gov. GovSpend reveals $8-15M/yr in FL transactions you can't see otherwise.",
      cost: "$6.5K/yr (optional)",
    },
    {
      title: "Set-Asides",
      desc: "If eligible for SDB, HUBZone, or 8(a), win rates jump to 28%+ with 25% margins. Set-aside contracts are less competitive by design.",
      cost: "Free if eligible",
    },
  ];

  channels.forEach((ch, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.6;
    const y = 1.5 + row * 2.8;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: 4.2, h: 2.4, rectRadius: 0.1,
      fill: { color: C.lightGray },
    });
    slide.addText(ch.title, {
      x: x + 0.25, y: y + 0.15, w: 3.7, h: 0.45,
      fontSize: 14, fontFace: FONT_HEADER, color: C.primary, bold: true,
    });
    slide.addText(ch.desc, {
      x: x + 0.25, y: y + 0.65, w: 3.7, h: 1.2,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
    slide.addText(ch.cost, {
      x: x + 0.25, y: y + 1.9, w: 3.7, h: 0.35,
      fontSize: 11, fontFace: FONT_BODY, color: C.green, bold: true,
    });
  });
}

// ============================================================================
// SLIDE 9: How It Works — Evaluation
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "How It Works: Evaluating & Bidding");

  slide.addText("2 of 3", {
    x: 8.5, y: 0.35, w: 1.2, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.medGray, align: "right",
  });

  // Left: Bid scoring
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.5, w: 4.3, h: 5.0, rectRadius: 0.1,
    fill: { color: C.tealLight },
  });
  slide.addText("Bid/No-Bid Scoring", {
    x: 0.75, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 16, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });
  slide.addText("Every opportunity gets a 0-100 score across 9 weighted factors:", {
    x: 0.75, y: 2.2, w: 3.8, h: 0.4,
    fontSize: 11, fontFace: FONT_BODY, color: C.textDark,
  });

  const factors = [
    "Contract value & margin potential",
    "Competition density (# bidders)",
    "Geographic match (FL delivery)",
    "Product category alignment",
    "Past performance requirements",
    "Set-aside eligibility",
    "Timeline feasibility",
    "Relationship potential (recurring)",
    "Strategic value (reference-building)",
  ];

  factors.forEach((f, i) => {
    slide.addText(`${i + 1}.  ${f}`, {
      x: 0.75, y: 2.7 + i * 0.38, w: 3.8, h: 0.35,
      fontSize: 10, fontFace: FONT_BODY, color: C.textDark,
    });
  });

  // Right: Proposal prep
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 5.2, y: 1.5, w: 4.3, h: 5.0, rectRadius: 0.1,
    fill: { color: C.lightGray },
  });
  slide.addText("Proposal Preparation", {
    x: 5.45, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 16, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });

  const prepSteps = [
    { step: "Capability Statement", desc: "One-page overview of Newport's qualifications, NAICS codes, past performance, and differentiators." },
    { step: "Technical Response", desc: "How Newport will fulfill the specific contract requirements — delivery schedule, cold chain, quality control." },
    { step: "Pricing", desc: "Competitive pricing leveraging Newport's wholesale cost advantage. LPTA evaluation = lowest price wins." },
    { step: "Compliance Docs", desc: "SAM.gov registration, insurance certificates, food safety certifications as required." },
  ];

  prepSteps.forEach((p, i) => {
    const y = 2.3 + i * 1.1;
    slide.addText(p.step, {
      x: 5.45, y, w: 3.8, h: 0.3,
      fontSize: 12, fontFace: FONT_BODY, color: C.primary, bold: true,
    });
    slide.addText(p.desc, {
      x: 5.45, y: y + 0.3, w: 3.8, h: 0.7,
      fontSize: 10, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.2,
    });
  });
}

// ============================================================================
// SLIDE 10: How It Works — Pipeline
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "How It Works: Managing the Pipeline");

  slide.addText("3 of 3", {
    x: 8.5, y: 0.35, w: 1.2, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.medGray, align: "right",
  });

  // Pipeline stages
  const stages = [
    { name: "Identified", desc: "SAM.gov match found", color: C.medGray },
    { name: "Scored", desc: "Bid/no-bid evaluated", color: C.secondary },
    { name: "Pursuing", desc: "Proposal in progress", color: C.primary },
    { name: "Submitted", desc: "Bid delivered", color: C.accent },
    { name: "Awarded", desc: "Contract won", color: C.green },
  ];

  stages.forEach((s, i) => {
    const x = 0.4 + i * 1.9;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y: 1.6, w: 1.7, h: 1.0, rectRadius: 0.08,
      fill: { color: s.color },
    });
    slide.addText(s.name, {
      x, y: 1.6, w: 1.7, h: 0.55,
      fontSize: 12, fontFace: FONT_HEADER, color: C.white, bold: true, align: "center", valign: "bottom",
    });
    slide.addText(s.desc, {
      x, y: 2.2, w: 1.7, h: 0.35,
      fontSize: 9, fontFace: FONT_BODY, color: C.white, align: "center",
    });
    if (i < stages.length - 1) {
      slide.addText("\u25B6", {
        x: x + 1.65, y: 1.8, w: 0.3, h: 0.6,
        fontSize: 14, color: C.medGray, align: "center", valign: "middle",
      });
    }
  });

  // Three management components
  const components = [
    {
      title: "Daily Opportunity Digest",
      desc: "New matches from SAM.gov scored and delivered to your inbox every morning. No manual checking required.",
    },
    {
      title: "Decision-Maker Outreach",
      desc: "For high-value opportunities, we identify contracting officers and program managers. Build relationships before RFPs drop.",
    },
    {
      title: "Pipeline Dashboard",
      desc: "Full lifecycle tracking: deadlines, stages, win rates, projected revenue. Monthly reporting on pipeline health and bid performance.",
    },
  ];

  components.forEach((c, i) => {
    const x = 0.4 + i * 3.15;
    const y = 3.3;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: 2.9, h: 3.0, rectRadius: 0.1,
      fill: { color: C.lightGray },
    });
    slide.addText(c.title, {
      x: x + 0.2, y: y + 0.2, w: 2.5, h: 0.5,
      fontSize: 13, fontFace: FONT_HEADER, color: C.primary, bold: true,
    });
    slide.addText(c.desc, {
      x: x + 0.2, y: y + 0.8, w: 2.5, h: 2.0,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
  });
}

// ============================================================================
// SLIDE 11: Two Routes (Free vs. Optimal)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Two Routes: Start Free or Go Full Coverage");

  const rows = [
    ["Component", "Free Route ($0/yr)", "Paid Route ($13K/yr)"],
    ["Federal Monitoring", "SAM.gov API (built) — 117 FL contracts visible", "+ CLEATUS AI scoring ($3K/yr)"],
    ["State/Local (FL $600M-$1.2B)", "Manual portal checking", "HigherGov — 40K+ agencies ($3.5K/yr)"],
    ["Micro-Purchases (83% invisible)", "Cannot see $8-15M/yr FL", "GovSpend — 1,500+ FL transactions ($6.5K/yr)"],
    ["Competitive Intel", "USASpending + FPDS (built)", "Same (already strong)"],
    ["Pipeline Tracking", "Google Sheets (built)", "Same"],
    ["Market Coverage", "~40-50% ($6.4M visible)", "~90%+ ($19-33M visible)"],
    ["Projected Y5 Owner Earnings", fmtDollarsK(fin.owner_earnings[4]), fmtDollarsK(fin.owner_earnings[4]) + "+"],
  ];

  rows[0] = rows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 11, align: "center" },
  }));
  for (let i = 1; i < rows.length; i++) {
    const isHighlight = i >= 6;
    const bg = isHighlight ? C.tealLight : (i % 2 === 0 ? C.lightGray : C.white);
    rows[i] = rows[i].map((t, j) => ({
      text: t, options: {
        fill: { color: bg }, fontSize: 10.5,
        bold: j === 0 || isHighlight,
        color: isHighlight ? C.primary : C.textDark,
      },
    }));
  }

  slide.addTable(rows, {
    x: 0.4, y: 1.5, w: 9.2,
    colW: [2.2, 3.2, 3.8],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: [0.4, 0.45, 0.45, 0.45, 0.4, 0.4, 0.45, 0.45],
  });

  slide.addText("Both routes use the same intelligence system. The Paid Route adds visibility into the 83% of opportunities that are invisible to free tools.", {
    x: 0.6, y: 5.8, w: 8.8, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 12: The Strategy (Phased: micro → simplified → renewals)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "The Strategy: Build Credibility, Then Compound");

  // Three phases as visual progression
  const phases = [
    {
      title: "Phase 1: Micro-Purchases",
      period: "Year 1",
      desc: "Target contracts under $15K. No past performance required. 83% of FL awards. Build credibility with 8-12 wins. Learn government fulfillment at low risk.",
      metrics: `${fin.bids[0]} bids \u2192 ${fin.wins[0]} wins \u2192 ${fmtDollarsK(fin.revenue[0])} revenue`,
      color: C.primary,
    },
    {
      title: "Phase 2: Simplified Acquisitions",
      period: "Years 2-3",
      desc: "Graduate to $15K-$250K contracts. Past performance from Phase 1 qualifies. Higher margins, longer terms. Renewals at 70% compound the portfolio.",
      metrics: `${fin.active[2]} active contracts \u2192 ${fmtDollarsK(fin.revenue[2])} revenue`,
      color: C.secondary,
    },
    {
      title: "Phase 3: Incumbent Advantage",
      period: "Years 4-5",
      desc: "Preferred vendor status on renewals. Win rates improve to 25%+. Compounding portfolio of 50-70 active contracts generates predictable recurring revenue.",
      metrics: `${fin.active[4]} active contracts \u2192 ${fmtDollarsK(fin.revenue[4])} revenue`,
      color: C.accent,
    },
  ];

  phases.forEach((p, i) => {
    const y = 1.5 + i * 2.0;

    // Phase card
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 0.5, y, w: 9.0, h: 1.7, rectRadius: 0.1,
      fill: { color: C.lightGray },
    });

    // Colored left accent
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.5, y, w: 0.12, h: 1.7,
      fill: { color: p.color },
    });

    slide.addText(p.title, {
      x: 0.9, y: y + 0.1, w: 4.0, h: 0.4,
      fontSize: 15, fontFace: FONT_HEADER, color: C.accent, bold: true,
    });
    slide.addText(p.period, {
      x: 7.5, y: y + 0.1, w: 1.8, h: 0.4,
      fontSize: 12, fontFace: FONT_BODY, color: C.primary, bold: true, align: "right",
    });
    slide.addText(p.desc, {
      x: 0.9, y: y + 0.55, w: 8.3, h: 0.65,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
    slide.addText(p.metrics, {
      x: 0.9, y: y + 1.25, w: 8.3, h: 0.35,
      fontSize: 11, fontFace: FONT_BODY, color: C.primary, bold: true,
    });

    // Arrow between phases
    if (i < phases.length - 1) {
      slide.addText("\u25BC", {
        x: 4.5, y: y + 1.65, w: 1.0, h: 0.35,
        fontSize: 14, color: C.medGray, align: "center",
      });
    }
  });
}

// ============================================================================
// SLIDE 13: 5-Year Financial Summary (Owner Earnings focus)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "5-Year Financial Summary");

  slide.addText("Owner Earnings: What Newport Actually Keeps After All Costs", {
    x: 0.6, y: 1.1, w: 8.8, h: 0.35,
    fontSize: 12, fontFace: FONT_BODY, color: C.secondary, italic: true, align: "center",
  });

  const rows = [
    ["Metric", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
    ["Bids Submitted", ...fin.bids.map(String)],
    ["Contracts Won (New)", ...fin.wins.map(String)],
    ["Active Contracts", ...fin.active.map(String)],
    ["Renewed (70%)", ...fin.renewed.map(String)],
    ["Revenue", ...fin.revenue.map(v => fmtDollarsK(v))],
    ["Gross Profit (22%)", ...fin.gross_profit.map(v => fmtDollarsK(v))],
    ["Bid Prep Costs", ...fin.bid_prep.map(v => `(${fmtDollarsK(v)})`)],
    ["Fulfillment (3%)", ...fin.fulfillment.map(v => `(${fmtDollarsK(v)})`)],
    ["Program Costs", ...fin.program.map(v => `(${fmtDollarsK(v)})`)],
    ["Owner Earnings", ...fin.owner_earnings.map(v => fmtDollarsK(v))],
    ["Cumulative OE", ...fin.cumulative_oe.map(v => fmtDollarsK(v))],
  ];

  rows[0] = rows[0].map((t, j) => ({
    text: t, options: {
      bold: true, color: C.white, fontSize: 9.5, align: "center",
      fill: { color: j === 0 ? C.accent : C.primary },
    },
  }));

  for (let i = 1; i < rows.length; i++) {
    const isOE = i === rows.length - 2; // Owner Earnings row
    const isCumOE = i === rows.length - 1; // Cumulative OE row
    const isCost = i >= 7 && i <= 9; // Cost rows
    const bg = isOE ? "E8F5E9" : isCumOE ? C.tealLight : (i % 2 === 0 ? C.lightGray : C.white);
    rows[i] = rows[i].map((t, j) => ({
      text: t, options: {
        fill: { color: bg }, fontSize: 9,
        bold: j === 0 || isOE || isCumOE,
        color: isOE ? "2E7D32" : isCumOE ? C.primary : isCost ? C.red : C.textDark,
        align: j === 0 ? "left" : "center",
      },
    }));
  }

  slide.addTable(rows, {
    x: 0.3, y: 1.6, w: 9.4,
    colW: [1.7, 1.4, 1.4, 1.4, 1.4, 1.4],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: 0.36,
  });

  slide.addText("Year 1 builds credibility at modest cost. Renewals at 70% create compounding portfolio. By Year 5, Owner Earnings reach $457K/yr with $841K cumulative.", {
    x: 0.6, y: 6.3, w: 8.8, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.primary, bold: true, italic: true, align: "center",
  });

  addSource(slide, "Source: v7 Financial Model — conservative assumptions, 22% gross margin, 70% renewal rate");
}

// ============================================================================
// SLIDE 14: The Compounding Flywheel (Stacked bar chart)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "The Compounding Flywheel");

  slide.addText("Renewed contracts stack on new wins — predictable, recurring revenue", {
    x: 0.6, y: 1.1, w: 8.8, h: 0.35,
    fontSize: 12, fontFace: FONT_BODY, color: C.secondary, italic: true, align: "center",
  });

  // Stacked bar chart using rectangles
  const maxActive = fin.active[4]; // 70
  const chartX = 1.5;
  const chartY = 1.8;
  const chartW = 7.0;
  const chartH = 4.0;
  const barW = 1.0;
  const barGap = 0.4;

  // Y-axis labels
  for (let i = 0; i <= 4; i++) {
    const val = Math.round(maxActive * i / 4);
    const y = chartY + chartH - (chartH * i / 4);
    slide.addText(String(val), {
      x: 0.5, y: y - 0.15, w: 0.8, h: 0.3,
      fontSize: 9, fontFace: FONT_BODY, color: C.medGray, align: "right",
    });
    // Grid line
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: chartX, y, w: chartW, h: 0.01,
      fill: { color: "E5E7EB" },
    });
  }

  // Bars for each year
  fin.years.forEach((yr, i) => {
    const x = chartX + 0.3 + i * (barW + barGap);
    const newContracts = fin.active[i] - fin.renewed[i];
    const renewedContracts = fin.renewed[i];

    // Renewed portion (bottom)
    if (renewedContracts > 0) {
      const renewH = (renewedContracts / maxActive) * chartH;
      const renewY = chartY + chartH - renewH;
      slide.addShape(pptx.shapes.RECTANGLE, {
        x, y: renewY, w: barW, h: renewH,
        fill: { color: C.secondary },
      });
      if (renewH > 0.3) {
        slide.addText(String(renewedContracts), {
          x, y: renewY, w: barW, h: renewH,
          fontSize: 10, fontFace: FONT_BODY, color: C.white, bold: true, align: "center", valign: "middle",
        });
      }
    }

    // New wins portion (top, stacked)
    const totalH = (fin.active[i] / maxActive) * chartH;
    const newH = (newContracts / maxActive) * chartH;
    const newY = chartY + chartH - totalH;
    slide.addShape(pptx.shapes.RECTANGLE, {
      x, y: newY, w: barW, h: newH,
      fill: { color: C.primary },
    });
    if (newH > 0.3) {
      slide.addText(String(newContracts), {
        x, y: newY, w: barW, h: newH,
        fontSize: 10, fontFace: FONT_BODY, color: C.white, bold: true, align: "center", valign: "middle",
      });
    }

    // Year label
    slide.addText(`Y${yr}`, {
      x, y: chartY + chartH + 0.1, w: barW, h: 0.3,
      fontSize: 11, fontFace: FONT_BODY, color: C.textDark, bold: true, align: "center",
    });

    // Total label above bar
    slide.addText(String(fin.active[i]), {
      x, y: newY - 0.35, w: barW, h: 0.3,
      fontSize: 11, fontFace: FONT_BODY, color: C.accent, bold: true, align: "center",
    });
  });

  // Legend
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 1.5, y: 6.4, w: 0.3, h: 0.25,
    fill: { color: C.primary },
  });
  slide.addText("New Wins", {
    x: 1.9, y: 6.38, w: 1.5, h: 0.3,
    fontSize: 10, fontFace: FONT_BODY, color: C.textDark,
  });
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 3.5, y: 6.4, w: 0.3, h: 0.25,
    fill: { color: C.secondary },
  });
  slide.addText("Renewed (70%)", {
    x: 3.9, y: 6.38, w: 2.0, h: 0.3,
    fontSize: 10, fontFace: FONT_BODY, color: C.textDark,
  });

  slide.addText("Y-Axis: Active Contracts", {
    x: 0.1, y: 3.3, w: 1.3, h: 0.3,
    fontSize: 8, fontFace: FONT_BODY, color: C.medGray, rotate: 270,
  });
}

// ============================================================================
// SLIDE 15: Risk & Compliance
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Risk & Compliance: Lower Barrier Than You Think");

  // Left column: Required
  slide.addText("What You Need", {
    x: 0.5, y: 1.4, w: 4.3, h: 0.5,
    fontSize: 16, fontFace: FONT_HEADER, color: C.primary, bold: true,
  });

  const reqRows = [["Item", "Cost", "Timeline"]];
  COMPLIANCE_REQUIRED.forEach(r => {
    reqRows.push([r.item, r.cost, r.timeline]);
  });

  reqRows[0] = reqRows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 10, align: "center" },
  }));
  for (let i = 1; i < reqRows.length; i++) {
    const bg = i % 2 === 0 ? C.lightGray : C.white;
    reqRows[i] = reqRows[i].map((t, j) => ({
      text: t, options: { fill: { color: bg }, fontSize: 10, align: j === 0 ? "left" : "center" },
    }));
  }

  slide.addTable(reqRows, {
    x: 0.5, y: 2.0, w: 4.3,
    colW: [2.0, 1.1, 1.2],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: 0.4,
  });

  slide.addText("Total required investment: $4K-$31.5K\n(depends on existing certifications)", {
    x: 0.5, y: 4.5, w: 4.3, h: 0.6,
    fontSize: 10, fontFace: FONT_BODY, color: C.primary, bold: true, align: "center",
  });

  // Right column: NOT needed
  slide.addText("What You DON'T Need", {
    x: 5.2, y: 1.4, w: 4.3, h: 0.5,
    fontSize: 16, fontFace: FONT_HEADER, color: C.green, bold: true,
  });

  const notRows = [["Item", "Cost Avoided"]];
  COMPLIANCE_NOT_NEEDED.forEach(r => {
    notRows.push([r.item, r.cost]);
  });

  notRows[0] = notRows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.green }, fontSize: 10, align: "center" },
  }));
  for (let i = 1; i < notRows.length; i++) {
    const bg = i % 2 === 0 ? "E8F5E9" : C.white;
    notRows[i] = notRows[i].map((t, j) => ({
      text: t, options: { fill: { color: bg }, fontSize: 10, align: j === 0 ? "left" : "center", color: "2E7D32" },
    }));
  }

  slide.addTable(notRows, {
    x: 5.2, y: 2.0, w: 4.3,
    colW: [2.8, 1.5],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: 0.4,
  });

  slide.addText("$120-360K in compliance costs avoided.\nFood supply contracts are simpler than most gov work.", {
    x: 5.2, y: 4.5, w: 4.3, h: 0.6,
    fontSize: 10, fontFace: FONT_BODY, color: "2E7D32", bold: true, align: "center",
  });

  // Bottom callout
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 5.4, w: 9.0, h: 1.2, rectRadius: 0.1,
    fill: { color: C.tealLight },
  });
  slide.addText("The Misconception: Government contracting requires expensive certifications and complex compliance.", {
    x: 0.7, y: 5.5, w: 8.6, h: 0.4,
    fontSize: 11, fontFace: FONT_BODY, color: C.textDark, bold: true,
  });
  slide.addText("The Reality: Food supply contracts under $250K need SAM.gov registration (free), standard insurance, and food safety certification. That's it. The expensive compliance requirements (DCAA, CMMC, CAS) apply to IT, defense, and consulting — not food procurement.", {
    x: 0.7, y: 5.9, w: 8.6, h: 0.6,
    fontSize: 10, fontFace: FONT_BODY, color: C.textDark,
    lineSpacingMultiple: 1.3,
  });
}

// ============================================================================
// SLIDE 16: Your Investment
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Your Investment: What Newport Pays vs. What We Handle");

  // Left: Newport's investment
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.5, w: 4.3, h: 4.5, rectRadius: 0.1,
    fill: { color: C.tealLight },
    line: { color: C.primary, width: 1.5 },
  });
  slide.addText("Newport Pays", {
    x: 0.75, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 18, fontFace: FONT_HEADER, color: C.primary, bold: true,
  });

  const newportItems = [
    "SAM.gov registration — $0",
    "State portal registrations — $0",
    "Food safety cert (if needed) — $0-$23.5K",
    "Insurance (if needed) — $1.5-3K/yr",
    "Legal review — $2.5-5K (one-time)",
    "Optional: Paid monitoring tools — $13K/yr",
  ];

  newportItems.forEach((item, i) => {
    slide.addText(`\u2022  ${item}`, {
      x: 0.75, y: 2.4 + i * 0.5, w: 3.8, h: 0.45,
      fontSize: 11, fontFace: FONT_BODY, color: C.textDark,
    });
  });

  // Right: Still Mind handles
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 5.2, y: 1.5, w: 4.3, h: 4.5, rectRadius: 0.1,
    fill: { color: C.lightGray },
    line: { color: C.secondary, width: 1.5 },
  });
  slide.addText("Still Mind Handles", {
    x: 5.45, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 18, fontFace: FONT_HEADER, color: C.secondary, bold: true,
  });

  const smcItems = [
    "Federal opportunity monitoring system",
    "Bid/no-bid scoring framework",
    "Pipeline tracking & lifecycle management",
    "Daily opportunity digests",
    "Capability statement & proposal templates",
    "Competitive intelligence dashboard",
    "Monthly reporting & strategy",
    "Ongoing system optimization",
  ];

  smcItems.forEach((item, i) => {
    slide.addText(`\u2713  ${item}`, {
      x: 5.45, y: 2.4 + i * 0.45, w: 3.8, h: 0.4,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
    });
  });

  slide.addText("Newport focuses on what it does best — fulfilling orders. We handle the intelligence, targeting, and proposal infrastructure.", {
    x: 0.5, y: 6.3, w: 9.0, h: 0.5,
    fontSize: 12, fontFace: FONT_BODY, color: C.primary, bold: true, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 17: Key Questions
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Key Questions: Critical Decisions That Shape the Model");

  const rows = [
    ["#", "Question", "If Yes", "If No"],
  ];

  KEY_QUESTIONS.forEach(q => {
    const num = q.priority.split(" ")[0];
    rows.push([num, q.question, q.ifYes, q.ifNo]);
  });

  rows[0] = rows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 9, align: "center" },
  }));

  for (let i = 1; i < rows.length; i++) {
    const priority = KEY_QUESTIONS[i - 1].priority;
    let priColor = C.textDark;
    if (priority.includes("HIGHEST")) priColor = C.red;
    else if (priority.includes("HIGH")) priColor = C.yellow;
    else if (priority.includes("MEDIUM")) priColor = C.secondary;

    const bg = i % 2 === 0 ? C.lightGray : C.white;
    rows[i] = rows[i].map((t, j) => ({
      text: t, options: {
        fill: { color: bg }, fontSize: 8.5,
        align: j === 0 ? "center" : "left",
        bold: j === 0,
        color: j === 0 ? priColor : j === 2 ? "2E7D32" : j === 3 ? C.red : C.textDark,
      },
    }));
  }

  slide.addTable(rows, {
    x: 0.2, y: 1.3, w: 9.6,
    colW: [0.4, 3.0, 3.0, 3.2],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: [0.35, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
  });

  slide.addText("These questions directly change the financial model. Answering them lets us customize projections to Newport's actual situation.", {
    x: 0.6, y: 7.0, w: 8.8, h: 0.4,
    fontSize: 10, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 18: Next Steps
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.primary };

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 7, y: 5, w: 4, h: 4, rotate: 45,
    fill: { color: C.secondary, transparency: 70 },
  });

  slide.addText("Next Steps", {
    x: 0.8, y: 0.8, w: 8.4, h: 0.8,
    fontSize: 36, fontFace: FONT_HEADER, color: C.white, bold: true,
  });

  const steps = [
    { num: "1", title: "Answer Key Questions", desc: "Review the 10 questions on the previous slide. Your answers let us customize the financial model to Newport's actual situation." },
    { num: "2", title: "Register on SAM.gov", desc: "Free registration takes 2-4 weeks. This is the gateway to all federal contracting. We'll guide you through the process." },
    { num: "3", title: "Choose Your Route", desc: "Free Route ($0) or Paid Route ($13K/yr). Both work — the Paid Route gets to traction 12-18 months faster." },
    { num: "4", title: "30-Day Target: First Bids", desc: "Once SAM.gov is active, we begin daily monitoring and submit first micro-purchase bids within 30 days." },
  ];

  steps.forEach((s, i) => {
    const y = 2.0 + i * 1.2;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 0.8, y, w: 7.5, h: 0.9, rectRadius: 0.08,
      fill: { color: C.accent, transparency: 50 },
    });
    slide.addShape(pptx.shapes.OVAL, {
      x: 0.95, y: y + 0.2, w: 0.5, h: 0.5,
      fill: { color: C.white, transparency: 70 },
    });
    slide.addText(s.num, {
      x: 0.95, y: y + 0.18, w: 0.5, h: 0.5,
      fontSize: 16, fontFace: FONT_HEADER, color: C.white, bold: true, align: "center", valign: "middle",
    });
    slide.addText(s.title, {
      x: 1.65, y: y + 0.05, w: 6.5, h: 0.35,
      fontSize: 14, fontFace: FONT_HEADER, color: C.white, bold: true,
    });
    slide.addText(s.desc, {
      x: 1.65, y: y + 0.4, w: 6.5, h: 0.45,
      fontSize: 11, fontFace: FONT_BODY, color: C.white, transparency: 10,
      lineSpacingMultiple: 1.2,
    });
  });

  slide.addText("Zack  |  Still Mind Creative  |  zack@stillmindcreative.com", {
    x: 0.8, y: 6.8, w: 7.5, h: 0.4,
    fontSize: 12, fontFace: FONT_BODY, color: C.white, transparency: 20,
  });
}

// ============================================================================
// Generate file
// ============================================================================
const outPath = path.join(__dirname, "newport-govcon-proposal.pptx");
pptx.writeFile({ fileName: outPath }).then(() => {
  console.log(`\nPresentation saved to ${outPath}`);
  console.log("18 slides generated (v7 narrative).");
}).catch(err => {
  console.error("Failed to generate presentation:", err);
  process.exit(1);
});
