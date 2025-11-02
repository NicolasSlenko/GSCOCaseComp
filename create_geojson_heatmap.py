import pandas as pd
import json
import os

# Load all counties data
counties_csv = os.path.join('data', 'Florida_all_counties_2035_2045.csv')
counties_data = pd.read_csv(counties_csv)

# Florida county centroids (approximate lat, lon for major counties)
county_coords = {
    'ALACHUA': [29.6437, -82.3105],
    'BAKER': [30.3316, -82.2859],
    'BAY': [30.2086, -85.6602],
    'BRADFORD': [29.9447, -82.1759],
    'BREVARD': [28.2639, -80.7214],
    'BROWARD': [26.1224, -80.3724],
    'CALHOUN': [30.3971, -85.1974],
    'CHARLOTTE': [26.8939, -82.0453],
    'CITRUS': [28.8894, -82.4812],
    'CLAY': [29.9763, -81.7293],
    'COLLIER': [26.1420, -81.7089],
    'COLUMBIA': [30.1898, -82.6393],
    'DESOTO': [27.1645, -81.8109],
    'DIXIE': [29.5935, -83.0779],
    'DUVAL': [30.3322, -81.6557],
    'ESCAMBIA': [30.4213, -87.2169],
    'FLAGLER': [29.4686, -81.2534],
    'FRANKLIN': [29.8439, -84.8785],
    'GADSDEN': [30.5883, -84.6422],
    'GILCHRIST': [29.6994, -82.8084],
    'GLADES': [26.9531, -81.1359],
    'GULF': [29.9885, -85.2799],
    'HAMILTON': [30.5235, -82.9540],
    'HARDEE': [27.4900, -81.8209],
    'HENDRY': [26.5531, -81.1359],
    'HERNANDO': [28.5353, -82.4759],
    'HIGHLANDS': [27.3164, -81.3431],
    'HILLSBOROUGH': [27.9947, -82.4596],
    'HOLMES': [30.8547, -85.8352],
    'INDIAN RIVER': [27.6648, -80.5706],
    'JACKSON': [30.7816, -85.2299],
    'JEFFERSON': [30.5469, -83.8679],
    'LAFAYETTE': [29.9841, -83.2279],
    'LAKE': [28.7606, -81.6348],
    'LEE': [26.5629, -81.8723],
    'LEON': [30.4583, -84.2807],
    'LEVY': [29.3025, -82.7579],
    'LIBERTY': [30.2391, -84.8785],
    'MADISON': [30.4691, -83.4129],
    'MANATEE': [27.4989, -82.3264],
    'MARION': [29.1944, -82.1401],
    'MARTIN': [27.1017, -80.3977],
    'MIAMI-DADE': [25.6171, -80.6437],
    'MONROE': [24.7543, -81.1359],
    'NASSAU': [30.6102, -81.7848],
    'OKALOOSA': [30.6326, -86.5764],
    'OKEECHOBEE': [27.2439, -80.8298],
    'ORANGE': [28.5421, -81.3723],
    'OSCEOLA': [28.2174, -81.3888],
    'PALM BEACH': [26.7056, -80.2683],
    'PASCO': [28.2978, -82.4359],
    'PINELLAS': [27.9119, -82.7623],
    'POLK': [28.0295, -81.7714],
    'PUTNAM': [29.6486, -81.6637],
    'SANTA ROSA': [30.6535, -86.9877],
    'SARASOTA': [27.2770, -82.5242],
    'SEMINOLE': [28.7239, -81.2373],
    'ST. JOHNS': [29.9002, -81.3628],
    'ST. LUCIE': [27.4467, -80.3256],
    'SUMTER': [28.6783, -82.0859],
    'SUWANNEE': [30.1869, -82.9540],
    'TAYLOR': [30.0688, -83.5879],
    'UNION': [30.0597, -82.4359],
    'VOLUSIA': [29.0280, -81.0998],
    'WAKULLA': [30.1419, -84.3985],
    'WALTON': [30.6269, -86.1077],
    'WASHINGTON': [30.6102, -85.6502]
}

# GTO Triangle counties for highlighting
gto_counties = {'ALACHUA', 'ORANGE', 'HILLSBOROUGH', 'OSCEOLA', 'POLK'}

# Create separate GeoJSON files for each year
years = [2035, 2040, 2045]

for year in years:
    # Normalize population for this year
    min_pop = counties_data[str(year)].min()
    max_pop = counties_data[str(year)].max()
    
    features = []
    for idx, row in counties_data.iterrows():
        county = row['County'].upper()
        if county in county_coords:
            lat, lon = county_coords[county]
            population = row[str(year)]
            intensity = (population - min_pop) / (max_pop - min_pop)
            
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "county": county,
                    "population": int(population),
                    "intensity": round(intensity, 3),
                    "is_gto": county in gto_counties
                }
            }
            features.append(feature)
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Save GeoJSON for this year
    output_path = os.path.join('data', f'Florida_heatmap_{year}.geojson')
    with open(output_path, 'w') as f:
        json.dump(geojson_data, f, indent=2)
    
    print(f"✓ Created {output_path} with {len(features)} counties")

print("\n✓ All heatmap GeoJSON files created!")