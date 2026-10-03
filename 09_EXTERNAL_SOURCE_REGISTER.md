# 09 External Source Register & Schneider Electric Alignment
**Document ID:** SRC-REG-2026-V1  
**Verification Standard:** Primary Technical, Government & Corporate Literature  
**Status:** Ingested & Traceable  

---

## 1. External Source Register

| Claim / Benchmark | Source Authority | Publication Title | Year | Citation / Identifier | Confidence |
|---|---|---|:---:|---|:---:|
| **10.9 Lakh Standalone Solar Pumps** | Ministry of New and Renewable Energy (MNRE) | PM-KUSUM Scheme Progress Report & Lok Sabha Q&A | 2024 | MNRE Official Portal (Component B Sanctions) | `High (Official)` |
| **8.37% Farm-Gate Tomato Loss** | NABARD Consultancy Services (NABCONS) | Study on Determining Post-Harvest Losses of Major Crops in India | 2022 | Ministry of Food Processing Industries (MoFPI) | `High (Official)` |
| **12°C Tomato Chilling Injury Limit** | Indian Council of Agricultural Research (ICAR) & FAO | Post-Harvest Management of Horticultural Crops (FAO Irrigation & Drainage 56 / ICAR-CIPHET) | 2021 | ICAR Tech Bulletin No. 44 / FAO Chapter 7 | `High (Empirical)` |
| **Dual $K_c$ Evapotranspiration Model** | Food and Agriculture Organization (FAO) | Crop Evapotranspiration - Guidelines for Computing Crop Water Requirements (FAO-56) | 1998 | FAO Irrigation and Drainage Paper No. 56 | `High (Standard)` |
| **Altivar ATV320 Drive Registers** | Schneider Electric SE | Altivar Machine ATV320 Modbus Communication Manual | 2023 | Document Reference NVE41308 (CiA402 Profile) | `High (Manufacturer)` |
| **35% Capital Subsidy for Cold Storage** | Ministry of Agriculture & Farmers Welfare | Mission for Integrated Development of Horticulture (MIDH) & Agriculture Infrastructure Fund (AIF) | 2023 | MIDH Operational Guidelines (Component 3.1) | `High (Statutory)` |
| **Groundwater Over-Exploitation** | Central Ground Water Board (CGWB) | National Compilation on Dynamic Ground Water Resources of India | 2023 | CGWB Dynamic Assessment Report | `High (Official)` |
| **Grid Decarbonization Factor (0.71 t/MWh)** | Central Electricity Authority (CEA) | CO2 Baseline Database for the Indian Power Sector, User Guide v19.0 | 2023 | CEA Baseline Emission Factors Table 3 | `High (Statutory)` |

---

## 2. Schneider Electric EcoStruxure™ Alignment

AgroStruxure™ maps seamlessly into Schneider Electric’s three-tier **EcoStruxure™** industrial IoT architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ECOSTRUXURE™ THREE TIERS                        │
├────────────────────────────────┬───────────────────────────────────────┤
│ Tier 3: Apps, Analytics &      │ Krishi Mitra Smallholder Vernacular   │
│         Services               │ Voice Copilot; FPO Fleet Digital Twin;│
│                                │ EcoStruxure Resource Advisor telemetry│
├────────────────────────────────┼───────────────────────────────────────┤
│ Tier 2: Edge Control           │ ESP32-S3 AgroStruxure Controller;     │
│                                │ Modbus Master (CiA402 State Machine); │
│                                │ Local FAO-56 Balance; 5s DC Dead-Band │
├────────────────────────────────┼───────────────────────────────────────┤
│ Tier 1: Connected Products     │ Altivar Solar ATV320 VFDs;            │
│                                │ TeSys D Interlocked Contactors;       │
│                                │ PowerLogic PM5000 Meters; FDR Probes  │
└────────────────────────────────┴───────────────────────────────────────┘
```

1. **Tier 1 — Connected Products:**
   - **Altivar Machine ATV320 Solar Drive:** 3.7 kW / 5.0 HP solar VFD executing Maximum Power Point Tracking (MPPT) with dual dry-run and high-temperature motor protections.
   - **TeSys D Contactors (2x LC1D09BD):** 24V DC coil contactors with mechanical and electrical interlocking rated for DC-3 switching up to 600V DC.
   - **PowerLogic PM5350 Energy Meter:** Precision Modbus power monitoring tracking DC bus voltage, current, and true harmonic power factors.
2. **Tier 2 — Edge Control:**
   - **AgroStruxure Edge Controller:** ESP32-S3 executing deterministic Modbus RTU communication over isolated RS485 at 19,200 baud, 8-E-1. Enforces the 3-layer water entitlement engine and safety interlocks locally without requiring persistent cloud connectivity.
   - **CiA402 Motion & State Control:** Uses Command Word Register `8501` and Speed Reference Register `8502` to ramp drive output to 0 Hz before contactor actuation.
3. **Tier 3 — Apps, Analytics & Services:**
   - **Krishi Mitra Vernacular Assistant:** Deterministic agentic voice assistant delivering real-time WhatsApp updates in Marathi, Hindi, and English.
   - **EcoStruxure Water & Microgrid Cloud:** Centralized multi-tenant fleet management dashboard for FPOs, tracking pump operating hours, cold storage thermal inventory, and community groundwater quota compliance.
