# DESIGN IMPLEMENTATION & ENGINEERING PLAN
**Project:** AgroStruxure™ Presentation Engineering  
**Hackathon:** Yuva Yodha Energy Tech Hackathon 2026 (Schneider Electric India)  
**Standard:** Frontend-Slides Skill Invariants + Schneider QuartzDS (`DESIGN_SYSTEM.md`)  
**Date:** October 3, 2026  
**Document Code:** DES-IMP-2026-V1  

---

## 1. Design Token Mapping (Authoritative `DESIGN_SYSTEM.md`)

```css
:root {
  /* Brand Tokens */
  --se-primary: #3DCD58;       /* Schneider Electric Bright Green */
  --yy-deep-forest: #024230;   /* Yuva Yodha Primary Deep Forest */
  --yy-emerald: #0D8752;       /* Secondary Emerald */
  --yy-solar-gold: #FFCE00;    /* Solar PV Accent / Warning */
  
  /* Industrial Status Tokens */
  --status-pumping: #3DCD58;   /* Green: Irrigation Active */
  --status-cutoff: #0087CD;    /* Blue: Quota / Saturated Cutoff */
  --status-cooling: #8015E8;   /* Purple: Solar Diverted to Cold Storage */
  --status-transient: #E47F00; /* Orange: 5s Dead-Band Dwell */
  --status-alarm: #DC0A0A;     /* Red: Trip / Fault / Depletion */
  --status-standby: #9FA0A4;   /* Grey: Overnight Idle */

  /* Surface Elevation Tokens (Dark Industrial Canvas) */
  --bg-canvas: #0B1115;        /* Deep Industrial Charcoal / Black */
  --bg-card: #151A1C;          /* Elevated Component Surface */
  --bg-panel: #1D2428;         /* High-contrast Panel */
  --border-subtle: #242D32;    /* 1px Structural Dividers */
  --border-focus: #3DCD58;     /* Active Focus / Selection */

  /* Text & Typography Hierarchy */
  --text-primary: #FFFFFF;     /* High-emphasis Readout (100%) */
  --text-secondary: #9FA0A4;   /* Medium-emphasis Labels (70%) */
  --text-muted: #626469;       /* Low-emphasis Captions (50%) */
  --text-accent: #3DCD58;      /* Brand Highlighting */

  /* Typography Families */
  --font-heading: 'Poppins', 'Segoe UI', -apple-system, sans-serif;
  --font-body: 'Segoe UI', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Roboto Mono', monospace;
}
```

---

## 2. Frontend-Slides Skill Invariants

1. **Fixed Stage Dimensions:**
   All slide layouts are constructed strictly within a `1920 × 1080 px` canvas (`aspect-ratio: 16 / 9; width: 1920px; height: 1080px;`).
2. **Viewport Scaling Wrapper:**
   Uniform scaling logic calculates `Math.min(window.innerWidth / 1920, window.innerHeight / 1080)` and applies `transform: scale(...)` to the stage, preventing text reflow, clipping, or viewport wrapping at any display resolution.
3. **Slide State Management:**
   Slide transitions are managed via CSS classes (`.active` / `.visible`) modifying `opacity` and `pointer-events`, preserving CSS Grid / Flexbox geometry without overriding `display: grid` or `display: flex`.
4. **Self-Contained & Zero-Dependency:**
   All SVGs (Lucide icons, Schneider logo, Altivar VFD dial, TeSys contactor, soil moisture columns) are inlined directly into the HTML to ensure zero external network latency, full offline capability, and instant rendering.
5. **Keyboard & Touch Navigation:**
   Supports `ArrowRight`, `ArrowLeft`, `Space`, `Backspace`, `PageDown`, `PageUp`, `Home`, and `End`, along with bottom-right floating HUD controls and slide indicator badges.

---

## 3. Dual Deliverable Pipeline Architecture

```text
[DESIGN_SYSTEM.md + CLAIM_LEDGER.md + SLIDE_SPECIFICATION.md]
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
[presentation.html]                             [01_FINAL_YUVA_YODHA_DECK.pptx]
• Fixed 1920×1080 stage                         • Native python-pptx assembly
• Live interactive CSS gauges                   • 100% editable native shapes & text
• Inline SVG icons & assets                     • Exact RGB hex token matching
• Diurnal timeline scrubber                     • Native tables with cell padding
• Slide navigation & keyboard controls          • High-res photography embeds
        │                                               │
        ▼                                               ▼
[Headless Browser Render]                       [Visual QA & Verification]
• Slide-by-slide PNG capture                    • Text box overflow checks
• 01_FINAL_YUVA_YODHA_DECK.pdf                  • 16:9 widescreen layout lock
• Visual QA & Contact Sheet audit               • Single Source of Truth check
```

---

## 4. PPTX Native Assembly Plan (`python-pptx`)
- **Slide Width & Height:** 13.333 × 7.5 inches (standard 16:9 widescreen).
- **Background:** Solid Fill `#0B1115`.
- **Card Shapes:** Native Rounded Rectangle (`MSO_SHAPE.ROUNDED_RECTANGLE`) with Fill `#151A1C` and Border `#242D32`.
- **Accent Lines:** Thin native shapes with Fill `#3DCD58` (Schneider Green) and `#FFCE00` (Solar Gold).
- **Typography:** Arial / Segoe UI / Trebuchet MS for high cross-platform compatibility without missing-font fallback glitches, with JetBrains Mono / Consolas for telemetry.
- **Data Tables:** Native PPTX Table objects with explicit column widths, cell margins, and custom header fills (`#1D2428`).
- **Images:** Scaled and positioned via inches coordinates, maintaining aspect ratios.
