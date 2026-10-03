# AgroStruxure™ Complete User Flows & System State Transitions

> **Superseded figures (2026-10-03).** This document predates the corrected impact model. Numbers such as 42–64% water saving, 2,555 kWh, 4,200 kWh, 2.8 t, +₹72,450, "<18-day payback", ₹3,480 BoM, 3,187 kWh "captured" and 2.94 t CO₂e are retired. Quote figures only from `docs/08_CLAIM_LEDGER.md` (41.2%, 7,000 m³, 1,062 kWh cluster cooling, 1.31 t, ₹25,332/yr, 2.0-year payback, ₹7,540 BoM, 0.39 t CO₂e).

**Document Code:** FLOW-UX-01  
**Project:** AgroStruxure™ (Yuva Yodha 2026 / Schneider Electric India)  
**Author:** Senior UX Architect & System Engineer  
**Status:** Complete State-Machine & Journey Contract  

---

## Table of End-to-End User Flows
1. [Flow 1: Morning Precision Irrigation Sequence](#flow-1-morning-precision-irrigation-sequence)
2. [Flow 2: Midday Field Capacity Cutoff & Cold Storage Diversion](#flow-2-midday-field-capacity-cutoff--cold-storage-diversion)
3. [Flow 3: Smallholder Vernacular Advisory & Voice Copilot Experience](#flow-3-smallholder-vernacular-advisory--voice-copilot-experience)
4. [Flow 4: Edge Fault Detection, Cloud Transient & Safety Recovery](#flow-4-edge-fault-detection-cloud-transient--safety-recovery)
5. [Flow 5: Plot Delineation, Soil Profile & DPDP Consent Onboarding](#flow-5-plot-delineation-soil-profile--dpdp-consent-onboarding)
6. [Flow 6: Industrial Modbus RTU Commissioning & Drive Inspection](#flow-6-industrial-modbus-rtu-commissioning--drive-inspection)
7. [Flow 7: End-of-Season Impact Audit & Verified PDF Certificate Export](#flow-7-end-of-season-impact-audit--verified-pdf-certificate-export)

---

## Flow 1: Morning Precision Irrigation Sequence

### Scenario Summary
Smallholder farmer Ramesh Patil has a 2.2-acre tomato crop in Marathwada. At dawn, solar power rises. Rather than manually walking to the pump shed at night or letting the pump run unchecked, AgroStruxure initiates precision irrigation based on real-time soil and meteorological physics.

```mermaid
flowchart TD
    START(["06:00 AM: Sunrise & Ambient Awakening"]) --> S1["ESP32-S3 Edge Gateway boots telemetry sensors"]
    S1 --> S2{"Solar Irradiance > 250 W/m²?"}
    S2 -- No --> WAIT["Hold in Standby Mode (Display Night Theme)"]
    WAIT --> S2
    S2 -- Yes --> S3["Read LoRa Dual-Depth Soil Probes (10cm & 30cm)"]
    S3 --> S4["Calculate Daily Reference ET0 (FAO-56 Penman-Monteith)"]
    S4 --> S5["Compute Root Depletion Dr vs RAW Threshold"]
    S5 --> S6{"Is Soil Moisture < RAW Threshold? (Thirsty Crop)"}
    S6 -- No --> BYPASS["Soil sufficiently hydrated. Bypass pumping; hold for cold room"]
    S6 -- Yes --> S7["Pulse open 12V Latching Solenoid Drip Valve"]
    S7 --> S8["Send RS485 Modbus Run Command (Register 8501: 0x0002) to Altivar ATV320"]
    S8 --> S9["VFD executes soft-start ramp (0 to 48.2 Hz over 12 seconds)"]
    S9 --> S10["Water delivered directly to plant root zone at 140 L/min"]
    S10 --> UI["Cockpit UI shifts to STAGE 1: GREEN ACTIVE PUMPING"]
```

### UI & System States During Flow 1
- **UI State:** Top banner illuminates in Schneider Electric green (`#3DCD58`); water flow animation active; Altivar dial sweeps to 48.2 Hz; soil moisture gauge shows water level rising.
- **Physical Safety:** Soft-start ramp prevents water hammer in PVC drip lines and protects motor windings from inrush spikes.
- **Farmer Feedback:** Notification on WhatsApp/SMS: *"Namaskar Ramesh. Solar pumping started for your tomato plot."*

---

## Flow 2: Midday Field Capacity Cutoff & Cold Storage Diversion

### Scenario Summary
At 11:30 AM, solar irradiance reaches its peak (850 W/m²). The root zone reaches Field Capacity ($FC = 45\%$). Traditional PM-KUSUM setups continue over-pumping, wasting water and drowning roots. AgroStruxure cuts water extraction and shifts 100% of peak power to on-farm cold storage.

```mermaid
flowchart TD
    PUMPING["Stage 1: Pumping Active (11:15 AM)"] --> CHECK["Edge Controller samples root moisture theta(t) every 10s"]
    CHECK --> THRESH{"theta(t) >= Field Capacity (45.0%)?"}
    THRESH -- No --> PUMPING
    THRESH -- Yes --> S1["TRIGGER CUTOFF: Prevent Solar Rebound Paradox"]
    S1 --> S2["Send Decelerate & Stop to Altivar VFD (Freq -> 0 Hz)"]
    S2 --> S3["Pulse Latching Solenoid Valve CLOSED (0 bar)"]
    S3 --> S4["DEAD-BAND SAFETY: 150ms Interlock Pause (Zero Back-EMF)"]
    S4 --> S5["Actuate Schneider TeSys Contactor (Switch Position A -> B)"]
    S5 --> S6["Altivar VFD re-engages output to Micro-Cold Room PCM Compressor"]
    S6 --> S7["3.8 kW Clean Solar DC cools eutectic solution down to -2°C (Chamber: 4°C)"]
    S7 --> UI["Cockpit UI shifts to STAGE 3: PURPLE COLD ROOM DIVERSION"]
    S8["Farmer receives Marathi Voice Note: 'Pumping Done; Cold Storage Active'"]
```

### Edge Transitions & Physical Interlocks
- **Contactor Interlock:** An electrical and software dead-band of **150ms** is enforced to ensure the pump motor has completely demagnetized before the compressor circuit is closed, eliminating phase arcing.
- **Energy Accounting:** Diverted kilowatt-hours are logged into the cumulative cold-storage energy counter (Register `3208`).

---

## Flow 3: Smallholder Vernacular Advisory & Voice Copilot Experience

### Scenario Summary
Farmer Ramesh opens the mobile app or receives a WhatsApp voice audio note. He wants to know if he needs to pump more water and verify his cold storage temperature.

```mermaid
flowchart TD
    START(["Farmer Opens AgroStruxure Mobile App"]) --> DETECT["App detects vernacular preference (Default: Marathi / मराठी)"]
    DETECT --> SCREEN["Displays Farmer Hub Screen with high-contrast tactile cards"]
    SCREEN --> ACT1{"Farmer Action?"}
    ACT1 -- Tap 'Listen in Marathi' --> AUDIO["Krishi Mitra Synthesizes Coloquial Voice Note"]
    AUDIO --> V1["'Namaskar Ramesh! Tomato plot received full water (2,400 L). Pump is OFF. Cold room is 4°C.'"]
    ACT1 -- Inspect Soil --> SOIL_VIEW["Examines Plant Root Cross-Section Graphic"]
    SOIL_VIEW --> EXP["Sees underground root is full green (45%), even though surface has minor dry cracks"]
    EXP --> TRUST["Trust established: Farmer refrains from unnecessary over-pumping"]
    ACT1 -- Needs Emergency Pumping --> OVERRIDE["Taps 'Manual 30-Min Boost' (Requires 3-second hold)"]
    OVERRIDE --> WARN["Modal explains: 'Roots are already full. Extra water will cause fungal rot. Confirm?'"]
    WARN -- Confirmed --> BOOST["Runs 30-min timer then safely reverts to cold storage"]
```

---

## Flow 4: Edge Fault Detection, Cloud Transient & Safety Recovery

### Scenario Summary
During the monsoon season, a heavy rain cloud obscures the solar PV array. Solar irradiance drops from 850 W/m² to 280 W/m² in 4 seconds. Simultaneously, a borewell suction pipe develops an air pocket, risking motor cavitation.

```mermaid
flowchart TD
    NORMAL["System Operating at 48 Hz"] --> S1["Cloud Event: Irradiance drops from 850 -> 280 W/m²"]
    S1 --> S2["DC Bus Voltage drops toward undervoltage trip threshold (350V)"]
    S2 --> S3["TinyML MPPT Algorithm detects rate of voltage collapse (dV/dt)"]
    S3 --> S4["Rapidly throttles Altivar frequency from 48 Hz -> 32 Hz"]
    S4 --> S5{"Did DC Voltage Stabilize > 360V?"}
    S5 -- Yes --> STABLE["Maintain throttled pumping; UI displays Amber Transient Badge"]
    S5 -- No --> FAULT1["Irradiance < 200 W/m²: Controlled graceful shutdown to Standby"]
    
    NORMAL --> B1["Borewell Water Level drops below suction strainer"]
    B1 --> B2["Motor Current drops abruptly by 65% with zero flow on sensor"]
    B2 --> B3["TinyML Current Autoencoder detects Dry-Run signature within 1.2s"]
    B3 --> B4["EMERGENCY STOP: Altivar ATV320 trips Register 8501 Bit 0"]
    B4 --> B5["UI triggers Flashing Red Alarm Card; Lockout timer set for 60 minutes"]
    B5 --> B6["SMS Alert sent to Farmer & Technician: 'Borewell dry-run. Motor protected.'"]
```

---

## Flow 5: Plot Delineation, Soil Profile & DPDP Consent Onboarding

### Scenario Summary
FPO Director Sunita Shinde registers a new marginal farmer's plot in the district database.

```mermaid
flowchart TD
    START(["FPO Director Initiates Plot Onboarding (/plots)"]) --> S1["Centers interactive Leaflet satellite map on village cadastral survey"]
    S1 --> S2["Draws boundary polygon around 2.2-acre plot (Live Acreage Computed)"]
    S2 --> S3["Selects Crop Type (Tomato - Solanum lycopersicum) & Sowing Date"]
    S3 --> S4["Selects Soil Texture: 'Deep Black Cotton Soil' (Vertisol)"]
    S4 --> S5["System auto-populates Field Capacity (45%) & Wilting Point (18%)"]
    S5 --> S6["Selects PM-KUSUM Hardware: 5HP Submersible + Altivar ATV320 VFD"]
    S6 --> S7["Links to Village Farm-Gate Micro-Cold Room #02"]
    S7 --> S8["Farmer provides statutory consent under Indian DPDP Act 2023"]
    S8 --> S9["Click 'Save Plot Profile & Initialize Edge'"]
    S9 --> SUCCESS(["Backend generates cryptographic Plot UUID & provisions edge gateway"])
```

---

## Flow 6: Industrial Modbus RTU Commissioning & Drive Inspection

### Scenario Summary
Schneider Electric field technician Suresh Kumar or a hackathon jury judge inspects the live communications between the edge gateway and the Altivar ATV320 drive.

```mermaid
flowchart TD
    START(["Technician navigates to /telemetry"]) --> S1["System opens WebSocket link to virtual/physical Modbus gateway"]
    S1 --> S2["Renders live Modbus register grid (Registers 3201-3208)"]
    S2 --> S3["Technician views live Motor Frequency (3201: 482 -> 48.2 Hz)"]
    S3 --> S4["Technician inspects Motor Amps (3202: 74 -> 7.4 A)"]
    S4 --> S5["Technician inspects DC Bus Voltage (3203: 542 V)"]
    S5 --> S6["Inspects FAO-56 math engine live parameters (Rn, VPD, ET0, Kc)"]
    S6 --> S7{"Test Register Write?"}
    S7 -- Yes --> S8["Opens Write Modal -> Inputs target frequency 42.0 Hz to Register 8502"]
    S8 --> S9["Drive confirms acknowledgment; cell flashes green; VFD decelerates"]
    S7 -- No --> S10["Exports timestamped Modbus diagnostic CSV log"]
```

---

## Flow 7: End-of-Season Impact Audit & Verified PDF Certificate Export

### Scenario Summary
At harvest, farmer Ramesh and FPO Director Sunita generate the verified **AgroStruxure™ Farm Energy & Water Audit Certificate** to qualify for PMKSY subsidies and claim carbon credits.

```mermaid
flowchart TD
    START(["User Navigates to /analytics"]) --> S1["System aggregates seasonal telemetry from PostgreSQL & Time-Series DB"]
    S1 --> S2["Computes total groundwater extraction avoided (1,890 m³ = 42% saved)"]
    S2 --> S3["Computes surplus solar PV redirected to cold room (2,555 kWh)"]
    S3 --> S4["Computes post-harvest vegetable spoilage avoided (2.8 metric tonnes)"]
    S4 --> S5["Calculates Net Farmer Income Uplift (+₹72,450 net gain)"]
    S5 --> S6["User clicks 'Generate Official PDF Audit Certificate'"]
    S6 --> S7["Backend ReportLab service compiles 3-page verified cryptographic certificate"]
    S7 --> S8["PDF downloads immediately with QR code link to digital twin telemetry"]
    S8 --> CLOSE(["Farmer submits certificate to bank for interest subvention under AIF"])
```
