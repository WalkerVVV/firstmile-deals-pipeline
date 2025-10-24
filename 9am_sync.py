#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEBUCHADNEZZAR v2.0 - 9AM Pipeline Sync
Daily morning synchronization for priority deals
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

# Configuration
API_KEY = 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'
OWNER_ID = '699257003'
PIPELINE_ID = '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'

# Stage mapping (VERIFIED 2025-10-10 from HubSpot API)
STAGE_MAP = {
    '1090865183': '[01-DISCOVERY-SCHEDULED]',
    'd2a08d6f-cc04-4423-9215-594fe682e538': '[02-DISCOVERY-COMPLETE]',
    'e1c4321e-afb6-4b29-97d4-2b2425488535': '[03-RATE-CREATION]',
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a': '[04-PROPOSAL-SENT]',
    '4e549d01-674b-4b31-8a90-91ec03122715': '[05-SETUP-DOCS-SENT]',
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307': '[06-IMPLEMENTATION]',
    '3fd46d94-78b4-452b-8704-62a338a210fb': '[07-STARTED-SHIPPING]',  # HubSpot label: "Started Shipping"
    '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8': '[08-CLOSED-LOST]'
}

# SLA windows (days)
SLA_WINDOWS = {
    '[01-DISCOVERY-SCHEDULED]': 30,
    '[02-DISCOVERY-COMPLETE]': 30,
    '[03-RATE-CREATION]': 14,  # Bottleneck stage
    '[04-PROPOSAL-SENT]': 30,
    '[05-SETUP-DOCS-SENT]': 14,
    '[06-IMPLEMENTATION]': 30
}

# Priority stages for sync (VERIFIED 2025-10-10)
PRIORITY_STAGES = [
    'e1c4321e-afb6-4b29-97d4-2b2425488535',  # [03-RATE-CREATION]
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a',  # [04-PROPOSAL-SENT]
    '4e549d01-674b-4b31-8a90-91ec03122715',  # [05-SETUP-DOCS-SENT]
    'd2a08d6f-cc04-4423-9215-594fe682e538',  # [02-DISCOVERY-COMPLETE]
    '1090865183'                              # [01-DISCOVERY-SCHEDULED]
]

def days_since(date_str):
    """Calculate days since date string"""
    if not date_str:
        return 999
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now(date.tzinfo) - date).days
    except:
        return 999

def main():
    print('=' * 80)
    print('NEBUCHADNEZZAR v2.0 - 9AM PIPELINE SYNC')
    print('=' * 80)
    print(f'Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Owner Lock: {OWNER_ID} ✓')
    print(f'Pipeline Lock: {PIPELINE_ID} ✓')
    print()

    # Fetch priority deals
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'filterGroups': [{
            'filters': [
                {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': OWNER_ID},
                {'propertyName': 'pipeline', 'operator': 'EQ', 'value': PIPELINE_ID},
                {'propertyName': 'dealstage', 'operator': 'IN', 'values': PRIORITY_STAGES}
            ]
        }],
        'properties': ['dealname', 'dealstage', 'amount', 'createdate', 'notes_last_updated', 'hs_lastmodifieddate'],
        'limit': 100
    }

    print('🔄 Fetching priority deals from HubSpot...')
    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/deals/search',
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print(f'❌ Error fetching deals: {response.status_code}')
        print(response.text)
        return

    results = response.json()
    deals = results.get('results', [])

    print(f'✓ Fetched {len(deals)} priority deals')
    print()

    # Organize by stage
    deals_by_stage = defaultdict(list)
    for deal in deals:
        stage_id = deal['properties'].get('dealstage')
        stage_name = STAGE_MAP.get(stage_id, 'UNKNOWN')
        deals_by_stage[stage_name].append(deal)

    print('=' * 80)
    print('PRIORITY STAGE ANALYSIS')
    print('=' * 80)
    print()

    priority_actions = []

    # [04-PROPOSAL-SENT] - Day 1/3/7/10/14 cadence
    if '[04-PROPOSAL-SENT]' in deals_by_stage:
        print(f'[04-PROPOSAL-SENT] ({len(deals_by_stage["[04-PROPOSAL-SENT]"])} deals)')
        print('-' * 80)
        for deal in deals_by_stage['[04-PROPOSAL-SENT]']:
            name = deal['properties'].get('dealname', 'Unnamed')
            created = deal['properties'].get('createdate')
            days = days_since(created)

            cadence_day = None
            if days == 1:
                cadence_day = 'DAY 1'
            elif days == 3:
                cadence_day = 'DAY 3'
            elif days == 7:
                cadence_day = 'DAY 7'
            elif days == 10:
                cadence_day = 'DAY 10'
            elif days == 14:
                cadence_day = 'DAY 14'
            elif days > 30:
                cadence_day = 'OVERDUE'

            status = f'{days}d in stage'
            if cadence_day:
                status += f' | {cadence_day} FOLLOW-UP DUE'
                priority_actions.append({
                    'deal': name,
                    'stage': '[04-PROPOSAL-SENT]',
                    'action': f'{cadence_day} follow-up',
                    'urgency': 95 if cadence_day == 'OVERDUE' else 85,
                    'days': days
                })

            print(f'  • {name} - {status}')
        print()

    # [03-RATE-CREATION] - 3-5 day SLA (BOTTLENECK STAGE)
    if '[03-RATE-CREATION]' in deals_by_stage:
        print(f'[03-RATE-CREATION] ({len(deals_by_stage["[03-RATE-CREATION]"])} deals) ⚠️  BOTTLENECK')
        print('-' * 80)
        for deal in deals_by_stage['[03-RATE-CREATION]']:
            name = deal['properties'].get('dealname', 'Unnamed')
            created = deal['properties'].get('createdate')
            days = days_since(created)

            sla_status = '✓ Within SLA' if days <= 14 else '⚠️  SLA VIOLATION'
            print(f'  • {name} - {days}d in stage {sla_status}')

            if days >= 5:
                priority_actions.append({
                    'deal': name,
                    'stage': '[03-RATE-CREATION]',
                    'action': 'Complete rate calculation and move to proposal',
                    'urgency': 90 if days > 14 else 75,
                    'days': days
                })
        print()

    # [05-SETUP-DOCS-SENT] - Contract acknowledgment
    if '[05-SETUP-DOCS-SENT]' in deals_by_stage:
        print(f'[05-SETUP-DOCS-SENT] ({len(deals_by_stage["[05-SETUP-DOCS-SENT]"])} deals)')
        print('-' * 80)
        for deal in deals_by_stage['[05-SETUP-DOCS-SENT]']:
            name = deal['properties'].get('dealname', 'Unnamed')
            created = deal['properties'].get('createdate')
            days = days_since(created)

            sla_status = '✓ Within SLA' if days <= 14 else '⚠️  SLA VIOLATION'
            print(f'  • {name} - {days}d in stage {sla_status}')

            if days >= 7:
                priority_actions.append({
                    'deal': name,
                    'stage': '[05-SETUP-DOCS-SENT]',
                    'action': 'Follow up on contract/setup acknowledgment',
                    'urgency': 85 if days > 14 else 70,
                    'days': days
                })
        print()

    # [02-DISCOVERY-COMPLETE] - Follow-up scheduling
    if '[02-DISCOVERY-COMPLETE]' in deals_by_stage:
        print(f'[02-DISCOVERY-COMPLETE] ({len(deals_by_stage["[02-DISCOVERY-COMPLETE]"])} deals)')
        print('-' * 80)
        for deal in deals_by_stage['[02-DISCOVERY-COMPLETE]']:
            name = deal['properties'].get('dealname', 'Unnamed')
            created = deal['properties'].get('createdate')
            days = days_since(created)

            sla_status = '✓ Within SLA' if days <= 30 else '⚠️  SLA VIOLATION'
            print(f'  • {name} - {days}d in stage {sla_status}')

            if days >= 14:
                priority_actions.append({
                    'deal': name,
                    'stage': '[02-DISCOVERY-COMPLETE]',
                    'action': 'Schedule rate creation follow-up',
                    'urgency': 70 if days > 30 else 60,
                    'days': days
                })
        print()

    # [01-DISCOVERY-SCHEDULED] - Meeting confirmations
    if '[01-DISCOVERY-SCHEDULED]' in deals_by_stage:
        print(f'[01-DISCOVERY-SCHEDULED] ({len(deals_by_stage["[01-DISCOVERY-SCHEDULED]"])} deals)')
        print('-' * 80)
        for deal in deals_by_stage['[01-DISCOVERY-SCHEDULED]']:
            name = deal['properties'].get('dealname', 'Unnamed')
            created = deal['properties'].get('createdate')
            days = days_since(created)

            print(f'  • {name} - {days}d in stage')

            if days >= 7:
                priority_actions.append({
                    'deal': name,
                    'stage': '[01-DISCOVERY-SCHEDULED]',
                    'action': 'Confirm discovery meeting scheduled',
                    'urgency': 65,
                    'days': days
                })
        print()

    print('=' * 80)
    print('TOP PRIORITY ACTIONS (Urgency Sorted)')
    print('=' * 80)
    print()

    # Sort by urgency
    priority_actions.sort(key=lambda x: (-x['urgency'], -x['days']))

    if priority_actions:
        for i, action in enumerate(priority_actions[:5], 1):
            print(f'{i}. [{action["stage"]}] {action["deal"]}')
            print(f'   Action: {action["action"]}')
            print(f'   Urgency: {action["urgency"]}/100 | Days in Stage: {action["days"]}')
            print()
    else:
        print('✓ No urgent actions required - all deals within acceptable timelines')
        print()

    # Calculate SLA violations
    sla_violations = 0
    for stage_name, stage_deals in deals_by_stage.items():
        sla_window = SLA_WINDOWS.get(stage_name, 30)
        for deal in stage_deals:
            if days_since(deal['properties'].get('createdate')) > sla_window:
                sla_violations += 1

    print('=' * 80)
    print('PIPELINE HEALTH METRICS')
    print('=' * 80)
    print(f'Total Priority Deals: {len(deals)}')
    print(f'Action Items Generated: {len(priority_actions)}')
    print(f'High Urgency (>85): {len([a for a in priority_actions if a["urgency"] > 85])}')
    print(f'SLA Violations: {sla_violations}')
    print()
    print(f'Next Sync: Tomorrow 9:00 AM')
    print('=' * 80)

if __name__ == '__main__':
    main()
