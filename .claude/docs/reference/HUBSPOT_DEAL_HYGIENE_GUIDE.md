# HubSpot Deal Hygiene & Sync System Guide

Comprehensive reference for FirstMile deal management automation based on production implementation learnings.

---

## Critical API Rules

### Authentication
```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
```

**Never**: Hardcode API keys in scripts

### Required Filters for Brett Walker's Deals

**Always include these filters** to avoid pulling 3,000+ deals from entire CRM:

```python
OWNER_ID = "699257003"  # Brett Walker
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"  # FM BW clone

payload = {
    "filterGroups": [{
        "filters": [
            {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
            {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID}
        ]
    }],
    "properties": [...],
    "limit": 100
}
```

**Result**: Returns ~40 active deals instead of 3,246

---

## Read-Only Fields (Cannot Set Directly)

### `notes_next_activity_date`
- **Error**: `"notes_next_activity_date" is a read only property; its value cannot be set`
- **Solution**: Create a task with due date instead - HubSpot auto-calculates this field from associated tasks

```python
def create_task_for_deal(deal_id, subject, due_date):
    """Create task to populate notes_next_activity_date"""
    due_timestamp = int(due_date.timestamp() * 1000)

    task_data = {
        "properties": {
            "hs_task_subject": subject,
            "hs_task_body": "Auto-created follow-up task",
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": "MEDIUM",
            "hs_timestamp": str(due_timestamp),
            "hubspot_owner_id": OWNER_ID,
            "hs_task_type": "TODO"
        },
        "associations": [{
            "to": {"id": deal_id},
            "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 216}]
        }]
    }

    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/tasks",
        headers=headers,
        json=task_data,
        timeout=10
    )
    return response.status_code == 201
```

---

## Timestamp Formats

### Dates (closedate, hs_timestamp)
**Format**: Unix milliseconds as STRING

```python
from datetime import datetime

# Correct
timestamp_ms = int(datetime.now().timestamp() * 1000)
properties["closedate"] = str(timestamp_ms)  # "1738281600000"

# Wrong - ISO strings don't work
properties["closedate"] = "2025-01-31"  # FAILS
```

### Common Date Conversions
```python
# January 31, 2025 in Unix ms
"1738281600000"

# Calculate from datetime
target_date = datetime(2025, 1, 31)
unix_ms = str(int(target_date.timestamp() * 1000))
```

---

## Association Type IDs

| Type | ID | Usage |
|------|-----|-------|
| Note → Deal | 214 | `create_hubspot_note()` |
| Task → Deal | 216 | `create_task_for_deal()` |
| Contact → Company | 280 | Lead creation |
| Deal → Company | 341 | Deal association |

---

## Custom Field Names

HubSpot custom properties use `__c` suffix. Common fields:

| UI Label | API Property Name | Type |
|----------|-------------------|------|
| Monthly Volume | `monthly_volume__c` | number |
| Returns per Month Volume | `returns_per_month_volume__c` | number |

**Important**: Don't guess field names. Query `/crm/v3/properties/deals` to find exact names:

```python
response = requests.get(
    'https://api.hubapi.com/crm/v3/properties/deals',
    headers=headers
)
for p in response.json().get('results', []):
    if 'volume' in p.get('label', '').lower():
        print(f"{p['name']} | {p['label']}")
```

```python
"associations": [{
    "to": {"id": deal_id},
    "types": [{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 216  # Task-Deal
    }]
}]
```

---

## Stage Configuration

### Pipeline Stage IDs and Follow-Up Logic

```python
STAGE_CONFIG = {
    "1090865183": {
        "name": "[01-DISCOVERY-SCHEDULED]",
        "next_step": "Conduct discovery call - understand volume, pain points, timeline",
        "days_out": 3
    },
    "d2a08d6f-cc04-4423-9215-594fe682e538": {
        "name": "[02-DISCOVERY-COMPLETE]",
        "next_step": "Create custom rate card based on discovery insights",
        "days_out": 5
    },
    "e1c4321e-afb6-4b29-97d4-2b2425488535": {
        "name": "[03-RATE-CREATION]",
        "next_step": "Finalize rates and prepare proposal presentation",
        "days_out": 3
    },
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": {
        "name": "[04-PROPOSAL-SENT]",
        "next_step": "Follow up on proposal - address questions, negotiate terms",
        "days_out": 5
    },
    "4e549d01-674b-4b31-8a90-91ec03122715": {
        "name": "[05-SETUP-DOCS-SENT]",
        "next_step": "Confirm setup docs received - assist with completion",
        "days_out": 3
    },
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": {
        "name": "[06-IMPLEMENTATION]",
        "next_step": "Monitor implementation progress - resolve blockers",
        "days_out": 7
    },
    "3fd46d94-78b4-452b-8704-62a338a210fb": {
        "name": "[07-STARTED-SHIPPING]",
        "next_step": "QBR check-in - review performance, identify growth opportunities",
        "days_out": 30
    }
}
```

---

## Required Deal Fields for Completeness

```python
REQUIRED_DEAL_FIELDS = [
    "dealname",
    "dealstage",
    "amount",
    "closedate",
    "hs_next_step",
    "notes_next_activity_date",  # Populated by tasks, not directly
    "description"
]
```

### Audit Function Pattern

```python
def audit_deal_completeness():
    """Audit all deals for missing required fields"""
    deals = fetch_all_deals()

    complete = 0
    incomplete = 0
    missing_fields = {}
    deals_needing_attention = []

    for deal in deals:
        props = deal.get("properties", {})
        missing = []

        for field in REQUIRED_DEAL_FIELDS:
            value = props.get(field)
            if not value or value == "0":
                missing.append(field)
                missing_fields[field] = missing_fields.get(field, 0) + 1

        if missing:
            incomplete += 1
            deals_needing_attention.append({
                "name": props.get("dealname"),
                "stage": props.get("dealstage"),
                "missing": missing
            })
        else:
            complete += 1

    return {
        "total": len(deals),
        "complete": complete,
        "incomplete": incomplete,
        "missing_fields": missing_fields,
        "deals_needing_attention": deals_needing_attention
    }
```

---

## Windows Console Encoding Fix

**Problem**: Emojis fail with `UnicodeEncodeError: 'charmap' codec can't encode character`

**Solution**: Add UTF-8 wrapper to ALL scripts:

```python
import sys
import io

# Fix Windows console encoding - ADD THIS AT TOP OF EVERY SCRIPT
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

**Subprocess calls**:
```python
result = subprocess.run(
    ['python', 'script.py'],
    capture_output=True,
    encoding='utf-8',  # NOT text=True (uses cp1252)
    timeout=30
)
```

---

## Bulk Update Pattern

### Safe Update with Error Handling

```python
def update_deal(deal_id, properties):
    """Update a single deal in HubSpot"""
    try:
        response = requests.patch(
            f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}",
            headers=headers,
            json={"properties": properties},
            timeout=10
        )

        if response.status_code != 200:
            print(f"API Error: {response.text[:100]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False
```

### Skip Weekend Due Dates

```python
from datetime import datetime, timedelta

def calculate_due_date(days_out):
    """Calculate due date, skipping weekends"""
    next_date = datetime.now() + timedelta(days=days_out)
    while next_date.weekday() >= 5:  # Saturday=5, Sunday=6
        next_date += timedelta(days=1)
    return next_date
```

---

## Common Mistakes to Avoid

### 1. Wrong Deal IDs
- **Problem**: Using example IDs or wrong format
- **Solution**: Always fetch deal IDs via search API first

### 2. Setting Read-Only Fields
- **Problem**: Trying to set `notes_next_activity_date` directly
- **Solution**: Create tasks instead - HubSpot auto-calculates

### 3. Wrong Timestamp Format
- **Problem**: Using ISO strings like "2025-01-31"
- **Solution**: Use Unix milliseconds as string: "1738281600000"

### 4. Missing Owner/Pipeline Filters
- **Problem**: Pulling all 3,000+ CRM deals
- **Solution**: Always filter by `hubspot_owner_id` and `pipeline`

### 5. Encoding Errors on Windows
- **Problem**: Emojis crash scripts
- **Solution**: UTF-8 wrapper at script start

### 6. Division by Zero
- **Problem**: Calculating percentages when count is 0
- **Solution**: Always check denominator
```python
pct = (count / total * 100) if total > 0 else 0
```

---

## Sync System Architecture

### Entry Point
```bash
python unified_sync.py [9am|noon|3pm|eod|weekly|monthly]
```

### Integration Features
1. **Task Management**: Fetch, create, track overdue tasks
2. **Notes**: Log activities and sync notes to deals
3. **Next Steps**: Auto-populate based on deal stage
4. **Audit**: Track record completeness with actionable reports

### Report Output
- Location: `sync_reports/SYNCTYPE_YYYYMMDD_HHMMSS.md`
- Continuity: `_DAILY_LOG.md` updated each sync
- Actions: `FOLLOW_UP_REMINDERS.txt` for queue

---

## Quick Reference Commands

```bash
# Run weekly sync with full audit
python unified_sync.py weekly

# Preview bulk hygiene updates
python bulk_update_deal_hygiene.py --dry-run

# Execute bulk updates
python bulk_update_deal_hygiene.py

# Check specific deal
python -c "
import os, requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')
headers = {'Authorization': f'Bearer {API_KEY}'}
r = requests.get(f'https://api.hubapi.com/crm/v3/objects/deals/DEAL_ID', headers=headers)
print(r.json())
"
```

---

## Success Metrics

After implementing this system:
- **Before**: 0% complete records (0/40)
- **After**: 100% complete records (40/40)
- **Tasks Created**: 100 with stage-appropriate due dates
- **Pipeline Visibility**: Full next steps and follow-up dates

---

*Generated from production implementation - November 22, 2025*
*System: Nebuchadnezzar v3.0*
