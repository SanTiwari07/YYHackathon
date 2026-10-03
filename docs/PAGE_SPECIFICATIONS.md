# AgroStruxure™ Complete Page & Screen Specifications
**Document Code:** SPEC-PAGE-01  
**Project:** AgroStruxure™ (Yuva Yodha 2026 / Schneider Electric India)  
**Author:** Senior Product Designer, UX Architect & Frontend Design Engineer  
**Status:** Comprehensive UI Specification Contract  

---

## Screen Directory Overview
1. **Page 1:** [Live Operational Cockpit & Digital Twin](#page-1-live-operational-cockpit--digital-twin-route-cockpit-or-)
2. **Page 2:** [Farmer Vernacular Advisory Hub](#page-2-farmer-vernacular-advisory-hub-route-farmer-hub)
3. **Page 3:** [Cadastral Plot & Crop Profile Onboarding](#page-3-cadastral-plot--crop-profile-onboarding-route-plots)
4. **Page 4:** [Industrial Hardware & Modbus Register Telemetry Inspector](#page-4-industrial-hardware--modbus-register-telemetry-inspector-route-telemetry)
5. **Page 5:** [Energy, Water & Carbon Impact Analytics](#page-5-energy-water--carbon-impact-analytics-route-analytics)

---

## Page 1: Live Operational Cockpit & Digital Twin (Route: `/cockpit` or `/`)

### 1. Purpose
The primary interactive command center and digital twin of the AgroStruxure™ microgrid. It visually links solar energy generation, variable frequency pump actuation, soil hydration cutoff, and post-harvest cold storage diversion into a single glanceable, interactive surface. Built for live operator monitoring and the 5-minute hackathon jury pitch demonstration.

### 2. User
- **Primary:** Hackathon Jury & Schneider Technical Evaluators, FPO Microgrid Managers.
- **Secondary:** Field Service Technicians, Progressive Farmers.

### 3. Information Hierarchy
1. **Primary Operational State Banner:** Massive visual header declaring the active microgrid phase:
   - `STAGE 1: SOLAR PUMPING ACTIVE (VFD at 48.2 Hz | Drip Line Pressure: 2.1 bar)`
   - `STAGE 2: ROOT ZONE SATURATED — WATER CUT-OFF (Field Capacity: 45.2% reached)`
   - `STAGE 3: SURPLUS SOLAR DIVERTED TO COLD ROOM (3.8 kW DC Cooling Produce at 4°C)`
2. **Live Power Flow Topology Graphic:** Animated schematic showing electricity flow from PV array $\to$ Altivar VFD $\to$ TeSys Contactor $\to$ Pumping / Cold Storage loads.
3. **24-Hour Interactive Diurnal Scrubber:** Full-width timeline slider with play/pause, time acceleration, and key diurnal milestone markers (06:00, 08:30, 11:30, 15:30, 18:30).
4. **Core Telemetry Gauges Grid:**
   - Solar PV Generation: $kW$ and $W/m^2$ irradiance.
   - Altivar VFD Frequency: $0\text{ to }50\text{ Hz}$ operating dial with motor current ($A$).
   - Dual-Depth Soil Moisture: 10cm surface & 30cm root moisture vs. Field Capacity threshold.
   - Cold Storage Environment: Chamber temperature ($°C$) and thermal PCM charge %.
5. **Edge Scenario Stress-Test Dock:** One-click simulation triggers:
   - "Inject Monsoon Cloud Transient"
   - "Simulate Borewell Dry-Run Alarm"
   - "Simulate Severe Root Drought"

### 4. Layout
- **Desktop (12 Columns):**
  - Columns 1–8: Operational State Banner, Animated Flow Topology, 24-hr Diurnal Scrubber, and Scenario Stress-Test Bar.
  - Columns 9–12: Instrumentation Gauges Stack, Real-time Physical Readouts, and Live Modbus Sync Badge.
- **Mobile (<640px):**
  - Single stacked column: State Banner $\to$ Compact Flow Diagram $\to$ Draggable Scrubber $\to$ 2x2 Gauge Grid $\to$ Quick Trigger Buttons.

### 5. Components
- `StateIndicatorBanner` (High-contrast alert card with pulsing phase indicator).
- `MicrogridFlowTopology` (Interactive SVG/Canvas canvas with animated electron packets).
- `DiurnalTimelineScrubber` (Draggable slider, timeline ticks, speed multipliers [1x, 5x, 30x]).
- `AltivarVfdGauge` (Radial SVG meter with frequency needle and torque indicators).
- `DualDepthMoistureGauge` (Layered root-zone graphical tank).
- `ColdRoomTempGauge` (Thermometer gauge with eutectic PCM freeze state).
- `ScenarioTriggerPill` (Interactive simulation buttons with state icons).

### 6. Primary CTA
- **"Toggle Simulation Play / Pause"** (Plays the 24-hour diurnal cycle autonomously).

### 7. Secondary Actions
- **"Inject Cloud Transient"** (Tests MPPT throttle response down to 32 Hz).
- **"Emergency Manual Contactor Override"** (Forces TeSys switchgear into safe standby).
- **"Switch to Vernacular Farmer View"** (Seamless navigation to Page 2).

### 8. States Supported
- **Idle / Night (`00:00–06:00`):** Low-light dark slate mode; gauges dimmed; *"Solar Inactive $(<200\text{ W/m}^2)$"*.
- **Morning Pumping (`08:30–11:30`):** Vibrant Schneider Green; pulsing water flow lines; Altivar VFD active at 48 Hz.
- **Cutoff & Cold Diversion (`11:30–15:30`):** Electric Purple / Cyan; animated TeSys contactor snaps to Cold Storage; compressor spins at 50 Hz.
- **Cloud Cover Fault:** Amber caution banner; VFD throttles down smoothly to avoid tripping.
- **Borewell Dry-Run Trip:** Flashing red alert card; zero water flow detected; pump locked out.

### 9. Responsive Behavior
- **Desktop (1440px):** Full digital twin SCADA experience with simultaneous gauge readouts and uncompressed topology diagram.
- **Tablet (768px–1024px):** 2-column layout; topology diagram height scales to 280px; gauges align in a 2x2 grid.
- **Mobile (<768px):** Sticky top state badge; horizontal scrolling for simulation triggers; touch-optimized timeline scrubber with snap-to-hour functionality.

### 10. Accessibility (a11y)
- Dynamic state updates announced via `aria-live="assertive"`.
- All SVGs feature descriptive `aria-label` tags (e.g., `aria-label="Power flow currently routing 3.8 kilowatts to cold room compressor"`).
- Keyboard shortcuts: `Space` for Play/Pause, `Left/Right Arrow` to scrub time by 30-minute intervals.

### 11. Motion Principles
- Contactor switchover features a 250ms mechanical recoil animation (`cubic-bezier(0.34, 1.56, 0.64, 1)`).
- Water pulse and electricity paths utilize SVG stroke-dasharray keyframe animations with speed bound to flow rate and kW output.

---

## Page 2: Farmer Vernacular Advisory Hub (Route: `/farmer-hub`)

### 1. Purpose
Designed explicitly for the rural smallholder farmer (Persona 1: Ramesh Patil). Strips away engineering jargon and replaces complex engineering graphs with tactile physical metaphors, high-contrast visual indicators, plain vernacular copy (Marathi, Hindi, English), WhatsApp-style audio voice notes, and 1-click mechanical bypass controls.

### 2. User
- **Primary:** Smallholder Farmers (low technical literacy, vernacular-first).
- **Secondary:** FPO Field Coordinators ("Urja Mitras").

### 3. Information Hierarchy
1. **Vernacular Audio Copilot Banner ("Krishi Mitra Sahayak"):**
   - Prominent pill player with Play/Pause, animated sound wave, and colloquial text transcript:
     *"Namaskar Ramesh! Your onion plot has received full water (2,400 litres). Pump is now OFF. Free solar power is running your cold storage room."*
   - Language selector buttons (`मराठी` | `हिंदी` | `English`).
2. **"Is My Crop Thirsty?" Root-Zone Cross-Section:**
   - Visual cross section of a tomato or cotton plant showing the dry soil surface vs. saturated underground root zone (15–30cm). Eliminates the "dry cracked surface" psychological urge to over-water.
3. **Pumping & Cold Storage Glanceable Cards:**
   - Big Green Card: *"Pump Status: Complete & Resting"* (2,400 Litres Delivered).
   - Big Purple Card: *"Cold Room: 4°C Chilling Active"* (14 Crates of Produce Protected).
4. **Daily Financial Uplift Counter:**
   - Large bold rupee figures: *"Today's Benefit: ₹380 Saved (₹240 Crops Protected + ₹140 Diesel Avoided)"*.
5. **Physical Manual Override Box:**
   - Visual illustration of the field enclosure manual bypass switch with 1-tap emergency start (requires 3-second hold to prevent accidental activation).

### 4. Layout
- Single mobile-first container with large touch cards, `24px` internal padding, high-contrast dark green / pure white surfaces, and floating sticky bottom voice trigger.

### 5. Components
- `VernacularVoiceCard` (Waveform audio player with localized transcript).
- `PlantRootCrossSection` (Botanical soil illustration with dynamic water level).
- `GlanceableStatusTile` (Extra-large status tile with physical icon).
- `RupeeImpactTicker` (Prominent currency savings counter).
- `HoldToActivateButton` (Safety latch button requiring a 3-second sustained press).

### 6. Primary CTA
- **"Listen in Marathi / मराठीत ऐका"** (Plays synthesized vernacular advisory note).

### 7. Secondary Actions
- **"Manual 30-Minute Pump Boost"** (Emergency override for fertilizer application).
- **"Call Field Technician (Urja Mitra)"** (Direct 1-tap phone dialer).

### 8. States Supported
- **Normal Balanced State:** Clear sunny day icon, green tick marks, calming audio message.
- **Irrigation In Progress:** Blue flowing water droplet animation; countdown timer to Field Capacity.
- **Over-Watering Warning (Educational State):** Gentle yellow card explaining: *"Adding more water will rot your roots and waste solar power."*
- **Offline SMS Mode:** Falls back to plain text SMS preview if internet is disconnected.

### 9. Responsive Behavior
- Designed natively for mobile viewport (`360px–428px` width), scales gracefully to tablet for FPO kiosk display.

### 10. Accessibility (a11y)
- Screen reader announcements in native Devanagari script (`lang="mr"` / `lang="hi"`).
- Minimum font size `16px`; touch targets `56px` height.
- Contrast ratio $\ge 7:1$ for outdoor sunlight readability.

### 11. Motion Principles
- Calming, rhythmic pulse on the audio play button (`scale(1.04)` over 2.5s).
- Soil water level gently rises with an organic liquid ease (`cubic-bezier(0.25, 1, 0.5, 1)`).

---

## Page 3: Cadastral Plot & Crop Profile Onboarding (Route: `/plots`)

### 1. Purpose
Enables farmers and FPO managers to register their agricultural land boundaries, specify soil texture properties, select current crop cycles, and configure connected PM-KUSUM solar pump specifications. Incorporates statutory consent under the **Indian Digital Personal Data Protection (DPDP) Act 2023**.

### 2. User
- **Primary:** FPO Directors (Persona 2: Sunita Shinde), Field Technicians.
- **Secondary:** Progressive Smallholder Farmers.

### 3. Information Hierarchy
1. **Interactive Cadastral Satellite Map:** Leaflet map container displaying satellite imagery with GPS boundary polygon drawing tools, acreage calculation, and survey number lookup.
2. **Crop & Agronomic Parameters Card:**
   - Crop selector (Tomato, Onion, Cotton, Soybean, Wheat).
   - Sowing date picker and computed season duration.
   - Stage-dependent crop coefficient ($K_c$) preview.
3. **Soil Hydraulic Properties Selector:**
   - Soil Texture dropdown (Deep Black Cotton Soil, Sandy Loam, Clay Loam, Alluvial).
   - Automated lookup of Field Capacity ($\theta_{FC}$) and Permanent Wilting Point ($\theta_{WP}$).
4. **PM-KUSUM Solar Pump & Drive Configuration:**
   - Pump rating (3 HP, 5 HP, 7.5 HP submersible).
   - VFD Model (Schneider Altivar Solar ATV320 default).
   - Solar Array Capacity ($kW_p$) and borewell depth ($m$).
5. **DPDP Act 2023 Statutory Consent Check:**
   - Plain-language checkbox authorizing satellite telemetry and groundwater monitoring.

### 4. Layout
- Split-screen desktop layout: Left 6 columns for interactive map polygon delineation; Right 6 columns for the multi-step accordion configuration form. Stacks vertically on mobile.

### 5. Components
- `CadastralPolygonMap` (Leaflet satellite canvas with polygon drawing controls).
- `CropSelectorCards` (Icon-rich cards with crop imagery and standard water requirements).
- `SoilHydraulicSlider` (Dual thumb slider configuring Field Capacity and Wilting Point).
- `HardwareSpecsForm` (Clean form inputs styled with QuartzDS 8px radius tokens).
- `DpdpConsentBox` (Verifiable compliance card with timestamp).

### 6. Primary CTA
- **"Save Plot Profile & Initialize AgroStruxure Edge"** (Validates boundaries and triggers backend Modbus calibration).

### 7. Secondary Actions
- **"Detect Location via GPS"** (Centers map on user's current field position).
- **"Fetch Soil Profile via ICAR Soil Health Grid"** (Automated national database fill).

### 8. States Supported
- **Initial / Empty State:** Map centered on Maharashtra agricultural belt; helper banner guiding the user to click map corners.
- **Drawing In Progress:** Dashed bounding polygon with live hectare calculation.
- **Validated State:** Solid green plot boundary with soil moisture heatmap overlay.
- **Form Error State:** Field validation alerts with specific corrective guidance (e.g., *"Wilting point cannot exceed field capacity"*).

### 9. Responsive Behavior
- On mobile devices, map is presented in a 300px collapsible drawer with a "Fullscreen Map" toggle for easy boundary drawing using finger gestures.

### 10. Accessibility (a11y)
- Alternative coordinate entry inputs provided for users unable to use pointer-based map drawing.
- Accessible form labels with explicit `aria-describedby` links to help text.

### 11. Motion Principles
- Smooth map panning and zooming (`flyTo` animations with 800ms duration).
- Accordion sections expand with height transitions (`max-height` 300ms ease-out).

---

## Page 4: Industrial Hardware & Modbus Register Telemetry Inspector (Route: `/telemetry`)

### 1. Purpose
The deep engineering and commissioning console built for Schneider Electric engineers, DISCOM officials, and hackathon jury judges. Exposes raw industrial telemetry, Modbus RTU holding registers, mathematical equation validation (FAO-56 Penman-Monteith step-by-step variables), and RS485 communication diagnostics.

### 2. User
- **Primary:** Schneider Industrial Automation Evaluators, DISCOM Electrical Engineers (Persona 4: Anand Rao), Field Service Technicians (Persona 3: Suresh Kumar).

### 3. Information Hierarchy
1. **Schneider Industrial Drive Status Bar:**
   - Drive Status Word (Register `3208`: `0x0004 - DRIVE READY & RUNNING`).
   - Active Command Word (Register `8501`: `0x0002 - RUN ACTIVE`).
   - Communication Link: `RS485 Modbus RTU @ 19,200 baud | Error Rate: 0.00%`.
2. **Live Modbus Holding Register Table:**
   - Register address, parameter name, raw INT16/UINT16 value, scaled physical value, engineering units, and read/write permissions.
3. **FAO-56 Penman-Monteith Math Validation Panel:**
   - Transparent step-by-step equation breakdown with live values:
     - Net Radiation $R_n$: $18.4\text{ MJ/m}^2\text{/day}$
     - Mean Temp $T$: $32.4°\text{C}$ | Wind Speed $u_2$: $2.1\text{ m/s}$
     - Vapor Pressure Deficit ($e_s - e_a$): $2.41\text{ kPa}$
     - Psychrometric Constant $\gamma$: $0.067\text{ kPa/°C}$
     - Resulting $ET_0$: $5.82\text{ mm/day} \implies ET_c: 6.69\text{ mm/day}$
4. **Live MQTT Stream / WebSocket Event Log:**
   - Scrolling terminal console showing JSON payloads emitted by the ESP32-S3 edge gateway.
5. **TeSys Switchgear Interlock Diagnostics:**
   - Contactor state, mechanical cycles counter, coil voltage (24V DC), and interlock dead-band timer verification ($150\text{ms}$).

### 4. Layout
- Multi-pane engineering workbench:
  - Top full-width status ribbon.
  - Left 7 columns: Live Modbus Register Table and RS485 Link Health.
  - Right 5 columns: FAO-56 Math Engine Inspector and Terminal Event Log.

### 5. Components
- `ModbusRegisterTable` (High-density tabular grid with monospace font and live value flashing).
- `MathematicalProofCard` (KaTeX formatted equations with live numerical substitutions).
- `RawTerminalLog` (Monochrome dark terminal with autoscroll and pause toggle).
- `SwitchgearHealthBadge` (Electromechanical contact wear and cycle count tracker).

### 6. Primary CTA
- **"Write Register Command"** (Allows authorized engineers to write speed reference to Register `8502`).

### 7. Secondary Actions
- **"Export Modbus Diagnostic CSV"** (Downloads timestamped register dump).
- **"Clear Terminal Log"** (Resets the WebSocket event stream).

### 8. States Supported
- **Healthy Sync State:** Green pulse indicator; register rows flash subtly on value changes.
- **Communication Loss Alarm:** High-priority red banner: *"RS485 Bus Timeout (Address 0x01 Unresponsive). Checking fallback..."*
- **Register Write Modal State:** Secure dialog with numeric clamp to prevent motor overspeed (>50 Hz).

### 9. Responsive Behavior
- Desktop-first layout. On mobile, table enables horizontal scroll with sticky column headers and pinned Register Address column.

### 10. Accessibility (a11y)
- Tabular figures (`font-variant-numeric: tabular-nums`) to prevent layout shifts.
- Terminal log includes pause button to satisfy WCAG auto-updating content standards.

### 11. Motion Principles
- Table cells flash a 200ms background highlight (`#3DCD58` at 15% opacity) when an updated Modbus packet is written.

---

## Page 5: Energy, Water & Carbon Impact Analytics (Route: `/analytics`)

### 1. Purpose
The macro impact and financial validation dashboard. Proves the economic and environmental return on investment (ROI) for smallholders, FPOs, and state DISCOMs. Displays quantified groundwater conservation metrics, surplus solar energy diversion totals, post-harvest crop preservation records, and enables 1-click generation of the dynamic PDF audit certificate.

### 2. User
- **Primary:** FPO Directors, DISCOM Policy Makers, Hackathon Jury Judges.
- **Secondary:** Bank Credit Officers (Agriculture Infrastructure Fund loans).

### 3. Information Hierarchy
1. **Executive Impact Summary Metric Tiles (4 Pillars):**
   - **Groundwater Saved:** $1,890\text{ m}^3$ (42% extraction avoided).
   - **Surplus Solar Harvested:** $2,555\text{ kWh/year}$ redirected to cooling.
   - **Crop Spoilage Avoided:** $2.8\text{ metric tonnes}$ vegetables preserved.
   - **Net Farmer Income Uplift:** **+₹72,450 / year** (sub-20-day payback).
2. **Interactive Diurnal Energy-Water Nexus Chart (Apache ECharts):**
   - Dual-axis graph charting Solar Irradiance ($W/m^2$), Pumping Power ($kW$), and Cold Storage Diversion ($kW$) across seasonal crop cycles.
3. **Smallholder Unit Economics & Payback Model:**
   - Breakdown of financial gains (Crop value saved: ₹56,000; Burnout avoided: ₹7,500; Yield boost: ₹14,200; Energy saved: ₹9,750; IoT fee: -₹1,200).
4. **FPO Fleet Cold Storage Capacity Utilization:**
   - Multi-farm thermal battery ledger tracking crate occupancy, chilling hours, and APMC mandi price arbitrage gains.
5. **PDF Audit Generation Section:**
   - Live preview card of the official **"AgroStruxure™ Farm Energy & Water Audit Certificate"**.

### 4. Layout
- 12-column responsive dashboard:
  - Top: 4-column metric cards.
  - Middle: 8 columns for Apache ECharts interactive visualization; 4 columns for Financial Payback Breakdown.
  - Bottom: 7 columns for FPO Fleet Ledger; 5 columns for PDF Audit Card Generator.

### 5. Components
- `MetricCardKpi` (Bold stat card with icon, percentage delta badge, and helper tooltip).
- `NexusEChart` (Responsive Apache ECharts dual-axis area chart with zoom and series toggle).
- `FinancialRoiTable` (Clean accounting breakdown showing net farmer uplift).
- `ColdStorageLedger` (Visual crate inventory with storage duration meters).
- `PdfAuditGenerator` (1-click trigger initiating ReportLab dynamic PDF rendering).

### 6. Primary CTA
- **"Generate Official PDF Audit Certificate"** (Compiles telemetry and downloads verified ReportLab PDF).

### 7. Secondary Actions
- **"Export CSV Dataset"** (Downloads raw energy and water ledger).
- **"Simulate 5-Year Carbon Credit Accrual"** (Projects voluntary carbon market revenue).

### 8. States Supported
- **Loaded Historical Data:** Complete multi-month curves with seasonal toggle (Kharif, Rabi, Zaid).
- **Generating Report State:** Shimmering progress indicator with status: *"Compiling FAO-56 Water Balance & Modbus kWh Counters..."*
- **Empty / New Plot State:** Informational placeholder illustrating anticipated savings based on regional averages.

### 9. Responsive Behavior
- Charts automatically re-calculate aspect ratios on resize (`chart.resize()`).
- On mobile, KPI cards render in a 2x2 grid, and the financial table collapses into a clean card list.

### 10. Accessibility (a11y)
- Charts provide tabular data table equivalents for screen-reader users (`aria-expanded="false"` toggle).
- High-contrast chart color palette adhering to deuteranopia/protanopia safe palettes.

### 11. Motion Principles
- Metric numbers count up smoothly from 0 to final values over 1,200ms using easing.
- ECharts series animate in sequentially with subtle opacity fade and path draw.
