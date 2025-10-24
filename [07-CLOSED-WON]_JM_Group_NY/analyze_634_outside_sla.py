"""
Detailed analysis of the 634 in-transit shipments outside SLA window
"""

import pandas as pd
from datetime import datetime

# Configuration
DATA_FILE = r"C:\Users\BrettWalker\FirstMile_Deals\[07-CLOSED-WON]_JM_Group_NY\JM Group NY_FirstMile_Domestic_Tracking_9.30.25.xlsx"
TODAY = pd.Timestamp.now()

# SLA Windows
SLA_WINDOWS = {
    "Ground": 8,
    "Expedited": 5,
    "Priority": 3,
    "Direct Call": 3
}

SERVICE_NAME_MAP = {
    'Ground': 'Xparcel Ground',
    'Expedited': 'Xparcel Expedited',
    'Priority': 'Xparcel Priority',
    'Direct Call': 'Xparcel Priority'
}

print("="*80)
print("DETAILED ANALYSIS: 634 In-Transit Shipments Outside SLA Window")
print("="*80)

# Load data
df = pd.read_excel(DATA_FILE, sheet_name='Export')
print(f"\nTotal shipments in dataset: {len(df)}")

# Filter for in-transit
in_transit = df[df['Delivered Status'] != 'Delivered'].copy()
print(f"Total in-transit shipments: {len(in_transit)}")

# Calculate days since ship
in_transit['Start Date'] = pd.to_datetime(in_transit['Start Date'], errors='coerce')
in_transit['Days Since Ship'] = (TODAY - in_transit['Start Date']).dt.days

# Add SLA window
in_transit['SLA Window'] = in_transit['Xparcel Type'].map(SLA_WINDOWS)
in_transit['Service Name'] = in_transit['Xparcel Type'].map(SERVICE_NAME_MAP)

# Determine if outside SLA window
in_transit['Within SLA Window'] = in_transit.apply(
    lambda r: 'Yes' if pd.notna(r['Days Since Ship']) and pd.notna(r['SLA Window'])
              and r['Days Since Ship'] <= r['SLA Window'] else 'No',
    axis=1
)

# Calculate days late
in_transit['Days Late'] = in_transit.apply(
    lambda r: max(0, r['Days Since Ship'] - r['SLA Window']) if pd.notna(r['Days Since Ship']) and pd.notna(r['SLA Window']) else 0,
    axis=1
)

# Filter for outside SLA window
outside_sla = in_transit[in_transit['Within SLA Window'] == 'No'].copy()

print(f"\n{'='*80}")
print(f"IN-TRANSIT OUTSIDE SLA WINDOW: {len(outside_sla)} shipments")
print(f"{'='*80}")

if len(outside_sla) == 0:
    print("\nNo shipments found outside SLA window!")
    exit()

# Summary by service level
print("\n" + "="*80)
print("BREAKDOWN BY SERVICE LEVEL")
print("="*80)

service_summary = outside_sla.groupby('Service Name').agg({
    'Tracking Number': 'count',
    'Days Since Ship': ['mean', 'median', 'min', 'max'],
    'Days Late': ['mean', 'median', 'min', 'max']
}).round(1)

print(service_summary.to_string())

# Detailed breakdown by service
for service in sorted([s for s in outside_sla['Service Name'].unique() if pd.notna(s)]):
    service_df = outside_sla[outside_sla['Service Name'] == service]
    sla_window = service_df['SLA Window'].iloc[0]

    print(f"\n{'='*80}")
    print(f"{service} ({int(sla_window)}-day SLA)")
    print(f"{'='*80}")
    print(f"Total Outside Window: {len(service_df)}")
    print(f"Average Days Since Ship: {service_df['Days Since Ship'].mean():.1f}")
    print(f"Average Days Late: {service_df['Days Late'].mean():.1f}")
    print(f"Max Days Late: {service_df['Days Late'].max():.0f}")

    # Days late distribution
    print(f"\nDays Late Distribution:")
    days_late_dist = service_df['Days Late'].value_counts().sort_index()
    for days, count in days_late_dist.items():
        pct = (count / len(service_df)) * 100
        print(f"  {int(days)} days late: {count} shipments ({pct:.1f}%)")

# Age buckets
print(f"\n{'='*80}")
print("AGE DISTRIBUTION (Days Since Ship)")
print(f"{'='*80}")

buckets = [
    (0, 5, '0-5 days'),
    (6, 8, '6-8 days'),
    (9, 10, '9-10 days'),
    (11, 15, '11-15 days'),
    (16, 20, '16-20 days'),
    (21, 30, '21-30 days'),
    (31, 999, '31+ days')
]

for min_days, max_days, label in buckets:
    count = len(outside_sla[(outside_sla['Days Since Ship'] >= min_days) &
                            (outside_sla['Days Since Ship'] <= max_days)])
    pct = (count / len(outside_sla)) * 100 if len(outside_sla) > 0 else 0
    print(f"  {label}: {count} ({pct:.1f}%)")

# Top states
print(f"\n{'='*80}")
print("TOP 15 STATES")
print(f"{'='*80}")

state_summary = outside_sla.groupby('Destination State').agg({
    'Tracking Number': 'count',
    'Days Late': 'mean'
}).sort_values('Tracking Number', ascending=False).head(15)
state_summary.columns = ['Count', 'Avg Days Late']
print(state_summary.to_string())

# Top ZIPs
print(f"\n{'='*80}")
print("TOP 20 ZIP CODES")
print(f"{'='*80}")

zip_summary = outside_sla.groupby('Destination Zip').agg({
    'Tracking Number': 'count',
    'Days Late': 'mean',
    'Service Name': lambda x: x.mode()[0] if len(x) > 0 else ''
}).sort_values('Tracking Number', ascending=False).head(20)
zip_summary.columns = ['Count', 'Avg Days Late', 'Primary Service']
print(zip_summary.to_string())

# Zone distribution
print(f"\n{'='*80}")
print("ZONE DISTRIBUTION")
print(f"{'='*80}")

zone_summary = outside_sla.groupby('Calculated Zone').agg({
    'Tracking Number': 'count',
    'Days Late': 'mean'
}).sort_index()
zone_summary.columns = ['Count', 'Avg Days Late']

for zone, row in zone_summary.iterrows():
    if pd.notna(zone):
        pct = (row['Count'] / len(outside_sla)) * 100
        print(f"  Zone {int(zone)}: {int(row['Count'])} ({pct:.1f}%) - Avg {row['Avg Days Late']:.1f} days late")

# Delivered status breakdown
print(f"\n{'='*80}")
print("DELIVERED STATUS BREAKDOWN")
print(f"{'='*80}")

status_counts = outside_sla['Delivered Status'].value_counts()
for status, count in status_counts.items():
    pct = (count / len(outside_sla)) * 100
    print(f"  {status}: {count} ({pct:.1f}%)")

# Most recent scan analysis
print(f"\n{'='*80}")
print("MOST RECENT SCAN ANALYSIS")
print(f"{'='*80}")

if 'Most Recent Scan' in outside_sla.columns:
    scan_summary = outside_sla['Most Recent Scan'].value_counts().head(10)
    print("\nTop 10 Most Recent Scans:")
    for scan, count in scan_summary.items():
        pct = (count / len(outside_sla)) * 100
        print(f"  {scan}: {count} ({pct:.1f}%)")

# Calculate days since last scan
if 'Most Recent Scan Date' in outside_sla.columns:
    outside_sla['Most Recent Scan Date'] = pd.to_datetime(outside_sla['Most Recent Scan Date'], errors='coerce')
    outside_sla['Days Since Last Scan'] = (TODAY - outside_sla['Most Recent Scan Date']).dt.days

    print(f"\nDays Since Last Scan:")
    print(f"  Average: {outside_sla['Days Since Last Scan'].mean():.1f} days")
    print(f"  Median: {outside_sla['Days Since Last Scan'].median():.1f} days")
    print(f"  Max: {outside_sla['Days Since Last Scan'].max():.0f} days")

    # Distribution
    stale_1day = len(outside_sla[outside_sla['Days Since Last Scan'] <= 1])
    stale_3day = len(outside_sla[outside_sla['Days Since Last Scan'] <= 3])
    stale_7day = len(outside_sla[outside_sla['Days Since Last Scan'] <= 7])
    stale_more = len(outside_sla[outside_sla['Days Since Last Scan'] > 7])

    print(f"\n  Scanned within 1 day: {stale_1day} ({stale_1day/len(outside_sla)*100:.1f}%)")
    print(f"  Scanned within 3 days: {stale_3day} ({stale_3day/len(outside_sla)*100:.1f}%)")
    print(f"  Scanned within 7 days: {stale_7day} ({stale_7day/len(outside_sla)*100:.1f}%)")
    print(f"  No scan in 7+ days: {stale_more} ({stale_more/len(outside_sla)*100:.1f}%)")

# Sample records (oldest 20)
print(f"\n{'='*80}")
print("OLDEST 20 SHIPMENTS (Highest Priority)")
print(f"{'='*80}")

oldest = outside_sla.nlargest(20, 'Days Since Ship')
sample_cols = ['Tracking Number', 'Service Name', 'Start Date', 'Days Since Ship', 'Days Late',
               'Delivered Status', 'Most Recent Scan', 'Destination State', 'Destination Zip', 'Calculated Zone']
available_cols = [c for c in sample_cols if c in oldest.columns]

print(oldest[available_cols].to_string(index=False))

# Export to CSV for further analysis
output_file = r"C:\Users\BrettWalker\FirstMile_Deals\[07-CLOSED-WON]_JM_Group_NY\In_Transit_Outside_SLA_Detail.csv"
outside_sla.to_csv(output_file, index=False)

print(f"\n{'='*80}")
print(f"FULL DETAIL EXPORTED TO:")
print(f"{output_file}")
print(f"{'='*80}")

print(f"\nTotal records exported: {len(outside_sla)}")
