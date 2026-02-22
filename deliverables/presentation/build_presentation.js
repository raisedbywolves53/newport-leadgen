/**
 * Newport GovCon Proposal Deck — Phase 4 (5-Year Plan)
 *
 * Generates a 17-slide 16:9 PowerPoint proposal for Newport Wholesalers.
 * Ocean Gradient palette: #065A82, #1C7293, #21295C
 *
 * Reads deliverables/market_data.json for live FPDS/USASpending data.
 * Falls back to hardcoded values if market_data.json doesn't exist.
 *
 * Run: node deliverables/presentation/build_presentation.js
 * Output: deliverables/presentation/newport-govcon-proposal.pptx
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

// Fallback data — confirmed from live FPDS/USASpending reports + research foundation (Feb 2026)
const FALLBACK_NAICS = [
  // Confirmed via live FPDS competition density report (537 awards, 32 NAICS/agency combos)
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

// Confirmed totals from live FPDS report
const FALLBACK_TOTALS = { transactions: 537, avg_offers: 2.3, sole_source_pct: 56.2 };

// Confirmed PSC spending from research foundation (USASpending FY2024 actuals)
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

// Confirmed from research foundation + live FPDS/USASpending (Feb 2026)
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

// Resolve data sources
const fpdsNaics = (marketData && marketData.fpds && marketData.fpds.by_naics) || FALLBACK_NAICS;
const fpdsTotals = (marketData && marketData.fpds && marketData.fpds.totals) || FALLBACK_TOTALS;
const fpdsPsc = (marketData && marketData.fpds && marketData.fpds.by_psc) || FALLBACK_PSC;
const tamData = (marketData && marketData.tam) || {};
const productOpp = (marketData && marketData.product_opportunity) || FALLBACK_PRODUCTS;
const dataFY = (marketData && marketData.fiscal_year) ? `FY${marketData.fiscal_year}` : "FY2025";

// Helper: format large dollar amounts
function fmtDollars(n) {
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(0)}M`;
  if (n >= 1e3) return `$${(n / 1e3).toFixed(0)}K`;
  return `$${n}`;
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
    x: 0.6, y: 0.3, w: 8.8, h: 0.7,
    fontSize: 24, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.6, y: 0.95, w: 1.2, h: 0.05,
    fill: { color: C.secondary },
  });
}

function addSource(slide, text) {
  slide.addText(text, {
    x: 0.6, y: 7.0, w: 8.8, h: 0.3,
    fontSize: 9, fontFace: FONT_BODY, color: C.medGray, italic: true,
  });
}

// ============================================================================
// SLIDE 1: Title Slide
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.primary };

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
    fontSize: 34, fontFace: FONT_HEADER, color: C.white, bold: true,
    lineSpacingMultiple: 1.2,
  });
  slide.addText("A Turnkey System for Finding, Bidding, and Winning\nGovernment Food Supply Contracts", {
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
// SLIDE 2: The Opportunity
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Newport Is Sitting on a $7.2B Federal Food Market");

  const stats = [
    { value: "$7.2B", label: "Annual Federal\nFood Spending (FY2024)" },
    { value: "$85M", label: "FL Food Contracts\nUnder $350K/Year" },
    { value: "93%", label: "Sole-Source Rate\nfor Grocery at DoD" },
  ];

  stats.forEach((s, i) => {
    const x = 0.5 + i * 3.2;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y: 1.6, w: 2.8, h: 3.2, rectRadius: 0.1,
      fill: { color: C.tealLight },
    });
    slide.addText(s.value, {
      x, y: 1.9, w: 2.8, h: 1.2,
      fontSize: 44, fontFace: FONT_HEADER, color: C.primary, bold: true, align: "center",
    });
    slide.addText(s.label, {
      x, y: 3.2, w: 2.8, h: 1.0,
      fontSize: 13, fontFace: FONT_BODY, color: C.textDark, align: "center",
      lineSpacingMultiple: 1.2,
    });
  });

  slide.addText("Government food procurement is massive, fragmented, and undercontested.\n117 FL food contracts totaling $6.4M confirmed — most with ZERO competing bids.", {
    x: 0.6, y: 5.3, w: 8.8, h: 0.8,
    fontSize: 13, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 3: The Headline Insight (DYNAMIC)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.accent };

  const solePct = fpdsTotals.sole_source_pct.toFixed(1);
  const txnCount = fpdsTotals.transactions.toLocaleString();

  slide.addText(`${solePct}%`, {
    x: 0, y: 1.5, w: 10, h: 2.0,
    fontSize: 96, fontFace: FONT_HEADER, color: C.white, bold: true, align: "center",
  });
  slide.addText("of Federal Food Contracts Are Sole-Source", {
    x: 1, y: 3.5, w: 8, h: 0.7,
    fontSize: 22, fontFace: FONT_BODY, color: C.white, align: "center",
  });
  slide.addText(`Confirmed: FPDS analysis across ${txnCount} food contracting transactions (live data, Feb 2026).\n15 of 32 NAICS/agency combinations show LOW competition. The barrier isn't competition \u2014 it's visibility.`, {
    x: 1.5, y: 4.5, w: 7, h: 1.0,
    fontSize: 13, fontFace: FONT_BODY, color: C.white, transparency: 20, align: "center",
    lineSpacingMultiple: 1.3,
  });
  addSource(slide, `Source: Federal Procurement Data System (FPDS), ${dataFY}`);
}

// ============================================================================
// SLIDE 4: Why Newport Is Positioned to Win
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Newport's Competitive Advantages");

  const blocks = [
    {
      title: "30-Year Track Record",
      icon: "\u2605",
      body: "Three decades of wholesale distribution. Proven reliability, established supplier relationships, operational infrastructure.",
    },
    {
      title: "South Florida Warehouse",
      icon: "\u2302",
      body: "Strategic location for FEMA disaster response staging. FL is #1 for federal emergency declarations. Pistol Point got $22.7M for Hurricane Helene food delivery.",
    },
    {
      title: "Existing Distribution Network",
      icon: "\u2708",
      body: "Trucks, routes, cold chain already in place. FL competitors #5-10 doing $1-5M are smaller companies. Government delivery is incremental volume on existing routes.",
    },
    {
      title: "No Past Performance Required (Year 1)",
      icon: "\u2713",
      body: "83% of FL food contracts are micro-purchases under $15K — no past performance required. 93% of DoD grocery contracts are sole-source. Commercial experience qualifies.",
    },
  ];

  blocks.forEach((b, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.6;
    const y = 1.5 + row * 2.5;

    slide.addShape(pptx.shapes.OVAL, {
      x, y, w: 0.55, h: 0.55,
      fill: { color: C.secondary },
    });
    slide.addText(b.icon, {
      x, y: y - 0.02, w: 0.55, h: 0.55,
      fontSize: 18, color: C.white, align: "center", valign: "middle",
    });
    slide.addText(b.title, {
      x: x + 0.7, y, w: 3.6, h: 0.45,
      fontSize: 15, fontFace: FONT_HEADER, color: C.accent, bold: true,
    });
    slide.addText(b.body, {
      x: x + 0.7, y: y + 0.5, w: 3.6, h: 1.3,
      fontSize: 11, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
  });
}

// ============================================================================
// SLIDE 5: The Process
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "From Registration to Revenue: The Path Forward");

  const steps = [
    { num: "1", title: "Register", desc: "SAM.gov + state/local\nportals (2-4 wks, $0)" },
    { num: "2", title: "Find", desc: "Monitor opportunities\ndaily via data feeds" },
    { num: "3", title: "Score", desc: "Evaluate with bid/\nno-bid framework" },
    { num: "4", title: "Bid", desc: "Capability statement,\ntechnical response, pricing" },
    { num: "5", title: "Win", desc: "Deliver, invoice, build\npast performance" },
    { num: "6", title: "Scale", desc: "Win rate improves\nwith every contract" },
  ];

  steps.forEach((s, i) => {
    const x = 0.25 + i * 1.6;
    slide.addShape(pptx.shapes.OVAL, {
      x: x + 0.3, y: 1.8, w: 0.7, h: 0.7,
      fill: { color: C.primary },
    });
    slide.addText(s.num, {
      x: x + 0.3, y: 1.78, w: 0.7, h: 0.7,
      fontSize: 22, fontFace: FONT_HEADER, color: C.white, bold: true, align: "center", valign: "middle",
    });
    if (i < steps.length - 1) {
      slide.addShape(pptx.shapes.RECTANGLE, {
        x: x + 1.1, y: 2.05, w: 0.5, h: 0.04,
        fill: { color: C.medGray },
      });
    }
    slide.addText(s.title, {
      x, y: 2.7, w: 1.5, h: 0.4,
      fontSize: 13, fontFace: FONT_HEADER, color: C.accent, bold: true, align: "center",
    });
    slide.addText(s.desc, {
      x, y: 3.1, w: 1.5, h: 1.0,
      fontSize: 10, fontFace: FONT_BODY, color: C.textDark, align: "center",
      lineSpacingMultiple: 1.2,
    });
  });

  slide.addText("The first 3-5 wins are the hardest. After that, the flywheel turns.", {
    x: 0.6, y: 5.5, w: 8.8, h: 0.5,
    fontSize: 13, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 6: Target Market Segments
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Where Newport Wins First");

  const rows = [
    ["Buyer Category", "Why It's a Fit", "Confirmed Data"],
    ["DOJ / Bureau of Prisons", "#1 FL food buyer confirmed: $3.7M, 71 contracts (FY2024)", "Rainmaker doing $5M — direct competitive target"],
    ["Military / DoD", "#2 FL food buyer: $2.3M, 43 contracts. 93% sole-source grocery", "MacDill AFB, Homestead ARB, NAS Jax, Patrick SFB"],
    ["FEMA / Emergency", "FL is #1 state for disaster declarations. Disaster registry entry", "Pistol Point got $22.7M for Hurricane Helene food delivery"],
    ["School Districts", "$500M-$1B FL market (SLED, not in federal data)", "Miami-Dade, Broward, Palm Beach — 67 FL districts"],
    ["Corrections (State)", "FL DOC $50-100M. Separate from federal DOJ/BOP", "FL vendor portal + MyFloridaMarketPlace"],
  ];

  const colW = [2.0, 3.8, 3.4];
  const tableOpts = {
    x: 0.4, y: 1.5, w: 9.2,
    fontSize: 11, fontFace: FONT_BODY,
    color: C.textDark,
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    colW,
    autoPage: false,
    rowH: [0.4, 0.55, 0.55, 0.55, 0.55, 0.55],
  };

  rows[0] = rows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 11, align: "center" },
  }));
  for (let i = 1; i < rows.length; i++) {
    const bgColor = i % 2 === 0 ? C.lightGray : C.white;
    rows[i] = rows[i].map((t, j) => ({
      text: t, options: { fill: { color: bgColor }, fontSize: 10.5, bold: j === 0 },
    }));
  }

  slide.addTable(rows, tableOpts);
}

// ============================================================================
// SLIDE 7: FPDS Competition Analysis (DYNAMIC)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Federal Food Contracting: Less Competition Than You Think");

  // Build table from dynamic data (top 6 NAICS by awards)
  const sortedNaics = [...fpdsNaics].sort((a, b) => b.awards - a.awards).slice(0, 6);

  const data = [
    ["NAICS", "Description", "Awards", "Avg Offers", "Sole Source %"],
  ];

  sortedNaics.forEach(n => {
    data.push([
      n.naics,
      n.description,
      String(n.awards),
      n.avg_offers.toFixed(1),
      n.sole_source_pct >= 95 ? `~100%` : `${n.sole_source_pct}%`,
    ]);
  });

  data[0] = data[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 10, align: "center" },
  }));
  for (let i = 1; i < data.length; i++) {
    const bg = i % 2 === 0 ? C.lightGray : C.white;
    data[i] = data[i].map((t, j) => ({
      text: t, options: { fill: { color: bg }, fontSize: 10, align: j >= 2 ? "center" : "left" },
    }));
  }

  slide.addTable(data, {
    x: 0.4, y: 1.5, w: 5.8,
    colW: [0.8, 1.8, 0.8, 0.8, 1.0],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: 0.35,
  });

  // Callout box
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 6.5, y: 1.5, w: 3.1, h: 2.5, rectRadius: 0.1,
    fill: { color: C.tealLight },
    line: { color: C.secondary, width: 1.5 },
  });
  slide.addText(`Average of ${fpdsTotals.avg_offers} offers per contract in Food Service contracting means Newport often competes against ZERO other bidders.`, {
    x: 6.7, y: 1.7, w: 2.7, h: 2.1,
    fontSize: 12, fontFace: FONT_BODY, color: C.accent, bold: true,
    lineSpacingMultiple: 1.3,
  });

  addSource(slide, `Source: FPDS ${dataFY}, 10 food NAICS codes, ${fpdsTotals.transactions.toLocaleString()} transactions`);
}

// ============================================================================
// SLIDE 8: What the Government Buys Most (NEW — Product Spending by PSC)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "What the Federal Government Buys: $7.17B in Food (FY2024)");

  // Sort PSC data by spending, take top 8
  const sortedPsc = [...fpdsPsc]
    .filter(p => p.total_spending > 0)
    .sort((a, b) => b.total_spending - a.total_spending)
    .slice(0, 8);

  const totalPscSpending = sortedPsc.reduce((sum, p) => sum + p.total_spending, 0);

  const rows = [
    ["Product Category", "PSC", "Annual Spending", "Share", "Opportunity"],
  ];

  sortedPsc.forEach(p => {
    const share = totalPscSpending > 0 ? ((p.total_spending / totalPscSpending) * 100).toFixed(0) : "—";
    rows.push([
      p.description,
      p.psc,
      fmtDollars(p.total_spending),
      `${share}%`,
      p.opportunity_tier,
    ]);
  });

  rows[0] = rows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 10, align: "center" },
  }));
  for (let i = 1; i < rows.length; i++) {
    const tier = sortedPsc[i - 1].opportunity_tier;
    let bg = i % 2 === 0 ? C.lightGray : C.white;
    if (tier === "HIGH") bg = "E8F5E9"; // light green highlight
    const tierColor = tier === "HIGH" ? "2E7D32" : tier === "MODERATE" ? C.textDark : tier === "LOW" ? C.red : C.medGray;
    rows[i] = rows[i].map((t, j) => ({
      text: t, options: {
        fill: { color: bg }, fontSize: 10,
        align: j >= 2 ? "center" : "left",
        bold: j === 4,
        color: j === 4 ? tierColor : C.textDark,
      },
    }));
  }

  slide.addTable(rows, {
    x: 0.3, y: 1.4, w: 9.4,
    colW: [2.4, 0.7, 1.6, 0.8, 1.2],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: 0.4,
  });

  slide.addText("GREEN = High opportunity for Newport  |  In 10 of 13 categories, just 5 companies control the majority of spending", {
    x: 0.6, y: 5.5, w: 8.8, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.primary, bold: true, italic: true, align: "center",
  });

  addSource(slide, `Source: FPDS ${dataFY} + USDA spending analysis`);
}

// ============================================================================
// SLIDE 9: Where Newport Wins — Product Priorities (NEW)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Where Newport Wins: Priority Product Categories");

  const priorities = productOpp.priority_products || FALLBACK_PRODUCTS.priority_products;
  const avoids = productOpp.avoid || FALLBACK_PRODUCTS.avoid;

  // 2x2 grid of priority products
  priorities.slice(0, 4).forEach((p, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.4 + col * 4.7;
    const y = 1.4 + row * 2.3;

    // Card background
    const cardColor = p.tier === 1 ? "E8F5E9" : C.tealLight;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: 4.3, h: 2.0, rectRadius: 0.1,
      fill: { color: cardColor },
    });

    // Tier badge
    const tierLabel = p.tier === 1 ? "TIER 1" : "TIER 2";
    const tierColor = p.tier === 1 ? C.green : C.secondary;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: x + 3.2, y: y + 0.1, w: 0.9, h: 0.3, rectRadius: 0.05,
      fill: { color: tierColor },
    });
    slide.addText(tierLabel, {
      x: x + 3.2, y: y + 0.08, w: 0.9, h: 0.3,
      fontSize: 8, fontFace: FONT_BODY, color: C.white, bold: true, align: "center", valign: "middle",
    });

    // Product name + spending
    slide.addText(`${p.name} (PSC ${p.psc})`, {
      x: x + 0.2, y: y + 0.15, w: 2.9, h: 0.35,
      fontSize: 13, fontFace: FONT_HEADER, color: C.accent, bold: true,
    });
    slide.addText(fmtDollars(p.annual_spending) + "/year", {
      x: x + 0.2, y: y + 0.5, w: 2.9, h: 0.3,
      fontSize: 12, fontFace: FONT_BODY, color: C.primary, bold: true,
    });

    // Rationale
    slide.addText(p.rationale, {
      x: x + 0.2, y: y + 0.85, w: 3.9, h: 1.0,
      fontSize: 10, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
  });

  // Avoid callout at bottom
  const avoidText = avoids.map(a => `${a.name}: ${a.rationale}`).join("  |  ");
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.4, y: 6.1, w: 9.2, h: 0.6, rectRadius: 0.05,
    fill: { color: "FFF3E0" },
    line: { color: C.yellow, width: 1 },
  });
  slide.addText(`AVOID:  ${avoidText}`, {
    x: 0.6, y: 6.1, w: 8.8, h: 0.6,
    fontSize: 9, fontFace: FONT_BODY, color: C.textDark, valign: "middle",
    lineSpacingMultiple: 1.2,
  });
}

// ============================================================================
// SLIDE 10: Economies of Scale — Newport's Pricing Advantage (NEW)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Economies of Scale: Newport's Pricing Advantage");

  // Key points — confirmed from FPDS/competition data
  const points = [
    {
      title: "LPTA = Lowest Price Wins",
      body: "Most food supply contracts use Lowest Price Technically Acceptable evaluation. FPDS confirms 93% of DoD grocery contracts are sole-source — whoever shows up at the right price wins.",
    },
    {
      title: "Existing Distribution Network",
      body: "Newport's trucks, routes, and cold chain are already operating. Government delivery is incremental cost. Top FL competitors (Oakes Farms $26M, US Foods $24M) prove the wholesale-to-gov model works.",
    },
    {
      title: "Bulk Purchasing Power",
      body: "FL competitors #5-10 do $1-5M each — small companies without Newport's scale. Newport's existing supplier relationships and purchase volumes provide a structural pricing advantage.",
    },
  ];

  points.forEach((p, i) => {
    const y = 1.4 + i * 1.4;
    slide.addShape(pptx.shapes.OVAL, {
      x: 0.6, y: y + 0.05, w: 0.45, h: 0.45,
      fill: { color: C.primary },
    });
    slide.addText(String(i + 1), {
      x: 0.6, y: y + 0.03, w: 0.45, h: 0.45,
      fontSize: 16, color: C.white, align: "center", valign: "middle", bold: true,
    });
    slide.addText(p.title, {
      x: 1.3, y, w: 8, h: 0.4,
      fontSize: 14, fontFace: FONT_HEADER, color: C.accent, bold: true,
    });
    slide.addText(p.body, {
      x: 1.3, y: y + 0.4, w: 8, h: 0.8,
      fontSize: 11, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
  });

  // Comparison table
  const compRows = [
    ["Product Category", "Typical Gov Vendor Markup", "Newport Wholesale Advantage"],
    ["Fresh Produce", "15-25% over wholesale", "Direct sourcing at wholesale cost"],
    ["Confectionery & Snacks", "20-30% markup", "Existing Segment E supplier pricing"],
    ["Dairy & Eggs", "12-20% markup", "Regional distribution, lower delivery cost"],
    ["General Grocery", "15-25% markup", "Volume purchasing, existing logistics"],
  ];

  compRows[0] = compRows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 10, align: "center" },
  }));
  for (let i = 1; i < compRows.length; i++) {
    const bg = i % 2 === 0 ? C.lightGray : C.white;
    compRows[i] = compRows[i].map((t, j) => ({
      text: t, options: {
        fill: { color: j === 2 ? "E8F5E9" : bg }, fontSize: 10,
        bold: j === 2, color: j === 2 ? "2E7D32" : C.textDark,
      },
    }));
  }

  slide.addTable(compRows, {
    x: 0.4, y: 5.5, w: 9.2,
    colW: [2.2, 3.0, 4.0],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: 0.3,
  });
}

// ============================================================================
// SLIDE 11: The System We've Built (was slide 8)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Your Government Contracting Command Center");

  const components = [
    {
      title: "Federal Opportunity Monitor",
      icon: "\uD83D\uDCE1",
      body: "Automated daily scan of SAM.gov for food/grocery contracts matching Newport's NAICS codes. New opportunities scored and delivered to your inbox every morning.",
    },
    {
      title: "Competitive Intelligence Engine",
      icon: "\uD83D\uDD0D",
      body: "FPDS and USASpending analysis reveals who's winning, how much they're winning, and where the gaps are. Know your competition before you bid.",
    },
    {
      title: "Bid/No-Bid Scoring Framework",
      icon: "\uD83C\uDFAF",
      body: "9-factor weighted evaluation matrix. Every opportunity gets a score (0-100) and a recommendation. No more guessing which contracts to pursue.",
    },
    {
      title: "Pipeline Tracker",
      icon: "\uD83D\uDCCA",
      body: "Full lifecycle management from Identified through Awarded. Track deadlines, stages, and win rates in one place.",
    },
  ];

  components.forEach((c, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.6;
    const y = 1.5 + row * 2.7;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: 4.2, h: 2.3, rectRadius: 0.1,
      fill: { color: C.lightGray },
    });
    slide.addText(c.title, {
      x: x + 0.3, y: y + 0.2, w: 3.6, h: 0.45,
      fontSize: 14, fontFace: FONT_HEADER, color: C.primary, bold: true,
    });
    slide.addText(c.body, {
      x: x + 0.3, y: y + 0.7, w: 3.6, h: 1.3,
      fontSize: 11, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
  });
}

// ============================================================================
// SLIDE 12: Free vs. Optimal System (was slide 9)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Investment Options: Start Free or Go Full Coverage");

  const rows = [
    ["Component", "Free Version ($0/yr)", "Optimal Version ($13K/yr)"],
    ["Federal Monitoring", "SAM.gov API (built) — 117 FL contracts visible", "+ CLEATUS AI scoring ($3K/yr)"],
    ["State/Local (FL $600M-$1.2B)", "Manual portal checking", "HigherGov — 40K+ agencies ($3.5K/yr)"],
    ["Micro-Purchases (83% invisible)", "Cannot see $8-15M/yr FL", "GovSpend — 1,500+ FL transactions ($6.5K/yr)"],
    ["Competitive Intel", "USASpending + FPDS (built)", "Same (already strong)"],
    ["Proposal Writing", "Claude AI + templates", "CLEATUS AI shredder"],
    ["Pipeline Tracking", "Google Sheets (built)", "Same"],
    ["Market Coverage", "~40-50% ($6.4M visible)", "~90%+ ($19-33M visible)"],
    ["Bid Capacity/Year", "20-30 bids", "40-60 bids"],
  ];

  rows[0] = rows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 11, align: "center" },
  }));
  for (let i = 1; i < rows.length; i++) {
    const isHighlight = i >= 7;
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
    rowH: [0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.45, 0.45],
  });
}

// ============================================================================
// SLIDE 13: Financial Projections — 5-Year (was slide 10)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "5-Year Revenue Trajectory: Compounding Government Revenue");

  // TAM context line — confirmed data
  const tamLine = tamData.total_spending
    ? `Federal food TAM: ${fmtDollars(tamData.total_spending)} | FL under $350K: $85M | FL visible (>$10K): $6.4M/117 contracts`
    : "Federal food TAM: $7.17B | FL under $350K: $85M/yr | FL visible (>$10K): $6.4M/117 contracts";

  slide.addText(tamLine, {
    x: 0.4, y: 1.3, w: 9.2, h: 0.3,
    fontSize: 10, fontFace: FONT_BODY, color: C.secondary, italic: true, align: "center",
  });

  // Revenue projections aligned with research foundation scenarios
  const rows = [
    ["Metric", "Year 1", "Year 2", "Year 3", "Year 5"],
    ["Win Rate", "15-25%", "35%", "40%", "50%"],
    ["Bids Submitted", "28-58", "36-60", "45-75", "50-90"],
    ["Contracts Won", "8-20", "12-25", "18-35", "25-50"],
    ["Revenue (Moderate)", "$150K-$350K", "$500K-$1M", "$1M-$1.5M", "$1.5M-$3M"],
    ["Gross Margin (11%)", "$16K-$39K", "$55K-$110K", "$110K-$165K", "$165K-$330K"],
    ["Cumulative Revenue", "$150K-$350K", "$650K-$1.35M", "$1.65M-$2.85M", "$4.8M-$9M"],
  ];

  rows[0] = rows[0].map((t, j) => ({
    text: t, options: {
      bold: true, color: C.white, fontSize: 10.5, align: "center",
      fill: { color: j === 0 ? C.accent : [C.primary, C.primary, C.secondary, C.accent][j - 1] },
    },
  }));

  for (let i = 1; i < rows.length; i++) {
    const isTotal = i >= rows.length - 1;
    const bg = isTotal ? C.tealLight : (i % 2 === 0 ? C.lightGray : C.white);
    rows[i] = rows[i].map((t, j) => ({
      text: t, options: {
        fill: { color: bg }, fontSize: 10,
        bold: j === 0 || isTotal,
        color: isTotal ? C.primary : C.textDark,
        align: j === 0 ? "left" : "center",
      },
    }));
  }

  slide.addTable(rows, {
    x: 0.3, y: 1.8, w: 9.4,
    colW: [2.0, 1.8, 1.8, 1.8, 2.0],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
  });

  slide.addText("Year 1 builds credibility. Years 2-3 compound past performance. Years 4-5 deliver incumbent advantage and preferred vendor status.", {
    x: 0.6, y: 5.7, w: 8.8, h: 0.5,
    fontSize: 12, fontFace: FONT_BODY, color: C.primary, bold: true, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 14: Implementation Timeline (was slide 11)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "90-Day Launch Plan");

  const milestones = [
    { period: "Weeks 1-2", desc: "SAM.gov registration submitted. State/local portal registrations complete.", color: C.primary },
    { period: "Weeks 2-4", desc: "SAM.gov validated. Command center operational. Daily monitoring begins.", color: C.secondary },
    { period: "Weeks 3-6", desc: "First 5-10 opportunities scored. First 2-3 bids submitted.", color: C.primary },
    { period: "Weeks 6-10", desc: "Capability statement refined. Expand to state/local bids.", color: C.secondary },
    { period: "Weeks 10-13", desc: "First award decisions received. Pipeline building. Adjust targeting.", color: C.primary },
  ];

  milestones.forEach((m, i) => {
    const y = 1.6 + i * 1.05;
    slide.addShape(pptx.shapes.OVAL, {
      x: 0.7, y: y + 0.15, w: 0.35, h: 0.35,
      fill: { color: m.color },
    });
    if (i < milestones.length - 1) {
      slide.addShape(pptx.shapes.RECTANGLE, {
        x: 0.855, y: y + 0.5, w: 0.04, h: 0.6,
        fill: { color: C.medGray },
      });
    }
    slide.addText(m.period, {
      x: 1.3, y, w: 1.8, h: 0.55,
      fontSize: 13, fontFace: FONT_HEADER, color: C.accent, bold: true, valign: "middle",
    });
    slide.addText(m.desc, {
      x: 3.1, y, w: 6.2, h: 0.55,
      fontSize: 11.5, fontFace: FONT_BODY, color: C.textDark, valign: "middle",
      lineSpacingMultiple: 1.2,
    });
  });
}

// ============================================================================
// SLIDE 15: What Still Mind Creative Delivers (was slide 12)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Your Government Revenue Partner");

  const deliverables = [
    "Custom-built federal opportunity monitoring system (SAM.gov + FPDS + USASpending)",
    "Bid/No-Bid scoring framework calibrated to Newport's capabilities",
    "Government contracting pipeline tracker with lifecycle management",
    "Daily opportunity digest delivered to your inbox",
    "Capability statement and proposal templates",
    "Competitive intelligence dashboard showing market gaps",
    "Monthly reporting on pipeline activity, bid volume, and win rate",
    "Ongoing system optimization and strategy refinement",
  ];

  deliverables.forEach((d, i) => {
    const y = 1.5 + i * 0.6;
    slide.addShape(pptx.shapes.OVAL, {
      x: 0.7, y: y + 0.05, w: 0.35, h: 0.35,
      fill: { color: C.green },
    });
    slide.addText("\u2713", {
      x: 0.7, y: y + 0.02, w: 0.35, h: 0.35,
      fontSize: 14, color: C.white, align: "center", valign: "middle", bold: true,
    });
    slide.addText(d, {
      x: 1.3, y, w: 8, h: 0.5,
      fontSize: 12.5, fontFace: FONT_BODY, color: C.textDark, valign: "middle",
    });
  });
}

// ============================================================================
// SLIDE 16: Investment & Next Steps (was slide 13)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.primary };

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 7, y: 5, w: 4, h: 4, rotate: 45,
    fill: { color: C.secondary, transparency: 70 },
  });

  slide.addText("Next Steps", {
    x: 0.8, y: 0.8, w: 8.4, h: 0.8,
    fontSize: 30, fontFace: FONT_HEADER, color: C.white, bold: true,
  });

  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.8, y: 1.6, w: 1.2, h: 0.05,
    fill: { color: C.white, transparency: 40 },
  });

  const phases = [
    { label: "Phase 1", desc: "System activation + SAM.gov registration (Weeks 1-4)" },
    { label: "Phase 2", desc: "First bids submitted (Weeks 4-8)" },
    { label: "Phase 3", desc: "Pipeline optimization + scaling (Weeks 8-13)" },
  ];

  phases.forEach((p, i) => {
    const y = 2.2 + i * 0.9;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 0.8, y, w: 7.5, h: 0.65, rectRadius: 0.08,
      fill: { color: C.accent, transparency: 50 },
    });
    slide.addText(`${p.label}:  ${p.desc}`, {
      x: 1.0, y, w: 7.3, h: 0.65,
      fontSize: 14, fontFace: FONT_BODY, color: C.white, valign: "middle",
    });
  });

  slide.addText("Let's schedule a working session to begin SAM.gov registration\nand activate the command center.", {
    x: 0.8, y: 5.0, w: 7.5, h: 0.8,
    fontSize: 14, fontFace: FONT_BODY, color: C.white, italic: true,
    lineSpacingMultiple: 1.3,
  });

  slide.addText("Zack  |  Still Mind Creative  |  zack@stillmindcreative.com", {
    x: 0.8, y: 6.3, w: 7.5, h: 0.4,
    fontSize: 12, fontFace: FONT_BODY, color: C.white, transparency: 20,
  });
}

// ============================================================================
// SLIDE 17: Appendix — FPDS Data Detail (DYNAMIC, was slide 14)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Federal Food Procurement Data \u2014 Full Breakdown");

  // Build from dynamic data
  const data = [
    ["NAICS", "Description", "Awards", "Avg Value", "Avg Offers", "Sole Source %"],
  ];

  // Sort by awards descending for the detail table
  const allNaics = [...fpdsNaics].sort((a, b) => b.awards - a.awards);
  allNaics.forEach(n => {
    data.push([
      n.naics,
      n.description,
      String(n.awards),
      fmtDollars(n.avg_value),
      n.avg_offers.toFixed(1),
      n.sole_source_pct >= 95 ? `~100%` : `${n.sole_source_pct}%`,
    ]);
  });

  // Totals row
  const totals = [
    "TOTAL",
    "All Food NAICS",
    fpdsTotals.transactions.toLocaleString(),
    "\u2014",
    `${fpdsTotals.avg_offers} avg`,
    `${fpdsTotals.sole_source_pct}%`,
  ];

  data[0] = data[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 9.5, align: "center" },
  }));
  for (let i = 1; i < data.length; i++) {
    const bg = i % 2 === 0 ? C.lightGray : C.white;
    data[i] = data[i].map((t, j) => ({
      text: t, options: { fill: { color: bg }, fontSize: 9.5, align: j >= 2 ? "center" : "left" },
    }));
  }
  // Totals row
  data.push(totals.map(t => ({
    text: t, options: { bold: true, fill: { color: C.tealLight }, fontSize: 9.5, color: C.primary, align: "center" },
  })));

  slide.addTable(data, {
    x: 0.3, y: 1.4, w: 9.4,
    colW: [0.8, 2.0, 0.9, 1.2, 1.0, 1.2],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: 0.35,
  });

  addSource(slide, `Source: FPDS ${dataFY} via Federal Procurement Data System API`);
}

// ============================================================================
// Generate file
// ============================================================================
const outPath = path.join(__dirname, "newport-govcon-proposal.pptx");
pptx.writeFile({ fileName: outPath }).then(() => {
  console.log(`Presentation saved to ${outPath}`);
  console.log("17 slides generated.");
}).catch(err => {
  console.error("Failed to generate presentation:", err);
  process.exit(1);
});
