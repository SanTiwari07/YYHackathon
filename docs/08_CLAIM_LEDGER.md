# 08 Claim Ledger: Quantitative Single Source of Truth
**Document ID:** CLAIM-LEDGER-2026-V2 (corrected 2026-10-03)
**Engine:** `research/08_IMPACT/impact_model.py` (reference unit: 1 ha tomato, Nashik, 4.8 kWp PM-KUSUM Component B pump, 2 cycles/yr)
**Deck:** `AgroStruxure_YuvaYodha_2026_Final.pptx` (repo root) (slide numbers below refer to it)

Status tags: `[MODEL]` reproduces from `impact_model.py` (arithmetic only) · `[ASSUMPTION]` input chosen by the team, not a measurement ·
`[SOURCE-CHECKED]` external figure confirmed against a public source on 2026-10-03 · `[TO CONFIRM]` quoted as reported; confirm before relying on it.

## 1. Water and pumping energy

| Claim | Number | Unit | Derivation | Status | Slide |
|---|---|---|---|:---:|:---:|
| Baseline water (flood) | 17,000 | m³/ha/yr | 850 mm/season × 10 × 2 seasons | `[ASSUMPTION]` | 2, 4 |
| Entitlement water (drip) | 10,000 | m³/ha/yr | ETc 450 mm ÷ 0.90 efficiency = 500 mm × 10 × 2 | `[MODEL]` | 4 |
| Groundwater conserved | 7,000 (41.2%) | m³/ha/yr | 17,000 − 10,000 | `[MODEL]` | 1, 4, 10 |
| of which drip hardware | 5,000 (29.4 pts) | m³/ha/yr | conventional drip at 600 mm vs flood | `[MODEL]` | 4 |
| of which entitlement cap | 2,000 (11.8 pts) | m³/ha/yr | 600 mm → 500 mm | `[MODEL]` | 4 |
| Pumping energy, flood / right-sized | 4,118 / 2,422 | kWh/ha/yr | 0.242 kWh/m³ (40 m head, 45% wire-to-water) | `[MODEL]` | 2, 4 |
| Pumping energy freed | 1,696 | kWh/ha/yr | 4,118 − 2,422 | `[MODEL]` | 4 |

Water saving assumes drip is already installed (existing or subsidised); drip hardware is **not** in the capex.

## 2. Solar energy (host-farm array)

| Claim | Number | Unit | Derivation | Status | Slide |
|---|---|---|---|:---:|:---:|
| PV generation | 6,559 | kWh/yr | 4.8 kWp × 4.8 peak-sun-h × 365 × 0.78 PR (= 3.74 effective h/day) | `[ASSUMPTION]` | 1, 2, 5 |
| Idle PV today (flood pumping) | 2,442 (37%) | kWh/yr | 6,559 − 4,118 | `[MODEL]` | 2 |
| Idle PV once water is right-sized | 4,137 (63%) | kWh/yr | 6,559 − 2,422 = idle today + 1,696 freed | `[MODEL]` | 1, 2, 10 |
| Cluster cold-chain energy | 1,062 | kWh/yr | 60 batches (4 farms × 30 t ÷ 2 MT) × (13.7 pull-down + 4.0 hold) kWh | `[MODEL]` | 1, 3, 5 |
| Per-farm equivalent | 266 | kWh/yr | 1,062 ÷ 4 | `[MODEL]` | 5 |
| Share of host-farm surplus used | 26% | % | 1,062 ÷ 4,137 | `[MODEL]` | 5 |
| Headroom after cooling (not claimed) | 3,075 (47% of PV) | kWh/yr | 4,137 − 1,062 | `[MODEL]` | 3, 5 |
| Pre-cooler batch energy | 13.7 el / 41.1 th | kWh | 2,000 kg × 3.7 kJ/kg·K × 20 K ÷ 3,600; COP 3.0 | `[ASSUMPTION]` | 5, 6 |
| Room utilisation | 33% | % | 120 t/yr of 360 t/yr capacity | `[MODEL]` | notes |

*Correction (2026-10-03):* earlier versions multiplied one batch-day by 180 operating days (3,187 kWh, "77% captured"), which implied 360 t/yr through the room for one hectare that yields 30 t.

## 3. Post-harvest, carbon, money

| Claim | Number | Unit | Derivation | Status | Slide |
|---|---|---|---|:---:|:---:|
| Tomato farm-stage loss (baseline) | 8.37% | % | NABCONS 2022 for MoFPI (total 11.62% incl. 3.25% market handling) | `[SOURCE-CHECKED]` | 2, 6 |
| Loss with pre-cooling | 4.00% | % | design target, not a measurement | `[ASSUMPTION]` | 6 |
| Produce preserved | 1.31 | t/ha/yr | 30 t × (8.37% − 4.00%) | `[MODEL]` | 1, 6, 10 |
| Spoilage value | ₹15,732 | ₹/ha/yr | 1,311 kg × ₹12/kg | `[ASSUMPTION]` price | 6, 8 |
| Price-timing gain | ₹12,000 | ₹/ha/yr | +₹1–2/kg on 8 t | `[ASSUMPTION]` | 6, 8 |
| Net farmer gain | ₹25,332 | ₹/farm/yr | 15,732 + 12,000 − 2,400 opex | `[MODEL]` | 3, 6, 8 |
| Embodied emissions avoided (headline) | 0.39 | t CO₂e/ha/yr | 1.31 t × 0.30 kg CO₂e/kg | `[ASSUMPTION]` factor | 6, 10 |
| Scenario only: diesel-cooling displacement | +0.21 | t CO₂e/ha/yr | 266 kWh × 0.80 kg/kWh; not in headline | `[ASSUMPTION]` | none |
| Edge controller BoM | ₹7,540 | ₹/unit | 11-line BoM, 1,000 units | `[ASSUMPTION]` | 8 |
| Pre-cooler net capex per farm | ₹50,212 | ₹/farm | (₹400,000 − ₹91,000) × 0.65 ÷ 4 | `[MODEL]` | 1, 3, 8 |
| Tier A payback | 2.0 | years | 50,212 ÷ 25,332 (= 4 harvests; 3.0 yr without subsidy) | `[MODEL]` | 1, 3, 8, 10 |
| Controller payback | 1.5 | years | 7,540 ÷ ~5,000 (= 3 crop seasons) | `[ASSUMPTION]` benefit | 8 |
| Combined payback | ≈1.9 | years | (50,212 + 7,540) ÷ (25,332 + 5,000) | `[MODEL]` | 8 |
| Tier B hub payback | 4.2 | years | ₹780,000 ÷ ₹184,375 | `[MODEL]` | 8 |

## 4. External context (as shown on slides 2 and 9)

| Claim | Value | Source | Status |
|---|---|---|:---:|
| Over-exploited assessment units | 736 of 6,553 | CGWB National Compilation on Dynamic Ground Water Resources 2023 | `[SOURCE-CHECKED]` |
| Solarisation raised extraction | 16–39% | IWMI-reported research study, Rajasthan | `[TO CONFIRM]` exact citation |
| Component B pumps installed | ≈10.06 lakh (of 13.3 lakh sanctioned), 31 Jan 2026 | MNRE PM-KUSUM progress, as reported | `[TO CONFIRM]` on MNRE dashboard |
| Maharashtra installed | ≈4.67 lakh, 30 Nov 2025 | MNRE, as reported | `[TO CONFIRM]` |

Removed from the deck as unverified or wrong: "10.9 lakh Component B pumps" (the 10.9 lakh figure covers all components), "water table decline > 2.5 m/yr in 31% of semi-arid units", "28 Olympic pools" (7,000 m³ ≈ 2.8 pools), "pump run-time 1,373 → 807 h", "Sahyadri FPO / Schneider EPC partnership" (proposed only), "2.94 t CO₂e/ha/yr".
