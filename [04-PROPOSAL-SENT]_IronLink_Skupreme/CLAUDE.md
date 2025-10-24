# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FirstMile IronLink deals analysis project focused on shipping data analysis and reporting. The project contains shipping order data and templates for customer proposals and performance analytics.

## Key Files

- **IronLink Orders Report.csv**: Main shipment data file containing tracking numbers, service levels, addresses, dimensions, weights, and delivery status
- **FirstMile_Move_Update_Template.txt**: Customer proposal template for rate comparisons and FirstMile solution advantages
- **IronLink_Shipment_Analysis_Report.pdf**: Analysis reports (multiple versions)

## Data Structure

The CSV order data contains:
- Shipment metadata (created date, tracking number, provider, service level)
- Origin/destination addresses (from/to name, street, city, state, zip, country)
- Package dimensions (length, width, height, weight)
- Delivery status and created_by information
- Reference numbers and metadata fields

## FirstMile Service Definitions

When analyzing or reporting on service levels:
- **Xparcel Ground**: 3-8 day economy ground service
- **Xparcel Expedited**: 2-5 day faster ground solution (1-20 lb)
- **Xparcel Priority**: 1-3 day premium option with money-back guarantee

## Analysis Tasks

Common analysis operations include:
1. **Service Level Performance**: Calculate SLA compliance for each service type
2. **Geographic Distribution**: Analyze top destination states and regional patterns
3. **Weight Profile Analysis**: Distribution of packages by weight categories
4. **Transit Time Analysis**: Calculate average days in transit by service level
5. **Volume Metrics**: Daily/monthly shipping volumes and patterns

## Performance Reporting Standards

When generating FirstMile performance reports, always follow this mandatory sequence:
1. **SLA Compliance** (always first - primary metric)
2. **Operational Metrics Table**
3. **Transit Performance Breakdown Table**
4. **Top Destination States Table**

SLA Windows:
- Xparcel Priority: 3-day SLA
- Xparcel Expedited: 5-day SLA
- Xparcel Ground: 8-day SLA

Performance thresholds:
- Perfect Compliance: 100%
- Exceeds Standard: ≥95%
- Meets Standard: ≥90%
- Below Standard: <90%

## Important Constraints

- Never name specific carrier partners (UPS, FedEx, etc.) - use "National" or "Select" network
- Always emphasize FirstMile advantages: dynamic routing, Audit Queue, Claims, Returns, single support
- Spell "eCommerce" with camel-case 'C'
- Present Xparcel as FirstMile ship-methods, not a separate company
- Never lead reports with daily delivery percentages - SLA compliance comes first

## Data Processing Notes

- The CSV uses ISO datetime format for timestamps
- Tracking numbers may be in scientific notation - handle appropriately
- Service level mapping: Ground/Surepost → Xparcel Ground, Expedited → Xparcel Expedited
- Weight is in pounds (lb), dimensions in inches (in)
- All addresses include standard US/International format fields

## Common Commands

For data analysis in Python:
```python
import pandas as pd

# Load shipment data
df = pd.read_csv('IronLink Orders Report.csv')

# Parse dates
df['object created'] = pd.to_datetime(df['object created'])

# Filter by service level
ground_shipments = df[df['rate__servicelevel__servicelevel_name'] == 'Ground']

# Analyze destination states
state_distribution = df['rate__shipment__address_to__state'].value_counts()

# Calculate average weight by service
avg_weight_by_service = df.groupby('rate__servicelevel__servicelevel_name')['parcel__weight'].mean()
```

## Proposal Generation

When creating customer proposals:
1. Extract current state metrics (volume, avg weight, costs, transit times)
2. Calculate FirstMile solution savings (typically 40% cost reduction)
3. Highlight transit time improvements (e.g., 2.5 day average)
4. Emphasize single integration and intelligent routing advantages
5. Include clear next steps with contact information