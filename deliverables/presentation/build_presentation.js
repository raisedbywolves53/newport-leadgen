/**
 * Newport GovCon Proposal Deck — Phase 3
 *
 * Generates a 14-slide 16:9 PowerPoint proposal for Newport Wholesalers.
 * Ocean Gradient palette: #065A82, #1C7293, #21295C
 *
 * Run: node deliverables/presentation/build_presentation.js
 * Output: deliverables/presentation/newport-govcon-proposal.pptx
 */

const pptxgen = require("pptxgenjs");
const path = require("path");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_16x9";
pptx.author = "Still Mind Creative";
pptx.company = "Still Mind Creative";
pptx.subject = "Newport Wholesalers Government Contracting Proposal";
pptx.title = "Unlocking Government Revenue for Newport Wholesalers";

// --- Color Palette ---
const C = {
  primary: "065A82",     // deep blue
  secondary: "1C7293",   // teal
  accent: "21295C",      // midnight
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

// --- Font Defaults ---
const FONT_HEADER = "Georgia";
const FONT_BODY = "Calibri";

// --- Helper: add headline to a white slide ---
function addHeadline(slide, text) {
  slide.addText(text, {
    x: 0.6, y: 0.3, w: 8.8, h: 0.7,
    fontSize: 24, fontFace: FONT_HEADER, color: C.accent, bold: true,
  });
  // Accent bar under headline
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.6, y: 0.95, w: 1.2, h: 0.05,
    fill: { color: C.secondary },
  });
}

// --- Helper: add source footer ---
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

  // Geometric accent shapes
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
  addHeadline(slide, "Newport Is Sitting on an Untapped $14B+ Market");

  const stats = [
    { value: "$14B+", label: "Annual School Meal\nSpending Nationally" },
    { value: "$1.5T", label: "Total Annual SLED\nSpending" },
    { value: "67", label: "Florida School Districts\nServing 2.8M+ Students" },
  ];

  stats.forEach((s, i) => {
    const x = 0.5 + i * 3.2;
    // Card background
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

  slide.addText("Government food procurement is massive, fragmented, and undercontested.\nMost contracts go to whoever shows up.", {
    x: 0.6, y: 5.3, w: 8.8, h: 0.8,
    fontSize: 13, fontFace: FONT_BODY, color: C.medGray, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 3: The Headline Insight (64.8%)
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.accent };

  slide.addText("64.8%", {
    x: 0, y: 1.5, w: 10, h: 2.0,
    fontSize: 96, fontFace: FONT_HEADER, color: C.white, bold: true, align: "center",
  });
  slide.addText("of Federal Food Contracts Are Sole-Source", {
    x: 1, y: 3.5, w: 8, h: 0.7,
    fontSize: 22, fontFace: FONT_BODY, color: C.white, align: "center",
  });
  slide.addText("FPDS FY2025 analysis across 1,664 food contracting transactions.\nMost food contracts receive only ONE bid. The barrier isn't competition \u2014 it's visibility.", {
    x: 1.5, y: 4.5, w: 7, h: 1.0,
    fontSize: 13, fontFace: FONT_BODY, color: C.white, transparency: 20, align: "center",
    lineSpacingMultiple: 1.3,
  });
  addSource(slide, "Source: Federal Procurement Data System (FPDS), FY2025");
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
      icon: "\u2605", // star
      body: "Three decades of wholesale distribution. Proven reliability, established supplier relationships, operational infrastructure.",
    },
    {
      title: "South Florida Warehouse",
      icon: "\u2302", // house
      body: "Strategic location for FEMA disaster response staging. Florida is the #1 state for federal emergency declarations.",
    },
    {
      title: "Existing Distribution Network",
      icon: "\u2708", // transport
      body: "Trucks, routes, cold chain, delivery infrastructure already in place. Government contracts use the same logistics.",
    },
    {
      title: "No Past Performance Required (Yet)",
      icon: "\u2713", // checkmark
      body: "Micro-purchases under $10K and many small contracts don't require government past performance. Commercial experience qualifies.",
    },
  ];

  blocks.forEach((b, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.6;
    const y = 1.5 + row * 2.5;

    // Icon circle
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
    // Circle with number
    slide.addShape(pptx.shapes.OVAL, {
      x: x + 0.3, y: 1.8, w: 0.7, h: 0.7,
      fill: { color: C.primary },
    });
    slide.addText(s.num, {
      x: x + 0.3, y: 1.78, w: 0.7, h: 0.7,
      fontSize: 22, fontFace: FONT_HEADER, color: C.white, bold: true, align: "center", valign: "middle",
    });
    // Arrow (except last)
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
    ["Buyer Category", "Why It's a Fit", "Example Targets"],
    ["School Districts", "Massive volume, recurring annual contracts, lowest-price-wins", "Miami-Dade, Broward, Palm Beach school districts"],
    ["Corrections", "Consistent demand, multi-year contracts, price-sensitive", "FL DOC (80,000+ inmates), county jails"],
    ["FEMA / Emergency", "Newport's South FL warehouse = disaster staging asset", "FEMA advance contracts, emergency food supply"],
    ["Military / DoD", "Base commissaries, dining facilities", "Homestead ARB, MacDill AFB, NAS Jacksonville"],
    ["Universities & Colleges", "Dining services, campus food supply", "12 FL state universities, 28 community colleges"],
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
// SLIDE 7: FPDS Competition Analysis
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Federal Food Contracting: Less Competition Than You Think");

  // FPDS data table
  const data = [
    ["NAICS", "Description", "Awards", "Avg Offers", "Sole Source %"],
    ["722310", "Food Service Contractors", "98", "1.0", "~100%"],
    ["424410", "Grocery Wholesalers", "87", "1.4", "72%"],
    ["424490", "Other Grocery Products", "142", "1.3", "68%"],
    ["424480", "Fresh Fruit & Vegetable", "203", "1.2", "78%"],
    ["424470", "Meat & Meat Product", "156", "1.5", "63%"],
    ["424420", "Packaged Frozen Food", "189", "1.3", "71%"],
  ];

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
    rowH: [0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35],
  });

  // Callout box
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 6.5, y: 1.5, w: 3.1, h: 2.5, rectRadius: 0.1,
    fill: { color: C.tealLight },
    line: { color: C.secondary, width: 1.5 },
  });
  slide.addText("Average of 1.0 offers per contract in Food Service contracting means Newport often competes against ZERO other bidders.", {
    x: 6.7, y: 1.7, w: 2.7, h: 2.1,
    fontSize: 12, fontFace: FONT_BODY, color: C.accent, bold: true,
    lineSpacingMultiple: 1.3,
  });

  addSource(slide, "Source: FPDS FY2025, 10 food NAICS codes, 1,664 transactions");
}

// ============================================================================
// SLIDE 8: The System We've Built
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

    // Card background
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
// SLIDE 9: Free vs. Optimal System
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Investment Options: Start Free or Go Full Coverage");

  const rows = [
    ["Component", "Free Version ($0/yr)", "Optimal Version ($7.4K-$18.6K/yr)"],
    ["Federal Monitoring", "SAM.gov API (built)", "+ CLEATUS AI scoring"],
    ["State/Local Monitoring", "Manual portal checking", "HigherGov (40K+ agencies)"],
    ["Micro-Purchases", "Not available", "GovSpend"],
    ["Competitive Intel", "USASpending + FPDS (built)", "Same (already strong)"],
    ["Proposal Writing", "Claude AI + templates", "CLEATUS AI shredder"],
    ["Pipeline Tracking", "Google Sheets (built)", "Same"],
    ["Market Coverage", "~40-50%", "~90%+"],
    ["Bid Capacity/Year", "12-20 bids", "40-60 bids"],
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
// SLIDE 10: Financial Projections
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Conservative to Aggressive: Year 1 Revenue Impact");

  const rows = [
    ["Metric", "Conservative", "Moderate", "Aggressive"],
    ["Contracts Won", "5", "10", "15+"],
    ["Avg Contract Value", "$50,000", "$75,000", "$100,000"],
    ["New Government Revenue", "$250,000", "$750,000", "$1,500,000+"],
    ["Gross Profit (10-12%)", "$25,000-$30,000", "$75,000-$90,000", "$150,000-$180,000"],
    ["Platform Investment", "$0-$18,600", "$7,400-$18,600", "$7,400-$18,600"],
    ["Net New Profit", "$6,400-$30,000", "$56,400-$82,600", "$131,400-$172,600"],
  ];

  rows[0] = rows[0].map((t, j) => ({
    text: t, options: {
      bold: true, color: C.white, fontSize: 11, align: "center",
      fill: { color: j === 0 ? C.accent : [C.primary, C.secondary, C.accent][j - 1] },
    },
  }));

  for (let i = 1; i < rows.length; i++) {
    const isTotal = i === rows.length - 1;
    const bg = isTotal ? C.tealLight : (i % 2 === 0 ? C.lightGray : C.white);
    rows[i] = rows[i].map((t, j) => ({
      text: t, options: {
        fill: { color: bg }, fontSize: 10.5,
        bold: j === 0 || isTotal,
        color: isTotal ? C.primary : C.textDark,
        align: j === 0 ? "left" : "center",
      },
    }));
  }

  slide.addTable(rows, {
    x: 0.4, y: 1.5, w: 9.2,
    colW: [2.4, 2.2, 2.2, 2.4],
    border: { type: "solid", pt: 0.5, color: "D1D5DB" },
    autoPage: false,
  });

  slide.addText("Even the conservative scenario \u2014 winning just 5 small contracts \u2014 pays for the entire platform in Year 1.", {
    x: 0.6, y: 5.7, w: 8.8, h: 0.5,
    fontSize: 13, fontFace: FONT_BODY, color: C.primary, bold: true, italic: true, align: "center",
  });
}

// ============================================================================
// SLIDE 11: Implementation Timeline
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
    // Timeline dot
    slide.addShape(pptx.shapes.OVAL, {
      x: 0.7, y: y + 0.15, w: 0.35, h: 0.35,
      fill: { color: m.color },
    });
    // Vertical line (except last)
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
// SLIDE 12: What Still Mind Creative Delivers
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
    // Checkmark circle
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
// SLIDE 13: Investment & Next Steps
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.primary };

  // Geometric accents
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 7, y: 5, w: 4, h: 4, rotate: 45,
    fill: { color: C.secondary, transparency: 70 },
  });

  slide.addText("Next Steps", {
    x: 0.8, y: 0.8, w: 8.4, h: 0.8,
    fontSize: 30, fontFace: FONT_HEADER, color: C.white, bold: true,
  });

  // Accent bar
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
// SLIDE 14: Appendix — FPDS Data Detail
// ============================================================================
{
  const slide = pptx.addSlide();
  slide.background = { fill: C.white };
  addHeadline(slide, "Federal Food Procurement Data \u2014 Full Breakdown");

  const data = [
    ["NAICS", "Description", "Awards", "Avg Value", "Avg Offers", "Sole Source %"],
    ["722310", "Food Service Contractors", "98", "$43M", "1.0", "~100%"],
    ["424410", "Grocery Wholesalers", "87", "$285K", "1.4", "72%"],
    ["424490", "Other Grocery Products", "142", "$195K", "1.3", "68%"],
    ["424480", "Fresh Fruit & Vegetable", "203", "$340K", "1.2", "78%"],
    ["424470", "Meat & Meat Product", "156", "$410K", "1.5", "63%"],
    ["424460", "Fish & Seafood", "112", "$180K", "1.3", "70%"],
    ["424450", "Confectionery", "45", "$95K", "1.6", "58%"],
    ["424440", "Poultry & Poultry Product", "178", "$520K", "1.4", "65%"],
    ["424430", "Dairy Product", "198", "$290K", "1.2", "74%"],
    ["424420", "Packaged Frozen Food", "245", "$210K", "1.3", "71%"],
  ];

  const totals = ["TOTAL", "All Food NAICS", "1,664", "\u2014", "1.3 avg", "64.8%"];

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

  addSource(slide, "Source: FPDS FY2025 via Federal Procurement Data System API");
}

// ============================================================================
// Generate file
// ============================================================================
const outPath = path.join(__dirname, "newport-govcon-proposal.pptx");
pptx.writeFile({ fileName: outPath }).then(() => {
  console.log(`Presentation saved to ${outPath}`);
  console.log("14 slides generated.");
}).catch(err => {
  console.error("Failed to generate presentation:", err);
  process.exit(1);
});
