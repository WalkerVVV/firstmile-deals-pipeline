import pandas as pd
import numpy as np
import math

# Read the CSV
df = pd.read_csv("jmgroup30daydata.csv")

print("="*60)
print("BILLABLE WEIGHT DISTRIBUTION ANALYSIS")
print("="*60)
print("(All weights rounded up for billing purposes)")
print()

# Convert Weight to numeric (in ounces)
df["Weight_Numeric"] = pd.to_numeric(df["Weight"], errors="coerce")
df["Shipping_Cost"] = pd.to_numeric(df["Amount - Shipping Cost"], errors="coerce")

# Calculate billable weight
def calculate_billable_weight(weight_oz):
    if pd.isna(weight_oz):
        return np.nan
    if weight_oz < 16:
        # Under 1 lb: round up to next whole ounce, max 15.99
        rounded = math.ceil(weight_oz)
        if rounded >= 16:
            return 15.99
        return rounded
    elif weight_oz == 16:
        # Exactly 16 oz = 1 lb
        return 16
    else:
        # Over 1 lb: round up to next whole pound (16 oz increments)
        return math.ceil(weight_oz / 16) * 16

df["Billable_Weight"] = df["Weight_Numeric"].apply(calculate_billable_weight)

# Detailed weight distribution using billable weights
print("DETAILED BILLABLE WEIGHT BREAKDOWN:")
print("-"*40)

# Under 1 lb breakdown (using billable weights)
oz_1_4 = df[(df["Billable_Weight"] >= 1) & (df["Billable_Weight"] <= 4)]
oz_5_8 = df[(df["Billable_Weight"] >= 5) & (df["Billable_Weight"] <= 8)]
oz_9_12 = df[(df["Billable_Weight"] >= 9) & (df["Billable_Weight"] <= 12)]
oz_13_15 = df[(df["Billable_Weight"] >= 13) & (df["Billable_Weight"] <= 15)]
oz_15_99 = df[df["Billable_Weight"] == 15.99]
oz_16_exact = df[df["Billable_Weight"] == 16]
under_16oz = df[df["Billable_Weight"] < 16]

print("Under 1 lb Breakdown (Billable Weight):")
print(f"  1-4 oz: {len(oz_1_4):,} ({(len(oz_1_4)/len(df))*100:.1f}%) - Avg cost: ${oz_1_4['Shipping_Cost'].mean():.2f}")
print(f"  5-8 oz: {len(oz_5_8):,} ({(len(oz_5_8)/len(df))*100:.1f}%) - Avg cost: ${oz_5_8['Shipping_Cost'].mean():.2f}")
print(f"  9-12 oz: {len(oz_9_12):,} ({(len(oz_9_12)/len(df))*100:.1f}%) - Avg cost: ${oz_9_12['Shipping_Cost'].mean():.2f}")
print(f"  13-15 oz: {len(oz_13_15):,} ({(len(oz_13_15)/len(df))*100:.1f}%) - Avg cost: ${oz_13_15['Shipping_Cost'].mean():.2f}")
print(f"  15.99 oz (15.1-15.99): {len(oz_15_99):,} ({(len(oz_15_99)/len(df))*100:.1f}%) - Avg cost: ${oz_15_99['Shipping_Cost'].mean():.2f}" if len(oz_15_99) > 0 else "  15.99 oz: 0 (0.0%)")
print(f"  16 oz exactly (1 lb): {len(oz_16_exact):,} ({(len(oz_16_exact)/len(df))*100:.1f}%) - Avg cost: ${oz_16_exact['Shipping_Cost'].mean():.2f}" if len(oz_16_exact) > 0 else "  16 oz exactly: 0 (0.0%)")
print(f"  Total Under 1 lb (<16 oz): {len(under_16oz):,} ({(len(under_16oz)/len(df))*100:.1f}%)")
print(f"  Total 16 oz exactly: {len(oz_16_exact):,} ({(len(oz_16_exact)/len(df))*100:.1f}%)")
print()

# 1-5 lbs breakdown by billable pound
lb2 = df[df["Billable_Weight"] == 32]  # 2 lbs billable
lb3 = df[df["Billable_Weight"] == 48]  # 3 lbs billable
lb4 = df[df["Billable_Weight"] == 64]  # 4 lbs billable
lb5 = df[df["Billable_Weight"] == 80]  # 5 lbs billable
lb1_5_total = df[(df["Billable_Weight"] > 16) & (df["Billable_Weight"] <= 80)]

print("1-5 lbs Breakdown by Billable Pound:")
print(f"  2 lbs billable (16.1-32 oz actual): {len(lb2):,} ({(len(lb2)/len(df))*100:.1f}%) - Avg cost: ${lb2['Shipping_Cost'].mean():.2f}")
print(f"  3 lbs billable (32.1-48 oz actual): {len(lb3):,} ({(len(lb3)/len(df))*100:.1f}%) - Avg cost: ${lb3['Shipping_Cost'].mean():.2f}")
print(f"  4 lbs billable (48.1-64 oz actual): {len(lb4):,} ({(len(lb4)/len(df))*100:.1f}%) - Avg cost: ${lb4['Shipping_Cost'].mean():.2f}")
print(f"  5 lbs billable (64.1-80 oz actual): {len(lb5):,} ({(len(lb5)/len(df))*100:.1f}%) - Avg cost: ${lb5['Shipping_Cost'].mean():.2f}")
print(f"  Total 1-5 lbs billable: {len(lb1_5_total):,} ({(len(lb1_5_total)/len(df))*100:.1f}%)")
print()

# Over 5 lbs
lb6_10 = df[(df["Billable_Weight"] > 80) & (df["Billable_Weight"] <= 160)]
over_10lb = df[df["Billable_Weight"] > 160]

print("Over 5 lbs Billable:")
print(f"  6-10 lbs billable: {len(lb6_10):,} ({(len(lb6_10)/len(df))*100:.1f}%) - Avg cost: ${lb6_10['Shipping_Cost'].mean():.2f}")
print(f"  Over 10 lbs billable: {len(over_10lb):,} ({(len(over_10lb)/len(df))*100:.1f}%) - Avg cost: ${over_10lb['Shipping_Cost'].mean():.2f}")
print()

# Create summary table with billable weights
print("BILLABLE WEIGHT DISTRIBUTION SUMMARY TABLE:")
print("-"*60)

# Define billable weight ranges for summary
billable_ranges = [
    ("1-4 oz", oz_1_4),
    ("5-8 oz", oz_5_8),
    ("9-12 oz", oz_9_12),
    ("13-15 oz", oz_13_15),
    ("15.99 oz", oz_15_99),
    ("16 oz (1 lb)", oz_16_exact),
    ("2 lbs", lb2),
    ("3 lbs", lb3),
    ("4 lbs", lb4),
    ("5 lbs", lb5),
    ("6-10 lbs", lb6_10),
    ("10+ lbs", over_10lb)
]

total_cost = df["Shipping_Cost"].sum()
print(f"{'Billable Weight':<15} {'Packages':>10} {'% Total':>10} {'Avg Cost':>12} {'Total Cost':>15} {'% Spend':>10}")
print("-"*85)

for range_name, range_df in billable_ranges:
    count = len(range_df)
    pct_total = (count/len(df))*100 if len(df) > 0 else 0
    avg_cost = range_df["Shipping_Cost"].mean() if len(range_df) > 0 else 0
    range_total = range_df["Shipping_Cost"].sum()
    pct_spend = (range_total/total_cost)*100 if total_cost > 0 else 0
    
    print(f"{range_name:<15} {count:>10,} {pct_total:>10.1f}% ${avg_cost:>11.2f} ${range_total:>14,.2f} {pct_spend:>10.1f}%")

print()
print(f"{'TOTAL':<15} {len(df):>10,} {100.0:>10.1f}% ${df['Shipping_Cost'].mean():>11.2f} ${total_cost:>14,.2f} {100.0:>10.1f}%")
print()

# Show actual vs billable weight comparison
print("ACTUAL VS BILLABLE WEIGHT COMPARISON:")
print("-"*40)
valid_weights = df[df["Billable_Weight"].notna()]
print(f"Average Actual Weight: {valid_weights['Weight_Numeric'].mean():.1f} oz")
print(f"Average Billable Weight: {valid_weights['Billable_Weight'].mean():.1f} oz")
print(f"Average Weight Difference: {(valid_weights['Billable_Weight'] - valid_weights['Weight_Numeric']).mean():.1f} oz")
print(f"Total Billable Ounces Lost to Rounding: {(valid_weights['Billable_Weight'] - valid_weights['Weight_Numeric']).sum():.0f} oz")