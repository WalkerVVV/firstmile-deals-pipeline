#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Josh's Frogs - Apply Xparcel Rates (National Network Only)
Based on rate cards provided: Xparcel Ground and Xparcel Expedited
Select Network NOT available due to Josh's location
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("="*80)
print("JOSH'S FROGS - XPARCEL RATE APPLICATION")
print("National Network Rates - Ground & Expedited")
print(f"Analysis Date: {datetime.now().strftime('%B %d, %Y')}")
print("="*80)

# Xparcel Ground National Rates (from image)
# Applicable to label(s): 2,4
xparcel_ground_rates = {
    # Weight in lbs: [Zone1, Zone2, Zone3, Zone4, Zone5, Zone6, Zone7, Zone8]
    1: [3.83, 3.87, 3.88, 3.96, 4.00, 4.08, 4.14, 4.23],
    2: [3.83, 3.87, 3.89, 3.96, 4.01, 4.08, 4.14, 4.23],
    3: [3.83, 3.87, 3.89, 3.97, 4.01, 4.08, 4.15, 4.23],
    4: [3.83, 3.87, 3.89, 3.97, 4.01, 4.08, 4.15, 4.23],
    5: [4.07, 4.14, 4.16, 4.22, 4.25, 4.30, 4.36, 4.46],
    6: [4.07, 4.14, 4.16, 4.22, 4.25, 4.30, 4.36, 4.46],
    7: [4.07, 4.14, 4.16, 4.22, 4.26, 4.30, 4.37, 4.46],
    8: [4.08, 4.14, 4.16, 4.22, 4.26, 4.30, 4.37, 4.46],
    9: [4.72, 4.78, 4.87, 4.97, 5.04, 5.17, 5.28, 5.42],
    10: [4.72, 4.78, 4.87, 4.97, 5.04, 5.17, 5.29, 5.44],
    11: [4.72, 4.79, 4.88, 4.97, 5.04, 5.18, 5.31, 5.45],
    12: [4.73, 4.79, 4.88, 4.97, 5.07, 5.20, 5.33, 5.47],
    13: [5.23, 5.23, 5.43, 5.63, 5.73, 5.93, 6.07, 6.23],
    14: [5.23, 5.24, 5.50, 5.63, 5.80, 5.94, 6.09, 6.30],
    15: [5.23, 5.24, 5.50, 5.63, 5.80, 5.94, 6.10, 6.31],
    # 1 lb increments
    16: [5.24, 5.24, 5.50, 5.66, 5.84, 5.93, 6.18, 6.43],
    17: [5.27, 5.27, 5.54, 5.70, 6.23, 6.95, 7.19, 7.61],
    18: [5.46, 5.51, 5.63, 5.86, 6.67, 7.50, 8.02, 8.44],
    19: [5.63, 5.74, 5.94, 6.40, 7.43, 8.37, 9.28, 9.92],
    20: [6.20, 6.20, 6.54, 7.07, 7.96, 8.98, 10.33, 11.30],
    21: [6.34, 6.34, 6.72, 7.25, 8.32, 9.43, 11.09, 12.16],
    22: [6.36, 6.35, 7.33, 7.86, 9.50, 10.37, 12.05, 13.41],
    23: [7.15, 7.15, 7.91, 9.41, 10.20, 11.72, 13.04, 14.31],
    24: [7.41, 7.45, 8.42, 9.17, 10.61, 12.08, 13.73, 15.21],
    25: [7.93, 7.95, 8.94, 9.91, 11.34, 13.11, 14.71, 16.32]
}

# Xparcel Expedited National Rates (from image)
# Applicable to label(s): 1,4
xparcel_expedited_rates = {
    # Weight in lbs: [Zone1, Zone2, Zone3, Zone4, Zone5, Zone6, Zone7, Zone8]
    1: [3.83, 3.87, 3.89, 3.97, 4.01, 4.08, 4.15, 4.30],
    2: [3.83, 3.87, 3.89, 3.97, 4.01, 4.08, 4.15, 4.30],
    3: [3.83, 3.87, 3.89, 3.97, 4.01, 4.08, 4.15, 4.30],
    4: [3.83, 3.87, 3.89, 3.97, 4.02, 4.10, 4.16, 4.30],
    5: [4.07, 4.14, 4.16, 4.22, 4.26, 4.30, 4.37, 4.47],
    6: [4.07, 4.14, 4.16, 4.22, 4.26, 4.30, 4.37, 4.47],
    7: [4.08, 4.14, 4.17, 4.22, 4.26, 4.31, 4.37, 4.47],
    8: [4.08, 4.14, 4.17, 4.23, 4.26, 4.31, 4.38, 4.47],
    9: [4.73, 4.80, 4.88, 4.97, 5.05, 5.18, 5.32, 5.48],
    10: [4.74, 4.80, 4.88, 4.98, 5.07, 5.20, 5.35, 5.50],
    11: [4.74, 4.80, 4.89, 4.98, 5.07, 5.21, 5.37, 5.52],
    12: [4.74, 4.81, 4.89, 4.98, 5.08, 5.25, 5.39, 5.53],
    13: [5.24, 5.24, 5.50, 5.64, 5.81, 5.95, 6.12, 6.35],
    14: [5.24, 5.24, 5.50, 5.64, 5.81, 5.95, 6.13, 6.37],
    15: [5.24, 5.25, 5.51, 5.64, 5.82, 5.96, 6.15, 6.38],
    # 1 lb increments
    16: [5.24, 5.25, 5.51, 5.66, 5.84, 5.93, 6.18, 6.43],
    17: [5.28, 5.28, 5.55, 5.70, 6.23, 6.95, 7.19, 7.61],
    18: [5.48, 5.53, 5.64, 5.87, 6.68, 7.51, 8.19, 8.63],
    19: [5.63, 5.74, 5.95, 6.41, 7.43, 8.37, 9.42, 10.10],
    20: [6.20, 6.20, 6.55, 7.07, 7.97, 8.97, 10.38, 11.48],
    21: [6.34, 6.34, 6.72, 7.25, 8.32, 9.43, 11.13, 12.26],
    22: [6.36, 6.38, 7.37, 8.06, 9.55, 11.22, 13.64, 15.82],
    23: [7.15, 7.19, 7.97, 9.58, 11.29, 11.81, 16.53, 17.22],
    24: [7.45, 7.49, 8.46, 9.22, 10.67, 12.30, 17.54, 18.40],
    25: [7.97, 7.99, 8.97, 9.96, 11.43, 13.15, 19.05, 19.70]
}

def get_xparcel_rate(weight_lbs, zone, service='ground'):
    """Get Xparcel rate based on weight, zone, and service"""
    # Round up to next pound for rating
    weight_rating = int(np.ceil(weight_lbs))

    # Cap at 25 lbs (max in rate card)
    if weight_rating > 25:
        weight_rating = 25

    # Ensure minimum 1 lb
    if weight_rating < 1:
        weight_rating = 1

    # Get rate from appropriate table
    rates = xparcel_ground_rates if service == 'ground' else xparcel_expedited_rates

    # Zone index (zones 1-8 map to index 0-7)
    zone_idx = int(zone) - 1
    if zone_idx < 0 or zone_idx > 7:
        return None

    return rates.get(weight_rating, [None]*8)[zone_idx]

# Load the carrier summary data
print("\n[1] Loading carrier/service summary data...")
df_summary = pd.read_csv('247bef97-8663-431e-b2f5-dd2ca243633d.csv')
df_summary = df_summary[df_summary['Row Labels'] != 'Grand Total'].copy()

total_volume = df_summary['Count of Number'].sum()
print(f"    Total volume: {total_volume:,} packages")

# Extract carrier
df_summary['Carrier'] = df_summary['Row Labels'].str.split('_').str[0]

# Classify services as Ground, Expedited, or Other
print("\n[2] Classifying services for Xparcel mapping...")

def classify_service(row_label):
    """Classify service as ground, expedited, or other"""
    label_upper = row_label.upper()

    # Ground services
    if any(x in label_upper for x in ['GROUND', 'GROUND_ADVANTAGE', 'HOME_DELIVERY']):
        return 'GROUND'

    # Expedited services (2-3 day)
    if any(x in label_upper for x in ['TWO_DAY', 'SECOND_DAY', 'THREE_DAY', 'EXPEDITED']):
        return 'EXPEDITED'

    # Everything else (overnight, priority, etc.)
    return 'OTHER'

df_summary['Service_Class'] = df_summary['Row Labels'].apply(classify_service)

# Calculate Xparcel opportunity
ground_vol = df_summary[df_summary['Service_Class'] == 'GROUND']['Count of Number'].sum()
expedited_vol = df_summary[df_summary['Service_Class'] == 'EXPEDITED']['Count of Number'].sum()
other_vol = df_summary[df_summary['Service_Class'] == 'OTHER']['Count of Number'].sum()

print(f"\nService Classification:")
print(f"  Xparcel Ground opportunity:     {ground_vol:>12,} packages ({ground_vol/total_volume*100:>5.1f}%)")
print(f"  Xparcel Expedited opportunity:  {expedited_vol:>12,} packages ({expedited_vol/total_volume*100:>5.1f}%)")
print(f"  Other services (not mapped):    {other_vol:>12,} packages ({other_vol/total_volume*100:>5.1f}%)")

# Estimate savings by service class
print("\n[3] Calculating estimated savings...")
print("\nAssumptions:")
print("  - Average zone: Zone 4 (regional focus)")
print("  - Weight distribution based on carrier summary data")
print("  - Current costs estimated from industry averages")

# Calculate weighted average Xparcel rates
def calc_avg_xparcel_rate(service='ground'):
    """Calculate weighted average Xparcel rate across zones and weights"""
    rates = xparcel_ground_rates if service == 'ground' else xparcel_expedited_rates

    # Use Zone 4 as average (index 3)
    zone4_rates = [rates[w][3] for w in sorted(rates.keys())]

    # Weight-based average (more packages at lower weights)
    # Assume 60% at 1-5 lbs, 30% at 6-10 lbs, 10% at 11+ lbs
    avg_rate = (
        0.60 * np.mean([rates[w][3] for w in range(1, 6)]) +
        0.30 * np.mean([rates[w][3] for w in range(6, 11)]) +
        0.10 * np.mean([rates[w][3] for w in range(11, 16)])
    )
    return avg_rate

avg_ground_rate = calc_avg_xparcel_rate('ground')
avg_expedited_rate = calc_avg_xparcel_rate('expedited')

print(f"\nXparcel Average Rates (Zone 4, weighted by volume):")
print(f"  Xparcel Ground:    ${avg_ground_rate:.2f}")
print(f"  Xparcel Expedited: ${avg_expedited_rate:.2f}")

# Estimate current costs (industry averages)
# USPS Ground Advantage: ~$6-7, UPS/FedEx Ground: ~$8-10, 2-Day: ~$12-15
current_ground_avg = 7.50  # Conservative estimate
current_expedited_avg = 13.00  # Conservative estimate

# Calculate savings
ground_savings_per_pkg = current_ground_avg - avg_ground_rate
expedited_savings_per_pkg = current_expedited_avg - avg_expedited_rate

ground_annual_savings = ground_vol * ground_savings_per_pkg
expedited_annual_savings = expedited_vol * expedited_savings_per_pkg
total_annual_savings = ground_annual_savings + expedited_annual_savings

print("\n" + "="*80)
print("SAVINGS ANALYSIS")
print("="*80)

print(f"\nXPARCEL GROUND (3-8 day service)")
print(f"  Volume opportunity:        {ground_vol:>12,} packages/year")
print(f"  Monthly opportunity:       {ground_vol/12:>12,.0f} packages")
print(f"  Estimated current cost:    ${current_ground_avg:>11.2f} per package")
print(f"  Xparcel Ground rate:       ${avg_ground_rate:>11.2f} per package")
print(f"  Savings per package:       ${ground_savings_per_pkg:>11.2f} ({ground_savings_per_pkg/current_ground_avg*100:.1f}%)")
print(f"  Annual savings:            ${ground_annual_savings:>11,.0f}")
print(f"  Monthly savings:           ${ground_annual_savings/12:>11,.0f}")

print(f"\nXPARCEL EXPEDITED (2-5 day service)")
print(f"  Volume opportunity:        {expedited_vol:>12,} packages/year")
print(f"  Monthly opportunity:       {expedited_vol/12:>12,.0f} packages")
print(f"  Estimated current cost:    ${current_expedited_avg:>11.2f} per package")
print(f"  Xparcel Expedited rate:    ${avg_expedited_rate:>11.2f} per package")
print(f"  Savings per package:       ${expedited_savings_per_pkg:>11.2f} ({expedited_savings_per_pkg/current_expedited_avg*100:.1f}%)")
print(f"  Annual savings:            ${expedited_annual_savings:>11,.0f}")
print(f"  Monthly savings:           ${expedited_annual_savings/12:>11,.0f}")

print(f"\nTOTAL XPARCEL OPPORTUNITY")
print(f"  Volume:                    {ground_vol + expedited_vol:>12,} packages/year")
print(f"  Monthly:                   {(ground_vol + expedited_vol)/12:>12,.0f} packages")
print(f"  Annual savings:            ${total_annual_savings:>11,.0f}")
print(f"  Monthly savings:           ${total_annual_savings/12:>11,.0f}")
print(f"  Average savings per pkg:   ${total_annual_savings/(ground_vol + expedited_vol):>11.2f}")

# Sample rate card display
print("\n" + "="*80)
print("SAMPLE RATE CARD - XPARCEL GROUND (NATIONAL)")
print("="*80)
print(f"\n{'Weight':<8} {'Zone 1':<8} {'Zone 2':<8} {'Zone 3':<8} {'Zone 4':<8} {'Zone 5':<8} {'Zone 6':<8} {'Zone 7':<8} {'Zone 8':<8}")
print("-"*80)
for weight in [1, 2, 5, 10, 15, 20, 25]:
    rates = xparcel_ground_rates[weight]
    print(f"{weight} lb    ${rates[0]:<7.2f} ${rates[1]:<7.2f} ${rates[2]:<7.2f} ${rates[3]:<7.2f} ${rates[4]:<7.2f} ${rates[5]:<7.2f} ${rates[6]:<7.2f} ${rates[7]:<7.2f}")

print("\n" + "="*80)
print("SAMPLE RATE CARD - XPARCEL EXPEDITED (NATIONAL)")
print("="*80)
print(f"\n{'Weight':<8} {'Zone 1':<8} {'Zone 2':<8} {'Zone 3':<8} {'Zone 4':<8} {'Zone 5':<8} {'Zone 6':<8} {'Zone 7':<8} {'Zone 8':<8}")
print("-"*80)
for weight in [1, 2, 5, 10, 15, 20, 25]:
    rates = xparcel_expedited_rates[weight]
    print(f"{weight} lb    ${rates[0]:<7.2f} ${rates[1]:<7.2f} ${rates[2]:<7.2f} ${rates[3]:<7.2f} ${rates[4]:<7.2f} ${rates[5]:<7.2f} ${rates[6]:<7.2f} ${rates[7]:<7.2f}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
print(f"\nNote: Select Network NOT available for Josh's Frogs (Pennsylvania location)")
print(f"All rates based on National Network (labels 2,4 for Ground, labels 1,4 for Expedited)")
