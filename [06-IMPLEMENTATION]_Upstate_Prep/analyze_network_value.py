import pandas as pd
import numpy as np

# Load the PLD data
df = pd.read_csv('T30 PLD Upstate Prep.csv')

# Clean and analyze data
df['Label Cost'] = pd.to_numeric(df['Label Cost'], errors='coerce')
df['Weight (lb)'] = pd.to_numeric(df['Weight (lb)'], errors='coerce')

# Top states analysis
state_summary = df.groupby('State').agg({
    'Shipping Label ID': 'count',
    'Label Cost': 'sum'
}).rename(columns={'Shipping Label ID': 'Volume'})
state_summary['% of Volume'] = (state_summary['Volume'] / state_summary['Volume'].sum() * 100).round(1)
state_summary = state_summary.sort_values('Volume', ascending=False).head(15)

print('=' * 60)
print('TOP 15 DESTINATION STATES:')
print('=' * 60)
print(state_summary.to_string())
print()

# Service level analysis
service_summary = df.groupby('Shipping Method').agg({
    'Shipping Label ID': 'count',
    'Label Cost': ['sum', 'mean']
}).round(2)
service_summary.columns = ['Volume', 'Total Cost', 'Avg Cost']
print('=' * 60)
print('SERVICE LEVEL DISTRIBUTION:')
print('=' * 60)
print(service_summary.to_string())
print()

# Weight analysis for lightweight packages
df['Billable Weight'] = df['Weight (lb)'].apply(lambda x: min(1, np.ceil(x*16)/16) if x <= 1 else np.ceil(x))
lightweight = df[df['Weight (lb)'] <= 1]
print('=' * 60)
print('LIGHTWEIGHT ANALYSIS (<1 lb):')
print('=' * 60)
print(f'Total lightweight packages: {len(lightweight)} ({len(lightweight)/len(df)*100:.1f}% of total)')
print(f'Average weight: {lightweight["Weight (lb)"].mean():.3f} lbs')
print(f'Total spend on lightweight: ${lightweight["Label Cost"].sum():.2f}')
print()

# Zone-skipping opportunity analysis
# Map states to potential induction points from the network map
state_to_hub = {
    'CA': 'LAX',
    'TX': 'DFW/IAH',  
    'FL': 'MIA',
    'NY': 'JFK',
    'PA': 'JFK',
    'OH': 'ORD',
    'IL': 'ORD',
    'NC': 'ATL',
    'GA': 'ATL',
    'WA': 'SEA',
    'NV': 'SLC',
    'CO': 'DEN',
    'MI': 'ORD/DTW',
    'MA': 'JFK',
    'NJ': 'JFK'
}

# Add hub mapping to states
for state, vol_data in state_summary.iterrows():
    hub = state_to_hub.get(state, 'Regional')
    print(f'{state}: {vol_data["Volume"]} packages → FirstMile Hub: {hub}')