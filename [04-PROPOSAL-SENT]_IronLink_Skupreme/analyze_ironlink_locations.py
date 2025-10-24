#!/usr/bin/env python3
"""
IronLink Location Analysis Script
Analyzes shipping volumes and patterns from three specific locations
"""

import pandas as pd
import numpy as np
from collections import Counter
import re

def load_and_analyze_ironlink_data():
    """Load and analyze IronLink Orders Report CSV data"""
    
    # Load the CSV file
    print("Loading IronLink Orders Report...")
    df = pd.read_csv('IronLink Orders Report.csv')
    
    print(f"Total records loaded: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    
    # Define the three target locations with flexible matching
    locations = {
        'Florence_NJ': {
            'pattern': r'1400.*Front.*St|Front.*St.*Florence|Florence.*NJ.*0?8518',
            'address': '1400 West Front St., Florence, NJ 08518'
        },
        'Ladson_SC': {
            'pattern': r'6880.*Weber.*Blvd|Weber.*Blvd.*Ladson|Ladson.*SC.*29456',
            'address': '6880 Weber Blvd., Ladson, SC 29456'
        },
        'Ontario_CA': {
            'pattern': r'821.*Rockefeller|Rockefeller.*Ontario|Ontario.*CA.*91761',
            'address': '821 S Rockefeller Ave., Ontario, CA 91761'
        }
    }
    
    results = {}
    
    for location_key, location_info in locations.items():
        print(f"\n{'='*60}")
        print(f"ANALYZING: {location_info['address']}")
        print(f"{'='*60}")
        
        # Filter data for this location using flexible pattern matching
        location_mask = df['rate__shipment__address_from__street1'].str.contains(
            location_info['pattern'], case=False, na=False, regex=True
        )
        
        location_df = df[location_mask].copy()
        
        if len(location_df) == 0:
            print(f"No shipments found for {location_key}")
            continue
            
        print(f"Total shipments: {len(location_df):,}")
        
        # Service Level Analysis
        service_levels = location_df['rate__servicelevel__servicelevel_name'].value_counts()
        print(f"\nService Level Distribution:")
        for service, count in service_levels.items():
            percentage = (count / len(location_df)) * 100
            print(f"  {service}: {count:,} ({percentage:.1f}%)")
        
        # Weight Distribution Analysis
        location_df['parcel__weight'] = pd.to_numeric(location_df['parcel__weight'], errors='coerce')
        weights = location_df['parcel__weight'].dropna()
        
        weight_ranges = {
            '0-1 lb': (weights >= 0) & (weights <= 1),
            '1-5 lb': (weights > 1) & (weights <= 5),
            '5-10 lb': (weights > 5) & (weights <= 10),
            '10-20 lb': (weights > 10) & (weights <= 20),
            '20-50 lb': (weights > 20) & (weights <= 50),
            '50+ lb': weights > 50
        }
        
        print(f"\nWeight Distribution:")
        for range_name, range_mask in weight_ranges.items():
            count = range_mask.sum()
            percentage = (count / len(weights)) * 100 if len(weights) > 0 else 0
            print(f"  {range_name}: {count:,} ({percentage:.1f}%)")
        
        # Average weight and dimensions
        avg_weight = weights.mean() if len(weights) > 0 else 0
        print(f"\nAverage Package Weight: {avg_weight:.1f} lb")
        
        # Dimensions analysis
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
            print(f"  {state}: {count:,} ({percentage:.1f}%)")
        
        # Store results for summary
        results[location_key] = {
            'address': location_info['address'],
            'total_shipments': len(location_df),
            'service_levels': dict(service_levels),
            'avg_weight': avg_weight,
            'avg_dimensions': (avg_length, avg_width, avg_height),
            'top_states': dict(dest_states.head(5)),
            'weight_distribution': {range_name: range_mask.sum() for range_name, range_mask in weight_ranges.items()}
        }
    
    # Summary comparison
    print(f"\n{'='*80}")
    print("SUMMARY COMPARISON")
    print(f"{'='*80}")
    
    summary_data = []
    for location_key, data in results.items():
        summary_data.append({
            'Location': data['address'],
            'Total Shipments': f"{data['total_shipments']:,}",
            'Avg Weight (lb)': f"{data['avg_weight']:.1f}",
            'Avg Dimensions (in)': f"{data['avg_dimensions'][0]:.1f} x {data['avg_dimensions'][1]:.1f} x {data['avg_dimensions'][2]:.1f}",
            'Top Service': max(data['service_levels'], key=data['service_levels'].get) if data['service_levels'] else 'N/A'
        })
    
    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))
    
    return results

if __name__ == "__main__":
    results = load_and_analyze_ironlink_data()