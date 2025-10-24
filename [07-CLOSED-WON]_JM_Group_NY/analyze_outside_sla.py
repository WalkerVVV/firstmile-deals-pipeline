"""
Analyze in-transit shipments showing as outside SLA window
"""

import pandas as pd
from datetime import datetime

# Load data
DATA_FILE = r"C:\Users\BrettWalker\FirstMile_Deals\[07-CLOSED-WON]_JM_Group_NY\JM Group NY_FirstMile_Domestic_Tracking_9.30.25.xlsx"
df = pd.read_excel(DATA_FILE)

print("="*80)
print("Analysis of In-Transit Shipments Outside SLA Window")
print("="*80)

# Filter for in-transit only
in_transit = df[df['Delivered Status'] != 'Delivered'].copy()

print(f"\nTotal In-Transit Shipments: {len(in_transit)}")
print(f"Service Level: Xparcel Ground (8-day SLA window)")

# Calculate days since start date
today = pd.Timestamp.now()
in_transit['Start Date'] = pd.to_datetime(in_transit['Start Date'], errors='coerce')
in_transit['Days Since Ship'] = (today - in_transit['Start Date']).dt.days

# Separate within and outside SLA
within_sla = in_transit[in_transit['Days Since Ship'] <= 8]
outside_sla = in_transit[in_transit['Days Since Ship'] > 8]

print(f"\nWithin SLA Window (<=8 days): {len(within_sla)}")
print(f"Outside SLA Window (>8 days): {len(outside_sla)}")

# Analyze the outside SLA shipments
print("\n" + "="*80)
print("OUTSIDE SLA WINDOW ANALYSIS (>8 days in transit)")
print("="*80)

if len(outside_sla) > 0:
    # Days distribution
    print("\nDays Since Ship Distribution:")
    days_dist = outside_sla['Days Since Ship'].value_counts().sort_index()
    for days, count in days_dist.items():
        print(f"  {days} days: {count} shipments")

    # Statistics
    print(f"\nStatistics:")
    print(f"  Average Days Since Ship: {outside_sla['Days Since Ship'].mean():.1f}")
    print(f"  Median Days Since Ship: {outside_sla['Days Since Ship'].median():.1f}")
    print(f"  Max Days Since Ship: {outside_sla['Days Since Ship'].max():.0f}")
    print(f"  Min Days Since Ship: {outside_sla['Days Since Ship'].min():.0f}")

    # Delivery status breakdown
    print(f"\nDelivered Status Breakdown:")
    status_counts = outside_sla['Delivered Status'].value_counts()
    for status, count in status_counts.items():
        print(f"  {status}: {count} shipments")

    # State distribution (top 10)
    print(f"\nTop 10 States:")
    state_counts = outside_sla['Destination State'].value_counts().head(10)
    for state, count in state_counts.items():
        pct = (count / len(outside_sla)) * 100
        print(f"  {state}: {count} ({pct:.1f}%)")

    # Zone distribution
    print(f"\nZone Distribution:")
    zone_counts = outside_sla['Calculated Zone'].value_counts().sort_index()
    for zone, count in zone_counts.items():
        pct = (count / len(outside_sla)) * 100
        print(f"  Zone {zone}: {count} ({pct:.1f}%)")

    # Sample records
    print(f"\n" + "="*80)
    print("SAMPLE RECORDS (First 10 Outside SLA)")
    print("="*80)

    sample_cols = ['Tracking Number', 'Start Date', 'Days Since Ship', 'Delivered Status',
                   'Most Recent Scan', 'Destination State', 'Calculated Zone']

    available_cols = [col for col in sample_cols if col in outside_sla.columns]
    sample_df = outside_sla[available_cols].head(10)

    print(sample_df.to_string(index=False))

    # Age buckets
    print(f"\n" + "="*80)
    print("AGE BUCKETS")
    print("="*80)

    buckets = [
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

else:
    print("\nNo shipments found outside SLA window!")

print("\n" + "="*80)
print("WITHIN SLA WINDOW ANALYSIS (<=8 days)")
print("="*80)

if len(within_sla) > 0:
    print(f"\nTotal: {len(within_sla)} shipments")
    print(f"\nDays Since Ship Distribution:")
    days_dist = within_sla['Days Since Ship'].value_counts().sort_index()
    for days, count in days_dist.items():
        pct = (count / len(within_sla)) * 100
        print(f"  {days} days: {count} ({pct:.1f}%)")

    print(f"\nAverage Days Since Ship: {within_sla['Days Since Ship'].mean():.1f}")

print("\n" + "="*80)
