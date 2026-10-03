# AgroStruxure™ UI Component Library Specifications
**Document Code:** SPEC-COMP-01  
**Project:** AgroStruxure™ (Yuva Yodha 2026 / Schneider Electric India)  
**Author:** Senior Frontend Design Engineer & UX Architect  
**Status:** Complete Implementation Contract  

---

## 1. Design Primitive Components

### 1.1 `Button`
- **Scope:** Primary, secondary, destructive, and icon button triggers.
- **Props Interface:**
  ```typescript
  interface ButtonProps {
    variant: 'primary' | 'secondary' | 'destructive' | 'voice' | 'ghost';
    size: 'sm' | 'md' | 'lg' | 'xl';
    disabled?: boolean;
    loading?: boolean;
    icon?: React.ReactNode;
    children: React.ReactNode;
    onClick?: () => void;
  }
  ```
- **Visual Anatomy & Tokens:**
  - `primary`: Background `var(--se-primary, #3DCD58)`; text `var(--text-on-primary, #090B0C)`; border `none`; border-radius `var(--radius-md, 8px)`.
  - `secondary`: Background `transparent`; text `var(--text-primary)`; border `1px solid var(--border-subtle, #E2E8F0)`.
  - `destructive`: Background `var(--color-trip-alarm, #DC0A0A)`; text `#FFFFFF`; border `none`.
  - `voice`: Pill radius (`9999px`); background `rgba(61, 205, 88, 0.15)`; border `1.5px solid #3DCD58`; text `#0D8752`.
- **States:**
  - `hover`: Lightness shift +10% or overlay `rgba(255, 255, 255, 0.08)`.
  - `active`: Scale down `transform: scale(0.98)`.
  - `focus-visible`: Outline `2px solid #0087CD`, offset `2px`.
  - `disabled`: Opacity `0.45`, cursor `not-allowed`.
  - `loading`: Replaces icon with spinning SVG ring.
- **Accessibility:** `aria-disabled={disabled}`, `aria-busy={loading}`, role `button`.

---

### 1.2 `Badge` / `StatusChip`
- **Scope:** Glanceable status tags for operational states, alarm levels, and communication flags.
- **Props Interface:**
  ```typescript
  interface BadgeProps {
    variant: 'pumping' | 'cutoff' | 'coldroom' | 'transient' | 'alarm' | 'standby';
    size?: 'sm' | 'md';
    pulseDot?: boolean;
    children: React.ReactNode;
  }
  ```
- **Visual Anatomy & Tokens:**
  - Height `24px`; padding `2px 10px`; border-radius `9999px`; font-weight `600`; font-size `12px`.
  - `pumping`: Background `rgba(61, 205, 88, 0.15)`, text `#0D8752`, border `1px solid rgba(61, 205, 88, 0.4)`.
  - `cutoff`: Background `rgba(0, 135, 205, 0.15)`, text `#0087CD`, border `1px solid rgba(0, 135, 205, 0.4)`.
  - `coldroom`: Background `rgba(128, 21, 232, 0.15)`, text `#8015E8`, border `1px solid rgba(128, 21, 232, 0.4)`.
  - `alarm`: Background `rgba(220, 10, 10, 0.15)`, text `#DC0A0A`, border `1px solid rgba(220, 10, 10, 0.4)`.
- **Motion:** When `pulseDot: true`, a 6px circular indicator pulses infinitely (`scale(1.4)`, `opacity: 0` over 1.5s).

---

### 1.3 `Card` / `SurfacePanel`
- **Scope:** Foundation container for all widgets, gauges, and form groupings.
- **Props Interface:**
  ```typescript
  interface CardProps {
    elevation?: 0 | 1 | 2 | 3;
    highlightBorder?: boolean;
    header?: React.ReactNode;
    footer?: React.ReactNode;
    children: React.ReactNode;
    className?: string;
  }
  ```
- **Visual Anatomy & Tokens:**
  - Background `var(--surface-card, #FFFFFF)`; border `0.8px solid var(--border-subtle, #E6E6E6)`; border-radius `var(--radius-lg, 12px)`.
  - Padding: `var(--space-6, 24px)` (desktop), `var(--space-4, 16px)` (mobile).
  - Hover transition: `box-shadow 300ms cubic-bezier(0.4, 0, 0.2, 1)`.

---

## 2. Domain-Specific Industrial Instrumentation Components

### 2.1 `StateIndicatorBanner`
- **Scope:** Declares the microgrid's real-time operational state at the top of the Cockpit.
- **Props Interface:**
  ```typescript
  interface StateIndicatorBannerProps {
    activeState: 'STAGE_1_PUMPING' | 'STAGE_2_CUTOFF' | 'STAGE_3_COLD_DIVERT' | 'TRANSIENT_CLOUD' | 'DRY_RUN_ALARM';
    telemetrySnippet: {
      vfdHz: number;
      solarKw: number;
      soilPct: number;
      coldTempC: number;
    };
  }
  ```
- **Visual Anatomy:**
  - Full-width hero banner with dynamic background gradient tied to active phase.
  - Left: Massive phase icon with pulsing status LED.
  - Middle: High-legibility title and physical description (e.g., *"STAGE 1: SOLAR PUMPING ACTIVE — Altivar ATV320 driving 5HP pump at 48.2 Hz"*).
  - Right: Live parameter chips ($kW$, $Hz$, $\% \text{ FC}$, $°C$).
- **Accessibility:** Configured as an `aria-live="polite"` landmark with `role="region"`.

---

### 2.2 `MicrogridFlowTopology`
- **Scope:** Visualizes live power flow and hydraulic paths dynamically switching between pumping and cold storage.
- **Props Interface:**
  ```typescript
  interface FlowTopologyProps {
    solarKw: number;
    activeLoad: 'PUMP' | 'COLD_ROOM' | 'STANDBY';
    pumpFlowRateLpm: number;
    contactorPosition: 'A' | 'B' | 'TRANSITION';
    interlockActive: boolean;
  }
  ```
- **Visual Anatomy:**
  - Industrial SVG schematic featuring 4 primary nodes:
    1. **Solar PV Array Node:** Displays DC voltage (`540V`) and irradiance.
    2. **Schneider Altivar ATV320 VFD Node:** Displays drive state, frequency, and motor kW.
    3. **Schneider TeSys Contactor Switch Node:** Visual animated rocker contact arm showing Position A (Pump) vs. Position B (Cold Storage).
    4. **Load Nodes:** Submersible Pump and Micro-Cold Storage Room.
  - Animated electron dots flow along active electrical lines using SVG `stroke-dashoffset`.
  - Pulsing water ripples animate inside the irrigation piping when the pump is running.
- **Motion:** Path animation duration is dynamically bound to solar output: $\text{duration} = \max(0.4\text{s}, 2.5\text{s} - (\text{solarKw} \times 0.4\text{s}))$.

---

### 2.3 `DiurnalTimelineScrubber`
- **Scope:** 24-hour interactive time scrubber allowing operators and judges to navigate the farming day.
- **Props Interface:**
  ```typescript
  interface ScrubberProps {
    currentHour: number; // 0.0 to 23.9
    isPlaying: boolean;
    playbackSpeed: 1 | 5 | 30;
    onTimeChange: (hour: number) => void;
    onTogglePlay: () => void;
    onSpeedChange: (speed: 1 | 5 | 30) => void;
  }
  ```
- **Visual Anatomy:**
  - Full-width draggable horizontal track with a solar diurnal backdrop (deep dark night $\to$ golden sunrise at 06:00 $\to$ bright midday solar noon at 12:00 $\to$ twilight at 18:30).
  - Milestone pin markers with hover tooltips:
    - `08:30` Morning Pumping Commences
    - `11:30` Root Field Capacity Reached $\to$ Cutoff & Diversion
    - `15:30` Thermal Storage Shift $\to$ Solar Taper
  - Floating scrub thumb with magnetic snap-to-milestone behavior.
  - Transport dock: Play/Pause button, 1x/5x/30x toggle pills, reset to 08:30 AM button.
- **Accessibility:** Keyboard navigable with `Left/Right` arrow keys adjusting time in 15-minute increments; `Home/End` jumping to sunrise/sunset.

---

### 2.4 `AltivarVfdGauge`
- **Scope:** High-precision radial gauge emulating the Schneider Electric Altivar Solar ATV320 display.
- **Props Interface:**
  ```typescript
  interface VfdGaugeProps {
    frequencyHz: number; // 0.0 to 50.0
    motorAmps: number;
    dcBusVolts: number;
    driveStatus: 'READY' | 'RUNNING' | 'THROTTLED' | 'FAULT';
  }
  ```
- **Visual Anatomy:**
  - Semi-circular 240° dial rendered in SVG with tick marks every 5 Hz.
  - Safe MPPT operating zone highlighted between 32 Hz and 50 Hz.
  - Central readout: Large 36px tabular monospace number (`48.2 Hz`).
  - Secondary digital readout: Motor current (`7.4 A`) and DC voltage (`542 V`).
  - Drive status badge matching Schneider QuartzDS standards.

---

### 2.5 `DualDepthMoistureGauge`
- **Scope:** Root-zone soil hydration indicator eliminating the farmer mental model error of over-pumping.
- **Props Interface:**
  ```typescript
  interface SoilMoistureGaugeProps {
    moisture10cm: number; // %
    moisture30cm: number; // %
    fieldCapacity: number; // e.g., 45%
    wiltingPoint: number; // e.g., 18%
    soilTexture: string;
    isFailoverSatellite: boolean;
  }
  ```
- **Visual Anatomy:**
  - Cross-section illustration showing the plant stem, 10cm topsoil layer, and 30cm deep root zone.
  - Layered water level filling the root zone with color shift:
    - Amber ($<22\%$): Soil Stress (Needs Water).
    - Green ($22\%–44\%$): Optimal Root Hydration.
    - Blue ($\ge 45\%$): Saturated Field Capacity (Cutoff Engaged).
  - Dashed benchmark line marking the exact Field Capacity cutoff target.
  - Failover chip: Displays *"Sentinel-1 SAR Radar"* when satellite estimation is active.

---

### 2.6 `ColdRoomTempGauge`
- **Scope:** Visual thermometer and phase-change thermal storage monitor.
- **Props Interface:**
  ```typescript
  interface ColdRoomGaugeProps {
    chamberTempC: number; // e.g., 4.2°C
    pcmChargePct: number; // 0 to 100%
    cratesStored: number;
    compressorRunning: boolean;
  }
  ```
- **Visual Anatomy:**
  - Vertical cylindrical thermometer gauge measuring $-5°C\text{ to }+30°C$.
  - Target chilling zone ($2°C–6°C$) highlighted with an electric cyan band.
  - Thermal PCM Battery ring: Displays the stored latent cold energy percentage.
  - Perishable produce crate counter badge (`"14 Crates Protected"`).

---

### 2.7 `VernacularVoiceCard`
- **Scope:** Empathetic, grounded rural audio interface delivering non-hallucinatory AI guidance.
- **Props Interface:**
  ```typescript
  interface VoiceCardProps {
    language: 'mr' | 'hi' | 'en';
    audioUrl?: string;
    transcript: string;
    cropName: string;
    waterSavedLiters: number;
    isPlaying: boolean;
    onPlayToggle: () => void;
    onLanguageChange: (lang: 'mr' | 'hi' | 'en') => void;
  }
  ```
- **Visual Anatomy:**
  - WhatsApp-style audio note card with prominent play/pause button.
  - Dynamic audio waveform visualizer (animated SVG bars).
  - Language toggle buttons: `मराठी` (default), `हिंदी`, `English`.
  - Plain Devanagari text transcript with highlighted numerical entities.
  - Direct 1-tap phone button: *"Call Urja Mitra"*.

---

### 2.8 `ModbusRegisterTable`
- **Scope:** Live engineering telemetry inspector for Altivar ATV320 registers.
- **Props Interface:**
  ```typescript
  interface RegisterTableProps {
    registers: Array<{
      address: number;
      name: string;
      rawHex: string;
      scaledValue: string | number;
      unit: string;
      access: 'R' | 'R/W';
      lastUpdated: string;
    }>;
    onWriteRegister?: (address: number, val: number) => void;
  }
  ```
- **Visual Anatomy:**
  - Monospace tabular figures with subtle 1px border grid.
  - Flashing green cell highlight (150ms) when a register receives an updated polling packet.
  - Quick action button to edit writable registers (`8501`, `8502`).
  - Sticky header row with sorting and filtering by register address.
