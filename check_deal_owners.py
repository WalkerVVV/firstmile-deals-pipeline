#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check which owners have deals in the audit results
"""

import sys
import os
import io
from dotenv import load_dotenv
from hubspot_sync_core import HubSpotSyncManager
from collections import defaultdict

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ACTIVE_STAGES = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[02-DISCOVERY-COMPLETE]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "4e549d01-674b-4b31-8a90-91ec03122715": "[05-SETUP-DOCS-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
    "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-STARTED-SHIPPING]"
}

def main():
    load_dotenv()
    API_KEY = os.environ.get('HUBSPOT_API_KEY')

    sync = HubSpotSyncManager(
        api_key=API_KEY,
        owner_id="699257003",  # Brett Walker
        pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
    )

    print("\nFETCHING ACTIVE DEALS AND CHECKING OWNERS...\n")

    properties = ['dealname', 'dealstage', 'hubspot_owner_id', 'amount']

    deals = sync.fetch_deals(
        pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be",
        properties=properties
    )

    # Filter to active stages
    active_deals = [
        d for d in deals
        if d.get('properties', {}).get('dealstage') in ACTIVE_STAGES
    ]

    print(f"Total active deals: {len(active_deals)}\n")

    # Count by owner
    by_owner = defaultdict(lambda: {'count': 0, 'total_value': 0, 'deals': []})

    for deal in active_deals:
        props = deal.get('properties', {})
        owner_id = props.get('hubspot_owner_id', 'Unassigned')
        amount = float(props.get('amount', 0) or 0)
        deal_name = props.get('dealname', 'Unknown')

        by_owner[owner_id]['count'] += 1
        by_owner[owner_id]['total_value'] += amount
        by_owner[owner_id]['deals'].append(deal_name)

    print("DEALS BY OWNER:")
    print("="*80)

    # Known owner IDs
    OWNERS = {
        "699257003": "Brett Walker",
        # Add others if known
    }

    for owner_id, info in sorted(by_owner.items(), key=lambda x: x[1]['count'], reverse=True):
        owner_name = OWNERS.get(owner_id, f"Unknown ({owner_id})")

        print(f"\n{owner_name}")
        print(f"  Owner ID: {owner_id}")
        print(f"  Deal Count: {info['count']}")
        print(f"  Total Value: ${info['total_value']:,.0f}")

        if owner_id == "699257003":
            print(f"  ✅ BRETT WALKER'S DEALS")
            print(f"\n  Sample deals:")
            for deal in info['deals'][:5]:
                print(f"    - {deal}")
        else:
            print(f"  ⚠️  NOT Brett Walker's deals")

    brett_deals = by_owner.get("699257003", {}).get('count', 0)

    print("\n" + "="*80)
    print(f"\nBRETT WALKER'S ACTIVE DEALS: {brett_deals}")
    print(f"OTHER OWNERS' ACTIVE DEALS: {len(active_deals) - brett_deals}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
