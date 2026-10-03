"""
build_pptx.py - Native Editable PPTX Generator for AgroStruxure™
Yuva Yodha Energy Tech Hackathon 2026 (Schneider Electric India)
Challenge 01: Sustainable Agriculture (Energy, Water & Productivity)
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# DESIGN SYSTEM TOKENS (RGB)
# -------------------------------------------------------------
COLOR_CANVAS = RGBColor(11, 17, 21)        # #0B1115
COLOR_CARD = RGBColor(21, 26, 28)          # #151A1C
COLOR_PANEL = RGBColor(29, 36, 40)         # #1D2428
COLOR_BORDER = RGBColor(36, 45, 50)        # #242D32

COLOR_PRIMARY = RGBColor(61, 205, 88)      # #3DCD58 (Schneider Green)
COLOR_EMERALD = RGBColor(13, 135, 82)      # #0D8752
COLOR_DEEP_FOREST = RGBColor(2, 66, 48)    # #024230
COLOR_SOLAR = RGBColor(255, 206, 0)        # #FFCE00 (Solar Irradiance Gold)
COLOR_CUTOFF = RGBColor(0, 135, 205)       # #0087CD (Water Cutoff Blue)
COLOR_COOLING = RGBColor(181, 116, 255)    # #B574FF (Cold Chain Purple)
COLOR_ALARM = RGBColor(220, 10, 10)        # #DC0A0A (Alarm Red)

COLOR_TEXT_PRIMARY = RGBColor(255, 255, 255)
COLOR_TEXT_SECONDARY = RGBColor(159, 160, 164)
COLOR_TEXT_MUTED = RGBColor(98, 100, 105)

FONT_HEADING = "Trebuchet MS"
FONT_BODY = "Segoe UI"
FONT_MONO = "Consolas"

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
def set_shape_flat(shape, fill_color, line_color=None, line_width=1):
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()

def create_slide_base(prs):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    set_shape_flat(bg, COLOR_CANVAS)
    return slide

def add_header(slide, category_text, subcategory_text=""):
    # Header container
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.4), Inches(9.5), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = f"YUVA YODHA 2026 · {category_text.upper()}"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    
    if subcategory_text:
        run = p.add_run()
        run.text = f"  |  {subcategory_text}"
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_SECONDARY

    # Schneider Electric corporate badge
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.8), Inches(0.35), Inches(1.9), Inches(0.42))
    set_shape_flat(badge, COLOR_EMERALD)
    bp = badge.text_frame.paragraphs[0]
    bp.text = "Schneider Electric"
    bp.alignment = PP_ALIGN.CENTER
    bp.font.name = FONT_HEADING
    bp.font.size = Pt(11)
    bp.font.bold = True
    bp.font.color.rgb = COLOR_TEXT_PRIMARY

def add_footer(slide, sources_text, slide_num_str):
    # Divider line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(6.9), Inches(12.13), Inches(0.015))
    set_shape_flat(line, COLOR_BORDER)

    # Source citation
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(6.95), Inches(10.5), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = f"Sources: {sources_text}"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_TEXT_MUTED

    # Slide number
    tb2 = slide.shapes.add_textbox(Inches(11.2), Inches(6.95), Inches(1.5), Inches(0.4))
    p2 = tb2.text_frame.paragraphs[0]
    p2.text = f"SLIDE {slide_num_str} / 10"
    p2.alignment = PP_ALIGN.RIGHT
    p2.font.name = FONT_MONO
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_MUTED

def add_title_area(slide, title_text, subtitle_text):
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.85), Inches(12.13), Inches(0.95))
    p1 = tb.text_frame.paragraphs[0]
    p1.text = title_text
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_PRIMARY
    
    p2 = tb.text_frame.add_paragraph()
    p2.text = subtitle_text
    p2.font.name = FONT_BODY
    p2.font.size = Pt(12)
    p2.font.color.rgb = COLOR_TEXT_SECONDARY
    p2.space_before = Pt(4)

def format_cell(cell, text, font_size=10, bold=False, color=COLOR_TEXT_PRIMARY, bg_color=None, align=PP_ALIGN.LEFT):
    cell.text = text
    p = cell.text_frame.paragraphs[0]
    p.alignment = align
    p.font.name = FONT_BODY
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    if bg_color:
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color


# -------------------------------------------------------------
# SLIDE BUILDERS (1 TO 10)
# -------------------------------------------------------------

def build_slide_01(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Energy Tech Hackathon 2026", "Track: Challenge 01 — Sustainable Agriculture")
    add_footer(slide, "CGWB Assessment (2023) · NABCONS / MoFPI Post-Harvest Study (2022) · impact_model.py", "01")

    # Left content box
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(1.2), Inches(6.5), Inches(3.2))
    p1 = tb.text_frame.paragraphs[0]
    p1.text = "OFF-GRID SOLAR AGRI-ENERGY MICROGRID"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_PRIMARY

    p2 = tb.text_frame.add_paragraph()
    p2.text = "AgroStruxure™"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(44)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(6)

    p3 = tb.text_frame.add_paragraph()
    p3.text = "Solar-Synchronized Agri-Energy Microgrid & Closed-Loop Precision Irrigation"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(16)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TEXT_PRIMARY
    p3.space_before = Pt(8)

    p4 = tb.text_frame.add_paragraph()
    p4.text = "Monetizing agricultural water conservation by coupling PM-KUSUM Component B solar pump arrays with on-farm pre-cooling—turning unpumped groundwater into perishable shelf life."
    p4.font.name = FONT_BODY
    p4.font.size = Pt(12)
    p4.font.color.rgb = COLOR_TEXT_SECONDARY
    p4.space_before = Pt(12)

    # 4 Metric Cards (Bottom-Left)
    metrics = [
        ("41.2%", "Water Saved", "7,000 m³/ha/yr conserved", COLOR_PRIMARY),
        ("1,696", "kWh Freed", "Pumping power freed/yr", COLOR_CUTOFF),
        ("1.31 t", "Produce Saved", "Farm-gate heat eliminated", COLOR_COOLING),
        ("2.0 Yrs", "Cluster Payback", "2 crop seasons (Tier A)", COLOR_SOLAR)
    ]
    card_w = Inches(1.52)
    gap = Inches(0.12)
    for i, (m_num, m_lbl, m_desc, m_col) in enumerate(metrics):
        x = Inches(0.6) + i * (card_w + gap)
        y = Inches(4.7)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, Inches(1.9))
        set_shape_flat(card, COLOR_CARD, COLOR_BORDER)
        
        tb_m = slide.shapes.add_textbox(x, y + Inches(0.1), card_w, Inches(1.7))
        p = tb_m.text_frame.paragraphs[0]
        p.text = m_num
        p.font.name = FONT_HEADING
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = m_col
        
        p_lbl = tb_m.text_frame.add_paragraph()
        p_lbl.text = m_lbl.upper()
        p_lbl.font.name = FONT_BODY
        p_lbl.font.size = Pt(9)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = COLOR_TEXT_PRIMARY
        p_lbl.space_before = Pt(4)

        p_desc = tb_m.text_frame.add_paragraph()
        p_desc.text = m_desc
        p_desc.font.name = FONT_BODY
        p_desc.font.size = Pt(8.5)
        p_desc.font.color.rgb = COLOR_TEXT_MUTED
        p_desc.space_before = Pt(4)

    # Right Image Hero
    img_path = os.path.join("assets", "solar_panels_farm_opt.jpg")
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(7.3), Inches(1.2), Inches(5.4), Inches(4.3))
        # Overlay box
        ov = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.3), Inches(5.6), Inches(5.4), Inches(1.0))
        set_shape_flat(ov, COLOR_CARD, COLOR_BORDER)
        tb_o = slide.shapes.add_textbox(Inches(7.4), Inches(5.65), Inches(5.2), Inches(0.9))
        po = tb_o.text_frame.paragraphs[0]
        po.text = "● SCHNEIDER ECOSTRUXURE TELEMETRY | NODE ID: MH-NSK-042"
        po.font.name = FONT_MONO
        po.font.size = Pt(9)
        po.font.bold = True
        po.font.color.rgb = COLOR_PRIMARY
        
        po2 = tb_o.text_frame.add_paragraph()
        po2.text = "DC Bus: 520V DC  |  Drive Speed: 44.2 Hz  |  Root Moisture: 38.4%  |  State: PV_SHARED_TIME"
        po2.font.name = FONT_MONO
        po2.font.size = Pt(9)
        po2.font.color.rgb = COLOR_TEXT_PRIMARY
        po2.space_before = Pt(3)


def build_slide_02(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Problem Definition", "Structural Bottlenecks in Indian Smallholder Agriculture")
    add_title_area(slide, "The Dual Agricultural Crisis: Aquifer Depletion & Farm-Gate Spoilage",
                   "India extracts more groundwater than China and the US combined—while ₹1.53 Lakh Crore of food rots at the farm gate.")
    add_footer(slide, "CGWB Dynamic Ground Water Assessment (2023) · CEA Energy Statistics (2024) · NABCONS / MoFPI (2022)", "02")

    # Card 1: Groundwater Depletion
    card1 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.9), Inches(5.9), Inches(4.8))
    set_shape_flat(card1, COLOR_CARD, COLOR_ALARM, line_width=1.5)
    
    tb1 = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(5.5), Inches(4.5))
    p = tb1.text_frame.paragraphs[0]
    p.text = "CRISIS 1: AQUIFER EXHAUSTION"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_ALARM

    p2 = tb1.text_frame.add_paragraph()
    p2.text = "245 BCM / Year"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_ALARM
    p2.space_before = Pt(4)

    p3 = tb1.text_frame.add_paragraph()
    p3.text = "Total Annual National Groundwater Extraction (CGWB 2023)"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TEXT_PRIMARY
    p3.space_before = Pt(2)

    bullets1 = [
        "87% Dedicated to Agriculture: Irrigation extracts 213 BCM/year, dwarfing domestic (11%) and industrial (2%) usage.",
        "1,114 Assessment Units Over-Exploited: Extraction exceeds annual replenishable recharge across key agrarian states.",
        "255,000 GWh Power Drain: Agricultural pumping consumes 16.53% of all Indian electricity (CEA 2024).",
        "Pumping Fleet Scale: 21.5M electric pumps, 8.5M diesel pumps, and 10.9L standalone solar pumps (PM-KUSUM)."
    ]
    for b in bullets1:
        pb = tb1.text_frame.add_paragraph()
        pb.text = f"▪  {b}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = COLOR_TEXT_SECONDARY
        pb.space_before = Pt(8)

    # Card 2: Food Spoilage
    card2 = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.9), Inches(4.8))
    set_shape_flat(card2, COLOR_CARD, COLOR_SOLAR, line_width=1.5)

    tb2 = slide.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.5), Inches(4.5))
    p = tb2.text_frame.paragraphs[0]
    p.text = "CRISIS 2: PERISHABLE VALUE COLLAPSE"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR

    p2 = tb2.text_frame.add_paragraph()
    p2.text = "₹1.53 Lakh Crore"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_SOLAR
    p2.space_before = Pt(4)

    p3 = tb2.text_frame.add_paragraph()
    p3.text = "Annual Post-Harvest Economic Loss in India (NABCONS 2022)"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TEXT_PRIMARY
    p3.space_before = Pt(2)

    bullets2 = [
        "8.37% Farm-Gate Tomato Spoilage: High respiration heat at harvest (32°C+) causes rapid decay within 48 hours.",
        "Mandi Distress Selling: Lacking cold storage, smallholders dump produce for ₹2–4/kg to middlemen to avoid total rot.",
        "Distal Cold Storage Failure: Commercial cold chains operate 30–50 km away in district hubs—unreachable for smallholders.",
        "Smallholder Vulnerability: 86.2% of Indian landholdings are small/marginal (<2.0 ha, average 1.08 ha)."
    ]
    for b in bullets2:
        pb = tb2.text_frame.add_paragraph()
        pb.text = f"▪  {b}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = COLOR_TEXT_SECONDARY
        pb.space_before = Pt(8)


def build_slide_03(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Systemic Analysis", "Why Technology Without Economic Alignment Fails")
    add_title_area(slide, "The Solar Rebound Paradox: Why Free Power Wastes Water",
                   "PM-KUSUM deployed 10.9 lakh standalone pumps, but zero marginal operating cost induces the Jevons paradox.")
    add_footer(slide, "Gupta (2019) Energy Policy 129:598 · Shah et al. (2016) IWMI-Tata SPaRC · impact_model.py §2a", "03")

    # Left: Econometric evidence card
    card_l = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.9), Inches(5.9), Inches(4.8))
    set_shape_flat(card_l, COLOR_CARD, COLOR_BORDER)

    tb_l = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(5.5), Inches(4.5))
    p = tb_l.text_frame.paragraphs[0]
    p.text = "THE REBOUND MECHANISM (JEVONS PARADOX)"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR

    p2 = tb_l.text_frame.add_paragraph()
    p2.text = "+16% to +39%"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_SOLAR
    p2.space_before = Pt(4)

    p3 = tb_l.text_frame.add_paragraph()
    p3.text = "Measured Increase in Groundwater Extraction Post-Solar Adoption"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TEXT_PRIMARY
    p3.space_before = Pt(2)

    bullets = [
        "Zero Marginal Operating Cost: Replacing ₹80/hour diesel pumps with solar removes all financial constraints on pumping time.",
        "Empirical Proof: Econometric field measurement in Rajasthan (Gupta, 2019) confirmed significant extraction expansion.",
        "The Advisory Trap: Telling smallholders to pump less fails because unconsumed solar electricity has ₹0 off-grid cash value.",
        "Systemic Mandate: Water conservation must be coupled with an immediate physical and economic benefit."
    ]
    for b in bullets:
        pb = tb_l.text_frame.add_paragraph()
        pb.text = f"▪  {b}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = COLOR_TEXT_SECONDARY
        pb.space_before = Pt(8)

    # Right: The Wasted Asset & Flawed Status Quo
    card_r = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.9), Inches(4.8))
    set_shape_flat(card_r, COLOR_CARD, COLOR_BORDER)

    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.5), Inches(1.8))
    p = tb_r.text_frame.paragraphs[0]
    p.text = "THE 63% IDLE SOLAR ENERGY REALITY"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_CUTOFF

    p2 = tb_r.text_frame.add_paragraph()
    p2.text = "4,137 kWh / Year Sits Idle"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_CUTOFF
    p2.space_before = Pt(4)

    p3 = tb_r.text_frame.add_paragraph()
    p3.text = "A 4.8 kWp pump array generates 6,559 kWh/yr; scheduled drip uses 2,422 kWh (37%). 63% is completely wasted without alternative loads (Shah et al., IWMI)."
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = COLOR_TEXT_SECONDARY
    p3.space_before = Pt(4)

    # Table of flawed competitors
    table_shape = slide.shapes.add_table(4, 3, Inches(7.0), Inches(3.9), Inches(5.5), Inches(2.6))
    table = table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(1.8)
    table.columns[2].width = Inches(1.9)

    headers = ["Player / Tech", "Current Model", "The Critical Flaw"]
    for c_idx, h in enumerate(headers):
        format_cell(table.cell(0, c_idx), h, font_size=9.5, bold=True, color=COLOR_TEXT_SECONDARY, bg_color=COLOR_PANEL)

    rows = [
        ("Solar Cold Rooms (Ecozen)", "Dedicated PV + Cold Room", "Forces 2nd PV array (₹91k wasted capex)"),
        ("IoT Advisory Apps (Fasal)", "Soil moisture alerts on phone", "No actuation; cannot stop over-pumping"),
        ("GSM Pump Starters", "Remote phone motor on/off", "Convenience accelerates aquifer depletion")
    ]
    for r_idx, (c0, c1, c2) in enumerate(rows):
        format_cell(table.cell(r_idx + 1, 0), c0, font_size=9, bold=True, color=COLOR_TEXT_PRIMARY, bg_color=COLOR_CARD)
        format_cell(table.cell(r_idx + 1, 1), c1, font_size=9, color=COLOR_TEXT_SECONDARY, bg_color=COLOR_CARD)
        format_cell(table.cell(r_idx + 1, 2), c2, font_size=9, color=COLOR_ALARM, bg_color=COLOR_CARD)


def build_slide_04(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Solution Blueprint", "Direct Mapping to Challenge 01 Expected Outcomes")
    add_title_area(slide, "AgroStruxure™: Monetizing Water Conservation",
                   "A shared-array agri-energy microgrid that enforces a volumetric water entitlement and diverts freed solar power to cooling.")
    add_footer(slide, "100% of figures verified against impact_model.py and official Challenge 01 rubric", "04")

    # Banner: Core Innovation
    ban = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.9), Inches(12.13), Inches(0.65))
    set_shape_flat(ban, COLOR_DEEP_FOREST, COLOR_PRIMARY, line_width=1)
    tb_b = slide.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(11.7), Inches(0.55))
    p = tb_b.text_frame.paragraphs[0]
    p.text = "CORE INNOVATION: Physical time-sharing between PM-KUSUM PV array + Schneider Altivar ATV320 VFD + TeSys D Contactor + 2 MT Pre-Cooler"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY

    # 4 Quadrants
    quads = [
        ("1. REDUCE ENERGY & WATER INTENSITY", "41.2% Water Saved",
         "Local FAO-56 Penman-Monteith water budgeting with dual-depth capacitive FDR probes. Cuts seasonal irrigation from 850 mm (flood) to 500 mm (pulsed drip), saving 7,000 m³/ha/yr.",
         "Pumping Power Freed: 1,696 kWh/ha/yr", COLOR_PRIMARY),
        ("2. MINIMIZE POST-HARVEST LOSSES", "1.31 Tonnes Preserved",
         "Captures 3,187 kWh/yr (77%) of idle midday solar surplus to drive an on-farm 2 MT PCM pre-cooler at 12°C. Reduces farm-gate tomato spoilage from 8.37% down to 4.00% (NABCONS 2022).",
         "Preserved Value: +₹15,732/ha/yr", COLOR_COOLING),
        ("3. EMPOWER THE SMALLHOLDER", "2.0-Yr Cluster Payback",
         "Affordable industrial retrofit BOM (₹7,540 at 1,000 units). Delivers spoken vernacular audio advisories in Marathi and Hindi over WhatsApp (Krishi Mitra). 4-farm cluster net gain: ₹25,332/yr.",
         "Cluster Capex: ₹50,212 per farm (net)", COLOR_SOLAR),
        ("4. STRENGTHEN CLIMATE RESILIENCE", "2.94 t CO₂e Abated",
         "Locks water extraction to CGWB/Atal Bhujal block budgets; 100% thick-edge execution on ESP32-S3 with 90-day offline flash buffer; prevents dry-run and protects deep Deccan aquifers.",
         "Displaced Diesel & Spoilage GHG: 2.94 t/ha/yr", COLOR_CUTOFF)
    ]

    for idx, (q_title, q_badge, q_body, q_foot, q_color) in enumerate(quads):
        row = idx // 2
        col = idx % 2
        x = Inches(0.6) + col * Inches(6.2)
        y = Inches(2.7) + row * Inches(2.05)
        
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.93), Inches(1.9))
        set_shape_flat(card, COLOR_CARD, q_color, line_width=1)

        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), Inches(5.5), Inches(1.65))
        p = tb.text_frame.paragraphs[0]
        p.text = q_title
        p.font.name = FONT_BODY
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = q_color

        run = p.add_run()
        run.text = f"  ({q_badge})"
        run.font.bold = True
        run.font.color.rgb = COLOR_TEXT_PRIMARY

        pb = tb.text_frame.add_paragraph()
        pb.text = q_body
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = COLOR_TEXT_SECONDARY
        pb.space_before = Pt(4)

        pf = tb.text_frame.add_paragraph()
        pf.text = f"Key Metric: {q_foot}"
        pf.font.name = FONT_MONO
        pf.font.size = Pt(9.5)
        pf.font.bold = True
        pf.font.color.rgb = q_color
        pf.space_before = Pt(6)


def build_slide_05(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Operational Journey", "Closed-Loop Diurnal Hydraulics & Fail-Safe Automation")
    add_title_area(slide, "Closed-Loop Precision Hydraulics & Diurnal Journey",
                   "A deterministic 24-hour cycle: soft-start drip irrigation, field-capacity cutoff, and zero-flow valve latching.")
    add_footer(slide, "CiA402 Drive Profile (NVE41308) · FAO-56 Penman-Monteith · FreeRTOS Deterministic Tasks", "05")

    # Diurnal Timeline Bar Box
    bar_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.9), Inches(12.13), Inches(1.1))
    set_shape_flat(bar_box, COLOR_CARD, COLOR_BORDER)

    tb_b = slide.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(11.7), Inches(0.95))
    p = tb_b.text_frame.paragraphs[0]
    p.text = "DIURNAL POWER SCRUBBER (06:00 SUNRISE TO 18:00 SUNSET)"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_SECONDARY

    p2 = tb_b.text_frame.add_paragraph()
    p2.text = "[06:00-08:30 Standby PV<200W] ⟶ [08:30-11:30 IRRIGATE: Altivar ATV320 VFD 38-50Hz] ⟶ [11:30: 5s DEAD-BAND DWELL] ⟶ [11:30-15:30 PRE-COOL: 2 MT PCM Cold Room 3.43kW] ⟶ [15:30-18:00 Overnight PCM Hold]"
    p2.font.name = FONT_MONO
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PRIMARY
    p2.space_before = Pt(4)

    # 3 Columns
    cols_data = [
        ("DUAL-DEPTH SENSING", COLOR_CUTOFF, [
            "10cm Surface Probe: Tracks evaporation rate and crusting dynamics.",
            "30cm Root-Zone Probe: Monitors active transpiration and root depletion.",
            "Dynamic Thresholds: Field Capacity cutoff at 45%; Permanent Wilting threshold at 18%.",
            "Hydrological Modeling: Inputs dual FDR + solar pyranometer into FAO-56 Penman-Monteith balance."
        ]),
        ("ANTI-WATER HAMMER SEQUENCE", COLOR_PRIMARY, [
            "Step 1: Daily quota reached (3,500 L) or root zone achieves 45% Field Capacity.",
            "Step 2: Gateway commands Altivar VFD to decelerate from 48 Hz to 0 Hz over 8 seconds.",
            "Step 3: Pulse flow meter confirms zero flow (Q = 0 LPM); latching valve closes safely.",
            "Step 4: 5-second dead-band dwell discharges DC bus capacitors before TeSys changeover."
        ]),
        ("WHATSAPP VOICE ADVISORY", COLOR_SOLAR, [
            "Vernacular Audio Note: Dispatched in Marathi & Hindi via WhatsApp Krishi Mitra.",
            "Actionable Message: 'Ram-bhau, 3,500 L delivered today. Soil moisture is 44%. Solar diverted to 2 MT cold room.'",
            "Zero Hallucination: LLM strictly reads structured JSON data; has zero actuation authority.",
            "Smallholder Simplicity: No complex dashboard; operates like a familiar voice note."
        ])
    ]

    card_w = Inches(3.85)
    gap = Inches(0.29)
    for i, (c_title, c_color, c_points) in enumerate(cols_data):
        x = Inches(0.6) + i * (card_w + gap)
        y = Inches(3.2)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, Inches(3.5))
        set_shape_flat(card, COLOR_CARD, c_color, line_width=1)

        tb = slide.shapes.add_textbox(x + Inches(0.2), y + Inches(0.15), card_w - Inches(0.4), Inches(3.2))
        p = tb.text_frame.paragraphs[0]
        p.text = c_title
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_color

        for pt in c_points:
            pb = tb.text_frame.add_paragraph()
            pb.text = f"▪  {pt}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = COLOR_TEXT_SECONDARY
            pb.space_before = Pt(8)


def build_slide_06(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Technical Architecture", "EcoStruxure™ 3-Tier Integration & Upstream DC Changeover")
    add_title_area(slide, "Schneider EcoStruxure™ Architecture & Power Topology",
                   "Engineered break-before-make upstream DC changeover with 5-second dead-band eliminates drive stress.")
    add_footer(slide, "Altivar Solar ATV320 Manual NVE41308 · TeSys D Contactor Interlock Catalog · CiA402 Standard", "06")

    # Left: 3-Tier EcoStruxure Stack
    card_l = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.9), Inches(5.9), Inches(4.8))
    set_shape_flat(card_l, COLOR_CARD, COLOR_BORDER)

    tb_l = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(5.5), Inches(4.5))
    p = tb_l.text_frame.paragraphs[0]
    p.text = "ECOSTRUXURE™ 3-TIER STACK INTEGRATION"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    tiers = [
        ("Tier 3: Apps, Analytics & Services (EcoStruxure Cloud)", COLOR_COOLING, [
            "Agronomic digital twin with Sentinel-2 10m NDVI/NDWI satellite ingestion.",
            "Deterministic Krishi Mitra vernacular copilot (Marathi/Hindi).",
            "PM-KUSUM RMS & Central Aquifer Depletion Monitoring Portal."
        ]),
        ("Tier 2: Edge Control (EcoStruxure Edge Gateway)", COLOR_PRIMARY, [
            "ESP32-S3 FreeRTOS gateway running 100% thick-edge control loop.",
            "Modbus RTU Master Engine operating CiA402 profile over isolated RS485.",
            "Deterministic 3-layer entitlement engine & 90-day offline flash FIFO."
        ]),
        ("Tier 1: Connected Products & Switchgear", COLOR_CUTOFF, [
            "Schneider Altivar Solar ATV320 VFD (MPPT tracking, dry-run protection).",
            "Schneider TeSys D Contactors (2x LC1D09BD, mechanical & electrical interlock).",
            "Dual FDR soil probes, pulse flow meter, latching valve, pyranometer."
        ])
    ]
    for t_name, t_color, t_bullets in tiers:
        pt = tb_l.text_frame.add_paragraph()
        pt.text = t_name
        pt.font.name = FONT_BODY
        pt.font.size = Pt(10.5)
        pt.font.bold = True
        pt.font.color.rgb = t_color
        pt.space_before = Pt(8)
        for b in t_bullets:
            pb = tb_l.text_frame.add_paragraph()
            pb.text = f"  • {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(9)
            pb.font.color.rgb = COLOR_TEXT_SECONDARY
            pb.space_before = Pt(2)

    # Right: Upstream DC Power Changeover & Register Map
    card_r = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.9), Inches(4.8))
    set_shape_flat(card_r, COLOR_CARD, COLOR_BORDER)

    tb_r = slide.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.5), Inches(4.5))
    p = tb_r.text_frame.paragraphs[0]
    p.text = "UPSTREAM DC BUS POWER TOPOLOGY"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR

    p2 = tb_r.text_frame.add_paragraph()
    p2.text = "PV Array (4.8 kWp, 350-600V DC) ⟶ DC SPD ⟶ TeSys D Changeover ⟶"
    p2.font.name = FONT_MONO
    p2.font.size = Pt(9.5)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_PRIMARY
    p2.space_before = Pt(6)

    paths = [
        ("Position 1 (08:30–11:30 AM):", "Schneider Altivar Solar ATV320 VFD ⟶ 5 HP Submersible Pump."),
        ("5-Second Deadband Dwell:", "Both contactors de-energized; DC bus bleeds below 50V DC."),
        ("Position 2 (11:30 AM–15:30 PM):", "Inverter ⟶ 2 MT Phase Change Material Pre-Cooler (12°C).")
    ]
    for p_lbl, p_val in paths:
        pp = tb_r.text_frame.add_paragraph()
        pp.text = f"▪ {p_lbl} {p_val}"
        pp.font.name = FONT_BODY
        pp.font.size = Pt(9.5)
        pp.font.color.rgb = COLOR_TEXT_SECONDARY
        pp.space_before = Pt(6)

    # Safety proof callout
    p_sf = tb_r.text_frame.add_paragraph()
    p_sf.text = "CRITICAL ELECTRICAL SAFETY PROOF:"
    p_sf.font.name = FONT_BODY
    p_sf.font.size = Pt(10)
    p_sf.font.bold = True
    p_sf.font.color.rgb = COLOR_ALARM
    p_sf.space_before = Pt(12)

    p_sfd = tb_r.text_frame.add_paragraph()
    p_sfd.text = "Switching contactors downstream on a running VFD causes destructive V = L·di/dt inductive voltage spikes and trips drive fault codes. Switching upstream on the DC bus with an engineered 5-second deadband dwell protects both motor windings and inverter electronics."
    p_sfd.font.name = FONT_BODY
    p_sfd.font.size = Pt(9)
    p_sfd.font.color.rgb = COLOR_TEXT_SECONDARY
    p_sfd.space_before = Pt(3)

    # Modbus registers
    p_mb = tb_r.text_frame.add_paragraph()
    p_mb.text = "CiA402 Registers: 8501 (CMD Word) | 8502 (Target Speed) | 3201 (Status ETA) | 3207 (DC Bus V)"
    p_mb.font.name = FONT_MONO
    p_mb.font.size = Pt(8.5)
    p_mb.font.bold = True
    p_mb.font.color.rgb = COLOR_PRIMARY
    p_mb.space_before = Pt(10)


def build_slide_07(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Competitive Strategy", "Why AgroStruxure Dominates Legacy and Point Solutions")
    add_title_area(slide, "System Innovation & Competitive Defense",
                   "A multi-vector moat: time-shared solar PV capex, closed-loop entitlement governance, and thick-edge reliability.")
    add_footer(slide, "Analysis against Ecozen Solutions Ecotron/Ecofrost · Fasal Cultyvate · IWMI Dhundi SPaRC Model", "07")

    # 5-Column Table
    table_shape = slide.shapes.add_table(7, 5, Inches(0.6), Inches(1.9), Inches(8.5), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(1.6)
    table.columns[2].width = Inches(1.7)
    table.columns[3].width = Inches(1.6)
    table.columns[4].width = Inches(1.8)

    headers = ["Feature Dimension", "Conventional Solar", "Ecozen Solutions", "Fasal / IoT Apps", "AgroStruxure™ (Ours)"]
    for c_idx, h in enumerate(headers):
        bg = COLOR_DEEP_FOREST if c_idx == 4 else COLOR_PANEL
        col = COLOR_PRIMARY if c_idx == 4 else COLOR_TEXT_SECONDARY
        format_cell(table.cell(0, c_idx), h, font_size=9.5, bold=True, color=col, bg_color=bg)

    rows = [
        ("Solar Asset Sizing", "Pump only (63% wasted)", "2 Separate PV Arrays", "N/A (Grid/Battery IoT)", "1 Shared Array (Saves ₹91k)"),
        ("Water Governance", "Unconstrained pumping", "Unconstrained pumping", "Advisory graphs only", "Volumetric Rebound Lock"),
        ("Automated Actuation", "Manual knife switch", "Independent inverters", "Zero actuation", "Automated TeSys DC Changeover"),
        ("Offline Resilience", "Manual DOL start", "Cloud dependent", "Cloud dependent", "100% Local FreeRTOS Loop"),
        ("Vernacular Advisory", "None", "Basic English App", "Mobile app notifications", "WhatsApp Voice in Marathi/Hindi"),
        ("Payback Period", "5+ Years (Diesel replace)", "6-8 Years (High Capex)", "Subscription Overhead", "2.0 Years (2 Crop Seasons)")
    ]
    for r_idx, r_data in enumerate(rows):
        for c_idx, val in enumerate(r_data):
            bg = RGBColor(15, 35, 25) if c_idx == 4 else COLOR_CARD
            col = COLOR_PRIMARY if c_idx == 4 else (COLOR_SOLAR if c_idx == 4 and r_idx == 5 else COLOR_TEXT_PRIMARY)
            format_cell(table.cell(r_idx + 1, c_idx), val, font_size=9, bold=(c_idx == 4 or c_idx == 0), color=col, bg_color=bg)

    # Right Moat Box
    card_m = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.3), Inches(1.9), Inches(3.43), Inches(4.8))
    set_shape_flat(card_m, COLOR_CARD, COLOR_PRIMARY, line_width=1.5)

    tb_m = slide.shapes.add_textbox(Inches(9.5), Inches(2.0), Inches(3.0), Inches(4.5))
    p = tb_m.text_frame.paragraphs[0]
    p.text = "THE SHARED-ARRAY MOAT"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    p2 = tb_m.text_frame.add_paragraph()
    p2.text = "₹91,000"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_PRIMARY
    p2.space_before = Pt(4)

    p3 = tb_m.text_frame.add_paragraph()
    p3.text = "Avoided PV Capex per Pre-Cooler Installation"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(11)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TEXT_PRIMARY
    p3.space_before = Pt(2)

    moat_points = [
        "Eliminating Redundant Solar: Competitors force farmers to buy a dedicated 4 kWp array for cooling. AgroStruxure time-shares the existing pump array.",
        "Zero Land Footprint: Avoids consuming 200 sq.ft of productive farmland for extra solar structures.",
        "Retrofit Architecture: Integrates seamlessly onto existing Shakti, Lubi, or Kirloskar solar pumps."
    ]
    for mp in moat_points:
        pb = tb_m.text_frame.add_paragraph()
        pb.text = f"▪  {mp}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = COLOR_TEXT_SECONDARY
        pb.space_before = Pt(8)


def build_slide_08(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Impact Verification", "The Single Source of Truth: Mathematical & Physical Derivations")
    add_title_area(slide, "Quantified Impact: The Single Source of Truth",
                   "Every figure reproduced directly from impact_model.py with explicit baseline tracking and transparent bounds.")
    add_footer(slide, "Run python impact_model.py in root directory to reproduce all figures identically", "08")

    # 4 Giant Metric Cards
    kpis = [
        ("41.2%", "Water Saved", "7,000 m³ / ha / year", "Baseline: 17,000 m³ (flood) ⟶ 10,000 m³ (scheduled drip).", COLOR_PRIMARY),
        ("1,696", "kWh Freed", "3,187 kWh Surplus Captured", "Pumping cut from 4,118 to 2,422 kWh/yr; 77% surplus captured.", COLOR_CUTOFF),
        ("1.31 t", "Produce Saved", "+₹15,732 Revenue Gain", "Farm-gate tomato spoilage cut from 8.37% (NABCONS) to 4.00%.", COLOR_COOLING),
        ("2.94 t", "CO₂e Abated", "2.55t Diesel + 0.39t Food", "Displaces diesel generator cooling emissions + embodied food waste.", COLOR_SOLAR)
    ]
    card_w = Inches(2.9)
    gap = Inches(0.17)
    for i, (k_num, k_lbl, k_main, k_sub, k_col) in enumerate(kpis):
        x = Inches(0.6) + i * (card_w + gap)
        y = Inches(1.9)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, Inches(2.1))
        set_shape_flat(card, COLOR_CARD, k_col, line_width=1)

        tb = slide.shapes.add_textbox(x + Inches(0.15), y + Inches(0.12), card_w - Inches(0.3), Inches(1.85))
        p = tb.text_frame.paragraphs[0]
        p.text = k_num
        p.font.name = FONT_HEADING
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = k_col

        p_lbl = tb.text_frame.add_paragraph()
        p_lbl.text = k_lbl.upper()
        p_lbl.font.name = FONT_BODY
        p_lbl.font.size = Pt(9.5)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = COLOR_TEXT_PRIMARY
        p_lbl.space_before = Pt(2)

        p_m = tb.text_frame.add_paragraph()
        p_m.text = k_main
        p_m.font.name = FONT_BODY
        p_m.font.size = Pt(11)
        p_m.font.bold = True
        p_m.font.color.rgb = COLOR_TEXT_PRIMARY
        p_m.space_before = Pt(4)

        p_s = tb.text_frame.add_paragraph()
        p_s.text = k_sub
        p_s.font.name = FONT_BODY
        p_s.font.size = Pt(8.5)
        p_s.font.color.rgb = COLOR_TEXT_MUTED
        p_s.space_before = Pt(3)

    # Bottom Left: Honest Water Attribution Table
    card_bl = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(4.2), Inches(5.9), Inches(2.5))
    set_shape_flat(card_bl, COLOR_CARD, COLOR_BORDER)

    tb_bl = slide.shapes.add_textbox(Inches(0.8), Inches(4.25), Inches(5.5), Inches(2.4))
    p = tb_bl.text_frame.paragraphs[0]
    p.text = "HONEST WATER ATTRIBUTION BREAKDOWN (PER SEASON)"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    table_shape1 = slide.shapes.add_table(4, 3, Inches(0.8), Inches(4.6), Inches(5.5), Inches(1.9))
    t1 = table_shape1.table
    t1.columns[0].width = Inches(2.3)
    t1.columns[1].width = Inches(1.5)
    t1.columns[2].width = Inches(1.7)
    format_cell(t1.cell(0, 0), "Transition Stage", font_size=9, bold=True, color=COLOR_TEXT_SECONDARY, bg_color=COLOR_PANEL)
    format_cell(t1.cell(0, 1), "Application", font_size=9, bold=True, color=COLOR_TEXT_SECONDARY, bg_color=COLOR_PANEL)
    format_cell(t1.cell(0, 2), "Savings Delivered", font_size=9, bold=True, color=COLOR_TEXT_SECONDARY, bg_color=COLOR_PANEL)

    w_rows = [
        ("Flood Baseline", "8,500 m³ / ha", "0 m³ (Baseline)"),
        ("Flood ⟶ Conventional Drip", "6,000 m³ / ha", "2,500 m³ (29.4% HW saving)"),
        ("Drip ⟶ AgroStruxure Entitlement", "5,000 m³ / ha", "1,000 m³ (11.8% + locked)")
    ]
    for r_i, (c0, c1, c2) in enumerate(w_rows):
        format_cell(t1.cell(r_i + 1, 0), c0, font_size=8.5, color=COLOR_TEXT_PRIMARY, bg_color=COLOR_CARD)
        format_cell(t1.cell(r_i + 1, 1), c1, font_size=8.5, color=COLOR_TEXT_SECONDARY, bg_color=COLOR_CARD)
        col = COLOR_PRIMARY if r_i == 2 else COLOR_TEXT_PRIMARY
        format_cell(t1.cell(r_i + 1, 2), c2, font_size=8.5, bold=(r_i == 2), color=col, bg_color=COLOR_CARD)

    # Bottom Right: Thermal Pull-Down Sizing
    card_br = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.2), Inches(5.9), Inches(2.5))
    set_shape_flat(card_br, COLOR_CARD, COLOR_BORDER)

    tb_br = slide.shapes.add_textbox(Inches(7.0), Inches(4.25), Inches(5.5), Inches(2.4))
    p = tb_br.text_frame.paragraphs[0]
    p.text = "THERMAL SIZING & FEASIBILITY BOUNDS (32°C TO 12°C)"
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = COLOR_COOLING

    p2 = tb_br.text_frame.add_paragraph()
    p2.text = "Produce batch pull-down electrical power requirements (COP = 3.0, Cp = 3.7 kJ/kg·K):"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_SECONDARY
    p2.space_before = Pt(2)

    thermal_bullets = [
        "1.0 MT Batch: 1.71 kW avg over 4 hours (6.8 kWh_el) ⟶ Easily fits single 4.8 kWp pump array.",
        "2.0 MT Batch: 3.43 kW avg over 4 hours (13.7 kWh_el) ⟶ OPTIMAL FIT (Selected for Tier A 4-Farm Cluster).",
        "5.0 MT Batch: 8.56 kW avg over 4 hours (34.3 kWh_el) ⟶ Exceeds single array; requires Tier B Hub with 4 kWp dedicated PV.",
        "Tomato Biology: Storing tomatoes < 10°C causes chilling injury. 12°C target setpoint preserves texture and shelf life."
    ]
    for tb_item in thermal_bullets:
        pb = tb_br.text_frame.add_paragraph()
        pb.text = f"▪  {tb_item}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(8.5)
        pb.font.color.rgb = COLOR_TEXT_SECONDARY
        pb.space_before = Pt(3)


def build_slide_09(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Commercial Viability", "Industrial BOM, Cluster Payback & Market Scaling")
    add_title_area(slide, "Industrial BOM, Unit Economics & Scaling",
                   "A ₹7,540 edge controller BOM delivers a 2.0-year capital payback for a 4-farm pre-cooler cluster.")
    add_footer(slide, "Itemized Industrial BOM · MIDH Operational Guidelines · AIF 3% Interest Subvention Scheme", "09")

    # Left: BOM Table (45%)
    card_l = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.9), Inches(5.5), Inches(4.8))
    set_shape_flat(card_l, COLOR_CARD, COLOR_BORDER)

    tb_l = slide.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(5.1), Inches(4.5))
    p = tb_l.text_frame.paragraphs[0]
    p.text = "EDGE CONTROLLER BOM (1,000 UNITS)"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    bom_table_shape = slide.shapes.add_table(11, 2, Inches(0.8), Inches(2.35), Inches(5.1), Inches(3.9))
    bt = bom_table_shape.table
    bt.columns[0].width = Inches(4.0)
    bt.columns[1].width = Inches(1.1)

    format_cell(bt.cell(0, 0), "Component Description", font_size=8.5, bold=True, color=COLOR_TEXT_SECONDARY, bg_color=COLOR_PANEL)
    format_cell(bt.cell(0, 1), "Cost (INR)", font_size=8.5, bold=True, color=COLOR_TEXT_SECONDARY, bg_color=COLOR_PANEL, align=PP_ALIGN.RIGHT)

    bom_items = [
        ("ESP32-S3-WROOM-1 (16MB Flash, 8MB PSRAM)", "₹420"),
        ("Isolated MAX485 Transceiver + TVS Diode", "₹180"),
        ("Dual FDR Capacitive Soil Probes (10cm & 30cm)", "₹760"),
        ("Sensirion SHT31-D Temp/RH + Pyranometer", "₹600"),
        ("1-inch Hall-Effect Pulse Flow Meter", "₹650"),
        ("1-inch 12V Bistable Latching Solenoid Valve", "₹650"),
        ("Schneider TeSys D Contactors ×2 (LC1D09BD)", "₹2,300"),
        ("24V SMPS + Opto-Isolated Relay Driver", "₹380"),
        ("SIM7600 4G LTE Cat-1 Cellular Module", "₹620"),
        ("IP67 Enclosure, DIN Rail, DC SPD, Cabling", "₹980"),
    ]
    for b_idx, (desc, cost) in enumerate(bom_items):
        bg = COLOR_CARD
        col = COLOR_PRIMARY if b_idx == 6 else COLOR_TEXT_PRIMARY
        format_cell(bt.cell(b_idx + 1, 0), desc, font_size=8, bold=(b_idx == 6), color=col, bg_color=bg)
        format_cell(bt.cell(b_idx + 1, 1), cost, font_size=8, bold=True, color=col, bg_color=bg, align=PP_ALIGN.RIGHT)

    # Right: 2-Tier Payback Breakdown
    card_r = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.4), Inches(1.9), Inches(6.33), Inches(4.8))
    set_shape_flat(card_r, COLOR_CARD, COLOR_BORDER)

    tb_r = slide.shapes.add_textbox(Inches(6.6), Inches(2.0), Inches(5.9), Inches(4.5))
    p = tb_r.text_frame.paragraphs[0]
    p.text = "TWO-TIER ASSET OWNERSHIP ECONOMICS"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SOLAR

    # Tier A Box
    pt_a = tb_r.text_frame.add_paragraph()
    pt_a.text = "Tier A: Farm Pre-Cooler (4-Farm Cluster sharing 2 MT Unit) — 2.0 YR PAYBACK"
    pt_a.font.name = FONT_BODY
    pt_a.font.size = Pt(11)
    pt_a.font.bold = True
    pt_a.font.color.rgb = COLOR_PRIMARY
    pt_a.space_before = Pt(6)

    tier_a_points = [
        "Gross Capex: ₹4,00,000 | Less Avoided PV: -₹91,000 | Net Capex: ₹3,09,000.",
        "After 35% MIDH/AIF Subsidy: ₹2,00,850 total (₹50,212 per smallholder farm).",
        "Annual Farmer Net Gain: +₹25,332 / farm / year (₹15,732 spoilage saved + ₹12,000 mandi price timing gain - ₹2,400 opex).",
        "Payback Period: Exactly 2.0 Years (2 crop seasons). (Pre-subsidy payback: 3.0 years)."
    ]
    for pt in tier_a_points:
        pb = tb_r.text_frame.add_paragraph()
        pb.text = f"▪ {pt}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9)
        pb.font.color.rgb = COLOR_TEXT_SECONDARY
        pb.space_before = Pt(2)

    # Tier B Box
    pt_b = tb_r.text_frame.add_paragraph()
    pt_b.text = "Tier B: FPO Holding Hub (20-Farm Cooperative Hub, 5 MT Unit) — 4.2 YR PAYBACK"
    pt_b.font.name = FONT_BODY
    pt_b.font.size = Pt(11)
    pt_b.font.bold = True
    pt_b.font.color.rgb = COLOR_COOLING
    pt_b.space_before = Pt(8)

    tier_b_points = [
        "Hub Capex: ₹12,00,000 (owns 4 kWp PV) ⟶ ₹7,80,000 after 35% subsidy.",
        "Net Storage Revenue (@ ₹3.00/kg/stay): ₹1,84,375 / year (Claims zero shared-array saving).",
        "Payback Period: 4.2 Years post-subsidy (6.5 years pre-subsidy)."
    ]
    for pt in tier_b_points:
        pb = tb_r.text_frame.add_paragraph()
        pb.text = f"▪ {pt}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9)
        pb.font.color.rgb = COLOR_TEXT_SECONDARY
        pb.space_before = Pt(2)

    # GTM Channels
    pt_gtm = tb_r.text_frame.add_paragraph()
    pt_gtm.text = "GO-TO-MARKET CHANNELS & FINANCING:"
    pt_gtm.font.name = FONT_BODY
    pt_gtm.font.size = Pt(10.5)
    pt_gtm.font.bold = True
    pt_gtm.font.color.rgb = COLOR_TEXT_PRIMARY
    pt_gtm.space_before = Pt(8)

    gtm_points = [
        "1. PM-KUSUM Retrofit: Distributed through FPOs & PACS under AIF 3% interest subvention.",
        "2. Schneider OEM Skid: Pre-assembled Altivar Solar + TeSys skid bundled for new EPC solar tenders."
    ]
    for pt in gtm_points:
        pb = tb_r.text_frame.add_paragraph()
        pb.text = f"• {pt}"
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9)
        pb.font.color.rgb = COLOR_TEXT_SECONDARY
        pb.space_before = Pt(2)


def build_slide_10(prs):
    slide = create_slide_base(prs)
    add_header(slide, "Execution Plan", "12-Month Deployment Roadmap & Multidisciplinary Team")
    add_title_area(slide, "Implementation Roadmap & Multidisciplinary Team",
                   "From software simulation to a 25-farm field pilot in Maharashtra with Schneider Electric India Foundation synergy.")
    add_footer(slide, "Phase 1 Submission · Schneider Electric India & YouNoodle Hackathon Portal", "10")

    # Top Half: 4-Phase Roadmap
    card_top = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.9), Inches(12.13), Inches(1.9))
    set_shape_flat(card_top, COLOR_CARD, COLOR_BORDER)

    tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(11.7), Inches(1.8))
    p = tb_t.text_frame.paragraphs[0]
    p.text = "12-MONTH EXECUTION ROADMAP"
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY

    phases = [
        ("PHASE 1 (OCT 2026)", "Simulation & Truth", "AgroSim model validated; CiA402 Modbus mapped; deterministic prompt guards verified.", COLOR_PRIMARY),
        ("PHASE 2 (NOV-DEC 2026)", "HIL Test Bench", "Hardware bench with Altivar ATV320 VFD, TeSys D contactors, and 5s deadband validation.", COLOR_SOLAR),
        ("PHASE 3 (Q1 2027)", "Nashik Field Pilot", "25-farm cluster pilot with 2 FPOs in Nashik horticulture belt. Tomato harvesting trials.", COLOR_CUTOFF),
        ("PHASE 4 (Q3 2027+)", "Commercial Scale", "OEM pre-assembled skid for PM-KUSUM tenders; expansion to 250 farms across Maharashtra.", COLOR_COOLING)
    ]
    ph_w = Inches(2.78)
    gap = Inches(0.18)
    for i, (ph_tag, ph_title, ph_desc, ph_col) in enumerate(phases):
        x = Inches(0.8) + i * (ph_w + gap)
        y = Inches(2.35)
        pbox = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, ph_w, Inches(1.3))
        set_shape_flat(pbox, COLOR_PANEL, ph_col, line_width=1)
        
        tb_p = slide.shapes.add_textbox(x + Inches(0.1), y + Inches(0.08), ph_w - Inches(0.2), Inches(1.15))
        p = tb_p.text_frame.paragraphs[0]
        p.text = ph_tag
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = ph_col

        p2 = tb_p.text_frame.add_paragraph()
        p2.text = ph_title
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_PRIMARY
        p2.space_before = Pt(2)

        p3 = tb_p.text_frame.add_paragraph()
        p3.text = ph_desc
        p3.font.name = FONT_BODY
        p3.font.size = Pt(8)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.space_before = Pt(3)

    # Bottom Half: 4 Team Roles
    roles = [
        ("EMBEDDED SYSTEMS", "Firmware Lead", "ESP32-S3 & Modbus Engine",
         "FreeRTOS tasks, CiA402 drive state machine, isolated RS485 communication, circular FIFO flash storage.", COLOR_PRIMARY),
        ("POWER ELECTRONICS", "Electrical Architect", "Switchgear & Sizing",
         "Upstream DC changeover design, TeSys D mechanical interlocks, 5s deadband bleed down, and thermal pull-down models.", COLOR_SOLAR),
        ("AGRONOMY & SATELLITE", "Data Scientist", "Hydrology & AI RAG",
         "FAO-56 Penman-Monteith algorithms, Sentinel-2 NDVI/NDWI satellite validation, and deterministic prompt guards.", COLOR_CUTOFF),
        ("PRODUCT & IMPACT", "Product Strategist", "Smallholder UX & Policy",
         "Rural smallholder interfaces, QuartzDS compliance, FPO cluster economic models, and Atal Bhujal policy integration.", COLOR_COOLING)
    ]
    card_w = Inches(2.9)
    gap = Inches(0.17)
    for i, (r_domain, r_title, r_spec, r_desc, r_col) in enumerate(roles):
        x = Inches(0.6) + i * (card_w + gap)
        y = Inches(4.0)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, Inches(2.1))
        set_shape_flat(card, COLOR_CARD, COLOR_BORDER)

        tb = slide.shapes.add_textbox(x + Inches(0.15), y + Inches(0.12), card_w - Inches(0.3), Inches(1.85))
        p = tb.text_frame.paragraphs[0]
        p.text = r_domain
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = r_col

        p2 = tb.text_frame.add_paragraph()
        p2.text = r_title
        p2.font.name = FONT_BODY
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_PRIMARY
        p2.space_before = Pt(2)

        p3 = tb.text_frame.add_paragraph()
        p3.text = r_spec
        p3.font.name = FONT_BODY
        p3.font.size = Pt(9.5)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.space_before = Pt(1)

        p4 = tb.text_frame.add_paragraph()
        p4.text = r_desc
        p4.font.name = FONT_BODY
        p4.font.size = Pt(8.5)
        p4.font.color.rgb = COLOR_TEXT_SECONDARY
        p4.space_before = Pt(4)

    # Corporate Synergy Banner
    ban = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.25), Inches(12.13), Inches(0.55))
    set_shape_flat(ban, COLOR_DEEP_FOREST, COLOR_PRIMARY, line_width=1)
    tb_bn = slide.shapes.add_textbox(Inches(0.8), Inches(6.28), Inches(11.7), Inches(0.48))
    p = tb_bn.text_frame.paragraphs[0]
    p.text = "SCHNEIDER ECOSYSTEM ALIGNMENT: Pre-Placement Interview (PPI) readiness, SE Ventures incubation fit, and SEIF Climate Smart Village rollout synergy."
    p.font.name = FONT_HEADING
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT_PRIMARY


# -------------------------------------------------------------
# MAIN ASSEMBLY
# -------------------------------------------------------------
def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    print("Building Slide 01: Hero / Product Launch...")
    build_slide_01(prs)
    print("Building Slide 02: The Dual Agricultural Crisis...")
    build_slide_02(prs)
    print("Building Slide 03: The Solar Rebound Paradox...")
    build_slide_03(prs)
    print("Building Slide 04: Proposed Solution & Challenge Alignment...")
    build_slide_04(prs)
    print("Building Slide 05: Precision Hydraulics & Diurnal Journey...")
    build_slide_05(prs)
    print("Building Slide 06: Schneider EcoStruxure Architecture & Power Topology...")
    build_slide_06(prs)
    print("Building Slide 07: Innovation & Competitive Defense...")
    build_slide_07(prs)
    print("Building Slide 08: Quantified Impact & Mathematical Proofs...")
    build_slide_08(prs)
    print("Building Slide 09: Industrial BOM, Unit Economics & Scaling...")
    build_slide_09(prs)
    print("Building Slide 10: Implementation Roadmap & Multidisciplinary Team...")
    build_slide_10(prs)

    output_path = "01_FINAL_YUVA_YODHA_DECK.pptx"
    prs.save(output_path)
    print(f"\nSuccessfully generated {output_path} ({os.path.getsize(output_path)} bytes)")

if __name__ == "__main__":
    build_deck()
