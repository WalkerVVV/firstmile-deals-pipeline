# Tracking Data Parsing - Comprehensive Learnings

**Created**: November 4, 2025
**Context**: BoxiiShip System Beauty TX tracking data processing
**Purpose**: Document all learnings and mistakes to avoid in future tracking data processing tasks

---

## Context
User provides unstructured tracking data (text format from web scraping) and needs it converted to Excel files for integration into a larger dataset. The tracking data includes tracking numbers with associated status updates, dates, and locations.

---

## Critical Rules - DO NOT VIOLATE

### 1. Parse User's Provided Data, Not Existing Files
**MISTAKE**: Using existing structured data (Excel files) instead of parsing the raw text data the user provided
**CORRECT**: Always parse the EXACT data the user provides in their message or referenced files

### 2. Verify Counts Match User's Specification
**MISTAKE**: Processing 110 tracking numbers when user provided 693, or 1,332 when user provided 1,436
**CORRECT**:
- If user says "I'm giving you X tracking IDs", the output MUST have exactly X rows
- Count verification is MANDATORY before completing the task
- If counts don't match, find the missing items and include them

### 3. Don't Overanalyze - Deliver What's Requested
**MISTAKE**: Creating analysis documents, summaries, and interpretations when user only asked for Excel files
**CORRECT**:
- User says "I just need the two files" = deliver two files, nothing else
- No analysis, no conclusions, no context beyond what's explicitly requested
- The data is a piece of a larger puzzle - respect that you don't have the full context

### 4. Handle Missing Data Gracefully
**MISTAKE**: Excluding tracking numbers that don't have status updates
**CORRECT**:
- If user provides list of 1,436 tracking IDs but only 1,332 have tracking data, create Excel with ALL 1,436
- Fill missing data with blank/empty cells, not exclude rows
- Preserve the EXACT list the user provided

---

## Data Format Understanding

### Tracking Data Text Format
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
1. Identify tracking numbers: Lines starting with digit, length ≥18
2. Skip empty lines and separators ("View More Tracking Info")
3. Extract status: First non-empty line after tracking number
4. Extract date: Look for day-of-week keywords (Monday-Sunday)
5. Extract location: Line after date, before next "View More" (if exists)
6. Handle cases where location is missing (don't fail, just leave empty)

---

## Exact Task Execution Flow

### Step 1: Understand the Request
- How many tracking number files? (e.g., 2: "BLANK -MP" and "In-Transit -MP")
- How many tracking IDs in each? (e.g., 1,436 and 693)
- What source data files? (e.g., .txt files with raw tracking data)

### Step 2: Parse Each Source File
```python
# Read source file
with open('source_file.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f.readlines()]

# Parse tracking data
tracking_data = []
i = 0
while i < len(lines):
    line = lines[i]

    # Skip headers, empty lines
    if not line or 'header text' in line:
        i += 1
        continue

    # Identify tracking number
    if line[0].isdigit() and len(line) >= 18:
        tracking_num = line
        status = ''
        date = ''
        location = ''

        # Get status (next non-empty line)
        j = i + 1
        while j < len(lines) and not lines[j]:
            j += 1
        if j < len(lines) and 'View More' not in lines[j]:
            status = lines[j]
            j += 1

        # Get date (look for day of week)
        while j < len(lines) and not lines[j]:
            j += 1
        if j < len(lines):
            potential_date = lines[j]
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            if any(day in potential_date for day in days):
                date = potential_date
                j += 1

                # Get location (if exists)
                while j < len(lines) and not lines[j]:
                    j += 1
                if j < len(lines) and 'View More' not in lines[j]:
                    location = lines[j]

        tracking_data.append({
            'Tracking Number': tracking_num,
            'Status': status,
            'Date': date,
            'Location': location
        })

    i += 1
```

### Step 3: Handle User's Specific Tracking List
If user provides a specific list of tracking IDs (e.g., 1,436 IDs):
```python
# Read user's tracking list
with open('user_tracking_list.txt', 'r') as f:
    user_tracking_ids = [line.strip() for line in f if line.strip()]

# Create dictionary from parsed data
tracking_dict = {item['Tracking Number']: item for item in tracking_data}

# Build complete dataset with ALL user's tracking IDs
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
```

### Step 4: Verify Count BEFORE Creating Excel
```python
expected_count = 1436  # or whatever user specified
actual_count = len(complete_data)

if actual_count != expected_count:
    print(f"ERROR: Expected {expected_count}, got {actual_count}")
    # FIX THIS BEFORE PROCEEDING
else:
    print(f"✓ Count verified: {actual_count} tracking numbers")
```

### Step 5: Create Excel with Professional Formatting
```python
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment

df = pd.DataFrame(complete_data)

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name='Sheet Name')
    worksheet = writer.sheets['Sheet Name']

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
```

### Step 6: Final Verification
```python
# Verify the Excel file
df_verify = pd.read_excel(output_file)
print(f"Final file has {len(df_verify)} rows")
print(f"Status filled: {df_verify['Status'].notna().sum()}")
print(f"Date filled: {df_verify['Date'].notna().sum()}")
print(f"Location filled: {df_verify['Location'].notna().sum()}")
```

---

## Common Pitfalls to Avoid

### ❌ WRONG: Using Existing Data
```python
# DON'T DO THIS
df = pd.read_excel('existing_file.xlsx')
df_filtered = df[df['column'] == 'value']
# This ignores the user's provided data!
```

### ✅ CORRECT: Parse User's Data
```python
# DO THIS
with open('user_provided_file.txt', 'r') as f:
    user_data = parse_tracking_data(f.read())
df = pd.DataFrame(user_data)
```

### ❌ WRONG: Excluding Missing Data
```python
# DON'T DO THIS
if tracking_id in parsed_data:
    complete_data.append(parsed_data[tracking_id])
# This creates fewer rows than user expects!
```

### ✅ CORRECT: Include All with Blanks
```python
# DO THIS
if tracking_id in parsed_data:
    complete_data.append(parsed_data[tracking_id])
else:
    complete_data.append({'Tracking Number': tracking_id, 'Status': '', 'Date': '', 'Location': ''})
```

### ❌ WRONG: Creating Analysis Documents
```python
# DON'T DO THIS when user only asked for Excel files
create_summary_document()
create_analysis_report()
create_recommendations()
```

### ✅ CORRECT: Deliver Requested Files Only
```python
# DO THIS
create_excel_file_1()
create_excel_file_2()
# Done. Nothing more.
```

---

## Success Criteria Checklist

- [ ] Parsed user's provided data (not existing Excel files)
- [ ] Final row count matches user's specification exactly
- [ ] All tracking IDs from user's list are included
- [ ] Missing data filled with blanks, not excluded
- [ ] Excel has proper formatting (FirstMile blue headers, centered alignment)
- [ ] Auto-filter enabled
- [ ] No additional analysis documents created (unless explicitly requested)
- [ ] File size reasonable (check with `ls -lh`)
- [ ] Verification output shown to user with exact counts

---

## Example User Request Pattern

**User**: "Create two Excel files: BLANK -MP with 1,436 tracking IDs and In-Transit -MP with 693 tracking IDs. Source data in these .txt files."

**Your Response**:
1. Parse both .txt files
2. Match against user's tracking ID lists (if provided)
3. Create Excel file 1 with EXACTLY 1,436 rows
4. Create Excel file 2 with EXACTLY 693 rows
5. Report: "Created BLANK_MP_Tracking_Nov4_2025.xlsx (1,436 rows) and In_Transit_MP_Tracking_Complete_Nov4_2025.xlsx (693 rows)"
6. STOP. No analysis. No summary. Task complete.

---

## File Naming Convention
- Use descriptive names: `BLANK_MP_Tracking_Nov4_2025.xlsx`
- Include date: `Nov4_2025` or similar
- Use underscores, not spaces
- Keep consistent with user's existing file naming patterns

---

## Actual Files Created from This Learning

**Session Date**: November 4, 2025

**Files Created**:
1. `BLANK_MP_Tracking_Nov4_2025.xlsx` (50KB, 1,436 rows)
   - Source: `BLANK -MP BoxiiShip SB Logistics LLC TX Oct 6.txt`
   - User's tracking list: `blank_mp_tracking_list.txt`
   - All 1,436 tracking IDs included with complete data where available

2. `In_Transit_MP_Tracking_Complete_Nov4_2025.xlsx` (27KB, 693 rows)
   - Source: `raw_tracking_data.txt`
   - All 693 tracking IDs with complete tracking status updates

**Scripts Created**:
- `parse_blank_mp_complete.py` - Parses BLANK -MP tracking data
- `create_complete_blank_mp.py` - Creates complete Excel with all 1,436 IDs
- `parse_all_tracking_data.py` - Parses In-Transit -MP tracking data

---

## Key Takeaways

1. **Listen to the user's count** - If they say 1,436, deliver 1,436, not 1,332
2. **Don't take shortcuts** - Parse the data they gave you, not what's easier
3. **Don't overanalyze** - If they say "just the files", give them just the files
4. **Include everything** - Missing data = blank cells, not missing rows
5. **Verify before declaring done** - Row count must match specification

---

**End of Document**
