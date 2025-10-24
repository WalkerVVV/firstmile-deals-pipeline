"""
Create Volume Distribution Matrix by Weight and Zone for Upstate Prep
Formatted for Excel copy/paste into tier tool
"""

import pandas as pd
import numpy as np
import random

# Load the data
df = pd.read_csv('T30 PLD Upstate Prep.csv')

# Clean and prepare data
df['Weight (lb)'] = pd.to_numeric(df['Weight (lb)'], errors='coerce')
df['Weight (oz)'] = df['Weight (lb)'] * 16

# Since we don't have actual zone data in the PLD, we'll need to estimate based on state distribution
# Zone mapping (approximate based on shipping from SC)
zone_mapping = {
    'SC': 2, 'NC': 2, 'GA': 2, 'VA': 3, 'TN': 3,
    'FL': 3, 'AL': 3, 'MS': 3, 'KY': 3, 'WV': 3,
    'MD': 4, 'DE': 4, 'PA': 4, 'NJ': 4, 'NY': 4, 'CT': 4, 'RI': 4, 'MA': 4, 'VT': 4, 'NH': 4, 'ME': 4,
    'OH': 4, 'IN': 4, 'MI': 4, 'IL': 4, 'WI': 4,
    'LA': 4, 'AR': 4, 'MO': 4, 'IA': 4, 'MN': 4,
    'TX': 5, 'OK': 5, 'KS': 5, 'NE': 5, 'SD': 5, 'ND': 5,
    'CO': 5, 'NM': 5, 'WY': 5, 'MT': 5,
    'AZ': 6, 'UT': 6, 'NV': 6, 'ID': 6,
    'CA': 7, 'OR': 7, 'WA': 7,
    'AK': 8, 'HI': 8
}

# Assign zones based on state
df['Zone'] = df['State'].map(zone_mapping).fillna(5)  # Default to zone 5 for unmapped

# Create billable weight based on carrier rules
def calculate_billable_weight(weight_oz):
    if pd.isna(weight_oz):
        return np.nan
    if weight_oz < 16:
        # Under 1 lb: round up to next oz, but 15.99 is special tier
        if weight_oz > 15 and weight_oz < 16:
            return 15.99
        else:
            return np.ceil(weight_oz)
    else:
        # Over 1 lb: round up to next pound, convert to oz
        return np.ceil(weight_oz / 16) * 16

df['Billable Weight (oz)'] = df['Weight (oz)'].apply(calculate_billable_weight)

# Create weight categories for the matrix
weight_categories = []
# Under 1 lb (1-15 oz and 15.99 oz)
for oz in range(1, 16):
    weight_categories.append(f"{oz}oz")
weight_categories.append("15.99oz")
# 1 lb and up (16oz to 400oz in 16oz/1lb increments)
for lb in range(1, 26):  # 1-25 lbs (16-400 oz)
    weight_categories.append(f"{lb*16}oz")

# Initialize the matrix
zones = [1, 2, 3, 4, 5, 6, 7, 8]
matrix_data = []

# Count shipments by billable weight and zone
for weight_cat in weight_categories:
    row = {'Weight': weight_cat}
    
    # Parse weight from category
    if weight_cat == "15.99oz":
        weight_val = 15.99
    else:
        weight_val = float(weight_cat.replace('oz', ''))
    
    for zone in zones:
        # Count packages in this weight and zone
        if weight_val == 15.99:
            count = len(df[(df['Billable Weight (oz)'] == 15.99) & (df['Zone'] == zone)])
        elif weight_val < 16:
            count = len(df[(df['Billable Weight (oz)'] == weight_val) & (df['Zone'] == zone)])
        else:
            # For weights >= 16oz, match the exact pound weight
            count = len(df[(df['Billable Weight (oz)'] == weight_val) & (df['Zone'] == zone)])
        
        row[f'Zone {zone}'] = count
    
    # Add total for this weight
    if weight_val == 15.99:
        row['Total'] = len(df[df['Billable Weight (oz)'] == 15.99])
    elif weight_val < 16:
        row['Total'] = len(df[df['Billable Weight (oz)'] == weight_val])
    else:
        row['Total'] = len(df[df['Billable Weight (oz)'] == weight_val])
    
    matrix_data.append(row)

# Create DataFrame
matrix_df = pd.DataFrame(matrix_data)

# Only include rows with at least 1 shipment
matrix_df_filtered = matrix_df[matrix_df['Total'] > 0].copy()

# Calculate zone totals
zone_totals = {'Weight': 'TOTAL'}
for zone in zones:
    zone_totals[f'Zone {zone}'] = matrix_df[f'Zone {zone}'].sum()
zone_totals['Total'] = matrix_df['Total'].sum()

# Append totals row
matrix_df_filtered = pd.concat([matrix_df_filtered, pd.DataFrame([zone_totals])], ignore_index=True)

print("=" * 100)
print("UPSTATE PREP - VOLUME DISTRIBUTION BY WEIGHT AND ZONE")
print("For Excel Copy/Paste into Tier Tool")
print("=" * 100)
print()

# Format for Excel copy/paste (tab-delimited)
print("Weight\tZone 1\tZone 2\tZone 3\tZone 4\tZone 5\tZone 6\tZone 7\tZone 8\tTotal")
print("-" * 80)

for _, row in matrix_df_filtered.iterrows():
    print(f"{row['Weight']}\t{int(row['Zone 1'])}\t{int(row['Zone 2'])}\t{int(row['Zone 3'])}\t{int(row['Zone 4'])}\t{int(row['Zone 5'])}\t{int(row['Zone 6'])}\t{int(row['Zone 7'])}\t{int(row['Zone 8'])}\t{int(row['Total'])}")

print()
print("=" * 100)
print("COMPLETE MATRIX INCLUDING ZEROS (All weights 1oz to 400oz)")
print("For Excel Copy/Paste - Tab-delimited")
print("=" * 100)
print()

# Print complete matrix with all weights
print("Weight\tZone 1\tZone 2\tZone 3\tZone 4\tZone 5\tZone 6\tZone 7\tZone 8\tTotal")
for _, row in matrix_df.iterrows():
    if row['Weight'] != 'TOTAL':  # Skip total row temporarily
        print(f"{row['Weight']}\t{int(row['Zone 1'])}\t{int(row['Zone 2'])}\t{int(row['Zone 3'])}\t{int(row['Zone 4'])}\t{int(row['Zone 5'])}\t{int(row['Zone 6'])}\t{int(row['Zone 7'])}\t{int(row['Zone 8'])}\t{int(row['Total'])}")

# Add totals at the end
print(f"TOTAL\t{int(zone_totals['Zone 1'])}\t{int(zone_totals['Zone 2'])}\t{int(zone_totals['Zone 3'])}\t{int(zone_totals['Zone 4'])}\t{int(zone_totals['Zone 5'])}\t{int(zone_totals['Zone 6'])}\t{int(zone_totals['Zone 7'])}\t{int(zone_totals['Zone 8'])}\t{int(zone_totals['Total'])}")

# Also save to CSV for easy import
matrix_df.to_csv('upstate_prep_volume_matrix.csv', index=False)
print()
print("Matrix also saved to: upstate_prep_volume_matrix.csv")

# Print summary statistics
print()
print("=" * 100)
print("SUMMARY STATISTICS")
print("=" * 100)
print(f"Total Packages: {int(zone_totals['Total'])}")
print()
print("Volume by Zone:")
for zone in zones:
    pct = (zone_totals[f'Zone {zone}'] / zone_totals['Total']) * 100
    print(f"  Zone {zone}: {int(zone_totals[f'Zone {zone}'])} packages ({pct:.1f}%)")

print()
print("Top Weight Categories:")
top_weights = matrix_df_filtered[matrix_df_filtered['Weight'] != 'TOTAL'].nlargest(10, 'Total')
for _, row in top_weights.iterrows():
    pct = (row['Total'] / zone_totals['Total']) * 100
    print(f"  {row['Weight']}: {int(row['Total'])} packages ({pct:.1f}%)")