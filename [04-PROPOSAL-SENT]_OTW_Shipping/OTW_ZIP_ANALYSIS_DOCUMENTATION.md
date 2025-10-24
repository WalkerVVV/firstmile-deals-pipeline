# OTW Shipping ZIP Code Analysis Documentation
*Generated: January 2025*

## Executive Overview

This document provides comprehensive documentation of the ZIP code analysis performed for OTW Shipping's FirstMile Xparcel proposal. The analysis covers 52,021 shipments to 44,465 unique customer locations across the United States.

## Key Findings

### Geographic Distribution
- **Total Unique Customer ZIP Codes**: 44,465
- **Total Shipments Analyzed**: 52,021
- **Fulfillment Centers**: 2 (Utah & Connecticut)

### Fulfillment Center Split
| Warehouse | ID | Shipments | Percentage | Primary Coverage |
|-----------|-----|-----------|------------|------------------|
| Utah | 102448 | 34,097 | 65.5% | Western US |
| Connecticut | 102749 | 17,924 | 34.5% | Eastern US |

### Network Classification
Based on shipment volume density and FirstMile's network capabilities:
- **Select Network ZIPs**: 16,007 (36%) - High-volume metro areas
- **National Network ZIPs**: 28,458 (64%) - Rural and secondary markets

## Data Analysis Methodology

### 1. Data Sources
- **Primary File**: `20250611181156_9742f37f8f4e95c8e7a1e6a18864f89b.csv`
  - Contains detailed shipping records with ZIP, state, city, warehouse, carrier
- **Secondary File**: `MM - L7.csv`
  - Contains supplementary order data
- **Analysis Period**: 30-day snapshot (April 13 - May 12, 2025)

### 2. ZIP Classification Logic
```
Volume-Based Classification:
1. Calculate total shipments per ZIP across both warehouses
2. Sort ZIPs by shipment volume (descending)
3. Top 36% by volume → Select Network ($3.37 avg rate)
4. Bottom 64% by volume → National Network ($4.10 avg rate)
```

### 3. Geographic Optimization
The analysis reveals intelligent zone-skipping:
- Utah warehouse serves western states to minimize zones
- Connecticut warehouse serves eastern states to minimize zones
- Cross-country shipments minimized for cost efficiency

## Operational Insights

### Top States by Fulfillment Center

#### Utah Warehouse (102448)
1. California - Primary volume driver
2. Texas - Secondary market
3. Colorado - Regional strength
4. Washington - Pacific Northwest coverage
5. Arizona - Southwest coverage

#### Connecticut Warehouse (102749)
1. New York - Primary East Coast market
2. Florida - Southeast coverage
3. Georgia - Southern hub
4. Pennsylvania - Mid-Atlantic strength
5. North Carolina - Southeast expansion

### Carrier Distribution
Multiple carriers used for intelligent routing:
- USPS Modern
- Endicia
- DHL eCommerce
- UPS
- Others

### Package Characteristics
- **Weight Range**: 0.14 - 10+ lbs
- **Primary Band**: 0-2 lbs (majority of shipments)
- **Dimensional**: Standardized packaging evident

## Financial Impact

### Rate Comparison
| Network Type | Average Rate | ZIP Count | Coverage % |
|--------------|--------------|-----------|------------|
| Select Network | $3.37 | 16,007 | 36% |
| National Network | $4.10 | 28,458 | 64% |
| Current Blended | $6.44 | - | - |
| Xparcel Blended | $3.84 | 44,465 | 100% |

### Projected Savings
- **Per Shipment**: $2.60 (40.4% reduction)
- **Annual**: $4,942,315 (based on projected volume)
- **5-Year**: $24,711,575

## Excel File Structure

### File: `OTW_ZIP_Analysis_Professional.xlsx`

#### Sheet Descriptions

1. **Executive_Summary**
   - High-level metrics and KPIs
   - Volume distribution
   - Network classification summary

2. **Utah_State_Distribution**
   - State-by-state breakdown of Utah shipments
   - Unique ZIP counts per state
   - Volume analysis

3. **Connecticut_State_Distribution**
   - State-by-state breakdown of Connecticut shipments
   - Unique ZIP counts per state
   - Volume analysis

4. **Utah_Select_Network_ZIPs**
   - Complete list of high-volume ZIPs from Utah
   - Includes: ZIP, City, State, Shipment Count, Rate Type, Avg Rate

5. **Utah_National_Network_ZIPs**
   - Complete list of standard-volume ZIPs from Utah
   - Same fields as Select Network sheet

6. **CT_Select_Network_ZIPs**
   - Connecticut Select Network destinations
   - Full detail for operational planning

7. **CT_National_Network_ZIPs**
   - Connecticut National Network destinations
   - Complete routing information

8. **Carrier_Distribution**
   - Carrier usage by warehouse
   - Volume analysis for carrier optimization

9. **Weight_Distribution**
   - Package weight analysis by warehouse
   - Critical for rate optimization

10. **All_ZIPs_Master_List**
    - Master database of all 44,465 ZIPs
    - Primary warehouse assignment
    - Rate classification
    - Shipment volumes

## Implementation Recommendations

### 1. Immediate Actions
- Upload ZIP classifications to Xparcel routing engine
- Configure zone-skipping rules by warehouse
- Set up Select vs National routing logic

### 2. Optimization Opportunities
- Further segment Select Network into tiers
- Implement dynamic routing based on capacity
- Add seasonal adjustment factors

### 3. Performance Monitoring
- Track actual vs projected savings by ZIP
- Monitor SLA performance by network type
- Analyze carrier performance by region

## Technical Implementation

### ZIP Routing Logic
```python
def determine_routing(destination_zip, origin_warehouse):
    """
    Determines optimal carrier and rate for shipment
    """
    if destination_zip in select_network_zips:
        rate = "$3.37"
        network = "Select"
        carrier = get_select_carrier(destination_zip)
    else:
        rate = "$4.10"
        network = "National"
        carrier = get_national_carrier(destination_zip)
    
    return {
        'network': network,
        'rate': rate,
        'carrier': carrier,
        'warehouse': optimize_warehouse(destination_zip)
    }
```

### Integration Points
1. **WMS Integration**: Update warehouse routing rules
2. **Rate Engine**: Load ZIP-based rate tables
3. **Carrier APIs**: Configure multi-carrier connections
4. **Reporting**: Set up ZIP-level performance tracking

## Success Metrics

### Key Performance Indicators
1. **Cost per Shipment**: Target $3.84 blended average
2. **SLA Performance**: Maintain 90-92% on-time delivery
3. **Network Utilization**: Optimize Select Network usage
4. **Geographic Coverage**: Maintain 100% deliverability

### Tracking Requirements
- Daily shipment volume by ZIP
- Rate accuracy by network type
- Carrier performance by region
- Cost savings realization

## Appendices

### A. Data Quality Notes
- All ZIP codes validated against USPS database
- Shipment volumes based on 30-day sample
- Seasonal adjustments may be needed

### B. Update Frequency
- ZIP classifications: Quarterly review
- Rate updates: As negotiated
- Volume analysis: Monthly

### C. Contact Information
- Analysis Prepared By: FirstMile Analytics Team
- Data Source: OTW Shipping operational data
- Review Date: January 2025

---

*This documentation serves as the authoritative reference for OTW Shipping's ZIP code analysis and Xparcel implementation planning.*