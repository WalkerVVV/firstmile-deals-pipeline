import pandas as pd
import numpy as np

# Load Loy shipping data
df = pd.read_csv('Order Export Loy.csv')

# Clean weight data
df['Weight (lb)'] = pd.to_numeric(df['Weight (lb)'], errors='coerce')

# Calculate billable weight in ounces
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

df['Billable_Oz'] = df['Weight (lb)'].apply(calculate_billable_oz)

# Analysis for 1-6 oz range
print("LOY SHIPMENTS: 1-6 OZ ANALYSIS")
print("="*60)

# Count shipments in 1-6 oz range
in_range_1_6oz = df[(df['Billable_Oz'] >= 1) & (df['Billable_Oz'] <= 6)]
total_valid_weight = df[df['Billable_Oz'] > 0]

# Detailed breakdown by ounce
print("\nDETAILED BREAKDOWN BY OUNCE (1-6 oz):")
print("-"*40)
print(f"{'Weight':<10} {'Count':>8} {'% of Total':>12} {'Cumulative %':>14}")
print("-"*40)

cumulative_count = 0
total_count = len(total_valid_weight)

for oz in range(1, 7):
    count = len(df[df['Billable_Oz'] == oz])
    cumulative_count += count
    pct = (count / total_count) * 100
    cum_pct = (cumulative_count / total_count) * 100
    print(f"{oz}oz{'':<7} {count:>8} {pct:>11.1f}% {cum_pct:>13.1f}%")

print("-"*40)
print(f"{'TOTAL 1-6oz':<10} {len(in_range_1_6oz):>8} {(len(in_range_1_6oz)/total_count)*100:>11.1f}%")

# Summary statistics
print("\n" + "="*60)
print("SUMMARY STATISTICS:")
print("-"*40)

print(f"Total shipments with valid weight: {total_count:,}")
print(f"Shipments 1-6 oz: {len(in_range_1_6oz):,}")
print(f"Percentage 1-6 oz: {(len(in_range_1_6oz)/total_count)*100:.2f}%")

# Cost impact analysis
print("\n" + "="*60)
print("COST IMPACT ANALYSIS:")
print("-"*40)

# Using the rates we know: $3.20-$3.60 for 1-6 oz
avg_rate_1_6oz = 3.30  # Average of provided rates
monthly_volume_1_6oz = len(in_range_1_6oz)
monthly_spend_1_6oz = monthly_volume_1_6oz * avg_rate_1_6oz

print(f"Monthly volume (1-6 oz): {monthly_volume_1_6oz:,} packages")
print(f"Average rate (1-6 oz): ${avg_rate_1_6oz:.2f}")
print(f"Monthly spend (1-6 oz): ${monthly_spend_1_6oz:,.2f}")
print(f"Annual projection (1-6 oz): ${monthly_spend_1_6oz * 12:,.2f}")

# Compare to total
print("\n" + "-"*40)
print("AS PERCENTAGE OF TOTAL SHIPPING:")
print(f"Volume share: {(len(in_range_1_6oz)/total_count)*100:.1f}% of packages are 1-6 oz")
print(f"This represents your rate card 'sweet spot' with known pricing")

# Additional insights
print("\n" + "="*60)
print("KEY INSIGHTS:")
print("-"*40)

# Most common weight in range
weight_counts = df[df['Billable_Oz'].between(1, 6)]['Billable_Oz'].value_counts()
if not weight_counts.empty:
    most_common = weight_counts.index[0]
    most_common_count = weight_counts.iloc[0]
    print(f"• Most common weight in 1-6 oz range: {most_common:.0f}oz ({most_common_count:,} packages)")

# Zone distribution for 1-6 oz packages
df['Zone_Estimate'] = df['Zip'].astype(str).str[0]
zone_dist = in_range_1_6oz['Zone_Estimate'].value_counts().head(5)
print(f"\n• Top destination zones for 1-6 oz packages:")
for zone, count in zone_dist.items():
    print(f"  Zone {zone}: {count:,} packages ({(count/len(in_range_1_6oz))*100:.1f}%)")

print("\n" + "="*60)