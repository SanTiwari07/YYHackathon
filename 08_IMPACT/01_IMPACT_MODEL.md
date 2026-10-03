# 01 Quantified Impact Model & Baseline Derivations

**Document Code:** IMP-MODEL-01  
**Evaluation Pillar Target:** Impact & Measurability (25% Judging Weight)  
**Verification Baseline:** Grounded in Official Indian Statistics (CGWB 2023, NABCONS 2022, CEA, NIWE)  
**Executable Python Reference:** `impact_model.py` (Run `python impact_model.py` to reproduce all figures)

---

## 1. Single Source of Truth Impact Matrix

All figures are modeled for a reference **1-hectare tomato farm in Nashik district, Maharashtra** (2 cycles/year, 120 days/cycle, 5 HP Component B pump, 4.8 kWp solar PV array):

```
========================================================================================
                               SINGLE SOURCE OF TRUTH MATRIX
========================================================================================
Metric Parameter                     Baseline               AgroStruxure           Net Impact
----------------------------------------------------------------------------------------
Water Extraction (per season)        8,500 m³/ha (850 mm)   5,000 m³/ha (500 mm)   3,500 m³ saved (41.2%)
Water Extraction (annual, 2 cycles) 17,000 m³/ha/yr         10,000 m³/ha/yr         7,000 m³/ha/yr saved
Specific Pumping Energy (@ 40m head) 0.242 kWh/m³           0.242 kWh/m³           45% wire-to-water eff.
Annual Solar PV Generation (4.8kWp)  6,559 kWh/year         6,559 kWh/year         4.8 PSH/day, PR 0.78
Pumping Electricity Consumed         4,118 kWh/year         2,422 kWh/year         1,696 kWh/yr freed
Daytime PV Surplus (Idle Today)      4,137 kWh/year (63%)   3,187 kWh/yr routed    77% surplus utilized
Residual Uncaptured Surplus          0 kWh                  951 kWh/year (23%)     Transparently stated
Post-Harvest Loss (Farm Stage)       8.37% (2.51 t/ha/yr)   4.00% (1.20 t/ha/yr)   1.31 t/ha/yr preserved
Direct Economic Spoilage Saved       Baseline loss          ₹15,732 / ha / year    @ ₹12/kg farm-gate
Distress-Sale Avoidance (Price timing)Baseline distress      ₹12,000 / ha / year    Holding 2–4 days
GHG Emissions Abated (per year)      Baseline genset/loss   2.94 t CO₂e / ha / yr  Cooling (2.55) + Food (0.39)
Edge Controller BOM (1,000 units)    Disjointed systems     ₹7,540                 Complete industrial BOM
Shared-Array PV Capex Avoided        ₹91,000 (own 2.6kWp)   ₹0 (shared pump PV)    -₹91,000 capex saving
Tier A Pre-Cooler Payback (4 farms)  Commercial cold        2.0 Years (2 seasons)  Post-subsidy (3.0 yr pre)
Tier B FPO Holding Room Payback      Commercial cold        4.2 Years              Post-subsidy (6.5 yr pre)
========================================================================================
```

---

## 2. Mathematical Impact Formulations & Derivations

### A. Water Conservation & Attribution Breakdown:
Under status quo flood irrigation, the gross irrigation water depth applied per crop cycle ($D_{flood}$) for tomato in Maharashtra is:

$$D_{flood} = 850\text{ mm} \equiv 8,500\text{ m}^3/\text{ha / season}$$

Under AgroStruxure's closed-loop precision pulsed drip irrigation:

$$D_{Agro} = \frac{ET_c}{\eta_{drip}} = \frac{450\text{ mm}}{0.90} = 500.0\text{ mm} \equiv 5,000.0\text{ m}^3/\text{ha / season}$$

$$\Delta W_{saved} = D_{flood} - D_{Agro} = 8,500 - 5,000 = \mathbf{3,500.0\text{ m}^3/\text{ha / season}} \quad (\mathbf{41.2\% \text{ reduction}})$$
$$\Delta W_{annual} = 3,500 \times 2 = \mathbf{7,000.0\text{ m}^3/\text{ha / year}}$$

#### Honest Attribution Breakdown (per season):
1. **Hardware Shift (Flood to Standard Drip):** Saves $8,500 - 6,000 = 2,500\text{ m}^3$ (**29.4%** of baseline).
2. **AgroStruxure Closed-Loop Entitlement Scheduling:** Saves $6,000 - 5,000 = 1,000\text{ m}^3$ (**11.8%** of baseline).
3. **The Governance Lock:** Without Layer 3 entitlement enforcement, the 3,500 m³ saved is re-extracted to irrigate an extra acre (Jevons Paradox, documented by Gupta 2019 in Rajasthan at 16–39% extraction surge). AgroStruxure locks this water in the ground by converting it into cold-chain credits.

---

### B. Energy Savings & Solar Surplus Derivation:
Specific Energy Consumption ($SEC$) to pump $1\text{ m}^3$ of water over a dynamic head $H = 40\text{ meters}$ with wire-to-water efficiency $\eta = 45\%$:

$$SEC = \frac{\rho \cdot g \cdot H}{3.6 \times 10^6 \times \eta_{system}} = \frac{1000 \times 9.81 \times 40}{3.6 \times 10^6 \times 0.45} = \mathbf{0.242\text{ kWh / m}^3}$$

1. **Pumping Energy Freed:**
   $$E_{freed} = \Delta W_{annual} \times SEC = 7,000\text{ m}^3 \times 0.242\text{ kWh/m}^3 = \mathbf{1,696\text{ kWh / ha / year}}$$

2. **Solar PV Surplus Today (Idle Wastage):**
   - 4.8 kWp array generates $4.8 \times 4.8\text{ PSH} \times 365 \times 0.78 = \mathbf{6,559\text{ kWh / year}}$.
   - Scheduled pumping consumes $10,000\text{ m}^3 \times 0.242 = 2,422\text{ kWh / year}$.
   - **Idle Solar Surplus Today:** $6,559 - 2,422 = \mathbf{4,137\text{ kWh / year}}$ (**63.1% of generation sits idle**, matching Shah et al. 2016).

3. **Surplus Put to Work (2 MT PCM Farm Pre-Cooler):**
   - Pull-down of 2 MT tomato from 32 °C to 12 °C safe setpoint: $Q_{th} = 2000 \times 3.7 \times 20 / 3600 = 41.1\text{ kWh}_{th}$.
   - Electrical demand @ COP 3.0: $41.1 / 3.0 = 13.7\text{ kWh}_{el}$. Over 4-hour diversion window: **3.43 kW** (fits inside 4.8 kWp array).
   - Daily energy (pull-down 13.7 kWh + hold 4.0 kWh): $17.7\text{ kWh/day}$.
   - Operating over 180 cold-chain days/year: $17.7 \times 180 = \mathbf{3,187\text{ kWh / year}}$ captured (**77% of surplus utilized**).
   - **Residual Uncaptured Surplus:** $4,137 - 3,187 = \mathbf{951\text{ kWh / year (23\%)}}$, transparently acknowledged.

---

### C. Post-Harvest Produce Preservation & Economics:
- **Baseline Farm-Stage Loss:** **8.37%** for tomatoes (NABCONS 2022 MoFPI study; supersedes ICAR-CIPHET 2015).
- On 30 t/ha/year yield (15 t/cycle × 2 cycles): baseline loss = $2.51\text{ t/ha/year}$.
- Residual loss with on-farm pre-cooling to 12 °C: **4.00%** ($1.20\text{ t/ha/year}$).
- **Produce Preserved:** $2.51 - 1.20 = \mathbf{1.31\text{ tonnes / ha / year}}$.
- Direct Economic Value (@ conservative farm-gate ₹12/kg): $1.31 \times 12,000 = \mathbf{₹15,732 / \text{ha / year}}$.
- Distress-Sale Avoidance (holding 2–4 days for mandi price stabilization): $\mathbf{₹12,000 / \text{ha / year}}$.

---

### D. Greenhouse Gas (GHG) Abatement:
- Solar cooling displacing diesel genset ($3,187\text{ kWh} \times 0.80\text{ kg CO}_2\text{e/kWh}$): $2.55\text{ t CO}_2\text{e/year}$.
- Embodied emissions in avoided tomato spoilage ($1.31\text{ t} \times 0.30\text{ kg CO}_2\text{e/kg}$): $0.39\text{ t CO}_2\text{e/year}$.
- **Total Carbon Mitigated:** $\mathbf{2.94\text{ tonnes CO}_2\text{e / ha / year}}$.
