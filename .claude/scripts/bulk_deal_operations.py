#!/usr/bin/env python3
"""
Bulk Deal Operations Script
Uses the hubspot_deals_reference.json data structure for batch operations.

Example usage:
    # Get all deals from reference
    python bulk_deal_operations.py --list

    # Update specific deal
    python bulk_deal_operations.py --update-deal 43491605362 --stage "08d9c411-5e1b-487b-8732-9c2bcbbd0307"

    # Batch update multiple deals
    python bulk_deal_operations.py --batch-update --input deals.json
"""

import json
import requests
import argparse
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment
load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')

# Paths
SCRIPT_DIR = Path(__file__).parent
REFERENCE_FILE = SCRIPT_DIR.parent / 'data' / 'hubspot_deals_reference.json'

def load_deal_reference():
    """Load the deal reference JSON."""
    if not REFERENCE_FILE.exists():
        print(f"❌ Reference file not found: {REFERENCE_FILE}")
        return None

    with open(REFERENCE_FILE, 'r') as f:
        return json.load(f)

def get_deal_by_id(deal_id):
    """Get single deal from HubSpot API."""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    url = f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def update_deal(deal_id, properties):
    """Update deal properties."""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    url = f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}"
    payload = {"properties": properties}

    try:
        response = requests.patch(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✅ Updated deal {deal_id}")
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def list_reference_deals():
    """List all deals from reference file."""
    data = load_deal_reference()
    if not data:
        return

    print("\n" + "="*80)
    print("REFERENCE DEALS")
    print("="*80 + "\n")

    for i, deal in enumerate(data['sample_deals'], 1):
        print(f"{i}. {deal['deal_name']}")
        print(f"   ID: {deal['deal_id']}")
        print(f"   Stage: {deal['deal_stage']}")
        print(f"   Amount: ${deal['amount']:,}")
        print(f"   Next Step: {deal.get('next_step', 'None')}")
        print(f"   URL: {deal['deal_url']}")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="Bulk Deal Operations using reference JSON"
    )
    parser.add_argument('--list', action='store_true', help='List all reference deals')
    parser.add_argument('--get', type=str, help='Get deal by ID from HubSpot')
    parser.add_argument('--update-deal', type=str, help='Deal ID to update')
    parser.add_argument('--stage', type=str, help='New stage ID')
    parser.add_argument('--priority', type=str, help='Priority (high/medium/low)')
    parser.add_argument('--next-step', type=str, help='Next step text')

    args = parser.parse_args()

    if args.list:
        list_reference_deals()

    elif args.get:
        deal = get_deal_by_id(args.get)
        if deal:
            print(json.dumps(deal, indent=2))

    elif args.update_deal:
        properties = {}
        if args.stage:
            properties['dealstage'] = args.stage
        if args.priority:
            properties['hs_priority'] = args.priority
        if args.next_step:
            properties['hs_next_step'] = args.next_step

        if properties:
            update_deal(args.update_deal, properties)
        else:
            print("❌ No properties to update. Use --stage, --priority, or --next-step")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
