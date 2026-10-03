# 04 Business Models, Unit Economics & Go-to-Market Strategy

> **Superseded figures (2026-10-03).** This document predates the corrected impact model. Numbers such as 42–64% water saving, 2,555 kWh, 4,200 kWh, 2.8 t, +₹72,450, "<18-day payback", ₹3,480 BoM, 3,187 kWh "captured" and 2.94 t CO₂e are retired. Quote figures only from `docs/08_CLAIM_LEDGER.md` (41.2%, 7,000 m³, 1,062 kWh cluster cooling, 1.31 t, ₹25,332/yr, 2.0-year payback, ₹7,540 BoM, 0.39 t CO₂e).

**Document Code:** MKT-BIZ-04  
**Domain:** Commercial Sustainability, Revenue Streams, Unit Economics & Scaling Channels  

---

## 1. Commercial Delivery Models

To bypass the prohibitive capex barrier for smallholders, three complementary go-to-market channels are established:

```
┌────────────────────────────────────────────────────────────────────────┐
│                     TRI-PARTITE COMMERCIAL VEHICLE                     │
├──────────────────────────┬──────────────────────────┬──────────────────┤
│ MODEL 1: PM-KUSUM OEM    │ MODEL 2: FPO Shared      │ MODEL 3: Small   │
│ Direct Retrofit (B2B)    │ Infrastructure (B2B2C)   │ Farmer Direct    │
├──────────────────────────┼──────────────────────────┼──────────────────┤
│ • Sold directly to pump  │ • FPO purchases 10HP     │ • Ultra-low-cost │
│   manufacturers (Shakti, │   Solar Pump + Cold Room │   sensor + valve │
│   Kirloskar, CRI) and    │   using AIF / NABARD     │   retrofit kit   │
│   solar EPC developers.  │   subsidies.             │   (<₹3,500).     │
│ • Bundled with Altivar   │ • Farmers pay ₹50/hour   │ • Farmers buy on │
│   VFD to meet mandatory  │   for pressurized drip;  │   Kisan Credit   │
│   RMS compliance.        │   ₹2/crate/day storage.  │   Card (KCC).    │
└──────────────────────────┴──────────────────────────┴──────────────────┘
```

---

## 2. Unit Economics Breakdown

### Capex Breakdown (Single-Farm 1-Hectare Retrofit):

| Bill of Materials (BOM) Item | Component Specification | Sourced Price (INR) |
|---|---|:---:|
| **Root-Zone Soil Sensor** | Dual-depth Frequency Domain Reflectometry (FDR) Capacitive Probe (10cm & 30cm) | ₹1,250 |
| **Edge Controller Module** | ESP32-S3 Microcontroller + RS485 Modbus Transceiver + Solar LiFePO4 Battery + IP65 Case | ₹1,400 |
| **Latching Solenoid Valve** | 2-inch Low-Power Pulse Solenoid Valve (9–12V DC Latching) | ₹850 |
| **Total Hardware BOM Cost** | **Complete Edge Retrofit Kit** | **₹3,500** |

### Annual Economic Return for a 1-Hectare Smallholder (Onion/Cotton Model):

| Financial Vector | Status Quo (Baseline) | With Proposed Smart System | Net Annual Financial Gain |
|---|:---:|:---:|:---:|
| **Water Pumping Costs** | Diesel backup or electric rewinding costs: ~₹8,000/yr | 100% Solar-driven with zero rewinding: ₹500/yr | **+₹7,500** |
| **Fertilizer Leaching Loss** | High leaching due to flood irrigation: ₹6,500/yr | Precision pulse fertigation saves 30% fertilizer: ₹4,550/yr | **+₹1,950** |
| **Yield Improvement** | Waterlogged / drought-stressed crop yield: 18 MT/ha | Optimized root oxygenation & moisture: 22 MT/ha (+22%) | **+₹28,000** |
| **Post-Harvest Loss Savings** | 18% spoilage on 18 MT sold at distress: ₹32,000 loss | 5 MT stored in micro-cold room; sold at peak mandi prices | **+₹35,000** |
| **Net Financial Impact** | Net household profit: ~₹75,000/ha | Net household profit: ~₹1,47,450/ha | **+₹72,450 / year** |

* `[INTERPRETATION]` **Payback Period:** Against an upfront retrofit investment of **₹3,500**, an annual net gain of **₹72,450** represents a payback period of **less than 18 days of harvest operation** (<0.1 crop season). Even under conservative assumptions, payback is achieved within a single crop cycle.

---

## 3. Financing & Government Scheme Alignment

1. **Agriculture Infrastructure Fund (AIF):** Provides 3% interest subvention and credit guarantee for FPOs establishing farm-gate cold rooms and post-harvest infrastructure up to ₹2 Crore.
2. **PM-KUSUM Component B & C:** Leverages the existing 60% central/state capital subsidy for solar pumping infrastructure.
3. **Per Drop More Crop (PDMC) under PMKSY:** Subsidizes micro-irrigation (drip/sprinkler) equipment up to 55% for small/marginal farmers.
