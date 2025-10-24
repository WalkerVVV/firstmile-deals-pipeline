#!/usr/bin/env python3
"""
Josh's Frogs - Complete Xparcel Analysis (Simplified)
- Full PLD analysis with simplified zone calculation
- Incumbent carrier rate card extraction (zone x weight matrices)
- Serviceable vs non-serviceable breakdown
- FirstMile Xparcel savings projection
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("JOSH'S FROGS - FULL XPARCEL ANALYSIS")
print("=" * 80)
print()

# Load PLD data
print("Loading PLD data...")
df = pd.read_csv("Josh's Frogs PLD_with_costs_6_month_data.csv")
print(f"Total shipments: {len(df):,}")
print()

# Simplified zone mapping based on ZIP prefix and state
# Origin is 19529 (Pennsylvania)
def get_zone_from_zip(dest_zip):
    """Simplified zone calculation based on destination ZIP prefix"""
    try:
        zip_str = str(dest_zip).split('-')[0].zfill(5)
        zip3 = int(zip_str[:3])

        # Pennsylvania and nearby (Zone 1-2)
        if 150 <= zip3 <= 196:  # PA, NJ, DE, MD
            return 2
        # Northeast (Zone 3)
        elif (10 <= zip3 <= 149) or (197 <= zip3 <= 199):  # NY, CT, MA, RI, NH, VT, ME
            return 3
        # Southeast (Zone 4)
        elif (200 <= zip3 <= 289) or (300 <= zip3 <= 319) or (320 <= zip3 <= 399):  # VA, WV, NC, SC, GA, FL
            return 4
        # Midwest (Zone 4)
        elif (400 <= zip3 <= 499) or (600 <= zip3 <= 699):  # OH, IN, MI, KY, WI, MN, IL
            return 4
        # South Central (Zone 5)
        elif (700 <= zip3 <= 799) or (500 <= zip3 <= 599):  # TX, OK, AR, LA, TN, MS, AL
            return 5
        # Mountain West (Zone 6)
        elif (800 <= zip3 <= 879) or (820 <= zip3 <= 831) or (590 <= zip3 <= 599):  # CO, WY, MT, ND, SD
            return 6
        # Southwest (Zone 7)
        elif (850 <= zip3 <= 899) or (880 <= zip3 <= 884):  # AZ, NM
            return 7
        # West Coast (Zone 8)
        elif (900 <= zip3 <= 999):  # CA, OR, WA, NV, UT, ID
            return 8
        else:
            return 5  # Default middle zone
    except:
        return None

# Calculate zones for all shipments
print("Calculating shipping zones from ZIP codes...")
df['Zone'] = df['Destination'].apply(get_zone_from_zip)
print(f"Zones calculated for {df['Zone'].notna().sum():,} shipments")
print()

# Calculate billable weight (round up to next pound if > 1 lb)
def calculate_billable_weight(weight):
    if pd.isna(weight):
        return None
    if weight <= 1:
        return weight
    return np.ceil(weight)

df['Billable_Weight'] = df['Weight'].apply(calculate_billable_weight)

# Create weight tiers for rate card
def get_weight_tier(weight):
    if pd.isna(weight):
        return None
    if weight <= 1:
        return "0-1"
    elif weight <= 2:
        return "1-2"
    elif weight <= 3:
        return "2-3"
    elif weight <= 4:
        return "3-4"
    elif weight <= 5:
        return "4-5"
    elif weight <= 10:
        return "5-10"
    elif weight <= 15:
        return "10-15"
    elif weight <= 20:
        return "15-20"
    else:
        return "20+"

df['Weight_Tier'] = df['Billable_Weight'].apply(get_weight_tier)

# Define serviceable vs non-serviceable services
EXCLUDED_SERVICES = [
    'FEDEX_FIRST_OVERNIGHT',
    'FEDEX_PRIORITY_OVERNIGHT',
    'FEDEX_STANDARD_OVERNIGHT',
    'UPS_NEXT_DAY_AIR',
    'UPS_NEXT_DAY_AIR_SAVER'
]

df['Serviceable'] = ~df['Service'].isin(EXCLUDED_SERVICES)

print("=" * 80)
print("VOLUME BREAKDOWN")
print("=" * 80)
print()

total_shipments = len(df)
serviceable_shipments = df['Serviceable'].sum()
excluded_shipments = total_shipments - serviceable_shipments

print(f"Total Shipments (6 months): {total_shipments:,}")
print(f"  Monthly Average: {total_shipments/6:,.0f}")
print(f"  Annual Projection: {total_shipments*2:,.0f}")
print()
print(f"Serviceable by FirstMile: {serviceable_shipments:,} ({serviceable_shipments/total_shipments*100:.1f}%)")
print(f"  Monthly Average: {serviceable_shipments/6:,.0f}")
print(f"  Annual Projection: {serviceable_shipments*2:,.0f}")
print()
print(f"Excluded (Express/Overnight): {excluded_shipments:,} ({excluded_shipments/total_shipments*100:.1f}%)")
print(f"  Monthly Average: {excluded_shipments/6:,.0f}")
print()

# Serviceable data
serviceable_df = df[df['Serviceable']]

print("=" * 80)
print("SERVICEABLE SERVICES BREAKDOWN")
print("=" * 80)
print()

service_summary = serviceable_df.groupby('Service').agg({
    'Number': 'count',
    'Weight': 'mean',
    'Cost': ['mean', 'sum']
}).round(2)
service_summary.columns = ['Count', 'Avg_Weight', 'Avg_Cost', 'Total_Cost']
service_summary = service_summary.sort_values('Count', ascending=False)
service_summary['Pct'] = (service_summary['Count'] / serviceable_shipments * 100).round(1)

print(service_summary.to_string())
print()

print("=" * 80)
print("CARRIER FAMILY BREAKDOWN (Serviceable)")
print("=" * 80)
print()

carrier_summary = serviceable_df.groupby('Carrier').agg({
    'Number': 'count',
    'Weight': 'mean',
    'Cost': ['mean', 'sum']
}).round(2)
carrier_summary.columns = ['Count', 'Avg_Weight', 'Avg_Cost', 'Total_Cost']
carrier_summary = carrier_summary.sort_values('Count', ascending=False)
carrier_summary['Pct'] = (carrier_summary['Count'] / serviceable_shipments * 100).round(1)

print(carrier_summary.to_string())
print()

print("=" * 80)
print("WEIGHT DISTRIBUTION (Serviceable)")
print("=" * 80)
print()

weight_dist = serviceable_df.groupby('Weight_Tier').agg({
    'Number': 'count',
    'Cost': ['mean', 'sum']
}).round(2)
weight_dist.columns = ['Count', 'Avg_Cost', 'Total_Cost']
weight_order = ["0-1", "1-2", "2-3", "3-4", "4-5", "5-10", "10-15", "15-20", "20+"]
weight_dist = weight_dist.reindex([w for w in weight_order if w in weight_dist.index])
weight_dist['Pct'] = (weight_dist['Count'] / serviceable_shipments * 100).round(1)

print(weight_dist.to_string())
print()

print("=" * 80)
print("ZONE DISTRIBUTION (Serviceable)")
print("=" * 80)
print()

zone_dist = serviceable_df[serviceable_df['Zone'].notna()].groupby('Zone').agg({
    'Number': 'count',
    'Cost': ['mean', 'sum']
}).round(2)
zone_dist.columns = ['Count', 'Avg_Cost', 'Total_Cost']
zone_dist['Pct'] = (zone_dist['Count'] / serviceable_df['Zone'].notna().sum() * 100).round(1)

print(zone_dist.to_string())
print()

# Regional vs Cross-Country
zones_with_data = serviceable_df[serviceable_df['Zone'].notna()]
regional = zones_with_data[zones_with_data['Zone'] <= 4]
cross_country = zones_with_data[zones_with_data['Zone'] >= 5]

print(f"Regional (Zones 1-4): {len(regional):,} ({len(regional)/len(zones_with_data)*100:.1f}%)")
print(f"Cross-Country (Zones 5-8): {len(cross_country):,} ({len(cross_country)/len(zones_with_data)*100:.1f}%)")
print()

print("=" * 80)
print("FINANCIAL SUMMARY (Serviceable Shipments Only)")
print("=" * 80)
print()

total_6mo_spend = serviceable_df['Cost'].sum()
monthly_spend = total_6mo_spend / 6
annual_spend = total_6mo_spend * 2
avg_cost = serviceable_df['Cost'].mean()

print(f"6-Month Spend (Serviceable): ${total_6mo_spend:,.2f}")
print(f"Monthly Average: ${monthly_spend:,.2f}")
print(f"Annual Projection: ${annual_spend:,.2f}")
print(f"Average Cost per Package: ${avg_cost:.2f}")
print()

# FirstMile Savings Projections
savings_12pct = monthly_spend * 0.12
savings_15pct = monthly_spend * 0.15

print("FIRSTMILE XPARCEL SAVINGS PROJECTIONS:")
print(f"  12% Savings: ${savings_12pct:,.2f}/month (${savings_12pct*12:,.2f}/year)")
print(f"  15% Savings: ${savings_15pct:,.2f}/month (${savings_15pct*12:,.2f}/year)")
print()

print("=" * 80)
print("INCUMBENT CARRIER RATE CARD EXTRACTION")
print("=" * 80)
print()

# Create rate cards for each major carrier/service combination
major_services = serviceable_df.groupby(['Carrier', 'Service']).size().reset_index(name='count')
major_services = major_services[major_services['count'] >= 100].sort_values('count', ascending=False)

print(f"Creating rate cards for {len(major_services)} major services...")
print()

# Create Excel writer
with pd.ExcelWriter('Joshs_Frogs_Incumbent_Rate_Cards.xlsx', engine='openpyxl') as writer:

    # Summary tab
    summary_data = {
        'Metric': [
            'Total Shipments (6 months)',
            'Monthly Average',
            'Annual Projection',
            '',
            'Serviceable by FirstMile',
            'Serviceable Monthly Avg',
            'Serviceable Annual Projection',
            '',
            'Excluded (Express/Overnight)',
            'Excluded Monthly Avg',
            '',
            'Total 6-Month Spend (Serviceable)',
            'Monthly Spend (Serviceable)',
            'Annual Spend (Serviceable)',
            'Average Cost per Package',
            '',
            'FirstMile Savings (12%)',
            'FirstMile Savings (15%)',
            '',
            'FirstMile Monthly Savings (12%)',
            'FirstMile Monthly Savings (15%)',
            'FirstMile Annual Savings (12%)',
            'FirstMile Annual Savings (15%)'
        ],
        'Value': [
            f"{total_shipments:,}",
            f"{total_shipments/6:,.0f}",
            f"{total_shipments*2:,.0f}",
            '',
            f"{serviceable_shipments:,} ({serviceable_shipments/total_shipments*100:.1f}%)",
            f"{serviceable_shipments/6:,.0f}",
            f"{serviceable_shipments*2:,.0f}",
            '',
            f"{excluded_shipments:,} ({excluded_shipments/total_shipments*100:.1f}%)",
            f"{excluded_shipments/6:,.0f}",
            '',
            f"${total_6mo_spend:,.2f}",
            f"${monthly_spend:,.2f}",
            f"${annual_spend:,.2f}",
            f"${avg_cost:.2f}",
            '',
            f"12%",
            f"15%",
            '',
            f"${savings_12pct:,.2f}",
            f"${savings_15pct:,.2f}",
            f"${savings_12pct*12:,.2f}",
            f"${savings_15pct*12:,.2f}"
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_excel(writer, sheet_name='Summary', index=False)

    # Service breakdown tab
    service_summary_full = service_summary.reset_index()
    service_summary_full.to_excel(writer, sheet_name='Service Breakdown', index=False)

    # Carrier breakdown tab
    carrier_summary_full = carrier_summary.reset_index()
    carrier_summary_full.to_excel(writer, sheet_name='Carrier Breakdown', index=False)

    # Weight distribution tab
    weight_dist_full = weight_dist.reset_index()
    weight_dist_full.to_excel(writer, sheet_name='Weight Distribution', index=False)

    # Zone distribution tab
    zone_dist_full = zone_dist.reset_index()
    zone_dist_full.to_excel(writer, sheet_name='Zone Distribution', index=False)

    # Create incumbent rate cards for each major service
    for idx, row in major_services.iterrows():
        carrier = row['Carrier']
        service = row['Service']
        count = row['count']

        # Filter data for this service
        service_data = serviceable_df[
            (serviceable_df['Carrier'] == carrier) &
            (serviceable_df['Service'] == service) &
            (serviceable_df['Zone'].notna()) &
            (serviceable_df['Weight_Tier'].notna())
        ]

        if len(service_data) < 50:
            continue

        # Create zone x weight matrix
        rate_card = service_data.groupby(['Zone', 'Weight_Tier'])['Cost'].mean().unstack(fill_value=0).round(2)

        # Reorder columns
        weight_order_matrix = [w for w in weight_order if w in rate_card.columns]
        rate_card = rate_card[weight_order_matrix]

        # Create sheet name (max 31 chars for Excel)
        sheet_name = f"{carrier}_{service}"[:31]

        # Add volume counts
        volume_card = service_data.groupby(['Zone', 'Weight_Tier']).size().unstack(fill_value=0)
        volume_card = volume_card[[w for w in weight_order_matrix if w in volume_card.columns]]

        # Combine rate card and volume card
        combined = pd.DataFrame()
        combined = pd.concat([
            pd.DataFrame({'': ['AVERAGE RATES']}),
            rate_card.reset_index(),
            pd.DataFrame({'': ['']}),
            pd.DataFrame({'': ['SHIPMENT VOLUMES']}),
            volume_card.reset_index()
        ], ignore_index=True)

        combined.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Created rate card: {sheet_name} ({count:,} shipments)")

print()
print(f"✓ Incumbent rate cards saved to: Joshs_Frogs_Incumbent_Rate_Cards.xlsx")
print()

print("=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
print()
print("Generated Files:")
print("  1. Joshs_Frogs_Incumbent_Rate_Cards.xlsx - Complete analysis with rate cards")
print()
print("Next Steps:")
print("  1. Review incumbent carrier rate cards (zone x weight matrices)")
print("  2. Compare against FirstMile Xparcel rate card")
print("  3. Calculate line-item savings by zone/weight combination")
print("  4. Prepare customer proposal with side-by-side comparison")
print()
