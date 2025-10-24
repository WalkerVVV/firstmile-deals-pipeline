"""
Comprehensive PLD Analysis for Upstate Prep
T30 (Trailing 30 Days) Parcel Level Detail Analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the data
print("=" * 80)
print("UPSTATE PREP - T30 PLD COMPREHENSIVE ANALYSIS")
print("=" * 80)

df = pd.read_csv('T30 PLD Upstate Prep.csv')
print(f"\nTotal Shipments Loaded: {len(df):,}")

# Clean and prepare data
df['Order date'] = pd.to_datetime(df['Order date'], errors='coerce')
df['Created at'] = pd.to_datetime(df['Created at'], errors='coerce')
df['Weight (lb)'] = pd.to_numeric(df['Weight (lb)'], errors='coerce')
df['Label Cost'] = pd.to_numeric(df['Label Cost'], errors='coerce')
df['Difference'] = pd.to_numeric(df['Difference'], errors='coerce')
df['Height (in)'] = pd.to_numeric(df['Height (in)'], errors='coerce')
df['Width (in)'] = pd.to_numeric(df['Width (in)'], errors='coerce')
df['Length (in)'] = pd.to_numeric(df['Length (in)'], errors='coerce')

# Get date range
date_min = df['Order date'].min()
date_max = df['Order date'].max()
days_in_period = (date_max - date_min).days + 1

print(f"Date Range: {date_min.strftime('%Y-%m-%d')} to {date_max.strftime('%Y-%m-%d')} ({days_in_period} days)")

# ========================================
# 1. VOLUME PROFILE
# ========================================
print("\n" + "=" * 60)
print("1. VOLUME PROFILE")
print("=" * 60)

total_volume = len(df)
daily_average = total_volume / days_in_period
monthly_projection = daily_average * 30

print(f"Total Shipments (T30): {total_volume:,}")
print(f"Daily Average: {daily_average:.1f}")
print(f"Monthly Projection: {monthly_projection:.0f}")

# Analyze by marketplace/profile
profile_dist = df['Profile'].value_counts()
print("\nProfile Distribution:")
for profile, count in profile_dist.items():
    pct = (count / total_volume) * 100
    print(f"  {profile}: {count:,} ({pct:.1f}%)")

# ========================================
# 2. CARRIER MIX
# ========================================
print("\n" + "=" * 60)
print("2. CARRIER MIX - Volume & Spend Analysis")
print("=" * 60)

carrier_analysis = df.groupby('Carrier').agg({
    'Shipping Label ID': 'count',
    'Label Cost': 'sum'
}).rename(columns={'Shipping Label ID': 'Volume'})

carrier_analysis['Volume %'] = (carrier_analysis['Volume'] / total_volume * 100)
carrier_analysis['Spend %'] = (carrier_analysis['Label Cost'] / df['Label Cost'].sum() * 100)
carrier_analysis = carrier_analysis.sort_values('Volume', ascending=False)

print("\n{:<30} {:>10} {:>10} {:>12} {:>10}".format(
    "Carrier", "Volume", "Vol %", "Spend ($)", "Spend %"
))
print("-" * 75)

for carrier in carrier_analysis.index:
    print("{:<30} {:>10,} {:>9.1f}% ${:>11,.2f} {:>9.1f}%".format(
        carrier,
        carrier_analysis.loc[carrier, 'Volume'],
        carrier_analysis.loc[carrier, 'Volume %'],
        carrier_analysis.loc[carrier, 'Label Cost'],
        carrier_analysis.loc[carrier, 'Spend %']
    ))

print("-" * 75)
print("{:<30} {:>10,} {:>9.1f}% ${:>11,.2f} {:>9.1f}%".format(
    "TOTAL",
    carrier_analysis['Volume'].sum(),
    100.0,
    carrier_analysis['Label Cost'].sum(),
    100.0
))

# ========================================
# 3. SERVICE LEVEL DISTRIBUTION
# ========================================
print("\n" + "=" * 60)
print("3. SERVICE LEVEL DISTRIBUTION")
print("=" * 60)

service_analysis = df.groupby('Shipping Method').agg({
    'Shipping Label ID': 'count',
    'Label Cost': ['sum', 'mean']
}).round(2)

service_analysis.columns = ['Volume', 'Total Cost', 'Avg Cost']
service_analysis['Volume %'] = (service_analysis['Volume'] / total_volume * 100)
service_analysis = service_analysis.sort_values('Volume', ascending=False)

print("\n{:<30} {:>10} {:>10} {:>12} {:>10}".format(
    "Service Level", "Volume", "Vol %", "Total Cost", "Avg Cost"
))
print("-" * 75)

for service in service_analysis.index:
    print("{:<30} {:>10,} {:>9.1f}% ${:>11,.2f} ${:>9.2f}".format(
        service,
        service_analysis.loc[service, 'Volume'],
        service_analysis.loc[service, 'Volume %'],
        service_analysis.loc[service, 'Total Cost'],
        service_analysis.loc[service, 'Avg Cost']
    ))

# ========================================
# 4. EXPANDED WEIGHT DISTRIBUTION
# ========================================
print("\n" + "=" * 60)
print("4. EXPANDED WEIGHT DISTRIBUTION")
print("=" * 60)

# Calculate actual weight in ounces for detailed breakdown
df['Weight (oz)'] = df['Weight (lb)'] * 16

# Define weight categories
def categorize_weight(weight_oz):
    if weight_oz <= 4: return '0-4 oz'
    elif weight_oz <= 8: return '5-8 oz'
    elif weight_oz <= 12: return '9-12 oz'
    elif weight_oz <= 15: return '13-15 oz'
    elif weight_oz <= 15.99: return '15.01-15.99 oz'
    elif weight_oz == 16: return '16 oz (1 lb)'
    elif weight_oz <= 32: return '17-32 oz (1-2 lb)'
    elif weight_oz <= 48: return '33-48 oz (2-3 lb)'
    elif weight_oz <= 64: return '49-64 oz (3-4 lb)'
    elif weight_oz <= 80: return '65-80 oz (4-5 lb)'
    elif weight_oz <= 160: return '81-160 oz (5-10 lb)'
    else: return 'Over 10 lb'

df['Weight Category'] = df['Weight (oz)'].apply(categorize_weight)

weight_dist = df.groupby('Weight Category').agg({
    'Shipping Label ID': 'count',
    'Label Cost': 'sum'
}).rename(columns={'Shipping Label ID': 'Volume'})

# Sort by logical order
weight_order = ['0-4 oz', '5-8 oz', '9-12 oz', '13-15 oz', '15.01-15.99 oz', 
                '16 oz (1 lb)', '17-32 oz (1-2 lb)', '33-48 oz (2-3 lb)', 
                '49-64 oz (3-4 lb)', '65-80 oz (4-5 lb)', '81-160 oz (5-10 lb)', 
                'Over 10 lb']

weight_dist = weight_dist.reindex([w for w in weight_order if w in weight_dist.index])
weight_dist['Volume %'] = (weight_dist['Volume'] / total_volume * 100)
weight_dist['Spend %'] = (weight_dist['Label Cost'] / df['Label Cost'].sum() * 100)

print("\n{:<25} {:>10} {:>10} {:>12} {:>10}".format(
    "Weight Range", "Volume", "Vol %", "Spend ($)", "Spend %"
))
print("-" * 70)

for weight_cat in weight_dist.index:
    print("{:<25} {:>10,} {:>9.1f}% ${:>11,.2f} {:>9.1f}%".format(
        weight_cat,
        weight_dist.loc[weight_cat, 'Volume'],
        weight_dist.loc[weight_cat, 'Volume %'],
        weight_dist.loc[weight_cat, 'Label Cost'],
        weight_dist.loc[weight_cat, 'Spend %']
    ))

# Key threshold analysis
under_1lb = df[df['Weight (lb)'] < 1].shape[0]
exactly_16oz = df[df['Weight (oz)'] == 16].shape[0]
under_16oz = df[df['Weight (oz)'] < 16].shape[0]

print(f"\nKey Thresholds:")
print(f"  Under 16 oz: {under_16oz:,} ({under_16oz/total_volume*100:.1f}%)")
print(f"  Exactly 16 oz: {exactly_16oz:,} ({exactly_16oz/total_volume*100:.1f}%)")
print(f"  Under 1 lb total: {under_1lb:,} ({under_1lb/total_volume*100:.1f}%)")

# ========================================
# 5. DIMENSIONAL ANALYSIS
# ========================================
print("\n" + "=" * 60)
print("5. DIMENSIONAL ANALYSIS")
print("=" * 60)

# Calculate cubic volume
df['Cubic Inches'] = df['Length (in)'] * df['Width (in)'] * df['Height (in)']
df['Cubic Feet'] = df['Cubic Inches'] / 1728

avg_dims = {
    'Length': df['Length (in)'].mean(),
    'Width': df['Width (in)'].mean(),
    'Height': df['Height (in)'].mean(),
    'Cubic Inches': df['Cubic Inches'].mean()
}

print(f"\nAverage Package Dimensions:")
print(f"  Length: {avg_dims['Length']:.1f} inches")
print(f"  Width: {avg_dims['Width']:.1f} inches")
print(f"  Height: {avg_dims['Height']:.1f} inches")
print(f"  Cubic Volume: {avg_dims['Cubic Inches']:.0f} cubic inches ({avg_dims['Cubic Inches']/1728:.2f} cubic feet)")

# Analyze by cubic feet categories
under_1_cuft = df[df['Cubic Feet'] < 1].shape[0]
over_1_cuft = df[df['Cubic Feet'] >= 1].shape[0]

print(f"\nCubic Volume Distribution:")
print(f"  Under 1 cubic foot: {under_1_cuft:,} ({under_1_cuft/total_volume*100:.1f}%)")
print(f"  1+ cubic feet: {over_1_cuft:,} ({over_1_cuft/total_volume*100:.1f}%)")

# Analyze by box type
box_dist = df['Box Name'].value_counts().head(5)
print(f"\nTop 5 Package Types:")
for box, count in box_dist.items():
    pct = (count / total_volume) * 100
    print(f"  {box}: {count:,} ({pct:.1f}%)")

# ========================================
# 6. GEOGRAPHIC DISTRIBUTION
# ========================================
print("\n" + "=" * 60)
print("6. GEOGRAPHIC DISTRIBUTION - Top 10 States")
print("=" * 60)

state_dist = df['State'].value_counts().head(10)
state_analysis = pd.DataFrame({
    'Volume': state_dist,
    'Volume %': (state_dist / total_volume * 100)
})

# Add spend analysis
state_spend = df.groupby('State')['Label Cost'].sum().loc[state_dist.index]
state_analysis['Spend'] = state_spend
state_analysis['Spend %'] = (state_spend / df['Label Cost'].sum() * 100)

print("\n{:<15} {:>10} {:>10} {:>12} {:>10}".format(
    "State", "Volume", "Vol %", "Spend ($)", "Spend %"
))
print("-" * 60)

for state in state_analysis.index:
    print("{:<15} {:>10,} {:>9.1f}% ${:>11,.2f} {:>9.1f}%".format(
        state,
        state_analysis.loc[state, 'Volume'],
        state_analysis.loc[state, 'Volume %'],
        state_analysis.loc[state, 'Spend'],
        state_analysis.loc[state, 'Spend %']
    ))

# ========================================
# 7. COST ANALYSIS
# ========================================
print("\n" + "=" * 60)
print("7. COST ANALYSIS")
print("=" * 60)

total_spend = df['Label Cost'].sum()
avg_cost = df['Label Cost'].mean()
median_cost = df['Label Cost'].median()

print(f"Total Spend (T30): ${total_spend:,.2f}")
print(f"Average Cost per Shipment: ${avg_cost:.2f}")
print(f"Median Cost per Shipment: ${median_cost:.2f}")
print(f"Daily Spend Average: ${total_spend/days_in_period:.2f}")
print(f"Monthly Spend Projection: ${total_spend/days_in_period*30:,.2f}")

# Cost distribution
cost_percentiles = df['Label Cost'].quantile([0.25, 0.5, 0.75, 0.90, 0.95])
print(f"\nCost Distribution Percentiles:")
print(f"  25th percentile: ${cost_percentiles[0.25]:.2f}")
print(f"  50th percentile: ${cost_percentiles[0.50]:.2f}")
print(f"  75th percentile: ${cost_percentiles[0.75]:.2f}")
print(f"  90th percentile: ${cost_percentiles[0.90]:.2f}")
print(f"  95th percentile: ${cost_percentiles[0.95]:.2f}")

# ========================================
# 8. BILLABLE WEIGHT IMPACT
# ========================================
print("\n" + "=" * 60)
print("8. BILLABLE WEIGHT IMPACT ANALYSIS")
print("=" * 60)

def calculate_billable_weight(weight_lb):
    """Apply carrier billable weight rules"""
    if pd.isna(weight_lb):
        return np.nan
    weight_oz = weight_lb * 16
    if weight_oz <= 16:
        # Round up to next oz, max 16
        return min(16, np.ceil(weight_oz)) / 16
    else:
        # Round up to next pound
        return np.ceil(weight_lb)

df['Billable Weight (lb)'] = df['Weight (lb)'].apply(calculate_billable_weight)
df['Weight Uplift (lb)'] = df['Billable Weight (lb)'] - df['Weight (lb)']
df['Weight Uplift %'] = (df['Weight Uplift (lb)'] / df['Weight (lb)']) * 100

# Calculate impact
avg_actual_weight = df['Weight (lb)'].mean()
avg_billable_weight = df['Billable Weight (lb)'].mean()
avg_uplift = avg_billable_weight - avg_actual_weight
avg_uplift_pct = (avg_uplift / avg_actual_weight) * 100

print(f"\nWeight Impact Summary:")
print(f"  Average Actual Weight: {avg_actual_weight:.3f} lb")
print(f"  Average Billable Weight: {avg_billable_weight:.3f} lb")
print(f"  Average Weight Uplift: {avg_uplift:.3f} lb ({avg_uplift_pct:.1f}%)")

# Packages affected by rounding
affected_packages = df[df['Weight Uplift (lb)'] > 0].shape[0]
print(f"\nPackages Affected by Weight Rounding: {affected_packages:,} ({affected_packages/total_volume*100:.1f}%)")

# Estimated cost impact (rough estimate assuming $5/lb average)
estimated_cost_impact = avg_uplift * total_volume * 5
print(f"Estimated Monthly Cost Impact from Weight Rounding: ${estimated_cost_impact:.2f}")

# ========================================
# EXECUTIVE SUMMARY
# ========================================
print("\n" + "=" * 80)
print("EXECUTIVE SUMMARY - UPSTATE PREP T30 ANALYSIS")
print("=" * 80)

print(f"""
VOLUME METRICS:
   - Total Shipments: {total_volume:,}
   - Daily Average: {daily_average:.0f} shipments
   - Monthly Projection: {monthly_projection:.0f} shipments

COST METRICS:
   - Total Spend: ${total_spend:,.2f}
   - Average Cost: ${avg_cost:.2f}/shipment
   - Monthly Projection: ${total_spend/days_in_period*30:,.2f}

CARRIER MIX:
   - Primary Carrier: {carrier_analysis.index[0]} ({carrier_analysis.iloc[0]['Volume']:,} shipments, {carrier_analysis.iloc[0]['Volume %']:.1f}%)
   - Multi-Carrier Strategy: {len(carrier_analysis)} carriers active

PACKAGE PROFILE:
   - Lightweight Focus: {under_1lb:,} packages under 1 lb ({under_1lb/total_volume*100:.1f}%)
   - Average Weight: {avg_actual_weight:.3f} lb (billable: {avg_billable_weight:.3f} lb)
   - Primary Package Type: {box_dist.index[0]} ({box_dist.iloc[0]:,} shipments)

GEOGRAPHIC REACH:
   - Top State: {state_dist.index[0]} ({state_dist.iloc[0]:,} shipments, {state_dist.iloc[0]/total_volume*100:.1f}%)
   - State Coverage: {df['State'].nunique()} unique states

OPTIMIZATION OPPORTUNITIES:
   - Weight Rounding Impact: {avg_uplift_pct:.1f}% uplift on billable weight
   - Lightweight Optimization: {under_16oz:,} packages under 16 oz
   - Cost Savings Potential: Estimated 30-40% with FirstMile dynamic routing
""")

print("\n" + "=" * 80)
print("Analysis Complete - Ready for FirstMile Rate Creation")
print("=" * 80)