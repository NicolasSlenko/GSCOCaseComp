import pandas as pd
import json
import os

# Use relative paths from current working directory
file_path = os.path.join('data', 'Population Data Low-Medium-High.xlsx')
df = pd.read_excel(file_path)

# Fill NaN counties with the previous county value (forward fill)
df['County'] = df['County'].fillna(method='ffill')

# Print columns to verify
print("Available columns:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head(10))

# GTO Triangle counties
gto_counties = ['ALACHUA', 'ORANGE', 'HILLSBOROUGH', 'OSCEOLA', 'POLK']

# Filter to GTO counties and Medium series (most realistic projection)
gto_data = df[(df['County'].str.upper().isin(gto_counties)) & (df['Series'] == 'Medium')].copy()

# Extract only 2035, 2040, 2045 columns (as integers, not strings)
years_cols = [2035, 2040, 2045]
gto_filtered = gto_data[['County'] + years_cols]

print("\nGTO Population Data (2035-2045):")
print(gto_filtered)

# Calculate average population across the decade for heatmap intensity
gto_filtered['avg_population'] = gto_filtered[years_cols].mean(axis=1)

# Save as CSV for reference
output_path = os.path.join('data', 'GTO_population_2035_2045.csv')
gto_filtered.to_csv(output_path, index=False)
print(f"\n✓ CSV saved: {output_path}")