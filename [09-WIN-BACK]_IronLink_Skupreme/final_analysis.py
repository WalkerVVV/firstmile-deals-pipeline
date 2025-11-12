import pandas as pd
import numpy as np

# Load the CSV file
df = pd.read_csv('IronLink Orders Report.csv', encoding='utf-8')

print("IRONLINK SHIPMENT ANALYSIS BY WEIGHT, SERVICE LEVEL, AND LOCATION")
print("=" * 80)
print(f"Analysis Period: 2025-04-01 to 2025-06-09")
print(f"Total Records: {len(df):,}")

# Clean and prepare the data
df['weight_rounded'] = df['parcel__weight'].round().astype(int)
df['service_level'] = df['rate__servicelevel__servicelevel_name']
df['location'] = df['rate__shipment__address_from__city'] + ', ' + df['rate__shipment__address_from__state']

# Enhanced service level mapping to Priority/Expedited/Ground
def map_service_level(service):
    if 'Ground' in service or 'Surepost' in service:
        return 'Ground'
    elif 'Next Day' in service or 'Overnight' in service:
        return 'Priority'
    elif '2nd Day' in service or '3 Day' in service or 'Expedited' in service:
        return 'Expedited'
    elif 'Standard' in service:
        return 'Ground'  # Most Standard services are ground equivalent
    else:
        return 'Other'

# Apply service level mapping
df['service_mapped'] = df['service_level'].apply(map_service_level)

# Focus on the three main locations mentioned in the request
main_locations = ['Ontario, CA', 'Florence, NJ', 'Ladson, SC']

# Filter for main locations (combine ONTARIO, CA with Ontario, CA)
df['location_clean'] = df['location'].replace('ONTARIO, CA', 'Ontario, CA')
main_df = df[df['location_clean'].isin(main_locations)].copy()

print(f"Filtered to main locations: {len(main_df):,} records")

# Service level summary
print("\nSERVICE LEVEL DISTRIBUTION:")
print("-" * 40)
service_summary = main_df['service_mapped'].value_counts()
for service, count in service_summary.items():
    pct = (count / len(main_df)) * 100
    print(f"{service:12}: {count:,} shipments ({pct:.1f}%)")

# Summary by location
print(f"\nSHIPMENTS BY LOCATION:")
print("-" * 30)
for location in main_locations:
    location_data = main_df[main_df['location_clean'] == location]
    print(f"{location:15}: {len(location_data):,} shipments")

# Summary by location and service
print(f"\nSUMMARY BY LOCATION AND SERVICE LEVEL:")
print("-" * 50)
location_service_summary = main_df.groupby(['location_clean', 'service_mapped']).size().unstack(fill_value=0)
print(location_service_summary)

# Weight statistics by service level
print(f"\nWEIGHT STATISTICS BY SERVICE LEVEL:")
print("-" * 40)
weight_stats = main_df.groupby('service_mapped')['weight_rounded'].agg(['count', 'min', 'max', 'mean', 'median']).round(1)
print(weight_stats)

# Detailed analysis - top weight/service combinations
print(f"\nTOP 30 WEIGHT/SERVICE/LOCATION COMBINATIONS")
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
detailed_df = detailed_df.sort_values(['Count', 'Weight_LBS'], ascending=[False, True])

print(detailed_df.head(30).to_string(index=False))

# Weight distribution analysis
print(f"\nWEIGHT TIER ANALYSIS BY LOCATION AND SERVICE")
print("=" * 50)

weight_tiers = [
    ('1-5 lbs', 1, 5),
    ('6-10 lbs', 6, 10), 
    ('11-20 lbs', 11, 20),
    ('21-30 lbs', 21, 30),
    ('31-50 lbs', 31, 50),
    ('51-75 lbs', 51, 75),
    ('76+ lbs', 76, 999)
]

for location in main_locations:
    location_data = main_df[main_df['location_clean'] == location]
    if len(location_data) == 0:
        continue
        
    print(f"\n{location}")
    print("-" * len(location))
    
    for service in ['Ground', 'Expedited', 'Priority']:
        service_data = location_data[location_data['service_mapped'] == service]
        if len(service_data) == 0:
            continue
            
        print(f"\n  {service} ({len(service_data):,} total shipments):")
        
        for tier_name, min_wt, max_wt in weight_tiers:
            tier_data = service_data[
                (service_data['weight_rounded'] >= min_wt) & 
                (service_data['weight_rounded'] <= max_wt)
            ]
            if len(tier_data) > 0:
                pct = (len(tier_data) / len(service_data)) * 100
                print(f"    {tier_name:12}: {len(tier_data):,} shipments ({pct:.1f}%)")

# Export detailed results
detailed_df.to_csv('IronLink_Final_Analysis.csv', index=False)

# Create a comprehensive weight breakdown
print(f"\nINDIVIDUAL WEIGHT BREAKDOWN FOR KEY WEIGHTS")
print("=" * 50)

# Show detailed breakdown for weights with >50 shipments total
weight_summary = main_df.groupby('weight_rounded').size().sort_values(ascending=False)
key_weights = weight_summary[weight_summary >= 50].index.tolist()

for weight in sorted(key_weights):
    weight_data = main_df[main_df['weight_rounded'] == weight]
    print(f"\n{weight} LB Shipments (Total: {len(weight_data):,}):")
    
    breakdown = weight_data.groupby(['location_clean', 'service_mapped']).size().unstack(fill_value=0)
    if not breakdown.empty:
        print(breakdown)

print(f"\nEXPORTED: IronLink_Final_Analysis.csv")
print("Analysis Complete!")