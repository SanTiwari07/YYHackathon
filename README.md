<p align="center">
  <img src="assets/schneider_logo.png" alt="Schneider Electric Logo" width="280"/>
</p>

# AgroStruxure™: An Agricultural Energy Orchestration Platform for Schneider Solar Infrastructure

## Yuva Yodha Energy Tech Hackathon 2026 · Challenge 01: Sustainable Agriculture
### Host: Schneider Electric India | Team: Team Paladrex

> **Core Invention:** Dynamically reallocating surplus solar generation from irrigation to farm-gate thermal storage.

AgroStruxure™ is proposed to Schneider Electric India as an **OEM skid and software package** that extends **EcoStruxure™** (Connected Products → Edge Control → Cloud Apps & Analytics). It converts a single-function solar pump inverter (Schneider Altivar Solar ATV320) into a multi-load agricultural energy microgrid hub across India's **816,710 installed PM-KUSUM Component-B solar pumps** (MNRE, Aug 2026). Schneider's rural EPC channel and Sahyadri Farmers Producer Co. are **proposed partners**.

---

## 🏆 Team Paladrex & Engineering Credentials

<p align="left">
  <b>Team Credentials & National Awards:</b>
  <br/>
  • 🏆 <b>Winner, Pune Agri Hackathon 2026:</b> Awarded by the <b>Chief Minister of Maharashtra</b> (Currently working with Govt. of Maharashtra).
  <br/>
  • 🥈 <b>Top 3, VOIS Innovation Marathon 2026:</b> Selected out of 630+ teams nationwide (Backed by Vodafone Idea).
  <br/>
  • 🥇 <b>1st Rank, Techfiesta 2026 Agriculture Domain:</b> International domain competition winner.
</p>

### 👥 Team Member Roles & Technical Domains

| Member | Title / Role | Core Technical Focus |
| :--- | :--- | :--- |
| **Member 1** | **Embedded IoT & Hardware Lead** | ESP32-S3 FreeRTOS Firmware, RS485 Modbus RTU (Altivar CiA402 Profile), DC Switchgear |
| **Member 2** | **Hydrology & Agronomy Specialist** | FAO-56 Evapotranspiration Modelling, Soil Moisture Telemetry (FDR Probes), Crop Entitlement |
| **Member 3** | **System Architect & Thermal Lead** | Solar PV Surplus Thermodynamics, 2 MT PCM Cold Storage Pull-Down, `AgroSim` Digital Twin |
| **Member 4** | **Cloud Backend & Vernacular AI Lead** | Python FastAPI Microservices, TimescaleDB Telemetry, Multilingual WhatsApp Audio Copilot |

---

## 📁 Repository Structure: Completed Deliverables vs. Research Work

The repository is organized into **Completed Core Deliverables** and a centralized **Research Directory**:

```
YYHackathon/
├── 📄 agrostructure.pdf                   ★ Primary Pitch Deck Presentation (PDF)
├── 📄 AgroStruxure_YuvaYodha_2026_Final.pdf  Native Presentation PDF Proof
├── 📊 AgroStruxure_YuvaYodha_2026_Final.pptx Native Editable PowerPoint Deck (16:9)
│
├── 📂 docs/                               ★ COMPLETED CANONICAL SPECIFICATIONS
│   ├── 06_PRODUCT_TRUTH.md               Twenty Dimensions of Product Truth & Guardrails
│   ├── 08_CLAIM_LEDGER.md               Single Source of Quantitative Truth & Derivations
│   ├── DESIGN_SYSTEM.md                  Schneider QuartzDS (@quartzds) Visual Specifications
│   ├── COMPONENT_SPECIFICATIONS.md       Hardware & Sensor Datasheet Specifications
│   └── PAGE_SPECIFICATIONS.md            UI Cockpit Specifications
│
├── 📂 research/                           ★ CENTRALIZED RESEARCH WORK & AUDITS
│   ├── 00_ADMIN/                         Competition Admin & Guidelines
│   ├── 01_HACKATHON/                     Hackathon Track Analysis & Scoring Criteria
│   ├── 02_SCHNEIDER_ELECTRIC/            Schneider Product Catalog, Altivar & EcoStruxure Research
│   ├── 03_PS1/                           Problem Statement 1 Deep Dive
│   ├── 04_MARKET_RESEARCH/               PM-KUSUM Statistics & Crop Economics Data
│   ├── 05_TECHNICAL_RESEARCH/            Modbus RTU, FDR Sensors, PCM Thermodynamics
│   ├── 06_OLD_WORK_AUDIT/                Audit of Prior Codebases & References
│   ├── 07_SOLUTION_DESIGN/               System Architecture & DC Bus Changeover Design
│   ├── 08_IMPACT/                        impact_model.py (Executable Python Impact Model)
│   ├── 09_PROTOTYPE/                     Firmware & Software Simulation Logic
│   ├── 10_DEPLOYMENT/                    FPO Clustering & Commercialization Plan
│   ├── 11_SUBMISSION/                    Portal Proposals (EXEC_SUMMARY_500W.md, PROPOSAL.md)
│   └── 12_SOURCES/                       Academic Papers, NABCONS & MNRE Reference Links
│
├── 📂 presentation/                       ★ PRESENTATION BUILD SYSTEM & PROOFS
│   ├── build/                            python-pptx Builders (build_deck.py, kit.py, slides_a/b/c.py)
│   ├── qa/                               1920x1080 Slide Proof Screenshots
│   └── docs/                             Audit & Rebuild Changelog
│
└── 📂 assets/                             ★ MEDIA & BRAND ASSET LEDGER
    ├── schneider_logo.png                Schneider Brand Logo
    ├── drip_irrigation_farm.jpg          Field Telemetry Imagery
    └── ASSET_LEDGER.md                   Media Registry
```

---

## ⚡ Executive Summary: System Architecture & Impact

### 1. The Problem
Solar electricity under PM-KUSUM Component B is free to the farmer, so nothing limits pumping, causing severe groundwater table decline. Once irrigation is right-sized, **63.1% (4,137 kWh/yr)** of the 4.8 kWp solar array's output sits idle. Meanwhile, **8.37% of perishable horticulture produce rots** at the farm gate due to zero chilling (NABCONS 2022).

### 2. The Solution
A ₹7,540 (1,000-unit BOM) industrial edge controller executes an **FAO-56 Penman-Monteith water entitlement**, monitors dual-depth FDR soil moisture probes, stops the pump at field capacity, and makes a **controlled zero-current transition** through interlocked **Schneider TeSys D contactors (2x LC1D09BD)** to a shared 2 MT Phase Change Material (PCM) pre-cooler serving a 4-farm cluster.

### 3. Dual-Plane System Architecture
* **Control Plane:** Sensors (Soil FDR, Pulse Flow, PV, Temp) → ESP32-S3 Edge Controller → Modbus RTU Commands (CiA402 Profile) → **Schneider Altivar ATV320 Solar VFD**.
* **Power Plane:** PV Array (4.8 kWp DC Bus) → Power Conversion / Interlocked Switching Stage → Load A (Solar Pump) / Load B (2 MT PCM Chiller).

```
                     SOLAR PV ARRAY (4.8 kWp)
                               │
                               ▼
                   [ Altivar ATV320 Solar VFD ]
                               │
                               ▼
     ┌───────────────────────────────────────────────────┐
     │ CONTROL PLANE: AgroStruxure Edge Controller      │
     │ (ESP32-S3 FreeRTOS · FAO-56 Engine · Modbus RTU)  │
     └─────────────────────────┬─────────────────────────┘
                               │
       ┌───────────────────────┴───────────────────────┐
       ▼ [CURRENT PROTOTYPE]                           ▼ [EXPANSION ROADMAP]
  PRIMARY LOAD           SECONDARY LOAD             EXPANDABLE PORTFOLIO
  Solar Pumping          PCM Cold Storage           Productive Farm Loads
  (FAO-56 Drip)          (2 MT PCM Chiller)         • Crop Drying
                                                    • Packhouse Sorting/Grading
                                                    • Dairy Milk Chilling
                                                    • Water Purification
```

---

## 📊 Transparent 3-Step Solar Energy Balance

Calculated per hectare of tomato in Nashik on a 4.8 kWp pump array (`research/08_IMPACT/impact_model.py`):

```text
STEP 1: TOTAL PV GENERATION
4.8 kWp Array (Nashik Insolation) ───────────────────────────────────► 6,559 kWh/yr (100.0%)

STEP 2: OPTIMIZED IRRIGATION DEMAND
FAO-56 Rightsized Drip Pumping ──────────────────────────────────────► 2,422 kWh/yr (36.9%)
                                                                      ───────────────────────
AVAILABLE SURPLUS AFTER IRRIGATION                                    = 4,137 kWh/yr (63.1%)

STEP 3: PCM COLD STORAGE ALLOCATION
4-Farm Cluster Pre-Cooler (1,062 kWh/yr total) ──────────────────────► 1,062 kWh/yr (16.2%)
                                                                      ───────────────────────
REMAINING UNALLOCATED HEADROOM (Consciously Unclaimed)                = 3,075 kWh/yr (46.9%)
```

> **Key Energy Finding:** PCM pre-cooling requires 1,062 kWh/yr—just **43% of the 2,442 kWh/yr idle PV already available in the flood baseline**.

---

## 🛠️ Hardware Integration with Schneider Portfolio

| Schneider Product | Industrial Role in AgroStruxure™ | Interface & Protocol |
| :--- | :--- | :--- |
| **Altivar ATV320 Solar VFD** | Drives borewell pump (Load A); ramped to 0 Hz in 8 s before load transfer | Modbus RTU Master on ESP32-S3: Reg `8501` (Command), Reg `8502` (Frequency); CiA402 profile per Doc NVE41308 |
| **TeSys D Contactors (2× LC1D09BD)** | Mechanically & electrically interlocked changeover on 350–600V DC bus | Controlled zero-current transition (5s dead-band dwell parameter for HIL testing) |
| **EcoStruxure Architecture** | Connected Products → Edge Control → Cloud Apps & Analytics | MQTT over TLS to Python FastAPI microservices & Vernacular WhatsApp Copilot |
| **Schneider QuartzDS (`@quartzds`)** | Industrial UI design system compliance | Emerald Green (`#3DCD58`), Dark Surface (`#0F1416`), Slate Neutrals |

---

## 🗓️ Hackathon Submission & Milestone Roadmap

- 🟢 **Phase 1 (Completed):** Software Digital Twin, Reproducible Math Engine (`impact_model.py`), Presentation Decks & Documentation.
- 🟡 **Phase 2 (Prototype Window: Oct 11 – Nov 22, 2026):** Physical Hardware-in-the-Loop (HIL) Test Bench with Altivar ATV320 & TeSys D Switchgear.
- 🔵 **Phase 3 (Proposed Pilot):** 20-Farm FPO Cluster Field Pilot in Nashik (Proposed: Sahyadri FPO).
- 🟣 **Phase 4 (National Scale):** OEM Skid Pre-assembly & Distribution via Schneider Rural EPC Channel.

---

### 📥 Deliverables & Quick Links
- **Primary Pitch Presentation (PDF):** [`agrostructure.pdf`](./agrostructure.pdf)
- **Editable PowerPoint Deck (PPTX):** [`AgroStruxure_YuvaYodha_2026_Final.pptx`](./AgroStruxure_YuvaYodha_2026_Final.pptx)
- **Product Truth Specification:** [`docs/06_PRODUCT_TRUTH.md`](./docs/06_PRODUCT_TRUTH.md)
- **Quantitative Claim Ledger:** [`docs/08_CLAIM_LEDGER.md`](./docs/08_CLAIM_LEDGER.md)
- **Mathematical Impact Model:** [`research/08_IMPACT/impact_model.py`](./research/08_IMPACT/impact_model.py)
- **Executive Submission Summary:** [`research/11_SUBMISSION/EXEC_SUMMARY_500W.md`](./research/11_SUBMISSION/EXEC_SUMMARY_500W.md)
2 prototype and evaluation window:** October 11 to November 22, 2026.
* **Top 10 announced:** December 6, 2026. **National finale:** January 2027, Bengaluru.
