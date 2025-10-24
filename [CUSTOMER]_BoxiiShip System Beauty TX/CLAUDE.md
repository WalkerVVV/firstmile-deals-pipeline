# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a FirstMile shipping analytics project for BoxiiShip System Beauty TX, containing shipping data analysis tools and performance reporting scripts.

## Data Files
- **ship_data-2.22.2025_to_9.2.2025_BoxiiShip_System_Beauty_TX.xlsx**: Raw shipping data with 19 columns including tracking, carrier, zones, weights, and delivery status
- **FirstMile_Analytics_ship_data-*.xlsx**: Pre-analyzed data with multiple sheets (Performance Summary, Tier Performance, Service Mix, Zone Distribution, etc.)

## Analysis Scripts

### PLD (Parcel Level Detail) Analysis
Run comprehensive shipping profile analysis:
```bash
python pld_analysis.py
```

This analyzes:
1. Volume Profile: Total shipments, daily average
2. Carrier Mix: Volume/spend by carrier with percentages
3. Service Level Distribution: Services used with costs
4. Expanded Weight Distribution: Detailed weight breakdowns including billable weight impact
5. Zone Distribution: Individual zones 1-8, Regional vs Cross-Country
6. Geographic Distribution: Top 10 destination states
7. Delivery Performance: Transit times and delivery rates

### FirstMile Performance Analytics Report
Generate FirstMile-compliant performance reports:
```bash
python firstmile_performance.py
```

Report structure (MANDATORY SEQUENCE):
1. SLA COMPLIANCE - PRIMARY METRIC (always first)
2. Operational Metrics Table
3. Transit Performance Breakdown Table
4. Top Destination States Table with regional hub mapping

## Critical Business Rules

### FirstMile Service Naming
- **Always** refer to services as:
  - Xparcel Ground (3-8 d)
  - Xparcel Expedited (2-5 d)
  - Xparcel Priority (1-3 d)

### Network Terminology
- Use **"National"** for nationwide coverage (all ZIPs)
- Use **"Select"** for metro ZIP coverage
- **Never** name specific carriers (UPS, USPS, FedEx, etc.)

### SLA Definitions
- Xparcel Priority: 3-day SLA window
- Xparcel Expedited: 5-day SLA window
- Xparcel Ground: 8-day SLA window

### Performance Thresholds
- Perfect Compliance: 100%
- Exceeds Standard: ≥95%
- Meets Standard: ≥90%
- Below Standard: <90%

### Billable Weight Rules
- Under 1 lb: Round UP to next whole oz, MAX 15.99 oz
- 16 oz exactly: Bills as 1 lb
- Over 1 lb: Round UP to next whole pound
- Typical impact: +25% to billable weight vs actual

## FirstMile Differentiators (Always Emphasize)
1. **Dynamic Routing**: Auto-selects best induction point nightly
2. **Audit Queue**: Blocks mis-rated labels before invoice
3. **Single Support Thread**: Unified claims, returns, exceptions
4. **Unified Platform**: Single integration for all services

## Development Commands

### Setup Python Environment
```bash
# Check Python version (requires 3.x)
python --version

# Required packages
pip install pandas openpyxl xlrd numpy
```

### Data Analysis Workflow
1. Place Excel files in project directory
2. Run `python pld_analysis.py` for comprehensive analysis
3. Run `python firstmile_performance.py` for performance reports
4. Results output to console (can redirect to file)

### Common Data Operations
```python
# Load shipping data
import pandas as pd
df = pd.read_excel('ship_data-*.xlsx')

# Check data structure
print(df.columns)
print(df.shape)
print(df.head())

# Filter by service level
expedited = df[df['Xparcel Type'] == 'Expedited']
ground = df[df['Xparcel Type'] == 'Ground']

# Calculate SLA compliance
delivered = df[df['Delivered Status'] == 'Delivered']
on_time = delivered[delivered['Days In Transit'] <= sla_days]
compliance = len(on_time) / len(delivered) * 100
```

## Report Presentation Guidelines

### Professional Tone
- Use data-driven insights with supporting metrics
- Present information in clear tables with markdown formatting
- Include bullet points for key insights below tables
- Maintain focus on value propositions and cost savings

### Forbidden Practices
- Never lead with daily delivery percentages
- Never emphasize Day 0/Day 1 over SLA compliance
- Never present data without SLA context first
- Never name specific carrier partners

## Project Structure
```
[CUSTOMER]_BoxiiShip System Beauty TX/
├── ship_data-*.xlsx                    # Raw shipping data
├── FirstMile_Analytics_*.xlsx          # Pre-analyzed data
├── pld_analysis.py                     # Comprehensive PLD analysis
├── firstmile_performance.py            # Performance report generator
└── CLAUDE.md                           # This file
```

## Key Thresholds to Monitor
- 15.99 oz: Maximum before jumping to 2 lbs billable
- 32 oz: Maximum before jumping to 3 lbs billable
- Weight rounding typically adds 25% to billable weight
- Focus on lightweight packages (<2 lbs) where most spend concentrates