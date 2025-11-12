#!/usr/bin/env python3
"""Check for deals in priority stages."""

import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('HUBSPOT_API_KEY')
OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

PRIORITY_STAGES = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]"
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "filterGroups": [{
        "filters": [
            {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
            {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID},
            {"propertyName": "dealstage", "operator": "IN", "values": list(PRIORITY_STAGES.keys())}
        ]
    }],
    "properties": ["dealname", "dealstage", "amount", "createdate"],
    "limit": 100
}

print("Searching for deals in PRIORITY stages...")
print("Stage IDs being searched:", list(PRIORITY_STAGES.keys()))
print("-" * 50)

try:
    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/deals/search",
        headers=headers,
        json=payload,
        timeout=10
    )

    print(f"Response status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        total = data.get("total", 0)
        results = data.get("results", [])

        print(f"Total priority deals found: {total}")
        print()

        if results:
            by_stage = {}
            for deal in results:
                stage_id = deal["properties"]["dealstage"]
                stage_name = PRIORITY_STAGES.get(stage_id, "UNKNOWN")
                if stage_name not in by_stage:
                    by_stage[stage_name] = []
                by_stage[stage_name].append({
                    "name": deal["properties"]["dealname"],
                    "amount": deal["properties"].get("amount", "0")
                })

            for stage, deals in by_stage.items():
                print(f"{stage} ({len(deals)} deals):")
                for deal in deals[:5]:
                    amount = f"${int(deal['amount']):,}" if deal['amount'] != '0' else "No amount"
                    print(f"  - {deal['name']} - {amount}")
                if len(deals) > 5:
                    print(f"  ... and {len(deals) - 5} more")
                print()
        else:
            print("No deals found in priority stages!")
    else:
        print(f"ERROR: {response.text}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
