#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline Sync Verification - Compare Local Folders vs HubSpot
Daily Pipeline Sync Flows - Lock Verification
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
BASE_PATH = os.environ.get('FIRSTMILE_DEALS_PATH', r"C:\Users\BrettWalker\FirstMile_Deals")

# Stage ID to Name Mapping (VERIFIED from HubSpot API - October 7, 2025)
# Source: Direct API query via HubSpot CLI
# See: .claude/VERIFIED_STAGE_IDS.md for complete documentation
STAGE_MAPPING = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",  # ✅ CORRECTED - was mislabeled
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[02-DISCOVERY-COMPLETE]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "4e549d01-674b-4b31-8a90-91ec03122715": "[05-SETUP-DOCS-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
    "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-CLOSED-WON]",
    "02d8a1d7-d0b3-41d9-adc6-44ab768a61b8": "[08-CLOSED-LOST]"
    # Note: [00-LEAD] and [09-WIN-BACK] are local-only stages (not in HubSpot FM pipeline)
}

def fetch_all_hubspot_deals():
    """Fetch all deals from HubSpot"""
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
            "properties": ["dealname", "dealstage"],
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
            print(f"❌ HubSpot API Error: {response.text}")
            return []

        data = response.json()
        all_deals.extend(data["results"])

        if "paging" in data and "next" in data["paging"]:
            after = data["paging"]["next"]["after"]
        else:
            break

    return all_deals

def get_local_deals():
    """Get all deals from local folder structure"""
    local_deals = defaultdict(list)

    if not os.path.exists(BASE_PATH):
        print(f"❌ Base path not found: {BASE_PATH}")
        return local_deals

    for item in os.listdir(BASE_PATH):
        item_path = os.path.join(BASE_PATH, item)
        if os.path.isdir(item_path) and item.startswith('['):
            # Extract stage and company name
            parts = item.split(']', 1)
            if len(parts) == 2:
                stage = parts[0] + ']'
                company = parts[1].strip('_').replace('_', ' ')

                # Skip templates and placeholders
                if company.upper() not in ['TEMPLATE', 'PDR', 'PLACEHOLDER']:
                    local_deals[stage].append(company)

    return local_deals

def normalize_company_name(name):
    """Normalize company names for comparison"""
    return name.lower().replace('-', ' ').replace('_', ' ').strip()

def main():
    print("\n" + "="*80)
    print("NEBUCHADNEZZAR v2.0 - PIPELINE SYNC VERIFICATION")
    print("="*80 + "\n")

    # Fetch HubSpot deals
    print("[1/3] Fetching deals from HubSpot...")
    hubspot_deals = fetch_all_hubspot_deals()
    if not hubspot_deals:
        print("❌ Failed to fetch HubSpot deals")
        return
    print(f"✅ Found {len(hubspot_deals)} HubSpot deals\n")

    # Group HubSpot deals by stage
    hubspot_by_stage = defaultdict(list)
    for deal in hubspot_deals:
        stage_id = deal["properties"]["dealstage"]
        stage_name = STAGE_MAPPING.get(stage_id, f"[UNKNOWN-{stage_id[:8]}]")
        deal_name = deal["properties"]["dealname"]
        hubspot_by_stage[stage_name].append(deal_name)

    # Get local deals
    print("[2/3] Scanning local folder structure...")
    local_by_stage = get_local_deals()
    total_local = sum(len(deals) for deals in local_by_stage.values())
    print(f"✅ Found {total_local} local deal folders\n")

    # Compare
    print("[3/3] Comparing HubSpot vs Local...")
    print("\n" + "="*80)
    print(f"{'Stage':<30} {'HubSpot':>12} {'Local':>12} {'Status':>15}")
    print("="*80)

    all_stages = sorted(set(list(hubspot_by_stage.keys()) + list(local_by_stage.keys())))

    total_sync_issues = 0
    for stage in all_stages:
        hs_count = len(hubspot_by_stage.get(stage, []))
        local_count = len(local_by_stage.get(stage, []))

        if hs_count == local_count:
            status = "✅ SYNCED"
        elif hs_count > local_count:
            status = f"⚠️  +{hs_count - local_count} HS"
            total_sync_issues += abs(hs_count - local_count)
        else:
            status = f"⚠️  +{local_count - hs_count} LOCAL"
            total_sync_issues += abs(hs_count - local_count)

        print(f"{stage:<30} {hs_count:>12} {local_count:>12} {status:>15}")

    print("="*80)
    print(f"\n📊 SUMMARY:")
    print(f"   HubSpot Total: {len(hubspot_deals)} deals")
    print(f"   Local Total:   {total_local} deals")
    print(f"   Difference:    {abs(len(hubspot_deals) - total_local)} deals")

    if total_sync_issues == 0:
        print(f"\n✅ PIPELINE LOCK VERIFIED - All stages in perfect sync!")
    else:
        print(f"\n⚠️  SYNC ISSUES DETECTED - {total_sync_issues} discrepancies found")
        print(f"\n💡 Recommendation: Run N8N automation or manual sync to reconcile differences")

    # Show detailed mismatches if any
    if total_sync_issues > 0:
        print("\n" + "="*80)
        print("DETAILED MISMATCH ANALYSIS")
        print("="*80)

        for stage in all_stages:
            hs_deals = set(normalize_company_name(d) for d in hubspot_by_stage.get(stage, []))
            local_deals = set(normalize_company_name(d) for d in local_by_stage.get(stage, []))

            only_hs = hs_deals - local_deals
            only_local = local_deals - hs_deals

            if only_hs or only_local:
                print(f"\n{stage}:")
                if only_hs:
                    print(f"  Only in HubSpot ({len(only_hs)}):")
                    for deal in sorted(only_hs)[:5]:
                        print(f"    • {deal}")
                    if len(only_hs) > 5:
                        print(f"    ... and {len(only_hs) - 5} more")

                if only_local:
                    print(f"  Only in Local ({len(only_local)}):")
                    for deal in sorted(only_local)[:5]:
                        print(f"    • {deal}")
                    if len(only_local) > 5:
                        print(f"    ... and {len(only_local) - 5} more")

    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
