# 06 Product Truth: AgroStruxure™ Technical Baseline
**Document ID:** PROD-TRUTH-2026-V3  
**Project:** AgroStruxure™ — Solar-Synchronized Agri-Energy Microgrid & Closed-Loop Precision Irrigation  
**Hackathon:** Yuva Yodha Energy Tech Hackathon 2026 (Schneider Electric India)  
**Track:** Challenge 01 — Sustainable Agriculture: Energy, Water & Productivity  
**Title:** AgroStruxure: An Agricultural Energy Orchestration Platform for Schneider Solar Infrastructure  
**Core invention:** Dynamically reallocating surplus solar generation from irrigation to farm-gate thermal storage.  
**Framing:** Strategic OEM skid and software proposal to Schneider Electric India, extending EcoStruxure (see §3)  
**Status:** Canonical Truth Baseline  

---

## 1. Twenty Dimensions of Product Truth

1. **Exact Problem:**
   The "Solar Rebound Paradox" under PM-KUSUM Component B. When rural smallholders receive zero-marginal-cost solar pumping electricity, they pump continuously without economic constraint. This accelerates groundwater depletion, waterlogs root zones, and leaves solar capacity idle (37% of PV output today under flood irrigation; 63% once irrigation is right-sized). Simultaneously, 8.37% of perishable horticulture produce rots at the farm gate due to the lack of pre-cooling.
2. **Target User:**
   Indian smallholder horticulture farmers (0.5 to 2.0 ha operational landholding) organized into Farmer Producer Organizations (FPOs) and Primary Agricultural Credit Societies (PACS).
3. **Target Geography:**
   Water-stressed, semi-arid agricultural regions in India with high PM-KUSUM standalone pump density—initially Maharashtra (Nashik, Chhatrapati Sambhajinagar, Ahmednagar) and Rajasthan (Jaipur, Sikar), expanding to Karnataka, Telangana, and MP.
4. **Target Crops:**
   High-value, perishable horticulture crops with chilling sensitivity, **Tomato** is the modelled benchmark. Chili, capsicum, onion and leafy greens are candidate cluster crops that need their own setpoints (not modelled). Non-perishable crops (wheat, cotton) need only the standalone kit, not the cooler add-on.
5. **Energy Component:**
   4.8 kWp PM-KUSUM Component B standalone solar PV array (350–600V DC). Three-step energy balance: 6,559 kWh/yr PV → 2,422 kWh pumping → 1,062 kWh pre-cooling → 3,075 kWh (46.9%) unallocated headroom. Flood pumping would use 4,118 kWh/yr, so 2,442 kWh/yr (37%) is already idle today; once irrigation is right-sized, idle PV rises to 4,137 kWh/yr (63.1%). A 4-farm cluster's 2 MT pre-cooler draws 1,062 kWh/yr: 43% of today's idle solar and 26% of the right-sized surplus (≈4× margin), so it does not depend on irrigation savings.
6. **Water Component:**
   FAO-56 Penman-Monteith water budgeting coupled with 1-inch pulse flow meter and dual-depth capacitive FDR soil moisture probes. **Reduced Irrigation Demand:** a 41.2% reduction in modelled irrigation water application, from 850 mm (flood) to 500 mm (pulsed drip) per season, i.e. 7,000 m³/ha/yr. Of this, 5,000 m³ comes from drip hardware (assumed installed) and 2,000 m³ from the entitlement cap that the kit enforces. This is a modelled reduction in irrigation water application, not measured aquifer recovery.
7. **Productivity Component:**
   Rapid farm-gate pre-cooling to 12°C halts respiration heat and extends shelf life by 4–7 days, reducing farm-stage spoilage from 8.37% to 4.00%, preserving 1.31 tonnes/ha/yr of marketable produce.
8. **Hardware:**
   Industrial-grade retrofit kit: ESP32-S3 microcontroller, dual Schneider TeSys D mechanically and electrically interlocked contactors (2x LC1D09BD), Type-2 DC SPD, 24V SMPS, IP67 polycarbonate enclosure with DIN rail mounting. Cluster add-on: shared 2 MT PCM pre-cooler (compressor + encapsulated salt hydrate PCM plates; target 12–15 °C melt point, 190–210 kJ/kg latent heat; design target, confirm the vendor datasheet). Confirm the LC1D09BD's DC rating at 350–600 V against the Schneider datasheet.
9. **Sensors:**
   Dual-depth capacitive Frequency Domain Reflectometry (FDR) soil moisture probes (10cm surface & 30cm root zone), 1-inch Hall-effect pulse flow meter (K-factor calibrated), Sensirion SHT31-D ambient temperature/RH sensor, calibrated silicon pyranometer / PV reference cell.
10. **Software:**
    Edge firmware in FreeRTOS/C++ executing Modbus RTU master communication (CiA402 drive profile per Schneider documentation NVE41308), local FAO-56 balance, 3-layer entitlement engine, and circular flash buffer.
11. **AI/ML:**
    On-device TinyML Random Forest regression for root-zone depletion prediction; cloud-based Deterministic Agentic RAG architecture (Krishi Mitra copilot) that grounds vernacular LLM responses strictly in structured JSON data (zero hallucination, zero actuation authority).
12. **Data Sources:**
    Local ground telemetry (FDR, SHT31, pyranometer, flow meter), Open-Meteo API (48-hr weather forecast), Sentinel-2 10m NDVI/NDWI satellite canopy moisture, CGWB district groundwater extraction indices.
13. **Backend/Cloud:**
    Python FastAPI microservices, TimescaleDB for time-series telemetry, Redis caching, MQTT broker (EMQX) over TLS with automatic 2G/4G fallback.
14. **Decision Engine:**
    Deterministic 3-layer volumetric water entitlement engine: Layer 1 (Agronomic ETc), Layer 2 (Soil moisture deficit & field capacity cutoff), Layer 3 (Community aquifer quota). Controlled zero-current transition for upstream DC changeover (the 5-second dead-band is a parameter to tune on the HIL bench).
15. **User Interface:**
    AgroStruxure Cockpit web console adhering to `@quartzds` standards; smallholder vernacular audio interface delivering WhatsApp spoken updates in Marathi, Hindi, and English.
16. **Workflow:**
    Sense (08:30 AM solar rise) $\to$ Pump (VFD ramps to 38–50 Hz for pulsed drip) $\to$ Cutoff (11:30 AM root zone reaches Field Capacity 45% or daily quota met) $\to$ Ramp Down VFD (8s to 0 Hz) $\to$ Close Solenoid at Zero Flow $\to$ Controlled Zero-Current Transition $\to$ Switch Contactor $\to$ Energize 2 MT PCM Pre-Cooler (11:30 AM–03:30 PM) $\to$ Standby / PCM Hold overnight. Irrigation is scheduled according to crop water requirement and soil moisture telemetry, while PV generation continues through midday.
17. **Deployment Model:**
    Cluster add-on (optional, horticulture only): 4 smallholder farms share one 2 MT pre-cooler unit, avoiding ₹91,000 in standalone PV capex. FPO Hub model: 20 farms share a central 5 MT aggregation cold room. Supported by local "Urja Mitras" (trained rural clean-tech youth).
18. **Business/Economic Model:**
    Two-part model, with the return based strictly on physical produce-loss reduction. Standalone kit: ₹7,540 BoM at 1,000 units, 1.5 years (3 crop seasons) payback on assumed pump and yield protection of ≈₹5,000/yr; reduced irrigation demand has no farm-gate cash value under free solar power and is not counted. Cluster pre-cooler add-on: ₹50,212 per farm after 35% MIDH/AIF subsidy. Base case: 1.31 t/ha/yr preserved × ₹12/kg = ₹15,732/yr (≈₹15,720 at the rounded 1.31 t), net ₹13,332/yr after ₹2,400 opex, payback 3.8 years (≈7.5 harvests; 5.8 years unsubsidised). Optional price-timing scenario (+₹12,000/yr): net ₹25,332/yr, payback 2.0 years.
19. **Scalability:**
    Proposed to Schneider Electric India as an OEM skid and software package extending EcoStruxure: Altivar ATV320 + TeSys D changeover + AgroStruxure gateway for new tenders, converting a single-function solar drive into a multi-load microgrid hub. Opportunity: 4,137 kWh/yr modelled surplus (63.1%) in our 4.8 kWp reference system; Component B installed base (816,710 pumps as of Aug 2026, MNRE; team-supplied, confirm on the MNRE dashboard) provides the target deployment opportunity, reached through a drive-agnostic retrofit (digital I/O or RS485 Modbus). Schneider's own share of that fleet is not documented.
20. **Current Implementation Status:**
    Phase 1 completed: code (`impact_model.py`), math model (arithmetic-reconciled; not field-validated) and AgroSim (team-reported; AgroSim source is not in this repository, so link it before submission). Phase 2 prototype: hardware-in-the-loop (HIL) test bench with Altivar ATV320 and TeSys D. No field hardware exists.

---

## 2. Epistemic Classification

```text
WHAT ACTUALLY EXISTS
• Arithmetic-reconciled impact model (impact_model.py) deriving water, energy and thermal balances (internally consistent; not field-validated).
• Rigorous system architecture with upstream DC changeover topology and CiA402 Modbus register mapping.
• Complete industrial Bill of Materials (BOM) priced at ₹7,540 (1,000-unit volume).
• Deterministic Agentic RAG architecture and multilingual prompt guard engines harvested from audited prior art.
• Open-Meteo weather client and Sentinel-2 cadastral NDVI/NDWI pipeline.
• AgroStruxure™ Industrial Design System specification (DESIGN_SYSTEM.md) conforming to Schneider QuartzDS.

WHAT IS PROTOTYPED  (confirm build status: AgroSim, cockpit and Modbus emulator source are not in this repository)
• Software simulation engine (AgroSim) running Python/FastAPI.
• Interactive frontend cockpit interfaces adhering to 1920×1080 stage and QuartzDS design tokens.
• Modbus register state machine emulating Altivar ATV320 command (8501) and speed reference (8502) registers.

WHAT IS SIMULATED
• 24-hour diurnal day solar irradiance curve (0 to 950 W/m²) and monsoon cloud transient event.
• Dual-depth capacitive soil moisture transitions (18% wilting point to 45% field capacity).
• Controlled zero-current changeover through the TeSys D pair (5-second dead-band parameter, simulated; to be tested on the HIL bench).
• PCM thermal storage pull-down thermodynamics (32°C harvest heat to 12°C setpoint).

WHAT IS DEMONSTRATED  (confirm: the demo build is not in this repository)
• 5-minute interactive jury pitch demo arc simulating a complete farming day.
• Automated cutoff of irrigation upon field capacity saturation and zero-flow valve closure.
• Spoken vernacular voice advisory synthesis in Marathi and Hindi via WhatsApp audio simulation.

WHAT IS PROPOSED
• Strategic proposal to Schneider Electric India: OEM skid (Altivar ATV320 + TeSys D changeover + AgroStruxure gateway) and software, extending EcoStruxure. Schneider's rural EPC channel and Sahyadri FPO are proposed partners; no signed agreement exists.
• Integration with Atal Bhujal Yojana digital aquifer monitoring and FPO collective storage leasing.
• Training of rural youth as "Urja Mitras" for installation and maintenance under PACS.

WHAT IS PLANNED
• Phase 2 hardware-in-the-loop pilot bench with physical Altivar ATV320 drive and TeSys contactors.
• Field pilot across 250 farms in Nashik and Chhatrapati Sambhajinagar districts across 5 FPOs.

WHAT IS PROJECTED
• 41.2% reduction in modelled irrigation water application (7,000 m³/ha/yr; Reduced Irrigation Demand).
• 1,696 kWh/ha/yr pumping energy liberated.
• 1,062 kWh/yr of cluster pre-cooling energy (43% of today's idle 2,442 kWh; 26% of the right-sized 4,137 kWh surplus; 266 kWh per farm); 3,075 kWh (46.9%) unallocated headroom.
• 0.39 t CO₂e/ha/yr embodied emissions of avoided spoilage.
• 1.31 tonnes/ha/yr perishable produce preserved.
• ₹13,332/farm/yr base-case net benefit from physical loss reduction (₹25,332 with the optional price-timing scenario).
• 3.8-year base-case payback for the 4-farm cluster add-on (2.0 years with the optional price-timing scenario).

WHAT WE MUST NOT CLAIM
• We MUST NOT claim that physical hardware has been field-tested in Nashik or Rajasthan during Phase 1.
• We MUST NOT claim that the edge controller BOM is ₹3,480 (it is ₹7,540 for industrial grade).
• We MUST NOT claim 18-day payback (base-case payback is 3.8 years for the cluster add-on, 2.0 years only with the optional price-timing scenario, 1.5 years for the standalone controller).
• We MUST NOT claim 4°C cold storage for tomatoes (it causes chilling injury; setpoint is 12°C).
• We MUST NOT claim that contactors switch on the VFD output (they switch upstream on the DC bus).
• We MUST NOT claim the surplus is fully used: cooling a 4-farm cluster uses 1,062 kWh/yr (26% of the host farm's surplus); 3,075 kWh/yr (46.9% of PV) is unallocated headroom.
• We MUST NOT claim a diesel-displacement carbon credit (headline is 0.39 t CO₂e/ha/yr; smallholders have no cooling today).
• We MUST NOT call Sahyadri FPO or the Schneider rural EPC channel confirmed partners (proposed only).
• We MUST NOT present 63% idle PV as today's figure (it is 37% today; 63% after right-sizing water).
• We MUST NOT claim nationwide deployment has already occurred.
• We MUST NOT credit the ₹7,540 kit alone with the full 7,000 m³ saving (kit share 2,000 m³; 5,000 m³ is drip hardware).
• We MUST NOT present PCM design life, PCM holdover or battery cost as measured or quoted (assumptions A15–A17 in the proposal).
• We MUST NOT call AgroSim working or validated until its source is linked and run.
• We MUST NOT count reduced irrigation demand as farm-gate cash value while solar power is free.
• We MUST NOT describe the 41.2% as groundwater saved or aquifer protection; it is a modelled reduction in irrigation water application.
• We MUST NOT put price-timing arbitrage into the base-case return; it is an optional scenario.
• We MUST NOT present the CURRENT PROTOTYPE scope as field hardware: it is simulated in Phase 1 and built on the HIL bench in Phase 2.
• We MUST NOT attach an energy or revenue figure to the EXPANSION ROADMAP loads (crop drying, packhouse sorting, dairy chilling, water treatment).
```

---

## 3. Proposal Alignment with Schneider Electric Ecosystem

### 3.1 The Proposal
AgroStruxure™ is proposed to **Schneider Electric India as an OEM skid and software package** that extends EcoStruxure into off-grid agriculture. It converts Schneider's single-function Altivar solar pump drive into a multi-load microgrid hub: the same PV array runs the pump and, on harvest days, a shared farm-gate pre-cooler.

| EcoStruxure tier | AgroStruxure element | Schneider portfolio touchpoint |
|---|---|---|
| **Connected Products** | FDR probes, flow meter, SHT31 + pyranometer; pump drive; interlocked contactor pair | Altivar ATV320 (Modbus RTU, Reg 8501 / 8502); TeSys D LC1D09BD × 2 |
| **Edge Control** | ESP32-S3: FAO-56 budget, field-capacity cutoff, controlled zero-current changeover; offline-first | EcoStruxure edge pattern; Run/Stop digital I/O fallback for non-Schneider drives |
| **Cloud Apps & Analytics** | FastAPI telemetry, read-only vernacular advisory, FPO fleet dashboard | EcoStruxure Apps pattern; SE Ventures path to scale |

* **New tenders:** Altivar ATV320 + TeSys D changeover + AgroStruxure gateway as a pre-wired skid.
* **Installed base:** 4,137 kWh/yr modelled surplus (63.1%) in our 4.8 kWp reference system; Component B installed base (816,710 pumps as of Aug 2026, MNRE; team-supplied, confirm on the dashboard) provides the target deployment opportunity. The retrofit is drive-agnostic. Schneider's own share of that fleet is not documented.
* **Partners:** Schneider Electric's rural EPC channel and Sahyadri Farmers Producer Co. are **proposed only**; no signed agreement exists.

### 3.2 Solar Surplus Physics: Baseline Idle 2,442 kWh vs Cooling Demand 1,062 kWh
* PV generation (4.8 kWp, Nashik): **6,559 kWh/yr**. Flood pumping uses 4,118 kWh/yr, so **2,442 kWh/yr (37%) is already idle today**, before any irrigation saving.
* The 4-farm cluster PCM pre-cooler draws **1,062 kWh/yr**: **43% of today's idle solar**. It does not depend on irrigation savings to operate.
* Once water is right-sized (2,422 kWh/yr pumping), idle PV grows to **4,137 kWh/yr (63%)**: a **≈4× margin** for cooling (3.9×).
* **Three-step balance:** 6,559 kWh PV → 2,422 kWh pumping → 1,062 kWh pre-cooling → **3,075 kWh (46.9%) unallocated headroom** for future loads or grid feed-in.
* *Limit:* this is an annual energy balance. The cooler needs 3.43 kW for about 4 h at midday on harvest days; the overlap must be confirmed in AgroSim and on the Phase 2 bench.

### 3.3 Why Phase-Change Material (PCM) Instead of a Battery
1. **Capital cost and ROI.** One batch-day needs 17.7 kWh (13.7 pull-down + 4.0 hold). A battery carrying all of it is ≈22 kWh nominal (80% depth of discharge); carrying only the hold is ≈5 kWh. At an indicative ₹10,000–20,000 per kWh (assumption, get quotes) that is ₹2.2–4.4 lakh, or ₹0.5–1.0 lakh for the hold alone, before inverter and replacement. PCM plates are part of the ₹400,000 cooler that four farms share (₹50,212 per farm after subsidy).
2. **Economic value per kWh.** On physical loss reduction alone, cooling turns surplus into ≈₹59/kWh gross ((₹15,732 × 4) ÷ 1,062), ₹50 net of opex. With the optional price-timing scenario it is ≈₹104/kWh gross, ₹95 net. A battery for general use or export earns about ₹3–5/kWh (indicative).
3. **Rural thermal durability.** No electrochemical cycling. Specification: encapsulated salt hydrate PCM, target 12–15 °C melt point (low end, ≈12 °C, so the store holds the room near the 12 °C setpoint) and 190–210 kJ/kg latent heat; ≈216 kg (206–227 kg) carries the 4.0 kWh overnight hold (12 kWh thermal). Designed for a 10-year life in 45 °C ambient (design target: confirm the vendor's rated freeze–thaw cycles and holdover). Lithium and lead-acid batteries age faster under sustained heat and daily deep cycling.

### 3.4 Modularity: Standalone Kit vs Cluster Add-On
| | **Standalone retrofit kit** | **Cluster pre-cooler add-on** |
|---|---|---|
| Cost | ₹7,540 BoM (1,000 units) | ₹50,212 per farm after 35% MIDH/AIF |
| Works on | Any PM-KUSUM pump | Horticulture clusters (tomato modelled; chili, leafy greens need own setpoints). Not wheat or cotton |
| Benefit | Entitlement cap: 2,000 m³/ha/yr of the 7,000 m³ reduction in modelled irrigation water application (5,000 m³ is drip hardware, assumed installed); pump and yield protection ≈₹5,000/yr (assumption) | Base case: 1.31 t preserved = ₹15,732/yr, net ₹13,332 per farm. Optional price-timing scenario: +₹12,000, net ₹25,332 |
| Payback | 1.5 years (3 crop seasons) | Base case 3.8 years (≈7.5 harvests; 5.8 unsubsidised). With the optional timing scenario 2.0 years (3.0 unsubsidised) |

### 3.5 Re-Verification of the Twenty Dimensions (2026-10-03)
| # | Dimension | Status | Note |
|:-:|---|:-:|---|
| 1 | Exact Problem | Corrected | 63% idle is *after* right-sizing; 37% (2,442 kWh) is idle today |
| 2 | Target User | Aligned | |
| 3 | Target Geography | Aligned | |
| 4 | Target Crops | Corrected | Tomato modelled; other crops are candidates; wheat/cotton need only the kit |
| 5 | Energy Component | Corrected | Three-step balance 6,559 → 2,422 → 1,062 → 3,075 kWh (46.9% unallocated); cooler = 43% of today's idle, 26% of right-sized surplus |
| 6 | Water Component | Corrected | Reduced Irrigation Demand: 41.2% reduction in modelled irrigation water application = 5,000 m³ hardware + 2,000 m³ entitlement cap |
| 7 | Productivity Component | Aligned | 4.00% post-cooling loss is a design target |
| 8 | Hardware | Aligned | Confirm LC1D09BD DC rating at 350–600 V against the datasheet |
| 9 | Sensors | Aligned | |
| 10 | Software | Aligned | Register map per Schneider NVE41308 as cited; confirm against the installed firmware's manual |
| 11 | AI/ML | Aligned | Read-only, zero actuation authority |
| 12 | Data Sources | Aligned | |
| 13 | Backend/Cloud | Aligned | FastAPI |
| 14 | Decision Engine | Corrected | "Controlled zero-current transition"; the 5 s dead-band is a HIL tuning parameter |
| 15 | User Interface | Aligned | |
| 16 | Workflow | Corrected | Same transition wording; irrigation scheduled to crop water requirement and soil moisture telemetry while PV continues through midday |
| 17 | Deployment Model | Corrected | Cluster cooler is an optional add-on; kit stands alone |
| 18 | Business/Economic Model | Corrected | Base case on physical loss reduction: ₹13,332/yr, 3.8 years. Price timing is an optional scenario (2.0 years) |
| 19 | Scalability | Corrected | OEM skid and software proposal to Schneider; target opportunity is the Component B installed base (816,710 pumps, Aug 2026, MNRE; confirm) |
| 20 | Current Implementation Status | Corrected | Phase 1 completed (code, math model, AgroSim: link its source) vs Phase 2 prototype (HIL test bench) |

### 3.6 Dual-Plane Architecture and Load Portfolio
* **Control plane:** Sensors (soil, flow, PV, temperature) → ESP32-S3 edge controller → Modbus RTU commands (CiA402 profile) to the Altivar ATV320 VFD.
* **Power plane:** PV array (4.8 kWp) → power conversion / interlocked switch stage → Load A (solar pump) / Load B (PCM chiller).

| Load portfolio | Loads |
|---|---|
| **CURRENT PROTOTYPE** | Solar pumping + soil/water control + PCM cooling |
| **EXPANSION ROADMAP** | Crop drying + packhouse sorting + dairy chilling + water treatment |

The current-prototype scope is simulated in Phase 1 and built on the HIL bench in Phase 2; no field hardware exists. Roadmap loads are not modelled, and no energy, revenue or percentage split is claimed for them.

### 3.7 Engineering Artifacts: Phase 1 Completed vs Phase 2 Prototype
| Phase | Artifact | Status |
|---|---|---|
| **Phase 1 completed** | Code: `research/08_IMPACT/impact_model.py` | In this repository; runs and reconciles |
| **Phase 1 completed** | Math model (water, energy, thermal, economics) | Arithmetic-reconciled; not field-validated |
| **Phase 1 completed** | AgroSim software simulator | Team-reported complete; source not in this repository, link it before submission |
| **Phase 2 prototype** | HIL test bench: ESP32-S3 firmware + Altivar ATV320 + TeSys D (5 s dead-band tuned here) | Planned; no hardware yet |
