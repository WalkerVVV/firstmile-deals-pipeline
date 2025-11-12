#!/usr/bin/env python3
"""Check what HubSpot properties are available for key deals."""

import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

API_KEY = os.environ.get('HUBSPOT_API_KEY')
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Check deals mentioned by user
deals_to_check = {
    "Athleta": "Athleta - Parcel Shipping Optimization",
    "COLDEST": "COLDEST",
    "Upstate Prep": "Upstate Prep - New Deal",
    "Stackd Logistics": "Stackd Logistics - New Deal",
    "BoxiiShip System Beauty": "Boxiiship_System Beauty Logistics LLC-"
}

# Search for each deal
for label, deal_name in deals_to_check.items():
    payload = {
        "filterGroups": [{
            "filters": [{"propertyName": "dealname", "operator": "CONTAINS_TOKEN", "value": deal_name.split()[0]}]
        }],
        "properties": ["dealname", "dealstage", "amount", "priority", "deal_status", "hs_priority", "notes_last_updated"],
        "limit": 5
    }
    
    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/deals/search",
        headers=headers,
        json=payload,
        timeout=10
    )
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        for deal in results:
            if deal_name.lower() in deal["properties"]["dealname"].lower():
                print(f"\n{label} ({deal['properties']['dealname']}):")
                print(f"  Deal ID: {deal['id']}")
                print(f"  Stage: {deal['properties']['dealstage']}")
                print(f"  Amount: ${deal['properties'].get('amount', '0')}")
                print(f"  All properties available:")
                for prop, value in deal["properties"].items():
                    if value and prop not in ['dealname', 'dealstage', 'amount']:
                        print(f"    {prop}: {value}")
                break
