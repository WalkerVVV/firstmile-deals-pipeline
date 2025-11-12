import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv('IronLink Orders Report.csv', encoding='utf-8')

print("IRONLINK SHIPMENT ANALYSIS BY WEIGHT, SERVICE LEVEL, AND LOCATION")
print("=" * 80)
print(f"Analysis Period: {df['object created'].min()} to {df['object created'].max()}")
print(f"Total Records: {len(df):,}")

# Clean and prepare the data
df['weight_rounded'] = df['parcel__weight'].round().astype(int)
df['service_level'] = df['rate__servicelevel__servicelevel_name']
df['location'] = df['rate__shipment__address_from__city'] + ', ' + df['rate__shipment__address_from__state']

# Enhanced service level mapping to Priority/Expedited/Ground
service_mapping = {
    # Ground services
    'Ground': 'Ground',
    'Surepost': 'Ground',
    'Ground Advantage': 'Ground',
    
    # Priority services (1-day and overnight)
    'Next Day Air®': 'Priority',
    'Next Day Air Saver®': 'Priority',
    'Standard Overnight®': 'Priority',
    
    # Expedited services (2-3 day)
    '2nd Day Air®': 'Expedited',
    '3 Day Select®': 'Expedited',
    'Expedited®': 'Expedited',
    
    # International and specialty services - map based on speed
    'Worldwide Expedited®': 'Expedited',
    'Standard℠': 'Ground',  # Treating as ground since no clear definition
}

# Apply service level mapping
df['service_mapped'] = df['service_level'].map(lambda x: service_mapping.get(x, 'Other'))

# Focus on the three main locations mentioned in the request
main_locations = ['Ontario, CA', 'Florence, NJ', 'Ladson, SC']

# Filter for main locations (note: we also have 'ONTARIO, CA' which should be combined)
df['location_clean'] = df['location'].replace('ONTARIO, CA', 'Ontario, CA')

# Filter for main locations
main_df = df[df['location_clean'].isin(main_locations)].copy()

print(f"\nFiltered to main locations: {len(main_df):,} records")

# Print service level mapping summary
print("\nSERVICE LEVEL MAPPING:")
print("-" * 30)
original_counts = df['service_level'].value_counts()
for original, mapped in service_mapping.items():
    if original in original_counts:
        print(f"{original:25} -> {mapped:10} ({original_counts[original]:,} shipments)")

unmapped = df[~df['service_level'].isin(service_mapping.keys())]['service_level'].value_counts()
if len(unmapped) > 0:
    print("\nUnmapped services:")
    for service, count in unmapped.items():
        print(f"{service:25} -> Other     ({count:,} shipments)")

# Summary by location and service
print(f"\nSUMMARY BY LOCATION AND SERVICE LEVEL:")
print("-" * 50)
location_service_summary = main_df.groupby(['location_clean', 'service_mapped']).size().unstack(fill_value=0)
print(location_service_summary)

# Create comprehensive weight analysis
print(f"\nCOMPREHENSIVE WEIGHT TIER ANALYSIS")
print("=" * 50)

# Create weight tier buckets for better readability
weight_buckets = {
    '1-5 lbs': (1, 5),
    '6-10 lbs': (6, 10),
    '11-20 lbs': (11, 20),
    '21-30 lbs': (21, 30),
    '31-40 lbs': (31, 40),
    '41-50 lbs': (41, 50),
    '51-75 lbs': (51, 75),
    '76-100 lbs': (76, 100),
    '100+ lbs': (101, 1000)
}

# Analyze by weight buckets
for location in main_locations:
    location_data = main_df[main_df['location_clean'] == location]
    if len(location_data) == 0:
        continue
        
    print(f"\n{location.upper()}")
    print("-" * len(location))
    print(f"Total Shipments: {len(location_data):,}")
    
    for service in ['Priority', 'Expedited', 'Ground']:
        service_data = location_data[location_data['service_mapped'] == service]
        if len(service_data) == 0:
            continue
            
        print(f"\n{service} Service ({len(service_data):,} shipments):")
        
        for bucket_name, (min_weight, max_weight) in weight_buckets.items():
            bucket_data = service_data[
                (service_data['weight_rounded'] >= min_weight) & 
                (service_data['weight_rounded'] <= max_weight)
            ]
            if len(bucket_data) > 0:
                print(f"  {bucket_name:12}: {len(bucket_data):,} shipments")

# Detailed weight breakdown for most common weights
print(f"\nTOP 20 INDIVIDUAL WEIGHT/SERVICE/LOCATION COMBINATIONS")
print("=" * 60)

detailed_analysis = []
for location in main_locations:
    location_data = main_df[main_df['location_clean'] == location]
    
    for service in ['Priority', 'Expedited', 'Ground']:
        service_data = location_data[location_data['service_mapped'] == service]
        
        weight_counts = service_data['weight_rounded'].value_counts()
        
        for weight, count in weight_counts.items():
            detailed_analysis.append({
                'Location': location,
                'Service': service,
                'Weight_LBS': weight,
                'Count': count
            })

# Convert to DataFrame and show top combinations
detailed_df = pd.DataFrame(detailed_analysis)
detailed_df = detailed_df.sort_values('Count', ascending=False)

print(detailed_df.head(20).to_string(index=False))

# Export the detailed analysis
detailed_df.to_csv('IronLink_Detailed_Weight_Analysis.csv', index=False)
main_df.to_csv('IronLink_Main_Locations_Data.csv', index=False)

print(f"\n\nEXPORTED FILES:")
print(f"- IronLink_Detailed_Weight_Analysis.csv (summary by weight/service/location)")
print(f"- IronLink_Main_Locations_Data.csv (full data for main locations)")

# Create a pivot table for easy reference
print(f"\nWEIGHT DISTRIBUTION PIVOT TABLE")
print("=" * 40)

# Create pivot showing count of shipments by location and service for key weights
key_weights = [1, 2, 5, 10, 11, 18, 24, 37, 48, 70]
for weight in key_weights:
    weight_data = main_df[main_df['weight_rounded'] == weight]
    if len(weight_data) > 0:
        pivot = weight_data.groupby(['location_clean', 'service_mapped']).size().unstack(fill_value=0)
        if not pivot.empty:
            print(f"\n{weight} LB Shipments:")
            print(pivot)

print("\nAnalysis Complete!")