# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FirstMile Upstate Prep deals analysis project in the Discovery Complete stage. The project contains T30 (trailing 30 days) Parcel Level Detail (PLD) shipping data for analysis and proposal generation. The project also includes two Safety Data Sheets (SDS) for isopropyl alcohol products, which are relevant for hazmat shipping considerations.

## Key Files

- **T30 PLD Upstate Prep.csv**: Main PLD shipping data file (10,428 rows) containing comprehensive parcel-level shipment details from Upstate Prep warehouse
- **75% Isopropyl Alcohol SDS.pdf**: Safety data sheet for 75% isopropyl alcohol products
- **99% Isopropyl Alcohol SDS.pdf**: Safety data sheet for 99% isopropyl alcohol products (hazmat consideration)

## Data Structure

The PLD CSV contains the following columns:
- **Shipping Label ID**: Unique identifier for each shipment
- **Quantity shipped**: Number of units in shipment
- **Order date**: Date order was placed
- **Created at**: Label creation timestamp
- **Company**: Customer company name (if applicable)
- **Phone**: Customer phone number
- **Order Number**: Internal order ID
- **Profile**: Shipping profile used (Default 2, default)
- **Warehouse**: Origin facility (Upstate Prep / Primary)
- **Warehouse ID**: Facility identifier (113705)
- **Order ID**: System order identifier
- **Carrier**: Shipping carrier (ups, amazon_shipping_api_v2, shippo__usps)
- **Shipping Method**: Service level (UPS Ground, UPS 2nd Day Air, Amazon Shipping Ground, usps_ground_advantage)
- **Shipping Name**: Service category (Standard, Expedited, FreeEconomy)
- **Tracking Number**: Carrier tracking number
- **City, State, Zip, Country**: Destination address details
- **Size (Length x Width x Height) (in)**: Package dimensions in inches
- **Weight (lb)**: Package weight in pounds
- **Height, Width, Length (in)**: Individual dimension fields
- **Insurance Amount**: Declared value for insurance
- **Box Name**: Package type identifier
- **Label Cost**: Shipping cost
- **Difference**: Cost differential (negative values indicate savings)

## Analysis Framework

### PLD Analysis Components (Execute in Order)

1. **Volume Profile**: Total shipments, daily average, marketplace mix
2. **Carrier Mix**: Volume/spend by carrier with percentages
3. **Service Level Distribution**: Services used with costs
4. **Expanded Weight Distribution**: 
   - Under 1 lb: 1-4, 5-8, 9-12, 13-15, 15.99, 16 oz exactly
   - 1-5 lbs by billable pound (2, 3, 4, 5 lbs)
   - Over 5 lbs categories
5. **Dimensional Analysis**: Average dims, cubic volume (</>1 cu ft)
6. **Zone Distribution**: Individual zones 1-8, Regional vs Cross-Country
7. **Geographic Distribution**: Top 10 states
8. **Cost Analysis**: Total spend, avg/median costs
9. **Billable Weight Impact**: Actual vs billable weight comparison

### Critical Billable Weight Rules

- Under 1 lb: Round UP to next whole oz, MAX 15.99 oz
- 16 oz exactly: Bills as 1 lb (16 oz)
- Over 1 lb: Round UP to next whole pound (32, 48, 64 oz, etc.)
- Weight rounding typically adds 25% to billable weight vs actual

## Common Analysis Commands

```python
import pandas as pd
import numpy as np

# Load PLD data
df = pd.read_csv('T30 PLD Upstate Prep.csv')

# Parse dates
df['Order date'] = pd.to_datetime(df['Order date'])
df['Created at'] = pd.to_datetime(df['Created at'])

# Clean numeric fields
df['Weight (lb)'] = pd.to_numeric(df['Weight (lb)'], errors='coerce')
df['Label Cost'] = pd.to_numeric(df['Label Cost'], errors='coerce')

# Carrier volume analysis
carrier_summary = df.groupby('Carrier').agg({
    'Shipping Label ID': 'count',
    'Label Cost': 'sum'
}).rename(columns={'Shipping Label ID': 'Volume'})

# Service level analysis
service_summary = df.groupby('Shipping Method').agg({
    'Shipping Label ID': 'count',
    'Label Cost': ['sum', 'mean']
})

# State distribution
state_dist = df['State'].value_counts().head(10)

# Weight distribution with billable weight rules
def calculate_billable_weight(weight_lb):
    """Apply carrier billable weight rules"""
    weight_oz = weight_lb * 16
    if weight_oz <= 16:
        return min(16, np.ceil(weight_oz)) / 16  # Round up to next oz, max 15.99
    else:
        return np.ceil(weight_lb)  # Round up to next pound

df['Billable Weight'] = df['Weight (lb)'].apply(calculate_billable_weight)
```

## FirstMile Performance Analytics Report

When user requests "FirstMile Xparcel Performance Analytics Report", generate comprehensive report with:

### Report Requirements

1. **Header Information**:
   - Customer: Upstate Prep
   - Report Period: [from data date range]
   - Generated: [today's date]

2. **MANDATORY SEQUENCE**:
   - SLA COMPLIANCE - PRIMARY METRIC (always first)
   - Operational Metrics Table
   - Transit Performance Breakdown Table
   - Top Destination States Table

3. **Service Mapping**:
   - UPS Ground → Xparcel Ground (8-day SLA)
   - UPS 2nd Day Air → Xparcel Expedited (5-day SLA)
   - Amazon Shipping Ground → Xparcel Ground (8-day SLA)
   - USPS Ground Advantage → Xparcel Ground (8-day SLA)

## FirstMile Solution Positioning

When creating proposals or analyses, emphasize:

1. **Dynamic Routing**: Auto-selects best induction point nightly based on SLA & cost
2. **Audit Queue**: Blocks mis-rated labels before invoice hits A/P
3. **Single Support Thread**: Claims, returns, exceptions managed via one FirstMile ticket
4. **Unified Platform**: Single integration for all services and networks

Network terminology:
- **National Network**: Nationwide induction partners covering 100% U.S. ZIPs
- **Select Network**: High-density metro injection points for zone-skipping

## Project Stage Context

This account is in stage [02-DISCOVERY-COMPLETE], meaning:
- Discovery meeting has been completed
- Requirements have been gathered
- Ready for rate creation and proposal generation
- Next step: Move to [03-RATE-CREATION] for custom pricing matrix

## Hazmat Considerations

The presence of isopropyl alcohol SDS files indicates potential hazmat shipping:
- 75% concentration: Limited quantity exceptions may apply
- 99% concentration: Full hazmat requirements likely
- Consider special handling fees and carrier restrictions in proposals