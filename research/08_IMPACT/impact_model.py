"""
AgroStruxure v2 Impact & Economic Model
Reference Unit: 1 ha, Nashik district (19.99° N), Tomato, PM-KUSUM Component B standalone solar pump.
Run: python impact_model.py
"""

SEP = "=" * 74

# ============================================================== 1. ASSUMPTIONS
PUMP_HP           = 5.0      # MNRE Component B cap 7.5 HP; 5 HP is modal
PUMP_KW           = PUMP_HP * 0.746 # 3.73 kW
PV_KWP            = 4.8      # PV ~1.3x pump kW per Component B norms
PEAK_SUN_HOURS    = 4.8      # Nashik annual daily mean (NIWE range 4.5-5.2)
PERFORMANCE_RATIO = 0.78     # soiling, temperature, wiring, conversion

TDH_M             = 40.0     # total dynamic head, Deccan basalt (30-60 m)
WIRE_TO_WATER_EFF = 0.45     # submersible + VFD combined, field-realistic

CYCLES_PER_YEAR   = 2        # tomato, 120-day cycle
FLOOD_MM_SEASON   = 850.0    # unmetered flood baseline, tomato, Maharashtra
ETC_MM_SEASON     = 450.0    # FAO-56 ETc; Kc 0.60 -> 1.15 -> 0.80
DRIP_EFFICIENCY   = 0.90     # pulsed micro-drip application efficiency

YIELD_T_HA_YEAR   = 30.0     # marketable tomato, 1 ha, both cycles (15 t/cycle)
LOSS_FARM_BASE    = 0.0837   # NABCONS 2022, tomato farm-stage loss (8.37%)
LOSS_FARM_AFTER   = 0.0400   # residual after pre-cooling (4.00%, NOT zero)
TOMATO_PRICE_T    = 12000.0  # Rs/t farm-gate, conservative multi-year mean (Rs 12/kg)

# Thermal
CP_PRODUCE        = 3.7      # kJ/kg.K, tomato
FIELD_T           = 32.0     # field heat at harvest (°C)
TARGET_T          = 12.0     # tomato-safe setpoint; 4°C causes chilling injury
COP               = 3.0      # small vapour-compression at this lift
WINDOW_H          = 4.0      # 11:30-15:30 diversion window
PRECOOL_MT        = 2.0      # farm-level pre-cooler batch size (Tier A)
PCM_LATENT_KJ_KG  = 200.0    # encapsulated salt hydrate PCM, design target 190-210 kJ/kg, melt point 12-15 C (confirm vendor datasheet)
COLD_DAYS_YEAR    = 180      # harvest + storage operating days (room CAPACITY window, not demand)
CLUSTER_FARMS     = 4        # 1 ha farms sharing one pre-cooler, powered by the host farm's PV

def run_model():
    print(SEP); print("1. WATER  (per hectare)"); print(SEP)
    flood_m3   = FLOOD_MM_SEASON * 10          # 1 mm over 1 ha = 10 m3
    sched_mm   = ETC_MM_SEASON / DRIP_EFFICIENCY
    sched_m3   = sched_mm * 10
    saved_s    = flood_m3 - sched_m3
    saved_pct  = saved_s / flood_m3 * 100
    saved_y    = saved_s * CYCLES_PER_YEAR
    print(f"  Flood baseline         {FLOOD_MM_SEASON:>7.0f} mm   {flood_m3:>8,.0f} m3/season")
    print(f"  Entitlement-scheduled  {sched_mm:>7.0f} mm   {sched_m3:>8,.0f} m3/season")
    print(f"  SAVED                  {saved_pct:>7.1f} %    {saved_s:>8,.0f} m3/season")
    print(f"  SAVED (annual)                      {saved_y:>8,.0f} m3/year")
    
    # Attribution breakdown
    conv_drip_mm = 600.0
    conv_drip_m3 = conv_drip_mm * 10
    drip_hw_saving = flood_m3 - conv_drip_m3
    entitlement_saving = conv_drip_m3 - sched_m3
    print(f"\n  Honest Attribution Breakdown (per season):")
    print(f"    - Flood to Conventional Drip:       {drip_hw_saving:>8,.0f} m3 ({(drip_hw_saving/flood_m3)*100:.1f}% saving)")
    print(f"    - Drip to AgroStruxure Entitlement: {entitlement_saving:>8,.0f} m3 ({(entitlement_saving/flood_m3)*100:.1f}% saving, locked against rebound)")

    print(); print(SEP); print("2a. ENERGY  (per hectare)"); print(SEP)
    spec = (1000 * 9.81 * TDH_M) / (3.6e6 * WIRE_TO_WATER_EFF)   # kWh/m3
    pv_y        = PV_KWP * PEAK_SUN_HOURS * 365 * PERFORMANCE_RATIO
    pump_base   = flood_m3 * CYCLES_PER_YEAR * spec
    pump_sched  = sched_m3 * CYCLES_PER_YEAR * spec
    freed       = pump_base - pump_sched
    surplus     = pv_y - pump_sched
    surplus_pct = surplus / pv_y * 100
    print(f"  Specific pumping energy       {spec:>8.3f} kWh/m3  @ {TDH_M:.0f} m head")
    print(f"  PV generation ({PV_KWP} kWp)      {pv_y:>8,.0f} kWh/year")
    print(f"  Pump demand, flood baseline   {pump_base:>8,.0f} kWh/year")
    print(f"  Pump demand, scheduled        {pump_sched:>8,.0f} kWh/year")
    print(f"  Pumping energy freed          {freed:>8,.0f} kWh/year")
    idle_flood  = pv_y - pump_base
    print(f"  Idle PV today (flood baseline){idle_flood:>8,.0f} kWh/year  = {idle_flood/pv_y*100:.0f}% of generation")
    print(f"  + freed by right-sizing water {freed:>8,.0f} kWh/year")
    print(f"  SURPLUS once water is right-sized {surplus:>5,.0f} kWh/year  = {surplus_pct:.0f}% of generation")
    print(f"  (surplus = idle-today + freed; it exists BECAUSE irrigation is right-sized)")

    print(); print(SEP); print("2b. COOLING LOAD SIZING  (the v1 correction)"); print(SEP)
    print(f"  Setpoint {TARGET_T:.0f}°C (tomato-safe). Pull-down from {FIELD_T:.0f}°C field heat, COP {COP}.")
    for mt in (1.0, 2.0, 5.0):
        q_th = mt * 1000 * CP_PRODUCE * (FIELD_T - TARGET_T) / 3600
        q_el = q_th / COP
        kw   = q_el / WINDOW_H
        verdict = "fits array" if kw <= PV_KWP * 0.75 else "EXCEEDS single-farm array"
        print(f"  {mt:>4.1f} MT batch  {q_th:>6.1f} kWh_th  {q_el:>5.1f} kWh_el  {kw:>5.2f} kW avg   {verdict}")

    # v3 correction (2026-10-03): cold-chain energy is driven by the TONNAGE that is actually
    # pre-cooled, not by the number of days the room could run. One hectare yields 30 t/yr,
    # i.e. 15 batches of 2 MT. The 4-farm cluster (4 ha) therefore runs 60 batches/yr, all
    # powered from the HOST farm's idle PV surplus (the other three farms' arrays are not used).
    q_el_batch = PRECOOL_MT * 1000 * CP_PRODUCE * (FIELD_T - TARGET_T) / 3600 / COP
    hold_kwh   = 4.0                       # overnight hold on PCM, insulated 2 MT box (per batch-day)
    precool_kw = q_el_batch / WINDOW_H
    batches_ha      = YIELD_T_HA_YEAR / PRECOOL_MT          # 15 pull-downs per ha-year
    batches_cluster = batches_ha * CLUSTER_FARMS            # 60 per cluster-year
    cold_kwh_cluster = batches_cluster * (q_el_batch + hold_kwh)
    cold_kwh_y = cold_kwh_cluster / CLUSTER_FARMS           # per farm (1 ha)
    capture    = cold_kwh_cluster / surplus * 100           # share of the HOST farm's idle surplus
    residual   = surplus - cold_kwh_cluster                 # host-farm headroom after cooling
    room_cap_t = PRECOOL_MT * COLD_DAYS_YEAR                # theoretical room throughput
    room_util  = batches_cluster * PRECOOL_MT / room_cap_t * 100
    print(f"\n  CHOSEN: {PRECOOL_MT:.0f} MT farm pre-cooler -> {precool_kw:.2f} kW avg over {WINDOW_H:.0f} h")
    print(f"  Per batch: {q_el_batch:.1f} kWh pull-down + {hold_kwh:.1f} kWh hold = {q_el_batch+hold_kwh:.1f} kWh")
    print(f"  Batches: {batches_ha:.0f}/ha-year x {CLUSTER_FARMS} farms = {batches_cluster:.0f}/cluster-year "
          f"({batches_cluster*PRECOOL_MT:.0f} t of {room_cap_t:.0f} t room capacity = {room_util:.0f}% utilised)")
    print(f"  Cluster cold-chain energy     {cold_kwh_cluster:>8,.0f} kWh/year  = {capture:.0f}% of host-farm idle surplus")
    print(f"  Per farm (1 ha) equivalent    {cold_kwh_y:>8,.0f} kWh/year")
    print(f"  Unallocated headroom after cooling {residual:>5,.0f} kWh/year  ({residual/pv_y*100:.1f}% of PV output; stated, not claimed)")
    hold_th_kwh = hold_kwh * COP                                  # thermal energy the PCM must carry overnight
    pcm_kg = hold_th_kwh * 3600 / PCM_LATENT_KJ_KG
    print(f"  PCM carrying the {hold_kwh:.1f} kWh_el overnight hold ({hold_th_kwh:.0f} kWh_th): {pcm_kg:.0f} kg at {PCM_LATENT_KJ_KG:.0f} kJ/kg "
          f"({hold_th_kwh*3600/210:.0f}-{hold_th_kwh*3600/190:.0f} kg across the 190-210 kJ/kg target)")

    print(); print(SEP); print("3. POST-HARVEST  (per hectare)"); print(SEP)
    loss_b  = YIELD_T_HA_YEAR * LOSS_FARM_BASE
    loss_a  = YIELD_T_HA_YEAR * LOSS_FARM_AFTER
    saved_t = loss_b - loss_a
    saved_v = saved_t * TOMATO_PRICE_T
    print(f"  Baseline farm-stage loss   {LOSS_FARM_BASE*100:>5.2f}%  {loss_b:>5.2f} t/year   [NABCONS 2022]")
    print(f"  With pre-cooling           {LOSS_FARM_AFTER*100:>5.2f}%  {loss_a:>5.2f} t/year")
    print(f"  PRESERVED                           {saved_t:>5.2f} t/year")
    print(f"  Value @ Rs {TOMATO_PRICE_T/1000:.0f}/kg                 Rs {saved_v:>8,.0f}/year")

    print(); print(SEP); print("4. CARBON  (per hectare)"); print(SEP)
    # Headline = embodied emissions of produce NOT wasted. The smallholder baseline has no cooling,
    # so solar cooling displaces nothing; the diesel-genset case is shown as a scenario only.
    CO2_GENSET, CO2_EMBODIED = 0.80, 0.30   # kg/kWh diesel genset ; kg/kg tomato
    co2_food = saved_t * 1000 * CO2_EMBODIED / 1000
    co2_cool_scenario = cold_kwh_y * CO2_GENSET / 1000
    co2_total = co2_food
    print(f"  Spoilage avoided (embodied)         {co2_food:>5.2f} t CO2e/ha/year   <- HEADLINE")
    print(f"  Scenario only: if solar cooling displaced a diesel genset  +{co2_cool_scenario:.2f} t CO2e/ha/year (not in headline)")

    print(); print(SEP); print("5. TIER A - FARM PRE-COOLER (array-shared, 4-farm cluster)"); print(SEP)
    PRECOOL_CAPEX  = 400000   # 2 MT PCM pre-cooler, no PV of its own
    PV_AVOIDED     = 2.6      # kWp the pre-cooler does not need
    PV_RATE        = 35000    # Rs/kWp installed, small systems
    MIDH           = 0.35     # MIDH / AIF support, conservative
    TIMING_GAIN    = 12000    # Rs/farm/yr from avoiding distress sale (2-4 day hold)
    OPEX_FARM      = 2400     # SIM + maintenance

    array_saving = PV_AVOIDED * PV_RATE
    net_capex    = PRECOOL_CAPEX - array_saving
    after_sub    = net_capex * (1 - MIDH)
    per_farm_cap = after_sub / CLUSTER_FARMS
    farm_gain_base = saved_v - OPEX_FARM                  # BASE CASE: physical produce-loss reduction only
    farm_gain    = saved_v + TIMING_GAIN - OPEX_FARM       # SCENARIO: adds optional price-timing arbitrage
    payback_base = per_farm_cap / farm_gain_base
    payback_a    = per_farm_cap / farm_gain
    print(f"  Pre-cooler capex                    Rs {PRECOOL_CAPEX:>9,.0f}")
    print(f"  Less shared-array saving ({PV_AVOIDED} kWp)  Rs {array_saving:>9,.0f}   <- core novelty claim")
    print(f"  Net capex                           Rs {net_capex:>9,.0f}")
    print(f"  After {MIDH*100:.0f}% MIDH/AIF support         Rs {after_sub:>9,.0f}")
    print(f"  Per farm ({CLUSTER_FARMS}-farm cluster)           Rs {per_farm_cap:>9,.0f}")
    print(f"\n  Farmer annual gain:")
    print(f"    spoilage avoided                  Rs {saved_v:>9,.0f}   [high confidence]")
    print(f"    distress-sale avoidance           Rs {TIMING_GAIN:>9,.0f}   [medium, price-volatile]")
    print(f"    less opex                         Rs {-OPEX_FARM:>9,.0f}")
    print(f"    NET, scenario incl. price timing  Rs {farm_gain:>9,.0f}/year")
    print(f"    NET, BASE CASE (loss reduction)   Rs {farm_gain_base:>9,.0f}/year   <- headline (timing excluded)")
    print(f"  PAYBACK, Tier A BASE CASE              {payback_base:>6.1f} years (= {payback_base*CYCLES_PER_YEAR:.1f} harvests; pre-subsidy: {(net_capex/CLUSTER_FARMS)/farm_gain_base:.1f} years)")
    print(f"  PAYBACK, Tier A scenario + timing      {payback_a:>6.1f} years (pre-subsidy: {(net_capex/CLUSTER_FARMS)/farm_gain:.1f} years)")
    CONTROLLER_BOM, CONTROLLER_GAIN = 7540, 5000   # see section 7; benefit is approximate and NOT in farm_gain
    combined = (per_farm_cap + CONTROLLER_BOM) / (farm_gain + CONTROLLER_GAIN)
    combined_base = (per_farm_cap + CONTROLLER_BOM) / (farm_gain_base + CONTROLLER_GAIN)
    print(f"  Combined (cooler share + Rs {CONTROLLER_BOM:,} controller, +Rs {CONTROLLER_GAIN:,}/yr): base {combined_base:.1f} years | scenario {combined:.1f} years")
    print(f"  Value of surplus used for cooling: base Rs {farm_gain_base*CLUSTER_FARMS/cold_kwh_cluster:,.0f}/kWh net "
          f"(Rs {saved_v*CLUSTER_FARMS/cold_kwh_cluster:,.0f} gross) | scenario Rs {farm_gain*CLUSTER_FARMS/cold_kwh_cluster:,.0f}/kWh net "
          f"(Rs {(saved_v+TIMING_GAIN)*CLUSTER_FARMS/cold_kwh_cluster:,.0f} gross)")

    print(); print(SEP); print("6. TIER B - FPO HOLDING ROOM (own array, 20-farm hub)"); print(SEP)
    HUB_CAPEX, HUB_MT  = 1200000, 5.0
    RESIDENCE_D, UTIL  = 8.0, 0.65
    TARIFF_KG          = 3.0
    HUB_OPEX           = 35000
    turns  = COLD_DAYS_YEAR / RESIDENCE_D
    thru_t = HUB_MT * turns * UTIL
    rev    = thru_t * 1000 * TARIFF_KG
    net    = rev - HUB_OPEX
    hub_as = HUB_CAPEX * (1 - MIDH)
    print(f"  Hub capex (5 MT, own 4 kWp PV)      Rs {HUB_CAPEX:>9,.0f}")
    print(f"  After {MIDH*100:.0f}% MIDH/AIF support         Rs {hub_as:>9,.0f}")
    print(f"  Throughput {turns:.1f} turns x {UTIL*100:.0f}% util     {thru_t:>9,.0f} t/year")
    print(f"  Revenue @ Rs {TARIFF_KG:.2f}/kg/stay          Rs {rev:>9,.0f}/year")
    print(f"  Less opex                           Rs {-HUB_OPEX:>9,.0f}")
    print(f"  NET                                 Rs {net:>9,.0f}/year")
    print(f"  PAYBACK, Tier B                        {hub_as/net:>6.1f} years (pre-subsidy: {HUB_CAPEX/net:.1f} years)")
    print("  NOTE: Tier B claims NO shared-array saving - it has its own PV.")

    print(); print(SEP); print("7. EDGE CONTROLLER BOM (1,000-unit scale)"); print(SEP)
    bom = [
        ("ESP32-S3-WROOM-1 (16 MB flash, 8 MB PSRAM)",               420),
        ("MAX485 isolated RS485 transceiver + TVS",                  180),
        ("FDR capacitive soil probes x2 (10 cm / 30 cm)",            760),
        ("SHT31-D temperature + RH, IP65 probe  [ET0 input]",        180),
        ("Silicon pyranometer / PV reference cell  [ET0 input]",     420),
        ("Hall-effect flow meter 1in  [entitlement metering]",       650),
        ("12 V bistable latching solenoid valve, 1in",               650),
        ("Schneider TeSys D contactor x2, mech. interlocked",       2300),
        ("24 V SMPS + isolated relay driver board",                  380),
        ("SIM7600 4G LTE module + antenna",                          620),
        ("IP67 enclosure, DIN rail, SPD, wiring, PCB",               980),
    ]
    for n, c in bom:
        print(f"  {n:<54} Rs {c:>6,}")
    print(f"  {'-'*54}    {'-'*6}")
    bom_total = sum(c for _, c in bom)
    print(f"  {'TOTAL':<54} Rs {bom_total:>6,}")
    print(f"\n  Standalone Controller Payback (Water, Pump Health, Yield Protection ~Rs 5,000/yr):")
    print(f"  Payback = {bom_total / 5000:.1f} years (= {bom_total / 5000 * CYCLES_PER_YEAR:.0f} crop seasons at {CYCLES_PER_YEAR} cycles/year).")

    print(); print(SEP); print("8. HEADLINE SET  (Single Source of Truth)"); print(SEP)
    print(f"  Groundwater saved        {saved_pct:.0f}%   ({saved_y:,.0f} m3/ha/year)")
    print(f"  Pumping energy freed     {freed:,.0f} kWh/ha/year")
    print(f"  Idle PV surplus today    {surplus:,.0f} kWh/ha/year ({surplus_pct:.0f}% of generation)")
    print(f"  Cold-chain energy        {cold_kwh_cluster:,.0f} kWh/cluster-year ({capture:.0f}% of host-farm surplus; {cold_kwh_y:,.0f} kWh per farm)")
    print(f"  Produce preserved        {saved_t:.2f} t/ha/year")
    print(f"  Carbon                   {co2_total:.2f} t CO2e/ha/year (embodied emissions of avoided spoilage)")
    print(f"  Farmer net gain          Rs {farm_gain_base:,.0f}/ha/year base case | Rs {farm_gain:,.0f} with optional price timing")
    print(f"  Controller BOM           Rs {bom_total:,}")
    print(f"  Tier A payback           {payback_base:.1f} years base case | {payback_a:.1f} years with optional price timing  |  Tier B payback {hub_as/net:.1f} years")
    print(SEP)

if __name__ == "__main__":
    run_model()
