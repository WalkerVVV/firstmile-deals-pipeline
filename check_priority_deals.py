#!/usr/bin/env python3
"""Check status of BoxiiShip AF and DYLN deals"""
import requests
import json

API_KEY = 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'
OWNER_ID = '699257003'

STAGE_MAP = {
    '1090865183': '[01-DISCOVERY-SCHEDULED]',
    'd2a08d6f-cc04-4423-9215-594fe682e538': '[02-DISCOVERY-COMPLETE]',
    'e1c4321e-afb6-4b29-97d4-2b2425488535': '[03-RATE-CREATION]',
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a': '[04-PROPOSAL-SENT]',
    '4e549d01-674b-4b31-8a90-91ec03122715': '[05-SETUP-DOCS-SENT]',
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307': '[06-IMPLEMENTATION]',
    '3fd46d94-78b4-452b-8704-62a338a210fb': '[07-STARTED-SHIPPING]',  # HubSpot: "Started Shipping"
    '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8': '[08-CLOSED-LOST]'
}

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

def search_deal(keyword):
    payload = {
        'filterGroups': [{
            'filters': [
                {'propertyName': 'dealname', 'operator': 'CONTAINS_TOKEN', 'value': keyword},
                {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': OWNER_ID}
            ]
        }],
        'properties': ['dealname', 'dealstage', 'amount', 'hs_priority', 'notes_last_updated', 'createdate'],
        'limit': 10
    }

    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/deals/search',
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f'Error searching for {keyword}: {response.status_code}')
        return []

print('=' * 80)
print('PRIORITY DEAL STATUS CHECK')
print('=' * 80)
print()

# BoxiiShip
print('BoxiiShip AF / Make Wellness ($7.1M Win-Back)')
print('-' * 80)
boxii_deals = search_deal('BoxiiShip')
if boxii_deals:
    for deal in boxii_deals:
        stage_id = deal['properties'].get('dealstage')
        stage_name = STAGE_MAP.get(stage_id, f'Unknown ({stage_id})')
        print(f"Deal Name: {deal['properties'].get('dealname')}")
        print(f"  HubSpot ID: {deal['id']}")
        print(f"  Stage: {stage_name}")
        print(f"  Amount: ${deal['properties'].get('amount', '0')}")
        print(f"  Priority: {deal['properties'].get('hs_priority', 'Not set')}")
        print(f"  Last Note Update: {deal['properties'].get('notes_last_updated', 'Never')}")
        print()
else:
    print('  No deals found')
    print()

# DYLN
print('DYLN Inc. ($3.6M New Business)')
print('-' * 80)
dyln_deals = search_deal('DYLN')
if dyln_deals:
    for deal in dyln_deals:
        stage_id = deal['properties'].get('dealstage')
        stage_name = STAGE_MAP.get(stage_id, f'Unknown ({stage_id})')
        print(f"Deal Name: {deal['properties'].get('dealname')}")
        print(f"  HubSpot ID: {deal['id']}")
        print(f"  Stage: {stage_name}")
        print(f"  Amount: ${deal['properties'].get('amount', '0')}")
        print(f"  Priority: {deal['properties'].get('hs_priority', 'Not set')}")
        print(f"  Last Note Update: {deal['properties'].get('notes_last_updated', 'Never')}")
        print()
else:
    print('  No deals found')
    print()

print('=' * 80)
