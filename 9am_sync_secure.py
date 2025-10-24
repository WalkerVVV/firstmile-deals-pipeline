#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEBUCHADNEZZAR v2.0 - 9AM Pipeline Sync (SECURE VERSION)
Daily morning synchronization for priority deals

SECURITY:
- Uses environment variables for API credentials
- Centralized configuration management
- Shared utilities for code reuse
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from datetime import datetime
from collections import defaultdict

# Import secure utilities
from config import Config
from hubspot_utils import HubSpotClient, days_since, format_currency, get_status_emoji

# SLA windows (days) - moved from hardcoded to constants
SLA_WINDOWS = {
    '[01-DISCOVERY-SCHEDULED]': 30,
    '[02-DISCOVERY-COMPLETE]': 30,
    '[03-RATE-CREATION]': 14,  # Bottleneck stage
    '[04-PROPOSAL-SENT]': 30,
    '[05-SETUP-DOCS-SENT]': 14,
    '[06-IMPLEMENTATION]': 30
}

# Priority stages for sync (using Config.STAGE_NAME_TO_ID)
PRIORITY_STAGE_IDS = [
    Config.get_stage_id('[03-RATE-CREATION]'),
    Config.get_stage_id('[04-PROPOSAL-SENT]'),
    Config.get_stage_id('[05-SETUP-DOCS-SENT]'),
    Config.get_stage_id('[02-DISCOVERY-COMPLETE]'),
    Config.get_stage_id('[01-DISCOVERY-SCHEDULED]')
]


def main():
    """Main sync workflow for 9AM pipeline check."""
    print('=' * 80)
    print('NEBUCHADNEZZAR v2.0 - 9AM PIPELINE SYNC (SECURE)')
    print('=' * 80)
    print(f'Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

    # Initialize HubSpot client (validates API key from .env)
    try:
        client = HubSpotClient()
        print(f'Owner Lock: {client.owner_id} ✓')
        print(f'Pipeline Lock: {client.pipeline_id} ✓')
        print('✅ API credentials loaded from environment')
        print()
    except ValueError as e:
        print(f'❌ Configuration Error: {e}')
        print()
        print('REQUIRED: Create .env file with HubSpot credentials')
        print('See .env.example for template')
        return

    # Fetch priority deals using centralized client
    print('🔄 Fetching priority deals from HubSpot...')

    filters = [
        {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': client.owner_id},
        {'propertyName': 'pipeline', 'operator': 'EQ', 'value': client.pipeline_id},
        {'propertyName': 'dealstage', 'operator': 'IN', 'values': PRIORITY_STAGE_IDS}
    ]

    properties = ['dealname', 'dealstage', 'amount', 'createdate', 'notes_last_updated', 'hs_lastmodifieddate']

    try:
        result = client.search_deals(filters, properties, limit=100)
        deals = result.get('results', [])
    except Exception as e:
        print(f'❌ Error fetching deals: {e}')
        return

    print(f'✅ Found {len(deals)} priority deals\n')

    if not deals:
        print('✨ No priority deals in pipeline - all clear!')
        return

    # Analyze deals by stage
    stage_counts = defaultdict(int)
    sla_violations = []
    high_urgency = []
    needs_follow_up = []

    for deal in deals:
        stage_id = deal['properties'].get('dealstage')
        stage_name = Config.get_stage_name(stage_id)
        stage_counts[stage_name] += 1

        # Calculate age
        created = deal['properties'].get('createdate')
        age_days = days_since(created)

        # Check SLA
        sla_window = SLA_WINDOWS.get(stage_name, 30)
        if age_days > sla_window:
            sla_violations.append({
                'name': deal['properties'].get('dealname', 'Unnamed'),
                'stage': stage_name,
                'age': age_days,
                'sla': sla_window,
                'amount': deal['properties'].get('amount', 0)
            })

        # High urgency (>2x SLA)
        if age_days > sla_window * 2:
            high_urgency.append({
                'name': deal['properties'].get('dealname', 'Unnamed'),
                'stage': stage_name,
                'age': age_days,
                'amount': deal['properties'].get('amount', 0)
            })

        # Needs follow-up (no recent activity)
        last_activity = deal['properties'].get('notes_last_updated') or deal['properties'].get('hs_lastmodifieddate')
        days_since_activity = days_since(last_activity)
        if days_since_activity > 14:  # No activity in 2 weeks
            needs_follow_up.append({
                'name': deal['properties'].get('dealname', 'Unnamed'),
                'stage': stage_name,
                'days_inactive': days_since_activity,
                'amount': deal['properties'].get('amount', 0)
            })

    # Print Summary Report
    print('📊 PIPELINE HEALTH SUMMARY')
    print('─' * 80)
    print(f'Total Priority Deals: {len(deals)}')
    print(f'SLA Violations: {len(sla_violations)} ({len(sla_violations)/len(deals)*100:.1f}%)')
    print(f'High Urgency (>2x SLA): {len(high_urgency)}')
    print(f'Needs Follow-Up (>14d inactive): {len(needs_follow_up)}')
    print()

    # Stage Distribution
    print('📋 DEALS BY STAGE')
    print('─' * 80)
    for stage_name in sorted(stage_counts.keys()):
        count = stage_counts[stage_name]
        emoji = '⚠️ ' if count > 5 else '✓ '
        print(f'{emoji}{stage_name}: {count} deals')
    print()

    # SLA Violations Detail
    if sla_violations:
        print('🚨 SLA VIOLATIONS (Sorted by Age)')
        print('─' * 80)
        sla_violations.sort(key=lambda x: x['age'], reverse=True)
        for v in sla_violations[:10]:  # Show top 10
            emoji = get_status_emoji(v['age'], v['sla'])
            amount_str = format_currency(v['amount']) if v['amount'] else 'N/A'
            print(f"{emoji} {v['name'][:40]:<40} | {v['stage']:<25} | {v['age']:>3}d (SLA: {v['sla']:>2}d) | {amount_str:>8}")
        if len(sla_violations) > 10:
            print(f'... and {len(sla_violations) - 10} more')
        print()

    # High Urgency Deals
    if high_urgency:
        print('🔴 HIGH URGENCY DEALS (>2x SLA)')
        print('─' * 80)
        high_urgency.sort(key=lambda x: x['age'], reverse=True)
        for h in high_urgency[:5]:  # Show top 5
            amount_str = format_currency(h['amount']) if h['amount'] else 'N/A'
            print(f"🔴 {h['name'][:40]:<40} | {h['stage']:<25} | {h['age']:>3}d | {amount_str:>8}")
        if len(high_urgency) > 5:
            print(f'... and {len(high_urgency) - 5} more')
        print()

    # Needs Follow-Up
    if needs_follow_up:
        print('💤 NEEDS FOLLOW-UP (>14d Inactive)')
        print('─' * 80)
        needs_follow_up.sort(key=lambda x: x['days_inactive'], reverse=True)
        for n in needs_follow_up[:5]:  # Show top 5
            amount_str = format_currency(n['amount']) if n['amount'] else 'N/A'
            print(f"💤 {n['name'][:40]:<40} | {n['stage']:<25} | {n['days_inactive']:>3}d inactive | {amount_str:>8}")
        if len(needs_follow_up) > 5:
            print(f'... and {len(needs_follow_up) - 5} more')
        print()

    # Action Items
    print('✅ RECOMMENDED ACTIONS')
    print('─' * 80)
    if stage_counts.get('[03-RATE-CREATION]', 0) > 5:
        print('• ⚠️  BOTTLENECK: [03-RATE-CREATION] has >5 deals - prioritize rate creation')
    if len(high_urgency) > 0:
        print(f'• 🔴 URGENT: {len(high_urgency)} deals >2x SLA - immediate attention required')
    if len(needs_follow_up) > 10:
        print(f'• 💤 STALE: {len(needs_follow_up)} deals inactive >14d - schedule follow-ups')
    if len(sla_violations) < len(deals) * 0.2:
        print('• ✅ HEALTHY: <20% SLA violations - pipeline in good shape')
    else:
        print(f'• ⚠️  ATTENTION: {len(sla_violations)/len(deals)*100:.0f}% SLA violations - review capacity')
    print()

    print('=' * 80)
    print('🏁 9AM SYNC COMPLETE')
    print('=' * 80)


if __name__ == '__main__':
    main()
