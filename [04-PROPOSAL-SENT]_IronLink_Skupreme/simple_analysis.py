#!/usr/bin/env python3
"""
Simple IronLink Location Analysis Script
"""

import pandas as pd
import sys

def analyze_location(df, location_pattern, location_name):
    """Analyze a specific location"""
    
    # Filter data for this location
    location_mask = df['rate__shipment__address_from__street1'].str.contains(
        location_pattern, case=False, na=False, regex=True
    )
    
    location_df = df[location_mask].copy()
    
    if len(location_df) == 0:
        print(f"No shipments found for {location_name}")
        return None
        
    print(f"\n{location_name}")
    print("=" * 60)
    print(f"Total shipments: {len(location_df)}")
    
    # Service Level Analysis
    service_levels = location_df['rate__servicelevel__servicelevel_name'].value_counts()
    print(f"\nService Level Distribution:")
    for service, count in service_levels.items():
        percentage = (count / len(location_df)) * 100
        print(f"  {service}: {count} ({percentage:.1f}%)")
    
    # Weight Analysis
    location_df['parcel__weight'] = pd.to_numeric(location_df['parcel__weight'], errors='coerce')
    weights = location_df['parcel__weight'].dropna()
    
    if len(weights) > 0:
        # Weight ranges
        weight_0_1 = ((weights >= 0) & (weights <= 1)).sum()
        weight_1_5 = ((weights > 1) & (weights <= 5)).sum()
        weight_5_10 = ((weights > 5) & (weights <= 10)).sum()
        weight_10_20 = ((weights > 10) & (weights <= 20)).sum()
        weight_20_50 = ((weights > 20) & (weights <= 50)).sum()
        weight_50_plus = (weights > 50).sum()
        
        print(f"\nWeight Distribution:")
        print(f"  0-1 lb: {weight_0_1} ({weight_0_1/len(weights)*100:.1f}%)")
        print(f"  1-5 lb: {weight_1_5} ({weight_1_5/len(weights)*100:.1f}%)")
        print(f"  5-10 lb: {weight_5_10} ({weight_5_10/len(weights)*100:.1f}%)")
        print(f"  10-20 lb: {weight_10_20} ({weight_10_20/len(weights)*100:.1f}%)")
        print(f"  20-50 lb: {weight_20_50} ({weight_20_50/len(weights)*100:.1f}%)")
        print(f"  50+ lb: {weight_50_plus} ({weight_50_plus/len(weights)*100:.1f}%)")
        
        print(f"\nAverage Package Weight: {weights.mean():.1f} lb")
    
    # Dimensions
    location_df['parcel__length'] = pd.to_numeric(location_df['parcel__length'], errors='coerce')
    location_df['parcel__width'] = pd.to_numeric(location_df['parcel__width'], errors='coerce')
    location_df['parcel__height'] = pd.to_numeric(location_df['parcel__height'], errors='coerce')
    
    avg_length = location_df['parcel__length'].mean()
    avg_width = location_df['parcel__width'].mean()
    avg_height = location_df['parcel__height'].mean()
    
    print(f"Average Dimensions: {avg_length:.1f} x {avg_width:.1f} x {avg_height:.1f} inches")
    
    # Top destination states
    dest_states = location_df['rate__shipment__address_to__state'].value_counts().head(10)
    print(f"\nTop 10 Destination States:")
    for state, count in dest_states.items():
        percentage = (count / len(location_df)) * 100
        print(f"  {state}: {count} ({percentage:.1f}%)")
    
    return {
        'total': len(location_df),
        'avg_weight': weights.mean() if len(weights) > 0 else 0,
        'service_levels': dict(service_levels),
        'top_state': dest_states.index[0] if len(dest_states) > 0 else 'N/A'
    }

def main():
    # Load data
    print("Loading IronLink Orders Report...")
    df = pd.read_csv('IronLink Orders Report.csv')
    print(f"Total records loaded: {len(df)}")
    
    # Analyze each location
    locations = [
        (r'1400.*Front.*St', '1400 West Front St., Florence, NJ 08518 (Florence_NJ)'),
        (r'6880.*Weber.*Blvd', '6880 Weber Blvd., Ladson, SC 29456 (Ladson_SC)'),
        (r'821.*Rockefeller', '821 S Rockefeller Ave., Ontario, CA 91761 (Ontario_CA)')
    ]
    
    results = {}
    for pattern, name in locations:
        result = analyze_location(df, pattern, name)
        if result:
            results[name] = result
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    for name, data in results.items():
        print(f"{name}: {data['total']} shipments, Avg: {data['avg_weight']:.1f} lb, Top State: {data['top_state']}")

if __name__ == "__main__":
    main()