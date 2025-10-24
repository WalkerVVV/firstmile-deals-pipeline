# FirstMile Xparcel Performance Report — Orchestrator Prompt (v2)

## Purpose

Create a consistent, professional Excel deliverable for customers analyzing FirstMile performance using Xparcel ship methods, broken down by service level (Priority, Expedited, Ground).

## Critical Business Context

### Brand Identity (never violate)

* FirstMile = The carrier.
* Xparcel = The ship method and service level.
* Xparcel is not a separate company. It is a FirstMile service offering.
* Never name specific carriers. Use "National Network" or "Select Network".
* Spell "eCommerce" with camel-case C.
* Keep the tone plain, factual, and professional.

## Xparcel Service Levels and SLA Windows

```python
SLA_WINDOWS = {
    "Ground": 8,        # Xparcel Ground: 3–8 day service, 8-day SLA
    "Expedited": 5,     # Xparcel Expedited: 2–5 day service, 5-day SLA
    "Priority": 3       # Xparcel Priority: 1–3 day service, 3-day SLA
}

SERVICE_NAME_MAP = {
    "Ground": "Xparcel Ground",
    "Expedited": "Xparcel Expedited",
    "Priority": "Xparcel Priority"
}
```

## Network Structure

* National Network: Coverage for all ZIP codes in the lower 48 states.
* Select Network: Metro and regional injection lanes (examples: LAX, DFW, ATL, ORD, JFK/EWR).

## SLA Calculation Rules (critical)

### Rule 1: SLA compliance applies to delivered packages only

* SLA compliance percentage is based only on delivered packages.

```python
delivered = df[df['Delivered Status'] == 'Delivered']
# per service calculation is required; see Rule 2
```

### Rule 2: Always break down by service level

* Calculate SLA compliance separately for Priority, Expedited, and Ground.
* Each service has its own SLA window.
* Never present overall SLA before showing the per-service breakdown.

```python
results = []
for service in ["Priority","Expedited","Ground"]:
    svc = delivered[delivered["Xparcel Type"] == service]
    if len(svc) == 0:
        continue
    win = SLA_WINDOWS[service]
    within = svc[svc["Days In Transit"] <= win]
    comp = (len(within) / len(svc)) * 100
    results.append({"service": service, "delivered": len(svc), "within_sla": len(within), "compliance_pct": comp})
```

### Rule 3: In-transit shipments must be checked against the SLA window

* In-transit is not automatically an SLA miss.
* Use Start Date to determine Days Since Ship, then compare to the service SLA window.

```python
in_transit = df[df['Delivered Status'] != 'Delivered'].copy()
today = pd.to_datetime(report_run_date)  # set once
in_transit['Days Since Ship'] = (today - pd.to_datetime(in_transit['Start Date'])).dt.days
in_transit['Within SLA Window'] = in_transit.apply(
    lambda r: "Yes" if r['Days Since Ship'] <= SLA_WINDOWS.get(r['Xparcel Type'], 9999) else "No", axis=1
)
# An in-transit shipment is an SLA miss only if Days Since Ship > SLA window
```

* Examples:

  * Ground shipped 9/1/25, today 9/30/25 → 30 days vs 8-day SLA → SLA miss.
  * Ground shipped 9/25/25, today 9/30/25 → 5 days vs 8-day SLA → Not an SLA miss (still within window).

### Rule 4: Use correct date fields

* Delivered calculations: use Days In Transit.
* In-transit calculations: use Start Date to compute Days Since Ship.
* Report period: min and max of Request Date or Start Date.

## Required Input Data

### Expected columns

* Customer Name
* Tracking Number
* Xparcel Type         (Priority, Expedited, Ground)
* Delivered Status     (Delivered, In Transit, etc.)
* Days In Transit      (for delivered shipments)
* Start Date           (actual ship date)
* Destination State
* Destination ZIP
* Calculated Zone
* Most Recent Scan
* Most Recent Scan Date

### Data validation

```python
required = ['Xparcel Type','Delivered Status','Days In Transit','Start Date','Destination State','Destination ZIP','Calculated Zone']
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Clean zone to numeric
df['Calculated Zone'] = (
    df['Calculated Zone'].astype(str).str.extract(r'(\d+)')[0].astype('Int64')
)

# Handle NaN in service types
df['Xparcel Type'] = df['Xparcel Type'].astype('string')
service_types = [x for x in df['Xparcel Type'].dropna().unique() if x in SLA_WINDOWS]
```

## Excel Output Structure (9 tabs)

### Tab 1: Executive Summary

**Purpose:** High-level overview with performance by service level.

**Content:**

* Customer Name and Report Period.
* Overall Performance:

  * Total Shipments
  * Total Delivered
  * Overall SLA Compliance (delivered-only, aggregated after per-service is shown)
  * Performance Status (Perfect, Exceeds Standard, Meets Standard, Below Standard)
  * Total In-Transit Shipments (tracked separately; not part of delivered-only SLA)
* Performance by Xparcel Service Level:

| Service Level     | SLA Window | Delivered | Within SLA | Compliance % | Status             |
| ----------------- | ---------- | --------- | ---------- | ------------ | ------------------ |
| Xparcel Priority  | 3 Days     | ###       | ###        | ##.#%        | Exceeds Standard   |
| Xparcel Expedited | 5 Days     | ###       | ###        | ##.#%        | Perfect Compliance |
| Xparcel Ground    | 8 Days     | ###       | ###        | ##.#%        | Meets Standard     |

**Notes to emphasize:**

* SLA compliance is calculated on delivered packages only.
* In-transit shipments are checked against the SLA window using Start Date.

### Tab 2: SLA Compliance

**Purpose:** Detailed SLA metrics per service level.

| Metric               | Value        |
| -------------------- | ------------ |
| Total Delivered      | ###          |
| Within SLA           | ###          |
| Outside SLA          | ###          |
| SLA Compliance %     | ##.#%        |
| Performance Status   | Exceeds Std. |
| Average Transit Days | #.#          |
| Median Transit Days  | #.#          |
| 90th Percentile      | #.#          |
| 95th Percentile      | #.#          |

**Rules:**

* Delivered-only SLA.
* Separate tables for Priority, Expedited, Ground.

### Tab 3: Transit Performance

**Purpose:** Show distribution of delivery speed without overshadowing SLA compliance.

| Transit Days | Count | Percentage | Cumulative % | SLA Status  |
| ------------ | ----- | ---------- | ------------ | ----------- |
| Day 0        | ###   | ##.#%      | ##.#%        | Within SLA  |
| Day 1        | ###   | ##.#%      | ##.#%        | Within SLA  |
| …            | ###   | ##.#%      | ##.#%        | Within SLA  |
| Day X+1      | ###   | ##.#%      | ##.#%        | Outside SLA |

**Simplification rule:** Frame daily insights relative to the SLA window. Example: "95% of Ground delivered by Day 6, within the 8-day SLA."

### Tab 4: Geographic Distribution

**Purpose:** Top 15 destination states with hub assignment and network type.

| State | Shipment Count | % of Total | Primary Hub | Network Type |
| ----- | -------------- | ---------- | ----------- | ------------ |
| NY    | ###            | ##.#%      | JFK/EWR     | Select       |
| CA    | ###            | ##.#%      | LAX         | Select       |
| …     | …              | …          | …           | National     |

**Note:** Reinforce that both Select and National support SLA performance.

### Tab 5: Zone Analysis

**Purpose:** Zone 1–8 distribution and regional vs cross-country summary. Use delivered packages for averages.

* Zone-by-zone: delivered count, share, average transit days, SLA status.
* Regional (Zones 1–4) vs Cross-Country (Zones 5–8) summary.

### Tab 6: In-Transit Detail

**Purpose:** Show current in-transit status by service level and determine if each shipment is within the SLA window.

**Summary by Service Level:**

| Service Level | SLA Window | Total In-Transit | Within Window | Outside Window (Late) | % Within |
| ------------- | ---------- | ---------------- | ------------- | --------------------- | -------- |

**Detailed records (top N rows):**

* Xparcel Type
* Start Date
* Days Since Ship
* SLA Window (3, 5, 8)
* Within SLA Window (Yes/No)
* Delivered Status
* Destination State
* Destination ZIP
* Calculated Zone
* Most Recent Scan
* Most Recent Scan Date

**Rule:** Within Window if Days Since Ship <= SLA Window. Otherwise Outside Window (SLA miss while in-transit).

### Tab 7: Notes and Assumptions

* SLA compliance is based on delivered shipments only, by service level.
* In-transit shipments are evaluated against Start Date + SLA window.
* SLA windows:

  * Priority = 3 days
  * Expedited = 5 days
  * Ground = 8 days
* Performance thresholds:

  * 100% = Perfect Compliance
  * ≥95% = Exceeds Standard
  * ≥90% = Meets Standard
  * <90% = Below Standard
* National Network = lower 48 coverage.
* Select Network = metro and regional focus.
* No carrier names are used in the report.

### Tab 8: SLA Misses

**Purpose:** List every shipment that is an SLA miss for fast diagnosis and ZIP-level tuning with the Pricing and Xparcel setup teams.

**SLA miss definitions**

* Delivered Outside SLA: delivered shipment with Days In Transit > SLA window.
* In-Transit Outside Window: in-transit shipment with Days Since Ship > SLA window.

**Output columns**

* Tracking Number
* Xparcel Service (Xparcel Priority, Expedited, Ground)
* Delivered Status
* Start Date
* Days In Transit or Days Since Ship
* SLA Window (days)
* SLA Miss Type (Delivered Outside SLA | In-Transit Outside Window)
* Destination ZIP
* Destination State
* Calculated Zone
* Network Type (National | Select)
* Primary Hub
* Most Recent Scan
* Most Recent Scan Date
* Days Since Last Scan
* Suggested Action

**Suggested Action examples**

* "Evaluate ZIP-limit: Ground → Expedited for this ZIP cluster."
* "Investigate linehaul and induction cadence for this lane."
* "Consider Expedited for Zones 7–8 on this lane."

**At-a-glance summaries at the top**

1. By Service: Misses, % of misses, split by miss type.
2. By Network Type: Misses and split by miss type.
3. Top 20 ZIPs by misses: ZIP, misses, service mix, avg days late.
4. By Zone: Misses, % of misses, service mix.

### Tab 9: Brand Style Guide

**Purpose:** Color reference for consistent branding.

**Colors**

* FirstMile Blue: `#366092`
* Light Gray: `#DDDDDD`
* Red: `#FFC7CE` (Below Standard)
* Yellow: `#FFEB84` (Meets Standard)
* Green: `#C6EFCE` (Exceeds or Perfect)

**Excel styling**

* All header rows use FirstMile Blue with white bold text.
* Thin gray borders for data.
* Auto-filters on all header rows.
* Columns auto-size with max width 50 characters.

## Excel Styling Requirements (helpers)

```python
FIRSTMILE_BLUE = "366092"
LIGHT_GRAY = "DDDDDD"
RED_BG = "FFC7CE"
YELLOW_BG = "FFEB84"
GREEN_BG = "C6EFCE"

def apply_header_style(ws, row=1):
    blue_fill = PatternFill(start_color=FIRSTMILE_BLUE, end_color=FIRSTMILE_BLUE, fill_type="solid")
    white_font = Font(color="FFFFFF", bold=True, size=11)
    center_align = Alignment(horizontal="center", vertical="center")
    for cell in ws[row]:
        cell.fill = blue_fill
        cell.font = white_font
        cell.alignment = center_align

def apply_data_style(ws, start_row=2):
    thin = Side(style='thin', color=LIGHT_GRAY)
    thin_border = Border(left=thin, right=thin, top=thin, bottom=thin)
    center_align = Alignment(horizontal="center", vertical="center")
    for row in ws.iter_rows(min_row=start_row):
        for cell in row:
            cell.border = thin_border
            cell.alignment = center_align

def auto_size_columns(ws, max_width=50):
    for col in ws.columns:
        length = max(len(str(c.value)) if c.value is not None else 0 for c in col)
        ws.column_dimensions[col[0].column_letter].width = min(length + 2, max_width)
```

## Common Mistakes to Avoid

**Mistake 1: Wrong service detection**

* Wrong: using a Days In Transit average that includes in-transit rows.
* Correct: rely on Xparcel Type and per-service calculations only.

**Mistake 2: Including in-transit in delivered SLA**

* Wrong: denominator includes all packages.
* Correct: delivered-only denominator for SLA compliance.

**Mistake 3: Single SLA window for all services**

* Wrong: assume 8 days for everything.
* Correct: use 3, 5, 8 by service.

**Mistake 4: NaN handling**

* Wrong: iterating or sorting on NaN service types.
* Correct: filter out NaN before loops and mapping.

**Mistake 5: Wrong date for in-transit evaluation**

* Wrong: using Request Date.
* Correct: use Start Date to compute Days Since Ship for SLA window checks.

**Mistake 6: Marking all in-transit as not a miss**

* Wrong: assuming "in-transit = not a miss".
* Correct: evaluate Start Date + SLA window to determine if it is already late.

**Mistake 7: Unicode issues in console**

* Keep console output ASCII safe.

## Performance Thresholds

```python
PERF_THRESHOLDS = [
    (100.0, "Perfect Compliance"),
    (95.0, "Exceeds Standard"),
    (90.0, "Meets Standard"),
    (0.0,  "Below Standard")
]

def status_from_pct(pct):
    for threshold, label in PERF_THRESHOLDS:
        if pct >= threshold:
            return label
```

## Output Filename Format

```python
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
customer_clean = CUSTOMER_NAME.replace(' ', '_')
filename = f"FirstMile_Xparcel_Performance_{customer_clean}_{timestamp}.xlsx"
# Example: FirstMile_Xparcel_Performance_JM_Group_NY_20250930_1149.xlsx
```

## Validation Checklist (final QA before send)

* SLA compliance is calculated on delivered packages only.
* Performance is broken down by Priority, Expedited, Ground with correct SLA windows (3, 5, 8).
* In-transit shipments are evaluated using Start Date against the SLA window.
* SLA misses are flagged for:

  * Delivered Outside SLA (delivered rows only)
  * In-Transit Outside Window (in-transit rows beyond the window)
* Transit performance shows cumulative percentages by day, framed against SLA windows.
* Geographic tab shows Select vs National network with correct definitions.
* Zone analysis uses delivered packages only for averages.
* Tab 8 (SLA Misses) exists with Top 20 ZIPs and Suggested Action populated.
* Tab 9 (Brand Style Guide) is present with color definitions.
* FirstMile blue headers, white text, borders, filters, and column auto-size applied.
* No carrier names. "eCommerce" spelled with camel-case C.
* Plain, factual, professional tone.

## Key Insights to Surface

* Overall delivered SLA compliance (typically ≥ 99% when supported by data).
* Service-level compliance and statuses.
* Early delivery as a supporting metric only, tied to SLA windows.
* In-transit status: count within window vs outside window, with examples.
* Network distribution and reliability across Select and National.

## Forbidden Practices

* Do not calculate SLA on all shipments.
* Do not mark all in-transit shipments as misses or not misses. Always check Start Date vs SLA window.
* Do not collapse service levels into a single SLA window.
* Do not name carriers.
* Do not lead with daily delivery percentages over SLA compliance.

## Python Dependencies

```python
import pandas as pd
import numpy as np
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
```

## Implementation Notes and Workflow

Always use this workflow:

1. Load data and validate required columns.
2. Detect report period from date columns.
3. Calculate delivered-only SLA by service level.
4. Calculate in-transit status by service level using Start Date + SLA window.
5. Calculate geographic and zone distributions.
6. Create Excel workbook with 9 tabs (Executive Summary, SLA Compliance, Transit Performance, Geographic Distribution, Zone Analysis, In-Transit Detail, Notes and Assumptions, SLA Misses, Brand Style Guide).
7. Apply consistent styling (FirstMile blue headers, borders, filters, auto-size).
8. Save with timestamp filename.

## Code Structure (recommended functions)

```python
def load_data(file_path)
def detect_report_period(df)
def calculate_sla_by_service_level(df)              # returns list of dicts
def calculate_in_transit_by_service_level(df, today) # returns list, summary, detail
def calculate_geographic_distribution(df, hub_map, network_lookup)
def calculate_zone_analysis(df)
def build_tab_executive_summary(wb, ...)
def build_tab_sla_compliance(wb, ...)
def build_tab_transit_performance(wb, ...)
def build_tab_geographic(wb, ...)
def build_tab_zone_analysis(wb, ...)
def build_tab_in_transit(wb, ...)
def build_tab_notes(wb)
def build_tab_sla_misses(wb, ...)                    # new tab 8
def build_tab_brand_style(wb)                        # moved to tab 9
def apply_header_style(ws, row=1)
def apply_data_style(ws, start_row=2)
def auto_size_columns(ws, max_width=50)
def generate_report()
```

## Sample Output Summary (customer-facing example)

**FirstMile Xparcel Performance Report**
Customer: JM Group NY
Period: August 7 – September 29, 2025

**SLA Performance by Service Level**

* Xparcel Priority (3-day SLA)
  100.0% compliance (26 delivered). All delivered same day (Day 0).
* Xparcel Expedited (5-day SLA)
  100.0% compliance (62 delivered). Average 2.0 days. 100% delivered by Day 4.
* Xparcel Ground (8-day SLA)
  99.9% compliance (1,053 delivered). Average 3.3 days. 95.3% delivered by Day 6. 1 package exceeded the 8-day SLA.

Overall delivered SLA compliance: 99.9% — Exceeds Standard.

**In-Transit Status (Start Date + SLA window)**

* Total In-Transit: 1,084
* Within SLA Window: 1,053 (97.1%)
* Outside SLA Window (SLA Miss): 31 (2.9%)

Examples:

* Ground shipment shipped 9/1/25 → 30 days vs 8-day SLA → SLA Miss.
* Ground shipment shipped 9/25/25 → 5 days vs 8-day SLA → Within Window.

**Network Distribution**

* Select Network: 45%
* National Network: 55%
* SLA performance consistent across both networks.

## Document Version

* Version: 2.0
* Last Updated: 2025-09-30
* Validated Against: JM Group NY dataset (2,817 shipments, Aug–Sep 2025)
