# Antigravity 2.0 Project Rules — Yuva Yodha / AgroStruxure™

This repository contains the official hackathon research, design system, and presentation decks for **AgroStruxure™** (Yuva Yodha Tech Hackathon 2026).

---

## 1. Installed Skills & Workflow Stack

Antigravity 2.0 is configured with the following focused skill architecture:

1. **`frontend-slides` (Core Presentation Engine)**:
   - Primary engine for creating pitch decks and presentations.
   - Authoring standard: Fixed 16:9 stage (1920×1080) scaled uniformly to viewport using `viewport-base.css`.
   - Equipped with **34 Bold Template Packs** and **88 Layout Presets** (`layout-presets/`).
   - Single-file zero-dependency HTML output with Tailwind CDN and scoped CSS choreography.
2. **`pptx-official` (PPTX Creation & Manipulation)**:
   - Official OOXML script pipeline (`unpack.py`, `pack.py`, `validate.py`, `html2pptx.js`).
   - Use for PowerPoint generation, layout inspection, slide notes, and text extraction.
3. **`pdf-official` (PDF Processing & Verification)**:
   - Document inspection, page verification, table and text extraction, and export verification.
4. **`efficient-web-research` & `deep-research` (Domain & Competitor Research)**:
   - Structured, token-efficient research protocol for problem statements, market data, and regulatory schemes (PM-KUSUM, FAO-56).
5. **`high-end-visual-design` & `ui-visual-validator` (Visual QA & Design System Compliance)**:
   - Strict anti-slop guidelines: bans generic fonts (Inter, Arial, Roboto) and generic purple gradients.
   - Enforces pixel-perfect visual validation and verification before deliverables are marked complete.

---

## 2. Source of Truth & Guidelines

When generating slides, proposals, architecture diagrams, or code:

1. **Design System Source of Truth**:
   - Always adhere to [`DESIGN_SYSTEM.md`](./DESIGN_SYSTEM.md).
   - Core Brand Tokens:
     - Schneider QuartzDS Green: `--se-primary` (`#3DCD58`), hover: `#32AD3C`
     - Yuva Yodha Deep Forest: `--yy-deep-forest` (`#024230`)
     - Yuva Yodha Emerald: `--yy-emerald` (`#0D8752`)
     - Solar Gold: `--yy-solar-gold` (`#FFCE00`)
     - Industrial Surface Dark: `--surface-dark` (`#0F1416`), `--surface-card` (`#1A2226`)
     - Slate Neutral: `#8C9DA8`
   - Physics-grounded industrial metaphors: telemetry indicators, VFD status, Modbus registers, water level bars.
2. **Product Truth & Claim Integrity**:
   - Refer to [`06_PRODUCT_TRUTH.md`](./06_PRODUCT_TRUTH.md) and [`08_CLAIM_LEDGER.md`](./08_CLAIM_LEDGER.md).
   - **Zero Hallucination Mandate**: Never invent metrics, savings percentages, or sensor specifications. All calculations must align with FAO-56 Penman-Monteith physics and PM-KUSUM guidelines.
3. **Asset Registry**:
   - Reference [`ASSET_LEDGER.md`](./ASSET_LEDGER.md) and [`10_IMAGE_ASSET_RESEARCH.md`](./10_IMAGE_ASSET_RESEARCH.md) for approved images and diagrams in `./assets/`.

---

## 3. Deck Generation Workflow

To build or update presentations:
```
[Content & Facts]              [Style & Tokens]
06_PRODUCT_TRUTH.md     +      DESIGN_SYSTEM.md
CLAIM_LEDGER.md                (QuartzDS + Yuva Yodha)
        │                              │
        ▼                              ▼
  frontend-slides  ─────────►  88 Layout Presets / 34 Bold Packs
        │
        ▼
Fixed 16:9 Stage (1920×1080) HTML Presentation
        │
        ├──────────────────────┬──────────────────────┐
        ▼                      ▼                      ▼
  Browser Preview         pptx-official          pdf-official
  (Interactive deck)     (.pptx deliverable)    (.pdf deliverable)
        │
        ▼
ui-visual-validator & high-end-visual-design
(Visual QA: contrast, spacing, zero-overflow, zero-slop)
```
