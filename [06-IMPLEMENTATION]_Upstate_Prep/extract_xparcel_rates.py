"""
Extract and parse Xparcel Ground rates from the FirstMile rate file
"""

import pandas as pd
import numpy as np

# Load the rate file
rate_file = 'Upstate Prep_FirstMile_Xparcel_08-20-25.xlsx'

# Read Xparcel Ground sheet with proper header row detection
df_ground = pd.read_excel(rate_file, sheet_name='Xparcel Ground SLT_NATL', header=None)

print("=" * 80)
print("XPARCEL GROUND RATE EXTRACTION")
print("=" * 80)

# Display the first 20 rows to understand structure
print("\nFirst 20 rows of Xparcel Ground sheet:")
print(df_ground.iloc[:20])

# Find the row with "Zone" headers
zone_row_idx = None
for idx, row in df_ground.iterrows():
    row_str = ' '.join(str(val) for val in row.values if pd.notna(val))
    if 'Zone' in row_str or 'zone' in row_str.lower():
        zone_row_idx = idx
        print(f"\nFound Zone header at row {idx}")
        print(f"Zone row content: {row.values}")
        break

# Extract Select rates (first section)
print("\n" + "="*60)
print("EXTRACTING SELECT RATES")
print("="*60)

if zone_row_idx is not None:
    # Use the zone row as header
    select_start = zone_row_idx + 1
    select_end = select_start + 20  # Assuming up to 20 lb
    
    # Get zone columns
    zone_cols = df_ground.iloc[zone_row_idx, 2:10].values  # Zones 1-8 typically in columns 2-9
    print(f"Zone columns found: {zone_cols}")
    
    # Extract Select rates
    select_rates = df_ground.iloc[select_start:select_end, 1:10].copy()
    select_rates.columns = ['Weight'] + [f'Zone {i}' for i in range(1, 9)]
    
    print("\nSelect Rates (first 10 rows):")
    print(select_rates.head(10))

# Find National rates section (should be below Select)
print("\n" + "="*60)
print("LOOKING FOR NATIONAL RATES")
print("="*60)

# Search for "National" keyword
national_row_idx = None
for idx in range(zone_row_idx + 20, len(df_ground)):
    row_str = ' '.join(str(val) for val in df_ground.iloc[idx].values if pd.notna(val))
    if 'National' in row_str or 'national' in row_str.lower():
        national_row_idx = idx
        print(f"Found National section at row {idx}")
        break

# Check the row structure around National section
if national_row_idx:
    print(f"\nRows around National section:")
    for i in range(max(0, national_row_idx-2), min(len(df_ground), national_row_idx+5)):
        print(f"Row {i}: {df_ground.iloc[i, :5].values}")  # Show first 5 columns