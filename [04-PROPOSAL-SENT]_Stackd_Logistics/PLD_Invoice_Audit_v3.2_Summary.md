# Stackd Logistics - PLD Invoice Audit Builder v3.2 Results

## Executive Summary
**Analysis Date**: September 24, 2025
**Data Source**: Chin Mounts Shopify shipment data (August 2025)
**Total Shipments Analyzed**: 8,957
**Analysis Tool**: PLD Invoice Audit Builder v3.2 with Tab 10 Rate Discovery

## Financial Impact

### Current vs FirstMile Comparison
| Metric | Current State | With FirstMile | Savings | Savings % |
|--------|--------------|----------------|---------|-----------|
| **Monthly Spend** | $44,453.35 | $30,472.17 | $14,078.32 | 31.7% |
| **Annual Projection** | $533,440.20 | $365,666.04 | $168,939.79 | 31.7% |
| **Avg Cost/Package** | $4.96 | $3.40 | $1.56 | 31.5% |

### Key Findings

**Volume Profile**:
- 8,957 shipments analyzed
- 8,943 shipments (99.8%) show savings opportunity
- Average weight: 0.36 lb (ultra-lightweight profile)
- Zone 6 most common destination

**Service Mix Analysis**:
- **Current**: 70.6% DHL Expedited, 4% UPS 2nd Day Air
- **Recommended**: 95.9% Xparcel Ground, 4% Xparcel Expedited
- **Strategy**: Service downgrade from expedited to ground

**Weight Distribution Insights**:
- 99%+ packages under 1 lb
- Perfect for Select Network zone-skipping
- Billable weight optimization opportunity at 15.99 oz breakpoint

## Why v3.2 Shows Higher Savings Than v3.1

The PLD Invoice Audit Builder v3.2 identified **31.7% savings** (vs 9.7% in v3.1) due to:

1. **Corrected Xparcel Rate Structure**:
   - v3.1 used rates: $3.73-$4.24 (too high)
   - v3.2 uses rates: $2.89-$3.49 (accurate market rates)

2. **Tab 10 Rate Discovery**:
   - Auto-detects current carrier rates from PLD
   - Provides transparent rate comparison
   - Uses MODE/MEDIAN for accurate rate determination

3. **Service Mix Optimization**:
   - Properly identifies DHL Expedited → Xparcel Ground opportunity
   - 95.9% of volume can use ground service (3-8 days)
   - Maintains expedited only where truly needed

## Tab 10: Discovered Rate Cards Feature

**New in v3.2**: Automatic rate reverse-engineering from PLD data

### How It Works:
1. Groups shipments by service level and billable weight
2. Uses statistical analysis (MODE with MEDIAN fallback)
3. Creates transparent rate table showing current vs proposed
4. Identifies exact savings per weight/zone combination

### Sample Discovered Rates:
| Weight | DHL Expedited | Xparcel Ground | Savings |
|--------|---------------|----------------|---------|
| 1-8 oz | $4.32 | $2.89 | $1.43 (33%) |
| 9-12 oz | $4.32 | $2.95 | $1.37 (32%) |
| 13-15 oz | $4.32 | $2.99 | $1.33 (31%) |
| 1 lb | $4.32 | $3.09 | $1.23 (28%) |

## Optimization Opportunities

### Immediate Actions
1. **Service Level Migration**
   - Convert 6,319 DHL Expedited → Xparcel Ground
   - Maintain 3-8 day SLA (adequate for lightweight packages)
   - Save 31-33% per package

2. **Expedited Consolidation**
   - Convert 361 UPS 2nd Day Air → Xparcel Expedited
   - $17.21 → ~$5-7 per package
   - 60-70% savings on premium shipments

3. **Select Network Optimization**
   - Leverage zone-skipping for 99% sub-1 lb packages
   - Dynamic routing through metro injection points
   - Additional 5-10% savings potential

### Strategic Recommendations

1. **Service Level Rationalization**
   - Audit if 70% expedited volume truly needs 2-5 day service
   - Most lightweight packages can use 3-8 day ground
   - Customer satisfaction unlikely to be impacted

2. **Billing Optimization**
   - Focus on 15.99 oz breakpoint management
   - Prevent jumping to 2 lb billable weight
   - Package design consultation opportunity

3. **Network Strategy**
   - FirstMile's dynamic routing selects best carrier nightly
   - Single integration replacing DHL, UPS, USPS
   - Unified support for claims and exceptions

## Files Generated

1. **Stackd_Logistics_PLD_Audit_v3.2.xlsx** - 10-tab comprehensive analysis
   - Executive Summary
   - Shipment Details (1,000 samples)
   - Rate Comparison Matrix
   - Zone Analysis
   - Service Analysis
   - Weight Distribution
   - Top Savings Opportunities
   - 12-Month Projections
   - Service Level Comparison
   - **Tab 10: Discovered Rate Cards** (NEW)

2. **Stackd_Logistics_Detailed_Data_v3.2.csv** - Full dataset with calculations

3. **Stackd_Logistics_Discovered_Rates.csv** - Extracted rate tables

## Implementation Roadmap

### Week 1: Validation
- Review discovered rates with Stackd team
- Confirm service level requirements
- Validate volume projections

### Week 2: Pilot Program
- Start with 10% of DHL Expedited volume
- Test Xparcel Ground performance
- Monitor customer satisfaction

### Week 3-4: Scale Up
- Expand to 50% of eligible volume
- Fine-tune routing preferences
- Implement Audit Queue controls

### Month 2: Full Migration
- Complete service migration
- Optimize Select Network routing
- Establish performance baselines

## Conclusion

PLD Invoice Audit Builder v3.2 reveals **$168,940 annual savings opportunity** through:
- **Service optimization**: Migrating expedited to ground where appropriate
- **Rate arbitrage**: Xparcel rates 30-70% below current carriers
- **Network efficiency**: Select Network zone-skipping for lightweight packages
- **Operational simplification**: Single platform replacing multiple carriers

The discovered rate cards in Tab 10 provide complete transparency into current costs and proposed savings, building trust and enabling data-driven decision making.

**Next Steps**: Schedule discovery call to review audit findings and implementation timeline.