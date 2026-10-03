# Yuva Yodha Energy Tech Hackathon 2026: Research & Architecture Repository
## Track: Challenge 01, Sustainable Agriculture: Energy, Water & Productivity
### Host: Schneider Electric India

Research, system architecture, impact model and pitch deck for **AgroStruxure™**.

---

## Executive Summary: AgroStruxure™

**AgroStruxure™** is an edge-first agri-energy microgrid and closed-loop precision irrigation retrofit for **PM-KUSUM Component B** solar pumps. It bridges Schneider Electric's **EcoStruxure™** architecture (Altivar Solar ATV320, TeSys D) with smallholder realities.

* **The problem:** Daytime solar power is free, so nothing limits pumping (an IWMI-cited Rajasthan study reports 16–39% more extraction after solarisation; CGWB 2023 lists 736 of 6,553 assessment units as over-exploited). Once irrigation is right-sized, most of the array's output has no pumping use, and 8.37% of tomatoes are lost at farm stage (NABCONS 2022).
* **The solution:** A ₹7,540 (1,000-unit BoM) edge controller sets an FAO-56 water entitlement, reads dual-depth FDR probes and a flow meter, stops the pump at field capacity, and, after an 8 s ramp-down and 5 s dead-band, transfers the DC bus through interlocked TeSys D contactors to a shared 2 MT pre-cooler serving four farms. A read-only AI gives Marathi/Hindi WhatsApp voice advice.
* **Impact (per hectare of tomato, Nashik, 4.8 kWp pump; `research/08_IMPACT/impact_model.py`):**
  - **41.2% less groundwater**: 17,000 → 10,000 m³/yr (7,000 m³; 5,000 from drip hardware, 2,000 from the entitlement cap). Assumes drip is already installed.
  - **Energy:** pumping 4,118 → 2,422 kWh; idle PV 2,442 kWh (37%) today, 4,137 kWh (63%) once water is right-sized; cooling a four-farm cluster uses 1,062 kWh (26% of the host farm's surplus).
  - **1.31 t of tomatoes saved** (8.37% → 4.00% farm-stage loss, a design target), worth ₹15,732 plus ₹12,000 price timing.
  - **Net farmer gain ₹25,332/yr; payback 2.0 years** (4 harvests; 3.0 years unsubsidised) on ₹50,212 net capex per farm. Controller alone: 1.5 years.
  - **0.39 t CO₂e/ha/yr** embodied emissions of avoided spoilage (no diesel credit claimed).

All claims are tracked in [`docs/08_CLAIM_LEDGER.md`](./docs/08_CLAIM_LEDGER.md).

---

## Deliverables

* **Deck (native, editable, 16:9, 10 slides):** [`AgroStruxure_YuvaYodha_2026_Final.pptx`](./AgroStruxure_YuvaYodha_2026_Final.pptx). Real text, native charts and tables, speaker notes. Fonts: Calibri and Consolas (Nirmala UI for Devanagari).
* **Deck (PDF, searchable text, fonts embedded):** [`AgroStruxure_YuvaYodha_2026_Final.pdf`](./AgroStruxure_YuvaYodha_2026_Final.pdf)
* **Viewer:** [`presentation.html`](./presentation.html) (slide proofs, keyboard navigation)
* **300–500-word portal summary:** [`research/11_SUBMISSION/EXEC_SUMMARY_500W.md`](./research/11_SUBMISSION/EXEC_SUMMARY_500W.md)
* **Long-form proposal:** [`research/11_SUBMISSION/PROPOSAL.md`](./research/11_SUBMISSION/PROPOSAL.md)
* **Audit and rebuild log:** [`presentation/docs/AUDIT_AND_REBUILD_2026-10-03.md`](./presentation/docs/AUDIT_AND_REBUILD_2026-10-03.md)

Rebuild the deck (Windows with desktop PowerPoint; `pip install python-pptx pillow`):

```powershell
python presentation/build/build_deck.py
powershell -NoProfile -ExecutionPolicy Bypass -File presentation/build/export_office.ps1
```

---

## Repository layout

```
YYHackathon/
├── AgroStruxure_YuvaYodha_2026_Final.pptx / .pdf   the deck (single copy)
├── presentation/
│   ├── build/        python-pptx builder (kit.py, charts.py, slides_a/b/c.py), export_office.ps1
│   ├── qa/           1920x1080 PNG proofs exported from PowerPoint
│   └── docs/         audit and rebuild log
├── docs/             design system, product truth, claim ledger, component/page specs
├── research/         00_ADMIN … 12_SOURCES (hackathon rules, Schneider, PS1, market, technical, solution,
│                     impact model, prototype, deployment, submission, sources)
├── assets/           media and brand assets, asset ledger
└── archive/          superseded decks, HTML deck v1, v1 deck docs, legacy scripts, old work
```

---

## Key dates

* **Phase 1 idea submission:** closes **October 4, 2026** (the public pages show "Aug 15 – Oct 4"; confirm the exact time and file requirements on the YouNoodle form).
* **Phase 2 prototype and evaluation window:** October 11 to November 22, 2026.
* **Top 10 announced:** December 6, 2026. **National finale:** January 2027, Bengaluru.
