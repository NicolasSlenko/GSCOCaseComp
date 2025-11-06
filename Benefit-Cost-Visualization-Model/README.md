# FOVI Enhanced Dashboard - Standalone Version

## Florida Olympics Economic Viability Analysis

This is the **comprehensive BCR (Benefit-Cost Ratio) analysis dashboard** that shows the viability of hosting the Olympics in Florida.

## Key Features

- **Benefit-Cost Ratio (BCR) Analysis** - Primary viability metric
  - BCR < 1.0 = Not Viable
  - BCR = 1.0 = Break-Even
  - BCR > 1.0 = Viable
  - BCR > 1.5 = Highly Viable

- **Comprehensive Benefits Model** including:
  - Core Tourism Revenue
  - Property Tax Growth
  - Corporate Relocations
  - Construction Tax Offset
  - Major Events Pipeline
  - Convention Business Growth
  - Infrastructure Value
  - Migration Benefits

- **Clean McKinsey-Style Presentation**
- **Full Economic Impact Analysis**
- **Historical Validation** (Barcelona, Atlanta, London)

## Quick Start

### Windows:
Double-click `run_dashboard.bat`

### Manual:
```bash
pip install -r requirements.txt
streamlit run fovi_dashboard_enhanced.py --server.port 8502
```

The dashboard will open at: **http://localhost:8502**

## Default Settings

With default parameters, the dashboard shows:
- **BCR: ~1.4-1.8** (Highly Viable)
- **Total Benefits: ~$15,000M**
- **Net Public Cost: ~$10,000M**
- **Net Fiscal Gain: ~+$5,000M**

## Analysis Modes

1. **Basic Tourism Model** - Conservative estimate
2. **Comprehensive Benefits Model** - Moderate estimate
3. **Full Economic Impact** (Default) - Full estimate with timeline corrections

## Requirements

- Python 3.8 or higher
- See `requirements.txt` for package dependencies

## Files Included

- `fovi_dashboard_enhanced.py` - Main dashboard application
- `requirements.txt` - Python dependencies
- `Growth/Industries/SAGDP8_FL_1997_2024.csv` - Florida GDP data
- `run_dashboard.bat` - Windows launcher script
- `README.md` - This file

## Notes

This standalone version includes all necessary files to run the dashboard independently. The dashboard uses industry-standard BCR methodology as used by World Bank, OECD, and U.S. OMB.

