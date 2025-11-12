#!/usr/bin/env python3
"""Test the exact fetch_hubspot_priorities function from sync script."""

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

def fetch_hubspot_priorities():
    """Fetch priority deals from HubSpot - EXACT COPY from sync script"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
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

    try:
        print("Making API call...")
        response = requests.post("https://api.hubapi.com/crm/v3/objects/deals/search", headers=headers, json=payload, timeout=10)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            deals = response.json().get("results", [])
            print(f"Got {len(deals)} deals from API")
            
            by_stage = {}
            for deal in deals:
                stage_id = deal["properties"]["dealstage"]
                stage_name = PRIORITY_STAGES.get(stage_id, "UNKNOWN")
                if stage_name not in by_stage:
                    by_stage[stage_name] = []
                by_stage[stage_name].append({
                    "name": deal["properties"]["dealname"],
                    "amount": deal["properties"].get("amount", "0"),
                    "created": deal["properties"]["createdate"]
                })
            
            print(f"Returning dict with {len(by_stage)} stages")
            return by_stage
        else:
            print(f"Non-200 response, returning empty dict")
            return {}
    except Exception as e:
        print(f"Exception caught: {e}")
        return {}

# Run the function
print("Testing fetch_hubspot_priorities()...")
print("-" * 50)
result = fetch_hubspot_priorities()

print("\nResult:")
print(f"Type: {type(result)}")
print(f"Truthy: {bool(result)}")
print(f"Keys: {list(result.keys()) if result else 'No keys'}")
print(f"Total deals: {sum(len(stage_deals) for stage_deals in result.values()) if result else 0}")
