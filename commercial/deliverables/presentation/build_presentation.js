/**
 * Newport Commercial SDR Proposal Deck — 12-Slide Build
 *
 * Generates a 12-slide 16:9 PowerPoint proposal for Newport Wholesalers'
 * commercial SDR (AI-powered outbound) channel.
 *
 * Ocean Gradient palette: #065A82, #1C7293, #21295C
 * (Same design system as GovCon deck)
 *
 * Financial data hardcoded from build_commercial_model.py at default params.
 *
 * Run: cd commercial/deliverables/presentation && node build_presentation.js
 * Output: commercial/deliverables/presentation/newport-commercial-sdr-proposal.pptx
 */

const pptxgen = require("pptxgenjs");
const path = require("path");

// ---------------------------------------------------------------------------
// Financial data — pre-computed from build_commercial_model.py at defaults
// ---------------------------------------------------------------------------
// Default params: 30 emails/day, 3 mailboxes, 22% open, 3.5% reply,
// 35% reply→meeting, 18% meeting→deal, 45-day sales cycle, 2 reps @ 20 meetings/mo
// Weighted avg deal size: $28,000

const SCENARIOS = {
  free: {
    name: "Free",
    toolCostAnnual: 0,
    prospectsWeek: 50,
    prospectsMonth: 217,        // 50 * 4.33
    prospects12mo: 2600,        // 217 * 12
    meetings12mo: 3,            // 217 * 0.035 * 0.35 = 2.66/mo → cap at 40 → ~3/mo, lagged
    deals12mo: 5,               // meetings * 0.18, lagged 2mo → 10mo of deals
    revenue12mo: 140000,        // 5 * 28000
    grossProfit12mo: 30800,     // 140000 * 0.22
    netContribution12mo: 30800, // no tool costs
  },
  moderate: {
    name: "Moderate",
    toolCostAnnual: 1032,
    prospectsWeek: 450,
    prospectsMonth: 1949,       // 450 * 4.33
    prospects12mo: 23400,
    meetings12mo: 24,           // 1949 * 0.035 * 0.35 = 23.9/mo → cap 40 → 24/mo
    deals12mo: 43,              // 24 * 0.18 = 4.3/mo, 10mo lagged
    revenue12mo: 1204000,       // 43 * 28000
    grossProfit12mo: 264880,    // 1204000 * 0.22
    netContribution12mo: 263848, // 264880 - 1032
  },
  aggressive: {
    name: "Aggressive",
    toolCostAnnual: 9072,
    prospectsWeek: 900,
    prospectsMonth: 3897,       // 900 * 4.33
    prospects12mo: 46800,
    meetings12mo: 40,           // 3897 * 0.035 * 0.35 = 47.7/mo → cap at 40
    deals12mo: 72,              // 40 * 0.18 = 7.2/mo, 10mo lagged
    revenue12mo: 2016000,       // 72 * 28000
    grossProfit12mo: 443520,    // 2016000 * 0.22
    netContribution12mo: 434448, // 443520 - 9072
  },
};

// ICP Segments from icp_definitions.json + build_commercial_model.py
const ICP_SEGMENTS = [
  { code: "A", name: "Enterprise Grocery", pipeline: "Direct-to-customer", geo: "US/UK/EU", companies: 2000, avgDeal: 50000, priority: 1 },
  { code: "B", name: "Manufacturers", pipeline: "Partner", geo: "US/UK/EU", companies: 3000, avgDeal: 25000, priority: 2 },
  { code: "C", name: "Gov Buyers", pipeline: "Direct-to-customer", geo: "US only", companies: 500, avgDeal: 15000, priority: 3 },
  { code: "D", name: "Corrections", pipeline: "Direct-to-customer", geo: "US only", companies: 200, avgDeal: 30000, priority: 3 },
  { code: "E", name: "Candy/Confectionery", pipeline: "Partner", geo: "US/LATAM", companies: 1831, avgDeal: 20000, priority: 1 },
];

const TOTAL_COMPANIES = ICP_SEGMENTS.reduce((s, seg) => s + seg.companies, 0);
const TOTAL_TAM = ICP_SEGMENTS.reduce((s, seg) => s + seg.companies * seg.avgDeal, 0);

// Key Questions from build_commercial_model.py Key Questions sheet
const KEY_QUESTIONS = [
  { priority: "1 HIGHEST", question: "What are actual deal sizes by customer type?", ifYes: "Calibrates entire model. Current values are placeholders.", ifNo: "Model uses estimates; directionally right but imprecise" },
  { priority: "2 HIGHEST", question: "What is current gross margin on wholesale deals?", ifYes: "Determines profitability at every scenario level.", ifNo: "22% assumption may over- or under-state returns" },
  { priority: "3 HIGH", question: "How many sales reps will handle inbound meetings?", ifYes: "Capacity constraint. More reps = more throughput.", ifNo: "2 reps cap at 40 meetings/mo; may bottleneck Aggressive" },
  { priority: "4 HIGH", question: "Which segments to prioritize first?", ifYes: "Focus resources on 1-2 segments for faster traction.", ifNo: "Spreading across all 5 dilutes effort and slows results" },
  { priority: "5 HIGH", question: "Willing to invest in Instantly email automation?", ifYes: "Unlocks Moderate scenario (450/wk vs 50/wk).", ifNo: "Free scenario only; manual LinkedIn outreach" },
  { priority: "6 MEDIUM", question: "Current close rate on warm introductions?", ifYes: "Baseline calibration. Cold outreach typically 40-60% lower.", ifNo: "We use 18% default for cold; adjust if warm rate known" },
  { priority: "7 MEDIUM", question: "Interest in LATAM candy import/export?", ifYes: "Expands Seg E scope. USMCA = $0 tariff from Mexico.", ifNo: "Focus US-only Seg E; still 1,831 firms to target" },
  { priority: "8 MEDIUM", question: "Existing CRM or sales tracking system?", ifYes: "Integrate SDR pipeline into existing workflow.", ifNo: "Recommend HubSpot Free CRM or Google Sheets tracker" },
  { priority: "9 INFO", question: "What does a typical sales cycle look like today?", ifYes: "Calibrates 45-day default. Shorter = faster revenue.", ifNo: "We keep 45-day assumption; conservative but standard" },
  { priority: "10 INFO", question: "Any existing outbound prospecting?", ifYes: "Baseline comparison. SDR adds to existing effort.", ifNo: "Greenfield \u2014 all SDR revenue is incremental" },
];

// ---------------------------------------------------------------------------
// Helpers (verbatim from GovCon deck)
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
pptx.subject = "Newport Wholesalers Commercial SDR Proposal";
pptx.title = "Systematic Growth for Newport Wholesalers";

// --- Color Palette (verbatim from GovCon) ---
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

  slide.addText("Systematic Growth\nfor Newport Wholesalers", {
    x: 0.8, y: 1.8, w: 8.4, h: 2.0,
    fontSize: 36, fontFace: FONT_HEADER, color: C.white, bold: true,
    lineSpacingMultiple: 1.2,
  });
  slide.addText("30 Years of Relationships.\nNow: Scale with Intelligence.", {
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
// SLIDE 2: Where Newport Stands
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Where Newport Stands");

  const blocks = [
    {
      title: "30 Years of Wholesale Success",
      body: "Relationships built over 3 decades. Real warehouse, fleet, W-2 workforce. A foundation competitors can\u2019t replicate overnight.",
    },
    {
      title: "Strong Existing Business",
      body: "Established customer base across grocery, foodservice, and confectionery. Revenue grows when salespeople sell.",
    },
    {
      title: "Growth Bottleneck",
      body: "Revenue grows when salespeople make calls. When they stop, it stops. No systematic pipeline. No repeatable prospecting engine.",
    },
    {
      title: "The Opportunity",
      body: "AI-powered prospecting adds repeatable scale without replacing what works. Systematic outbound across 5 growth segments.",
    },
  ];

  blocks.forEach((b, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.6;
    const y = 1.5 + row * 2.7;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: 4.2, h: 2.3, rectRadius: 0.1,
      fill: { color: i === 3 ? "E8F5E9" : C.tealLight },
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
  addHeadline(slide, "The Opportunity");

  const stats = [
    { value: fmtDollars(TOTAL_COMPANIES).replace("$", ""), label: "Total Addressable Companies\nAcross 5 ICP Segments" },
    { value: fmtDollars(TOTAL_TAM), label: "Estimated Segment TAM\n(Companies x Deal Sizes)" },
    { value: "5", label: "Distinct Growth Segments\nFrom Enterprise Grocery\nto Candy Wholesale" },
  ];

  stats.forEach((s, i) => {
    addStatCard(slide, 0.5 + i * 3.2, 1.6, 2.8, 3.0, s.value, s.label);
  });

  slide.addText("AI-powered prospecting identifies, enriches, and engages decision-makers\nacross all 5 segments \u2014 systematically, at scale.", {
    x: 0.6, y: 5.0, w: 8.8, h: 0.8,
    fontSize: 13, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });

  addSource(slide, "Source: Apollo.io coverage estimates, ICP definitions, commercial model \u2014 Feb 2026");
}

// ============================================================================
// SLIDE 4: Five Growth Segments
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Five Growth Segments");

  const rows = [
    ["Segment", "Pipeline", "Geography", "Companies", "Avg Deal", "Priority"],
  ];

  ICP_SEGMENTS.forEach(seg => {
    const priLabel = seg.priority === 1 ? "\u2605 Priority 1" : seg.priority === 2 ? "Priority 2" : "Priority 3";
    rows.push([
      `${seg.code}: ${seg.name}`,
      seg.pipeline,
      seg.geo,
      seg.companies.toLocaleString(),
      fmtDollars(seg.avgDeal),
      priLabel,
    ]);
  });

  // Total row
  rows.push([
    "TOTAL",
    "",
    "",
    TOTAL_COMPANIES.toLocaleString(),
    "$28K avg",
    "",
  ]);

  // Style header row
  rows[0] = rows[0].map(t => ({
    text: t, options: { bold: true, color: C.white, fill: { color: C.primary }, fontSize: 11, align: "center" },
  }));

  // Style data rows
  for (let i = 1; i < rows.length - 1; i++) {
    const seg = ICP_SEGMENTS[i - 1];
    const isPriority1 = seg.priority === 1;
    const bg = isPriority1 ? "E8F5E9" : (i % 2 === 0 ? C.lightGray : C.white);
    rows[i] = rows[i].map((t, j) => ({
      text: t, options: {
        fill: { color: bg }, fontSize: 10.5,
        align: j === 0 ? "left" : "center",
        bold: isPriority1 && (j === 0 || j === 5),
        color: isPriority1 ? "2E7D32" : C.textDark,
      },
    }));
  }

  // Style total row
  const lastIdx = rows.length - 1;
  rows[lastIdx] = rows[lastIdx].map((t, j) => ({
    text: t, options: {
      fill: { color: C.tealLight }, fontSize: 11,
      bold: true, color: C.primary,
      align: j === 0 ? "left" : "center",
    },
  }));

  slide.addTable(rows, {
    x: 0.3, y: 1.5, w: 9.4,
    colW: [2.2, 1.7, 1.2, 1.2, 1.2, 1.5],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: 0.55,
  });

  slide.addText("Segments A (Enterprise Grocery) and E (Candy/Confectionery) are Priority 1 \u2014 highest deal density and strongest Newport fit.", {
    x: 0.6, y: 6.0, w: 8.8, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.primary, bold: true, italic: true, align: "center",
  });

  addSource(slide, "Source: ICP definitions, Apollo.io coverage, commercial model \u2014 Feb 2026");
}

// ============================================================================
// SLIDE 5: How It Works — Find (1 of 4)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "How It Works: Find");

  slide.addText("1 of 4", {
    x: 8.5, y: 0.35, w: 1.2, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.medGray, align: "right",
  });

  const channels = [
    {
      title: "Apollo.io Search",
      desc: "AI-powered contact discovery across all 5 segments. 60-70% US coverage. Filters by title, seniority, company size, NAICS code.",
    },
    {
      title: "LinkedIn Intelligence",
      desc: "Manual enrichment for high-value targets. Decision-maker mapping. Company org charts and buying committee identification.",
    },
    {
      title: "Industry Databases",
      desc: "NAICS 424450 (1,831 candy firms), trade show exhibitor lists, CDA/NCA directories. Census data for market sizing.",
    },
    {
      title: "LATAM Coverage",
      desc: "Mexico 30-50%, Central America 10-25%. Spanish keyword targeting. USMCA = $0 tariff on Mexican candy imports.",
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
      x: x + 0.25, y: y + 0.65, w: 3.7, h: 1.5,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3,
    });
  });
}

// ============================================================================
// SLIDE 6: How It Works — Enrich (2 of 4)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "How It Works: Enrich");

  slide.addText("2 of 4", {
    x: 8.5, y: 0.35, w: 1.2, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.medGray, align: "right",
  });

  // Left column: pipeline
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.5, w: 4.3, h: 5.0, rectRadius: 0.1,
    fill: { color: C.tealLight },
  });
  slide.addText("Contact Enrichment Pipeline", {
    x: 0.75, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 16, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });

  const pipelineSteps = [
    "Apollo reveals: email, phone, title",
    "Email verification (bounce-check)",
    "Company data: size, revenue, NAICS",
    "Tech stack detection",
    "Intent signals (hiring, funding)",
    "ICP scoring & segment assignment",
    "Dedup against existing contacts",
    "CRM-ready contact card",
  ];

  pipelineSteps.forEach((p, i) => {
    slide.addText(`${i + 1}.  ${p}`, {
      x: 0.75, y: 2.4 + i * 0.45, w: 3.8, h: 0.4,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
    });
  });

  // Right column: sample card
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 5.2, y: 1.5, w: 4.3, h: 5.0, rectRadius: 0.1,
    fill: { color: C.lightGray },
  });
  slide.addText("Sample Prospect Card", {
    x: 5.45, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 16, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });

  const cardFields = [
    ["Name", "Jane Rodriguez"],
    ["Title", "VP of Procurement"],
    ["Company", "Southeast Grocers"],
    ["Email", "jane.r@segrocers.com \u2705"],
    ["Phone", "(305) 555-0142"],
    ["Company Size", "5,001-10,000 employees"],
    ["Est. Revenue", "$100M-$500M"],
    ["Location", "Jacksonville, FL"],
    ["Segment", "A \u2014 Enterprise Grocery"],
  ];

  cardFields.forEach((f, i) => {
    const y = 2.4 + i * 0.42;
    slide.addText(f[0] + ":", {
      x: 5.45, y, w: 1.4, h: 0.38,
      fontSize: 10, fontFace: FONT_BODY, color: C.medGray, bold: true,
    });
    slide.addText(f[1], {
      x: 6.85, y, w: 2.5, h: 0.38,
      fontSize: 10, fontFace: FONT_BODY, color: C.textDark,
    });
  });

  slide.addText("(Illustrative \u2014 not a real contact)", {
    x: 5.45, y: 6.3, w: 3.8, h: 0.3,
    fontSize: 8, fontFace: FONT_BODY, color: C.medGray, italic: true,
  });
}

// ============================================================================
// SLIDE 7: How It Works — Reach (3 of 4)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "How It Works: Reach");

  slide.addText("3 of 4", {
    x: 8.5, y: 0.35, w: 1.2, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.medGray, align: "right",
  });

  const scenarios = [
    {
      title: "Free",
      cost: "$0/yr",
      capacity: "50 prospects/week",
      desc: "Manual LinkedIn + Apollo. Personal outreach. Best for testing the waters.",
      color: C.green,
      bgColor: "E8F5E9",
    },
    {
      title: "Moderate",
      cost: "$1,032/yr",
      capacity: "450 contacts/week",
      desc: "Email automation via Instantly. Sequenced follow-ups. 9x the reach of Free.",
      color: C.secondary,
      bgColor: C.tealLight,
    },
    {
      title: "Aggressive",
      cost: "$9,072/yr",
      capacity: "900 contacts/week",
      desc: "Multi-channel \u2014 email + SMS + AI voice. 18x reach. Full automation stack.",
      color: C.yellow,
      bgColor: "FFF8E1",
    },
  ];

  scenarios.forEach((s, i) => {
    const x = 0.4 + i * 3.15;
    const y = 1.5;
    const w = 2.9;
    const h = 5.0;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w, h, rectRadius: 0.1,
      fill: { color: s.bgColor },
    });

    // Colored accent bar at top
    slide.addShape(pptx.shapes.RECTANGLE, {
      x, y, w, h: 0.08,
      fill: { color: s.color },
    });

    slide.addText(s.title, {
      x: x + 0.2, y: y + 0.2, w: w - 0.4, h: 0.45,
      fontSize: 18, fontFace: FONT_HEADER, color: C.accent, bold: true, align: "center",
    });
    slide.addText(s.cost, {
      x: x + 0.2, y: y + 0.7, w: w - 0.4, h: 0.4,
      fontSize: 22, fontFace: FONT_HEADER, color: s.color, bold: true, align: "center",
    });
    slide.addText(s.capacity, {
      x: x + 0.2, y: y + 1.2, w: w - 0.4, h: 0.35,
      fontSize: 12, fontFace: FONT_BODY, color: C.primary, bold: true, align: "center",
    });
    slide.addText(s.desc, {
      x: x + 0.2, y: y + 1.7, w: w - 0.4, h: 1.5,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
      lineSpacingMultiple: 1.3, align: "center",
    });
  });

  slide.addText("All scenarios use the same enrichment pipeline. The difference is reach and automation.", {
    x: 0.6, y: 6.8, w: 8.8, h: 0.4,
    fontSize: 11, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 8: How It Works — Convert (4 of 4)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "How It Works: Convert");

  slide.addText("4 of 4", {
    x: 8.5, y: 0.35, w: 1.2, h: 0.5,
    fontSize: 11, fontFace: FONT_BODY, color: C.medGray, align: "right",
  });

  // Left: The Funnel (pipeline stages)
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.5, w: 4.3, h: 5.0, rectRadius: 0.1,
    fill: { color: C.tealLight },
  });
  slide.addText("The Funnel", {
    x: 0.75, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 16, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });

  const funnelStages = [
    { name: "Prospect", desc: "Identified & enriched", color: C.medGray, width: 3.6 },
    { name: "Opened", desc: "Email opened (22%)", color: C.secondary, width: 3.0 },
    { name: "Replied", desc: "Positive reply (3.5%)", color: C.primary, width: 2.4 },
    { name: "Meeting", desc: "Meeting booked (35%)", color: C.accent, width: 1.8 },
    { name: "Deal", desc: "Closed won (18%)", color: C.green, width: 1.2 },
  ];

  funnelStages.forEach((stage, i) => {
    const y = 2.4 + i * 0.75;
    const x = 0.75 + (3.6 - stage.width) / 2;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x, y, w: stage.width, h: 0.55, rectRadius: 0.06,
      fill: { color: stage.color },
    });
    slide.addText(`${stage.name} \u2014 ${stage.desc}`, {
      x, y, w: stage.width, h: 0.55,
      fontSize: 10, fontFace: FONT_BODY, color: C.white, bold: true, align: "center", valign: "middle",
    });
  });

  // Right: Conversion Metrics
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 5.2, y: 1.5, w: 4.3, h: 5.0, rectRadius: 0.1,
    fill: { color: C.lightGray },
  });
  slide.addText("Conversion Metrics", {
    x: 5.45, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 16, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });

  const metrics = [
    { label: "Email Open Rate", value: "22%", note: "B2B benchmark: 18-25%" },
    { label: "Reply Rate", value: "3.5%", note: "Cold email: 2-5%" },
    { label: "Reply \u2192 Meeting", value: "35%", note: "Positive replies that book" },
    { label: "Meeting \u2192 Deal", value: "18%", note: "Cold outreach close rate" },
    { label: "Avg Sales Cycle", value: "45 days", note: "First meeting to closed deal" },
    { label: "Avg Deal Size", value: "$28K", note: "Weighted across 5 segments" },
  ];

  metrics.forEach((m, i) => {
    const y = 2.4 + i * 0.7;

    slide.addText(m.label, {
      x: 5.45, y, w: 2.0, h: 0.3,
      fontSize: 10, fontFace: FONT_BODY, color: C.medGray,
    });
    slide.addText(m.value, {
      x: 7.5, y, w: 1.0, h: 0.3,
      fontSize: 13, fontFace: FONT_HEADER, color: C.primary, bold: true, align: "right",
    });
    slide.addText(m.note, {
      x: 5.45, y: y + 0.28, w: 3.8, h: 0.25,
      fontSize: 8, fontFace: FONT_BODY, color: C.medGray, italic: true,
    });
  });
}

// ============================================================================
// SLIDE 9: The Economics (3-scenario summary table)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "The Economics");

  slide.addText("12-Month Projection at Default Parameters", {
    x: 0.6, y: 1.1, w: 8.8, h: 0.35,
    fontSize: 12, fontFace: FONT_BODY, color: C.secondary, italic: true, align: "center",
  });

  const s = SCENARIOS;

  const rows = [
    ["Metric", "Free", "Moderate", "Aggressive"],
    ["Prospects/Month", s.free.prospectsMonth.toLocaleString(), s.moderate.prospectsMonth.toLocaleString(), s.aggressive.prospectsMonth.toLocaleString()],
    ["Meetings/Month", Math.round(s.free.meetings12mo / 10).toString(), Math.round(s.moderate.meetings12mo / 10).toString(), Math.round(s.aggressive.meetings12mo / 10).toString()],
    ["Deals (12-mo)", s.free.deals12mo.toString(), s.moderate.deals12mo.toString(), s.aggressive.deals12mo.toString()],
    ["Revenue (12-mo)", fmtDollarsK(s.free.revenue12mo), fmtDollarsK(s.moderate.revenue12mo), fmtDollarsK(s.aggressive.revenue12mo)],
    ["Gross Profit", fmtDollarsK(s.free.grossProfit12mo), fmtDollarsK(s.moderate.grossProfit12mo), fmtDollarsK(s.aggressive.grossProfit12mo)],
    ["Tool Costs", fmtDollarsK(s.free.toolCostAnnual), fmtDollarsK(s.moderate.toolCostAnnual), fmtDollarsK(s.aggressive.toolCostAnnual)],
    ["Net Contribution", fmtDollarsK(s.free.netContribution12mo), fmtDollarsK(s.moderate.netContribution12mo), fmtDollarsK(s.aggressive.netContribution12mo)],
  ];

  // Style header
  rows[0] = rows[0].map((t, j) => ({
    text: t, options: {
      bold: true, color: C.white, fontSize: 11, align: "center",
      fill: { color: j === 0 ? C.accent : C.primary },
    },
  }));

  // Style data rows
  for (let i = 1; i < rows.length; i++) {
    const isNet = i === rows.length - 1;
    const isCost = i === rows.length - 2;
    const bg = isNet ? "E8F5E9" : (i % 2 === 0 ? C.lightGray : C.white);

    rows[i] = rows[i].map((t, j) => {
      let color = C.textDark;
      if (j === 1) color = "2E7D32"; // Free = green
      if (j === 2) color = C.secondary; // Moderate = teal
      if (j === 3) color = C.yellow; // Aggressive = amber
      if (isCost && j > 0) color = C.red;

      return {
        text: t, options: {
          fill: { color: isNet ? "E8F5E9" : bg },
          fontSize: isNet ? 12 : 10.5,
          bold: j === 0 || isNet,
          color: j === 0 ? C.textDark : color,
          align: j === 0 ? "left" : "center",
        },
      };
    });
  }

  slide.addTable(rows, {
    x: 0.6, y: 1.7, w: 8.8,
    colW: [2.2, 2.0, 2.2, 2.4],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
    rowH: [0.45, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.6],
  });

  slide.addText("All scenarios share the same conversion assumptions. The difference is reach.\nModerate delivers 9x the prospects for $86/month. Aggressive delivers 18x for $756/month.", {
    x: 0.6, y: 6.0, w: 8.8, h: 0.7,
    fontSize: 11, fontFace: FONT_BODY, color: C.primary, bold: true, italic: true, align: "center",
    lineSpacingMultiple: 1.3,
  });

  addSource(slide, "Source: Commercial SDR Financial Model \u2014 default params, 22% margin, $28K avg deal, Feb 2026");
}

// ============================================================================
// SLIDE 10: Two Channels, One Strategy
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Two Channels, One Strategy");

  // Left: GovCon channel
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.5, w: 4.3, h: 4.5, rectRadius: 0.1,
    fill: { color: C.tealLight },
    line: { color: C.primary, width: 1.5 },
  });
  slide.addText("GovCon Channel", {
    x: 0.75, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 18, fontFace: FONT_HEADER, color: C.primary, bold: true,
  });

  const govconPoints = [
    "Federal/state food procurement",
    "$87M Florida TAM",
    "5-year compounding portfolio",
    "$841K cumulative owner earnings (v7 model)",
    "Post-fraud tailwind: 1,091 firms suspended",
    "Agencies need clean vendors now",
  ];

  govconPoints.forEach((p, i) => {
    slide.addText(`\u2022  ${p}`, {
      x: 0.75, y: 2.4 + i * 0.5, w: 3.8, h: 0.45,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
    });
  });

  // Right: Commercial SDR channel
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 5.2, y: 1.5, w: 4.3, h: 4.5, rectRadius: 0.1,
    fill: { color: C.lightGray },
    line: { color: C.secondary, width: 1.5 },
  });
  slide.addText("Commercial SDR", {
    x: 5.45, y: 1.7, w: 3.8, h: 0.5,
    fontSize: 18, fontFace: FONT_HEADER, color: C.secondary, bold: true,
  });

  const sdrPoints = [
    "AI-powered outbound prospecting",
    `${TOTAL_COMPANIES.toLocaleString()} target companies across 5 segments`,
    "12-month payback cycle",
    "Scales with investment",
    "Immediate revenue potential",
    `Up to ${fmtDollarsK(SCENARIOS.aggressive.netContribution12mo)} net in Year 1`,
  ];

  sdrPoints.forEach((p, i) => {
    slide.addText(`\u2022  ${p}`, {
      x: 5.45, y: 2.4 + i * 0.5, w: 3.8, h: 0.45,
      fontSize: 10.5, fontFace: FONT_BODY, color: C.textDark,
    });
  });

  // Bottom callout
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 6.3, w: 9.0, h: 0.9, rectRadius: 0.1,
    fill: { color: "FFF8E1" },
  });
  slide.addText("Both channels share the same infrastructure: warehouse, fleet, workforce, relationships.\nEach contract won makes the next one easier.", {
    x: 0.7, y: 6.35, w: 8.6, h: 0.8,
    fontSize: 11, fontFace: FONT_BODY, color: C.textDark, bold: true, align: "center",
    lineSpacingMultiple: 1.3,
  });
}

// ============================================================================
// SLIDE 11: Key Questions
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  addHeadline(slide, "Key Questions: Decisions That Calibrate the Model");

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

  slide.addText("These questions directly change the financial model. Answering them lets us customize projections to Newport\u2019s actual situation.", {
    x: 0.6, y: 7.0, w: 8.8, h: 0.4,
    fontSize: 10, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 12: Next Steps
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
    { num: "1", title: "Answer Key Questions", desc: "Review the 10 questions. Your answers calibrate the model to Newport\u2019s actual deal sizes, margins, and capacity." },
    { num: "2", title: "Choose a Segment", desc: "Start with 1-2 priority segments for focused results. We recommend Segment A (Enterprise Grocery) and E (Candy)." },
    { num: "3", title: "Pick Your Scenario", desc: "Free, Moderate, or Aggressive \u2014 match your comfort level. You can always scale up after initial results." },
    { num: "4", title: "30-Day Pilot", desc: "One segment, one scenario, real results in 30 days. Measure opens, replies, meetings, and pipeline." },
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
const outPath = path.join(__dirname, "newport-commercial-sdr-proposal.pptx");
pptx.writeFile({ fileName: outPath }).then(() => {
  console.log(`\nPresentation saved to ${outPath}`);
  console.log("12 slides generated (commercial SDR deck).");
}).catch(err => {
  console.error("Failed to generate presentation:", err);
  process.exit(1);
});
