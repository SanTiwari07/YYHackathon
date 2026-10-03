# 04 User Research & Field Personas

**Document Code:** USER-RES-04  
**Domain:** Farmer Behavioral Archetypes, Mental Models & Field Journeys  

---

## 1. Key User Archetypes

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│ PERSONA 1: Ramesh Patil (48)    │       │ PERSONA 2: Sunita Shinde (38)   │
│ Smallholder Farmer (Marathwada) │       │ FPO Director & Lead Farmer      │
├─────────────────────────────────┤       ├─────────────────────────────────┤
│ • Land: 2.2 Acres (0.9 ha)      │       │ • Manages: 450 Smallholders     │
│ • Crops: Cotton, Soybean, Onion │       │ • Focus: Aggregation & Inputs   │
│ • Asset: 5HP Submersible Borewell│      │ • Pain: 22% Onion Spoilage      │
│ • Literacy: 8th Grade (Marathi) │       │ • Tech: Active WhatsApp / Excel │
│ • Goal: Avoid crop failure      │       │ • Goal: Farm-gate cold storage  │
└─────────────────────────────────┘       └─────────────────────────────────┘
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│ PERSONA 3: Suresh Kumar (34)    │       │ PERSONA 4: Anand Rao (42)       │
│ Solar Pump Field Technician     │       │ Assistant Engineer (MSEDCL/DISCOM)│
├─────────────────────────────────┤       ├─────────────────────────────────┤
│ • Role: Installs PM-KUSUM Pumps │       │ • Role: Rural Feeder Operations │
│ • Coverage: 30 Villages         │       │ • Pain: 3-Phase Feeder Tripping │
│ • Pain: Constant repair calls   │       │ • Pain: Massive Unmetered Losses│
│ • Tool: Basic Multimeter & App  │       │ • Goal: Shift Day Peak to Solar │
└─────────────────────────────────┘       └─────────────────────────────────┘
```

---

## 2. Farmer Day-in-the-Life Comparison: Before vs. After

### Before (Status Quo Baseline):
* **01:30 AM:** Phone rings. 3-phase grid power has arrived on the rural feeder.
* **02:00 AM:** Ramesh wakes up, grabs a torch, and walks 1.5 km to his field in the dark to press the green starter button on his 5HP pump.
* **02:15 AM:** Voltage fluctuates to 175V. The starter hums loudly; motor coil heats up.
* **05:30 AM:** Ramesh returns home to sleep while the pump floods the field unchecked for 4 hours. 60% of water percolates past roots or pools on the surface.
* **09:00 AM:** Power cuts out. Ramesh does not know how much water was pumped.
* **Harvest Week:** Harvests 4 tonnes of onions. Local APMC mandi price crashes from ₹25/kg to ₹7/kg due to oversupply. Ramesh has no storage; sells at ₹7/kg to avoid complete rotting.

### After (With Our Proposed Architecture):
* **08:30 AM:** Sunrise. Solar irradiance reaches threshold. The on-site Altivar Solar VFD powers up smoothly using clean DC solar electricity.
* **09:00 AM:** The edge controller reads the capacitive root-zone soil moisture and computes the day's crop water requirement ($ET_c$) using FAO-56. Soil moisture is at 38% (below Field Capacity of 45%).
* **09:15 AM:** Edge controller opens the automated pulse drip valve. Pump operates at optimal variable frequency, delivering exactly 18 mm of water directly to plant root zones.
* **11:45 AM:** Root soil moisture reaches field capacity (45%). Edge controller automatically closes the irrigation valve and slows the pump motor.
* **11:46 AM:** Surplus solar power (3.2 kW) is automatically diverted through the smart changeover switchgear to the FPO's farm-gate micro-cold room, cooling harvested onions to 4°C.
* **12:00 PM:** Ramesh receives a Marathi WhatsApp voice note & SMS: *"Namaskar Ramesh. Your onion plot has received full water (2,400 litres). Pump is OFF. Your cold storage unit is running on 100% solar power."*
* **Outcome:** Zero night visits; 40% water saved; 0 diesel spent; onions safely stored for 3 weeks until mandi prices recover to ₹22/kg.

---

## 3. Critical Mental Models & Trust Barriers

1. **The "Wet Soil Surface" Illusion:**
   - *Farmer Belief:* "If the top 2 inches of soil look dry and cracked, the crop is dying."
   - *Scientific Reality:* Deep root zones (15–40 cm) often retain sufficient capillary water. Pumping water when the surface is cracked leads to massive over-irrigation.
   - *Design Response:* Visual cross-section indicator in the mobile UI showing underground root moisture level, not just surface status.
2. **The "Free Power Means Maximize Pumping" Habit:**
   - *Farmer Belief:* "Water is wealth; more water equals higher yield."
   - *Scientific Reality:* Excess water suffocates roots, starves them of oxygen, promotes phytophthora root rot, and leaches expensive fertilizers.
   - *Design Response:* Educational yield-impact metrics showing how over-watering directly reduces crop output.
3. **The Fear of Automation Failure:**
   - *Farmer Belief:* "What if the computer hangs and my pump runs dry or doesn't water my cash crop?"
   - *Design Response:* Physical manual bypass switch on the enclosure; failsafe hardware watchdog timers that disconnect relays if microcontrollers stall.
