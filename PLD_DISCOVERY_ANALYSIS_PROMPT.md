# PLD Discovery Analysis - Complete System Prompt

## Overview
This is a **fully automated workflow** that analyzes prospect shipping data (PLD - Parcel Level Detail) and produces a tier tool-ready Excel deliverable. The user provides a CSV file path, and the system automatically generates console insights and a complete Excel workbook with NO manual Excel work required.

## Critical Requirements

### 1. Complete Weight Break Template (MOST IMPORTANT)
The Excel output MUST include ALL weight breaks from 1 oz to 400 oz, even if shipment count is zero:
- **Under 1 lb**: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15.99 oz
- **1+ lbs (16 oz increments)**: 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400 oz

**Why**: The FirstMile tier tool expects this exact format. Missing weight breaks (showing only weights with shipments) breaks the copy/paste alignment and makes the file unusable.

**Implementation**:
```python
# Create complete weight break template FIRST
weight_breaks = list(range(1, 16))  # 1-15 oz
weight_breaks.append(15.99)  # 15.99 oz
weight_breaks.extend([16 * i for i in range(1, 26)])  # 16-400 oz (1-25 lbs)

# Create DataFrame with all weight breaks
template_df = pd.DataFrame(index=weight_breaks, columns=["Priority", "Expedited", "Ground"])
template_df = template_df.fillna(0)

# Merge actual data into template
for weight in pivot_weight_service.index:
    if weight in template_df.index:
        template_df.loc[weight] = pivot_weight_service.loc[weight]
```

### 2. Billable Weight Calculation
All weights must be converted to carrier-compliant billable weight in ounces:

```python
def calculate_billable_weight_oz(weight_lb):
    """
    Calculate billable weight in ounces following carrier rounding rules:
    - Under 1 lb: Round UP to next whole oz, MAX 15 oz (then 15.99)
    - Exactly 16 oz: Bills as 1 lb (16 oz)
    - Over 1 lb: Round UP to next whole pound (32, 48, 64 oz, etc.)
    """
    if pd.isna(weight_lb) or weight_lb <= 0:
        return 0

    weight_oz = weight_lb * 16

    if weight_oz < 16:
        # Under 1 lb: round up to next whole oz, max 15
        return min(int(np.ceil(weight_oz)), 15)
    elif weight_oz == 16:
        # Exactly 16 oz bills as 16 oz (1 lb)
        return 16
    else:
        # Over 1 lb: round up to next whole pound
        billable_lbs = int(np.ceil(weight_lb))
        return billable_lbs * 16
```

### 3. Service Level Mapping
Automatically categorize all shipping methods into three FirstMile Xparcel services:

```python
def map_service(method):
    method_lower = str(method).lower()
    if "2nd day" in method_lower:
        return "Expedited"
    elif "ground" in method_lower or "parcel expedited" in method_lower:
        return "Ground"
    elif "priority" in method_lower or "express" in method_lower:
        return "Priority"
    else:
        return "Ground"  # Default to Ground
```

### 4. Excel Workbook Structure

#### Sheet 1: "Paste Data" (PRIMARY OUTPUT)
This is the critical sheet for the pricing team. Format requirements:

**Columns A-G**:
- A: Weight (oz) - ALL weight breaks 1-15.99, 16-400
- B: Priority (count)
- C: Expedited (count)
- D: Ground (count) - **HIGHLIGHTED IN YELLOW**
- E: Total Volume (sum of B+C+D)
- F: % of Total (formatted as "XX%")
- G: Avg per Week (Total Volume / weeks_in_period)

**Columns H-I: Summary Panel**:
- H2: "Total Volume (All XP Methods)" | I2: total_volume
- H3: "Weeks in period" | I3: weeks_in_period (rounded to 1 decimal)
- H4: "Avg Volume / Week" | I4: avg_volume_per_week
- H7: "Priority %" | I7: service_mix_priority (YELLOW FILL)
- H8: "Expedited %" | I8: service_mix_expedited (YELLOW FILL)
- H9: "Ground %" | I9: service_mix_ground (YELLOW FILL)
- H12: "Weight Band" | I12: "%" (BLACK HEADERS)
- H13-H17: Weight bands | I13-I17: Percentages

**Styling**:
- Headers: Black fill (#000000), white bold text
- Ground column (D): Yellow fill (#FFFF99)
- Service mix cells (I7-I9): Bright yellow fill (#FFFF00)
- All cells: Centered alignment, light gray borders

#### Sheet 2: "PLD Volume Analysis" (SUPPORTING DATA)
Four pivot tables side-by-side for reference:
1. **Bill Weight** (Columns A-C): Weight, COUNT, %
2. **Dimensions** (Columns E-G): DIMS (LxWxH), COUNT, %
3. **Country** (Columns I-K): Country (US/International), COUNT, %
4. **State** (Columns M-O): State, COUNT, %

#### Sheet 3: "Pivot Paste" (CONFIGURATION)
- Service mix percentages (yellow fills)
- Weeks in period
- Common period conversions (1 week, 2 weeks, 1 month, 3 months)
- Paste instructions

### 5. Required CSV Columns
The input CSV must contain:
- **Shipping Label ID** (unique identifier for pivot counting)
- **Weight (lb)** (decimal pounds, will be converted to billable oz)
- **Shipping Method** (service level names for mapping)
- **Order date** (or Created at / Ship date - for date range calculation)
- **State** (destination state for geographic analysis)
- **Carrier** (optional - for carrier mix analysis)
- **Length (in), Width (in), Height (in)** (optional - for dimensions)
- **Country** (optional - for domestic vs international split)

### 6. Console Output Format
Display comprehensive analysis in chat:

```
Loading [Customer] data...
Creating pivot tables...
Creating Excel workbook...

SUCCESS: [Customer]_PLD_TIER_TOOL_READY.xlsx created
  - Total volume: X,XXX shipments
  - Period: XX.X weeks (XX days)
  - Service mix: Priority X%, Expedited X%, Ground X%

  Weight Band Distribution:
    1-5 oz: XX%
    6-10 oz: XX%
    11-15 oz: XX%
    1-5 lbs: XX%
    5+ lbs: XX%

  Country Distribution:
    US: X,XXX (XX.XX%)
    International: XXX (X.XX%)

  Top 10 States:
    CA: X,XXX (XX.XX%)
    TX: XXX (X.XX%)
    ...

[OK] Sheet 1 'Paste Data' contains ALL weight breaks 1-15.99, 16-400 oz
[OK] Ready to send to pricing team!
```

## Command Format

**User command**:
```
"Run the PLD discovery analysis on [file_path]"
```

**Example**:
```
"Run the PLD discovery analysis on C:\Users\BrettWalker\FirstMile_Deals\[02-DISCOVERY-COMPLETE]_Stackd_Logistics\20250918193042_221aaf59f30469602caf8f7f7485b114.csv"
```

## Implementation Workflow

### Step 1: Load and Parse Data
```python
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side

# Load CSV
df = pd.read_csv(file_path)

# Parse dates and weights
df["Order date"] = pd.to_datetime(df["Order date"], errors="coerce")
df["Weight (lb)"] = pd.to_numeric(df["Weight (lb)"], errors="coerce")

# Calculate date range
date_range_days = (df["Order date"].max() - df["Order date"].min()).days + 1
weeks_in_period = date_range_days / 7
```

### Step 2: Calculate Billable Weights and Service Categories
```python
# Apply service mapping
df["Service Category"] = df["Shipping Method"].apply(map_service)

# Apply billable weight calculation
df["Bill Weight (oz)"] = df["Weight (lb)"].apply(calculate_billable_weight_oz)
```

### Step 3: Create Weight × Service Pivot with Complete Template
```python
# Create pivot with actual data
pivot_weight_service = pd.pivot_table(
    df,
    values="Shipping Label ID",
    index="Bill Weight (oz)",
    columns="Service Category",
    aggfunc="count",
    fill_value=0
)

# Ensure all service columns exist
for svc in ["Priority", "Expedited", "Ground"]:
    if svc not in pivot_weight_service.columns:
        pivot_weight_service[svc] = 0

# Create complete weight break template
weight_breaks = list(range(1, 16)) + [15.99] + [16 * i for i in range(1, 26)]
template_df = pd.DataFrame(index=weight_breaks, columns=["Priority", "Expedited", "Ground"])
template_df = template_df.fillna(0)

# Merge actual data into template
for weight in pivot_weight_service.index:
    if weight in template_df.index:
        template_df.loc[weight] = pivot_weight_service.loc[weight]

# Calculate totals
template_df["Total Volume"] = template_df["Priority"] + template_df["Expedited"] + template_df["Ground"]
total_shipments = template_df["Total Volume"].sum()
template_df["% of Total"] = (template_df["Total Volume"] / total_shipments * 100).round(0).astype(int)
template_df["Avg per Week"] = (template_df["Total Volume"] / weeks_in_period).round(0).astype(int)
```

### Step 4: Create Excel Workbook
```python
wb = Workbook()
ws1 = wb.active
ws1.title = "Paste Data"

# Define styles
header_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")
header_font = Font(color="FFFFFF", bold=True)
ground_fill = PatternFill(start_color="FFFF99", end_color="FFFF99", fill_type="solid")
yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")

# Write headers
headers = ["Weight", "Priority", "Expedited", "Ground", "Total Volume", "% of Total", "Avg per Week"]
for col_idx, header in enumerate(headers, start=1):
    cell = ws1.cell(row=1, column=col_idx)
    cell.value = header
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center")

# Write data rows - ALL weight breaks including zeros
for row_idx, row_data in enumerate(template_df.values, start=2):
    for col_idx, val in enumerate(row_data, start=1):
        cell = ws1.cell(row=row_idx, column=col_idx)

        # Format weight column (handle 15.99)
        if col_idx == 1:
            cell.value = 15.99 if val == 15.99 else int(val)
        else:
            cell.value = int(val)

        cell.alignment = Alignment(horizontal="center")

        # Highlight Ground column
        if col_idx == 4:
            cell.fill = ground_fill

        # Format % of Total
        if col_idx == 6:
            cell.value = f"{int(val)}%"

# Add Summary panel in columns H-I
# (Add summary data as shown in structure above)
```

### Step 5: Save and Report
```python
output_file = f"{customer_name}_PLD_TIER_TOOL_READY.xlsx"
wb.save(output_file)

# Print comprehensive console output
print(f"\nSUCCESS: {output_file} created")
# (Print all analysis as shown in console output format above)
```

## Common Pitfalls to Avoid

### ❌ DON'T: Create pivot with only weights that have shipments
```python
# WRONG - This creates gaps
pivot = pd.pivot_table(df, values="ID", index="Weight", columns="Service", aggfunc="count")
```

### ✅ DO: Create complete template then merge data
```python
# CORRECT - This ensures all weight breaks are present
weight_breaks = list(range(1, 16)) + [15.99] + [16 * i for i in range(1, 26)]
template_df = pd.DataFrame(index=weight_breaks, columns=["Priority", "Expedited", "Ground"])
template_df = template_df.fillna(0)
for weight in actual_data.index:
    if weight in template_df.index:
        template_df.loc[weight] = actual_data.loc[weight]
```

### ❌ DON'T: Use actual weight in ounces
```python
# WRONG - Doesn't follow carrier billing rules
df["Weight (oz)"] = (df["Weight (lb)"] * 16).round(0)
```

### ✅ DO: Calculate billable weight with carrier rounding rules
```python
# CORRECT - Follows carrier billing rules
df["Bill Weight (oz)"] = df["Weight (lb)"].apply(calculate_billable_weight_oz)
```

### ❌ DON'T: Require user to do Excel work
The user does NOT open Excel, does NOT copy/paste, does NOT format anything. The workflow produces a complete, ready-to-use deliverable.

### ✅ DO: Produce complete, tier tool-ready Excel file
The Excel file is 100% complete and ready for the pricing team to copy columns A-G into the FirstMile tier tool.

## FirstMile Brand Standards

### Terminology
- **FirstMile** is the carrier (not a platform or 3PL)
- **Xparcel** is the ship method (Priority, Expedited, Ground)
- **National Network**: Nationwide coverage (all ZIPs)
- **Select Network**: Metro injection points (LA, DAL, ATL, ORD, EWR, etc.)
- Never name specific carriers (UPS, FedEx, USPS) - use "National" or "Select"
- Spell "eCommerce" with camel-case 'C'

### Service Level Definitions
- **Xparcel Priority**: 1-3 day premium with money-back guarantee
- **Xparcel Expedited**: 2-5 day faster ground solution (1-20 lb)
- **Xparcel Ground**: 3-8 day economy ground service

## User Workflow (Hands-Off)

1. **User provides**: CSV file path
2. **System produces**:
   - Console analysis displayed in chat
   - Complete Excel workbook saved to disk
3. **User reviews**: Console insights to understand shipping profile
4. **User sends**: Excel file to pricing team (no editing required)
5. **Pricing team**: Copies columns A-G into FirstMile tier tool
6. **Pricing team returns**: Completed rate sheet for proposal

## File Naming Convention
`[Customer_Name]_PLD_TIER_TOOL_READY.xlsx`

Examples:
- `Stackd_Logistics_PLD_TIER_TOOL_READY.xlsx`
- `ABC_Company_PLD_TIER_TOOL_READY.xlsx`

## Success Criteria

✅ Excel file contains ALL weight breaks 1-15.99, 16-400 oz (no gaps)
✅ Weights with zero shipments show "0" (not blank, not missing)
✅ Ground column highlighted in yellow
✅ Service mix percentages highlighted in bright yellow
✅ Summary panel populated with all metrics
✅ Console output displays comprehensive analysis
✅ File name follows naming convention
✅ User does ZERO Excel work

## Reusability

This workflow is designed to be reusable for any prospect. The script should:
1. Accept CSV file path as input
2. Auto-detect customer name from file path or data
3. Apply same logic to any PLD export format (ShipStation, ShipHero, carrier exports, etc.)
4. Produce consistent output format regardless of input data variations

## Script Location
Save reusable script as: `create_pld_workbook.py` in customer folder

The script should be self-contained and runnable with:
```bash
python create_pld_workbook.py
```

## Documentation
Maintain `PLD_DISCOVERY_WORKFLOW.md` with:
- Command format
- What happens automatically
- Excel structure
- Required CSV columns
- Example console output
- User workflow (hands-off)
- Pricing team next steps
