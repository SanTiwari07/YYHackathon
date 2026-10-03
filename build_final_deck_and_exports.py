# -*- coding: utf-8 -*-
"""
AgroStruxure™ Master Deck Builder & Exporter
Yuva Yodha Energy Tech Hackathon 2026
Schneider Electric India & YouNoodle
"""

import os
import base64
import subprocess
from PIL import Image
import pptx
from pptx.util import Inches

def get_base64_uri(file_path, mime_type):
    with open(file_path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:{mime_type};base64,{data}"

def build():
    base_dir = r"D:\Research Work\YuvaYodhaHackathon Research"
    assets_dir = os.path.join(base_dir, "assets")
    
    # 1. Encode assets
    print("Encoding visual assets to data URIs...")
    img_solar = get_base64_uri(os.path.join(assets_dir, "solar_panels_farm_opt.jpg"), "image/jpeg")
    img_field = get_base64_uri(os.path.join(assets_dir, "indian_agriculture_field.jpg"), "image/jpeg")
    img_drip = get_base64_uri(os.path.join(assets_dir, "drip_irrigation_farm.jpg"), "image/jpeg")
    img_tomato = get_base64_uri(os.path.join(assets_dir, "tomato_harvest.jpg"), "image/jpeg")
    logo_schneider = get_base64_uri(os.path.join(assets_dir, "schneider_electric_logo.svg"), "image/svg+xml")

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AgroStruxure™ | Yuva Yodha Energy Tech Hackathon 2026</title>
  
  <!-- Typography Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&family=Poppins:wght@600;700;800&family=Noto+Sans+Devanagari:wght@400;600&display=swap" rel="stylesheet">

  <style>
    /* ==========================================================================
       DESIGN SYSTEM TOKENS (Authoritative: DESIGN_SYSTEM.md)
       Light Theme Architecture Inspired by Frontend Slides Blue Professional
       ========================================================================== */
    :root {{
      /* Brand & Accent Colors */
      --se-primary: #3DCD58;       /* Schneider "Life Is On" Green */
      --se-primary-hover: #32AD3C;
      --yy-deep-forest: #024230;   /* Deep Dark Emerald */
      --yy-emerald: #0D8752;       /* Mid Emerald */
      --yy-solar-gold: #FFCE00;    /* PM-KUSUM Solar Gold */
      --color-water: #0087CD;      /* Water Cyan */
      --color-cold-room: #8015E8;  /* Thermal Storage Purple */
      --color-transient: #E47F00;  /* Cloud Transient Amber */
      --color-alarm: #DC0A0A;      /* Alert Red */
      --color-standby: #9FA0A4;    /* Neutral Slate Gray */

      /* Light Theme Surfaces & Neutrals */
      --surface-canvas: #F8FAFC;   /* Primary Slide Canvas (Slate-50) */
      --surface-card: #FFFFFF;     /* Elevated Card Surface */
      --surface-subtle: #F1F5F9;   /* Inner Recessed Box Surface */
      --border-subtle: #E2E8F0;    /* 1px Structural Border */
      --border-focus: #CBD5E1;     /* Focus / Emphasized Border */

      /* Typography Tokens */
      --text-primary: #090B0C;     /* High-Contrast Charcoal Black */
      --text-secondary: #5C6466;   /* Muted Slate Body Copy */
      --text-tertiary: #94A3B8;    /* Caption & Micro-Copy */

      /* Fonts */
      --font-display: 'Poppins', system-ui, -apple-system, sans-serif;
      --font-body: 'Inter', system-ui, -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
      --font-devanagari: 'Noto Sans Devanagari', sans-serif;

      /* Spacing Scale (8pt Grid) */
      --space-1: 4px;
      --space-2: 8px;
      --space-3: 12px;
      --space-4: 16px;
      --space-5: 20px;
      --space-6: 24px;
      --space-8: 32px;
      --space-10: 40px;
      --space-12: 48px;

      /* Border Radii */
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --radius-pill: 9999px;

      /* Subtle Shadows (No Heavy Blurs) */
      --shadow-card: 0 2px 8px -2px rgba(15, 23, 42, 0.05), 0 1px 4px -1px rgba(15, 23, 42, 0.03);
      --shadow-hover: 0 8px 16px -4px rgba(15, 23, 42, 0.08);
      --shadow-float: 0 12px 28px -6px rgba(15, 23, 42, 0.12);
    }}

    /* Reset & Base Stage Setup */
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: #0F172A; /* Dark theater surround outside the 16:9 canvas */
      font-family: var(--font-body);
      color: var(--text-primary);
      -webkit-font-smoothing: antialiased;
    }}

    #presentation-stage {{
      position: absolute;
      top: 50%;
      left: 50%;
      width: 1920px;
      height: 1080px;
      transform-origin: center center;
      transform: translate(-50%, -50%) scale(1);
      background-color: var(--surface-canvas);
      overflow: hidden;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.4);
    }}

    .slide {{
      position: absolute;
      top: 0;
      left: 0;
      width: 1920px;
      height: 1080px;
      padding: 56px 72px 48px 72px;
      display: none;
      flex-direction: column;
      justify-content: space-between;
      opacity: 0;
      transition: opacity 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      background-color: var(--surface-canvas);
    }}

    .slide.active {{
      display: flex;
      opacity: 1;
    }}

    /* Common Slide Header */
    .slide-header {{
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border-subtle);
      margin-bottom: 24px;
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .project-badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background-color: #E8F8ED;
      color: var(--yy-emerald);
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 13px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      border-radius: var(--radius-pill);
      border: 1px solid #B8E8C7;
    }}

    .header-context {{
      font-size: 14px;
      font-weight: 500;
      color: var(--text-secondary);
      letter-spacing: 0.01em;
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 24px;
    }}

    .slide-counter {{
      font-family: var(--font-mono);
      font-size: 15px;
      font-weight: 600;
      color: var(--text-secondary);
      background: var(--surface-card);
      padding: 5px 14px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-subtle);
    }}

    .schneider-logo {{
      height: 38px;
      width: auto;
      display: block;
      object-fit: contain;
    }}

    /* Slide Title Area */
    .slide-title-block {{
      margin-bottom: 24px;
    }}

    .slide-eyebrow {{
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--yy-emerald);
      margin-bottom: 6px;
    }}

    .slide-title {{
      font-family: var(--font-display);
      font-size: 38px;
      font-weight: 700;
      line-height: 1.15;
      color: var(--text-primary);
      letter-spacing: -0.02em;
    }}

    .slide-subtitle {{
      font-size: 17px;
      color: var(--text-secondary);
      margin-top: 6px;
      font-weight: 400;
    }}

    /* Layout Utility Containers */
    .slide-body {{
      flex: 1;
      display: flex;
      gap: 32px;
      min-height: 0;
      position: relative;
    }}

    .card {{
      background: var(--surface-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 24px 28px;
      box-shadow: var(--shadow-card);
      display: flex;
      flex-direction: column;
    }}

    .card-title {{
      font-family: var(--font-display);
      font-size: 19px;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .card-subtitle {{
      font-size: 14px;
      color: var(--text-secondary);
      line-height: 1.5;
      margin-bottom: 16px;
    }}

    /* Metric Callout Component */
    .metric-pill-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      width: 100%;
    }}

    .metric-pill {{
      background: var(--surface-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-md);
      padding: 18px 22px;
      box-shadow: var(--shadow-card);
      position: relative;
      overflow: hidden;
    }}

    .metric-pill::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
      background: var(--se-primary);
    }}

    .metric-pill.cyan::before {{ background: var(--color-water); }}
    .metric-pill.gold::before {{ background: var(--yy-solar-gold); }}
    .metric-pill.purple::before {{ background: var(--color-cold-room); }}

    .metric-val {{
      font-family: var(--font-display);
      font-size: 40px;
      font-weight: 800;
      line-height: 1;
      color: var(--text-primary);
      letter-spacing: -0.03em;
      margin-bottom: 4px;
    }}

    .metric-val span {{
      font-size: 24px;
      font-weight: 600;
      color: var(--text-secondary);
      margin-left: 2px;
    }}

    .metric-label {{
      font-family: var(--font-display);
      font-size: 14px;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 4px;
    }}

    .metric-desc {{
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.4;
    }}

    /* Media Split Components */
    .media-card {{
      position: relative;
      border-radius: var(--radius-lg);
      overflow: hidden;
      box-shadow: var(--shadow-card);
      border: 1px solid var(--border-subtle);
      background: #E2E8F0;
    }}

    .media-card img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}

    .media-tag {{
      position: absolute;
      bottom: 16px;
      left: 16px;
      right: 16px;
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: blur(8px);
      padding: 10px 16px;
      border-radius: var(--radius-sm);
      font-size: 12px;
      font-weight: 500;
      color: var(--text-primary);
      border: 1px solid rgba(226, 232, 240, 0.8);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    /* Slide Footer Controls */
    .slide-footer {{
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 18px;
      border-top: 1px solid var(--border-subtle);
      margin-top: 20px;
      font-size: 13px;
      color: var(--text-tertiary);
    }}

    .nav-controls {{
      display: flex;
      gap: 12px;
    }}

    .nav-btn {{
      background: var(--surface-card);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-pill);
      padding: 8px 18px;
      font-family: var(--font-display);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-primary);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
      transition: all 0.15s ease;
    }}

    .nav-btn:hover {{
      background: #F8FAFC;
      border-color: var(--border-focus);
      color: var(--yy-emerald);
    }}

    /* SVG Icon Helpers */
    .icon {{
      width: 18px;
      height: 18px;
      stroke-width: 2.2;
      stroke: currentColor;
      fill: none;
      stroke-linecap: round;
      stroke-linejoin: round;
      display: inline-block;
      vertical-align: middle;
    }}
  </style>
</head>
<body>

  <div id="presentation-stage">

    <!-- ====================================================================
         SLIDE 01: COVER / TITLE & EXECUTIVE HOOK
         ==================================================================== -->
    <div class="slide active" id="slide-1">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">Challenge 01: Sustainable Agriculture</span>
          <span class="header-context">Yuva Yodha Energy Tech Hackathon 2026</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">01 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-body" style="gap: 48px;">
        <!-- Left Hero Narrative (54%) -->
        <div style="flex: 1.15; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div class="slide-eyebrow" style="color: var(--yy-emerald); font-size: 15px;">SCHNEIDER ELECTRIC INDIA • STUDENT INNOVATION TRACK</div>
            <h1 style="font-family: var(--font-display); font-size: 58px; font-weight: 800; line-height: 1.08; color: var(--text-primary); letter-spacing: -0.03em; margin: 12px 0 16px 0;">
              AgroStruxure™
            </h1>
            <p style="font-size: 22px; font-weight: 600; line-height: 1.35; color: var(--yy-deep-forest); margin-bottom: 18px;">
              Solar-Synchronized Agri-Energy Microgrid & Closed-Loop Precision Irrigation
            </p>
            <p style="font-size: 16px; line-height: 1.6; color: var(--text-secondary); max-width: 900px;">
              Decoupling agricultural water pumping from free solar energy to eliminate the <strong>Solar Rebound Paradox</strong> across 10.9 lakh PM-KUSUM installations. By synchronizing pumping with soil physics, AgroStruxure cuts groundwater extraction by <strong>41.2%</strong> and channels <strong>3,187 kWh/yr</strong> of idle solar surplus into farm-gate micro-cold chains.
            </p>
          </div>

          <!-- Bottom 3 Impact Anchor Cards -->
          <div class="metric-pill-grid">
            <div class="metric-pill cyan">
              <div class="metric-val">41.2<span>%</span></div>
              <div class="metric-label">Water Conserved</div>
              <div class="metric-desc">7,000 m³/ha/yr saved via dual-depth soil cutoff</div>
            </div>
            <div class="metric-pill gold">
              <div class="metric-val">3,187<span>kWh</span></div>
              <div class="metric-label">Solar Surplus Captured</div>
              <div class="metric-desc">77% of idle solar redirected to cooling</div>
            </div>
            <div class="metric-pill purple">
              <div class="metric-val">2.0<span>Yrs</span></div>
              <div class="metric-label">Cluster Payback</div>
              <div class="metric-desc">Tier A 4-farm pre-cooler sharing model</div>
            </div>
          </div>

          <!-- Authors & Academic Team Tag -->
          <div style="display: flex; align-items: center; gap: 16px; padding: 14px 20px; background: var(--surface-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md);">
            <svg class="icon" style="color: var(--yy-emerald);" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <div style="font-size: 13px; color: var(--text-secondary);">
              <strong style="color: var(--text-primary); font-weight: 600;">Engineering Team:</strong> Sanskar Tiwari (Firmware/Lead) • Shambhavi Patil (Geospatial) • Kanishka Salgude (Power/VFD) • Chaitanya Ranade (Agronomy/Product)
            </div>
          </div>
        </div>

        <!-- Right Visual Split (46%) -->
        <div style="flex: 0.85; position: relative;">
          <div class="media-card" style="height: 100%;">
            <img src="{img_solar}" alt="PM-KUSUM Solar Farm in Maharashtra">
            <div class="media-tag">
              <span><strong>PM-KUSUM Component B:</strong> 4.8 kWp Standalone Array (Nashik, MH)</span>
              <span style="font-family: var(--font-mono); color: var(--yy-emerald); font-weight: 600;">6,559 kWh/yr Total PV</span>
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>AgroStruxure™ Technical Pitch Deck • Confidential & Proprietary</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="nextSlide()">Next Slide <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></button>
        </div>
      </div>
    </div>


    <!-- ====================================================================
         SLIDE 02: THE SOLAR REBOUND PARADOX (PROBLEM FRAMING)
         ==================================================================== -->
    <div class="slide" id="slide-2">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">Problem Space</span>
          <span class="header-context">Systemic Bottleneck in Distributed Solar Agriculture</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">02 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-title-block">
        <div class="slide-eyebrow">THE SYSTEMIC REBOUND EFFECT</div>
        <h2 class="slide-title">Free Solar Pumping is Draining India's Aquifers</h2>
        <p class="slide-subtitle">Under PM-KUSUM Component B, zero-marginal-cost electricity incentivizes unconstrained pumping, wasting solar energy and desiccating ground reserves.</p>
      </div>

      <div class="slide-body">
        <!-- Left Editorial Photo Split (38%) -->
        <div style="flex: 0.38;">
          <div class="media-card" style="height: 100%;">
            <img src="{img_field}" alt="Semi-Arid Farmland in India">
            <div class="media-tag" style="flex-direction: column; align-items: flex-start; gap: 4px;">
              <span style="font-weight: 700; color: var(--color-alarm);">The Marathwada & Vidarbha Groundwater Crisis</span>
              <span style="font-size: 11px; color: var(--text-secondary);">CGWB Report 2023: Critical water table decline exceeding 2.5m/yr in 31% of semi-arid blocks.</span>
            </div>
          </div>
        </div>

        <!-- Right 3-Pillar Conflict Breakdown (62%) -->
        <div style="flex: 0.62; display: flex; flex-direction: column; gap: 16px;">
          <!-- Card 1 -->
          <div class="card" style="border-left: 5px solid var(--color-water);">
            <div class="card-title">
              <svg class="icon" style="color: var(--color-water);" viewBox="0 0 24 24"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>
              1. Unconstrained Extraction & Root Waterlogging (17,000 m³/ha/yr)
            </div>
            <p style="font-size: 14px; color: var(--text-secondary); line-height: 1.55;">
              Because solar power incurs zero billing friction, farmers operate pumps whenever sunlight is available (850 mm/season across flood basins). This results in root zone anoxia, fungal pathogens, nutrient leaching, and severe regional aquifer depletion without boosting yield.
            </p>
          </div>

          <!-- Card 2 -->
          <div class="card" style="border-left: 5px solid var(--yy-solar-gold);">
            <div class="card-title">
              <svg class="icon" style="color: #B98300;" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
              2. 4,137 kWh of Solar Energy Wasted Idle Annually (63% Curtailment)
            </div>
            <p style="font-size: 14px; color: var(--text-secondary); line-height: 1.55;">
              A 4.8 kWp standalone PV array generates 6,559 kWh/year. Pumping only requires 2,422 kWh/year. Corroborating Shah et al. (IWMI), <strong>nearly two-thirds (63.07%)</strong> of capital-subsidized solar power sits completely unused once farm ditches or storage ponds reach capacity.
            </p>
          </div>

          <!-- Card 3 -->
          <div class="card" style="border-left: 5px solid var(--color-cold-room);">
            <div class="card-title">
              <svg class="icon" style="color: var(--color-cold-room);" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
              3. 8.37% Farm-Gate Spoilage from Missing First-Mile Cooling
            </div>
            <p style="font-size: 14px; color: var(--text-secondary); line-height: 1.55;">
              Per NABCONS 2022, 8.37% of harvested tomatoes rot before leaving the farm gate due to extreme field respiration heat (32°C). Farmers face severe distress selling at local APMC mandis (selling at ₹2–₹4/kg vs ₹12/kg market benchmark) because decentralized pre-cooling is inaccessible.
            </p>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>Baseline Data Sources: CGWB 2023, NABCONS 2022 Post-Harvest Loss Study, Shah et al. (IWMI)</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="nextSlide()">Next Slide <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></button>
        </div>
      </div>
    </div>


    <!-- ====================================================================
         SLIDE 03: THE SOLUTION / SYSTEM ARCHITECTURE
         ==================================================================== -->
    <div class="slide" id="slide-3">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">System Architecture</span>
          <span class="header-context">EcoStruxure-Aligned Edge Control & Power Routing</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">03 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-title-block">
        <div class="slide-eyebrow">CLOSED-LOOP AUTOMATION</div>
        <h2 class="slide-title">AgroStruxure™ Architecture: Sense, Control & Divert</h2>
        <p class="slide-subtitle">A ruggedized industrial retrofit kit that transforms standalone solar pumps into intelligent, multi-function agri-energy microgrids without replacing existing motors or PV panels.</p>
      </div>

      <div class="slide-body" style="gap: 24px;">
        <!-- Column 1: Physical Sensing -->
        <div class="card" style="flex: 1;">
          <div class="card-title">
            <span style="background: #E8F8ED; color: var(--yy-emerald); padding: 4px 10px; border-radius: var(--radius-sm); font-size: 14px;">LAYER 1</span>
            Ground Physics & Sensing
          </div>
          <div class="card-subtitle">Real-time hydrological inputs and microclimate telemetry.</div>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 14px; font-size: 14px; color: var(--text-secondary); line-height: 1.5;">
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--se-primary); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">Dual-Depth FDR Probes:</strong> High-frequency capacitive soil sensors at 10cm (surface) & 30cm (active root zone) measuring moisture deficit.</div>
            </li>
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--se-primary); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">Hall-Effect Pulse Flow Meter:</strong> Calibrated 1-inch in-line meter logging exact volumetric application (litres/min).</div>
            </li>
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--se-primary); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">SHT31-D & Pyranometer:</strong> Solar irradiance (W/m²) and ambient RH for FAO-56 Penman-Monteith ET₀ calculation.</div>
            </li>
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--se-primary); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">Sentinel-2 Satellite Sync:</strong> 10m NDVI & NDWI canopy moisture indices validating edge ground truth.</div>
            </li>
          </ul>
        </div>

        <!-- Column 2: Edge Controller -->
        <div class="card" style="flex: 1; border: 2px solid #C4ECD0; background: #FAFDFB;">
          <div class="card-title">
            <span style="background: #D4F4DD; color: var(--yy-emerald); padding: 4px 10px; border-radius: var(--radius-sm); font-size: 14px;">LAYER 2</span>
            AgroStruxure Edge Controller
          </div>
          <div class="card-subtitle">FreeRTOS deterministic state engine in an IP67 enclosure.</div>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 14px; font-size: 14px; color: var(--text-secondary); line-height: 1.5;">
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--yy-emerald); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">ESP32-S3 Dual-Core SoC:</strong> Executes local water budgeting and fail-safe safety interlocks without cloud dependence.</div>
            </li>
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--yy-emerald); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">Modbus RTU Master:</strong> Isolated RS485 communication with Schneider Altivar ATV320 VFDs at 19,200 baud (8-E-1).</div>
            </li>
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--yy-emerald); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">CiA402 Drive State Machine:</strong> Direct control of Command Word (Reg 8501) and Speed Reference (Reg 8502) per doc NVE41308.</div>
            </li>
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--yy-emerald); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">3-Layer Entitlement Engine:</strong> Locks out pump when field capacity (45%) or daily quota is satisfied.</div>
            </li>
          </ul>
        </div>

        <!-- Column 3: Actuation & Loads -->
        <div class="card" style="flex: 1;">
          <div class="card-title">
            <span style="background: #E8F8ED; color: var(--yy-emerald); padding: 4px 10px; border-radius: var(--radius-sm); font-size: 14px;">LAYER 3</span>
            Dual-Load Actuation & Power
          </div>
          <div class="card-subtitle">Upstream DC bus transfer between pump and cooling.</div>
          <ul style="list-style: none; display: flex; flex-direction: column; gap: 14px; font-size: 14px; color: var(--text-secondary); line-height: 1.5;">
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--color-cold-room); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">Schneider TeSys D Switchgear:</strong> Dual mechanically & electrically interlocked contactors (2x LC1D09BD) switching on 350–600V DC.</div>
            </li>
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--color-water); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">Load A: Submersible Pump:</strong> Altivar ATV320 solar drive operates 3–5 HP pump with smooth MPPT tracking (32–50 Hz).</div>
            </li>
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--color-cold-room); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">Load B: 2 MT Pre-Cooler:</strong> DC compressor & organic Phase Change Material (PCM) thermal storage pulling harvest to 12°C.</div>
            </li>
            <li style="display: flex; gap: 10px;">
              <span style="color: var(--color-alarm); font-weight: 700;">•</span>
              <div><strong style="color: var(--text-primary);">5s Zero-Current Dead-Band:</strong> Eliminates inductive arcing and protects inverter IGBTs during transfer.</div>
            </li>
          </ul>
        </div>
      </div>

      <div class="slide-footer">
        <span>Hardware Architecture: Modbus RTU (CiA402 Profile) • Schneider Altivar ATV320 • Schneider TeSys D</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="nextSlide()">Next Slide <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></button>
        </div>
      </div>
    </div>


    <!-- ====================================================================
         SLIDE 04: PRECISION IRRIGATION & WATER ENTITLEMENT
         ==================================================================== -->
    <div class="slide" id="slide-4">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">Precision Irrigation</span>
          <span class="header-context">Closing the Loop on Crop Water Demand</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">04 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-title-block">
        <div class="slide-eyebrow">HYDROLOGICAL OPTIMIZATION</div>
        <h2 class="slide-title">Cutting Groundwater Withdrawal by 41.2% Without Yield Loss</h2>
        <p class="slide-subtitle">Combining FAO-56 dual Kc dynamic water budgeting with real-time FDR capacitive cutoff eliminates agricultural over-irrigation.</p>
      </div>

      <div class="slide-body">
        <!-- Left Editorial Image Split (42%) -->
        <div style="flex: 0.42;">
          <div class="media-card" style="height: 100%;">
            <img src="{img_drip}" alt="Commercial Drip Irrigation Rows">
            <div class="media-tag" style="flex-direction: column; align-items: flex-start; gap: 4px;">
              <span style="font-weight: 700; color: var(--color-water);">Sub-Surface Pulsed Drip Array</span>
              <span style="font-size: 11px; color: var(--text-secondary);">Delivers volumetric water entitlements directly to root zone; zero evaporation loss.</span>
            </div>
          </div>
        </div>

        <!-- Right Water Balance Breakdown (58%) -->
        <div style="flex: 0.58; display: flex; flex-direction: column; justify-content: space-between;">
          <!-- 3-Layer Entitlement Engine Card -->
          <div class="card" style="padding: 20px 24px;">
            <div class="card-title" style="font-size: 17px; margin-bottom: 8px;">
              <svg class="icon" style="color: var(--color-water);" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              The 3-Layer Water Entitlement Mechanism
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 10px;">
              <div style="background: var(--surface-subtle); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--color-water);">
                <div style="font-size: 11px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Layer 1: Agronomy</div>
                <div style="font-size: 13px; font-weight: 600; color: var(--text-primary); margin-top: 2px;">Dynamic FAO-56 ETc</div>
                <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">Computes daily crop transpiration from Open-Meteo & SHT31.</div>
              </div>
              <div style="background: var(--surface-subtle); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--se-primary);">
                <div style="font-size: 11px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Layer 2: Ground Truth</div>
                <div style="font-size: 13px; font-weight: 600; color: var(--text-primary); margin-top: 2px;">FDR Field Capacity Cutoff</div>
                <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">Automatic cutoff when 30cm root zone reaches 45% FC.</div>
              </div>
              <div style="background: var(--surface-subtle); padding: 12px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--yy-deep-forest);">
                <div style="font-size: 11px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Layer 3: Community</div>
                <div style="font-size: 13px; font-weight: 600; color: var(--text-primary); margin-top: 2px;">Aquifer Quota Cap</div>
                <div style="font-size: 11px; color: var(--text-secondary); margin-top: 4px;">Enforces Atal Bhujal FPO seasonal groundwater caps.</div>
              </div>
            </div>
          </div>

          <!-- Comparison Metrics Table -->
          <div class="card" style="padding: 20px 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
              <span style="font-family: var(--font-display); font-weight: 700; font-size: 16px;">Water & Energy Conservation Ledger (Per Hectare / Year)</span>
              <span style="font-family: var(--font-mono); font-size: 12px; color: var(--yy-emerald); font-weight: 600;">impact_model.py Verified</span>
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
              <thead>
                <tr style="border-bottom: 2px solid var(--border-subtle); text-align: left; color: var(--text-secondary);">
                  <th style="padding: 8px 6px;">Parameter</th>
                  <th style="padding: 8px 6px;">Baseline (Flood Irrigation)</th>
                  <th style="padding: 8px 6px;">AgroStruxure Precision</th>
                  <th style="padding: 8px 6px; color: var(--yy-emerald);">Net Savings</th>
                </tr>
              </thead>
              <tbody>
                <tr style="border-bottom: 1px solid var(--border-subtle);">
                  <td style="padding: 10px 6px; font-weight: 600;">Water Application</td>
                  <td style="padding: 10px 6px; font-family: var(--font-mono);">17,000 m³/ha (850 mm)</td>
                  <td style="padding: 10px 6px; font-family: var(--font-mono);">10,000 m³/ha (500 mm)</td>
                  <td style="padding: 10px 6px; font-family: var(--font-mono); font-weight: 700; color: var(--yy-emerald);">7,000 m³/ha (41.2% Saved)</td>
                </tr>
                <tr style="border-bottom: 1px solid var(--border-subtle);">
                  <td style="padding: 10px 6px; font-weight: 600;">Pumping Electricity</td>
                  <td style="padding: 10px 6px; font-family: var(--font-mono);">4,118 kWh/year</td>
                  <td style="padding: 10px 6px; font-family: var(--font-mono);">2,422 kWh/year</td>
                  <td style="padding: 10px 6px; font-family: var(--font-mono); font-weight: 700; color: var(--yy-emerald);">1,696 kWh/yr Liberated</td>
                </tr>
                <tr>
                  <td style="padding: 10px 6px; font-weight: 600;">Pumping Hours @ 40m</td>
                  <td style="padding: 10px 6px; font-family: var(--font-mono);">1,373 Hours/year</td>
                  <td style="padding: 10px 6px; font-family: var(--font-mono);">807 Hours/year</td>
                  <td style="padding: 10px 6px; font-family: var(--font-mono); font-weight: 700; color: var(--yy-emerald);">566 Hours Less Wear</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Bottom Attribution Note -->
          <div style="font-size: 12px; color: var(--text-secondary); background: #F1F5F9; padding: 10px 16px; border-radius: var(--radius-sm);">
            <strong>Honest Attribution:</strong> 29.4% saved by shifting flood to drip; <strong>11.8% additional saving</strong> uniquely locked in by AgroStruxure's automated soil cutoff to eliminate the solar rebound paradox.
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>Scientific Model: FAO Irrigation & Drainage Paper 56 • ICAR-IARI Horticultural Guidelines</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="nextSlide()">Next Slide <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></button>
        </div>
      </div>
    </div>


    <!-- ====================================================================
         SLIDE 05: ENERGY ARCHITECTURE & CONTACTOR DIVERT
         ==================================================================== -->
    <div class="slide" id="slide-5">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">Power Engineering</span>
          <span class="header-context">Upstream DC Bus Transfer & Surplus Solar Capture</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">05 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-title-block">
        <div class="slide-eyebrow">ELECTRICAL INNOVATION</div>
        <h2 class="slide-title">Dynamic Solar Routing via Upstream DC Bus Switching</h2>
        <p class="slide-subtitle">Capturing 77% of idle solar surplus by switching power safely upstream on the DC bus with dual interlocked Schneider TeSys D contactors.</p>
      </div>

      <div class="slide-body">
        <!-- Left Industrial Schematic Column (54%) -->
        <div class="card" style="flex: 1.15; justify-content: space-between;">
          <div>
            <div class="card-title">
              <svg class="icon" style="color: var(--yy-emerald);" viewBox="0 0 24 24"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
              Upstream DC Bus Architecture vs AC Switching
            </div>
            <p style="font-size: 13.5px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 14px;">
              Switching contactors on the AC output of a running VFD creates massive inductive voltage spikes, contact arcing, and instant drive trips. AgroStruxure switches <strong>upstream on the DC Bus (350–600V DC)</strong> under controlled zero-current conditions.
            </p>

            <!-- 5-Step Safe Changeover Flow -->
            <div style="display: flex; flex-direction: column; gap: 8px;">
              <div style="display: flex; align-items: center; gap: 12px; background: var(--surface-subtle); padding: 8px 14px; border-radius: var(--radius-sm);">
                <span style="font-family: var(--font-mono); font-weight: 700; color: var(--color-water); font-size: 12px;">STEP 1</span>
                <span style="font-size: 13px; color: var(--text-primary);">Root Zone Reaches 45% Field Capacity → Irrigation Cutoff Triggered</span>
              </div>
              <div style="display: flex; align-items: center; gap: 12px; background: var(--surface-subtle); padding: 8px 14px; border-radius: var(--radius-sm);">
                <span style="font-family: var(--font-mono); font-weight: 700; color: var(--se-primary); font-size: 12px;">STEP 2</span>
                <span style="font-size: 13px; color: var(--text-primary);">Altivar ATV320 Decelerates: Modbus Reg 8502 ramps frequency to 0 Hz in 8.0s</span>
              </div>
              <div style="display: flex; align-items: center; gap: 12px; background: var(--surface-subtle); padding: 8px 14px; border-radius: var(--radius-sm);">
                <span style="font-family: var(--font-mono); font-weight: 700; color: var(--yy-emerald); font-size: 12px;">STEP 3</span>
                <span style="font-size: 13px; color: var(--text-primary);">1-Inch Latching Hydraulic Solenoid Closes at Zero Flow (No Water Hammer)</span>
              </div>
              <div style="display: flex; align-items: center; gap: 12px; background: #FFF4E5; padding: 8px 14px; border-radius: var(--radius-sm); border: 1px solid #FFE0B2;">
                <span style="font-family: var(--font-mono); font-weight: 700; color: var(--color-transient); font-size: 12px;">STEP 4</span>
                <span style="font-size: 13px; color: var(--text-primary); font-weight: 600;">5.0-Second DC Dead-Band Dwell: Guarantees zero residual DC current</span>
              </div>
              <div style="display: flex; align-items: center; gap: 12px; background: #F3E8FF; padding: 8px 14px; border-radius: var(--radius-sm); border: 1px solid #E9D5FF;">
                <span style="font-family: var(--font-mono); font-weight: 700; color: var(--color-cold-room); font-size: 12px;">STEP 5</span>
                <span style="font-size: 13px; color: var(--text-primary); font-weight: 600;">TeSys D Contactor Transfers DC Bus to 3.8 kW Micro-Cold Room Compressor</span>
              </div>
            </div>
          </div>

          <div style="font-size: 12px; color: var(--text-secondary); border-top: 1px solid var(--border-subtle); padding-top: 10px;">
            Dual Mechanical & Electrical Interlocking prevents simultaneous contact closure under all single-fault conditions.
          </div>
        </div>

        <!-- Right Solar Distribution Column (46%) -->
        <div style="flex: 0.85; display: flex; flex-direction: column; gap: 18px;">
          <!-- Energy Partition Card -->
          <div class="card" style="flex: 1;">
            <div class="card-title">
              <svg class="icon" style="color: var(--yy-solar-gold);" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M18.36 5.64l1.42-1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42"/></svg>
              Annual Solar Energy Partition (4.8 kWp Standalone PV)
            </div>

            <div style="margin: 14px 0;">
              <!-- Progress Stack Bar -->
              <div style="height: 32px; width: 100%; border-radius: var(--radius-sm); overflow: hidden; display: flex; box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);">
                <div style="width: 36.9%; background: var(--color-water); display: flex; align-items: center; justify-content: center; color: white; font-family: var(--font-mono); font-size: 12px; font-weight: 700;">37% Pumping</div>
                <div style="width: 48.6%; background: var(--color-cold-room); display: flex; align-items: center; justify-content: center; color: white; font-family: var(--font-mono); font-size: 12px; font-weight: 700;">49% Cold Storage</div>
                <div style="width: 14.5%; background: #CBD5E1; display: flex; align-items: center; justify-content: center; color: var(--text-primary); font-family: var(--font-mono); font-size: 11px; font-weight: 600;">14% Residual</div>
              </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 10px; font-size: 13px;">
              <div style="display: flex; justify-content: space-between; padding-bottom: 6px; border-bottom: 1px solid var(--border-subtle);">
                <span style="color: var(--text-secondary);">Total Standalone Generation:</span>
                <span style="font-family: var(--font-mono); font-weight: 700;">6,559 kWh/year (100%)</span>
              </div>
              <div style="display: flex; justify-content: space-between; padding-bottom: 6px; border-bottom: 1px solid var(--border-subtle);">
                <span style="color: var(--color-water); font-weight: 600;">Pumping Consumption (Scheduled):</span>
                <span style="font-family: var(--font-mono); font-weight: 700;">2,422 kWh/year (36.9%)</span>
              </div>
              <div style="display: flex; justify-content: space-between; padding-bottom: 6px; border-bottom: 1px solid var(--border-subtle);">
                <span style="color: var(--text-secondary);">Idle Solar Surplus Generated:</span>
                <span style="font-family: var(--font-mono); font-weight: 700;">4,137 kWh/year (63.1%)</span>
              </div>
              <div style="display: flex; justify-content: space-between; padding-bottom: 6px; border-bottom: 1px solid var(--border-subtle);">
                <span style="color: var(--color-cold-room); font-weight: 700;">Surplus Put to Work (Cooling):</span>
                <span style="font-family: var(--font-mono); font-weight: 700; color: var(--color-cold-room);">3,187 kWh/year (77.0%)</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--text-secondary);">Residual Uncaptured Summer Midday:</span>
                <span style="font-family: var(--font-mono); font-weight: 600; color: var(--text-tertiary);">951 kWh/year (14.5%)</span>
              </div>
            </div>
          </div>

          <div style="background: #F8FAFC; border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px 18px; font-size: 12.5px; color: var(--text-secondary);">
            <strong style="color: var(--text-primary);">Zero False Claims:</strong> We transparently report 951 kWh/yr residual surplus. Once the 2 MT thermal PCM bank is saturated, cooling throttles down to prevent unnecessary compressor cycling.
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>Switchgear Specification: Schneider TeSys D (2x LC1D09BD) • Type-2 DC SPD • 500V DC Break Rating</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="nextSlide()">Next Slide <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></button>
        </div>
      </div>
    </div>


    <!-- ====================================================================
         SLIDE 06: FARM-GATE MICRO-COLD CHAIN & FOOD LOSS
         ==================================================================== -->
    <div class="slide" id="slide-6">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">Cold Chain Engineering</span>
          <span class="header-context">Decentralized Pre-Cooling & Shelf Life Extension</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">06 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-title-block">
        <div class="slide-eyebrow">POST-HARVEST VALUE PRESERVATION</div>
        <h2 class="slide-title">Halving Farm-Gate Spoilage from 8.37% to 4.00%</h2>
        <p class="slide-subtitle">Thermodynamically sized 2 MT farm-gate pre-cooling to 12°C halts respiration heat and extends tomato shelf life by 4–7 days.</p>
      </div>

      <div class="slide-body">
        <!-- Left Editorial Tomato Portrait (38%) -->
        <div style="flex: 0.38;">
          <div class="media-card" style="height: 100%;">
            <img src="{img_tomato}" alt="Freshly Harvested Tomatoes">
            <div class="media-tag" style="flex-direction: column; align-items: flex-start; gap: 4px;">
              <span style="font-weight: 700; color: var(--color-cold-room);">Critical Chilling Injury Threshold: 12.0°C</span>
              <span style="font-size: 11px; color: var(--text-secondary);">FAO & ICAR: Fresh tomatoes suffer cellular breakdown below 10°C. 12°C is the optimal setpoint.</span>
            </div>
          </div>
        </div>

        <!-- Right Sizing & Impact Ledger (62%) -->
        <div style="flex: 0.62; display: flex; flex-direction: column; justify-content: space-between;">
          <!-- Technical Sizing Specifications -->
          <div class="card" style="padding: 20px 24px;">
            <div class="card-title" style="font-size: 17px; margin-bottom: 8px;">
              <svg class="icon" style="color: var(--color-cold-room);" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>
              Thermodynamic Sizing: 2 MT Farm Pre-Cooler
            </div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 10px;">
              <div style="background: var(--surface-subtle); padding: 12px 14px; border-radius: var(--radius-sm);">
                <div style="font-size: 11px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Batch Sizing</div>
                <div style="font-size: 16px; font-weight: 700; color: var(--text-primary); margin-top: 2px;">2.0 Metric Tonnes</div>
                <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">Matches daily 4-farm cluster harvest volume.</div>
              </div>
              <div style="background: var(--surface-subtle); padding: 12px 14px; border-radius: var(--radius-sm);">
                <div style="font-size: 11px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">Thermal Pull-Down</div>
                <div style="font-size: 16px; font-weight: 700; color: var(--color-cold-room); margin-top: 2px;">32°C → 12°C (4 Hrs)</div>
                <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">3.43 kW average cooling load; COP = 3.0.</div>
              </div>
              <div style="background: var(--surface-subtle); padding: 12px 14px; border-radius: var(--radius-sm);">
                <div style="font-size: 11px; font-weight: 700; color: var(--text-secondary); text-transform: uppercase;">PCM Thermal Battery</div>
                <div style="font-size: 16px; font-weight: 700; color: var(--yy-emerald); margin-top: 2px;">14-Hour Holdover</div>
                <div style="font-size: 11px; color: var(--text-secondary); margin-top: 2px;">Organic salt hydrate buffer holds 12°C overnight.</div>
              </div>
            </div>
          </div>

          <!-- Impact Metrics Grid -->
          <div class="metric-pill-grid">
            <div class="metric-pill" style="border-top-color: var(--color-cold-room);">
              <div class="metric-val">1.31<span>Tonnes</span></div>
              <div class="metric-label">Tomatoes Saved/Ha/Yr</div>
              <div class="metric-desc">Farm-stage spoilage halved from 8.37% down to 4.00%</div>
            </div>
            <div class="metric-pill" style="border-top-color: var(--yy-emerald);">
              <div class="metric-val">₹15,732<span>/Yr</span></div>
              <div class="metric-label">Direct Revenue Saved</div>
              <div class="metric-desc">Preserved grade-A fruit sold at ₹12/kg mandi price</div>
            </div>
            <div class="metric-pill" style="border-top-color: var(--yy-solar-gold);">
              <div class="metric-val">+₹12,000<span>/Yr</span></div>
              <div class="metric-label">Distress-Sale Avoidance</div>
              <div class="metric-desc">4–7 day holdover gives farmers market bargaining leverage</div>
            </div>
          </div>

          <!-- Decarbonization Callout Strip -->
          <div style="background: #E8F8ED; border: 1px solid #B8E8C7; border-radius: var(--radius-md); padding: 12px 18px; font-size: 13px; color: var(--yy-deep-forest); display: flex; justify-content: space-between; align-items: center;">
            <span><strong>Decarbonization Benefit:</strong> Avoids 2.55 t CO₂e from diesel generator cold rooms + 0.39 t CO₂e embodied crop carbon.</span>
            <span style="font-family: var(--font-mono); font-weight: 700; font-size: 14px; color: var(--yy-emerald);">2.94 t CO₂e / ha / yr</span>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>Post-Harvest Literature: ICAR-CIPHET 2021 Bulletin 44 • NABCONS 2022 MoFPI Baseline</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="nextSlide()">Next Slide <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></button>
        </div>
      </div>
    </div>


    <!-- ====================================================================
         SLIDE 07: INTELLIGENCE LAYER & KRISHI MITRA (RAG AI)
         ==================================================================== -->
    <div class="slide" id="slide-7">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">Vernacular AI</span>
          <span class="header-context">Zero-Hallucination Cognitive Trust for Smallholders</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">07 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-title-block">
        <div class="slide-eyebrow">DETERMINISTIC AGENTIC ARCHITECTURE</div>
        <h2 class="slide-title">Krishi Mitra: Zero-Hallucination Vernacular Guidance</h2>
        <p class="slide-subtitle">LLMs have zero actuation authority over physical switchgear. Spoken advisories in Marathi and Hindi are 100% grounded in verified edge JSON telemetry.</p>
      </div>

      <div class="slide-body" style="gap: 32px;">
        <!-- Left Panel: Technical Ground Truth (48%) -->
        <div class="card" style="flex: 1; background: #FAFDFB;">
          <div class="card-title" style="color: var(--yy-deep-forest);">
            <svg class="icon" style="color: var(--yy-emerald);" viewBox="0 0 24 24"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
            Edge Telemetry Ground Truth (Modbus RTU)
          </div>
          <div class="card-subtitle">Local microcontroller outputs structured JSON over MQTT/SMS.</div>
          
          <pre style="background: #FFFFFF; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 16px; font-family: var(--font-mono); font-size: 13px; color: #1E293B; line-height: 1.5; overflow: hidden; margin-bottom: 14px;">
{{
  "timestamp": "2026-10-03T11:32:00+05:30",
  "soil_moisture_30cm_pct": 44.8,
  "field_capacity_cutoff_pct": 45.0,
  "vfd_frequency_hz": 0.0,
  "contactor_state": "POS_B_COLD_ROOM",
  "daily_water_applied_m3": 27.4,
  "daily_quota_limit_m3": 28.0,
  "solar_irradiance_w_m2": 820,
  "cold_room_temperature_c": 11.9,
  "pcm_storage_status": "CHARGING_ACTIVE"
}}</pre>

          <div style="font-size: 12.5px; color: var(--text-secondary); line-height: 1.5;">
            <strong style="color: var(--text-primary);">Deterministic Safeguard:</strong> The prompt engine uses strict Pydantic schema validation. If telemetry values are absent or corrupted, the copilot falls back to pre-compiled audio scripts.
          </div>
        </div>

        <!-- Right Panel: Smallholder Vernacular Experience (52%) -->
        <div class="card" style="flex: 1.1; justify-content: space-between;">
          <div>
            <div class="card-title">
              <svg class="icon" style="color: var(--se-primary);" viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              Farmer Experience: WhatsApp Spoken Advisory
            </div>
            <div class="card-subtitle">Zero-literacy voice note delivered automatically via WhatsApp Bot.</div>

            <!-- Vernacular Voice Card (Marathi) -->
            <div style="background: #E8F8ED; border: 1px solid #B8E8C7; border-radius: var(--radius-md); padding: 18px 20px; margin-bottom: 14px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="font-family: var(--font-devanagari); font-weight: 700; font-size: 14px; color: var(--yy-emerald);">मराठी ऑडिओ संदेश (Marathi Voice Note)</span>
                <span style="font-family: var(--font-mono); font-size: 12px; background: white; padding: 2px 8px; border-radius: 4px;">0:14 / 2G Safe</span>
              </div>
              <p style="font-family: var(--font-devanagari); font-size: 16px; line-height: 1.6; color: var(--yy-deep-forest); font-weight: 500;">
                "रामभाऊ, तुमच्या टोमॅटोच्या मुळांना पुरेसे पाणी मिळाले आहे (४४.८%). पंप सुरक्षितपणे बंद झाला असून सौर वीज शीतगृहाकडे वळवली आहे. शीतगृहाचे तापमान १२°C असून टोमॅटो थंड होत आहेत."
              </p>
              <div style="font-size: 12px; color: var(--text-secondary); margin-top: 6px; font-style: italic;">
                "Rambhau, your tomato roots have reached optimal moisture (44.8%). Pumping stopped safely and solar power is now running the cold room at 12°C."
              </div>
            </div>

            <!-- Key Features List -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 13px;">
              <div style="background: var(--surface-subtle); padding: 10px 14px; border-radius: var(--radius-sm);">
                <strong>Marathi & Hindi TTS:</strong> High-intelligibility rural dialect audio synthesis.
              </div>
              <div style="background: var(--surface-subtle); padding: 10px 14px; border-radius: var(--radius-sm);">
                <strong>Physical Override:</strong> Manual switch bypasses automation at any instant.
              </div>
            </div>
          </div>

          <div style="font-size: 12px; color: var(--text-secondary); border-top: 1px solid var(--border-subtle); padding-top: 10px;">
            Offline Mode: Operates via edge circular flash memory and SMS gateway if 4G network drops.
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>Software Architecture: FreeRTOS Edge Firmware • Fastify Gateway • Deterministic Agentic RAG</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="nextSlide()">Next Slide <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></button>
        </div>
      </div>
    </div>


    <!-- ====================================================================
         SLIDE 08: BOM ECONOMICS, UNIT COSTS & FARMER ROI
         ==================================================================== -->
    <div class="slide" id="slide-8">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">Financial Engineering</span>
          <span class="header-context">Industrial Unit Economics & Cluster Payback</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">08 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-title-block">
        <div class="slide-eyebrow">COMMERCIAL FEASIBILITY</div>
        <h2 class="slide-title">Industrial Feasibility with a 2.0-Year Cluster Payback</h2>
        <p class="slide-subtitle">A ₹7,540 edge controller BoM paired with a 4-farm shared pre-cooler array avoids dedicated solar capex, yielding rapid capital recovery.</p>
      </div>

      <div class="slide-body" style="gap: 28px;">
        <!-- Left Column: Itemized Controller BOM (48%) -->
        <div class="card" style="flex: 1;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div class="card-title" style="margin-bottom: 0;">
              <svg class="icon" style="color: var(--yy-emerald);" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              Edge Controller BOM (1,000 Units)
            </div>
            <span style="font-family: var(--font-mono); font-weight: 700; color: var(--yy-emerald); font-size: 16px;">Total: ₹7,540</span>
          </div>

          <table style="width: 100%; border-collapse: collapse; font-size: 12.5px; line-height: 1.4;">
            <thead>
              <tr style="border-bottom: 2px solid var(--border-subtle); color: var(--text-secondary); text-align: left;">
                <th style="padding: 6px 4px;">Component Description</th>
                <th style="padding: 6px 4px; text-align: right;">Unit Cost</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 6px 4px;">ESP32-S3-WROOM-1 (16MB Flash, 8MB PSRAM)</td>
                <td style="padding: 6px 4px; text-align: right; font-family: var(--font-mono);">₹420</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 6px 4px;">MAX485 Isolated RS485 Transceiver + TVS Diodes</td>
                <td style="padding: 6px 4px; text-align: right; font-family: var(--font-mono);">₹180</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 6px 4px;">Dual-Depth Capacitive FDR Soil Probes (10cm & 30cm)</td>
                <td style="padding: 6px 4px; text-align: right; font-family: var(--font-mono);">₹760</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 6px 4px;">SHT31-D Temp/RH IP65 Probe + Silicon Pyranometer</td>
                <td style="padding: 6px 4px; text-align: right; font-family: var(--font-mono);">₹600</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 6px 4px;">1-inch Hall Pulse Flow Meter + 12V Latching Solenoid</td>
                <td style="padding: 6px 4px; text-align: right; font-family: var(--font-mono);">₹1,300</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 6px 4px; font-weight: 600; color: var(--yy-emerald);">Schneider TeSys D Contactors x2 (Mech/Elec Interlock)</td>
                <td style="padding: 6px 4px; text-align: right; font-family: var(--font-mono); font-weight: 700;">₹2,300</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 6px 4px;">24V DIN-Rail SMPS + Isolated Relay Driver Board</td>
                <td style="padding: 6px 4px; text-align: right; font-family: var(--font-mono);">₹380</td>
              </tr>
              <tr style="border-bottom: 1px solid var(--border-subtle);">
                <td style="padding: 6px 4px;">SIM7600 4G LTE Cellular Module + External Antenna</td>
                <td style="padding: 6px 4px; text-align: right; font-family: var(--font-mono);">₹620</td>
              </tr>
              <tr>
                <td style="padding: 6px 4px;">IP67 Polycarbonate Enclosure, DIN Rail, DC SPD, Wiring</td>
                <td style="padding: 6px 4px; text-align: right; font-family: var(--font-mono);">₹980</td>
              </tr>
            </tbody>
          </table>

          <div style="margin-top: 10px; font-size: 12px; color: var(--text-secondary); background: #F8FAFC; padding: 8px 12px; border-radius: var(--radius-sm);">
            <strong>Standalone Controller Payback:</strong> Saves ₹5,000/yr in pump maintenance and crop yield protection → <strong>Pays back in 1.5 crop seasons.</strong>
          </div>
        </div>

        <!-- Right Column: Tier A Cluster Pre-Cooler Model (52%) -->
        <div class="card" style="flex: 1.1; justify-content: space-between;">
          <div>
            <div class="card-title">
              <svg class="icon" style="color: var(--color-cold-room);" viewBox="0 0 24 24"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              Tier A: 4-Farm Cluster Pre-Cooler Model (2 MT)
            </div>
            <div class="card-subtitle">4 adjacent smallholders share a single 2 MT pre-cooler unit.</div>

            <!-- Capex Waterfall Breakdown -->
            <div style="background: var(--surface-subtle); padding: 14px 18px; border-radius: var(--radius-md); margin-bottom: 14px; font-size: 13px;">
              <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span>Gross 2 MT Pre-Cooler Capex (Compressor + PCM):</span>
                <span style="font-family: var(--font-mono); font-weight: 600;">₹400,000</span>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 6px; color: var(--yy-emerald); font-weight: 600;">
                <span>Less Shared PV Saving (2.6 kWp array avoided):</span>
                <span style="font-family: var(--font-mono);">-₹91,000</span>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 6px; padding-top: 6px; border-top: 1px dashed var(--border-subtle);">
                <span>Net System Capital Cost:</span>
                <span style="font-family: var(--font-mono); font-weight: 600;">₹309,000</span>
              </div>
              <div style="display: flex; justify-content: space-between; color: var(--color-water); font-weight: 600;">
                <span>After 35% MIDH / AIF Scheme Capital Subsidy:</span>
                <span style="font-family: var(--font-mono);">₹200,850</span>
              </div>
              <div style="display: flex; justify-content: space-between; margin-top: 8px; padding-top: 8px; border-top: 2px solid var(--border-subtle); font-size: 15px; font-weight: 800; color: var(--text-primary);">
                <span>Net Capex Per Farm (4-Farm Cluster):</span>
                <span style="font-family: var(--font-mono); color: var(--yy-emerald);">₹50,212</span>
              </div>
            </div>

            <!-- Net Annual Gains Per Farm -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; text-align: center;">
              <div style="background: #FFFFFF; border: 1px solid var(--border-subtle); padding: 10px; border-radius: var(--radius-sm);">
                <div style="font-size: 11px; color: var(--text-secondary);">Spoilage Avoided</div>
                <div style="font-family: var(--font-mono); font-size: 15px; font-weight: 700; color: var(--yy-emerald); margin-top: 2px;">+₹15,732</div>
              </div>
              <div style="background: #FFFFFF; border: 1px solid var(--border-subtle); padding: 10px; border-radius: var(--radius-sm);">
                <div style="font-size: 11px; color: var(--text-secondary);">Distress Sale Timing</div>
                <div style="font-family: var(--font-mono); font-size: 15px; font-weight: 700; color: var(--yy-solar-gold); margin-top: 2px;">+₹12,000</div>
              </div>
              <div style="background: #FFFFFF; border: 1px solid var(--border-subtle); padding: 10px; border-radius: var(--radius-sm);">
                <div style="font-size: 11px; color: var(--text-secondary);">Less Opex / Maint.</div>
                <div style="font-family: var(--font-mono); font-size: 15px; font-weight: 700; color: var(--color-alarm); margin-top: 2px;">-₹2,400</div>
              </div>
            </div>
          </div>

          <!-- Bottom Payback Callout -->
          <div style="background: #E8F8ED; border: 1px solid #B8E8C7; border-radius: var(--radius-md); padding: 12px 18px; display: flex; justify-content: space-between; align-items: center;">
            <div>
              <div style="font-size: 12px; font-weight: 600; color: var(--yy-emerald);">NET ANNUAL FARMER BENEFIT: +₹25,332 / YEAR</div>
              <div style="font-size: 11px; color: var(--text-secondary);">₹50,212 net capex recovered in exactly two crop harvests.</div>
            </div>
            <div style="font-family: var(--font-display); font-size: 26px; font-weight: 800; color: var(--yy-deep-forest);">
              2.0 Yrs Payback
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span>Policy Alignment: MIDH Mission for Integrated Development of Horticulture • Agriculture Infrastructure Fund (AIF)</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="nextSlide()">Next Slide <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></button>
        </div>
      </div>
    </div>


    <!-- ====================================================================
         SLIDE 09: PILOT DEPLOYMENT & SCALABILITY PLAN
         ==================================================================== -->
    <div class="slide" id="slide-9">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">Deployment Roadmap</span>
          <span class="header-context">From Simulation to 250-Farm Commercial Pilot</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">09 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-title-block">
        <div class="slide-eyebrow">COMMERCIALIZATION ROADMAP</div>
        <h2 class="slide-title">From Software Digital Twin to 250-Farm Field Pilot</h2>
        <p class="slide-subtitle">Structured execution plan partnering with India's leading horticulture FPOs and Schneider Electric's rural partner network.</p>
      </div>

      <div class="slide-body" style="gap: 20px;">
        <!-- Phase 1 Card -->
        <div class="card" style="flex: 1; border-top: 4px solid var(--yy-emerald); justify-content: space-between;">
          <div>
            <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 700; color: var(--yy-emerald); margin-bottom: 4px;">PHASE 1 • CURRENT</div>
            <div style="font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">Software Twin & Math Validation</div>
            <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
              Validated FAO-56 hydrological models, thermodynamic pull-down curves, and complete CiA402 register state machines in Python/FastAPI (`AgroSim`).
            </p>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 14px;">
              <li><strong style="color: var(--text-primary);">• Hydrological Truth:</strong> `impact_model.py` verified across 365-day solar irradiance & ETc cycles.</li>
              <li><strong style="color: var(--text-primary);">• Firmware Stubs:</strong> Modbus RTU register mapping to Schneider Altivar ATV320 VFD registers.</li>
              <li><strong style="color: var(--text-primary);">• Vernacular NLP:</strong> Marathi & Hindi prompt engineering validated with Pydantic JSON schema.</li>
            </ul>
          </div>
          <div style="background: var(--surface-subtle); padding: 10px 12px; border-radius: var(--radius-sm); font-size: 12px; color: var(--text-primary); border-left: 3px solid var(--yy-emerald);">
            <strong>Exit Gate:</strong> Zero mathematical discrepancies in mass/energy balances (`impact_model.py`).
          </div>
        </div>

        <!-- Phase 2 Card -->
        <div class="card" style="flex: 1; border-top: 4px solid var(--color-water); justify-content: space-between;">
          <div>
            <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 700; color: var(--color-water); margin-bottom: 4px;">PHASE 2 • Q1-Q2 2027</div>
            <div style="font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">Hardware-in-the-Loop Test Bench</div>
            <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
              Physical integration bench pairing ESP32-S3 with Schneider Altivar ATV320 solar VFD, TeSys contactors, and motor dynamometer under solar simulator.
            </p>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 14px;">
              <li><strong style="color: var(--text-primary);">• Switchgear Safety:</strong> 5.0s DC dead-band dwell verification preventing inverter DC-bus trip.</li>
              <li><strong style="color: var(--text-primary);">• Thermal Endurance:</strong> 2 MT PCM salt-hydrate charging/discharging thermal cycle tests.</li>
              <li><strong style="color: var(--text-primary);">• Surge Protection:</strong> Type-2 DC SPD discharge tests up to 1,000V DC lightning transient.</li>
            </ul>
          </div>
          <div style="background: var(--surface-subtle); padding: 10px 12px; border-radius: var(--radius-sm); font-size: 12px; color: var(--text-primary); border-left: 3px solid var(--color-water);">
            <strong>Exit Gate:</strong> 500 faultless DC transfer cycles under full electrical load without drive trip.
          </div>
        </div>

        <!-- Phase 3 Card -->
        <div class="card" style="flex: 1; border-top: 4px solid var(--yy-solar-gold); justify-content: space-between;">
          <div>
            <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 700; color: #B98300; margin-bottom: 4px;">PHASE 3 • Q3-Q4 2027</div>
            <div style="font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">20-Farm FPO Pilot (Nashik)</div>
            <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
              Field pilot across 5 clusters (4 farms each) in partnership with <strong>Sahyadri Farmers Producer Co.</strong> (India's largest tomato FPO) in Dindori, Nashik.
            </p>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 14px;">
              <li><strong style="color: var(--text-primary);">• Real Field Operation:</strong> Real tomato crop cycles monitoring soil moisture & yield gain.</li>
              <li><strong style="color: var(--text-primary);">• Cold-Chain Logistics:</strong> Farm-gate pre-cooling to 12°C connected to reefer transport.</li>
              <li><strong style="color: var(--text-primary);">• Farmer Adoption:</strong> Marathi voice notes delivered via WhatsApp with 98%+ comprehension.</li>
            </ul>
          </div>
          <div style="background: var(--surface-subtle); padding: 10px 12px; border-radius: var(--radius-sm); font-size: 12px; color: var(--text-primary); border-left: 3px solid var(--yy-solar-gold);">
            <strong>Exit Gate:</strong> Measured >35% water conservation and 95%+ pre-cooler uptime over 2 seasons.
          </div>
        </div>

        <!-- Phase 4 Card -->
        <div class="card" style="flex: 1; border-top: 4px solid var(--color-cold-room); justify-content: space-between;">
          <div>
            <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 700; color: var(--color-cold-room); margin-bottom: 4px;">PHASE 4 • 2028</div>
            <div style="font-family: var(--font-display); font-size: 18px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">250-Farm Commercial Expansion</div>
            <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
              OEM pre-assembly retrofit skids for solar pump EPCs under PM-KUSUM Component B tenders. Training rural clean-tech youth as "Urja Mitras".
            </p>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 12.5px; color: var(--text-secondary); margin-bottom: 14px;">
              <li><strong style="color: var(--text-primary);">• OEM Retrofit Skids:</strong> Factory-assembled DIN-rail kit reducing field install time to 2 hours.</li>
              <li><strong style="color: var(--text-primary);">• Rural Franchises:</strong> Local ITI diploma youth trained for sensor calibration & servicing.</li>
              <li><strong style="color: var(--text-primary);">• Carbon Credits:</strong> Aggregating 2.94 t CO₂e/ha/yr for voluntary carbon offset monetization.</li>
            </ul>
          </div>
          <div style="background: var(--surface-subtle); padding: 10px 12px; border-radius: var(--radius-sm); font-size: 12px; color: var(--text-primary); border-left: 3px solid var(--color-cold-room);">
            <strong>Exit Gate:</strong> Commercial break-even with 5 FPO enterprise contracts in MH & RJ.
          </div>
        </div>
      </div>

      <!-- Bottom Partnership Strip -->
      <div style="margin-top: 18px; background: var(--surface-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px 22px; display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 13px; color: var(--text-secondary);"><strong style="color: var(--text-primary);">Government & Institutional Enablers:</strong> PM-KUSUM Component B (Pumps) • Atal Bhujal Yojana (Aquifer Quotas) • MIDH/AIF (35% Subsidies)</span>
        <span style="font-size: 13px; font-weight: 600; color: var(--yy-emerald);">Target Market: 10.9 Lakh Standalone Solar Pumps in India</span>
      </div>

      <div class="slide-footer">
        <span>Implementation Strategy: Cluster Asset Sharing • Rural Youth Clean-Tech Franchises • FPO Aggregation Hubs</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="nextSlide()">Next Slide <svg class="icon" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></button>
        </div>
      </div>
    </div>


    <!-- ====================================================================
         SLIDE 10: CONCLUSION, TEAM & THE VISION
         ==================================================================== -->
    <div class="slide" id="slide-10">
      <div class="slide-header">
        <div class="header-left">
          <span class="project-badge">Engineering Team</span>
          <span class="header-context">Yuva Yodha Energy Tech Hackathon 2026</span>
        </div>
        <div class="header-right">
          <span class="slide-counter">10 / 10</span>
          <img src="{logo_schneider}" alt="Schneider Electric" class="schneider-logo">
        </div>
      </div>

      <div class="slide-title-block">
        <div class="slide-eyebrow">THE AGROSTRUXURE™ VISION</div>
        <h2 class="slide-title">Engineering Sustainable Abundance for Indian Agriculture</h2>
        <p class="slide-subtitle">Transforming unconstrained solar pumps into connected, climate-resilient community energy and cold-chain assets.</p>
      </div>

      <div class="slide-body" style="gap: 20px; flex-direction: column;">
        <!-- Top Strategic Summary Card -->
        <div style="background: #E8F8ED; border: 1px solid #B8E8C7; border-radius: var(--radius-md); padding: 18px 24px; display: flex; justify-content: space-between; align-items: center;">
          <div style="max-width: 1200px;">
            <div style="font-family: var(--font-display); font-size: 17px; font-weight: 700; color: var(--yy-deep-forest); margin-bottom: 4px;">
              Direct Strategic Fit for Schneider Electric & SE Ventures
            </div>
            <div style="font-size: 14px; color: var(--text-secondary); line-height: 1.5;">
              AgroStruxure creates a high-margin digital IoT layer for Schneider Altivar Solar drives and TeSys switchgear, turning agricultural clean-tech from simple pump installations into scalable rural microgrid networks across the Global South.
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-family: var(--font-mono); font-size: 24px; font-weight: 800; color: var(--yy-emerald);">2.94 t CO₂e</div>
            <div style="font-size: 12px; color: var(--text-secondary);">Decarbonization / Ha / Year</div>
          </div>
        </div>

        <!-- 4-Member Multi-Disciplinary Engineering Team Grid -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; flex: 1;">
          <!-- Member 1: Sanskar Tiwari -->
          <div class="card" style="padding: 22px; border-top: 4px solid var(--yy-emerald); justify-content: space-between;">
            <div>
              <div style="font-family: var(--font-display); font-size: 19px; font-weight: 700; color: var(--text-primary);">Sanskar Tiwari</div>
              <div style="font-size: 12px; font-weight: 700; color: var(--yy-emerald); text-transform: uppercase; margin-top: 2px;">Embedded Firmware & Lead</div>
              <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-top: 10px;">
                ESP32-S3 FreeRTOS deterministic state machine, Modbus RTU master communication over isolated RS485, and IP67 industrial enclosure engineering.
              </p>
              <ul style="list-style: none; display: flex; flex-direction: column; gap: 6px; font-size: 12px; color: var(--text-secondary); margin-top: 10px;">
                <li>• FreeRTOS dual-core task priorities & watchdog</li>
                <li>• Isolated RS485 UART with auto-direction flow</li>
                <li>• CiA402 drive state machine register handlers</li>
              </ul>
            </div>
            <div style="background: var(--surface-subtle); padding: 8px 10px; border-radius: var(--radius-sm); font-size: 11px; color: var(--text-primary); margin-top: 12px;">
              <strong>Codebase:</strong> `main.cpp`, `rs485_master.c`, FreeRTOS tasks
            </div>
          </div>

          <!-- Member 2: Shambhavi Patil -->
          <div class="card" style="padding: 22px; border-top: 4px solid var(--color-water); justify-content: space-between;">
            <div>
              <div style="font-family: var(--font-display); font-size: 19px; font-weight: 700; color: var(--text-primary);">Shambhavi Patil</div>
              <div style="font-size: 12px; font-weight: 700; color: var(--color-water); text-transform: uppercase; margin-top: 2px;">Geospatial Intelligence Lead</div>
              <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-top: 10px;">
                Google Earth Engine cadastral analysis, Sentinel-2 10m NDVI/NDWI moisture extraction, and FAO-56 dual Kc dynamic water balance calibration.
              </p>
              <ul style="list-style: none; display: flex; flex-direction: column; gap: 6px; font-size: 12px; color: var(--text-secondary); margin-top: 10px;">
                <li>• Sentinel-2 MSI 10m resolution spectral analysis</li>
                <li>• Dynamic FAO-56 basal crop coefficient Kc curves</li>
                <li>• Aquifer recharge & soil moisture deficit modeling</li>
              </ul>
            </div>
            <div style="background: var(--surface-subtle); padding: 8px 10px; border-radius: var(--radius-sm); font-size: 11px; color: var(--text-primary); margin-top: 12px;">
              <strong>Pipelines:</strong> `gee_water_audit.py`, `sentinel_ndvi.py`
            </div>
          </div>

          <!-- Member 3: Kanishka Salgude -->
          <div class="card" style="padding: 22px; border-top: 4px solid var(--yy-solar-gold); justify-content: space-between;">
            <div>
              <div style="font-family: var(--font-display); font-size: 19px; font-weight: 700; color: var(--text-primary);">Kanishka Salgude</div>
              <div style="font-size: 12px; font-weight: 700; color: #B98300; text-transform: uppercase; margin-top: 2px;">Electrical Systems & VFD Lead</div>
              <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-top: 10px;">
                Schneider TeSys D switchgear interlocking, 350–600V DC bus power routing, Altivar ATV320 VFD configuration, and PCM thermal pull-down sizing.
              </p>
              <ul style="list-style: none; display: flex; flex-direction: column; gap: 6px; font-size: 12px; color: var(--text-secondary); margin-top: 10px;">
                <li>• TeSys D dual mechanical/electrical interlocking</li>
                <li>• 5.0s DC dead-band dwell zero-current transfer</li>
                <li>• 2 MT thermal pull-down & PCM salt-hydrate sizing</li>
              </ul>
            </div>
            <div style="background: var(--surface-subtle); padding: 8px 10px; border-radius: var(--radius-sm); font-size: 11px; color: var(--text-primary); margin-top: 12px;">
              <strong>Systems:</strong> `power_switch_schematic.dwg`, `vfd_cia402.py`
            </div>
          </div>

          <!-- Member 4: Chaitanya Ranade -->
          <div class="card" style="padding: 22px; border-top: 4px solid var(--color-cold-room); justify-content: space-between;">
            <div>
              <div style="font-family: var(--font-display); font-size: 19px; font-weight: 700; color: var(--text-primary);">Chaitanya Ranade</div>
              <div style="font-size: 12px; font-weight: 700; color: var(--color-cold-room); text-transform: uppercase; margin-top: 2px;">Product Strategy & Agronomy Lead</div>
              <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-top: 10px;">
                Smallholder WhatsApp vernacular copilot UX, 4-farm cluster economic modeling, AIF/MIDH policy subsidies, and Sahyadri FPO pilot partnership.
              </p>
              <ul style="list-style: none; display: flex; flex-direction: column; gap: 6px; font-size: 12px; color: var(--text-secondary); margin-top: 10px;">
                <li>• Sahyadri FPO pilot co-design & cluster economics</li>
                <li>• MIDH/AIF capital subsidy navigation (35%)</li>
                <li>• Vernacular Marathi voice bot & farmer trust loop</li>
              </ul>
            </div>
            <div style="background: var(--surface-subtle); padding: 8px 10px; border-radius: var(--radius-sm); font-size: 11px; color: var(--text-primary); margin-top: 12px;">
              <strong>Deliverables:</strong> `krishi_mitra_bot.py`, `impact_model.py`
            </div>
          </div>
        </div>
      </div>

      <div class="slide-footer">
        <span style="color: var(--yy-emerald); font-weight: 600;">Yuva Yodha Energy Tech Hackathon 2026 • Schneider Electric India & YouNoodle</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="goToSlide(1)">Restart Deck <svg class="icon" viewBox="0 0 24 24"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg></button>
        </div>
      </div>
    </div>

      <div class="slide-footer">
        <span style="color: var(--yy-emerald); font-weight: 600;">Yuva Yodha Energy Tech Hackathon 2026 • Schneider Electric India & YouNoodle</span>
        <div class="nav-controls">
          <button class="nav-btn" onclick="prevSlide()">Previous</button>
          <button class="nav-btn" onclick="goToSlide(1)">Restart Deck <svg class="icon" viewBox="0 0 24 24"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg></button>
        </div>
      </div>
    </div>

  </div>

  <!-- Interactive Slide Navigation Script & 16:9 Scale Stage -->
  <script>
    let currentSlide = 1;
    const totalSlides = 10;

    function scaleStage() {{
      const stage = document.getElementById('presentation-stage');
      const windowWidth = window.innerWidth;
      const windowHeight = window.innerHeight;
      
      const scaleX = windowWidth / 1920;
      const scaleY = windowHeight / 1080;
      const scale = Math.min(scaleX, scaleY);
      
      stage.style.transform = `translate(-50%, -50%) scale(${{scale}})`;
    }}

    function showSlide(n) {{
      document.querySelectorAll('.slide').forEach(slide => {{
        slide.classList.remove('active');
      }});
      
      const target = document.getElementById(`slide-${{n}}`);
      if (target) {{
        target.classList.add('active');
        currentSlide = n;
      }}
    }}

    function nextSlide() {{
      if (currentSlide < totalSlides) {{
        showSlide(currentSlide + 1);
      }}
    }}

    function prevSlide() {{
      if (currentSlide > 1) {{
        showSlide(currentSlide - 1);
      }}
    }}

    function goToSlide(n) {{
      if (n >= 1 && n <= totalSlides) {{
        showSlide(n);
      }}
    }}

    // Keyboard Navigation
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        prevSlide();
      }} else if (e.key >= '1' && e.key <= '9') {{
        goToSlide(parseInt(e.key));
      }} else if (e.key === '0') {{
        goToSlide(10);
      }}
    }});

    window.addEventListener('resize', scaleStage);
    window.addEventListener('DOMContentLoaded', () => {{
      scaleStage();
      const urlParams = new URLSearchParams(window.location.search);
      const slideParam = urlParams.get('slide');
      if (slideParam) {{
        showSlide(parseInt(slideParam));
      }} else if (window.location.hash) {{
        const hashNum = parseInt(window.location.hash.replace('#', ''));
        if (!isNaN(hashNum)) showSlide(hashNum);
      }} else {{
        showSlide(1);
      }}
    }});
  </script>
</body>
</html>
"""

    html_file = os.path.join(base_dir, "presentation.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"[OK] Generated pristine presentation.html ({len(html_template):,} chars)")

    # 2. Render 10 PNG screenshots using headless Chrome
    print("\nRendering 10 slides with headless Chrome...")
    output_dir = os.path.join(base_dir, "rendered_slides")
    os.makedirs(output_dir, exist_ok=True)
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    png_files = []

    for i in range(1, 11):
        slide_css = f"""
    #slide-{i} {{ display: flex !important; opacity: 1 !important; z-index: 10; }}
    .slide {{ display: none !important; }}
    #slide-{i} {{ display: flex !important; }}
"""
        single_html = html_template.replace("</style>", f"{slide_css}\n  </style>")
        single_file = os.path.join(output_dir, f"slide_{i:02d}.html")
        with open(single_file, "w", encoding="utf-8") as sf:
            sf.write(single_html)

        png_file = os.path.join(output_dir, f"slide_{i:02d}.png")
        file_url = "file:///" + single_file.replace("\\", "/")

        cmd = [
            chrome_path,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--window-size=1920,1080",
            f"--screenshot={png_file}",
            file_url
        ]

        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        if os.path.exists(png_file):
            png_files.append(png_file)
            print(f"  [OK] Rendered slide_{i:02d}.png ({os.path.getsize(png_file):,} bytes)")

    # 3. Compile high-resolution PDF
    print(f"\nCompiling PDF from {len(png_files)} slides...")
    pdf_path = os.path.join(base_dir, "AgroStruxure_YuvaYodha_2026_Final.pdf")
    images = [Image.open(p).convert("RGB") for p in png_files]
    images[0].save(pdf_path, save_all=True, append_images=images[1:], resolution=150.0, quality=95)
    print(f"  [OK] Saved PDF: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")

    # 4. Generate native PowerPoint presentation (PPTX)
    print("\nGenerating 16:9 PowerPoint presentation (AgroStruxure_YuvaYodha_2026_Final.pptx)...")
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for idx, png_file in enumerate(png_files, start=1):
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(png_file, 0, 0, width=prs.slide_width, height=prs.slide_height)
        print(f"  [OK] Slide {idx:02d} embedded into PPTX")

    pptx_path = os.path.join(base_dir, "AgroStruxure_YuvaYodha_2026_Final.pptx")
    prs.save(pptx_path)
    print(f"  [OK] Saved PowerPoint: {pptx_path} ({os.path.getsize(pptx_path):,} bytes)")

    print("\nMaster Deck Build & Export Complete!")

if __name__ == "__main__":
    build()
