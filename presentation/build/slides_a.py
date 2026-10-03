# -*- coding: utf-8 -*-
"""Slides 1-4: hero, problem, architecture (data/energy/money flows), water."""
import kit
from kit import *
import charts

SRC_MODEL = "Model: research/08_IMPACT/impact_model.py (1 ha tomato, Nashik, 4.8 kWp PM-KUSUM Component B pump)."


def slide01(prs):
    s = blank(prs, FOREST)
    pill(s, 0.7, 0.55, 5.55, 0.34, "YUVA YODHA 2026  ·  CHALLENGE 01: SUSTAINABLE AGRICULTURE", FOREST_2, GREEN, 11,
         name="Kicker")
    text(s, 0.7, 1.1, 6.9, 1.15, [[("AgroStruxure", {}), ("™", {"size": 26})]], size=62, bold=True, color=WHITE,
         name="Title")
    text(s, 0.7, 2.3, 6.4, 0.85, "Solar-synchronised agri-energy microgrid and precision irrigation for PM-KUSUM pumps",
         size=21, bold=True, color=GREEN, name="Subtitle")
    text(s, 0.7, 3.3, 6.4, 0.45, "“One solar pump can become a rural energy node.”", size=20, italic=True, color=WHITE)
    text(s, 0.7, 3.88, 6.35, 1.2,
         "A retrofit kit that caps irrigation at what the crop needs, so free daytime solar cannot over-pump the "
         "aquifer, then runs a shared farm-gate pre-cooler from the idle surplus.",
         size=16, color=ON_DARK_MUTED, line_spacing=1.05)
    tiles = [("41.2%", GREEN, "less groundwater", "7,000 m³/ha/yr"),
             ("63%", GOLD, "of PV output idle", "after right-sizing water"),
             ("1.31 t", "C9A3F5", "tomatoes saved", "per ha per year"),
             ("2.0 yr", "7FD0F7", "capital payback", "₹50,212 net per farm")]
    for i, (big, col, l1, l2) in enumerate(tiles):
        x = 0.7 + i * 1.62
        rect(s, x, 5.2, 1.5, 1.28, fill=FOREST_2, radius=0.1, name=f"KPI tile {i+1}")
        text(s, x + 0.1, 5.27, 1.3, 0.5, big, size=26, bold=True, color=col, name=f"KPI {i+1} value")
        text(s, x + 0.1, 5.82, 1.32, 0.62, [(l1, {"bold": True, "color": WHITE}), ], size=12, color=WHITE)
        text(s, x + 0.1, 6.1, 1.32, 0.38, l2, size=10, color=ON_DARK_MUTED)
    text(s, 0.7, 6.62, 6.4, 0.42,
         "Sanskar Tiwari (Firmware, lead)  ·  Shambhavi Patil (Geospatial)  ·  Kanishka Salgude (Power / VFD)  ·  "
         "Chaitanya Ranade (Agronomy / Product)", size=11, color=ON_DARK_MUTED, name="Team")

    # right: one-pump-two-loads schematic
    rect(s, 7.6, 0.55, 5.15, 6.3, fill=FOREST_2, line="0D8752", radius=0.16, name="System schematic card",
         alt="Schematic: PV array feeds the AgroStruxure controller, which splits power between a drip-irrigation "
             "pump and a shared pre-cooler")
    text(s, 7.9, 0.82, 4.6, 0.3, "ONE PUMP  ·  TWO LOADS  ·  ONE CONTROLLER", size=11, bold=True, color=GREEN)
    rect(s, 8.15, 1.3, 0.8, 0.8, fill=GOLD, shape=MSO_SHAPE.SUN, name="Sun icon")
    text(s, 9.15, 1.37, 3.4, 0.7, [("4.8 kWp PV array", {"bold": True, "color": WHITE, "size": 17}),
                                   ("6,559 kWh per year", {"size": 13, "color": ON_DARK_MUTED})], size=14)
    arrow(s, 10.17, 2.2, 10.17, 2.78, color=GOLD, width=3, name="Energy arrow PV to controller")
    rect(s, 8.15, 2.8, 4.05, 1.1, fill=GREEN, radius=0.12, name="Controller",
         paras=[("AgroStruxure edge controller", {"bold": True, "size": 17, "color": FOREST}),
                ("FAO-56 budget · field-capacity cutoff · TeSys changeover", {"size": 12, "color": FOREST})])
    arrow(s, 9.2, 3.92, 9.2, 4.5, color=GOLD, width=3)
    arrow(s, 11.2, 3.92, 11.2, 4.5, color=GOLD, width=3)
    rect(s, 8.0, 4.52, 2.4, 1.2, fill=WATER, radius=0.12, name="Load A",
         paras=[("Right-sized drip", {"bold": True, "size": 16, "color": WHITE}),
                ("Altivar ATV320 pump", {"size": 12, "color": WHITE}),
                ("2,422 kWh/yr", {"size": 12, "color": WHITE})])
    rect(s, 10.55, 4.52, 2.0, 1.2, fill=COLD, radius=0.12, name="Load B",
         paras=[("Shared pre-cooler", {"bold": True, "size": 16, "color": WHITE}),
                ("4-farm cluster", {"size": 12, "color": WHITE}),
                ("1,062 kWh/yr", {"size": 12, "color": WHITE})])
    pill(s, 8.0, 5.95, 2.4, 0.4, "−41.2% groundwater", WHITE, FOREST, 13)
    pill(s, 10.55, 5.95, 2.0, 0.4, "−52% farm-gate loss", WHITE, FOREST, 13)
    text(s, 7.9, 6.45, 4.6, 0.3, "Altivar Solar ATV320  ·  TeSys D  ·  Modbus RTU  ·  EcoStruxure-aligned",
         size=10, color=ON_DARK_MUTED, align="c")
    text(s, 0.7, 7.05, 11.5, 0.3, SRC_MODEL + " 63% idle PV = after irrigation is right-sized (37% idle today).",
         size=10, color=ON_DARK_MUTED, name="Sources")
    notes(s, "HOOK (20 s). One solar pump becomes a rural energy node: AgroStruxure is a retrofit kit for PM-KUSUM "
             "Component B pumps. It does two things: (1) caps irrigation at the crop's FAO-56 entitlement, which "
             "protects the aquifer from the solar rebound effect; (2) uses the idle midday solar to run a shared "
             "farm-gate pre-cooler for tomatoes. Headline numbers, all per hectare of tomato in Nashik: 41.2% less "
             "groundwater (7,000 m3/yr), 4,137 kWh/yr of PV output (63%) with no pumping use once water is "
             "right-sized, 1.31 t of tomatoes saved, 2.0-year payback on the farmer's share of a 4-farm pre-cooler. "
             "63% idle is AFTER right-sizing; today with flood irrigation 37% (2,442 kWh) is idle. "
             "Team roster to be confirmed before submission.")
    return s


def slide02(prs):
    s = blank(prs)
    header(s, "PROBLEM  ·  THE SOLAR REBOUND EFFECT",
           [("Free Solar Power Accelerates ", {}), ("Groundwater Collapse", {"color": EMERALD})],
           "Under PM-KUSUM Component B, daytime pumping costs nothing, so nothing limits the water drawn, "
           "and the sun goes unused.", kicker_w=3.55)
    card(s, 0.6, 2.3, 5.1, 4.4, name="Chart card")
    text(s, 0.85, 2.45, 4.6, 0.5, [("Annual energy, one 4.8 kWp pump", {"bold": True, "size": 15, "color": FOREST}),
                                   ("1 ha tomato, kWh per year", {"size": 12, "color": SLATE})], size=14)
    charts.column(s, 0.8, 3.0, 4.7, 2.55, ["Solar generation", "Pumping today (flood)", "Pumping right-sized"],
                  [6559, 4118, 2422], [GOLD, "8FC9EA", WATER], vmax=7800, size=12, label_size=15,
                  name="Energy chart", alt="Column chart: solar generation 6,559 kWh, flood pumping 4,118 kWh, "
                                           "right-sized pumping 2,422 kWh")
    text(s, 0.85, 5.62, 4.65, 1.0,
         [[("Today: ", {"bold": True}), "2,442 kWh idle (37%)."],
          [("Right-sized: ", {"bold": True}), "4,137 kWh idle (63%), because the pump now needs 1,696 kWh less."]],
         size=14, space_after=3)

    cards = [("01", "Free power, unlimited pumping",
              "Flood irrigation applies 17,000 m³/ha/yr against a 10,000 m³ crop entitlement. Zero marginal cost "
              "removes any reason to stop.", "16–39%", "more water pumped after solarisation (Rajasthan study, IWMI)", WATER),
             ("02", "Solar capacity stranded",
              "Once the water is right-sized, most of the array's output has no pumping use: a stranded asset "
              "at midday.", "63%", "of PV output idle after right-sizing water", GOLD_TXT),
             ("03", "Harvest rots where the power is",
              "No cold chain at the farm gate: tomatoes are lost at farm stage (11.62% including market handling).",
              "8.37%", "farm-stage tomato loss (NABCONS 2022, MoFPI)", COLD)]
    for i, (n, t, b, big, cap, col) in enumerate(cards):
        y = 2.3 + i * 1.5
        card(s, 6.0, y, 6.73, 1.38, name=f"Problem card {n}")
        circle(s, 6.2, y + 0.22, 0.5, n, FOREST, size=14)
        text(s, 6.9, y + 0.14, 3.6, 0.3, t, size=16, bold=True, color=FOREST)
        text(s, 6.9, y + 0.5, 3.6, 0.85, b, size=12, color=INK, line_spacing=1.0)
        text(s, 10.65, y + 0.14, 1.95, 0.55, big, size=30, bold=True, color=col, align="r")
        text(s, 10.65, y + 0.72, 1.95, 0.6, cap, size=11, color=SLATE, align="r")
    footer(s, "Sources: CGWB National Compilation 2023 (736 of 6,553 assessment units over-exploited) · NABCONS 2022 for MoFPI · "
              "IWMI (Shah et al.) · MNRE PM-KUSUM progress (≈10.06 lakh Component B pumps installed by 31 Jan 2026). " + SRC_MODEL,
           2)
    notes(s, "PROBLEM (45 s). Three linked failures. (1) Rebound: PM-KUSUM makes daytime power free, so farmers pump until "
             "fields flood. Baseline flood use is 850 mm x 2 seasons = 17,000 m3/ha/yr versus a 10,000 m3 FAO-56 "
             "entitlement. IWMI-cited research reports 16-39% more extraction after solarisation in Rajasthan "
             "(verify exact citation before quoting). (2) Stranded solar: PV generates 6,559 kWh/yr; flood pumping "
             "uses 4,118 kWh, leaving 2,442 kWh idle (37%). Right-size the water and pumping falls to 2,422 kWh, so "
             "4,137 kWh (63%) is idle. (3) Post-harvest: NABCONS 2022 farm-stage tomato loss is 8.37% (11.62% "
             "including market). Context: CGWB 2023 lists 736 of 6,553 assessment units as over-exploited; about "
             "10.06 lakh Component B pumps were installed by 31 Jan 2026 (MNRE, as reported; 13.3 lakh sanctioned).")
    return s


def _lane(s, y, label, sub, col, tint):
    rect(s, 0.6, y, 1.0, 1.45, fill=col, radius=0.1, name=f"{label} lane label",
         paras=[(label, {"bold": True, "size": 14, "color": WHITE}), (sub, {"size": 10, "color": WHITE})])
    rect(s, 1.7, y, 11.03, 1.45, fill=tint, radius=0.1, name=f"{label} lane band")


def _node(s, x, y, w, h, title, detail, col, name):
    rect(s, x, y, w, h, fill=CARD, line=col, line_w=1.5, radius=0.09, name=name, align="l", anchor="m", pad=0.1,
         paras=[(title, {"bold": True, "size": 14, "color": FOREST}), (detail, {"size": 12, "color": INK})])


def slide03(prs):
    s = blank(prs)
    header(s, "ARCHITECTURE  ·  ECOSTRUXURE-ALIGNED, EDGE-FIRST",
           [("One Retrofit Kit, Three Flows: ", {}), ("Data, Energy, Money", {"color": EMERALD})],
           "Sensing, switching and settlement in one design. The controller works offline; the cloud only advises.",
           kicker_w=4.4)
    lanes = [("DATA", "sense → advise", WATER, TINT_BLUE, 2.28),
             ("ENERGY", "DC bus → loads", "9C7400", TINT_GOLD, 3.82),
             ("MONEY", "subsidy → payback", EMERALD, TINT_GREEN, 5.36)]
    for lab, sub, col, tint, y in lanes:
        _lane(s, y, lab, sub, col, tint)
    xs = [1.82, 4.58, 7.34, 10.1]
    w = 2.45
    # DATA lane
    y = 2.28 + 0.12
    nd = [("Field sensors", "FDR probes at 10 and 30 cm · flow meter · SHT31 · pyranometer"),
          ("Edge controller", "ESP32-S3 · FAO-56 budget · field-capacity cutoff · commands the changeover"),
          ("4G gateway → FastAPI", "Validated JSON (Pydantic) · read-only AI copilot"),
          ("WhatsApp voice advice", "Marathi / Hindi · no app, no dashboard")]
    for i, (t, d) in enumerate(nd):
        _node(s, xs[i], y, w, 1.21, t, d, WATER, f"Data node {i+1}")
        if i < 3:
            arrow(s, xs[i] + w + 0.03, y + 0.6, xs[i + 1] - 0.03, y + 0.6, color=WATER, width=2.5)
    # ENERGY lane
    y = 3.82 + 0.12
    _node(s, xs[0], y, w, 1.21, "4.8 kWp PV array", "6,559 kWh/yr · 350–600 V DC bus", "9C7400", "Energy node 1")
    _node(s, xs[1], y, w, 1.21, "TeSys D changeover", "2× LC1D09BD interlocked · 5 s dead-band at 0 A", "9C7400",
          "Energy node 2")
    rect(s, xs[2], y, w, 0.58, fill=CARD, line=WATER, line_w=1.5, radius=0.09, align="l", pad=0.1,
         paras=[("Load A · ATV320 pump", {"bold": True, "size": 13, "color": FOREST}),
                ("2,422 kWh/yr · 08:30–11:30", {"size": 11})], name="Energy node 3a")
    rect(s, xs[2], y + 0.63, w, 0.58, fill=CARD, line=COLD, line_w=1.5, radius=0.09, align="l", pad=0.1,
         paras=[("Load B · cluster cooler", {"bold": True, "size": 13, "color": FOREST}),
                ("1,062 kWh/yr · 11:30–15:30", {"size": 11})], name="Energy node 3b")
    _node(s, xs[3], y, w, 1.21, "Idle headroom", "3,075 kWh/yr (47% of PV). Not claimed as a benefit",
          "9C7400", "Energy node 4")
    arrow(s, xs[0] + w + 0.03, y + 0.6, xs[1] - 0.03, y + 0.6, color="9C7400", width=3)
    arrow(s, xs[1] + w + 0.03, y + 0.3, xs[2] - 0.03, y + 0.3, color="9C7400", width=3)
    arrow(s, xs[1] + w + 0.03, y + 0.92, xs[2] - 0.03, y + 0.92, color="9C7400", width=3)
    arrow(s, xs[2] + w + 0.03, y + 0.6, xs[3] - 0.03, y + 0.6, color="9C7400", width=3, dash=True)
    # MONEY lane
    y = 5.36 + 0.12
    nm = [("35% MIDH / AIF subsidy", "₹108,150 off a ₹309,000 net system cost"),
          ("Farmer capex", "₹50,212 per farm (4-farm cluster) + ₹2,400/yr opex"),
          ("Annual farmer gain", "₹15,732 spoilage saved + ₹12,000 timing = ₹27,732"),
          ("Capital payback", "2.0 years (3.0 without subsidy)")]
    for i, (t, d) in enumerate(nm):
        _node(s, xs[i], y, w, 1.21, t, d, EMERALD, f"Money node {i+1}")
        if i < 3:
            arrow(s, xs[i] + w + 0.03, y + 0.6, xs[i + 1] - 0.03, y + 0.6, color=EMERALD, width=2.5)
    # cross-lane links
    arrow(s, xs[1] + w / 2, 2.28 + 1.33, xs[1] + w / 2, 3.82 + 0.12, color=WATER, width=2.5)  # controller commands changeover
    arrow(s, xs[2] + w / 2, 3.82 + 1.33, xs[2] + w / 2, 5.36 + 0.12, color=EMERALD, width=2.5)  # cooling creates gain
    footer(s, "Standards: IEC 60947-4-1 (TeSys D) · Altivar ATV320 Modbus: Reg 8501 command word, 8502 speed reference · "
              "Schneider EcoStruxure 3-tier pattern (connected products → edge control → apps & analytics).", 3)
    notes(s, "ARCHITECTURE (60 s). Read the three lanes top to bottom. DATA: dual-depth FDR probes, pulse flow meter and "
             "SHT31/pyranometer feed an ESP32-S3 running a deterministic FAO-56 water budget. Control never depends on "
             "the cloud; 4G only ships validated JSON to a FastAPI service that drives the WhatsApp voice advisory. "
             "ENERGY: the 4.8 kWp array feeds a 350-600 V DC bus. A mechanically interlocked pair of TeSys D contactors "
             "transfers power between Load A (Altivar ATV320 pump, 2,422 kWh/yr) and Load B (3.8 kW DC compressor, "
             "1,062 kWh/yr for a 4-farm cluster) with a 5 s zero-current dead-band. About 3,075 kWh/yr (47% of PV) "
             "stays as headroom and is not claimed. MONEY: 35% MIDH/AIF capital subsidy, farmer pays Rs 50,212 per "
             "farm as a share of a 4-farm pre-cooler, gains Rs 27,732/yr (Rs 15,732 spoilage + Rs 12,000 price timing) "
             "against Rs 2,400/yr opex: payback 2.0 years (3.0 without subsidy). Official deliverable 2 asks for "
             "data/energy/money flows; this slide is that diagram.")
    return s


def slide04(prs):
    s = blank(prs)
    header(s, "HYDROLOGY  ·  CLOSED-LOOP WATER BUDGETING",
           [("41.2% Less Groundwater, ", {}), ("Full Crop Requirement Met", {"color": WATER})],
           "A dual-Kc FAO-56 budget sets the entitlement; dual-depth FDR probes stop the pump at field capacity.",
           kicker_w=4.0)
    # left: soil profile
    card(s, 0.6, 2.3, 5.15, 4.4, name="Soil card")
    text(s, 0.85, 2.45, 4.6, 0.3, "Dual-depth soil moisture profile", size=15, bold=True, color=FOREST)
    bands = [("0–10 cm  ·  surface probe", "Evaporative zone, typically 18–32% VWC. Tracks diurnal loss.", TINT_GOLD, AMBER),
             ("10–40 cm  ·  root-zone probe", "Irrigation stops at field capacity (45% VWC), so there is no root-zone hypoxia.",
              TINT_GREEN, EMERALD),
             ("40 cm +  ·  deep percolation", "Pulsed drip leaves nothing to leach below the root zone.", "EEF1EF", SLATE)]
    for i, (t, d, f, c) in enumerate(bands):
        y = 2.9 + i * 1.12
        rect(s, 0.85, y, 4.65, 1.0, fill=f, radius=0.08, align="l", anchor="m", pad=0.15, name=f"Soil band {i+1}",
             paras=[(t, {"bold": True, "size": 14, "color": c}), (d, {"size": 12, "color": INK})])
    text(s, 0.85, 6.28, 4.65, 0.4, "Cutoffs are calibrated per soil type.",
         size=11, color=SLATE)
    # right: chart + table
    card(s, 6.0, 2.3, 6.73, 4.4, name="Water card")
    text(s, 6.25, 2.45, 6.2, 0.3, "Water applied, m³ per hectare per year", size=15, bold=True, color=FOREST)
    charts.column(s, 6.15, 2.75, 3.6, 2.35, ["Flood", "Conventional drip", "AgroStruxure"], [17000, 12000, 10000],
                  ["8FC9EA", "5BB2E0", WATER], vmax=20500, size=11, label_size=14, gap=45, name="Water chart",
                  alt="Column chart: flood 17,000, conventional drip 12,000, AgroStruxure 10,000 cubic metres per hectare per year")
    text(s, 9.9, 2.95, 2.65, 2.2,
         [[("7,000 m³", {"bold": True, "size": 26, "color": WATER})],
          [("conserved per ha per year", {"size": 12, "color": SLATE})],
          [("5,000 m³ ", {"bold": True}), "from drip hardware"],
          [("2,000 m³ ", {"bold": True}), "from the entitlement cap, locked against rebound"]],
         size=13, space_after=4)
    rows = [["Per hectare per year", "Flood", "AgroStruxure", "Change"],
            ["Water applied", "17,000 m³", "10,000 m³", "−7,000 m³"],
            ["Pumping electricity", "4,118 kWh", "2,422 kWh", "−1,696 kWh"]]
    table(s, 6.25, 5.2, 6.25, [2.1, 1.3, 1.5, 1.35], rows, row_h=0.36, size=12, col_align=["l", "r", "r", "r"])
    text(s, 6.25, 6.32, 6.3, 0.4, "Assumes drip is already installed (existing or subsidised). Drip hardware is not in the capex.",
         size=11, color=SLATE)
    footer(s, "FAO Irrigation & Drainage Paper 56 (Allen et al.) · Flood baseline 850 mm × 2 seasons; entitlement ETc 450 mm ÷ 0.90 drip efficiency "
              "→ 500 mm; 0.242 kWh/m³ at 40 m head. " + SRC_MODEL, 4)
    notes(s, "WATER (60 s). Baseline is unmetered flood irrigation at 850 mm per season, two seasons: 17,000 m3/ha/yr. "
             "AgroStruxure schedules to the FAO-56 entitlement: ETc 450 mm divided by 0.90 drip efficiency = 500 mm per "
             "season, 10,000 m3/yr. Saving 7,000 m3 = 41.2%. Honest attribution: conventional drip at 600 mm would "
             "already save 5,000 m3 (29.4 points); the AgroStruxure entitlement cap adds 2,000 m3 (11.8 points) and "
             "is what locks the saving against the rebound effect. The farmer needs drip in place for this: it is an "
             "assumption, not in the capex. Pumping energy at 0.242 kWh/m3 (40 m TDH, 45% wire-to-water) falls from "
             "4,118 to 2,422 kWh. Yield is protected because the entitlement meets full crop ET; no yield uplift is "
             "claimed.")
    return s
