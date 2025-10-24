# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FirstMile shipping data analysis project for DYLN. The repository contains fulfillment and shipment data that should be analyzed through the FirstMile lens to identify optimization opportunities and generate performance reports.

## Data Files

- `DYLN Fulfillment - Shipments.xlsx`: Raw shipment data
- `Pivot DYLN Fulfillment - Shipments.xlsx`: Pivoted/analyzed shipment data

## Analysis Framework

### PLD (Parcel Level Detail) Analysis

When analyzing shipping data, execute these components in order:

1. **Volume Profile**: Total shipments, daily average, marketplace mix
2. **Carrier Mix**: Volume/spend by carrier with percentages
3. **Service Level Distribution**: Services used with costs
4. **Weight Distribution**:
   - Under 1 lb: 1-4, 5-8, 9-12, 13-15, 15.99, 16 oz exactly
   - 1-5 lbs by billable pound
   - Over 5 lbs categories
5. **Dimensional Analysis**: Average dims, cubic volume
6. **Zone Distribution**: Zones 1-8, Regional vs Cross-Country
7. **Geographic Distribution**: Top states
8. **Cost Analysis**: Total spend, average/median costs
9. **Billable Weight Impact**: Actual vs billable comparison

### Critical Weight Rules

- Under 1 lb: Round UP to next whole oz, MAX 15.99 oz
- 16 oz exactly: Bills as 1 lb
- Over 1 lb: Round UP to next whole pound

## Python Analysis Commands

```python
# Load Excel data
import pandas as pd
df = pd.read_excel('DYLN Fulfillment - Shipments.xlsx')

# Basic analysis
df.info()
df.describe()
df.columns.tolist()
```

## FirstMile Service Mapping

When presenting results:
- **Xparcel Ground**: 3-8 day economy service
- **Xparcel Expedited**: 2-5 day faster ground (1-20 lb)
- **Xparcel Priority**: 1-3 day premium with guarantee

## Performance Report Generation

For FirstMile Xparcel Performance Analytics Reports, always present in this order:
1. SLA Compliance (PRIMARY - always first)
2. Operational Metrics Table
3. Transit Performance Breakdown
4. Top Destination States

SLA windows:
- Priority: 3 days
- Expedited: 5 days
- Ground: 8 days

## Important Constraints

- Never name specific carriers (UPS, FedEx, etc.) - use "National" or "Select" network
- Spell "eCommerce" with camel-case C
- Present Xparcel as FirstMile ship-methods, not separate company
- Lead with SLA compliance, not daily delivery percentages
- Emphasize FirstMile advantages: dynamic routing, Audit Queue, Claims, Returns support