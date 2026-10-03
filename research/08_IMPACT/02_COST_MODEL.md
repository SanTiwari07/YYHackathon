# 02 Cost Model, BOM Breakdown & Two-Tier Unit Economics

**Document Code:** COST-BOM-02  
**Domain:** Hardware Bill of Materials, Capex, Opex & Two-Tier Payback Economics  
**Python Reference Model:** `impact_model.py` (Run `python impact_model.py` to reproduce all figures)

---

## 1. Edge Controller Bill of Materials (BOM)

The physical AgroStruxure edge controller is engineered using commercially available industrial components in India, built from the bottom up to include all required sensing, switching, and metering hardware:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AGROSTRUXURE CONTROLLER BOM (1,000-UNIT SCALE)                      │
├────┬─────────────────────────────┬──────────────────────────────────────────┬──────────────┬───────────┤
│Item│ Component Description       │ Part / Engineering Specification         │ Unit Qty     │ Cost (INR)│
├────┼─────────────────────────────┼──────────────────────────────────────────┼──────────────┼───────────┤
│ 1  │ Edge Microcontroller (MCU)  │ ESP32-S3-WROOM-1 (16MB Flash, 8MB PSRAM) │ 1 Unit       │ ₹420      │
│ 2  │ RS485 Isolated Transceiver  │ MAX485 + TVS Diode Array (2.5kV Isol.)   │ 1 Unit       │ ₹180      │
│ 3  │ Dual-Depth FDR Soil Probes  │ Capacitive Sealed Probes (10cm & 30cm)   │ 2 Probes     │ ₹760      │
│ 4  │ Temperature & RH Sensor     │ SHT31-D IP65 Probe [Local ET0 Input]     │ 1 Unit       │ ₹180      │
│ 5  │ Solar Irradiance Sensor     │ Silicon Pyranometer / PV Cell [ET0 Input]│ 1 Unit       │ ₹420      │
│ 6  │ Pulse Flow Meter            │ 1-inch Hall-Effect [Entitlement Metering]│ 1 Unit       │ ₹650      │
│ 7  │ Latching Solenoid Valve     │ 1-inch 12V DC Bistable (Zero Hold Power) │ 1 Unit       │ ₹650      │
│ 8  │ DC Changeover Switchgear    │ Schneider TeSys D Contactors ×2 (Interl.)│ 1 Pair       │ ₹2,300    │
│ 9  │ Power Supply & Coil Driver  │ 24V SMPS + Opto-Isolated Relay Board     │ 1 Kit        │ ₹380      │
│ 10 │ Cellular Modem Backhaul     │ SIM7600 4G LTE Cat-1 + Antenna (2G Fall) │ 1 Unit       │ ₹620      │
│ 11 │ Industrial Enclosure & Prot.│ IP67 Enclosure, DIN Rail, DC SPD, PCB    │ 1 Kit        │ ₹980      │
├────┴─────────────────────────────┴──────────────────────────────────────────┴──────────────┼───────────┤
│ **TOTAL EDGE CONTROLLER BOM COST (1,000-Unit Production Volume)**                          │ **₹7,540**│
└────────────────────────────────────────────────────────────────────────────────────────────┴───────────┘
```

---

## 2. Two-Tier Unit Economics & System Payback

Rather than conflating cold storage revenues with controller costs, AgroStruxure evaluates capital expenditure across two distinct operational deployment tiers:

### Tier A: Farm-Gate Pre-Cooler (4-Farm Shared Cluster)
* **Design Concept:** A 2 MT Phase-Change Material (PCM) pre-cooler located at the pump shed, shared across 4 neighbouring smallholders.
* **Shared-Array Novelty:** Powered by the existing 4.8 kWp pump PV array during the midday 11:30 AM–03:30 PM surplus window. **Eliminates the need for a dedicated 2.6 kWp PV array.**
* **Capital Cost Derivation:**
  - 2 MT PCM Pre-Cooler Base Capex: **₹4,00,000**
  - Avoided PV Array Capex (2.6 kWp @ ₹35,000/kWp): **-₹91,000**
  - Net Hardware Capex: **₹3,09,000**
  - MIDH / AIF Capital Subsidy (35%): **-₹1,08,150**
  - Net Capital Outlay (Cluster Total): **₹2,00,850**
  - **Net Capital Outlay Per Farm (4-farm cluster):** **₹50,212**
* **Annual Farmer Net Financial Benefit:**
  - Avoided Farm-Stage Spoilage (1.31 t @ ₹12/kg): **+₹15,732/year**
  - Avoided Mandi Distress Sale (holding 2–4 days): **+₹12,000/year**
  - Less Annual Cluster Opex Share (SIM + Maint.): **-₹2,400/year**
  - **Total Net Annual Farmer Gain:** **₹25,332/year**
* **Payback Period (Tier A):**
  $$\text{Post-Subsidy Payback} = \frac{₹50,212}{₹25,332} = \mathbf{2.0\text{ Years (2 Crop Seasons)}}$$
  $$\text{Pre-Subsidy Payback} = \frac{₹3,09,000 / 4}{₹25,332} = \mathbf{3.0\text{ Years}}$$

---

### Tier B: FPO Aggregation Hub (20-Farm Village Center)
* **Design Concept:** A centralized 5 MT holding room with multi-day PCM holdover located at the village aggregation hub, supporting 20 member farms.
* **Array Specification:** Equipped with its own dedicated 4 kWp solar array (claims **no** shared-array capex deduction).
* **Capital Cost Derivation:**
  - 5 MT Hub Capex (including dedicated PV): **₹12,00,000**
  - MIDH / AIF Capital Subsidy (35%): **-₹4,20,000**
  - Net Capital Outlay: **₹7,80,000**
* **Operating Revenue & Opex:**
  - Annual Throughput (22.5 turns × 65% utilization): **73 tonnes/year**
  - Storage Revenue (@ ₹3.00/kg/stay): **₹2,19,375/year**
  - Less Annual Opex (operator + SIM + maintenance): **-₹35,000/year**
  - **Net Annual FPO Revenue:** **₹1,84,375/year**
* **Payback Period (Tier B):**
  $$\text{Post-Subsidy Payback} = \frac{₹7,80,000}{₹184,375} = \mathbf{4.2\text{ Years}}$$
  $$\text{Pre-Subsidy Payback} = \frac{₹12,00,000}{₹184,375} = \mathbf{6.5\text{ Years}}$$

---

### Standalone Controller Payback (Tier 0 Retrofit)
* **Controller Cost:** ₹7,540
* **Farmer Savings:**
  - Avoidance of pump dry-running and motor rewinding (1 rewind every 2 years @ ₹5,000 = ₹2,500/year).
  - Yield protection from root hypoxia and waterlogging (conservatively ~₹2,500/year).
  - Total annual savings: ~₹5,000/year.
* **Payback Period:**
  $$\text{Controller Payback} = \frac{₹7,540}{₹5,000} \approx \mathbf{1.5\text{ Years (~1.5 Crop Seasons)}}$$
