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

# Process each location
for location_name, address in locations.items():
    print(f"\n{'='*60}")
    print(f"LOCATION: {location_name} ({address})")
    print(f"{'='*60}")
    
    # Filter data for this location
    location_data = df[df['rate__shipment__address_from__street1'] == address].copy()
    
    if location_data.empty:
        print(f"No data found for {location_name}")
        continue
    
    print(f"Total shipments: {len(location_data)}")
    
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
    
    # Get weight range
    min_weight = int(pivot_table.index.min())
    max_weight = int(pivot_table.index.max())
    
    print(f"Weight range: {min_weight} - {max_weight} lbs")
    print(f"\nService level distribution:")
    service_totals = location_data['service_category'].value_counts()
    for service in ['Priority', 'Expedited', 'Ground']:
        count = service_totals.get(service, 0)
        print(f"  {service}: {count}")
    
    print(f"\nShipment Count by Weight and Service Level:")
    print("Weight\tPriority\tExpedited\tGround\tTotal")
    print("-" * 50)
    
    # Create full range from 1 to max weight
    for weight in range(1, max_weight + 1):
        if weight in pivot_table.index:
            priority = pivot_table.loc[weight, 'Priority']
            expedited = pivot_table.loc[weight, 'Expedited'] 
            ground = pivot_table.loc[weight, 'Ground']
            total = pivot_table.loc[weight, 'Total']
        else:
            priority = expedited = ground = total = 0
        
        # Use "-" for zero values to make it cleaner
        priority_str = str(priority) if priority > 0 else "-"
        expedited_str = str(expedited) if expedited > 0 else "-"
        ground_str = str(ground) if ground > 0 else "-"
        total_str = str(total) if total > 0 else "-"
        
        print(f"{weight}\t{priority_str}\t{expedited_str}\t{ground_str}\t{total_str}")

print(f"\n{'='*60}")
print("ANALYSIS COMPLETE")
print(f"{'='*60}")