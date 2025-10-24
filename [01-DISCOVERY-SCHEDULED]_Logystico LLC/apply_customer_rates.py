import pandas as pd
import numpy as np

# First, let's analyze the rate patterns from the sample data
sample_rates = """Origin Zip Code,Destination Zip Code,Country,Size,Weight (lb),Height (in),Width (in),Length (in),Insurance Amount,Label Cost
07104,17602-1001,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,20723-1351,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,07036-3666,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,33189-1001,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,10952-2888,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,07110-1411,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,97219-7271,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.4
07104,1867,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,89436-8621,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.4
07104,10977-3759,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,10977-5696,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,77375-1272,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,08755-1732,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,60185-3408,US,1.00 x 1.00 x 1.00,0.06,1,1,1,0,3.2
07104,27265-1442,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.2
07104,93923-8416,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.6
07104,91042-3029,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.6
07104,80123-3695,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.4
07104,75244-6928,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.2
07104,02893-7426,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.2
07104,20814-3803,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.2
07104,89074-5393,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.4
07104,30188-3717,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.2
07104,28078-4613,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.2
07104,83646-6787,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.6
07104,92346-2681,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.6
07104,46410-4848,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.2
07104,63123-1476,US,10.00 x 13.00 x 0.10,0.3675,0.1,13,10,0,3.2"""

# Parse sample rates
from io import StringIO
rates_df = pd.read_csv(StringIO(sample_rates))
rates_df['Weight (lb)'] = pd.to_numeric(rates_df['Weight (lb)'])
rates_df['Label Cost'] = pd.to_numeric(rates_df['Label Cost'])

# Extract ZIP prefix for zone determination
rates_df['Dest_Prefix'] = rates_df['Destination Zip Code'].str[:3]

print("CUSTOMER RATE ANALYSIS")
print("="*60)
print("\n1. RATE PATTERNS FROM SAMPLE DATA:")
print("-"*40)

# Analyze rates by weight
weight_rates = rates_df.groupby('Weight (lb)')['Label Cost'].agg(['mean', 'min', 'max', 'count'])
print("\nRates by Weight:")
print(weight_rates)

# Analyze zone patterns (simplified - using first digit of ZIP)
rates_df['Zone_Estimate'] = rates_df['Destination Zip Code'].str[0]
zone_rates = rates_df.groupby(['Weight (lb)', 'Zone_Estimate'])['Label Cost'].mean().unstack(fill_value=0)
print("\nRates by Weight and Zone (estimated):")
print(zone_rates)

# Load Loy shipping data
print("\n" + "="*60)
print("2. LOADING LOY SHIPPING DATA:")
print("-"*40)

loy_df = pd.read_csv('Order Export Loy.csv')
loy_df['Weight (lb)'] = pd.to_numeric(loy_df['Weight (lb)'], errors='coerce')

# Calculate billable weight
def calculate_billable_weight(actual_weight):
    if pd.isna(actual_weight) or actual_weight <= 0:
        return 0
    elif actual_weight < 1:
        oz = actual_weight * 16
        return min(15.99, np.ceil(oz)) / 16
    else:
        return np.ceil(actual_weight)

loy_df['Billable_Weight'] = loy_df['Weight (lb)'].apply(calculate_billable_weight)

# Estimate zones for Loy shipments (using ZIP prefix)
loy_df['Zone_Estimate'] = loy_df['Zip'].astype(str).str[0]

print(f"Total Loy shipments: {len(loy_df)}")
print(f"Shipments with valid weight: {loy_df['Billable_Weight'].notna().sum()}")

# Apply rates based on weight brackets
print("\n" + "="*60)
print("3. APPLYING CUSTOMER RATES TO LOY VOLUME:")
print("-"*40)

# Create rate lookup based on sample data
# For 0.06 lb (1 oz): $3.20-$3.40 depending on zone
# For 0.3675 lb (6 oz): $3.20-$3.60 depending on zone

def estimate_rate(weight, zone):
    """Estimate rate based on weight and zone from sample data"""
    # Convert weight to oz for easier matching
    weight_oz = weight * 16 if weight < 1 else weight
    
    # Base rates from sample data
    if weight_oz <= 1:  # 1 oz
        if zone in ['9', '8']:  # West Coast
            return 3.40
        else:
            return 3.20
    elif weight_oz <= 6:  # 2-6 oz
        if zone in ['9']:  # CA
            return 3.60
        elif zone in ['8']:  # Mountain
            return 3.40
        else:
            return 3.20
    elif weight_oz <= 8:  # 7-8 oz
        # Extrapolate slightly higher
        if zone in ['9']:
            return 3.80
        elif zone in ['8']:
            return 3.60
        else:
            return 3.40
    elif weight_oz <= 16:  # 9-16 oz
        # Progressive increase
        base = 3.60
        increment = (weight_oz - 8) * 0.05
        if zone in ['9']:
            return base + increment + 0.40
        elif zone in ['8']:
            return base + increment + 0.20
        else:
            return base + increment
    else:  # Over 1 lb
        # $0.30-0.40 per pound increment
        base = 4.50
        pounds = np.ceil(weight)
        increment = (pounds - 1) * 0.35
        if zone in ['9']:
            return base + increment + 0.50
        elif zone in ['8']:
            return base + increment + 0.30
        else:
            return base + increment

# Apply rate estimation to Loy data
loy_df['Estimated_Rate'] = loy_df.apply(
    lambda row: estimate_rate(row['Billable_Weight'], row['Zone_Estimate']) 
    if pd.notna(row['Billable_Weight']) else 0, 
    axis=1
)

# Calculate total spend
loy_df['Estimated_Cost'] = loy_df['Estimated_Rate']

# Create summary by weight
weight_summary = []
weight_buckets = [
    (0, 0.0625, "1oz"),
    (0.0625, 0.125, "2oz"),
    (0.125, 0.1875, "3oz"),
    (0.1875, 0.25, "4oz"),
    (0.25, 0.3125, "5oz"),
    (0.3125, 0.375, "6oz"),
    (0.375, 0.4375, "7oz"),
    (0.4375, 0.5, "8oz"),
    (0.5, 0.5625, "9oz"),
    (0.5625, 0.625, "10oz"),
    (0.625, 0.6875, "11oz"),
    (0.6875, 0.75, "12oz"),
    (0.75, 0.8125, "13oz"),
    (0.8125, 0.875, "14oz"),
    (0.875, 0.9375, "15oz"),
    (0.9375, 0.9994, "15.99oz"),
    (0.9994, 1.5, "1lb"),
    (1.5, 2.5, "2lb"),
    (2.5, 3.5, "3lb"),
    (3.5, 4.5, "4lb"),
    (4.5, 5.5, "5lb"),
    (5.5, 6.5, "6lb"),
    (6.5, 7.5, "7lb"),
    (7.5, 8.5, "8lb"),
    (8.5, 9.5, "9lb"),
    (9.5, 10.5, "10lb"),
    (10.5, 15.5, "11-15lb"),
    (15.5, 20.5, "16-20lb"),
    (20.5, 30, "21-30lb"),
    (30, 1000, "30lb+")
]

print("\n" + "="*60)
print("4. COST ANALYSIS BY WEIGHT:")
print("-"*40)
print(f"{'Weight Range':<15} {'Count':>8} {'Avg Rate':>10} {'Total Cost':>12}")
print("-"*40)

total_volume = 0
total_cost = 0

for min_w, max_w, label in weight_buckets:
    mask = (loy_df['Billable_Weight'] > min_w) & (loy_df['Billable_Weight'] <= max_w)
    count = mask.sum()
    if count > 0:
        avg_rate = loy_df[mask]['Estimated_Rate'].mean()
        range_cost = loy_df[mask]['Estimated_Cost'].sum()
        print(f"{label:<15} {count:>8} ${avg_rate:>9.2f} ${range_cost:>11.2f}")
        total_volume += count
        total_cost += range_cost

print("-"*40)
print(f"{'TOTAL':<15} {total_volume:>8} {'':>10} ${total_cost:>11.2f}")

# Monthly projection
print("\n" + "="*60)
print("5. MONTHLY SHIPPING SPEND PROJECTION:")
print("-"*40)

# Assuming data represents a typical month
days_in_data = (pd.to_datetime(loy_df['Created at']).max() - pd.to_datetime(loy_df['Created at']).min()).days
if days_in_data > 0:
    daily_avg_cost = total_cost / days_in_data
    monthly_projection = daily_avg_cost * 30
    annual_projection = monthly_projection * 12
else:
    monthly_projection = total_cost
    annual_projection = total_cost * 12

print(f"Data Period: {days_in_data} days")
print(f"Total Volume: {total_volume:,} packages")
print(f"Total Cost in Period: ${total_cost:,.2f}")
print(f"Daily Average: ${daily_avg_cost:,.2f}" if days_in_data > 0 else "N/A")
print(f"Monthly Projection: ${monthly_projection:,.2f}")
print(f"Annual Projection: ${annual_projection:,.2f}")

# Cost per package metrics
print("\n" + "-"*40)
print("COST PER PACKAGE METRICS:")
print(f"Average Cost per Package: ${total_cost/total_volume:.2f}")
print(f"Median Cost per Package: ${loy_df[loy_df['Estimated_Cost'] > 0]['Estimated_Cost'].median():.2f}")

# Zone distribution cost
print("\n" + "-"*40)
print("COST BY ZONE (ESTIMATED):")
zone_summary = loy_df[loy_df['Estimated_Cost'] > 0].groupby('Zone_Estimate').agg({
    'Estimated_Cost': ['count', 'sum', 'mean']
}).round(2)
zone_summary.columns = ['Volume', 'Total Cost', 'Avg Cost']
print(zone_summary)

print("\n" + "="*60)
print("NOTE: Rates are estimated based on limited sample data")
print("Actual rates may vary by service level, contract terms, and zones")