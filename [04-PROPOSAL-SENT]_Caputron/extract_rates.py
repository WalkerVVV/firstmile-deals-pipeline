import pandas as pd
import numpy as np

# Read the Excel file
ground = pd.read_excel('Caputron Medical Products, LLC._FirstMile_Xparcel_07-24-25.xlsx', 
                       sheet_name='Xparcel Ground SLT_NATL', 
                       skiprows=5)
expedited = pd.read_excel('Caputron Medical Products, LLC._FirstMile_Xparcel_07-24-25.xlsx', 
                          sheet_name='Xparcel Expedited SLT_NATL', 
                          skiprows=5)

# Clean up column names
ground.columns = ['Weight'] + [f'Zone {i}' for i in range(1, 9)]
expedited.columns = ['Weight'] + [f'Zone {i}' for i in range(1, 9)]

# Key weights based on Caputron's distribution
key_weights_oz = [1, 8, 12, 15]  # Representative weights under 1 lb
key_weights_lb = [1, 2, 3, 4, 5]  # 1-5 lb range

print("=== FIRSTMILE XPARCEL GROUND (SELECT) RATES ===")
print("\nUnder 1 lb weights (73% of volume):")
print("Weight\tZone 2\tZone 3\tZone 4\tZone 5")
for w in key_weights_oz:
    row = ground[ground['Weight'] == w]
    if not row.empty:
        print(f"{w} oz\t${row.iloc[0]['Zone 2']}\t${row.iloc[0]['Zone 3']}\t${row.iloc[0]['Zone 4']}\t${row.iloc[0]['Zone 5']}")

print("\n1-5 lb weights (22% of volume):")
for w in key_weights_lb:
    # Look for pound notation
    row = ground[ground['Weight'] == f'{w} lb'] if f'{w} lb' in ground['Weight'].values else ground[ground['Weight'] == w * 16]
    if not row.empty:
        print(f"{w} lb\t${row.iloc[0]['Zone 2']}\t${row.iloc[0]['Zone 3']}\t${row.iloc[0]['Zone 4']}\t${row.iloc[0]['Zone 5']}")

# Calculate average rate for under 1 lb packages
under_1lb_rows = ground[ground['Weight'].apply(lambda x: isinstance(x, (int, float)) and x <= 15)]
if not under_1lb_rows.empty:
    avg_rate = under_1lb_rows[['Zone 2', 'Zone 3', 'Zone 4', 'Zone 5']].mean().mean()
    print(f"\nAverage rate for <1 lb packages across zones 2-5: ${avg_rate:.2f}")

# Get current rates from tier tool data if available
print("\n=== CURRENT CARRIER RATES (for comparison) ===")
print("Need to extract from current carrier invoices or tier tool data")