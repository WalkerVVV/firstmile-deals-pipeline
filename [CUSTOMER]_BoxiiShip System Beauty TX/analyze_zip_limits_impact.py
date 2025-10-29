#!/usr/bin/env python3
"""
Analyze how FirstMile Xparcel ZIP limits will change BoxiiShip's carrier mix
Compares current carrier usage vs. what would be available with Xparcel Ground & Expedited
"""

import pandas as pd

# Load the PLD data
pld_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\BoxiiShip System Beauty Logistics LLC TX_Domestic_Tracking_10.1.25_to10.20.25.xlsx"
df = pd.read_excel(pld_file)

print("=" * 80)
print("BOXIISHIP SYSTEM BEAUTY TX - XPARCEL ZIP LIMIT IMPACT ANALYSIS")
print("Data Period: October 1-20, 2025")
print("=" * 80)

# Load the ZIP limit files
ground_zips_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\ACI-D 8 day .95 zip limit from 761.txt"
expedited_zips_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\ACI-D 5 day .95 zip limit from 761.txt"

# Read ZIP codes (skip header row)
ground_zips = set(pd.read_csv(ground_zips_file, skiprows=1, header=None)[0].astype(str).str.zfill(5))
expedited_zips = set(pd.read_csv(expedited_zips_file, skiprows=1, header=None)[0].astype(str).str.zfill(5))

print(f"\nFIRSTMILE XPARCEL COVERAGE FROM ORIGIN 761:")
print(f"   Xparcel Ground eligible ZIPs: {len(ground_zips):,}")
print(f"   Xparcel Expedited eligible ZIPs: {len(expedited_zips):,}")
print(f"   Ground-only ZIPs (no Expedited): {len(ground_zips - expedited_zips):,}")

# Standardize destination ZIP in data
print(f"\nORIGINAL DATA SUMMARY:")
print(f"   Total shipments: {len(df):,}")

# Try to find the destination ZIP column
zip_cols = [col for col in df.columns if 'zip' in col.lower() or 'postal' in col.lower()]
print(f"   ZIP columns found: {zip_cols}")

# Show first few rows to identify columns
print(f"\nSAMPLE DATA (first 3 rows):")
print(df.head(3).to_string())

# Show all column names
print(f"\nALL COLUMNS:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i:2d}. {col}")

# Identify key columns
print(f"\nKEY COLUMNS TO IDENTIFY:")
print("   - Destination ZIP code")
print("   - Current carrier/service level")
print("   - Weight (if available)")
print("   - Zone (if available)")

# Ask user to confirm column names or proceed with analysis
print(f"\n" + "=" * 80)
