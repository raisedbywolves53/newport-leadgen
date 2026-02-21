"""Generate Newport Wholesalers Government Contract Entry Pitchbook.

Creates a 16-slide professional PowerPoint presentation targeting
Newport leadership to secure buy-in for government contract entry,
with Still Mind Creative as the operational partner.

v2 — Full content rewrite: realistic FL pipeline numbers, sourced fraud data,
decision-tree risk framework, internal champions, selling seed, compelling close.

Usage:
    python pitchbook/generate_pitchbook.py
"""

import sys
from datetime import datetime
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "pitchbook"

# --- Color Palette ---
NAVY = RGBColor(0x1B, 0x2A, 0x4A)
GOLD = RGBColor(0xD4, 0xA8, 0x43)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF2, 0xF2, 0xF2)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MED_GRAY = RGBColor(0x66, 0x66, 0x66)
RED = RGBColor(0xCC, 0x00, 0x00)
GREEN = RGBColor(0x00, 0x7A, 0x33)
LIGHT_NAVY = RGBColor(0x2D, 0x3E, 0x6E)
GOLD_LIGHT = RGBColor(0xFF, 0xF8, 0xE7)
AMBER = RGBColor(0xE6, 0x8A, 0x00)

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def set_slide_bg(slide, color):
    """Set solid background color for a slide."""
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_textbox(slide, left, top, width, height, text="",
                font_size=18, font_color=DARK_GRAY, bold=False,
                alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    """Add a text box with styled text."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = font_color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_multiline_textbox(slide, left, top, width, height, lines,
                          font_size=16, font_color=DARK_GRAY, bold=False,
                          alignment=PP_ALIGN.LEFT, line_spacing=Pt(6)):
    """Add a text box with multiple styled paragraphs."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(font_size)
        p.font.color.rgb = font_color
        p.font.bold = bold
        p.font.name = "Calibri"
        p.alignment = alignment
        p.space_after = line_spacing
    return txBox


def add_bullet_list(slide, left, top, width, height, items,
                    font_size=16, font_color=DARK_GRAY, bullet_char="\u2022",
                    spacing=Pt(8)):
    """Add a bulleted list."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True

    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"{bullet_char} {item}"
        p.font.size = Pt(font_size)
        p.font.color.rgb = font_color
        p.font.name = "Calibri"
        p.space_after = spacing

    return txBox


def add_kpi_card(slide, left, top, width, height, value, label,
                 value_color=NAVY, value_size=36, border_color=GOLD):
    """Add a KPI card with large value and small label."""
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = border_color
    shape.line.width = Pt(2)
    shape.shadow.inherit = False

    txBox = slide.shapes.add_textbox(
        left + Inches(0.1), top + Inches(0.15),
        width - Inches(0.2), Inches(0.7)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = value
    p.font.size = Pt(value_size)
    p.font.color.rgb = value_color
    p.font.bold = True
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER

    txBox2 = slide.shapes.add_textbox(
        left + Inches(0.1), top + height - Inches(0.55),
        width - Inches(0.2), Inches(0.45)
    )
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    p2 = tf2.paragraphs[0]
    p2.text = label
    p2.font.size = Pt(11)
    p2.font.color.rgb = MED_GRAY
    p2.font.name = "Calibri"
    p2.alignment = PP_ALIGN.CENTER

    return shape


def add_table(slide, left, top, width, rows, cols, data,
              col_widths=None, header_bg=NAVY, header_fg=WHITE,
              font_size=12):
    """Add a styled table."""
    row_height = Inches(0.4)
    table_height = row_height * rows
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, table_height)
    table = table_shape.table

    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = w

    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.text = str(data[r][c]) if r < len(data) and c < len(data[r]) else ""

            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(font_size)
                paragraph.font.name = "Calibri"

                if r == 0:
                    paragraph.font.color.rgb = header_fg
                    paragraph.font.bold = True
                    paragraph.alignment = PP_ALIGN.CENTER
                else:
                    paragraph.font.color.rgb = DARK_GRAY

            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_bg
            elif r % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = LIGHT_GRAY

            cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    return table_shape


def add_divider(slide, left, top, width, color=GOLD):
    """Add a horizontal gold divider line."""
    shape = slide.shapes.add_shape(1, left, top, width, Pt(3))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_callout_bar(slide, left, top, width, height, text,
                    bg_color=NAVY, text_color=GOLD, font_size=16):
    """Add a colored bar with centered text."""
    shape = slide.shapes.add_shape(1, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()
    add_textbox(slide, left, top, width, height,
                text, font_size=font_size, font_color=text_color,
                bold=True, alignment=PP_ALIGN.CENTER)
    return shape


# ========== SLIDE BUILDERS ==========

def slide_01_cover(prs):
    """Slide 1: Cover"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_textbox(slide, Inches(1.5), Inches(1.5), Inches(10), Inches(1.5),
                "Newport Wholesalers", font_size=48, font_color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(1.5), Inches(3.0), Inches(10), Inches(1),
                "Government Contract Entry Strategy", font_size=32, font_color=GOLD,
                bold=False, alignment=PP_ALIGN.CENTER)

    add_divider(slide, Inches(4), Inches(4.2), Inches(5))

    add_textbox(slide, Inches(1.5), Inches(4.6), Inches(10), Inches(0.5),
                "Prepared by Still Mind Creative LLC", font_size=18,
                font_color=WHITE, alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(1.5), Inches(5.2), Inches(10), Inches(0.5),
                datetime.now().strftime("%B %Y"), font_size=16,
                font_color=MED_GRAY, alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(1.5), Inches(6.5), Inches(10), Inches(0.4),
                "CONFIDENTIAL", font_size=12, font_color=MED_GRAY,
                alignment=PP_ALIGN.CENTER)


def slide_02_exec_summary(prs):
    """Slide 2: Executive Summary — The 30-Year Seed"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Executive Summary", font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # The narrative — visual KPI row first
    cards = [
        ("30+", "Years in FL\nFood Wholesale"),
        ("$15-20M", "Realistic 3-Year\nPipeline (FL Only)"),
        ("76", "FL Decision Makers\nAlready Identified"),
        ("$5-12K", "Year 1 Investment\n(Registrations + Materials)"),
    ]
    card_width = Inches(2.7)
    card_gap = Inches(0.3)
    start_x = Inches(0.8)
    for i, (val, label) in enumerate(cards):
        x = start_x + i * (card_width + card_gap)
        add_kpi_card(slide, x, Inches(1.5), card_width, Inches(1.3), val, label,
                     value_size=30)

    # The story
    add_textbox(slide, Inches(0.8), Inches(3.2), Inches(11.5), Inches(0.4),
                "The Story in 60 Seconds:", font_size=20, font_color=NAVY, bold=True)

    items = [
        "Newport has spent 30 years building the exact infrastructure governments need: warehouses, trucks, cold chain, supplier relationships, and a track record of feeding people.",
        "The federal government is in the middle of the largest fraud crackdown in procurement history. Agencies are desperate for verifiable, legitimate American vendors.",
        "We've identified $15-20M in realistic, winnable Florida contracts over 3 years — school districts, county jails, federal prisons, and private contractor supply chains.",
        "Newport's sales team builds relationships and closes deals. Still Mind Creative handles the government procurement bureaucracy — monitoring, proposals, compliance.",
        "Year 1 is about winning contracts — even small ones — to build the credibility that compounds into larger wins. The investment is modest. The upside is a new revenue channel that transforms the business.",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(3.7), Inches(11.5), Inches(3.5),
                    items, font_size=15, spacing=Pt(8))


def slide_03_market_opportunity(prs):
    """Slide 3: The Market Opportunity — What Newport Can Actually Win"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "What Newport Can Actually Win in Florida",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(11), Inches(0.4),
                "Not the total market. Not the fantasy. The contracts a Florida wholesale distributor can realistically bid and win.",
                font_size=15, font_color=MED_GRAY)

    # Main table: FL opportunity breakdown
    data = [
        ["Channel", "# of Targets", "Contract Value (Each)", "Bid Window", "Year 1 Target", "3-Year Target"],
        ["FL School District ITBs\n(category bids: meat, dairy, frozen, produce)",
         "67 districts\n(Top 25 by enrollment)", "$2-10M per category", "Feb-May\n(for July start)",
         "$0-3M\n(1-2 wins)", "$5-15M/yr"],
        ["FL County Jail Food Supply\n(self-operated kitchens)",
         "3-5 confirmed\nself-op counties", "$1-3.5M/yr per county", "Varies by\ncounty cycle",
         "$0-2M\n(1 win)", "$3-8M/yr"],
        ["BOP Quarterly Subsistence\n(8 FL federal prisons)",
         "8 institutions\n(FCC Coleman = largest)", "$75K-2.5M/quarter", "Quarterly\n(constant cycle)",
         "$0-500K\n(1-2 quarters)", "$1-3M/yr"],
        ["Private Contractor Supply\n(GEO, CoreCivic, Trinity, Aramark)",
         "4-6 FL-based\ncontractors", "Varies by\nfacility", "Ongoing vendor\napplications",
         "Vendor approval\n+ first orders", "$1-3M/yr"],
        ["USDA AMS / LFPA / FEMA\n(commodity, emergency, food bank)",
         "Multiple\nprograms", "$200K-5M each", "Year-round", "Applications\nsubmitted",
         "$500K-3M/yr"],
    ]
    add_table(slide, Inches(0.3), Inches(1.8), Inches(12.7),
              len(data), 6, data,
              col_widths=[Inches(3.2), Inches(1.7), Inches(1.8), Inches(1.5), Inches(1.8), Inches(1.8)],
              font_size=10)

    # Bottom KPI summary
    cards = [
        ("$1-2.5M", "Year 1 Realistic\nMidpoint"),
        ("$5-8M", "Year 2 Realistic\nMidpoint"),
        ("$10-15M", "Year 3 Realistic\nMidpoint"),
        ("$15-20M", "Cumulative\n3-Year Pipeline"),
    ]
    card_width = Inches(2.7)
    for i, (val, label) in enumerate(cards):
        x = Inches(0.8) + i * (card_width + Inches(0.3))
        add_kpi_card(slide, x, Inches(5.8), card_width, Inches(1.3), val, label,
                     value_color=GREEN, value_size=28)

    add_textbox(slide, Inches(0.8), Inches(7.15), Inches(11), Inches(0.3),
                "Source: Conservative projection based on FL district enrollment data, BOP population, county jail populations, and industry bid win rates (15-25% for new entrants).",
                font_size=10, font_color=MED_GRAY)


def slide_04_fraud_crisis(prs):
    """Slide 4: Why Now — The Fraud Crisis"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Why Now — The Fraud Crisis Creates Opportunity",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # Fraud data table — sourced, not inflated
    data = [
        ["What Happened", "Scale", "Source", "Newport Implication"],
        ["False Claims Act recoveries hit\nall-time record (FY2025)",
         "$6.9 BILLION\n(single fiscal year)",
         "DOJ FCA\nAnnual Report",
         "Procurement officers are terrified of\nawarding to the wrong vendor"],
        ["COVID pandemic program fraud\n(PPP, EIDL, nutrition programs)",
         "$200-300 BILLION\n(cumulative est.)",
         "GAO / OIG\nReports",
         "Every new vendor faces heightened\nscrutiny — legitimacy is a weapon"],
        ["Feeding Our Future fraud\n(MN school nutrition)",
         "$250M stolen\n79 indicted, 56+ guilty",
         "DOJ Press\nReleases (2023-26)",
         "School nutrition procurement under\nmicroscope — clean vendors wanted"],
        ["SBA 8(a) program — first audit\nin 50 years",
         "1,091 firms suspended\n(25% of program)",
         "SBA OIG\n(Jan-Feb 2026)",
         "Set-aside contracts need legitimate\nsmall businesses to fill the gaps"],
        ["Aramark class-action (Dec 2025) —\ncutting meals, insect contamination",
         "Multiple states\naffected",
         "Reuters /\nLegal filings",
         "Agencies losing faith in mega-FSMCs —\nopening doors for alternatives"],
        ["Trinity Services OK contract voided\nafter 4 weeks (June 2025)",
         "State-level\ncontract failure",
         "OK DOC Public\nRecords",
         "Even experienced gov contractors\nare stumbling — room for new entrants"],
    ]
    add_table(slide, Inches(0.3), Inches(1.5), Inches(12.7),
              len(data), 4, data,
              col_widths=[Inches(3.2), Inches(2.2), Inches(1.8), Inches(3.5)],
              font_size=10)

    # Bottom callout
    add_callout_bar(slide, Inches(1.5), Inches(6.3), Inches(10), Inches(0.8),
                    '"Newport doesn\'t need to pretend to be something it\'s not.\n'
                    'It IS what the government is looking for — a real company, with real infrastructure, real history."',
                    font_size=15)


def slide_05_competitive_moat(prs):
    """Slide 5: Newport's Competitive Moat"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Newport's Competitive Moat", font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    add_textbox(slide, Inches(0.8), Inches(1.4), Inches(11), Inches(0.5),
                "What scared procurement officers want to see — and what Newport already has:",
                font_size=18, font_color=MED_GRAY)

    # Two-column table format instead of bullets
    data = [
        ["What Governments Verify", "Newport's Position", "Why It Matters"],
        ["Continuous business history", "30+ years in Florida",
         "Proves stability — shell companies get caught in months"],
        ["Physical infrastructure", "Warehouses + truck fleet (address verifiable)",
         "Inspectable, real — not a P.O. box and a dream"],
        ["Cold chain capability", "Existing refrigerated distribution",
         "Critical for food safety compliance (HACCP/SQF)"],
        ["Financial stability", "25+ years of American tax returns, banking relationships",
         "Auditable, provable — the 8(a) frauds had none of this"],
        ["Small business qualification", "NAICS 424410 ($200M threshold)",
         "Locks out Sysco, US Foods, Aramark from set-aside bids"],
        ["Florida home state", "Local presence, local preference scoring",
         "FL state/county contracts give scoring advantage to FL vendors"],
        ["Product breadth", "Grocery + frozen + dairy + produce + dry goods",
         "Single-vendor convenience for smaller agencies"],
        ["Existing sales team", "Experienced relationship builders",
         "Government contracts are won in meetings, not on paper"],
    ]
    add_table(slide, Inches(0.3), Inches(2.0), Inches(12.7),
              len(data), 3, data,
              col_widths=[Inches(3), Inches(4.2), Inches(5.5)],
              font_size=11)

    # Set-aside callout
    shape = slide.shapes.add_shape(1, Inches(0.8), Inches(6.2), Inches(11.7), Inches(1))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0xFE, 0xF9, 0xE7)
    shape.line.color.rgb = GOLD
    shape.line.width = Pt(2)

    add_textbox(slide, Inches(1.0), Inches(6.25), Inches(11.3), Inches(0.4),
                "KEY ADVANTAGE: ~23% of federal contracts are reserved for small businesses.",
                font_size=16, font_color=NAVY, bold=True)
    add_textbox(slide, Inches(1.0), Inches(6.65), Inches(11.3), Inches(0.5),
                "Newport qualifies. Sysco, US Foods, Aramark, Compass, and every other billion-dollar distributor do not. "
                "They are legally excluded from bidding on these contracts. This is not a nice-to-have — it is a structural advantage.",
                font_size=13, font_color=DARK_GRAY)


def slide_06_competitive_landscape(prs):
    """Slide 6: Competitive Landscape — flipped: FIGHT HERE on left."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Where to Fight — And Where Not To",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # LEFT: Fight here (the emphasis)
    add_textbox(slide, Inches(0.8), Inches(1.5), Inches(5.5), Inches(0.4),
                "FIGHT HERE — WIN NOW", font_size=20, font_color=GREEN, bold=True)
    fight_items = [
        "FL school district category ITBs (25 districts, lowest bid wins)",
        "FL county jails — self-operated kitchens (Pinellas, Polk, Miami-Dade)",
        "BOP quarterly subsistence (8 FL prisons, constant bid cycle)",
        "Small business set-aside contracts (Sysco/US Foods locked out)",
        "Private contractor vendor applications (GEO, Trinity — both in FL)",
        "Sources Sought responses (shape future solicitations in your favor)",
        "FEMA/FDEM emergency food staging (FL hurricane season)",
        "Simplified acquisitions $15K-$350K (posted on SAM.gov daily)",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.0), Inches(5.5), Inches(3.0),
                    fight_items, font_size=13, font_color=DARK_GRAY,
                    bullet_char="\u2713", spacing=Pt(5))

    # RIGHT: Don't fight here
    add_textbox(slide, Inches(6.8), Inches(1.5), Inches(5.5), Inches(0.4),
                "DON'T FIGHT HERE (YET)", font_size=20, font_color=RED, bold=True)
    dont_items = [
        "DLA Prime Vendor mega-contracts (Sysco/US Foods stranglehold)",
        "National FSMC contracts (Aramark, Compass, Sodexo)",
        "VA medical center food (locked under US Foods SPV through 2028)",
        "Large multi-state school nutrition cooperatives",
        "Contracts requiring 5+ years government past performance",
        "Micro-purchases under $15K (not posted, relationship-dependent)",
    ]
    add_bullet_list(slide, Inches(6.8), Inches(2.0), Inches(5.5), Inches(2.5),
                    dont_items, font_size=13, font_color=MED_GRAY,
                    bullet_char="\u2717", spacing=Pt(5))

    # Dual path strategy table
    add_textbox(slide, Inches(0.8), Inches(5.0), Inches(11), Inches(0.4),
                "THE DUAL-PATH STRATEGY", font_size=18, font_color=NAVY, bold=True)

    data = [
        ["Path", "Target", "How It Works", "Why It's Smart"],
        ["Path 1:\nDirect Government",
         "School districts, BOP,\ncounty jails, USDA",
         "Win contracts directly\nthrough competitive bidding",
         "Build past performance\n+ direct agency relationships"],
        ["Path 2:\nPrivate Contractor Supply",
         "GEO Group (Boca Raton),\nTrinity (Oldsmar), CoreCivic,\nAramark, Compass",
         "Become approved vendor —\nthey issue their own RFPs\nfor food supply",
         "Volume without bidding\noverhead — they manage\nthe government contract"],
    ]
    add_table(slide, Inches(0.5), Inches(5.5), Inches(12.3),
              len(data), 4, data,
              col_widths=[Inches(2), Inches(2.8), Inches(3.5), Inches(3)],
              font_size=10)

    add_textbox(slide, Inches(0.8), Inches(7.0), Inches(11), Inches(0.3),
                "GEO Group HQ: Boca Raton, FL. Trinity HQ: Oldsmar, FL. Local meetings are possible this month.",
                font_size=12, font_color=GOLD, bold=True)


def slide_07_pipeline(prs):
    """Slide 7: The Pipeline — Specific FL Opportunities"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Pipeline Is Real — Florida Opportunities",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(11), Inches(0.4),
                "Specific, identifiable FL contracts Newport can pursue in the next 12 months:",
                font_size=15, font_color=MED_GRAY)

    # Detailed pipeline table with bid windows
    data = [
        ["Opportunity", "Agency/Level", "Est. Annual Value", "Bid Window", "Entry Point", "Priority"],
        ["Category ITBs (meat, dairy,\nfrozen, produce, dry goods)",
         "Polk County Schools\n(105K students) — Local",
         "$5-10M\n(across categories)",
         "Feb-May 2026\n(July start)",
         "Lowest responsive\nbid wins (FL law)",
         "HIGH"],
        ["Category ITBs",
         "Lee County Schools\n(95K students) — Local",
         "$4-8M\n(across categories)",
         "Feb-May 2026",
         "Lowest responsive bid",
         "HIGH"],
        ["Self-op kitchen food supply",
         "Pinellas County Jail\n(~3,100 inmates) — Local",
         "$2.5-3.5M",
         "Check county\nprocurement cycle",
         "Direct buyer —\nno FSMC middleman",
         "HIGH"],
        ["Self-op kitchen food supply",
         "Polk County Jail\n(~2,600 inmates) — Local",
         "$2.1-3.0M",
         "Check county\nprocurement cycle",
         "Direct buyer",
         "HIGH"],
        ["Quarterly subsistence\n(meat, dairy, produce, bakery)",
         "FCC Coleman Complex\n(~7,100 inmates) — Federal",
         "$6-10M/yr\n($1.5-2.5M/qtr)",
         "Quarterly:\nAug/Nov/Feb/May",
         "Small business\nset-aside",
         "HIGH"],
        ["Quarterly subsistence",
         "FCI Miami + FDC Miami\n(~2,100 inmates) — Federal",
         "$1.5-3M/yr",
         "Quarterly cycle",
         "Small business\nset-aside",
         "MEDIUM"],
        ["Vendor application",
         "GEO Group HQ\n(Boca Raton) — Contractor",
         "Facility-dependent",
         "Ongoing — apply\nanytime",
         "Approved vendor list",
         "MEDIUM"],
        ["Vendor application",
         "Trinity Services\n(Oldsmar, FL) — Contractor",
         "Facility-dependent",
         "Ongoing",
         "Approved vendor list",
         "MEDIUM"],
    ]
    add_table(slide, Inches(0.2), Inches(1.8), Inches(12.9),
              len(data), 6, data,
              col_widths=[Inches(2.5), Inches(2.5), Inches(1.7), Inches(1.8), Inches(2.2), Inches(1.2)],
              font_size=9)

    # Bottom note
    add_textbox(slide, Inches(0.8), Inches(6.8), Inches(11), Inches(0.5),
                "This is Florida only. The same scanning and analysis methodology scales to all 50 states. "
                "Nationwide simplified acquisitions ($15K-$350K) in food categories: 1,600-3,000 postings/year, $400M-$1.25B total value.",
                font_size=12, font_color=NAVY, bold=True)


def slide_08_decision_makers(prs):
    """Slide 8: Decision Makers + Internal Champions"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "We Know Who Buys the Food",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # Two-panel layout: Left = contacts, Right = champions concept

    # LEFT: Contact database summary
    add_textbox(slide, Inches(0.5), Inches(1.3), Inches(6), Inches(0.4),
                "76 FL Decision Makers Identified", font_size=18, font_color=NAVY, bold=True)

    contact_data = [
        ["Category", "Count", "Named", "Phone", "Email"],
        ["School District Food Directors", "25", "23 (92%)", "25", "10"],
        ["BOP Food Service Administrators", "9", "Call to ID", "9", "0"],
        ["VA Nutrition & Food Service", "7", "Call to ID", "7", "0"],
        ["Military Commissary Directors", "5", "4 (80%)", "5", "0"],
        ["County Jail Food Service", "10", "2 named", "10", "4"],
        ["Private Contractors", "8", "HQ contacts", "8", "0"],
        ["Named FSMC Regional Execs", "7", "7 (100%)", "7", "0"],
        ["BOP Wardens", "5", "5 (100%)", "5", "0"],
    ]
    add_table(slide, Inches(0.3), Inches(1.8), Inches(6.3),
              len(contact_data), 5, contact_data,
              col_widths=[Inches(2.5), Inches(0.8), Inches(1.2), Inches(0.9), Inches(0.9)],
              font_size=10)

    # Data cost note
    add_textbox(slide, Inches(0.3), Inches(5.6), Inches(6.3), Inches(0.7),
                "Current data: $0 cost (public records, agency websites, gov directories). "
                "Full email enrichment via Apollo.io: ~$0.10/contact. "
                "Verified direct dials: ~$5-10/contact via ZoomInfo/Lusha.",
                font_size=10, font_color=MED_GRAY)

    # RIGHT: Internal Champions concept
    add_textbox(slide, Inches(7), Inches(1.3), Inches(5.5), Inches(0.4),
                "Who Actually Decides (And Who Influences)",
                font_size=16, font_color=NAVY, bold=True)

    champion_data = [
        ["Role", "What They Do", "Why They Matter"],
        ["Contracting Officer\n(CO)",
         "Legal authority to\nsign contracts",
         "Final decision maker —\nbut relies on evaluators"],
        ["Food Service\nAdministrator",
         "Runs daily operations,\nknows what works/doesn't",
         "Writes the specs that\ndetermine who can bid"],
        ["Nutrition Director\n(schools)",
         "Sets menu requirements\nand product standards",
         "Their specs drive\npurchasing decisions"],
        ["Warden / Facility\nDirector",
         "Oversees entire facility\nincluding food service",
         "Can push for vendor\nchanges if food = problems"],
        ["End Users\n(staff, inmates, students)",
         "File complaints about\ncurrent vendor quality",
         "Dissatisfaction with\nincumbent = your opening"],
    ]
    add_table(slide, Inches(6.8), Inches(1.8), Inches(6.2),
              len(champion_data), 3, champion_data,
              col_widths=[Inches(1.6), Inches(2.2), Inches(2.4)],
              font_size=10)

    # Bottom callout
    add_callout_bar(slide, Inches(0.8), Inches(6.5), Inches(11.7), Inches(0.7),
                    '"Target the Food Service Administrators first — they write the specs that determine who wins. '
                    'Then the Contracting Officers who sign the check."',
                    font_size=14)


def slide_09_operating_model(prs):
    """Slide 9: The Operating Model"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "How This Actually Works — The Division of Labor",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    data = [
        ["Newport Does", "Still Mind Creative Does"],
        ["Assigns 1 salesperson (part-time on gov)", "Monitors SAM.gov, MFMP, DemandStar daily"],
        ["Attends conferences & facility visits", "Scores and prioritizes opportunities"],
        ["Builds relationships with decision makers", "Drafts Sources Sought responses"],
        ["Reviews and approves proposals", "Prepares RFQ/RFP response drafts"],
        ["Delivers the food", "Tracks deadlines, compliance, registrations"],
        ["Signs the contracts", "Documents past performance after delivery"],
        ["Collects the payments", "Provides weekly pipeline dashboard reports"],
    ]
    add_table(slide, Inches(1.5), Inches(1.5), Inches(10.3),
              len(data), 2, data,
              col_widths=[Inches(5.15), Inches(5.15)])

    # Callout
    add_callout_bar(slide, Inches(1.5), Inches(5.3), Inches(10.3), Inches(0.7),
                    '"Your team does what they\'re already good at — selling and delivering.\n'
                    'We handle the government procurement bureaucracy so they don\'t have to learn it."',
                    font_size=16)

    # What they DON'T need to do
    add_textbox(slide, Inches(0.8), Inches(6.3), Inches(11), Inches(0.3),
                "What Newport Does NOT Need to Do:", font_size=16, font_color=RED, bold=True)

    no_items = [
        "Learn government procurement rules",
        "Monitor bidding portals daily",
        "Write proposals from scratch",
        "Track compliance deadlines",
        "Hire government sales specialists",
    ]
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(6.7), Inches(12), Inches(0.4))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "   ".join([f"\u2717 {item}" for item in no_items])
    p.font.size = Pt(12)
    p.font.color.rgb = MED_GRAY
    p.font.name = "Calibri"


def slide_10_roadmap_quick_wins(prs):
    """Slide 10: Quick Wins Roadmap (Months 1-6)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Roadmap: Quick Wins (Months 1-6)",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # Phase 1: Foundation (Months 1-2)
    shape1 = slide.shapes.add_shape(1, Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.45))
    shape1.fill.solid()
    shape1.fill.fore_color.rgb = NAVY
    shape1.line.fill.background()
    add_textbox(slide, Inches(0.9), Inches(1.4), Inches(5), Inches(0.45),
                "FOUNDATION  |  Months 1-2", font_size=16, font_color=WHITE, bold=True)

    foundation_data = [
        ["Action", "Owner", "Timeline", "Milestone"],
        ["Register on SAM.gov", "Newport + SMC assists", "Week 1 (30-45 day process)", "Active SAM registration"],
        ["Register on MFMP + VendorLink + DemandStar", "SMC handles", "Week 1-2", "Receiving FL bid alerts"],
        ["Create government capability statement", "SMC drafts, Newport reviews", "Week 2-3", "Sales-ready document"],
        ["Submit GEO Group + Trinity vendor applications", "SMC drafts, Newport submits", "Week 2-3", "In vendor pipeline"],
        ["Schedule 5 school district meetings", "Newport salesperson", "Month 1-2", "First relationships started"],
        ["Begin Sources Sought monitoring", "SMC (ongoing)", "Day 1", "Shaping future solicitations"],
    ]
    add_table(slide, Inches(0.5), Inches(1.9), Inches(12.3),
              len(foundation_data), 4, foundation_data,
              col_widths=[Inches(3.5), Inches(2.5), Inches(3), Inches(3.3)],
              font_size=10)

    # Phase 2: First Wins (Months 3-6)
    shape2 = slide.shapes.add_shape(1, Inches(0.8), Inches(4.5), Inches(11.7), Inches(0.45))
    shape2.fill.solid()
    shape2.fill.fore_color.rgb = LIGHT_NAVY
    shape2.line.fill.background()
    add_textbox(slide, Inches(0.9), Inches(4.5), Inches(5), Inches(0.45),
                "FIRST WINS  |  Months 3-6", font_size=16, font_color=WHITE, bold=True)

    wins_data = [
        ["Action", "Owner", "Target", "Why It Matters"],
        ["Respond to 5+ school district ITBs", "SMC drafts, Newport reviews", "Win 1-2 category bids", "Lowest bid wins under FL law"],
        ["Submit 4+ BOP quarterly subsistence bids", "SMC prepares, Newport prices", "Win 1-2 quarterly contracts", "Constant cycle = fast feedback"],
        ["Contact Pinellas + Polk jail purchasing", "Newport salesperson", "Get on vendor list / bid", "Self-op = direct buyer (no FSMC)"],
        ["Attend ACFSA or FSNA conference", "Newport salesperson", "10+ new agency relationships", "Face time with decision makers"],
        ["Respond to 5+ Sources Sought notices", "SMC handles", "Shape future solicitations", "Get known before bids drop"],
        ["Complete 5+ deliveries (any size)", "Newport operations", "5 written references", "Building the credibility portfolio"],
    ]
    add_table(slide, Inches(0.5), Inches(5.0), Inches(12.3),
              len(wins_data), 4, wins_data,
              col_widths=[Inches(3.5), Inches(2.5), Inches(3), Inches(3.3)],
              font_size=10)

    add_textbox(slide, Inches(0.8), Inches(7.1), Inches(11), Inches(0.3),
                "Month 6 checkpoint: Are we winning bids? Building relationships? Getting known? If yes \u2192 scale. If not \u2192 adjust targeting, not abandon the channel.",
                font_size=12, font_color=NAVY, bold=True)


def slide_11_roadmap_long_term(prs):
    """Slide 11: Long-Term Build (Years 2-5)"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Long-Term Build: From Channel to Division",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(11), Inches(0.4),
                "Year 1 builds the foundation. Years 2-5 turn government into a full business division.",
                font_size=16, font_color=MED_GRAY)

    # Timeline progression
    data = [
        ["Phase", "Timeline", "Revenue Target", "Key Milestones", "What Changes"],
        ["Scale\nFlorida",
         "Year 2\n(Months 7-18)",
         "$5-8M/yr",
         "5-10 active contracts\n15+ past perf. refs\nFSMC vendor approvals",
         "Dedicated gov salesperson\nBid win rate: 25-35%\nRepeat BOP supplier"],
        ["Regional\nExpansion",
         "Year 3\n(Months 19-30)",
         "$10-15M/yr",
         "Expand to GA, AL, SC\nGPO membership (Foodbuy)\nUSDA AMS qualified bidder",
         "Government division with\nP&L, dedicated ops\nMulti-state presence"],
        ["National\nCapability",
         "Years 4-5",
         "$15-25M/yr",
         "National bid capability\n30+ agency relationships\nSubcontracting on large IDIQs",
         "Government = 20-30%\nof Newport revenue\nTransformed business profile"],
    ]
    add_table(slide, Inches(0.5), Inches(1.9), Inches(12.3),
              len(data), 5, data,
              col_widths=[Inches(1.5), Inches(1.5), Inches(1.5), Inches(3.8), Inches(3)],
              font_size=11)

    # The flywheel
    add_textbox(slide, Inches(0.8), Inches(4.7), Inches(11), Inches(0.4),
                "THE CREDIBILITY FLYWHEEL — Why Government Contracts Compound",
                font_size=18, font_color=NAVY, bold=True, alignment=PP_ALIGN.CENTER)

    flywheel_steps = [
        "Win small\ncontracts",
        "Deliver\nexcellently",
        "Earn past\nperformance refs",
        "Qualify for\nlarger bids",
        "Win bigger\ncontracts",
    ]
    step_width = Inches(2)
    start_x = Inches(0.8)
    for i, step in enumerate(flywheel_steps):
        x = start_x + i * (step_width + Inches(0.3))
        shape = slide.shapes.add_shape(1, x, Inches(5.2), step_width, Inches(0.9))
        shape.fill.solid()
        shape.fill.fore_color.rgb = NAVY if i % 2 == 0 else GOLD
        shape.line.fill.background()
        fc = WHITE if i % 2 == 0 else NAVY
        add_textbox(slide, x, Inches(5.25), step_width, Inches(0.85),
                    step, font_size=13, font_color=fc, bold=True,
                    alignment=PP_ALIGN.CENTER)
        if i < len(flywheel_steps) - 1:
            add_textbox(slide, x + step_width, Inches(5.4), Inches(0.3), Inches(0.5),
                        "\u27A1", font_size=20, font_color=NAVY, alignment=PP_ALIGN.CENTER)

    # Automation callout
    shape = slide.shapes.add_shape(1, Inches(0.8), Inches(6.4), Inches(11.7), Inches(0.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0xFE, 0xF9, 0xE7)
    shape.line.color.rgb = GOLD
    shape.line.width = Pt(2)
    add_textbox(slide, Inches(1.0), Inches(6.45), Inches(11.3), Inches(0.3),
                "SCALABILITY: The scanning and analysis tools built for this pilot are automated.",
                font_size=14, font_color=NAVY, bold=True)
    add_textbox(slide, Inches(1.0), Inches(6.75), Inches(11.3), Inches(0.35),
                "The same pipeline that finds FL opportunities today can scan all 50 states tomorrow. "
                "1,600-3,000 food procurement postings/year nationwide, $400M-$1.25B in contract value — all filterable, scorable, trackable.",
                font_size=11, font_color=DARK_GRAY)


def slide_12_success_metrics(prs):
    """Slide 12: Success Metrics"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Success Metrics — Credibility Is the Currency",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(11), Inches(0.6),
                "Year 1 is not about revenue. It's about winning contracts — even small ones — to build a track record. "
                "Every contract won is a receipt. Receipts compound into credibility. Credibility wins bigger contracts.",
                font_size=15, font_color=DARK_GRAY)

    data = [
        ["Metric", "Year 1 Target", "Year 2 Target", "Why It Matters"],
        ["Registrations Complete", "SAM, MFMP,\nDemandStar, VendorLink", "USDA AMS, GPO\nmembership", "Can't bid without them"],
        ["Bids Submitted", "10-17", "28-43", "Each bid builds competency\nand gets your name known"],
        ["Sources Sought Responses", "5-10", "10-15", "Gets Newport on agency radars\nbefore solicitations drop"],
        ["Contracts Won", "1-4\n(any size)", "5-13", "THE primary metric — each win\n= past performance currency"],
        ["Past Performance References", "3-5", "10-15", "This is what wins Year 2+ bids.\nThe real asset."],
        ["Agency Relationships", "10+", "25+", "Do procurement officers know\nNewport by name?"],
        ["Contractor Vendor Approvals", "1-2", "3-4", "GEO, Trinity, Aramark =\nvolume without bidding"],
        ["Revenue", "$1-2.5M", "$5-8M", "Important but secondary to\ntrack record in Year 1"],
    ]
    add_table(slide, Inches(0.3), Inches(2.1), Inches(12.7),
              len(data), 4, data,
              col_widths=[Inches(2.5), Inches(2.2), Inches(2.2), Inches(3.8)],
              font_size=10)

    # Callout
    shape = slide.shapes.add_shape(1, Inches(2), Inches(6.3), Inches(9), Inches(0.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0xFE, 0xF9, 0xE7)
    shape.line.color.rgb = GOLD
    shape.line.width = Pt(2)
    add_textbox(slide, Inches(2), Inches(6.35), Inches(9), Inches(0.75),
                '"A $10,000 micro-purchase contract that generates a stellar past performance reference\n'
                'is worth more than $100,000 in revenue without documentation."',
                font_size=14, font_color=NAVY, bold=True, alignment=PP_ALIGN.CENTER)


def slide_13_investment(prs):
    """Slide 13: Investment — Symbiotic Partnership Voice"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Investment — What It Takes to Get Started",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    add_textbox(slide, Inches(0.8), Inches(1.2), Inches(11), Inches(0.4),
                "Newport brings the infrastructure and relationships. Still Mind Creative brings the procurement expertise. "
                "Neither can do this alone — together, it works.",
                font_size=14, font_color=MED_GRAY)

    # LEFT: Newport costs
    add_textbox(slide, Inches(0.5), Inches(1.7), Inches(5.5), Inches(0.4),
                "Newport's Investment (Year 1)", font_size=18, font_color=NAVY, bold=True)

    data1 = [
        ["Item", "Cost", "When"],
        ["SAM.gov registration", "Free", "Month 1"],
        ["MFMP + VendorLink + DemandStar", "$0-$400", "Month 1"],
        ["Industry memberships (ACFSA, FSNA)", "$225", "Month 2"],
        ["Conference attendance (1 person, 2 events)", "$1,500-$3,000", "As scheduled"],
        ["Capability statement + sales materials", "$300-$500", "Month 1"],
        ["SQF/HACCP certification (if not held)", "$3,000-$8,000", "Month 1-2"],
        ["Salesperson time (8-10 hrs/week)", "Existing staff", "Ongoing"],
        ["TOTAL", "$5,000-$12,000", "Year 1"],
    ]
    add_table(slide, Inches(0.3), Inches(2.2), Inches(6),
              len(data1), 3, data1,
              col_widths=[Inches(3.3), Inches(1.3), Inches(1.4)],
              font_size=11)

    # RIGHT: SMC contribution
    add_textbox(slide, Inches(6.8), Inches(1.7), Inches(5.5), Inches(0.4),
                "Still Mind Creative's Contribution", font_size=18, font_color=NAVY, bold=True)

    data2 = [
        ["Service", "Frequency"],
        ["Opportunity monitoring (SAM, MFMP, DemandStar)", "Daily"],
        ["Pipeline scoring & prioritization", "Weekly"],
        ["Sources Sought responses", "3-5/month"],
        ["RFQ/RFP response drafts", "2-3/month"],
        ["Contact intelligence & research", "Ongoing"],
        ["Past performance documentation", "Per delivery"],
        ["Pipeline dashboard reports", "Weekly"],
        ["Registration & compliance tracking", "Ongoing"],
    ]
    add_table(slide, Inches(6.8), Inches(2.2), Inches(6),
              len(data2), 2, data2,
              col_widths=[Inches(4), Inches(2)],
              font_size=11)

    # ROI context
    shape = slide.shapes.add_shape(1, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()

    add_textbox(slide, Inches(1.0), Inches(6.05), Inches(11.3), Inches(0.35),
                "THE MATH", font_size=18, font_color=GOLD, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(1.0), Inches(6.4), Inches(11.3), Inches(0.75),
                "One school district category win: $2-10M/year.  One BOP quarterly contract: $200K-2.5M.  "
                "One county jail supply contract: $1-3.5M/year.\n"
                "A single win pays for the entire Year 1 investment many times over. "
                "The question isn't whether government contracts are worth pursuing — it's whether you want to start now or let someone else take them.",
                font_size=14, font_color=WHITE, alignment=PP_ALIGN.CENTER)


def slide_14_compounding(prs):
    """Slide 14: The Compounding Effect — plant the 'selling' seed."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Compounding Effect", font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # 3-year projection table
    data = [
        ["", "Year 1", "Year 2", "Year 3", "Year 5 (projected)"],
        ["Contracts Won", "1-4", "5-13", "12-22", "30-50+"],
        ["Revenue", "$1-2.5M", "$5-8M", "$10-15M", "$15-25M"],
        ["Gross Margin (15-20%)", "$150K-$500K", "$750K-$1.6M", "$1.5-$3M", "$2.5-$5M"],
        ["Past Performance Refs", "3-5", "10-15", "20-30", "50+"],
        ["Bid Win Rate", "10-20%", "25-35%", "35-50%", "40-55%"],
        ["States Active", "FL only", "FL + 1-2", "FL + 3-4", "Southeast region"],
        ["% of Newport Revenue", "1-3%", "5-10%", "10-15%", "20-30%"],
    ]
    add_table(slide, Inches(0.5), Inches(1.4), Inches(12.3),
              len(data), 5, data,
              col_widths=[Inches(2.5), Inches(2.2), Inches(2.2), Inches(2.2), Inches(2.2)],
              font_size=11)

    # Why it compounds
    add_textbox(slide, Inches(0.8), Inches(5.0), Inches(11), Inches(0.4),
                "WHY GOVERNMENT CONTRACTS COMPOUND (AND PRIVATE SECTOR DOESN'T)",
                font_size=16, font_color=NAVY, bold=True, alignment=PP_ALIGN.CENTER)

    compound_data = [
        ["Private Sector", "Government Contracting"],
        ["Each sale is independent — start from zero", "Each contract creates documented past performance that helps win the next one"],
        ["Relationships are informal", "Relationships are formalized in evaluation criteria"],
        ["Competitors can undercut you anytime", "Incumbents with strong past performance are hard to displace"],
        ["Revenue is revenue — it doesn't change what the business IS", "Government contracts transform the business's profile and value"],
    ]
    add_table(slide, Inches(1.5), Inches(5.5), Inches(10.3),
              len(compound_data), 2, compound_data,
              col_widths=[Inches(5.15), Inches(5.15)],
              font_size=11, header_bg=MED_GRAY)

    # The seed — subtle, not a headline
    add_textbox(slide, Inches(0.8), Inches(7.05), Inches(11.5), Inches(0.35),
                "A food distributor with government contracts, past performance documentation, and active agency relationships is a fundamentally different "
                "business than one without — in capability, in recurring revenue, and in what it's worth.",
                font_size=12, font_color=NAVY, bold=True, alignment=PP_ALIGN.CENTER)


def slide_15_risks(prs):
    """Slide 15: Risk Factors — Two types: operational + existential."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Risks — Both Sides of the Coin",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # LEFT: Operational risks (things that could go wrong on execution)
    add_textbox(slide, Inches(0.5), Inches(1.3), Inches(6), Inches(0.4),
                "Execution Risks (What Could Slow Us Down)",
                font_size=16, font_color=AMBER, bold=True)

    ops_data = [
        ["Risk", "Likelihood", "Mitigation"],
        ["Lose early bids", "High\n(expected)",
         "Start with micro + simplified acq.\nEvery loss teaches eval criteria"],
        ["Slow relationship\nbuilding", "Medium",
         "Conference attendance + consistent\nfollow-up + Sources Sought = radar"],
        ["SAM.gov registration\ndelays (30-45 days)", "Medium",
         "Start immediately. Pursue FL\nstate/local while waiting"],
        ["Strong incumbent on\ntarget contracts", "Medium",
         "Focus on set-asides, expiring\ncontracts, agencies with complaints"],
        ["Certification gaps\n(SQF/HACCP)", "Low-Med",
         "Identify requirements early.\nBudget for cert if not held"],
        ["Salesperson bandwidth", "Medium",
         "SMC handles all admin = salesperson\nfocuses 100% on relationships"],
    ]
    add_table(slide, Inches(0.3), Inches(1.8), Inches(6.2),
              len(ops_data), 3, ops_data,
              col_widths=[Inches(1.8), Inches(1), Inches(3.4)],
              font_size=10)

    # RIGHT: Strategic/existential risk — decision tree framing
    add_textbox(slide, Inches(6.8), Inches(1.3), Inches(5.5), Inches(0.4),
                "Strategic Risk (The Bigger Question)",
                font_size=16, font_color=NAVY, bold=True)

    # Decision tree as a table
    tree_data = [
        ["If Newport...", "Then..."],
        ["Enters government contracting\nand it takes longer than expected",
         "You've built registrations, relationships,\nand capabilities that compound.\nThe investment was modest."],
        ["Enters government contracting\nand wins early contracts",
         "You've opened a new channel that\ncould reach $10-15M/yr by Year 3.\nThe business is fundamentally stronger."],
        ["Does nothing",
         "The fraud crackdown window closes.\nCompetitors register first.\nThe opportunity doesn't wait."],
    ]
    add_table(slide, Inches(6.8), Inches(1.8), Inches(6.2),
              len(tree_data), 2, tree_data,
              col_widths=[Inches(3), Inches(3.2)],
              font_size=11, header_bg=NAVY)

    # Bottom framing
    add_textbox(slide, Inches(6.8), Inches(4.7), Inches(5.5), Inches(0.8),
                "The execution risks are real and manageable — "
                "they're the normal cost of entering a new market. We mitigate "
                "them by starting small, learning fast, and adjusting.\n\n"
                "The strategic risk is the one that matters: this window won't stay open forever.",
                font_size=12, font_color=DARK_GRAY)

    # Full-width callout at bottom
    add_callout_bar(slide, Inches(0.8), Inches(6.2), Inches(11.7), Inches(1),
                    '"Newport has been doing the hard part for 30 years — building real infrastructure.\n'
                    'The only question is whether to put that infrastructure to work in a market\n'
                    'that desperately needs what you already have."',
                    font_size=14)


def slide_16_the_ask(prs):
    """Slide 16: The Ask — Compelling Close"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_textbox(slide, Inches(1.5), Inches(0.3), Inches(10), Inches(0.7),
                "What Happens Next", font_size=40, font_color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_divider(slide, Inches(4), Inches(1.0), Inches(5), color=GOLD)

    # The first 30 days — action table
    add_textbox(slide, Inches(0.8), Inches(1.2), Inches(11), Inches(0.4),
                "The First 30 Days:", font_size=22, font_color=GOLD, bold=True,
                alignment=PP_ALIGN.CENTER)

    data = [
        ["Week", "Action", "Owner", "Result"],
        ["Week 1", "Start SAM.gov registration\nRegister on MFMP + VendorLink",
         "Newport + SMC", "In the system — clock starts on 30-45 day SAM approval"],
        ["Week 1-2", "Submit vendor applications to\nGEO Group + Trinity + Aramark",
         "SMC drafts,\nNewport submits", "In the pipeline for private contractor supply"],
        ["Week 2-3", "Create capability statement\nand government sales materials",
         "SMC creates,\nNewport reviews", "Professional materials ready for agency meetings"],
        ["Week 2-4", "Schedule first 5 FL school\ndistrict procurement meetings",
         "Newport\nsalesperson", "Face-to-face relationships with decision makers"],
        ["Ongoing", "Begin daily opportunity monitoring\n+ Sources Sought responses",
         "Still Mind\nCreative", "Pipeline building starts immediately"],
    ]
    add_table(slide, Inches(0.5), Inches(1.7), Inches(12.3),
              len(data), 4, data,
              col_widths=[Inches(1), Inches(3.5), Inches(2), Inches(4.8)],
              header_bg=GOLD, header_fg=NAVY, font_size=11)

    # What Newport commits
    add_textbox(slide, Inches(0.8), Inches(5.0), Inches(5.5), Inches(0.4),
                "What Newport Commits:", font_size=18, font_color=GOLD, bold=True)
    commit_items = [
        "Authorize ~$5-12K for registrations + materials",
        "Assign 1 salesperson (8-10 hrs/week)",
        "Attend 1-2 industry conferences in Year 1",
        "12-month pilot commitment",
    ]
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(5.4), Inches(5.5), Inches(1.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(commit_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"\u2713  {item}"
        p.font.size = Pt(14)
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"
        p.space_after = Pt(6)

    # What SMC commits
    add_textbox(slide, Inches(6.8), Inches(5.0), Inches(5.5), Inches(0.4),
                "What Still Mind Creative Commits:", font_size=18, font_color=GOLD, bold=True)
    smc_items = [
        "Daily opportunity monitoring across all portals",
        "All proposal and response drafting",
        "Pipeline scoring, tracking, and reporting",
        "Full procurement compliance management",
    ]
    txBox2 = slide.shapes.add_textbox(Inches(6.8), Inches(5.4), Inches(5.5), Inches(1.5))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    for i, item in enumerate(smc_items):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.text = f"\u2713  {item}"
        p.font.size = Pt(14)
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"
        p.space_after = Pt(6)

    # Closing line
    add_textbox(slide, Inches(0.8), Inches(7.0), Inches(11.5), Inches(0.4),
                "Still Mind Creative LLC  |  " + datetime.now().strftime("%B %Y"),
                font_size=11, font_color=MED_GRAY, alignment=PP_ALIGN.CENTER)


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    print("Building pitchbook v2 slides...")
    slides = [
        ("Slide 1: Cover", slide_01_cover),
        ("Slide 2: Executive Summary", slide_02_exec_summary),
        ("Slide 3: Market Opportunity (Realistic FL)", slide_03_market_opportunity),
        ("Slide 4: Why Now — Fraud Crisis", slide_04_fraud_crisis),
        ("Slide 5: Competitive Moat", slide_05_competitive_moat),
        ("Slide 6: Competitive Landscape (Fight Here)", slide_06_competitive_landscape),
        ("Slide 7: Pipeline (FL Specifics)", slide_07_pipeline),
        ("Slide 8: Decision Makers + Champions", slide_08_decision_makers),
        ("Slide 9: Operating Model", slide_09_operating_model),
        ("Slide 10: Quick Wins Roadmap (Months 1-6)", slide_10_roadmap_quick_wins),
        ("Slide 11: Long-Term Build (Years 2-5)", slide_11_roadmap_long_term),
        ("Slide 12: Success Metrics", slide_12_success_metrics),
        ("Slide 13: Investment", slide_13_investment),
        ("Slide 14: The Compounding Effect", slide_14_compounding),
        ("Slide 15: Risk Factors (Both Sides)", slide_15_risks),
        ("Slide 16: The Ask", slide_16_the_ask),
    ]

    for name, builder in slides:
        print(f"  {name}")
        builder(prs)

    output_path = OUTPUT_DIR / f"newport_pitchbook_{datetime.now().strftime('%Y%m%d_%H%M')}.pptx"
    prs.save(str(output_path))
    print(f"\nPitchbook saved to: {output_path}")
    print(f"  {len(prs.slides)} slides")


if __name__ == "__main__":
    main()
