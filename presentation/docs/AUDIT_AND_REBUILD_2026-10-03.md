# Deck Audit and Rebuild: 2026-10-03

**Scope:** the original `AgroStruxure_YuvaYodha_2026_Final.pptx/.pdf` (10 PNG screenshots, no text layer), checked against `research/08_IMPACT/impact_model.py`, the claim ledger, the asset ledger, and the public Challenge 01 pages.
**Result:** rebuilt as a native, editable deck (repo root), model corrected, docs reconciled. Originals are kept in `archive/legacy_decks/02_image_only_deck_2026-10-03.*`.

**Phase 1 deadline:** Oct 4, 2026. Public pages show "Aug 15 – Oct 4" only; the 11:59 PM IST time in the repo notes was not confirmed on the portal.

---

## A. Findings and resolution

| # | Finding | Resolution |
|---|---|---|
| 1 | Slide 1 photo was a US farm (EXIF: DJI, 43°59′N 92°04′W) captioned as a PM-KUSUM Component B field asset | Removed. Slide 1 is now a native system schematic. No photo is attributed to India. |
| 2 | Slide 2 "Marathwada & Vidarbha" photo was a strawberry field with a US-style crate | Removed. Slide 2 uses a native energy chart. The only photo left (slide 6, tomatoes) is labelled "Illustrative image". |
| 3 | Cold-chain energy and carbon overstated: 180 batch-days × 17.7 kWh implied 360 t/yr for a 30 t/ha crop; 2.55 t CO₂e was a diesel-cooling credit smallholders cannot claim | **Model corrected.** Batches follow tonnage: 60/yr per 4-farm cluster = 1,062 kWh (26% of the host farm's surplus; 266 kWh per farm). Headline carbon 0.39 t CO₂e/ha/yr; diesel scenario (+0.21 t) documented, not claimed. |
| 4 | "4,137 kWh captured" on slides 1 and 10 | Relabelled "idle solar unlocked". Also fixed the framing: 4,137 kWh (63%) is idle **after** water is right-sized; today under flood irrigation 2,442 kWh (37%) is idle. |
| 5 | "Payback in 2 crop harvests" vs "2.0 years" | "2.0 years (4 harvests at 2 cycles/yr)". Controller payback also fixed: 1.5 years = 3 crop seasons (was "1.5 crop seasons"). Combined cooler + controller ≈1.9 years added to the model. |
| 6 | "28 Olympic pools" | Removed (7,000 m³ ≈ 2.8 pools). |
| 7 | "Fastify" backend | FastAPI. |
| 8 | Sahyadri FPO and Schneider EPC shown as partners | Slide 9 and notes: "proposed partners (not yet confirmed)". |
| 9 | Drip hardware missing from capex while 29.4 of 41.2 points of saving come from drip | Stated on slides 4 and 8 and in the footers: drip assumed already installed; attribution 5,000 m³ drip + 2,000 m³ entitlement cap. |
| 10 | "10.9 lakh Component B pumps" | ≈10.06 lakh installed by 31 Jan 2026 (13.3 lakh sanctioned); 10.9 lakh is the all-component figure. Flagged to confirm on the MNRE dashboard. |
| 11 | "Water table decline >2.5 m/yr in 31% of semi-arid units (CGWB 2023)" could not be verified | Replaced with CGWB 2023: 736 of 6,553 assessment units over-exploited. |
| 12 | NABCONS 8.37% | Source-checked: it is the farm-stage tomato loss (11.62% total). Kept; total added to slide 2. |
| 13 | PPTX/PDF image-only | **Native PPTX** (python-pptx): real text, 6 native charts, 1 native table, speaker notes on every slide, alt text on charts/images. **PDF exported by PowerPoint**: selectable text, fonts embedded, 0.5 MB. |
| 14 | Dead space, text ≈8 pt equivalent, slide 3 without flows | Re-laid out on a 13.33 × 7.5 in canvas. Slide 3 is now a three-lane **Data / Energy / Money** flow diagram (official deliverable 2). Slide 7 doubles as the UX artifact. |
| 15 | Stale numbers across README and research docs (42–64%, 2,555 kWh, +₹72,450, "<18 days", ₹3,480) | README, ledger (v2), product truth, impact-model doc, proposal, narrative, final report and conflicts register rewritten. Nine historical docs carry a "superseded figures" banner. |
| 16 | `PROPOSAL.md` is 4,963 words | `research/11_SUBMISSION/EXEC_SUMMARY_500W.md` (473 words) added for the portal. |
| 17 | `generate_deck.py` hard-coded a `D:\` path | Archived. New pipeline is `presentation/build/` (relative paths). |

## B. QA performed

- Rendered every slide in desktop PowerPoint 16.0 (`export_office.ps1`) and inspected all 10 PNGs; fixed title wrap (slide 1), label overlaps (slide 3), unreadable waterfall labels and tile collisions (slide 8), bar-label overflow (slide 5).
- `validate.py` from the pptx skill: **All validations PASSED**.
- python-pptx re-read: 10 slides, 16:9, notes 498–979 characters each.
- PDF: 10 pages, 960 × 540 pt, text layer on every page, fonts embedded (Calibri, Consolas, Nirmala UI).
- Text scan of deck and notes for retired figures (3,187 / 2.94 / 951 / 77% / Fastify / Olympic / 10.9): none.
- Viewer (`presentation.html`) tested over local HTTP.

## C. Limits to know about

- Body text in dense cards is 11.5–16 pt (captions and sources 10 pt). Slides 3, 5, 8 and 9 are the densest; the PDF reads well on screen, but a projector audience will want the slide notes.
- Rendered only in desktop PowerPoint. Fonts are Calibri/Consolas/Nirmala UI (standard with Office); other viewers may substitute.
- No photographs of Indian farms are used. If you add one, add an author credit and keep it off any claim about location.

## D. Needs a human before submitting

1. **Portal:** confirm the exact deadline time and the required file types/limits on the YouNoodle form.
2. **Team roster and roles** on slides 1 and 10.
3. **Marathi/Hindi text** on slide 7: native-speaker review.
4. **Citations to confirm:** IWMI "16–39%" study reference; MNRE installed-pump counts (10.06 lakh, 4.67 lakh).
5. **Electrical check (Power/VFD lead):** confirm the LC1D09BD contactor's DC voltage/utilisation-category rating at 350–600 V DC against the Schneider datasheet. Zero-current switching after the dead-band reduces arcing, but the datasheet rating governs.
6. **Design targets, not results:** 4.00% post-cooling loss, ₹12,000 price-timing gain, ~₹5,000/yr controller benefit, pilot exit gates.
7. **Partnerships:** Sahyadri FPO and Schneider's rural EPC channel remain proposals.
