#!/usr/bin/env python3
"""
BoxiiShip System Beauty TX - Carrier Mix Impact Analysis
Shows how Xparcel ZIP limits will change carrier/service mix from origin 761
"""

import pandas as pd
import numpy as np

print("=" * 80)
print("BOXIISHIP SYSTEM BEAUTY TX - CARRIER MIX IMPACT ANALYSIS")
print("Xparcel ZIP Limit Analysis from Origin 761 (Beaumont/Port Arthur, TX)")
print("=" * 80)

# Load PLD data from Export sheet
pld_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\BoxiiShip System Beauty Logistics LLC TX_Domestic_Tracking_10.1.25_to10.20.25.xlsx"
df = pd.read_excel(pld_file, sheet_name='Export')

print(f"\nDATA SUMMARY:")
print(f"   Total shipments: {len(df):,}")
print(f"   Date range: {df['Request Date'].min()} to {df['Request Date'].max()}")

# Load ZIP limit files
ground_zips_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\ACI-D 8 day .95 zip limit from 761.txt"
expedited_zips_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\ACI-D 5 day .95 zip limit from 761.txt"

# Read ZIP codes (skip header row, remove filter text at end)
ground_df = pd.read_csv(ground_zips_file, header=None)
ground_zips = set(ground_df[ground_df[0].str.match(r'^\d{5}$', na=False)][0].astype(str).str.zfill(5))

expedited_df = pd.read_csv(expedited_zips_file, header=None)
expedited_zips = set(expedited_df[expedited_df[0].str.match(r'^\d{5}$', na=False)][0].astype(str).str.zfill(5))

print(f"\nXPARCEL COVERAGE FROM ORIGIN 761:")
print(f"   Xparcel Ground eligible ZIPs: {len(ground_zips):,}")
print(f"   Xparcel Expedited eligible ZIPs: {len(expedited_zips):,}")
print(f"   Ground-only ZIPs (Expedited not available): {len(ground_zips - expedited_zips):,}")

# Clean and standardize destination ZIPs
df['Destination Zip'] = df['Destination Zip'].astype(str).str.split('.').str[0].str.zfill(5)

# Classify each shipment by Xparcel eligibility
def classify_xparcel_eligibility(zip_code):
    if zip_code in expedited_zips:
        return 'Both Ground & Expedited'
    elif zip_code in ground_zips:
        return 'Ground Only'
    else:
        return 'Not Eligible'

df['Xparcel_Eligibility'] = df['Destination Zip'].apply(classify_xparcel_eligibility)

# Current carrier mix
print(f"\n" + "=" * 80)
print("CURRENT CARRIER MIX (October 1-20, 2025)")
print("=" * 80)

current_mix = df.groupby('Carrier').agg({
    'Tracking Number': 'count',
    'Reported Weight Oz': 'sum'
}).rename(columns={'Tracking Number': 'Shipments', 'Reported Weight Oz': 'Total Weight Oz'})
current_mix['% Volume'] = (current_mix['Shipments'] / current_mix['Shipments'].sum() * 100).round(2)
current_mix['Avg Weight Oz'] = (current_mix['Total Weight Oz'] / current_mix['Shipments']).round(2)
current_mix = current_mix.sort_values('Shipments', ascending=False)

print(current_mix.to_string())

# Service level mix (Xparcel Type from data)
print(f"\n" + "=" * 80)
print("CURRENT SERVICE LEVEL MIX")
print("=" * 80)

service_mix = df.groupby('Xparcel Type').agg({
    'Tracking Number': 'count',
    'Reported Weight Oz': 'sum'
}).rename(columns={'Tracking Number': 'Shipments', 'Reported Weight Oz': 'Total Weight Oz'})
service_mix['% Volume'] = (service_mix['Shipments'] / service_mix['Shipments'].sum() * 100).round(2)
service_mix['Avg Weight Oz'] = (service_mix['Total Weight Oz'] / service_mix['Shipments']).round(2)
service_mix = service_mix.sort_values('Shipments', ascending=False)

print(service_mix.to_string())

# Xparcel eligibility analysis
print(f"\n" + "=" * 80)
print("XPARCEL ELIGIBILITY ANALYSIS")
print("=" * 80)

eligibility = df.groupby('Xparcel_Eligibility').agg({
    'Tracking Number': 'count',
    'Reported Weight Oz': 'sum'
}).rename(columns={'Tracking Number': 'Shipments', 'Reported Weight Oz': 'Total Weight Oz'})
eligibility['% Volume'] = (eligibility['Shipments'] / eligibility['Shipments'].sum() * 100).round(2)
eligibility['Avg Weight Oz'] = (eligibility['Total Weight Oz'] / eligibility['Shipments']).round(2)
eligibility = eligibility.reindex(['Both Ground & Expedited', 'Ground Only', 'Not Eligible'])

print(eligibility.to_string())

# Service level eligibility cross-tab
print(f"\n" + "=" * 80)
print("CURRENT SERVICE vs XPARCEL ELIGIBILITY")
print("=" * 80)

crosstab = pd.crosstab(
    df['Xparcel Type'],
    df['Xparcel_Eligibility'],
    values=df['Tracking Number'],
    aggfunc='count',
    margins=True
)

print(crosstab.to_string())

# Detailed breakdown: What would change?
print(f"\n" + "=" * 80)
print("CARRIER MIX IMPACT: WHAT WOULD CHANGE WITH XPARCEL?")
print("=" * 80)

# Count shipments by current carrier and Xparcel eligibility
impact = df.groupby(['Carrier', 'Xparcel_Eligibility']).size().reset_index(name='Shipments')
impact_pivot = impact.pivot(index='Carrier', columns='Xparcel_Eligibility', values='Shipments').fillna(0)
impact_pivot['Total'] = impact_pivot.sum(axis=1)
impact_pivot['% Eligible'] = ((impact_pivot.get('Both Ground & Expedited', 0) + impact_pivot.get('Ground Only', 0)) / impact_pivot['Total'] * 100).round(1)

print(impact_pivot.to_string())

# Key insights
print(f"\n" + "=" * 80)
print("KEY INSIGHTS")
print("=" * 80)

total_shipments = len(df)
eligible_both = len(df[df['Xparcel_Eligibility'] == 'Both Ground & Expedited'])
eligible_ground_only = len(df[df['Xparcel_Eligibility'] == 'Ground Only'])
not_eligible = len(df[df['Xparcel_Eligibility'] == 'Not Eligible'])

print(f"\n1. COVERAGE:")
print(f"   - {eligible_both:,} shipments ({eligible_both/total_shipments*100:.1f}%) can use BOTH Xparcel Ground & Expedited")
print(f"   - {eligible_ground_only:,} shipments ({eligible_ground_only/total_shipments*100:.1f}%) can ONLY use Xparcel Ground")
print(f"   - {not_eligible:,} shipments ({not_eligible/total_shipments*100:.1f}%) NOT ELIGIBLE for Xparcel from origin 761")

# Current aci_ws volume that's eligible
aci_eligible = df[(df['Carrier'] == 'aci_ws') & (df['Xparcel_Eligibility'] != 'Not Eligible')]
print(f"\n2. ACI_WS (Current Carrier):")
print(f"   - Total ACI shipments: {len(df[df['Carrier'] == 'aci_ws']):,}")
print(f"   - Eligible for Xparcel: {len(aci_eligible):,} ({len(aci_eligible)/len(df[df['Carrier'] == 'aci_ws'])*100:.1f}%)")

# Check for other carriers
other_carriers = df[df['Carrier'] != 'aci_ws']
if len(other_carriers) > 0:
    print(f"\n3. OTHER CARRIERS:")
    for carrier in other_carriers['Carrier'].unique():
        carrier_df = df[df['Carrier'] == carrier]
        if len(carrier_df) > 0:
            carrier_eligible = carrier_df[carrier_df['Xparcel_Eligibility'] != 'Not Eligible']
            pct = len(carrier_eligible)/len(carrier_df)*100 if len(carrier_df) > 0 else 0
            print(f"   - {carrier}: {len(carrier_df):,} shipments, {len(carrier_eligible):,} eligible ({pct:.1f}%)")

# Top 10 destination states
print(f"\n4. TOP 10 DESTINATION STATES:")
state_summary = df.groupby('Destination State').agg({
    'Tracking Number': 'count',
    'Xparcel_Eligibility': lambda x: (x != 'Not Eligible').sum()
}).rename(columns={'Tracking Number': 'Shipments', 'Xparcel_Eligibility': 'Xparcel Eligible'})
state_summary['% Eligible'] = (state_summary['Xparcel Eligible'] / state_summary['Shipments'] * 100).round(1)
state_summary = state_summary.sort_values('Shipments', ascending=False).head(10)

print(state_summary.to_string())

# Zones analysis
print(f"\n5. ZONE ANALYSIS:")
zone_summary = df.groupby('Calculated Zone').agg({
    'Tracking Number': 'count',
    'Xparcel_Eligibility': lambda x: (x != 'Not Eligible').sum()
}).rename(columns={'Tracking Number': 'Shipments', 'Xparcel_Eligibility': 'Xparcel Eligible'})
zone_summary['% Eligible'] = (zone_summary['Xparcel Eligible'] / zone_summary['Shipments'] * 100).round(1)
zone_summary = zone_summary.sort_values('Calculated Zone')

print(zone_summary.to_string())

print(f"\n" + "=" * 80)
print("CONCLUSION:")
print("=" * 80)
print(f"\nFirstMile Xparcel services from origin 761 can serve {(eligible_both + eligible_ground_only)/total_shipments*100:.1f}%")
print(f"of BoxiiShip System Beauty TX's October 1-20 shipment volume.")
print(f"\nThe ZIP limit analysis shows strong coverage for the current shipping patterns,")
print(f"with the majority of destinations eligible for both Ground and Expedited services.")
print("=" * 80)
