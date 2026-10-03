# 06 AI Architecture, TinyML Pipelines & Agentic RAG

**Document Code:** ARCH-AI-06  
**Domain:** Edge Inference, Digital Twin Physics & Zero-Hallucination Generative Interfaces  

---

## 1. Multi-Tier AI Topology

The AgroStruxure AI architecture operates across two synchronized domains:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AGROSTRUXURE AI PIPELINE                        │
├────────────────────────────────────────────────────────────────────────┤
│ DOMAIN 1: CLOUD DETERMINISTIC AGENTIC RAG (Human Interface)            │
│ 1. User Voice/Text Query Ingested (Hindi, Marathi, English)            │
│ 2. Few-Shot Intent Classifier routes query to domain processor        │
│ 3. Deterministic Python Engine queries PostgreSQL / Time-Series DB     │
│ 4. Rigid Anti-Hallucination Context Block Assembled                   │
│ 5. Gemini 2.5 Flash / Quantized Ollama synthesizes natural speech      │
├────────────────────────────────────────────────────────────────────────┤
│ DOMAIN 2: EDGE PHYSICS & TINYML ENGINE (Microcontroller Actuation)     │
│ 1. FAO-56 Penman-Monteith ET0 Calculation (Hourly)                    │
│ 2. Richards' Equation Approximation for Infiltration Depth             │
│ 3. Quantized GRU Neural Net: Soil Moisture Depletion (t+24h)           │
│ 4. Motor Current Harmonic Autoencoder: Cavitation / Dry-Run Detection  │
│ 5. Dynamic Switching Heuristic: Solar Energy Routing                   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. TinyML Edge Models & Mathematical Formulations

### Algorithm 1: Dynamic Evapotranspiration ($ET_0$) Calculation on Edge:
Because internet connectivity can drop, the edge gateway computes daily $ET_0$ locally using the FAO-56 equation with locally sensed temperature ($T$), relative humidity ($RH$), and solar radiation ($R_n$ measured via a miniature calibrated photodiode on the PV array):

$$e_s = 0.6108 \exp\left(\frac{17.27 T}{T + 237.3}\right)$$
$$e_a = e_s \times \frac{RH}{100}$$
$$\Delta = \frac{4098 \times e_s}{(T + 237.3)^2}$$
$$ET_0 = \frac{0.408 \Delta R_n + \gamma \frac{900}{T + 273} u_2 (e_s - e_a)}{\Delta + \gamma(1 + 0.34 u_2)}$$

### Algorithm 2: Dynamic Load Switching State Machine:
```python
def evaluate_load_routing(soil_moist_root, field_capacity, raw_threshold, solar_kw, cold_room_temp):
    """
    Evaluates microgrid power routing between pump motor and micro-cold storage.
    Runs every 30 seconds on ESP32-S3 edge gateway.
    """
    # Safety Check: Prevent pump dry-run or over-pressurization
    if soil_moist_root < raw_threshold:
        # Soil is depleted; priority is irrigation
        target_load = "IRRIGATION_PUMP"
        valve_state = "OPEN"
        vfd_speed_hz = calculate_optimal_mppt_hz(solar_kw)
    elif soil_moist_root >= field_capacity:
        # Root zone reached field capacity; CUT OFF WATER TO PREVENT REBOUND EFFECT
        valve_state = "CLOSED"
        if solar_kw > 1.2:
            # Sufficient surplus solar generation: route to farm-gate cold room
            target_load = "COLD_ROOM_COMPRESSOR"
            vfd_speed_hz = 50.0  # Run cold storage compressor at rated frequency
        else:
            target_load = "STANDBY"
            vfd_speed_hz = 0.0
    else:
        # In buffer zone; maintain current state to avoid relay fluttering
        target_load = "MAINTAIN_CURRENT"
        valve_state = "HOLD"
        vfd_speed_hz = None

    return target_load, valve_state, vfd_speed_hz
```

---

## 3. Deterministic Agentic RAG Pipeline

Evolved from the proven architecture in `My Old Work`, the Generative AI component does **not** make mathematical or irrigation decisions. It operates as an empathetic, natural multilingual communicator:

```python
# System prompt contract guaranteeing zero-hallucination execution
AGROSTRUXURE_PROMPT_CONTRACT = """
You are 'AgroStruxure Sahayak', a trusted agricultural engineer speaking with an Indian farmer.
You have been provided with deterministic real-time data from their field sensors and Schneider Altivar drive:
- Plot Crop: {crop_name} (Day {crop_age_days} of season)
- Root Zone Soil Moisture: {moisture_pct}% (Field Capacity: {fc_pct}%, Stress Threshold: {raw_pct}%)
- Pumping Status: {pump_status} (Today's Water Delivered: {water_litres} Litres)
- Solar Surplus Diverted: {diverted_kwh} kWh
- Cold Room Status: {cold_room_temp}°C ({crates_stored} crates of produce safely chilled)

STRICT RULES:
1. Speak in warm, respectful, colloquial {language} (Hindi, Marathi, or English).
2. Report the EXACT numbers given above. Never guess or modify water or energy values.
3. If the farmer asks to run the pump when soil moisture is already at Field Capacity, gently explain that over-watering suffocates roots and that their free solar power is currently saving their harvested crops in cold storage instead.
"""
```
