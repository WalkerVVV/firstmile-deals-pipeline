"""
Stackd Logistics Volume Correction - October 14, 2025

CRITICAL CORRECTION:
- Original analysis treated 8,419 packages as MONTHLY volume
- User correction: 8,419 packages = 2 WEEKS of volume
- Multiply by 2 to get 4-week monthly volume
- This DOUBLES the savings opportunity

Recalculate all metrics with corrected volume.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Load the comparison data
df = pd.read_csv('stackd_firstmile_vs_dhl_comparison.csv')

print("=" * 80)
print("STACKD LOGISTICS VOLUME CORRECTION")
print("=" * 80)
print(f"Analysis Date: {datetime.now().strftime('%B %d, %Y %I:%M %p')}")
print()

# Original (INCORRECT) assumptions
print("ORIGINAL ANALYSIS (INCORRECT):")
print("-" * 80)
packages_2_weeks = len(df)
print(f"Packages analyzed: {packages_2_weeks:,}")
print(f"Assumed period: 1 MONTH (INCORRECT)")
print(f"Assumed monthly volume: {packages_2_weeks:,}")
print()

# Corrected calculations
print("CORRECTED ANALYSIS:")
print("-" * 80)
print(f"Packages analyzed: {packages_2_weeks:,}")
print(f"Actual period: 2 WEEKS")
print(f"Corrected monthly volume: {packages_2_weeks * 2:,} packages/month")
print(f"Corrected annual volume: {packages_2_weeks * 2 * 12:,} packages/year")
print()

# Calculate savings from the comparison data
total_dhl_cost = df['Label Cost'].sum()
total_firstmile_cost = df['FirstMile_Cost'].sum()
total_savings_2weeks = total_dhl_cost - total_firstmile_cost
savings_pct = (total_savings_2weeks / total_dhl_cost) * 100

print("SAVINGS CALCULATION:")
print("-" * 80)
print(f"2-Week Period (8,419 packages):")
print(f"  DHL Cost: ${total_dhl_cost:,.2f}")
print(f"  FirstMile Cost: ${total_firstmile_cost:,.2f}")
print(f"  Savings: ${total_savings_2weeks:,.2f} ({savings_pct:.1f}%)")
print()

# Monthly savings (multiply by 2)
monthly_savings = total_savings_2weeks * 2
monthly_dhl = total_dhl_cost * 2
monthly_firstmile = total_firstmile_cost * 2
monthly_volume = packages_2_weeks * 2

print(f"Monthly (4 weeks, ~{monthly_volume:,} packages):")
print(f"  DHL Cost: ${monthly_dhl:,.2f}")
print(f"  FirstMile Cost: ${monthly_firstmile:,.2f}")
print(f"  Monthly Savings: ${monthly_savings:,.2f} ({savings_pct:.1f}%)")
print()

# Annual savings
annual_savings = monthly_savings * 12
annual_dhl = monthly_dhl * 12
annual_firstmile = monthly_firstmile * 12
annual_volume = monthly_volume * 12

print(f"Annual (12 months, ~{annual_volume:,} packages):")
print(f"  DHL Cost: ${annual_dhl:,.2f}")
print(f"  FirstMile Cost: ${annual_firstmile:,.2f}")
print(f"  Annual Savings: ${annual_savings:,.2f} ({savings_pct:.1f}%)")
print()

# Network breakdown
select_states = ['CA', 'TX', 'FL', 'NY', 'WA', 'AZ', 'NJ', 'IL', 'MA', 'GA']
df['Network'] = df['State'].apply(lambda x: 'Select' if x in select_states else 'National')

select_df = df[df['Network'] == 'Select']
national_df = df[df['Network'] == 'National']

select_savings_2weeks = select_df['Savings'].sum()
national_savings_2weeks = national_df['Savings'].sum()

select_dhl_2weeks = select_df['Label Cost'].sum()
national_dhl_2weeks = national_df['Label Cost'].sum()

select_pct = (select_savings_2weeks / select_dhl_2weeks) * 100 if select_dhl_2weeks > 0 else 0
national_pct = (national_savings_2weeks / national_dhl_2weeks) * 100 if national_dhl_2weeks > 0 else 0

print("NETWORK BREAKDOWN:")
print("-" * 80)
print(f"Select Network (Major Metros):")
print(f"  2-Week Volume: {len(select_df):,} packages ({len(select_df)/len(df)*100:.1f}%)")
print(f"  Monthly Volume: {len(select_df)*2:,} packages")
print(f"  2-Week Savings: ${select_savings_2weeks:,.2f} ({select_pct:.1f}%)")
print(f"  Monthly Savings: ${select_savings_2weeks*2:,.2f}")
print(f"  Annual Savings: ${select_savings_2weeks*24:,.2f}")
print()

print(f"National Network (All Other States):")
print(f"  2-Week Volume: {len(national_df):,} packages ({len(national_df)/len(df)*100:.1f}%)")
print(f"  Monthly Volume: {len(national_df)*2:,} packages")
print(f"  2-Week Savings: ${national_savings_2weeks:,.2f} ({national_pct:.1f}%)")
print(f"  Monthly Savings: ${national_savings_2weeks*2:,.2f}")
print(f"  Annual Savings: ${national_savings_2weeks*24:,.2f}")
print()

# Summary for Excel update
print("=" * 80)
print("SUMMARY FOR EXCEL UPDATE")
print("=" * 80)
print(f"Monthly Package Volume: {monthly_volume:,}")
print(f"Annual Package Volume: {annual_volume:,}")
print(f"Monthly Savings: ${monthly_savings:,.2f}")
print(f"Annual Savings: ${annual_savings:,.2f}")
print(f"Overall Savings Percentage: {savings_pct:.1f}%")
print(f"Average Savings per Package: ${monthly_savings/monthly_volume:.2f}")
print()
print(f"Select Network Monthly Savings: ${select_savings_2weeks*2:,.2f} ({select_pct:.1f}%)")
print(f"National Network Monthly Savings: ${national_savings_2weeks*2:,.2f} ({national_pct:.1f}%)")
print()

# Cost per package
avg_dhl_pkg = monthly_dhl / monthly_volume
avg_firstmile_pkg = monthly_firstmile / monthly_volume
avg_savings_pkg = monthly_savings / monthly_volume

print(f"Average Cost per Package:")
print(f"  DHL: ${avg_dhl_pkg:.2f}")
print(f"  FirstMile: ${avg_firstmile_pkg:.2f}")
print(f"  Savings: ${avg_savings_pkg:.2f} ({savings_pct:.1f}%)")
print()

print("=" * 80)
print("CORRECTION COMPLETE")
print("=" * 80)
print()
print("Next Steps:")
print("1. Update Excel file with corrected volume and savings")
print("2. Update email to Landon with corrected figures")
print("3. Update domain-memory-agent with corrected data")
print("4. Update implementation timeline if needed")
