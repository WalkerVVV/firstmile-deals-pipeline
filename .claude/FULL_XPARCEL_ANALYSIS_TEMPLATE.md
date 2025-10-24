# FULL XPARCEL ANALYSIS TEMPLATE

**Standard process for creating professional FirstMile Xparcel Savings Analysis for all prospects/customers**

## Purpose

Generate a professional, prospect-ready Excel deliverable analyzing shipping costs and FirstMile Xparcel savings potential. This analysis follows the Stackd Logistics blueprint with FirstMile blue branding (#366092) and standardized formatting.

---

## Required Input Data

### File Format
- **CSV or Excel file** with raw parcel-level detail (PLD) data
- Minimum 2 weeks of data (prefer 1-6 months for accuracy)

### Required Columns
```
- Tracking/Number: Shipment identifier
- Carrier: Current carrier name (USPS, FedEx, UPS, DHL, etc.)
- Service: Service level (Ground, Priority, 2-Day, etc.)
- Origin: Origin ZIP code
- Destination: Destination ZIP code
- Weight: Package weight in pounds
- Cost: Actual shipping cost paid
```

### Optional Columns (Enhance Analysis)
- Length, Width, Height: For dimensional analysis
- Ship Date / Delivery Date: For transit time analysis
- Reseller: For marketplace breakdown

---

## Analysis Process

### Step 1: Data Loading & Validation

```python
import pandas as pd
import numpy as np
from datetime import datetime

# Load PLD data
df = pd.read_csv("Customer_PLD_Data.csv", low_memory=False)

# Validate required columns
required_cols = ['Carrier', 'Service', 'Origin', 'Destination', 'Weight', 'Cost']
missing = [col for col in required_cols if col not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

print(f"Total shipments loaded: {len(df):,}")
```

### Step 2: Zone Calculation

```python
def get_zone_from_zip(origin_zip, dest_zip):
    """
    Calculate shipping zone from origin/destination ZIP codes
    Uses simplified ZIP3 prefix-based zone mapping
    """
    try:
        # Parse ZIP codes
        origin_zip_str = str(origin_zip).split('-')[0].zfill(5)
        dest_zip_str = str(dest_zip).split('-')[0].zfill(5)

        # If same ZIP3, Zone 1
        if origin_zip_str[:3] == dest_zip_str[:3]:
            return 1

        # Otherwise calculate based on destination ZIP3
        zip3 = int(dest_zip_str[:3])

        # Zone mapping (adjust based on origin)
        if 150 <= zip3 <= 196: return 2  # PA, NJ, DE, MD
        elif (10 <= zip3 <= 149) or (197 <= zip3 <= 199): return 3  # Northeast
        elif (200 <= zip3 <= 399): return 4  # Southeast
        elif (400 <= zip3 <= 699): return 4  # Midwest
        elif (500 <= zip3 <= 799): return 5  # South Central
        elif (800 <= zip3 <= 879): return 6  # Mountain West
        elif (850 <= zip3 <= 899) or (880 <= zip3 <= 884): return 7  # Southwest
        elif (900 <= zip3 <= 999): return 8  # West Coast
        else: return 5  # Default
    except:
        return None

df['Zone'] = df.apply(lambda row: get_zone_from_zip(row['Origin'], row['Destination']), axis=1)
```

### Step 3: Billable Weight Calculation

```python
def calculate_billable_weight(weight):
    """
    Calculate billable weight following carrier rules:
    - Under 1 lb: Keep actual weight
    - Over 1 lb: Round UP to next whole pound
    """
    if pd.isna(weight):
        return None
    if weight <= 1:
        return weight
    return np.ceil(weight)

df['Billable_Weight'] = df['Weight'].apply(calculate_billable_weight)
```

### Step 4: Weight Tier Assignment (CRITICAL - FirstMile Rate Card Structure)

```python
def get_weight_tier(weight):
    """
    Assign weight tier matching FirstMile Xparcel rate card structure:

    UNDER 1 LB (16 tiers):
    - 1 oz, 2 oz, 3 oz, 4 oz, 5 oz, 6 oz, 7 oz, 8 oz
    - 9 oz, 10 oz, 11 oz, 12 oz, 13 oz, 14 oz, 15 oz
    - 15.99 oz (critical threshold)

    OVER 1 LB (10 tiers):
    - 1 lb, 2 lb, 3 lb, 4 lb, 5 lb, 6 lb, 7 lb, 8 lb, 9 lb, 10 lb

    HEAVY (3 tiers):
    - 11-15 lb, 16-20 lb, 21+ lb
    """
    if pd.isna(weight):
        return None

    weight_oz = weight * 16  # Convert to ounces

    # Under 1 lb (by ounce)
    if weight_oz <= 1: return "1 oz"
    elif weight_oz <= 2: return "2 oz"
    elif weight_oz <= 3: return "3 oz"
    elif weight_oz <= 4: return "4 oz"
    elif weight_oz <= 5: return "5 oz"
    elif weight_oz <= 6: return "6 oz"
    elif weight_oz <= 7: return "7 oz"
    elif weight_oz <= 8: return "8 oz"
    elif weight_oz <= 9: return "9 oz"
    elif weight_oz <= 10: return "10 oz"
    elif weight_oz <= 11: return "11 oz"
    elif weight_oz <= 12: return "12 oz"
    elif weight_oz <= 13: return "13 oz"
    elif weight_oz <= 14: return "14 oz"
    elif weight_oz <= 15: return "15 oz"
    elif weight_oz < 16: return "15.99 oz"
    # Over 1 lb (by pound)
    elif weight <= 1: return "1 lb"
    elif weight <= 2: return "2 lb"
    elif weight <= 3: return "3 lb"
    elif weight <= 4: return "4 lb"
    elif weight <= 5: return "5 lb"
    elif weight <= 6: return "6 lb"
    elif weight <= 7: return "7 lb"
    elif weight <= 8: return "8 lb"
    elif weight <= 9: return "9 lb"
    elif weight <= 10: return "10 lb"
    elif weight <= 15: return "11-15 lb"
    elif weight <= 20: return "16-20 lb"
    else: return "21+ lb"

df['Weight_Tier'] = df['Billable_Weight'].apply(get_weight_tier)
```

### Step 5: Serviceable Filtering

```python
# FirstMile CANNOT service express/overnight for live goods
EXCLUDED_SERVICES = [
    'FEDEX_FIRST_OVERNIGHT',
    'FEDEX_PRIORITY_OVERNIGHT',
    'FEDEX_STANDARD_OVERNIGHT',
    'UPS_NEXT_DAY_AIR',
    'UPS_NEXT_DAY_AIR_SAVER',
    'UPS_NEXT_DAY_AIR_EARLY',
    'USPS_PRIORITY_MAIL_EXPRESS'
]

df['Serviceable'] = ~df['Service'].isin(EXCLUDED_SERVICES)
serviceable_df = df[df['Serviceable']]

print(f"Serviceable: {len(serviceable_df):,} ({len(serviceable_df)/len(df)*100:.1f}%)")
```

### Step 6: Calculate Key Metrics

```python
# Volume metrics
total_shipments = len(df)
serviceable_shipments = len(serviceable_df)
data_period_months = 6  # Adjust based on actual data period
monthly_shipments = total_shipments / data_period_months
annual_shipments = total_shipments * (12 / data_period_months)

# Financial metrics (serviceable only)
total_period_spend = serviceable_df['Cost'].sum()
monthly_spend = total_period_spend / data_period_months
annual_spend = total_period_spend * (12 / data_period_months)
avg_cost = serviceable_df['Cost'].mean()

# Weight profile
under_1lb = len(serviceable_df[serviceable_df['Billable_Weight'] <= 1])
under_1lb_pct = under_1lb / serviceable_shipments * 100
avg_weight = serviceable_df['Weight'].mean()

# FirstMile savings estimate
savings_rate = 0.12  # Conservative 12% (adjust based on data)
xparcel_monthly = monthly_spend * (1 - savings_rate)
monthly_savings = monthly_spend * savings_rate
annual_savings = monthly_savings * 12
```

---

## Excel Output Structure

### Required Tabs (6 Total)

#### 1. Executive Summary
**Content:**
- Main title: "[CUSTOMER NAME] - FIRSTMILE XPARCEL SAVINGS ANALYSIS"
- Analysis metadata (date, data period, total shipments)
- Savings summary table with green-highlighted savings
- Key metrics panel (volume, weight profile, projections)

**Formatting:**
- FirstMile blue header (#366092) with white text (18pt bold)
- Blue subheaders (14pt bold)
- Blue table headers (12pt bold, white text)
- Savings in green (#00B050, 12pt bold)
- Currency format: $#,##0.00
- Percentage format: 0.0%

#### 2. Weight Analysis
**Content:**
- Title: "SAVINGS BY WEIGHT - FIRSTMILE RATE CARD STRUCTURE"
- Table columns: Weight, Shipments, % of Total, Avg Current Cost, Avg Xparcel Cost, Avg Savings, Savings %, Total Savings
- Rows for EACH weight tier (29 tiers total)
- TOTAL row at bottom

**Weight Tier Order (CRITICAL):**
```
UNDER 1 LB:
1 oz, 2 oz, 3 oz, 4 oz, 5 oz, 6 oz, 7 oz, 8 oz, 9 oz, 10 oz, 11 oz, 12 oz, 13 oz, 14 oz, 15 oz, 15.99 oz

OVER 1 LB:
1 lb, 2 lb, 3 lb, 4 lb, 5 lb, 6 lb, 7 lb, 8 lb, 9 lb, 10 lb, 11-15 lb, 16-20 lb, 21+ lb
```

#### 3. Zone Analysis
**Content:**
- Title: "SAVINGS BY DESTINATION ZONE"
- Table columns: Zone, Shipments, % of Total, Avg Current Cost, Avg Xparcel Cost, Avg Savings/Pkg, Total Savings
- Rows for Zones 1-8 (as available in data)

#### 4. Incumbent Rate Cards
**Content:**
- Title: "CURRENT CARRIER RATE CARDS - ZONE × WEIGHT"
- Top 3-5 services by volume
- For each service:
  - Service header: "[CARRIER] - [SERVICE] (X shipments)"
  - Zone × Weight matrix showing average costs
  - Separate sections for "UNDER 1 LB" and "OVER 1 LB"

**Matrix Structure:**
```
               Zone 1  Zone 2  Zone 3  Zone 4  Zone 5  Zone 6  Zone 7  Zone 8
UNDER 1 LB
1 oz           $4.02   $4.07   $4.12   ...
2 oz           $4.04   $4.09   $4.14   ...
...

OVER 1 LB
1 lb           $5.23   $5.45   $5.67   ...
2 lb           $6.12   $6.34   $6.56   ...
...
```

#### 5. Carrier Breakdown
**Content:**
- Title: "CURRENT CARRIER ANALYSIS"
- Table columns: Carrier, Shipments, % of Total, 6-Month Spend, Monthly Spend, Annual Projection, Avg Cost/Pkg
- Rows for each carrier (USPS, FedEx, UPS, DHL, etc.)
- Sorted by volume (descending)

#### 6. FirstMile Advantages
**Content:**
- Title: "WHY FIRSTMILE FOR ECOMMERCE SHIPPERS"
- Sections:
  - **Cost Optimization**: Savings %, no hidden fees, transparent pricing, volume discounts
  - **Operational Excellence**: Audit Queue, single integration, dynamic routing, returns management
  - **Service & Support**: Single support thread, claims management, dedicated account manager, real-time tracking
  - **FirstMile Xparcel Service Levels**: Ground (3-8d), Expedited (2-5d), Priority (1-3d)

---

## Professional Formatting Standards

### Colors (FirstMile Brand)
```python
FM_BLUE = "366092"      # Primary brand color (headers, emphasis)
FM_WHITE = "FFFFFF"     # Header text
FM_GREEN = "00B050"     # Savings highlights
FM_LIGHT_GRAY = "F2F2F2"  # Alternating rows (optional)
```

### Fonts
- **Headers**: Calibri 18pt Bold, White text on Blue background
- **Subheaders**: Calibri 14pt Bold, White text on Blue background
- **Table Headers**: Calibri 12pt Bold, White text on Blue background
- **Body Text**: Calibri 11pt
- **Savings Values**: Calibri 12pt Bold, Green (#00B050)

### Alignment
- **Text**: Left aligned
- **Numbers**: Right aligned
- **Currency**: Right aligned with $ symbol
- **Percentages**: Center aligned
- **Headers**: Center aligned

### Column Widths
- Text columns: 16-20 characters
- Number columns: 12-16 characters
- Currency columns: 15-18 characters
- Description columns: 80+ characters

### Cell Formatting
```python
# Currency
cell.number_format = '$#,##0.00'

# Percentage
cell.number_format = '0.0%'

# Number with commas
cell.number_format = '#,##0'
```

---

## Quality Checklist

### Data Validation
- [ ] All required columns present in source data
- [ ] Zone calculation successful for >95% of shipments
- [ ] Weight tiers match FirstMile rate card structure exactly
- [ ] Serviceable filtering applied correctly
- [ ] No negative costs or weights
- [ ] Date ranges validated and displayed correctly

### Calculation Validation
- [ ] Monthly spend = (6-month spend / 6)
- [ ] Annual spend = (6-month spend × 2)
- [ ] Savings % applied consistently (default 12%)
- [ ] Weight tier totals sum to 100%
- [ ] Zone totals sum to 100%
- [ ] All currency values formatted with $ and 2 decimals

### Formatting Validation
- [ ] All headers use FirstMile blue (#366092)
- [ ] All header text is white and centered
- [ ] Savings values highlighted in green
- [ ] Column widths auto-sized appropriately
- [ ] No merged cells except headers
- [ ] Tab names are clear and professional

### Content Validation
- [ ] Customer name in title
- [ ] Analysis date is current
- [ ] Data period clearly stated
- [ ] 6 tabs present (Executive Summary, Weight Analysis, Zone Analysis, Rate Cards, Carrier Breakdown, FirstMile Advantages)
- [ ] Weight tier order: 1-15oz, 15.99oz, 1-10lb, 11-15lb, 16-20lb, 21+lb
- [ ] Rate cards show zone × weight matrices
- [ ] FirstMile Advantages tab includes all key benefits

### Prospect-Ready Validation
- [ ] No internal notes or debugging content
- [ ] No placeholder text or "TODO" items
- [ ] Professional tone throughout
- [ ] File saved with descriptive name: `[Customer]_FirstMile_Xparcel_Savings_Analysis_YYYYMMDD_HHMM.xlsx`
- [ ] File size <5MB for easy email delivery

---

## Standard Prompt Template

**Use this exact prompt for every Full Xparcel Analysis:**

```
Create a professional FirstMile Xparcel Savings Analysis for [CUSTOMER NAME].

DATA FILE: [path/to/customer_pld_data.csv]
DATA PERIOD: [e.g., "6 months (February - August 2025)"]

REQUIREMENTS:
1. Load PLD data and validate required columns
2. Calculate shipping zones from origin/destination ZIP codes
3. Calculate billable weight (round up to next pound if >1 lb)
4. Assign weight tiers matching FirstMile rate card structure:
   - Under 1 lb: 1-15oz, 15.99oz (16 tiers)
   - Over 1 lb: 1-10lb (10 tiers)
   - Heavy: 11-15lb, 16-20lb, 21+lb (3 tiers)
5. Filter out non-serviceable express/overnight services
6. Calculate monthly/annual spend and 12% savings projections
7. Generate professional Excel with 6 tabs:
   - Executive Summary (savings table + key metrics)
   - Weight Analysis (29 weight tiers)
   - Zone Analysis (Zones 1-8)
   - Incumbent Rate Cards (zone × weight matrices for top services)
   - Carrier Breakdown (current carrier spend)
   - FirstMile Advantages (why FirstMile)

FORMATTING:
- FirstMile blue headers (#366092, white text)
- Green savings highlights (#00B050)
- Currency: $#,##0.00
- Percentage: 0.0%
- Professional, prospect-ready deliverable

OUTPUT FILE: [Customer]_FirstMile_Xparcel_Savings_Analysis_YYYYMMDD_HHMM.xlsx

Follow .claude/FULL_XPARCEL_ANALYSIS_TEMPLATE.md for complete specifications.
```

---

## Example Usage

```bash
# For Josh's Frogs
python full_xparcel_analysis.py \
  --customer "Josh's Frogs" \
  --data "Joshs_Frogs_PLD_6mo.csv" \
  --period "6 months (February - August 2025)" \
  --savings-rate 0.12

# For Stackd Logistics
python full_xparcel_analysis.py \
  --customer "Stackd Logistics" \
  --data "Stackd_PLD_2weeks.csv" \
  --period "2 weeks (August - September 2025)" \
  --savings-rate 0.10
```

---

## Common Pitfalls to Avoid

### ❌ WRONG: Generic weight buckets
```python
# DON'T DO THIS
if weight <= 1: return "0-1 lb"
elif weight <= 5: return "1-5 lb"
```

### ✅ CORRECT: FirstMile rate card structure
```python
# DO THIS
if weight_oz <= 1: return "1 oz"
elif weight_oz <= 2: return "2 oz"
# ... all 16 under-1lb tiers
elif weight_oz < 16: return "15.99 oz"
elif weight <= 1: return "1 lb"
# ... all 10 over-1lb tiers
```

### ❌ WRONG: Unformatted Excel with default styling
```python
# DON'T DO THIS
df.to_excel(writer, sheet_name='Summary')
```

### ✅ CORRECT: Professional FirstMile branding
```python
# DO THIS
cell.font = Font(size=18, bold=True, color='FFFFFF')
cell.fill = PatternFill(start_color='366092', fill_type='solid')
cell.alignment = Alignment(horizontal='center')
```

### ❌ WRONG: Including non-serviceable services in savings
```python
# DON'T DO THIS
monthly_savings = df['Cost'].sum() * 0.12
```

### ✅ CORRECT: Only calculate savings on serviceable volume
```python
# DO THIS
serviceable_df = df[~df['Service'].isin(EXCLUDED_SERVICES)]
monthly_savings = serviceable_df['Cost'].sum() * 0.12
```

---

## Maintenance & Updates

### When to Update This Template
- FirstMile rate card structure changes
- New service levels added (e.g., Xparcel Express)
- Branding/color changes
- New required analysis tabs
- Customer feedback on formatting

### Version History
- **v1.0** (2025-10-08): Initial template based on Stackd Logistics blueprint
- Weight tier structure: 1-15oz, 15.99oz, 1-10lb, 11-15lb, 16-20lb, 21+lb
- FirstMile blue branding (#366092)
- 6-tab standard structure

---

## Related Documentation

- [FIRSTMILE.md](FIRSTMILE.md) - FirstMile brand standards and terminology
- [DEAL_FOLDER_TEMPLATE.md](DEAL_FOLDER_TEMPLATE.md) - Standard deal folder structure
- [DAILY_SYNC_OPERATIONS.md](DAILY_SYNC_OPERATIONS.md) - Pipeline workflow

---

## Questions?

For issues with this template or to suggest improvements:
1. Check existing Full Xparcel Analysis files in `[03-RATE-CREATION]` folders
2. Review Stackd Logistics analysis as reference blueprint
3. Update this template and commit changes to `.claude/` folder
