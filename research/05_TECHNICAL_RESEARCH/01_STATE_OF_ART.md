# 01 Technical State of the Art: Academic & Industrial SOTA

**Document Code:** TECH-SOTA-01  
**Domain:** Agronomic Physics, Evapotranspiration, Edge AI, Power Electronics & Digital Twins  

---

## 1. The Physics Backbone: FAO-56 Penman-Monteith Evapotranspiration

The universal standard for quantifying crop water demand is the **FAO-56 Penman-Monteith equation** (Food and Agriculture Organization Irrigation and Drainage Paper No. 56). It calculates the **Reference Evapotranspiration ($ET_0$)** in $\text{mm/day}$ from an idealized grass reference crop:

$$ET_0 = \frac{0.408 \Delta (R_n - G) + \gamma \frac{900}{T + 273} u_2 (e_s - e_a)}{\Delta + \gamma (1 + 0.34 u_2)}$$

### Parameter Definitions:
* $R_n$: Net radiation at the crop surface ($\text{MJ } \text{m}^{-2} \text{ day}^{-1}$).
* $G$: Soil heat flux density ($\text{MJ } \text{m}^{-2} \text{ day}^{-1}$), negligible for daily calculations ($G \approx 0$).
* $T$: Mean daily air temperature at 2m height ($^\circ\text{C}$).
* $u_2$: Wind speed at 2m height ($\text{m } \text{s}^{-1}$).
* $e_s$: Saturation vapour pressure ($\text{kPa}$).
* $e_a$: Actual vapour pressure ($\text{kPa}$), derived from relative humidity $RH$.
* $e_s - e_a$: Saturation vapour pressure deficit (VPD in $\text{kPa}$).
* $\Delta$: Slope of the vapour pressure curve ($\text{kPa } ^\circ\text{C}^{-1}$).
* $\gamma$: Psychrometric constant ($\approx 0.067 \text{ kPa } ^\circ\text{C}^{-1}$ at sea level).

### Dynamic Crop Evapotranspiration ($ET_c$):
To determine the actual water consumption of a specific crop at a specific phenological growth stage, $ET_0$ is scaled by the empirical **crop coefficient ($K_c$)**:

$$ET_c = K_c \times ET_0$$

```
   Crop Coefficient (Kc) Curve Over Growth Season
   Kc
   ▲
1.2│                     ┌──────────────┐
1.0│                    /                \
0.8│                   /                  \
0.6│                  /                    \
0.4│  ───────────────┘                      └────────
   └──────────────────────────────────────────────────► Time (Days)
       Initial Stage    Development    Mid-Season  Late Season
       (Germination)      (Rapid)     (Flowering)  (Maturity)
```

---

## 2. Soil Moisture Dynamics & Water Balance Model

Soil functions as a natural water reservoir. The available water capacity is bounded by two critical thresholds:

1. **Field Capacity ($\theta_{FC}$):** The volumetric water content retained after excess gravitational water has drained away (typically 24–48 hours after saturating rain or irrigation).
2. **Permanent Wilting Point ($\theta_{PWP}$):** The minimum soil moisture at which plant roots can no longer extract water against soil matric suction, leading to irreversible wilting.
3. **Total Available Water ($TAW$):**
   $$TAW = 1000 \times (\theta_{FC} - \theta_{PWP}) \times Z_r$$
   Where $Z_r$ is the effective crop rooting depth in meters.
4. **Readily Available Water ($RAW$):** The portion of $TAW$ that a crop can extract without suffering water stress:
   $$RAW = p \times TAW$$
   Where $p$ is the soil water depletion fraction (typically $0.4$ to $0.6$ depending on crop drought sensitivity).

### The Trigger Rule:
Irrigation is triggered if and only if root-zone soil water depletion $D_r$ exceeds $RAW$:
$$\text{Trigger Condition: } D_r \ge RAW$$
The target irrigation volume $V_{irr}$ required to restore root zone to field capacity is:
$$V_{irr} = \frac{D_r \times A_{field}}{\eta_{irr}}$$
Where $\eta_{irr}$ is the irrigation application efficiency ($0.90$ for drip; $0.35$ for flood).

---

## 3. TinyML & Edge Intelligence on Microcontrollers

Running machine learning models on resource-constrained microcontrollers (e.g., ESP32, STM32, ARM Cortex-M4) enables zero-latency closed-loop decision making in offline rural environments:

```
┌───────────────────────────┬───────────────────────────┬───────────────────────────┐
│ TinyML Model              │ Algorithmic Backbone      │ Operational Role at Edge  │
├───────────────────────────┼───────────────────────────┼───────────────────────────┤
│ 1. Soil Moisture          │ 1D CNN / Quantized        │ Forecasts root moisture   │
│    Trajectory Predictor   │ LSTM (TensorFlow Lite)    │ depletion over next 24h   │
├───────────────────────────┼───────────────────────────┼───────────────────────────┤
│ 2. Pump Anomaly Detector  │ Autoencoder / Isolation   │ Analyzes 3-phase current  │
│    (Predictive Maint.)    │ Forest on RMS Current     │ & vibration for dry-run   │
├───────────────────────────┼───────────────────────────┼───────────────────────────┤
│ 3. Solar MPPT Frequency   │ Regression Tree / Tiny    │ Maps PV voltage curve to  │
│    Governor               │ Gradient Boosted Decision │ optimal motor speed ($Hz$)│
└───────────────────────────┴───────────────────────────┴───────────────────────────┘
```

---

## 4. Solar Pumping Power Electronics & Motor Hydraulics

The mechanical hydraulic power $P_{hyd}$ required to lift a flow rate $Q$ ($\text{m}^3/\text{s}$) over a total dynamic head $H$ ($\text{m}$) is governed by:

$$P_{hyd} = \rho \cdot g \cdot H \cdot Q$$

Where:
* $\rho = 1000 \text{ kg/m}^3$ (density of water).
* $g = 9.81 \text{ m/s}^2$ (acceleration due to gravity).
* Electrical input power $P_{elec} = \frac{P_{hyd}}{\eta_{pump} \times \eta_{motor} \times \eta_{VFD}}$.

### Affinity Laws for Variable Speed Centrifugal Pumps:
When a Schneider Altivar VFD modulates motor frequency $f$ from $50\text{ Hz}$ down to $35\text{ Hz}$ under passing clouds:
1. Flow rate varies linearly: $\frac{Q_1}{Q_2} = \frac{f_1}{f_2}$
2. Head varies quadratically: $\frac{H_1}{H_2} = \left(\frac{f_1}{f_2}\right)^2$
3. Power consumption varies cubically: $\frac{P_1}{P_2} = \left(\frac{f_1}{f_2}\right)^3$

* `[CRITICAL INSIGHT]` A 20% reduction in pump speed reduces power consumption by nearly **49%** ($0.8^3 = 0.512$). This allows solar pumps to maintain continuous, stable irrigation during overcast or low-radiation mornings rather than violently tripping on/off!
