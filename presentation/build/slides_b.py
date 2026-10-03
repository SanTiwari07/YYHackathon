# -*- coding: utf-8 -*-
"""Slides 5-7: power engineering, cold chain, vernacular advisory."""
import os
import kit
from kit import *
import charts

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_MODEL = "Model: research/08_IMPACT/impact_model.py (1 ha tomato, Nashik, 4.8 kWp PM-KUSUM Component B pump)."


def slide05(prs):
    s = blank(prs)
    header(s, "POWER ENGINEERING  ·  UPSTREAM DC BUS ROUTING",
           [("Cooling a 4-Farm Cluster Uses ", {}), ("26% of One Farm's Idle Solar", {"color": GOLD_TXT})],
           "Power is switched upstream on the DC bus at zero current, so no inductive spike reaches the drive.",
           kicker_w=4.5)
    card(s, 0.6, 2.3, 5.95, 2.5, name="Energy split card")
    text(s, 0.85, 2.42, 5.5, 0.3, "Where the host farm's 6,559 kWh/yr goes (kWh)", size=15, bold=True, color=FOREST)
    charts.stacked_bar(s, 0.75, 2.72, 5.7, 1.3, "PV output",
                       [("Pumping 37%", 2422, WATER, WHITE), ("Cluster cold chain 16%", 1062, COLD, WHITE),
                        ("Headroom 47%", 3075, "E3D27A", INK)], size=11, label_size=14, fmt='#,##0', name="Energy split chart",
                       alt="Stacked bar: pumping 2,422 kWh, cluster cold chain 1,062 kWh, headroom 3,075 kWh")
    text(s, 0.85, 4.03, 5.5, 0.75,
         [[("1,062 kWh = 26% of the 4,137 kWh surplus. ", {"bold": True}),
           "60 batches a year (4 farms × 15) at 17.7 kWh each. Headroom is reported, not claimed."]],
         size=13)
    card(s, 0.6, 4.95, 5.95, 1.75, name="SLD card")
    text(s, 0.85, 5.05, 5.5, 0.3, "Single-line diagram", size=13, bold=True, color=FOREST)
    rect(s, 0.85, 5.5, 1.35, 0.95, fill=GOLD, radius=0.08, paras=[("PV array", {"bold": True, "size": 13}),
                                                                   ("350–600 V DC", {"size": 11})], color=INK,
         name="SLD PV")
    arrow(s, 2.22, 5.97, 2.72, 5.97, color="9C7400", width=3)
    rect(s, 2.74, 5.5, 1.55, 0.95, fill=GREEN, radius=0.08, name="SLD TeSys",
         paras=[("TeSys D", {"bold": True, "size": 13, "color": FOREST}), ("interlocked", {"size": 11, "color": FOREST})])
    arrow(s, 4.31, 5.72, 4.78, 5.62, color="9C7400", width=3)
    arrow(s, 4.31, 6.22, 4.78, 6.32, color="9C7400", width=3)
    rect(s, 4.8, 5.5, 1.55, 0.45, fill=WATER, radius=0.08, paras=[("ATV320 pump", {"bold": True, "size": 11, "color": WHITE})],
         name="SLD load A")
    rect(s, 4.8, 6.0, 1.55, 0.45, fill=COLD, radius=0.08, paras=[("3.8 kW cooler", {"bold": True, "size": 11, "color": WHITE})],
         name="SLD load B")

    card(s, 6.8, 2.3, 5.93, 4.4, name="Sequence card")
    text(s, 7.05, 2.42, 5.4, 0.3, "Five-step zero-current transfer", size=15, bold=True, color=FOREST)
    steps = [("Saturation or quota reached", "30 cm probe hits 45% field capacity, or the daily entitlement is used.", "T = 0 s", WATER),
             ("Controlled VFD ramp-down", "Modbus Reg 8502 takes the ATV320 to 0 Hz over 8 s.", "0 → 8 s", WATER),
             ("Zero-flow valve closure", "Latching solenoid shuts at zero velocity: no water hammer.", "T = 8 s", WATER),
             ("5 s DC dead-band", "Bus capacitors discharge and DC current reaches 0 A.", "8 → 13 s", "9C7400"),
             ("TeSys D transfer", "Interlocked contactor energises the 3.8 kW compressor.", "T = 13.2 s", COLD)]
    for i, (t, d, tm, col) in enumerate(steps):
        y = 2.88 + i * 0.76
        circle(s, 7.05, y + 0.08, 0.5, str(i + 1), col, size=14)
        text(s, 7.75, y, 3.55, 0.3, t, size=14, bold=True, color=FOREST)
        text(s, 7.75, y + 0.28, 3.6, 0.45, d, size=11.5, color=INK)
        pill(s, 11.45, y + 0.12, 1.15, 0.32, tm, TINT_GREEN if i != 3 else TINT_GOLD, INK, size=11, name=f"Time chip {i+1}")
    footer(s, "Break-before-make interlock per IEC 60947-4-1 · Type-2 DC SPD rated 1,000 V DC · LC1D09BD dual interlocked "
              "pair, 150 ms break, 5 s dwell. " + SRC_MODEL, 5)
    notes(s, "POWER (60 s). Honest energy partition for the host farm's 4.8 kWp array: 6,559 kWh/yr. Pumping uses "
             "2,422 kWh (37%). The shared 2 MT pre-cooler serves a 4-farm cluster: 4 farms x 15 batches = 60 batches/yr, "
             "17.7 kWh each (13.7 kWh pull-down at COP 3.0 + 4.0 kWh hold) = 1,062 kWh, i.e. 26% of the host farm's "
             "4,137 kWh surplus and 16% of its PV output. The other three farms' arrays are not used. 3,075 kWh (47%) "
             "stays as headroom, shown for transparency and NOT counted in any benefit. Note the correction vs earlier "
             "drafts: cooling energy follows tonnes cooled (120 t/yr for the cluster = 33% of the room's 360 t/yr "
             "capacity), not days of operation. Safety: transfer happens only at 0 A after an 8 s ramp-down, closed "
             "solenoid and 5 s dead-band; the TeSys pair is mechanically and electrically interlocked.")
    return s


def slide06(prs):
    s = blank(prs)
    header(s, "THERMAL ENGINEERING  ·  DECENTRALISED COLD CHAIN",
           [("Halving Farm-Gate Tomato Spoilage: ", {}), ("8.37% to 4.00%", {"color": COLD})],
           "A shared 2 MT pre-cooler pulls harvest-hot tomatoes from 32 °C to a safe 12 °C within four hours.",
           kicker_w=4.4)
    card(s, 0.6, 2.3, 3.05, 4.4, name="Image card")
    image(s, os.path.join(HERE, "assets", "tomato_still.jpg"), 0.75, 2.45, h=3.75,
          alt="Illustrative close-up of three vine tomatoes with water droplets", name="Tomato image")
    text(s, 0.75, 6.3, 2.8, 0.3, "Illustrative image", size=10, color=SLATE)
    kp = [("1.31 t", "tomatoes saved per ha per year (2.51 t → 1.20 t)", COLD),
          ("₹15,732", "spoilage saved per year at ₹12/kg", EMERALD),
          ("₹12,000", "price timing: hold crates for the evening mandi (+₹1–2/kg on 8 t)", WATER)]
    for i, (big, cap, col) in enumerate(kp):
        x = 3.85 + i * 3.0
        card(s, x, 2.3, 2.88, 1.3, name=f"KPI card {i+1}")
        text(s, x + 0.15, 2.38, 2.6, 0.5, big, size=28, bold=True, color=col)
        text(s, x + 0.15, 2.92, 2.6, 0.62, cap, size=11.5, color=INK)
    card(s, 3.85, 3.75, 4.2, 2.0, name="Spoilage chart card")
    text(s, 4.05, 3.82, 3.9, 0.3, "Farm-stage loss, % of harvest", size=14, bold=True, color=FOREST)
    charts.column(s, 3.95, 4.1, 4.0, 1.62, ["Today", "With pre-cooling"], [8.37, 4.0], ["E8A0A0", COLD],
                  fmt='0.00"%"', vmax=10.8, size=12, label_size=14, gap=70, name="Spoilage chart",
                  alt="Column chart: farm-stage tomato loss 8.37% today, 4.00% with pre-cooling")
    card(s, 8.25, 3.75, 4.48, 2.0, name="Physics card")
    text(s, 8.45, 3.82, 4.1, 0.3, "Thermal physics", size=14, bold=True, color=FOREST)
    text(s, 8.45, 4.15, 4.1, 1.55,
         [[("41 kWh ", {"bold": True}), "of heat removed per 2 MT batch (32 → 12 °C)."],
          [("13.7 kWh ", {"bold": True}), "of electricity at COP 3.0: 3.43 kW for 4 h, within the 4.8 kWp array."],
          [("12 °C setpoint ", {"bold": True}), "avoids chilling injury below 10 °C. Phase-change plates hold overnight."]],
         size=12.5, space_after=5)
    rect(s, 3.85, 5.9, 8.88, 0.8, fill=TINT_GREEN, radius=0.1, name="Net gain strip", align="l", pad=0.2,
         paras=[[("Net farmer gain ₹25,332 per year ", {"bold": True, "size": 17, "color": FOREST}),
                 ("= ₹15,732 + ₹12,000 − ₹2,400 opex", {"size": 13, "color": INK})],
                [("Embodied emissions avoided: 0.39 t CO₂e per ha per year", {"size": 13, "color": INK})]])
    footer(s, "Sources: NABCONS 2022 for MoFPI (tomato farm-stage loss 8.37%, total 11.62%) · 12 °C chilling threshold per ICAR-CIPHET guidance · "
              "30 t/ha/yr yield, ₹12/kg farm-gate price are model assumptions. " + SRC_MODEL, 6)
    notes(s, "COLD CHAIN (45 s). NABCONS 2022 reports 8.37% farm-stage loss for tomato (11.62% in total). Rapid pull-down "
             "to 12 C is assumed to cut farm-stage loss to 4.00%, not zero. On a 30 t/ha/yr yield that preserves 1.31 t, "
             "worth Rs 15,732 at Rs 12/kg. Price timing (holding crates for the evening mandi, +Rs 1-2/kg on 8 t) adds "
             "Rs 12,000 and is price-volatile (medium confidence). Opex Rs 2,400/yr. Net Rs 25,332/yr. Thermal: "
             "2,000 kg x 3.7 kJ/kg.K x 20 K = 41.1 kWh thermal, 13.7 kWh electric at COP 3.0, 3.43 kW over a "
             "4 h window. Carbon: only the embodied emissions of tomatoes that are NOT wasted are counted: 1.31 t x "
             "0.30 kg CO2e/kg = 0.39 t CO2e/ha/yr. Solar cooling is not credited against diesel because smallholders "
             "have no cooling today. The 4.00% post-cooling loss is a design target to be measured in the pilot.")
    return s


def slide07(prs):
    s = blank(prs)
    header(s, "COGNITIVE TRUST  ·  DETERMINISTIC VERNACULAR AI",
           [("Vernacular Advice Grounded in ", {}), ("Hardware Truth", {"color": EMERALD})],
           "Spoken Marathi and Hindi advisories on WhatsApp. The AI can read telemetry; it can never switch a contactor.",
           kicker_w=4.6)
    card(s, 0.6, 2.3, 5.9, 4.4, name="Pipeline card")
    text(s, 0.85, 2.42, 5.4, 0.3, "Four-stage trust pipeline", size=15, bold=True, color=FOREST)
    st = [("Edge telemetry", "MCU logs FDR moisture, flow and VFD status over Modbus RTU."),
          ("Schema validation", "Pydantic checks every JSON record; bad data blocks the model."),
          ("Read-only RAG prompt", "Copilot sees telemetry and agronomy templates, with no tool access."),
          ("Voice synthesis", "Marathi / Hindi audio delivered as a WhatsApp voice note.")]
    for i, (t, d) in enumerate(st):
        y = 2.85 + i * 0.7
        circle(s, 0.85, y + 0.05, 0.46, str(i + 1), FOREST, size=13)
        text(s, 1.45, y, 4.9, 0.28, t, size=14, bold=True, color=FOREST)
        text(s, 1.45, y + 0.27, 4.95, 0.4, d, size=12, color=INK)
    rect(s, 0.85, 5.62, 5.4, 0.5, fill="0F2A22", radius=0.06, align="l", pad=0.12, name="JSON snippet",
         paras=[('{"vwc_30cm": 0.448, "status": "FC_CUTOFF", "pv_kw": 4.21, "load": "PRE_COOLER"}',
                 {"font": MONO, "size": 10.5, "color": "9FE8B5"})])
    rect(s, 0.85, 6.17, 5.4, 0.47, fill=TINT_RED, radius=0.06, align="l", pad=0.12, name="Safety invariant",
         paras=[[("Hard invariant: ", {"bold": True, "color": ALARM}),
                 ("only the FreeRTOS state machine switches power; a manual IP67 switch overrides.", {"color": INK})]],
         size=11)
    # WhatsApp mock
    rect(s, 6.75, 2.3, 5.98, 4.4, fill="E6EDE8", line=BORDER, radius=0.12, shadow=True, name="Phone card")
    rect(s, 6.75, 2.3, 5.98, 0.6, fill=EMERALD, radius=0.12, name="Chat header")
    rect(s, 6.75, 2.62, 5.98, 0.28, fill=EMERALD, name="Chat header fill")
    circle(s, 6.95, 2.4, 0.4, "K", WHITE, color=EMERALD, size=14)
    text(s, 7.5, 2.4, 4.0, 0.45, [("Krishi Mitra", {"bold": True, "size": 14, "color": WHITE}),
                                  ("WhatsApp voice advisory · Nashik cluster", {"size": 10, "color": "D6F0DF"})], size=12)
    rect(s, 6.95, 3.1, 5.3, 2.35, fill=WHITE, radius=0.12, name="Voice bubble")
    text(s, 7.15, 3.2, 4.9, 1.2,
         "रामभाऊ, तुमच्या टोमॅटोच्या मुळांना पुरेसे पाणी मिळाले आहे (४४.८%). पंप सुरक्षितपणे बंद झाला असून "
         "सौर वीज शीतगृहाकडे वळवली आहे.", size=17, font=DEVA, color=INK, line_spacing=1.0, name="Marathi message")
    rect(s, 7.15, 4.4, 4.9, 0.42, fill="E8F3EC", radius=0.21, name="Voice bar")
    rect(s, 7.2, 4.44, 0.34, 0.34, fill=EMERALD, shape=MSO_SHAPE.ISOSCELES_TRIANGLE, name="Play").rotation = 90
    rect(s, 7.7, 4.59, 3.1, 0.05, fill="B9D6C5", radius=0.02)
    rect(s, 7.7, 4.59, 1.5, 0.05, fill=EMERALD, radius=0.02)
    text(s, 10.9, 4.46, 1.1, 0.3, "0:14 / 0:26", size=10.5, color=SLATE, font=MONO)
    text(s, 7.15, 4.9, 4.9, 0.5,
         "Translation: “Rambhau, your tomato roots have reached optimal moisture (44.8%). Pumping stopped safely; "
         "solar power now runs the cold room.”", size=10.5, italic=True, color=SLATE)
    rect(s, 8.55, 5.6, 3.7, 0.5, fill="DCF8C6", radius=0.12, name="Reply bubble")
    text(s, 8.7, 5.6, 3.4, 0.5, "धन्यवाद! उद्या पाणी कधी सुरू होईल?", size=14, font=DEVA, color=INK, anchor="m")
    text(s, 6.95, 6.2, 5.6, 0.45, "UX artifact: 20-second voice notes at key state changes (pumping done, cold room online); "
                                  "built for zero-literacy use.", size=11, color=SLATE)
    footer(s, "AI architecture: deterministic agentic RAG · FastAPI backend · FreeRTOS edge firmware · Pydantic schema. "
              "Marathi text to be reviewed by a native speaker before field use.", 7)
    notes(s, "TRUST (40 s). Farmers do not use dashboards, so the interface is a 20-second WhatsApp voice note in Marathi "
             "or Hindi, sent at state changes: pumping done, cold room online. The model is deliberately boxed in: "
             "stage 1 the MCU logs telemetry; stage 2 Pydantic validates the JSON and blocks the LLM if data is "
             "missing; stage 3 a read-only RAG prompt sees only telemetry and agronomy templates; stage 4 TTS. LLMs "
             "never control contactors; all switching is by the deterministic FreeRTOS state machine and a manual "
             "override on the IP67 box. This screen is also the UX design artifact requested in the Challenge 01 "
             "deliverables. Control works offline; the advisory needs 4G.")
    return s
