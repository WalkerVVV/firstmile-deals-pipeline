import pandas as pd
import numpy as np
from collections import defaultdict
import sys

# Set output encoding to handle Unicode characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Load the CSV file
df = pd.read_csv('IronLink Orders Report.csv', encoding='utf-8')

print(f"Total records loaded: {len(df)}")
print(f"Date range: {df['object created'].min()} to {df['object created'].max()}")

# Clean and prepare the data
df['weight_rounded'] = df['parcel__weight'].round().astype(int)
df['service_level'] = df['rate__servicelevel__servicelevel_name']
df['location'] = df['rate__shipment__address_from__city'] + ', ' + df['rate__shipment__address_from__state']

# Map service levels according to instructions
service_mapping = {
    'Surepost': 'Ground',
    'Ground Advantage': 'Ground',
    'Ground': 'Ground',
    'Priority': 'Priority',
    'Expedited': 'Expedited',
    'Express': 'Priority',  # Assuming Express maps to Priority
    'Next Day Air': 'Priority',
    '2nd Day Air': 'Expedited',
    '3 Day Select': 'Expedited'
}

# Apply service level mapping
df['service_mapped'] = df['service_level'].map(lambda x: service_mapping.get(x, x))

# Check unique service levels to see what we have
print("\nUnique service levels in data:")
service_counts = df['service_level'].value_counts()
for service, count in service_counts.items():
    print(f"  {repr(service)}: {count}")

print("\nMapped service levels:")
mapped_counts = df['service_mapped'].value_counts()
for service, count in mapped_counts.items():
    print(f"  {service}: {count}")

print("\nUnique locations:")
location_counts = df['location'].value_counts()
for location, count in location_counts.items():
    print(f"  {location}: {count}")

# Create weight tiers from 1 to 400 lbs
weight_tiers = list(range(1, 401))  # 1 to 400 lbs

# Create analysis by weight, service level, and location
analysis_results = []

for location in df['location'].unique():
    location_data = df[df['location'] == location]
    
    for service in ['Priority', 'Expedited', 'Ground']:
        service_data = location_data[location_data['service_mapped'] == service]
        
        for weight in weight_tiers:
            count = len(service_data[service_data['weight_rounded'] == weight])
            if count > 0:  # Only include weights that have shipments
                analysis_results.append({
                    'Location': location,
                    'Service_Level': service,
                    'Weight_LB': weight,
                    'Shipment_Count': count
                })

# Convert to DataFrame for easier analysis
results_df = pd.DataFrame(analysis_results)

print(f"\nTotal shipment combinations with volume: {len(results_df)}")

# Summary statistics
print("\nSummary by Location and Service Level:")
summary = df.groupby(['location', 'service_mapped']).agg({
    'parcel__weight': ['count', 'min', 'max', 'mean', 'median']
}).round(2)
print(summary)

# Weight distribution analysis
print("\nWeight Distribution Summary:")
weight_stats = df.groupby('service_mapped')['weight_rounded'].agg(['count', 'min', 'max', 'mean', 'median']).round(2)
print(weight_stats)

# Export detailed results
results_df.to_csv('IronLink_Shipment_Analysis_by_Weight_Service_Location.csv', index=False)
print(f"\nDetailed analysis exported to: IronLink_Shipment_Analysis_by_Weight_Service_Location.csv")

# Create summary tables
print("\n" + "="*80)
print("COMPREHENSIVE SHIPMENT ANALYSIS BY WEIGHT, SERVICE LEVEL, AND LOCATION")
print("="*80)

# Top 20 weight/service combinations
print("\nTOP 20 WEIGHT/SERVICE COMBINATIONS BY VOLUME:")
top_combinations = results_df.nlargest(20, 'Shipment_Count')
print(top_combinations.to_string(index=False))

# Weight range analysis
print("\nWEIGHT RANGE ANALYSIS:")
for service in ['Priority', 'Expedited', 'Ground']:
    service_data = df[df['service_mapped'] == service]
    if len(service_data) > 0:
        print(f"\n{service}:")
        print(f"  Total Shipments: {len(service_data)}")
        print(f"  Weight Range: {service_data['weight_rounded'].min()} - {service_data['weight_rounded'].max()} lbs")
        print(f"  Average Weight: {service_data['weight_rounded'].mean():.1f} lbs")
        print(f"  Median Weight: {service_data['weight_rounded'].median():.1f} lbs")

# Location analysis
print("\nLOCATION ANALYSIS:")
for location in df['location'].unique():
    location_data = df[df['location'] == location]
    print(f"\n{location}:")
    print(f"  Total Shipments: {len(location_data)}")
    service_breakdown = location_data['service_mapped'].value_counts()
    for service, count in service_breakdown.items():
        print(f"  {service}: {count} shipments")

print("\nAnalysis complete!")