#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEBUCHADNEZZAR v3.1.0 - NOON SYNC
Midday priority check and afternoon action planning
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment (SECURE)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)
OWNER_ID = '699257003'
PIPELINE_ID = '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

PRIORITY_STAGES = [
    'e1c4321e-afb6-4b29-97d4-2b2425488535',  # [03-RATE-CREATION]
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a',  # [04-PROPOSAL-SENT]
    '4e549d01-674b-4b31-8a90-91ec03122715',  # [05-SETUP-DOCS-SENT]
]

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

def days_since(date_str):
    if not date_str:
        return 999
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now(date.tzinfo) - date).days
    except:
        return 999

def main():
    print('=' * 80)
    print('NEBUCHADNEZZAR v3.1.0 - NOON SYNC')
    print('=' * 80)
    print(f'Timestamp: {datetime.now().strftime("%Y-%m-%d %I:%M %p")}')
    print(f'Owner: {OWNER_ID} | Pipeline: {PIPELINE_ID}')
    print()

    # Fetch priority deals
    payload = {
        'filterGroups': [{
            'filters': [
                {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': OWNER_ID},
                {'propertyName': 'pipeline', 'operator': 'EQ', 'value': PIPELINE_ID},
                {'propertyName': 'dealstage', 'operator': 'IN', 'values': PRIORITY_STAGES}
            ]
        }],
        'properties': ['dealname', 'dealstage', 'amount', 'createdate', 'notes_last_updated'],
        'limit': 50
    }

    print('🔄 Fetching afternoon priority deals...')
    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/deals/search',
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print(f'❌ Error: {response.status_code}')
        return

    deals = response.json().get('results', [])
    print(f'✅ Found {len(deals)} priority deals')
    print()

    # Analyze by stage
    stage_summary = {}
    urgent_items = []

    for deal in deals:
        props = deal.get('properties', {})
        stage_id = props.get('dealstage')
        stage_name = STAGE_MAP.get(stage_id, 'Unknown')

        if stage_name not in stage_summary:
            stage_summary[stage_name] = []

        age = days_since(props.get('createdate'))
        last_activity = days_since(props.get('notes_last_updated') or props.get('createdate'))

        deal_info = {
            'name': props.get('dealname', 'Unnamed'),
            'amount': float(props.get('amount', 0)),
            'age': age,
            'last_activity': last_activity
        }

        stage_summary[stage_name].append(deal_info)

        # Flag urgent items
        if stage_name == '[03-RATE-CREATION]' and age > 14:
            urgent_items.append(f"{deal_info['name']} - {age}d in Rate Creation")
        elif stage_name == '[04-PROPOSAL-SENT]' and age > 30:
            urgent_items.append(f"{deal_info['name']} - {age}d in Proposal Sent")
        elif last_activity > 14:
            urgent_items.append(f"{deal_info['name']} - {last_activity}d no activity")

    print('📊 AFTERNOON PRIORITY SUMMARY')
    print('─' * 80)

    for stage in ['[03-RATE-CREATION]', '[04-PROPOSAL-SENT]', '[05-SETUP-DOCS-SENT]']:
        deals_in_stage = stage_summary.get(stage, [])
        if deals_in_stage:
            print(f'\n{stage}: {len(deals_in_stage)} deals')
            for d in deals_in_stage[:3]:  # Show top 3
                amount_str = f"${d['amount']/1000:.0f}K" if d['amount'] else 'N/A'
                print(f"  • {d['name'][:40]:<40} | {d['age']:>3}d old | {amount_str:>8}")

    print()
    print('🚨 URGENT ITEMS FOR AFTERNOON')
    print('─' * 80)

    if urgent_items:
        for item in urgent_items[:5]:
            print(f'  ⚠️  {item}')
    else:
        print('  ✅ No urgent items - pipeline in good shape')

    print()
    print('📅 AFTERNOON PLAN')
    print('─' * 80)
    print('  1. Work through [03-RATE-CREATION] backlog (highest priority)')
    print('  2. Follow up on stale [04-PROPOSAL-SENT] deals')
    print('  3. Check for any new inbound leads or responses')
    print('  4. Update HubSpot tasks with progress')
    print('  5. Review priority deal progress from morning')
    print()

    print('=' * 80)
    print('🎯 SALES DISCIPLINE CHECK (Optional Mid-Day)')
    print('=' * 80)
    print('\nIf stale proposals need urgent attention, run:')
    print('  python .claude/agents/sales_execution_agent.py')
    print('\n💡 Best practice: Review morning priority progress before 3PM sync')
    print()

    print('=' * 80)
    print('NOON SYNC COMPLETE')
    print('Next Check: 3PM Sync (afternoon checkpoint)')
    print('=' * 80)

if __name__ == '__main__':
    main()
