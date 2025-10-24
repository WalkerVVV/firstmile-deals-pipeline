import pandas as pd
import numpy as np

# Parse the sample rates to determine zones
sample_data = """Origin,Destination,Weight_lb,Rate
07104,17602,0.06,3.2
07104,20723,0.06,3.2
07104,07036,0.06,3.2
07104,33189,0.06,3.2
07104,10952,0.06,3.2
07104,07110,0.06,3.2
07104,97219,0.06,3.4
07104,01867,0.06,3.2
07104,89436,0.06,3.4
07104,10977,0.06,3.2
07104,10977,0.06,3.2
07104,77375,0.06,3.2
07104,08755,0.06,3.2
07104,60185,0.06,3.2
07104,27265,0.3675,3.2
07104,93923,0.3675,3.6
07104,91042,0.3675,3.6
07104,80123,0.3675,3.4
07104,75244,0.3675,3.2
07104,02893,0.3675,3.2
07104,20814,0.3675,3.2
07104,89074,0.3675,3.4
07104,30188,0.3675,3.2
07104,28078,0.3675,3.2
07104,83646,0.3675,3.6
07104,92346,0.3675,3.6
07104,46410,0.3675,3.2
07104,63123,0.3675,3.2"""

# Zone mapping based on ZIP code prefixes (from Newark, NJ 07104)
# This is a simplified zone mapping
def get_zone(origin, dest):
    """Estimate zone based on ZIP code distance"""
    origin_prefix = str(origin)[:3]
    dest_prefix = str(dest)[:3]
    
    # Zone 1: Same state/nearby NJ (070-089)
    if dest_prefix in ['070', '071', '072', '073', '074', '075', '076', '077', '078', '079', '080', '081', '082', '083', '084', '085', '086', '087', '088', '089']:
        return 1
    # Zone 2: NY, PA, CT, MA (100-149, 150-199, 060-069, 010-029)
    elif dest_prefix[0] == '1' or (dest_prefix[:2] in ['06', '01', '02']):
        return 2
    # Zone 3: MD, VA, NC, DE (200-289)
    elif dest_prefix[0] == '2':
        return 3
    # Zone 4: Southeast (300-399)
    elif dest_prefix[0] == '3':
        return 4
    # Zone 5: Midwest (400-599)
    elif dest_prefix[0] in ['4', '5']:
        return 5
    # Zone 6: Central (600-799)
    elif dest_prefix[0] in ['6', '7']:
        return 6
    # Zone 7: Mountain (800-899)
    elif dest_prefix[0] == '8':
        return 7
    # Zone 8: West Coast (900-999)
    elif dest_prefix[0] == '9':
        return 8
    else:
        return 5  # Default to Zone 5

# Analyze the sample data
from io import StringIO
df = pd.read_csv(StringIO(sample_data))

# Add zones
df['Zone'] = df['Destination'].apply(lambda x: get_zone(7104, x))

# Convert weight to ounces
df['Weight_oz'] = df['Weight_lb'] * 16

print("GROUND SHIPPING PRICING MATRIX")
print("="*100)
print("Origin: Newark, NJ (07104)")
print("Service: Ground")
print("\nSample Rate Analysis:")
print("-"*50)

# Show rates by weight and zone from sample
for weight in df['Weight_oz'].unique():
    weight_data = df[df['Weight_oz'] == weight]
    print(f"\nWeight: {weight:.1f} oz ({weight/16:.4f} lb)")
    zone_rates = weight_data.groupby('Zone')['Rate'].first()
    for zone, rate in zone_rates.items():
        print(f"  Zone {zone}: ${rate:.2f}")

# Create the full pricing matrix
print("\n" + "="*100)
print("COMPLETE PRICING MATRIX")
print("-"*100)

# Define all weights
weights_oz = list(range(1, 16)) + [15.99] + list(range(16, 401, 16))
weight_labels = []
for w in weights_oz:
    if w < 16:
        weight_labels.append(f"{w:.0f}oz" if w != 15.99 else "15.99oz")
    elif w == 16:
        weight_labels.append("1lb")
    else:
        weight_labels.append(f"{w//16}lb")

# Create matrix
zones = list(range(1, 9))
matrix = []

for i, weight_oz in enumerate(weights_oz):
    row = {'Weight': weight_labels[i]}
    for zone in zones:
        # Check if we have this rate in our sample
        if weight_oz <= 1:  # 1 oz
            if zone <= 7:
                row[f'Zone {zone}'] = '$3.20'
            else:
                row[f'Zone {zone}'] = '$3.40'
        elif weight_oz <= 6:  # 2-6 oz
            if zone <= 6:
                row[f'Zone {zone}'] = '$3.20'
            elif zone == 7:
                row[f'Zone {zone}'] = '$3.40'
            else:
                row[f'Zone {zone}'] = '$3.60'
        else:
            # We don't have rates for these
            row[f'Zone {zone}'] = 'X'
    matrix.append(row)

# Create DataFrame
matrix_df = pd.DataFrame(matrix)

# Print the matrix in a formatted way
print("\n| Weight     | Zone 1 | Zone 2 | Zone 3 | Zone 4 | Zone 5 | Zone 6 | Zone 7 | Zone 8 |")
print("|------------|--------|--------|--------|--------|--------|--------|--------|--------|")

for _, row in matrix_df.iterrows():
    weight = row['Weight'].ljust(10)
    z1 = row['Zone 1'].center(6)
    z2 = row['Zone 2'].center(6)
    z3 = row['Zone 3'].center(6)
    z4 = row['Zone 4'].center(6)
    z5 = row['Zone 5'].center(6)
    z6 = row['Zone 6'].center(6)
    z7 = row['Zone 7'].center(6)
    z8 = row['Zone 8'].center(6)
    print(f"| {weight} | {z1} | {z2} | {z3} | {z4} | {z5} | {z6} | {z7} | {z8} |")
    
    # Add separator after 15.99oz
    if row['Weight'] == '15.99oz':
        print("|------------|--------|--------|--------|--------|--------|--------|--------|--------|")

# Save to CSV for Excel
matrix_df.to_csv('loy_pricing_matrix.csv', index=False)
print("\n" + "="*100)
print("Matrix saved to 'loy_pricing_matrix.csv'")
print("\nNOTE: 'X' indicates rates not provided in sample data")
print("Rates shown are based on limited sample of 1oz and 6oz packages only")