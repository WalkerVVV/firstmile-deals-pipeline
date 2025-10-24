from hubspot_config import get_hubspot_config
import requests
from datetime import datetime

config = get_hubspot_config()
headers = {
    'Authorization': f'Bearer {config["API_KEY"]}',
    'Content-Type': 'application/json'
}

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
    'properties': ['dealname', 'dealstage', 'amount', 'closedate', 'hs_lastmodifieddate', 'notes_last_updated'],
    'limit': 100
}

response = requests.post(
    f'{config["BASE_URL"]}/crm/v3/objects/deals/search',
    headers=headers,
    json=search_payload
)

print(f'[EOD SYNC] HubSpot Query Status: {response.status_code}')
print(f'[EOD SYNC] Modified Deals Today: {response.json()["total"]}\n')

deals = response.json().get('results', [])
if deals:
    print("DEALS MODIFIED TODAY:")
    for d in deals:
        deal_name = d['properties']['dealname']
        deal_stage = d['properties']['dealstage']
        deal_amount = d['properties'].get('amount', '0')
        print(f"  - {deal_name}")
        print(f"    Stage: {deal_stage}")
        print(f"    Amount: ${deal_amount}")
        print()
else:
    print("No deals modified today.")
