import pandas as pd

# Load the aggregated data
df = pd.read_csv('247bef97-8663-431e-b2f5-dd2ca243633d.csv')

# Clean up the data - remove Grand Total row
df = df[df['Row Labels'] != 'Grand Total']

# Parse carrier and service from Row Labels
df['Carrier'] = df['Row Labels'].apply(lambda x: x.split('_')[0] if '_' in x else x)
df['Service'] = df['Row Labels']

# Group by carrier for summary
carrier_summary = df.groupby('Carrier').agg({
    'Count of Number': 'sum',
    'Average of Weight': 'mean'
}).round(2)

print('JOSH\'S FROGS - VOLUME ASSUMPTIONS FOR TIER TOOL')
print('=' * 60)
print()

# Total volume
total_volume = df['Count of Number'].sum()
print(f'Total Annual Volume: {total_volume:,} parcels')
print()

# Calculate daily average (assuming 260 shipping days/year)
daily_avg = total_volume / 260
print(f'Daily Average: {int(daily_avg):,} parcels')
print(f'Monthly Average: {int(total_volume/12):,} parcels')
print()

# Carrier mix
print('CARRIER MIX:')
print('-' * 40)
for carrier in carrier_summary.index:
    volume = carrier_summary.loc[carrier, 'Count of Number']
    pct = (volume / total_volume) * 100
    avg_weight = carrier_summary.loc[carrier, 'Average of Weight']
    print(f'{carrier:8} {int(volume):8,} ({pct:5.1f}%)  Avg: {avg_weight:.1f} lbs')

print()
print('SERVICE BREAKDOWN FOR TIER TOOL:')
print('-' * 40)

# Key services for tier tool
usps_ground = df[df['Row Labels'] == 'USPS_GROUND_ADVANTAGE']['Count of Number'].sum()
usps_priority = df[df['Row Labels'] == 'USPS_PRIORITY_MAIL']['Count of Number'].sum()
usps_first = df[df['Row Labels'] == 'USPS_FIRST_CLASS_MAIL']['Count of Number'].sum()
ups_ground = df[df['Row Labels'].str.contains('UPS_GROUND')]['Count of Number'].sum()
fedex_ground = df[df['Row Labels'].str.contains('FEDEX_GROUND|FEDEX_HOME')]['Count of Number'].sum()
express_services = df[df['Row Labels'].str.contains('OVERNIGHT|EXPRESS|EXPEDITED|TWO_DAY|SECOND_DAY|THREE_DAY')]['Count of Number'].sum()

print(f'USPS Ground Advantage: {usps_ground:,} ({(usps_ground/total_volume)*100:.1f}%)')
print(f'USPS Priority Mail: {usps_priority:,} ({(usps_priority/total_volume)*100:.1f}%)')
print(f'UPS Ground: {ups_ground:,} ({(ups_ground/total_volume)*100:.1f}%)')
print(f'FedEx Ground/Home: {fedex_ground:,} ({(fedex_ground/total_volume)*100:.1f}%)')
print(f'Express/Expedited Services: {express_services:,} ({(express_services/total_volume)*100:.1f}%)')

print()
print('WEIGHT DISTRIBUTION:')
print('-' * 40)

# Weight buckets for tier tool
light = df[df['Average of Weight'] <= 1]['Count of Number'].sum()
medium = df[(df['Average of Weight'] > 1) & (df['Average of Weight'] <= 5)]['Count of Number'].sum()
heavy = df[df['Average of Weight'] > 5]['Count of Number'].sum()

print(f'Under 1 lb: {light:,} ({(light/total_volume)*100:.1f}%)')
print(f'1-5 lbs: {medium:,} ({(medium/total_volume)*100:.1f}%)')
print(f'Over 5 lbs: {heavy:,} ({(heavy/total_volume)*100:.1f}%)')

# Calculate weighted average
total_weight_sum = sum(df['Count of Number'] * df['Average of Weight'])
overall_avg_weight = total_weight_sum / total_volume
print(f'\nOverall Average Weight: {overall_avg_weight:.2f} lbs')

print()
print('TIER TOOL INPUT SUMMARY:')
print('=' * 60)
print('Copy these values to your tier tool:')
print()
print(f'Annual Volume: {total_volume:,}')
print(f'Daily Average: {int(daily_avg):,}')
print(f'Average Weight: {overall_avg_weight:.2f} lbs')
print()
print('Service Mix:')
print(f'  Ground Services: {(usps_ground + ups_ground + fedex_ground)/total_volume*100:.0f}%')
print(f'  Express Services: {express_services/total_volume*100:.0f}%')
print(f'  USPS Dominant: {df[df["Carrier"] == "USPS"]["Count of Number"].sum()/total_volume*100:.0f}%')