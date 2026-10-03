# 11 Presentation Implementation Plan: 10-Slide Master Arc
**Document ID:** PPT-PLAN-2026-V1  
**Deck Format:** 16:9 Widescreen (1920 × 1080 Stage)  
**Theme:** Light Mode (`#F8FAFC` Canvas, `#FFFFFF` Cards, `#090B0C` Typography)  
**Typography:** Poppins (Headings) + Inter (Body) + JetBrains Mono (Tabular Metrics)  
**Target Length:** Exactly 10 Slides  
**Status:** Canonical Implementation Plan  

---

## 1. Ten-Slide Structural Arc

```text
SLIDE 01: TITLE & EXECUTIVE HOOK
• Title: AgroStruxure™: Solar-Synchronized Agri-Energy Microgrid
• Subtitle: Decoupling Groundwater Extraction from Free Solar Energy to Power Farm-Gate Cold Storage
• Visual: Asymmetric 55/45 split with high-res solar farmland photo (assets/solar_panels_farm_opt.jpg)
• Metric Anchors: 41.2% Water Conserved | 3,187 kWh Solar Diverted | 2.0-Year Payback
• Hackathon Context: Yuva Yodha Energy Tech Hackathon 2026 | Schneider Electric India

SLIDE 02: THE SOLAR REBOUND PARADOX (PROBLEM FRAMING)
• Headline: Free Solar Power is Draining India's Aquifers
• Core Conflict: 10.9 Lakh PM-KUSUM Component B solar pumps extract water with zero marginal cost.
  Pumps run continuously beyond agronomic crop needs, wasting 63% of solar power idle and drying borewells.
• Visual: 2-column split pairing rural landscape (assets/indian_agriculture_field.jpg) with a 3-stage breakdown:
  1. Water Waste: 17,000 m³/ha/yr flood irrigation causing waterlogging & salinization.
  2. Idle Solar Surplus: 4,137 kWh/yr sitting unused once tanks fill.
  3. Post-Harvest Rot: 8.37% perishable tomatoes rot at farm-gate without pre-cooling.

SLIDE 03: AGROSTRUXURE™ SYSTEM ARCHITECTURE
• Headline: Closed-Loop Agri-Energy Microgrid Architecture
• Core Concept: A retrofit intelligent edge controller interfacing with PM-KUSUM VFDs to synchronize
  irrigation with soil physics, and redirect surplus solar DC energy to micro-cooling.
• Visual: 3-column architectural pipeline diagram:
  1. Sensing & Physics: Dual FDR soil probes (10cm/30cm) + FAO-56 dual Kc water budget.
  2. Edge Decision: ESP32-S3 FreeRTOS controller executing CiA402 Modbus RTU at 19,200 baud.
  3. Dynamic Actuation: Dual mechanically interlocked TeSys D contactors + pulse flow meter.

SLIDE 04: CLOSED-LOOP IRRIGATION & WATER ENTITLEMENT
• Headline: Cutting Groundwater Withdrawal by 41.2% Without Yield Loss
• Technical Core: 3-Layer Entitlement Engine (Agronomic ETc + Soil Moisture Deficit + Community Aquifer Quota).
  Automatic VFD cutoff when root zone reaches Field Capacity (45%).
• Visual: 50/50 split pairing commercial drip field photo (assets/drip_irrigation_farm.jpg) with
  water balance comparison chart:
  - Baseline Flood: 17,000 m³/ha/yr (4,118 kWh pumping)
  - AgroStruxure Pulsed Drip: 10,000 m³/ha/yr (2,422 kWh pumping)
  - Net Saved: 7,000 m³/ha/yr water saved (41.2%) & 1,696 kWh/yr pumping electricity freed.

SLIDE 05: UPSTREAM DC POWER DIVERSION & SWITCHGEAR
• Headline: Dynamic Solar Routing via Upstream DC Bus Switching
• Technical Innovation: TeSys D mechanical & electrical interlocking switching upstream on the DC bus
  (350–600V DC) rather than destructive downstream VFD AC switching.
• Switching Sequence: 8s VFD ramp-down to 0 Hz → Zero-flow solenoid close → 5s DC dead-band dwell →
  Contactor changeover → 3.8 kW cold storage compressor energization.
• Visual: Industrial schematic diagram of DC bus routing + solar energy distribution chart:
  6,559 kWh total generation → 2,422 kWh pumping (37%) → 3,187 kWh cooling (49%) → 951 kWh residual (14%).

SLIDE 06: FARM-GATE MICRO-COLD CHAIN & POST-HARVEST IMPACT
• Headline: Halving Farm-Gate Spoilage from 8.37% to 4.00%
• Thermodynamic Sizing: 2 MT farm pre-cooler pulling down 2,000 kg tomatoes from 32°C to 12°C in 4 hours
  (3.43 kW thermal load). Utilizes organic Phase Change Material (PCM) thermal buffer holding 12°C overnight.
• Visual: Editorial split with freshly harvested tomato portrait (assets/tomato_harvest.jpg) and
  post-harvest economic metrics:
  - Preserved Produce: 1.31 tonnes/ha/yr of marketable tomatoes.
  - Farmer Revenue Gain: +₹15,732/yr direct produce preservation (+₹12,000/yr distress-sale avoidance).

SLIDE 07: KRISHI MITRA: ZERO-HALLUCINATION VERNACULAR AI
• Headline: Deterministic Grounded Intelligence for the Smallholder
• Core Safety Principle: Deterministic Agentic RAG architecture. LLM has ZERO actuation authority;
  it only explains edge telemetry in spoken Marathi, Hindi, and English over WhatsApp voice notes.
• Visual: Visual dual-panel layout showing:
  - Left: Edge Modbus telemetry JSON payload (soil moisture 44.8%, VFD 42 Hz, solar 820 W/m²).
  - Right: Farmer-facing WhatsApp vernacular card: "पाणी देणे पूर्ण झाले. वीज आता शीतगृहाकडे वळवली आहे."
    ("Irrigation complete. Solar power safely redirected to cold room.")

SLIDE 08: BOM ECONOMICS, UNIT COSTS & FARMER ROI
• Headline: Industrial Feasibility with a 2.0-Year Cluster Payback
• Controller BOM: ₹7,540 at 1,000-unit industrial volume (ESP32-S3, TeSys D contactors, Type-2 SPD, IP67).
• Tier A Cluster Model: 4 smallholder farms share one 2 MT pre-cooler unit.
  - Gross Capex: ₹400,000 | Less shared PV array savings: -₹91,000 | Net: ₹309,000.
  - After 35% MIDH/AIF capital subsidy: ₹200,850 total (₹50,212 per farm).
  - Net Farmer Benefit: ₹25,332/farm/yr → Payback in exactly 2.0 years (2 crop cycles).
• Standalone Controller Payback: 1.5 crop seasons.

SLIDE 09: PILOT DEPLOYMENT & SCALABILITY ROADMAP
• Headline: From Software Digital Twin to 250-Farm Field Pilot
• Phased Scalability:
  - Phase 1 (Now): Validated mathematical model (`impact_model.py`) & software simulator (`AgroSim`).
  - Phase 2 (Q1 2027): Hardware-in-the-loop testbench with physical Altivar ATV320 & TeSys D switchgear.
  - Phase 3 (Q3 2027): 20-farm pilot in Nashik district under Sahyadri Farmers Producer Company.
  - Phase 4 (2028): 250-farm commercial expansion across 5 FPOs in Maharashtra & Rajasthan.
• Visual: Structured milestone timeline with clear exit gates and FPO partnership structure.

SLIDE 10: TEAM, VISION & SCHNEIDER SYNERGY
• Headline: Engineering Sustainable Abundance for Indian Agriculture
• Schneider Synergy: Natural commercial skid retrofit for Schneider Altivar Solar drives;
  distribution via Schneider Electric India rural network and SE Ventures climate portfolio.
• Verified Team Members & Roles:
  - Sanskar Tiwari: Embedded Firmware & Hardware Lead (ESP32-S3, FreeRTOS, Modbus Master)
  - Shambhavi Patil: Geospatial Intelligence & Agronomy Lead (Google Earth Engine, Sentinel-2, FAO-56)
  - Kanishka Salgude: Electrical Architecture & Power Systems Lead (TeSys D Switchgear, DC Bus, VFD)
  - Chaitanya Ranade: Product Strategy & Farm Systems Lead (Smallholder UX, FPO Economics, Field Pilot)
• Closing Call: "Powering India's agricultural clean-tech transition—one solar drop at a time."
```
