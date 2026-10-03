# 05 Requirements Traceability Matrix

**Document Code:** RTM-PS1-05  
**Scope:** Bi-Directional Traceability: Official Hackathon Brief ↔ Indian Ground Realities ↔ Technical Solution Architecture  

---

## 1. Bi-Directional Traceability Matrix

| Official PS1 Mandate | Indian Ground Reality Bottleneck | Architectural Component | Verification / KPI Metric |
|---|---|---|---|
| **Objective 1: Reduce Energy & Water Intensity** | Flood irrigation wastes 65% water; pumps burn unmetered subsidized power for 6–8 hrs. | • Low-cost FDR Capacitive Soil Moisture Node.<br>• FAO-56 Penman-Monteith ET0 Calculation Engine.<br>• Closed-Loop Solenoid Pulse Irrigation Controller. | • **≥40% reduction** in water volume pumped ($\text{m}^3/\text{ha}$).<br>• **≥35% reduction** in pump electrical consumption ($\text{kWh/ha}$). |
| **Objective 2: Minimize Post-Harvest Losses** | Perishable crops rot at farm-gate (15–20% loss) due to lack of cold storage and forced distress sales. | • Dynamic Solar Power Router (Schneider TeSys switchgear).<br>• Farm-Gate Micro-Cold Room Interfacing.<br>• Thermal Buffer Management Algorithm. | • **≤5% post-harvest spoilage** (down from 18% baseline).<br>• Divert **≥65%** of idle daytime solar energy to cooling. |
| **Objective 3: Empower the Smallholder** | 86% smallholders (<2 ha); high illiteracy; fragmented plots; low willingness to pay for expensive IoT. | • Low-cost edge Bill of Materials (₹7,540 industrial BoM at 1,000 units).<br>• Multilingual Vernacular Voice/SMS interface (Hindi/Marathi/English).<br>• 1-Click Physical Manual Override Switch. | • Controller payback 1.5 years (3 crop seasons); cooler-share payback 2.0 years.<br>• >85% farmer usability score in vernacular dialect testing. |
| **Objective 4: Strengthen Climate Resilience** | Groundwater depletion (water table sinking 1m/yr); erratic monsoon dry spells and extreme heatwaves. | • Aquifer Extraction Budgeting Algorithm.<br>• Satellite vegetative stress monitoring (Sentinel-2 NDVI).<br>• Predictive Drought & Heat Stress Pre-Watering Alerts. | • Cumulative aquifer extraction maintained **below replenishment budget**.<br>• Zero crop failure during 14-day dry spells. |
| **Schneider Integration: OT/IT Convergence** | Existing solar pumps under PM-KUSUM lack automated agronomic closed-loop intelligence. | • Direct Modbus/RS485 interface to **Altivar Solar ATV320 VFD**.<br>• **EcoStruxure** 3-Tier Architecture alignment.<br>• Motor protection via **TeSys** contactor logic. | • 100% compliance with PM-KUSUM RMS telemetry protocol.<br>• Sub-second motor shutdown on dry-run or phase loss. |
