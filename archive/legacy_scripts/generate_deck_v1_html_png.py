# -*- coding: utf-8 -*-
"""
AgroStruxure™ Master Presentation Engine — Pass 2 Refinement
Yuva Yodha Energy Tech Hackathon 2026 — Schneider Electric India
Pixel-perfect visual refinement addressing all Pass 1 QA findings:
- Eliminates all mangled LaTeX/f-string characters (unicode arrows)
- Fills unintentional dead space with authentic engineering schematics and data
- Adds physical drip photo inset, Pydantic JSON snippet, and cashflow charts
- Continuous horizontal roadmap progression
- Authentic superscript brand marks and typography
"""

import os
import base64
import subprocess
import shutil
from PIL import Image
import pptx
from pptx.util import Inches

BASE_DIR = r"D:\Research Work\YuvaYodhaHackathon Research"
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOURCE_DIR = os.path.join(BASE_DIR, "presentation", "source")
SLIDES_DIR = os.path.join(SOURCE_DIR, "slides")
QA_DIR = os.path.join(BASE_DIR, "presentation", "qa")
FINAL_DIR = os.path.join(BASE_DIR, "presentation", "final")
RENDERED_DIR = os.path.join(BASE_DIR, "rendered_slides")

for d in [SOURCE_DIR, SLIDES_DIR, QA_DIR, FINAL_DIR, RENDERED_DIR]:
    os.makedirs(d, exist_ok=True)

def encode_file(path, mime):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode('utf-8')}"

print("Step 1: Encoding high-res visual assets...")
IMG_SOLAR = encode_file(os.path.join(ASSETS_DIR, "solar_panels_farm_opt.jpg"), "image/jpeg")
IMG_FIELD = encode_file(os.path.join(ASSETS_DIR, "indian_agriculture_field.jpg"), "image/jpeg")
IMG_DRIP = encode_file(os.path.join(ASSETS_DIR, "drip_irrigation_farm.jpg"), "image/jpeg")
IMG_TOMATO = encode_file(os.path.join(ASSETS_DIR, "tomato_harvest.jpg"), "image/jpeg")
SVG_LOGO = encode_file(os.path.join(ASSETS_DIR, "schneider_electric_logo.svg"), "image/svg+xml")

# Common Head with Google Fonts
HTML_HEAD = """
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1920, height=1080, initial-scale=1.0">
  <title>AgroStruxure™ | Yuva Yodha 2026</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      width: 1920px;
      height: 1080px;
      overflow: hidden;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      background: #F8FAFC;
      color: #0F172A;
    }
    .font-mono { font-family: 'JetBrains Mono', monospace; }
    .font-display { font-family: 'Space Grotesk', sans-serif; }
    .font-devanagari { font-family: 'Noto Sans Devanagari', sans-serif; }
    
    :root {
      --se-primary: #3DCD58;
      --se-primary-hover: #32AD3C;
      --yy-deep-forest: #024230;
      --yy-emerald: #0D8752;
      --yy-solar-gold: #FFCE00;
      --color-water: #0087CD;
      --color-cold-room: #8015E8;
      --color-transient: #E47F00;
      --color-alarm: #DC0A0A;
      --surface-dark-canvas: #0B1115;
      --surface-dark-card: #13191C;
      --surface-dark-panel: #1A2226;
      --border-dark: rgba(255, 255, 255, 0.08);
      --surface-light-canvas: #F8FAFC;
      --surface-light-card: #FFFFFF;
      --border-light: #E2E8F0;
    }

    .slide-stage {
      width: 1920px;
      height: 1080px;
      position: relative;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
  </style>
"""

# ==============================================================================
# SLIDE 01: HERO / EXECUTIVE VISION (Refined)
# ==============================================================================
SLIDE_01 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .hero-container {{
      display: grid;
      grid-template-columns: 53% 47%;
      height: 1080px;
      width: 1920px;
      position: relative;
      background: #F8FAFC;
    }}
    .hero-content {{
      padding: 64px 76px 56px 84px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      z-index: 2;
    }}
    .hero-visual {{
      position: relative;
      height: 1080px;
      overflow: hidden;
      background: #0B1115;
    }}
    .hero-img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      filter: saturate(1.05) contrast(1.02);
    }}
    .hero-gradient-overlay {{
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(90deg, rgba(248,250,252,1) 0%, rgba(248,250,252,0) 8%, rgba(11,17,21,0.2) 60%, rgba(11,17,21,0.88) 100%);
    }}
    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 12px;
      padding: 8px 16px;
      background: #E8F8ED;
      border: 1px solid #B7EBC4;
      border-radius: 6px;
      color: #024230;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      width: fit-content;
    }}
    .hero-badge .dot {{
      width: 8px; height: 8px; border-radius: 50%; background: #3DCD58;
    }}
    .hero-title {{
      font-size: 80px;
      font-weight: 700;
      line-height: 0.95;
      letter-spacing: -0.03em;
      color: #024230;
      margin-top: 24px;
      margin-bottom: 12px;
    }}
    .hero-title sup {{
      font-size: 32px;
      color: #0D8752;
      font-weight: 600;
      vertical-align: super;
      margin-left: 4px;
    }}
    .hero-sub {{
      font-size: 25px;
      font-weight: 600;
      color: #0D8752;
      line-height: 1.3;
      letter-spacing: -0.01em;
      margin-bottom: 24px;
    }}
    .hero-hook-quote {{
      border-left: 4px solid #3DCD58;
      padding-left: 20px;
      font-size: 28px;
      font-weight: 700;
      color: #0F172A;
      line-height: 1.35;
      margin-bottom: 20px;
    }}
    .hero-desc {{
      font-size: 18px;
      color: #475569;
      line-height: 1.55;
      max-width: 820px;
      margin-bottom: 28px;
    }}
    .hero-stats-row {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 32px;
      padding-top: 24px;
      border-top: 2px solid #E2E8F0;
      margin-bottom: 28px;
    }}
    .hero-stat-item {{
      display: flex;
      flex-direction: column;
    }}
    .hero-stat-val {{
      font-size: 54px;
      font-weight: 700;
      line-height: 1;
      letter-spacing: -0.03em;
      font-family: 'Space Grotesk', sans-serif;
      display: flex;
      align-items: baseline;
      gap: 4px;
    }}
    .val-green {{ color: #0D8752; }}
    .val-gold {{ color: #D97706; }}
    .val-purple {{ color: #7C3AED; }}
    .hero-stat-label {{
      font-size: 14px;
      font-weight: 700;
      color: #1E293B;
      margin-top: 6px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .hero-stat-desc {{
      font-size: 13px;
      color: #64748B;
      margin-top: 4px;
      line-height: 1.35;
    }}
    .hero-team-bar {{
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 14px 20px;
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      font-size: 13px;
      color: #334155;
    }}
    .hero-team-bar strong {{ color: #024230; }}
    .hud-card {{
      position: absolute;
      bottom: 48px;
      right: 48px;
      background: rgba(11, 17, 21, 0.88);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 10px;
      padding: 24px 28px;
      color: #FFFFFF;
      max-width: 440px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.5);
    }}
    .hud-tag {{
      display: inline-block;
      font-size: 11px;
      font-weight: 700;
      color: #3DCD58;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 8px;
    }}
    .hud-title {{
      font-size: 18px;
      font-weight: 700;
      line-height: 1.3;
      margin-bottom: 12px;
    }}
    .hud-telemetry {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      color: #94A3B8;
    }}
    .hud-telemetry strong {{ color: #FFFFFF; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="hero-container">
    <div class="hero-content">
      <div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
          <div class="hero-badge">
            <span class="dot"></span>
            Yuva Yodha 2026 • Challenge 01: Sustainable Agriculture
          </div>
          <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 38px; width: auto;">
        </div>
        
        <h1 class="hero-title font-display">AgroStruxure<sup>™</sup></h1>
        <h2 class="hero-sub font-display">Solar-Synchronized Agri-Energy Microgrid & Precision Irrigation</h2>
        
        <div class="hero-hook-quote">
          "One solar pump can become a rural energy node."
        </div>
        
        <p class="hero-desc">
          Decoupling agricultural water pumping from free solar energy to eliminate the <strong>Solar Rebound Paradox</strong> across 10.9 lakh PM-KUSUM installations. AgroStruxure dynamically diverts idle midday solar generation into farm-gate thermal pre-cooling while automating closed-loop groundwater conservation.
        </p>
      </div>

      <div>
        <div class="hero-stats-row">
          <div class="hero-stat-item">
            <div class="hero-stat-val val-green">41.2%</div>
            <div class="hero-stat-label">Water Conserved</div>
            <div class="hero-stat-desc">7,000 m³/ha/yr preserved via dual-depth soil cutoff</div>
          </div>
          <div class="hero-stat-item">
            <div class="hero-stat-val val-gold">4,137 <span style="font-size: 26px; font-weight: 600;">kWh</span></div>
            <div class="hero-stat-label">Solar Surplus Captured</div>
            <div class="hero-stat-desc">63% wasted PV redirected to 2 MT pre-cooling</div>
          </div>
          <div class="hero-stat-item">
            <div class="hero-stat-val val-purple">2.0 <span style="font-size: 26px; font-weight: 600;">Yrs</span></div>
            <div class="hero-stat-label">Cluster Payback</div>
            <div class="hero-stat-desc">Tier A 4-farm asset sharing at ₹50,212/farm capex</div>
          </div>
        </div>

        <div class="hero-team-bar">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0D8752" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>
          <div><strong>Core Engineering Team:</strong> Sanskar Tiwari (Firmware/Lead) • Shambhavi Patil (Geospatial) • Kanishka Salgude (Power/VFD) • Chaitanya Ranade (Agronomy/Product)</div>
        </div>
      </div>
    </div>

    <div class="hero-visual">
      <img src="{IMG_SOLAR}" alt="Agricultural Solar Array" class="hero-img">
      <div class="hero-gradient-overlay"></div>
      
      <div class="hud-card">
        <div class="hud-tag">Field Asset Architecture</div>
        <div class="hud-title font-display">PM-KUSUM Component B: 4.8 kWp Standalone PV</div>
        <p style="font-size: 13px; color: #CBD5E1; line-height: 1.45; margin-bottom: 12px;">
          Ground-mounted perimeter array powering 3-phase submersible pump with automated upstream DC changeover to 2 MT thermal PCM cold storage.
        </p>
        <div class="hud-telemetry">
          <div>PV Array: <strong>4.8 kWp (DC)</strong></div>
          <div>Annual Yield: <strong>6,559 kWh</strong></div>
          <div>Bus Voltage: <strong>350–600V DC</strong></div>
          <div>Telemetry: <strong>Modbus RTU / 4G</strong></div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>"""

# ==============================================================================
# SLIDE 02: SPLIT CAUSAL CHAIN (Refined with Connectors)
# ==============================================================================
SLIDE_02 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .slide-body {{
      padding: 56px 80px 48px 80px;
      height: 1080px;
      width: 1920px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #F8FAFC;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .tag-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #991B1B;
      background: #FEE2E2;
      border: 1px solid #FECACA;
      padding: 6px 14px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .slide-hook {{
      font-size: 52px;
      font-weight: 700;
      color: #0F172A;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .slide-sub {{
      font-size: 20px;
      color: #475569;
      line-height: 1.45;
      max-width: 1200px;
      margin-bottom: 28px;
    }}
    .causal-grid {{
      display: grid;
      grid-template-columns: 34% 66%;
      gap: 36px;
      align-items: stretch;
      flex: 1;
    }}
    .ground-reality-card {{
      position: relative;
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 32px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.08);
      background: #0B1115;
    }}
    .ground-reality-card img {{
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover;
      opacity: 0.85;
    }}
    .ground-reality-overlay {{
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(180deg, rgba(11,17,21,0.2) 0%, rgba(11,17,21,0.92) 80%);
    }}
    .ground-reality-content {{
      position: relative;
      z-index: 2;
      color: #FFFFFF;
    }}
    .chain-container {{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 12px;
    }}
    .chain-node {{
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 22px 28px;
      display: grid;
      grid-template-columns: 80px 1fr 180px;
      align-items: center;
      gap: 24px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
      position: relative;
    }}
    .chain-node-num {{
      width: 64px;
      height: 64px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
    }}
    .num-water {{ background: #E0F2FE; color: #0284C7; }}
    .num-energy {{ background: #FEF3C7; color: #D97706; }}
    .num-spoilage {{ background: #F3E8FF; color: #7E22CE; }}
    .node-title {{
      font-size: 19px;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 6px;
    }}
    .node-desc {{
      font-size: 14px;
      color: #475569;
      line-height: 1.45;
    }}
    .node-metric {{
      text-align: right;
      padding-left: 16px;
      border-left: 1px solid #E2E8F0;
    }}
    .metric-val {{
      font-size: 38px;
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
      line-height: 1;
    }}
    .metric-unit {{
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-top: 4px;
    }}
    .color-water {{ color: #0284C7; }}
    .color-energy {{ color: #D97706; }}
    .color-spoilage {{ color: #7E22CE; }}
    .causal-arrow {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      color: #94A3B8;
      padding: 2px 0;
    }}
    .footer-bar {{
      padding-top: 16px;
      border-top: 1px solid #E2E8F0;
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #64748B;
    }}
  </style>
</head>
<body>
  <div class="slide-body">
    <div>
      <div class="header-bar">
        <div class="tag-pill">Problem Space • The Systemic Rebound Effect</div>
        <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 34px; width: auto;">
      </div>
      <h1 class="slide-hook font-display">Free Solar Power Accelerates Groundwater Collapse</h1>
      <p class="slide-sub">
        Under PM-KUSUM Component B, zero marginal electricity cost removes the economic friction on pumping, triggering a triple cascading bottleneck across water reserves, clean energy utility, and smallholder income.
      </p>
    </div>

    <div class="causal-grid">
      <div class="ground-reality-card">
        <img src="{IMG_FIELD}" alt="Indian Agriculture Field">
        <div class="ground-reality-overlay"></div>
        <div class="ground-reality-content">
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: #3DCD58; text-transform: uppercase; margin-bottom: 8px;">
            The Semi-Arid Ground Truth
          </div>
          <h3 class="font-display" style="font-size: 24px; font-weight: 700; line-height: 1.25; margin-bottom: 12px;">
            Marathwada & Vidarbha Groundwater Crisis
          </h3>
          <p style="font-size: 14px; color: #E2E8F0; line-height: 1.5;">
            CGWB National Ground Water Report 2023: Water table decline exceeds <strong>2.5 meters/year</strong> in 31% of semi-arid assessment units. When subsidized solar pumps run 8–10 hours daily without metering, the aquifer becomes an open-access sink.
          </p>
        </div>
      </div>

      <div class="chain-container">
        <!-- Node 1 -->
        <div class="chain-node">
          <div class="chain-node-num num-water">01</div>
          <div>
            <div class="node-title font-display">Unconstrained Extraction & Root Waterlogging</div>
            <div class="node-desc">
              Farmers operate pumps whenever sunlight is available (850 mm/season across flood basins). This floods root zones, inducing hypoxia, fungal collar rot, nutrient leaching, and massive aquifer depletion without yielding additional crop tonnage.
            </div>
          </div>
          <div class="node-metric">
            <div class="metric-val color-water">17,000</div>
            <div class="metric-unit color-water">m³/ha/yr Extracted</div>
          </div>
        </div>

        <div class="causal-arrow">
          <span>&darr;</span> ZERO PUMPING FRICTION SATURATES FIELD STORAGE WITHOUT COLD CHAIN <span>&darr;</span>
        </div>

        <!-- Node 2 -->
        <div class="chain-node">
          <div class="chain-node-num num-energy">02</div>
          <div>
            <div class="node-title font-display">4,137 kWh of Solar Energy Wasted Idle Annually</div>
            <div class="node-desc">
              A 4.8 kWp standalone array generates 6,559 kWh/year. Pumping only requires 2,422 kWh/year. Corroborating IWMI findings (Shah et al.), <strong>nearly two-thirds of capital-subsidized solar power sits unused</strong> once storage ditches reach capacity.
            </div>
          </div>
          <div class="node-metric">
            <div class="metric-val color-energy">63.1%</div>
            <div class="metric-unit color-energy">Solar Energy Curtailment</div>
          </div>
        </div>

        <div class="causal-arrow">
          <span>&darr;</span> UNSTABLE FIELD HEAT ACCELERATES POST-HARVEST RESPIRATION <span>&darr;</span>
        </div>

        <!-- Node 3 -->
        <div class="chain-node">
          <div class="chain-node-num num-spoilage">03</div>
          <div>
            <div class="node-title font-display">8.37% Farm-Gate Spoilage from Missing Cold Chain</div>
            <div class="node-desc">
              Per NABCONS 2022 Post-Harvest Loss Study, 8.37% of harvested tomatoes rot before leaving the farm gate due to extreme 32°C respiration heat. Farmers face severe distress selling at local mandis (₹2–₹4/kg vs ₹12/kg market benchmark).
            </div>
          </div>
          <div class="node-metric">
            <div class="metric-val color-spoilage">8.37%</div>
            <div class="metric-unit color-spoilage">Perishable Crop Lost</div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar font-mono">
      <div>Data Sources: Central Ground Water Board (CGWB 2023) • NABCONS 2022 MoFPI Baseline • Shah et al. (IWMI)</div>
      <div>AgroStruxure™ Problem Audit • Slide 02 / 10</div>
    </div>
  </div>
</body>
</html>"""

# ==============================================================================
# SLIDE 03: INDUSTRIAL SCHEMATIC (Refined: Vector Traces, No LaTeX Glitches)
# ==============================================================================
SLIDE_03 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .slide-body {{
      padding: 52px 76px 44px 76px;
      height: 1080px;
      width: 1920px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #0B1115;
      color: #FFFFFF;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
    }}
    .tag-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #3DCD58;
      background: rgba(61, 205, 88, 0.12);
      border: 1px solid rgba(61, 205, 88, 0.3);
      padding: 6px 14px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .slide-hook {{
      font-size: 48px;
      font-weight: 700;
      color: #FFFFFF;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 6px;
    }}
    .slide-hook span {{ color: #3DCD58; }}
    .slide-sub {{
      font-size: 19px;
      color: #94A3B8;
      line-height: 1.4;
      max-width: 1280px;
      margin-bottom: 22px;
    }}
    .schematic-canvas {{
      flex: 1;
      background: #11171B;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 26px 28px;
      display: grid;
      grid-template-columns: 28% 44% 28%;
      gap: 24px;
      position: relative;
    }}
    .schematic-col {{
      display: flex;
      flex-direction: column;
      gap: 14px;
      justify-content: space-between;
    }}
    .col-title {{
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 2px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .col-inputs-title {{ color: #0087CD; }}
    .col-brain-title {{ color: #3DCD58; }}
    .col-loads-title {{ color: #FFCE00; }}
    
    .tech-box {{
      background: #172026;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 16px 18px;
      position: relative;
    }}
    .tech-box-highlight {{
      border: 1.5px solid #3DCD58;
      background: #152520;
    }}
    .box-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}
    .box-name {{
      font-size: 16px;
      font-weight: 700;
      color: #FFFFFF;
    }}
    .box-protocol {{
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      padding: 2px 8px;
      border-radius: 4px;
      background: rgba(255,255,255,0.08);
      color: #94A3B8;
    }}
    .box-list {{
      font-size: 13px;
      color: #94A3B8;
      line-height: 1.45;
      padding-left: 18px;
    }}
    .box-list li {{ margin-bottom: 4px; }}
    .box-list strong {{ color: #E2E8F0; }}

    .footer-bar {{
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #64748B;
    }}
  </style>
</head>
<body>
  <div class="slide-body">
    <div>
      <div class="header-bar">
        <div class="tag-pill">System Architecture • EcoStruxure-Aligned Industrial Topology</div>
        <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 34px; width: auto; filter: brightness(0) invert(1);">
      </div>
      <h1 class="slide-hook font-display">A Retrofit Kit Turning Solar Pumps into <span>Dual-Load Microgrids</span></h1>
      <p class="slide-sub">
        Industrial-grade retrofit marrying ESP32-S3 edge intelligence with Schneider Altivar Solar VFDs and TeSys switchgear, operating autonomously without cloud dependency.
      </p>
    </div>

    <div class="schematic-canvas">
      <!-- Left: Ground & Satellite Inputs -->
      <div class="schematic-col">
        <div class="col-title col-inputs-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0087CD" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          Layer 1: Field Hydrometry & Atmosphere
        </div>

        <div class="tech-box">
          <div class="box-header">
            <span class="box-name">Dual FDR Capacitive Probes</span>
            <span class="box-protocol">Analog / SDI-12</span>
          </div>
          <ul class="box-list">
            <li><strong>10cm Surface:</strong> Evaporative soil boundary</li>
            <li><strong>30cm Root Zone:</strong> Root uptake & Field Capacity</li>
            <li>Calibrated for Black Cotton & Sandy Loam</li>
          </ul>
        </div>

        <div class="tech-box">
          <div class="box-header">
            <span class="box-name">Volumetric Pulse Flow Meter</span>
            <span class="box-protocol">Interrupt Pulse</span>
          </div>
          <ul class="box-list">
            <li>1-inch Hall effect in-line pulse sensor</li>
            <li>Precision K-factor: <strong>0.45 L/pulse</strong></li>
            <li>Real-time flow tracking & cumulative audit</li>
          </ul>
        </div>

        <div class="tech-box">
          <div class="box-header">
            <span class="box-name">SHT31-D + Pyranometer</span>
            <span class="box-protocol">I2C / 0–5V</span>
          </div>
          <ul class="box-list">
            <li>Solar Irradiance: <strong>0 to 1,200 W/m²</strong></li>
            <li>Sensirion Ambient Temp & Relative Humidity</li>
            <li>Inputs for on-device FAO-56 Penman-Monteith</li>
          </ul>
        </div>
      </div>

      <!-- Center: Edge Controller & Contactor Interlock -->
      <div class="schematic-col">
        <div class="col-title col-brain-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#3DCD58" stroke-width="2.5"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 1v3M15 1v3M9 20v3M15 20v3M20 9h3M20 14h3M1 9h3M1 14h3"/></svg>
          Layer 2: AgroStruxure™ Edge Controller (IP67)
        </div>

        <div class="tech-box tech-box-highlight">
          <div class="box-header">
            <span class="box-name" style="color: #3DCD58; font-size: 18px;">ESP32-S3 Dual-Core Industrial MCU</span>
            <span class="box-protocol" style="background: rgba(61,205,88,0.2); color: #3DCD58;">FreeRTOS</span>
          </div>
          <p style="font-size: 13px; color: #CBD5E1; line-height: 1.4; margin-bottom: 10px;">
            Deterministic state engine executing local FAO-56 water budgeting and fail-safe interlocks without cloud dependence.
          </p>
          <div style="background: rgba(0,0,0,0.3); border-radius: 6px; padding: 10px 14px; font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #3DCD58; margin-bottom: 10px;">
            Modbus Master: Schneider Altivar ATV320<br>
            • Reg 8501: Command Word (CiA402 Profile)<br>
            • Reg 8502: Frequency Reference (0.1 Hz)
          </div>
          <div style="font-size: 12px; color: #94A3B8; line-height: 1.4;">
            <strong>Deterministic State Machine:</strong> Dynamic Soil Moisture Cutoff (FC = 45%) &rarr; 8s VFD Ramp-Down &rarr; 5s DC Bus Dead-Band Dwell &rarr; TeSys Contactor Transfer.
          </div>
        </div>

        <div class="tech-box" style="border-left: 3px solid #FFCE00;">
          <div class="box-header">
            <span class="box-name">Schneider TeSys D Switchgear</span>
            <span class="box-protocol">350–600V DC</span>
          </div>
          <p style="font-size: 13px; color: #E2E8F0; line-height: 1.4;">
            Dual mechanically & electrically interlocked contactors (2x LC1D09BD) with break-before-make <strong>150ms transfer</strong> and <strong>5.0s zero-current dwell</strong>. Eliminates inductive spikes and inverter trips.
          </p>
        </div>
      </div>

      <!-- Right: Dual Actuation Loads -->
      <div class="schematic-col">
        <div class="col-title col-loads-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#FFCE00" stroke-width="2.5"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          Layer 3: Dual Switched Industrial Loads
        </div>

        <div class="tech-box" style="border-top: 3px solid #0087CD;">
          <div class="box-header">
            <span class="box-name">Load A: Altivar Solar ATV320</span>
            <span class="box-protocol" style="color: #0087CD;">08:30–11:30 AM</span>
          </div>
          <ul class="box-list">
            <li>Drives 3–5 HP Submersible Borewell Pump</li>
            <li>Smooth 30–50 Hz MPPT frequency tracking</li>
            <li>Consumes <strong>2,422 kWh/yr</strong> scheduled quota</li>
            <li>Shuts down immediately at 45% Field Capacity</li>
          </ul>
        </div>

        <div class="tech-box" style="border-top: 3px solid #8015E8;">
          <div class="box-header">
            <span class="box-name">Load B: 2 MT Pre-Cooler</span>
            <span class="box-protocol" style="color: #8015E8;">11:30–15:30 PM</span>
          </div>
          <ul class="box-list">
            <li>3.8 kW DC Variable Refrigerant Compressor</li>
            <li>Harnesses <strong>3,187 kWh/yr</strong> diverted solar surplus</li>
            <li>Pulls harvest down: 32°C &rarr; 12°C in 4 hrs</li>
            <li>Organic salt-hydrate PCM holds 14 hrs overnight</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-bar font-mono">
      <div>Hardware Norms: Schneider Electric NVE41308 (Altivar CiA402) • IEC 60947-4-1 (TeSys D) • IP67 Enclosure</div>
      <div>AgroStruxure™ Engineering Topology • Slide 03 / 10</div>
    </div>
  </div>
</body>
</html>"""

# ==============================================================================
# SLIDE 04: HYDROLOGICAL OPTIMIZATION (Refined with Drip Photo Inset)
# ==============================================================================
SLIDE_04 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .slide-body {{
      padding: 56px 80px 48px 80px;
      height: 1080px;
      width: 1920px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #F8FAFC;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .tag-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #0369A1;
      background: #E0F2FE;
      border: 1px solid #BAE6FD;
      padding: 6px 14px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .slide-hook {{
      font-size: 52px;
      font-weight: 700;
      color: #0F172A;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .slide-hook span {{ color: #0284C7; }}
    .slide-sub {{
      font-size: 20px;
      color: #475569;
      line-height: 1.45;
      max-width: 1200px;
      margin-bottom: 28px;
    }}
    .hydro-grid {{
      display: grid;
      grid-template-columns: 46% 54%;
      gap: 36px;
      align-items: stretch;
      flex: 1;
    }}
    .soil-column-card {{
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 26px 28px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .soil-diagram {{
      border: 2px dashed #CBD5E1;
      border-radius: 8px;
      background: #F8FAFC;
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin: 12px 0;
    }}
    .soil-layer {{
      border-radius: 6px;
      padding: 12px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: relative;
    }}
    .layer-evap {{
      background: #FEF3C7;
      border: 1px solid #FDE68A;
      color: #92400E;
    }}
    .layer-root {{
      background: #DCFCE7;
      border: 1.5px solid #86EFAC;
      color: #166534;
    }}
    .layer-deep {{
      background: #F1F5F9;
      border: 1px solid #E2E8F0;
      color: #64748B;
    }}
    .drip-inset-row {{
      display: flex;
      gap: 16px;
      align-items: center;
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      padding: 10px 14px;
      margin-top: 10px;
    }}
    .drip-thumb {{
      width: 110px;
      height: 70px;
      border-radius: 6px;
      object-fit: cover;
      flex-shrink: 0;
    }}
    .balance-card {{
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 28px 32px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .ledger-row {{
      display: grid;
      grid-template-columns: 1.4fr 1fr 1fr 1.2fr;
      padding: 13px 0;
      border-bottom: 1px solid #F1F5F9;
      align-items: center;
      font-size: 15px;
    }}
    .ledger-header {{
      font-weight: 700;
      color: #64748B;
      text-transform: uppercase;
      font-size: 12px;
      letter-spacing: 0.05em;
      border-bottom: 2px solid #E2E8F0;
      padding-bottom: 10px;
    }}
    .stat-hero-box {{
      background: #F0FDF4;
      border: 1.5px solid #BBF7D0;
      border-radius: 10px;
      padding: 18px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: 14px;
    }}
    .stat-hero-val {{
      font-size: 52px;
      font-weight: 700;
      color: #15803D;
      font-family: 'Space Grotesk', sans-serif;
      line-height: 1;
    }}
    .footer-bar {{
      padding-top: 16px;
      border-top: 1px solid #E2E8F0;
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #64748B;
    }}
  </style>
</head>
<body>
  <div class="slide-body">
    <div>
      <div class="header-bar">
        <div class="tag-pill">Hydrological Optimization • Closed-Loop Water Budgeting</div>
        <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 34px; width: auto;">
      </div>
      <h1 class="slide-hook font-display">41.2% Less Groundwater. <span>Zero Compromise on Yield.</span></h1>
      <p class="slide-sub">
        Combining FAO-56 dual Kc dynamic evapotranspiration budgeting with real-time FDR capacitive cutoff eliminates agricultural over-irrigation.
      </p>
    </div>

    <div class="hydro-grid">
      <!-- Left: Physical Soil Profile -->
      <div class="soil-column-card">
        <div>
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: #0284C7; text-transform: uppercase;">
            Ground Truth Physics
          </div>
          <h3 class="font-display" style="font-size: 21px; font-weight: 700; color: #0F172A; margin: 4px 0 8px 0;">
            Dual-Depth Soil Moisture Profile
          </h3>
          <p style="font-size: 14px; color: #475569; line-height: 1.45;">
            Continuous capacitive frequency domain reflectometry (FDR) prevents irrigation beyond Field Capacity (FC), eliminating deep percolation losses.
          </p>

          <div class="soil-diagram">
            <div class="soil-layer layer-evap">
              <div>
                <strong style="font-size: 14px;">0–10 cm: Surface Evaporative Zone</strong>
                <div style="font-size: 12px; margin-top: 2px;">Tracked by 10cm FDR Probe • High diurnal vapor loss</div>
              </div>
              <span class="font-mono" style="font-weight: 700; font-size: 13px;">18%–32% VWC</span>
            </div>

            <div class="soil-layer layer-root">
              <div>
                <strong style="font-size: 14px;">10–40 cm: Active Crop Root Zone</strong>
                <div style="font-size: 12px; margin-top: 2px;">Dynamic Cutoff Triggered at <strong>FC = 45%</strong> • Zero Hypoxia</div>
              </div>
              <span class="font-mono" style="font-weight: 700; font-size: 13px; color: #15803D;">FC CUTOFF</span>
            </div>

            <div class="soil-layer layer-deep">
              <div>
                <strong style="font-size: 14px;">40+ cm: Deep Percolation Saturated Zone</strong>
                <div style="font-size: 12px; margin-top: 2px;">Eliminated by pulsed drip • Previously 7,000 m³ drained uselessly</div>
              </div>
              <span class="font-mono" style="font-weight: 700; font-size: 13px;">NO LEACHING</span>
            </div>
          </div>
        </div>

        <div class="drip-inset-row">
          <img src="{IMG_DRIP}" alt="Precision Drip Irrigation" class="drip-thumb">
          <div style="font-size: 13px; color: #334155; line-height: 1.4;">
            <strong>Hydraulic Solenoid Interlock:</strong> Closes automatically upon root-zone field capacity saturation. Prevents collar rot in Solanaceae crops and halts unnecessary pump power draw.
          </div>
        </div>
      </div>

      <!-- Right: Hydrological Ledger -->
      <div class="balance-card">
        <div>
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: #15803D; text-transform: uppercase;">
            impact_model.py Quantitative Proof
          </div>
          <h3 class="font-display" style="font-size: 21px; font-weight: 700; color: #0F172A; margin: 4px 0 14px 0;">
            Water & Energy Conservation Ledger (Per Ha / Year)
          </h3>

          <div class="ledger-row ledger-header font-mono">
            <div>Parameter</div>
            <div>Baseline Flood</div>
            <div>AgroStruxure</div>
            <div>Net Savings</div>
          </div>

          <div class="ledger-row">
            <div><strong>Water Application</strong></div>
            <div class="font-mono">17,000 m³</div>
            <div class="font-mono">10,000 m³</div>
            <div class="font-mono" style="color: #15803D; font-weight: 700;">-7,000 m³ (-41.2%)</div>
          </div>

          <div class="ledger-row">
            <div><strong>Pumping Electricity</strong></div>
            <div class="font-mono">4,118 kWh</div>
            <div class="font-mono">2,422 kWh</div>
            <div class="font-mono" style="color: #15803D; font-weight: 700;">-1,696 kWh Liberated</div>
          </div>

          <div class="ledger-row">
            <div><strong>Pumping Operating Time</strong></div>
            <div class="font-mono">1,373 hrs</div>
            <div class="font-mono">807 hrs</div>
            <div class="font-mono" style="color: #15803D; font-weight: 700;">-566 hrs Less Wear</div>
          </div>

          <div class="ledger-row" style="border-bottom: none;">
            <div><strong>Root Zone Health</strong></div>
            <div style="color: #DC2626;">Hypoxia / Leaching</div>
            <div style="color: #15803D;">Aerobic / Optimal</div>
            <div style="color: #15803D; font-weight: 700;">Zero Waterlogging</div>
          </div>
        </div>

        <div>
          <div class="stat-hero-box">
            <div>
              <div style="font-size: 13px; font-weight: 700; text-transform: uppercase; color: #166534; letter-spacing: 0.04em;">
                Conserved Groundwater Per Hectare
              </div>
              <div class="stat-hero-val">7,000 m³ / Year</div>
              <div style="font-size: 13px; color: #15803D; margin-top: 4px;">
                Equivalent to 28 Olympic swimming pools of community aquifer water preserved.
              </div>
            </div>
            <div style="text-align: right; border-left: 2px solid #86EFAC; padding-left: 24px;">
              <div style="font-size: 42px; font-weight: 700; color: #15803D; font-family: 'Space Grotesk', sans-serif;">41.2%</div>
              <div style="font-size: 12px; font-weight: 700; color: #166534; text-transform: uppercase;">Direct Reduction</div>
            </div>
          </div>

          <p style="font-size: 12px; color: #64748B; margin-top: 10px; font-style: italic;">
            <strong>Honest Attribution:</strong> 29.4% saved by shifting flood to drip; 11.8% additional saving uniquely locked in by AgroStruxure's automated soil cutoff to eliminate the solar rebound paradox.
          </p>
        </div>
      </div>
    </div>

    <div class="footer-bar font-mono">
      <div>Agronomic Standards: FAO Irrigation & Drainage Paper 56 (Allen et al.) • ICAR-IARI Water Technology Center</div>
      <div>AgroStruxure™ Hydrological Engine • Slide 04 / 10</div>
    </div>
  </div>
</body>
</html>"""

# ==============================================================================
# SLIDE 05: POWER ENGINEERING (Refined: Inset Comparison, Eliminates Void)
# ==============================================================================
SLIDE_05 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .slide-body {{
      padding: 52px 76px 44px 76px;
      height: 1080px;
      width: 1920px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #0F1416;
      color: #FFFFFF;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
    }}
    .tag-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #FFCE00;
      background: rgba(255, 206, 0, 0.12);
      border: 1px solid rgba(255, 206, 0, 0.3);
      padding: 6px 14px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .slide-hook {{
      font-size: 48px;
      font-weight: 700;
      color: #FFFFFF;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 6px;
    }}
    .slide-hook span {{ color: #FFCE00; }}
    .slide-sub {{
      font-size: 19px;
      color: #94A3B8;
      line-height: 1.4;
      max-width: 1280px;
      margin-bottom: 22px;
    }}
    .power-grid {{
      display: grid;
      grid-template-columns: 50% 50%;
      gap: 32px;
      align-items: stretch;
      flex: 1;
    }}
    .power-card {{
      background: #151D22;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 12px;
      padding: 26px 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }}
    .sankey-bar {{
      display: flex;
      height: 48px;
      border-radius: 8px;
      overflow: hidden;
      margin: 14px 0 16px 0;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }}
    .bar-pump {{
      background: #0087CD;
      width: 36.9%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 13px;
    }}
    .bar-cold {{
      background: #8015E8;
      width: 48.6%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 13px;
    }}
    .bar-resid {{
      background: #475569;
      width: 14.5%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 12px;
      color: #CBD5E1;
    }}
    .partition-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }}
    .partition-table td {{
      padding: 8px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 14px;
    }}
    .comparison-callout {{
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 12px 16px;
      margin-top: 12px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      font-size: 12px;
    }}
    .sequence-step {{
      background: #1B242A;
      border-left: 3px solid #3DCD58;
      border-radius: 0 6px 6px 0;
      padding: 11px 16px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .step-time {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(255,255,255,0.08);
      color: #FFCE00;
      min-width: 72px;
      text-align: center;
    }}
    .footer-bar {{
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #64748B;
    }}
  </style>
</head>
<body>
  <div class="slide-body">
    <div>
      <div class="header-bar">
        <div class="tag-pill">Power Engineering • Upstream DC Bus Routing</div>
        <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 34px; width: auto; filter: brightness(0) invert(1);">
      </div>
      <h1 class="slide-hook font-display">4,137 kWh Surplus Captured at <span>Zero AC Transient Risk</span></h1>
      <p class="slide-sub">
        Switching power safely upstream on the 350–600V DC bus eliminates inductive voltage spikes and inverter drive trips during load transfer.
      </p>
    </div>

    <div class="power-grid">
      <!-- Left: Energy Partition & Electrical Physics -->
      <div class="power-card">
        <div>
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: #FFCE00; text-transform: uppercase;">
            4.8 kWp Standalone PV Generation Partition
          </div>
          <h3 class="font-display" style="font-size: 21px; font-weight: 700; color: #FFFFFF; margin: 4px 0 8px 0;">
            Annual Solar Yield: 6,559 kWh / Year
          </h3>
          <p style="font-size: 14px; color: #94A3B8; line-height: 1.4;">
            Without AgroStruxure, 63.07% of clean energy is curtailed once pumping halts. AgroStruxure routes <strong>77.04% of this surplus (3,187 kWh/yr)</strong> into farm-gate cooling.
          </p>

          <div class="sankey-bar font-mono">
            <div class="bar-pump">36.9% Pumping</div>
            <div class="bar-cold">48.6% Cold Chain</div>
            <div class="bar-resid">14.5% Res.</div>
          </div>

          <table class="partition-table">
            <tr>
              <td><strong>Total Standalone Generation:</strong></td>
              <td class="font-mono" style="text-align: right;">6,559 kWh</td>
              <td style="text-align: right; color: #94A3B8;">100.0%</td>
            </tr>
            <tr>
              <td style="color: #0087CD;"><strong>Pumping Demand (Scheduled):</strong></td>
              <td class="font-mono" style="text-align: right; color: #0087CD;">2,422 kWh</td>
              <td style="text-align: right; color: #0087CD;">36.9%</td>
            </tr>
            <tr>
              <td style="color: #FFCE00;"><strong>Total Idle Surplus Available:</strong></td>
              <td class="font-mono" style="text-align: right; color: #FFCE00;">4,137 kWh</td>
              <td style="text-align: right; color: #FFCE00;">63.1%</td>
            </tr>
            <tr>
              <td style="color: #8015E8;"><strong>Surplus Put to Work (Cooling):</strong></td>
              <td class="font-mono" style="text-align: right; color: #8015E8; font-weight: 700;">3,187 kWh</td>
              <td style="text-align: right; color: #8015E8; font-weight: 700;">77.0%</td>
            </tr>
            <tr>
              <td style="color: #64748B;">Residual Midday Summer Surplus:</td>
              <td class="font-mono" style="text-align: right; color: #64748B;">951 kWh</td>
              <td style="text-align: right; color: #64748B;">14.5%</td>
            </tr>
          </table>
        </div>

        <div>
          <div class="comparison-callout">
            <div style="border-right: 1px solid rgba(255,255,255,0.1); padding-right: 12px;">
              <strong style="color: #EF4444; text-transform: uppercase;">Flawed AC Side Switching:</strong>
              <div style="color: #94A3B8; margin-top: 4px; line-height: 1.35;">
                Disconnecting running motor AC leads to inductive back-EMF spikes <strong>>1,200V</strong>, instant VFD IGBT punch-through & contact arcing.
              </div>
            </div>
            <div style="padding-left: 4px;">
              <strong style="color: #3DCD58; text-transform: uppercase;">AgroStruxure Upstream DC:</strong>
              <div style="color: #94A3B8; margin-top: 4px; line-height: 1.35;">
                Controlled VFD deceleration to 0 Hz followed by <strong>5.0s zero-current dead-band</strong> ensures contactors switch at exact 0.00 Amps.
              </div>
            </div>
          </div>

          <div style="font-size: 12px; color: #64748B; margin-top: 8px;">
            <strong>Zero Hallucination Mandate:</strong> 951 kWh residual summer surplus transparently reported (compressor throttles once PCM fully frozen).
          </div>
        </div>
      </div>

      <!-- Right: Break-Before-Make Sequence -->
      <div class="power-card">
        <div>
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: #3DCD58; text-transform: uppercase;">
            Upstream DC Bus vs Risky AC Switching
          </div>
          <h3 class="font-display" style="font-size: 21px; font-weight: 700; color: #FFFFFF; margin: 4px 0 8px 0;">
            5-Step Zero-Current Transfer Sequence
          </h3>
          <p style="font-size: 14px; color: #94A3B8; line-height: 1.4; margin-bottom: 14px;">
            Deterministic firmware interlock guaranteeing break-before-make switching without contact wear:
          </p>

          <div class="sequence-step">
            <span class="step-time">EVENT</span>
            <div>
              <strong style="color: #FFFFFF; font-size: 14px;">1. Moisture Saturation Cutoff</strong>
              <div style="font-size: 12px; color: #94A3B8;">30cm FDR reaches 45% Field Capacity or daily quota exhausted.</div>
            </div>
          </div>

          <div class="sequence-step">
            <span class="step-time">T = 0.0s</span>
            <div>
              <strong style="color: #FFFFFF; font-size: 14px;">2. Controlled VFD Deceleration</strong>
              <div style="font-size: 12px; color: #94A3B8;">Modbus Reg 8502 ramps Altivar ATV320 to 0 Hz smoothly over 8.0 seconds.</div>
            </div>
          </div>

          <div class="sequence-step">
            <span class="step-time">T = 8.0s</span>
            <div>
              <strong style="color: #FFFFFF; font-size: 14px;">3. Zero-Flow Solenoid Closure</strong>
              <div style="font-size: 12px; color: #94A3B8;">1-inch latching valve shuts at zero velocity; zero water hammer shock.</div>
            </div>
          </div>

          <div class="sequence-step" style="border-left-color: #FFCE00; background: #222218;">
            <span class="step-time" style="color: #FFCE00;">T = 8–13s</span>
            <div>
              <strong style="color: #FFCE00; font-size: 14px;">4. 5.0-Second DC Dead-Band Dwell</strong>
              <div style="font-size: 12px; color: #CBD5E1;">Guarantees bus capacitors discharge and DC current reaches 0.00 Amps.</div>
            </div>
          </div>

          <div class="sequence-step" style="border-left-color: #8015E8;">
            <span class="step-time" style="color: #A855F7;">T = 13.2s</span>
            <div>
              <strong style="color: #FFFFFF; font-size: 14px;">5. TeSys D Contactor Transfer</strong>
              <div style="font-size: 12px; color: #94A3B8;">Dual interlocked contactor energizes 3.8 kW micro-cold room compressor.</div>
            </div>
          </div>

          <!-- Single-Line Electrical Routing Diagram -->
          <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; padding: 10px 14px; margin-top: 12px;">
            <div style="font-size: 11px; font-weight: 700; color: #3DCD58; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px;">
              Single-Line Upstream DC Architecture (SLD)
            </div>
            <svg viewBox="0 0 720 75" width="100%" height="75" fill="none" xmlns="http://www.w3.org/2000/svg" style="font-family: 'JetBrains Mono', monospace;">
              <!-- PV Array Node -->
              <rect x="2" y="16" width="125" height="42" rx="4" fill="#1E293B" stroke="#FFCE00" stroke-width="1.5"/>
              <text x="64" y="34" fill="#FFCE00" font-weight="bold" text-anchor="middle" font-size="11">PV ARRAY</text>
              <text x="64" y="48" fill="#94A3B8" text-anchor="middle" font-size="9.5">4.8 kWp (350-600V)</text>
              
              <!-- Bus Wire -->
              <path d="M127 37 H 205" stroke="#FFCE00" stroke-width="2.5" stroke-dasharray="4 2"/>
              <polygon points="203,33 213,37 203,41" fill="#FFCE00"/>
              
              <!-- TeSys Interlock Box -->
              <rect x="215" y="8" width="185" height="58" rx="4" fill="#064E3B" stroke="#3DCD58" stroke-width="2"/>
              <text x="307" y="27" fill="#3DCD58" font-weight="bold" text-anchor="middle" font-size="11">TeSys D LC1D09BD</text>
              <text x="307" y="42" fill="#FFFFFF" text-anchor="middle" font-size="9.5">Dual Interlocked Transfer</text>
              <text x="307" y="55" fill="#A7F3D0" text-anchor="middle" font-size="9">150ms Break • 5s Dwell</text>
              
              <!-- Dual Branch Wires -->
              <path d="M400 24 H 465" stroke="#0087CD" stroke-width="2"/>
              <polygon points="463,20 473,24 463,28" fill="#0087CD"/>
              
              <path d="M400 50 H 465" stroke="#A855F7" stroke-width="2"/>
              <polygon points="463,46 473,50 463,54" fill="#A855F7"/>
              
              <!-- Load A Node -->
              <rect x="475" y="8" width="240" height="30" rx="4" fill="#0C2538" stroke="#0087CD" stroke-width="1.2"/>
              <text x="595" y="23" fill="#38BDF8" font-weight="bold" text-anchor="middle" font-size="10">Load A: Altivar ATV320 (08:30-11:30)</text>
              <text x="595" y="34" fill="#94A3B8" text-anchor="middle" font-size="8.5">Borewell Pump • 2,422 kWh/yr</text>
              
              <!-- Load B Node -->
              <rect x="475" y="42" width="240" height="30" rx="4" fill="#2E1065" stroke="#A855F7" stroke-width="1.2"/>
              <text x="595" y="56" fill="#C084FC" font-weight="bold" text-anchor="middle" font-size="10">Load B: 3.8 kW Compressor (11:30-15:30)</text>
              <text x="595" y="68" fill="#94A3B8" text-anchor="middle" font-size="8.5">2 MT Cold Storage • 3,187 kWh/yr</text>
            </svg>
          </div>
        </div>

        <div style="font-size: 12px; color: #64748B; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 10px; margin-top: 6px;">
          Hardware Specification: Schneider Electric TeSys D LC1D09BD (Dual Interlocked) • Type-2 DC SPD Rated 1,000V DC.
        </div>
      </div>
    </div>

    <div class="footer-bar font-mono">
      <div>Safety Standard: IEC 60947-4-1 (Break-before-make interlock) • NFPA 79 Electrical Standard for Industrial Machinery</div>
      <div>AgroStruxure™ Power Engineering • Slide 05 / 10</div>
    </div>
  </div>
</body>
</html>"""

# ==============================================================================
# SLIDE 06: COLD CHAIN & THERMAL DYNAMICS (Refined with Carbon & Metrics)
# ==============================================================================
SLIDE_06 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .slide-body {{
      padding: 56px 80px 48px 80px;
      height: 1080px;
      width: 1920px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #0B1115;
      color: #FFFFFF;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .tag-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #3DCD58;
      background: rgba(61, 205, 88, 0.12);
      border: 1px solid rgba(61, 205, 88, 0.3);
      padding: 6px 14px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .slide-hook {{
      font-size: 52px;
      font-weight: 700;
      color: #FFFFFF;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .slide-hook span {{ color: #3DCD58; }}
    .slide-sub {{
      font-size: 20px;
      color: #94A3B8;
      line-height: 1.45;
      max-width: 1200px;
      margin-bottom: 26px;
    }}
    .cold-grid {{
      display: grid;
      grid-template-columns: 38% 62%;
      gap: 36px;
      align-items: stretch;
      flex: 1;
    }}
    .photo-card {{
      position: relative;
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: flex-end;
      padding: 28px;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }}
    .photo-card img {{
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover;
    }}
    .photo-overlay {{
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(180deg, rgba(11,17,21,0.1) 0%, rgba(11,17,21,0.92) 75%);
    }}
    .photo-content {{
      position: relative;
      z-index: 2;
    }}
    .thermal-data-panel {{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
    }}
    .stats-trio {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 18px;
    }}
    .stat-box {{
      background: #141C21;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 22px 20px;
    }}
    .stat-val {{
      font-size: 42px;
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
      line-height: 1;
      margin-bottom: 8px;
    }}
    .stat-title {{
      font-size: 13px;
      font-weight: 700;
      color: #CBD5E1;
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .stat-detail {{
      font-size: 13px;
      color: #94A3B8;
      line-height: 1.35;
    }}
    .thermal-curve-box {{
      background: #141C21;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 22px 26px;
    }}
    .footer-bar {{
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #64748B;
    }}
  </style>
</head>
<body>
  <div class="slide-body">
    <div>
      <div class="header-bar">
        <div class="tag-pill">Thermal Engineering • Decentralized Cold Chain</div>
        <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 34px; width: auto; filter: brightness(0) invert(1);">
      </div>
      <h1 class="slide-hook font-display">Halving Farm-Gate Spoilage from <span>8.37% to 4.00%</span></h1>
      <p class="slide-sub">
        Thermodynamically sized 2 MT farm-gate pre-cooler halts respiration heat within 4 hours, extending tomato shelf life by 4–7 days.
      </p>
    </div>

    <div class="cold-grid">
      <!-- Left: Tomato Photography -->
      <div class="photo-card">
        <img src="{IMG_TOMATO}" alt="Fresh Tomato Harvest">
        <div class="photo-overlay"></div>
        <div class="photo-content">
          <div style="font-size: 11px; font-weight: 700; letter-spacing: 0.08em; color: #3DCD58; text-transform: uppercase; margin-bottom: 6px;">
            Horticulture Physics
          </div>
          <h3 class="font-display" style="font-size: 22px; font-weight: 700; margin-bottom: 8px;">
            Critical Chilling Threshold: 12.0°C
          </h3>
          <p style="font-size: 13px; color: #CBD5E1; line-height: 1.45;">
            FAO & ICAR baseline: Fresh tomatoes suffer cellular collapse & chilling injury below 10°C. AgroStruxure precision controls thermal hold at exactly <strong>12.0°C</strong> with 14-hour passive PCM holdover.
          </p>
        </div>
      </div>

      <!-- Right: Thermal Metrics & Economics -->
      <div class="thermal-data-panel">
        <div class="stats-trio">
          <div class="stat-box" style="border-top: 3px solid #3DCD58;">
            <div class="stat-val" style="color: #3DCD58;">1.31 <span style="font-size: 22px;">Tonnes</span></div>
            <div class="stat-title">Produce Preserved / Ha</div>
            <div class="stat-detail">Farm-stage spoilage cut by more than half (8.37% down to 4.00%).</div>
          </div>

          <div class="stat-box" style="border-top: 3px solid #FFCE00;">
            <div class="stat-val" style="color: #FFCE00;">₹15,732</div>
            <div class="stat-title">Direct Revenue Saved</div>
            <div class="stat-detail">1,311 kg grade-A fruit preserved @ ₹12/kg mandi benchmark.</div>
          </div>

          <div class="stat-box" style="border-top: 3px solid #0087CD;">
            <div class="stat-val" style="color: #0087CD;">+₹12,000</div>
            <div class="stat-title">Distress Sale Timing</div>
            <div class="stat-detail">Holding crates for evening mandi pricing (+₹1–₹2/kg on 8 tonnes).</div>
          </div>
        </div>

        <div class="thermal-curve-box">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #3DCD58;">
              Thermodynamic Pull-Down & Thermal Battery
            </div>
            <div class="font-mono" style="font-size: 12px; color: #94A3B8;">COP = 3.0 • 3.43 kW Cooling Load</div>
          </div>
          
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; font-size: 14px; color: #CBD5E1; line-height: 1.5;">
            <div>
              <strong style="color: #FFFFFF;">Rapid Pull-Down (11:30 AM – 3:30 PM):</strong><br>
              Direct solar surplus drives the DC compressor to drop 2.0 MT fresh produce core temperature from 32°C ambient harvest heat to 12.0°C within 4 hours.
            </div>
            <div>
              <strong style="color: #FFFFFF;">Passive PCM Buffer (14-Hour Holdover):</strong><br>
              Inorganic salt-hydrate phase change plates freeze at 10°C, maintaining the cold room at 12°C overnight without battery storage or diesel backup.
            </div>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 16px;">
          <div style="background: rgba(61, 205, 88, 0.08); border: 1px solid rgba(61, 205, 88, 0.2); border-radius: 8px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 13px; color: #E2E8F0;">
              <strong style="color: #3DCD58;">Net Farmer Gain (Tier A):</strong><br>
              ₹15,732 (saved fruit) + ₹12,000 (timing) - ₹2,400 (opex)
            </div>
            <div class="font-mono" style="font-size: 18px; font-weight: 700; color: #3DCD58;">
              +₹25,332/yr
            </div>
          </div>

          <div style="background: rgba(0, 135, 205, 0.08); border: 1px solid rgba(0, 135, 205, 0.2); border-radius: 8px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center;">
            <div style="font-size: 13px; color: #E2E8F0;">
              <strong style="color: #0087CD;">Decarbonization:</strong><br>
              Replaces diesel cold chain & avoids spoilage loss
            </div>
            <div class="font-mono" style="font-size: 18px; font-weight: 700; color: #0087CD;">
              2.94 tCO₂e
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar font-mono">
      <div>Post-Harvest Reference: ICAR-CIPHET 2021 Bulletin 44 • NABCONS 2022 MoFPI Baseline Study</div>
      <div>AgroStruxure™ Cold Chain Engineering • Slide 06 / 10</div>
    </div>
  </div>
</body>
</html>"""

# ==============================================================================
# SLIDE 07: KRISHI MITRA VERNACULAR AI (Refined with Schema & Dialog)
# ==============================================================================
SLIDE_07 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .slide-body {{
      padding: 56px 80px 48px 80px;
      height: 1080px;
      width: 1920px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #F8FAFC;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .tag-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #0D8752;
      background: #E8F8ED;
      border: 1px solid #B7EBC4;
      padding: 6px 14px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .slide-hook {{
      font-size: 52px;
      font-weight: 700;
      color: #0F172A;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .slide-hook span {{ color: #0D8752; }}
    .slide-sub {{
      font-size: 20px;
      color: #475569;
      line-height: 1.45;
      max-width: 1200px;
      margin-bottom: 26px;
    }}
    .trust-grid {{
      display: grid;
      grid-template-columns: 46% 54%;
      gap: 36px;
      align-items: stretch;
      flex: 1;
    }}
    .firewall-card {{
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 26px 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .firewall-step {{
      display: flex;
      gap: 14px;
      align-items: flex-start;
      margin-bottom: 12px;
    }}
    .step-badge {{
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: #024230;
      color: #FFFFFF;
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .schema-preview {{
      background: #0F172A;
      border-radius: 6px;
      padding: 10px 14px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #38BDF8;
      margin: 8px 0 10px 42px;
      line-height: 1.4;
    }}
    .safety-banner {{
      background: #FEF2F2;
      border: 1.5px solid #FCA5A5;
      border-radius: 8px;
      padding: 14px 18px;
      margin-top: 10px;
    }}
    .chat-card {{
      background: #ECE5DD;
      border: 1px solid #CBD5E1;
      border-radius: 12px;
      padding: 26px 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }}
    .whatsapp-bubble {{
      background: #FFFFFF;
      border-radius: 8px 8px 8px 0;
      padding: 18px 22px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.08);
      position: relative;
      margin-bottom: 14px;
    }}
    .whatsapp-user-bubble {{
      background: #DCF8C6;
      border-radius: 8px 8px 0 8px;
      padding: 12px 18px;
      align-self: flex-end;
      box-shadow: 0 2px 6px rgba(0,0,0,0.06);
      margin-bottom: 12px;
      font-size: 15px;
      color: #1E293B;
      max-width: 80%;
    }}
    .audio-player {{
      display: flex;
      align-items: center;
      gap: 14px;
      background: #F0FDF4;
      border: 1px solid #BBF7D0;
      border-radius: 30px;
      padding: 10px 18px;
      margin-top: 12px;
    }}
    .footer-bar {{
      padding-top: 16px;
      border-top: 1px solid #E2E8F0;
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #64748B;
    }}
  </style>
</head>
<body>
  <div class="slide-body">
    <div>
      <div class="header-bar">
        <div class="tag-pill">Cognitive Trust • Deterministic Vernacular AI</div>
        <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 34px; width: auto;">
      </div>
      <h1 class="slide-hook font-display">Vernacular AI Grounded in Hardware Truth. <span>Zero Actuation Authority.</span></h1>
      <p class="slide-sub">
        Spoken voice advisories in Marathi and Hindi delivered over WhatsApp, grounded 100% in edge telemetry with zero authority to actuate physical switchgear.
      </p>
    </div>

    <div class="trust-grid">
      <!-- Left: Deterministic Safety Pipeline -->
      <div class="firewall-card">
        <div>
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: #0D8752; text-transform: uppercase;">
            Deterministic Agentic Architecture
          </div>
          <h3 class="font-display" style="font-size: 21px; font-weight: 700; color: #0F172A; margin: 4px 0 14px 0;">
            The 4-Stage Cognitive Trust Pipeline
          </h3>

          <div class="firewall-step">
            <div class="step-badge">1</div>
            <div>
              <strong style="font-size: 14px; color: #0F172A;">Edge Telemetry Extraction (Modbus RTU)</strong>
              <div style="font-size: 13px; color: #475569; margin-top: 1px;">
                MCU samples FDR sensors (44.8% FC), flow meter (27.4 m³), and Altivar VFD status into circular flash buffer.
              </div>
            </div>
          </div>

          <div class="firewall-step">
            <div class="step-badge">2</div>
            <div>
              <strong style="font-size: 14px; color: #0F172A;">Pydantic Strict Schema Validation</strong>
              <div style="font-size: 13px; color: #475569; margin-top: 1px;">
                Telemetry serializes into deterministic JSON. If fields are missing or corrupted, LLM fallback is blocked instantly.
              </div>
            </div>
          </div>

          <div class="schema-preview">
            &#123;"vwc_30cm": 0.448, "status": "FC_CUTOFF", "pv_kw": 4.21, "load": "PRE_COOLER", "temp_c": 12.0&#125;
          </div>

          <div class="firewall-step">
            <div class="step-badge">3</div>
            <div>
              <strong style="font-size: 14px; color: #0F172A;">Read-Only Deterministic RAG Prompt</strong>
              <div style="font-size: 13px; color: #475569; margin-top: 1px;">
                The copilot has read access to verified JSON data and agronomy templates, with strictly ZERO tool execution authority.
              </div>
            </div>
          </div>

          <div class="firewall-step">
            <div class="step-badge">4</div>
            <div>
              <strong style="font-size: 14px; color: #0F172A;">Vernacular Speech Synthesis (TTS)</strong>
              <div style="font-size: 13px; color: #475569; margin-top: 1px;">
                Generates high-intelligibility spoken audio in rural Marathi and Hindi dialects delivered via WhatsApp voice notes.
              </div>
            </div>
          </div>
        </div>

        <div class="safety-banner">
          <div style="display: flex; align-items: center; gap: 8px; color: #991B1B; font-weight: 700; font-size: 13px; text-transform: uppercase;">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#991B1B" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            Hard Physical Safety Invariant
          </div>
          <p style="font-size: 12px; color: #7F1D1D; line-height: 1.4; margin-top: 3px;">
            <strong>LLMs do NOT control physical contactors.</strong> All switching decisions are executed exclusively by deterministic FreeRTOS C++ state machines. A manual physical switch on the IP67 box allows instant human override.
          </p>
        </div>
      </div>

      <!-- Right: WhatsApp Voice Experience -->
      <div class="chat-card">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="width: 12px; height: 12px; border-radius: 50%; background: #25D366;"></div>
              <strong style="font-size: 16px; color: #075E54;">Krishi Mitra • WhatsApp Spoken Advisory</strong>
            </div>
            <span class="font-mono" style="font-size: 12px; color: #64748B;">11:32 AM • Nashik Cluster</span>
          </div>

          <div class="whatsapp-bubble font-devanagari">
            <div style="font-size: 18px; line-height: 1.55; color: #1E293B; font-weight: 600;">
              "रामभाऊ, तुमच्या टोमॅटोच्या मुळांना पुरेसे पाणी मिळाले आहे (४४.८%). पंप सुरक्षितपणे बंद झाला असून सौर वीज शीतगृहाकडे वळवली आहे. शीतगृहाचे तापमान १२°C असून टोमॅटो थंड होत आहेत."
            </div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 13px; color: #64748B; margin-top: 8px; font-style: italic; line-height: 1.4;">
              Translation: "Rambhau, your tomato roots have reached optimal moisture (44.8%). Pumping stopped safely and solar power is now running the cold room at 12°C."
            </div>
            
            <div class="audio-player">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="#0D8752"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              <div style="flex: 1; height: 6px; background: #CBD5E1; border-radius: 3px; position: relative;">
                <div style="width: 55%; height: 100%; background: #0D8752; border-radius: 3px;"></div>
              </div>
              <span class="font-mono" style="font-size: 12px; font-weight: 700; color: #0D8752;">0:14 / 0:26</span>
            </div>
          </div>

          <div class="whatsapp-user-bubble font-devanagari" style="display: flex; justify-content: space-between; align-items: center;">
            <div>"धन्यवाद! उद्या पाणी कधी सुरू होईल?" <span style="font-size: 12px; font-family: sans-serif; color: #64748B;">(When tomorrow?)</span></div>
            <span class="font-mono" style="font-size: 10px; color: #64748B; margin-left: 12px;">11:34 AM &#10003;&#10003;</span>
          </div>
        </div>

        <div style="background: #FFFFFF; border-radius: 8px; padding: 14px 18px; border: 1px solid #E2E8F0;">
          <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.05em; margin-bottom: 4px;">
            Zero-Literacy Design Paradigm
          </div>
          <p style="font-size: 13px; color: #334155; line-height: 1.4;">
            Smallholder farmers do not use complex dashboards. Krishi Mitra pushes automated 20-second audio voice notes over WhatsApp at key state transitions (Pumping Done &rarr; Cold Storage Online), establishing high cognitive trust.
          </p>
        </div>
      </div>
    </div>

    <div class="footer-bar font-mono">
      <div>AI Architecture: Deterministic Agentic RAG • Fastify Backend • FreeRTOS Edge Firmware • Pydantic Schema</div>
      <div>AgroStruxure™ Vernacular Cognitive Trust • Slide 07 / 10</div>
    </div>
  </div>
</body>
</html>"""

# ==============================================================================
# SLIDE 08: INDUSTRIAL UNIT ECONOMICS (Refined with Stepped Waterfall & Cashflow)
# ==============================================================================
SLIDE_08 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .slide-body {{
      padding: 56px 80px 48px 80px;
      height: 1080px;
      width: 1920px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #F8FAFC;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .tag-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #0D8752;
      background: #E8F8ED;
      border: 1px solid #B7EBC4;
      padding: 6px 14px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .slide-hook {{
      font-size: 52px;
      font-weight: 700;
      color: #0F172A;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .slide-hook span {{ color: #0D8752; }}
    .slide-sub {{
      font-size: 20px;
      color: #475569;
      line-height: 1.45;
      max-width: 1200px;
      margin-bottom: 26px;
    }}
    .finance-grid {{
      display: grid;
      grid-template-columns: 50% 50%;
      gap: 36px;
      align-items: stretch;
      flex: 1;
    }}
    .waterfall-card {{
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 26px 30px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .waterfall-step {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 11px 0;
      border-bottom: 1px solid #F1F5F9;
      font-size: 15px;
    }}
    .payback-card {{
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 26px 30px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .bom-box {{
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      padding: 14px 18px;
      margin-top: 14px;
    }}
    .footer-bar {{
      padding-top: 16px;
      border-top: 1px solid #E2E8F0;
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #64748B;
    }}
  </style>
</head>
<body>
  <div class="slide-body">
    <div>
      <div class="header-bar">
        <div class="tag-pill">Commercial Feasibility • Industrial Unit Economics</div>
        <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 34px; width: auto;">
      </div>
      <h1 class="slide-hook font-display">₹50,212 Net Capex per Farm. <span>Payback in 2.0 Years.</span></h1>
      <p class="slide-sub">
        Ultra-lean ₹7,540 edge controller BoM paired with a 4-farm cluster pre-cooler sharing model yields rapid capital recovery across two crop harvests.
      </p>
    </div>

    <div class="finance-grid">
      <!-- Left: Capex Waterfall -->
      <div class="waterfall-card">
        <div>
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: #0D8752; text-transform: uppercase;">
            Tier A: 4-Farm Cluster Asset Sharing Model (2 MT)
          </div>
          <h3 class="font-display" style="font-size: 21px; font-weight: 700; color: #0F172A; margin: 4px 0 12px 0;">
            Capital Expenditure Waterfall
          </h3>

          <div class="waterfall-step">
            <div><strong>Gross 2 MT Pre-Cooler Capex (Compressor + PCM)</strong></div>
            <div class="font-mono" style="font-weight: 700;">₹400,000</div>
          </div>

          <div class="waterfall-step" style="color: #0284C7;">
            <div><strong>Less: Shared Solar PV Saving (2.6 kWp array avoided)</strong></div>
            <div class="font-mono" style="font-weight: 700;">-₹91,000</div>
          </div>

          <div class="waterfall-step">
            <div>Net System Capital Cost</div>
            <div class="font-mono">₹309,000</div>
          </div>

          <div class="waterfall-step" style="color: #15803D;">
            <div><strong>Less: 35% MIDH / AIF Scheme Capital Subsidy</strong></div>
            <div class="font-mono" style="font-weight: 700;">-₹108,150</div>
          </div>

          <div class="waterfall-step" style="background: #F0FDF4; padding: 12px 16px; border-radius: 6px; margin-top: 8px;">
            <div style="font-size: 15px; font-weight: 700; color: #166534;">Net Capex Per Farm (4-Farm Shared Cluster)</div>
            <div class="font-mono" style="font-size: 24px; font-weight: 700; color: #15803D;">₹50,212</div>
          </div>

          <!-- Visual Waterfall Stepped Graphic -->
          <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px 14px; margin: 12px 0;">
            <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; margin-bottom: 6px; letter-spacing: 0.05em;">Capex Partition Per Farm (₹100,000 Base)</div>
            <div style="display: flex; height: 20px; border-radius: 4px; overflow: hidden; background: #E2E8F0; font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 700;">
              <div style="width: 50.2%; background: #15803D; color: #FFF; display: flex; align-items: center; justify-content: center;">₹50,212 (Farmer Capex)</div>
              <div style="width: 27.0%; background: #0284C7; color: #FFF; display: flex; align-items: center; justify-content: center;">-₹27,038 (MIDH 35%)</div>
              <div style="width: 22.8%; background: #EAB308; color: #1E293B; display: flex; align-items: center; justify-content: center;">-₹22,750 (Avoided PV)</div>
            </div>
            <div style="font-size: 11px; color: #64748B; margin-top: 5px; display: flex; justify-content: space-between;">
              <span>Net Farmer Outlay: 50.2%</span>
              <span>Avoided Standalone PV + 35% Capital Subsidy</span>
            </div>
          </div>
        </div>

        <div>
          <div style="font-size: 12px; font-weight: 700; text-transform: uppercase; color: #64748B; margin-bottom: 8px; letter-spacing: 0.05em;">
            Annual Value Accretion Engine (Per Farm)
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; font-size: 13px;">
            <div style="background: #F8FAFC; padding: 10px; border-radius: 6px; border: 1px solid #E2E8F0;">
              <div style="color: #64748B;">Spoilage Saved</div>
              <strong style="color: #15803D; font-size: 16px;">+₹15,732</strong>
            </div>
            <div style="background: #F8FAFC; padding: 10px; border-radius: 6px; border: 1px solid #E2E8F0;">
              <div style="color: #64748B;">Distress Timing</div>
              <strong style="color: #0284C7; font-size: 16px;">+₹12,000</strong>
            </div>
            <div style="background: #F8FAFC; padding: 10px; border-radius: 6px; border: 1px solid #E2E8F0;">
              <div style="color: #64748B;">Annual Opex</div>
              <strong style="color: #DC2626; font-size: 16px;">-₹2,400</strong>
            </div>
          </div>

          <div style="background: #F1F5F9; border-radius: 6px; padding: 10px 14px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center; font-size: 13px;">
            <span>Tier B Comparison (5 MT FPO Community Hub):</span>
            <span class="font-mono" style="font-weight: 700; color: #0284C7;">4.2-Year Payback (Leasing)</span>
          </div>
        </div>
      </div>

      <!-- Right: Payback Trajectory & BOM -->
      <div class="payback-card">
        <div>
          <div style="font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: #15803D; text-transform: uppercase;">
            Capital Recovery Dynamics
          </div>
          <h3 class="font-display" style="font-size: 21px; font-weight: 700; color: #0F172A; margin: 4px 0 12px 0;">
            Cumulative Cash Flow & 2.0-Year Breakeven
          </h3>

          <div style="display: flex; flex-direction: column; gap: 7px;">
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 14px; background: #FEF2F2; border-radius: 6px; font-size: 13.5px;">
              <span><strong>Day 0 (Initial Capex Investment):</strong></span>
              <span class="font-mono" style="color: #DC2626; font-weight: 700;">-₹50,212</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 14px; background: #FFFBEB; border-radius: 6px; font-size: 13.5px;">
              <span>End of Season 1 (Month 6):</span>
              <span class="font-mono" style="color: #D97706; font-weight: 600;">-₹37,546</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 14px; background: #F8FAFC; border-radius: 6px; font-size: 13.5px;">
              <span>End of Year 1 (Month 12):</span>
              <span class="font-mono" style="color: #475569; font-weight: 600;">-₹24,880</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 14px; background: #F8FAFC; border-radius: 6px; font-size: 13.5px;">
              <span>End of Season 3 (Month 18):</span>
              <span class="font-mono" style="color: #475569; font-weight: 600;">-₹12,214</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 14px; background: #F0FDF4; border: 1.5px solid #86EFAC; border-radius: 6px; font-size: 13.5px;">
              <span style="color: #166534; font-weight: 700;">Month 24 (Year 2.0) — FULL CAPITAL PAYBACK:</span>
              <span class="font-mono" style="color: #15803D; font-weight: 700; font-size: 15px;">+₹452 (Net Profit)</span>
            </div>
          </div>

          <!-- Breakeven Recovery Bar -->
          <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px 14px; margin-top: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
              <span style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">Breakeven Recovery Trajectory</span>
              <span class="font-mono" style="font-size: 11px; font-weight: 700; color: #15803D; background: #DCFCE7; padding: 2px 6px; border-radius: 4px;">IRR: 48.6%</span>
            </div>
            <div style="height: 8px; background: #E2E8F0; border-radius: 4px; overflow: hidden;">
              <div style="height: 100%; width: 100%; background: linear-gradient(90deg, #DC2626 0%, #D97706 40%, #15803D 100%);"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 10px; color: #64748B; margin-top: 4px; font-family: 'JetBrains Mono', monospace;">
              <span>M0: -₹50.2k</span>
              <span>M6: -₹37.5k</span>
              <span>M12: -₹24.9k</span>
              <span>M18: -₹12.2k</span>
              <span style="color: #15803D; font-weight: 700;">M24: Breakeven</span>
            </div>
          </div>
        </div>

        <div class="bom-box">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <strong style="font-size: 14px; color: #024230;">Industrial Edge Controller BoM (1,000-Unit Scale):</strong>
            <span class="font-mono" style="font-size: 18px; font-weight: 700; color: #0D8752;">₹7,540 / Unit</span>
          </div>
          <div style="font-size: 12px; color: #64748B; line-height: 1.45;">
            ESP32-S3 (₹420) • Isolated MAX485 (₹180) • Dual FDR Probes (₹760) • SHT31 (₹600) • Pulse Flow Meter (₹1,300) • Schneider TeSys D Contactors x2 (₹2,300) • 24V SMPS (₹380) • 4G LTE Module (₹620) • IP67 Enclosure & SPD (₹980).
          </div>
          <div style="font-size: 12px; color: #0D8752; font-weight: 600; margin-top: 6px;">
            Standalone Controller Payback: 1.5 crop seasons from pump maintenance & yield protection.
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar font-mono">
      <div>Financial Model: impact_model.py • Policy Alignment: MIDH Mission for Integrated Development of Horticulture</div>
      <div>AgroStruxure™ Commercial Feasibility • Slide 08 / 10</div>
    </div>
  </div>
</body>
</html>"""

# ==============================================================================
# SLIDE 09: COMMERCIALIZATION ROADMAP (Refined Continuous Progression)
# ==============================================================================
SLIDE_09 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .slide-body {{
      padding: 52px 76px 44px 76px;
      height: 1080px;
      width: 1920px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #11161B;
      color: #FFFFFF;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
    }}
    .tag-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #3DCD58;
      background: rgba(61, 205, 88, 0.12);
      border: 1px solid rgba(61, 205, 88, 0.3);
      padding: 6px 14px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .slide-hook {{
      font-size: 48px;
      font-weight: 700;
      color: #FFFFFF;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 6px;
    }}
    .slide-hook span {{ color: #3DCD58; }}
    .slide-sub {{
      font-size: 19px;
      color: #94A3B8;
      line-height: 1.4;
      max-width: 1280px;
      margin-bottom: 20px;
    }}
    .timeline-container {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }}
    .phases-row {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      position: relative;
    }}
    .phase-card {{
      background: #182026;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 22px 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 490px;
    }}
    .phase-badge {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 10px;
      width: fit-content;
    }}
    .badge-p1 {{ background: rgba(61, 205, 88, 0.2); color: #3DCD58; }}
    .badge-p2 {{ background: rgba(0, 135, 205, 0.2); color: #0087CD; }}
    .badge-p3 {{ background: rgba(255, 206, 0, 0.2); color: #FFCE00; }}
    .badge-p4 {{ background: rgba(168, 85, 247, 0.2); color: #A855F7; }}
    
    .phase-title {{
      font-size: 18px;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 10px;
      line-height: 1.25;
    }}
    .phase-bullets {{
      font-size: 13px;
      color: #94A3B8;
      line-height: 1.45;
      padding-left: 16px;
    }}
    .phase-bullets li {{ margin-bottom: 6px; }}
    .phase-bullets strong {{ color: #E2E8F0; }}
    
    .scale-metric {{
      font-family: 'Space Grotesk', sans-serif;
      font-size: 26px;
      font-weight: 700;
      margin: 10px 0 6px 0;
    }}
    
    .exit-gate {{
      background: rgba(0, 0, 0, 0.35);
      border-radius: 6px;
      padding: 10px 12px;
      border-left: 3px solid #3DCD58;
      font-size: 12px;
      color: #CBD5E1;
      margin-top: 10px;
    }}
    .scale-bar {{
      background: #182026;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 14px;
    }}
    .footer-bar {{
      padding-top: 16px;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #64748B;
    }}
  </style>
</head>
<body>
  <div class="slide-body">
    <div>
      <div class="header-bar">
        <div class="tag-pill">Deployment Strategy • De-Risked Scaling Trajectory</div>
        <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 34px; width: auto; filter: brightness(0) invert(1);">
      </div>
      <h1 class="slide-hook font-display">From Software Digital Twin to <span>250-Farm Commercial Pilot</span></h1>
      <p class="slide-sub">
        Structured execution pathway partnering with India's leading horticulture FPOs and Schneider Electric's rural distribution network.
      </p>
    </div>

    <div class="timeline-container">
      <!-- Continuous Scale Progress Ribbon -->
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.08); border-radius: 6px; padding: 8px 24px; font-family: 'JetBrains Mono', monospace; font-size: 12px;">
        <span style="color: #3DCD58; font-weight: 700;">● Phase 1: Digital Twin (Q4 2026)</span>
        <span style="color: #64748B;">────────►</span>
        <span style="color: #0087CD; font-weight: 700;">● Phase 2: HW Testbench (Q1–Q2 2027)</span>
        <span style="color: #64748B;">────────►</span>
        <span style="color: #FFCE00; font-weight: 700;">● Phase 3: 20-Farm Pilot (Q3–Q4 2027)</span>
        <span style="color: #64748B;">────────►</span>
        <span style="color: #A855F7; font-weight: 700;">● Phase 4: 250 Farms (2028 Scale)</span>
      </div>

      <div class="phases-row">
        <!-- Phase 1 -->
        <div class="phase-card" style="border-top: 3px solid #3DCD58;">
          <div>
            <span class="phase-badge badge-p1">PHASE 1 • CURRENT</span>
            <div class="phase-title font-display">Software Twin & Math Validation</div>
            <div class="scale-metric" style="color: #3DCD58;">0 Physical Units</div>
            <ul class="phase-bullets">
              <li><strong>Mathematical Truth:</strong> 365-day energy, water, and thermal balance derived in <code>impact_model.py</code>.</li>
              <li><strong>Modbus State Machine:</strong> Emulated Altivar ATV320 Command (8501) and Speed (8502) registers.</li>
              <li><strong>Vernacular NLP:</strong> Pydantic prompt guard verified for Marathi & Hindi voice note synthesis.</li>
              <li><strong>Zero-Cloud Guarantee:</strong> Deterministic C++ state machine runs without cellular dependency.</li>
            </ul>
          </div>
          <div class="exit-gate" style="border-left-color: #3DCD58;">
            <strong style="color: #3DCD58;">Exit Gate:</strong> Zero discrepancies in mathematical mass and thermal balances.
          </div>
        </div>

        <!-- Phase 2 -->
        <div class="phase-card" style="border-top: 3px solid #0087CD;">
          <div>
            <span class="phase-badge badge-p2">PHASE 2 • Q1–Q2 2027</span>
            <div class="phase-title font-display">Hardware-in-the-Loop Testbench</div>
            <div class="scale-metric" style="color: #0087CD;">1 Testbench</div>
            <ul class="phase-bullets">
              <li><strong>Physical Bench:</strong> ESP32-S3 paired with Schneider Altivar ATV320 solar VFD & motor dynamometer.</li>
              <li><strong>Switchgear Safety:</strong> 5.0s DC dead-band dwell verified under 500V DC break conditions.</li>
              <li><strong>Surge Resilience:</strong> Type-2 DC SPD endurance testing against 1,000V DC lightning transients.</li>
              <li><strong>Inverter Protection:</strong> Validated zero IGBT punch-through across 500 repeated transfer cycles.</li>
            </ul>
          </div>
          <div class="exit-gate" style="border-left-color: #0087CD;">
            <strong style="color: #0087CD;">Exit Gate:</strong> 500 faultless DC transfer cycles under full electrical load without drive trip.
          </div>
        </div>

        <!-- Phase 3 -->
        <div class="phase-card" style="border-top: 3px solid #FFCE00;">
          <div>
            <span class="phase-badge badge-p3">PHASE 3 • Q3–Q4 2027</span>
            <div class="phase-title font-display">20-Farm FPO Pilot (Nashik)</div>
            <div class="scale-metric" style="color: #FFCE00;">20 Farms (5 Clusters)</div>
            <ul class="phase-bullets">
              <li><strong>Field Partnership:</strong> Deployed across 5 clusters (4 farms each) with Sahyadri Farmers Producer Co.</li>
              <li><strong>Real Tomato Harvest:</strong> Continuous FDR root monitoring & pre-cooling connected to reefer transport.</li>
              <li><strong>Farmer Trust Loop:</strong> Daily spoken WhatsApp notes achieving 98%+ farmer comprehension.</li>
              <li><strong>Agronomic Cutoff:</strong> Validated collar rot prevention across two full Solanaceae harvest cycles.</li>
            </ul>
          </div>
          <div class="exit-gate" style="border-left-color: #FFCE00;">
            <strong style="color: #FFCE00;">Exit Gate:</strong> Measured >35% water conservation & 95%+ pre-cooler uptime over 2 seasons.
          </div>
        </div>

        <!-- Phase 4 -->
        <div class="phase-card" style="border-top: 3px solid #A855F7;">
          <div>
            <span class="phase-badge badge-p4">PHASE 4 • 2028</span>
            <div class="phase-title font-display">250-Farm Commercial Expansion</div>
            <div class="scale-metric" style="color: #A855F7;">250 Farms (5 FPOs)</div>
            <ul class="phase-bullets">
              <li><strong>OEM Retrofit Skids:</strong> Factory-assembled DIN rail kits reducing solar pump EPC install time to 2 hours.</li>
              <li><strong>"Urja Mitra" Network:</strong> Local ITI diploma youth trained for sensor calibration & field servicing.</li>
              <li><strong>Carbon Revenue:</strong> Aggregating 2.94 t CO₂e/ha/yr for verified voluntary carbon credit issuance.</li>
              <li><strong>Channel Synergy:</strong> Pre-integrated as catalog option with Schneider Electric Rural EPC network.</li>
            </ul>
          </div>
          <div class="exit-gate" style="border-left-color: #A855F7;">
            <strong style="color: #A855F7;">Exit Gate:</strong> Commercial breakeven with 5 FPO enterprise contracts in Maharashtra & Rajasthan.
          </div>
        </div>
      </div>

      <div class="scale-bar">
        <div style="font-size: 13px; color: #94A3B8;">
          <strong style="color: #3DCD58;">Government & Institutional Enablers:</strong> PM-KUSUM Component B (Pumps) • Atal Bhujal Yojana (Aquifer Quotas) • MIDH/AIF (35% Subsidies)
        </div>
        <div class="font-mono" style="font-size: 14px; color: #FFCE00; font-weight: 700;">
          National Market Size: 10.9 Lakh Standalone Solar Pumps
        </div>
      </div>
    </div>

    <div class="footer-bar font-mono">
      <div>Scale Partner: Sahyadri Farmers Producer Co. (India's Largest Horticulture FPO) • Schneider Electric Rural EPCs</div>
      <div>AgroStruxure™ Commercialization Roadmap • Slide 09 / 10</div>
    </div>
  </div>
</body>
</html>"""

# ==============================================================================
# SLIDE 10: VISIONARY CLOSING & TEAM (Refined: Balanced Vertical Grid)
# ==============================================================================
SLIDE_10 = f"""<!DOCTYPE html>
<html lang="en">
<head>
  {HTML_HEAD}
  <style>
    .slide-body {{
      padding: 56px 80px 48px 80px;
      height: 1080px;
      width: 1920px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: #024230;
      color: #FFFFFF;
    }}
    .header-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }}
    .tag-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      font-weight: 700;
      color: #3DCD58;
      background: rgba(61, 205, 88, 0.15);
      border: 1px solid rgba(61, 205, 88, 0.35);
      padding: 6px 14px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}
    .slide-hook {{
      font-size: 52px;
      font-weight: 700;
      color: #FFFFFF;
      line-height: 1.1;
      letter-spacing: -0.02em;
      margin-bottom: 8px;
    }}
    .slide-hook span {{ color: #3DCD58; }}
    .slide-sub {{
      font-size: 20px;
      color: #A7F3D0;
      line-height: 1.45;
      max-width: 1240px;
      margin-bottom: 24px;
    }}
    .outcomes-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 22px;
      margin-bottom: 22px;
    }}
    .outcome-card {{
      background: rgba(13, 135, 82, 0.25);
      border: 1px solid rgba(61, 205, 88, 0.3);
      border-radius: 12px;
      padding: 24px 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 220px;
    }}
    .outcome-num {{
      font-size: 44px;
      font-weight: 700;
      font-family: 'Space Grotesk', sans-serif;
      line-height: 1;
      margin-bottom: 8px;
    }}
    .outcome-title {{
      font-size: 16px;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 6px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .outcome-desc {{
      font-size: 13px;
      color: #CBD5E1;
      line-height: 1.45;
    }}
    .team-strip {{
      background: rgba(0, 0, 0, 0.35);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 10px;
      padding: 22px 24px;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 20px;
      margin-bottom: 16px;
    }}
    .team-member {{
      border-left: 2px solid #3DCD58;
      padding-left: 14px;
    }}
    .member-name {{
      font-size: 17px;
      font-weight: 700;
      color: #FFFFFF;
    }}
    .member-role {{
      font-size: 12px;
      color: #3DCD58;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-top: 3px;
    }}
    .member-spec {{
      font-size: 12px;
      color: #94A3B8;
      margin-top: 4px;
      line-height: 1.35;
    }}
    .strategic-box {{
      background: rgba(61, 205, 88, 0.1);
      border: 1px solid rgba(61, 205, 88, 0.25);
      border-radius: 8px;
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 13px;
    }}
    .footer-bar {{
      padding-top: 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.15);
      display: flex;
      justify-content: space-between;
      font-size: 13px;
      color: #6EE7B7;
    }}
  </style>
</head>
<body>
  <div class="slide-body">
    <div>
      <div class="header-bar">
        <div class="tag-pill">Executive Synthesis • Yuva Yodha Hackathon 2026</div>
        <img src="{SVG_LOGO}" alt="Schneider Electric" style="height: 38px; width: auto; filter: brightness(0) invert(1);">
      </div>
      <h1 class="slide-hook font-display">One Solar Pump. <span>Four System Outcomes.</span></h1>
      <p class="slide-sub">
        AgroStruxure creates a high-margin digital IoT layer for Schneider Altivar Solar drives and TeSys switchgear, turning agricultural clean-tech from standalone pumps into connected community microgrids.
      </p>
    </div>

    <div>
      <div class="outcomes-grid">
        <div class="outcome-card">
          <div>
            <div class="outcome-num" style="color: #38BDF8;">41.2%</div>
            <div class="outcome-title">Water Conserved</div>
            <div class="outcome-desc">
              7,000 m³/ha/yr aquifer water saved. Root-zone hypoxia eliminated, stabilizing critical groundwater tables.
            </div>
          </div>
        </div>

        <div class="outcome-card">
          <div>
            <div class="outcome-num" style="color: #FBBF24;">4,137 <span style="font-size: 22px;">kWh</span></div>
            <div class="outcome-title">Clean Energy Captured</div>
            <div class="outcome-desc">
              Surplus solar redirected upstream on DC bus into 2 MT cold storage, avoiding dedicated solar capex.
            </div>
          </div>
        </div>

        <div class="outcome-card">
          <div>
            <div class="outcome-num" style="color: #C084FC;">1.31 <span style="font-size: 22px;">Tonnes</span></div>
            <div class="outcome-title">Produce Preserved</div>
            <div class="outcome-desc">
              Farm-stage spoilage halved from 8.37% to 4.00%. First-mile pre-cooling extends shelf life by 4–7 days.
            </div>
          </div>
        </div>

        <div class="outcome-card">
          <div>
            <div class="outcome-num" style="color: #4ADE80;">2.0 <span style="font-size: 22px;">Years</span></div>
            <div class="outcome-title">Capital Payback</div>
            <div class="outcome-desc">
              ₹50,212 net capex recovered in 2 crop harvests. Generates +₹25,332/farm/yr in ongoing net profits.
            </div>
          </div>
        </div>
      </div>

      <div class="team-strip">
        <div class="team-member">
          <div class="member-name">Sanskar Tiwari</div>
          <div class="member-role">Embedded Firmware & Lead</div>
          <div class="member-spec">FreeRTOS deterministic state machine, Modbus RTU, CiA402 drive control.</div>
        </div>

        <div class="team-member">
          <div class="member-name">Shambhavi Patil</div>
          <div class="member-role">Geospatial Intelligence</div>
          <div class="member-spec">Sentinel-2 MSI 10m NDVI/NDWI, dynamic FAO-56 dual Kc curves, aquifer balance.</div>
        </div>

        <div class="team-member">
          <div class="member-name">Kanishka Salgude</div>
          <div class="member-role">Electrical Systems & VFD</div>
          <div class="member-spec">Schneider Altivar ATV320 VFD configuration, TeSys D interlocking, DC power routing.</div>
        </div>

        <div class="team-member">
          <div class="member-name">Chaitanya Ranade</div>
          <div class="member-role">Product Strategy & Agronomy</div>
          <div class="member-spec">Sahyadri FPO cluster economics, MIDH/AIF subsidies, vernacular WhatsApp bot UX.</div>
        </div>
      </div>

      <div class="strategic-box">
        <div>
          <strong style="color: #3DCD58;">Schneider Electric Strategic Synergies:</strong> Altivar Solar Drives OEM Pre-Installation • EcoStruxure Microgrid Edge Integration • SE Ventures Cleantech Scale
        </div>
        <div class="font-mono" style="font-size: 14px; color: #FFFFFF; font-weight: 700;">
          Net Decarbonization: 2.94 t CO₂e / ha / year
        </div>
      </div>
    </div>

    <div class="footer-bar font-mono">
      <div>Schneider Electric India • SE Ventures • Yuva Yodha Energy Tech Hackathon 2026</div>
      <div style="color: #3DCD58; font-weight: 700;">Challenge 01: Sustainable Agriculture</div>
    </div>
  </div>
</body>
</html>"""

SLIDES = [
    ("slide_01.html", SLIDE_01),
    ("slide_02.html", SLIDE_02),
    ("slide_03.html", SLIDE_03),
    ("slide_04.html", SLIDE_04),
    ("slide_05.html", SLIDE_05),
    ("slide_06.html", SLIDE_06),
    ("slide_07.html", SLIDE_07),
    ("slide_08.html", SLIDE_08),
    ("slide_09.html", SLIDE_09),
    ("slide_10.html", SLIDE_10),
]

print("Step 2: Writing individual standalone slide HTML files...")
for fname, content in SLIDES:
    p = os.path.join(SLIDES_DIR, fname)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] Saved {p}")

print("Step 3: Creating Master Deck presentation (index.html)...")
master_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AgroStruxure™ | Yuva Yodha Hackathon 2026 Pitch Deck</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #070B0D;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      overflow: hidden;
      font-family: sans-serif;
    }}
    #presentation-viewport {{
      width: 100vw;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }}
    #stage-scaler {{
      width: 1920px;
      height: 1080px;
      transform-origin: center center;
      position: absolute;
      box-shadow: 0 25px 70px rgba(0,0,0,0.8);
      background: #000;
    }}
    .slide-frame {{
      width: 1920px;
      height: 1080px;
      border: none;
      display: none;
      position: absolute;
      top: 0; left: 0;
    }}
    .slide-frame.active {{
      display: block;
    }}
    #nav-controls {{
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 20, 22, 0.85);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 30px;
      padding: 8px 18px;
      display: flex;
      align-items: center;
      gap: 16px;
      z-index: 1000;
      color: #FFFFFF;
      font-size: 14px;
      font-family: monospace;
      opacity: 0.4;
      transition: opacity 0.2s;
    }}
    #nav-controls:hover {{ opacity: 1; }}
    .nav-btn {{
      background: none;
      border: none;
      color: #3DCD58;
      cursor: pointer;
      font-size: 16px;
      font-weight: bold;
      padding: 4px 8px;
    }}
  </style>
</head>
<body>
  <div id="presentation-viewport">
    <div id="stage-scaler">
"""

for i in range(1, 11):
    active_cls = " active" if i == 1 else ""
    master_html += f'      <iframe class="slide-frame{active_cls}" id="frame-{i}" src="slides/slide_{i:02d}.html"></iframe>\n'

master_html += """    </div>
  </div>

  <div id="nav-controls">
    <button class="nav-btn" onclick="prevSlide()">&larr; Prev</button>
    <span id="slide-indicator">01 / 10</span>
    <button class="nav-btn" onclick="nextSlide()">Next &rarr;</button>
    <span style="color: #64748B; font-size: 12px;">(Arrow Keys / Space)</span>
  </div>

  <script>
    let currentSlide = 1;
    const totalSlides = 10;

    function updateScale() {
      const scaler = document.getElementById('stage-scaler');
      const w = window.innerWidth;
      const h = window.innerHeight;
      const scale = Math.min(w / 1920, h / 1080);
      scaler.style.transform = `scale(${scale})`;
    }

    window.addEventListener('resize', updateScale);
    updateScale();

    function showSlide(n) {
      if (n < 1 || n > totalSlides) return;
      currentSlide = n;
      for (let i = 1; i <= totalSlides; i++) {
        const frame = document.getElementById(`frame-${i}`);
        if (i === n) {
          frame.classList.add('active');
        } else {
          frame.classList.remove('active');
        }
      }
      document.getElementById('slide-indicator').innerText = `${String(n).padStart(2, '0')} / ${String(totalSlides).padStart(2, '0')}`;
    }

    function nextSlide() { showSlide(currentSlide + 1); }
    function prevSlide() { showSlide(currentSlide - 1); }

    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === 'Space' || e.key === 'PageDown') {
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        prevSlide();
      } else if (e.key === 'Home') {
        showSlide(1);
      } else if (e.key === 'End') {
        showSlide(totalSlides);
      }
    });
  </script>
</body>
</html>"""

with open(os.path.join(SOURCE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(master_html)
print(f"  [OK] Saved Master Deck to {os.path.join(SOURCE_DIR, 'index.html')}")

with open(os.path.join(BASE_DIR, "presentation.html"), "w", encoding="utf-8") as f:
    f.write(master_html.replace('src="slides/', 'src="presentation/source/slides/'))

print("Step 4: Rendering high-resolution screenshots via headless Chrome...")
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
rendered_pngs = []

for i in range(1, 11):
    slide_html_path = os.path.join(SLIDES_DIR, f"slide_{i:02d}.html")
    qa_png_path = os.path.join(QA_DIR, f"slide_{i:02d}.png")
    root_png_path = os.path.join(BASE_DIR, f"slide_{i:02d}.png")
    rendered_dir_png = os.path.join(RENDERED_DIR, f"slide_{i:02d}.png")
    
    file_url = "file:///" + os.path.abspath(slide_html_path).replace("\\", "/")
    
    cmd = [
        chrome_path,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--window-size=1920,1080",
        f"--screenshot={os.path.abspath(qa_png_path)}",
        file_url
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if os.path.exists(qa_png_path) and os.path.getsize(qa_png_path) > 10000:
        rendered_pngs.append(qa_png_path)
        shutil.copyfile(qa_png_path, root_png_path)
        shutil.copyfile(qa_png_path, rendered_dir_png)
        print(f"  [OK] Rendered Slide {i:02d} ({os.path.getsize(qa_png_path):,} bytes)")
    else:
        print(f"  [FAIL] Error rendering slide_{i:02d}.png: {res.stderr.decode('utf-8', errors='ignore')}")

print(f"Step 5: Compiling 16:9 PDF Presentation ({len(rendered_pngs)} slides)...")
if rendered_pngs:
    pdf_final = os.path.join(FINAL_DIR, "AgroStruxure_YuvaYodha_2026_Final.pdf")
    pdf_root = os.path.join(BASE_DIR, "AgroStruxure_YuvaYodha_2026_Final.pdf")
    
    images = [Image.open(p).convert("RGB") for p in rendered_pngs]
    images[0].save(pdf_final, save_all=True, append_images=images[1:], resolution=150.0, quality=95)
    shutil.copyfile(pdf_final, pdf_root)
    print(f"  [OK] Successfully compiled PDF: {pdf_final} ({os.path.getsize(pdf_final):,} bytes)")

print("Step 6: Generating Native PowerPoint Deck (AgroStruxure_YuvaYodha_2026_Final.pptx)...")
prs = pptx.Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

for idx, p in enumerate(rendered_pngs, start=1):
    slide = prs.slides.add_slide(blank_layout)
    slide.shapes.add_picture(p, 0, 0, width=prs.slide_width, height=prs.slide_height)
    print(f"  [OK] Added Slide {idx:02d} to PPTX")

pptx_final = os.path.join(FINAL_DIR, "AgroStruxure_YuvaYodha_2026_Final.pptx")
pptx_root = os.path.join(BASE_DIR, "AgroStruxure_YuvaYodha_2026_Final.pptx")
prs.save(pptx_final)
shutil.copyfile(pptx_final, pptx_root)
print(f"  [OK] Successfully saved PowerPoint: {pptx_final} ({os.path.getsize(pptx_final):,} bytes)")

print("\nPass 2 Refinement completed successfully!")
