import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('Order Export Loy.csv')

# Clean weight data
df['Weight (lb)'] = pd.to_numeric(df['Weight (lb)'], errors='coerce')

# Function to calculate billable weight in ounces
def calculate_billable_oz(actual_weight_lb):
    if pd.isna(actual_weight_lb) or actual_weight_lb <= 0:
        return 0
    
    actual_oz = actual_weight_lb * 16
    
    if actual_oz < 16:
        # Under 1 lb: round up to next whole oz, max 15.99
        billable_oz = min(15.99, np.ceil(actual_oz))
    else:
        # 1 lb and over: round up to next whole pound, convert to oz
        billable_lb = np.ceil(actual_weight_lb)
        billable_oz = billable_lb * 16
    
    return billable_oz

# Calculate billable weight in ounces
df['Billable_Oz'] = df['Weight (lb)'].apply(calculate_billable_oz)

# Map service levels based on shipping method
def map_service_level(row):
    method = str(row['Shipping Method']).lower() if pd.notna(row['Shipping Method']) else ''
    carrier = str(row['Carrier']).lower() if pd.notna(row['Carrier']) else ''
    
    # Priority indicators
    if 'priority' in method or 'express' in method or '2day' in method or '2 day' in method:
        return 'Priority'
    # Expedited indicators
    elif 'expedited' in method or 'surepost' in method:
        return 'Expedited'
    # Ground is default
    else:
        return 'Ground'

df['Service_Level'] = df.apply(map_service_level, axis=1)

# Create the 41 weight buckets (in ounces)
weight_buckets = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15.99,
    16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208,
    224, 240, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400
]

# Initialize results
priority_volumes = []
expedited_volumes = []
ground_volumes = []

# Count volumes for each weight bucket
for weight_oz in weight_buckets:
    if weight_oz <= 15:
        # For 1-15 oz, match exact ounce
        mask = (df['Billable_Oz'] == weight_oz)
    elif weight_oz == 15.99:
        # Special case for 15.99 oz
        mask = (df['Billable_Oz'] == 15.99)
    else:
        # For pound weights (16, 32, 48...), match exact ounce value
        mask = (df['Billable_Oz'] == weight_oz)
    
    priority_count = len(df[mask & (df['Service_Level'] == 'Priority')])
    expedited_count = len(df[mask & (df['Service_Level'] == 'Expedited')])
    ground_count = len(df[mask & (df['Service_Level'] == 'Ground')])
    
    priority_volumes.append(priority_count)
    expedited_volumes.append(expedited_count)
    ground_volumes.append(ground_count)

# Add totals
priority_volumes.append(sum(priority_volumes))
expedited_volumes.append(sum(expedited_volumes))
ground_volumes.append(sum(ground_volumes))

# Print summary statistics first
print("SHIPPING VOLUME ANALYSIS - LOY\n")
print("="*50)
print(f"Total Records: {len(df)}")
print(f"Records with valid weight: {df['Weight (lb)'].notna().sum()}")
print(f"\nService Level Distribution:")
print(df['Service_Level'].value_counts())
print("\n" + "="*50)

# Print the volume matrix for verification
print("\nVOLUME MATRIX BY WEIGHT AND SERVICE LEVEL:")
print("-"*50)
print(f"{'Weight':<10} {'Priority':>10} {'Expedited':>10} {'Ground':>10}")
print("-"*50)

for i, weight in enumerate(weight_buckets + ['Total']):
    if i < len(weight_buckets):
        weight_label = f"{weight}oz" if weight < 16 or weight == 15.99 else f"{weight/16:.0f}lb"
        print(f"{weight_label:<10} {priority_volumes[i]:>10} {expedited_volumes[i]:>10} {ground_volumes[i]:>10}")
    else:
        print(f"{'Total':<10} {priority_volumes[i]:>10} {expedited_volumes[i]:>10} {ground_volumes[i]:>10}")

print("\n" + "="*50)
print("\nEXCEL PASTE FORMAT (Copy each column separately):\n")

# Output for Excel paste
print("PRIORITY COLUMN:")
print("-"*20)
for vol in priority_volumes:
    print(vol)

print("\nEXPEDITED COLUMN:")
print("-"*20)
for vol in expedited_volumes:
    print(vol)

print("\nGROUND COLUMN:")
print("-"*20)
for vol in ground_volumes:
    print(vol)

# Additional analysis
print("\n" + "="*50)
print("WEIGHT DISTRIBUTION INSIGHTS:")
print("-"*50)

# Calculate percentages for non-zero weights
total_packages = len(df[df['Weight (lb)'].notna()])
under_1lb = len(df[df['Billable_Oz'] < 16])
exactly_1lb = len(df[df['Billable_Oz'] == 16])
under_2lb = len(df[df['Billable_Oz'] <= 32])
over_5lb = len(df[df['Billable_Oz'] > 80])

print(f"Under 1 lb: {under_1lb} packages ({under_1lb/total_packages*100:.1f}%)")
print(f"Exactly 1 lb (16 oz): {exactly_1lb} packages ({exactly_1lb/total_packages*100:.1f}%)")
print(f"Under 2 lbs: {under_2lb} packages ({under_2lb/total_packages*100:.1f}%)")
print(f"Over 5 lbs: {over_5lb} packages ({over_5lb/total_packages*100:.1f}%)")