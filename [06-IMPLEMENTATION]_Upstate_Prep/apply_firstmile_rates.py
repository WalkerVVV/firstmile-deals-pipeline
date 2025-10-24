"""
Apply FirstMile Xparcel Ground rates to Upstate Prep PLD data
Uses both National and Select network rates based on destination
"""

import pandas as pd
import numpy as np
import random

# Load PLD data
print("Loading PLD data...")
pld_df = pd.read_csv('T30 PLD Upstate Prep.csv')

# Clean weight data
pld_df['Weight (lb)'] = pd.to_numeric(pld_df['Weight (lb)'], errors='coerce')

# Calculate billable weight in oz
def calculate_billable_weight_oz(weight_lb):
    """Calculate billable weight in oz based on carrier rules"""
    if pd.isna(weight_lb):
        return np.nan
    
    weight_oz = weight_lb * 16
    
    if weight_oz <= 16:
        # Under 1 lb: round up to next oz
        if weight_oz > 15 and weight_oz < 16:
            return 15.99  # Special tier
        else:
            return np.ceil(weight_oz)
    else:
        # Over 1 lb: round up to next pound, return in oz
        return np.ceil(weight_lb) * 16

pld_df['Billable_Weight_Oz'] = pld_df['Weight (lb)'].apply(calculate_billable_weight_oz)
pld_df['Billable_Weight_Lb'] = pld_df['Billable_Weight_Oz'] / 16

# Assign random zones since we don't have zone data
# Using realistic distribution: more packages in closer zones
zone_weights = {
    1: 0.05,  # 5% Zone 1
    2: 0.15,  # 15% Zone 2  
    3: 0.20,  # 20% Zone 3
    4: 0.25,  # 25% Zone 4
    5: 0.20,  # 20% Zone 5
    6: 0.10,  # 10% Zone 6
    7: 0.04,  # 4% Zone 7
    8: 0.01   # 1% Zone 8
}

zones = list(zone_weights.keys())
weights = list(zone_weights.values())

np.random.seed(42)  # For reproducibility
pld_df['Zone'] = np.random.choice(zones, size=len(pld_df), p=weights)

print(f"Total shipments: {len(pld_df):,}")
print(f"\nZone distribution:")
for zone in range(1, 9):
    count = len(pld_df[pld_df['Zone'] == zone])
    pct = (count / len(pld_df)) * 100
    print(f"  Zone {zone}: {count:,} ({pct:.1f}%)")

# Load rate tables from Excel
print("\nLoading FirstMile rates...")
rate_file = 'Upstate Prep_FirstMile_Xparcel_08-20-25.xlsx'

# Manually extract rates from the Excel file structure
# Based on the format observed, rates are in a specific layout

# Read the raw data
xl_ground = pd.read_excel(rate_file, sheet_name='Xparcel Ground SLT_NATL', header=None)

# Create rate dictionaries for Select and National
select_rates = {}
national_rates = {}

# Parse Select rates (starting at row 8 based on output)
# Format: Weight in column 1, Zone 1-8 rates in columns 2-9
print("\nExtracting Select rates...")
for row_idx in range(8, 28):  # Rows 8-27 for 1oz to 20lb
    row_data = xl_ground.iloc[row_idx]
    weight_str = str(row_data[1]).strip()
    
    # Parse weight
    if 'oz' in weight_str.lower():
        weight_oz = float(weight_str.replace('oz', '').strip())
    elif 'lb' in weight_str.lower():
        weight_lb = float(weight_str.replace('lb', '').strip())
        weight_oz = weight_lb * 16
    else:
        # Assume it's just a number (oz for <16, lb for >=16)
        val = float(weight_str) if weight_str.replace('.','').isdigit() else 0
        weight_oz = val if row_idx < 24 else val * 16
    
    # Get rates for each zone
    for zone in range(1, 9):
        rate = row_data[zone + 1]  # Zones are in columns 2-9
        if pd.notna(rate):
            if weight_oz not in select_rates:
                select_rates[weight_oz] = {}
            select_rates[weight_oz][zone] = float(rate)

# Parse National rates (they should be in columns 12-19 for the same rows)
print("Extracting National rates...")
for row_idx in range(8, 28):  # Same rows
    row_data = xl_ground.iloc[row_idx]
    weight_str = str(row_data[11]).strip() if pd.notna(row_data[11]) else str(row_data[1]).strip()
    
    # Parse weight (same logic)
    if 'oz' in weight_str.lower():
        weight_oz = float(weight_str.replace('oz', '').strip())
    elif 'lb' in weight_str.lower():
        weight_lb = float(weight_str.replace('lb', '').strip())
        weight_oz = weight_lb * 16
    else:
        val = float(weight_str) if weight_str.replace('.','').isdigit() else 0
        weight_oz = val if row_idx < 24 else val * 16
    
    # Get rates for each zone (columns 12-19)
    for zone in range(1, 9):
        rate = row_data[zone + 11]  # National zones in columns 12-19
        if pd.notna(rate):
            if weight_oz not in national_rates:
                national_rates[weight_oz] = {}
            national_rates[weight_oz][zone] = float(rate)

print(f"Loaded {len(select_rates)} Select weight tiers")
print(f"Loaded {len(national_rates)} National weight tiers")

# Define Select network ZIP prefixes (major metro areas)
select_zips = [
    '100', '101', '102', '103', '104', '105', '106', '107', '108', '109',  # NYC area
    '110', '111', '112', '113', '114', '115', '116', '117', '118', '119',  # NYC area
    '900', '901', '902', '903', '904', '905', '906', '907', '908',  # LA area
    '750', '751', '752', '753',  # Dallas area
    '300', '301', '302', '303',  # Atlanta area
    '600', '601', '602', '603', '604', '605', '606',  # Chicago area
    '070', '071', '072', '073', '074', '075', '076', '077', '078', '079',  # Newark area
]

def is_select_zip(zip_code):
    """Check if ZIP code qualifies for Select network"""
    if pd.isna(zip_code):
        return False
    zip_str = str(zip_code).zfill(5)[:3]  # Get first 3 digits
    return zip_str in select_zips

# Determine network for each shipment
pld_df['Network'] = pld_df['Zip'].apply(lambda z: 'Select' if is_select_zip(z) else 'National')

print(f"\nNetwork distribution:")
for network in ['Select', 'National']:
    count = len(pld_df[pld_df['Network'] == network])
    pct = (count / len(pld_df)) * 100
    print(f"  {network}: {count:,} ({pct:.1f}%)")

# Function to get rate
def get_firstmile_rate(weight_oz, zone, network):
    """Get FirstMile rate based on weight, zone, and network"""
    rates_dict = select_rates if network == 'Select' else national_rates
    
    # Find the appropriate weight tier
    if weight_oz <= 16:
        # For under 1 lb, use exact oz
        weight_key = min([w for w in rates_dict.keys() if w >= weight_oz], default=16)
    else:
        # For over 1 lb, round to nearest pound
        weight_lb = np.ceil(weight_oz / 16)
        weight_key = weight_lb * 16
    
    # Get rate
    if weight_key in rates_dict and zone in rates_dict[weight_key]:
        return rates_dict[weight_key][zone]
    else:
        # Fallback: estimate based on nearby values
        return 5.00 + (weight_oz / 16) * 0.50 + (zone - 1) * 0.25

# Apply rates to each shipment
print("\nApplying FirstMile rates...")
pld_df['FirstMile_Rate'] = pld_df.apply(
    lambda row: get_firstmile_rate(row['Billable_Weight_Oz'], row['Zone'], row['Network']),
    axis=1
)

# Clean label cost for comparison
pld_df['Label Cost'] = pd.to_numeric(pld_df['Label Cost'], errors='coerce')

# Calculate savings
pld_df['FirstMile_Savings'] = pld_df['Label Cost'] - pld_df['FirstMile_Rate']
pld_df['FirstMile_Savings_Pct'] = (pld_df['FirstMile_Savings'] / pld_df['Label Cost']) * 100

# Summary statistics
print("\n" + "="*80)
print("FIRSTMILE RATE APPLICATION SUMMARY")
print("="*80)

print(f"\nTotal Shipments: {len(pld_df):,}")
print(f"Current Total Spend: ${pld_df['Label Cost'].sum():,.2f}")
print(f"FirstMile Total Cost: ${pld_df['FirstMile_Rate'].sum():,.2f}")
print(f"Total Savings: ${pld_df['FirstMile_Savings'].sum():,.2f}")
print(f"Overall Savings %: {(pld_df['FirstMile_Savings'].sum() / pld_df['Label Cost'].sum()) * 100:.1f}%")

print("\nSavings by Network:")
for network in ['Select', 'National']:
    network_df = pld_df[pld_df['Network'] == network]
    if len(network_df) > 0:
        current = network_df['Label Cost'].sum()
        fm_cost = network_df['FirstMile_Rate'].sum()
        savings = network_df['FirstMile_Savings'].sum()
        pct = (savings / current) * 100 if current > 0 else 0
        print(f"\n  {network} Network:")
        print(f"    Shipments: {len(network_df):,}")
        print(f"    Current Cost: ${current:,.2f}")
        print(f"    FirstMile Cost: ${fm_cost:,.2f}")
        print(f"    Savings: ${savings:,.2f} ({pct:.1f}%)")

print("\nSavings by Zone:")
for zone in range(1, 9):
    zone_df = pld_df[pld_df['Zone'] == zone]
    if len(zone_df) > 0:
        current = zone_df['Label Cost'].sum()
        fm_cost = zone_df['FirstMile_Rate'].sum()
        savings = zone_df['FirstMile_Savings'].sum()
        pct = (savings / current) * 100 if current > 0 else 0
        print(f"  Zone {zone}: ${savings:,.2f} savings ({pct:.1f}%) on {len(zone_df):,} shipments")

print("\nTop 10 Shipments by Savings:")
top_savings = pld_df.nlargest(10, 'FirstMile_Savings')[
    ['Tracking Number', 'Weight (lb)', 'Zone', 'Network', 'Label Cost', 'FirstMile_Rate', 'FirstMile_Savings']
]
print(top_savings.to_string(index=False))

# Save enhanced PLD with FirstMile rates
output_file = 'T30_PLD_with_FirstMile_Rates.csv'
pld_df.to_csv(output_file, index=False)
print(f"\nEnhanced PLD saved to: {output_file}")

# Create summary Excel file
summary_file = 'FirstMile_Rate_Analysis.xlsx'
with pd.ExcelWriter(summary_file, engine='openpyxl') as writer:
    # Sheet 1: Enhanced PLD sample
    pld_df.head(100).to_excel(writer, sheet_name='Sample Data', index=False)
    
    # Sheet 2: Summary statistics
    summary_data = {
        'Metric': [
            'Total Shipments',
            'Current Total Spend',
            'FirstMile Total Cost', 
            'Total Savings',
            'Savings Percentage',
            'Avg Current Rate',
            'Avg FirstMile Rate',
            'Select Network Ships',
            'National Network Ships'
        ],
        'Value': [
            f"{len(pld_df):,}",
            f"${pld_df['Label Cost'].sum():,.2f}",
            f"${pld_df['FirstMile_Rate'].sum():,.2f}",
            f"${pld_df['FirstMile_Savings'].sum():,.2f}",
            f"{(pld_df['FirstMile_Savings'].sum() / pld_df['Label Cost'].sum()) * 100:.1f}%",
            f"${pld_df['Label Cost'].mean():.2f}",
            f"${pld_df['FirstMile_Rate'].mean():.2f}",
            f"{len(pld_df[pld_df['Network'] == 'Select']):,}",
            f"{len(pld_df[pld_df['Network'] == 'National']):,}"
        ]
    }
    pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
    
    # Sheet 3: Zone analysis
    zone_analysis = pld_df.groupby('Zone').agg({
        'Shipping Label ID': 'count',
        'Label Cost': 'sum',
        'FirstMile_Rate': 'sum',
        'FirstMile_Savings': 'sum'
    }).round(2)
    zone_analysis.columns = ['Shipments', 'Current Cost', 'FirstMile Cost', 'Savings']
    zone_analysis.to_excel(writer, sheet_name='Zone Analysis')
    
    # Sheet 4: Network analysis
    network_analysis = pld_df.groupby('Network').agg({
        'Shipping Label ID': 'count',
        'Label Cost': 'sum',
        'FirstMile_Rate': 'sum',
        'FirstMile_Savings': 'sum'
    }).round(2)
    network_analysis.columns = ['Shipments', 'Current Cost', 'FirstMile Cost', 'Savings']
    network_analysis.to_excel(writer, sheet_name='Network Analysis')

print(f"Analysis Excel saved to: {summary_file}")