# Security Migration Guide - FirstMile Deals System

**Created**: 2025-10-10
**Status**: Phase 1 Complete - Phase 2 Pending

---

## Overview

This guide provides step-by-step instructions for migrating the FirstMile Deals codebase from hardcoded API keys to secure environment-based configuration.

---

## Phase 1: Foundation (✅ COMPLETE)

### Files Created

| File | Purpose | Status |
|------|---------|--------|
| `config.py` | Centralized configuration management | ✅ Complete |
| `hubspot_utils.py` | Shared HubSpot API client with security | ✅ Complete |
| `date_utils.py` | Shared date/time utilities | ✅ Complete |
| `.gitignore` | Security exclusions | ✅ Complete |
| `requirements.txt` | Dependency management | ✅ Complete |
| `SECURITY.md` | Security documentation | ✅ Complete |
| `9am_sync_secure.py` | Secure example script | ✅ Complete |

### Setup Instructions

**1. Install Dependencies**:
```bash
pip install python-dotenv
# OR install all dependencies
pip install -r requirements.txt
```

**2. Create `.env` File**:
```bash
# Copy example template
cp .env.example .env

# Edit .env with actual credentials
# File is already in .gitignore - safe to edit
```

**3. Test Secure Configuration**:
```bash
# Run secure version of 9AM sync
python 9am_sync_secure.py

# Should see: "✅ API credentials loaded from environment"
```

---

## Phase 2: Script Migration (⚠️ IN PROGRESS)

### Priority 1: Daily Operations (IMMEDIATE)

**Critical Scripts** (use daily, high visibility):

1. ✅ `9am_sync.py` → `9am_sync_secure.py` (EXAMPLE COMPLETE)
2. ⏳ `check_priority_deals.py` (NEXT)
3. ⏳ `get_pipeline_stages.py`
4. ⏳ `pipeline_sync_verification.py`
5. ⏳ `hubspot_pipeline_verify.py`

**Migration Steps**:

```python
# BEFORE (Insecure):
API_KEY = '${HUBSPOT_API_KEY}'
OWNER_ID = '699257003'
PIPELINE_ID = '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

STAGE_MAP = {
    '1090865183': '[01-DISCOVERY-SCHEDULED]',
    # ... 7 more stages
}

def days_since(date_str):
    # 10 lines of duplicate code
    pass

# AFTER (Secure):
from config import Config
from hubspot_utils import HubSpotClient, days_since
from date_utils import days_since  # Alternative if only need date utils

try:
    client = HubSpotClient()
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    print("See .env.example for template")
    return

# Use client methods
deals = client.search_deals(filters, properties)

# Use Config for constants
stage_name = Config.get_stage_name(stage_id)
stage_id = Config.get_stage_id('[03-RATE-CREATION]')
```

### Priority 2: Deal Management (THIS WEEK)

**Deal-Specific Scripts**:

6. ⏳ `create_boxiiship_winback_deal.py`
7. ⏳ `fix_boxiiship_correct_structure.py`
8. ⏳ `update_team_shipper.py`
9. ⏳ `create_boxiiship_tasks.py`
10. ⏳ `[CUSTOMER]_Driftaway_Coffee/update_hubspot_winback.py`
11. ⏳ `[CUSTOMER]_Driftaway_Coffee/update_hubspot_winback_v2.py`
12. ⏳ `[CUSTOMER]_BoxiiShip System Beauty TX/update_meeting_notes.py`

### Priority 3: Customer Folders (THIS MONTH)

**Customer-Specific HubSpot Integration**:

- ⏳ `[07-CLOSED-WON]_JM_Group_NY/hubspot_upload.py`
- ⏳ `[07-CLOSED-WON]_JM_Group_NY/hubspot_config.py`
- ⏳ All other customer folders with HubSpot scripts

**Note**: These are lower priority as they're used less frequently.

---

## Migration Template

### Step-by-Step Migration Process

**1. Backup Original Script**:
```bash
# Keep original for reference
cp original_script.py original_script_OLD.py
```

**2. Update Imports**:
```python
# Add at top of file (after standard library imports)
from config import Config
from hubspot_utils import HubSpotClient
from date_utils import days_since  # If using date utilities
```

**3. Replace Hardcoded Config**:
```python
# REMOVE these lines:
# API_KEY = 'pat-na1-...'
# OWNER_ID = '699257003'
# PIPELINE_ID = '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'

# REMOVE stage mapping:
# STAGE_MAP = {...}

# ADD client initialization:
try:
    client = HubSpotClient()
except ValueError as e:
    print(f"❌ Configuration Error: {e}")
    print("Please ensure .env file exists with HUBSPOT_API_KEY")
    print("See .env.example for template")
    return  # or sys.exit(1)
```

**4. Replace API Calls**:
```python
# BEFORE:
headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
response = requests.post('https://api.hubapi.com/crm/v3/objects/deals/search',
                        headers=headers, json=payload)

# AFTER:
result = client.search_deals(filters, properties, limit=100)
deals = result.get('results', [])
```

**5. Replace Utility Functions**:
```python
# BEFORE:
def days_since(date_str):
    if not date_str:
        return 999
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now(date.tzinfo) - date).days
    except:
        return 999

# AFTER:
from date_utils import days_since  # Just import, function already exists
```

**6. Replace Stage Lookups**:
```python
# BEFORE:
STAGE_MAP = {'1090865183': '[01-DISCOVERY-SCHEDULED]', ...}
stage_name = STAGE_MAP.get(stage_id)

# AFTER:
from config import Config
stage_name = Config.get_stage_name(stage_id)
stage_id = Config.get_stage_id('[03-RATE-CREATION]')
```

**7. Test Script**:
```bash
# Run migrated script
python migrated_script.py

# Verify:
# - ✅ Loads credentials from .env
# - ✅ API calls succeed
# - ✅ Output matches original script
# - ✅ No errors related to missing API_KEY
```

**8. Replace Original** (only after testing):
```bash
# After thorough testing
mv original_script.py original_script_BACKUP.py
mv migrated_script.py original_script.py

# Or use the secure version naming
# Keep both: original_script.py (old) and original_script_secure.py (new)
```

---

## Common Patterns Reference

### Pattern 1: Simple Deal Search

```python
# OLD
headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
payload = {
    'filterGroups': [{'filters': filters}],
    'properties': properties,
    'limit': 100
}
response = requests.post('https://api.hubapi.com/crm/v3/objects/deals/search',
                        headers=headers, json=payload)
deals = response.json().get('results', [])

# NEW
client = HubSpotClient()
result = client.search_deals(filters, properties, limit=100)
deals = result.get('results', [])
```

### Pattern 2: Deal Update

```python
# OLD
headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
payload = {'properties': {'dealstage': new_stage_id}}
response = requests.patch(f'https://api.hubapi.com/crm/v3/objects/deals/{deal_id}',
                         headers=headers, json=payload)

# NEW
client = HubSpotClient()
updated_deal = client.update_deal(deal_id, {'dealstage': new_stage_id})
```

### Pattern 3: Create Note

```python
# OLD
import time
timestamp_ms = int(time.time() * 1000)
headers = {'Authorization': f'Bearer {API_KEY}', 'Content-Type': 'application/json'}
payload = {
    'properties': {
        'hs_timestamp': timestamp_ms,
        'hs_note_body': note_text,
        'hubspot_owner_id': OWNER_ID
    },
    'associations': [...]
}
response = requests.post('https://api.hubapi.com/crm/v3/objects/notes',
                        headers=headers, json=payload)

# NEW
client = HubSpotClient()
note = client.create_note(deal_id, note_text)  # timestamp automatic
```

### Pattern 4: Date Calculations

```python
# OLD
def days_since(date_str):
    if not date_str:
        return 999
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now(date.tzinfo) - date).days
    except:
        return 999

# NEW
from date_utils import days_since  # Just import
```

---

## Testing Checklist

For each migrated script:

- [ ] Script runs without errors
- [ ] `.env` file is loaded correctly
- [ ] API calls succeed (check HubSpot)
- [ ] Output matches original script
- [ ] Error handling works (test with missing `.env`)
- [ ] No hardcoded API keys remain in file
- [ ] Stage mappings work correctly
- [ ] Date calculations match original
- [ ] No regression in functionality

---

## Rollback Procedure

If migration causes issues:

**1. Immediate Rollback**:
```bash
# Restore backup
cp original_script_BACKUP.py original_script.py
```

**2. Document Issue**:
- What broke?
- Error message?
- Expected vs actual behavior?

**3. Fix and Re-test**:
- Address specific issue
- Test thoroughly
- Retry migration

---

## Post-Migration Tasks

### After All Scripts Migrated

**1. Rotate API Key** (CRITICAL):
```
HubSpot → Settings → Integrations → Private Apps
→ "FirstMile Deals API" → Regenerate Token
→ Update .env file
```

**2. Archive Old Scripts**:
```bash
mkdir _archive_OLD_INSECURE_SCRIPTS
mv *_OLD.py _archive_OLD_INSECURE_SCRIPTS/
mv *_BACKUP.py _archive_OLD_INSECURE_SCRIPTS/
```

**3. Update Documentation**:
- Update README.md with security improvements
- Note migration completion date in SECURITY.md
- Add to CHANGELOG

**4. Security Audit**:
```bash
# Search for any remaining hardcoded keys
grep -r "pat-na1-" *.py

# Should return no results (except .env.example)
```

---

## Migration Progress Tracker

| Category | Total | Migrated | Remaining | % Complete |
|----------|-------|----------|-----------|------------|
| **Priority 1: Daily Ops** | 5 | 1 | 4 | 20% |
| **Priority 2: Deal Mgmt** | 7 | 0 | 7 | 0% |
| **Priority 3: Customer** | 14 | 0 | 14 | 0% |
| **TOTAL** | 26 | 1 | 25 | 4% |

**Last Updated**: 2025-10-10 12:25 PM

---

## Questions or Issues?

**Common Problems**:

Q: "Script says 'HUBSPOT_API_KEY is not set'"
A: Create `.env` file from `.env.example` template

Q: "Import error: No module named 'config'"
A: Run `pip install python-dotenv` and ensure script is in project root

Q: "API calls fail with 401 Unauthorized"
A: Check `.env` file has correct API key (starts with `pat-na1-`)

Q: "Stage mapping returns None"
A: Verify stage IDs match Config.STAGE_MAP (corrected 2025-10-10)

---

**Next Steps**: Begin Priority 1 migrations (check_priority_deals.py next)
