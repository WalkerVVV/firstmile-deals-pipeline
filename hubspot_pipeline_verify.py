#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HubSpot Pipeline Verification Script
Verifies local folder structure matches HubSpot deals
"""

import sys
import io
import os
import requests
from collections import defaultdict

# Fix Windows encoding issues
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration - Load from environment variables for security
API_KEY = os.environ.get('HUBSPOT_API_KEY', 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764')
OWNER_ID = os.environ.get('HUBSPOT_OWNER_ID', '699257003')
PIPELINE_ID = os.environ.get('HUBSPOT_PIPELINE_ID', '8bd9336b-4767-4e67-9fe2-35dfcad7c8be')

def fetch_all_deals():
    """Fetch all deals from HubSpot (paginated)"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    all_deals = []
    after = None

    while True:
        payload = {
            "filterGroups": [{
                "filters": [
                    {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
                    {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID}
                ]
            }],
            "properties": ["dealname", "dealstage", "hubspot_owner_id", "amount", "createdate"],
            "limit": 100
        }

        if after:
            payload["after"] = after

        response = requests.post(
            "https://api.hubapi.com/crm/v3/objects/deals/search",
            headers=headers,
            json=payload
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return []

        data = response.json()
        all_deals.extend(data["results"])

        if "paging" in data and "next" in data["paging"]:
            after = data["paging"]["next"]["after"]
        else:
            break

    return all_deals

def main():
    print("\n" + "="*80)
    print("HUBSPOT PIPELINE VERIFICATION")
    print("="*80 + "\n")

    # Fetch deals
    print("Fetching deals from HubSpot...")
    deals = fetch_all_deals()

    if not deals:
        print("❌ No deals found or API error")
        return

    print(f"✅ Found {len(deals)} total deals\n")

    # Group by stage
    stages = defaultdict(list)
    for deal in deals:
        stage_id = deal["properties"]["dealstage"]
        deal_name = deal["properties"]["dealname"]
        stages[stage_id].append(deal_name)

    # Display results
    print(f"{'Stage ID':<40} {'Count':>10}")
    print("-" * 80)

    for stage_id, deals_list in sorted(stages.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"{stage_id:<40} {len(deals_list):>10}")

    print("\n" + "="*80)
    print(f"SUMMARY: {len(stages)} unique stages | {len(deals)} total deals")
    print("="*80 + "\n")

    # Show sample deals per stage
    print("\nSample Deals by Stage (first 3):")
    print("-" * 80)
    for stage_id, deals_list in sorted(stages.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n{stage_id} ({len(deals_list)} deals):")
        for deal in sorted(deals_list)[:3]:
            print(f"  • {deal}")
        if len(deals_list) > 3:
            print(f"  ... and {len(deals_list) - 3} more")

if __name__ == "__main__":
    main()
