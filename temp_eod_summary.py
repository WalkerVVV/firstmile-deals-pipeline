#!/usr/bin/env python3
"""
EOD Summary Generator for Nebuchadnezzar System
Generates comprehensive end-of-day summary with tomorrow's priorities
"""

from hubspot_config import get_hubspot_config, STAGE_MAPPING
import requests
from datetime import datetime, timedelta
import os

config = get_hubspot_config()
headers = {
    'Authorization': f'Bearer {config["API_KEY"]}',
    'Content-Type': 'application/json'
}

print("=" * 80)
print("NEBUCHADNEZZAR END OF DAY WRAP")
print("=" * 80)
print(f"Date: {datetime.now().strftime('%A, %B %d, %Y')}")
print(f"Time: {datetime.now().strftime('%I:%M %p')}")
print(f"Owner: Brett Walker (ID: {config['OWNER_ID']})")
print(f"Pipeline: {config['PIPELINE_ID']}")
print("=" * 80)
print()

# ============================================================================
# PHASE 1: TODAY'S ACTIVITY
# ============================================================================
print("PHASE 1: TODAY'S SUMMARY")
print("-" * 80)

# Get today's start timestamp (midnight)
today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000

# Query deals modified today
search_payload = {
    'filterGroups': [{
        'filters': [
            {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': config['OWNER_ID']},
            {'propertyName': 'pipeline', 'operator': 'EQ', 'value': config['PIPELINE_ID']},
            {'propertyName': 'hs_lastmodifieddate', 'operator': 'GTE', 'value': int(today_start)}
        ]
    }],
    'properties': ['dealname', 'dealstage', 'amount', 'closedate', 'hs_lastmodifieddate',
                   'createdate', 'notes_last_updated'],
    'limit': 100
}

response = requests.post(
    f'{config["BASE_URL"]}/crm/v3/objects/deals/search',
    headers=headers,
    json=search_payload
)

deals_modified_today = response.json().get('results', [])
print(f"DEALS MODIFIED TODAY: {len(deals_modified_today)}")
print()

if deals_modified_today:
    # Group by stage
    by_stage = {}
    for deal in deals_modified_today:
        stage_id = deal['properties']['dealstage']
        stage_name = STAGE_MAPPING.get(stage_id, f"Unknown ({stage_id})")
        if stage_name not in by_stage:
            by_stage[stage_name] = []
        by_stage[stage_name].append(deal)

    for stage_name in sorted(by_stage.keys()):
        print(f"\n{stage_name}:")
        for deal in by_stage[stage_name]:
            deal_name = deal['properties']['dealname']
            deal_amount = deal['properties'].get('amount', '0')
            create_date = deal['properties'].get('createdate', '')

            # Check if created today
            if create_date:
                try:
                    # Try parsing as ISO timestamp
                    create_dt = datetime.fromisoformat(create_date.replace('Z', '+00:00'))
                    if create_dt.date() == datetime.now().date():
                        print(f"  [NEW] {deal_name} - ${int(float(deal_amount)):,}")
                    else:
                        print(f"  [UPDATED] {deal_name} - ${int(float(deal_amount)):,}")
                except:
                    # Try as millisecond timestamp
                    try:
                        create_ts = int(create_date) / 1000
                        create_dt = datetime.fromtimestamp(create_ts)
                        if create_dt.date() == datetime.now().date():
                            print(f"  [NEW] {deal_name} - ${int(float(deal_amount)):,}")
                        else:
                            print(f"  [UPDATED] {deal_name} - ${int(float(deal_amount)):,}")
                    except:
                        print(f"  [UPDATED] {deal_name} - ${int(float(deal_amount)):,}")
            else:
                print(f"  [UPDATED] {deal_name} - ${int(float(deal_amount)):,}")
else:
    print("No deals modified today.")

print()

# ============================================================================
# PHASE 2: PIPELINE HEALTH SNAPSHOT
# ============================================================================
print("\nPHASE 2: PIPELINE HEALTH SNAPSHOT")
print("-" * 80)

# Get all active deals
all_deals_payload = {
    'filterGroups': [{
        'filters': [
            {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': config['OWNER_ID']},
            {'propertyName': 'pipeline', 'operator': 'EQ', 'value': config['PIPELINE_ID']},
            {'propertyName': 'dealstage', 'operator': 'NEQ', 'value': '3fd46d94-78b4-452b-8704-62a338a210fb'},  # Not Closed Won
            {'propertyName': 'dealstage', 'operator': 'NEQ', 'value': '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8'}   # Not Closed Lost
        ]
    }],
    'properties': ['dealname', 'dealstage', 'amount', 'closedate'],
    'limit': 100
}

response = requests.post(
    f'{config["BASE_URL"]}/crm/v3/objects/deals/search',
    headers=headers,
    json=all_deals_payload
)

active_deals = response.json().get('results', [])
print(f"ACTIVE DEALS IN PIPELINE: {len(active_deals)}")
print()

# Pipeline by stage
pipeline_by_stage = {}
total_pipeline_value = 0

for deal in active_deals:
    stage_id = deal['properties']['dealstage']
    stage_name = STAGE_MAPPING.get(stage_id, f"Unknown ({stage_id})")
    amount = float(deal['properties'].get('amount', '0') or '0')

    if stage_name not in pipeline_by_stage:
        pipeline_by_stage[stage_name] = {'count': 0, 'value': 0}

    pipeline_by_stage[stage_name]['count'] += 1
    pipeline_by_stage[stage_name]['value'] += amount
    total_pipeline_value += amount

print("PIPELINE BY STAGE:")
for stage_name in sorted(pipeline_by_stage.keys()):
    count = pipeline_by_stage[stage_name]['count']
    value = pipeline_by_stage[stage_name]['value']
    print(f"  {stage_name}: {count} deals (${value:,.0f})")

print()
print(f"TOTAL PIPELINE VALUE: ${total_pipeline_value:,.0f}")
print()

# ============================================================================
# PHASE 3: TOMORROW'S PRIORITIES
# ============================================================================
print("\nPHASE 3: TOMORROW'S PRIORITIES")
print("-" * 80)

tomorrow = datetime.now() + timedelta(days=1)
tomorrow_date = tomorrow.strftime('%Y-%m-%d')

# Get tasks due tomorrow
tasks_payload = {
    'filterGroups': [{
        'filters': [
            {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': config['OWNER_ID']},
            {'propertyName': 'hs_task_status', 'operator': 'EQ', 'value': 'NOT_STARTED'},
            {'propertyName': 'hs_timestamp', 'operator': 'LTE', 'value': int(tomorrow.replace(hour=23, minute=59, second=59).timestamp() * 1000)}
        ]
    }],
    'properties': ['hs_task_subject', 'hs_task_body', 'hs_task_priority', 'hs_timestamp'],
    'limit': 100
}

response = requests.post(
    f'{config["BASE_URL"]}/crm/v3/objects/tasks/search',
    headers=headers,
    json=tasks_payload
)

tasks_due = response.json().get('results', [])
print(f"TASKS DUE TOMORROW OR OVERDUE: {len(tasks_due)}")

if tasks_due:
    # Sort by priority
    high_priority = [t for t in tasks_due if t['properties'].get('hs_task_priority') == 'HIGH']
    other_tasks = [t for t in tasks_due if t['properties'].get('hs_task_priority') != 'HIGH']

    if high_priority:
        print("\nHIGH PRIORITY:")
        for task in high_priority[:5]:
            subject = task['properties'].get('hs_task_subject', 'No subject')
            print(f"  - {subject}")

    if other_tasks:
        print("\nOTHER TASKS:")
        for task in other_tasks[:5]:
            subject = task['properties'].get('hs_task_subject', 'No subject')
            print(f"  - {subject}")

print()

# ============================================================================
# PHASE 4: KEY INSIGHTS
# ============================================================================
print("\nPHASE 4: KEY INSIGHTS")
print("-" * 80)

# New deals today
new_deals_today = []
for d in deals_modified_today:
    create_date = d['properties'].get('createdate', '')
    if create_date:
        try:
            create_dt = datetime.fromisoformat(create_date.replace('Z', '+00:00'))
            if create_dt.date() == datetime.now().date():
                new_deals_today.append(d)
        except:
            pass

if new_deals_today:
    print(f"NEW DEALS CREATED TODAY: {len(new_deals_today)}")
    for deal in new_deals_today:
        amount = int(float(deal['properties'].get('amount', '0') or '0'))
        print(f"  - {deal['properties']['dealname']} (${amount:,})")
else:
    print("NEW DEALS CREATED TODAY: 0")

print()

# Deals in Rate Creation (bottleneck stage)
rate_creation_deals = [d for d in active_deals if
                       d['properties']['dealstage'] == 'e1c4321e-afb6-4b29-97d4-2b2425488535']

if rate_creation_deals:
    print(f"DEALS IN RATE CREATION (BOTTLENECK): {len(rate_creation_deals)}")
    for deal in rate_creation_deals:
        print(f"  - {deal['properties']['dealname']}")
else:
    print("DEALS IN RATE CREATION: 0")

print()

# ============================================================================
# PHASE 5: TOMORROW'S OPENING CHECKLIST
# ============================================================================
print("\nPHASE 5: TOMORROW'S OPENING CHECKLIST (9AM SYNC)")
print("-" * 80)

print("\n1. LOAD THESE DEALS FIRST:")
if new_deals_today:
    print("   - Brand Scout v3.7 results (Phase 0.5):")
    for deal in new_deals_today:
        print(f"     - {deal['properties']['dealname']}")
else:
    print("   - No new Brand Scout deals to review")

if high_priority:
    print("\n2. HIGH PRIORITY TASKS:")
    for task in high_priority[:3]:
        print(f"   - {task['properties'].get('hs_task_subject', 'No subject')}")

if rate_creation_deals:
    print("\n3. RATE CREATION BOTTLENECK:")
    print("   - Review these deals for Jira ticket status:")
    for deal in rate_creation_deals[:3]:
        print(f"     - {deal['properties']['dealname']}")

print("\n4. EXPECTED START TIME: 9:00 AM")
print("5. ESTIMATED SYNC DURATION: 2 hours (9:00 AM - 11:00 AM)")
print()

# ============================================================================
# EOD COMPLETE
# ============================================================================
print("=" * 80)
print("EOD SYNC COMPLETE")
print("=" * 80)
print(f"Next sync: Tomorrow at 9:00 AM ({tomorrow.strftime('%A, %B %d, %Y')})")
print("System Status: [OK] Nebuchadnezzar v2.0 Active")
print("Context preserved for morning continuity")
print("=" * 80)
