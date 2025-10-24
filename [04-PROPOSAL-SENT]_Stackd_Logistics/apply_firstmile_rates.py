"""
Stackd Logistics - Apply FirstMile Xparcel Rates
Calculates real savings vs DHL baseline using actual FirstMile rate card
"""

import pandas as pd
import numpy as np

# Load the shipment data
df = pd.read_csv('20250918193042_221aaf59f30469602caf8f7f7485b114.csv')

print("=" * 80)
print("STACKD LOGISTICS - FIRSTMILE RATE APPLICATION")
print("=" * 80)
print()

# Filter to DHL eCommerce only (our target to replace)
dhl_df = df[df['Carrier'] == 'dhl_ecommerce'].copy()
print(f"Target Volume: {len(dhl_df):,} packages (DHL eCommerce only)")
print(f"Current DHL Cost: ${dhl_df['Label Cost'].sum():,.2f}")
print(f"Average DHL Cost: ${dhl_df['Label Cost'].mean():.2f}/pkg")
print()

# FirstMile Xparcel Ground - National Rates (from screenshot)
# Weight tiers in pounds, zones 1-8
national_rates = {
    0.0625: [3.86, 3.91, 3.93, 4.02, 4.07, 4.16, 4.23, 4.32],  # 1 oz
    0.125: [3.87, 3.92, 3.93, 4.02, 4.07, 4.16, 4.23, 4.33],   # 2 oz
    0.1875: [3.87, 3.92, 3.93, 4.02, 4.07, 4.17, 4.23, 4.35],  # 3 oz
    0.25: [3.87, 3.92, 3.93, 4.03, 4.07, 4.17, 4.23, 4.36],    # 4 oz
    0.3125: [4.14, 4.22, 4.24, 4.31, 4.35, 4.37, 4.37, 4.37],  # 5 oz
    0.375: [4.14, 4.22, 4.24, 4.31, 4.35, 4.37, 4.38, 4.38],   # 6 oz
    0.4375: [4.14, 4.22, 4.24, 4.31, 4.35, 4.38, 4.39, 4.39],  # 7 oz
    0.5: [4.15, 4.22, 4.25, 4.31, 4.35, 4.40, 4.40, 4.40],     # 8 oz
    0.5625: [4.78, 4.86, 4.96, 5.01, 5.10, 5.26, 5.39, 5.55],  # 9 oz
    0.625: [4.78, 4.86, 4.96, 5.01, 5.10, 5.26, 5.40, 5.55],   # 10 oz
    0.6875: [4.79, 4.86, 4.96, 5.02, 5.13, 5.28, 5.41, 5.56],  # 11 oz
    0.75: [4.79, 4.86, 4.96, 5.02, 5.13, 5.31, 5.42, 5.57],    # 12 oz
    0.8125: [5.13, 5.27, 5.54, 5.58, 5.92, 6.10, 6.15, 6.16],  # 13 oz
    0.875: [5.14, 5.29, 5.56, 5.59, 5.93, 6.10, 6.21, 6.22],   # 14 oz
    0.9375: [5.15, 5.30, 5.57, 5.62, 5.95, 6.10, 6.26, 6.38],  # 15 oz
    0.9999: [5.28, 5.31, 5.58, 5.79, 5.97, 6.11, 6.29, 6.53],  # 15.99 oz
    1: [5.30, 5.32, 5.59, 5.84, 6.11, 6.30, 6.65, 6.69],       # 1 lb
    2: [5.53, 5.63, 5.77, 5.94, 6.40, 6.69, 7.51, 7.87],       # 2 lbs
}

# FirstMile Xparcel Ground - Select Rates (from screenshot)
select_rates = {
    0.0625: [3.21, 3.22, 3.22, 3.23, 3.24, 3.25, 3.26, 3.27],  # 1 oz
    0.125: [3.26, 3.27, 3.29, 3.29, 3.32, 3.34, 3.35, 3.38],   # 2 oz
    0.1875: [3.27, 3.30, 3.33, 3.35, 3.38, 3.40, 3.43, 3.45],  # 3 oz
    0.25: [3.32, 3.35, 3.39, 3.41, 3.45, 3.48, 3.51, 3.54],    # 4 oz
    0.3125: [3.35, 3.39, 3.44, 3.48, 3.52, 3.56, 3.60, 3.65],  # 5 oz
    0.375: [3.40, 3.44, 3.50, 3.54, 3.58, 3.64, 3.68, 3.72],   # 6 oz
    0.4375: [3.41, 3.45, 3.52, 3.57, 3.64, 3.69, 3.75, 3.81],  # 7 oz
    0.5: [3.41, 3.46, 3.53, 3.61, 3.68, 3.75, 3.82, 3.90],     # 8 oz
    0.5625: [3.74, 3.82, 3.90, 3.99, 4.06, 4.16, 4.24, 4.32],  # 9 oz
    0.625: [3.75, 3.83, 3.91, 4.00, 4.07, 4.16, 4.25, 4.33],   # 10 oz
    0.6875: [3.76, 3.87, 3.97, 4.08, 4.18, 4.29, 4.40, 4.50],  # 11 oz
    0.75: [3.77, 3.89, 4.00, 4.12, 4.24, 4.35, 4.47, 4.58],    # 12 oz
    0.8125: [3.81, 3.94, 4.06, 4.20, 4.32, 4.44, 4.57, 4.69],  # 13 oz
    0.875: [3.82, 3.96, 4.10, 4.24, 4.37, 4.50, 4.65, 4.78],   # 14 oz
    0.9375: [3.83, 3.99, 4.13, 4.28, 4.41, 4.57, 4.71, 4.85],  # 15 oz
    0.9999: [3.89, 4.06, 4.21, 4.36, 4.52, 4.67, 4.81, 4.97],  # 15.99 oz
    1: [4.18, 4.34, 4.49, 4.65, 4.79, 4.96, 5.11, 5.27],       # 1 lb
    2: [4.72, 4.99, 5.27, 5.55, 5.82, 6.10, 6.38, 6.65],       # 2 lbs
}

def get_weight_tier(weight_lb):
    """Convert actual weight to rate card weight tier"""
    if weight_lb <= 0.0625:
        return 0.0625
    elif weight_lb <= 0.125:
        return 0.125
    elif weight_lb <= 0.1875:
        return 0.1875
    elif weight_lb <= 0.25:
        return 0.25
    elif weight_lb <= 0.3125:
        return 0.3125
    elif weight_lb <= 0.375:
        return 0.375
    elif weight_lb <= 0.4375:
        return 0.4375
    elif weight_lb <= 0.5:
        return 0.5
    elif weight_lb <= 0.5625:
        return 0.5625
    elif weight_lb <= 0.625:
        return 0.625
    elif weight_lb <= 0.6875:
        return 0.6875
    elif weight_lb <= 0.75:
        return 0.75
    elif weight_lb <= 0.8125:
        return 0.8125
    elif weight_lb <= 0.875:
        return 0.875
    elif weight_lb <= 0.9375:
        return 0.9375
    elif weight_lb < 1:
        return 0.9999
    elif weight_lb <= 1:
        return 1
    elif weight_lb <= 2:
        return 2
    else:
        return 2  # Default to 2 lb rate for heavier packages

def get_zone_index(state):
    """Map destination state to zone (simplified - would need actual zone mapping)"""
    # This is a simplified zone mapping - in reality would need ZIP-based zone lookup
    # For now, using average zone 4-5 for most states
    zone_mapping = {
        'UT': 1,  # Local
        'ID': 2, 'WY': 2, 'NV': 2, 'CO': 2, 'AZ': 2,  # Zone 2
        'CA': 3, 'OR': 3, 'WA': 3, 'NM': 3, 'MT': 3,  # Zone 3
        'TX': 4, 'OK': 4, 'KS': 4, 'NE': 4,  # Zone 4
    }
    return zone_mapping.get(state, 5) - 1  # Default to zone 5, return 0-indexed

def is_select_eligible(state):
    """Determine if destination is Select Network eligible (major metros)"""
    # Major metro states/cities typically eligible for Select Network
    select_states = ['CA', 'NY', 'IL', 'TX', 'FL', 'WA', 'AZ', 'NJ', 'MA', 'GA']
    return state in select_states

# Apply FirstMile rates
def calculate_firstmile_cost(row):
    weight = row['Weight (lb)']
    state = row['State']

    weight_tier = get_weight_tier(weight)
    zone_idx = get_zone_index(state)

    # Use Select rates if eligible, otherwise National
    if is_select_eligible(state):
        if weight_tier in select_rates:
            return select_rates[weight_tier][zone_idx]
        else:
            return select_rates[2][zone_idx]  # Default to 2 lb rate
    else:
        if weight_tier in national_rates:
            return national_rates[weight_tier][zone_idx]
        else:
            return national_rates[2][zone_idx]  # Default to 2 lb rate

# Calculate FirstMile costs
print("Calculating FirstMile rates for each package...")
dhl_df['FirstMile_Cost'] = dhl_df.apply(calculate_firstmile_cost, axis=1)
dhl_df['Savings'] = dhl_df['Label Cost'] - dhl_df['FirstMile_Cost']
dhl_df['Savings_Pct'] = (dhl_df['Savings'] / dhl_df['Label Cost'] * 100).round(1)

print()
print("=" * 80)
print("FIRSTMILE VS DHL COMPARISON")
print("=" * 80)
print()

# Overall comparison
total_dhl_cost = dhl_df['Label Cost'].sum()
total_fm_cost = dhl_df['FirstMile_Cost'].sum()
total_savings = total_dhl_cost - total_fm_cost
savings_pct = (total_savings / total_dhl_cost * 100)

print(f"DHL Current Cost:     ${total_dhl_cost:,.2f}")
print(f"FirstMile Cost:       ${total_fm_cost:,.2f}")
print(f"Monthly Savings:      ${total_savings:,.2f} ({savings_pct:.1f}%)")
print(f"Annual Savings:       ${total_savings * 12:,.2f}")
print()

# Breakdown by network
select_packages = dhl_df[dhl_df.apply(lambda x: is_select_eligible(x['State']), axis=1)]
national_packages = dhl_df[~dhl_df.apply(lambda x: is_select_eligible(x['State']), axis=1)]

print("=" * 80)
print("NETWORK BREAKDOWN")
print("=" * 80)
print()

print(f"Select Network (Major Metros):")
print(f"  Volume: {len(select_packages):,} packages ({len(select_packages)/len(dhl_df)*100:.1f}%)")
print(f"  DHL Cost: ${select_packages['Label Cost'].sum():,.2f}")
print(f"  FirstMile Cost: ${select_packages['FirstMile_Cost'].sum():,.2f}")
print(f"  Savings: ${(select_packages['Label Cost'].sum() - select_packages['FirstMile_Cost'].sum()):,.2f}")
print()

print(f"National Network:")
print(f"  Volume: {len(national_packages):,} packages ({len(national_packages)/len(dhl_df)*100:.1f}%)")
print(f"  DHL Cost: ${national_packages['Label Cost'].sum():,.2f}")
print(f"  FirstMile Cost: ${national_packages['FirstMile_Cost'].sum():,.2f}")
print(f"  Savings: ${(national_packages['Label Cost'].sum() - national_packages['FirstMile_Cost'].sum()):,.2f}")
print()

# Weight tier analysis
print("=" * 80)
print("SAVINGS BY WEIGHT TIER")
print("=" * 80)
print()

weight_bins = [0, 0.25, 0.5, 0.75, 1, 2, 999]
weight_labels = ['<4 oz', '4-8 oz', '8-12 oz', '12-16 oz', '1-2 lbs', '>2 lbs']
dhl_df['Weight_Category'] = pd.cut(dhl_df['Weight (lb)'], bins=weight_bins, labels=weight_labels)

weight_analysis = dhl_df.groupby('Weight_Category').agg({
    'Label Cost': ['count', 'sum', 'mean'],
    'FirstMile_Cost': ['sum', 'mean'],
    'Savings': 'sum'
}).round(2)

weight_analysis.columns = ['Volume', 'DHL Total', 'DHL Avg', 'FM Total', 'FM Avg', 'Total Savings']
weight_analysis['Savings/Pkg'] = (weight_analysis['DHL Avg'] - weight_analysis['FM Avg']).round(2)
weight_analysis['% Savings'] = ((weight_analysis['Total Savings'] / weight_analysis['DHL Total']) * 100).round(1)

print(weight_analysis.to_string())
print()

# State analysis (top 10)
print("=" * 80)
print("TOP 10 STATES - SAVINGS ANALYSIS")
print("=" * 80)
print()

state_analysis = dhl_df.groupby('State').agg({
    'Label Cost': ['count', 'sum', 'mean'],
    'FirstMile_Cost': ['sum', 'mean'],
    'Savings': 'sum'
}).round(2)

state_analysis.columns = ['Volume', 'DHL Total', 'DHL Avg', 'FM Total', 'FM Avg', 'Total Savings']
state_analysis['Savings/Pkg'] = (state_analysis['DHL Avg'] - state_analysis['FM Avg']).round(2)
state_analysis = state_analysis.sort_values('Volume', ascending=False).head(10)

print(state_analysis.to_string())
print()

print("=" * 80)
print("SUMMARY & RECOMMENDATIONS")
print("=" * 80)
print()

print(f">> Monthly Volume (DHL only): {len(dhl_df):,} packages")
print(f">> Current Monthly Cost: ${total_dhl_cost:,.2f}")
print(f">> FirstMile Monthly Cost: ${total_fm_cost:,.2f}")
print(f">> Monthly Savings: ${total_savings:,.2f} ({savings_pct:.1f}%)")
print(f">> ANNUAL SAVINGS: ${total_savings * 12:,.2f}")
print()

if savings_pct > 15:
    print(">> ASSESSMENT: STRONG COMPETITIVE ADVANTAGE")
    print("   FirstMile beats DHL by >15% - compelling cost case for switching")
elif savings_pct > 10:
    print(">> ASSESSMENT: MODERATE COMPETITIVE ADVANTAGE")
    print("   FirstMile beats DHL by 10-15% - good cost case + operational benefits")
elif savings_pct > 5:
    print(">> ASSESSMENT: MARGINAL COMPETITIVE ADVANTAGE")
    print("   FirstMile beats DHL by 5-10% - need strong operational benefits pitch")
else:
    print(">> ASSESSMENT: WEAK COMPETITIVE POSITION")
    print("   FirstMile savings <5% - may not justify switching cost")

print()
print("=" * 80)

# Save detailed comparison to CSV
dhl_df[['Shipping Label ID', 'Weight (lb)', 'State', 'Label Cost', 'FirstMile_Cost', 'Savings', 'Savings_Pct']].to_csv(
    'stackd_firstmile_vs_dhl_comparison.csv', index=False
)
print("Detailed comparison saved to: stackd_firstmile_vs_dhl_comparison.csv")
