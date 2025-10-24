# PLD DISCOVERY ANALYSIS - Fully Automated Workflow

## Purpose
**100% automated** analysis of prospect PLD (Parcel Level Detail) data. You provide the CSV file path, the workflow automatically produces:
1. **Console Analysis Report** - Detailed insights displayed in chat during execution
2. **Excel Workbook** - Complete, tier tool-ready deliverable for pricing team

**YOU DO NO WORK IN EXCEL.** This is a hands-off workflow that produces the final deliverable automatically.

## When to Use
Run this analysis when you have:
- PLD export from ShipStation, ShipHero, or other 3PL/carrier systems
- Prospect shipping data in CSV format
- Need to understand shipping profile AND prepare data for pricing team

## Command to Run
```
"Run the PLD discovery analysis on [file_path]"
```

Example:
```
"Run the PLD discovery analysis on C:\Users\BrettWalker\FirstMile_Deals\[02-DISCOVERY-COMPLETE]_Stackd_Logistics\20250918193042_221aaf59f30469602caf8f7f7485b114.csv"
```

## What Happens Automatically

### Step 1: Console Analysis (Displayed in Chat)
Immediate insights displayed during execution:
- **Volume Metrics**: Total shipments, date range, daily/weekly averages, period weeks
- **Service Mix**: Priority %, Expedited %, Ground % distribution
- **Weight Profile**: Distribution across 1-5 oz, 6-10 oz, 11-15 oz, 1-5 lbs, 5+ lbs bands
- **Geographic Distribution**: Domestic vs International, Top 10 states with percentages
- **Key Insights**: Profile summary and FirstMile Xparcel fit assessment

### Step 2: Excel Workbook Generation (Automated)
File created: `[Customer_Name]_PLD_TIER_TOOL_READY.xlsx`

**Sheet 1: "Paste Data"** (PRIMARY - For Pricing Team)
- **Weight × Service Matrix** with ALL weight breaks (NO GAPS):
  - Under 1 lb: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15.99 oz
  - 1+ lbs: 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400 oz
- **Columns**: Weight | Priority | Expedited | Ground | Total Volume | % of Total | Avg per Week
- **Critical**: Shows 0 for weights with no shipments (maintains FirstMile tier tool format)
- **Ground column highlighted in yellow**
- **Summary Panel** (columns H-I):
  - Total Volume, Weeks in period, Avg Volume/Week
  - Service Mix % (Priority, Expedited, Ground) - highlighted yellow
  - Weight Band Distribution (1-5 oz, 6-10 oz, 11-15 oz, 1-5 lbs, 5+ lbs)

**Sheet 2: "PLD Volume Analysis"** (Supporting Data)
Four pivot tables side-by-side for reference:
1. **Bill Weight** - Count and % by billable weight
2. **Dimensions** - Package dimensions distribution (LxWxH)
3. **Country** - US vs International split
4. **State** - Geographic distribution by state

**Sheet 3: "Pivot Paste"** (Configuration Reference)
- Weeks in period (editable reference)
- Service mix percentages summary
- Paste instructions for reference

## Required Data Fields
The CSV must contain these columns:
- **Shipping Label ID** (or equivalent unique identifier)
- **Carrier** (ups, dhl_ecommerce, usps_modern, etc.)
- **Shipping Method** (UPS 2nd Day Air, DHL Parcel Expedited, USPS Ground Advantage, etc.)
- **Weight (lb)** (decimal weight in pounds)
- **Label Cost** (actual cost paid for shipping label)
- **Order date** (or Created at / Ship date)
- **State** (destination state for geographic analysis)
- **Total Shipping Charged** (amount charged to customer) *optional*
- **3PL Customer** (brand name if 3PL operation) *optional*

## Service Level Mapping Logic
The analysis automatically maps service methods to three categories:
- **Priority**: Services with "priority", "express", "next day" in name (1-3 day)
- **Expedited**: Services with "2nd day", "expedited" in name (2-5 day)
- **Ground**: All ground services and DHL Parcel Expedited (3-8 day)

## Weight Conversion
- Weights are converted from pounds to ounces for pivot table
- Weight bands: 1-5 oz, 6-10 oz, 11-15 oz, 1-5 lbs (16-80 oz), 5+ lbs (80+ oz)

## Output Format
The workbook matches the standard FirstMile PLD Discovery format:
- Yellow cells = editable configuration values
- Black headers with white text
- Ground column highlighted for visibility
- Service mix percentages prominently displayed
- Summary panel in columns H-I

## Typical Analysis Results
For Stackd Logistics example:
- 8,957 shipments over 96 days = 93/day
- 96% Ground (DHL), 4% Expedited (UPS)
- 92.5% under 1 lb (lightweight e-commerce)
- $4.96 average label cost
- Dominated by Chin Mounts brand (65.4% of volume)

## Your Workflow (Hands-Off)
1. **Run Command**: Provide CSV file path in chat
2. **Review Console Output**: Read shipping profile insights displayed in chat
3. **Send Excel File to Pricing Team**: They use `[Customer]_PLD_TIER_TOOL_READY.xlsx` in FirstMile tier tool
4. **Done**: No Excel work required from you

## Pricing Team's Next Step
Your pricing team receives the Excel workbook and:
1. Opens FirstMile tier tool
2. Copies columns A-G from "Paste Data" sheet
3. Pastes into tier tool to generate Xparcel domestic rates
4. Returns completed rate sheet to you for proposal

## Example Console Output
```
SUCCESS: Stackd_Logistics_PLD_TIER_TOOL_READY.xlsx created
  - Total volume: 8,957 shipments
  - Period: 13.7 weeks (96 days)
  - Service mix: Priority 0%, Expedited 4%, Ground 96%

  Weight Band Distribution:
    1-5 oz: 65.4%
    6-10 oz: 21.1%
    11-15 oz: 6.0%
    1-5 lbs: 7.2%
    5+ lbs: 0.3%

  Top 10 States:
    CA: 1,488 (16.67%)
    TX: 756 (8.47%)

[OK] Sheet 1 'Paste Data' contains ALL weight breaks 1-15.99, 16-400 oz
[OK] Ready to send to pricing team!
```

## Key Points
- ✅ **100% Automated** - Zero manual Excel work required from you
- ✅ **Complete Weight Template** - All weight breaks present, including zeros
- ✅ **Tier Tool Ready** - Format matches FirstMile tier tool exactly
- ✅ **Console Insights** - Immediate profile understanding in chat
- ✅ **Pricing Team Friendly** - Simple copy/paste into tier tool

## Files Created
- `create_pld_workbook.py` - Reusable Python script for future prospects
- `[Customer]_PLD_TIER_TOOL_READY.xlsx` - Final deliverable for pricing team

## To Rerun on New Prospect
```
"Run the PLD discovery analysis on [new_customer_csv_path]"
```
The workflow handles everything automatically.
