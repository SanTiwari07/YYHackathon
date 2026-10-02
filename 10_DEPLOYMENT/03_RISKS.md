# 03 Comprehensive Risk Register & Mitigation Matrix

**Document Code:** RISK-REG-03  
**Domain:** Risk Assessment, Failure Modes & Resilience Protocols  

---

## 1. Multi-Dimensional Risk Heatmap

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SYSTEM RISK HEATMAP                             │
├────┬─────────────────────────────┬──────────┬──────────┬──────────────┤
│ ID │ Risk Description            │ Severity │ Likeli-  │ Overall Risk │
│    │                             │ (1–5)    │ hood(1–5)│ Rating       │
├────┼─────────────────────────────┼──────────┼──────────┼──────────────┤
│ R1 │ In-Field Sensor Fouling /   │ 4 (High) │ 4 (High) │ **CRITICAL** │
│    │ Rodent Damage               │          │          │              │
├────┼─────────────────────────────┼──────────┼──────────┼──────────────┤
│ R2 │ Farmer Bypassing Controller │ 4 (High) │ 3 (Med)  │ **HIGH**     │
│    │ (Manual override abuse)     │          │          │              │
├────┼─────────────────────────────┼──────────┼──────────┼──────────────┤
│ R3 │ Rural Cellular Blackouts    │ 3 (Med)  │ 5 (High) │ **HIGH**     │
│    │ (Long telecommunication loss│          │          │              │
├────┼─────────────────────────────┼──────────┼──────────┼──────────────┤
│ R4 │ Extreme High Ambient Heat   │ 4 (High) │ 3 (Med)  │ **HIGH**     │
│    │ (Pump shed reaches 52°C)    │          │          │              │
├────┼─────────────────────────────┼──────────┼──────────┼──────────────┤
│ R5 │ Rural Lightning Strikes /   │ 5 (Fatal)│ 2 (Low)  │ **HIGH**     │
│    │ High-Voltage Surges         │          │          │              │
├────┼─────────────────────────────┼──────────┼──────────┼──────────────┤
│ R6 │ Cold Room PCM Refrigeration │ 3 (Med)  │ 2 (Low)  │ **MEDIUM**   │
│    │ Leak or Thermal Decay       │          │          │              │
├────┼─────────────────────────────┼──────────┼──────────┼──────────────┤
│ R7 │ PM-KUSUM Subsidy Delay /    │ 3 (Med)  │ 3 (Med)  │ **MEDIUM**   │
│    │ Regulatory Policy Shift     │          │          │              │
└────┴─────────────────────────────┴──────────┴──────────┴──────────────┘
```

---

## 2. Granular Risk Analysis & Mitigation Strategies

### Risk R1: In-Field Sensor Fouling & Physical Damage
* **Vulnerability:** Field probes are exposed to rodents, tractor tillers, fertilizer salts, and extreme soil baking.
* **Mitigation Strategy:**
  1. Use stainless steel-armored subterranean conduit for probe wiring.
  2. Adopt sealed FDR capacitive sensors with no exposed metal traces.
  3. Implement automated algorithmic plausibility checks: if a sensor reads 0% or 100% moisture for >6 hours without rain, the gateway flags an "Inspect Sensor" alarm and falls back to historical ET0 scheduling.

### Risk R2: Farmer Bypassing the Automation Controller
* **Vulnerability:** If farmers do not trust the automated system, they will cut wires and wire the pump motor directly to the switchgear, re-enabling flood irrigation.
* **Mitigation Strategy:**
  1. Provide a prominent, labeled physical **Manual Override Rotary Switch** on the enclosure: `[AUTO | MANUAL RUN | OFF]`.
  2. Implement an "Educational Credit" model in the FPO: farmers who follow automated water quotas receive priority hours for micro-cold room storage.

### Risk R3: Rural Cellular Telecommunication Outages
* **Vulnerability:** Cell towers frequently lose grid power for days during monsoons or storms.
* **Mitigation Strategy:**
  1. **Strict Thick-Edge Design:** The edge gateway executes 100% of irrigation and power-routing algorithms autonomously without requiring a cloud connection.
  2. On-board circular flash memory stores up to 90 days of operational telemetry.

### Risk R4: High Ambient Heat & Electronics Degradation
* **Vulnerability:** Metal pump sheds in Rajasthan and Maharashtra reach internal temperatures exceeding 50°C during April–May.
* **Mitigation Strategy:**
  1. Use industrial-grade components rated for $-40^\circ\text{C}$ to $+85^\circ\text{C}$ operation.
  2. Utilize passive heatsink dissipation, IP66-rated breathable vents, and UV-stabilized polycarbonate enclosures.

### Risk R5: Rural Lightning Strikes & Power Grid Surges
* **Vulnerability:** Overhead lines in open rural plains attract high-voltage lightning surges that destroy microcontrollers.
* **Mitigation Strategy:**
  1. Dedicated Class II DC Surge Protection Devices (SPD) on the PV input lines.
  2. Galvanically isolated RS485 transceivers with TVS diodes protecting communication channels.
  3. Proper earth-grounding rod installation mandated for every installation.
