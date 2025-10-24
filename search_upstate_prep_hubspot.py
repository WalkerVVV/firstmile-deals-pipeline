#!/usr/bin/env python3
"""Search HubSpot for Upstate Prep deal"""

import requests
import json
from hubspot_config import get_hubspot_config, get_api_headers

# Get HubSpot configuration
config = get_hubspot_config()
headers = get_api_headers()

# Search for Upstate Prep deal
search_url = f"{config['BASE_URL']}/crm/v3/objects/deals/search"
search_payload = {
    'filterGroups': [{
        'filters': [{
            'propertyName': 'dealname',
            'operator': 'CONTAINS_TOKEN',
            'value': 'Upstate'
        }]
    }],
    'properties': [
        'dealname',
        'dealstage',
        'amount',
        'closedate',
        'pipeline',
        'hs_object_id',
        'createdate',
        'hs_lastmodifieddate'
    ],
    'limit': 10
}

print("Searching HubSpot for Upstate Prep deal...")
print()

response = requests.post(search_url, headers=headers, json=search_payload)

if response.status_code == 200:
    results = response.json()
    if results.get('total', 0) > 0:
        print(f"Found {results['total']} deal(s) matching 'Upstate':")
        print()
        for deal in results['results']:
            deal_id = deal['id']
            props = deal['properties']

            print(f"Deal ID: {deal_id}")
            print(f"Deal Name: {props.get('dealname', 'N/A')}")
            print(f"Amount: ${props.get('amount', 'N/A')}")
            print(f"Stage ID: {props.get('dealstage', 'N/A')}")
            print(f"Created: {props.get('createdate', 'N/A')}")
            print(f"Last Modified: {props.get('hs_lastmodifieddate', 'N/A')}")
            print('=' * 70)

            # Get engagements/activities for this deal
            print(f"\nFetching activities for Deal ID {deal_id}...")
            activities_url = f"{config['BASE_URL']}/crm/v3/objects/deals/{deal_id}/associations/notes"
            activities_response = requests.get(activities_url, headers=headers)

            if activities_response.status_code == 200:
                activities_data = activities_response.json()
                if activities_data.get('results'):
                    print(f"Found {len(activities_data['results'])} note(s)")
                else:
                    print("No notes found")

            # Get tasks
            tasks_url = f"{config['BASE_URL']}/crm/v3/objects/deals/{deal_id}/associations/tasks"
            tasks_response = requests.get(tasks_url, headers=headers)

            if tasks_response.status_code == 200:
                tasks_data = tasks_response.json()
                if tasks_data.get('results'):
                    print(f"Found {len(tasks_data['results'])} task(s)")
                else:
                    print("No tasks found")

            print()
    else:
        print('No deals found matching "Upstate"')
else:
    print(f'Error: {response.status_code}')
    print(response.text)
