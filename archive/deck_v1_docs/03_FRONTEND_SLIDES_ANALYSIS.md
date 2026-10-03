# 03 Frontend Slides Analysis: Template Selection & Composition Strategy
**Document ID:** AUDIT-FES-2026-V1  
**Target Repository:** `zarazhangrui/frontend-slides`  
**Reference Assets:** `SKILL.md`, `STYLE_PRESETS.md`, `bold-template-pack/selection-index.json`, `bold-template-pack/templates/blue-professional/design.md`  
**Status:** Ingested & Evaluated  

---

## 1. Executive Summary

The AgroStruxure™ pitch deck requires an elite, human-crafted, consulting-grade visual presence suitable for senior engineering directors at Schneider Electric and climate-tech investors at SE Ventures. It must convey **engineering rigor**, **operational feasibility in rural India**, and **commercial scalability**—without lapsing into AI-generated "neon dashboard slop" or generic corporate clipart.

Frontend Slides provides the structural discipline: fixed 1920×1080 stage architecture, scale-to-fit letterboxing, asymmetric multi-column layouts, editorial hierarchy, and rigorous visual QA. Among all 34 templates in the bold pack and 12 style presets, **Blue Professional** (`templates/blue-professional`) provides the exact compositional blueprint required.

However, **we strictly decouple composition from color identity**:
- **Compositional Inspiration:** Blue Professional (editorial splits, asymmetric stat callouts, restrained cards, high-contrast headline anchors).
- **Visual & Brand Authority:** `DESIGN_SYSTEM.md` (Schneider Green `#3DCD58`, Deep Forest `#024230`, Solar Gold `#FFCE00`, Water Cyan `#0087CD`, Light Canvas `#F8FAFC`, White Cards `#FFFFFF`). Under no circumstances is the deck turned blue.

---

## 2. Template Evaluation Matrix

| Template / System | Strength | Weakness | Use? | Reason |
|---|---|---|:---:|---|
| **Blue Professional** (`bold-template-pack/templates/blue-professional`) | Consulting-grade editorial structure; asymmetric splits; high-contrast metric callouts; medium density without clutter; clean light mode aesthetic. | Color scheme is cobalt blue (#1e2bfa) which conflicts with Schneider Electric green and agricultural identity. | **YES (Composition Only)** | Adopt editorial card layouts, stat blocks, and two-column split rhythm. Substitute colors with AgroStruxure design tokens. |
| **Terminal Green** (`STYLE_PRESETS.md #10`) | Authentic engineering feel; strong developer credibility; monospaced precision. | Dark theme; reads like a CLI or hacker tool; illegible for business/market judges; lacks photographic warmth. | **NO** | Disqualified by anti-AI-slop rule and light theme mandate. Monospace restricted to tabular Modbus registers only. |
| **Neon Cyber / 8-Bit Orbit** (`STYLE_PRESETS.md #9`) | High hackathon energy; vibrant accents. | Quintessential AI slop; dark neon glow; illegible in daylight; destroys industrial Schneider credibility. | **NO** | Violates core requirement against dark futuristic neon aesthetic. |
| **Swiss Modern** (`STYLE_PRESETS.md #11`) | Bauhaus minimalism; disciplined typography; strong grid structure; light background. | Can feel overly stark, abstract, and academic; lacks domain warmth and physical agricultural imagery. | **PARTIAL** | Adopt its strict 8pt grid alignment and typographic hierarchy, but pair with real photography and rich industrial diagrams. |
| **Notebook Tabs** (`STYLE_PRESETS.md #5`) | Tactile editorial feel; organized section tabs; warm paper surface. | Skewmorphic binder tabs consume valuable 1920×1080 horizontal real estate; distracting for technical jury. | **NO** | Clean top breadcrumb navigation is superior for 10-slide executive pitch. |

---

## 3. Structural Rules Adopted from Frontend Slides

1. **Fixed 1920×1080 Canvas Architecture:**
   - Every slide is strictly contained within a root `.slide` element sized `width: 1920px; height: 1080px; position: relative; overflow: hidden;`.
   - Responsive scaling is handled via CSS `transform: scale(...)` inside `#presentation-viewport` centered in the window, preventing broken mobile reflows.
2. **Anti-AI-Slop Compositional Principles:**
   - **Zero Center Alignment for Body Content:** Headings and narrative text are left-aligned against deliberate structural margins (padding: `72px 80px`).
   - **Intentional Asymmetry:** 50/50, 60/40, or 35/65 asymmetric splits pairing crisp technical architecture or metrics with authentic high-resolution agricultural photography.
   - **No Gratuitous Glassmorphism or Neon Borders:** Cards use clean white `#FFFFFF` surfaces with crisp 1px borders (`#E2E8F0`) and subtle shadows (`rgba(0,0,0,0.04)`).
   - **No Emojis:** Functionally necessary symbols use single-library Lucide SVG icons with exact 16px/20px sizing.
3. **Typographic Rhythm:**
   - Display/Headings: Poppins (Bold 700 / Extrabold 800) with tight line height (1.1–1.15) and subtle negative tracking (`-0.02em`).
   - Body/Narrative: Inter (Regular 400 / Medium 500) with generous line height (1.5–1.6) for effortless scannability.
   - Numbers & Registers: JetBrains Mono with tabular figures (`font-variant-numeric: tabular-nums`).

---

## 4. Visual QA & Verification Standard

The frontend-slides skill enforces automated visual verification before sign-off:
- Slide-by-slide rendering to full-resolution 1920×1080 PNG images (`slide_01.png` to `slide_10.png`).
- Explicit automated checks for:
  1. Content clipping, text overflow, or horizontal/vertical scrollbars.
  2. Contrast compliance against WCAG 2.1 AA (minimum 4.5:1 for body, 7:1 for headers).
  3. Image aspect ratio integrity (no stretched or distorted photos).
  4. Typographic collisions between headings and cards.
