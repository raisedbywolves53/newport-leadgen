#!/usr/bin/env python3
"""
Build Newport GovCon Pro Forma Financial Model.

Generates a professional Excel workbook with 4 sheets:
  1. Assumptions  - All editable inputs (blue text, yellow highlights)
  2. Revenue Model - 24-month projection x 3 scenarios (all Excel formulas)
  3. Summary       - Executive view pulling from Revenue Model
  4. Platform Comparison - Free vs Optimal side-by-side

ALL calculations use Excel formulas, NOT Python math.
"""

import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------
BLUE_FONT = Font(name="Calibri", size=11, color="0000FF")
BLUE_FONT_BOLD = Font(name="Calibri", size=11, color="0000FF", bold=True)
BLACK_FONT = Font(name="Calibri", size=11, color="000000")
BLACK_FONT_BOLD = Font(name="Calibri", size=11, color="000000", bold=True)
GREEN_FONT = Font(name="Calibri", size=11, color="008000")
GREEN_FONT_BOLD = Font(name="Calibri", size=11, color="008000", bold=True)
HEADER_FONT = Font(name="Calibri", size=12, color="000000", bold=True)
TITLE_FONT = Font(name="Calibri", size=14, color="000000", bold=True)
SECTION_FONT = Font(name="Calibri", size=11, color="000000", bold=True, italic=True)

YELLOW_FILL = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
LIGHT_GRAY_FILL = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
LIGHT_BLUE_FILL = PatternFill(start_color="DCE6F1", end_color="DCE6F1", fill_type="solid")
WHITE_FILL = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
ALT_ROW_FILL = PatternFill(start_color="F5F5F5", end_color="F5F5F5", fill_type="solid")

THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)

FMT_CURRENCY = '$#,##0'
FMT_PERCENT = '0.0%'
FMT_COUNT = '#,##0'
FMT_COUNT_1 = '0.0'


def set_cell(ws, row, col, value, font=None, fill=None, fmt=None, alignment=None, border=None):
    """Helper to set a cell's value and styling."""
    cell = ws.cell(row=row, column=col, value=value)
    if font:
        cell.font = font
    if fill:
        cell.fill = fill
    if fmt:
        cell.number_format = fmt
    if alignment:
        cell.alignment = alignment
    if border:
        cell.border = border
    return cell


def auto_fit_columns(ws, min_width=10, max_width=40):
    """Auto-fit column widths based on content."""
    for col_cells in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col_cells[0].column)
        for cell in col_cells:
            if cell.value is not None:
                val_str = str(cell.value)
                # Truncate formula display for width calc
                if val_str.startswith("="):
                    val_str = val_str[:20]
                max_len = max(max_len, len(val_str))
        width = min(max(max_len + 3, min_width), max_width)
        ws.column_dimensions[col_letter].width = width


# ---------------------------------------------------------------------------
# Sheet 1: Assumptions
# ---------------------------------------------------------------------------
def build_assumptions(wb):
    ws = wb.active
    ws.title = "Assumptions"

    # Title
    set_cell(ws, 1, 1, "Newport GovCon Pro Forma Assumptions", font=TITLE_FONT)
    ws.merge_cells("A1:C1")

    # ---- Section: Newport Business Assumptions ----
    set_cell(ws, 2, 1, "Newport Business Assumptions", font=SECTION_FONT, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 2, 2, None, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 2, 3, None, fill=LIGHT_GRAY_FILL)

    labels_business = [
        (3, "Wholesale Gross Margin", 0.11, FMT_PERCENT, True,
         "Newport's estimated margin on government food supply"),
        (4, "Average Contract Value - Conservative", 50000, FMT_CURRENCY, True, ""),
        (5, "Average Contract Value - Moderate", 75000, FMT_CURRENCY, True, ""),
        (6, "Average Contract Value - Aggressive", 100000, FMT_CURRENCY, True, ""),
        (7, "Average Contract Duration (months)", 12, FMT_COUNT, False, "Most small contracts are annual"),
        (8, "Revenue Recognition", "Monthly", None, False, "Spread evenly over contract duration"),
    ]
    for row, label, value, fmt, highlight, note in labels_business:
        set_cell(ws, row, 1, label, font=BLACK_FONT)
        set_cell(ws, row, 2, value, font=BLUE_FONT, fmt=fmt,
                 fill=YELLOW_FILL if highlight else None)
        if note:
            set_cell(ws, row, 3, note, font=Font(name="Calibri", size=10, color="808080", italic=True))

    # ---- Section: Win Rate Assumptions ----
    set_cell(ws, 10, 1, "Win Rate Assumptions", font=SECTION_FONT, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 10, 2, None, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 10, 3, None, fill=LIGHT_GRAY_FILL)

    labels_winrate = [
        (11, "Year 1 Win Rate (Months 1-6)", 0.15, FMT_PERCENT, True,
         "New entrant, no past performance"),
        (12, "Year 1 Win Rate (Months 7-12)", 0.25, FMT_PERCENT, True,
         "Some past performance building"),
        (13, "Year 2 Win Rate", 0.35, FMT_PERCENT, True,
         "Established past performance"),
    ]
    for row, label, value, fmt, highlight, note in labels_winrate:
        set_cell(ws, row, 1, label, font=BLACK_FONT)
        set_cell(ws, row, 2, value, font=BLUE_FONT, fmt=fmt,
                 fill=YELLOW_FILL if highlight else None)
        if note:
            set_cell(ws, row, 3, note, font=Font(name="Calibri", size=10, color="808080", italic=True))

    # ---- Section: Bid Volume Assumptions ----
    set_cell(ws, 15, 1, "Bid Volume Assumptions", font=SECTION_FONT, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 15, 2, None, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 15, 3, None, fill=LIGHT_GRAY_FILL)

    labels_bid = [
        (16, "Bids/Month - Conservative (Free system)", 1.5, FMT_COUNT_1, True, "~18/year"),
        (17, "Bids/Month - Moderate (Optimal system)", 3, FMT_COUNT_1, True, "~36/year"),
        (18, "Bids/Month - Aggressive (Optimal + dedicated effort)", 5, FMT_COUNT_1, True, "~60/year"),
    ]
    for row, label, value, fmt, highlight, note in labels_bid:
        set_cell(ws, row, 1, label, font=BLACK_FONT)
        set_cell(ws, row, 2, value, font=BLUE_FONT, fmt=fmt,
                 fill=YELLOW_FILL if highlight else None)
        if note:
            set_cell(ws, row, 3, note, font=Font(name="Calibri", size=10, color="808080", italic=True))

    # ---- Section: Platform Cost Assumptions ----
    set_cell(ws, 20, 1, "Platform Cost Assumptions", font=SECTION_FONT, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 20, 2, None, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 20, 3, None, fill=LIGHT_GRAY_FILL)

    labels_platform = [
        (21, "Free System Cost (annual)", 0, FMT_CURRENCY, False, "Built-in tools only"),
        (22, "CLEATUS (annual)", 3000, FMT_CURRENCY, True, "Mid-range estimate"),
        (23, "HigherGov (annual)", 3500, FMT_CURRENCY, True, "Mid-range estimate"),
        (24, "GovSpend (annual)", 6500, FMT_CURRENCY, True, "Mid-range estimate"),
        (25, "Optimal System Total (annual)", "=SUM(B22:B24)", FMT_CURRENCY, False,
         "Formula: sum of platform costs"),
        (26, "Consulting Fee - Monthly Retainer", None, FMT_CURRENCY, True,
         "Leave blank for Newport to discuss"),
    ]
    for row, label, value, fmt, highlight, note in labels_platform:
        set_cell(ws, row, 1, label, font=BLACK_FONT)
        font_to_use = BLACK_FONT if (isinstance(value, str) and str(value).startswith("=")) else BLUE_FONT
        set_cell(ws, row, 2, value, font=font_to_use, fmt=fmt,
                 fill=YELLOW_FILL if highlight else None)
        if note:
            set_cell(ws, row, 3, note, font=Font(name="Calibri", size=10, color="808080", italic=True))

    # ---- Section: Ramp Assumptions ----
    set_cell(ws, 28, 1, "Ramp Assumptions", font=SECTION_FONT, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 28, 2, None, fill=LIGHT_GRAY_FILL)
    set_cell(ws, 28, 3, None, fill=LIGHT_GRAY_FILL)

    labels_ramp = [
        (29, "Months to First Bid", 2, FMT_COUNT, True,
         "SAM.gov registration + first opportunity cycle"),
        (30, "Months to First Win", 4, FMT_COUNT, True,
         "Average award timeline after first submission"),
    ]
    for row, label, value, fmt, highlight, note in labels_ramp:
        set_cell(ws, row, 1, label, font=BLACK_FONT)
        set_cell(ws, row, 2, value, font=BLUE_FONT, fmt=fmt,
                 fill=YELLOW_FILL if highlight else None)
        if note:
            set_cell(ws, row, 3, note, font=Font(name="Calibri", size=10, color="808080", italic=True))

    # Column widths
    ws.column_dimensions["A"].width = 48
    ws.column_dimensions["B"].width = 18
    ws.column_dimensions["C"].width = 52

    return ws


# ---------------------------------------------------------------------------
# Sheet 2: Revenue Model
# ---------------------------------------------------------------------------
def build_revenue_model(wb):
    ws = wb.create_sheet("Revenue Model")

    months_label = [
        "Mar 2026", "Apr 2026", "May 2026", "Jun 2026", "Jul 2026", "Aug 2026",
        "Sep 2026", "Oct 2026", "Nov 2026", "Dec 2026", "Jan 2027", "Feb 2027",
        "Mar 2027", "Apr 2027", "May 2027", "Jun 2027", "Jul 2027", "Aug 2027",
        "Sep 2027", "Oct 2027", "Nov 2027", "Dec 2027", "Jan 2028", "Feb 2028",
    ]

    # -- Row 1: Title + month headers --
    set_cell(ws, 1, 1, "Revenue Model - 24 Month Projection", font=TITLE_FONT)
    for m in range(24):
        col = m + 2  # columns B..Y
        set_cell(ws, 1, col, None, fill=LIGHT_GRAY_FILL)

    # -- Row 2: Month numbers 1-24 --
    set_cell(ws, 2, 1, "Month #", font=HEADER_FONT, fill=LIGHT_GRAY_FILL)
    for m in range(24):
        col = m + 2
        set_cell(ws, 2, col, m + 1, font=BLACK_FONT_BOLD, fill=LIGHT_GRAY_FILL,
                 alignment=Alignment(horizontal="center"))

    # -- Row 3: Calendar month labels --
    set_cell(ws, 3, 1, "Calendar Month", font=HEADER_FONT, fill=LIGHT_GRAY_FILL)
    for m in range(24):
        col = m + 2
        set_cell(ws, 3, col, months_label[m], font=BLACK_FONT, fill=LIGHT_GRAY_FILL,
                 alignment=Alignment(horizontal="center"))

    # -------------------------------------------------------------------
    # Scenario definitions
    # Each scenario: (title, header_row, first_metric_row, bid_vol_ref, avg_cv_ref, platform_cost_formula)
    #   header_row   = row for scenario title label
    #   first_metric_row = first row of 12 metric rows
    #   bid_vol_ref  = Assumptions cell for bids/month
    #   avg_cv_ref   = Assumptions cell for avg contract value
    #   platform_cost_formula = monthly platform cost formula
    #
    # Layout per spec: Conservative rows 5-16, Moderate rows 18-29, Aggressive rows 31-42
    # -------------------------------------------------------------------
    scenarios = [
        ("CONSERVATIVE SCENARIO",  4,  5, "B16", "B4", "=Assumptions!$B$21/12"),
        ("MODERATE SCENARIO",     17, 18, "B17", "B5", "=Assumptions!$B$25/12"),
        ("AGGRESSIVE SCENARIO",   30, 31, "B18", "B6", "=Assumptions!$B$25/12"),
    ]

    # Row labels for each scenario block (12 metric rows)
    metric_labels = [
        "Bids Submitted",
        "Win Rate",
        "New Contracts Won",
        "Cumulative Contracts Won",
        "Active Contracts",
        "Monthly Revenue",
        "Cumulative Revenue",
        "Monthly Gross Profit",
        "Cumulative Gross Profit",
        "Monthly Platform Cost",
        "Monthly Net Contribution",
        "Cumulative Net Contribution",
    ]

    # Number formats per metric
    metric_fmts = [
        FMT_COUNT_1,   # Bids Submitted
        FMT_PERCENT,   # Win Rate
        FMT_COUNT,     # New Contracts Won
        FMT_COUNT,     # Cumulative Contracts Won
        FMT_COUNT,     # Active Contracts
        FMT_CURRENCY,  # Monthly Revenue
        FMT_CURRENCY,  # Cumulative Revenue
        FMT_CURRENCY,  # Monthly Gross Profit
        FMT_CURRENCY,  # Cumulative Gross Profit
        FMT_CURRENCY,  # Monthly Platform Cost
        FMT_CURRENCY,  # Monthly Net Contribution
        FMT_CURRENCY,  # Cumulative Net Contribution
    ]

    for scenario_title, hdr_row, sr, bid_ref, cv_ref, plat_formula in scenarios:
        # Scenario header row (above the metric rows)
        set_cell(ws, hdr_row, 1, scenario_title, font=HEADER_FONT, fill=LIGHT_BLUE_FILL)
        for m in range(24):
            set_cell(ws, hdr_row, m + 2, None, fill=LIGHT_BLUE_FILL)

        # Metric labels (12 rows starting at sr)
        for i, label in enumerate(metric_labels):
            row = sr + i
            set_cell(ws, row, 1, label, font=BLACK_FONT_BOLD)

        # Metric row absolute positions (sr + offset)
        r_bids    = sr + 0   # Bids Submitted
        r_wr      = sr + 1   # Win Rate
        r_new     = sr + 2   # New Contracts Won
        r_cum     = sr + 3   # Cumulative Contracts Won
        r_active  = sr + 4   # Active Contracts
        r_rev     = sr + 5   # Monthly Revenue
        r_cumrev  = sr + 6   # Cumulative Revenue
        r_gp      = sr + 7   # Monthly Gross Profit
        r_cumgp   = sr + 8   # Cumulative Gross Profit
        r_plat    = sr + 9   # Monthly Platform Cost
        r_net     = sr + 10  # Monthly Net Contribution
        r_cumnet  = sr + 11  # Cumulative Net Contribution

        for m in range(24):
            col = m + 2
            month_num = m + 1
            col_letter = get_column_letter(col)

            # ----- Bids Submitted -----
            # =IF(month_num < Assumptions!$B$29, 0, Assumptions!$B$16)
            # month_num is in row 2 of that column
            f_bids = f'=IF({col_letter}$2<Assumptions!$B$29,0,Assumptions!${bid_ref[0]}${bid_ref[1:]})'
            set_cell(ws, r_bids, col, f_bids, font=BLACK_FONT, fmt=metric_fmts[0])

            # ----- Win Rate -----
            # =IF(month_num<=6, Assumptions!$B$11, IF(month_num<=12, Assumptions!$B$12, Assumptions!$B$13))
            # Also 0 if month < months_to_first_win
            f_wr = (
                f'=IF({col_letter}$2<Assumptions!$B$30,0,'
                f'IF({col_letter}$2<=6,Assumptions!$B$11,'
                f'IF({col_letter}$2<=12,Assumptions!$B$12,Assumptions!$B$13)))'
            )
            set_cell(ws, r_wr, col, f_wr, font=GREEN_FONT, fmt=metric_fmts[1])

            # ----- New Contracts Won -----
            # =ROUND(Bids * WinRate, 0)
            f_new = f'=ROUND({col_letter}{r_bids}*{col_letter}{r_wr},0)'
            set_cell(ws, r_new, col, f_new, font=BLACK_FONT, fmt=metric_fmts[2])

            # ----- Cumulative Contracts Won -----
            if m == 0:
                f_cum = f'={col_letter}{r_new}'
            else:
                prev_col = get_column_letter(col - 1)
                f_cum = f'={prev_col}{r_cum}+{col_letter}{r_new}'
            set_cell(ws, r_cum, col, f_cum, font=BLACK_FONT, fmt=metric_fmts[3])

            # ----- Active Contracts -----
            # Active = cumulative won now - cumulative won N months ago,
            # where N = contract duration (Assumptions!$B$7).
            f_active = (
                f'={col_letter}{r_cum}'
                f'-IF({col_letter}$2>Assumptions!$B$7,'
                f'OFFSET({col_letter}{r_cum},0,-Assumptions!$B$7),0)'
            )
            set_cell(ws, r_active, col, f_active, font=BLACK_FONT, fmt=metric_fmts[4])

            # ----- Monthly Revenue -----
            # =Active Contracts * (Avg Contract Value / Contract Duration)
            f_rev = (
                f'={col_letter}{r_active}*(Assumptions!${cv_ref[0]}${cv_ref[1:]}/Assumptions!$B$7)'
            )
            set_cell(ws, r_rev, col, f_rev, font=GREEN_FONT, fmt=metric_fmts[5])

            # ----- Cumulative Revenue -----
            if m == 0:
                f_cumrev = f'={col_letter}{r_rev}'
            else:
                prev_col = get_column_letter(col - 1)
                f_cumrev = f'={prev_col}{r_cumrev}+{col_letter}{r_rev}'
            set_cell(ws, r_cumrev, col, f_cumrev, font=BLACK_FONT, fmt=metric_fmts[6])

            # ----- Monthly Gross Profit -----
            f_gp = f'={col_letter}{r_rev}*Assumptions!$B$3'
            set_cell(ws, r_gp, col, f_gp, font=GREEN_FONT, fmt=metric_fmts[7])

            # ----- Cumulative Gross Profit -----
            if m == 0:
                f_cumgp = f'={col_letter}{r_gp}'
            else:
                prev_col = get_column_letter(col - 1)
                f_cumgp = f'={prev_col}{r_cumgp}+{col_letter}{r_gp}'
            set_cell(ws, r_cumgp, col, f_cumgp, font=BLACK_FONT, fmt=metric_fmts[8])

            # ----- Monthly Platform Cost -----
            set_cell(ws, r_plat, col, plat_formula, font=GREEN_FONT, fmt=metric_fmts[9])

            # ----- Monthly Net Contribution -----
            f_net = f'={col_letter}{r_gp}-{col_letter}{r_plat}'
            set_cell(ws, r_net, col, f_net, font=BLACK_FONT, fmt=metric_fmts[10])

            # ----- Cumulative Net Contribution -----
            if m == 0:
                f_cumnet = f'={col_letter}{r_net}'
            else:
                prev_col = get_column_letter(col - 1)
                f_cumnet = f'={prev_col}{r_cumnet}+{col_letter}{r_net}'
            set_cell(ws, r_cumnet, col, f_cumnet, font=BLACK_FONT, fmt=metric_fmts[11])

    # Freeze panes: freeze row 3 and column A (cell B4)
    ws.freeze_panes = "B4"

    # Column widths
    ws.column_dimensions["A"].width = 30
    for m in range(24):
        ws.column_dimensions[get_column_letter(m + 2)].width = 14

    return ws


# ---------------------------------------------------------------------------
# Sheet 3: Summary
# ---------------------------------------------------------------------------
def build_summary(wb):
    ws = wb.create_sheet("Summary")

    # Title
    set_cell(ws, 1, 1, "Newport GovCon Financial Summary", font=TITLE_FONT)
    ws.merge_cells("A1:D1")

    # Headers
    headers = ["Metric", "Conservative", "Moderate", "Aggressive"]
    for i, h in enumerate(headers):
        set_cell(ws, 3, i + 1, h, font=HEADER_FONT, fill=LIGHT_GRAY_FILL,
                 alignment=Alignment(horizontal="center"))

    # Scenario first-metric rows on Revenue Model
    # Conservative sr=5 (rows 5-16), Moderate sr=18 (rows 18-29), Aggressive sr=31 (rows 31-42)
    srs = [5, 18, 31]  # first metric rows for conservative, moderate, aggressive

    # -------------------------------------------------------------------
    # Section: Year 1 Results
    # -------------------------------------------------------------------
    set_cell(ws, 5, 1, "YEAR 1 RESULTS (Months 1-12)", font=HEADER_FONT, fill=LIGHT_BLUE_FILL)
    for c in range(2, 5):
        set_cell(ws, 5, c, None, fill=LIGHT_BLUE_FILL)

    year1_metrics = [
        ("Total Bids Submitted", 0, FMT_COUNT_1, "sum"),     # offset +0 = Bids (sum)
        ("Contracts Won (Year 1)", 3, FMT_COUNT, "point"),    # offset +3 = CumWon at M12
        ("Total Revenue", 6, FMT_CURRENCY, "point"),          # offset +6 = CumRev at M12
        ("Gross Profit", 8, FMT_CURRENCY, "point"),           # offset +8 = CumGP at M12
        ("Platform Investment", 9, FMT_CURRENCY, "sum"),      # offset +9 = sum of monthly platform
        ("Net Contribution", 11, FMT_CURRENCY, "point"),      # offset +11 = CumNetContrib at M12
    ]

    row_cursor = 6
    for label, offset, fmt, agg in year1_metrics:
        fill = ALT_ROW_FILL if (row_cursor % 2 == 0) else WHITE_FILL
        set_cell(ws, row_cursor, 1, label, font=BLACK_FONT, fill=fill)
        for s_idx, sr in enumerate(srs):
            metric_row = sr + offset
            if agg == "sum":
                # Sum across year 1 months
                formula = f"=SUM('Revenue Model'!B{metric_row}:M{metric_row})"
            else:
                # Cumulative value at month 12 (column M)
                formula = f"='Revenue Model'!M{metric_row}"
            set_cell(ws, row_cursor, s_idx + 2, formula, font=GREEN_FONT, fmt=fmt, fill=fill)
        row_cursor += 1

    # ROI row
    fill = ALT_ROW_FILL if (row_cursor % 2 == 0) else WHITE_FILL
    set_cell(ws, row_cursor, 1, "ROI", font=BLACK_FONT_BOLD, fill=fill)
    for s_idx, sr in enumerate(srs):
        col_letter = get_column_letter(s_idx + 2)
        net_row = row_cursor - 1
        plat_row = row_cursor - 2
        formula = f'=IF({col_letter}{plat_row}=0,"N/A (Free)",{col_letter}{net_row}/{col_letter}{plat_row})'
        set_cell(ws, row_cursor, s_idx + 2, formula, font=BLACK_FONT_BOLD, fmt=FMT_PERCENT, fill=fill)
    row_cursor += 1

    # Breakeven Month Year 1
    fill = ALT_ROW_FILL if (row_cursor % 2 == 0) else WHITE_FILL
    set_cell(ws, row_cursor, 1, "Breakeven Month", font=BLACK_FONT_BOLD, fill=fill)
    for s_idx, sr in enumerate(srs):
        cum_net_row = sr + 11  # Cumulative Net Contribution row (offset +11)
        formula = (
            f'=IFERROR(MATCH(TRUE,INDEX(\'Revenue Model\'!B{cum_net_row}:Y{cum_net_row}>0,),0),"Not in 24mo")'
        )
        set_cell(ws, row_cursor, s_idx + 2, formula, font=BLACK_FONT_BOLD, fmt=FMT_COUNT, fill=fill)
    row_cursor += 2

    # -------------------------------------------------------------------
    # Section: Year 2 Results
    # -------------------------------------------------------------------
    set_cell(ws, row_cursor, 1, "YEAR 2 RESULTS (Months 13-24)", font=HEADER_FONT, fill=LIGHT_BLUE_FILL)
    for c in range(2, 5):
        set_cell(ws, row_cursor, c, None, fill=LIGHT_BLUE_FILL)
    row_cursor += 1

    year2_metrics = [
        ("Total Bids Submitted", 0, FMT_COUNT_1),     # offset +0 = Bids
        ("Contracts Won (Year 2)", 2, FMT_COUNT),     # offset +2 = NewWon (sum in Y2)
        ("Total Revenue", 5, FMT_CURRENCY),           # offset +5 = MonthlyRev (sum in Y2)
        ("Gross Profit", 7, FMT_CURRENCY),            # offset +7 = MonthlyGP (sum in Y2)
        ("Platform Investment", 9, FMT_CURRENCY),     # offset +9 = PlatCost (sum in Y2)
        ("Net Contribution", 10, FMT_CURRENCY),       # offset +10 = NetContrib (sum in Y2)
    ]

    for label, offset, fmt in year2_metrics:
        fill = ALT_ROW_FILL if (row_cursor % 2 == 0) else WHITE_FILL
        set_cell(ws, row_cursor, 1, label, font=BLACK_FONT, fill=fill)
        for s_idx, sr in enumerate(srs):
            metric_row = sr + offset
            # Year 2 sums: columns N (14) to Y (25)
            formula = f"=SUM('Revenue Model'!N{metric_row}:Y{metric_row})"
            set_cell(ws, row_cursor, s_idx + 2, formula, font=GREEN_FONT, fmt=fmt, fill=fill)
        row_cursor += 1

    # Year 2 ROI
    fill = ALT_ROW_FILL if (row_cursor % 2 == 0) else WHITE_FILL
    set_cell(ws, row_cursor, 1, "ROI", font=BLACK_FONT_BOLD, fill=fill)
    for s_idx, sr in enumerate(srs):
        col_letter = get_column_letter(s_idx + 2)
        net_row = row_cursor - 1
        plat_row = row_cursor - 2
        formula = f'=IF({col_letter}{plat_row}=0,"N/A (Free)",{col_letter}{net_row}/{col_letter}{plat_row})'
        set_cell(ws, row_cursor, s_idx + 2, formula, font=BLACK_FONT_BOLD, fmt=FMT_PERCENT, fill=fill)
    row_cursor += 2

    # -------------------------------------------------------------------
    # Section: 24-Month Totals
    # -------------------------------------------------------------------
    set_cell(ws, row_cursor, 1, "24-MONTH TOTALS", font=HEADER_FONT, fill=LIGHT_BLUE_FILL)
    for c in range(2, 5):
        set_cell(ws, row_cursor, c, None, fill=LIGHT_BLUE_FILL)
    row_cursor += 1

    total_metrics = [
        ("Total Bids Submitted", 0, FMT_COUNT_1, "sum"),      # offset +0 = Bids (sum)
        ("Total Contracts Won", 3, FMT_COUNT, "point"),        # offset +3 = CumWon at M24
        ("Total Revenue", 6, FMT_CURRENCY, "point"),           # offset +6 = CumRev at M24
        ("Total Gross Profit", 8, FMT_CURRENCY, "point"),      # offset +8 = CumGP at M24
        ("Total Platform Investment", 9, FMT_CURRENCY, "sum"), # offset +9 = PlatCost (sum)
        ("Total Net Contribution", 11, FMT_CURRENCY, "point"), # offset +11 = CumNetContrib at M24
    ]

    for label, offset, fmt, agg in total_metrics:
        fill = ALT_ROW_FILL if (row_cursor % 2 == 0) else WHITE_FILL
        set_cell(ws, row_cursor, 1, label, font=BLACK_FONT, fill=fill)
        for s_idx, sr in enumerate(srs):
            metric_row = sr + offset
            if agg == "sum":
                # Sum of all 24 months
                formula = f"=SUM('Revenue Model'!B{metric_row}:Y{metric_row})"
            else:
                # Cumulative value at month 24 (column Y)
                formula = f"='Revenue Model'!Y{metric_row}"
            set_cell(ws, row_cursor, s_idx + 2, formula, font=GREEN_FONT, fmt=fmt, fill=fill)
        row_cursor += 1

    # 24-month ROI
    fill = ALT_ROW_FILL if (row_cursor % 2 == 0) else WHITE_FILL
    set_cell(ws, row_cursor, 1, "24-Month ROI", font=BLACK_FONT_BOLD, fill=fill)
    for s_idx, sr in enumerate(srs):
        col_letter = get_column_letter(s_idx + 2)
        net_row = row_cursor - 1
        plat_row = row_cursor - 2
        formula = f'=IF({col_letter}{plat_row}=0,"N/A (Free)",{col_letter}{net_row}/{col_letter}{plat_row})'
        set_cell(ws, row_cursor, s_idx + 2, formula, font=BLACK_FONT_BOLD, fmt=FMT_PERCENT, fill=fill)

    # Column widths
    ws.column_dimensions["A"].width = 32
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 20
    ws.column_dimensions["D"].width = 20

    return ws


# ---------------------------------------------------------------------------
# Sheet 4: Platform Comparison
# ---------------------------------------------------------------------------
def build_platform_comparison(wb):
    ws = wb.create_sheet("Platform Comparison")

    # Title
    set_cell(ws, 1, 1, "Platform Comparison: Free vs. Optimal Investment", font=TITLE_FONT)
    ws.merge_cells("A1:C1")

    # Headers
    headers = ["Component", "Free", "Optimal"]
    for i, h in enumerate(headers):
        set_cell(ws, 3, i + 1, h, font=HEADER_FONT, fill=LIGHT_GRAY_FILL,
                 alignment=Alignment(horizontal="center"))

    # Data rows
    comparison_data = [
        ("Federal Monitoring", 'SAM.gov API - $0', '+ CLEATUS - $3,000/yr', False),
        ("State/Local Monitoring", 'Manual - $0', 'HigherGov - $3,500/yr', False),
        ("Micro-Purchase Intel", 'N/A - $0', 'GovSpend - $6,500/yr', False),
        ("Competitive Intelligence", 'FPDS + USASpending - $0', 'Same - $0', False),
        ("Proposal Writing", 'Claude + Templates - $0', 'CLEATUS AI - included', False),
        ("Pipeline Tracking", 'Google Sheets - $0', 'Same - $0', False),
    ]

    row_cursor = 4
    for label, free_val, optimal_val, is_total in comparison_data:
        fill = ALT_ROW_FILL if (row_cursor % 2 == 0) else WHITE_FILL
        set_cell(ws, row_cursor, 1, label, font=BLACK_FONT, fill=fill)
        set_cell(ws, row_cursor, 2, free_val, font=BLACK_FONT, fill=fill,
                 alignment=Alignment(horizontal="center"))
        set_cell(ws, row_cursor, 3, optimal_val, font=BLACK_FONT, fill=fill,
                 alignment=Alignment(horizontal="center"))
        row_cursor += 1

    # Separator
    row_cursor += 1

    # Totals row - reference Assumptions sheet
    set_cell(ws, row_cursor, 1, "Total Annual Cost", font=BLACK_FONT_BOLD, fill=LIGHT_BLUE_FILL)
    set_cell(ws, row_cursor, 2, "=Assumptions!B21", font=GREEN_FONT_BOLD, fmt=FMT_CURRENCY,
             fill=LIGHT_BLUE_FILL, alignment=Alignment(horizontal="center"))
    set_cell(ws, row_cursor, 3, "=Assumptions!B25", font=GREEN_FONT_BOLD, fmt=FMT_CURRENCY,
             fill=LIGHT_BLUE_FILL, alignment=Alignment(horizontal="center"))
    row_cursor += 1

    # Additional comparison rows
    set_cell(ws, row_cursor, 1, "Market Coverage", font=BLACK_FONT_BOLD)
    set_cell(ws, row_cursor, 2, "~40-50%", font=BLACK_FONT,
             alignment=Alignment(horizontal="center"))
    set_cell(ws, row_cursor, 3, "~90%+", font=BLACK_FONT,
             alignment=Alignment(horizontal="center"))
    row_cursor += 1

    set_cell(ws, row_cursor, 1, "Bid Capacity/Year", font=BLACK_FONT_BOLD)
    set_cell(ws, row_cursor, 2, "12-20", font=BLACK_FONT,
             alignment=Alignment(horizontal="center"))
    set_cell(ws, row_cursor, 3, "40-60", font=BLACK_FONT,
             alignment=Alignment(horizontal="center"))
    row_cursor += 1

    set_cell(ws, row_cursor, 1, "Estimated Win Rate Uplift", font=BLACK_FONT_BOLD)
    set_cell(ws, row_cursor, 2, "Baseline", font=BLACK_FONT,
             alignment=Alignment(horizontal="center"))
    set_cell(ws, row_cursor, 3, "+30-50% more bids = more wins", font=BLACK_FONT,
             alignment=Alignment(horizontal="center"))
    row_cursor += 2

    # Monthly cost breakdown
    set_cell(ws, row_cursor, 1, "Monthly Cost Breakdown", font=HEADER_FONT, fill=LIGHT_GRAY_FILL)
    set_cell(ws, row_cursor, 2, None, fill=LIGHT_GRAY_FILL)
    set_cell(ws, row_cursor, 3, None, fill=LIGHT_GRAY_FILL)
    row_cursor += 1

    set_cell(ws, row_cursor, 1, "Monthly Platform Cost", font=BLACK_FONT)
    set_cell(ws, row_cursor, 2, "=Assumptions!B21/12", font=GREEN_FONT, fmt=FMT_CURRENCY,
             alignment=Alignment(horizontal="center"))
    set_cell(ws, row_cursor, 3, "=Assumptions!B25/12", font=GREEN_FONT, fmt=FMT_CURRENCY,
             alignment=Alignment(horizontal="center"))
    row_cursor += 1

    set_cell(ws, row_cursor, 1, "Consulting Retainer", font=BLACK_FONT)
    set_cell(ws, row_cursor, 2, "N/A", font=BLACK_FONT,
             alignment=Alignment(horizontal="center"))
    set_cell(ws, row_cursor, 3, '=IF(Assumptions!B26="","TBD",Assumptions!B26)', font=GREEN_FONT,
             fmt=FMT_CURRENCY, alignment=Alignment(horizontal="center"))

    # Column widths
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 35

    return ws


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------
def main():
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "newport-govcon-proforma.xlsx")

    print("=" * 60)
    print("Newport GovCon Pro Forma Financial Model Builder")
    print("=" * 60)

    wb = Workbook()

    print("[1/4] Building Assumptions sheet...")
    build_assumptions(wb)

    print("[2/4] Building Revenue Model sheet (24 months x 3 scenarios)...")
    build_revenue_model(wb)

    print("[3/4] Building Summary sheet...")
    build_summary(wb)

    print("[4/4] Building Platform Comparison sheet...")
    build_platform_comparison(wb)

    # Save
    wb.save(output_path)
    print()
    print(f"Saved: {output_path}")
    print(f"File size: {os.path.getsize(output_path):,} bytes")
    print()

    # Verification
    print("Verification:")
    print(f"  Sheets: {wb.sheetnames}")
    for ws_name in wb.sheetnames:
        ws = wb[ws_name]
        print(f"  {ws_name}: {ws.max_row} rows x {ws.max_column} cols")

    print()
    print("All calculations use Excel formulas (=SUM, =IF, =ROUND, =OFFSET, etc.)")
    print("Blue text = editable inputs | Black text = formulas | Green text = cross-sheet refs")
    print("Yellow background = key assumptions to review")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
