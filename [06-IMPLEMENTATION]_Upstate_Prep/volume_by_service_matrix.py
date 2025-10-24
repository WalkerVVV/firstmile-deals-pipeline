"""
Create Volume Distribution Matrix by Weight and Service Level for Upstate Prep
Formatted for Excel copy/paste into tier tool
Service Levels: Xparcel Priority, Xparcel Expedited, Xparcel Ground
"""

import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('T30 PLD Upstate Prep.csv')

# Clean and prepare data
df['Weight (lb)'] = pd.to_numeric(df['Weight (lb)'], errors='coerce')
df['Weight (oz)'] = df['Weight (lb)'] * 16

# Map current services to Xparcel service levels
service_mapping = {
    # Ground Services → Xparcel Ground
    'UPS Ground': 'Xparcel Ground',
    'UPS Standard': 'Xparcel Ground',
    'UPS SurePost': 'Xparcel Ground',
    'Amazon Shipping Ground': 'Xparcel Ground',
    'usps_ground_advantage': 'Xparcel Ground',
    'Fedex Ground Services': 'Xparcel Ground',
    'FEDEX_GROUND': 'Xparcel Ground',
    'Generic': 'Xparcel Ground',
    'Generic Label': 'Xparcel Ground',
    'genericlabel': 'Xparcel Ground',
    'Wholesale Generic': 'Xparcel Ground',
    
    # Expedited Services → Xparcel Expedited  
    'UPS 2nd Day Air': 'Xparcel Expedited',
    'UPS 3 Day Select': 'Xparcel Expedited',
    'UPS Expedited': 'Xparcel Expedited',
    'usps_priority': 'Xparcel Expedited',
    'FedEx International Connect Plus': 'Xparcel Expedited',
    
    # Priority/Express Services → Xparcel Priority
    'UPS Next Day Air': 'Xparcel Priority',
    'UPS Next Day Air Saver': 'Xparcel Priority',
    'UPS Next Day Air Early': 'Xparcel Priority',
    'UPS Express': 'Xparcel Priority',
    'UPS Saver': 'Xparcel Priority',
    'Domestic Express Doc': 'Xparcel Priority',
    'Express Worldwide NonDoc': 'Xparcel Priority',
    
    # International and Other
    'usps_first_class_package_international_service': 'Xparcel Ground',
    'usps_priority_mail_international': 'Xparcel Expedited',
    
    # LTL stays separate for now
    'LTL': 'Xparcel Ground'
}

# Apply service mapping
df['Xparcel Service'] = df['Shipping Method'].map(service_mapping).fillna('Xparcel Ground')

# Create billable weight based on carrier rules
def calculate_billable_weight(weight_oz):
    if pd.isna(weight_oz):
        return np.nan
    if weight_oz < 16:
        # Under 1 lb: round up to next oz, but 15.99 is special tier
        if weight_oz > 15 and weight_oz < 16:
            return 15.99
        else:
            return np.ceil(weight_oz)
    else:
        # Over 1 lb: round up to next pound, convert to oz
        return np.ceil(weight_oz / 16) * 16

df['Billable Weight (oz)'] = df['Weight (oz)'].apply(calculate_billable_weight)

# Create complete weight list
weight_list = []
# Under 1 lb (1-15 oz)
for oz in range(1, 16):
    weight_list.append((f"{oz}oz", oz))
# Special 15.99oz tier
weight_list.append(("15.99oz", 15.99))
# 16oz (1 lb) up to 400oz (25 lbs) in 1 lb increments
for lb in range(1, 26):  # 1-25 lbs
    weight_list.append((f"{lb*16}oz", lb*16))

# Initialize the matrix
services = ['Xparcel Priority', 'Xparcel Expedited', 'Xparcel Ground']
matrix_data = []

print("=" * 100)
print("UPSTATE PREP - VOLUME DISTRIBUTION BY WEIGHT AND SERVICE LEVEL")
print("For Excel Copy/Paste into Tier Tool")
print("=" * 100)
print()

# Create matrix
for weight_label, weight_val in weight_list:
    row = {'Weight': weight_label}
    
    for service in services:
        # Count packages in this weight and service level
        if weight_val == 15.99:
            count = len(df[(df['Billable Weight (oz)'] == 15.99) & (df['Xparcel Service'] == service)])
        else:
            count = len(df[(df['Billable Weight (oz)'] == weight_val) & (df['Xparcel Service'] == service)])
        
        row[service] = count
    
    # Add total for this weight
    if weight_val == 15.99:
        row['Total'] = len(df[df['Billable Weight (oz)'] == 15.99])
    else:
        row['Total'] = len(df[df['Billable Weight (oz)'] == weight_val])
    
    matrix_data.append(row)

# Create DataFrame
matrix_df = pd.DataFrame(matrix_data)

# Calculate service totals
service_totals = {'Weight': 'TOTAL'}
for service in services:
    service_totals[service] = matrix_df[service].sum()
service_totals['Total'] = matrix_df['Total'].sum()

# Print for Excel copy/paste (tab-delimited)
print("COPY AND PASTE THIS INTO EXCEL:")
print("=" * 80)
print()
print("Weight\tXparcel Priority\tXparcel Expedited\tXparcel Ground\tTotal")

for _, row in matrix_df.iterrows():
    print(f"{row['Weight']}\t{int(row['Xparcel Priority'])}\t{int(row['Xparcel Expedited'])}\t{int(row['Xparcel Ground'])}\t{int(row['Total'])}")

# Add totals
print(f"TOTAL\t{int(service_totals['Xparcel Priority'])}\t{int(service_totals['Xparcel Expedited'])}\t{int(service_totals['Xparcel Ground'])}\t{int(service_totals['Total'])}")

print()
print("=" * 100)
print("SUMMARY STATISTICS")
print("=" * 100)
print(f"Total Packages: {int(service_totals['Total'])}")
print()
print("Volume by Service Level:")
for service in services:
    pct = (service_totals[service] / service_totals['Total']) * 100 if service_totals['Total'] > 0 else 0
    print(f"  {service}: {int(service_totals[service])} packages ({pct:.1f}%)")

print()
print("Top Weight Categories with Service Mix:")
# Find top weights
top_weights = matrix_df.nlargest(10, 'Total')
for _, row in top_weights.iterrows():
    if row['Total'] > 0:
        print(f"\n  {row['Weight']}: {int(row['Total'])} total")
        for service in services:
            if row[service] > 0:
                pct = (row[service] / row['Total']) * 100
                print(f"    - {service}: {int(row[service])} ({pct:.1f}%)")

# Save to file
matrix_df_with_totals = pd.concat([matrix_df, pd.DataFrame([service_totals])], ignore_index=True)
matrix_df_with_totals.to_csv('upstate_prep_service_matrix.csv', index=False)

# Also save tab-delimited version for easy copy/paste
with open('upstate_prep_service_matrix.txt', 'w') as f:
    f.write("UPSTATE PREP - VOLUME BY WEIGHT AND SERVICE LEVEL\n")
    f.write("Copy and paste directly into Excel\n\n")
    f.write("Weight\tXparcel Priority\tXparcel Expedited\tXparcel Ground\tTotal\n")
    for _, row in matrix_df.iterrows():
        f.write(f"{row['Weight']}\t{int(row['Xparcel Priority'])}\t{int(row['Xparcel Expedited'])}\t{int(row['Xparcel Ground'])}\t{int(row['Total'])}\n")
    f.write(f"TOTAL\t{int(service_totals['Xparcel Priority'])}\t{int(service_totals['Xparcel Expedited'])}\t{int(service_totals['Xparcel Ground'])}\t{int(service_totals['Total'])}\n")

print()
print("Files saved:")
print("  - upstate_prep_service_matrix.csv")
print("  - upstate_prep_service_matrix.txt")