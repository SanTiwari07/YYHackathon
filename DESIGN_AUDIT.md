# AgroStruxure™ UI/UX Design Audit & Architecture Assessment
**Document Code:** AUDIT-UI-01  
**Project:** AgroStruxure™ (Yuva Yodha 2026 / Schneider Electric India)  
**Author:** Senior Product Designer & UX Architect  
**Status:** Complete Audit & Gap Analysis  

---

## 1. Executive Summary of Audit

An exhaustive forensic inspection was conducted across the repository, past intellectual property assets (`GramDrishti` and `Pragya` in `06_OLD_WORK_AUDIT`), solution specifications (`07_SOLUTION_DESIGN`), and prototype plans (`09_PROTOTYPE`).

The audit reveals that while the **mathematical models (FAO-56 Penman-Monteith)**, **satellite pipelines (Sentinel-1 SAR and Sentinel-2)**, and **backend simulation engines** are exceptionally robust, the **front-end presentation layer requires a systematic upgrade** to match the industrial polish of Schneider Electric’s **QuartzDS** and the high-energy clarity of the **Yuva Yodha Tech Hackathon**.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DESIGN AUDIT SCORECARD                          │
├────────────────────────┬────────┬──────────────────────────────────────┤
│ Dimension              │ Rating │ Audit Finding                        │
├────────────────────────┼────────┼──────────────────────────────────────┤
│ 1. Domain Physics      │ 98/100 │ FAO-56 and hydraulic models rigorous │
│ 2. Data Architecture   │ 95/100 │ Modbus register maps & MQTT well-spec│
│ 3. Industrial Semantics│ 72/100 │ Altivar & TeSys visual assets pending│
│ 4. Rural Accessibility │ 68/100 │ High dependency on English dashboards│
│ 5. Component Harmony   │ 64/100 │ Fragmented styling across past repos │
│ 6. Demonstration Impact│ 60/100 │ 24-hr diurnal scrubber needed in UI  │
└────────────────────────┴────────┴──────────────────────────────────────┘
```

---

## 2. Forensic Review of Reusable Assets from Old Work

### 2.1 Harvestable Assets from `GramDrishti` (`06_OLD_WORK_AUDIT`)
| Source Asset | Original Purpose | Usability for AgroStruxure | Audit Status | Required Redesign / Adaptation |
|---|---|:---:|:---:|---|
| `backend/services/ai/rag_service.py` | Gram Panchayat RAG Copilot | High | **KEEP & REPURPOSE** | Enforce rigid prompt contract: inject Modbus registers, VFD kW, and soil % into context block to guarantee zero-hallucination. |
| `frontend/src/locales/{en,hi,mr}.json`| Tri-lingual localization | High | **KEEP & EXPAND** | Harvest existing Hindi and Marathi agricultural dictionaries. Add microgrid, VFD frequency, contactor switch, and cold room terms. |
| `backend/services/reports/pdf_generator.py`| PDF audit report | High | **KEEP & REPROFILE**| Rebrand ReportLab template with Schneider Electric typography and AgroStruxure dual-audit card (Energy Saved + Water Saved). |
| `frontend/src/components/dashboard/` | Panchayat macro risk cards | Low | **DISCARD** | Discard macro-level village flood indicators; focus strictly on field-level microgrid telemetry. |

### 2.2 Harvestable Assets from `Pragya` / Global Farmer Platform (`06_OLD_WORK_AUDIT`)
| Source Asset | Original Purpose | Usability for AgroStruxure | Audit Status | Required Redesign / Adaptation |
|---|---|:---:|:---:|---|
| `internal/pipeline/radar_indices.go` | Sentinel-1 SAR SMI calculation | High | **KEEP & INTEGRATE**| Cloud-penetrating soil moisture index serves as satellite failover anchor in UI when physical FDR probes disconnect. |
| `internal/pipeline/indices.go` | Sentinel-2 NDVI / NDMI | High | **KEEP & REPURPOSE**| Maps crop canopy vigor to stage-dependent crop coefficient ($K_c$) for real-time evapotranspiration calculation. |
| `frontend/src/pages/steps/` | 8-step farmer onboarding wizard | Medium | **RESTRUCTURE** | Streamline from 8 verbose steps down to 3 high-impact onboarding steps: 1) Cadastral plot & soil, 2) Solar pump & VFD rating, 3) Cold storage link. |
| `frontend/src/components/map/` | Leaflet cadastral boundary map | High | **KEEP & ADAPT** | Retain polygon drawing tool with satellite layer; add root moisture depth overlay. |

---

## 3. UI/UX Gaps in Existing Architecture

### 3.1 Gap 1: Disconnected Mental Models (Pumping vs. Storage)
- **Current Defect:** Solar pumping dashboards typically display motor RPM or water flow as isolated metrics. The farmer or operator does not see *why* pumping stopped or *where* solar energy is flowing.
- **Remediation:** Introduce the **Animated Industrial Flow Topology** on the primary cockpit. The user visually tracks solar DC power traveling from the PV array through the Altivar VFD to the TeSys contactor, and dynamically rerouting into the cold room compressor when soil field capacity is achieved.

### 3.2 Gap 2: Cognitive Overload for Low-Literacy Farmers
- **Current Defect:** Traditional SCADA screens display walls of numbers ($e_s$, $e_a$, $\Delta$, $\gamma$, Modbus hex codes) that intimidate rural operators.
- **Remediation:** Implement **Dual-Persona Layering**:
  - **Farmer Mode (Default):** High-contrast physical metaphors: underground soil root moisture tank, big green/blue status buttons, 1-click Marathi/Hindi voice advisory audio note, simplified rupee savings counter.
  - **Technician & Jury Mode (Tab Switch):** Real-time Modbus register telemetry inspector (Registers `3201–3208`, `8501–8502`), live FAO-56 Penman-Monteith physics calculation stream, inverter efficiency curves.

### 3.3 Gap 3: Demonstration Friction for Hackathon Pitch
- **Current Defect:** Testing solar diurnal behavior requires waiting 12 real-world hours. In a 5-minute hackathon jury pitch, evaluators cannot see the morning pumping transition into the afternoon cold storage without an interactive control.
- **Remediation:** Build the **24-Hour Diurnal Interactive Time Scrubber**. A draggable slider lets evaluators scrub through the day in 10 seconds, triggering simulated solar curves, soil saturation events, contactor latching, and passing cloud transients in real time.

---

## 4. Design System Compliance Audit Against Schneider QuartzDS

| QuartzDS Standard Element | Present in Existing Code | Target State in AgroStruxure | Compliance Roadmap |
|---|:---:|:---:|---|
| **Signature Green (`#3DCD58`)** | Partial (Generic green used) | Full `@quartzds` color token alignment | Standardize on `--se-primary: #3dcd58` with `#090b0c` text contrast |
| **Typography (`Arial Rounded MT`)**| No (System sans used) | Fallback stack with rounded contours | Import `"Arial Rounded MT for SE"` and `"Poppins"` |
| **Pill Inputs (`radius: 999px`)** | No (Rectangular inputs used) | Full implementation for search & filters | Adopt QuartzDS 40px height pill inputs with 0.8px subtle border |
| **Card Borders (`0.8px #e6e6e6`)** | No (Standard Tailwind `border-gray-200`) | Exact 0.8px divider tokens | Clean industrial cards with subtle hover elevation (`hover:shadow-xl`) |
| **Dark Theme Footer (`#151a1c`)** | No (Standard dark footer) | Exact QuartzDS `#151A1C` surface | Implement inverted theme bottom bar with legal and telemetry stamps |

---

## 5. Audit Recommendations & Architecture Roadmap

1. **Establish a Single Source of Truth:** Unify all design variables into `DESIGN_SYSTEM.md` and implement CSS design tokens in the front-end layout.
2. **Build Modular Primitive Components:** Construct reusable UI primitives (`Button`, `Badge`, `Gauge`, `Scrubber`, `ContactorGraphic`, `VoiceCard`) before constructing full views.
3. **Isolate Simulation Engine from Presentation:** Keep `AgroSim` (FastAPI / WebSockets) completely decoupled from the React 18 front-end so UI state updates reactively to incoming Modbus events.
4. **Enforce Accessibility Benchmarks:** Test color combinations under simulated bright outdoor daylight (simulated 10,000 lux desaturation) to ensure field usability for smallholders.
