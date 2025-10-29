#!/usr/bin/env python3
"""
Explore the Excel file structure to find the actual PLD data
"""

import pandas as pd

# Load the Excel file
excel_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\BoxiiShip System Beauty Logistics LLC TX_Domestic_Tracking_10.1.25_to10.20.25.xlsx"

# Get all sheet names
xl_file = pd.ExcelFile(excel_file)
print("=" * 80)
print("EXCEL FILE STRUCTURE EXPLORATION")
print("=" * 80)
print(f"\nFile: {excel_file.split('\\')[-1]}")
print(f"\nSheet Names ({len(xl_file.sheet_names)}):")
for i, sheet in enumerate(xl_file.sheet_names, 1):
    print(f"   {i}. {sheet}")

# Read each sheet and show summary
for sheet_name in xl_file.sheet_names:
    print(f"\n{'=' * 80}")
    print(f"SHEET: {sheet_name}")
    print("=" * 80)

    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"Dimensions: {df.shape[0]} rows x {df.shape[1]} columns")

    print(f"\nColumns:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i:2d}. {col}")

    print(f"\nFirst 5 rows:")
    print(df.head(5).to_string())

    # Check for ZIP-like columns
    zip_like = [col for col in df.columns if any(x in str(col).lower() for x in ['zip', 'postal', 'destination', 'dest'])]
    if zip_like:
        print(f"\nPotential ZIP columns: {zip_like}")

    # Check for carrier/service columns
    carrier_like = [col for col in df.columns if any(x in str(col).lower() for x in ['carrier', 'service', 'ship', 'method'])]
    if carrier_like:
        print(f"Potential carrier/service columns: {carrier_like}")

print(f"\n{'=' * 80}")
