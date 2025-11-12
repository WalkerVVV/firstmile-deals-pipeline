# FirstMile Deals - Master Comprehensive Learnings

**Purpose**: Universal reference document for all FirstMile Deals analysis, automation, and workflow tasks
**Created**: November 3-4, 2025
**Last Updated**: November 4, 2025
**Status**: Production Reference ✅

---

## 📚 Document Overview

This master document combines learnings from multiple sessions into one comprehensive reference:

1. **Tracking Data Parsing** - Universal principles for processing shipping data
2. **Prioritization & Pipeline Management** - HubSpot API integration best practices
3. **System Architecture** - FirstMile Deals automation framework
4. **General Workflow Principles** - Cross-cutting concerns and best practices

---

# PART 1: TRACKING DATA PARSING LEARNINGS

## Context
Processing unstructured tracking data (text from web scraping, carrier exports) into structured Excel files for analysis, reporting, and integration with larger datasets.

## ⚠️ CRITICAL RULES - DO NOT VIOLATE

### 1. Parse User's Provided Data, Not Existing Files
❌ **WRONG**: Using existing structured data (Excel files) instead of parsing raw text
✅ **CORRECT**: Always parse the EXACT data the user provides in their message or referenced files

**Why**: User is asking you to process NEW data, not reformat existing processed data.

### 2. Verify Counts Match User's Specification
❌ **WRONG**: Processing 110 tracking numbers when user provided 693, or 1,332 when user provided 1,436
✅ **CORRECT**:
- If user says "I'm giving you X tracking IDs", output MUST have exactly X rows
- Count verification is MANDATORY before completing the task
- If counts don't match, find missing items and include them

**Why**: Missing data indicates incomplete processing, not that the data doesn't exist.

### 3. Don't Overanalyze - Deliver What's Requested
❌ **WRONG**: Creating analysis documents, summaries, interpretations when user only asked for Excel files
✅ **CORRECT**:
- User says "I just need the two files" = deliver two files, nothing else
- No analysis, no conclusions, no context beyond what's explicitly requested
- Data is piece of a larger puzzle - respect that you don't have full context

**Why**: User has their own analysis plan; extra documents create confusion, not value.

### 4. Handle Missing Data Gracefully
❌ **WRONG**: Excluding tracking numbers that don't have status updates
✅ **CORRECT**:
- If user provides 1,436 tracking IDs but only 1,332 have tracking data, create Excel with ALL 1,436
- Fill missing data with blank/empty cells, not exclude rows
- Preserve the EXACT list the user provided

**Why**: Blank cells communicate "no data available"; missing rows communicate "forgotten/lost".

## Tracking Data Text Format

### Standard Pattern
```
[Tracking Number - 18+ digits]
[Empty line]
[Status - e.g., "Delivered", "Shipment info received."]
[Date - includes day of week, e.g., "Monday, October 6, 2025"]
[Location - OPTIONAL, e.g., "Norfolk, MA" or empty]
[Separator line - "View More Tracking Info"]
[Next Tracking Number]
```

### Parsing Logic
```python
def parse_tracking_data(lines):
    tracking_data = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines and headers
        if not line or 'View More' in line:
            i += 1
            continue

        # Identify tracking number (starts with digit, length ≥18)
        if line[0].isdigit() and len(line) >= 18:
            tracking_num = line
            status = ''
            date = ''
            location = ''

            # Get status (next non-empty line)
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and 'View More' not in lines[j]:
                status = lines[j].strip()
                j += 1

            # Get date (look for day of week)
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                potential_date = lines[j].strip()
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                if any(day in potential_date for day in days):
                    date = potential_date
                    j += 1

                    # Get location (if exists)
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and 'View More' not in lines[j]:
                        location = lines[j].strip()

            tracking_data.append({
                'Tracking Number': tracking_num,
                'Status': status,
                'Date': date,
                'Location': location
            })

        i += 1

    return tracking_data
```

## Excel Creation with FirstMile Branding

```python
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment

def create_firstmile_excel(data, output_file, sheet_name='Tracking Data'):
    """Create Excel with FirstMile professional formatting"""

    df = pd.DataFrame(data)

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)
        worksheet = writer.sheets[sheet_name]

        # Column widths
        worksheet.column_dimensions['A'].width = 28  # Tracking Number
        worksheet.column_dimensions['B'].width = 50  # Status
        worksheet.column_dimensions['C'].width = 30  # Date
        worksheet.column_dimensions['D'].width = 35  # Location

        # FirstMile blue header (#366092)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF", size=11)
        header_alignment = Alignment(horizontal="center", vertical="center")

        for cell in worksheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = header_alignment

        # Center align tracking numbers and dates
        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=1, max_col=1):
            for cell in row:
                cell.alignment = Alignment(horizontal="center")

        for row in worksheet.iter_rows(min_row=2, max_row=worksheet.max_row, min_col=3, max_col=3):
            for cell in row:
                cell.alignment = Alignment(horizontal="center")

        # Auto-filter
        worksheet.auto_filter.ref = worksheet.dimensions

    return df
```

## Complete Workflow Example

```python
# Step 1: Read user's tracking list
with open('user_tracking_list.txt', 'r') as f:
    user_tracking_ids = [line.strip() for line in f if line.strip()]

print(f"User provided {len(user_tracking_ids)} tracking IDs")

# Step 2: Parse raw tracking data
with open('raw_tracking_data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

tracking_data = parse_tracking_data(lines)
print(f"Parsed {len(tracking_data)} tracking records from source")

# Step 3: Create complete dataset (ALL user's IDs)
tracking_dict = {item['Tracking Number']: item for item in tracking_data}

complete_data = []
for tracking_id in user_tracking_ids:
    if tracking_id in tracking_dict:
        complete_data.append(tracking_dict[tracking_id])
    else:
        # Missing data - include with blanks
        complete_data.append({
            'Tracking Number': tracking_id,
            'Status': '',
            'Date': '',
            'Location': ''
        })

# Step 4: VERIFY COUNT
expected = len(user_tracking_ids)
actual = len(complete_data)

if actual != expected:
    print(f"❌ ERROR: Expected {expected}, got {actual}")
    # FIX THIS BEFORE PROCEEDING
else:
    print(f"✓ Count verified: {actual} tracking numbers")

# Step 5: Create Excel
df = create_firstmile_excel(
    complete_data,
    'Tracking_Data_Complete.xlsx',
    'Tracking Data'
)

# Step 6: Final verification
filled_status = df['Status'].notna().sum()
filled_date = df['Date'].notna().sum()
print(f"Final file: {len(df)} rows, {filled_status} with status, {filled_date} with dates")
```

## Success Criteria Checklist

- [ ] Parsed user's provided data (not existing Excel files)
- [ ] Final row count matches user's specification exactly
- [ ] All tracking IDs from user's list are included
- [ ] Missing data filled with blanks, not excluded
- [ ] Excel has FirstMile blue headers (#366092), centered alignment
- [ ] Auto-filter enabled
- [ ] No additional analysis documents created (unless explicitly requested)
- [ ] Verification output shown with exact counts

---

# PART 2: PRIORITIZATION & PIPELINE MANAGEMENT

## Context
Managing FirstMile sales pipeline with HubSpot CRM integration, ensuring accurate priority calculations and actionable daily reports.

## ⚠️ CRITICAL RULES - DO NOT VIOLATE

### 1. Always Use HubSpot API as Source of Truth
❌ **WRONG**: Parse folder structure and markdown files for deal data
✅ **CORRECT**: Query HubSpot API directly for all deal information

**Why**: Folder structure can get out of sync due to manual moves, git operations, automation delays. HubSpot is authoritative.

### 2. Filter to Active Stages Only (1-6)
❌ **WRONG**: Include stage 0 (LEAD), stage 7 (Started Shipping), stage 8 (Closed Lost)
✅ **CORRECT**: Only include stages 1-6 in priority calculations

**HubSpot Pipeline (8 stages)**:
1. Discovery Scheduled ✅ ACTIVE
2. Discovery Complete ✅ ACTIVE
3. Rate Creation ✅ ACTIVE
4. Proposal Sent ✅ ACTIVE
5. Setup Docs Sent ✅ ACTIVE
6. Implementation ✅ ACTIVE
7. Started Shipping ❌ EXCLUDE (Closed Won)
8. Closed Lost ❌ EXCLUDE

**Why**: Closed deals don't need daily prioritization; cold leads (stage 0) managed separately in `_LEADS/` folder.

### 3. Use Stage IDs, Not Stage Numbers
❌ **WRONG**: Filter by `stage_num in [1, 2, 3, 4, 5, 6]` from folder names
✅ **CORRECT**: Filter by HubSpot stage IDs: `'1090865183', 'd2a08d6f-cc04-4423-9215-594fe682e538', ...`

**Why**: Folder numbering may not match HubSpot's internal stage structure.

### 4. Calculate Stagnation from hs_lastmodifieddate
❌ **WRONG**: Use git log timestamps or folder modification dates
✅ **CORRECT**: Use HubSpot's `hs_lastmodifieddate` property

**Why**: Git commits don't reflect deal activity; HubSpot tracks real customer engagement.

### 5. Use Deal Amount Property, Not Parsed Values
❌ **WRONG**: Regex parse markdown files for dollar amounts
✅ **CORRECT**: Use HubSpot's `amount` property directly

**Why**: Markdown files can be outdated; HubSpot has current deal value.

## HubSpot API Integration

### Fetch Active Deals
```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('HUBSPOT_API_KEY')
OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

ACTIVE_STAGES = [
    '1090865183',                               # [01-DISCOVERY-SCHEDULED]
    'd2a08d6f-cc04-4423-9215-594fe682e538',     # [02-DISCOVERY-COMPLETE]
    'e1c4321e-afb6-4b29-97d4-2b2425488535',     # [03-RATE-CREATION]
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a',     # [04-PROPOSAL-SENT]
    '4e549d01-674b-4b31-8a90-91ec03122715',     # [05-SETUP-DOCS-SENT]
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307'      # [06-IMPLEMENTATION]
]

def fetch_active_deals_from_hubspot():
    """Fetch active deals from HubSpot (stages 1-6 only)"""

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'filterGroups': [{
            'filters': [
                {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': OWNER_ID},
                {'propertyName': 'pipeline', 'operator': 'EQ', 'value': PIPELINE_ID},
                {'propertyName': 'dealstage', 'operator': 'IN', 'values': ACTIVE_STAGES}
            ]
        }],
        'properties': ['dealname', 'dealstage', 'amount', 'createdate', 'hs_lastmodifieddate'],
        'limit': 100
    }

    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/deals/search',
        headers=headers,
        json=payload,
        timeout=10
    )

    if response.status_code != 200:
        print(f'❌ HubSpot API Error: {response.status_code}')
        return []

    return response.json().get('results', [])
```

### Priority Scoring Algorithm
```python
SCORING_WEIGHTS = {
    "deal_size": 0.50,      # 50% - Deal value drives priority
    "stage": 0.20,          # 20% - Later stages need more attention
    "stagnation": 0.15,     # 15% - Stale deals need immediate action
    "complexity": 0.10,     # 10% - Complex deals need more time
    "strategic": 0.05       # 5% - Strategic accounts bonus
}

DEAL_TIERS = {
    "mega": 10_000_000,      # $10M+
    "enterprise": 1_000_000,  # $1M+
    "mid_market": 500_000,    # $500K+
    "small": 100_000,         # $100K+
    "micro": 0                # <$100K
}

STAGE_MULTIPLIERS = {
    "[01-DISCOVERY-SCHEDULED]": 0.3,
    "[02-DISCOVERY-COMPLETE]": 0.4,
    "[03-RATE-CREATION]": 0.6,      # Bottleneck stage
    "[04-PROPOSAL-SENT]": 0.8,       # High urgency
    "[05-SETUP-DOCS-SENT]": 0.9,
    "[06-IMPLEMENTATION]": 1.0,      # Highest priority
}

def calculate_priority_score(deal_name, deal_value, stage_name, days_stagnant):
    """Calculate comprehensive priority score (0-100)"""

    score = 0

    # 1. Deal size score (0-50 points)
    if deal_value >= DEAL_TIERS["mega"]:
        size_score = 50
        tier = "MEGA"
    elif deal_value >= DEAL_TIERS["enterprise"]:
        size_score = 40
        tier = "ENTERPRISE"
    elif deal_value >= DEAL_TIERS["mid_market"]:
        size_score = 30
        tier = "MID-MARKET"
    elif deal_value >= DEAL_TIERS["small"]:
        size_score = 20
        tier = "SMALL"
    else:
        size_score = 10
        tier = "MICRO"

    score += size_score * SCORING_WEIGHTS["deal_size"]

    # 2. Stage score (0-20 points)
    stage_multiplier = STAGE_MULTIPLIERS.get(stage_name, 0.5)
    stage_score = stage_multiplier * 20
    score += stage_score * SCORING_WEIGHTS["stage"]

    # 3. Stagnation urgency (0-15 points)
    if days_stagnant > 60:
        stagnation_score = 15  # CRITICAL
    elif days_stagnant > 21:
        stagnation_score = 12  # HIGH
    elif days_stagnant > 14:
        stagnation_score = 9   # MEDIUM
    elif days_stagnant > 7:
        stagnation_score = 6   # LOW
    else:
        stagnation_score = 3   # RECENT

    score += stagnation_score * SCORING_WEIGHTS["stagnation"]

    # 4. Complexity multiplier (0-10 points)
    if deal_value >= DEAL_TIERS["enterprise"]:
        complexity_score = 10
    elif deal_value >= DEAL_TIERS["mid_market"]:
        complexity_score = 7
    else:
        complexity_score = 5

    score += complexity_score * SCORING_WEIGHTS["complexity"]

    # 5. Strategic account bonus (0-5 points)
    strategic_keywords = ["wellness", "vitamin", "supplement", "health", "beauty"]
    is_strategic = any(kw in deal_name.lower() for kw in strategic_keywords)
    strategic_score = 5 if is_strategic else 0
    score += strategic_score * SCORING_WEIGHTS["strategic"]

    return round(score, 1), tier
```

## Folder Organization

### Before (WRONG)
```
FirstMile_Deals/
  ├── [00-LEAD]_AG1_Athletic_Greens/
  ├── [00-LEAD]_Athleta/
  ├── ... (46 more cold leads)
  ├── [01-DISCOVERY-SCHEDULED]_Joshs_Frogs/
  └── [04-PROPOSAL-SENT]_ODW_Logistics/
```

### After (CORRECT)
```
FirstMile_Deals/
  ├── _LEADS/ (centralized cold leads)
  │   ├── AG1_Athletic_Greens/
  │   ├── Athleta/
  │   └── ... (16 cold leads)
  ├── [01-DISCOVERY-SCHEDULED]_Joshs_Frogs/
  └── [04-PROPOSAL-SENT]_ODW_Logistics/
```

**Why**: Cold leads don't need daily prioritization; keep main directory clean for active pipeline (stages 1-6).

---

# PART 3: SYSTEM ARCHITECTURE PRINCIPLES

## Data Source Hierarchy

**Priority Order** (most authoritative first):
1. **HubSpot API** - CRM data, deal stages, amounts, dates
2. **User-Provided Files** - Raw data explicitly given in current task
3. **Folder Structure** - Organizational system (NOT data source)
4. **Markdown Documentation** - Supporting context (can be outdated)

**Rule**: Always use highest-priority available source for each data type.

## Error Handling

### Null Value Handling
```python
# ALWAYS handle null/empty values from APIs and user data

# Example: Deal amount
amount_str = deal['properties'].get('amount', '0')
try:
    deal_value = int(float(amount_str)) if amount_str else 0
except:
    deal_value = 0

# Example: Date parsing
from dateutil import parser

def days_since(date_str):
    if not date_str:
        return 999  # High number indicates "unknown"
    try:
        date = parser.parse(date_str)
        return (datetime.now(date.tzinfo) - date).days
    except:
        return 999
```

### API Error Handling
```python
try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)

    if response.status_code != 200:
        print(f'❌ API Error: {response.status_code}')
        return []

    return response.json().get('results', [])

except requests.exceptions.Timeout:
    print('❌ API Timeout')
    return []
except Exception as e:
    print(f'❌ Unexpected error: {e}')
    return []
```

## File Naming Conventions

### Excel Files
- **Pattern**: `{Description}_{Category}_{Date}.xlsx`
- **Examples**:
  - `BLANK_MP_Tracking_Nov4_2025.xlsx`
  - `In_Transit_MP_Tracking_Complete_Nov4_2025.xlsx`
  - `PRIORITIZATION_REPORT_20251103.md`

### Script Files
- **Pattern**: `{action}_{subject}_{variant}.py`
- **Examples**:
  - `parse_blank_mp_complete.py`
  - `create_complete_blank_mp.py`
  - `prioritization_agent.py`

### Documentation Files
- **Pattern**: `{SUBJECT}_{TYPE}.md`
- **Examples**:
  - `TRACKING_DATA_PARSING_LEARNINGS.md`
  - `PRIORITIZATION_AGENT_PROMPT.md`
  - `EOD_SYNC_TUESDAY_NOV_4_2025.md`

## FirstMile Branding Standards

### Colors
- **Primary**: #366092 (FirstMile blue)
- **Headers**: White text on #366092 background
- **Alternating rows**: Light gray (#F2F2F2) for readability

### Excel Formatting
- **Bold headers**: Font size 11, centered, white on blue
- **Column widths**: Auto-sized to content (max 50 chars)
- **Auto-filter**: Always enabled on header row
- **Alignment**: Center for tracking numbers, dates; left for status/location

### Service Level Names
- **Xparcel Ground**: 3-8 day economy
- **Xparcel Expedited**: 2-5 day faster ground
- **Xparcel Priority**: 1-3 day premium

**NEVER** name specific carriers (UPS, FedEx, USPS) - use "National" or "Select" network instead.

---

# PART 4: UNIVERSAL WORKFLOW PRINCIPLES

## The Three Laws of Task Execution

### 1. Evidence > Assumptions
- **Count verification** is mandatory before completion
- **API responses** must be validated (status code, data structure)
- **File existence** must be checked before reading
- **User specifications** must be matched exactly

### 2. Simplicity > Complexity
- **Deliver requested items only** - no extra analysis unless asked
- **Use direct APIs** when available - don't parse derived data
- **Include all data with blanks** - don't exclude missing items
- **Clear verification output** - show counts, not just "done"

### 3. Context > Cleverness
- **Understand user's larger goal** - don't just complete task mechanically
- **Preserve user's exact list** - if they gave 1,436 IDs, return 1,436 rows
- **Respect existing patterns** - match naming conventions, folder structures
- **Ask when ambiguous** - don't guess critical details

## Common Mistakes Across All Tasks

### ❌ Using Existing Processed Data Instead of Raw Data
**Pattern**: Reading Excel files when user provided .txt files
**Fix**: Always parse the EXACT data user provided

### ❌ Excluding Items with Missing Values
**Pattern**: Filtering out records without status updates
**Fix**: Include ALL items from user's list, fill missing with blanks

### ❌ Creating Unrequested Documentation
**Pattern**: Adding analysis reports when user asked for "just the files"
**Fix**: Deliver exactly what was requested, nothing more

### ❌ Trusting Folder Structure as Data Source
**Pattern**: Parsing folder names/files instead of querying APIs
**Fix**: Use authoritative source (HubSpot API) for all data

### ❌ Skipping Count Verification
**Pattern**: Assuming output is correct without checking row count
**Fix**: ALWAYS verify count matches user's specification before finishing

### ❌ Hardcoding Values That Can Change
**Pattern**: Using `stage_num in [1, 2, 3]` instead of API stage IDs
**Fix**: Use configuration variables that match current system state

## Quality Checklist (Apply to Every Task)

- [ ] **User Request Understood**: Clear on what user wants (not what's easier)
- [ ] **Data Source Verified**: Using correct source (API > user files > derived data)
- [ ] **Count Matches Specification**: Output rows = user's stated count
- [ ] **Missing Data Handled**: Blanks included, not rows excluded
- [ ] **Format Matches Standards**: FirstMile branding, naming conventions
- [ ] **Errors Handled Gracefully**: Try/except for nulls, API failures
- [ ] **Verification Output Shown**: Print counts, status before declaring done
- [ ] **Only Requested Items Delivered**: No extra analysis unless asked

---

# PART 5: REFERENCE QUICK GUIDE

## HubSpot Pipeline Stage IDs

```python
STAGE_MAP = {
    '1090865183': '[01-DISCOVERY-SCHEDULED]',
    'd2a08d6f-cc04-4423-9215-594fe682e538': '[02-DISCOVERY-COMPLETE]',
    'e1c4321e-afb6-4b29-97d4-2b2425488535': '[03-RATE-CREATION]',
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a': '[04-PROPOSAL-SENT]',
    '4e549d01-674b-4b31-8a90-91ec03122715': '[05-SETUP-DOCS-SENT]',
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307': '[06-IMPLEMENTATION]',
    '3fd46d94-78b4-452b-8704-62a338a210fb': '[07-STARTED-SHIPPING]',
    '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8': '[08-CLOSED-LOST]'
}
```

## FirstMile Contact Information

```python
OWNER_ID = "699257003"  # Brett Walker
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
PORTAL_ID = "46526832"
```

## Standard Python Imports

```python
import os
import sys
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime
from dateutil import parser
from dotenv import load_dotenv
from openpyxl.styles import Font, PatternFill, Alignment
```

## Related Documentation Files

- **`.claude/NEBUCHADNEZZAR_REFERENCE.md`** - System IDs, stage mappings, command reference
- **`.claude/PRIORITIZATION_AGENT_LEARNINGS.md`** - Deep dive on prioritization agent fixes
- **`.claude/PRIORITIZATION_AGENT_PROMPT.md`** - Production-ready code templates
- **`_LEADS/WORKFLOW_GUIDE.md`** - Cold lead management process
- **`[CUSTOMER]_BoxiiShip/TRACKING_DATA_PARSING_LEARNINGS.md`** - Original tracking data learnings

---

# SUMMARY: KEY TAKEAWAYS

## 🎯 Top 10 Universal Principles

1. **Parse user's provided data** - not existing processed files
2. **Count verification is mandatory** - before declaring task complete
3. **Use APIs as source of truth** - not derived folder/file data
4. **Include all items with blanks** - not exclude missing data
5. **Handle nulls gracefully** - try/except for all external data
6. **Match exact user specifications** - 1,436 means 1,436, not 1,332
7. **Deliver only what's requested** - no extra analysis unless asked
8. **FirstMile branding always** - blue headers, proper formatting
9. **Verify before finishing** - show counts, status in output
10. **Document learnings** - capture mistakes to prevent recurrence

## 🚫 Top 10 Mistakes to Avoid

1. ❌ Using existing Excel files instead of parsing raw data
2. ❌ Excluding records with missing values
3. ❌ Creating unrequested analysis documents
4. ❌ Trusting folder structure as data source
5. ❌ Skipping count verification
6. ❌ Hardcoding values that can change (stage numbers)
7. ❌ Naming specific carriers (use "National"/"Select")
8. ❌ Not handling null values from APIs
9. ❌ Including closed deals in daily priorities
10. ❌ Parsing dates from git logs instead of HubSpot

---

**Version**: 1.0 Master
**Status**: Production Reference ✅
**Last Updated**: November 4, 2025
**Applies To**: All FirstMile Deals analysis, automation, and workflow tasks
