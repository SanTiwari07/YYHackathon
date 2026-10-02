# 02 Reusable Code Assets, Libraries & Architectural Modules

**Document Code:** ASSETS-REUSE-02  
**Domain:** Code Reuse Inventory & Migration Feasibility  

---

## 1. Concrete Inventory of Reusable Software Modules

```
┌────────────────────────────────────────────────────────────────────────┐
│                        REUSABLE ASSET INVENTORY                        │
├──────────────────┬─────────────────────┬───────────────────────────────┤
│ Module Name      │ Original File Path  │ Migration Scope & Adaptations │
├──────────────────┼─────────────────────┼───────────────────────────────┤
│ 1. Deterministic │ `backend/services/  │ Extract intent classification │
│    AI Pipeline   │  ai_service.py` &   │ & prompt construction logic.  │
│                  │ `classifier.py`     │ Repoint intents to irrigation │
│                  │                     │ and solar power metrics.      │
├──────────────────┼─────────────────────┼───────────────────────────────┤
│ 2. Weather       │ `backend/services/  │ Reuse Open-Meteo client;      │
│    Engine        │  weather_service.py`│ expand ingested fields to     │
│                  │                     │ include solar radiation ($Rn$)│
│                  │                     │ and wind speed ($u2$) for ET0.│
├──────────────────┼─────────────────────┼───────────────────────────────┤
│ 3. Geospatial    │ `backend/services/  │ Extract Sentinel-2 cloud      │
│    Processor     │  gee_service.py`    │ masking and NDVI/NDWI red-nir │
│                  │                     │ reducer logic; accept plot BBox│
├──────────────────┼─────────────────────┼───────────────────────────────┤
│ 4. ReportLab PDF │ `backend/services/  │ Retain PDF styling, canvas    │
│    Generator     │  report_service.py` │ layout, and logo headers.     │
│                  │                     │ Change data tables to energy  │
│                  │                     │ audit and water saved.        │
├──────────────────┼─────────────────────┼───────────────────────────────┤
│ 5. Multilingual  │ `frontend/src/i18n/`│ Retain translation keys for   │
│    i18n Core     │                     │ common agricultural terms;    │
│                  │                     │ add energy & solar glossary.  │
├──────────────────┼─────────────────────┼───────────────────────────────┤
│ 6. ECharts Data  │ `frontend/src/      │ Adapt time-series charts to   │
│    Visualizers   │  components/charts/`│ render solar PV curve (kW) vs │
│                  │                     │ pump load (kW) vs soil moisture│
└──────────────────┴─────────────────────┴───────────────────────────────┘
```

---

## 2. Reusable Code Snippets & Design Patterns

### The Deterministic Prompt Guard Pattern:
```python
# Proven anti-hallucination prompt wrapper from GramDrishti
SYSTEM_INSTRUCTION = """
You are an expert agricultural and energy systems advisor for Indian farmers.
CRITICAL MANDATE:
1. Base all quantitative recommendations STRICTLY on the numerical data provided in the CONTEXT.
2. If soil moisture is above Field Capacity, NEVER recommend irrigation.
3. If solar surplus power is available, explain how it is powering cold storage.
4. If a metric is missing, explicitly state "Data unavailable" rather than guessing.
5. Provide concise, vernacular responses in the requested language.
"""
```

### The Fast In-Memory Caching Pattern:
The `TTLCache` mechanism with exponential backoff and timeout handling allows the web server to cache satellite and weather calls, ensuring sub-second response times during live jury presentations without hitting external rate limits.
