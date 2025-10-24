"""
PLD (Parcel Level Detail) Analysis Script
Comprehensive shipping profile analysis for BoxiiShip System Beauty TX
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_data(file_path):
    """Load shipping data from Excel file"""
    return pd.read_excel(file_path)

def volume_profile(df):
    """Analyze volume profile"""
    print("\n=== VOLUME PROFILE ===")
    total_shipments = len(df)
    date_range = df['Request Date'].max() - df['Request Date'].min()
    daily_avg = total_shipments / max(date_range.days, 1)
    
    print(f"Total Shipments: {total_shipments:,}")
    print(f"Date Range: {df['Request Date'].min().date()} to {df['Request Date'].max().date()}")
    print(f"Daily Average: {daily_avg:.1f}")
    
    return {'total': total_shipments, 'daily_avg': daily_avg}

def carrier_mix(df):
    """Analyze carrier mix with volume and percentages"""
    print("\n=== CARRIER MIX ===")
    carrier_stats = df.groupby('Carrier').size().reset_index(name='Volume')
    carrier_stats['Percentage'] = (carrier_stats['Volume'] / len(df) * 100).round(2)
    carrier_stats = carrier_stats.sort_values('Volume', ascending=False)
    
    print(carrier_stats.to_string(index=False))
    return carrier_stats

def service_level_distribution(df):
    """Analyze service levels used"""
    print("\n=== SERVICE LEVEL DISTRIBUTION ===")
    
    # Group by Product and Xparcel Type
    service_stats = df.groupby(['Xparcel Type', 'Product']).size().reset_index(name='Volume')
    service_stats['Percentage'] = (service_stats['Volume'] / len(df) * 100).round(2)
    service_stats = service_stats.sort_values('Volume', ascending=False)
    
    print(service_stats.head(10).to_string(index=False))
    return service_stats

def expanded_weight_distribution(df):
    """Analyze weight distribution with detailed breakdowns"""
    print("\n=== EXPANDED WEIGHT DISTRIBUTION ===")
    
    # Convert oz to lbs for categorization
    df['Weight_Lbs'] = df['Reported Weight Oz'] / 16
    
    # Create detailed weight categories
    weight_bins = [
        (0, 0.0625, '0-1 oz'),
        (0.0625, 0.25, '1-4 oz'),
        (0.25, 0.5, '5-8 oz'),
        (0.5, 0.75, '9-12 oz'),
        (0.75, 0.9375, '13-15 oz'),
        (0.9375, 0.999, '15.99 oz'),
        (0.999, 1.001, '16 oz exactly'),
        (1.001, 2, '1-2 lbs'),
        (2, 3, '2-3 lbs'),
        (3, 4, '3-4 lbs'),
        (4, 5, '4-5 lbs'),
        (5, 10, '5-10 lbs'),
        (10, 20, '10-20 lbs'),
        (20, 100, '20+ lbs')
    ]
    
    weight_dist = []
    for min_w, max_w, label in weight_bins:
        count = len(df[(df['Weight_Lbs'] > min_w) & (df['Weight_Lbs'] <= max_w)])
        if count > 0:
            weight_dist.append({
                'Weight Range': label,
                'Volume': count,
                'Percentage': round(count / len(df) * 100, 2)
            })
    
    weight_df = pd.DataFrame(weight_dist)
    print(weight_df.to_string(index=False))
    
    # Calculate billable weight impact
    print("\n=== BILLABLE WEIGHT IMPACT ===")
    df['Billable_Weight_Lbs'] = df['Weight_Lbs'].apply(lambda x: 
        np.ceil(x * 16) / 16 if x < 1 else np.ceil(x)
    )
    
    actual_avg = df['Weight_Lbs'].mean()
    billable_avg = df['Billable_Weight_Lbs'].mean()
    impact_pct = ((billable_avg - actual_avg) / actual_avg * 100)
    
    print(f"Average Actual Weight: {actual_avg:.2f} lbs")
    print(f"Average Billable Weight: {billable_avg:.2f} lbs")
    print(f"Billable Weight Impact: +{impact_pct:.1f}%")
    
    return weight_df

def zone_distribution(df):
    """Analyze zone distribution"""
    print("\n=== ZONE DISTRIBUTION ===")
    
    zone_stats = df.groupby('Calculated Zone').size().reset_index(name='Volume')
    zone_stats['Percentage'] = (zone_stats['Volume'] / len(df) * 100).round(2)
    zone_stats = zone_stats.sort_values('Calculated Zone')
    
    print(zone_stats.to_string(index=False))
    
    # Regional vs Cross-Country
    regional = df[df['Calculated Zone'] <= 4].shape[0]
    cross_country = df[df['Calculated Zone'] >= 5].shape[0]
    
    print(f"\nRegional (Zones 1-4): {regional:,} ({regional/len(df)*100:.1f}%)")
    print(f"Cross-Country (Zones 5-8): {cross_country:,} ({cross_country/len(df)*100:.1f}%)")
    
    return zone_stats

def geographic_distribution(df):
    """Analyze top destination states"""
    print("\n=== TOP 10 DESTINATION STATES ===")
    
    state_stats = df.groupby('Destination State').size().reset_index(name='Volume')
    state_stats['Percentage'] = (state_stats['Volume'] / len(df) * 100).round(2)
    state_stats = state_stats.sort_values('Volume', ascending=False).head(10)
    
    print(state_stats.to_string(index=False))
    return state_stats

def cost_analysis(df):
    """Analyze delivery performance and transit times"""
    print("\n=== DELIVERY PERFORMANCE ===")
    
    # Calculate delivery metrics
    delivered = df[df['Delivered Status'] == 'Delivered'].shape[0]
    in_transit = df[df['Delivered Status'] == 'In Transit'].shape[0]
    
    print(f"Delivered: {delivered:,} ({delivered/len(df)*100:.1f}%)")
    print(f"In Transit: {in_transit:,} ({in_transit/len(df)*100:.1f}%)")
    
    # Transit time analysis for delivered packages
    delivered_df = df[df['Delivered Status'] == 'Delivered']
    if not delivered_df.empty:
        avg_transit = delivered_df['Days In Transit'].mean()
        median_transit = delivered_df['Days In Transit'].median()
        
        print(f"\nAverage Transit Time: {avg_transit:.1f} days")
        print(f"Median Transit Time: {median_transit:.1f} days")

def main():
    """Run comprehensive PLD analysis"""
    print("=" * 60)
    print("PLD (PARCEL LEVEL DETAIL) ANALYSIS")
    print("Customer: BoxiiShip System Beauty TX")
    print("Generated:", datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("=" * 60)
    
    # Load data
    df = load_data('ship_data-2.22.2025_to_9.2.2025_BoxiiShip_System_Beauty_TX.xlsx')
    
    # Run all analyses
    volume_profile(df)
    carrier_mix(df)
    service_level_distribution(df)
    expanded_weight_distribution(df)
    zone_distribution(df)
    geographic_distribution(df)
    cost_analysis(df)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()