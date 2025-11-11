#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Brett Walker Pipeline Audit - YOUR DEALS ONLY
"""

import sys
import os
import io
from datetime import datetime
from dotenv import load_dotenv
from hubspot_sync_core import HubSpotSyncManager

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BRETT_OWNER_ID = "699257003"

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
    print("\n" + "="*80)
    print("BRETT WALKER PIPELINE AUDIT - YOUR DEALS ONLY")
    print("="*80 + "\n")

    load_dotenv()
    API_KEY = os.environ.get('HUBSPOT_API_KEY')

    sync = HubSpotSyncManager(
        api_key=API_KEY,
        owner_id=BRETT_OWNER_ID,
        pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
    )

    properties = [
        'dealname', 'dealstage', 'amount', 'closedate',
        'monthly_volume', 'hs_monthly_volume', 'next_step',
        'hubspot_owner_id'
    ]

    deals = sync.fetch_deals(
        pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be",
        properties=properties
    )

    # Filter to Brett's active deals only
    brett_active_deals = [
        d for d in deals
        if d.get('properties', {}).get('dealstage') in ACTIVE_STAGES
        and d.get('properties', {}).get('hubspot_owner_id') == BRETT_OWNER_ID
    ]

    print(f"YOUR Active Deals: {len(brett_active_deals)}\n")
    print("="*80)
    print("DEALS REQUIRING UPDATES")
    print("="*80 + "\n")

    total_value = 0

    for deal in brett_active_deals:
        props = deal.get('properties', {})
        deal_id = deal.get('id')
        deal_name = props.get('dealname', 'Unknown')
        stage = ACTIVE_STAGES.get(props.get('dealstage'), 'Unknown')
        amount = float(props.get('amount', 0) or 0)
        next_step = props.get('next_step', '')
        monthly_volume = props.get('monthly_volume') or props.get('hs_monthly_volume')
        close_date = props.get('closedate')

        total_value += amount

        issues = []
        if not close_date:
            issues.append("⚠️  Close date missing")
        if not monthly_volume:
            issues.append("⚠️  Monthly volume missing")
        if not amount or amount == 0:
            issues.append("❌ Amount missing or $0")
        if not next_step or next_step.lower() == 'none':
            issues.append("❌ Next Step empty or 'None'")

        print(f"Deal: {deal_name}")
        print(f"Stage: {stage}")
        print(f"Amount: ${amount:,.0f}")
        print(f"Deal ID: {deal_id}")
        print(f"HubSpot: https://app.hubspot.com/contacts/8210927/record/0-3/{deal_id}")

        if issues:
            print(f"Issues ({len(issues)}):")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("✅ NO ISSUES - Deal data complete!")

        print(f"\nCurrent Values:")
        print(f"  Close Date: {close_date or 'NOT SET'}")
        print(f"  Monthly Volume: {monthly_volume or 'NOT SET'}")
        print(f"  Next Step: {next_step or 'NOT SET'}")

        print("\n" + "-"*80 + "\n")

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"\nTotal Active Deals: {len(brett_active_deals)}")
    print(f"Total Pipeline Value: ${total_value:,.0f}")
    print(f"\n✅ ONLY UPDATE THESE {len(brett_active_deals)} DEALS FOR EOD DEADLINE")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
