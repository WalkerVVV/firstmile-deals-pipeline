# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FirstMile shipping analysis project for the Loy account, containing order export data for parcel-level detail (PLD) analysis. The repository analyzes shipping patterns, carrier performance, and optimization opportunities.

## Data Structure

### Primary Data File: Order Export Loy.csv
- **Records**: ~8,677 shipping records
- **Key Fields**:
  - Distinct Items Shipped, Quantity shipped
  - Created at (timestamp)
  - Carrier (usps_modern, fedex, ups, uni_uni, genericlabel, shippo__rr_donnelley)
  - Shipping Method (Ground Advantage, Ground, SurePost, etc.)
  - Tracking Number
  - Address fields (Address 1, Address 2, City, Zip, State, Country)
  - Dimensions: Size (LxWxH in inches), Weight (lb), individual Height/Width/Length
  - Insurance Amount, Box Name, Alternate Tracking ID

## Common Analysis Tasks

### PLD (Parcel Level Detail) Analysis
Execute comprehensive shipping profile analysis in this order:
1. **Volume Profile**: Total shipments, daily average, marketplace mix
2. **Carrier Mix**: Volume/spend by carrier with percentages
3. **Service Level Distribution**: Services used with costs
4. **Weight Distribution**: 
   - Under 1 lb (by oz: 1-4, 5-8, 9-12, 13-15, 15.99, 16 exactly)
   - 1-5 lbs by billable pound
   - Over 5 lbs categories
5. **Dimensional Analysis**: Average dimensions, cubic volume analysis
6. **Zone Distribution**: Zones 1-8, Regional vs Cross-Country
7. **Geographic Distribution**: Top 10 states by volume
8. **Cost Analysis**: Total spend, average/median costs
9. **Billable Weight Impact**: Actual vs billable weight comparison

### Critical Billable Weight Rules
- Under 1 lb: Round UP to next whole oz, MAX 15.99 oz
- 16 oz exactly: Bills as 1 lb
- Over 1 lb: Round UP to next whole pound

### Key Analysis Thresholds
- 15.99 oz: Maximum before jumping to 2 lbs billable
- Weight rounding typically adds 25% to billable weight vs actual
- Focus on lightweight packages (<2 lbs) where most spend concentrates

## FirstMile Analysis Framework

### Service Level Mapping
- **Xparcel Ground**: 3-8 day economy service
- **Xparcel Expedited**: 2-5 day faster ground (1-20 lb)
- **Xparcel Priority**: 1-3 day premium with guarantee

### Network Classification
- **National Network**: Nationwide coverage (100% U.S. ZIPs)
- **Select Network**: High-density metro injection points

### Presentation Standards
- Always lead with SLA compliance metrics
- Use markdown tables for all data presentation
- Include bullet points for key insights
- Never name specific carrier partners (use "National" or "Select")
- Spell "eCommerce" with camel-case 'C'

## Python Analysis Patterns

When creating analysis scripts:
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('Order Export Loy.csv')

# Standard data cleaning
df['Weight (lb)'] = pd.to_numeric(df['Weight (lb)'], errors='coerce')
df['Created at'] = pd.to_datetime(df['Created at'])

# Calculate billable weight
def calculate_billable_weight(actual_weight):
    if actual_weight <= 0:
        return 0
    elif actual_weight < 1:
        # Convert to oz and round up
        oz = actual_weight * 16
        return min(15.99, np.ceil(oz)) / 16
    else:
        # Round up to next whole pound
        return np.ceil(actual_weight)
```

## Performance Reporting Format

When generating FirstMile Xparcel Performance Analytics Reports:

1. **MANDATORY SEQUENCE**:
   - SLA Compliance (PRIMARY - always first)
   - Operational Metrics Table
   - Transit Performance Breakdown
   - Top Destination States

2. **SLA Windows**:
   - Xparcel Priority: 3-day SLA
   - Xparcel Expedited: 5-day SLA
   - Xparcel Ground: 8-day SLA

3. **Performance Status**:
   - Perfect: 100%
   - Exceeds: ≥95%
   - Meets: ≥90%
   - Below: <90%

## Data Processing Commands

```bash
# Count total records
wc -l "Order Export Loy.csv"

# Preview data structure
head -10 "Order Export Loy.csv" | cut -d',' -f1-10

# Get unique carriers
cut -d',' -f4 "Order Export Loy.csv" | sort | uniq -c | sort -rn

# Extract date range
cut -d',' -f3 "Order Export Loy.csv" | tail -n +2 | sort | head -1
cut -d',' -f3 "Order Export Loy.csv" | tail -n +2 | sort | tail -1
```

## Important Notes

- This is a discovery-phase project (indicated by folder name: [01-DISCOVERY-SCHEDULED]_Loy)
- Focus on data-driven insights with supporting metrics
- Maintain professional tone in all analysis outputs
- Emphasize FirstMile advantages: dynamic routing, Audit Queue, unified platform
- All geographic analysis should consider regional hub mapping