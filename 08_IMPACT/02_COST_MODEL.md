# 02 Cost Model, BOM Breakdown & Operational Expenditure

**Document Code:** COST-BOM-02  
**Domain:** Hardware Bill of Materials, Capex, Opex & Manufacturing Economics  

---

## 1. Granular Bill of Materials (BOM) Architecture

The physical system is engineered using commercially available industrial components in India, avoiding expensive custom silicon:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AGROSTRUXURE HARDWARE BOM BREAKDOWN                                   │
├────┬─────────────────────────────┬───────────────────────────┬──────────────┬──────────────┬────────────┤
│ Item│ Component Description      │ Part / Specification      │ Unit Qty     │ Unit Cost    │ Total (INR)│
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 1  │ Dual-Depth FDR Soil Probe   │ Waterproof Capacitive     │ 1 Unit       │ ₹1,250       │ ₹1,250     │
│    │                             │ Probe (10cm & 30cm)       │              │              │            │
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 2  │ Field Node Microcontroller  │ ESP32-C3 RISC-V with      │ 1 Unit       │ ₹420         │ ₹420       │
│    │ & Wireless Transceiver      │ Semtech SX1262 LoRa IN865 │              │              │            │
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 3  │ Field Node Enclosure & Power│ IP66 ABS UV-Stabilized Box│ 1 Kit        │ ₹380         │ ₹380       │
│    │                             │ + 1W Solar + LiFePO4 18650│              │              │            │
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 4  │ Edge Gateway MCU (Hub)      │ ESP32-S3 Dual-Core 240MHz │ 1 Unit       │ ₹650         │ ₹650       │
│    │                             │ with 8MB PSRAM & RTC      │              │              │            │
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 5  │ Cellular Modem Backhaul     │ SIM7600EI 4G LTE Cat-1    │ 1 Unit       │ ₹1,150       │ ₹1,150     │
│    │                             │ with 2G GPRS fallback     │              │              │            │
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 6  │ RS485 Modbus Isolated Driver│ MAX13487 Auto-Direction   │ 1 Unit       │ ₹120         │ ₹120       │
│    │                             │ RS485 Transceiver Breakout│              │              │            │
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 7  │ Latching Solenoid Pulse H-Br│ DRV8833 Dual H-Bridge     │ 1 Unit       │ ₹180         │ ₹180       │
│    │                             │ Pulse Controller Board    │              │              │            │
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 8  │ 2-inch Latching Pulse Valve │ 9V–12V DC Impulse Solenoid│ 1 Unit       │ ₹850         │ ₹850       │
│    │                             │ (Zero Continuous Current) │              │              │            │
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 9  │ Power Contactor Changeover  │ Schneider TeSys LC1D12    │ 1 Unit       │ ₹1,200       │ ₹1,200     │
│    │ Switch (Motor/Storage)      │ 3-Pole 25A Contactor      │              │ (Optional)   │ (FPO Tier) │
├────┼─────────────────────────────┼───────────────────────────┼──────────────┼──────────────┼────────────┤
│ 10 │ Surge Protection & Wiring   │ Type 2 40kA DC Surge Prot.│ 1 Kit        │ ₹450         │ ₹450       │
│    │                             │ + Shielded RS485 Cable    │              │              │            │
├────┴─────────────────────────────┴───────────────────────────┴──────────────┼──────────────┼────────────┤
│ **TOTAL RETROFIT HARDWARE COST (Basic Farm Tier: Items 1–8, 10)**            │ **PER PLOT** │ **₹5,450** │
│ **SCALE PRODUCTION COST (Volume: 5,000+ Units - Direct Sourcing / SMT)**     │ **PER PLOT** │ **₹3,480** │
└──────────────────────────────────────────────────────────────────────────────┴──────────────┴────────────┘
```

---

## 2. Operational Expenditure (Opex) Modeling

| Cost Vector | Frequency | Cost per Installation (INR) | Justification |
|---|---|:---:|---|
| **Cellular IoT SIM Data** | Annual | ₹480 / year | 100 MB/month Cat-1 M2M telemetry SIM (Jio / Airtel IoT plan) |
| **Cloud Digital Twin & DB** | Annual | ₹180 / farm / year | Multi-tenant PostgreSQL & Redis shared across 1,000 farms |
| **Field Maintenance & Battery**| Every 4 Years | ₹350 (amortized: ₹90/yr) | 18650 LiFePO4 battery replacement cycle (2,000 cycles) |
| **Total Annual Opex** | **Annual** | **₹750 / farm / year** | **Ultra-low recurring software and connectivity burden** |

* `[INTERPRETATION]` Comparing this ₹750/year opex against the **₹8,000/year** smallholders currently spend on motor winding repairs and diesel backup proves immediate cash-flow positive status from Month 1.
