import pandas as pd
import numpy as np

# Load the data
df = pd.read_excel('DYLN Fulfillment - Shipments.xlsx')

print("="*60)
print("CHECKING FOR REVENUE/COST DATA")
print("="*60)

# Check all columns
print("\nAvailable columns:")
for col in df.columns:
    print(f"  - {col}")

# Check for any numeric columns that might contain pricing
print("\nNumeric columns and their ranges:")
for col in df.columns:
    if df[col].dtype in ['float64', 'int64']:
        print(f"\n{col}:")
        print(f"  Min: {df[col].min()}")
        print(f"  Max: {df[col].max()}")
        print(f"  Mean: {df[col].mean():.2f}")
        print(f"  Sum: {df[col].sum():,.2f}")

# Check if there's pricing in the pivot file
print("\n" + "="*60)
print("CHECKING PIVOT FILE")
print("="*60)

try:
    df_pivot = pd.read_excel('Pivot DYLN Fulfillment - Shipments.xlsx')
    print(f"\nPivot file has {len(df_pivot)} rows and {len(df_pivot.columns)} columns")
    print("\nPivot columns:")
    for col in df_pivot.columns:
        print(f"  - {col}")
    
    # Check for revenue/cost columns
    revenue_keywords = ['revenue', 'cost', 'price', 'amount', 'total', 'sales', 'dollar', '$']
    found_columns = []
    for col in df_pivot.columns:
        if any(keyword in str(col).lower() for keyword in revenue_keywords):
            found_columns.append(col)
    
    if found_columns:
        print(f"\nPotential revenue/cost columns found:")
        for col in found_columns:
            print(f"  - {col}")
            if df_pivot[col].dtype in ['float64', 'int64']:
                print(f"    Range: ${df_pivot[col].min():,.2f} - ${df_pivot[col].max():,.2f}")
                print(f"    Total: ${df_pivot[col].sum():,.2f}")
except Exception as e:
    print(f"Could not analyze pivot file: {e}")

# Annual projection based on current data
print("\n" + "="*60)
print("VOLUME-BASED PROJECTIONS")
print("="*60)

# Calculate annualized volume
total_shipments = len(df)
date_range = (df['shipment_date'].max() - df['shipment_date'].min()).days + 1
daily_avg = total_shipments / date_range
annual_projection = daily_avg * 365

print(f"\nBased on {date_range} days of data:")
print(f"  Daily average: {daily_avg:.0f} shipments")
print(f"  Monthly average: {daily_avg * 30:.0f} shipments")
print(f"  Annual projection: {annual_projection:,.0f} shipments")

print("\nNote: Revenue calculation requires pricing data which is not")
print("available in the current dataset. To calculate revenue, we would need:")
print("  - Product prices or order values")
print("  - Shipping costs charged to customers")
print("  - Or total order amounts")