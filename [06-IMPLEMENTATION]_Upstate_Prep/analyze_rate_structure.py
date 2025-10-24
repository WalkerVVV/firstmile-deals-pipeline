"""
Analyze the structure of the FirstMile rate file
"""

import pandas as pd
import numpy as np

# Load the rate file
rate_file = 'Upstate Prep_FirstMile_Xparcel_08-20-25.xlsx'

# Try to read all sheets
xl_file = pd.ExcelFile(rate_file)
print("=" * 80)
print(f"RATE FILE STRUCTURE: {rate_file}")
print("=" * 80)
print(f"\nAvailable sheets: {xl_file.sheet_names}")
print()

# Read each sheet and display structure
for sheet_name in xl_file.sheet_names:
    print(f"\n{'='*60}")
    print(f"SHEET: {sheet_name}")
    print('='*60)
    
    df = pd.read_excel(rate_file, sheet_name=sheet_name)
    print(f"Shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    
    # Show first few rows
    print(f"\nFirst 5 rows:")
    print(df.head())
    
    # Check if it looks like a rate table
    if 'Zone' in ' '.join(str(col) for col in df.columns) or any('zone' in str(col).lower() for col in df.columns):
        print("\nThis appears to be a rate table with zones!")
    
    # Check for weight columns
    weight_cols = [col for col in df.columns if any(indicator in str(col).lower() for indicator in ['lb', 'oz', 'weight', '1', '2', '3', '4', '5'])]
    if weight_cols:
        print(f"\nPotential weight columns found: {weight_cols[:10]}")  # Show first 10

xl_file.close()