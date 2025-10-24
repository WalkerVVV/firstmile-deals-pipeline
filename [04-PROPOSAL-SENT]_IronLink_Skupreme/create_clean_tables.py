import pandas as pd
import math

# Read the CSV file
df = pd.read_csv('IronLink Orders Report.csv')

# Define the locations and their addresses
locations = {
    'Ontario, CA': '821 S. ROCKEFELLER ST',
    'Florence, NJ': '1400 W Front St', 
    'Ladson, SC': '6880 Weber Blvd'
}

# Service level mapping
def categorize_service(service_name):
    service_name = str(service_name).lower()
    
    # Priority services
    if any(term in service_name for term in ['next day air', 'overnight', 'express', 'priority']):
        return 'Priority'
    
    # Expedited services  
    elif any(term in service_name for term in ['2nd day', '2 day', '3 day', 'expedited', 'worldwide expedited']):
        return 'Expedited'
    
    # Ground services (default)
    else:
        return 'Ground'

# Find max weight across all locations
all_weights = []
for location_name, address in locations.items():
    location_data = df[df['rate__shipment__address_from__street1'] == address].copy()
    if not location_data.empty:
        location_data['weight_rounded'] = location_data['parcel__weight'].apply(lambda x: round(float(x)))
        all_weights.extend(location_data['weight_rounded'].tolist())

max_weight_in_data = max(all_weights) if all_weights else 0
print(f"Maximum weight in data: {max_weight_in_data} lbs")

# Determine the range to show (up to max weight found, but at least 20)
max_weight_to_show = max(max_weight_in_data, 20)

print("\n" + "="*80)
print("IRONLINK SHIPMENT ANALYSIS - WEIGHT BY SERVICE LEVEL TABLES")
print("="*80)

# Process each location
for location_name, address in locations.items():
    print(f"\n{location_name} ({address})")
    print("-" * 60)
    
    # Filter data for this location
    location_data = df[df['rate__shipment__address_from__street1'] == address].copy()
    
    if location_data.empty:
        print(f"No data found for {location_name}")
        continue
    
    # Round weights to nearest integer
    location_data['weight_rounded'] = location_data['parcel__weight'].apply(lambda x: round(float(x)))
    
    # Categorize service levels
    location_data['service_category'] = location_data['rate__servicelevel__servicelevel_name'].apply(categorize_service)
    
    # Create pivot table
    pivot_table = location_data.groupby(['weight_rounded', 'service_category']).size().unstack(fill_value=0)
    
    # Ensure all service columns exist
    for service in ['Priority', 'Expedited', 'Ground']:
        if service not in pivot_table.columns:
            pivot_table[service] = 0
    
    # Reorder columns
    pivot_table = pivot_table[['Priority', 'Expedited', 'Ground']]
    
    # Add total column
    pivot_table['Total'] = pivot_table.sum(axis=1)
    
    print("Weight\tPriority\tExpedited\tGround\tTotal")
    
    # Show all weights from 1 to the max found in this location's data
    location_max = location_data['weight_rounded'].max() if not location_data.empty else 0
    
    for weight in range(1, location_max + 1):
        if weight in pivot_table.index:
            priority = pivot_table.loc[weight, 'Priority']
            expedited = pivot_table.loc[weight, 'Expedited'] 
            ground = pivot_table.loc[weight, 'Ground']
            total = pivot_table.loc[weight, 'Total']
        else:
            priority = expedited = ground = total = 0
        
        # Use "0" for zero values for clean copy-paste
        print(f"{weight}\t{priority}\t{expedited}\t{ground}\t{total}")
        
    # Summary stats
    print(f"\nSummary for {location_name}:")
    print(f"Total shipments: {len(location_data)}")
    service_totals = location_data['service_category'].value_counts()
    for service in ['Priority', 'Expedited', 'Ground']:
        count = service_totals.get(service, 0)
        percentage = (count / len(location_data) * 100) if len(location_data) > 0 else 0
        print(f"  {service}: {count} ({percentage:.1f}%)")

print(f"\n{'='*80}")
print("COPY-PASTE READY TABLES COMPLETE")
print(f"{'='*80}")