#!/usr/bin/env python3
"""
IronLink Weight Tier Analysis Script
Reorganizes shipment data according to billing weight tier structure
"""

import pandas as pd
import numpy as np
from collections import defaultdict

def convert_to_ounces(weight, unit):
    """Convert weight to ounces"""
    if unit.lower() == 'lb':
        return weight * 16
    elif unit.lower() == 'oz':
        return weight
    else:
        # Assume pounds if unknown
        return weight * 16

def get_billing_tier(weight_oz):
    """
    Apply billing logic to determine weight tier
    Rules:
    - If weight <= 15 oz → bill at 1 lb
    - If weight = 15.99 oz → bill at 15.99 oz tier
    - If weight > 16 oz → round UP to next pound tier
    """
    if weight_oz <= 15:
        return 1  # 1 lb tier
    elif abs(weight_oz - 15.99) < 0.01:  # Check for exactly 15.99 oz
        return 15.99  # Special 15.99 oz tier
    elif weight_oz > 16:
        # Round up to next pound tier
        return int(np.ceil(weight_oz / 16))
    else:
        # For weights between 15.01 and 16 oz, bill at 1 lb
        return 1

def categorize_service_level(service_name):
    """Categorize service levels into Priority, Expedited, or Ground"""
    service_name = service_name.lower()
    
    # Priority services (fastest)
    priority_keywords = ['next day', 'overnight', '2nd day', '2 day', 'priority', 'express']
    if any(keyword in service_name for keyword in priority_keywords):
        return 'Priority'
    
    # Expedited services (medium speed)
    expedited_keywords = ['expedited', '3 day', 'select', 'standard℠', 'worldwide expedited']
    if any(keyword in service_name for keyword in expedited_keywords):
        return 'Expedited'
    
    # Everything else is Ground
    return 'Ground'

def get_location_group(sender_name):
    """Group senders into IronLink locations"""
    sender = sender_name.strip()
    
    if 'IronLink Logistics - CA' in sender or 'IronLink Logistics CA' in sender:
        return 'IronLink CA'
    elif 'IronLink Logistics NJ' in sender:
        return 'IronLink NJ'
    elif 'IronLink Logistics - SC' in sender:
        return 'IronLink SC'
    else:
        return 'Other'

def main():
    # Read the CSV file
    print("Loading IronLink Orders Report...")
    df = pd.read_csv('IronLink Orders Report.csv')
    
    print(f"Total records loaded: {len(df)}")
    
    # Filter for IronLink locations only
    ironlink_mask = df['rate__shipment__address_from__name'].str.contains('IronLink Logistics', na=False)
    df_ironlink = df[ironlink_mask].copy()
    
    print(f"IronLink records: {len(df_ironlink)}")
    
    # Convert weights to ounces
    df_ironlink['weight_oz'] = df_ironlink.apply(
        lambda row: convert_to_ounces(row['parcel__weight'], row['parcel__mass_unit']), 
        axis=1
    )
    
    # Apply billing tier logic
    df_ironlink['billing_tier'] = df_ironlink['weight_oz'].apply(get_billing_tier)
    
    # Categorize service levels
    df_ironlink['service_category'] = df_ironlink['rate__servicelevel__servicelevel_name'].apply(categorize_service_level)
    
    # Group by location
    df_ironlink['location'] = df_ironlink['rate__shipment__address_from__name'].apply(get_location_group)
    
    # Create summary tables for each location
    locations = ['IronLink CA', 'IronLink NJ', 'IronLink SC']
    
    for location in locations:
        print(f"\n{'='*50}")
        print(f"{location.upper()} WEIGHT TIER ANALYSIS")
        print(f"{'='*50}")
        
        location_data = df_ironlink[df_ironlink['location'] == location]
        
        if len(location_data) == 0:
            print(f"No data found for {location}")
            continue
            
        print(f"Total shipments: {len(location_data)}")
        
        # Create pivot table
        pivot = location_data.pivot_table(
            index='billing_tier',
            columns='service_category',
            values='tracking number',
            aggfunc='count',
            fill_value=0
        )
        
        # Ensure all service categories are present
        for service in ['Priority', 'Expedited', 'Ground']:
            if service not in pivot.columns:
                pivot[service] = 0
        
        # Reorder columns
        pivot = pivot[['Priority', 'Expedited', 'Ground']]
        
        # Add total column
        pivot['Total'] = pivot.sum(axis=1)
        
        # Sort by weight tier
        pivot = pivot.sort_index()
        
        # Format the weight tier display
        def format_weight_display(tier):
            if tier == 15.99:
                return "15.99 oz"
            else:
                return f"{int(tier)} lb"
        
        # Create formatted table
        print("\n| Weight | Priority | Expedited | Ground | Total |")
        print("|--------|----------|-----------|--------|-------|")
        
        for tier in sorted(pivot.index):
            weight_display = format_weight_display(tier)
            priority_count = pivot.loc[tier, 'Priority']
            expedited_count = pivot.loc[tier, 'Expedited']
            ground_count = pivot.loc[tier, 'Ground']
            total_count = pivot.loc[tier, 'Total']
            
            print(f"| {weight_display:<6} | {priority_count:>8} | {expedited_count:>9} | {ground_count:>6} | {total_count:>5} |")
        
        # Print totals
        print("|--------|----------|-----------|--------|-------|")
        total_priority = pivot['Priority'].sum()
        total_expedited = pivot['Expedited'].sum()
        total_ground = pivot['Ground'].sum()
        grand_total = pivot['Total'].sum()
        
        print(f"| TOTAL  | {total_priority:>8} | {total_expedited:>9} | {total_ground:>6} | {grand_total:>5} |")
        
        # Print percentage breakdown
        print(f"\nService Level Distribution:")
        print(f"Priority: {total_priority:,} ({total_priority/grand_total*100:.1f}%)")
        print(f"Expedited: {total_expedited:,} ({total_expedited/grand_total*100:.1f}%)")
        print(f"Ground: {total_ground:,} ({total_ground/grand_total*100:.1f}%)")
        
        # Print weight distribution insights
        print(f"\nWeight Distribution Insights:")
        top_tiers = pivot.nlargest(5, 'Total')
        for i, (tier, row) in enumerate(top_tiers.iterrows(), 1):
            weight_display = format_weight_display(tier)
            percentage = row['Total'] / grand_total * 100
            print(f"{i}. {weight_display}: {row['Total']:,} shipments ({percentage:.1f}%)")

if __name__ == "__main__":
    main()