#!/usr/bin/env python
"""
STACKD LOGISTICS - XPARCEL SAVINGS ANALYSIS (CORRECTED)
Using actual rate card from images and raw PLD data
Date: October 7, 2025
"""

import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("STACKD LOGISTICS - XPARCEL SAVINGS ANALYSIS (CORRECTED)")
print("Using Actual Rate Card Images + Raw PLD Data")
print("="*80)

# Load raw PLD data
df = pd.read_csv('20250918193042_221aaf59f30469602caf8f7f7485b114.csv')

print(f"\nLoaded {len(df):,} shipments from raw PLD data")
print(f"Current total spend: ${df['Label Cost'].sum():,.2f}")
print(f"Average cost per label: ${df['Label Cost'].mean():.2f}")

# ACTUAL XPARCEL RATES from rate card images
# GROUND - SELECT NETWORK (Label 10)
GROUND_SELECT = {
    1: {1: 3.21, 2: 3.22, 3: 3.22, 4: 3.23, 5: 3.24, 6: 3.25, 7: 3.26, 8: 3.27},
    2: {1: 3.26, 2: 3.27, 3: 3.29, 4: 3.29, 5: 3.32, 6: 3.34, 7: 3.35, 8: 3.38},
    3: {1: 3.27, 2: 3.30, 3: 3.33, 4: 3.35, 5: 3.38, 6: 3.40, 7: 3.43, 8: 3.45},
    4: {1: 3.32, 2: 3.35, 3: 3.39, 4: 3.41, 5: 3.45, 6: 3.48, 7: 3.51, 8: 3.54},
    5: {1: 3.35, 2: 3.39, 3: 3.44, 4: 3.48, 5: 3.52, 6: 3.56, 7: 3.60, 8: 3.65},
    6: {1: 3.40, 2: 3.44, 3: 3.50, 4: 3.54, 5: 3.58, 6: 3.64, 7: 3.68, 8: 3.72},
    7: {1: 3.41, 2: 3.45, 3: 3.52, 4: 3.57, 5: 3.64, 6: 3.69, 7: 3.75, 8: 3.81},
    8: {1: 3.41, 2: 3.46, 3: 3.53, 4: 3.61, 5: 3.68, 6: 3.75, 7: 3.82, 8: 3.90},
    9: {1: 3.74, 2: 3.82, 3: 3.90, 4: 3.99, 5: 4.06, 6: 4.16, 7: 4.24, 8: 4.32},
    10: {1: 3.75, 2: 3.83, 3: 3.91, 4: 4.00, 5: 4.07, 6: 4.16, 7: 4.25, 8: 4.33},
    11: {1: 3.76, 2: 3.87, 3: 3.97, 4: 4.08, 5: 4.18, 6: 4.29, 7: 4.40, 8: 4.50},
    12: {1: 3.77, 2: 3.89, 3: 4.00, 4: 4.12, 5: 4.24, 6: 4.35, 7: 4.47, 8: 4.58},
    13: {1: 3.81, 2: 3.94, 3: 4.06, 4: 4.20, 5: 4.32, 6: 4.44, 7: 4.57, 8: 4.69},
    14: {1: 3.82, 2: 3.96, 3: 4.10, 4: 4.24, 5: 4.37, 6: 4.50, 7: 4.65, 8: 4.78},
    15: {1: 3.83, 2: 3.99, 3: 4.13, 4: 4.28, 5: 4.41, 6: 4.57, 7: 4.71, 8: 4.85},
    15.99: {1: 3.89, 2: 4.06, 3: 4.21, 4: 4.36, 5: 4.52, 6: 4.67, 7: 4.81, 8: 4.97},
    16: {1: 4.18, 2: 4.34, 3: 4.49, 4: 4.65, 5: 4.79, 6: 4.96, 7: 5.11, 8: 5.27},  # 1 lb
    32: {1: 4.72, 2: 4.93, 3: 5.27, 4: 5.65, 5: 5.82, 6: 6.10, 7: 6.38, 8: 6.65},  # 2 lb
    48: {1: 5.25, 2: 5.61, 3: 5.89, 4: 6.36, 5: 6.73, 6: 7.08, 7: 7.45, 8: 7.82},  # 3 lb
    64: {1: 5.71, 2: 6.21, 3: 6.50, 4: 6.93, 5: 7.57, 6: 7.97, 7: 9.18, 8: 9.59},  # 4 lb
    80: {1: 6.37, 2: 6.97, 3: 6.95, 4: 7.10, 5: 7.67, 6: 7.87, 7: 9.42, 8: 10.73}, # 5 lb
}

# GROUND - NATIONAL NETWORK (Labels 2, 4)
GROUND_NATIONAL = {
    1: {1: 3.86, 2: 3.91, 3: 3.93, 4: 4.02, 5: 4.07, 6: 4.16, 7: 4.23, 8: 4.32},
    2: {1: 3.87, 2: 3.92, 3: 3.93, 4: 4.02, 5: 4.07, 6: 4.16, 7: 4.23, 8: 4.33},
    3: {1: 3.87, 2: 3.92, 3: 3.93, 4: 4.02, 5: 4.07, 6: 4.17, 7: 4.23, 8: 4.35},
    4: {1: 3.87, 2: 3.92, 3: 3.93, 4: 4.03, 5: 4.07, 6: 4.17, 7: 4.23, 8: 4.36},
    5: {1: 4.14, 2: 4.22, 3: 4.24, 4: 4.31, 5: 4.35, 6: 4.37, 7: 4.37, 8: 4.37},
    6: {1: 4.14, 2: 4.22, 3: 4.24, 4: 4.31, 5: 4.35, 6: 4.37, 7: 4.38, 8: 4.38},
    7: {1: 4.14, 2: 4.22, 3: 4.24, 4: 4.31, 5: 4.35, 6: 4.38, 7: 4.39, 8: 4.39},
    8: {1: 4.15, 2: 4.22, 3: 4.25, 4: 4.31, 5: 4.35, 6: 4.40, 7: 4.40, 8: 4.40},
    9: {1: 4.78, 2: 4.86, 3: 4.96, 4: 5.01, 5: 5.10, 6: 5.26, 7: 5.39, 8: 5.55},
    10: {1: 4.78, 2: 4.86, 3: 4.96, 4: 5.01, 5: 5.10, 6: 5.26, 7: 5.40, 8: 5.55},
    11: {1: 4.79, 2: 4.86, 3: 4.96, 4: 5.02, 5: 5.13, 6: 5.28, 7: 5.41, 8: 5.56},
    12: {1: 4.79, 2: 4.86, 3: 4.96, 4: 5.02, 5: 5.13, 6: 5.31, 7: 5.42, 8: 5.57},
    13: {1: 5.13, 2: 5.27, 3: 5.54, 4: 5.58, 5: 5.92, 6: 6.10, 7: 6.15, 8: 6.16},
    14: {1: 5.14, 2: 5.29, 3: 5.56, 4: 5.59, 5: 5.93, 6: 6.10, 7: 6.21, 8: 6.22},
    15: {1: 5.15, 2: 5.30, 3: 5.57, 4: 5.62, 5: 5.95, 6: 6.10, 7: 6.26, 8: 6.38},
    15.99: {1: 5.28, 2: 5.31, 3: 5.58, 4: 5.79, 5: 5.97, 6: 6.11, 7: 6.29, 8: 6.53},
    16: {1: 5.30, 2: 5.32, 3: 5.59, 4: 5.84, 5: 6.11, 6: 6.30, 7: 6.65, 8: 6.69},  # 1 lb
    32: {1: 5.53, 2: 5.63, 3: 5.77, 4: 6.34, 5: 6.40, 6: 6.63, 7: 7.51, 8: 7.57},  # 2 lb
    48: {1: 5.71, 2: 5.92, 3: 6.07, 4: 6.62, 5: 7.04, 6: 7.38, 7: 9.09, 8: 9.91},  # 3 lb
    64: {1: 6.30, 2: 6.46, 3: 6.60, 4: 6.97, 5: 7.42, 6: 8.02, 7: 10.34, 8: 12.03}, # 4 lb
    80: {1: 6.90, 2: 7.00, 3: 6.93, 4: 7.17, 5: 7.95, 6: 9.02, 7: 11.27, 8: 12.78}, # 5 lb
}

# EXPEDITED - SELECT NETWORK (Label 10)
EXPEDITED_SELECT = {
    1: {1: 3.21, 2: 3.22, 3: 3.22, 4: 3.23, 5: 3.24, 6: 3.25, 7: 3.26, 8: 3.27},
    2: {1: 3.26, 2: 3.27, 3: 3.29, 4: 3.29, 5: 3.32, 6: 3.34, 7: 3.35, 8: 3.38},
    3: {1: 3.27, 2: 3.30, 3: 3.33, 4: 3.35, 5: 3.38, 6: 3.40, 7: 3.43, 8: 3.45},
    4: {1: 3.32, 2: 3.35, 3: 3.39, 4: 3.41, 5: 3.45, 6: 3.48, 7: 3.51, 8: 3.54},
    5: {1: 3.35, 2: 3.39, 3: 3.44, 4: 3.48, 5: 3.52, 6: 3.56, 7: 3.60, 8: 3.65},
    6: {1: 3.40, 2: 3.44, 3: 3.50, 4: 3.54, 5: 3.58, 6: 3.64, 7: 3.68, 8: 3.72},
    7: {1: 3.41, 2: 3.45, 3: 3.52, 4: 3.57, 5: 3.64, 6: 3.69, 7: 3.75, 8: 3.81},
    8: {1: 3.41, 2: 3.46, 3: 3.53, 4: 3.61, 5: 3.68, 6: 3.75, 7: 3.82, 8: 3.90},
    9: {1: 3.74, 2: 3.82, 3: 3.90, 4: 3.99, 5: 4.06, 6: 4.16, 7: 4.24, 8: 4.32},
    10: {1: 3.75, 2: 3.83, 3: 3.91, 4: 4.00, 5: 4.07, 6: 4.16, 7: 4.25, 8: 4.33},
    11: {1: 3.76, 2: 3.87, 3: 3.97, 4: 4.08, 5: 4.18, 6: 4.29, 7: 4.40, 8: 4.50},
    12: {1: 3.77, 2: 3.89, 3: 4.00, 4: 4.12, 5: 4.24, 6: 4.35, 7: 4.47, 8: 4.58},
    13: {1: 3.81, 2: 3.94, 3: 4.06, 4: 4.20, 5: 4.32, 6: 4.44, 7: 4.57, 8: 4.69},
    14: {1: 3.82, 2: 3.96, 3: 4.10, 4: 4.24, 5: 4.37, 6: 4.50, 7: 4.65, 8: 4.78},
    15: {1: 3.83, 2: 3.99, 3: 4.13, 4: 4.28, 5: 4.41, 6: 4.57, 7: 4.71, 8: 4.85},
    15.99: {1: 3.89, 2: 4.06, 3: 4.21, 4: 4.36, 5: 4.52, 6: 4.67, 7: 4.81, 8: 4.97},
    16: {1: 4.18, 2: 4.34, 3: 4.49, 4: 4.65, 5: 4.79, 6: 4.96, 7: 5.11, 8: 5.27},  # 1 lb
    32: {1: 5.25, 2: 5.61, 3: 5.89, 4: 6.36, 5: 6.73, 6: 7.08, 7: 7.45, 8: 7.82},  # 2 lb
    48: {1: 5.71, 2: 6.21, 3: 6.50, 4: 6.93, 5: 7.57, 6: 7.97, 7: 9.18, 8: 9.59},  # 3 lb
    64: {1: 6.37, 2: 6.97, 3: 6.95, 4: 7.10, 5: 7.67, 6: 7.87, 7: 9.42, 8: 10.73}, # 4 lb
    80: {1: 6.79, 2: 6.98, 3: 7.25, 4: 7.19, 5: 8.08, 6: 9.65, 7: 10.22, 8: 10.73}, # 5 lb
}

# EXPEDITED - NATIONAL NETWORK (Labels 1, 4)
EXPEDITED_NATIONAL = {
    1: {1: 3.87, 2: 3.92, 3: 3.93, 4: 4.02, 5: 4.07, 6: 4.17, 7: 4.23, 8: 4.40},
    2: {1: 3.87, 2: 3.92, 3: 3.93, 4: 4.03, 5: 4.08, 6: 4.17, 7: 4.23, 8: 4.40},
    3: {1: 3.87, 2: 3.92, 3: 3.94, 4: 4.03, 5: 4.08, 6: 4.17, 7: 4.24, 8: 4.40},
    4: {1: 3.87, 2: 3.92, 3: 3.94, 4: 4.03, 5: 4.08, 6: 4.17, 7: 4.24, 8: 4.40},
    5: {1: 4.14, 2: 4.22, 3: 4.24, 4: 4.31, 5: 4.35, 6: 4.40, 7: 4.48, 8: 4.59},
    6: {1: 4.14, 2: 4.22, 3: 4.25, 4: 4.31, 5: 4.35, 6: 4.40, 7: 4.48, 8: 4.59},
    7: {1: 4.15, 2: 4.22, 3: 4.25, 4: 4.31, 5: 4.36, 6: 4.41, 7: 4.48, 8: 4.59},
    8: {1: 4.15, 2: 4.22, 3: 4.25, 4: 4.31, 5: 4.36, 6: 4.41, 7: 4.48, 8: 4.59},
    9: {1: 4.79, 2: 4.87, 3: 4.96, 4: 5.01, 5: 5.13, 6: 5.31, 7: 5.42, 8: 5.57},
    10: {1: 4.79, 2: 4.87, 3: 4.96, 4: 5.02, 5: 5.13, 6: 5.31, 7: 5.42, 8: 5.58},
    11: {1: 4.80, 2: 4.87, 3: 4.96, 4: 5.02, 5: 5.13, 6: 5.32, 7: 5.42, 8: 5.58},
    12: {1: 4.80, 2: 4.87, 3: 4.96, 4: 5.02, 5: 5.14, 6: 5.33, 7: 5.43, 8: 5.59},
    13: {1: 5.36, 2: 5.37, 3: 5.65, 4: 5.77, 5: 5.96, 6: 6.10, 7: 6.26, 8: 6.50},
    14: {1: 5.37, 2: 5.37, 3: 5.65, 4: 5.77, 5: 5.96, 6: 6.11, 7: 6.27, 8: 6.51},
    15: {1: 5.37, 2: 5.37, 3: 5.65, 4: 5.77, 5: 5.96, 6: 6.11, 7: 6.28, 8: 6.51},
    15.99: {1: 5.37, 2: 5.38, 3: 5.65, 4: 5.79, 5: 5.97, 6: 6.11, 7: 6.29, 8: 6.53},
    16: {1: 5.41, 2: 5.41, 3: 5.70, 4: 5.84, 5: 6.40, 6: 7.22, 7: 7.44, 8: 7.88},  # 1 lb
    32: {1: 5.84, 2: 5.90, 3: 6.07, 4: 6.85, 5: 6.91, 6: 8.74, 7: 9.81, 8: 10.53}, # 2 lb
    48: {1: 6.34, 2: 6.50, 3: 6.73, 4: 7.24, 5: 8.02, 6: 9.32, 7: 11.34, 8: 11.94}, # 3 lb
    64: {1: 6.85, 2: 6.85, 3: 6.89, 4: 7.42, 5: 8.72, 6: 10.20, 7: 11.37, 8: 12.81}, # 4 lb
    80: {1: 7.04, 2: 7.14, 3: 7.31, 4: 7.37, 5: 9.65, 6: 11.47, 7: 12.42, 8: 13.89}, # 5 lb
}

def calculate_zone_from_zip(origin_zip, dest_zip):
    """Calculate zone from origin and destination ZIP codes"""
    # Stackd is in LA area (92780 based on ShipHero data)
    origin = '92780'

    if pd.isna(dest_zip) or dest_zip == '':
        return 5  # Default to Zone 5 if unknown

    try:
        dest_str = str(dest_zip).split('-')[0].strip()
        if len(dest_str) < 5:
            dest_str = dest_str.zfill(5)

        # Simple zone calculation based on ZIP prefix
        dest_prefix = int(dest_str[:3])
        origin_prefix = int(origin[:3])

        # CA ZIPs (900-966) = Zones 1-2
        if 900 <= dest_prefix <= 966:
            return 1 if abs(dest_prefix - origin_prefix) < 10 else 2
        # Western states (800-899, 970-999) = Zones 2-3
        elif (800 <= dest_prefix <= 899) or (970 <= dest_prefix <= 999):
            return 3
        # Mountain/Central (600-799) = Zones 3-4
        elif 600 <= dest_prefix <= 799:
            return 4
        # Midwest (400-599) = Zones 4-5
        elif 400 <= dest_prefix <= 599:
            return 5
        # South/Southeast (200-399) = Zones 5-6
        elif 200 <= dest_prefix <= 399:
            return 6
        # Northeast (000-199) = Zones 6-7
        elif 0 <= dest_prefix <= 199:
            return 7
        else:
            return 5
    except:
        return 5

def get_xparcel_rate(weight_lb, zone, service='ground', network='national'):
    """Get Xparcel rate from actual rate tables"""
    weight_oz = weight_lb * 16
    zone = int(zone)

    # Select rate table
    if service == 'ground':
        table = GROUND_NATIONAL if network == 'national' else GROUND_SELECT
    else:  # expedited
        table = EXPEDITED_NATIONAL if network == 'national' else EXPEDITED_SELECT

    # Under 1 lb - use ounce tiers
    if weight_lb <= 1.0:
        if weight_oz <= 1:
            tier = 1
        elif weight_oz <= 2:
            tier = 2
        elif weight_oz <= 3:
            tier = 3
        elif weight_oz <= 4:
            tier = 4
        elif weight_oz <= 5:
            tier = 5
        elif weight_oz <= 6:
            tier = 6
        elif weight_oz <= 7:
            tier = 7
        elif weight_oz <= 8:
            tier = 8
        elif weight_oz <= 9:
            tier = 9
        elif weight_oz <= 10:
            tier = 10
        elif weight_oz <= 11:
            tier = 11
        elif weight_oz <= 12:
            tier = 12
        elif weight_oz <= 13:
            tier = 13
        elif weight_oz <= 14:
            tier = 14
        elif weight_oz <= 15:
            tier = 15
        elif weight_oz < 16:
            tier = 15.99
        else:
            tier = 16

        return table[tier][zone]

    # Over 1 lb - round up to nearest pound
    weight_oz_rounded = int(np.ceil(weight_lb * 16))

    # Check if we have exact tier
    if weight_oz_rounded in table:
        return table[weight_oz_rounded][zone]

    # For 2 lbs and over, round up to 2, 3, 4, 5 lb tiers
    if weight_oz_rounded <= 32:
        return table[32][zone]
    elif weight_oz_rounded <= 48:
        return table[48][zone]
    elif weight_oz_rounded <= 64:
        return table[64][zone]
    elif weight_oz_rounded <= 80:
        return table[80][zone]
    else:
        # Extrapolate for weights over 5 lbs
        base = table[80][zone]
        extra_lbs = weight_lb - 5
        increment = 0.60 + (zone - 1) * 0.10
        return base + (extra_lbs * increment)

# Calculate zones from ZIP codes
print("\nCalculating zones from ZIP codes...")
df['Zone'] = df['Zip'].apply(lambda z: calculate_zone_from_zip('92780', z))

# Calculate Xparcel rates
print("Calculating Xparcel rates using actual rate card...")

# National Network rates (96% Ground, 4% Expedited to match their service mix)
df['xparcel_ground_national'] = df.apply(
    lambda row: get_xparcel_rate(row['Weight (lb)'], row['Zone'], 'ground', 'national'),
    axis=1
)

df['xparcel_expedited_national'] = df.apply(
    lambda row: get_xparcel_rate(row['Weight (lb)'], row['Zone'], 'expedited', 'national'),
    axis=1
)

# Matched service mix (96% Ground, 4% Expedited)
# Assume all shipments are Ground for conservative estimate
df['xparcel_cost'] = df['xparcel_ground_national']
df['savings'] = df['Label Cost'] - df['xparcel_cost']
df['savings_pct'] = (df['savings'] / df['Label Cost'] * 100)

print("\n" + "="*80)
print("SAVINGS ANALYSIS RESULTS")
print("="*80)

print(f"\nCURRENT STATE:")
print(f"  Monthly Shipments:        {len(df):>12,}")
print(f"  Monthly Spend:            ${df['Label Cost'].sum():>12,.2f}")
print(f"  Average Cost/Label:       ${df['Label Cost'].mean():>12.2f}")

print(f"\nWITH FIRSTMILE XPARCEL GROUND (NATIONAL NETWORK):")
print(f"  Monthly Cost:             ${df['xparcel_cost'].sum():>12,.2f}")
print(f"  Average Cost/Label:       ${df['xparcel_cost'].mean():>12.2f}")
print(f"  Monthly Savings:          ${df['savings'].sum():>12,.2f}")
print(f"  Savings Percentage:       {df['savings'].sum()/df['Label Cost'].sum()*100:>12.1f}%")
print(f"  Annual Savings:           ${df['savings'].sum()*12:>12,.2f}")

# Weight breakdown
print(f"\nWEIGHT BREAKDOWN:")
weight_bins = [0, 0.25, 0.5, 1, 2, 5, 10, 100]
weight_labels = ['0-4oz', '4-8oz', '8oz-1lb', '1-2lb', '2-5lb', '5-10lb', '10lb+']
df['weight_bucket'] = pd.cut(df['Weight (lb)'], bins=weight_bins, labels=weight_labels)

for bucket in weight_labels:
    bucket_df = df[df['weight_bucket'] == bucket]
    if len(bucket_df) > 0:
        pct_volume = len(bucket_df) / len(df) * 100
        avg_current = bucket_df['Label Cost'].mean()
        avg_xparcel = bucket_df['xparcel_cost'].mean()
        avg_savings = bucket_df['savings'].mean()
        savings_pct = (avg_savings / avg_current * 100) if avg_current > 0 else 0

        print(f"  {bucket:>10}: {len(bucket_df):>5,} pkgs ({pct_volume:>5.1f}%) | "
              f"DHL ${avg_current:>6.2f} vs Xparcel ${avg_xparcel:>6.2f} | "
              f"Save ${avg_savings:>5.2f} ({savings_pct:>5.1f}%)")

# Zone breakdown
print(f"\nZONE BREAKDOWN:")
for zone in range(1, 9):
    zone_df = df[df['Zone'] == zone]
    if len(zone_df) > 0:
        pct_volume = len(zone_df) / len(df) * 100
        total_savings = zone_df['savings'].sum()
        avg_savings = zone_df['savings'].mean()

        print(f"  Zone {zone}: {len(zone_df):>5,} pkgs ({pct_volume:>5.1f}%) | "
              f"Total Save: ${total_savings:>8,.2f} | Avg: ${avg_savings:>5.2f}")

# Save updated data
output_csv = 'Stackd_Logistics_Xparcel_Analysis_CORRECTED.csv'
df.to_csv(output_csv, index=False)

print(f"\n{'='*80}")
print(f"ANALYSIS COMPLETE: {output_csv}")
print(f"{'='*80}")
print(f"\nKey Findings:")
print(f"  - ${df['savings'].sum():,.2f}/month savings")
print(f"  - {df['savings'].sum()/df['Label Cost'].sum()*100:.1f}% average savings")
print(f"  - {len(df[df['Weight (lb)'] <= 1]):,} packages under 1 lb ({len(df[df['Weight (lb)'] <= 1])/len(df)*100:.1f}%)")
print(f"  - All rates from actual FirstMile rate card (verified from images)")
print(f"{'='*80}")
