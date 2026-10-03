# 07 Research Conflict Resolution: AgroStruxure™ Technical Veracity
**Document ID:** CONF-RES-2026-V1  
**Status:** Canonical Decision Register  
**Authoritative Basis:** Thermodynamics, ICAR agronomy, IEEE switchgear standards, `impact_model.py`  

---

## 1. Conflict Resolution Matrix

| Conflict | Value A (Legacy / Flawed) | Value B (Rigorous / Correct) | Resolution | Physical / Empirical Reason |
|---|---|---|:---:|---|
| **1. Cold Storage Temperature Setpoint** | 4°C | 12°C | **12°C (Adopted)** | Storing fresh tomatoes below 10°C causes irreversible *chilling injury* (cellular breakdown, surface pitting, failure to ripen, ICAR/FAO post-harvest guidelines). 12°C halts field heat and respiration while preserving fruit texture for 4–7 days. |
| **2. Controller BOM Cost** | ₹3,480 | ₹7,540 | **₹7,540 (Adopted)** | ₹3,480 omitted industrial-grade components (dual mechanically/electrically interlocked contactors, Type-2 DC SPD, IP67 polycarbonate enclosure, DIN-rail 24V SMPS, Phoenix contact terminals). ₹7,540 reflects genuine 1,000-unit industrial volume production costs. |
| **3. Financial Payback Period** | 18 days | 2.0 years (pre-cooler cluster) / 1.5 crop cycles (controller) | **2.0 Years (Adopted)** | 18 days was an unrealistic claim assuming 100% produce price capture on an entire harvest. Real-world cluster-shared pre-cooler (₹50,212 net capex per farm after 35% MIDH subsidy) generates ₹25,332/farm/yr in net income, yielding a robust 2.0-year payback (2 crop seasons). Standalone controller (₹7,540) pays back in 1.5 crop seasons. |
| **4. Contactor Switching Location** | Downstream on AC VFD output | Upstream on DC Bus (350–600V DC) | **Upstream DC Bus (Adopted)** | Switching contactors on the AC output of a running VFD causes severe $V/f$ inductive spikes, destructive contact arcing, and instant drive IGBT overcurrent trips. AgroStruxure switches upstream on the DC bus with an 8s VFD controlled ramp-down to 0 Hz and a mandatory 5-second dead-band dwell. |
| **5. Surplus Solar Energy Capture** | 100% captured (4,137 kWh/yr) | 77.04% captured (3,187 kWh/yr; 951 kWh uncaptured) | **77.04% (Adopted)** | Claiming 100% solar capture violates thermodynamic capacity limits. Micro-cold room compressor and PCM latent heat bank saturate once daily pull-down is completed. Exactly 3,187 kWh/yr is utilized for cooling; 951 kWh/yr remains residual during peak summer solstice. |
| **6. Water Conservation Metrics** | 60% reduction / vague numbers | 41.2% reduction (7,000 m³/ha/yr saved) | **41.2% / 7,000 m³ (Adopted)** | Baseline flood irrigation: 17,000 m³/ha/yr (850 mm across 2 cycles). AgroStruxure precision pulsed drip: 10,000 m³/ha/yr (500 mm). Net water saved = 7,000 m³/ha/yr (41.18% conservation, mathematically verified in `impact_model.py`). |
| **7. Produce Loss Mitigation Metrics** | 25% reduction | 8.37% $\to$ 4.00% farm-gate spoilage (1.31 t/ha/yr saved) | **8.37% $\to$ 4.00% (Adopted)** | Total supply chain loss is 15–20%, but farm-gate loss specifically attributable to lack of pre-cooling is 8.37%. Reducing this to 4.00% preserves 1.31 tonnes/ha/yr of marketable tomatoes on a 30 t/ha baseline (+₹15,732 revenue at ₹12/kg). |
| **8. Solar Pump Rebound Effect** | Ignored in standard solar pumping | Explicitly solved via automated cutoff & diversion | **Closed-loop cutoff (Adopted)** | Free solar electricity incentivizes farmers to pump 100% of solar daylight hours. AgroStruxure decouples solar generation from water pumping via dual-depth soil saturation cutoff. |
