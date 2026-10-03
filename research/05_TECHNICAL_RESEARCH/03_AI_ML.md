# 03 AI/ML Architecture, Digital Twins & Predictive Modeling

**Document Code:** TECH-AI-03  
**Domain:** Edge TinyML, Hybrid Physics-AI Modeling & Hallucination-Free RAG  

---

## 1. The Hybrid AI Philosophy: Physics-First, ML-Enhanced

In mission-critical agricultural and energy systems, purely black-box deep learning models fail because:
1. They lack physical boundary guarantees (e.g., an unconstrained neural network might predict negative soil moisture or demand infinite irrigation).
2. They cannot be explained to skeptical farmers or electrical safety inspectors.

Therefore, our architecture uses a **Physics-Informed Hybrid Architecture**:
* **The Physics Core:** Governed by deterministic thermodynamic and agronomic laws (FAO-56 Penman-Monteith, Richards' equation for unsaturated soil water flow, and Affinity Laws for centrifugal pumps).
* **The Machine Learning Layer:** Tunes empirical coefficients, compensates for unmeasured local microclimate anomalies, and detects equipment wear.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   HYBRID PHYSICS-INFORMED AI STACK                     │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 3: Deterministic Agronomic Physics (FAO-56 & Water Balance)       │
│ • Calculates ET0, RAW, TAW, and allowable soil depletion               │
│ • Guarantees that water quotas never violate crop biology              │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 2: Edge TinyML Inference (Microcontroller Level)                  │
│ • Model A: Soil Moisture Depletion Predictor (1D CNN)                  │
│ • Model B: Pump Mechanical Anomaly Detector (Autoencoder)              │
│ • Model C: Solar Irradiance 2-Hour Nowcasting (Quantized LightGBM)     │
├────────────────────────────────────────────────────────────────────────┤
│ TIER 1: Agentic Deterministic RAG (Cloud / Advisory Interface)         │
│ • Deterministic calculation engines compute metrics first              │
│ • Generative LLM translates structured JSON into vernacular narrative  │
│ • Strict zero-hallucination prompt boundaries (from GramDrishti)       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Model Specifications & Quantization

### Model A: Soil Moisture Depletion Nowcaster (TinyML)
* **Target:** Predict root-zone volumetric water content $\theta(t + 24\text{h})$ to anticipate stress before it manifests visually.
* **Input Features ($8\times 1$ vector):** Current 10cm moisture, current 30cm moisture, 24h delta, air temp, humidity, solar radiation, crop stage day, soil type index.
* **Architecture:** Quantized 2-layer GRU / 1D Convolutional Neural Network.
* **Footprint:** Model weights quantized to `int8` (<32 KB flash memory, <8 KB RAM on ESP32-S3).
* **Inference Latency:** <12 milliseconds on a 240 MHz Xtensa LX7 core.

### Model B: Pump Motor Health & Anomaly Detector
* **Target:** Detect bearing wear, impeller cavitation, and borewell sand-intake before catastrophic pump failure occurs.
* **Input Features:** High-frequency RMS motor current ripple ($I_{rms}$), power factor ($\cos\phi$), and DC bus ripple voltage polled from Altivar VFD registers.
* **Architecture:** Unsupervised Convolutional Autoencoder trained on healthy motor baseline signatures.
* **Metric:** Reconstruction error exceeding threshold $\epsilon_{fault}$ triggers automated drive deceleration and SMS warning.

---

## 3. Cloud Digital Twin & Deterministic RAG Architecture

For macro-level advisory, farm-gate planning, and FPO aggregation:
* **The Digital Twin:** A cloud-based state representation of each registered farm plot tracking:
  - Cumulative seasonal water balance ($\sum ET_c - \sum P_{eff} - \sum I_{irr}$).
  - Satellite vegetative vigor history (Sentinel-2 10m NDVI and NDWI timeseries).
  - Energy audit ledger (Total solar kWh generated vs. pumping kWh vs. cold storage kWh).
* **Deterministic RAG Pattern (Evolved from GramDrishti):**
  - When a farmer asks a question via voice/WhatsApp (e.g., *"Can I irrigate tomorrow?"*):
  1. The question is classified into an intent vector (`irrigation_schedule`, `energy_diversion`, `cold_storage`).
  2. The deterministic pipeline computes exact numerical answers from the Digital Twin (e.g., `soil_moisture: 34%`, `et0_tomorrow: 5.2mm`, `recommended_water: 0 L (rain forecast 22mm)`).
  3. The structured JSON is fed into the LLM with a strict system constraint: *"State only the numbers provided in the context. Never fabricate water volumes or operational hours."*
  4. Output is rendered into natural spoken audio in Marathi/Hindi.
