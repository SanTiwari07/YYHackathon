# 03 Step-by-Step Jury Demonstration Script

> **Superseded figures (2026-10-03).** This document predates the corrected impact model. Numbers such as 42–64% water saving, 2,555 kWh, 4,200 kWh, 2.8 t, +₹72,450, "<18-day payback", ₹3,480 BoM, 3,187 kWh "captured" and 2.94 t CO₂e are retired. Quote figures only from `docs/08_CLAIM_LEDGER.md` (41.2%, 7,000 m³, 1,062 kWh cluster cooling, 1.31 t, ₹25,332/yr, 2.0-year payback, ₹7,540 BoM, 0.39 t CO₂e).

**Document Code:** DEMO-SCRIPT-03  
**Target Audience:** Schneider Electric Senior Leadership & Hackathon Evaluation Jury  
**Duration:** Exactly 5 Minutes (Standard Pitch Window)  

---

## 1. Demo Narrative Arc & Timing Blueprint

```
┌────────────────────────────────────────────────────────────────────────┐
│                        5-MINUTE PITCH & DEMO ARC                       │
├──────────┬─────────────────────────────┬───────────────────────────────┤
│ Timestamp│ Scene / Action              │ Key Talking Points & Impact   │
├──────────┼─────────────────────────────┼───────────────────────────────┤
│ 00:00 –  │ SCENE 1: The Indian Agri-   │ • 87% groundwater extraction; │
│ 00:45    │ Energy Paradox              │   unmetered free farm power.  │
│          │ (Problem Context)           │ • The PM-KUSUM Rebound Effect │
│          │                             │   and 20% post-harvest loss.  │
├──────────┼─────────────────────────────┼───────────────────────────────┤
│ 00:45 –  │ SCENE 2: The Solution       │ • Introduce AgroStruxure:     │
│ 01:30    │ (EcoStruxure Convergence)   │   Connected Products + Edge.  │
│          │                             │ • Altivar Solar ATV320 synergy│
├──────────┼─────────────────────────────┼───────────────────────────────┤
│ 01:30 –  │ SCENE 3: Live Simulation    │ • Launch interactive console. │
│ 03:00    │ Walkthrough (The Magic)     │ • Morning: Precision Pumping. │
│          │                             │ • Noon: Auto-cut & Diversion. │
│          │                             │ • Cloud transient test.       │
├──────────┼─────────────────────────────┼───────────────────────────────┤
│ 03:00 –  │ SCENE 4: Farmer Experience  │ • Play Marathi voice note.    │
│ 03:45    │ & Smallholder UX            │ • Show 1-click manual override│
│          │                             │ • Display ₹3,480 BOM cost.    │
├──────────┼─────────────────────────────┼───────────────────────────────┤
│ 03:45 –  │ SCENE 5: Quantified Impact  │ • 42% water saved; 2,555 kWh; │
│ 05:00    │ & Commercial Scale-up       │ • +₹72,450 net farmer income. │
│          │ (Closing Pitch)             │ • SE Ventures & FPO model.    │
└──────────┴─────────────────────────────┴───────────────────────────────┘
```

---

## 2. Minute-by-Minute Spoken Script & Screen Actions

### 00:00 – 00:45 | Scene 1: The Context
* **Presenter:** *"Good morning, esteemed jury members. Today across rural India, 30 million agricultural pumps consume nearly 17% of the nation's electricity and extract 87% of all groundwater. Under the ambitious PM-KUSUM scheme, millions of solar pumps are being deployed. But here lies an unintended catastrophe: because solar power is free during daytime hours, farmers flood their fields continuously, accelerating groundwater collapse! Meanwhile, just 500 meters away, 20% of their harvested perishables rot in open heat due to lack of cold storage. Today, we introduce AgroStruxure—transforming solar irrigation from an unmetered extraction hazard into an integrated energy, water, and post-harvest microgrid."*

### 00:45 – 01:30 | Scene 2: The Solution
* **Presenter:** *"AgroStruxure natively implements Schneider Electric's EcoStruxure 3-tier architecture. At Connected Products, we integrate the Altivar Solar ATV320 VFD and TeSys contactors with an ultra-low-cost FDR soil probe. At Edge Control, our microcontroller executes local FAO-56 Penman-Monteith physics and TinyML motor protection. And at Apps & Analytics, we provide a unified digital twin for FPOs and utilities."*

### 01:30 – 03:00 | Scene 3: Live Simulation Walkthrough
* **Action:** Presenter clicks **"Start Morning Simulation" (08:30 AM)** on the live web console.
* **Screen:** Gauges animate. Solar irradiance climbs to $550\text{ W/m}^2$.
* **Presenter:** *"Notice how at 08:30 AM, root soil moisture is at 36%, below the stress threshold. Our edge controller signals the Altivar VFD over Modbus RTU. The pump starts smoothly at 38 Hz, delivering pulsed micro-drip irrigation directly to the root zone."*
* **Action:** Presenter clicks **"Fast Forward to 11:30 AM"**.
* **Screen:** Soil moisture hits 45% (Field Capacity). Valve closes instantly. The contactor animation flips. Solar power graph diverts from "Pump" to "Cold Storage Compressor".
* **Presenter:** *"Watch this pivotal moment: the instant root-zone soil moisture reaches Field Capacity, the edge controller shuts the irrigation valve! We completely prevent the solar rebound effect. But we don't shut down the solar PV. Our smart load router engages the Schneider TeSys contactor, routing 3.8 kW of peak midday solar energy to the farm-gate micro-cold room, bringing fresh tomatoes down to 4°C."*
* **Action:** Presenter clicks **"Simulate Passing Monsoon Cloud"**.
* **Screen:** Irradiance drops sharply from $800\text{ W/m}^2$ to $320\text{ W/m}^2$. VFD output frequency throttles down to 32 Hz without tripping.
* **Presenter:** *"When a dense cloud passes overhead, the Altivar drive does not violently trip; its embedded MPPT logic decelerates the compressor smoothly, maintaining continuous cooling."*

### 03:00 – 03:45 | Scene 4: Smallholder Accessibility
* **Action:** Presenter clicks the Marathi audio button.
* **Audio plays:** *"नमस्कार रमेश. तुमच्या कांद्याच्या शेताला संपूर्ण पाणी मिळाले आहे. पंप बंद आहे. तुमची सौर शीतगृह युनिट आता १००% सौर ऊर्जेवर सुरू आहे."*
* **Presenter:** *"For a smallholder in Marathwada, complex graphs are replaced by spoken Marathi audio on WhatsApp. If the farmer ever wants manual control, a single physical toggle switch on the enclosure instantly bypasses automation."*

### 03:45 – 05:00 | Scene 5: The Numbers & Close
* **Presenter:** *"The unit economics are compelling. Our edge retrofit Bill of Materials costs just ₹3,480 at scale. Against this, an average smallholder saves ₹7,500 on motor rewinding, increases crop yield by 22%, and saves 2.8 tonnes of produce, delivering an annual net gain of ₹72,450—repaying the entire capex in under 3 weeks! For Schneider Electric, AgroStruxure transforms standard solar drives into an indispensable digital microgrid, perfectly positioned for PM-KUSUM tenders and SE Ventures investment. Thank you."*
