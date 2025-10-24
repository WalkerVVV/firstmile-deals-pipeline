import pandas as pd
import numpy as np

# Read the CSV
df = pd.read_csv("jmgroup30daydata.csv")

print("="*60)
print("EXPANDED WEIGHT DISTRIBUTION ANALYSIS")
print("="*60)
print()

# Convert Weight to numeric (in ounces)
df["Weight_Numeric"] = pd.to_numeric(df["Weight"], errors="coerce")
df["Shipping_Cost"] = pd.to_numeric(df["Amount - Shipping Cost"], errors="coerce")

# Detailed weight distribution
print("DETAILED WEIGHT BREAKDOWN:")
print("-"*40)

# Under 1 lb breakdown
under_16oz = df[df["Weight_Numeric"] <= 16]
oz_1_4 = df[(df["Weight_Numeric"] >= 1) & (df["Weight_Numeric"] <= 4)]
oz_4_8 = df[(df["Weight_Numeric"] > 4) & (df["Weight_Numeric"] <= 8)]
oz_8_12 = df[(df["Weight_Numeric"] > 8) & (df["Weight_Numeric"] <= 12)]
oz_12_16 = df[(df["Weight_Numeric"] > 12) & (df["Weight_Numeric"] <= 16)]

print("Under 1 lb Breakdown:")
print(f"  1-4 oz: {len(oz_1_4):,} ({(len(oz_1_4)/len(df))*100:.1f}%) - Avg cost: ${oz_1_4['Shipping_Cost'].mean():.2f}")
print(f"  4-8 oz: {len(oz_4_8):,} ({(len(oz_4_8)/len(df))*100:.1f}%) - Avg cost: ${oz_4_8['Shipping_Cost'].mean():.2f}")
print(f"  8-12 oz: {len(oz_8_12):,} ({(len(oz_8_12)/len(df))*100:.1f}%) - Avg cost: ${oz_8_12['Shipping_Cost'].mean():.2f}")
print(f"  12-16 oz: {len(oz_12_16):,} ({(len(oz_12_16)/len(df))*100:.1f}%) - Avg cost: ${oz_12_16['Shipping_Cost'].mean():.2f}")
print(f"  Total Under 1 lb: {len(under_16oz):,} ({(len(under_16oz)/len(df))*100:.1f}%)")
print()

# 1-5 lbs breakdown by individual pound
lb1_2 = df[(df["Weight_Numeric"] > 16) & (df["Weight_Numeric"] <= 32)]
lb2_3 = df[(df["Weight_Numeric"] > 32) & (df["Weight_Numeric"] <= 48)]
lb3_4 = df[(df["Weight_Numeric"] > 48) & (df["Weight_Numeric"] <= 64)]
lb4_5 = df[(df["Weight_Numeric"] > 64) & (df["Weight_Numeric"] <= 80)]

print("1-5 lbs Breakdown by Pound:")
print(f"  1-2 lbs (16-32 oz): {len(lb1_2):,} ({(len(lb1_2)/len(df))*100:.1f}%) - Avg cost: ${lb1_2['Shipping_Cost'].mean():.2f}")
print(f"  2-3 lbs (32-48 oz): {len(lb2_3):,} ({(len(lb2_3)/len(df))*100:.1f}%) - Avg cost: ${lb2_3['Shipping_Cost'].mean():.2f}")
print(f"  3-4 lbs (48-64 oz): {len(lb3_4):,} ({(len(lb3_4)/len(df))*100:.1f}%) - Avg cost: ${lb3_4['Shipping_Cost'].mean():.2f}")
print(f"  4-5 lbs (64-80 oz): {len(lb4_5):,} ({(len(lb4_5)/len(df))*100:.1f}%) - Avg cost: ${lb4_5['Shipping_Cost'].mean():.2f}")
print(f"  Total 1-5 lbs: {len(lb1_2) + len(lb2_3) + len(lb3_4) + len(lb4_5):,} ({((len(lb1_2) + len(lb2_3) + len(lb3_4) + len(lb4_5))/len(df))*100:.1f}%)")
print()

# Over 5 lbs
lb5_10 = df[(df["Weight_Numeric"] > 80) & (df["Weight_Numeric"] <= 160)]
over_10lb = df[df["Weight_Numeric"] > 160]

print("Over 5 lbs:")
print(f"  5-10 lbs: {len(lb5_10):,} ({(len(lb5_10)/len(df))*100:.1f}%) - Avg cost: ${lb5_10['Shipping_Cost'].mean():.2f}")
print(f"  Over 10 lbs: {len(over_10lb):,} ({(len(over_10lb)/len(df))*100:.1f}%) - Avg cost: ${over_10lb['Shipping_Cost'].mean():.2f}")
print()

# Create summary table data
print("WEIGHT DISTRIBUTION SUMMARY TABLE:")
print("-"*40)
weight_ranges = [
    ("1-4 oz", oz_1_4),
    ("4-8 oz", oz_4_8),
    ("8-12 oz", oz_8_12),
    ("12-16 oz", oz_12_16),
    ("1-2 lbs", lb1_2),
    ("2-3 lbs", lb2_3),
    ("3-4 lbs", lb3_4),
    ("4-5 lbs", lb4_5),
    ("5-10 lbs", lb5_10),
    ("10+ lbs", over_10lb)
]

total_cost = df["Shipping_Cost"].sum()
print(f"{'Weight Range':<15} {'Packages':>10} {'% Total':>10} {'Avg Cost':>12} {'Total Cost':>15} {'% Spend':>10}")
print("-"*85)

for range_name, range_df in weight_ranges:
    count = len(range_df)
    pct_total = (count/len(df))*100 if len(df) > 0 else 0
    avg_cost = range_df["Shipping_Cost"].mean() if len(range_df) > 0 else 0
    range_total = range_df["Shipping_Cost"].sum()
    pct_spend = (range_total/total_cost)*100 if total_cost > 0 else 0
    
    print(f"{range_name:<15} {count:>10,} {pct_total:>10.1f}% ${avg_cost:>11.2f} ${range_total:>14,.2f} {pct_spend:>10.1f}%")

print()
print(f"{'TOTAL':<15} {len(df):>10,} {100.0:>10.1f}% ${df['Shipping_Cost'].mean():>11.2f} ${total_cost:>14,.2f} {100.0:>10.1f}%")