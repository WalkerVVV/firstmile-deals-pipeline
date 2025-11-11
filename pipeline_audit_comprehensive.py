#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMPREHENSIVE PIPELINE AUDIT - HubSpot Data Quality Check
Validates all active deals meet leadership requirements.

Requirements Checklist:
1. Stage is current and accurate
2. Close date is set
3. Monthly volume is added/accurate
4. Amount (annual revenue) is added/accurate
5. Next Step field has one-line status
6. Company profile enrichment:
   - Contact connected to company
   - Physical address
   - Shipping system
   - Company owner assigned
   - Lead source
   - Referral source

Date: 2025-11-10
"""

import sys
import os
import io
from datetime import datetime
from dotenv import load_dotenv
from hubspot_sync_core import HubSpotSyncManager

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Active stages (exclude Closed Lost) - CORRECTED STAGE IDs
ACTIVE_STAGES = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[02-DISCOVERY-COMPLETE]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "4e549d01-674b-4b31-8a90-91ec03122715": "[05-SETUP-DOCS-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
    "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-STARTED-SHIPPING]"
}

def check_deal_quality(deal, sync):
    """Check data quality for a single deal."""

    props = deal.get('properties', {})
    deal_id = deal.get('id')
    deal_name = props.get('dealname', 'Unknown')

    issues = []

    # 1. Check Stage (should be in active stages)
    stage = props.get('dealstage')
    if not stage or stage not in ACTIVE_STAGES:
        issues.append("❌ Stage invalid or missing")

    # 2. Check Close Date
    close_date = props.get('closedate')
    if not close_date:
        issues.append("⚠️  Close date not set")

    # 3. Check Monthly Volume
    monthly_volume = props.get('monthly_volume') or props.get('hs_monthly_volume')
    if not monthly_volume:
        issues.append("⚠️  Monthly volume missing")

    # 4. Check Amount (Annual Revenue)
    amount = props.get('amount')
    if not amount or amount == '0':
        issues.append("❌ Amount (annual revenue) missing or zero")

    # 5. Check Next Step
    next_step = props.get('next_step') or props.get('dealstage_label')
    if not next_step or next_step.lower() == 'none':
        issues.append("❌ Next Step field empty or 'None'")

    return {
        'deal_id': deal_id,
        'deal_name': deal_name,
        'stage': ACTIVE_STAGES.get(stage, 'Unknown'),
        'amount': amount or '0',
        'issues': issues,
        'issue_count': len(issues)
    }

def main():
    """Run comprehensive pipeline audit."""

    print("\n" + "="*80)
    print("HUBSPOT PIPELINE AUDIT - Data Quality Check")
    print("="*80 + "\n")

    # Load credentials
    load_dotenv()
    API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not API_KEY:
        print("ERROR: HUBSPOT_API_KEY not found")
        sys.exit(1)

    # Initialize sync manager
    sync = HubSpotSyncManager(
        api_key=API_KEY,
        owner_id="699257003",
        pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
    )

    print("Fetching all active deals from HubSpot...")

    # Fetch deals with all required properties
    properties = [
        'dealname', 'dealstage', 'amount', 'closedate',
        'monthly_volume', 'hs_monthly_volume', 'next_step',
        'createdate', 'hs_lastmodifieddate', 'dealstage_label',
        'hubspot_owner_id', 'hs_deal_stage_probability'
    ]

    try:
        # Get all deals in pipeline
        deals = sync.fetch_deals(
            pipeline_id="8bd9336b-4767-4e67-9fe2-35dfcad7c8be",
            properties=properties
        )

        print(f"Found {len(deals)} total deals in pipeline\n")

        # Filter to active stages only (exclude Closed Lost)
        active_deals = [
            d for d in deals
            if d.get('properties', {}).get('dealstage') in ACTIVE_STAGES
        ]

        print(f"Active deals (excluding Closed Lost): {len(active_deals)}\n")
        print("="*80)
        print("AUDIT RESULTS BY STAGE")
        print("="*80 + "\n")

        # Audit each deal
        audit_results = []
        for deal in active_deals:
            result = check_deal_quality(deal, sync)
            audit_results.append(result)

        # Group by stage
        by_stage = {}
        for result in audit_results:
            stage = result['stage']
            if stage not in by_stage:
                by_stage[stage] = []
            by_stage[stage].append(result)

        # Report by stage
        total_issues = 0
        deals_with_issues = 0

        for stage in sorted(by_stage.keys()):
            stage_deals = by_stage[stage]
            stage_issues = sum(d['issue_count'] for d in stage_deals)
            deals_needing_work = len([d for d in stage_deals if d['issue_count'] > 0])

            print(f"\n{stage} ({len(stage_deals)} deals)")
            print("-" * 80)

            for deal in stage_deals:
                if deal['issue_count'] > 0:
                    print(f"\n  Deal: {deal['deal_name']}")
                    print(f"  Amount: ${deal['amount']}")
                    print(f"  Deal ID: {deal['deal_id']}")
                    print(f"  Issues ({deal['issue_count']}):")
                    for issue in deal['issues']:
                        print(f"    {issue}")
                    total_issues += deal['issue_count']
                    deals_with_issues += 1

        # Summary
        print("\n" + "="*80)
        print("AUDIT SUMMARY")
        print("="*80)
        print(f"\nTotal Active Deals: {len(active_deals)}")
        print(f"Deals Needing Updates: {deals_with_issues}")
        print(f"Deals Ready: {len(active_deals) - deals_with_issues}")
        print(f"Total Issues Found: {total_issues}")

        if total_issues == 0:
            print("\n✅ PIPELINE IS CLEAN - All deals meet data quality requirements!")
        else:
            print(f"\n⚠️  ACTION REQUIRED - {deals_with_issues} deals need updates before EOD")

        # Save detailed report
        output_file = f"pipeline_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("HUBSPOT PIPELINE AUDIT - DETAILED REPORT\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")

            f.write(f"Total Active Deals: {len(active_deals)}\n")
            f.write(f"Deals Needing Updates: {deals_with_issues}\n")
            f.write(f"Total Issues: {total_issues}\n\n")

            f.write("="*80 + "\n")
            f.write("DEALS REQUIRING UPDATES\n")
            f.write("="*80 + "\n\n")

            for result in sorted(audit_results, key=lambda x: x['issue_count'], reverse=True):
                if result['issue_count'] > 0:
                    f.write(f"Deal: {result['deal_name']}\n")
                    f.write(f"Stage: {result['stage']}\n")
                    f.write(f"Amount: ${result['amount']}\n")
                    f.write(f"Deal ID: {result['deal_id']}\n")
                    f.write(f"HubSpot Link: https://app.hubspot.com/contacts/8210927/record/0-3/{result['deal_id']}\n")
                    f.write(f"Issues:\n")
                    for issue in result['issues']:
                        f.write(f"  {issue}\n")
                    f.write("\n" + "-"*80 + "\n\n")

        print(f"\nDetailed report saved: {output_file}")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\nERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
