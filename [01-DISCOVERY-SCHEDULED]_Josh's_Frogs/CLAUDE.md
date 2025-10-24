# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FirstMile shipping analytics project focused on analyzing parcel-level detail (PLD) data for shipping optimization and carrier performance analysis. The project deals with live insect shipping requirements and carrier cost/service analysis.

## Data Structure

### Primary Data File
- **247bef97-8663-431e-b2f5-dd2ca243633d.csv**: Parcel shipment data with columns:
  - Number (tracking ID)
  - Reseller (SENDLE, UPS_ALT)
  - Carrier (USPS, UPS)
  - Service (USPS_GROUND_ADVANTAGE, UPS_GROUND)
  - Origin ZIP (19529-9179 primary origin)
  - Destination ZIP
  - Weight (lbs)
  - Dimensions (Length, Width, Height in inches)
  - Packaging (CARDBOARD_BOX)
  - Cost ($)

### Supporting Documentation
- **Live Insects Requirements- Final (2).pdf**: Carrier requirements for shipping live insects/animals

## Analysis Framework

### PLD (Parcel Level Detail) Analysis Components

Execute analyses in this order:

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

### Key Thresholds
- 15.99 oz: Maximum before jumping to 2 lbs billable
- 32 oz: Maximum before jumping to 3 lbs billable
- Focus on lightweight packages (<2 lbs) where most spend concentrates

## FirstMile Xparcel Service Mapping

When analyzing or presenting data:

### Service Level Definitions
- **Xparcel Ground**: 3-8 day economy service (maps to USPS_GROUND_ADVANTAGE)
- **Xparcel Expedited**: 2-5 day faster ground (when expedited flag present)
- **Xparcel Priority**: 1-3 day premium option (maps to UPS services or priority indicators)

### Network Structure
- **National Network**: Nationwide coverage for all ZIPs
- **Select Network**: High-density metro injection points

### Key Constraints
- Refer to services as **"Xparcel Ground (3-8 d), Xparcel Expedited (2-5 d), Xparcel Priority (1-3 d)"**
- Frame carrier capacity as **"National"** and **"Select"** - do not name specific carriers
- Emphasize FirstMile advantages: dynamic routing, Audit Queue, Claims, Returns
- **Never** present Xparcel as separate company

## Performance Reporting Standards

When generating FirstMile Xparcel Performance Analytics Report:

### Mandatory Sequence
1. **SLA Compliance** (always first)
   - Xparcel Priority: 3-day SLA
   - Xparcel Expedited: 5-day SLA  
   - Xparcel Ground: 8-day SLA
2. Operational Metrics Table
3. Transit Performance Breakdown Table
4. Top Destination States Table

### Performance Thresholds
- Perfect Compliance: 100%
- Exceeds Standard: ≥95%
- Meets Standard: ≥90%
- Below Standard: <90%

### Data Mappings
- "USPS_GROUND_ADVANTAGE" = Xparcel Ground
- "UPS_GROUND" = May indicate Xparcel Priority based on cost/speed

## Common Analysis Tasks

### Zone Analysis
Calculate zones based on origin-destination ZIP pairs:
- Zones 1-4: Regional (same/adjacent regions)
- Zones 5-8: Cross-Country (distant regions)

### Cost Optimization
Focus areas:
- Weight optimization (especially packages near billable thresholds)
- Service level rightsizing
- Zone skipping opportunities via Select Network

### Carrier Performance
Analyze:
- Average cost per service level
- Weight distribution by carrier
- Geographic coverage patterns