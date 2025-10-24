# Josh's Frogs - FirstMile PLD Analysis Summary
*Analysis Date: November 2024*

## Executive Summary
Josh's Frogs is a live insect and reptile supplier with significant shipping volume and optimization opportunities. This analysis reveals a $2.34M annual revenue opportunity for FirstMile with 12-15% cost savings for the customer.

## Volume Profile
- **Total Shipments Analyzed**: 175,531 (March 2024 - August 2025)
- **Current Monthly Volume**: 27,000-31,000 packages
- **Daily Average**: 900-1,000 packages
- **Peak Month**: July 2025 with 31,603 shipments
- **Annual Run Rate**: ~324,000 packages

## Current Shipping Profile

### Carrier Mix
| Carrier | Volume % | Spend % | Avg Cost |
|---------|----------|---------|----------|
| USPS | 59.1% | 45.5% | $6.32 |
| FedEx | 25.5% | 31.0% | $9.99 |
| UPS | 11.1% | 20.8% | $15.31 |
| Others | 4.3% | 2.7% | Various |

### Service Distribution
- **USPS Ground Advantage**: 56.8% of volume
- **FedEx Services**: Mix of Ground, Home Delivery, Express options
- **UPS Ground**: 7.3% of volume
- **Premium Services**: Significant overnight/expedited usage

## Weight Analysis

### Weight Distribution
- **43.7% of packages under 1 lb** (76,777 packages)
- **Most common range**: 1-2 lbs (25.9% of volume)
- **Average actual weight**: 3.04 lbs
- **Average billable weight**: 3.33 lbs (17% increase)

### Critical Findings
- **7,996 packages at 15-15.99 oz threshold** - Prime optimization targets
- **21.6% of packages see >25% billable weight increase**
- **$286,241 spent on billable weight penalties**

### Detailed Weight Breakdown
| Weight Range | Volume % | Spend % |
|--------------|----------|---------|
| 1-4 oz | 2.8% | 2.0% |
| 5-8 oz | 19.0% | 13.9% |
| 9-12 oz | 9.4% | 7.3% |
| 13-15 oz | 10.4% | 8.5% |
| 15.01-15.99 oz | 2.2% | 1.9% |
| 16 oz exactly | 1.3% | 1.1% |
| 1-2 lbs | 25.9% | 21.7% |
| 2-3 lbs | 9.4% | 10.7% |
| 3-4 lbs | 5.2% | 7.6% |
| 4-5 lbs | 2.6% | 3.4% |
| Over 5 lbs | 11.9% | 21.9% |

## Geographic & Zone Distribution

### Zone Analysis
- **Regional (Zones 1-4)**: 65.1% - Opportunity for zone-skipping
- **Cross-Country (Zones 5-8)**: 34.9%
- **Origin**: Pennsylvania (ZIP 19529)

### Top Destination States
1. California - 8.1%
2. Texas - 6.1%
3. New York - 5.6%
4. Pennsylvania - 5.6%
5. Michigan - 5.2%
6. Ohio - 4.7%
7. Florida - 4.5%
8. Illinois - 3.8%
9. North Carolina - 3.6%
10. Washington - 3.1%

## Dimensional Profile
- **Average dimensions**: 9.8"L × 7.1"W × 6.2"H
- **93.1% of packages under 1 cubic foot**
- **Good profile for avoiding dimensional weight charges**

## Cost Analysis

### Current State
- **Total Annual Spend**: $1,441,814
- **Average Cost per Package**: $8.21
- **Median Cost**: $6.25
- **50.4% of packages cost under $7**

### Cost Distribution
| Cost Range | Volume % | Spend % |
|------------|----------|---------|
| $0-5 | 18.2% | 10.0% |
| $5-7 | 32.2% | 23.5% |
| $7-9 | 13.5% | 12.8% |
| $9-11 | 9.4% | 11.2% |
| $11+ | 15.6% | 42.6% |

## FirstMile Opportunity Analysis

### Revenue Projections
- **Monthly FirstMile Revenue**: $189,000-195,000
- **Annual FirstMile Revenue**: $2.27M-2.34M
- **Customer Monthly Savings**: $26,000-32,000
- **Customer Annual Savings**: $312,000-384,000

### Pricing Scenarios

#### Scenario 1: Standard FirstMile Optimization (12% savings)
- New average cost: $7.22/package
- Monthly revenue: $194,940
- Annual revenue: $2.34M

#### Scenario 2: Volume-Based Enterprise Pricing (15% savings)
- New average cost: $7.00/package
- Monthly revenue: $189,000
- Annual revenue: $2.27M

## Key Optimization Strategies

### 1. Weight Threshold Management
- Focus on 7,996 packages at 15-15.99 oz threshold
- Package redesign for items near billable thresholds
- Potential savings: $50,000+ annually

### 2. Carrier Optimization
- Migrate UPS Ground volume to Xparcel Ground
- USPS costs $6.32 vs UPS $15.31 (142% higher)
- Implement dynamic routing for FedEx volume

### 3. FirstMile Xparcel Service Mapping
- **Xparcel Ground (3-8 day)**: Map 59% USPS volume
- **Xparcel Expedited (2-5 day)**: For time-sensitive shipments
- **Xparcel Priority (1-3 day)**: Replace premium services

### 4. Network Optimization
- **National Network**: Full ZIP coverage
- **Select Network**: Zone-skip for 65% regional volume
- Dynamic routing optimization

## Implementation Recommendations

### Immediate Actions
1. **Rate Card Review**: Present 12% savings proposal
2. **Live Animal Compliance**: Verify Xparcel compatibility with live insect requirements
3. **API Integration**: Plan technical implementation
4. **Pilot Program**: Start with 1,000 packages for validation

### Value Propositions
- **For Josh's Frogs**:
  - 12-15% cost reduction ($26-32K monthly savings)
  - Single integration for all services
  - Enhanced tracking and claims management
  - Audit Queue prevents billing errors

- **For FirstMile**:
  - Stable high-volume customer
  - $2.3M+ annual revenue
  - Growth potential (shown 10% growth trend)
  - Predictable lightweight shipping profile

### Success Metrics
- Cost per package reduction: Target <$7.25
- On-time delivery: Maintain >95%
- Claims reduction: Target <0.5%
- Customer satisfaction: NPS >8

## Technical Details

### Data Files Created
1. `pld_analysis.py` - Comprehensive PLD analysis script
2. `monthly_volume_analysis.py` - Monthly trending analysis
3. `create_excel_report.py` - Excel report generation
4. `Joshs_Frogs_PLD_Analysis.xlsx` - Complete Excel workbook with 8 detailed sheets

### Analysis Methodology
- Analyzed 175,531 shipment records
- Date range: March 2024 - August 2025
- Billable weight calculations per carrier rules
- Zone estimation based on ZIP3 analysis
- State mapping from destination ZIPs

## HubSpot Integration Notes

### Deal Properties to Update
- Deal Value: $2,340,000
- Close Date: Q1 2025
- Pipeline Stage: Discovery/Rate Creation
- Annual Volume: 324,000 packages
- Monthly Volume: 27,000 packages
- Current Annual Spend: $1,440,000
- Estimated Savings: $320,000

### Key Selling Points
1. **Volume**: Consistent 27,000 monthly packages
2. **Profile**: 43.7% lightweight ideal for Xparcel
3. **Geography**: 65% regional for zone-skipping
4. **Growth**: Scaled from 28 to 31,000 packages/month
5. **Savings**: Clear 12-15% cost reduction opportunity

## Conclusion
Josh's Frogs represents an ideal FirstMile customer with consistent high volume, lightweight profile, and regional concentration. The $2.34M annual revenue opportunity with clear value delivery makes this a priority prospect for Q1 2025 implementation.

---
*Analysis performed using FirstMile PLD framework*
*Last updated: November 2024*