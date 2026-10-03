# -*- coding: utf-8 -*-
"""Slides 8-10: unit economics, roadmap, summary."""
import kit
from kit import *
import charts

SRC_MODEL = "Model: research/08_IMPACT/impact_model.py (1 ha tomato, Nashik, 4.8 kWp PM-KUSUM Component B pump)."


def slide08(prs):
    s = blank(prs)
    header(s, "COMMERCIAL FEASIBILITY  ·  UNIT ECONOMICS",
           [("₹50,212 Net Capex per Farm, ", {}), ("Payback in 2.0 Years", {"color": EMERALD})],
           "A farm's share of a 4-farm pre-cooler after the 35% subsidy. The ₹7,540 edge controller is separate "
           "and pays back in 1.5 years.", kicker_w=4.2)
    card(s, 0.6, 2.3, 6.2, 3.4, name="Capex card")
    text(s, 0.85, 2.42, 5.7, 0.3, "Capex waterfall, ₹ thousand per 4-farm cluster", size=15, bold=True, color=FOREST)
    charts.waterfall(s, 0.7, 2.75, 6.0, 2.9,
                     ["Gross pre-cooler", "Shared PV avoided", "Net system", "35% subsidy", "Cluster net", "Per farm (÷4)"],
                     [0, 309, 0, 200.85, 0, 0], [400, 91, 309, 108.15, 200.85, 50.2],
                     [FOREST, "D9A400", FOREST, "D9A400", FOREST, EMERALD],
                     ["₹400k", "−₹91k", "₹309k", "−₹108k", "₹201k", "₹50.2k"], vmax=470, size=11, label_size=12, label_colors=[WHITE, INK, WHITE, INK, WHITE, WHITE],
                     name="Capex waterfall", alt="Waterfall: gross 400k, minus shared PV 91k, net 309k, minus 35% subsidy 108k, "
                                                 "cluster net 201k, per farm 50.2k rupees")
    card(s, 7.0, 2.3, 5.73, 3.4, name="Cash flow card")
    text(s, 7.25, 2.42, 5.3, 0.3, "Cumulative cash flow per farm, ₹ thousand", size=15, bold=True, color=FOREST)
    charts.line(s, 7.1, 2.75, 5.55, 2.9, ["Day 0", "Month 6", "Month 12", "Month 18", "Month 24"],
                [-50.212, -37.546, -24.880, -12.214, 0.452], EMERALD, '"₹"#,##0.0"k";"−₹"#,##0.0"k"', -60, 15,
                size=11, label_size=12, name="Cash flow chart",
                alt="Line chart of cumulative cash flow from minus 50.2k rupees at day 0 to plus 0.5k at month 24")
    tiles = [("Annual farmer gain", "₹25,332", "₹15,732 spoilage + ₹12,000 timing − ₹2,400 opex", EMERALD),
             ("Edge controller BoM", "₹7,540", "Pays back in 1.5 yr; ≈1.9 yr combined with the cooler share", WATER),
             ("Tier B FPO hub (5 MT)", "4.2 yr", "Own array, leasing: ₹780k net capex, ₹184k/yr net revenue", COLD)]
    for i, (t, big, d, col) in enumerate(tiles):
        x = 0.6 + i * 4.1
        card(s, x, 5.85, 3.95, 0.92, name=f"Tile {i+1}")
        text(s, x + 0.15, 5.9, 3.7, 0.25, t, size=11, bold=True, color=SLATE)
        text(s, x + 0.15, 6.16, 1.4, 0.5, big, size=22, bold=True, color=col)
        text(s, x + 1.55, 6.17, 2.3, 0.55, d, size=10.5, color=INK)
    footer(s, "Assumes 35% MIDH/AIF support (3.0 yr payback without it), ₹35,000/kWp PV, 30 t/ha yield, ₹12/kg. Excludes drip hardware "
              "(assumed in place) and the host farm's PV. Controller benefit (~₹5,000/yr) is not in the ₹25,332. " + SRC_MODEL, 8)
    notes(s, "ECONOMICS (60 s). Gross 2 MT pre-cooler (compressor + PCM) Rs 400,000. It needs no PV of its own because it "
             "runs on the host farm's idle surplus, avoiding 2.6 kWp x Rs 35,000 = Rs 91,000. Net Rs 309,000. 35% "
             "MIDH/AIF support = Rs 108,150, leaving Rs 200,850 for the cluster, Rs 50,212 per farm. Annual gain "
             "Rs 25,332: payback 1.98 years (3.0 without subsidy). Month-by-month: -50.2k at day 0, -37.5k at month 6, "
             "-24.9k at month 12, -12.2k at month 18, +0.5k at month 24. 2.0 years = 4 harvests at 2 cycles per year. "
             "Edge controller BoM Rs 7,540 (ESP32-S3, MAX485, FDR probes, SHT31, pyranometer, flow meter, latching "
             "valve, 2 TeSys D, SMPS, SIM7600, IP67 enclosure); standalone payback 1.5 years = 3 seasons on ~Rs 5,000/yr "
             "of water, pump-health and yield protection. Combined (57,752 / 30,332) = 1.9 years. Tier B 5 MT FPO hub "
             "pays back in 4.2 years. Not included: drip hardware, which the saving assumes is already installed.")
    return s


def slide09(prs):
    s = blank(prs)
    header(s, "DEPLOYMENT  ·  DE-RISKED SCALING",
           [("From Digital Twin to a ", {}), ("250-Farm Pilot", {"color": EMERALD})],
           "Each phase has an exit gate. Targets below are plans, not results.", kicker_w=3.4)
    cols = [("PHASE 1", "Q4 2026", "Digital twin", "0 physical units", GREEN,
             ["365-day energy, water and thermal model that reconciles to zero discrepancy",
              "Modbus state machine emulating ATV320 (Reg 8501 / 8502)",
              "Marathi / Hindi advisory prototype"],
             "Exit: mass and energy balances reconcile"),
            ("PHASE 2", "Q1–Q2 2027", "Hardware-in-loop bench", "1 testbench", WATER,
             ["ESP32-S3 with ATV320 and motor dynamometer",
              "500 DC transfer cycles with the 5 s dead-band",
              "Type-2 DC SPD surge endurance at 1,000 V DC"],
             "Exit: 500 faultless transfers, no drive trip"),
            ("PHASE 3", "Q3–Q4 2027", "Nashik FPO pilot", "20 farms · 5 clusters", "C9A100",
             ["Real tomato harvests with continuous FDR monitoring",
              "One shared pre-cooler per 4-farm cluster",
              "Daily WhatsApp voice notes to farmers"],
             "Exit: >35% water saving, ≥95% pre-cooler uptime over 2 seasons"),
            ("PHASE 4", "2028", "Commercial expansion", "250 farms · 5 FPOs", COLD,
             ["Factory-assembled DIN-rail retrofit kits",
              "Urja Mitra: local ITI-trained technicians",
              "Catalogue option with Schneider rural EPCs (proposed)"],
             "Exit: break-even on 5 FPO contracts")]
    for i, (ph, when, title, big, col, bl, gate) in enumerate(cols):
        x = 0.6 + i * 3.07
        shape = MSO_SHAPE.PENTAGON if i < 3 else MSO_SHAPE.PENTAGON
        rect(s, x, 2.25, 3.0, 0.5, fill=col, shape=shape, name=f"{ph} chevron", align="l", pad=0.15,
             paras=[(f"{ph}  ·  {when}", {"bold": True, "size": 12, "color": (INK if col in (GREEN, "C9A100") else WHITE)})])
        card(s, x, 2.9, 2.93, 3.05, name=f"{ph} card")
        text(s, x + 0.15, 3.0, 2.65, 0.3, title, size=14, bold=True, color=FOREST)
        text(s, x + 0.15, 3.3, 2.65, 0.4, big, size=18, bold=True, color=col if col != GREEN else EMERALD)
        text(s, x + 0.15, 3.78, 2.65, 1.5, [{"runs": [("• ", {"bold": True}), b], "space_after": 3} for b in bl], size=11.5)
        rect(s, x + 0.12, 5.3, 2.69, 0.55, fill=TINT_GREEN, radius=0.06, align="l", pad=0.1, name=f"{ph} exit gate",
             paras=[(gate, {"size": 10.5, "bold": True, "color": FOREST})])
    rect(s, 0.6, 6.1, 12.13, 0.65, fill=FOREST, radius=0.1, align="l", pad=0.2, name="Enablers strip",
         paras=[[("Enablers  ", {"bold": True, "color": GREEN}),
                 ("PM-KUSUM Component B (≈10.06 lakh pumps installed, 4.67 lakh in Maharashtra) · Atal Bhujal Yojana · MIDH / AIF 35%.  ",
                  {"color": WHITE}),
                 ("Proposed partners (not yet confirmed): ", {"bold": True, "color": GOLD}),
                 ("Sahyadri Farmers Producer Co., Nashik; Schneider Electric rural EPC channel.", {"color": WHITE})]],
         size=11.5)
    footer(s, "Installed-pump counts: MNRE PM-KUSUM progress reports (31 Jan 2026; Maharashtra figure 30 Nov 2025), as reported. "
              "Phase dates and exit gates are targets.", 9)
    notes(s, "ROADMAP (40 s). Four gated phases. Phase 1 (now, Q4 2026) is the software digital twin: 365-day energy, "
             "water and thermal balances, Modbus emulator, vernacular prototype; this is what Phase 2 of the hackathon "
             "(Oct 11 - Nov 22) builds on. Phase 2 hardware-in-loop bench with an Altivar ATV320 and dynamometer: "
             "500 faultless DC transfers. Phase 3 a 20-farm, 5-cluster pilot in Nashik: exit gate is more than 35% "
             "measured water saving and 95% pre-cooler uptime over two seasons. Phase 4 250 farms across 5 FPOs. "
             "MARKET: about 10.06 lakh Component B pumps installed by 31 Jan 2026 (13.3 lakh sanctioned), 4.67 lakh in "
             "Maharashtra (Nov 2025) - confirm on the MNRE dashboard before quoting. Sahyadri FPO and Schneider's "
             "rural EPC channel are PROPOSED partners; no agreement exists yet - say so if asked.")
    return s


def slide10(prs):
    s = blank(prs, FOREST)
    header(s, "EXECUTIVE SYNTHESIS  ·  YUVA YODHA 2026",
           [("One Solar Pump. ", {}), ("Four Measured Outcomes.", {"color": GREEN})],
           "A connected retrofit layer for Altivar Solar drives and TeSys switchgear that turns standalone pumps "
           "into community microgrids.", dark=True, kicker_w=3.9)
    outs = [("41.2%", GREEN, "less groundwater", "7,000 m³ per ha per year; full crop requirement still met"),
            ("4,137 kWh", GOLD, "idle solar unlocked", "per farm per year once water is right-sized; cooling a 4-farm cluster uses 1,062 kWh"),
            ("1.31 t", "C9A3F5", "tomatoes saved", "per ha per year; farm-stage loss 8.37% → 4.00%"),
            ("2.0 years", "7FD0F7", "capital payback", "₹50,212 net capex per farm; ₹25,332 net gain per year")]
    for i, (big, col, t, d) in enumerate(outs):
        x = 0.6 + i * 3.07
        rect(s, x, 2.35, 2.93, 2.35, fill=FOREST_2, radius=0.12, name=f"Outcome {i+1}")
        text(s, x + 0.2, 2.5, 2.55, 0.6, big, size=30, bold=True, color=col)
        text(s, x + 0.2, 3.12, 2.55, 0.3, t.upper(), size=13, bold=True, color=WHITE)
        text(s, x + 0.2, 3.5, 2.55, 1.2, d, size=14, color=ON_DARK_MUTED)
    rect(s, 0.6, 4.85, 12.13, 0.5, fill=FOREST_2, radius=0.08, align="l", pad=0.2, name="Sustainability strip",
         paras=[[("Sustainability  ", {"bold": True, "color": GREEN}),
                 ("0.39 t CO₂e per ha per year (embodied emissions of avoided spoilage) · 7,000 m³ groundwater conserved · no diesel, no battery",
                  {"color": WHITE})]], size=12.5)
    team = [("Sanskar Tiwari", "Embedded firmware and lead", "FreeRTOS state machine, Modbus RTU, CiA402 drive control"),
            ("Shambhavi Patil", "Geospatial intelligence", "Sentinel-2 NDVI/NDWI, dynamic FAO-56 Kc curves, aquifer balance"),
            ("Kanishka Salgude", "Electrical systems and VFD", "Altivar ATV320 configuration, TeSys D interlocking, DC routing"),
            ("Chaitanya Ranade", "Product and agronomy", "FPO cluster economics, MIDH/AIF subsidies, vernacular WhatsApp UX")]
    for i, (n, r, d) in enumerate(team):
        x = 0.6 + i * 3.07
        rect(s, x, 5.5, 2.93, 1.2, fill="04382A", line="0D8752", radius=0.1, name=f"Team {i+1}", align="l", anchor="t",
             pad=0.15, paras=[(n, {"bold": True, "size": 14, "color": WHITE}), (r, {"size": 11, "bold": True, "color": GREEN}),
                              (d, {"size": 10.5, "color": ON_DARK_MUTED})])
    footer(s, "Schneider Electric synergies: Altivar Solar OEM pre-installation · EcoStruxure microgrid edge integration · SE Ventures cleantech scale.  "
              "Challenge 01: Sustainable Agriculture.  " + SRC_MODEL, 10, dark=True)
    notes(s, "CLOSE (30 s). Four measured outcomes per hectare: 41.2% less groundwater, 4,137 kWh/yr of idle solar "
             "unlocked (of which a 4-farm pre-cooler uses 1,062 kWh), 1.31 t of tomatoes saved, 2.0-year payback. "
             "Carbon claim is deliberately modest: 0.39 t CO2e/ha/yr, embodied emissions of avoided spoilage. For "
             "Schneider: Altivar Solar drives pre-installed with the controller, EcoStruxure-aligned edge integration, "
             "and a cleantech scale path via SE Ventures. Confirm team roster and roles before submission.")
    return s
