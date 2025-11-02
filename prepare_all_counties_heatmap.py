import pandas as pd
import json
import os

# Use relative paths from current working directory
file_path = os.path.join('data', 'Population Data Low-Medium-High.xlsx')
df = pd.read_excel(file_path)

# Fill NaN counties with the previous county value (forward fill)
df['County'] = df['County'].fillna(method='ffill')

# Filter to Medium series (most realistic projection) for ALL counties
all_counties_data = df[df['Series'] == 'Medium'].copy()

# Extract only 2035, 2040, 2045 columns (as integers)
years_cols = [2035, 2040, 2045]
counties_filtered = all_counties_data[['County'] + years_cols].copy()

print(f"Total Florida counties: {len(counties_filtered)}")
print("\nAll Florida Counties Population Data (2035-2045):")
print(counties_filtered.head(10))

# Save as CSV for reference
output_path = os.path.join('data', 'Florida_all_counties_2035_2045.csv')
counties_filtered.to_csv(output_path, index=False)
print(f"\n✓ CSV saved: {output_path}")