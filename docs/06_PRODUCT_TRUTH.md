# 06 Product Truth: AgroStruxure™ Technical Baseline
**Document ID:** PROD-TRUTH-2026-V1  
**Project:** AgroStruxure™ — Solar-Synchronized Agri-Energy Microgrid & Closed-Loop Precision Irrigation  
**Hackathon:** Yuva Yodha Energy Tech Hackathon 2026 (Schneider Electric India)  
**Track:** Challenge 01 — Sustainable Agriculture: Energy, Water & Productivity  
**Status:** Canonical Truth Baseline  

---

## 1. Twenty Dimensions of Product Truth

1. **Exact Problem:**
   The "Solar Rebound Paradox" under PM-KUSUM Component B. When rural smallholders receive zero-marginal-cost solar pumping electricity, they pump continuously without economic constraint. This accelerates groundwater depletion, waterlogs root zones, and wastes 63% of generated solar electricity (sitting idle once tanks fill). Simultaneously, 8.37% of perishable horticulture produce rots at the farm gate due to the lack of pre-cooling.
2. **Target User:**
   Indian smallholder horticulture farmers (0.5 to 2.0 ha operational landholding) organized into Farmer Producer Organizations (FPOs) and Primary Agricultural Credit Societies (PACS).
3. **Target Geography:**
   Water-stressed, semi-arid agricultural regions in India with high PM-KUSUM standalone pump density—initially Maharashtra (Nashik, Chhatrapati Sambhajinagar, Ahmednagar) and Rajasthan (Jaipur, Sikar), expanding to Karnataka, Telangana, and MP.
4. **Target Crops:**
   High-value, perishable horticulture crops with chilling sensitivity, primarily **Tomato** (model benchmark), alongside chili, onion, capsicum, and leafy greens.
5. **Energy Component:**
   4.8 kWp PM-KUSUM Component B standalone solar PV array (350–600V DC). Generates 6,559 kWh/yr; scheduled pumping consumes 2,422 kWh/yr; surplus 4,137 kWh/yr (63%) once irrigation is right-sized (today, under flood irrigation, 2,442 kWh/yr = 37% is idle); a 4-farm cluster's 2 MT pre-cooler draws 1,062 kWh/yr (26% of the host farm's surplus; 266 kWh per farm); the remaining 3,075 kWh/yr (47% of PV output) is headroom and is not claimed.
6. **Water Component:**
   FAO-56 Penman-Monteith water budgeting coupled with 1-inch pulse flow meter and dual-depth capacitive FDR soil moisture probes. Reduces seasonal water application from 850 mm (flood) to 500 mm (pulsed drip), saving 7,000 m³/ha/yr (41.2% conservation).
7. **Productivity Component:**
   Rapid farm-gate pre-cooling to 12°C halts respiration heat and extends shelf life by 4–7 days, reducing farm-stage spoilage from 8.37% to 4.00%, preserving 1.31 tonnes/ha/yr of marketable produce.
8. **Hardware:**
   Industrial-grade retrofit kit: ESP32-S3 microcontroller, dual Schneider TeSys D mechanically and electrically interlocked contactors (2x LC1D09BD), Type-2 DC SPD, 24V SMPS, IP67 polycarbonate enclosure with DIN rail mounting.
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
    Deterministic 3-layer volumetric water entitlement engine: Layer 1 (Agronomic ETc), Layer 2 (Soil moisture deficit & field capacity cutoff), Layer 3 (Community aquifer quota). Mandatory 5-second dead-band sequence for upstream DC changeover.
15. **User Interface:**
    AgroStruxure Cockpit web console adhering to `@quartzds` standards; smallholder vernacular audio interface delivering WhatsApp spoken updates in Marathi, Hindi, and English.
16. **Workflow:**
    Sense (08:30 AM solar rise) $\to$ Pump (VFD ramps to 38–50 Hz for pulsed drip) $\to$ Cutoff (11:30 AM root zone reaches Field Capacity 45% or daily quota met) $\to$ Ramp Down VFD (8s to 0 Hz) $\to$ Close Solenoid at Zero Flow $\to$ 5s DC Bus Dead-band Dwell $\to$ Switch Contactor $\to$ Energize 2 MT PCM Pre-Cooler (11:30 AM–03:30 PM) $\to$ Standby / PCM Hold overnight.
17. **Deployment Model:**
    Cluster-shared model: 4 smallholder farms share one 2 MT pre-cooler unit, avoiding ₹91,000 in standalone PV capex. FPO Hub model: 20 farms share a central 5 MT aggregation cold room. Supported by local "Urja Mitras" (trained rural clean-tech youth).
18. **Business/Economic Model:**
    Controller BOM is ₹7,540 at 1,000-unit scale. Tier A cluster pre-cooler costs ₹50,212 per farm after 35% MIDH/AIF subsidy, generating +₹25,332/farm/yr in net benefits (spoilage saved + price timing - opex). Capital payback in 2.0 years (4 harvests at 2 cycles/yr). Standalone controller pays back in 1.5 years (3 crop seasons).
19. **Scalability:**
    Drive-agnostic design compatible with the ≈10.06 lakh PM-KUSUM Component B standalone pumps installed by 31 Jan 2026 (MNRE, as reported; 13.3 lakh sanctioned) via digital I/O or RS485 Modbus; OEM pre-assembly skid with Schneider Altivar Solar drives for new tenders.
20. **Current Implementation Status:**
    Complete mathematical model (`impact_model.py`), complete system architecture and Modbus register maps, functional deterministic RAG and weather clients from validated prior art, and high-fidelity software simulator (`AgroSim`).

---

## 2. Epistemic Classification

```text
WHAT ACTUALLY EXISTS
• Mathematically validated impact model (impact_model.py) deriving exact water, energy, and thermal balances.
• Rigorous system architecture with upstream DC changeover topology and CiA402 Modbus register mapping.
• Complete industrial Bill of Materials (BOM) priced at ₹7,540 (1,000-unit volume).
• Deterministic Agentic RAG architecture and multilingual prompt guard engines harvested from audited prior art.
• Open-Meteo weather client and Sentinel-2 cadastral NDVI/NDWI pipeline.
• AgroStruxure™ Industrial Design System specification (DESIGN_SYSTEM.md) conforming to Schneider QuartzDS.

WHAT IS PROTOTYPED
• Software simulation engine (AgroSim) running Python/FastAPI.
• Interactive frontend cockpit interfaces adhering to 1920×1080 stage and QuartzDS design tokens.
• Modbus register state machine emulating Altivar ATV320 command (8501) and speed reference (8502) registers.

WHAT IS SIMULATED
• 24-hour diurnal day solar irradiance curve (0 to 950 W/m²) and monsoon cloud transient event.
• Dual-depth capacitive soil moisture transitions (18% wilting point to 45% field capacity).
• TeSys D contactor changeover sequence with 5-second dead-band DC bus dwell.
• PCM thermal storage pull-down thermodynamics (32°C harvest heat to 12°C setpoint).

WHAT IS DEMONSTRATED
• 5-minute interactive jury pitch demo arc simulating a complete farming day.
• Automated cutoff of irrigation upon field capacity saturation and zero-flow valve closure.
• Spoken vernacular voice advisory synthesis in Marathi and Hindi via WhatsApp audio simulation.

WHAT IS PROPOSED
• OEM integration skid partnering with Schneider Electric and solar EPCs for PM-KUSUM tenders.
• Integration with Atal Bhujal Yojana digital aquifer monitoring and FPO collective storage leasing.
• Training of rural youth as "Urja Mitras" for installation and maintenance under PACS.

WHAT IS PLANNED
• Phase 2 hardware-in-the-loop pilot bench with physical Altivar ATV320 drive and TeSys contactors.
• Field pilot across 250 farms in Nashik and Chhatrapati Sambhajinagar districts across 5 FPOs.

WHAT IS PROJECTED
• 41.2% groundwater conservation (7,000 m³/ha/yr).
• 1,696 kWh/ha/yr pumping energy liberated.
• 1,062 kWh/yr of cluster pre-cooling energy (26% of the host farm's 4,137 kWh/yr surplus; 266 kWh per farm).
• 0.39 t CO₂e/ha/yr embodied emissions of avoided spoilage.
• 1.31 tonnes/ha/yr perishable produce preserved.
• ₹25,332/farm/yr net economic benefit.
• 2.0-year capital payback for Tier A 4-farm cluster.

WHAT WE MUST NOT CLAIM
• We MUST NOT claim that physical hardware has been field-tested in Nashik or Rajasthan during Phase 1.
• We MUST NOT claim that the edge controller BOM is ₹3,480 (it is ₹7,540 for industrial grade).
• We MUST NOT claim 18-day payback (payback is 2.0 years for Tier A pre-cooler, 1.5 years (3 crop seasons) for controller).
• We MUST NOT claim 4°C cold storage for tomatoes (it causes chilling injury; setpoint is 12°C).
• We MUST NOT claim that contactors switch on the VFD output (they switch upstream on the DC bus).
• We MUST NOT claim the surplus is fully used: cooling a 4-farm cluster uses 1,062 kWh/yr (26% of the host farm's surplus); 3,075 kWh/yr is unclaimed headroom.
• We MUST NOT claim a diesel-displacement carbon credit (headline is 0.39 t CO₂e/ha/yr; smallholders have no cooling today).
• We MUST NOT call Sahyadri FPO or the Schneider rural EPC channel confirmed partners (proposed only).
• We MUST NOT present 63% idle PV as today's figure (it is 37% today; 63% after right-sizing water).
• We MUST NOT claim nationwide deployment has already occurred.
```
