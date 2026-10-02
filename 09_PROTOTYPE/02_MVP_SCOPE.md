# 02 MVP Scope vs. Full Production Roadmap

**Document Code:** PROTO-SCOPE-02  
**Domain:** Minimum Viable Product Definition & Feature Boundary Management  

---

## 1. Feature Prioritization Matrix (MoSCoW Method)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AGROSTRUXURE FEATURE SCOPE                      │
├────────────────────────────────────────────────────────────────────────┤
│ MUST HAVE (In Hackathon MVP Demo)                                      │
│ • Real-time simulation of 24h diurnal solar irradiance curve           │
│ • FAO-56 Penman-Monteith ET0 and root-zone soil moisture balance model │
│ • Automated closed-loop valve actuation based on Field Capacity & RAW  │
│ • Altivar Solar ATV320 Modbus register emulation (Vdc, Irms, Hz)       │
│ • Dynamic power diversion switchgear to micro-cold storage compressor  │
│ • Interactive Web UI with live multi-parameter gauges & ECharts        │
│ • Marathi/Hindi/English vernacular voice advisory generator            │
├────────────────────────────────────────────────────────────────────────┤
│ SHOULD HAVE (In Hackathon Prototype if Time Permits)                  │
│ • Cloud-synchronized plot NDVI/NDWI overlay via Sentinel-2 API         │
│ • Simulated pump anomaly detection (dry-run and phase loss trips)      │
│ • Downloadable 3-page PDF Energy & Water Audit Report                  │
├────────────────────────────────────────────────────────────────────────┤
│ COULD HAVE (Commercial Phase 1 Pilot)                                  │
│ • Physical hardware bench testing with ESP32 and actual Altivar VFD   │
│ • Native mobile Android APK with Bluetooth Low Energy (BLE) direct link│
│ • Multi-tenant FPO fleet manager dashboard                             │
├────────────────────────────────────────────────────────────────────────┤
│ WON'T HAVE (Out of Scope for 2026 Hackathon)                           │
│ • Commercial manufacturing tooling and die-cast IP67 aluminum tooling  │
│ • Full DISCOM SCADA integration protocols (IEC 60870-5-104)           │
│ • Drone multispectral flight control integration                       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Granular MVP Functional Specifications

1. **Interactive Day Simulation Control:**
   - A slider allowing judges to scrub through 24 hours of farm life (from 06:00 AM to 06:00 PM) or click "Play Simulation" at 10x speed.
   - Interactive toggles: "Inject Passing Cloud" (drops solar kW by 60%), "Simulate Soil Drought" (forces moisture below RAW), "Simulate Borewell Dry-Run" (drops motor current).
2. **Visual State Indicator:**
   - Explicit visual confirmation of current operational state:
     - `STATE 1: SOLAR PUMPING ACTIVE` (Water flowing, frequency modulating).
     - `STATE 2: ROOT ZONE SATURATED — CUTTING OFF WATER` (Valve closed, zero over-pumping).
     - `STATE 3: SOLAR SURPLUS DIVERTED TO COLD ROOM` (TeSys contactor flipped, compressor running at 4°C).
3. **Auditory Vernacular Experience:**
   - Single-click audio button that speaks the real-time status in authentic Marathi and Hindi dialects, proving accessibility for non-literate farmers.
