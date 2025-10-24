import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load the data
print("="*80)
print("DYLN FULFILLMENT - COMPLETE VOLUME ANALYSIS")
print("="*80)

df = pd.read_excel('DYLN Fulfillment - Shipments.xlsx')

# 1. VOLUME PROFILE
print("\n" + "="*60)
print("1. VOLUME PROFILE")
print("="*60)

total_shipments = len(df)
date_range = df['shipment_date'].max() - df['shipment_date'].min()
days_in_range = date_range.days + 1

# Calculate daily average (excluding weekends for business days)
df['weekday'] = df['shipment_date'].dt.dayofweek
business_days = df[df['weekday'] < 5]['shipment_date'].dt.date.nunique()
daily_avg = total_shipments / business_days if business_days > 0 else 0

# Monthly breakdown
df['month'] = df['shipment_date'].dt.to_period('M')
monthly_volume = df.groupby('month').size()

print(f"Total Shipments: {total_shipments:,}")
print(f"Date Range: {df['shipment_date'].min().date()} to {df['shipment_date'].max().date()} ({days_in_range} days)")
print(f"Business Days in Range: {business_days}")
print(f"Daily Average (Business Days): {daily_avg:.0f} shipments")
print(f"Unique Orders: {df['order'].nunique():,}")

print("\nMonthly Volume:")
for month, volume in monthly_volume.items():
    print(f"  {month}: {volume:,} shipments")

# 2. WEIGHT DISTRIBUTION ANALYSIS
print("\n" + "="*60)
print("2. EXPANDED WEIGHT DISTRIBUTION")
print("="*60)

# Convert weight to pounds for analysis
df['weight_lbs'] = df['Weight (oz)'] / 16

# Billable weight calculation (FirstMile rules)
def calculate_billable_weight(weight_oz):
    if weight_oz <= 0:
        return 0
    elif weight_oz < 16:
        # Under 1 lb: round UP to next whole oz, max 15.99
        return min(np.ceil(weight_oz), 15.99)
    else:
        # Over 1 lb: round UP to next whole pound
        weight_lbs = weight_oz / 16
        return np.ceil(weight_lbs) * 16

df['billable_weight_oz'] = df['Weight (oz)'].apply(calculate_billable_weight)
df['billable_weight_lbs'] = df['billable_weight_oz'] / 16

# Weight categories
weight_categories = []
weight_volumes = []
weight_percentages = []

# Under 1 lb detailed breakdown
under_1lb = df[df['Weight (oz)'] < 16]
categories_under_1lb = [
    (0, 4, "0-4 oz"),
    (4, 8, "5-8 oz"),
    (8, 12, "9-12 oz"),
    (12, 15, "13-15 oz"),
    (15, 15.99, "15-15.99 oz"),
    (15.99, 16, "Exactly 16 oz")
]

print("Under 1 lb breakdown:")
for min_oz, max_oz, label in categories_under_1lb:
    if max_oz == 16:
        count = len(df[(df['Weight (oz)'] >= min_oz) & (df['Weight (oz)'] <= max_oz)])
    else:
        count = len(df[(df['Weight (oz)'] > min_oz) & (df['Weight (oz)'] <= max_oz)])
    pct = (count / total_shipments) * 100
    weight_categories.append(label)
    weight_volumes.append(count)
    weight_percentages.append(pct)
    print(f"  {label:15} {count:6,} ({pct:5.1f}%)")

# 1-5 lbs breakdown by pound
print("\n1-5 lbs breakdown:")
for lb in range(1, 6):
    min_oz = lb * 16
    max_oz = (lb + 1) * 16
    count = len(df[(df['Weight (oz)'] > min_oz) & (df['Weight (oz)'] <= max_oz)])
    pct = (count / total_shipments) * 100
    label = f"{lb}-{lb+1} lbs"
    weight_categories.append(label)
    weight_volumes.append(count)
    weight_percentages.append(pct)
    print(f"  {label:15} {count:6,} ({pct:5.1f}%)")

# Over 5 lbs
over_5lbs = len(df[df['weight_lbs'] > 5])
pct_over_5 = (over_5lbs / total_shipments) * 100
weight_categories.append("Over 5 lbs")
weight_volumes.append(over_5lbs)
weight_percentages.append(pct_over_5)
print(f"\nOver 5 lbs:        {over_5lbs:6,} ({pct_over_5:5.1f}%)")

# Key weight statistics
print("\nWeight Statistics:")
print(f"  Average Weight: {df['Weight (oz)'].mean():.2f} oz ({df['weight_lbs'].mean():.2f} lbs)")
print(f"  Median Weight: {df['Weight (oz)'].median():.2f} oz ({df['weight_lbs'].median():.2f} lbs)")
print(f"  Min Weight: {df['Weight (oz)'].min():.2f} oz")
print(f"  Max Weight: {df['Weight (oz)'].max():.2f} oz ({df['weight_lbs'].max():.2f} lbs)")

# 3. BILLABLE WEIGHT IMPACT
print("\n" + "="*60)
print("3. BILLABLE WEIGHT IMPACT ANALYSIS")
print("="*60)

actual_total_oz = df['Weight (oz)'].sum()
billable_total_oz = df['billable_weight_oz'].sum()
weight_uplift_pct = ((billable_total_oz - actual_total_oz) / actual_total_oz) * 100

print(f"Total Actual Weight: {actual_total_oz:,.0f} oz ({actual_total_oz/16:,.0f} lbs)")
print(f"Total Billable Weight: {billable_total_oz:,.0f} oz ({billable_total_oz/16:,.0f} lbs)")
print(f"Weight Uplift: {weight_uplift_pct:.1f}%")

# Billable weight distribution
print("\nBillable Weight Distribution:")
billable_categories = [
    (0, 1, "Billable <=1 lb"),
    (1, 2, "Billable 2 lbs"),
    (2, 3, "Billable 3 lbs"),
    (3, 5, "Billable 4-5 lbs"),
    (5, 999, "Billable >5 lbs")
]

for min_lbs, max_lbs, label in billable_categories:
    count = len(df[(df['billable_weight_lbs'] > min_lbs) & (df['billable_weight_lbs'] <= max_lbs)])
    pct = (count / total_shipments) * 100
    print(f"  {label:20} {count:6,} ({pct:5.1f}%)")

# 4. GEOGRAPHIC DISTRIBUTION
print("\n" + "="*60)
print("4. GEOGRAPHIC DISTRIBUTION")
print("="*60)

# Top states
state_volume = df.groupby('state').size().sort_values(ascending=False)
print("Top 10 Destination States:")
for i, (state, volume) in enumerate(state_volume.head(10).items(), 1):
    pct = (volume / total_shipments) * 100
    print(f"  {i:2}. {state:3} {volume:6,} ({pct:5.1f}%)")

# Domestic vs International
domestic = df[df['country'] == 'US']
international = df[df['country'] != 'US']
domestic_pct = (len(domestic) / total_shipments) * 100
intl_pct = (len(international) / total_shipments) * 100

print(f"\nDomestic vs International:")
print(f"  Domestic (US): {len(domestic):,} ({domestic_pct:.1f}%)")
print(f"  International: {len(international):,} ({intl_pct:.1f}%)")

if len(international) > 0:
    print("\nTop International Countries:")
    intl_countries = international.groupby('country').size().sort_values(ascending=False)
    for country, volume in intl_countries.head(5).items():
        pct = (volume / total_shipments) * 100
        print(f"  {country}: {volume:,} ({pct:.1f}%)")

# 5. PACKAGE TYPE ANALYSIS
print("\n" + "="*60)
print("5. PACKAGE TYPE DISTRIBUTION")
print("="*60)

package_types = df.groupby('Package').agg({
    'order': 'count',
    'Weight (oz)': 'mean'
}).rename(columns={'order': 'Volume', 'Weight (oz)': 'Avg Weight (oz)'})
package_types['% of Total'] = (package_types['Volume'] / total_shipments) * 100
package_types = package_types.sort_values('Volume', ascending=False)

print("Package Types Used:")
for package, row in package_types.iterrows():
    print(f"  {package:25} {row['Volume']:6,} ({row['% of Total']:5.1f}%) - Avg {row['Avg Weight (oz)']:.1f} oz")

# 6. SHIPPING PATTERNS
print("\n" + "="*60)
print("6. SHIPPING PATTERNS")
print("="*60)

# Day of week analysis
weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_volume = df.groupby('weekday').size()

print("Shipments by Day of Week:")
for day in range(7):
    if day in weekday_volume.index:
        volume = weekday_volume[day]
        pct = (volume / total_shipments) * 100
        print(f"  {weekday_names[day]:10} {volume:6,} ({pct:5.1f}%)")

# Hourly patterns
df['hour'] = df['shipment_date'].dt.hour
peak_hours = df.groupby('hour').size().sort_values(ascending=False).head(5)

print("\nTop 5 Peak Shipping Hours:")
for hour, volume in peak_hours.items():
    pct = (volume / total_shipments) * 100
    print(f"  {hour:02d}:00-{hour:02d}:59  {volume:6,} ({pct:5.1f}%)")

# 7. FIRSTMILE OPTIMIZATION OPPORTUNITIES
print("\n" + "="*60)
print("7. FIRSTMILE XPARCEL OPTIMIZATION OPPORTUNITIES")
print("="*60)

# Lightweight package opportunity
lightweight = df[df['Weight (oz)'] <= 16]
lightweight_pct = (len(lightweight) / total_shipments) * 100

print(f"Lightweight Package Opportunity (<1 lb):")
print(f"  Volume: {len(lightweight):,} shipments ({lightweight_pct:.1f}%)")
print(f"  Perfect for Xparcel Ground via Select Network")

# Zone-skipping opportunity (assuming lightweight goes to major metros)
top_5_states = state_volume.head(5).index.tolist()
metro_eligible = df[df['state'].isin(top_5_states)]
metro_pct = (len(metro_eligible) / total_shipments) * 100

print(f"\nMetro Zone-Skip Opportunity:")
print(f"  Top 5 States Volume: {len(metro_eligible):,} ({metro_pct:.1f}%)")
print(f"  Eligible for Select Network injection points")

# Service level recommendations
print("\nRecommended Service Mix:")
ground_eligible = df[df['Weight (oz)'] <= 16]
expedited_eligible = df[(df['Weight (oz)'] > 16) & (df['Weight (oz)'] <= 320)]  # 1-20 lbs
priority_eligible = df[df['Weight (oz)'] > 320]

print(f"  Xparcel Ground (3-8 days):     {len(ground_eligible):,} ({len(ground_eligible)/total_shipments*100:.1f}%)")
print(f"  Xparcel Expedited (2-5 days):  {len(expedited_eligible):,} ({len(expedited_eligible)/total_shipments*100:.1f}%)")
print(f"  Xparcel Priority (1-3 days):   {len(priority_eligible):,} ({len(priority_eligible)/total_shipments*100:.1f}%)")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)