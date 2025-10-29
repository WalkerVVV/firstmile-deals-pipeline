#!/usr/bin/env python3
"""
BoxiiShip System Beauty TX - Volume Shift Analysis
Shows how ZIP limits will shift volume from ACI to DHL
"""

import pandas as pd

print("=" * 80)
print("BOXIISHIP SYSTEM BEAUTY TX - VOLUME SHIFT ANALYSIS")
print("How ZIP Limits Will Change ACI vs DHL Volume Split")
print("=" * 80)

# Load PLD data from Export sheet
pld_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\BoxiiShip System Beauty Logistics LLC TX_Domestic_Tracking_10.1.25_to10.20.25.xlsx"
df = pd.read_excel(pld_file, sheet_name='Export')

# Load ZIP limit files
ground_zips_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\ACI-D 8 day .95 zip limit from 761.txt"
expedited_zips_file = r"C:\Users\BrettWalker\FirstMile_Deals\[CUSTOMER]_BoxiiShip System Beauty TX\ACI-D 5 day .95 zip limit from 761.txt"

# Read ZIP codes (skip header row, remove filter text at end)
ground_df = pd.read_csv(ground_zips_file, header=None)
ground_zips = set(ground_df[ground_df[0].str.match(r'^\d{5}$', na=False)][0].astype(str).str.zfill(5))

expedited_df = pd.read_csv(expedited_zips_file, header=None)
expedited_zips = set(expedited_df[expedited_df[0].str.match(r'^\d{5}$', na=False)][0].astype(str).str.zfill(5))

# Clean destination ZIPs
df['Destination Zip'] = df['Destination Zip'].astype(str).str.split('.').str[0].str.zfill(5)

# Check if each shipment is eligible for ACI based on ZIP limits
def check_aci_eligible(row):
    zip_code = row['Destination Zip']
    service = row['Xparcel Type']

    # Check eligibility based on service type
    if service == 'Ground':
        return zip_code in ground_zips
    elif service == 'Expedited':
        return zip_code in expedited_zips
    elif service == 'Priority':
        return zip_code in expedited_zips  # Priority uses same network as Expedited
    else:
        return False

df['ACI_Eligible_After_Limit'] = df.apply(check_aci_eligible, axis=1)

print(f"\nTOTAL VOLUME: {len(df):,} shipments")
print(f"Date Range: October 1-20, 2025")

# Current state
print(f"\n" + "=" * 80)
print("CURRENT STATE (Before ZIP Limits)")
print("=" * 80)

current = df.groupby('Carrier').agg({
    'Tracking Number': 'count'
}).rename(columns={'Tracking Number': 'Shipments'})
current['% Volume'] = (current['Shipments'] / current['Shipments'].sum() * 100).round(2)
current = current.sort_values('Shipments', ascending=False)

print(current.to_string())
print(f"\nTotal: {current['Shipments'].sum():,} shipments")

# After ZIP limits applied
print(f"\n" + "=" * 80)
print("AFTER ZIP LIMITS (Projected Volume Shift)")
print("=" * 80)

# Count how many shipments are ACI-eligible after limits
aci_eligible_count = df['ACI_Eligible_After_Limit'].sum()
aci_not_eligible_count = (~df['ACI_Eligible_After_Limit']).sum()

print(f"\nACI-Eligible Destinations (can ship via ACI): {aci_eligible_count:,} ({aci_eligible_count/len(df)*100:.1f}%)")
print(f"NOT ACI-Eligible (must use DHL): {aci_not_eligible_count:,} ({aci_not_eligible_count/len(df)*100:.1f}%)")

# Break down current ACI volume by eligibility
print(f"\n" + "-" * 80)
print("IMPACT ON CURRENT ACI VOLUME:")
print("-" * 80)

current_aci = df[df['Carrier'] == 'aci_ws']
aci_stays = current_aci[current_aci['ACI_Eligible_After_Limit']]
aci_moves_to_dhl = current_aci[~current_aci['ACI_Eligible_After_Limit']]

print(f"\nCurrent ACI volume: {len(current_aci):,} shipments")
print(f"  - CAN STAY with ACI: {len(aci_stays):,} ({len(aci_stays)/len(current_aci)*100:.1f}%)")
print(f"  - MUST MOVE to DHL: {len(aci_moves_to_dhl):,} ({len(aci_moves_to_dhl)/len(current_aci)*100:.1f}%)")

# Break down current DHL volume
print(f"\n" + "-" * 80)
print("IMPACT ON CURRENT DHL VOLUME:")
print("-" * 80)

current_dhl = df[df['Carrier'] == 'dhl']
dhl_could_move_to_aci = current_dhl[current_dhl['ACI_Eligible_After_Limit']]
dhl_stays = current_dhl[~current_dhl['ACI_Eligible_After_Limit']]

print(f"\nCurrent DHL volume: {len(current_dhl):,} shipments")
print(f"  - Could move to ACI: {len(dhl_could_move_to_aci):,} ({len(dhl_could_move_to_aci)/len(current_dhl)*100:.1f}%)")
print(f"  - STAYS with DHL: {len(dhl_stays):,} ({len(dhl_stays)/len(current_dhl)*100:.1f}%)")

# New carrier mix after ZIP limits
print(f"\n" + "=" * 80)
print("NEW CARRIER MIX (After ZIP Limits Applied)")
print("=" * 80)

# Calculate new volumes
new_aci_volume = len(aci_stays)  # Only ACI shipments that can stay
new_dhl_volume = len(aci_moves_to_dhl) + len(current_dhl)  # Forced DHL + existing DHL

print(f"\nSCENARIO 1: All ineligible ACI shipments move to DHL")
print(f"  ACI: {new_aci_volume:,} shipments ({new_aci_volume/len(df)*100:.1f}%)")
print(f"  DHL: {new_dhl_volume:,} shipments ({new_dhl_volume/len(df)*100:.1f}%)")

# Alternative scenario: Keep as much on ACI as possible
print(f"\nSCENARIO 2: BoxiiShip moves DHL-eligible volume to ACI (maximize ACI)")
new_aci_volume_max = len(aci_stays) + len(dhl_could_move_to_aci)
new_dhl_volume_min = len(aci_moves_to_dhl) + len(dhl_stays)

print(f"  ACI: {new_aci_volume_max:,} shipments ({new_aci_volume_max/len(df)*100:.1f}%)")
print(f"  DHL: {new_dhl_volume_min:,} shipments ({new_dhl_volume_min/len(df)*100:.1f}%)")

# Summary comparison
print(f"\n" + "=" * 80)
print("VOLUME SHIFT SUMMARY")
print("=" * 80)

print(f"\n{'Scenario':<40} {'ACI Volume':<20} {'DHL Volume':<20}")
print("-" * 80)
print(f"{'CURRENT (No ZIP Limits)':<40} {len(current_aci):>6} ({len(current_aci)/len(df)*100:>5.1f}%)      {len(current_dhl):>6} ({len(current_dhl)/len(df)*100:>5.1f}%)")
print(f"{'AFTER ZIP Limits (Worst Case)':<40} {new_aci_volume:>6} ({new_aci_volume/len(df)*100:>5.1f}%)      {new_dhl_volume:>6} ({new_dhl_volume/len(df)*100:>5.1f}%)")
print(f"{'AFTER ZIP Limits (Best Case)':<40} {new_aci_volume_max:>6} ({new_aci_volume_max/len(df)*100:>5.1f}%)      {new_dhl_volume_min:>6} ({new_dhl_volume_min/len(df)*100:>5.1f}%)")

# Calculate the shift
aci_loss_worst = len(current_aci) - new_aci_volume
dhl_gain_worst = new_dhl_volume - len(current_dhl)

print(f"\n" + "=" * 80)
print("THE BOTTOM LINE")
print("=" * 80)

print(f"\nWORST CASE SCENARIO (All ineligible ACI moves to DHL):")
print(f"  - ACI LOSES: {aci_loss_worst:,} shipments ({aci_loss_worst/len(current_aci)*100:.1f}% of current ACI volume)")
print(f"  - DHL GAINS: {dhl_gain_worst:,} shipments")
print(f"  - New split: ACI {new_aci_volume/len(df)*100:.1f}% / DHL {new_dhl_volume/len(df)*100:.1f}%")

print(f"\nBEST CASE SCENARIO (BoxiiShip consolidates ACI-eligible volume):")
print(f"  - ACI GAINS: {len(dhl_could_move_to_aci):,} shipments from DHL")
print(f"  - ACI keeps: {len(aci_stays):,} of current volume")
print(f"  - New split: ACI {new_aci_volume_max/len(df)*100:.1f}% / DHL {new_dhl_volume_min/len(df)*100:.1f}%")

# Service level breakdown for shipments that must move
print(f"\n" + "=" * 80)
print("WHAT SERVICE LEVELS ARE AFFECTED?")
print("=" * 80)

print(f"\nACI shipments that MUST MOVE to DHL ({len(aci_moves_to_dhl):,} total):")
service_breakdown = aci_moves_to_dhl.groupby('Xparcel Type').size()
for service, count in service_breakdown.items():
    print(f"  - {service}: {count:,} shipments ({count/len(aci_moves_to_dhl)*100:.1f}%)")

print(f"\n" + "=" * 80)
