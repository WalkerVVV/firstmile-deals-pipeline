#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEBUCHADNEZZAR v3.1.0 - EOD SYNC
End of day wrap with context preservation and tomorrow prep
"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment (SECURE)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)

OWNER_ID = '699257003'
PIPELINE_ID = '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'
DOWNLOADS = Path.home() / "Downloads"
DAILY_LOG = DOWNLOADS / "_DAILY_LOG.md"
FOLLOW_UP = DOWNLOADS / "FOLLOW_UP_REMINDERS.txt"
PIPELINE_TRACKER = DOWNLOADS / "_PIPELINE_TRACKER.csv"

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# All active stages (excluding CLOSED-LOST)
ACTIVE_STAGES = [
    '1090865183',  # [01-DISCOVERY-SCHEDULED]
    'd2a08d6f-cc04-4423-9215-594fe682e538',  # [02-DISCOVERY-COMPLETE]
    'e1c4321e-afb6-4b29-97d4-2b2425488535',  # [03-RATE-CREATION]
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a',  # [04-PROPOSAL-SENT]
    '4e549d01-674b-4b31-8a90-91ec03122715',  # [05-SETUP-DOCS-SENT]
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307',  # [06-IMPLEMENTATION]
    '3fd46d94-78b4-452b-8704-62a338a210fb',  # [07-STARTED-SHIPPING]
]

STAGE_MAP = {
    '1090865183': '[01-DISCOVERY-SCHEDULED]',
    'd2a08d6f-cc04-4423-9215-594fe682e538': '[02-DISCOVERY-COMPLETE]',
    'e1c4321e-afb6-4b29-97d4-2b2425488535': '[03-RATE-CREATION]',
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a': '[04-PROPOSAL-SENT]',
    '4e549d01-674b-4b31-8a90-91ec03122715': '[05-SETUP-DOCS-SENT]',
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307': '[06-IMPLEMENTATION]',
    '3fd46d94-78b4-452b-8704-62a338a210fb': '[07-STARTED-SHIPPING]',
    '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8': '[08-CLOSED-LOST]'
}

def days_since(date_str):
    """Calculate days since a given date"""
    if not date_str:
        return 999
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now(date.tzinfo) - date).days
    except:
        return 999

def format_currency(amount):
    """Format currency value"""
    if not amount:
        return "$0"
    # Convert string to float if needed
    if isinstance(amount, str):
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            return "$0"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.0f}K"
    else:
        return f"${amount:,.0f}"

def extract_todays_context():
    """Extract today's completed and pending items from daily log"""
    if not DAILY_LOG.exists():
        return {"completed": [], "pending": [], "context": ""}

    content = DAILY_LOG.read_text(encoding='utf-8')
    today = datetime.now().strftime("%Y-%m-%d")

    # Find today's section
    today_section = ""
    for line in content.split('\n'):
        if today in line:
            idx = content.find(line)
            remaining = content[idx:]
            next_date_idx = remaining.find('\n## ', 10)
            if next_date_idx > 0:
                today_section = remaining[:next_date_idx]
            else:
                today_section = remaining
            break

    # Extract items
    completed = []
    pending = []

    for line in today_section.split('\n'):
        if '✅' in line or 'COMPLETED' in line.upper():
            completed.append(line.strip('- ').strip())
        elif '🔄' in line or '⏳' in line or 'PENDING' in line.upper() or 'IN PROGRESS' in line.upper():
            pending.append(line.strip('- ').strip())

    return {
        "completed": completed,
        "pending": pending,
        "context": today_section
    }

def fetch_all_deals():
    """Fetch all active deals from HubSpot"""
    payload = {
        'filterGroups': [{
            'filters': [
                {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': OWNER_ID},
                {'propertyName': 'pipeline', 'operator': 'EQ', 'value': PIPELINE_ID},
                {'propertyName': 'dealstage', 'operator': 'IN', 'values': ACTIVE_STAGES}
            ]
        }],
        'properties': ['dealname', 'dealstage', 'amount', 'createdate', 'notes_last_updated', 'closedate'],
        'limit': 100
    }

    try:
        response = requests.post(
            'https://api.hubapi.com/crm/v3/objects/deals/search',
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json().get('results', [])
    except Exception as e:
        print(f"❌ Error fetching deals: {e}")
        return []

def calculate_pipeline_health(deals):
    """Calculate pipeline health metrics"""
    health = {
        'total_deals': len(deals),
        'total_value': 0,
        'by_stage': {},
        'at_risk': [],
        'recently_updated': []
    }

    for deal in deals:
        props = deal.get('properties', {})
        stage = props.get('dealstage')
        stage_name = STAGE_MAP.get(stage, 'UNKNOWN')
        amount = props.get('amount') or 0

        # Convert string to float if needed
        if isinstance(amount, str):
            try:
                amount = float(amount)
            except (ValueError, TypeError):
                amount = 0

        health['total_value'] += amount

        # Count by stage
        if stage_name not in health['by_stage']:
            health['by_stage'][stage_name] = {'count': 0, 'value': 0}
        health['by_stage'][stage_name]['count'] += 1
        health['by_stage'][stage_name]['value'] += amount

        # Identify at-risk deals (stale)
        days = days_since(props.get('notes_last_updated') or props.get('createdate'))
        if days > 30:
            health['at_risk'].append({
                'name': props.get('dealname', 'Unknown'),
                'stage': stage_name,
                'amount': format_currency(amount),
                'days_stale': days
            })

        # Recently updated (last 7 days)
        if days <= 7:
            health['recently_updated'].append({
                'name': props.get('dealname', 'Unknown'),
                'stage': stage_name,
                'amount': format_currency(amount),
                'days_ago': days
            })

    return health

def generate_tomorrow_action_queue(todays_context, pipeline_health):
    """Generate prioritized action queue for tomorrow"""
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%A, %B %d, %Y')

    queue = []
    queue.append(f"# FOLLOW-UP REMINDERS - {tomorrow_str}")
    queue.append("")
    queue.append("=" * 80)
    queue.append("")

    # Priority 1: Pending items from today
    if todays_context["pending"]:
        queue.append("## 🚨🚨🚨 PRIORITY 1 - ROLLED OVER FROM TODAY")
        queue.append("")
        for i, item in enumerate(todays_context["pending"][:5], 1):
            queue.append(f"{i}. {item}")
        queue.append("")
        queue.append("=" * 80)
        queue.append("")

    # Critical: At-risk deals (>30 days stale)
    queue.append("## 🚨 CRITICAL (Do First)")
    queue.append("")

    if pipeline_health['at_risk']:
        queue.append("### At-Risk Deals (>30 days since update):\n")
        for deal in sorted(pipeline_health['at_risk'], key=lambda x: x['days_stale'], reverse=True)[:5]:
            queue.append(f"- **{deal['name']}** ({deal['amount']}) - {deal['stage']} - {deal['days_stale']} days stale")
        queue.append("")
    else:
        queue.append("✅ No critical at-risk deals\n")

    queue.append("=" * 80)
    queue.append("")

    # High Priority: Active deals
    queue.append("## 📋 HIGH PRIORITY (This Week)")
    queue.append("")
    queue.append("(Check HubSpot for scheduled follow-ups and SLA deadlines)")
    queue.append("")

    return "\n".join(queue)

def append_eod_to_daily_log(todays_context, pipeline_health):
    """Append EOD summary to daily log"""
    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    eod_summary = []
    eod_summary.append("")
    eod_summary.append("=" * 80)
    eod_summary.append(f"## EOD SUMMARY - {now.strftime('%I:%M %p')}")
    eod_summary.append("=" * 80)
    eod_summary.append("")

    # Today's Completions
    eod_summary.append("### ✅ TODAY'S COMPLETIONS")
    eod_summary.append("")
    if todays_context['completed']:
        for item in todays_context['completed']:
            eod_summary.append(f"- {item}")
    else:
        eod_summary.append("_No completed items logged today_")
    eod_summary.append("")

    # Pending Items
    if todays_context['pending']:
        eod_summary.append("### ⏳ ROLLED TO TOMORROW")
        eod_summary.append("")
        for item in todays_context['pending']:
            eod_summary.append(f"- {item}")
        eod_summary.append("")

    # Pipeline Health Snapshot
    eod_summary.append("### 📊 PIPELINE HEALTH SNAPSHOT")
    eod_summary.append("")
    eod_summary.append(f"- **Total Active Deals**: {pipeline_health['total_deals']}")
    eod_summary.append(f"- **Total Pipeline Value**: {format_currency(pipeline_health['total_value'])}")
    eod_summary.append(f"- **At-Risk Deals**: {len(pipeline_health['at_risk'])} (>30 days stale)")
    eod_summary.append(f"- **Recently Active**: {len(pipeline_health['recently_updated'])} (updated last 7 days)")
    eod_summary.append("")

    # Tomorrow's Top Priorities
    eod_summary.append(f"### 🎯 TOMORROW'S TOP PRIORITIES ({tomorrow.strftime('%A, %B %d')})")
    eod_summary.append("")
    if todays_context['pending']:
        eod_summary.append("**Rolled Over Items:**")
        for i, item in enumerate(todays_context['pending'][:3], 1):
            eod_summary.append(f"{i}. {item}")
    else:
        eod_summary.append("✅ Clean slate - no pending items")
    eod_summary.append("")

    eod_summary.append("=" * 80)
    eod_summary.append(f"**Next Sync**: Tomorrow 9:00 AM - Context loaded and ready")
    eod_summary.append("=" * 80)
    eod_summary.append("")

    with open(DAILY_LOG, 'a', encoding='utf-8') as f:
        f.write("\n".join(eod_summary))

def main():
    """Main EOD sync workflow"""
    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    print('=' * 80)
    print('NEBUCHADNEZZAR END OF DAY WRAP - EOD SYNC')
    print('=' * 80)
    print(f'Time: {now.strftime("%I:%M %p %Z")}')
    print(f'Date: {now.strftime("%A, %B %d, %Y")}')
    print(f'Owner Lock: {OWNER_ID} | Pipeline: {PIPELINE_ID}')
    print('=' * 80)
    print()

    # PHASE 1: TODAY'S SUMMARY
    print('## PHASE 1: TODAY\'S SUMMARY\n')
    print('📊 Analyzing today\'s activities from daily log...')
    todays_context = extract_todays_context()
    print(f'✅ Completed: {len(todays_context["completed"])} items')
    print(f'⏳ Pending: {len(todays_context["pending"])} items\n')

    # PHASE 2: HUBSPOT PIPELINE HEALTH CHECK
    print('## PHASE 2: PIPELINE HEALTH CHECK\n')
    print('🔄 Fetching pipeline data from HubSpot...')
    deals = fetch_all_deals()
    pipeline_health = calculate_pipeline_health(deals)

    print(f'📊 Pipeline Metrics:')
    print(f'   - Total Active Deals: {pipeline_health["total_deals"]}')
    print(f'   - Total Pipeline Value: {format_currency(pipeline_health["total_value"])}')
    print(f'   - At-Risk (>30 days stale): {len(pipeline_health["at_risk"])}')
    print(f'   - Recently Active (last 7 days): {len(pipeline_health["recently_updated"])}\n')

    # Show pipeline by stage
    print('### Pipeline by Stage:\n')
    for stage, metrics in sorted(pipeline_health['by_stage'].items()):
        print(f'   {stage}: {metrics["count"]} deals ({format_currency(metrics["value"])})')
    print()

    # PHASE 3: TOMORROW PREP
    print('## PHASE 3: TOMORROW PREP\n')
    print(f'📅 Preparing action queue for {tomorrow.strftime("%A, %B %d")}...')
    tomorrow_queue = generate_tomorrow_action_queue(todays_context, pipeline_health)

    with open(FOLLOW_UP, 'w', encoding='utf-8', newline='\n') as f:
        f.write(tomorrow_queue)
    print(f'✅ Updated: {FOLLOW_UP}\n')

    # PHASE 4: DOCUMENTATION
    print('## PHASE 4: DOCUMENTATION\n')
    print('📝 Appending EOD summary to daily log...')
    append_eod_to_daily_log(todays_context, pipeline_health)
    print(f'✅ Updated: {DAILY_LOG}\n')

    # PHASE 5: STATE CHECKPOINT
    print('## PHASE 5: STATE CHECKPOINT\n')
    print('=' * 80)
    print(f'🎯 TOMORROW\'S OPENING CHECKLIST ({tomorrow.strftime("%A, %B %d")})')
    print('=' * 80)
    print()

    if todays_context['pending']:
        print('### 🚨 Priority 1 - Rolled Over from Today:\n')
        for i, item in enumerate(todays_context['pending'][:5], 1):
            print(f'{i}. {item}')
        print()

    if pipeline_health['at_risk']:
        print('### ⚠️ At-Risk Deals (Immediate Attention):\n')
        for deal in sorted(pipeline_health['at_risk'], key=lambda x: x['days_stale'], reverse=True)[:5]:
            print(f'- **{deal["name"]}** ({deal["amount"]}) - {deal["days_stale"]} days stale')
        print()

    print('### 📊 Pipeline Health Alert:\n')
    rate_creation = pipeline_health['by_stage'].get('[03-RATE-CREATION]', {'count': 0})
    proposal_sent = pipeline_health['by_stage'].get('[04-PROPOSAL-SENT]', {'count': 0})

    if rate_creation['count'] > 5:
        print(f'⚠️  Rate Creation backlog: {rate_creation["count"]} deals')
    if proposal_sent['count'] > 10:
        print(f'⚠️  Proposal Sent stage: {proposal_sent["count"]} deals (check for stale proposals)')
    if not pipeline_health['at_risk']:
        print('✅ No deals at risk - pipeline health is good')
    print()

    # Sales Discipline Agents
    print('=' * 80)
    print('🎯 SALES DISCIPLINE REVIEW')
    print('=' * 80)

    # Check if it's Friday for weekly metrics
    is_friday = now.weekday() == 4  # 0=Monday, 4=Friday

    if is_friday:
        print('\n🎯 FRIDAY WEEKLY METRICS REVIEW (Required):')
        print('   python .claude/agents/weekly_metrics_tracker.py')
        print('\n   Track 5/2/3/1 goals: 5 leads, 2 discoveries, 3 proposals, 1 close')
        print('   Review conversion rates and weekly performance')
    else:
        print('\n📊 Optional: Run weekly metrics anytime to check current week progress:')
        print('   python .claude/agents/weekly_metrics_tracker.py')

    print('\n💡 Daily verification: Did #1 priority deal get touched today?')
    print('   python .claude/agents/prioritization_agent.py --daily-reminder')
    print()

    # Final summary
    print('=' * 80)
    print('EOD SYNC COMPLETE')
    print('=' * 80)
    print()
    print(f'✅ Today: {len(todays_context["completed"])} completed, {len(todays_context["pending"])} rolled over')
    print(f'✅ Tomorrow: {len(todays_context["pending"])} priority items + {len(pipeline_health["at_risk"])} at-risk deals')
    print(f'✅ Next sync: Tomorrow 9:00 AM - Context loaded and ready to execute')
    print()
    print('[MODE: QM3.1 ACTIVE]')
    print('[SYSTEM: NEBUCHADNEZZAR]')
    print('[OWNER: 699257003]')
    print('=' * 80)

if __name__ == '__main__':
    main()
