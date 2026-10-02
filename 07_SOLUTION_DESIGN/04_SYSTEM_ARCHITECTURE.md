# 04 End-to-End System Architecture & Flow Topologies

**Document Code:** ARCH-SYS-04  
**Framework Alignment:** Schneider Electric EcoStruxure™ 3-Tier Industrial Architecture  

---

## 1. High-Level Architecture Diagram

AgroStruxure organizes all hardware, edge devices, network protocols, and software services into a unified, modular architecture:

```mermaid
graph TB
    subgraph "Tier 3: Apps, Analytics & Services (Cloud / Enterprise)"
        FPO_Dash[FPO Fleet Management & Carbon Ledger]
        DISCOM_Port[DISCOM Feeder Telemetry & RMS Portal]
        Agro_Twin[Agronomic & Hydrological Digital Twin]
        Det_RAG[Deterministic Agentic RAG Engine]
        Farmer_App[Smallholder Vernacular Web & Mobile UI]
    end

    subgraph "Tier 2: Edge Control & Automation (Pump Shed / Field Hub)"
        Edge_MCU[AgroStruxure Industrial Edge Gateway\nESP32-S3 Dual-Core 240MHz]
        TinyML_Engine[Embedded TinyML Inference Engine\nSoil Depletion & Motor Health]
        Modbus_Master[RS485 Modbus RTU Master Driver]
        Load_Router[Dynamic Microgrid Power Routing Logic]
        Offline_DB[(Local SQLite / Flash Circular FIFO)]
    end

    subgraph "Tier 1: Connected Products (Sensors, Drives & Actuators)"
        PV_Array[PM-KUSUM Solar PV Array 3kW-5kW]
        Altivar_VFD[Schneider Altivar Solar ATV320 VFD]
        TeSys_Switch[Schneider TeSys Contactor Changeover]
        Sub_Pump[3-Phase Submersible Pump Motor 3HP/5HP]
        Cold_Comp[Micro-Cold Room Thermal PCM Compressor]
        Soil_Node[FDR Dual-Depth Capacitive Soil Probe\nLoRa 865 MHz IN865]
        Pulse_Valve[9V-12V DC Latching Solenoid Valve]
    end

    Soil_Node -->|LoRa IN865 Wireless| Edge_MCU
    Edge_MCU -->|100ms Pulse Signal| Pulse_Valve
    
    PV_Array -->|DC Power Bus| Altivar_VFD
    Altivar_VFD <-->|RS485 Modbus RTU| Modbus_Master
    Modbus_Master <--> Edge_MCU
    
    Edge_MCU -->|GPIO / Relay Trigger| TeSys_Switch
    Altivar_VFD --> TeSys_Switch
    TeSys_Switch -->|Load 1: Irrigation Mode| Sub_Pump
    TeSys_Switch -->|Load 2: Cold-Chain Mode| Cold_Comp

    Edge_MCU <--> Offline_DB
    Edge_MCU <--> TinyML_Engine
    Edge_MCU <--> Load_Router

    Edge_MCU <-->|MQTT over TLS via 4G / 2G Fallback| Agro_Twin
    Agro_Twin <--> Det_RAG
    Agro_Twin <--> FPO_Dash
    Agro_Twin <--> DISCOM_Port
    Det_RAG <--> Farmer_App
```

---

## 2. The Three Flow Topologies

### Flow 1: Data Flow Topology

```mermaid
sequenceDiagram
    autonumber
    participant Soil as FDR Soil Probe
    participant Edge as Edge Gateway (MCU)
    participant VFD as Altivar Solar VFD
    participant Cloud as Cloud Digital Twin
    participant Farmer as Farmer Phone (WhatsApp/SMS)

    Soil->>Edge: Periodic LoRa Telemetry (Moisture @ 10cm, 30cm, Temp)
    Edge->>VFD: Poll Modbus Registers (DC Bus V, Motor Current, Hz, Faults)
    VFD-->>Edge: Returns Telemetry Payload
    Edge->>Edge: Execute Local FAO-56 Water Balance & TinyML Depletion
    alt Moisture < RAW (Depletion Threshold Met)
        Edge->>VFD: Send Modbus RUN command (Target: 48 Hz)
        Edge->>Soil: Pulse OPEN Latching Solenoid Valve
        Edge->>Farmer: SMS/Audio: "Irrigation Started. Solar Pumping Active."
    else Moisture >= Field Capacity (Soil Saturated)
        Edge->>Soil: Pulse CLOSE Latching Solenoid Valve
        Edge->>VFD: Ramp down pump motor to 0 Hz
        Edge->>Edge: Trigger TeSys Contactor: Divert Solar to Cold Room
        Edge->>Farmer: SMS/Audio: "Root Zone Full. Diverting Solar to Cold Storage."
    end
    Edge->>Cloud: Opportunistic MQTT Batch Upload (Compressed JSON)
```

### Flow 2: Energy Flow Topology

```mermaid
flowchart LR
    Solar[Solar PV Array\n3.0 kW - 5.0 kW Peak DC] -->|DC Bus: 350V - 600V| Inverter[Altivar ATV320\nVariable Frequency Drive]
    
    Inverter --> Switch{Schneider TeSys\nContactor Interlock}
    
    Switch -->|Morning / Soil Stress| Pump[Submersible Pump Motor\n3HP AC Induction Motor]
    Pump --> Hydraulic[Pressurized Water Output\n12,000 Litres/hr into Drip Lines]
    
    Switch -->|Afternoon / Quota Met| Cold[Micro-Cold Room\n1.8 kW Variable Speed Compressor]
    Cold --> Thermal[Thermal Storage / PCM Ice Bank\nMaintains 4°C for 36 Hours]
```

### Flow 3: Financial & Economic Flow Topology

```mermaid
flowchart TD
    Gov[Ministry MNRE / State Govt] -->|60% PM-KUSUM Subsidy| SolarHardware[Solar Pump & Altivar VFD Capital]
    Bank[NABARD / Commercial Bank] -->|30% Soft Loan at 4% Interest| FPO[Farmer Producer Org / Farmer]
    Farmer[Smallholder Farmer] -->|10% Equity Margin (₹15,000)| FPO
    
    FPO -->|Deploys AgroStruxure| Asset[Shared Pump & Micro-Cold Storage]
    
    Asset -->|Saves ₹8,000 Diesel / Pump Repairs| Savings[Farmer Working Capital Retained]
    Asset -->|Eliminates 20% Onion/Veg Spoilage| MandiRevenue[High Mandi Off-Season Sales: +₹35,000]
    
    Savings --> LoanRepay[Loan Amortization: Paid off in <14 Months]
    MandiRevenue --> LoanRepay
    LoanRepay --> NetWealth[Sustainable Rural Prosperity & Aquifer Conservation]
```
