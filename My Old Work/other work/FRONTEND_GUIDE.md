# Pragya Frontend Architecture & Compatibility Guide

> **The Single Source of Truth for Frontend Engineering, Component Design, and Asset Management.**  
> *Every feature, refactor, and AI-driven update must strictly comply with this specification.*

---

## 1. Quickstart & Environment Setup

### 1.1 Prerequisites
- **Node.js**: `v18.0.0` or higher (Recommended: `v20.x` or `v22.x LTS`)
- **Package Manager**: `npm` (v9+)
- **OS**: Windows, macOS, or Linux

### 1.2 Installation & Execution
```bash
# Navigate to the frontend directory
cd frontend

# Install all dependencies exactly as pinned
npm install

# Start local development server (default: http://localhost:5173)
npm run dev

# Run automated architecture & asset compliance verification
npm run verify

# Build for production
npm run build

# Preview production build locally
npm run preview
```

---

## 2. Core Dependencies & Stack Overview

| Category | Library | Version | Purpose & Usage |
| :--- | :--- | :--- | :--- |
| **Framework** | `react`, `react-dom` | `^19.2.4` | Core React 19 framework |
| **Build Tool** | `vite` | `^8.0.4` | Ultra-fast build & HMR server |
| **Routing** | `react-router-dom` | `^7.18.0` | Client-side routing (`/`, `/login`, `/analysis`, `/onboarding/*`) |
| **Styling** | `tailwindcss`, `postcss`, `autoprefixer` | `^3.4.19` | Utility-first CSS engine |
| **Tailwind Utils** | `clsx`, `tailwind-merge`, `cva` | Latest | Dynamic class merging (`cn()` utility) |
| **3D Engine** | `three`, `@react-three/fiber`, `@react-three/drei` | `^0.186`, `^9.8`, `^10.7` | WebGL 3D diorama with Draco mesh compression |
| **Mapping & GIS**| `leaflet`, `react-leaflet`, `leaflet-draw`, `@turf/turf` | `^1.9`, `^5.0`, `^1.0`, `^7.3` | Interactive satellite maps, farm polygon drawing & centroid calculations |
| **Icons** | `lucide-react` | `^1.7.0` | Consistent 16px/20px iconography |
| **Networking** | `axios` | `^1.18.1` | REST client with automatic JWT token attachment |
| **Auth** | `firebase` | `^12.19.0` | Firebase Phone OTP verification |
| **Charts** | `recharts` | `^3.8.1` | Vegetation index temporal trend graphs |

---

## 3. Directory Structure & File Placement Rules

```
frontend/
├── index.html                     # HTML5 entrypoint with Google Fonts
├── vite.config.js                 # Vite configuration with proxy rules
├── tailwind.config.js             # Tailwind colors, shadows, and animations
├── package.json                   # Dependencies, build & verify scripts
│
├── public/                        # Static assets served at root /
│   ├── favicon.svg                # Browser favicon
│   ├── banner/                    # Static UI backdrops (farmer, fields, satellites)
│   ├── draco/gltf/                # WebAssembly Draco decoders for .glb models
│   │   ├── draco_decoder.wasm
│   │   ├── draco_decoder.js
│   │   └── draco_wasm_wrapper.js
│   └── models/                    # 3D GLTF/GLB models & textures
│       ├── earth.glb
│       ├── farm.glb
│       └── satellite.glb
│
├── scripts/                       # Automation, CI verification, and test scripts
│   ├── verify-frontend.mjs        # Automated compliance test suite (npm run verify)
│   ├── optimize-models.mjs        # Draco 3D mesh compressor
│   └── capture-*.mjs              # Headless browser render inspection tools
│
└── src/
    ├── main.jsx                   # React root mount
    ├── App.jsx                    # Root router with ProtectedRoute guards
    ├── index.css                  # Global design tokens, font definitions, scrollbars
    ├── analysis.css               # Map viewport and analysis layout styling
    │
    ├── assets/                    # Project source assets
    │   ├── hero.png               # Static fallback images
    │   └── captures/              # Organized screenshots & render outputs
    │       ├── hero/              # 3D scene renders and blend verification
    │       ├── farm/              # Farm zoom and mesh resolution captures
    │       ├── earth/             # Globe multi-angle snapshots
    │       └── debug/             # Canvas clip test files
    │
    ├── components/                # DOMAIN-SEPARATED COMPONENTS
    │   ├── ui/                    # HeroUI v3 Atomic Design System (ProgressCircle, Button, etc.)
    │   ├── map/                   # MapView, HeatmapLayer, Legend, TimelineBar, LocationForm
    │   ├── assistant/             # Krishi Mitra AI Chatbot, Sidebar, FarmSummary
    │   ├── analysis/              # LoadingOverlay, NavbarDropdown, FieldNameModal
    │   ├── auth/                  # PremiumAuthFlow, AuthModal
    │   ├── 3d/                    # Hero3DScene, DioramaModels, VolumetricSpotlight
    │   └── [onboarding]/          # FarmCard, DataPanel, InputField, SelectField
    │
    ├── context/                   # React Context Providers (OnboardingContext)
    ├── api/                       # API clients (axios instance, auth, farm, weather)
    ├── utils/                     # Pure mathematical/GIS helpers (colorUtils.js, firestore.js)
    └── lib/                       # Utility helpers (utils.js -> cn())
```

> [!IMPORTANT]
> **Zero Loose File Rule:** Never dump `.png`, `.jpg`, `.txt`, or scratch scripts into the `frontend/` root or `frontend/src/` root.
> - Visual captures **must** go to `src/assets/captures/<category>/`.
> - 3D models **must** go to `public/models/`.
> - Components **must** go to their appropriate `src/components/<domain>/` subfolder.

---

## 4. HeroUI v3 Design System Standards

Pragya follows the official **HeroUI v3** specification combined with **Apple Human Interface Design Principles**.

### 4.1 Strict Compound Component Anatomy
HeroUI v3 uses compound sub-components rather than flat property configurations:

```jsx
// ✅ CORRECT: HeroUI v3 Compound Pattern
import { ProgressCircle } from '../components/ui/progress-circle';

<ProgressCircle value={85} color="accent">
  <ProgressCircle.Track>
    <ProgressCircle.TrackCircle />
    <ProgressCircle.FillCircle />
  </ProgressCircle.Track>
</ProgressCircle>
```

```jsx
// ❌ WRONG: Legacy v2 Flat / Provider Pattern
import { Progress } from '@heroui/react';
<Progress value={85} /> // DO NOT DO THIS
```

### 4.2 Available Design System Components (`src/components/ui/`)
- `ProgressCircle`: High-precision circular progress gauge with SVG stroke calibration.
- `Button`: Clean tactile buttons with active scale micro-interactions.
- `Card`: Surface cards with Apple-style subtle hairline borders (`border-slate-200/80`).
- `Badge`: Status badges for indices, online presence, and category tags.
- `Chip`: Filter chips and metric chips.
- `Dialog`: Modals, confirm dialogs, and slide-over sheets.
- `TextField`: Calibrated form inputs with floating labels and state error rings.
- `Tabs`: Smooth pill tab bars with sliding highlight states.
- `MetricCard`: Farm telemetry cards (Vegetation Index, Soil Moisture, Health Confidence).

---

## 5. Design Philosophy & UI/UX Rules

### 5.1 Color Tokens & Theme Contract
Pragya uses an **Enterprise Light Canvas**. Never render dark backgrounds, pitch-black containers, or low-contrast washed-out grey boxes:
- **Canvas / Background**: Clean White (`#FFFFFF`) and Soft Slate (`#F8FAFC`).
- **Surface Elevation**: `#FFFFFF` with hairline border `border-slate-200/90` and multi-layered soft drop shadows (`shadow-[0_12px_32px_-4px_rgba(15,23,42,0.18)]`).
- **Brand Primary Accent**: Agriculture Emerald:
  - Deep Brand: `#065F2C`
  - Active / Interactive: `#059669` / `emerald-600`
  - Focus Ring / Glow: `emerald-500/20`
  - Subtle Badges: `bg-emerald-50 text-emerald-800 border-emerald-200/60`

### 5.2 Typography Contract
- **Font Stack**: `Inter`, `SF Pro Display`, `-apple-system`, `system-ui`, `sans-serif`.
- **Numbers & Gauges**: **NEVER use monospaced fonts (`font-mono`)** inside circular progress gauges, telemetry cards, or user badges. Monospace creates blocky, retro, unaligned text.
- **Tabular Figures**: Always apply `tabular-nums` so numbers align cleanly without character jitter during animations.

### 5.3 Leaflet Map Z-Index Guard
Leaflet manages an internal stack of layers:
- Marker pane: `z-index: 600`
- Popup pane: `z-index: 700`
- Control pane: `z-index: 800`
- Top/Bottom controls: `z-index: 1000`

> [!CAUTION]
> Any custom floating button, modal, or overlay placed over `<MapView />` **must** specify:
> ```html
> className="... z-[9999] pointer-events-auto ..."
> ```
> Failure to set `z-[9999]` causes Leaflet's invisible canvas panes to intercept clicks or hide the UI element.

### 5.4 Panel Collapse & Multi-Channel Restoration
When any collapsible side panel (like Krishi Mitra) collapses to width 0:
1. **Top Navbar Button**: Must have a persistent Assistant toggle button next to the logo.
2. **Floating Pill**: Must display an Apple-style floating trigger on the map canvas (`z-[9999]`).
3. **Left Seam Dock Handle**: Must provide a vertical edge seam button (`left-0 top-1/2`).
4. **Keyboard Shortcut**: Must support `Ctrl + B` / `Cmd + B` globally.

---

## 6. The Frontend Compatibility Checklist

Before committing or submitting any code change, verify that every item on this checklist is satisfied:

```markdown
### Phase 1: Dependencies & Environment
- [ ] No extraneous unpinned packages added to `package.json`.
- [ ] Application starts cleanly via `npm run dev` with zero console errors.

### Phase 2: Architecture & File Placement
- [ ] Zero loose files (.png, .jpg, .webp, .txt, .mjs) in `frontend/` or `frontend/src/` root.
- [ ] New components placed in `src/components/<domain>/` with a barrel export in `index.js`.
- [ ] New visual renders/captures routed to `src/assets/captures/<category>/`.
- [ ] Static 3D models placed in `public/models/`.

### Phase 3: Design & HeroUI Conformity
- [ ] Strict white / emerald design theme maintained (no dark-mode regressions).
- [ ] HeroUI compound component anatomy used for gauges, buttons, cards, and dialogs.
- [ ] No `font-mono` inside circular progress gauges or telemetry cards.
- [ ] All floating elements over the map use `z-[9999] pointer-events-auto`.
- [ ] Sidebar toggle supports all 4 restoration triggers (Navbar, Floating Pill, Seam, Ctrl+B).

### Phase 4: Automated Verification
- [ ] `npm run verify` runs and reports 10/10 PASS.
- [ ] `npm run build` generates production bundle in under 5 seconds with zero syntax or build errors.
```

---

## 7. Automated Verification Suite (`npm run verify`)

To ensure that future commits and AI pairs strictly maintain this standard without manual effort, run:

```bash
npm run verify
```

The verification engine performs:
1. **Asset Cleanliness Check**: Asserts that no loose images or dumps exist in the root.
2. **Directory Integrity Check**: Validates that all domain component folders (`ui`, `map`, `assistant`, `analysis`, `auth`, `3d`) and capture folders exist.
3. **Static Model Presence**: Verifies `earth.glb`, `farm.glb`, `satellite.glb`, and Draco decoders.
4. **Production Build Validation**: Executes a clean Rollup/Vite build to verify imports and bundle integrity.

*If any check fails, the script returns exit code 1 with actionable failure messages specifying exactly what file or folder needs correction.*
