import pandas as pd
import numpy as np
from datetime import datetime
import sys

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

# Load the data
df = pd.read_csv('IronLink Orders Report.csv')
df['object created'] = pd.to_datetime(df['object created'])

print('=== FIRSTMILE OPPORTUNITY ANALYSIS FOR IRONLINK ===\n')

# Calculate daily average
days_in_period = (df['object created'].max() - df['object created'].min()).days + 1
daily_avg = len(df) / days_in_period

print(f'Analysis Period: {df["object created"].min().date()} to {df["object created"].max().date()} ({days_in_period} days)')
print(f'Total Shipments: {len(df):,}')
print(f'Daily Average: {daily_avg:.0f} shipments/day\n')

# Service mix for FirstMile mapping
print('=== SERVICE MIX ANALYSIS ===')
service_mapping = {
    'Ground': 'Xparcel Ground (3-8 d)',
    'Ground Advantage': 'Xparcel Ground (3-8 d)',
    'Surepost': 'Xparcel Ground (3-8 d)',
    'Standard℠': 'Xparcel Ground (3-8 d)',
    '2nd Day Air®': 'Xparcel Expedited (2-5 d)',
    '3 Day Select®': 'Xparcel Expedited (2-5 d)',
    'Expedited®': 'Xparcel Expedited (2-5 d)',
    'Next Day Air®': 'Xparcel Priority (1-3 d)',
    'Next Day Air Saver®': 'Xparcel Priority (1-3 d)',
    'Standard Overnight®': 'Xparcel Priority (1-3 d)',
    'Worldwide Expedited®': 'International'
}

# Map services
df['firstmile_service'] = df['rate__servicelevel__servicelevel_name'].map(service_mapping)
df['firstmile_service'] = df['firstmile_service'].fillna('Other')

service_summary = df['firstmile_service'].value_counts()
for service, count in service_summary.items():
    pct = count / len(df) * 100
    print(f'  {service}: {count:,} ({pct:.1f}%)')

# Zone analysis based on state distance from origin states
print('\n=== GEOGRAPHIC DISTRIBUTION FOR ZONE ANALYSIS ===')
# Main origins are in NJ, CA, TX based on the data
origin_states = df['rate__shipment__address_from__state'].value_counts().head(5)
print('Top Origin States:')
for state, count in origin_states.items():
    print(f'  {state}: {count:,} ({count/len(df)*100:.1f}%)')

print('\nTop Destination Regions:')
# Regional grouping
west_states = ['CA', 'WA', 'OR', 'NV', 'AZ', 'CO', 'UT', 'ID', 'MT', 'WY', 'NM']
central_states = ['TX', 'OK', 'KS', 'NE', 'SD', 'ND', 'MN', 'IA', 'MO', 'AR', 'LA', 'WI', 'IL', 'IN', 'MI', 'OH', 'KY', 'TN', 'MS', 'AL']
east_states = ['FL', 'GA', 'SC', 'NC', 'VA', 'WV', 'MD', 'DE', 'PA', 'NJ', 'NY', 'CT', 'RI', 'MA', 'VT', 'NH', 'ME']

df['region'] = 'Other'
df.loc[df['rate__shipment__address_to__state'].isin(west_states), 'region'] = 'West'
df.loc[df['rate__shipment__address_to__state'].isin(central_states), 'region'] = 'Central'
df.loc[df['rate__shipment__address_to__state'].isin(east_states), 'region'] = 'East'

region_dist = df['region'].value_counts()
for region, count in region_dist.items():
    print(f'  {region}: {count:,} ({count/len(df)*100:.1f}%)')

# Weight profile for pricing
print('\n=== WEIGHT PROFILE FOR PRICING ===')
weight_ranges = {
    '0-1 lb': (df['parcel__weight'] <= 1).sum(),
    '1-5 lb': ((df['parcel__weight'] > 1) & (df['parcel__weight'] <= 5)).sum(),
    '5-20 lb': ((df['parcel__weight'] > 5) & (df['parcel__weight'] <= 20)).sum(),
    '>20 lb': (df['parcel__weight'] > 20).sum()
}

for range_name, count in weight_ranges.items():
    pct = count / len(df) * 100
    print(f'  {range_name}: {count:,} ({pct:.1f}%)')

# FirstMile network fit
print('\n=== FIRSTMILE NETWORK FIT ===')
# Calculate Select network eligibility (metro areas + <5lb)
select_metros = ['CA', 'TX', 'IL', 'NY', 'NJ', 'GA', 'FL']
select_eligible = df[(df['rate__shipment__address_to__state'].isin(select_metros)) & (df['parcel__weight'] <= 5)].shape[0]
national_volume = len(df) - select_eligible

print(f'  Select Network (Metro Zone-Skip): {select_eligible:,} ({select_eligible/len(df)*100:.1f}%)')
print(f'  National Network (Full Coverage): {national_volume:,} ({national_volume/len(df)*100:.1f}%)')

# Delivery performance opportunity
print('\n=== DELIVERY PERFORMANCE OPPORTUNITY ===')
print(f'  Current Delivery Rate: {(df["tracking_status"] == "DELIVERED").sum() / len(df) * 100:.1f}%')
print(f'  In-Transit/Pre-Transit: {((df["tracking_status"] == "TRANSIT") | (df["tracking_status"] == "PRE_TRANSIT")).sum():,} shipments')
print(f'  Failed/Returned: {((df["tracking_status"] == "FAILURE") | (df["tracking_status"] == "RETURNED")).sum():,} shipments')

# Cost savings estimate
print('\n=== ESTIMATED FIRSTMILE SAVINGS ===')
avg_current_cost = 8.50  # Typical UPS Ground cost
firstmile_cost = 5.10    # FirstMile average
annual_volume = len(df) * (365 / days_in_period)
annual_savings = annual_volume * (avg_current_cost - firstmile_cost)

print(f'  Estimated Annual Volume: {annual_volume:,.0f} shipments')
print(f'  Average Cost Reduction: ${avg_current_cost - firstmile_cost:.2f}/shipment (40% savings)')
print(f'  Projected Annual Savings: ${annual_savings:,.2f}')