#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEBUCHADNEZZAR v3.1.0 - 3PM SYNC
Afternoon checkpoint and deal documentation
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

def read_todays_log():
    """Extract today's activities from daily log"""
    if not DAILY_LOG.exists():
        return {"completed": [], "in_progress": [], "context": ""}

    content = DAILY_LOG.read_text(encoding='utf-8')
    today = datetime.now().strftime("%Y-%m-%d")

    # Find today's section
    today_section = ""
    for line in content.split('\n'):
        if today in line:
            # Start capturing from this point
            idx = content.find(line)
            # Get everything after this line until next date or end
            remaining = content[idx:]
            next_date_idx = remaining.find('\n## ', 10)  # Find next section
            if next_date_idx > 0:
                today_section = remaining[:next_date_idx]
            else:
                today_section = remaining
            break

    # Extract completed and in-progress items
    completed = []
    in_progress = []

    for line in today_section.split('\n'):
        if '✅' in line or 'COMPLETED' in line.upper():
            completed.append(line.strip('- ').strip())
        elif '🔄' in line or 'IN PROGRESS' in line.upper() or 'WORKING ON' in line.upper():
            in_progress.append(line.strip('- ').strip())

    return {
        "completed": completed,
        "in_progress": in_progress,
        "context": today_section[:500] if today_section else "No activity logged yet"
    }

def read_morning_priorities():
    """Extract priority items from follow-up reminders"""
    if not FOLLOW_UP.exists():
        return {"critical": [], "high": [], "medium": []}

    content = FOLLOW_UP.read_text(encoding='utf-8')

    priorities = {"critical": [], "high": [], "medium": []}
    current_section = None

    for line in content.split('\n'):
        if '🚨🚨🚨 PRIORITY 1' in line or 'CUSTOMER CRISIS' in line:
            current_section = 'critical'
        elif '🚨 CRITICAL' in line:
            current_section = 'critical'
        elif '📋 HIGH PRIORITY' in line:
            current_section = 'high'
        elif '🔵 MEDIUM' in line or '🔵 LOW' in line:
            current_section = 'medium'
        elif current_section and line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '-')):
            priorities[current_section].append(line.strip())

    return priorities

def fetch_active_deals():
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

def categorize_deals(deals):
    """Categorize deals by stage and urgency"""
    categorized = {
        'rate_creation': [],
        'proposal_sent': [],
        'setup_docs': [],
        'implementation': [],
        'discovery': []
    }

    for deal in deals:
        props = deal.get('properties', {})
        stage = props.get('dealstage')
        stage_name = STAGE_MAP.get(stage, 'UNKNOWN')
        days = days_since(props.get('createdate'))

        # Get amount and ensure it's a number
        amount = props.get('amount') or 0
        if isinstance(amount, str):
            try:
                amount = float(amount)
            except (ValueError, TypeError):
                amount = 0

        deal_info = {
            'id': deal.get('id'),
            'name': props.get('dealname', 'Unknown'),
            'stage': stage_name,
            'amount': format_currency(amount),
            'days_in_stage': days,
            'last_updated': days_since(props.get('notes_last_updated'))
        }

        # Categorize by stage
        if '[03-RATE-CREATION]' in stage_name:
            categorized['rate_creation'].append(deal_info)
        elif '[04-PROPOSAL-SENT]' in stage_name:
            categorized['proposal_sent'].append(deal_info)
        elif '[05-SETUP-DOCS-SENT]' in stage_name:
            categorized['setup_docs'].append(deal_info)
        elif '[06-IMPLEMENTATION]' in stage_name:
            categorized['implementation'].append(deal_info)
        elif '[01-DISCOVERY' in stage_name or '[02-DISCOVERY' in stage_name:
            categorized['discovery'].append(deal_info)

    return categorized

def generate_report():
    """Generate the 3PM sync report"""
    now = datetime.now()
    print('=' * 80)
    print('NEBUCHADNEZZAR AFTERNOON CHECKPOINT - 3PM SYNC')
    print('=' * 80)
    print(f'Time: {now.strftime("%I:%M %p %Z")}')
    print(f'Date: {now.strftime("%A, %B %d, %Y")}')
    print(f'Owner Lock: {OWNER_ID} | Pipeline: {PIPELINE_ID}')
    print('=' * 80)
    print()

    # 1. Time Check
    print('## ⏰ TIME CHECK\n')
    print(f'**Current Time**: {now.strftime("%I:%M %p")}')
    print(f'**Remaining Work Time**: ~2 hours until 5:00 PM')
    print(f'**EOD Target**: 5:00 PM')
    print()

    # 2. Today's Activity Review
    print('## 📊 TODAY\'S ACTIVITY REVIEW\n')
    todays_log = read_todays_log()

    if todays_log['completed']:
        print('### ✅ Completed Today:\n')
        for item in todays_log['completed'][:10]:
            print(f'- {item}')
        print()
    else:
        print('### ✅ Completed Today:\n')
        print('_No completed items logged yet - update _DAILY_LOG.md with your progress_\n')

    if todays_log['in_progress']:
        print('### 🔄 In Progress:\n')
        for item in todays_log['in_progress'][:5]:
            print(f'- {item}')
        print()
    else:
        print('### 🔄 In Progress:\n')
        print('_No items currently flagged as in progress_\n')

    # 3. Morning Priorities Check
    print('## 📋 MORNING PRIORITIES STATUS\n')
    priorities = read_morning_priorities()

    if priorities['critical']:
        print('### 🚨 Critical Items Status:\n')
        for item in priorities['critical'][:5]:
            print(f'{item}')
            print('   - [ ] ✅ COMPLETED')
            print('   - [ ] 🔄 IN PROGRESS')
            print('   - [ ] ❌ BLOCKED\n')

    if priorities['high']:
        print('### 📋 High Priority Items:\n')
        for item in priorities['high'][:5]:
            print(f'{item}')
        print()

    # 4. HubSpot Deal Updates
    print('## 🎯 DEAL UPDATES REQUIRED\n')
    print('🔄 Fetching active deals from HubSpot...\n')

    deals = fetch_active_deals()
    categorized = categorize_deals(deals)

    # Show urgent deals needing attention
    urgent_count = 0

    if categorized['rate_creation']:
        urgent_rates = [d for d in categorized['rate_creation'] if d['days_in_stage'] > 14]
        if urgent_rates:
            print(f'### ⚠️ Rate Creation Urgent ({len(urgent_rates)} deals >14 days):\n')
            for deal in urgent_rates[:5]:
                print(f'- **{deal["name"]}** ({deal["amount"]}) - {deal["days_in_stage"]} days')
                urgent_count += 1
            print()

    if categorized['proposal_sent']:
        urgent_proposals = [d for d in categorized['proposal_sent'] if d['days_in_stage'] > 30]
        if urgent_proposals:
            print(f'### ⚠️ Proposal Sent Stale ({len(urgent_proposals)} deals >30 days):\n')
            for deal in urgent_proposals[:5]:
                print(f'- **{deal["name"]}** ({deal["amount"]}) - {deal["days_in_stage"]} days')
                urgent_count += 1
            print()

    if categorized['setup_docs']:
        print(f'### 📄 Setup Docs Sent ({len(categorized["setup_docs"])} deals):\n')
        for deal in categorized['setup_docs'][:3]:
            print(f'- **{deal["name"]}** ({deal["amount"]}) - {deal["days_in_stage"]} days')
        print()

    if categorized['implementation']:
        print(f'### 🚀 Implementation Active ({len(categorized["implementation"])} deals):\n')
        for deal in categorized['implementation'][:3]:
            print(f'- **{deal["name"]}** ({deal["amount"]}) - {deal["days_in_stage"]} days')
        print()

    if urgent_count == 0:
        print('✅ No urgent deal updates required at this time\n')

    # 5. EOD Priorities
    print('## 🎯 EOD PRIORITIES (Must Finish Today)\n')
    print('Review and mark what MUST be completed before 5:00 PM:\n')
    print('- [ ] Close open loops from morning critical items')
    print('- [ ] Update HubSpot notes for all completed calls/emails')
    print('- [ ] Send any pending proposals or rate requests')
    print('- [ ] Set follow-up tasks for tomorrow')
    print('- [ ] Update _DAILY_LOG.md with final activities')
    print()

    # 6. Tomorrow Prep
    print('## 📅 TOMORROW PREP\n')
    tomorrow = now + timedelta(days=1)
    print(f'**Tomorrow**: {tomorrow.strftime("%A, %B %d, %Y")}\n')
    print('### Calendar Check:\n')
    print('- [ ] Review tomorrow\'s scheduled calls/meetings')
    print('- [ ] Prepare materials for tomorrow\'s calls')
    print('- [ ] Review follow-up reminders for tomorrow')
    print()

    print('### Materials to Prepare Tonight:\n')
    print('_List any proposals, rate sheets, or documents needed for tomorrow_\n')
    print()

    # Sales Discipline Check
    print('=' * 80)
    print('🎯 SALES DISCIPLINE CHECK (Before EOD)')
    print('=' * 80)
    print('\nEnsure top priority deal moved forward today:')
    print('  python .claude/agents/prioritization_agent.py --daily-reminder')
    print('\nGenerate urgency follow-ups if needed:')
    print('  python .claude/agents/sales_execution_agent.py')
    print('\n💡 Best practice: Verify daily touchpoint on #1 priority deal')
    print()

    # Summary
    print('=' * 80)
    print('NEXT STEPS:')
    print('=' * 80)
    print('1. Mark completed items above')
    print('2. Update HubSpot notes for today\'s activities')
    print('3. Close urgent loops before EOD')
    print('4. Run EOD sync at 5:00 PM to roll over to tomorrow')
    print()
    print('[MODE: QM3.1 ACTIVE]')
    print('[SYSTEM: NEBUCHADNEZZAR]')
    print('[OWNER: 699257003]')
    print('=' * 80)

if __name__ == '__main__':
    generate_report()
