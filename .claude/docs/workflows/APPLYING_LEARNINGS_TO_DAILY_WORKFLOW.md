# Applying Master Learnings to FirstMile Deals Daily Workflow

**Created**: November 5, 2025
**Purpose**: Translate comprehensive learnings from debugging sessions into actionable daily improvements

---

## Overview

This document shows **exactly how** to apply the principles from `MASTER_LEARNINGS_COMPREHENSIVE.md` to improve your FirstMile Deals workflow. Each section maps a learning to a specific script, process, or daily operation.

---

## 🎯 PRINCIPLE 1: Always Use HubSpot API as Source of Truth

### Current Issue
Multiple scripts still rely on folder parsing which can get out of sync with HubSpot.

### Affected Scripts & Fixes

#### ✅ ALREADY FIXED:
- **`prioritization_agent.py`** (v2.0) - Now uses HubSpot API directly

#### 🔧 NEEDS UPDATE:
- **`pipeline_sync_verification.py`** - Should query HubSpot first, then compare folders
- **`noon_sync.py`** - Already uses HubSpot API ✅ (no changes needed)
- **`daily_9am_sync.py`** - Already uses HubSpot API ✅ (no changes needed)

### Implementation Checklist

**For ANY new script that needs deal data:**
```python
# ✅ CORRECT - Query HubSpot API first
import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')
OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

payload = {
    'filterGroups': [{
        'filters': [
            {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': OWNER_ID},
            {'propertyName': 'pipeline', 'operator': 'EQ', 'value': PIPELINE_ID}
        ]
    }],
    'properties': ['dealname', 'dealstage', 'amount', 'hs_lastmodifieddate'],
    'limit': 100
}

response = requests.post(
    'https://api.hubapi.com/crm/v3/objects/deals/search',
    headers=headers, json=payload, timeout=10
)

deals = response.json().get('results', [])

# ❌ WRONG - Parsing folders as primary source
# for folder in repo_root.iterdir():
#     if folder.name.startswith('['):
#         # Parsing folder names for deal data
```

### Daily Application

**Morning 9AM Sync:**
1. Trust HubSpot API data shown in sync report
2. If folder names seem wrong → Fix folders to match HubSpot (not vice versa)
3. Verify with: `python .claude/agents/prioritization_agent.py`

---

## 🎯 PRINCIPLE 2: Complete Discovery Before Making Changes

### Current Issue
Tendency to make reactive changes without full codebase search, leading to missed references.

### Affected Workflows

#### When Renaming/Refactoring:
**MANDATORY Process:**
1. **Search ALL file types** for ALL variations
2. **Document all references** with context
3. **Plan update sequence** based on dependencies
4. **Execute changes** in coordinated manner
5. **Verify completion** with comprehensive post-change search

### Daily Application

**Example: Updating a stage name or ID**

**❌ WRONG Approach:**
```bash
# Just change it in one file and hope for the best
sed -i 's/old-stage-id/new-stage-id/' prioritization_agent.py
```

**✅ CORRECT Approach:**
```bash
# Step 1: Complete discovery
grep -r "old-stage-id" . --include="*.py" --include="*.md" > search_results.txt
grep -r "OLD_STAGE" . --include="*.py" --include="*.md" >> search_results.txt
grep -r "old stage" . --include="*.py" --include="*.md" >> search_results.txt

# Step 2: Review all matches, document impact
# Step 3: Create change plan with order of operations
# Step 4: Execute coordinated changes
# Step 5: Verify with same search - should return 0 matches
```

**When This Applies:**
- Renaming variables/constants across codebase
- Changing API endpoints or IDs
- Updating folder naming conventions
- Modifying stage names or workflows
- Refactoring common patterns

---

## 🎯 PRINCIPLE 3: Validate Regex Patterns Thoroughly

### Current Issue
Regex bugs can silently fail, showing 0 results instead of errors.

### Affected Scripts

#### Common Regex Patterns to Audit:
```python
# ❌ WRONG - Double backslash in raw string
match = re.match(r'\[(\\d+)-', folder_name)

# ✅ CORRECT - Single backslash in raw string
match = re.match(r'\[(\d+)-', folder_name)
```

### Daily Testing Protocol

**Before deploying ANY regex:**
```python
import re

# Test pattern on sample data
test_cases = [
    "[03-RATE-CREATION]_CustomerName",
    "[04-PROPOSAL-SENT]_AnotherCustomer",
    "[00-LEAD]_ColdLead"
]

pattern = r'\[(\d+)-([^\]]+)\]_(.+)'

for test in test_cases:
    match = re.match(pattern, test)
    if match:
        print(f"✅ {test} → Stage: {match.group(1)}, Name: {match.group(3)}")
    else:
        print(f"❌ {test} → NO MATCH (REGEX BUG!)")
```

### Implementation Checklist

**For ANY new script with regex:**
- [ ] Test pattern on 3-5 sample strings before deployment
- [ ] Include edge cases (shortest/longest names, special characters)
- [ ] Verify capture groups extract expected values
- [ ] Add debug output showing match results
- [ ] Document expected pattern in code comments

---

## 🎯 PRINCIPLE 4: Flexible File Search Over Hardcoded Names

### Current Issue
Scripts that only check specific filenames miss 90% of documentation.

### Affected Scripts & Fixes

#### ❌ OLD PATTERN (Brittle):
```python
# Only checks 2 specific files
for doc_file in ['Customer_Relationship_Documentation.md', 'README.md']:
    doc_path = folder / doc_file
    if doc_path.exists():
        content = doc_path.read_text()
```

#### ✅ NEW PATTERN (Flexible):
```python
# Search ALL markdown files
md_files = list(folder.glob('*.md'))
for doc_path in md_files:
    try:
        content = doc_path.read_text(encoding='utf-8', errors='ignore')
        # Extract data from content
    except Exception as e:
        print(f"⚠️  Could not read {doc_path}: {e}")
```

### Daily Application

**When Creating New Analysis Scripts:**
1. **Don't assume** file names - use glob patterns
2. **Search broadly** first, filter results second
3. **Handle errors** gracefully (encoding issues, permissions)
4. **Log what you find** for debugging

---

## 🎯 PRINCIPLE 5: Handle Null Values Gracefully

### Current Issue
HubSpot API returns null/empty for many fields, causing script failures.

### Affected Scripts

#### ✅ ALREADY FIXED:
- **`prioritization_agent.py`** (v2.0) - Has null handling
- **`noon_sync.py`** - Has null handling

#### 🔧 APPLY TO NEW SCRIPTS:

```python
# ✅ CORRECT - Safe null handling
deal_name = deal['properties'].get('dealname', 'Unnamed')
stage_id = deal['properties'].get('dealstage', '')

# Handle amount (can be null, empty, or string)
amount_str = deal['properties'].get('amount', '0')
try:
    deal_value = int(float(amount_str)) if amount_str else 0
except (ValueError, TypeError):
    deal_value = 0

# Handle dates (can be null)
last_modified = deal['properties'].get('hs_lastmodifieddate')
if last_modified:
    days_stagnant = days_since(last_modified)
else:
    days_stagnant = 999  # High number for "unknown"
```

### Daily Application

**Every HubSpot API call should:**
- Use `.get()` with defaults, never direct indexing
- Wrap type conversions in try/except
- Test with deals that have missing data
- Provide sensible defaults (0 for amounts, 'Unknown' for names)

---

## 🎯 PRINCIPLE 6: Exclude System Folders from Processing

### Current Issue
Processing `_LEADS/`, `.claude/`, `.git/` folders wastes time and causes errors.

### Affected Scripts & Fixes

#### ✅ ALREADY FIXED:
- **`prioritization_agent.py`** (v2.0) - Skips `_*` and `.*` folders
- **`brand_scout_agent.py`** - Creates folders in `_LEADS/`

#### 🔧 STANDARD PATTERN:

```python
from pathlib import Path

repo_root = Path('c:/Users/BrettWalker/FirstMile_Deals')

for folder in repo_root.iterdir():
    # Skip system folders (starts with _ or .)
    if folder.name.startswith('_') or folder.name.startswith('.'):
        continue

    # Skip non-directories
    if not folder.is_dir():
        continue

    # Skip specific system folders by name
    if folder.name in ['node_modules', 'venv', '__pycache__']:
        continue

    # Process only deal folders
    if folder.name.startswith('['):
        # This is a deal folder - process it
        pass
```

### Daily Application

**Folder Organization Rules:**
- `_LEADS/` → Cold leads only, excluded from active pipeline
- `.claude/` → System configuration, excluded from deal processing
- `.git/` → Version control, never process
- `[##-STAGE]_CustomerName/` → Active deals only

---

## 🎯 PRINCIPLE 7: Evidence-Based Validation

### Current Issue
Scripts complete without verifying actual results match expectations.

### Daily Sync Workflow Enhancement

#### Current EOD Sync Process:
```markdown
## EOD SYNC CHECKLIST (BEFORE)
- [ ] Run EOD sync script
- [ ] Files created in Downloads/
- [ ] Done
```

#### ✅ ENHANCED Evidence-Based Process:
```markdown
## EOD SYNC CHECKLIST (AFTER)
- [ ] Run EOD sync script
- [ ] Verify _DAILY_LOG.md has today's date (not yesterday!)
- [ ] Verify FOLLOW_UP_REMINDERS.txt shows tomorrow's date
- [ ] Count: Expected X customer emails → Found X in log (match!)
- [ ] Verify HubSpot pipeline movements have quotes as evidence
- [ ] Verify file sizes reasonable (>5KB minimum for comprehensive log)
- [ ] Open files and spot-check for data quality
- [ ] Done with evidence ✅
```

### Implementation for ALL Scripts

**Add verification step at the end:**
```python
def verify_results(expected_count, actual_count, output_file):
    """Verify results match expectations with evidence"""

    if actual_count != expected_count:
        print(f"❌ MISMATCH: Expected {expected_count}, got {actual_count}")
        print(f"   Check {output_file} for errors")
        return False

    if not output_file.exists():
        print(f"❌ OUTPUT FILE MISSING: {output_file}")
        return False

    file_size = output_file.stat().st_size
    if file_size < 1000:  # Less than 1KB is suspicious
        print(f"⚠️  WARNING: Output file very small ({file_size} bytes)")
        print(f"   Expected more data - verify content quality")

    print(f"✅ VERIFIED: {actual_count} items processed")
    print(f"✅ OUTPUT: {output_file} ({file_size:,} bytes)")
    return True

# Use at script end:
if __name__ == '__main__':
    results = main()
    verify_results(
        expected_count=len(input_data),
        actual_count=len(results),
        output_file=Path('output.xlsx')
    )
```

---

## 🎯 PRINCIPLE 8: Count Verification is Mandatory

### Current Issue
Scripts complete with wrong row counts, missing data.

### Tracking Data Processing Enhancement

#### For BoxiiShip-style Tracking Scripts:

**❌ OLD Approach:**
```python
# Create Excel file
df.to_excel('output.xlsx', index=False)
print("Done!")
```

**✅ NEW Evidence-Based Approach:**
```python
# Create Excel file
df.to_excel('output.xlsx', index=False)

# MANDATORY VERIFICATION
print(f"\n{'='*60}")
print("VERIFICATION REPORT")
print(f"{'='*60}")
print(f"User specified: {USER_EXPECTED_COUNT} tracking IDs")
print(f"Actually created: {len(df)} rows in Excel")
print(f"Match: {'✅ YES' if len(df) == USER_EXPECTED_COUNT else '❌ NO - INVESTIGATE!'}")
print(f"File size: {Path('output.xlsx').stat().st_size:,} bytes")
print(f"Status filled: {df['Status'].notna().sum()} / {len(df)}")
print(f"Date filled: {df['Date'].notna().sum()} / {len(df)}")
print(f"{'='*60}\n")

# FAIL if counts don't match
if len(df) != USER_EXPECTED_COUNT:
    print(f"🚨 CRITICAL ERROR: Row count mismatch!")
    print(f"   Expected {USER_EXPECTED_COUNT}, got {len(df)}")
    print(f"   Missing {USER_EXPECTED_COUNT - len(df)} rows")
    sys.exit(1)
```

### Daily Application

**For ANY Excel generation:**
1. User says "I have X items" → Your output MUST have exactly X rows
2. Print verification report showing expected vs actual
3. If mismatch → STOP and investigate before continuing
4. Include filled data stats (how many have status, dates, etc.)

---

## 🎯 PRINCIPLE 9: Don't Overanalyze - Deliver What's Requested

### Current Issue
Creating extra analysis documents when user only asked for Excel files.

### Daily Workflow Rule

**User Request Classification:**

| User Says | They Want | Don't Create |
|-----------|-----------|--------------|
| "Create Excel files with tracking data" | 2 Excel files | ❌ Analysis docs, summaries, insights |
| "Analyze shipping performance" | Full analysis report | ❌ Just raw Excel |
| "Quick PLD analysis" | Standard PLD output | ❌ Executive summary, recommendations |

**Implementation:**
```python
def determine_deliverables(user_request):
    """Parse what user actually wants, not what might be nice"""

    # Explicit request wins
    if "just the Excel" in user_request.lower():
        return {'excel': True, 'analysis': False, 'summary': False}

    if "I need two files" in user_request.lower():
        return {'file_count': 2, 'extras': False}

    # Default: match request scope
    if "analysis" in user_request.lower():
        return {'excel': True, 'analysis': True}

    return {'excel': True}  # Conservative default
```

### Daily Application

**Before creating any output:**
1. Re-read user's exact request
2. List what they explicitly asked for
3. Create ONLY those items
4. If you want to add value → ASK first: "Would you like me to also create X?"

---

## 🎯 PRINCIPLE 10: Comprehensive Documentation Prevents Repeat Issues

### Current Implementation

#### ✅ ALREADY DONE:
- Created `MASTER_LEARNINGS_COMPREHENSIVE.md`
- Created `PRIORITIZATION_AGENT_LEARNINGS.md`
- Created `PRIORITIZATION_AGENT_PROMPT.md`
- Created `TRACKING_DATA_PARSING_LEARNINGS.md`
- Created `EOD_SYNC_TUESDAY_NOV_4_2025.md`

#### 🔧 DAILY HABIT TO ADD:

**When You Fix a Bug:**
```markdown
## BUG FIX LOG

**Date**: 2025-11-05
**Script**: [script_name.py]
**Bug**: [One-line description]
**Root Cause**: [Why it happened]
**Fix**: [What changed]
**Verification**: [How you confirmed it works]
**Learning**: [Principle to prevent recurrence]
**Reference**: [Link to MASTER_LEARNINGS section]
```

**Where to Log:**
- Quick fixes → Add to `_DAILY_LOG_FEEDBACK.md`
- Major fixes → Create dedicated learning document
- Pattern fixes → Update `MASTER_LEARNINGS_COMPREHENSIVE.md`

---

## 📋 DAILY WORKFLOW ENHANCEMENTS

### Morning 9AM Sync (ENHANCED)

**Current Process:**
```bash
python daily_9am_sync.py
python .claude/agents/prioritization_agent.py --daily-reminder
```

**✅ ADD Evidence Checks:**
```bash
# 1. Run sync
python daily_9am_sync.py

# 2. Verify output quality
echo "Verification checks:"
grep -c "HubSpot" ~/Downloads/_DAILY_LOG.md  # Should show API was called
grep -c "Priority" ~/Downloads/_DAILY_LOG.md  # Should show priorities loaded

# 3. Run prioritization with v2.0 API version
python .claude/agents/prioritization_agent.py --daily-reminder

# 4. Verify deal count matches HubSpot
# (Open HubSpot and manually verify top 3 deals exist)
```

### Noon Sync (ENHANCED)

**Current Process:**
```bash
python noon_sync.py
```

**✅ ADD Quality Gates:**
```python
# At end of noon_sync.py, add:
print("\n" + "="*80)
print("🔍 QUALITY VERIFICATION")
print("="*80)
print(f"Expected deals in priority stages: [estimate]")
print(f"Actually fetched: {len(deals)}")
print(f"API response time: {response.elapsed.total_seconds():.2f}s")

if len(deals) == 0:
    print("🚨 WARNING: 0 deals returned - investigate!")
    print("   Check: HubSpot API key valid?")
    print("   Check: Owner ID correct?")
    print("   Check: Active stages filter correct?")
```

### EOD Sync (ENHANCED)

**Current Process:**
- Manual EOD logging in `_DAILY_LOG.md`

**✅ ADD Count Verification:**
```markdown
## [DATE] EOD SUMMARY

**Activity Count Verification:**
- Customer emails sent: 12 (verified in Superhuman)
- Customer responses received: 8 (verified in Superhuman)
- HubSpot deals worked: 6 (verified in HubSpot activity)
- Pipeline movements: 2 (verified with evidence quotes below)
- New leads created: 1 (verified folder exists + HubSpot record)

**Match Status**: ✅ All counts verified with evidence
```

---

## 🛠️ SCRIPT AUDIT CHECKLIST

Use this when creating or reviewing ANY Python script:

### Data Source
- [ ] Uses HubSpot API as primary source (not folders)
- [ ] Falls back gracefully if API unavailable
- [ ] Documented in code why folders are used (if applicable)

### Error Handling
- [ ] All HubSpot API calls have try/except
- [ ] Null values handled with .get() and defaults
- [ ] Type conversions wrapped in try/except
- [ ] Encoding errors handled (encoding='utf-8', errors='ignore')

### Regex Patterns
- [ ] Tested on 3-5 sample strings before deployment
- [ ] Uses raw strings correctly (single backslash in \d, \w, etc.)
- [ ] Edge cases covered (shortest/longest names, special chars)
- [ ] Debug output shows what matched/didn't match

### File Operations
- [ ] Uses glob patterns instead of hardcoded filenames
- [ ] Skips system folders (_*, .*, node_modules, etc.)
- [ ] Checks if files exist before reading
- [ ] Absolute paths used (not relative)

### Validation
- [ ] Count verification: expected == actual (MANDATORY)
- [ ] File size check: output >1KB minimum
- [ ] Data quality checks: required fields filled
- [ ] Evidence logged: what was found and verified

### Documentation
- [ ] Docstring explains purpose and usage
- [ ] Comments explain WHY not just WHAT
- [ ] Example usage in header or README
- [ ] Linked to relevant MASTER_LEARNINGS section

---

## 🚀 QUICK WIN IMPROVEMENTS (Do This Week)

### 1. Add Verification to Existing Scripts (2 hours)

**Priority Order:**
1. `noon_sync.py` - Add deal count verification
2. `daily_9am_sync.py` - Add HubSpot API call verification
3. `pipeline_sync_verification.py` - Query HubSpot first, then folders

### 2. Create Script Template (30 min)

**File**: `.claude/templates/python_script_template.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[SCRIPT NAME] - [One-line purpose]

Purpose: [Detailed description]
Usage: python script_name.py [args]
Output: [What files/reports are created]

Reference: See .claude/MASTER_LEARNINGS_COMPREHENSIVE.md
"""

import sys, io, os
from pathlib import Path
from dotenv import load_dotenv
import requests

# UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

# Configuration (from environment)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    sys.exit(1)

OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

def main():
    """Main execution with error handling"""
    try:
        # Step 1: Fetch data (HubSpot API first!)
        data = fetch_data_from_hubspot()

        # Step 2: Process data
        results = process_data(data)

        # Step 3: Generate output
        output_file = generate_output(results)

        # Step 4: MANDATORY VERIFICATION
        verify_results(
            expected_count=len(data),
            actual_count=len(results),
            output_file=output_file
        )

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def fetch_data_from_hubspot():
    """Query HubSpot API for deal data"""
    # Implementation here
    pass

def process_data(data):
    """Transform data with null handling"""
    results = []
    for item in data:
        # Use .get() with defaults
        name = item.get('name', 'Unknown')
        value = item.get('value', 0)
        # Handle type conversions safely
        try:
            amount = int(float(value)) if value else 0
        except (ValueError, TypeError):
            amount = 0
        results.append({'name': name, 'amount': amount})
    return results

def generate_output(results):
    """Create output file"""
    # Implementation here
    pass

def verify_results(expected_count, actual_count, output_file):
    """Evidence-based verification (MANDATORY)"""
    print(f"\n{'='*60}")
    print("VERIFICATION REPORT")
    print(f"{'='*60}")
    print(f"Expected: {expected_count} items")
    print(f"Actual: {actual_count} items")
    print(f"Match: {'✅ YES' if expected_count == actual_count else '❌ NO'}")

    if output_file and output_file.exists():
        size = output_file.stat().st_size
        print(f"Output: {output_file} ({size:,} bytes)")

    print(f"{'='*60}\n")

    if expected_count != actual_count:
        print("🚨 Count mismatch - investigate before using output!")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

### 3. Add EOD Verification Checklist (15 min)

**File**: `_EOD_VERIFICATION_CHECKLIST.md` (keep in Downloads for easy access)

```markdown
# EOD Sync Verification Checklist

Date: _________

## File Creation
- [ ] _DAILY_LOG.md updated (check timestamp)
- [ ] FOLLOW_UP_REMINDERS.txt has tomorrow's date
- [ ] File sizes >5KB (comprehensive data)

## Data Quality
- [ ] Today's date appears 3+ times (header, entries, summary)
- [ ] Customer email count matches Superhuman (sent: ___, received: ___)
- [ ] Pipeline movements have evidence quotes
- [ ] All urgent actions have Who/What/When/Why
- [ ] HubSpot API queried (or fallback noted)

## Verification Evidence
- [ ] Spot-checked 3 random entries for accuracy
- [ ] Cross-referenced with HubSpot activity
- [ ] Confirmed meeting times are correct
- [ ] Verified customer names spelled correctly

## Status
✅ All checks passed - EOD complete
❌ Issues found - logged in _DAILY_LOG_FEEDBACK.md
```

---

## 💾 BACKUP & RECOVERY

### Daily Learnings Backup

**Add to Friday EOD Workflow:**
```bash
# Backup all learnings to dated archive
cp ~/Downloads/_DAILY_LOG_FEEDBACK.md \
   ~/Downloads/ARCHIVES/DAILY_LOG_FEEDBACK_2025_WK_$(date +%U).md

cp .claude/MASTER_LEARNINGS_COMPREHENSIVE.md \
   ~/Downloads/ARCHIVES/MASTER_LEARNINGS_$(date +%Y%m%d).md
```

---

## 📊 MEASURE SUCCESS

### Weekly Learning Metrics (Track in Friday EOD)

```markdown
## LEARNING VELOCITY METRICS

**This Week:**
- Bugs fixed: [count]
- New learnings documented: [count]
- Scripts audited for compliance: [count]
- Verification steps added: [count]
- Count mismatches caught: [count]

**Quality Indicators:**
- % of scripts with verification: [%]
- % of outputs validated: [%]
- Avg time to fix issues: [hours]
- Repeat bugs: [count] (target: 0)
```

---

## 🎯 30-DAY IMPROVEMENT PLAN

### Week 1: Foundation (Nov 5-11)
- [ ] Audit all scripts using checklist above
- [ ] Add verification to noon_sync.py and daily_9am_sync.py
- [ ] Create Python script template
- [ ] Add EOD verification checklist

### Week 2: Enhancement (Nov 12-18)
- [ ] Update 3 customer analysis scripts with count verification
- [ ] Test all regex patterns with sample data
- [ ] Document common pitfalls in MASTER_LEARNINGS
- [ ] Create quick reference guide for team

### Week 3: Optimization (Nov 19-25)
- [ ] Refactor folder-based scripts to use HubSpot API
- [ ] Implement evidence-based validation across all scripts
- [ ] Create automated testing for critical workflows
- [ ] Update documentation with examples

### Week 4: Validation (Nov 26-Dec 2)
- [ ] Run full week without count mismatches
- [ ] Zero repeat bugs from previous weeks
- [ ] Team can use templates successfully
- [ ] Learning capture rate >90%

---

## ✅ IMPLEMENTATION CHECKLIST

Copy this to your weekly review:

```markdown
## LEARNINGS APPLIED THIS WEEK

**HubSpot API as Source of Truth:**
- [ ] All new scripts query HubSpot first
- [ ] Folder parsing deprecated where possible
- [ ] Documentation updated

**Complete Discovery:**
- [ ] Systematic search before refactoring
- [ ] All references documented
- [ ] Change plan created and followed

**Validation & Verification:**
- [ ] All outputs have count verification
- [ ] Evidence-based validation added
- [ ] Quality gates enforced

**Error Handling:**
- [ ] Null values handled gracefully
- [ ] Type conversions protected with try/except
- [ ] Regex patterns tested before deployment

**Documentation:**
- [ ] Bugs logged with root cause
- [ ] Learnings added to master doc
- [ ] Scripts have usage examples
```

---

**Last Updated**: November 5, 2025
**Status**: Production Guide
**Next Review**: December 5, 2025 (1 month validation)
