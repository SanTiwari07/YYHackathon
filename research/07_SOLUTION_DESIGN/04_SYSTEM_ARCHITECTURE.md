# 04 End-to-End System Architecture

**Document Code:** ARCH-SPEC-04  
**Evaluation Pillar Target:** Solution Architecture & Schneider Integration (30% Judging Weight)  
**Hardware Topology:** Upstream DC Changeover with Mechanical/Electrical Interlock & 5-Second Dead-Band  

---

## 1. System Architecture Diagram

```mermaid
flowchart TD
    subgraph Tier3["Tier 3: Apps, Analytics & Services (EcoStruxure Cloud)"]
        Agro_Twin[Agronomic Digital Twin & Irrigation Scheduler]
        Det_RAG[Deterministic Vernacular Advisory / Copilot]
        FPO_Dash[FPO Entitlement & Credit Trading Ledger]
        DISCOM_Port[PM-KUSUM RMS & Aquifer Monitoring Portal]
    end

    subgraph Tier2["Tier 2: Edge Control (EcoStruxure Edge)"]
        Edge_MCU[AgroStruxure Industrial Gateway\nESP32-S3 Dual-Core 240MHz\nFreeRTOS Preemptive Tasks]
        Modbus_Master[Modbus RTU Master Engine\nCiA402 Drive Profile (NVE41308)]
        Load_Router[Deterministic Load Switcher\n5s Dead-Band Safety Sequencer]
        Offline_DB[Circular Flash Storage\n90-Day Offline Buffer]
        Entitle_Eng[3-Layer Entitlement Engine\nCGWB / Atal Bhujal Quota]
    end

    subgraph Tier1_Switch["Tier 1: Upstream Industrial Switchgear (DC Bus)"]
        PV_Array[PM-KUSUM PV Array\n4.8 kWp · 350V - 600V DC]
        DC_SPD[DC Isolator + Type-2 SPD]
        TeSys_Switch[Schneider TeSys D Changeover Contactors ×2\nMechanically & Electrically Interlocked\nBreak-Before-Make · Upstream of all Drives]
    end

    subgraph Tier1_Drives["Tier 1: Dedicated Motor Controllers"]
        Altivar_VFD[Schneider Altivar Solar ATV320 VFD\nRegisters: 8501 CMD, 8502 LFRd, 3201-3208\nEmbedded MPPT & Pump Protection]
        Cold_Comp[DC Brushless Compressor Inverter\nSoft-Start · Anti-Short Cycle Dwell]
    end

    subgraph Tier1_Loads["Tier 1: Controlled Industrial Loads"]
        Sub_Pump[5 HP Submersible Pump\nBorewell Pulsed Drip Irrigation]
        PCM_Cooler[2 MT Farm-Gate Pre-Cooler\nPCM Thermal Buffer · 12°C Tomato Safe]
    end

    subgraph Tier1_Sensors["Tier 1: Sensing & Metering Array"]
        Soil_Node[Dual-Depth Capacitive FDR Probes\n10cm & 30cm Root Moisture]
        Flow_Meter[1-inch Hall-Effect Pulse Flow Meter\nPhysical Entitlement Ground Truth]
        Local_Meteo[SHT31-D Temp/RH + Pyranometer\nLocal FAO-56 ET0 Inputs]
        Pulse_Valve[1-inch 12V Latching Solenoid Valve\nZero Holding Power]
    end

    Soil_Node -->|ADC / I2C| Edge_MCU
    Flow_Meter -->|Pulse Counter Interrupt| Edge_MCU
    Local_Meteo -->|I2C / Analog| Edge_MCU
    Edge_MCU -->|50ms DC Pulse| Pulse_Valve
    
    PV_Array ==> DC_SPD ==> TeSys_Switch
    TeSys_Switch ==>|Position 1: Morning Irrigation| Altivar_VFD ==> Sub_Pump
    TeSys_Switch ==>|Position 2: Afternoon Pre-Cooling| Cold_Comp ==> PCM_Cooler

    Altivar_VFD <-->|RS485 Modbus RTU| Modbus_Master
    Modbus_Master <--> Edge_MCU
    Edge_MCU -->|GPIO + Opto-Relay Interlock| TeSys_Switch

    Edge_MCU <--> Offline_DB
    Edge_MCU <--> Entitle_Eng
    Edge_MCU <--> Load_Router

    Edge_MCU <-->|MQTT over TLS via 4G / 2G Fallback| Agro_Twin
    Agro_Twin <--> Det_RAG
    Agro_Twin <--> FPO_Dash
    Agro_Twin <--> DISCOM_Port
```

---

## 2. The Three Flow Topologies

### Flow 1: Data Flow & Anti-Water Hammer Sequencing

```mermaid
sequenceDiagram
    autonumber
    participant Soil as FDR Soil Probes
    participant Flow as Hall-Effect Flow Meter
    participant Edge as Edge Gateway (ESP32-S3)
    participant VFD as Altivar Solar ATV320
    participant Valve as Latching Solenoid Valve
    participant TeSys as TeSys DC Changeover
    participant Comp as Pre-Cooler Compressor

    Soil->>Edge: Periodic Soil Moisture @ 10cm, 30cm
    Edge->>VFD: Poll Modbus Regs: 3201 (ETA), 3202 (RFRd), 3204 (LCR), 3207 (DC Bus)
    VFD-->>Edge: Returns Drive Telemetry
    Edge->>Flow: Increment Cumulative Litres Metered
    
    Note over Edge: Evaluate 3-Layer Entitlement: Is V_today >= V_day?
    alt Daily Quota Met OR Soil Saturated
        Edge->>VFD: Write 7 (0x0007) to Reg 8501 (CMD) -> Ramp down to 0 Hz (8s)
        VFD-->>Edge: Reg 3202 (RFRd) confirms 0.0 Hz; Reg 3201 confirms Drive Stopped
        Flow-->>Edge: Confirms Flow Q = 0 LPM
        Edge->>Valve: Send 50ms DC pulse to CLOSE valve under ZERO flow (Prevents Water Hammer)
        Note over Edge,TeSys: Mandatory 5-Second Dead-Band Dwell (DC Bus Bleed Down)
        Edge->>TeSys: De-energize Contactor 1; Energize Contactor 2 (DC Bus to Position 2)
        Edge->>Comp: Enable Compressor Inverter (12°C Tomato Pre-Cooling Active)
    end
```

### Flow 2: Energy Flow Topology (Upstream DC Routing)

```mermaid
flowchart LR
    PV[Solar PV Array\n4.8 kWp · 350V - 600V DC] --> SPD[DC Isolator +\nType-2 SPD]
    SPD --> TeSys{Schneider TeSys D\nDC Changeover Contactors\nMechanically Interlocked}
    
    TeSys -->|Position 1: 08:30 - 11:30 AM| VFD[Schneider Altivar Solar\nATV320 VFD]
    VFD --> Pump[5 HP Submersible Pump\nPulsed Micro-Drip: 7,000 m3/yr Saved]
    
    TeSys -->|Position 2: 11:30 AM - 03:30 PM\n(After 5s Dead-Band)| Inverter[Dedicated DC Inverter\nCompressor Controller]
    Inverter --> Cold[2 MT Farm Pre-Cooler\n12°C Safe Setpoint · 1.31 t/yr Saved\nUtilizes 3.43 kW Midday Surplus]
```

### Flow 3: Financial & Economic Flow Topology (4-Farm Cluster)

```mermaid
flowchart TD
    Asset[2 MT PCM Pre-Cooler\nGross Capex: ₹4,00,000] --> SharedSave[Shared-Array PV Capex Avoided:\n-₹91,000 (2.6 kWp not needed)]
    SharedSave --> NetCapex[Net Cluster Capex: ₹3,09,000]
    Gov[MIDH / AIF Capital Subsidy] -->|35% Subsidy Support: ₹1,08,150| ClusterCost[Net Cluster Outlay: ₹2,00,850]
    
    ClusterCost --> FarmShare[Capex Per Farm (4-Farm Cluster):\n₹50,212 per smallholder]
    
    FarmShare --> Benefits[Annual Smallholder Gains:\n• Spoilage Avoidance: +₹15,732\n• Distress-Sale Timing: +₹12,000\n• Less Opex: -₹2,400\n= Net Gain: ₹25,332 / year]
    
    Benefits --> Payback[Payback Period: 2.0 Years\n(2 Crop Seasons)]
```
