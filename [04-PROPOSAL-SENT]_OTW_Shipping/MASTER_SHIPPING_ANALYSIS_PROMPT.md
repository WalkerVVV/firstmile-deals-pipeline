# MASTER PROMPT: FirstMile Xparcel Shipping Analysis & Savings Calculator

## Objective
Create a comprehensive shipping cost analysis that compares current carrier costs (UPS/FedEx/USPS) against FirstMile Xparcel rates, demonstrating savings opportunities through dynamic routing and the Select Network.

## Required Input Data Structure
Analyze shipping data (CSV/Excel) containing:
- Tracking numbers
- Current carrier/service level
- Package weight (lbs)
- Shipping zones (1-8)
- Current costs
- Ship dates

## Analysis Framework

### 1. Data Processing Pipeline
```python
# Weight distribution pattern (typical e-commerce):
- 60% under 1 lb (exponential distribution, scale=0.3)
- 30% between 1-5 lbs (uniform distribution)
- 10% between 5-20 lbs (uniform distribution)

# Zone distribution (realistic e-commerce):
zone_probabilities = [0.03, 0.12, 0.22, 0.28, 0.18, 0.10, 0.05, 0.02]
# Zones 3-5 represent 68% of volume (most common)

# Service mix (ground-heavy):
service_distribution = {
    'UPS Ground': 35%,
    'FedEx Ground': 25%,
    'UPS SurePost': 15%,
    'FedEx SmartPost': 10%,
    'Express/Priority': 15%
}
```

### 2. Cost Calculation Methodology

#### Current Carrier Cost Formula:
```python
def calculate_current_cost(weight, zone, service):
    base_rates = {
        'UPS Ground': 6.50,
        'FedEx Ground': 6.45,
        'UPS SurePost': 5.80,
        'FedEx SmartPost': 5.75,
        'UPS Next Day Air': 28.50,
        'FedEx Express': 27.80,
        'USPS Priority': 7.95
    }

    base = base_rates[service]
    zone_multiplier = 1 + (zone - 1) * 0.08  # 8% per zone increase
    weight_multiplier = 1 + np.log1p(weight) * 0.15  # Logarithmic weight impact
    fuel_surcharge = 1.12  # 12% fuel and fees

    return base * zone_multiplier * weight_multiplier * fuel_surcharge
```

#### FirstMile Xparcel Rate Structure:
```python
def calculate_xparcel_rate(weight, zone, service):
    # Service level determination
    if expedited_service:
        # Xparcel Priority (1-3 days) - National Network rates
        base_rates = {1: 3.94, 2: 3.99, 3: 4.01, 4: 4.10,
                      5: 4.15, 6: 4.24, 7: 4.31, 8: 4.48}
    else:
        # Xparcel Ground (3-8 days) - National Network rates
        base_rates = {1: 3.73, 2: 3.79, 3: 3.80, 4: 3.89,
                      5: 3.94, 6: 4.02, 7: 4.09, 8: 4.24}

    # Weight-based tier pricing
    if weight <= 0.0625:    return base              # 1 oz
    elif weight <= 0.25:     return base + 0.10      # 4 oz
    elif weight <= 0.5:      return base + 0.25      # 8 oz
    elif weight <= 1.0:      return base + 0.50      # 1 lb
    elif weight <= 2.0:      return base + 1.30      # 2 lb
    elif weight <= 5.0:      return base + 4.10      # 5 lb
    elif weight <= 10.0:     return base + 7.50      # 10 lb
    else:                    return base + 7.50 + (weight - 10) * 0.35
```

### 3. Excel Workbook Structure (9 Essential Tabs)

#### Tab 1: Executive Summary
- Company header with analysis date
- Financial summary table:
  - Monthly/Annual spend comparison
  - Total savings amount and percentage
  - Cost per package metrics
- Quick stats sidebar:
  - Average weight
  - Most common zone
  - Service mix percentage
  - Implementation timeline (48 hours)
  - No contract minimums

#### Tab 2: Shipment Details
- First 1000 shipments with full details
- Columns: Tracking, Service, Weight, Zone, Ship Date, Current Cost, Xparcel Cost, Savings, Savings %
- Currency formatting for costs, percentage formatting for savings

#### Tab 3: Rate Comparison
- Ground service comparison matrix
- Sample weights (1oz, 4oz, 8oz, 1lb, 2lb, 5lb, 10lb)
- Sample zones (2-7)
- Current average rate vs Xparcel rate
- Color-coded savings percentages:
  - Green (bold): ≥50%
  - Blue (bold): 30-50%
  - Black: <30%
- Average savings by zone summary table

#### Tab 4: Zone Analysis
- Distribution by zone (1-8)
- Metrics per zone: Shipments, % of total, Current cost, Xparcel cost, Total savings, Avg weight, Avg savings/package
- Identify high-volume zones for optimization

#### Tab 5: Service Analysis
- Breakdown by current service type
- Show Xparcel service mapping
- Total and average costs by service
- Savings percentage by service level

#### Tab 6: Weight Distribution
- Weight buckets: 0-4oz, 4-8oz, 8oz-1lb, 1-2lb, 2-5lb, 5-10lb, 10-20lb, 20lb+
- Volume and cost analysis per weight range
- Identify lightweight optimization opportunities

#### Tab 7: Savings Breakdown
- Top 20 highest savings opportunities
- Detailed tracking-level savings analysis
- Highlight packages with >40% savings

#### Tab 8: Monthly Projections
- 12-month forecast with seasonal adjustments
  - Nov-Dec: 135% volume (peak season)
  - Jan-Feb: 85% volume (slow season)
  - Other months: 100% volume
- Cumulative savings tracking
- Annual totals row

#### Tab 9: Service Level Comparison
- Current service to Xparcel service mapping
- Transit time comparisons
- Feature comparisons ($100 insurance, tracking, etc.)
- Cost index (Lowest/Medium/Higher/Highest)

### 4. Styling Requirements

```python
# Color scheme
header_color = "1E4C8B"  # Dark blue
header_text = "FFFFFF"    # White
subheader_color = "E6E6E6"  # Light gray
success_color = "90EE90"  # Light green for advantages

# Formatting
- Headers: Bold, size 11, white text on dark blue
- Subheaders: Bold, size 12, gray background
- Currency: $#,##0.00
- Percentages: 0.0%
- Auto-adjust column widths (max 45 chars)
```

### 5. Key Metrics to Calculate & Display

**Primary KPIs:**
- Total monthly savings: Sum of all positive savings
- Annual projection: Monthly savings × 12
- Average savings per package
- Savings percentage: (Savings / Current Cost) × 100
- Package count with savings opportunity

**Secondary Metrics:**
- Average weight across shipments
- Zone distribution (% per zone)
- Service mix breakdown
- Weight distribution analysis
- Top savings opportunities

### 6. FirstMile Differentiators (Always Emphasize)

1. **Dynamic Routing**: Automatically selects best carrier nightly based on SLA & cost
2. **Audit Queue**: Blocks mis-rated labels before invoice
3. **Single Support Thread**: One ticket for all claims, returns, exceptions
4. **Unified Platform**: Single integration for all services
5. **No Minimums**: No volume commitments or setup fees
6. **48-Hour Implementation**: Fast onboarding

### 7. Output Requirements

**Files to Generate:**
1. `[Company]_Complete_Audit_v3.1.xlsx` - Main analysis workbook
2. `[Company]_Detailed_Data.csv` - Raw data export
3. Console output with summary statistics

**Console Output Format:**
```
================================================================================
INVOICE AUDIT BUILDER v3.1 - EXECUTION COMPLETE
================================================================================
Total Tabs Created: 9
Shipments Analyzed: [X,XXX]
Savings Identified: $[XX,XXX.XX]
Savings Percentage: [XX.X]%
Annual Projection: $[XXX,XXX.XX]
================================================================================
```

### 8. Special Considerations

**DAS (Delivery Area Surcharge) Handling:**
- Identify DAS zones from Select Network data
- Apply appropriate surcharges where applicable
- Show DAS avoidance through Select Network routing

**Select Network Optimization:**
- Route lightweight packages through Select carriers
- Zone-skip using metro injection points
- Leverage regional carriers for better rates

**Billable Weight Rules:**
- Under 1 lb: Round UP to next whole oz (max 15.99 oz)
- 16 oz exactly: Bills as 1 lb
- Over 1 lb: Round UP to next whole pound

### 9. Data Validation Steps

1. Ensure all arrays have matching lengths
2. Filter to positive savings only for analysis
3. Handle missing or invalid data gracefully
4. Validate zone ranges (1-8)
5. Confirm weight reasonableness (0.05-70 lbs typical)

### 10. Professional Presentation

**Language Guidelines:**
- Use "Xparcel" (not "XParcel" or "xparcel")
- Refer to services as "Xparcel Ground (3-8 d)", "Xparcel Expedited (2-5 d)", "Xparcel Priority (1-3 d)"
- Never name specific carriers in Select Network (use "National" or "Select")
- Always frame as FirstMile solution, not separate Xparcel company

**Value Propositions:**
- Lead with percentage savings (30-50% typical)
- Emphasize no setup fees or minimums
- Highlight single integration advantage
- Focus on dynamic routing intelligence

## Implementation Code Structure

```python
#!/usr/bin/env python3
"""
INVOICE AUDIT BUILDER v3.1 - [COMPANY NAME] COMPLETE ANALYSIS
All tabs, full detail, corrected Xparcel rates
"""

import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, PieChart, LineChart, Reference
from openpyxl.formatting.rule import ColorScaleRule
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# [Implementation follows structure above]
```

## Expected Results

When properly implemented, this analysis should demonstrate:
- **30-50% average savings** on ground shipments
- **20-40% savings** on expedited services
- **Highest savings** on lightweight (under 1 lb) packages in zones 4-8
- **DAS avoidance** saving $3-5 per affected package
- **Annual savings** typically 6-figures for mid-volume shippers

## Success Criteria

The analysis is complete when:
1. All 9 Excel tabs are populated with accurate data
2. Savings calculations use actual FirstMile rate structure
3. Professional formatting applied throughout
4. Executive summary clearly shows value proposition
5. Rate comparison demonstrates zone-by-zone advantages
6. Monthly projections include seasonal adjustments
7. All FirstMile differentiators are highlighted
8. Output files are created and ready for presentation

---

*This master prompt encapsulates the complete methodology for creating a professional FirstMile Xparcel shipping analysis that demonstrates clear value and savings opportunities through intelligent routing and the Select Network.*