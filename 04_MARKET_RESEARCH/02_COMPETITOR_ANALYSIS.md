# 02 Competitor Analysis & Benchmarking

**Document Code:** MKT-COMP-02  
**Domain:** Direct & Indirect Competitor Deep Dive  

---

## 1. Comprehensive Competitor Profile Matrix

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    COMPETITIVE BENCHMARKING MATRIX                                     │
├─────────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────────────────┤
│ Attribute       │ Kisan Raja   │ Fasal        │ Ecozen       │ Cultyvate    │ Our Proposed             │
│                 │ (Entelechy)  │ (Wolkus)     │ (Ecotron)    │              │ Architecture             │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Origin Country  │ India        │ India        │ India        │ India        │ India                    │
│ Primary Focus   │ Motor Remote │ Precision    │ Solar Pump   │ Paddy/Cane   │ Integrated Solar Energy, │
│                 │ Switching    │ Horticulture │ VFD / RMS    │ Irrigation   │ Irrigation & Cold-Chain  │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Upfront Hardware│ ₹4,000 –     │ ₹20,000 –    │ ₹35,000 –    │ ₹25,000+     │ Ultra-low-cost retrofit: │
│ Cost to Farmer  │ ₹6,500       │ ₹30,000      │ ₹65,000 (VFD)│ (Custom)     │ <₹3,500 (Sensor + Valve) │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Energy Source   │ Grid AC      │ Battery / PV │ Solar PV     │ Grid / Pump  │ Solar PV + Grid Hybrid   │
│ Awareness       │ (No Solar)   │ (Node only)  │ (DC Inverter)│ (No Solar)   │ (Altivar VFD Integration)│
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Water Demand    │ None (Manual │ Advanced AI  │ None         │ Advanced     │ Physics-based FAO-56 ET0 │
│ Model (ET0)     │ On/Off)      │ (Cloud ML)   │ (Motor Only) │ Crop Model   │ + TinyML Soil Balance    │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Closed-Loop     │ None         │ Advisory     │ None         │ Automated    │ Automated Solenoid Pulse │
│ Actuation       │ (No Valves)  │ Only (App)   │ (Manual)     │ Valves       │ Actuation + Manual Bypass│
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Surplus Energy  │ None         │ None         │ Partial      │ None         │ Dynamic Smart Switching  │
│ Diversion       │              │              │ (Off-grid)   │              │ to Micro-Cold Storage    │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Offline Edge    │ Basic Relay  │ Buffers data │ Basic VFD    │ Requires     │ Full Autonomous Edge     │
│ Resilience      │ Logic        │ to Cloud     │ Control      │ Connectivity │ Decision Loop (No Cloud) │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────────┤
│ Schneider OT/IT │ None         │ None         │ Competitor   │ None         │ Native EcoStruxure™      │
│ Synergy         │              │              │ VFD          │              │ Alignment & Modbus RTU   │
└─────────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────────────────┘
```

---

## 2. Granular Competitor Breakdown

### 1. Fasal (Wolkus Technology Solutions)
* **Hardware:** Proprietary in-field microclimate station with multi-depth soil moisture sensors, ambient temperature, humidity, rainfall, and leaf wetness.
* **Software:** Cloud AI/ML engine delivering micro-irrigation alerts, pest/disease warnings, and spray scheduling.
* **Strengths:** Highly accurate agronomic data models; strong adoption in export-oriented grapes, pomegranates, and chillies in Maharashtra and Karnataka.
* **Weaknesses:** High capex barrier (₹20k–₹30k upfront + annual subscription). Completely inaccessible to cereal, pulse, and smallholder farmers (<2 ha). No integration with solar pumping dynamics or power diversion. Advisory-only: requires the farmer to manually walk to the field to turn the valve.

### 2. Ecozen Solutions (Ecotron & Ecofrost)
* **Hardware:** Ecotron solar pump controller with high-efficiency MPPT (98%+ conversion efficiency) supporting induction, PMSM, and BLDC motors; Ecofrost solar-powered micro-cold storage room.
* **Software:** Ecozen Connect / RMS platform with GPS tracking, cloud telemetry, and mobile monitoring.
* **Strengths:** Market leader in PM-KUSUM solar pump drives; robust IP65 hardware engineering; proven cold storage technology.
* **Weaknesses:** Systems operate largely in silos. The solar pump controller regulates motor speed and telemetry, but does not calculate dynamic agronomic crop water balance ($ET_0$) or automate field valves based on soil moisture. High capital cost when purchased outside government subsidies.

### 3. Kisan Raja (Entelechy Systems)
* **Hardware:** GSM-based retrofittable motor starter controller with voltage surge protection, dry-run protection, and phase-loss sensing.
* **Software:** IVRS voice calls, SMS commands, and mobile app for remote switching.
* **Strengths:** Highly affordable (₹4,000–₹6,000); deeply trusted by Indian farmers; simple to install on existing DOL/Star-Delta starters; vernacular voice alerts.
* **Weaknesses:** Zero water intelligence. Gives the farmer remote control to waste water from their bed. Does not prevent aquifer depletion or optimize energy consumption.
