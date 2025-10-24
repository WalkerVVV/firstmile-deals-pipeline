#!/usr/bin/env python3
"""
SELECT NETWORK DAS ZIP ANALYSIS
Comprehensive analysis of FirstMile Select Network coverage and DAS zones
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import json

print("="*80)
print("SELECT NETWORK DAS ZIP ANALYSIS")
print("FirstMile Network Coverage & Delivery Area Surcharge Analysis")
print("="*80)

# Load the Select Network data
file_path = 'Select Carrier Zips and DAS ZIPS.xlsx'
print(f"\nLoading: {file_path}")

try:
    df = pd.read_excel(file_path, sheet_name='Sheet1')
    print(f"[OK] Loaded {len(df):,} rows, {len(df.columns)} columns")
    print(f"\nColumns found: {', '.join(df.columns.tolist())}")

    # Display first few rows to understand structure
    print("\n" + "="*60)
    print("DATA STRUCTURE PREVIEW:")
    print("="*60)
    print(df.head(10).to_string())

    print("\n" + "="*60)
    print("DATA TYPES:")
    print("="*60)
    print(df.dtypes)

    print("\n" + "="*60)
    print("SUMMARY STATISTICS:")
    print("="*60)

    # Analyze each column
    for col in df.columns:
        print(f"\n{col}:")
        if df[col].dtype == 'object':
            # String/categorical column
            unique_count = df[col].nunique()
            print(f"  - Unique values: {unique_count:,}")
            if unique_count <= 20:
                print(f"  - Values: {df[col].unique().tolist()}")
            else:
                print(f"  - Sample values: {df[col].dropna().unique()[:10].tolist()}")
            print(f"  - Most common: {df[col].value_counts().head(5).to_dict()}")
        else:
            # Numeric column
            print(f"  - Min: {df[col].min()}")
            print(f"  - Max: {df[col].max()}")
            print(f"  - Mean: {df[col].mean():.2f}")
            print(f"  - Non-null count: {df[col].notna().sum():,}")

    # Check for ZIP code columns
    print("\n" + "="*60)
    print("ZIP CODE ANALYSIS:")
    print("="*60)

    # Identify potential ZIP columns
    zip_columns = []
    for col in df.columns:
        # Check if column contains ZIP-like data
        if df[col].dtype == 'object':
            sample = df[col].dropna().astype(str).head(100)
            if sample.str.match(r'^\d{5}(-\d{4})?$').any():
                zip_columns.append(col)
                print(f"  [OK] Found ZIP column: {col}")
        elif df[col].dtype in ['int64', 'float64']:
            # Check if numeric column might be ZIP codes
            if df[col].min() >= 1 and df[col].max() <= 99999:
                sample_vals = df[col].dropna().unique()[:10]
                if all(1 <= v <= 99999 for v in sample_vals):
                    zip_columns.append(col)
                    print(f"  [OK] Found numeric ZIP column: {col}")

    # DAS Analysis if DAS column exists
    das_cols = [col for col in df.columns if 'DAS' in col.upper()]
    if das_cols:
        print("\n" + "="*60)
        print("DAS (DELIVERY AREA SURCHARGE) ANALYSIS:")
        print("="*60)

        for das_col in das_cols:
            print(f"\n{das_col}:")
            das_values = df[das_col].value_counts()
            print(das_values.to_string())

            # Calculate DAS coverage
            if len(das_values) > 0:
                das_zips = df[df[das_col].notna() & (df[das_col] != 0)]
                print(f"\nDAS ZIP Coverage:")
                print(f"  - Total ZIPs with DAS: {len(das_zips):,}")
                print(f"  - Percentage with DAS: {len(das_zips)/len(df)*100:.1f}%")

    # Network Type Analysis
    network_cols = [col for col in df.columns if any(x in col.upper() for x in ['NETWORK', 'CARRIER', 'SELECT', 'NATIONAL'])]
    if network_cols:
        print("\n" + "="*60)
        print("NETWORK TYPE ANALYSIS:")
        print("="*60)

        for net_col in network_cols:
            print(f"\n{net_col}:")
            net_values = df[net_col].value_counts()
            print(net_values.to_string())

    # Geographic Distribution
    if zip_columns:
        print("\n" + "="*60)
        print("GEOGRAPHIC DISTRIBUTION:")
        print("="*60)

        for zip_col in zip_columns[:1]:  # Analyze first ZIP column
            # Extract ZIP3 (first 3 digits) for regional analysis
            df['zip3'] = df[zip_col].astype(str).str[:3]

            # Map ZIP3 to regions
            def get_region(zip3):
                try:
                    z = int(zip3)
                    if z <= 99: return 'Northeast'
                    elif z <= 199: return 'Mid-Atlantic'
                    elif z <= 399: return 'Southeast'
                    elif z <= 499: return 'Midwest'
                    elif z <= 599: return 'South Central'
                    elif z <= 799: return 'Mountain'
                    elif z <= 899: return 'Pacific'
                    elif z <= 999: return 'Pacific'
                    else: return 'Other'
                except:
                    return 'Invalid'

            df['region'] = df['zip3'].apply(get_region)

            print("\nRegional Distribution:")
            region_dist = df['region'].value_counts()
            for region, count in region_dist.items():
                print(f"  {region}: {count:,} ZIPs ({count/len(df)*100:.1f}%)")

            # State-level analysis (ZIP to state mapping)
            print("\nTop ZIP3 Prefixes:")
            top_zip3 = df['zip3'].value_counts().head(20)
            for zip3, count in top_zip3.items():
                print(f"  {zip3}xx: {count:,} ZIPs")

    # Create comprehensive analysis dictionary
    analysis = {
        'total_records': len(df),
        'columns': df.columns.tolist(),
        'zip_columns_found': zip_columns,
        'das_columns_found': das_cols,
        'network_columns_found': network_cols
    }

    # Save analysis summary
    print("\n" + "="*60)
    print("SAVING ANALYSIS RESULTS:")
    print("="*60)

    # Save to JSON for further processing
    with open('select_network_das_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    print("[OK] Saved analysis to select_network_das_analysis.json")

    # Save cleaned data
    df.to_csv('select_network_das_cleaned.csv', index=False)
    print("[OK] Saved cleaned data to select_network_das_cleaned.csv")

    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"Total records analyzed: {len(df):,}")
    print(f"Data dimensions: {df.shape[0]} rows × {df.shape[1]} columns")

except Exception as e:
    print(f"\n[ERROR] Error loading file: {e}")
    print("\nAttempting alternative read methods...")

    # Try reading with different parameters
    try:
        df = pd.read_excel(file_path, sheet_name=0)
        print(f"[OK] Successfully loaded with sheet index 0")
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
    except Exception as e2:
        print(f"[ERROR] Alternative read also failed: {e2}")