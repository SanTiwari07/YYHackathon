# 01 Audit of Existing Codebase & Assets (My Old Work)

**Document Code:** AUDIT-OLD-01  
**Target Repositories Audited:**  
1. `GramDrishti` (Village-Level Geospatial Decision Support System)  
2. `Global Farmer Platform` (`other work/references/6182.md` EOSDA-style platform specification)  
**Audit Date:** October 2, 2026  
**Auditor:** Technical Due-Diligence & Systems Architect  

---

## 1. System Inventory & High-Level Architecture of Old Work

### Asset 1: GramDrishti
* **Type:** Geospatial Decision Support System (GDSS) for Gram Panchayats and district officials.
* **Stack:**
  - Frontend: React 18.3, Vite 8, TypeScript 5.9, Tailwind CSS 3.4, React Leaflet, ECharts, Framer Motion, i18next (EN, HI, MR).
  - Backend: FastAPI (Python 3.11), Uvicorn, Pydantic v2, Google Earth Engine API, Open-Meteo API, ReportLab (PDF), Gemini 2.5 Flash / Ollama (hybrid RAG).
  - Data Store: In-memory dictionary cache with TTL; pre-indexed local GeoJSON village boundary polygons.
* **Core Functionality:** Calculates village environmental health score across 5 dimensions: Water Security, Vegetation Health, Climate Stability, Flood Preparedness, and Land Sustainability. Features deterministic AI RAG pipeline with multilingual chat.

### Asset 2: Global Farmer Platform (`other work/references/6182.md`)
* **Type:** Field-level farm management and precision scouting platform specification.
* **Stack Proposed:** Go (Chi router, Sqlc, Goose migrations), PostGIS / PostgreSQL, Next.js, Redis, Google Earth Engine.
* **Core Functionality:** Farmer plot boundary registration, multi-spectral index calculation (NDVI, NDWI, EVI), variable rate application (VRA) zoning, weather risk alerts, and field scout logging.

---

## 2. Objective Component Categorization

Every component from the old work is critically evaluated against the requirements of the 2026 Yuva Yodha Hackathon (Challenge 01: Energy, Water & Productivity):

```
┌────────────────────────────────────────────────────────────────────────┐
│                  OLD WORK COMPONENT DISPOSITION MATRIX                 │
├───────────────┬───────────────────────────────┬────────────────────────┤
│ Category      │ Component Name                │ Disposition Summary    │
├───────────────┼───────────────────────────────┼────────────────────────┤
│ KEEP          │ • Agentic Deterministic RAG   │ Reusable as-is for     │
│               │   Orchestrator Architecture   │ hallucination-free AI  │
│               │ • Multilingual System (i18n)  │ Vernacular EN/HI/MR    │
│               │ • Open-Meteo Weather Service  │ Hourly weather parsing │
├───────────────┼───────────────────────────────┼────────────────────────┤
│ UPGRADE       │ • Google Earth Engine Pipeline│ Transition from village│
│               │   (Sentinel-2 NDVI & NDWI)    │ polygon to plot polygon│
│               │ • PDF Report Engine           │ Re-theme from village  │
│               │   (ReportLab Generator)       │ health to energy audit │
│               │ • ECharts Visual Dashboard    │ Add VFD power & solar  │
├───────────────┼───────────────────────────────┼────────────────────────┤
│ REWRITE       │ • Health Scoring Engine       │ Replace 5-pillar score │
│               │   (Village Composite Score)   │ with FAO-56 Water &    │
│               │                               │ Energy Nexus Engine    │
├───────────────┼───────────────────────────────┼────────────────────────┤
│ DISCARD       │ • Macro Village Boundary Index│ Not relevant to field- │
│               │   (Gram Panchayat GeoJSONs)   │ level farm irrigation  │
│               │ • Flood / Terrain Risk Matrix │ Irrelevant to solar    │
│               │   (Gram-level DEM analysis)   │ pump power scheduling  │
├───────────────┼───────────────────────────────┼────────────────────────┤
│ OPTIONAL /    │ • Go/PostGIS Backend Spec     │ Keep as enterprise     │
│ DEFERRED      │   (From 6182.md)              │ architecture reference │
└───────────────┴───────────────────────────────┴────────────────────────┘
```

---

## 3. Detailed Rationale by Category

### A. KEEP (High Value, Zero Rewrite Needed)
1. **Agentic Deterministic RAG Pattern (`backend/services/ai_service.py` & `processors/`):**
   - *Rationale:* The separation of computation (deterministic Python processors) from narrative generation (Gemini LLM) completely eliminates hallucination of critical metrics. This pattern is directly applicable to generating agronomic advisories from pump/soil data.
2. **Multilingual Architecture (`frontend/src/i18n/`):**
   - *Rationale:* Native support for English, Hindi, and Marathi with localized key-value JSON structures is already built and tested.

### B. UPGRADE (Valuable Intellectual Asset, Requires Domain Shift)
1. **Satellite Remote Sensing Pipeline (`backend/services/gee_service.py`):**
   - *Current State:* Takes a coarse village polygon boundary and computes spatial mean NDVI/NDWI across hundreds of hectares.
   - *Upgrade Mandate:* Adapt geometry input to accept specific farmer plot boundary GeoJSONs, extracting micro-plot vegetative vigor and canopy water stress.
2. **Automated Report Generation (`backend/services/report_service.py`):**
   - *Current State:* Generates a 3-page "Gram Panchayat Environmental Health Card" PDF.
   - *Upgrade Mandate:* Transform into a "Solar Farm Energy & Irrigation Audit Report" formatted for FPOs, showing kWh generated, water conserved, and post-harvest cold room utilization.

### C. REWRITE (Conceptual Intent Valid, Implementation Incompatible)
1. **The Scoring Engine (`backend/services/scoring_service.py`):**
   - *Current State:* Computes an abstract 0–100 score: $(0.25\times \text{Water}) + (0.25\times \text{Veg}) + (0.20\times \text{Climate}) + (0.15\times \text{Flood}) + (0.15\times \text{Land})$.
   - *Why It Must Be Rewritten:* This score is completely arbitrary for pump operations. It cannot tell a variable frequency drive when to open a valve or how many liters of water to apply.
   - *Target Rewrite:* A physics-grounded **Irrigation & Energy Management Engine** implementing the FAO-56 Penman-Monteith water balance and solar load diversion logic.

### D. DISCARD (Dead Weight for an Energy Tech Hackathon)
1. **Village-Level Administrative Indexing (`backend/data/*.geojson`):**
   - GramDrishti indexed specific administrative villages in Pune district (Mulshi, Maval, Haveli). Farmers do not irrigate administrative boundaries; they irrigate cadastral survey plots. Retaining this would distract the jury.
2. **Gram-Level Flood & Disaster Models:**
   - Flooding and terrain steepness models built for disaster preparedness are irrelevant to Challenge 01 (Sustainable Agriculture: Energy, Water & Productivity).
