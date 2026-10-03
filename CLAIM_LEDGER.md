# MASTER CLAIM LEDGER
**Project:** AgroStruxure™ — Solar-Synchronized Agri-Energy Microgrid & Closed-Loop Precision Irrigation  
**Hackathon:** Yuva Yodha Energy Tech Hackathon 2026 (Schneider Electric India)  
**Standard:** Absolute factual verification; every statistic tracked to official, institutional, or derived sources.  
**Date:** October 3, 2026  

---

## 1. Claim Ledger Table

| Claim | Value | Unit | Year | Geography | Source | URL | Source Tier | Slide | Status |
|---|---:|---|---|---|---|---|:---:|:---:|:---:|
| National annual groundwater extraction | 245 | BCM | 2023 | India | Central Ground Water Board (CGWB) | `https://cgwb.gov.in/` | Tier 2 | 02 | **VERIFIED** |
| Agricultural share of national groundwater extraction | 87 | % | 2023 | India | Central Ground Water Board (CGWB) | `https://cgwb.gov.in/` | Tier 2 | 02 | **VERIFIED** |
| Assessment units classified as Over-Exploited | 1,114 | Units | 2023 | India | Central Ground Water Board (CGWB) | `https://cgwb.gov.in/` | Tier 2 | 02 | **VERIFIED** |
| National agricultural electricity consumption | 255,000 | GWh | 2024 | India | Central Electricity Authority (CEA) / MoSPI | `https://mospi.gov.in/` | Tier 2 | 02 | **VERIFIED** |
| Agricultural share of national electricity use | 16.53 | % | 2024 | India | CEA Energy Statistics India 2024 | `https://mospi.gov.in/` | Tier 2 | 02 | **VERIFIED** |
| Standalone solar pumps deployed under PM-KUSUM Component B | 10.9 | Lakh pumps | 2024 | India | Ministry of New and Renewable Energy (MNRE) | `https://mnre.gov.in/` | Tier 2 | 02, 09 | **VERIFIED** |
| Empirical groundwater extraction increase after solar pump adoption | 16–39 | % | 2019 | Rajasthan, India | Gupta, E. (*Energy Policy*, Vol 129) | `https://doi.org/10.1016/j.enpol.2019.02.008` | Tier 3 | 03 | **VERIFIED** |
| Off-grid solar agricultural pump surplus energy wasted | ~66 | % | 2016 | India | Shah et al. (IWMI-Tata SPaRC) | `https://www.iwmi.cgiar.org/` | Tier 3 | 03 | **VERIFIED** |
| National cumulative post-harvest economic loss | 1,52,790 | ₹ Crore | 2022 | India | NABARD Consultancy Services (NABCONS) / MoFPI | `https://www.mofpi.gov.in/` | Tier 2 | 02, 03 | **VERIFIED** |
| Farm-gate harvest-stage spoilage rate for tomatoes | 8.37 | % | 2022 | India | NABCONS Post-Harvest Study 2022 | `https://www.mofpi.gov.in/` | Tier 2 | 03, 08 | **VERIFIED** |
| Small and marginal farmers share of operational holdings | 86.2 | % | 2021 | India | Agriculture Census of India (MoA&FW) | `https://agricoop.nic.in/` | Tier 2 | 02, 09 | **VERIFIED** |
| Chilling injury threshold temperature for tomatoes | < 10 | °C | 2016 | Global | USDA Agriculture Handbook 66 | `https://www.ars.usda.gov/` | Tier 3 | 04, 06 | **VERIFIED** |
| Safe farm-gate pre-cooling setpoint for tomatoes | 12 | °C | 2026 | Nashik, India | AgroStruxure Thermal Engineering Spec | `impact_model.py` §2b | Tier 1 | 04, 06 | **DERIVED** |
| Baseline tomato flood irrigation water volume (2 cycles) | 17,000 | m³/ha/yr | 2026 | Maharashtra | Baseline Agronomic Norms (850 mm/cycle) | `impact_model.py` §1 | Tier 2 | 08 | **VERIFIED** |
| Entitlement-scheduled drip irrigation water volume | 10,000 | m³/ha/yr | 2026 | Maharashtra | FAO-56 Penman-Monteith (500 mm/cycle) | `impact_model.py` §1 | Tier 1 | 08 | **DERIVED** |
| Annual groundwater conserved per hectare | 7,000 | m³/ha/yr | 2026 | Maharashtra | AgroStruxure Water Model (17,000 - 10,000) | `impact_model.py` §1 | Tier 1 | 04, 08 | **DERIVED** |
| Relative groundwater conservation percentage | 41.2 | % | 2026 | Maharashtra | Water conservation ratio (7,000 / 17,000) | `impact_model.py` §1 | Tier 1 | 01, 04, 08 | **DERIVED** |
| Water savings from conversion to conventional drip alone | 2,500 | m³/season | 2026 | Maharashtra | Baseline drip vs flood (850mm to 600mm) | `impact_model.py` §1 | Tier 1 | 08 | **DERIVED** |
| Water savings strictly from AgroStruxure entitlement lock | 1,000 | m³/season | 2026 | Maharashtra | Entitlement quota lock (600mm to 500mm) | `impact_model.py` §1 | Tier 1 | 08 | **DERIVED** |
| Specific pumping energy consumption at 40m head | 0.242 | kWh/m³ | 2026 | Deccan Basalt | Wire-to-water hydraulic equation (45% eff.) | `impact_model.py` §2a | Tier 1 | 06, 08 | **DERIVED** |
| Annual solar PV generation from 4.8 kWp Component B array | 6,559 | kWh/yr | 2026 | Nashik, India | NIWE Solar Insolation & PR 0.78 | `impact_model.py` §2a | Tier 1 | 08 | **DERIVED** |
| Baseline pumping energy consumption | 4,118 | kWh/ha/yr | 2026 | Maharashtra | Flood volume × specific pumping energy | `impact_model.py` §2a | Tier 1 | 08 | **DERIVED** |
| Entitlement-scheduled pumping energy consumption | 2,422 | kWh/ha/yr | 2026 | Maharashtra | Scheduled volume × specific pumping energy | `impact_model.py` §2a | Tier 1 | 08 | **DERIVED** |
| Pumping electricity freed per hectare annually | 1,696 | kWh/ha/yr | 2026 | Maharashtra | Baseline minus scheduled pumping | `impact_model.py` §2a | Tier 1 | 01, 08 | **DERIVED** |
| Surplus daytime solar generation idle under baseline | 4,137 | kWh/yr | 2026 | Maharashtra | PV generation minus pump demand | `impact_model.py` §2a | Tier 1 | 03, 08 | **DERIVED** |
| Surplus daytime solar generation share of total generation | 63.1 | % | 2026 | Maharashtra | 4,137 / 6,559 kWh | `impact_model.py` §2a | Tier 1 | 03, 08 | **DERIVED** |
| Pre-cooling thermal pull-down demand (2 MT batch, 32°C to 12°C) | 13.7 | kWh_el/day | 2026 | Nashik, India | Sensible heat formula (Cp=3.7, COP=3.0) | `impact_model.py` §2b | Tier 1 | 06, 08 | **DERIVED** |
| Average power required for 2 MT pre-cooling across 4h window | 3.43 | kW | 2026 | Nashik, India | 13.7 kWh / 4 hours (fits 4.8 kWp array) | `impact_model.py` §2b | Tier 1 | 06, 08 | **DERIVED** |
| Surplus solar energy captured by 2 MT pre-cooler (180 days) | 3,187 | kWh/yr | 2026 | Nashik, India | (13.7 kWh pull-down + 4 kWh hold) × 180 d | `impact_model.py` §2b | Tier 1 | 04, 08 | **DERIVED** |
| Surplus solar energy utilization share | 77.0 | % | 2026 | Nashik, India | 3,187 / 4,137 kWh | `impact_model.py` §2b | Tier 1 | 04, 08 | **DERIVED** |
| Residual uncaptured solar energy (non-cooling periods) | 951 | kWh/yr | 2026 | Nashik, India | 4,137 - 3,187 kWh (honestly reported) | `impact_model.py` §2b | Tier 1 | 08 | **DERIVED** |
| Perishable tomato produce preserved per hectare annually | 1.31 | Tonnes/yr | 2026 | Maharashtra | 30 t yield × (8.37% - 4.00% residual loss) | `impact_model.py` §3 | Tier 1 | 01, 04, 08 | **DERIVED** |
| Direct revenue from preserved produce (@ ₹12/kg farm-gate) | 15,732 | ₹/ha/yr | 2026 | Maharashtra | 1.31 tonnes × ₹12,000/tonne | `impact_model.py` §3 | Tier 1 | 08, 09 | **DERIVED** |
| Distress-sale price timing gain from 2–4 day buffer holding | 12,000 | ₹/farm/yr | 2026 | Maharashtra | Market timing model (conservative mean) | `impact_model.py` §5 | Tier 1 | 08, 09 | **PROJECTED** |
| Annual operational expenses per farm (SIM + maintenance) | 2,400 | ₹/farm/yr | 2026 | Maharashtra | 4G cellular SIM + sensor recalibration | `impact_model.py` §5 | Tier 1 | 08, 09 | **PROJECTED** |
| Annual net smallholder economic gain | 25,332 | ₹/farm/yr | 2026 | Maharashtra | ₹15,732 + ₹12,000 - ₹2,400 | `impact_model.py` §5 | Tier 1 | 01, 08, 09 | **DERIVED** |
| Avoided diesel genset emissions for cooling (0.80 kg CO₂e/kWh) | 2.55 | t CO₂e/yr | 2026 | Maharashtra | 3,187 kWh × 0.80 kg CO₂e/kWh | `impact_model.py` §4 | Tier 1 | 08 | **DERIVED** |
| Embodied carbon saved from avoided tomato spoilage (0.30 kg CO₂e/kg) | 0.39 | t CO₂e/yr | 2026 | Maharashtra | 1.31 tonnes × 300 kg CO₂e/tonne | `impact_model.py` §4 | Tier 1 | 08 | **DERIVED** |
| Total annual greenhouse gas abatement per hectare | 2.94 | t CO₂e/yr | 2026 | Maharashtra | 2.55 + 0.39 tonnes CO₂e | `impact_model.py` §4 | Tier 1 | 01, 08 | **DERIVED** |
| Edge controller Bill of Materials (BOM) at 1,000-unit scale | 7,540 | ₹ | 2026 | India | Industrial itemized BOM breakdown | `impact_model.py` §7 | Tier 1 | 04, 07, 09 | **DERIVED** |
| Shared-array solar PV capex avoided per pre-cooler (2.6 kWp) | 91,000 | ₹ | 2026 | India | 2.6 kWp avoided @ ₹35,000/kWp installed | `impact_model.py` §5 | Tier 1 | 07, 09 | **DERIVED** |
| Net capex per farm for Tier A 2 MT pre-cooler (4-farm cluster) | 50,212 | ₹ | 2026 | India | (₹4,00,000 - ₹91,000) × (1-0.35 subsidy) / 4 | `impact_model.py` §5 | Tier 1 | 09 | **DERIVED** |
| Capital payback period for Tier A cluster pre-cooler | 2.0 | Years | 2026 | Maharashtra | ₹50,212 / ₹25,332 net gain (2 crop seasons) | `impact_model.py` §5 | Tier 1 | 01, 09 | **DERIVED** |
| Capital payback period for Tier B FPO 5 MT holding hub | 4.2 | Years | 2026 | Maharashtra | ₹7,80,000 post-subsidy / ₹1,84,375 net rev | `impact_model.py` §6 | Tier 1 | 09 | **DERIVED** |
| Standalone controller payback via pump burnout / yield safety | 1.5 | Crop seasons | 2026 | Maharashtra | ₹7,540 / ~₹5,000 annual pump/yield value | `impact_model.py` §7 | Tier 1 | 09 | **PROJECTED** |

---

## 2. Explicitly Rejected or Corrected Claims (Blacklist)

| Rejected Claim | Stated Value in Early Drafts | Correct Ground Truth | Reason for Rejection |
|---|---|---|---|
| National post-harvest food loss | ₹92,000 Crore | **₹1,52,790 Crore (₹1.53 Lakh Crore)** | ₹92k Cr was from outdated ICAR-CIPHET (2015). NABCONS (2022) is current official figure. |
| Farm-gate tomato spoilage | 15% – 20% | **8.37% farm-gate / harvesting loss** | 15-20% is total supply chain loss; 8.37% is the exact portion on-farm pre-cooling eliminates. |
| Farm-gate tomato cold storage setpoint | 4°C | **12°C tomato-safe setpoint** | 4°C causes severe chilling injury per USDA Agriculture Handbook 66. |
| Edge controller BOM | ₹3,480 | **₹7,540 at 1,000-unit scale** | ₹3,480 omitted industrial TeSys contactors, IP67 enclosure, and pyranometer. |
| Capital payback period | 18 days | **2.0 years (2 crop seasons)** | 18 days erroneously divided gross cold-room benefits by a bare controller BOM. |
| Total solar surplus capture | 100% | **77.0% captured, 23% (951 kWh) residual** | Claims of 100% solar utilization ignore seasonal non-harvest periods and diurnal mismatch. |
| AC contactor load switching | Downstream of VFD | **Upstream DC changeover with 5s dead-band** | Switching AC output of running VFD trips Altivar drive and induces motor insulation damage. |
