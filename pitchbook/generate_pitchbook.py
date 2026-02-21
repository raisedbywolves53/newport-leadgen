"""Generate Newport Wholesalers Government Contract Entry Pitchbook.

Creates a 15-slide professional PowerPoint presentation targeting
Newport leadership to secure buy-in for government contract entry,
with Still Mind Creative as the operational partner.

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
                 value_color=NAVY, value_size=36):
    """Add a KPI card with large value and small label."""
    from pptx.oxml.ns import qn

    # Card background
    shape = slide.shapes.add_shape(
        1, left, top, width, height  # rectangle
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = GOLD
    shape.line.width = Pt(2)
    # Round corners
    shape.shadow.inherit = False

    # Value text
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

    # Label text
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
              col_widths=None, header_bg=NAVY, header_fg=WHITE):
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
                paragraph.font.size = Pt(12)
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
    shape = slide.shapes.add_shape(
        1, left, top, width, Pt(3)  # thin rectangle
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


# ========== SLIDE BUILDERS ==========

def slide_01_cover(prs):
    """Slide 1: Cover"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
    set_slide_bg(slide, NAVY)

    # Main title
    add_textbox(slide, Inches(1.5), Inches(1.5), Inches(10), Inches(1.5),
                "Newport Wholesalers", font_size=48, font_color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)

    # Subtitle
    add_textbox(slide, Inches(1.5), Inches(3.0), Inches(10), Inches(1),
                "Government Contract Entry Strategy", font_size=32, font_color=GOLD,
                bold=False, alignment=PP_ALIGN.CENTER)

    # Divider
    add_divider(slide, Inches(4), Inches(4.2), Inches(5))

    # Prepared by
    add_textbox(slide, Inches(1.5), Inches(4.6), Inches(10), Inches(0.5),
                "Prepared by Still Mind Creative LLC", font_size=18,
                font_color=WHITE, alignment=PP_ALIGN.CENTER)

    # Date
    add_textbox(slide, Inches(1.5), Inches(5.2), Inches(10), Inches(0.5),
                datetime.now().strftime("%B %Y"), font_size=16,
                font_color=MED_GRAY, alignment=PP_ALIGN.CENTER)

    # Confidential
    add_textbox(slide, Inches(1.5), Inches(6.5), Inches(10), Inches(0.4),
                "CONFIDENTIAL", font_size=12, font_color=MED_GRAY,
                alignment=PP_ALIGN.CENTER)


def slide_02_exec_summary(prs):
    """Slide 2: Executive Summary"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Executive Summary", font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    items = [
        "The Opportunity: $500M-$2B serviceable government food market in Florida alone",
        "The Timing: Historic fraud crackdown creates a \"flight to quality\" — agencies want verifiable, legitimate American vendors",
        "Newport's Moat: 25+ years of continuous Florida operations, real infrastructure, American ownership — exactly what scared procurement officers need",
        "The Model: Newport's sales team builds relationships and closes deals. Still Mind Creative handles the government procurement bureaucracy.",
        "The Currency: Credibility. Year 1 is about winning contracts — even small ones — to build a track record that compounds into larger wins",
        "The Ask: 12-month pilot commitment. One salesperson assigned part-time. ~$8K-$12K in registrations and materials. Ongoing operational support from Still Mind Creative.",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(1.5), Inches(11.5), Inches(5.5),
                    items, font_size=17, spacing=Pt(12))


def slide_03_market_opportunity(prs):
    """Slide 3: The Market Opportunity"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Market Opportunity", font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # KPI cards row
    cards = [
        ("$35-50B", "Total US Gov Food\nMarket (Annual)"),
        ("$1.47B", "Federal Food Spend\nFY2025 (Tracked)"),
        ("$500M-2B", "FL Serviceable\nMarket (Annual)"),
        ("+15%", "Federal Spend Growth\n(2-Year Trend)"),
    ]
    card_width = Inches(2.7)
    card_gap = Inches(0.3)
    start_x = Inches(0.8)
    for i, (val, label) in enumerate(cards):
        x = start_x + i * (card_width + card_gap)
        add_kpi_card(slide, x, Inches(1.6), card_width, Inches(1.5), val, label)

    # Market breakdown
    add_textbox(slide, Inches(0.8), Inches(3.5), Inches(11), Inches(0.5),
                "Where the Money Is — Federal Food Spending by Agency (FY2025)",
                font_size=18, font_color=NAVY, bold=True)

    data = [
        ["Agency", "FY2025 Spend", "% of Total", "2-Year Growth", "Newport Entry Path"],
        ["Dept of Defense", "$1.19B", "81%", "+10%", "Prime vendor relationship (Sysco/US Foods)"],
        ["Dept of Agriculture (USDA)", "$117M", "8%", "+77%", "USDA AMS Qualified Bidders List"],
        ["Homeland Security", "$90M", "6%", "+23%", "ICE detention facility supply"],
        ["Dept of Justice (BOP)", "$20M", "1.3%", "+19%", "Direct BOP institution supply"],
        ["Dept of Veterans Affairs", "$9M", "0.6%", "-2%", "VA medical center food service"],
    ]
    add_table(slide, Inches(0.8), Inches(4.1), Inches(11.7),
              len(data), 5, data,
              col_widths=[Inches(3), Inches(1.5), Inches(1.2), Inches(1.5), Inches(4.5)])

    # Note
    add_textbox(slide, Inches(0.8), Inches(6.7), Inches(11), Inches(0.6),
                "Note: Federal data only. State + local government food spending adds $25-40B+ annually (school districts, county jails, state prisons).",
                font_size=13, font_color=MED_GRAY)


def slide_04_fraud_crisis(prs):
    """Slide 4: Why Now — The Fraud Crisis"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Why Now — The Fraud Crisis Creates Opportunity",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # Fraud KPIs in red
    fraud_cards = [
        ("$6.8B", "False Claims Act\nRecoveries (FY2025)"),
        ("1,091", "8(a) Firms Suspended\n(25% of program)"),
        ("$250M+", "Feeding Our Future\nFraud (MN)"),
        ("10,000+", "DOGE Contracts\nTerminated"),
    ]
    card_width = Inches(2.7)
    card_gap = Inches(0.3)
    start_x = Inches(0.8)
    for i, (val, label) in enumerate(fraud_cards):
        x = start_x + i * (card_width + card_gap)
        add_kpi_card(slide, x, Inches(1.6), card_width, Inches(1.5),
                     val, label, value_color=RED, value_size=32)

    add_textbox(slide, Inches(0.8), Inches(3.5), Inches(11), Inches(0.5),
                "What This Means for Newport:",
                font_size=20, font_color=NAVY, bold=True)

    items = [
        "Government procurement is in crisis mode — agencies are desperate for verifiable, legitimate vendors",
        "The crackdown has created vendor gaps — suspended companies leave contracts that need new suppliers",
        "Procurement officers are scared of bad press — they want vendors with provable track records",
        "Small Business set-asides under increased scrutiny — legitimate small businesses (like Newport) gain advantage",
        "The fraud environment makes Newport's 25-year American history a competitive weapon, not just a resume line",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(4.1), Inches(11.5), Inches(3),
                    items, font_size=16, spacing=Pt(10))

    # Bottom callout
    shape = slide.shapes.add_shape(1, Inches(1.5), Inches(6.5), Inches(10), Inches(0.7))
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()
    add_textbox(slide, Inches(1.5), Inches(6.5), Inches(10), Inches(0.7),
                '"Newport doesn\'t need to pretend to be something it\'s not. It IS what the government is looking for."',
                font_size=16, font_color=GOLD, bold=True, alignment=PP_ALIGN.CENTER)


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

    # Two-column layout
    left_items = [
        "25+ Years of Continuous Florida Operations",
        "Real Warehouses (address verifiable)",
        "Real Truck Fleet (branded, inspectable)",
        "American-Owned, American Employees",
        "American Tax Returns (25+ years)",
        "Established Banking Relationships",
    ]
    right_items = [
        "Existing Supplier Relationships & Product Breadth",
        "Cold Chain Infrastructure (critical for food)",
        "Florida Home State Advantage (local preference scoring)",
        "Small Business Qualification (NAICS 424410, $200M threshold)",
        "Sales Team That Knows How to Build Relationships",
        "Clean Financial History (auditable, provable)",
    ]

    add_bullet_list(slide, Inches(0.8), Inches(2.1), Inches(5.5), Inches(3.5),
                    left_items, font_size=15, bullet_char="\u2713", spacing=Pt(10))
    add_bullet_list(slide, Inches(6.8), Inches(2.1), Inches(5.5), Inches(3.5),
                    right_items, font_size=15, bullet_char="\u2713", spacing=Pt(10))

    # Set-aside callout
    shape = slide.shapes.add_shape(1, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.5))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0xFE, 0xF9, 0xE7)
    shape.line.color.rgb = GOLD
    shape.line.width = Pt(2)

    add_textbox(slide, Inches(1.0), Inches(5.6), Inches(11.3), Inches(0.5),
                "KEY ADVANTAGE: Small Business Set-Asides",
                font_size=18, font_color=NAVY, bold=True)
    add_textbox(slide, Inches(1.0), Inches(6.1), Inches(11.3), Inches(0.7),
                "~23% of federal contracts are set aside for small businesses. Newport qualifies under NAICS 424410 ($200M size standard). "
                "This locks out Sysco, US Foods, Aramark, and every other billion-dollar distributor. They literally cannot bid on these contracts.",
                font_size=14, font_color=DARK_GRAY)


def slide_06_competitive_landscape(prs):
    """Slide 6: The Competitive Landscape"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Competitive Landscape — Where to Fight",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # Don't fight here
    add_textbox(slide, Inches(0.8), Inches(1.5), Inches(5.5), Inches(0.4),
                "DON'T FIGHT HERE (YET)", font_size=18, font_color=RED, bold=True)
    dont_items = [
        "DLA Prime Vendor mega-contracts (Sysco/US Foods stranglehold)",
        "National FSMC contracts (Aramark, Compass, Sodexo)",
        "Large multi-state school nutrition cooperatives",
        "Any contract requiring 5+ years government past performance",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(2.0), Inches(5.5), Inches(2.5),
                    dont_items, font_size=14, font_color=MED_GRAY,
                    bullet_char="\u2717", spacing=Pt(6))

    # Fight here
    add_textbox(slide, Inches(6.8), Inches(1.5), Inches(5.5), Inches(0.4),
                "FIGHT HERE (NOW)", font_size=18, font_color=GREEN, bold=True)
    fight_items = [
        "Florida school district food supply (25 districts, local preference)",
        "FL county jail self-operated kitchens (direct buyer!)",
        "BOP institution supply (8 FL federal prisons)",
        "VA medical center food service (7 FL VA hospitals)",
        "Micro-purchases under $10K (no competition required)",
        "Small business set-aside contracts",
        "Sources Sought responses (shape future solicitations)",
        "FEMA emergency food staging (FL hurricane season)",
    ]
    add_bullet_list(slide, Inches(6.8), Inches(2.0), Inches(5.5), Inches(3.5),
                    fight_items, font_size=14, font_color=DARK_GRAY,
                    bullet_char="\u2713", spacing=Pt(6))

    # Dual path
    add_textbox(slide, Inches(0.8), Inches(5.0), Inches(11), Inches(0.4),
                "THE DUAL-PATH STRATEGY", font_size=18, font_color=NAVY, bold=True)

    data = [
        ["Path", "Target", "How It Works", "Timeline"],
        ["Direct Government", "School districts, BOP, VA, county jails",
         "Win contracts directly through bidding", "Month 1+"],
        ["Private Contractor Supply", "GEO Group, CoreCivic, Trinity, Aramark, Compass",
         "Become approved vendor — they issue their own RFPs for food supply",
         "Month 2+"],
    ]
    add_table(slide, Inches(0.8), Inches(5.5), Inches(11.7),
              3, 4, data,
              col_widths=[Inches(2.2), Inches(3.5), Inches(4), Inches(2)])

    add_textbox(slide, Inches(0.8), Inches(6.9), Inches(11), Inches(0.4),
                "GEO Group HQ is in Boca Raton. Trinity HQ is in Oldsmar. Both are Florida companies — local meetings are possible this month.",
                font_size=13, font_color=GOLD, bold=True)


def slide_07_pipeline(prs):
    """Slide 7: The Pipeline Is Real"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Pipeline Is Real", font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    add_textbox(slide, Inches(0.8), Inches(1.4), Inches(11), Inches(0.5),
                "We identified 69+ Florida decision makers and 10 sample opportunities — and this is just the beginning.",
                font_size=16, font_color=MED_GRAY)

    data = [
        ["Opportunity", "Agency", "Level", "Est. Value", "Type", "Priority"],
        ["Food Supply — FCI Coleman Complex", "Bureau of Prisons", "Federal", "$250,000", "RFQ", "HIGH"],
        ["School Nutrition Supply — Polk County", "Polk County Schools", "Local", "$180,000", "IFB", "HIGH"],
        ["Jail Food Supply — Hillsborough County", "HCSO", "Local", "$320,000", "RFP", "HIGH"],
        ["Fresh Produce — VA Tampa", "Dept of Veterans Affairs", "Federal", "$120,000", "RFQ", "HIGH"],
        ["Emergency Food Staging — FEMA", "FEMA Region IV", "Federal", "$500,000", "Pre-Sol", "MEDIUM"],
        ["Dairy Products — NAS Jacksonville", "Defense Logistics Agency", "Federal", "$200,000", "Sources Sought", "MEDIUM"],
        ["Snack & Beverage — Seminole Schools", "Seminole County Schools", "Local", "$60,000", "RFQ", "MEDIUM"],
        ["Bakery Products — FL DOC", "Florida DOC", "State", "$150,000", "RFQ", "LOW"],
    ]
    add_table(slide, Inches(0.5), Inches(2.0), Inches(12.3),
              len(data), 6, data,
              col_widths=[Inches(3.5), Inches(2.5), Inches(1.2), Inches(1.5), Inches(1.5), Inches(1.5)])

    # Pipeline KPIs
    kpi_cards = [
        ("10", "Active\nOpportunities"),
        ("$1.9M+", "Total Pipeline\nValue"),
        ("5", "Expiring Contracts\nTracked"),
        ("3", "Sources Sought\nto Respond"),
    ]
    card_w = Inches(2.7)
    for i, (v, l) in enumerate(kpi_cards):
        x = Inches(0.8) + i * (card_w + Inches(0.3))
        add_kpi_card(slide, x, Inches(5.8), card_w, Inches(1.3), v, l, value_size=28)


def slide_08_decision_makers(prs):
    """Slide 8: Decision Makers Are Identifiable"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Decision Makers Are Identifiable",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # Contact summary KPIs
    contact_cards = [
        ("69", "Contacts\nIdentified"),
        ("35", "Named\nIndividuals"),
        ("61", "With Phone\nNumbers"),
        ("$0", "Data\nCost"),
    ]
    card_w = Inches(2.5)
    for i, (v, l) in enumerate(contact_cards):
        x = Inches(0.8) + i * (card_w + Inches(0.3))
        add_kpi_card(slide, x, Inches(1.5), card_w, Inches(1.2), v, l, value_size=32)

    # Contact breakdown table
    data = [
        ["Contact Category", "Count", "Named", "Phone", "Email", "Priority"],
        ["FL School District Food Directors (Top 25)", "25", "23 (92%)", "25 (100%)", "10 (40%)", "Tier 1-3"],
        ["FL BOP Food Service Administrators", "9", "Call", "9 (100%)", "0", "Tier 1"],
        ["FL VA Nutrition & Food Service", "7", "Call", "7 (100%)", "0", "Tier 2"],
        ["FL Military Commissary Directors", "5", "4 (80%)", "5 (100%)", "0", "Tier 2"],
        ["FL County Jail Food Service (Top 10)", "10", "2", "10 (100%)", "4", "Tier 1-2"],
        ["Private Contractors (GEO, CoreCivic, Trinity...)", "8", "Research", "8 (100%)", "0", "Tier 1"],
        ["BOP Wardens (Named)", "5", "5 (100%)", "5 (100%)", "0", "Tier 3"],
    ]
    add_table(slide, Inches(0.5), Inches(3.0), Inches(12.3),
              len(data), 6, data,
              col_widths=[Inches(4.5), Inches(1.2), Inches(1.5), Inches(1.5), Inches(1.2), Inches(1.5)])

    # Callout
    add_textbox(slide, Inches(0.8), Inches(6.5), Inches(11), Inches(0.7),
                '"We know who buys the food. We know their phone numbers. '
                'Your salesperson needs to pick up the phone and start building relationships."',
                font_size=16, font_color=NAVY, bold=True, alignment=PP_ALIGN.CENTER)


def slide_09_operating_model(prs):
    """Slide 9: How This Actually Works"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Operating Model — How This Actually Works",
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
    add_table(slide, Inches(1.5), Inches(1.6), Inches(10.3),
              len(data), 2, data,
              col_widths=[Inches(5.15), Inches(5.15)])

    # Callout
    shape = slide.shapes.add_shape(1, Inches(1.5), Inches(5.5), Inches(10.3), Inches(0.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()
    add_textbox(slide, Inches(1.5), Inches(5.5), Inches(10.3), Inches(0.8),
                '"Your team does what they\'re good at — selling and delivering.\n'
                'We handle the government procurement bureaucracy."',
                font_size=18, font_color=GOLD, bold=True, alignment=PP_ALIGN.CENTER)

    # What they don't need to do
    add_textbox(slide, Inches(0.8), Inches(6.6), Inches(11), Inches(0.4),
                "What Newport Does NOT Need to Do:",
                font_size=16, font_color=RED, bold=True)
    no_items = [
        "Learn government procurement rules",
        "Monitor bidding portals daily",
        "Write proposals from scratch",
        "Track compliance deadlines",
        "Hire government sales specialists",
    ]
    # Horizontal layout
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(12), Inches(0.4))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = "   ".join([f"\u2717 {item}" for item in no_items])
    p.font.size = Pt(12)
    p.font.color.rgb = MED_GRAY
    p.font.name = "Calibri"


def slide_10_roadmap(prs):
    """Slide 10: Year 1 Roadmap"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Year 1 Roadmap — Track Record First",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # Phase bars
    phases = [
        ("FOUNDATION", "Months 1-2", NAVY,
         ["SAM.gov + MFMP registration live", "Capability statement created",
          "5 school district meetings scheduled", "Sources Sought monitoring active",
          "Contractor vendor applications submitted (GEO, Trinity, Aramark)"]),
        ("FIRST WINS", "Months 3-6", LIGHT_NAVY,
         ["5+ deliveries completed", "3+ written references obtained",
          "ACFSA / FSNA conference attended", "10+ solicitations responded to",
          "First micro-purchase contracts won"]),
        ("SCALE", "Months 7-12", GOLD,
         ["10+ contracts won (building credibility portfolio)", "$100K-$500K cumulative revenue",
          "FSMC approved vendor status (Aramark, Compass)",
          "GPO membership (Foodbuy)", "Past performance portfolio = 5+ verified references"]),
    ]

    y = Inches(1.5)
    for phase_name, timeline, color, items in phases:
        # Phase header bar
        shape = slide.shapes.add_shape(1, Inches(0.8), y, Inches(11.7), Inches(0.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        add_textbox(slide, Inches(0.9), y, Inches(3), Inches(0.5),
                    f"{phase_name}  |  {timeline}", font_size=16,
                    font_color=WHITE if color != GOLD else NAVY, bold=True)

        y += Inches(0.55)
        add_bullet_list(slide, Inches(1.2), y, Inches(11), Inches(1.3),
                        items, font_size=13, spacing=Pt(4))
        y += Inches(1.2)

    # Key insight
    add_textbox(slide, Inches(0.8), Inches(6.8), Inches(11), Inches(0.5),
                "Key Insight: Year 1 success = contracts won (credibility), not revenue. The track record enables Year 2+ growth.",
                font_size=15, font_color=NAVY, bold=True)


def slide_11_success_metrics(prs):
    """Slide 11: Success Metrics — Credibility First"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Success Metrics — Credibility Is the Currency",
                font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    add_textbox(slide, Inches(0.8), Inches(1.4), Inches(11), Inches(0.8),
                "Year 1 is not about revenue. It's about winning as many contracts as possible — even small ones — "
                "to build a track record that proves Newport is trustworthy, reliable, and capable. "
                "Every contract won is a receipt. Receipts compound into credibility. Credibility wins bigger contracts.",
                font_size=16, font_color=DARK_GRAY)

    data = [
        ["Metric", "Year 1 Target", "Why It Matters"],
        ["Registrations Complete", "SAM.gov, MFMP, DemandStar", "Can't bid without them"],
        ["Solicitations Responded To", "15+", "Each response builds competency"],
        ["Sources Sought Responses", "10+", "Gets Newport on agency radars before bids drop"],
        ["Contracts Won", "3-5 (any size)", "THE primary metric — each win = credibility"],
        ["Past Performance References", "5+", "The real asset — this is what wins Year 2 bids"],
        ["Agency Relationships", "10+", "Do procurement officers know Newport by name?"],
        ["Contractor Vendor Approvals", "2-3", "GEO, Trinity, Aramark = volume without bidding"],
        ["Revenue", "$100K-$500K", "Secondary to track record — nice to have, not the goal"],
    ]
    add_table(slide, Inches(0.5), Inches(2.5), Inches(12.3),
              len(data), 3, data,
              col_widths=[Inches(3.5), Inches(3.5), Inches(5.3)])

    # Callout
    shape = slide.shapes.add_shape(1, Inches(2), Inches(6.3), Inches(9), Inches(0.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0xFE, 0xF9, 0xE7)
    shape.line.color.rgb = GOLD
    shape.line.width = Pt(2)
    add_textbox(slide, Inches(2), Inches(6.35), Inches(9), Inches(0.75),
                '"A $10,000 micro-purchase contract that generates a stellar past performance reference\n'
                'is worth more than $100,000 in revenue without documentation."',
                font_size=15, font_color=NAVY, bold=True, alignment=PP_ALIGN.CENTER)


def slide_12_investment(prs):
    """Slide 12: Investment Required"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Investment Required", font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    # Newport direct costs
    add_textbox(slide, Inches(0.8), Inches(1.4), Inches(5), Inches(0.4),
                "Newport Direct Costs (Year 1)", font_size=20, font_color=NAVY, bold=True)

    data1 = [
        ["Item", "Cost", "When"],
        ["SAM.gov registration", "Free", "Month 1"],
        ["MyFloridaMarketPlace (MFMP)", "Free-$25", "Month 1"],
        ["DemandStar subscription", "$0-$400", "Month 1"],
        ["Industry memberships (ACFSA, FSNA)", "$225", "Month 2"],
        ["Conference attendance (1 person, 2 events)", "$1,500-$3,000", "As scheduled"],
        ["Capability statement & sales materials", "$300-$500", "Month 1"],
        ["SQF Level 2 certification (if not held)", "$3,000-$8,000", "Month 1-2"],
        ["TOTAL NEWPORT COSTS", "$5,000-$12,000", "Year 1"],
    ]
    add_table(slide, Inches(0.5), Inches(1.9), Inches(5.8),
              len(data1), 3, data1,
              col_widths=[Inches(3.3), Inches(1.3), Inches(1.2)])

    # Still Mind services
    add_textbox(slide, Inches(6.8), Inches(1.4), Inches(5), Inches(0.4),
                "Still Mind Creative Services", font_size=20, font_color=NAVY, bold=True)

    data2 = [
        ["Service", "Included"],
        ["Daily opportunity monitoring", "Yes"],
        ["Pipeline scoring & prioritization", "Yes"],
        ["Sources Sought responses (3/mo)", "Yes"],
        ["RFQ/RFP response drafts (2/mo)", "Yes"],
        ["Contact intelligence & research", "Yes"],
        ["Past performance documentation", "Yes"],
        ["Weekly pipeline reports", "Yes"],
        ["Registration assistance", "Yes"],
    ]
    add_table(slide, Inches(6.8), Inches(1.9), Inches(5.8),
              len(data2), 2, data2,
              col_widths=[Inches(3.8), Inches(2)])

    # ROI callout
    shape = slide.shapes.add_shape(1, Inches(0.8), Inches(6.0), Inches(11.7), Inches(1.2))
    shape.fill.solid()
    shape.fill.fore_color.rgb = NAVY
    shape.line.fill.background()

    add_textbox(slide, Inches(1.0), Inches(6.05), Inches(11.3), Inches(0.4),
                "ROI CONTEXT", font_size=18, font_color=GOLD, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_textbox(slide, Inches(1.0), Inches(6.45), Inches(11.3), Inches(0.7),
                "A single school district food supply contract: $100K-$500K/year.  "
                "A single BOP institution supply contract: $200K-$1M/year.  "
                "One government contract win pays for the entire Year 1 investment multiple times over.",
                font_size=15, font_color=WHITE, alignment=PP_ALIGN.CENTER)


def slide_13_returns(prs):
    """Slide 13: Expected Returns — The Compounding Effect"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Compounding Effect", font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    add_textbox(slide, Inches(0.8), Inches(1.3), Inches(11), Inches(0.5),
                "Government past performance creates a flywheel. Each win makes the next bid stronger.",
                font_size=16, font_color=MED_GRAY)

    data = [
        ["", "Year 1", "Year 2", "Year 3"],
        ["Contracts Won", "3-5", "8-15", "15-30"],
        ["Revenue", "$100K-$500K", "$500K-$2M", "$2M-$5M"],
        ["Gross Margin (15-20%)", "$15K-$100K", "$75K-$400K", "$300K-$1M"],
        ["Past Performance Refs", "5+", "15+", "30+"],
        ["Agency Relationships", "10+", "25+", "50+"],
        ["Bid Win Rate", "10-20%", "25-35%", "35-50%"],
    ]
    add_table(slide, Inches(1.5), Inches(2.0), Inches(10),
              len(data), 4, data,
              col_widths=[Inches(3), Inches(2.3), Inches(2.3), Inches(2.4)])

    # Flywheel diagram (text-based)
    add_textbox(slide, Inches(0.8), Inches(5.0), Inches(11), Inches(0.4),
                "THE CREDIBILITY FLYWHEEL", font_size=20, font_color=NAVY, bold=True,
                alignment=PP_ALIGN.CENTER)

    flywheel_steps = [
        "Win small\ncontracts",
        "Document\nperformance",
        "Earn past\nperformance refs",
        "Qualify for\nlarger bids",
        "Win bigger\ncontracts",
    ]
    arrow = " \u2192 "
    step_width = Inches(2)
    start_x = Inches(0.8)
    for i, step in enumerate(flywheel_steps):
        x = start_x + i * (step_width + Inches(0.3))
        shape = slide.shapes.add_shape(1, x, Inches(5.5), step_width, Inches(0.9))
        shape.fill.solid()
        shape.fill.fore_color.rgb = NAVY if i % 2 == 0 else GOLD
        shape.line.fill.background()
        fc = WHITE if i % 2 == 0 else NAVY
        add_textbox(slide, x, Inches(5.55), step_width, Inches(0.85),
                    step, font_size=13, font_color=fc, bold=True,
                    alignment=PP_ALIGN.CENTER)
        if i < len(flywheel_steps) - 1:
            add_textbox(slide, x + step_width, Inches(5.7), Inches(0.3), Inches(0.5),
                        "\u27A1", font_size=20, font_color=NAVY, alignment=PP_ALIGN.CENTER)

    add_textbox(slide, Inches(0.8), Inches(6.7), Inches(11), Inches(0.5),
                "Year 1 may not be profitable after investment. Year 2+ is where the model pays off. This is a market entry play, not a quick win.",
                font_size=14, font_color=MED_GRAY, alignment=PP_ALIGN.CENTER)


def slide_14_risks(prs):
    """Slide 14: Risk Factors & Mitigation"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, WHITE)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "Risk Factors & Mitigation", font_size=36, font_color=NAVY, bold=True)
    add_divider(slide, Inches(0.8), Inches(1.1), Inches(3))

    data = [
        ["Risk", "Likelihood", "Impact", "Mitigation"],
        ["Lose early bids", "High (expected)", "Low",
         "Start with micro-purchases under $10K; learn evaluation criteria from each loss"],
        ["Slow relationship building", "Medium", "Medium",
         "Conference attendance; consistent follow-up; Sources Sought responses get you on the radar"],
        ["SAM.gov registration delays", "Medium", "High",
         "Start registration immediately — 30-45 day process; pursue state/local while waiting"],
        ["Salesperson bandwidth", "Medium", "Medium",
         "SMC handles all admin so sales focuses 100% on relationships and closing"],
        ["Strong incumbent on target contracts", "Medium", "Medium",
         "Focus on set-asides, expiring contracts, and agencies with known vendor complaints"],
        ["Certification requirements (SQF/HACCP)", "Low-Medium", "Medium",
         "Identify requirements early; budget for certification if not already held"],
    ]
    add_table(slide, Inches(0.5), Inches(1.5), Inches(12.3),
              len(data), 4, data,
              col_widths=[Inches(2.5), Inches(1.5), Inches(1), Inches(7.3)])

    # Realistic expectations
    add_textbox(slide, Inches(0.8), Inches(5.5), Inches(11), Inches(0.4),
                "Setting Realistic Expectations:",
                font_size=18, font_color=NAVY, bold=True)
    items = [
        "Newport WILL lose some early bids. That's normal and expected. Every loss teaches something.",
        "The first 3-6 months are groundwork. Visible results start in months 4-8.",
        "Government sales cycles are 3-12 months. Patience is required.",
        "The investment is modest relative to the opportunity. A single contract win justifies all Year 1 costs.",
    ]
    add_bullet_list(slide, Inches(0.8), Inches(5.9), Inches(11), Inches(1.5),
                    items, font_size=14, spacing=Pt(6))


def slide_15_the_ask(prs):
    """Slide 15: The Ask — Next Steps"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_textbox(slide, Inches(0.8), Inches(0.4), Inches(11), Inches(0.7),
                "The Ask", font_size=40, font_color=WHITE, bold=True,
                alignment=PP_ALIGN.CENTER)
    add_divider(slide, Inches(4), Inches(1.1), Inches(5), color=GOLD)

    add_textbox(slide, Inches(0.8), Inches(1.4), Inches(11), Inches(0.5),
                "What We Need From Newport:", font_size=24, font_color=GOLD, bold=True,
                alignment=PP_ALIGN.CENTER)

    ask_items = [
        "Authorize initial investment (~$5,000-$12,000 for registrations, memberships, materials)",
        "Designate a government sales point person (8-10 hours/week initially)",
        "Commit to attending 1-2 industry conferences in Year 1",
        "Engage Still Mind Creative for ongoing operational support",
        "Be patient — Year 1 builds the foundation; ROI compounds in Years 2-3",
    ]
    txBox = slide.shapes.add_textbox(Inches(1.5), Inches(2.1), Inches(10), Inches(2.5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(ask_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"\u2705  {item}"
        p.font.size = Pt(17)
        p.font.color.rgb = WHITE
        p.font.name = "Calibri"
        p.space_after = Pt(10)

    # Immediate next steps
    add_textbox(slide, Inches(0.8), Inches(4.8), Inches(11), Inches(0.5),
                "Immediate Next Steps:", font_size=22, font_color=GOLD, bold=True,
                alignment=PP_ALIGN.CENTER)

    data = [
        ["Action", "Owner", "Timeline"],
        ["Register on SAM.gov", "Newport (SMC assists)", "Start immediately (30-45 day process)"],
        ["Register on MyFloridaMarketPlace", "Newport (SMC assists)", "Week 1"],
        ["Submit vendor applications to GEO Group + Trinity", "SMC drafts, Newport submits", "Week 1-2"],
        ["Schedule 5 FL school district meetings", "Newport salesperson", "Month 1"],
        ["Join ACFSA ($150) and FSNA", "Newport", "Month 1"],
        ["Begin Sources Sought monitoring + responses", "Still Mind Creative", "Ongoing from Day 1"],
    ]
    add_table(slide, Inches(1), Inches(5.3), Inches(11.3),
              len(data), 3, data,
              col_widths=[Inches(5), Inches(3), Inches(3.3)],
              header_bg=GOLD, header_fg=NAVY)

    # Closing
    add_textbox(slide, Inches(0.8), Inches(7.0), Inches(11), Inches(0.4),
                "Still Mind Creative LLC  |  Prepared " + datetime.now().strftime("%B %Y"),
                font_size=12, font_color=MED_GRAY, alignment=PP_ALIGN.CENTER)


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT

    print("Building pitchbook slides...")
    slides = [
        ("Slide 1: Cover", slide_01_cover),
        ("Slide 2: Executive Summary", slide_02_exec_summary),
        ("Slide 3: Market Opportunity", slide_03_market_opportunity),
        ("Slide 4: Fraud Crisis", slide_04_fraud_crisis),
        ("Slide 5: Competitive Moat", slide_05_competitive_moat),
        ("Slide 6: Competitive Landscape", slide_06_competitive_landscape),
        ("Slide 7: Pipeline", slide_07_pipeline),
        ("Slide 8: Decision Makers", slide_08_decision_makers),
        ("Slide 9: Operating Model", slide_09_operating_model),
        ("Slide 10: Year 1 Roadmap", slide_10_roadmap),
        ("Slide 11: Success Metrics", slide_11_success_metrics),
        ("Slide 12: Investment", slide_12_investment),
        ("Slide 13: Returns / Compounding", slide_13_returns),
        ("Slide 14: Risk Factors", slide_14_risks),
        ("Slide 15: The Ask", slide_15_the_ask),
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
