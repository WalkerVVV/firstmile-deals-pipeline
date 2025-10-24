#!/usr/bin/env python3
"""
Revenue Calculator for Loy FirstMile Xparcel Deal
Applies standard Xparcel pricing to volume distribution
"""

import pandas as pd
import numpy as np

# FirstMile Xparcel Standard Pricing (per package)
# These are typical rates - actual rates may vary based on negotiation
XPARCEL_RATES = {
    'priority': {  # 1-3 day service
        '0-1': 6.50,    # Under 1 lb
        '1-5': 8.25,    # 1-5 lbs
        '5-10': 11.50,  # 5-10 lbs
        '10-25': 18.75  # 10-25 lbs
    },
    'expedited': {  # 2-5 day service
        '0-1': 4.95,    # Under 1 lb
        '1-5': 6.25,    # 1-5 lbs
        '5-10': 8.75,   # 5-10 lbs
        '10-25': 13.50  # 10-25 lbs
    },
    'ground': {  # 3-8 day service
        '0-1': 3.85,    # Under 1 lb
        '1-5': 4.95,    # 1-5 lbs
        '5-10': 6.95,   # 5-10 lbs
        '10-25': 10.25  # 10-25 lbs
    }
}

def calculate_revenue():
    """Calculate annual revenue based on volume assumptions"""
    
    # Load volume assumptions
    df = pd.read_csv('loy_volume_assumptions.csv')
    
    # Remove subtotal and total rows
    df_clean = df[~df['Weight_Range'].str.contains('TOTAL')].copy()
    
    # Map weight ranges to pricing tiers
    def get_price_tier(weight_range):
        if 'oz' in weight_range:
            return '0-1'
        elif any(f'{i}lb' in weight_range for i in range(1, 6)):
            return '1-5'
        elif any(f'{i}lb' in weight_range for i in range(5, 11)):
            return '5-10'
        else:
            return '10-25'
    
    df_clean['price_tier'] = df_clean['Weight_Range'].apply(get_price_tier)
    
    # Calculate revenue by service level
    revenue_data = []
    
    for _, row in df_clean.iterrows():
        tier = row['price_tier']
        
        priority_rev = row['Priority_Volume'] * XPARCEL_RATES['priority'][tier]
        expedited_rev = row['Expedited_Volume'] * XPARCEL_RATES['expedited'][tier]
        ground_rev = row['Ground_Volume'] * XPARCEL_RATES['ground'][tier]
        
        total_rev = priority_rev + expedited_rev + ground_rev
        
        revenue_data.append({
            'Weight_Range': row['Weight_Range'],
            'Priority_Revenue': priority_rev,
            'Expedited_Revenue': expedited_rev,
            'Ground_Revenue': ground_rev,
            'Total_Revenue': total_rev,
            'Volume': row['Total_Volume']
        })
    
    revenue_df = pd.DataFrame(revenue_data)
    
    # Calculate totals
    total_priority_rev = revenue_df['Priority_Revenue'].sum()
    total_expedited_rev = revenue_df['Expedited_Revenue'].sum()
    total_ground_rev = revenue_df['Ground_Revenue'].sum()
    total_revenue = revenue_df['Total_Revenue'].sum()
    total_volume = revenue_df['Volume'].sum()
    
    # Average revenue per package
    avg_revenue = total_revenue / total_volume
    
    # Annual projections
    # Using 271 daily average from analysis
    daily_volume = 271
    monthly_volume = 8676  # Actual from data
    annual_volume_365 = daily_volume * 365  # Calendar year
    annual_volume_260 = daily_volume * 260  # Business days only
    
    # Revenue projections
    monthly_revenue = (total_revenue / total_volume) * monthly_volume
    annual_revenue_365 = (total_revenue / total_volume) * annual_volume_365
    annual_revenue_260 = (total_revenue / total_volume) * annual_volume_260
    
    print("=" * 60)
    print("LOY FIRSTMILE XPARCEL REVENUE ANALYSIS")
    print("=" * 60)
    
    print("\nVOLUME METRICS:")
    print(f"  Daily Average: {daily_volume:,} shipments")
    print(f"  Monthly Volume: {monthly_volume:,} shipments")
    print(f"  Annual (365 days): {annual_volume_365:,} shipments")
    print(f"  Annual (260 business days): {annual_volume_260:,} shipments")
    
    print("\nSAMPLE PERIOD REVENUE (32 days):")
    print(f"  Priority Revenue: ${total_priority_rev:,.2f}")
    print(f"  Expedited Revenue: ${total_expedited_rev:,.2f}")
    print(f"  Ground Revenue: ${total_ground_rev:,.2f}")
    print(f"  Total Revenue: ${total_revenue:,.2f}")
    print(f"  Average per Package: ${avg_revenue:.2f}")
    
    print("\nMONTHLY REVENUE PROJECTION:")
    print(f"  Estimated Monthly Revenue: ${monthly_revenue:,.2f}")
    
    print("\nANNUAL REVENUE PROJECTIONS:")
    print(f"  Annual (365 days): ${annual_revenue_365:,.2f}")
    print(f"  Annual (260 business days): ${annual_revenue_260:,.2f}")
    
    print("\nREVENUE BY SERVICE LEVEL:")
    print(f"  Priority (15%): ${annual_revenue_365 * 0.15:,.2f}")
    print(f"  Expedited (60%): ${annual_revenue_365 * 0.60:,.2f}")
    print(f"  Ground (25%): ${annual_revenue_365 * 0.25:,.2f}")
    
    print("\nKEY METRICS:")
    print(f"  Average Revenue per Package: ${avg_revenue:.2f}")
    print(f"  Monthly Run Rate: ${monthly_revenue:,.2f}")
    print(f"  Annual Run Rate: ${annual_revenue_365:,.2f}")
    
    # Save detailed revenue breakdown
    revenue_df.to_csv('loy_revenue_breakdown.csv', index=False)
    print("\nDetailed revenue breakdown saved to: loy_revenue_breakdown.csv")
    
    return annual_revenue_365, monthly_revenue, avg_revenue

if __name__ == '__main__':
    annual_rev, monthly_rev, avg_rev = calculate_revenue()