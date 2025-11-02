import pandas as pd
import json
import os

print("=" * 60)
print("CREATING COMBINED POPULATION + INFRASTRUCTURE DATA")
print("=" * 60)

# ========== PART 1: POPULATION DATA ==========
print("\n[1/2] Processing Population Data...")

# Load all counties data
counties_csv = os.path.join('data', 'Florida_all_counties_2035_2045.csv')
counties_data = pd.read_csv(counties_csv)

# Calculate growth rate from 2035 to 2045
counties_data['growth_rate'] = ((counties_data['2045'] - counties_data['2035']) / counties_data['2035']) * 100

print("Top 10 counties by growth rate (2035-2045):")
top_counties = counties_data.nlargest(10, 'growth_rate')[['County', '2035', '2045', 'growth_rate']]
print(top_counties)

# County coordinates
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

# GTO Triangle counties
gto_counties = {'ALACHUA', 'ORANGE', 'HILLSBOROUGH', 'OSCEOLA', 'POLK'}

# Create GeoJSON files for each year
years = [2035, 2040, 2045]

for year in years:
    features = []
    for idx, row in counties_data.iterrows():
        county = row['County'].upper()
        if county in county_coords:
            lat, lon = county_coords[county]
            population = row[str(year)]
            growth_rate = row['growth_rate']
            
            # Map growth rate to intensity using fixed thresholds
            if growth_rate > 10:
                intensity = 1.0
            elif growth_rate >= 7:
                intensity = 0.75
            elif growth_rate >= 4:
                intensity = 0.5
            else:
                intensity = 0.25
            
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "county": county,
                    "population": int(population),
                    "growth_rate": round(growth_rate, 2),
                    "intensity": intensity,
                    "is_gto": county in gto_counties,
                    "layer": "population"
                }
            }
            features.append(feature)
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Save GeoJSON
    output_path = os.path.join('data', f'Florida_heatmap_{year}.geojson')
    with open(output_path, 'w') as f:
        json.dump(geojson_data, f, indent=2)
    
    print(f"  ✓ Created {output_path}")

# ========== PART 2: INFRASTRUCTURE DATA ==========
print("\n[2/2] Creating Infrastructure Data...")

infrastructure_data = {
    "airports": [
        {"name": "Orlando International Airport", "code": "MCO", "coords": [28.4294, -81.3089], "size": "Major Hub", "gto": True},
        {"name": "Tampa International Airport", "code": "TPA", "coords": [27.9755, -82.5332], "size": "Major Hub", "gto": True},
        {"name": "Gainesville Regional Airport", "code": "GNV", "coords": [29.6900, -82.2718], "size": "Regional", "gto": True},
        {"name": "Miami International Airport", "code": "MIA", "coords": [25.7932, -80.2906], "size": "Major Hub", "gto": False},
        {"name": "Fort Lauderdale-Hollywood", "code": "FLL", "coords": [26.0726, -80.1527], "size": "Major Hub", "gto": False},
        {"name": "Jacksonville International", "code": "JAX", "coords": [30.4941, -81.6879], "size": "Major Hub", "gto": False},
    ],
    
    "major_stadiums": [
        {"name": "Ben Hill Griffin Stadium", "location": "Gainesville", "coords": [29.6499, -82.3487], "capacity": 88548, "type": "Football", "gto": True, "olympic_ready": True},
        {"name": "Raymond James Stadium", "location": "Tampa", "coords": [27.9759, -82.5033], "capacity": 65618, "type": "Football/NFL", "gto": True, "olympic_ready": True},
        {"name": "Camping World Stadium", "location": "Orlando", "coords": [28.5392, -81.4025], "capacity": 65438, "type": "Football", "gto": True, "olympic_ready": True},
        {"name": "Amway Center", "location": "Orlando", "coords": [28.5392, -81.3839], "capacity": 18846, "type": "Arena", "gto": True, "olympic_ready": True},
        {"name": "Amalie Arena", "location": "Tampa", "coords": [27.9428, -82.4519], "capacity": 19092, "type": "Arena", "gto": True, "olympic_ready": True},
        {"name": "Hard Rock Stadium", "location": "Miami Gardens", "coords": [25.9580, -80.2389], "capacity": 64767, "type": "Football/NFL", "gto": False, "olympic_ready": False},
    ],
    
    "universities": [
        {"name": "University of Florida", "location": "Gainesville", "coords": [29.6436, -82.3549], "students": 55000, "gto": True},
        {"name": "University of South Florida", "location": "Tampa", "coords": [28.0587, -82.4139], "students": 50000, "gto": True},
        {"name": "University of Central Florida", "location": "Orlando", "coords": [28.6024, -81.2001], "students": 68000, "gto": True},
    ]
}

# Create infrastructure GeoJSON
infra_features = []

# Add airports
for airport in infrastructure_data["airports"]:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [airport["coords"][1], airport["coords"][0]]
        },
        "properties": {
            "name": airport["name"],
            "code": airport["code"],
            "type": "airport",
            "size": airport["size"],
            "is_gto": airport["gto"],
            "icon": "✈️",
            "layer": "infrastructure"
        }
    }
    infra_features.append(feature)

# Add stadiums
for stadium in infrastructure_data["major_stadiums"]:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [stadium["coords"][1], stadium["coords"][0]]
        },
        "properties": {
            "name": stadium["name"],
            "location": stadium["location"],
            "capacity": stadium["capacity"],
            "type": "stadium",
            "stadium_type": stadium["type"],
            "is_gto": stadium["gto"],
            "olympic_ready": stadium["olympic_ready"],
            "icon": "🏟️" if stadium["capacity"] > 60000 else "🏢",
            "layer": "infrastructure"
        }
    }
    infra_features.append(feature)

# Add universities
for university in infrastructure_data["universities"]:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [university["coords"][1], university["coords"][0]]
        },
        "properties": {
            "name": university["name"],
            "location": university["location"],
            "students": university["students"],
            "type": "university",
            "is_gto": university["gto"],
            "icon": "🎓",
            "layer": "infrastructure"
        }
    }
    infra_features.append(feature)

infra_geojson = {
    "type": "FeatureCollection",
    "features": infra_features
}

# Save infrastructure GeoJSON
infra_output = os.path.join('data', 'Florida_infrastructure.geojson')
with open(infra_output, 'w') as f:
    json.dump(infra_geojson, f, indent=2)

print(f"  ✓ Infrastructure data created: {len(infra_features)} features")
print(f"    - {len(infrastructure_data['airports'])} airports")
print(f"    - {len(infrastructure_data['major_stadiums'])} stadiums")
print(f"    - {len(infrastructure_data['universities'])} universities")
print(f"  ✓ Saved to: {infra_output}")

print("\n" + "=" * 60)
print("✅ ALL DATA GENERATED SUCCESSFULLY!")
print("=" * 60)
print("\nGenerated files:")
print("  - data/Florida_heatmap_2035.geojson")
print("  - data/Florida_heatmap_2040.geojson")
print("  - data/Florida_heatmap_2045.geojson")
print("  - data/Florida_infrastructure.geojson")
print("\nNext: Run the HTML file to see the combined visualization!")