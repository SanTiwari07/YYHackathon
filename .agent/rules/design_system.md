# AgroStruxure Design System & Deck Generation Rules

## Core Brand & Token Guidelines
- Always load and reference `DESIGN_SYSTEM.md` at project root.
- Primary Brand Color: `#3DCD58` (Schneider Electric "Life Is On" Green)
- Secondary Brand Colors: `#024230` (Yuva Yodha Deep Forest), `#0D8752` (Emerald), `#FFCE00` (Solar Gold)
- Dark Theme Backgrounds: `#0F1416` (industrial slate background), `#1A2226` (card surface), `#242E33` (elevated panels)
- Light Theme Backgrounds: `#F4F7F5` (sage tint surface), `#FFFFFF` (pure white cards), `#E2EAE5` (border tone)

## Presentation Authoring Rules
- **Fixed Stage (16:9 1920×1080)**: Never break 16:9 stage scaling. Use `viewport-base.css` rules.
- **No AI Slop**: Avoid standard fonts (Inter, Arial, Roboto). Use high-character typefaces like Plus Jakarta Sans, Outfit, DM Sans, or Clash Display.
- **Layout Presets**: Prioritize structured layout presets from `frontend-slides/layout-presets` (88 presets) or 34 bold template packs.
- **Visual QA**: Every presentation must undergo visual inspection via `ui-visual-validator` to guarantee no text overflows, overlapping cards, or broken contrast.
