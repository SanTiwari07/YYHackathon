# AgroStruxure™ Industrial Design System Specification
**Version:** 1.0.0  
**Domain:** Agricultural Microgrid & Industrial Precision Automation  
**Reference Alignment:** Schneider Electric QuartzDS (`@quartzds`) & Yuva Yodha Tech Hackathon Standards  

---

## 1. Design Philosophy

AgroStruxure™ exists at the convergence of **mission-critical industrial automation** and **rural smallholder accessibility**. The design philosophy is built upon three non-negotiable tenets:

1. **Industrial Reliability Meets Rural Empathy:** Field conditions in rural Maharashtra, Rajasthan, and Punjab feature harsh sunlight glare, intermittent 2G/4G connectivity, fluctuating electrical phases, and varying farmer literacy. The interface must communicate state with absolute clarity—favoring unmistakable physical metaphors (valves, pumps, switches, water levels, storage crates) over abstract software graphs.
2. **Physics-First Transparency:** Every metric displayed—from $ET_0$ evapotranspiration to root zone depletion ($D_r$), VFD motor frequency ($Hz$), and cold storage temperature ($°C$)—is physically grounded in real mathematical equations (FAO-56 Penman-Monteith, hydraulic affinity laws, thermodynamic phase transitions). The design system treats telemetry as live industrial physics, not arbitrary dashboards.
3. **Zero-Hallucination Cognitive Trust:** Smallholders risk their seasonal livelihood on irrigation and crop storage. The UI must never obscure automation states, never guess numbers, and always provide physical manual override controls alongside plain vernacular explanations (Marathi, Hindi, English).

---

## 2. Visual Direction & Brand Personality

### Brand Personality Attributes
- **Authoritative & Industrial:** Rooted in Schneider Electric’s century-old legacy in switchgear and power electronics. Clean, structural, robust, dependable.
- **Ecologically Grounded:** Vibrant agricultural green balanced by deep earthen slate and high-contrast alert indicators.
- **Modern & Energetic:** Infused with the high-energy hackathon spirit of Yuva Yodha—purpose-driven, youth-led clean energy innovation.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        BRAND ARCHETYPE MATRIX                          │
├────────────────────┬────────────────────┬──────────────────────────────┤
│ Core Dimension     │ Tone / Treatment   │ UX Manifestation             │
├────────────────────┼────────────────────┼──────────────────────────────┤
│ Tone of Voice      │ Calm, Direct,      │ Crisp labels, no jargon,     │
│                    │ Respectful, Clear  │ vernacular audio synthesis   │
│ Physical Feel      │ Tactile, Industrial│ High-contrast toggle switches│
│                    │ Solid-state        │ physical status LED pill tags│
│ Cognitive Load     │ Minimal, Layered   │ Glanceable top-level states; │
│                    │ Progressive        │ deep Modbus register views   │
│                    │ Disclosure         │ segregated for technicians   │
└────────────────────┴────────────────────┴──────────────────────────────┘
```

---

## 3. Color Palette & Tokens

The AgroStruxure color system harmonizes **Schneider Electric QuartzDS tokens** (`#3dcd58`, `#0087cd`, `#151a1c`) with **Yuva Yodha Tech Hackathon colors** (`#024230`, `#0d8752`, `#ffce00`, `#fee6c4`).

### 3.1 Primary Brand Colors
| Token Name | Hex Code | RGB | Role / Usage | Contrast (on #FFF / #000) |
|---|---|---|---|:---:|
| `--se-primary` | `#3DCD58` | `61, 205, 88` | Signature Schneider "Life Is On" Green. Active states, solar power online, primary buttons | 2.1:1 / 10.0:1 |
| `--se-primary-hover`| `#32AD3C` | `50, 173, 60` | Interactive hover state for primary green triggers | 2.6:1 / 8.0:1 |
| `--yy-deep-forest` | `#024230` | `2, 66, 48` | Deep dark emerald backdrop; typography header accent; brand grounding | 12.8:1 / 1.6:1 |
| `--yy-emerald` | `#0D8752` | `13, 135, 82` | Section badges, secondary accents, field capacity status tags | 4.8:1 / 4.4:1 |
| `--yy-solar-gold` | `#FFCE00` | `255, 206, 0` | PM-KUSUM Solar peak badges, highlight CTAs, solar irradiance indicators | 1.3:1 / 16.0:1 |

### 3.2 Functional & Industrial Status Tokens
| Token Name | Hex Code | RGB | Industrial Semantics |
|---|---|---|---|
| `--color-pump-active` | `#3DCD58` | `61, 205, 88` | Stage 1: Pumping active, VFD operating at 30–50 Hz |
| `--color-cutoff-active`| `#0087CD` | `0, 135, 205` | Stage 2: Root zone saturated; solenoid closed |
| `--color-cold-divert` | `#8015E8` | `128, 21, 232`| Stage 3: TeSys contactor switched; 3.8 kW cold room active |
| `--color-transient` | `#E47F00` | `228, 127, 0` | Passing cloud transient, MPPT throttling |
| `--color-trip-alarm` | `#DC0A0A` | `220, 10, 10` | Motor dry-run alarm, over-temperature, contactor trip |
| `--color-standby` | `#9FA0A4` | `159, 160, 164`| Nighttime / low solar insolation (<200 W/m²) |

### 3.3 Neutrals & Background Surfaces
| Token Name | Hex Code | Dark/Light Context | Application |
|---|---|---|---|
| `--surface-canvas-light` | `#F8FAFC` | Light Mode Canvas | Primary page background |
| `--surface-card-light` | `#FFFFFF` | Light Mode Cards | Container cards, elevation 1 |
| `--surface-canvas-dark` | `#0B1115` | Dark / Industrial Cockpit | Industrial night mode & VFD cockpit canvas |
| `--surface-card-dark` | `#151A1C` | Dark Mode Cards | QuartzDS footer-matched cards (`#151A1C`) |
| `--surface-panel-dark` | `#1D2428` | Elevated Cockpit Surface | Secondary elevation, modal backdrops |
| `--border-subtle` | `#E2E8F0` / `#2A343A` | Light / Dark | Card outlines, table borders, dividers |
| `--text-primary` | `#090B0C` / `#F8FAFC` | Light / Dark | Main titles, key numerical readings |
| `--text-secondary` | `#5C6466` / `#94A3B8` | Light / Dark | Subtitles, parameter units, helper descriptions |

---

## 4. Typography System

The typography architecture uses high-legibility geometric sans-serif typefaces engineered for technical dashboards and readability in outdoor direct sunlight.

### 4.1 Typeface Families
- **Primary Display & Headings:** `"Arial Rounded MT for SE"`, `"Poppins"`, `system-ui`, `-apple-system`, `sans-serif`  
  *(Proprietary Schneider aesthetic with friendly, high-contrast rounded contours)*
- **Data & Telemetry / Numbers:** `"JetBrains Mono"`, `"Roboto Mono"`, `monospace`  
  *(Tabular figures for jitter-free Modbus register values, frequencies, flow rates)*
- **Vernacular Scripts (Hindi / Marathi):** `"Noto Sans Devanagari"`, `"Mukta"`, `sans-serif`  
  *(Optimized conjuncts and diacritics for rural literacy)*

### 4.2 Font Scale & Hierarchy
| Level | Font Size | Line Height | Weight | Letter Spacing | Target Usage |
|---|---|---|---|---|---|
| **Display Hero** | `48px` (`3.0rem`) | `52px` | `800` (Extrabold) | `-0.025em` | Cockpit primary banner, key summary figure |
| **Heading 1 (H1)** | `32px` (`2.0rem`) | `38px` | `700` (Bold) | `-0.02em` | Page headers, screen titles |
| **Heading 2 (H2)** | `24px` (`1.5rem`) | `30px` | `700` (Bold) | `-0.015em` | Major section cards, subsystem headers |
| **Heading 3 (H3)** | `18px` (`1.125rem`)| `24px` | `600` (Semibold) | `-0.01em` | Gauge titles, metric groupings, modal titles |
| **Body Large** | `16px` (`1.0rem`) | `24px` | `400` / `500` | `normal` | Primary advisory copy, voice transcript text |
| **Body Medium** | `14px` (`0.875rem`)| `20px` | `400` / `500` | `normal` | Field values, table rows, button labels |
| **Body Small** | `12px` (`0.75rem`) | `16px` | `400` / `500` | `+0.01em` | Secondary metadata, timestamps, input helper text |
| **Telemetry Mono**| `14px` (`0.875rem`)| `18px` | `600` (Semibold) | `tabular-nums` | Modbus register addresses, hex codes, kW/Hz |

---

## 5. Spacing, Elevation & Layout Grid

### 5.1 Spacing Scale (8pt Grid)
All paddings, margins, gaps, and structural containers conform strictly to an **8px base unit scale**:

```css
--space-1: 4px;   /* Micro spacing, badge internal padding */
--space-2: 8px;   /* Icon-to-text gap, compact button padding */
--space-3: 12px;  /* Form field padding, list item separation */
--space-4: 16px;  /* Standard card internal padding, grid column gap */
--space-6: 24px;  /* Section gutters, component card padding */
--space-8: 32px;  /* Hero paddings, modal internal body */
--space-12: 48px; /* Macro section vertical separation */
--space-16: 64px; /* Major page block margins */
```

### 5.2 Border Radius Tokens
| Token | Value | Target Applications |
|---|---|---|
| `--radius-sm` | `4px` | Badges, tags, inner Modbus register chips |
| `--radius-md` | `8px` | Primary buttons, text inputs, dropdown triggers (Schneider QuartzDS standard) |
| `--radius-lg` | `12px` | Subsystem telemetry cards, dialog modals, time scrubber container |
| `--radius-xl` | `16px` | Main operational cockpit cards, flow diagram frame |
| `--radius-pill`| `9999px`| Pill buttons, search inputs, status indicators (Yuva Yodha standard) |

### 5.3 Elevation & Industrial Shadows
1. **Flat / Flush (`elevation-0`):** `box-shadow: none; border: 1px solid var(--border-subtle)`  
   *(Used for telemetry panels and clean technical readouts)*
2. **Subtle Elevation (`elevation-1`):** `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.04)`  
   *(Used for interactive cards, dropdown panels)*
3. **Elevated Card (`elevation-2`):** `box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)`  
   *(Used for hovering cards, floating action buttons, active state indicators)*
4. **Modal / Overlay (`elevation-3`):** `box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.25), 0 10px 10px -5px rgba(0, 0, 0, 0.1)`  
   *(Used for emergency manual override dialogs, settings modals)*
5. **Active Neon Glow (`glow-green`):** `box-shadow: 0 0 15px rgba(61, 205, 88, 0.35)`  
   *(Used when solar generation or cold storage compressor is active)*

### 5.4 Grid System & Responsive Breakpoints
- **Mobile First (`<640px` - `sm`):** 1 column stacked layout, touch targets $\ge 48\text{px}$, sticky bottom status dock.
- **Tablet (`640px–1024px` - `md`):** 6-column grid, dual-column telemetry cards.
- **Desktop (`1024px–1440px` - `lg`/`xl`):** 12-column grid, max-width `1380px`, triple-panel architecture (Navigation / Live Cockpit / Voice Copilot).
- **Ultra-Wide / Control Room (`>1440px` - `2xl`):** 16-column grid for full SCADA digital twin monitoring.

---

## 6. Core Component Library Specifications

### 6.1 Buttons & Triggers
- **Primary Industrial Button (`.btn-primary`):**  
  - Background: `#3DCD58`; Text: `#090B0C`; Font Weight: `700`; Radius: `8px`; Height: `44px` (touch-safe); Padding: `12px 24px`.  
  - Hover: `#32AD3C`; Active: scale(0.98); Focus ring: `2px solid #0087CD`.
- **Secondary Outline Button (`.btn-secondary`):**  
  - Background: `transparent`; Text: `var(--text-primary)`; Border: `1.5px solid var(--border-subtle)`; Radius: `8px`.
- **Destructive / Emergency Stop (`.btn-emergency`):**  
  - Background: `#DC0A0A`; Text: `#FFFFFF`; Icon: Lucide `OctagonAlert`; Extra-large touch target (`56px` height); Physical latch confirmation modal.
- **Vernacular Audio Play Button (`.btn-voice`):**  
  - Pill shape (`radius: 9999px`); Pulsing soundwave animation when audio is playing; Play/Pause icon with language indicator (`"मराठी ऐका"` / `"हिंदी सुनें"`).

### 6.2 Data Instrumentation & Physical Gauges
- **Root Zone Moisture Depth Gauge:** Dual-layer visual cross section showing 10cm surface moisture and 30cm root moisture. Displays exact Field Capacity ($FC = 45\%$) threshold marker and Wilting Point ($WP = 18\%$). Color shifts from Amber (Stress) to Green (Optimal) to Blue (Saturated/Cutoff).
- **Altivar VFD Frequency Meter:** Semi-circular dial with needle or circular SVG progress indicator measuring $0\text{ to }50\text{ Hz}$, with MPPT operating band marked between $32\text{ Hz}$ and $50\text{ Hz}$.
- **TeSys Changeover Contactor Graphic:** Real-time animated electromechanical switch showing contact position:
  - Position A: Contact closed to 3-Phase Submersible Pump.
  - Position B: Contact closed to Micro-Cold Room PCM Compressor.
  - Interlock Status: 150ms dead-band lock indicator to prevent arc fault.

### 6.3 24-Hour Diurnal Day Timeline Scrubber
- Full-width draggable horizontal timeline representing a farming day from 00:00 to 23:59.
- Visual sunlight gradient tracking solar irradiance curve ($0\text{ to }950\text{ W/m}^2$).
- Milestone markers for key events:
  - `06:00` Sunrise
  - `08:30` Solar Irradiance Threshold ($>250\text{ W/m}^2$) $\to$ Irrigation Starts
  - `11:30` Root Zone Reaches Field Capacity $\to$ Irrigation Cutoff & Cold Room Diversion
  - `15:30` Solar Irradiance Drops $\to$ Cold Storage Operates on Thermal PCM Buffer
  - `18:30` Sunset
- Play/Pause button with 1x, 5x, 30x simulation speed multipliers.

### 6.4 Status Badges & Pill Tags
- **Pill Shape:** Height `24px`, padding `2px 10px`, font size `12px`, font weight `600`, radius `9999px`.
- **Variants:**
  - `badge-solar`: Background `rgba(255, 206, 0, 0.15)`, text `#B98300`, border `1px solid rgba(255, 206, 0, 0.4)`.
  - `badge-pumping`: Background `rgba(61, 205, 88, 0.15)`, text `#0D8752`, border `1px solid rgba(61, 205, 88, 0.4)`.
  - `badge-coldroom`: Background `rgba(128, 21, 232, 0.15)`, text `#8015E8`, border `1px solid rgba(128, 21, 232, 0.4)`.
  - `badge-alarm`: Background `rgba(220, 10, 10, 0.15)`, text `#DC0A0A`, border `1px solid rgba(220, 10, 10, 0.4)`.

---

## 7. State System & Feedback Patterns

Every screen and component supports the complete operational lifecycle:

1. **Idle / Standby State:** Nighttime or low insolation. Grayed gauges with status indicator `"Solar Inactive (Irradiance < 200 W/m²)"`.
2. **Active Pumping State:** High-contrast green accents, animated pulsating water flow lines, live motor RPM and flow rate ticking.
3. **Cutoff & Divert Transition:** 1.5-second visual transition depicting contactor opening with an audible relay "click" sound effect, followed by purple circuit paths energizing the cold storage block.
4. **Passing Cloud Transient:** Irradiance drops from 850 W/m² to 320 W/m²; drive throttles frequency smoothly to 34 Hz; warning badge `"MPPT Throttling — Cloud Cover"`.
5. **Dry-Run Alarm State:** Flashing red alert card with audible buzzer option, automated pump cut-off, and vernacular advisory: *"Borewell water level critically low. Pump stopped to protect motor coils."*
6. **Loading & Skeletons:** Animated shimmering skeleton blocks matching exact gauge silhouettes during API re-sync.
7. **Offline / Satellite Failover:** Amber banner: `"Ground FDR probe signal intermittent. Failover active: Using Sentinel-1 SAR Cloud-Free Radar Soil Index (SMI: 0.42)"`.

---

## 8. Accessibility & Field Usability Rules (WCAG 2.1 AA+)

1. **Outdoor Glare Readability:** All text and critical instrumentation maintain a minimum contrast ratio of **4.5:1** for standard text and **7:1** for primary status figures against dark/light surfaces.
2. **High-Contrast Touch Targets:** All touch targets on mobile viewports are at least **48x48px** with a **12px minimum hit-padding**, accommodating farmers with dirt or water on their hands.
3. **Multimodal Feedback:** Visual changes are accompanied by icon glyphs, text labels, and vernacular voice synthesis so color blindness or low literacy never inhibits operation.
4. **Keyboard Navigation & Screen Readers:** Fully navigable via `Tab`, `Shift+Tab`, `Space`, `Enter`. Proper ARIA attributes (`aria-live="polite"`, `role="status"`, `aria-valuenow`).

---

## 9. Animation & Motion Principles

- **Motion Philosophy:** Functional, physical, and restrained. Motion in AgroStruxure communicates the physical movement of electricity and water—not decorative flourish.
- **Duration Scale:**
  - Fast (`100ms–150ms`): Button press, checkbox toggle, hover highlight.
  - Standard (`250ms–350ms`): Modal enter/exit, dropdown menu expansion, tab switch (`cubic-bezier(0.4, 0, 0.2, 1)`).
  - Physical Simulation (`600ms–1000ms`): Contactor arm rotation, water level filling, gauge needle dampening (`cubic-bezier(0.34, 1.56, 0.64, 1)`).
- **Reduced Motion Support:** All CSS transitions and animations honor `@media (prefers-reduced-motion: reduce)` by immediately jumping to final state values without duration.
