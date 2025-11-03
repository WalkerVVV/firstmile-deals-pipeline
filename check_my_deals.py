#!/usr/bin/env python3
import os
import requests

API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    raise ValueError("HUBSPOT_API_KEY environment variable must be set")
OWNER_ID = '699257003'
PIPELINE_ID = '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'

# Stage mappings from NEBUCHADNEZZAR_REFERENCE.md
STAGES = {
    "02d8a1d7-d0b3-41d9-adc6-44ab768a61b8": "[02-DISCOVERY-COMPLETE]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[03-RATE-CREATION]",
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[04-PROPOSAL-SENT]",
    "2b73ce8b-3c95-48ef-bcee-0bc2cd3b8a57": "[05-SETUP-DOCS-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
    "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-CLOSED-WON]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[08-CLOSED-LOST]"
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "filterGroups": [{
        "filters": [
            {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
            {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID}
        ]
    }],
    "properties": ["dealname", "dealstage", "amount", "createdate"],
    "limit": 100
}

response = requests.post(
    "https://api.hubapi.com/crm/v3/objects/deals/search",
    headers=headers,
    json=payload
)

deals = response.json().get('results', [])

# Group by stage - focus on active stages
active_stages = [
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a",  # [03-RATE-CREATION]
    "d2a08d6f-cc04-4423-9215-594fe682e538",  # [04-PROPOSAL-SENT]
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307",  # [06-IMPLEMENTATION]
]

print("="*80)
print("BRETT WALKER'S ACTIVE DEALS - 3PM PRIORITY CHECK")
print("="*80)

for stage_id in active_stages:
    stage_deals = [d for d in deals if d['properties']['dealstage'] == stage_id]
    if stage_deals:
        stage_name = STAGES.get(stage_id, stage_id)
        print(f"\n{stage_name} ({len(stage_deals)} deals):")
        for deal in stage_deals:
            name = deal['properties']['dealname']
            amount = deal['properties'].get('amount', 'N/A')
            print(f"  • {name} - ${amount}")

print("\n" + "="*80)
