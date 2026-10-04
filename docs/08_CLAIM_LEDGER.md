# 08 Claim Ledger: Quantitative Single Source of Truth
**Document ID:** CLAIM-LEDGER-2026-V4 (engineering-precision update, 2026-10-03)
**Title:** AgroStruxure: An Agricultural Energy Orchestration Platform for Schneider Solar Infrastructure
**Core invention:** Dynamically reallocating surplus solar generation from irrigation to farm-gate thermal storage.
**Framing:** a strategic OEM skid and software proposal to Schneider Electric India, an extension of EcoStruxure (Connected Products → Edge Control → Cloud Apps & Analytics).
**Engine:** `research/08_IMPACT/impact_model.py` (reference unit: 1 ha tomato, Nashik, 4.8 kWp PM-KUSUM Component B pump, 2 cycles/yr)
**Deck:** `AgroStruxure_YuvaYodha_2026_Final.pptx` (repo root; slide numbers below refer to it; the deck still carries the earlier wording, see §6)

Status tags: `[MODEL]` reproduces from `impact_model.py` (arithmetic only) · `[ASSUMPTION]` input chosen by the team, not a measurement · `[SOURCE-CHECKED]` external figure confirmed against a public source on 2026-10-03 · `[TO CONFIRM]` quoted as reported or supplied; confirm before relying on it.

## 1. Reduced irrigation demand and pumping energy

| Claim | Number | Unit | Derivation | Status | Slide |
|---|---|---|---|:---:|:---:|
| Modelled irrigation water application, flood baseline | 17,000 | m³/ha/yr | 850 mm/season × 10 × 2 seasons | `[ASSUMPTION]` | 2, 4 |
| Modelled irrigation water application, entitlement-scheduled drip | 10,000 | m³/ha/yr | ETc 450 mm ÷ 0.90 efficiency = 500 mm × 10 × 2 | `[MODEL]` | 4 |
| **Reduced Irrigation Demand** | **7,000 (41.2% reduction in modelled irrigation water application)** | m³/ha/yr | 17,000 − 10,000 | `[MODEL]` | 1, 4, 10 |
| of which drip hardware | 5,000 (29.4 pts) | m³/ha/yr | conventional drip at 600 mm vs flood | `[MODEL]` | 4 |
| of which entitlement cap (the kit) | 2,000 (11.8 pts) | m³/ha/yr | 600 mm → 500 mm | `[MODEL]` | 4 |
| Pumping energy, flood / right-sized | 4,118 / 2,422 | kWh/ha/yr | 0.242 kWh/m³ (40 m head, 45% wire-to-water) | `[MODEL]` | 2, 4 |
| Pumping energy freed | 1,696 | kWh/ha/yr | 4,118 − 2,422 | `[MODEL]` | 4 |

Irrigation is scheduled according to crop water requirement and soil moisture telemetry, while PV generation continues through midday. The figures above are a **modelled reduction in irrigation water application**, not measured aquifer recovery; whether it becomes recovery depends on governance (entitlement cap, no area expansion). Drip is assumed already installed (existing or subsidised) and is **not** in the capex. The ₹7,540 kit is credited only with the 2,000 m³ entitlement-cap share.

## 2. Solar energy (host-farm array)

| Claim | Number | Unit | Derivation | Status | Slide |
|---|---|---|---|:---:|:---:|
| PV generation | 6,559 | kWh/yr | 4.8 kWp × 4.8 peak-sun-h × 365 × 0.78 PR (= 3.74 effective h/day) | `[ASSUMPTION]` | 1, 2, 5 |
| **Three-step energy balance** | **6,559 PV → 2,422 pumping → 1,062 pre-cooling → 3,075 (46.9%) unallocated headroom** | kWh/yr | 6,559 − 2,422 − 1,062 = 3,075 | `[MODEL]` | 3, 5 |
| Baseline idle PV (flood pumping) | 2,442 (37%) | kWh/yr | 6,559 − 4,118; idle today, before any water saving | `[MODEL]` | 2 |
| Modelled surplus once irrigation is right-sized | 4,137 (63.1%) | kWh/yr | 6,559 − 2,422 = idle today + 1,696 freed | `[MODEL]` | 1, 2, 10 |
| Pre-cooler demand (4-farm cluster) | 1,062 | kWh/yr | 60 batches (4 farms × 30 t ÷ 2 MT) × (13.7 pull-down + 4.0 hold) kWh | `[MODEL]` | 1, 3, 5 |
| Pre-cooler share of baseline idle PV | 43% | % | 1,062 ÷ 2,442: the cooler does not depend on irrigation savings | `[MODEL]` | 5 |
| Pre-cooler share of right-sized surplus | 26% | % | 1,062 ÷ 4,137 | `[MODEL]` | 5 |
| Energy margin once right-sized | ≈3.9× (≈4×) | ratio | 4,137 ÷ 1,062 | `[MODEL]` | notes |
| **Unallocated headroom** | **3,075 (46.9% of PV)** | kWh/yr | 4,137 − 1,062; future loads or grid feed-in; not counted as a benefit | `[MODEL]` | 3, 5 |
| Per-farm equivalent | 266 | kWh/yr | 1,062 ÷ 4 | `[MODEL]` | 5 |
| Pre-cooler batch energy | 13.7 el / 41.1 th | kWh | 2,000 kg × 3.7 kJ/kg·K × 20 K ÷ 3,600; COP 3.0 | `[ASSUMPTION]` | 5, 6 |
| Pre-cooler power | 3.43 | kW for 4 h | 13.7 kWh ÷ 4 h; fits the 4.8 kWp array | `[MODEL]` | 5 |
| Room utilisation | 33% | % | 120 t/yr of 360 t/yr capacity | `[MODEL]` | notes |

*Limit:* rows above are annual energy balances. The cooler needs 3.43 kW for about 4 h at midday on harvest days, so coincident use depends on harvest-day scheduling (the controller lets the pump yield). Confirm the overlap in AgroSim and on the Phase 2 HIL bench.

*Opportunity framing:* 4,137 kWh/yr modelled surplus (63.1%) in our 4.8 kWp reference system; the Component B installed base provides the target deployment opportunity (§5). No fleet-wide energy figure is claimed.

## 3. Phase-change store: specification, sizing, and why not a battery

| Claim | Number | Unit | Derivation | Status | Slide |
|---|---|---|---|:---:|:---:|
| PCM type (design target) | Encapsulated salt hydrate; melt point 12–15 °C; latent heat 190–210 kJ/kg | n/a | design target; confirm vendor datasheet. Melt point should sit at the low end (≈12 °C) so the store holds the room near the 12 °C setpoint | `[ASSUMPTION]` `[TO CONFIRM]` | none |
| PCM mass to carry the overnight hold | ≈216 (206–227) | kg | 4.0 kWh el × COP 3.0 = 12 kWh th = 43,200 kJ ÷ 200 kJ/kg (÷ 210 to ÷ 190) | `[MODEL]` on `[ASSUMPTION]` | none |
| PCM design life | 10 years in 45 °C ambient | years | design target; confirm vendor rated freeze–thaw cycles, supercooling and phase separation | `[ASSUMPTION]` `[TO CONFIRM]` | none |
| Energy per batch-day | 17.7 | kWh el | 13.7 pull-down + 4.0 overnight hold | `[MODEL]` | notes |
| Battery to carry a full batch-day | ≈22 | kWh nominal | 17.7 ÷ 0.80 depth of discharge | `[MODEL]` on `[ASSUMPTION]` | none |
| Battery to carry the overnight hold only | ≈5 | kWh nominal | 4.0 ÷ 0.80 | `[MODEL]` on `[ASSUMPTION]` | none |
| Battery installed cost | ₹10,000–20,000 | ₹/kWh | indicative; get quotes | `[ASSUMPTION]` | none |
| Battery capex, full batch-day | ₹2.2–4.4 lakh (₹55,000–110,000 per farm ÷ 4) | ₹ | 22 kWh × cost range, before inverter, charge electronics and replacement | `[MODEL]` on `[ASSUMPTION]` | none |
| Battery capex, hold only | ₹0.5–1.0 lakh (₹12,500–25,000 per farm ÷ 4) | ₹ | 5 kWh × cost range | `[MODEL]` on `[ASSUMPTION]` | none |
| Value of surplus used for cooling, **base case** | ≈₹59 gross, ₹50 net of opex | ₹/kWh | (₹15,732 × 4) ÷ 1,062; (₹13,332 × 4) ÷ 1,062; physical loss reduction only | `[MODEL]` | none |
| Value of surplus used for cooling, price-timing scenario | ≈₹104 gross, ₹95 net of opex | ₹/kWh | (₹27,732 × 4) ÷ 1,062; (₹25,332 × 4) ÷ 1,062 | `[MODEL]` | none |
| Value of generic use or export | ₹3–5 | ₹/kWh | indicative tariff | `[ASSUMPTION]` `[TO CONFIRM]` | none |

The PCM plates are part of the ₹400,000 cooler (compressor + PCM) shared by four farms, i.e. ₹50,212 per farm after subsidy. No separate PCM price is claimed. Small LiFePO₄ cells remain in field sensor nodes; the comparison is about bulk energy storage.

## 4. Post-harvest, carbon, money, modularity

The financial return is based **strictly on physical produce-loss reduction**. Price-timing arbitrage is an **optional scenario** and is not in the base case.

| Claim | Number | Unit | Derivation | Status | Slide |
|---|---|---|---|:---:|:---:|
| Tomato farm-stage loss (baseline) | 8.37% | % | NABCONS 2022 for MoFPI (total 11.62% incl. 3.25% market handling) | `[SOURCE-CHECKED]` | 2, 6 |
| Loss with pre-cooling | 4.00% | % | design target, not a measurement | `[ASSUMPTION]` | 6 |
| Produce preserved | 1.31 | t/ha/yr | 30 t × (8.37% − 4.00%) = 1,311 kg | `[MODEL]` | 1, 6, 10 |
| **Spoilage value (base-case return)** | **₹15,732** (≈₹15,720 at the rounded 1.31 t) | ₹/ha/yr | 1,311 kg × ₹12/kg | `[ASSUMPTION]` price | 6, 8 |
| **Net farmer gain, base case** | **₹13,332** | ₹/farm/yr | 15,732 − 2,400 opex | `[MODEL]` | none |
| **Cluster add-on payback, base case** | **3.8 years (≈7.5 harvests; 5.8 unsubsidised)** | years | 50,212 ÷ 13,332 | `[MODEL]` | none |
| Optional scenario: price-timing arbitrage | +₹12,000 | ₹/ha/yr | +₹1–2/kg on 8 t; price-volatile | `[ASSUMPTION]` | 6, 8 |
| Net farmer gain, scenario with timing | ₹25,332 | ₹/farm/yr | 13,332 + 12,000 | `[MODEL]` | 3, 6, 8 |
| Cluster add-on payback, scenario with timing | 2.0 years (4 harvests; 3.0 unsubsidised) | years | 50,212 ÷ 25,332 | `[MODEL]` | 1, 3, 8, 10 |
| Embodied emissions avoided (headline) | 0.39 | t CO₂e/ha/yr | 1.31 t × 0.30 kg CO₂e/kg | `[ASSUMPTION]` factor | 6, 10 |
| Scenario only: diesel-cooling displacement | +0.21 | t CO₂e/ha/yr | 266 kWh × 0.80 kg/kWh. **Not claimed:** smallholders have no cooling today | `[ASSUMPTION]` | none |
| **Standalone kit** BoM | ₹7,540 | ₹/unit | 11-line BoM, 1,000 units; works on any PM-KUSUM pump | `[ASSUMPTION]` | 8 |
| Standalone kit payback | 1.5 | years (= 3 crop seasons) | 7,540 ÷ ~5,000/yr pump and yield protection. Reduced irrigation demand has no farm-gate cash value under free solar power and is not counted | `[ASSUMPTION]` benefit | 8 |
| **Cluster add-on** net capex | ₹50,212 | ₹/farm | (₹400,000 − ₹91,000) × 0.65 ÷ 4; shared 2 MT PCM unit, 35% MIDH/AIF | `[MODEL]` | 1, 3, 8 |
| Combined kit + add-on payback | base 3.2 years; scenario ≈1.9 years | years | (50,212 + 7,540) ÷ (13,332 + 5,000); ÷ (25,332 + 5,000) | `[MODEL]` | 8 |
| Tier B hub payback | 4.2 | years | ₹780,000 ÷ ₹184,375 (storage fees; unaffected by the timing scenario) | `[MODEL]` | 8 |

The cooler add-on suits horticulture clusters. Tomato is modelled; chili and leafy greens need their own setpoints and are not modelled. Non-perishable crops (wheat, cotton) need only the standalone kit.

## 5. External context, status, load portfolio and partners

| Claim | Value | Source | Status |
|---|---|---|:---:|
| Over-exploited assessment units | 736 of 6,553 | CGWB National Compilation on Dynamic Ground Water Resources 2023 | `[SOURCE-CHECKED]` |
| Solarisation raised extraction | 16–39% | IWMI-reported research study, Rajasthan | `[TO CONFIRM]` exact citation |
| **Component B installed base (target deployment opportunity)** | **816,710 pumps as of Aug 2026 (MNRE)** | supplied by the team | `[TO CONFIRM]` on the MNRE dashboard. The deck, `EXEC_SUMMARY_500W.md` and earlier notes quote ≈10.06 lakh (31 Jan 2026, secondary source); the two figures conflict and must be reconciled before submission |
| Schneider's own share of the installed fleet | not documented | none | unknown |
| **Load portfolio: CURRENT PROTOTYPE** | Solar pumping + soil/water control + PCM cooling | team | prototype scope: simulated in Phase 1, hardware bench in Phase 2; no field hardware |
| **Load portfolio: EXPANSION ROADMAP** | Crop drying + packhouse sorting + dairy chilling + water treatment | team | not modelled; no energy or revenue figure is claimed |
| **Partnership status** | **Schneider Electric rural EPC channel and Sahyadri Farmers Producer Co. are PROPOSED partners only. No signed agreement exists.** | team | disclaimer |
| **Development status** | **Phase 1 completed:** code (`impact_model.py`), math model, AgroSim (team-reported; AgroSim source is not in this repository, link it before submission). **Phase 2 prototype:** hardware-in-the-loop (HIL) test bench with Altivar ATV320 and TeSys D. No field data. | team | disclaimer |

## 6. Deck and summary alignment (open)

`AgroStruxure_YuvaYodha_2026_Final.pptx` and `research/11_SUBMISSION/EXEC_SUMMARY_500W.md` still use the earlier wording: "less groundwater", "5 s dead-band" on main slides, ₹25,332 / 2.0-year payback as the headline, ≈10.06 lakh pumps. They should be aligned to §1, §4 and §5 above before submission.

Removed from the docs as unverified, wrong or too strong: "10.9 lakh Component B pumps" (that figure covers all components), "1.1 million" pumps, "water table decline > 2.5 m/yr in 31% of semi-arid units", "28 Olympic pools" (7,000 m³ ≈ 2.8 pools), "pump run-time 1,373 → 807 h", "Sahyadri FPO / Schneider EPC partnership" (proposed only), "2.94 t CO₂e/ha/yr", "3,187 kWh captured / 77%", "groundwater saved / conserved" and "aquifer protection" (replaced by Reduced Irrigation Demand), price-timing gains inside the base-case return, and any statement that the ₹7,540 kit alone delivers the full 7,000 m³ reduction.
