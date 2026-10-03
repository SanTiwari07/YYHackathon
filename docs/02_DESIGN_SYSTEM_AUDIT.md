# 02 Design System Audit: AgroStruxure™ Industrial Design System
**Document ID:** AUDIT-DS-2026-V1  
**Source Document:** `DESIGN_SYSTEM.md` (Version 1.0.0)  
**Reference Alignment:** Schneider Electric QuartzDS (`@quartzds`) & Yuva Yodha Tech Standards  
**Status:** Complete Audit & Verification  

---

## 1. Design Philosophy

AgroStruxure™ converges **mission-critical industrial automation** with **rural smallholder accessibility** through three foundational tenets:

1. **Industrial Reliability Meets Rural Empathy:** Built for harsh direct sunlight glare, intermittent 2G/4G connectivity, fluctuating electrical phases, and diverse farmer literacy. Unmistakable physical metaphors (valves, pumps, contactors, water levels) take precedence over abstract graphs.
2. **Physics-First Transparency:** Telemetry reflects grounded physical equations (FAO-56 Penman-Monteith, hydraulic affinity laws, thermodynamic phase transitions), treating telemetry as live industrial physics rather than arbitrary software numbers.
3. **Zero-Hallucination Cognitive Trust:** Smallholders risk seasonal livelihoods. Automation states must never be obscured; manual override controls are always physically accessible alongside plain vernacular explanations (Marathi, Hindi, English).

---

## 2. Brand Identity & Personality

- **Authoritative & Industrial:** Rooted in Schneider Electric’s legacy in switchgear, motor control, and power electronics. Clean, structural, robust, dependable.
- **Ecologically Grounded:** Vibrant agricultural green balanced by deep earthen slate and high-contrast alert indicators.
- **Modern & Energetic:** Purpose-driven clean energy innovation aligned with the Yuva Yodha youth hackathon spirit.
- **Brand Dimensions:**
  - *Tone of Voice:* Calm, direct, respectful, clear; crisp labels without tech jargon.
  - *Physical Feel:* Tactile, solid-state industrial feel; high-contrast toggle switches and physical status LED indicators.
  - *Cognitive Load:* Glanceable top-level operational states; deep Modbus register views segregated for technicians.

---

## 3. Authoritative Color Palette & Tokens

### 3.1 Primary Brand Colors
| Token Name | Hex Code | RGB | Role / Usage |
|---|---|---|---|
| `--se-primary` | `#3DCD58` | `61, 205, 88` | Signature Schneider "Life Is On" Green. Active states, solar power online, primary buttons |
| `--se-primary-hover` | `#32AD3C` | `50, 173, 60` | Interactive hover state for primary green triggers |
| `--yy-deep-forest` | `#024230` | `2, 66, 48` | Deep dark emerald backdrop; typography header accent; brand grounding |
| `--yy-emerald` | `#0D8752` | `13, 135, 82` | Section badges, secondary accents, field capacity status tags |
| `--yy-solar-gold` | `#FFCE00` | `255, 206, 0` | PM-KUSUM Solar peak badges, highlight CTAs, solar irradiance indicators |

### 3.2 Functional & Industrial Status Tokens
| Token Name | Hex Code | RGB | Industrial Semantics |
|---|---|---|---|
| `--color-pump-active` | `#3DCD58` | `61, 205, 88` | Stage 1: Pumping active, VFD operating at 30–50 Hz |
| `--color-cutoff-active` | `#0087CD` | `0, 135, 205` | Stage 2: Root zone saturated; solenoid closed |
| `--color-cold-divert` | `#8015E8` | `128, 21, 232` | Stage 3: TeSys contactor switched; 3.8 kW cold room active |
| `--color-transient` | `#E47F00` | `228, 127, 0` | Passing cloud transient, MPPT throttling |
| `--color-trip-alarm` | `#DC0A0A` | `220, 10, 10` | Motor dry-run alarm, over-temperature, contactor trip |
| `--color-standby` | `#9FA0A4` | `159, 160, 164` | Nighttime / low solar insolation (<200 W/m²) |

### 3.3 Neutrals & Surface Colors (Light Mode Authoritative for Presentation)
| Token Name | Hex Code | Application |
|---|---|---|
| `--surface-canvas-light` | `#F8FAFC` | Primary slide background canvas (off-white / slate-50) |
| `--surface-card-light` | `#FFFFFF` | Container cards, white elevation panels |
| `--border-subtle` | `#E2E8F0` | Subtle card outlines, grid lines, dividers |
| `--text-primary` | `#090B0C` | High-contrast main titles, metric values, headlines |
| `--text-secondary` | `#5C6466` | Subtitles, supporting copy, labels, captions |

---

## 4. Typography System

- **Display & Headings:** `Poppins`, `Arial Rounded MT for SE`, `sans-serif` (Bold 700 / Extrabold 800).
- **Body & Editorial Copy:** `Inter`, `system-ui`, `sans-serif` (Regular 400 / Medium 500 / Semibold 600).
- **Telemetry & Technical Metrics:** `JetBrains Mono`, `monospace` (Semibold 600 / Tabular Figures).
- **Vernacular Scripts (Hindi / Marathi):** `Noto Sans Devanagari`, `Mukta`, `sans-serif`.

### Font Hierarchy:
- **Display Hero:** 48px / line-height 52px / weight 800
- **Heading 1 (H1):** 32px / line-height 38px / weight 700
- **Heading 2 (H2):** 24px / line-height 30px / weight 700
- **Heading 3 (H3):** 18px / line-height 24px / weight 600
- **Body Large:** 16px / line-height 24px / weight 400/500
- **Body Medium:** 14px / line-height 20px / weight 400/500
- **Body Small:** 12px / line-height 16px / weight 400/500
- **Telemetry Mono:** 14px / line-height 18px / weight 600 (tabular numbers)

---

## 5. Spacing, Elevation & Layout Grid

- **8pt Grid Scale:** 4px, 8px, 12px, 16px, 24px, 32px, 48px, 64px.
- **Border Radius:**
  - Badges/chips: 4px (`--radius-sm`)
  - Buttons/inputs: 8px (`--radius-md`)
  - Cards/modals: 12px–16px (`--radius-lg` / `--radius-xl`)
  - Pill tags: 9999px (`--radius-pill`)
- **Elevation / Shadows (Light Theme):**
  - Flat / Flush: `box-shadow: none; border: 1px solid #E2E8F0`
  - Elevation 1 (Card): `box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 1px 2px rgba(0, 0, 0, 0.03)`
  - Elevation 2 (Hover/Active): `box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -1px rgba(0, 0, 0, 0.04)`

---

## 6. UI Components & Visual Metaphors

- **Physical Metaphors:**
  - Solenoid Valves: Open / Closed indicators with flow indicators.
  - Submersible Pump: VFD frequency dial (0–50 Hz) and status badge.
  - TeSys Changeover Contactor: Electromechanical position indicator (Position A: Pump, Position B: Cold Room) with 5-second dead-band sequence.
  - Soil Cross Section: 10cm surface & 30cm root zone depth showing Field Capacity (45%) and Wilting Point (18%).
  - PCM Micro-Cold Room: Thermal buffer status and temperature gauge (12°C setpoint).
- **Iconography:** Lucide SVG icons only. No emojis, no mixed icon styles.

---

## 7. Light / Dark Rules & Presentation Theme Contract

- **Light Canvas Obligation:** The final presentation must use Light Mode (`#F8FAFC` canvas, `#FFFFFF` cards, `#090B0C` text).
- **Prohibited Aesthetics:** No dark futuristic neon cyberpunk styling, no fake glowing wires, no decorative dashboards, no simulated fake telemetry.
- **Required Aesthetic:** Editorial layout discipline, generous white space, photographic storytelling, clear engineering schematics, authoritative typography.
