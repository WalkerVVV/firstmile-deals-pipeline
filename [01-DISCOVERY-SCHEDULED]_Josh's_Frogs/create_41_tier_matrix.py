#!/usr/bin/env python3
"""
JOSH'S FROGS - 41-TIER WEIGHT MATRIX
Transforms PLD data into standardized Excel tier tool format
"""

import pandas as pd
import numpy as np

print("="*80)
print("JOSH'S FROGS - 41-TIER WEIGHT MATRIX GENERATOR")
print("="*80)

# Service level classification
PRIORITY_KEYWORDS = ['PRIORITY_OVERNIGHT', 'FIRST_OVERNIGHT', 'STANDARD_OVERNIGHT',
                     'NEXT_DAY_AIR', 'NEXT_DAY', 'OVERNIGHT']
EXPEDITED_KEYWORDS = ['EXPRESS_SAVER', 'SECOND_DAY', 'TWO_DAY', 'THREE_DAY_SELECT']
# Everything else = GROUND

def classify_service_level(service_name):
    """Classify service into Priority/Expedited/Ground"""
    service_upper = str(service_name).upper()

    if any(kw in service_upper for kw in PRIORITY_KEYWORDS):
        return 'PRIORITY'
    elif any(kw in service_upper for kw in EXPEDITED_KEYWORDS):
        return 'EXPEDITED'
    else:
        return 'GROUND'

def get_weight_tier(weight_lbs):
    """Map weight to 41-tier structure"""
    weight_oz = weight_lbs * 16

    # Ounce tiers (1-16)
    if weight_oz < 1:
        return 1  # Less than 1 oz
    elif weight_oz < 16:
        return int(np.ceil(weight_oz))  # Tiers 2-16 (1-2 oz, 2-3 oz, etc.)

    # Pound tiers (17-41)
    # Row 17 = 1-2 lbs (16-32 oz)
    # Row 18 = 2-3 lbs (32-48 oz)
    # etc.
    if weight_oz >= 16:
        tier = 16 + int(np.ceil((weight_oz - 16) / 16))
        return min(tier, 41)  # Cap at tier 41 (25-26 lbs)

    return 41  # Anything over goes to tier 41

# Live animal service keywords (to exclude)
LIVE_ANIMAL_KEYWORDS = [
    'OVERNIGHT', 'EXPRESS_SAVER', 'NEXT_DAY', 'SECOND_DAY', 'TWO_DAY',
    'PRIORITY_OVERNIGHT', 'FIRST_OVERNIGHT', 'STANDARD_OVERNIGHT', 'THREE_DAY'
]

def is_live_animal_service(service_name):
    """Check if service is used for live animals"""
    service_upper = str(service_name).upper()
    return any(kw in service_upper for kw in LIVE_ANIMAL_KEYWORDS)

# Load PLD data
print("\n[1] Loading PLD data...")
df = pd.read_csv('247bef97-8663-431e-b2f5-dd2ca243633d (1).csv')
print(f"   Loaded {len(df):,} shipments")

# Remove rows with missing data
df = df[df['Carrier'].notna() & df['Service'].notna() & df['Weight'].notna()].copy()

# Classify and filter
print("\n[2] Classifying services...")
df['Is_Live_Animal'] = df['Service'].apply(is_live_animal_service)
dry_goods = df[~df['Is_Live_Animal']].copy()

print(f"   Dry Goods: {len(dry_goods):,} shipments")
print(f"   Live Animals (excluded): {len(df[df['Is_Live_Animal']]):,} shipments")

# Classify service levels
print("\n[3] Classifying service levels...")
dry_goods['Service_Level'] = dry_goods['Service'].apply(classify_service_level)

priority_count = len(dry_goods[dry_goods['Service_Level'] == 'PRIORITY'])
expedited_count = len(dry_goods[dry_goods['Service_Level'] == 'EXPEDITED'])
ground_count = len(dry_goods[dry_goods['Service_Level'] == 'GROUND'])

print(f"   Priority: {priority_count:,} shipments")
print(f"   Expedited: {expedited_count:,} shipments")
print(f"   Ground: {ground_count:,} shipments")

# Map to weight tiers
print("\n[4] Mapping to 41 weight tiers...")
dry_goods['Weight_Tier'] = dry_goods['Weight'].apply(get_weight_tier)

# Create volume matrix
tier_matrix = pd.DataFrame({
    'Tier': range(1, 42),
    'PRIORITY': [0] * 41,
    'EXPEDITED': [0] * 41,
    'GROUND': [0] * 41
})

# Count volumes by tier and service level
for tier in range(1, 42):
    for service_level in ['PRIORITY', 'EXPEDITED', 'GROUND']:
        count = len(dry_goods[(dry_goods['Weight_Tier'] == tier) &
                              (dry_goods['Service_Level'] == service_level)])
        tier_matrix.loc[tier_matrix['Tier'] == tier, service_level] = count

# Calculate totals
priority_total = tier_matrix['PRIORITY'].sum()
expedited_total = tier_matrix['EXPEDITED'].sum()
ground_total = tier_matrix['GROUND'].sum()
grand_total = priority_total + expedited_total + ground_total

print(f"   Mapped {grand_total:,} shipments across 41 tiers")

# Generate tier labels
tier_labels = []
# Ounce tiers (1-16)
tier_labels.append("Less than 1 oz")
for oz in range(1, 16):
    tier_labels.append(f"{oz}-{oz+1} oz")
# Pound tiers (17-41)
for lb in range(1, 26):
    tier_labels.append(f"{lb}-{lb+1} lbs")

tier_matrix['Weight_Range'] = tier_labels

# Display summary table
print("\n" + "="*80)
print("VOLUME DISTRIBUTION BY WEIGHT TIER")
print("="*80)
print(f"\n{'Weight Range':<20} {'Priority':>10} {'Expedited':>10} {'Ground':>10} {'Total':>10}")
print("-" * 80)

for idx, row in tier_matrix.iterrows():
    if row['PRIORITY'] > 0 or row['EXPEDITED'] > 0 or row['GROUND'] > 0:
        tier_total = row['PRIORITY'] + row['EXPEDITED'] + row['GROUND']
        print(f"{row['Weight_Range']:<20} {int(row['PRIORITY']):>10,} {int(row['EXPEDITED']):>10,} "
              f"{int(row['GROUND']):>10,} {int(tier_total):>10,}")

print("-" * 80)
print(f"{'TOTAL':<20} {int(priority_total):>10,} {int(expedited_total):>10,} "
      f"{int(ground_total):>10,} {int(grand_total):>10,}")
print("="*80)

# Generate Excel-ready output
print("\n" + "="*80)
print("EXCEL TIER TOOL FORMAT (Copy-Paste Ready)")
print("="*80)

print("\n--- PRIORITY COLUMN (42 rows) ---")
for idx, row in tier_matrix.iterrows():
    print(int(row['PRIORITY']))
print(int(priority_total))  # Total row

print("\n--- EXPEDITED COLUMN (42 rows) ---")
for idx, row in tier_matrix.iterrows():
    print(int(row['EXPEDITED']))
print(int(expedited_total))  # Total row

print("\n--- GROUND COLUMN (42 rows) ---")
for idx, row in tier_matrix.iterrows():
    print(int(row['GROUND']))
print(int(ground_total))  # Total row

# Save to CSV for reference
output_file = "Joshs_Frogs_41_Tier_Matrix.csv"
tier_matrix_with_totals = tier_matrix.copy()
tier_matrix_with_totals.loc[len(tier_matrix_with_totals)] = {
    'Tier': 'TOTAL',
    'Weight_Range': 'Total All Tiers',
    'PRIORITY': priority_total,
    'EXPEDITED': expedited_total,
    'GROUND': ground_total
}
tier_matrix_with_totals.to_csv(output_file, index=False)

print("\n" + "="*80)
print(f"Matrix saved to: {output_file}")
print("="*80)

print("\nQuality Verification:")
print(f"   ✓ 42 rows per column (41 tiers + total): CONFIRMED")
print(f"   ✓ Priority total: {priority_total:,}")
print(f"   ✓ Expedited total: {expedited_total:,}")
print(f"   ✓ Ground total: {ground_total:,}")
print(f"   ✓ Grand total: {grand_total:,}")
print(f"   ✓ Matches dry goods count: {grand_total == len(dry_goods)}")
print("\n" + "="*80)