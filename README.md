Case Comp Team Salvador:

Teammates:
- Nicolas Slenko
- Zhicheng Li 
- Aman Vyas
- Ananda Chatterjee
- Elizabeth Jang

---

## Project Overview

**Florida Olympic Vision: Gainesville–Tampa–Orlando (GTO) Framework**

This project analyzes the feasibility of Florida hosting the Summer Olympic Games through a joint-city bid spanning Tampa, Orlando, and Lakeland, with Gainesville providing the main stadium venue.

### Central Question
*"Should the state of Florida host the Olympic Games? If so, where?"*

**Answer**: Yes — through a coordinated **Tampa–Orlando–Lakeland (TOL)** corridor approach with Gainesville's Ben Hill Griffin Stadium serving as the main venue.

---

## Key Documents

### 📊 Analysis & Strategy
- **[Executive Summary](docs/Executive_Summary.md)** — One-page recommendation and benefits summary
- **[Slide Deck Outline](docs/Slide_Outline.md)** — Complete presentation structure with data sources
- **[FDOT Transportation Infrastructure](docs/FDOT_Transportation_Infrastructure.md)** — Detailed transportation analysis supporting the bid

### 📈 Data & Visualizations
- **[City Compliance Matrix](data/city_compliance_matrix.csv)** — IOC requirements vs. candidate cities
- **[FDOT Dashboard](docs/fdot_transportation_dashboard.html)** — Interactive transportation infrastructure visualization
- **Population Heatmaps** — `data/Florida_heatmap_2035/2040/2045.geojson`
- **Infrastructure Assets** — `data/Florida_infrastructure.geojson`, `data/Florida_highways.geojson`

### 🖥️ Interactive Demos
- **[View Heatmap](view_heatmap.html)** — Population growth visualization (2035-2045)
- **[Olympic Requirements Dashboard](olympic_requirements_dashboard.html)** — IOC criteria tracker

---

## Key Findings

### Transportation Infrastructure
- **$66 billion FDOT investment** (2025-2030) with $18B allocated to Central Florida
- **Brightline high-speed rail** expansion: Orlando–Tampa in 60 minutes
- **3 major airports**: MCO (50M capacity), TPA (25M), GNV (regional)
- **I-4 corridor**: 84-mile Tampa-Orlando connection with express lanes
- **Projected ROI**: $2.6 billion annual productivity gain from transit improvements

### Venue & Lodging Compliance
- **40 venues**: Met through combined Orlando + Tampa facilities
- **80k+ stadium**: ✅ Ben Hill Griffin Stadium (Gainesville, 88,548 capacity)
- **50k hotel rooms**: ✅ Combined inventory exceeds requirement
- **5k restaurants**: ✅ Orlando + Tampa metro areas
- **Olympic Village**: Lakeland (central location, post-Games conversion to workforce housing)

### Economic Impact
- **Job creation**: Construction + hospitality sectors
- **Tourism boost**: Leveraging Florida's existing 130M+ annual visitors
- **Legacy benefits**: Permanent transit infrastructure + 3,000-4,000 housing units

---

## Project Structure

```
GSCOCaseComp/
├── docs/                              # Documentation & reports
│   ├── Executive_Summary.md           # One-page recommendation
│   ├── Slide_Outline.md              # Presentation structure
│   ├── FDOT_Transportation_Infrastructure.md
│   └── fdot_transportation_dashboard.html
├── data/                              # GeoJSON & CSV datasets
│   ├── city_compliance_matrix.csv
│   ├── Florida_heatmap_2035.geojson
│   ├── Florida_heatmap_2040.geojson
│   ├── Florida_heatmap_2045.geojson
│   ├── Florida_infrastructure.geojson
│   ├── Florida_highways.geojson
│   └── Florida_all_counties_2035_2045.csv
├── images/                            # Visual assets
│   ├── amway.avif
│   ├── jax.avif
│   └── ucf.avif
├── create_combined_data.py           # Data generation script
├── create_fdot_dashboard.py          # Transportation dashboard generator
├── view_heatmap.html                 # Population heatmap viewer
└── olympic_requirements_dashboard.html

```

---

## Running the Project

### Generate Data Files
```powershell
# Create population heatmaps + infrastructure GeoJSON
python create_combined_data.py

# Generate FDOT transportation dashboard
python create_fdot_dashboard.py
```

### View Interactive Dashboards
1. Open `view_heatmap.html` in a browser to see population growth projections
2. Open `docs/fdot_transportation_dashboard.html` for transportation infrastructure analysis
3. Open `olympic_requirements_dashboard.html` for IOC compliance tracking

---

## Data Sources

- **BEBR 2023**: Florida population projections (Medium series, 2025-2050)
- **FDOT 2025**: Infrastructure investment program
- **Brightline Florida**: Orlando-Tampa corridor specifications
- **Visit Florida 2024**: Tourism statistics and hotel inventories
- **ACS 2023**: Commuting patterns, employment data, housing metrics
- **IOC**: Olympic hosting requirements (2025 guidelines)

---

## Next Steps

1. ✅ Compliance matrix and executive summary completed
2. ✅ FDOT transportation analysis completed
3. ⏳ Finalize venue inventory with exact capacities
4. ⏳ Validate hotel room counts with Visit Florida data
5. ⏳ Create financial model (CAPEX breakdown + ROI scenarios)
6. ⏳ Build final presentation deck (PPTX)

---

## Contact

For questions about this analysis, contact the team members listed above.