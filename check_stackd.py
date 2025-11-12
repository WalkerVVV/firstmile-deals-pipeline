#!/usr/bin/env python3
import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

payload = {
    "filterGroups": [{"filters": [{"propertyName": "dealname", "operator": "CONTAINS_TOKEN", "value": "Stackd"}]}],
    "properties": ["dealname", "dealstage", "amount", "hs_priority", "createdate", "hs_lastmodifieddate"],
    "limit": 10
}

response = requests.post("https://api.hubapi.com/crm/v3/objects/deals/search", headers=headers, json=payload, timeout=10)
if response.status_code == 200:
    for deal in response.json().get("results", []):
        print(f"{deal['properties']['dealname']}:")
        print(f"  Stage: {deal['properties']['dealstage']}")
        print(f"  Amount: ${deal['properties'].get('amount', '0')}")
        print(f"  Priority: {deal['properties'].get('hs_priority', 'none')}")
        print(f"  Created: {deal['properties']['createdate'][:10]}")
        print(f"  Modified: {deal['properties']['hs_lastmodifieddate'][:10]}")
        print()
