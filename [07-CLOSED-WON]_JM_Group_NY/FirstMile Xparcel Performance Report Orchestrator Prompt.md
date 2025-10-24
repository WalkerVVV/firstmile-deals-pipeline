# FirstMile Xparcel Performance Report Orchestrator Prompt

## Purpose
Create a consistent, professional Excel deliverable for customers analyzing FirstMile (carrier) performance using Xparcel ship methods, **broken down by service level** (Priority, Expedited, Ground).

## Critical Business Context

### Brand Identity (NEVER VIOLATE)
- **FirstMile** = The carrier (like UPS, FedEx, USPS)
- **Xparcel** = The ship method/service level (like Ground, Express, Priority)
- **Xparcel is NOT a separate company** - it's FirstMile's service offering
- Never name specific carriers (UPS, FedEx, USPS) - use "National Network" or "Select Network"
- Spell "eCommerce" with camel-case 'C'

### Xparcel Service Levels & SLA Windows
```python
SLA_WINDOWS = {
    "Ground": 8,        # Xparcel Ground: 3-8 day service, 8-day SLA
    "Expedited": 5,     # Xparcel Expedited: 2-5 day service, 5-day SLA
    "Direct Call": 3    # Xparcel Priority: 1-3 day service, 3-day SLA
}

SERVICE_NAME_MAP = {
    'Ground': 'Xparcel Ground',
    'Expedited': 'Xparcel Expedited',
    'Direct Call': 'Xparcel Priority'
}
```

### Network Structure
- **National Network**: Nationwide coverage (all U.S. ZIP codes)
- **Select Network**: Metro-focused injection points (LA, DAL, ATL, ORD, EWR, etc.)

## SLA Calculation Rules (CRITICAL)

### Rule 1: SLA Only Applies to DELIVERED Packages
```python
# CORRECT
delivered = df[df['Delivered Status'] == 'Delivered']
sla_compliance = within_sla / len(delivered) * 100

# WRONG - Never include in-transit in SLA calculation
all_packages = df  # This includes in-transit!
sla_compliance = within_sla / len(all_packages) * 100  # WRONG!
```

### Rule 2: ALWAYS Break Down by Service Level
Each Xparcel service level has its own SLA window. **NEVER** calculate overall SLA without showing per-service breakdown first.

```python
# CORRECT - Calculate by service level
for service_type in ['Ground', 'Expedited', 'Direct Call']:
    service_df = delivered[delivered['Xparcel Type'] == service_type]
    sla_window = SLA_WINDOWS[service_type]
    within_sla = service_df[service_df['Days In Transit'] <= sla_window]
    compliance = (len(within_sla) / len(service_df)) * 100

# WRONG - Single overall calculation
delivered = df[df['Delivered Status'] == 'Delivered']
within_sla = delivered[delivered['Days In Transit'] <= 8]  # Which SLA window?
```

### Rule 3: In-Transit Shipments Are NOT SLA Misses
In-transit packages are **excluded from SLA calculations** but should be tracked separately with "Within SLA Window" indicators.

```python
# In-transit analysis (separate from SLA)
in_transit = df[df['Delivered Status'] != 'Delivered']
in_transit['Days Since Ship'] = (today - in_transit['Start Date']).dt.days
in_transit['Within SLA Window'] = in_transit.apply(
    lambda row: 'Yes' if row['Days Since Ship'] <= SLA_WINDOWS[row['Xparcel Type']] else 'No',
    axis=1
)
```

### Rule 4: Use Correct Date Column
- **For in-transit calculations**: Use `Start Date` (most accurate ship date)
- **For delivered calculations**: Use `Days In Transit` (pre-calculated)
- **For report period**: Use `Request Date` or `Start Date` (min/max)

## Required Input Data

### Expected Columns
```
- Customer Name
- Tracking Number
- Xparcel Type          # CRITICAL: Ground, Expedited, Direct Call
- Delivered Status      # CRITICAL: Delivered vs In Transit, etc.
- Days In Transit       # CRITICAL: For SLA calculation
- Start Date           # CRITICAL: For in-transit day calculations
- Destination State
- Calculated Zone
- Most Recent Scan
- Most Recent Scan Date
```

### Data Validation
```python
# Check for required columns
required = ['Xparcel Type', 'Delivered Status', 'Days In Transit']
if not all(col in df.columns for col in required):
    raise ValueError(f"Missing required columns: {required}")

# Clean zone data (extract numeric)
df['Calculated Zone'] = df['Calculated Zone'].astype(str).str.extract(r'(\d+)')[0].astype(float)

# Handle NaN in service types
service_types = [x for x in df['Xparcel Type'].unique() if pd.notna(x)]
```

## Excel Output Structure (8 Tabs)

### Tab 1: Executive Summary
**Purpose**: High-level overview with performance by service level

**Content**:
1. Overall Performance section
   - Total Shipments
   - Total Delivered
   - Overall SLA Compliance
   - Performance Status (Perfect/Exceeds/Meets/Below)
   - In-Transit Shipments

2. Performance by Xparcel Service Level table
   - Service Level | SLA Window | Delivered | Within SLA | Compliance % | Status
   - Row for each: Priority, Expedited, Ground

### Tab 2: SLA Compliance
**Purpose**: Detailed SLA metrics for each service level

**Content**: For EACH service level, show:
```
Service Name (X-day SLA)
  Metric                    Value
  Total Delivered           ###
  Within SLA               ###
  Outside SLA              ###
  SLA Compliance           ##.#%
  Performance Status       Exceeds Standard
  Average Transit Days     #.#
  Median Transit Days      #.#
  90th Percentile          #.#
  95th Percentile          #.#
```

### Tab 3: Transit Performance
**Purpose**: Day-by-day distribution showing cumulative delivery patterns

**Content**: For EACH service level, show:
```
Service Name (X-day SLA)
  Transit Days | Count | Percentage | Cumulative Count | Cumulative % | Status
  Day 0        | ###   | ##.#%      | ###             | ##.#%        | Within SLA
  Day 1        | ###   | ##.#%      | ###             | ##.#%        | Within SLA
  ...
  Day X        | ###   | ##.#%      | ###             | ##.#%        | Within SLA
  Day X+1      | ###   | ##.#%      | ###             | ##.#%        | Outside SLA
```

**Key Insight to Show**: "95.3% delivered by Day 6" for Ground (well within 8-day window)

### Tab 4: Geographic Distribution
**Purpose**: Top 15 states with hub assignments

**Content**:
```
State | Shipment Count | Percentage | Primary Hub | Network Type
NY    | ###           | ##.#%      | JFK/EWR - Northeast | Select Network
CA    | ###           | ##.#%      | LAX - West Coast    | Select Network
...
```

**Hub Mapping**:
```python
HUB_MAP = {
    "CA": "LAX - West Coast",
    "TX": "DFW - South Central",
    "FL": "MIA - Southeast",
    "NY": "JFK/EWR - Northeast",
    "IL": "ORD - Midwest",
    "GA": "ATL - Southeast",
    "NJ": "JFK/EWR - Northeast",
    "PA": "JFK/EWR - Northeast",
    "OH": "ORD - Midwest",
    "MI": "ORD - Midwest",
    "WI": "ORD - Midwest"
}
```

### Tab 5: Zone Analysis
**Purpose**: Zone 1-8 distribution with Regional vs Cross-Country split

**Content**:
1. Zone-by-zone breakdown (use delivered packages for avg transit)
2. Regional vs Cross-Country summary
   - Regional (Zones 1-4): count, percentage
   - Cross-Country (Zones 5-8): count, percentage

### Tab 6: In-Transit Detail
**Purpose**: Current in-transit status by service level

**Content**:
1. Summary by Service Level table
   ```
   Service Level | SLA Window | Total In-Transit | Within Window | Outside Window | % Within
   ```

2. Detailed records (top N rows showing):
   - Xparcel Type
   - Start Date
   - Days Since Ship
   - Within SLA Window (Yes/No)
   - Delivered Status
   - Destination State
   - Calculated Zone

### Tab 7: Notes & Assumptions
**Purpose**: Document business rules and definitions

**Content**:
```
Report Generated: YYYY-MM-DD HH:MM:SS

Business Rules:
- SLA Calculation: Based on delivered packages only, by service level
- Xparcel Ground: 8-day SLA window (3-8 day service)
- Xparcel Expedited: 5-day SLA window (2-5 day service)
- Xparcel Priority: 3-day SLA window (1-3 day service)
- In-Transit Status: Shipments not yet delivered are excluded from SLA calculations
- Performance Thresholds: 100%=Perfect, >=95%=Exceeds, >=90%=Meets, <90%=Below

Definitions:
- FirstMile: The carrier providing shipping services
- Xparcel: The ship method (Priority, Expedited, Ground)
- National Network: Nationwide coverage for all ZIP codes
- Select Network: Metro-focused injection points in major hubs
```

### Tab 8: Brand Style Guide
**Purpose**: Color reference for consistent branding

**Content**:
```
Color Name       | HEX     | RGB              | Usage
FirstMile Blue   | #366092 | RGB(54, 96, 146) | Primary brand color, headers
Light Gray       | #DDDDDD | RGB(221, 221, 221) | Borders, dividers
Red              | #FFC7CE | RGB(255, 199, 206) | Below standard (80-89%)
Yellow           | #FFEB84 | RGB(255, 235, 132) | Meets standard (90-94%)
Green            | #C6EFCE | RGB(198, 239, 206) | Exceeds standard (95-100%)
```

## Excel Styling Requirements

### Colors
```python
FIRSTMILE_BLUE = "366092"
LIGHT_GRAY = "DDDDDD"
RED_BG = "FFC7CE"
YELLOW_BG = "FFEB84"
GREEN_BG = "C6EFCE"
```

### Header Style
```python
def apply_header_style(ws, row=1):
    blue_fill = PatternFill(start_color=FIRSTMILE_BLUE, end_color=FIRSTMILE_BLUE, fill_type="solid")
    white_font = Font(color="FFFFFF", bold=True, size=11)
    center_align = Alignment(horizontal="center", vertical="center")
```

### Data Style
```python
def apply_data_style(ws, start_row=2):
    thin_border = Border(
        left=Side(style='thin', color=LIGHT_GRAY),
        right=Side(style='thin', color=LIGHT_GRAY),
        top=Side(style='thin', color=LIGHT_GRAY),
        bottom=Side(style='thin', color=LIGHT_GRAY)
    )
    center_align = Alignment(horizontal="center", vertical="center")
```

### Auto-sizing
- Columns sized to content with max width of 50 characters
- All data tables include auto-filters on header rows

## Common Mistakes to AVOID

### Mistake 1: Wrong Service Level Detection
```python
# WRONG - Uses Days In Transit average including in-transit packages
avg_transit = df['Days In Transit'].mean()  # Includes NaN, in-transit!

# CORRECT - Check Xparcel Type column first
if 'Xparcel Type' in df.columns:
    xparcel_counts = df['Xparcel Type'].value_counts()
    most_common = xparcel_counts.idxmax()
    # Map to service level using SLA_WINDOWS dict
```

### Mistake 2: Including In-Transit in SLA Calculation
```python
# WRONG
all_packages = df
within_sla = all_packages[all_packages['Days In Transit'] <= 8]
compliance = (len(within_sla) / len(all_packages)) * 100  # 62.8% WRONG!

# CORRECT
delivered = df[df['Delivered Status'] == 'Delivered']
within_sla = delivered[delivered['Days In Transit'] <= 8]
compliance = (len(within_sla) / len(delivered)) * 100  # 99.9% CORRECT!
```

### Mistake 3: Single SLA Window for All Services
```python
# WRONG - Assumes all packages have same 8-day SLA
delivered = df[df['Delivered Status'] == 'Delivered']
within_sla = delivered[delivered['Days In Transit'] <= 8]

# CORRECT - Each service has its own SLA
for service in ['Ground', 'Expedited', 'Direct Call']:
    service_df = delivered[delivered['Xparcel Type'] == service]
    sla_window = SLA_WINDOWS[service]  # 8, 5, or 3 days
    within_sla = service_df[service_df['Days In Transit'] <= sla_window]
```

### Mistake 4: Not Handling NaN in Service Types
```python
# WRONG - Crashes when sorting with NaN
for service_type in sorted(df['Xparcel Type'].unique()):  # TypeError!

# CORRECT - Filter out NaN values
for service_type in sorted([x for x in df['Xparcel Type'].unique() if pd.notna(x)]):
```

### Mistake 5: Wrong Date Column for In-Transit
```python
# WRONG - Request Date may be days before shipment
in_transit['Days Since Ship'] = (today - in_transit['Request Date']).dt.days

# CORRECT - Start Date is actual ship date
in_transit['Days Since Ship'] = (today - in_transit['Start Date']).dt.days
```

### Mistake 6: Unicode Characters in Windows Console
```python
# WRONG - Causes UnicodeEncodeError on Windows
print(f"Within SLA (<=8 days): {count}")  # <= symbol crashes!

# CORRECT - Use ASCII-safe characters
print(f"Within SLA (<=8 days): {count}")
```

## Performance Thresholds

```python
PERF_THRESHOLDS = [
    (100.0, "Perfect Compliance"),
    (95.0, "Exceeds Standard"),
    (90.0, "Meets Standard"),
    (0.0, "Below Standard")
]

# Usage
performance_status = next(
    status for threshold, status in PERF_THRESHOLDS
    if compliance_pct >= threshold
)
```

## Output Filename Format

```python
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
customer_clean = CUSTOMER_NAME.replace(' ', '_')
filename = f"FirstMile_Xparcel_Performance_{customer_clean}_{timestamp}.xlsx"
```

Example: `FirstMile_Xparcel_Performance_JM_Group_NY_20250930_1149.xlsx`

## Validation Checklist

Before finalizing report, verify:

- [ ] SLA compliance calculated on **delivered packages only**
- [ ] Performance broken down by **all three service levels** (Priority, Expedited, Ground)
- [ ] Each service level uses **correct SLA window** (3, 5, or 8 days)
- [ ] In-transit shipments **excluded from SLA calculation**
- [ ] In-transit shows "Within SLA Window" indicator using **Start Date**
- [ ] Transit performance shows **cumulative percentages** by day
- [ ] Key insight visible: "X% delivered by Day Y" for each service
- [ ] Geographic distribution shows **Select vs National Network**
- [ ] Zone analysis uses **delivered packages only** for avg transit
- [ ] All tables have **FirstMile blue headers** with white text
- [ ] All columns **auto-sized** with max 50 char width
- [ ] No carrier names mentioned (UPS, FedEx, USPS)
- [ ] "eCommerce" spelled with **camel-case C**
- [ ] No emojis or marketing language
- [ ] Plain, factual, professional tone

## Key Insights to Surface

The report should clearly show:

1. **Overall SLA Compliance** (typically 99%+)
   - Example: "99.9% of delivered packages met their SLA"

2. **Service-Level Performance**
   - Priority: 100% (all same-day or next-day)
   - Expedited: 100% (delivered within 5 days)
   - Ground: 99.9% (delivered within 8 days)

3. **Early Delivery Performance**
   - Example: "95.3% of Ground packages delivered by Day 6 (within 8-day window)"
   - Example: "71.2% of Ground packages delivered in 4 days or less"

4. **In-Transit Status**
   - Example: "1,053 packages within SLA window (62.8% of in-transit)"
   - Example: "Only 31 packages (1.8%) outside SLA window"

5. **Network Distribution**
   - Example: "Select Network: 45%, National Network: 55%"

## Sample Output Summary

```
FirstMile Xparcel Performance Report
Customer: JM Group NY
Period: August 7 - September 29, 2025

SLA Performance by Service Level:
================================================
Xparcel Priority (3-day SLA)
  100.0% compliance (26 delivered)
  All delivered same day (Day 0)

Xparcel Expedited (5-day SLA)
  100.0% compliance (62 delivered)
  Average: 2.0 days | 100% by Day 4

Xparcel Ground (8-day SLA)
  99.9% compliance (1,053 delivered)
  Average: 3.3 days | 95.3% by Day 6
  Only 1 package exceeded 8-day SLA

Overall Performance: 99.9% - Exceeds Standard
================================================
```

## Forbidden Practices

### NEVER Do These Things:
1. Lead with daily delivery percentages (always lead with SLA compliance)
2. Emphasize Day 0/Day 1 over SLA compliance metrics
3. Name specific carriers (UPS, FedEx, USPS) - use "National" or "Select"
4. Use emojis in the Excel report (console output is OK)
5. Include marketing language or slogans
6. Calculate SLA on all shipments (in-transit must be excluded)
7. Use a single SLA window for all services
8. Present data without breaking down by service level
9. Use Unicode characters that cause Windows console errors
10. Ignore NaN values when iterating over service types

## Python Dependencies

```python
import pandas as pd
import numpy as np
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
```

## Implementation Notes

### Always Use This Workflow:
1. Load data and validate required columns
2. Detect report period from date columns
3. Calculate SLA by service level (delivered only)
4. Calculate in-transit status by service level (separate)
5. Calculate geographic and zone distributions
6. Create Excel workbook with 8 tabs
7. Apply consistent styling (blue headers, bordered data)
8. Auto-size columns and add filters
9. Save with timestamp filename

### Code Structure:
```python
def load_data(file_path)
def detect_report_period(df)
def calculate_sla_by_service_level(df)  # Returns list of dicts
def calculate_in_transit_by_service_level(df)  # Returns list, summary, detail
def calculate_geographic_distribution(df)
def calculate_zone_analysis(df)
def apply_header_style(ws, row=1)
def apply_data_style(ws, start_row=2)
def auto_size_columns(ws, max_width=50)
def create_executive_summary(wb, ...)
def create_sla_compliance_by_service_tab(wb, ...)
def create_transit_performance_by_service_tab(wb, ...)
def create_geographic_tab(wb, ...)
def create_zone_analysis_tab(wb, ...)
def create_in_transit_tab(wb, ...)
def create_notes_tab(wb)
def create_brand_style_guide_tab(wb)
def generate_report()
```

## Success Criteria

A successful report will:
1. Show 99%+ SLA compliance (when data supports it)
2. Clearly break down performance by Priority, Expedited, and Ground
3. Demonstrate early delivery (e.g., "95% by Day 6 for 8-day service")
4. Properly exclude in-transit from SLA calculations
5. Present professional, branded Excel with 8 consistent tabs
6. Load without errors and display correctly in Excel
7. Use plain, factual language without marketing hype
8. Follow FirstMile brand guidelines precisely
9. Provide actionable insights for customer success teams
10. Generate in under 10 seconds for typical dataset sizes

---

## Usage Example

```python
# Run the report generator
python generate_firstmile_report_v2.py

# Expected console output:
# SLA Compliance Summary:
#   Xparcel Priority: 100.0% (26 delivered)
#   Xparcel Expedited: 100.0% (62 delivered)
#   Xparcel Ground: 99.9% (1053 delivered)
# Overall Performance: 99.9% - Exceeds Standard
```

---

**Document Version**: 1.0
**Last Updated**: 2025-09-30
**Validated Against**: JM Group NY dataset (2,817 shipments, Aug-Sep 2025)
