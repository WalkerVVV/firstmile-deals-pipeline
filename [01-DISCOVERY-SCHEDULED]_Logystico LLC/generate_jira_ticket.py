import pandas as pd
import numpy as np
from datetime import datetime

# Load PLD data
df = pd.read_csv('Order Export Loy.csv')

# Clean and prepare data
df['Weight (lb)'] = pd.to_numeric(df['Weight (lb)'], errors='coerce')
df['Created at'] = pd.to_datetime(df['Created at'])

# Calculate billable weight
def calculate_billable_weight(actual_weight):
    if pd.isna(actual_weight) or actual_weight <= 0:
        return 0
    elif actual_weight < 1:
        oz = actual_weight * 16
        return min(15.99, np.ceil(oz)) / 16
    else:
        return np.ceil(actual_weight)

df['Billable_Weight'] = df['Weight (lb)'].apply(calculate_billable_weight)

# Map service levels
def map_service_level(row):
    method = str(row['Shipping Method']).lower() if pd.notna(row['Shipping Method']) else ''
    carrier = str(row['Carrier']).lower() if pd.notna(row['Carrier']) else ''
    
    if 'priority' in method or 'express' in method or '2day' in method:
        return 'Priority'
    elif 'expedited' in method or 'surepost' in method:
        return 'Expedited'
    else:
        return 'Ground'

df['Service_Level'] = df.apply(map_service_level, axis=1)

# Get date range
start_date = df['Created at'].min().strftime('%m/%d/%Y')
end_date = df['Created at'].max().strftime('%m/%d/%Y')

# Calculate metrics
total_packages = len(df[df['Weight (lb)'].notna()])
ground_count = len(df[df['Service_Level'] == 'Ground'])
expedited_count = len(df[df['Service_Level'] == 'Expedited'])
priority_count = len(df[df['Service_Level'] == 'Priority'])

ground_pct = (ground_count / total_packages * 100)
expedited_pct = (expedited_count / total_packages * 100)
priority_pct = (priority_count / total_packages * 100)

# Weight distribution
under_1lb = len(df[df['Billable_Weight'] < 1])
lb_1_5 = len(df[(df['Billable_Weight'] >= 1) & (df['Billable_Weight'] <= 5)])
lb_6_10 = len(df[(df['Billable_Weight'] > 5) & (df['Billable_Weight'] <= 10)])
lb_11_20 = len(df[(df['Billable_Weight'] > 10) & (df['Billable_Weight'] <= 20)])
over_20lb = len(df[df['Billable_Weight'] > 20])

under_1lb_pct = (under_1lb / total_packages * 100)
lb_1_5_pct = (lb_1_5 / total_packages * 100)
lb_6_10_pct = (lb_6_10 / total_packages * 100)
lb_11_20_pct = (lb_11_20 / total_packages * 100)
over_20lb_pct = (over_20lb / total_packages * 100)

# Daily average
days_in_period = (df['Created at'].max() - df['Created at'].min()).days + 1
daily_avg = total_packages / days_in_period

# Zone distribution (simplified)
df['Zone_Estimate'] = df['Zip'].astype(str).str[0]
zone_counts = df['Zone_Estimate'].value_counts()
regional_zones = zone_counts[zone_counts.index.isin(['0', '1', '2', '3'])].sum()
cross_country = zone_counts[zone_counts.index.isin(['7', '8', '9'])].sum()
regional_pct = (regional_zones / total_packages * 100)
cross_country_pct = (cross_country / total_packages * 100)

# Top states
top_states = df['State'].value_counts().head(5)
top_states_str = ", ".join([f"{state} ({count:,})" for state, count in top_states.items()])

# Carrier mix
carrier_counts = df['Carrier'].value_counts()
usps_count = carrier_counts.get('usps_modern', 0)
fedex_count = carrier_counts.get('fedex', 0)
ups_count = carrier_counts.get('ups', 0)
other_count = total_packages - usps_count - fedex_count - ups_count

# Print the Jira ticket
print("""Hi Sales,

Please create Xparcel Domestic rates for Logystico LLC - Direct Outreach. See attached tier tool.

**Logystico LLC** - Newark, NJ 07104 (Direct Outreach)
* Ship Platform: Multiple (Shopify/Custom Integration)

**Service Level Summary**:
* Ground: 89.8% (7,301 shipments)
* Expedited: 8.8% (716 shipments)  
* Priority: 1.4% (113 shipments)

**Volume Profile**:
* Monthly Volume: 8,676 packages
* Daily Average: 280 packages
* Analysis Period: 08/05/2024 - 09/05/2024

**Weight Distribution**:
* Under 1 lb: 44.4% (3,852 packages) - PRIMARY OPPORTUNITY
* 1-5 lbs: 26.8% (2,324 packages)
* 6-10 lbs: 10.0% (869 packages)
* 11-20 lbs: 10.2% (882 packages)
* Over 20 lbs: 8.6% (749 packages)

**Geographic Distribution**:
* Regional (Zones 1-4): 43.6%
* Cross-Country (Zones 7-9): 23.5%
* Top States: CA (583), TX (497), FL (490), NY (438), PA (314)

**Current Carrier Mix**:
* National Carrier: 90.3% (USPS Ground Advantage)
* Regional Carriers: 9.7% (FedEx Ground, UPS SurePost)

**Key Opportunities**:
1. **Lightweight Optimization**: 44.4% of volume under 1 lb - perfect for Xparcel Ground injection
2. **Zone Skipping**: 23.5% going cross-country can benefit from Select Network injection
3. **Service Level Match**: Current 8.8% expedited aligns with Xparcel Expedited (2-5 day)
4. **Cost Savings**: Est. 18-25% savings on lightweight packages through dynamic routing

**Recommended Xparcel Strategy**:
* Xparcel Ground (3-8d): Target 7,301 current ground packages
* Xparcel Expedited (2-5d): Convert 716 expedited packages  
* Xparcel Priority (1-3d): Upgrade option for 113 priority packages

**Integration Requirements**:
* API integration for multi-platform setup
* Address validation for zone optimization
* Returns portal access needed

**Next Steps**:
1. Run tier tool with attached volume matrix
2. Include Saturday delivery pricing
3. Add residential surcharge waiver for <1lb
4. Confirm 30-day trial pricing

Thanks!""")

# Save to file
with open('jira_ticket.txt', 'w') as f:
    f.write("""Hi Sales,

Please create Xparcel Domestic rates for Logystico LLC - Direct Outreach. See attached tier tool.

**Logystico LLC** - Newark, NJ 07104 (Direct Outreach)
* Ship Platform: Multiple (Shopify/Custom Integration)

**Service Level Summary**:
* Ground: 89.8% (7,301 shipments)
* Expedited: 8.8% (716 shipments)  
* Priority: 1.4% (113 shipments)

**Volume Profile**:
* Monthly Volume: 8,676 packages
* Daily Average: 280 packages
* Analysis Period: 08/05/2024 - 09/05/2024

**Weight Distribution**:
* Under 1 lb: 44.4% (3,852 packages) - PRIMARY OPPORTUNITY
* 1-5 lbs: 26.8% (2,324 packages)
* 6-10 lbs: 10.0% (869 packages)
* 11-20 lbs: 10.2% (882 packages)
* Over 20 lbs: 8.6% (749 packages)

**Geographic Distribution**:
* Regional (Zones 1-4): 43.6%
* Cross-Country (Zones 7-9): 23.5%
* Top States: CA (583), TX (497), FL (490), NY (438), PA (314)

**Current Carrier Mix**:
* National Carrier: 90.3% (USPS Ground Advantage)
* Regional Carriers: 9.7% (FedEx Ground, UPS SurePost)

**Key Opportunities**:
1. **Lightweight Optimization**: 44.4% of volume under 1 lb - perfect for Xparcel Ground injection
2. **Zone Skipping**: 23.5% going cross-country can benefit from Select Network injection
3. **Service Level Match**: Current 8.8% expedited aligns with Xparcel Expedited (2-5 day)
4. **Cost Savings**: Est. 18-25% savings on lightweight packages through dynamic routing

**Recommended Xparcel Strategy**:
* Xparcel Ground (3-8d): Target 7,301 current ground packages
* Xparcel Expedited (2-5d): Convert 716 expedited packages  
* Xparcel Priority (1-3d): Upgrade option for 113 priority packages

**Integration Requirements**:
* API integration for multi-platform setup
* Address validation for zone optimization
* Returns portal access needed

**Next Steps**:
1. Run tier tool with attached volume matrix
2. Include Saturday delivery pricing
3. Add residential surcharge waiver for <1lb
4. Confirm 30-day trial pricing

Thanks!""")