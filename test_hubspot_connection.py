#!/usr/bin/env python3
"""Test HubSpot API connection and diagnose issues."""

import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get('HUBSPOT_API_KEY')
OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

print("Testing HubSpot API Connection...")
print("-" * 50)

if not API_KEY:
    print("ERROR: HUBSPOT_API_KEY not found in .env")
    exit(1)

if API_KEY.startswith('pat-na1-YOUR'):
    print("ERROR: API key is still using template value")
    print("Please update .env with actual HubSpot API key")
    exit(1)

print(f"API Key loaded: {API_KEY[:10]}...")
print(f"Owner ID: {OWNER_ID}")
print(f"Pipeline ID: {PIPELINE_ID}")
print()

# Test API connection with a simple request
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Test 1: Get account info
print("Test 1: Fetching account info...")
try:
    response = requests.get(
        "https://api.hubapi.com/integrations/v1/me",
        headers=headers,
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS: API connection working")
        data = response.json()
        print(f"Portal ID: {data.get('portalId')}")
        print(f"App ID: {data.get('appId')}")
    elif response.status_code == 401:
        print("ERROR: Authentication failed - API key is invalid or expired")
        print(f"Response: {response.text}")
    else:
        print(f"ERROR: Unexpected response - {response.text}")
except Exception as e:
    print(f"ERROR: Connection failed - {e}")

print()

# Test 2: Search for deals
print("Test 2: Searching for deals...")
payload = {
    "filterGroups": [{
        "filters": [
            {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
            {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID}
        ]
    }],
    "properties": ["dealname", "dealstage", "amount"],
    "limit": 5
}

try:
    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/deals/search",
        headers=headers,
        json=payload,
        timeout=10
    )
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        total = data.get("total", 0)
        print(f"SUCCESS: Found {total} deals")

        results = data.get("results", [])
        if results:
            print(f"\nFirst {len(results)} deals:")
            for deal in results:
                name = deal.get("properties", {}).get("dealname", "Unknown")
                stage = deal.get("properties", {}).get("dealstage", "Unknown")
                print(f"  - {name} (Stage: {stage})")
        else:
            print("  (No deals found - this might be normal if pipeline is empty)")
    elif response.status_code == 401:
        print("ERROR: Authentication failed")
        print(f"Response: {response.text}")
    else:
        print(f"ERROR: Request failed - {response.text}")
except Exception as e:
    print(f"ERROR: Request failed - {e}")

print()
print("Diagnosis complete.")
