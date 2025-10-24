import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter

# Load the data
df = pd.read_csv('247bef97-8663-431e-b2f5-dd2ca243633d.csv')

print("=" * 80)
print("JOSH'S FROGS - PLD (PARCEL LEVEL DETAIL) ANALYSIS")
print("=" * 80)
print()

# Extract date from Number field (format: YYYY-MM-DD-XXXX-X)
df['date'] = pd.to_datetime(df['Number'].str[:10], format='%Y-%m-%d', errors='coerce')

# 1. VOLUME PROFILE
print("1. VOLUME PROFILE")
print("-" * 40)
total_shipments = len(df)
date_range = f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}" if df['date'].notna().any() else "N/A"
days_in_range = (df['date'].max() - df['date'].min()).days + 1 if df['date'].notna().any() else 1
daily_average = total_shipments / days_in_range if days_in_range > 0 else total_shipments

print(f"Total Shipments: {total_shipments:,}")
print(f"Date Range: {date_range}")
print(f"Daily Average: {daily_average:.1f}")
print()

# 2. CARRIER MIX
print("2. CARRIER MIX")
print("-" * 40)
carrier_mix = df.groupby('Carrier').agg({
    'Number': 'count',
    'Cost': 'sum'
}).rename(columns={'Number': 'Volume'})
carrier_mix['Volume %'] = (carrier_mix['Volume'] / total_shipments * 100).round(1)
carrier_mix['Spend %'] = (carrier_mix['Cost'] / df['Cost'].sum() * 100).round(1)
carrier_mix['Avg Cost'] = (carrier_mix['Cost'] / carrier_mix['Volume']).round(2)
print(carrier_mix.to_string())
print()

# 3. SERVICE LEVEL DISTRIBUTION
print("3. SERVICE LEVEL DISTRIBUTION")
print("-" * 40)
service_dist = df.groupby('Service').agg({
    'Number': 'count',
    'Cost': 'sum'
}).rename(columns={'Number': 'Volume'})
service_dist['Volume %'] = (service_dist['Volume'] / total_shipments * 100).round(1)
service_dist['Spend %'] = (service_dist['Cost'] / df['Cost'].sum() * 100).round(1)
service_dist['Avg Cost'] = (service_dist['Cost'] / service_dist['Volume']).round(2)
print(service_dist.to_string())
print()

# 4. EXPANDED WEIGHT DISTRIBUTION
print("4. EXPANDED WEIGHT DISTRIBUTION")
print("-" * 40)

# Convert weight to ounces for detailed analysis
df['weight_oz'] = df['Weight'] * 16

# Calculate billable weight
def calculate_billable_weight(weight_oz):
    if weight_oz <= 16:
        # Under 1 lb: round up to next whole oz, max 15.99
        return min(np.ceil(weight_oz), 15.99)
    else:
        # Over 1 lb: round up to next whole pound
        return np.ceil(weight_oz / 16) * 16

df['billable_oz'] = df['weight_oz'].apply(calculate_billable_weight)
df['billable_lbs'] = df['billable_oz'] / 16

# Weight categories
weight_cats = []
for _, row in df.iterrows():
    weight_oz = row['weight_oz']
    if weight_oz <= 4:
        weight_cats.append('1-4 oz')
    elif weight_oz <= 8:
        weight_cats.append('5-8 oz')
    elif weight_oz <= 12:
        weight_cats.append('9-12 oz')
    elif weight_oz <= 15:
        weight_cats.append('13-15 oz')
    elif weight_oz <= 15.99:
        weight_cats.append('15.01-15.99 oz')
    elif weight_oz == 16:
        weight_cats.append('16 oz exactly')
    elif weight_oz <= 32:
        weight_cats.append('1-2 lbs')
    elif weight_oz <= 48:
        weight_cats.append('2-3 lbs')
    elif weight_oz <= 64:
        weight_cats.append('3-4 lbs')
    elif weight_oz <= 80:
        weight_cats.append('4-5 lbs')
    else:
        weight_cats.append('Over 5 lbs')

df['weight_category'] = weight_cats

weight_dist = df.groupby('weight_category').agg({
    'Number': 'count',
    'Cost': 'sum'
}).rename(columns={'Number': 'Volume'})
weight_dist['Volume %'] = (weight_dist['Volume'] / total_shipments * 100).round(1)
weight_dist['Spend %'] = (weight_dist['Cost'] / df['Cost'].sum() * 100).round(1)
weight_dist['Avg Cost'] = (weight_dist['Cost'] / weight_dist['Volume']).round(2)

# Order categories properly
category_order = ['1-4 oz', '5-8 oz', '9-12 oz', '13-15 oz', '15.01-15.99 oz', 
                  '16 oz exactly', '1-2 lbs', '2-3 lbs', '3-4 lbs', '4-5 lbs', 'Over 5 lbs']
weight_dist = weight_dist.reindex([c for c in category_order if c in weight_dist.index])
print(weight_dist.to_string())
print()

# Billable weight by pound for 1-5 lb range
print("Billable Weight Distribution (1-5 lbs):")
billable_1to5 = df[(df['billable_lbs'] >= 1) & (df['billable_lbs'] <= 5)].copy()
if not billable_1to5.empty:
    billable_dist = billable_1to5.groupby('billable_lbs').agg({
        'Number': 'count',
        'Cost': 'sum'
    }).rename(columns={'Number': 'Volume'})
    billable_dist['Spend %'] = (billable_dist['Cost'] / billable_1to5['Cost'].sum() * 100).round(1)
    print(billable_dist.to_string())
print()

# 5. DIMENSIONAL ANALYSIS
print("5. DIMENSIONAL ANALYSIS")
print("-" * 40)
# Filter out rows with missing dimensions
dims_df = df.dropna(subset=['Length', 'Width', 'Height'])
if not dims_df.empty:
    dims_df['cubic_inches'] = dims_df['Length'] * dims_df['Width'] * dims_df['Height']
    dims_df['cubic_feet'] = dims_df['cubic_inches'] / 1728
    
    print(f"Packages with dimensions: {len(dims_df):,} ({len(dims_df)/total_shipments*100:.1f}%)")
    print(f"Average dimensions: {dims_df['Length'].mean():.1f}L x {dims_df['Width'].mean():.1f}W x {dims_df['Height'].mean():.1f}H")
    print(f"Average cubic inches: {dims_df['cubic_inches'].mean():.1f}")
    print(f"Packages < 1 cu ft: {(dims_df['cubic_feet'] < 1).sum():,} ({(dims_df['cubic_feet'] < 1).sum()/len(dims_df)*100:.1f}%)")
    print(f"Packages >= 1 cu ft: {(dims_df['cubic_feet'] >= 1).sum():,} ({(dims_df['cubic_feet'] >= 1).sum()/len(dims_df)*100:.1f}%)")
else:
    print("No dimensional data available")
print()

# 6. ZONE DISTRIBUTION
print("6. ZONE DISTRIBUTION")
print("-" * 40)
# Extract origin and destination ZIP3
df['origin_zip3'] = df['Origin'].str[:3]
df['dest_zip3'] = df['Destination'].astype(str).str[:3]

# Simple zone estimation based on ZIP3 difference
def estimate_zone(origin_zip3, dest_zip3):
    try:
        diff = abs(int(origin_zip3) - int(dest_zip3))
        if diff <= 100:
            return 'Zone 1-2 (Local)'
        elif diff <= 300:
            return 'Zone 3-4 (Regional)'
        elif diff <= 500:
            return 'Zone 5-6 (National)'
        else:
            return 'Zone 7-8 (Cross-Country)'
    except:
        return 'Unknown'

df['zone_estimate'] = df.apply(lambda x: estimate_zone(x['origin_zip3'], x['dest_zip3']), axis=1)

zone_dist = df.groupby('zone_estimate').agg({
    'Number': 'count',
    'Cost': 'sum'
}).rename(columns={'Number': 'Volume'})
zone_dist['Volume %'] = (zone_dist['Volume'] / total_shipments * 100).round(1)
zone_dist['Spend %'] = (zone_dist['Cost'] / df['Cost'].sum() * 100).round(1)
zone_dist['Avg Cost'] = (zone_dist['Cost'] / zone_dist['Volume']).round(2)
print(zone_dist.to_string())
print()

# Regional vs Cross-Country
regional = df[df['zone_estimate'].isin(['Zone 1-2 (Local)', 'Zone 3-4 (Regional)'])]
cross_country = df[df['zone_estimate'].isin(['Zone 5-6 (National)', 'Zone 7-8 (Cross-Country)'])]
print(f"Regional (Zones 1-4): {len(regional):,} ({len(regional)/total_shipments*100:.1f}%)")
print(f"Cross-Country (Zones 5-8): {len(cross_country):,} ({len(cross_country)/total_shipments*100:.1f}%)")
print()

# 7. GEOGRAPHIC DISTRIBUTION
print("7. GEOGRAPHIC DISTRIBUTION (TOP 10 STATES)")
print("-" * 40)
# Map ZIP to state (simplified - using first 3 digits)
zip_to_state = {
    range(10, 28): 'MA', range(28, 30): 'RI', range(30, 39): 'NH',
    range(39, 50): 'ME', range(50, 60): 'VT', range(60, 70): 'CT',
    range(100, 150): 'NY', range(70, 90): 'NJ', range(150, 197): 'PA',
    range(197, 200): 'DE', range(200, 213): 'DC', range(206, 221): 'MD',
    range(220, 247): 'VA', range(247, 269): 'WV', range(270, 290): 'NC',
    range(290, 300): 'SC', range(300, 320): 'GA', range(320, 340): 'FL',
    range(350, 370): 'AL', range(370, 380): 'TN', range(380, 400): 'MS',
    range(400, 428): 'KY', range(430, 460): 'OH', range(460, 480): 'IN',
    range(480, 500): 'MI', range(500, 529): 'IA', range(530, 550): 'WI',
    range(550, 568): 'MN', range(570, 580): 'SD', range(580, 590): 'ND',
    range(600, 630): 'IL', range(630, 660): 'MO', range(660, 680): 'KS',
    range(680, 694): 'NE', range(700, 715): 'LA', range(716, 730): 'AR',
    range(730, 750): 'OK', range(750, 800): 'TX', range(800, 817): 'CO',
    range(820, 832): 'WY', range(832, 839): 'ID', range(840, 848): 'UT',
    range(850, 866): 'AZ', range(870, 885): 'NM', range(889, 899): 'NV',
    range(900, 962): 'CA', range(970, 979): 'OR', range(980, 995): 'WA',
    range(995, 1000): 'AK', range(967, 969): 'HI'
}

def get_state(zip_code):
    try:
        zip3 = int(str(zip_code)[:3])
        for range_obj, state in zip_to_state.items():
            if zip3 in range_obj:
                return state
    except:
        pass
    return 'Unknown'

df['dest_state'] = df['Destination'].apply(get_state)

state_dist = df['dest_state'].value_counts().head(10)
state_costs = df.groupby('dest_state')['Cost'].sum()

print("State     Volume    Volume%    Total Spend    Avg Cost")
print("-" * 55)
for state in state_dist.index:
    volume = state_dist[state]
    volume_pct = volume / total_shipments * 100
    total_cost = state_costs.get(state, 0)
    avg_cost = total_cost / volume if volume > 0 else 0
    print(f"{state:8} {volume:8,} {volume_pct:7.1f}% ${total_cost:11,.2f} ${avg_cost:7.2f}")
print()

# 8. COST ANALYSIS
print("8. COST ANALYSIS")
print("-" * 40)
total_spend = df['Cost'].sum()
avg_cost = df['Cost'].mean()
median_cost = df['Cost'].median()
min_cost = df['Cost'].min()
max_cost = df['Cost'].max()

print(f"Total Spend: ${total_spend:,.2f}")
print(f"Average Cost: ${avg_cost:.2f}")
print(f"Median Cost: ${median_cost:.2f}")
print(f"Min Cost: ${min_cost:.2f}")
print(f"Max Cost: ${max_cost:.2f}")
print()

# Cost distribution
cost_ranges = ['$0-5', '$5-7', '$7-9', '$9-11', '$11+']
cost_bins = [0, 5, 7, 9, 11, float('inf')]
df['cost_range'] = pd.cut(df['Cost'], bins=cost_bins, labels=cost_ranges)

cost_dist = df.groupby('cost_range').agg({
    'Number': 'count',
    'Cost': 'sum'
}).rename(columns={'Number': 'Volume'})
cost_dist['Volume %'] = (cost_dist['Volume'] / total_shipments * 100).round(1)
cost_dist['Spend %'] = (cost_dist['Cost'] / total_spend * 100).round(1)
print(cost_dist.to_string())
print()

# 9. BILLABLE WEIGHT IMPACT
print("9. BILLABLE WEIGHT IMPACT")
print("-" * 40)
df['weight_difference_oz'] = df['billable_oz'] - df['weight_oz']
df['weight_difference_pct'] = (df['weight_difference_oz'] / df['weight_oz'] * 100)

avg_actual = df['weight_oz'].mean()
avg_billable = df['billable_oz'].mean()
avg_difference = df['weight_difference_oz'].mean()
avg_difference_pct = df['weight_difference_pct'].mean()

print(f"Average Actual Weight: {avg_actual:.1f} oz ({avg_actual/16:.2f} lbs)")
print(f"Average Billable Weight: {avg_billable:.1f} oz ({avg_billable/16:.2f} lbs)")
print(f"Average Difference: {avg_difference:.1f} oz ({avg_difference_pct:.1f}% increase)")
print()

# Packages most impacted by billable weight rules
high_impact = df[df['weight_difference_pct'] > 25].copy()
print(f"Packages with >25% billable weight increase: {len(high_impact):,} ({len(high_impact)/total_shipments*100:.1f}%)")
if not high_impact.empty:
    print(f"Average cost of high-impact packages: ${high_impact['Cost'].mean():.2f}")
    print(f"Total spend on high-impact packages: ${high_impact['Cost'].sum():,.2f}")

print()
print("=" * 80)
print("OPTIMIZATION OPPORTUNITIES")
print("=" * 80)

# Key insights
under_1lb = df[df['Weight'] < 1]
print(f"• {len(under_1lb):,} packages ({len(under_1lb)/total_shipments*100:.1f}%) under 1 lb - focus area for optimization")
print(f"  Total spend: ${under_1lb['Cost'].sum():,.2f} ({under_1lb['Cost'].sum()/total_spend*100:.1f}% of total)")

near_threshold = df[(df['weight_oz'] > 14) & (df['weight_oz'] < 16)]
print(f"• {len(near_threshold):,} packages near 16 oz threshold - potential for weight optimization")

usps_packages = df[df['Carrier'] == 'USPS']
ups_packages = df[df['Carrier'] == 'UPS']
print(f"• USPS dominates with {len(usps_packages):,} packages ({len(usps_packages)/total_shipments*100:.1f}%)")
print(f"  Average USPS cost: ${usps_packages['Cost'].mean():.2f}")
if not ups_packages.empty:
    print(f"  Average UPS cost: ${ups_packages['Cost'].mean():.2f} ({(ups_packages['Cost'].mean()/usps_packages['Cost'].mean()-1)*100:.1f}% higher)")

print("\n" + "=" * 80)