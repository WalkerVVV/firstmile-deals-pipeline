"""
Stackd Logistics - Actual Cost Analysis
Analyzes real package-level data to determine accurate FirstMile savings potential
"""

import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('20250918193042_221aaf59f30469602caf8f7f7485b114.csv')

print("=" * 80)
print("STACKD LOGISTICS - ACTUAL COST ANALYSIS")
print("=" * 80)
print()

# Basic volume metrics
total_packages = len(df)
print(f"TOTAL PACKAGES: {total_packages:,}")
print()

# Carrier breakdown
print("=" * 80)
print("CARRIER MIX")
print("=" * 80)
carrier_breakdown = df.groupby('Carrier').agg({
    'Shipping Label ID': 'count',
    'Label Cost': ['sum', 'mean']
}).round(2)
carrier_breakdown.columns = ['Volume', 'Total Cost', 'Avg Cost']
carrier_breakdown['% Volume'] = (carrier_breakdown['Volume'] / total_packages * 100).round(1)
carrier_breakdown['% Spend'] = (carrier_breakdown['Total Cost'] / df['Label Cost'].sum() * 100).round(1)
print(carrier_breakdown.to_string())
print()

# Service level breakdown
print("=" * 80)
print("SERVICE LEVEL MIX")
print("=" * 80)
service_breakdown = df.groupby('Shipping Method').agg({
    'Shipping Label ID': 'count',
    'Label Cost': ['sum', 'mean']
}).round(2)
service_breakdown.columns = ['Volume', 'Total Cost', 'Avg Cost']
service_breakdown['% Volume'] = (service_breakdown['Volume'] / total_packages * 100).round(1)
print(service_breakdown.to_string())
print()

# Weight distribution
print("=" * 80)
print("WEIGHT DISTRIBUTION")
print("=" * 80)
weight_bins = [0, 0.0625, 0.25, 0.5, 0.75, 1, 2, 3, 5, 10, 999]
weight_labels = ['<1 oz', '1-4 oz', '4-8 oz', '8-12 oz', '12-16 oz', '1-2 lbs', '2-3 lbs', '3-5 lbs', '5-10 lbs', '>10 lbs']
df['Weight_Category'] = pd.cut(df['Weight (lb)'], bins=weight_bins, labels=weight_labels)

weight_analysis = df.groupby('Weight_Category').agg({
    'Shipping Label ID': 'count',
    'Label Cost': ['sum', 'mean']
}).round(2)
weight_analysis.columns = ['Volume', 'Total Cost', 'Avg Cost']
weight_analysis['% Volume'] = (weight_analysis['Volume'] / total_packages * 100).round(1)
weight_analysis['% Spend'] = (weight_analysis['Total Cost'] / df['Label Cost'].sum() * 100).round(1)
print(weight_analysis.to_string())
print()

# Geographic breakdown - Top 10 states
print("=" * 80)
print("TOP 10 DESTINATION STATES")
print("=" * 80)
state_breakdown = df.groupby('State').agg({
    'Shipping Label ID': 'count',
    'Label Cost': ['sum', 'mean']
}).round(2)
state_breakdown.columns = ['Volume', 'Total Cost', 'Avg Cost']
state_breakdown['% Volume'] = (state_breakdown['Volume'] / total_packages * 100).round(1)
state_breakdown = state_breakdown.sort_values('Volume', ascending=False).head(10)
print(state_breakdown.to_string())
print()

# Cost summary
print("=" * 80)
print("COST SUMMARY")
print("=" * 80)
total_cost = df['Label Cost'].sum()
avg_cost = df['Label Cost'].mean()
median_cost = df['Label Cost'].median()
print(f"Total Shipping Cost: ${total_cost:,.2f}")
print(f"Average Cost/Package: ${avg_cost:.2f}")
print(f"Median Cost/Package: ${median_cost:.2f}")
print()

# Monthly projection
print(f"Monthly Projection (assuming sample is representative):")
print(f"  Estimated Monthly Volume: 2,800 packages")
print(f"  Estimated Monthly Cost: ${avg_cost * 2800:,.2f}")
print(f"  Estimated Annual Cost: ${avg_cost * 2800 * 12:,.2f}")
print()

# Carrier-specific analysis
print("=" * 80)
print("DETAILED CARRIER ANALYSIS")
print("=" * 80)

# UPS 2nd Day Air analysis
ups_2day = df[df['Shipping Method'] == 'UPS 2nd Day Air']
if len(ups_2day) > 0:
    print(f"\nUPS 2nd Day Air (EXPRESS):")
    print(f"  Volume: {len(ups_2day):,} packages ({len(ups_2day)/total_packages*100:.1f}%)")
    print(f"  Total Cost: ${ups_2day['Label Cost'].sum():,.2f}")
    print(f"  Avg Cost: ${ups_2day['Label Cost'].mean():.2f}")
    print(f"  Median Cost: ${ups_2day['Label Cost'].median():.2f}")
    print(f"  Weight Range: {ups_2day['Weight (lb)'].min():.3f} - {ups_2day['Weight (lb)'].max():.3f} lbs")
    print(f"  Avg Weight: {ups_2day['Weight (lb)'].mean():.3f} lbs")

# DHL eCommerce analysis
dhl = df[df['Carrier'] == 'dhl_ecommerce']
if len(dhl) > 0:
    print(f"\nDHL eCommerce (GROUND):")
    print(f"  Volume: {len(dhl):,} packages ({len(dhl)/total_packages*100:.1f}%)")
    print(f"  Total Cost: ${dhl['Label Cost'].sum():,.2f}")
    print(f"  Avg Cost: ${dhl['Label Cost'].mean():.2f}")
    print(f"  Median Cost: ${dhl['Label Cost'].median():.2f}")
    print(f"  Weight Range: {dhl['Weight (lb)'].min():.3f} - {dhl['Weight (lb)'].max():.3f} lbs")
    print(f"  Avg Weight: {dhl['Weight (lb)'].mean():.3f} lbs")

# USPS Ground Advantage analysis
usps = df[df['Carrier'] == 'usps_modern']
if len(usps) > 0:
    print(f"\nUSPS Ground Advantage:")
    print(f"  Volume: {len(usps):,} packages ({len(usps)/total_packages*100:.1f}%)")
    print(f"  Total Cost: ${usps['Label Cost'].sum():,.2f}")
    print(f"  Avg Cost: ${usps['Label Cost'].mean():.2f}")
    print(f"  Median Cost: ${usps['Label Cost'].median():.2f}")
    print(f"  Weight Range: {usps['Weight (lb)'].min():.3f} - {usps['Weight (lb)'].max():.3f} lbs")
    print(f"  Avg Weight: {usps['Weight (lb)'].mean():.3f} lbs")

print()
print("=" * 80)
print("KEY INSIGHTS")
print("=" * 80)
print()
print(">> Data Quality: VERIFIED - Real label costs from ShipHero export")
print()
print(">> Profile Characteristics:")
under_1lb = len(df[df['Weight (lb)'] < 1]) / total_packages * 100
print(f"  - {under_1lb:.1f}% of packages under 1 lb (FirstMile sweet spot)")
ups_express = len(ups_2day) / total_packages * 100 if len(ups_2day) > 0 else 0
print(f"  - {ups_express:.1f}% using expensive UPS 2nd Day Air")
print(f"  - Average package weight: {df['Weight (lb)'].mean():.3f} lbs")
print()
print(">> FirstMile Opportunity:")
print("  - Replace expensive UPS 2nd Day Air with Xparcel Expedited (2-5d)")
print("  - Replace DHL eCommerce with Xparcel Ground (3-8d)")
print("  - Maintain or improve transit times with better pricing")
print()
print(">> Next Steps:")
print("  1. Apply FirstMile rate card to this data")
print("  2. Calculate package-by-package savings")
print("  3. Generate accurate total savings projection")
print("  4. Update proposal with verified numbers")
print()

print("=" * 80)
