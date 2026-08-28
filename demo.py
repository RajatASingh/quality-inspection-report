import streamlit as st
from pathlib import Path
from io import BytesIO
from datetime import date
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,
    PageBreak, KeepTogether, Image as PdfImage
)

LOGO_PATH = Path(__file__).with_name("demo.jpg")

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Process Sheet Generator",
    page_icon="📋",
    layout="wide",
)

# ============================================================
# CSS - CLEAN 2-COLUMN FORM
# ============================================================

st.markdown("""
<style>
    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .app-title {
        text-align: center;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 2px;
    }

    .app-subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 25px;
    }

    .section-title {
        background: #1f2937;
        color: white;
        padding: 10px 14px;
        border-radius: 6px;
        font-weight: 700;
        margin-top: 18px;
        margin-bottom: 10px;
    }

    .field-label {
        font-weight: 650;
        padding-top: 7px;
    }

    .hint {
        color: #777;
        font-size: 12px;
    }

    div[data-testid="stHorizontalBlock"] {
        align-items: center;
    }

    .download-note {
        background: #f3f4f6;
        padding: 12px;
        border-radius: 6px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPERS
# ============================================================

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def text_field(label, key, placeholder="", help_text=None):
    c1, c2 = st.columns([0.9, 2.1])
    with c1:
        st.markdown(f'<div class="field-label">{label}</div>', unsafe_allow_html=True)
        if help_text:
            st.markdown(f'<div class="hint">{help_text}</div>', unsafe_allow_html=True)
    with c2:
        return st.text_input(
            label,
            key=key,
            placeholder=placeholder,
            label_visibility="collapsed"
        )


def number_field(label, key, placeholder=""):
    c1, c2 = st.columns([0.9, 2.1])
    with c1:
        st.markdown(f'<div class="field-label">{label}</div>', unsafe_allow_html=True)
    with c2:
        return st.number_input(
            label,
            key=key,
            value=0.0,
            step=0.1,
            format="%.2f",
            label_visibility="collapsed"
        )


def date_field(label, key):
    c1, c2 = st.columns([0.9, 2.1])
    with c1:
        st.markdown(f'<div class="field-label">{label}</div>', unsafe_allow_html=True)
    with c2:
        return st.date_input(
            label,
            key=key,
            value=date.today(),
            label_visibility="collapsed"
        )


def two_input_row(label, key1, key2, placeholder1="", placeholder2=""):
    c1, c2 = st.columns([0.9, 2.1])
    with c1:
        st.markdown(f'<div class="field-label">{label}</div>', unsafe_allow_html=True)
    with c2:
        a, b = st.columns(2)
        with a:
            v1 = st.text_input(
                f"{label} 1", key=key1,
                placeholder=placeholder1,
                label_visibility="collapsed"
            )
        with b:
            v2 = st.text_input(
                f"{label} 2", key=key2,
                placeholder=placeholder2,
                label_visibility="collapsed"
            )
    return v1, v2


# ============================================================
# PDF HELPERS
# ============================================================

def p(text, style):
    return Paragraph(str(text).replace("\n", "<br/>"), style)


def build_pdf(data):
    """
    Creates a clean multi-page A4 process-sheet PDF.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=10 * mm,
        leftMargin=10 * mm,
        topMargin=9 * mm,
        bottomMargin=9 * mm,
        title="Process Sheet",
        author="Process Sheet Generator",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "title_custom",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        alignment=TA_CENTER,
        spaceAfter=2,
    )

    subtitle_style = ParagraphStyle(
        "subtitle_custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=13,
        alignment=TA_CENTER,
        spaceAfter=3,
    )

    section_style = ParagraphStyle(
        "section_custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=11,
        alignment=TA_CENTER,
    )

    label_style = ParagraphStyle(
        "label_custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9,
    )

    value_style = ParagraphStyle(
        "value_custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9,
    )

    small_style = ParagraphStyle(
        "small_custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=6.5,
        leading=8,
    )

    story = []

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    logo_cell = PdfImage(str(LOGO_PATH), width=24 * mm, height=24 * mm,
                         kind="proportional") if LOGO_PATH.exists() else ""
    header_table = Table([
        [logo_cell, [
            p("OM INDUSTRIES", title_style),
            #p("PROCESS SHEET", subtitle_style),
            # p("AUTOMOTIVE ENGINEERING COMPONENT G-64 MIDC AMBAD NASHIK 10", value_style),
        ]]
    ], colWidths=[32 * mm, 158 * mm])
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)

    rev_data = [
        [
            p("<b>Rev No.</b>", label_style),
            p(data["revision_no"], value_style),
            p("<b>Issued Date</b>", label_style),
            p(data["issued_date"], value_style),
        ]
    ]

    t = Table(rev_data, colWidths=[25*mm, 55*mm, 30*mm, 70*mm])
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.6, colors.black),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 4))

    # --------------------------------------------------------
    # GENERAL DETAILS
    # --------------------------------------------------------

    general_rows = [
        ["PART NAME", data["part_name"], "CUSTOMER NAME", data["customer_name"]],
        ["PART NO.", data["part_no"], "MACHINE NAME", data["machine_name"]],
        ["MACHINE NO.", data["machine_no"], "MOULD NO.", data["mould_no"]],
        ["MATERIAL NAME", data["material_name"], "GRADE", data["grade"]],
        ["M/C TONNAGE", data["machine_tonnage"], "MASTER BATCH", data["master_batch"]],
    ]

    story.append(make_pdf_table(general_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    # --------------------------------------------------------
    # PROCESS PARAMETERS
    # --------------------------------------------------------

    story.append(make_section_table("PROCESS PARAMETERS", section_style))
    process_rows = [
        ["PREHEATING TEMP. (+/-10°C)", data["preheating_temp"],
         "PREHEATING TIME", data["preheating_time"]],
        ["CYCLE TIME [SEC.]", data["cycle_time"],
         "COOLING TIME", data["cooling_time"]],
        ["CAVITY NO.", data["cavity_no"],
         "MTC TEMP.", data["mtc_temp"]],
        ["SHOT WT. - GM (+/-2%)", data["shot_weight"],
         "PART WT. - GM", data["part_weight"]],
        ["RUNNER WT. - GM", data["runner_weight"],
         "", ""],
    ]
    story.append(make_pdf_table(process_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    # --------------------------------------------------------
    # CLAMPING + EJECTOR
    # --------------------------------------------------------

    story.append(make_section_table("CLAMPING SYSTEM", section_style))

    clamp_rows = [
        ["PARAMETER", "SPEED", "PRESSURE", "POSITION", "TIME"],
        ["MOULD OPEN SLOW-1", data["mould_open_slow_1_speed"],
         data["mould_open_slow_1_pressure"], data["mould_open_slow_1_position"],
         data["mould_open_slow_1_time"]],
        ["OPEN FAST 2", data["open_fast_2_speed"],
         data["open_fast_2_pressure"], data["open_fast_2_position"],
         data["open_fast_2_time"]],
        ["OPEN SLOW 3", data["open_slow_3_speed"],
         data["open_slow_3_pressure"], data["open_slow_3_position"],
         data["open_slow_3_time"]],
        ["OPEN SLOW 4", data["open_slow_4_speed"],
         data["open_slow_4_pressure"], data["open_slow_4_position"],
         data["open_slow_4_time"]],
        ["MOULD CLOSING SLOW 1", data["mould_close_slow_1_speed"],
         data["mould_close_slow_1_pressure"], data["mould_close_slow_1_position"],
         data["mould_close_slow_1_time"]],
        ["CLOSE FAST 2", data["close_fast_2_speed"],
         data["close_fast_2_pressure"], data["close_fast_2_position"],
         data["close_fast_2_time"]],
        ["CLOSE SLOW 3", data["close_slow_3_speed"],
         data["close_slow_3_pressure"], data["close_slow_3_position"],
         data["close_slow_3_time"]],
        ["CLOSE SLOW 4", data["close_slow_4_speed"],
         data["close_slow_4_pressure"], data["close_slow_4_position"],
         data["close_slow_4_time"]],
    ]
    story.append(make_grid_table(clamp_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    story.append(make_section_table("EJECTOR SETTING", section_style))
    ejector_rows = [
        ["PARAMETER", "SPEED", "PRESSURE", "POSITION", "TIME"],
        ["EJECTOR FORWARD 1", data["ejector_forward_1_speed"],
         data["ejector_forward_1_pressure"], data["ejector_forward_1_position"],
         data["ejector_forward_1_time"]],
        ["EJECTOR FORWARD 2", data["ejector_forward_2_speed"],
         data["ejector_forward_2_pressure"], data["ejector_forward_2_position"],
         data["ejector_forward_2_time"]],
        ["EJECTOR RETURN 1", data["ejector_return_1_speed"],
         data["ejector_return_1_pressure"], data["ejector_return_1_position"],
         data["ejector_return_1_time"]],
        ["EJECTOR RETURN 2", data["ejector_return_2_speed"],
         data["ejector_return_2_pressure"], data["ejector_return_2_position"],
         data["ejector_return_2_time"]],
    ]
    story.append(make_grid_table(ejector_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    # --------------------------------------------------------
    # CORE
    # --------------------------------------------------------

    story.append(make_section_table("CORE SETTING", section_style))
    core_rows = [
        ["CORE PARAMETER", "VALUE"],
        ["CORE 1 (IN)", data["core_1_in"]],
        ["CORE 1 (OUT)", data["core_1_out"]],
        ["TIME", data["core_time"]],
    ]
    story.append(make_two_col_table(core_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    # --------------------------------------------------------
    # INJECTION
    # --------------------------------------------------------

    story.append(make_section_table("INJECTION SETTING", section_style))
    injection_rows = [
        ["PARAMETER", "SPEED", "PRESSURE", "POSITION", "TIME"],
        ["INJECTION 1", data["injection_1_speed"],
         data["injection_1_pressure"], data["injection_1_position"],
         data["injection_1_time"]],
        ["INJECTION 2", data["injection_2_speed"],
         data["injection_2_pressure"], data["injection_2_position"],
         data["injection_2_time"]],
        ["INJECTION 3", data["injection_3_speed"],
         data["injection_3_pressure"], data["injection_3_position"],
         data["injection_3_time"]],
    ]
    story.append(make_grid_table(injection_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    # --------------------------------------------------------
    # PLASTICIZING
    # --------------------------------------------------------

    story.append(make_section_table("PLASTICIZING PROFILE", section_style))
    plastic_rows = [
        ["PARAMETER", "SPEED", "PRESSURE", "POSITION"],
        ["PLASTICIZING 1", data["plastic_1_speed"],
         data["plastic_1_pressure"], data["plastic_1_position"]],
        ["PLASTICIZING 2", data["plastic_2_speed"],
         data["plastic_2_pressure"], data["plastic_2_position"]],
        ["PLASTICIZING 3", data["plastic_3_speed"],
         data["plastic_3_pressure"], data["plastic_3_position"]],
    ]
    story.append(make_grid_table(plastic_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    # --------------------------------------------------------
    # MELT / MOULD
    # --------------------------------------------------------

    melt_rows = [
        ["MELT CUSHION", data["melt_cushion"],
         "MOULD CLAMPING TONNAGE", data["mould_clamping_tonnage"]],
        ["BACK PRESSURE", data["back_pressure"],
         "SWITCHOVER SC STROKE", data["switchover_sc_stroke"]],
    ]
    story.append(make_pdf_table(melt_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    # --------------------------------------------------------
    # BARREL TEMPERATURE
    # --------------------------------------------------------

    story.append(make_section_table("BARREL TEMPERATURE", section_style))
    barrel_rows = [
        ["ZONE", "SET TEMP.", "ACTUAL TEMP."],
        ["ZONE 1", data["barrel_zone_1_set"], data["barrel_zone_1_actual"]],
        ["ZONE 2", data["barrel_zone_2_set"], data["barrel_zone_2_actual"]],
        ["ZONE 3", data["barrel_zone_3_set"], data["barrel_zone_3_actual"]],
        ["ZONE 4", data["barrel_zone_4_set"], data["barrel_zone_4_actual"]],
        ["ZONE 5", data["barrel_zone_5_set"], data["barrel_zone_5_actual"]],
    ]
    story.append(make_grid_table(barrel_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    # --------------------------------------------------------
    # HOLDING PROFILE
    # --------------------------------------------------------

    story.append(make_section_table("HOLDING PROFILE", section_style))
    holding_rows = [
        ["STEP", "PERCENTAGE", "SPEED", "PRESSURE", "HOLD TIME"],
        ["STEP-1", data["hold_step_1_pct"], data["hold_step_1_speed"],
         data["hold_step_1_pressure"], data["hold_step_1_time"]],
        ["STEP-2", data["hold_step_2_pct"], data["hold_step_2_speed"],
         data["hold_step_2_pressure"], data["hold_step_2_time"]],
        ["STEP-3", data["hold_step_3_pct"], data["hold_step_3_speed"],
         data["hold_step_3_pressure"], data["hold_step_3_time"]],
        ["STEP-4", data["hold_step_4_pct"], data["hold_step_4_speed"],
         data["hold_step_4_pressure"], data["hold_step_4_time"]],
    ]
    story.append(make_grid_table(holding_rows, label_style, value_style))
    story.append(Spacer(1, 5))

    story.append(p(
        "Tolerance: +/-20 if not specified / if required.",
        small_style
    ))
    story.append(Spacer(1, 10))

    # --------------------------------------------------------
    # SIGN-OFF
    # --------------------------------------------------------

    sign_rows = [
        ["PREPARED BY", data["prepared_by"], "APPROVED BY", data["approved_by"]],
    ]
    story.append(make_pdf_table(sign_rows, label_style, value_style))
    story.append(Spacer(1, 15))

    signature_rows = [
        ["Signature", "", "Signature", ""],
        ["Date", "", "Date", ""],
    ]
    story.append(make_pdf_table(signature_rows, label_style, value_style))

    # --------------------------------------------------------
    # PAGE NUMBER
    # --------------------------------------------------------

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7)
        canvas.drawCentredString(
            A4[0] / 2,
            5 * mm,
            f"Page {doc.page}"
        )
        canvas.restoreState()

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number
    )

    buffer.seek(0)
    return buffer.getvalue()


def make_section_table(title, style):
    t = Table([[p(title, style)]], colWidths=[190*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#e5e7eb")),
        ("BOX", (0,0), (-1,-1), 0.7, colors.black),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    return t


def make_pdf_table(rows, label_style, value_style):
    converted = []
    for row in rows:
        converted.append([
            p(row[0], label_style),
            p(row[1], value_style),
            p(row[2], label_style),
            p(row[3], value_style),
        ])

    t = Table(
        converted,
        colWidths=[38*mm, 57*mm, 38*mm, 57*mm]
    )
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.6, colors.black),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#f3f4f6")),
        ("BACKGROUND", (2,0), (2,-1), colors.HexColor("#f3f4f6")),
    ]))
    return t


def make_two_col_table(rows, label_style, value_style):
    converted = []
    for row in rows:
        converted.append([
            p(row[0], label_style),
            p(row[1], value_style)
        ])

    t = Table(converted, colWidths=[65*mm, 125*mm])
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.6, colors.black),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#f3f4f6")),
    ]))
    return t


def make_grid_table(rows, label_style, value_style):
    converted = []
    for i, row in enumerate(rows):
        converted.append([
            p(row[0], label_style if i == 0 else value_style),
            p(row[1], label_style if i == 0 else value_style),
            *[
                p(value, label_style if i == 0 else value_style)
                for value in row[2:]
            ],
        ])

    column_count = len(rows[0])
    if column_count == 5:
        col_widths = [54*mm, 34*mm, 34*mm, 34*mm, 34*mm]
    elif column_count == 4:
        col_widths = [70*mm, 40*mm, 40*mm, 40*mm]
    elif column_count == 3:
        col_widths = [70*mm, 60*mm, 60*mm]
    else:
        raise ValueError("Grid table must have three, four, or five columns")

    t = Table(converted, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.6, colors.black),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
        ("LEFTPADDING", (0,0), (-1,-1), 3),
        ("RIGHTPADDING", (0,0), (-1,-1), 3),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#e5e7eb")),
    ]))
    return t


# ============================================================
# APP HEADER
# ============================================================

header_logo, header_text = st.columns([1, 5])
with header_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=120)
with header_text:
    st.markdown(
        '<div class="app-title" style="text-align:left;">OM INDUSTRIES</div>',
        unsafe_allow_html=True
    )
    # st.markdown(
    #     '<div class="app-subtitle" style="text-align:left;">'
    #     'AUTOMOTIVE ENGINEERING COMPONENT G-64 MIDC AMBAD NASHIK 10'
    #     '</div>',
    #     unsafe_allow_html=True
    # )

# ============================================================
# HEADER / DOCUMENT DETAILS
# ============================================================

section("DOCUMENT DETAILS")

c1, c2 = st.columns(2)
with c1:
    revision_no = st.text_input("Revision No.", value="01")
with c2:
    issued_date = st.date_input("Issued Date", value=date.today())

# ============================================================
# PART DETAILS
# ============================================================

section("PART DETAILS")

part_name = text_field("Part Name", "part_name")
customer_name = text_field("Customer Name", "customer_name")
part_no = text_field("Part No.", "part_no")
machine_name = text_field("Machine Name", "machine_name")
machine_no = text_field("Machine No.", "machine_no")
mould_no = text_field("Mould No.", "mould_no")
material_name = text_field("Material Name", "material_name")
grade = text_field("Grade", "grade")
machine_tonnage = text_field("M/C Tonnage", "machine_tonnage")
master_batch = text_field("Master Batch", "master_batch")

# ============================================================
# PROCESS PARAMETERS
# ============================================================

section("PROCESS PARAMETERS")

preheating_temp = text_field("Preheating Temp. (+/-10°C)", "preheating_temp")
preheating_time = text_field("Preheating Time", "preheating_time")
cycle_time = text_field("Cycle Time [sec.]", "cycle_time")
cooling_time = text_field("Cooling Time", "cooling_time")
cavity_no = text_field("Cavity No.", "cavity_no")
mtc_temp = text_field("MTC Temp.", "mtc_temp")
shot_weight = text_field("Shot Wt. - gm (+/-2%)", "shot_weight")
part_weight = text_field("Part Wt. - gm", "part_weight")
runner_weight = text_field("Runner Wt. - gm", "runner_weight")

# ============================================================
# CLAMPING SYSTEM
# ============================================================

section("CLAMPING SYSTEM")

clamp_rows = [
    ("MOULD OPEN SLOW-1", "mould_open_slow_1"),
    ("OPEN FAST 2", "open_fast_2"),
    ("OPEN SLOW 3", "open_slow_3"),
    ("OPEN SLOW 4", "open_slow_4"),
    ("MOULD CLOSING SLOW 1", "mould_close_slow_1"),
    ("CLOSE FAST 2", "close_fast_2"),
    ("CLOSE SLOW 3", "close_slow_3"),
    ("CLOSE SLOW 4", "close_slow_4"),
]

clamp_values = {}
for label, prefix in clamp_rows:
    st.markdown(f"**{label}**")
    a, b, c, d = st.columns(4)
    with a:
        clamp_values[f"{prefix}_speed"] = st.text_input("Speed", key=f"{prefix}_speed", placeholder="Speed")
    with b:
        clamp_values[f"{prefix}_pressure"] = st.text_input("Pressure", key=f"{prefix}_pressure", placeholder="Pressure")
    with c:
        clamp_values[f"{prefix}_position"] = st.text_input("Position", key=f"{prefix}_position", placeholder="Position")
    with d:
        clamp_values[f"{prefix}_time"] = st.text_input("Time", key=f"{prefix}_time", placeholder="Time")

# ============================================================
# EJECTOR SETTING
# ============================================================

section("EJECTOR SETTING")

ejector_rows = [
    ("EJECTOR FORWARD 1", "ejector_forward_1"),
    ("EJECTOR FORWARD 2", "ejector_forward_2"),
    ("EJECTOR RETURN 1", "ejector_return_1"),
    ("EJECTOR RETURN 2", "ejector_return_2"),
]

ejector_values = {}
for label, prefix in ejector_rows:
    st.markdown(f"**{label}**")
    a, b, c, d = st.columns(4)
    with a:
        ejector_values[f"{prefix}_speed"] = st.text_input("Speed", key=f"{prefix}_speed", placeholder="Speed")
    with b:
        ejector_values[f"{prefix}_pressure"] = st.text_input("Pressure", key=f"{prefix}_pressure", placeholder="Pressure")
    with c:
        ejector_values[f"{prefix}_position"] = st.text_input("Position", key=f"{prefix}_position", placeholder="Position")
    with d:
        ejector_values[f"{prefix}_time"] = st.text_input("Time", key=f"{prefix}_time", placeholder="Time")

# ============================================================
# CORE SETTING
# ============================================================

section("CORE SETTING")

core_1_in = text_field("CORE 1 (IN)", "core_1_in")
core_1_out = text_field("CORE 1 (OUT)", "core_1_out")
core_time = text_field("Time", "core_time")

# ============================================================
# INJECTION SETTING
# ============================================================

section("INJECTION SETTING")

injection_rows = [
    ("INJECTION 1", "injection_1"),
    ("INJECTION 2", "injection_2"),
    ("INJECTION 3", "injection_3"),
]

injection_values = {}
for label, prefix in injection_rows:
    st.markdown(f"**{label}**")
    a, b, c, d = st.columns(4)
    with a:
        injection_values[f"{prefix}_speed"] = st.text_input("Speed", key=f"{prefix}_speed", placeholder="Speed")
    with b:
        injection_values[f"{prefix}_pressure"] = st.text_input("Pressure", key=f"{prefix}_pressure", placeholder="Pressure")
    with c:
        injection_values[f"{prefix}_position"] = st.text_input("Position", key=f"{prefix}_position", placeholder="Position")
    with d:
        injection_values[f"{prefix}_time"] = st.text_input("Time", key=f"{prefix}_time", placeholder="Time")

# ============================================================
# PLASTICIZING PROFILE
# ============================================================

section("PLASTICIZING PROFILE")

plastic_rows = [
    ("PLASTICIZING 1", "plastic_1"),
    ("PLASTICIZING 2", "plastic_2"),
    ("PLASTICIZING 3", "plastic_3"),
]

plastic_values = {}
for label, prefix in plastic_rows:
    st.markdown(f"**{label}**")
    a, b, c = st.columns(3)
    with a:
        plastic_values[f"{prefix}_speed"] = st.text_input("Speed", key=f"{prefix}_speed", placeholder="Speed")
    with b:
        plastic_values[f"{prefix}_pressure"] = st.text_input("Pressure", key=f"{prefix}_pressure", placeholder="Pressure")
    with c:
        plastic_values[f"{prefix}_position"] = st.text_input("Position", key=f"{prefix}_position", placeholder="Position")

# ============================================================
# MELT / MOULD
# ============================================================

section("MELT CUSHION / MOULD CLAMPING")

melt_cushion = text_field("Melt Cushion", "melt_cushion")
mould_clamping_tonnage = text_field("Mould Clamping Tonnage", "mould_clamping_tonnage")
back_pressure = text_field("Back Pressure", "back_pressure")
switchover_sc_stroke = text_field("Switchover SC Stroke", "switchover_sc_stroke")

# ============================================================
# BARREL TEMPERATURE
# ============================================================

section("BARREL TEMPERATURE")

barrel_values = {}

for i in range(1, 6):
    st.markdown(f"**Zone {i}**")
    a, b = st.columns(2)
    with a:
        barrel_values[f"barrel_zone_{i}_set"] = st.text_input(
            "Set Temp.",
            key=f"barrel_zone_{i}_set",
            placeholder="Set temperature"
        )
    with b:
        barrel_values[f"barrel_zone_{i}_actual"] = st.text_input(
            "Actual Temp.",
            key=f"barrel_zone_{i}_actual",
            placeholder="Actual temperature"
        )

# ============================================================
# HOLDING PROFILE
# ============================================================

section("HOLDING PROFILE")

st.caption("Tolerance: +/-20 if not specified / if required.")

holding_values = {}

for i in range(1, 5):
    st.markdown(f"**STEP-{i}**")
    a, b, c, d = st.columns(4)

    with a:
        holding_values[f"hold_step_{i}_pct"] = st.text_input(
            "Percentage",
            key=f"hold_step_{i}_pct",
            value="20 %"
        )
    with b:
        holding_values[f"hold_step_{i}_speed"] = st.text_input(
            "Speed",
            key=f"hold_step_{i}_speed",
            placeholder="Speed"
        )
    with c:
        holding_values[f"hold_step_{i}_pressure"] = st.text_input(
            "Pressure",
            key=f"hold_step_{i}_pressure",
            placeholder="Pressure"
        )
    with d:
        holding_values[f"hold_step_{i}_time"] = st.text_input(
            "Hold Time",
            key=f"hold_step_{i}_time",
            placeholder="Hold time"
        )

# ============================================================
# APPROVAL
# ============================================================

section("AUTHORIZATION")

prepared_by = text_field("Prepared By", "prepared_by")
approved_by = text_field("Approved By", "approved_by")

# ============================================================
# COLLECT DATA
# ============================================================

data = {
    "revision_no": revision_no,
    "issued_date": issued_date.strftime("%d.%m.%Y"),
    "part_name": part_name,
    "customer_name": customer_name,
    "part_no": part_no,
    "machine_name": machine_name,
    "machine_no": machine_no,
    "mould_no": mould_no,
    "material_name": material_name,
    "grade": grade,
    "machine_tonnage": machine_tonnage,
    "master_batch": master_batch,
    "preheating_temp": preheating_temp,
    "preheating_time": preheating_time,
    "cycle_time": cycle_time,
    "cooling_time": cooling_time,
    "cavity_no": cavity_no,
    "mtc_temp": mtc_temp,
    "shot_weight": shot_weight,
    "part_weight": part_weight,
    "runner_weight": runner_weight,
    "core_1_in": core_1_in,
    "core_1_out": core_1_out,
    "core_time": core_time,
    "melt_cushion": melt_cushion,
    "mould_clamping_tonnage": mould_clamping_tonnage,
    "back_pressure": back_pressure,
    "switchover_sc_stroke": switchover_sc_stroke,
    "prepared_by": prepared_by,
    "approved_by": approved_by,
    **clamp_values,
    **ejector_values,
    **injection_values,
    **plastic_values,
    **barrel_values,
    **holding_values,
}

# ============================================================
# GENERATE PDF
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="download-note">'
    '<b>Ready to create the document?</b><br>'
    'Click the button below. The application will generate the completed '
    'process sheet as a PDF. There is no database submit required.'
    '</div>',
    unsafe_allow_html=True
)

if st.button("📄 Generate PDF", type="primary", use_container_width=True):
    with st.spinner("Generating PDF..."):
        pdf_bytes = build_pdf(data)
        st.session_state["pdf_bytes"] = pdf_bytes

if "pdf_bytes" in st.session_state:
    st.success("PDF generated successfully.")

    st.download_button(
        label="⬇️ Download Process Sheet PDF",
        data=st.session_state["pdf_bytes"],
        file_name=f"Process_Sheet_{part_no or 'New'}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

