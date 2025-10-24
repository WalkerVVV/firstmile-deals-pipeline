# PLD (Parcel Level Detail) Analysis Instructions

## Overview
Complete shipping profile analysis for customer data to understand carriers, services, weights, dimensions, zones, and costs.

## Required Data File
- CSV file with standard shipping fields (ShipStation/stamps.com export format)
- Key columns: Carrier, Service, Weight, Dimensions, Zone, Cost, Destination

## Analysis Components (Execute in Order)

### 1. Volume Profile
- Total shipments count
- Daily average (total/30 for 30-day data)
- Marketplace mix percentages

### 2. Carrier Mix Analysis
```python
# Group by carrier, calculate:
- Volume per carrier
- Percentage of total volume
- Total spend per carrier
- Average cost per carrier
```

### 3. Service Level Distribution
```python
# Group by service level, show:
- Volume per service
- Percentage of total
- Average cost per service
- Total spend per service
```

### 4. Expanded Weight Distribution
```python
# CRITICAL: Billable Weight Rules
# Under 1 lb: Round UP to next whole oz, max 15.99 oz
# 16 oz exactly: Bills as 1 lb
# Over 1 lb: Round UP to next whole pound

# Breakdowns needed:
## Under 1 lb:
- 1-4 oz
- 5-8 oz  
- 9-12 oz
- 13-15 oz
- 15.99 oz (critical threshold)
- 16 oz exactly (1 lb)

## 1-5 lbs (by billable pound):
- 2 lbs (16.1-32 oz actual)
- 3 lbs (32.1-48 oz actual)
- 4 lbs (48.1-64 oz actual)
- 5 lbs (64.1-80 oz actual)

## Over 5 lbs:
- 6-10 lbs
- 10+ lbs

# For each range show:
- Package count
- % of total volume
- Average cost
- Total spend
- % of total spend
```

### 5. Dimensional Analysis
```python
# Calculate cubic inches (L × W × H)
# Show percentages with/without dimensions
# Average dimensions when provided

# Cubic volume categories:
- Under 1 cubic foot (<1,728 cu in)
- Over 1 cubic foot (≥1,728 cu in)

# Size categories:
- Small (<500 cu in)
- Medium (500-999 cu in)
- Large (1000-1727 cu in)
- Extra Large (≥1728 cu in)
```

### 6. Zone Distribution (Zones 1-8)
```python
# Individual zone breakdown:
- Volume per zone
- % of total
- Average cost per zone
- Average weight per zone

# Zone groupings:
- Regional (Zones 1-4): volume, %, total cost
- Cross-Country (Zones 5-8): volume, %, total cost

# Service mix by zone grouping
```

### 7. Geographic Distribution
```python
# Top 10 destination states:
- State code
- Volume
- % of total
```

### 8. Cost Analysis
```python
# Overall metrics:
- Total 30-day spend
- Average cost per shipment
- Median cost per shipment

# Cost by weight range
# Cost by zone
# Cost by carrier
```

### 9. Billable Weight Impact
```python
# Calculate billable vs actual weight:
- Average actual weight
- Average billable weight  
- Average difference
- Total billable ounces "lost" to rounding
```

## Output Format

### Summary Tables Required:
1. **Volume Profile Table**: Total packages, daily average, marketplace mix
2. **Carrier Mix Table**: Carrier, volume, %, spend, avg cost
3. **Weight Distribution Table**: Detailed breakdown with billable weights
4. **Zone Distribution Table**: All 8 zones individually
5. **Dimensional Analysis Table**: With cubic volume percentages
6. **Cost Summary Table**: Total spend breakdown by category

### Key Insights Section
Always include:
1. Lightweight concentration (% under 1 lb, 1-2 lbs)
2. Cross-country shipping percentage (Zones 5-8)
3. Billable weight impact (% extra weight paid for)
4. Service level mix insights
5. Dimensional data availability
6. Critical weight thresholds (15.99 oz, 32 oz, etc.)

### FirstMile Optimization Callouts
Identify opportunities for:
- Xparcel Ground (under 1 lb packages)
- Xparcel Expedited (1-5 lb packages)  
- Zone-skipping (Zones 5-8 volume)
- Weight threshold management
- Dynamic routing benefits

## Python Implementation Files
1. `weight_analysis.py` - Expanded weight distribution with billable weights
2. `dimension_analysis.py` - Dimensional and cubic volume analysis
3. `billable_weight_analysis.py` - Billable weight impact calculation

## Critical Notes
- ALL carriers including FirstMile round UP weights
- Maximum billable weight under 1 lb is 15.99 oz
- 16.00 oz exactly bills as 1 lb
- Focus on packages near weight thresholds for optimization
- Emphasize % of spend concentration in lightweight packages