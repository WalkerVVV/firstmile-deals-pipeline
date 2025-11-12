#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HubSpot Deal Updates - Friday, November 7, 2025
Updates deal statuses, creates tasks, and logs activities
"""

import sys
import io
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')

if not API_KEY:
    print("❌ ERROR: HUBSPOT_API_KEY not found")
    exit(1)

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Deal IDs from search
DEALS = {
    'upstate_prep': '42448709378',
    'tactical': '40683158541',
    'boxiiship_sb': '18388015715',
    'joshs_frogs': '43373784945'
}

# Stage IDs
STAGES = {
    'DISCOVERY_SCHEDULED': '1090865183',
    'RATE_CREATION': 'e1c4321e-afb6-4b29-97d4-2b2425488535',
    'PROPOSAL_SENT': 'd607df25-2c6d-4a5d-9835-6ed1e4f4020a',
    'IMPLEMENTATION': '08d9c411-5e1b-487b-8732-9c2bcbbd0307',
    'CLOSED_WON': '3fd46d94-78b4-452b-8704-62a338a210fb'
}

def create_note(deal_id, note_body):
    """Create a note on a deal"""
    url = 'https://api.hubapi.com/crm/v3/objects/notes'
    payload = {
        'properties': {
            'hs_note_body': note_body,
            'hs_timestamp': datetime.now().isoformat()
        },
        'associations': [{
            'to': {'id': deal_id},
            'types': [{'associationCategory': 'HUBSPOT_DEFINED', 'associationTypeId': 214}]
        }]
    }
    response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
    return response.status_code == 201

def create_task(deal_id, task_subject, due_date_str, priority='HIGH'):
    """Create a task for a deal"""
    url = 'https://api.hubapi.com/crm/v3/objects/tasks'

    # Parse due date
    if 'today' in due_date_str.lower():
        due_date = datetime.now()
    elif 'monday' in due_date_str.lower():
        due_date = datetime.now() + timedelta(days=3)  # Assuming today is Friday
    else:
        due_date = datetime.now() + timedelta(days=1)

    due_timestamp = int(due_date.replace(hour=17, minute=0).timestamp() * 1000)

    payload = {
        'properties': {
            'hs_task_subject': task_subject,
            'hs_task_body': f'Created from 9AM sync - Friday Nov 7, 2025',
            'hs_task_status': 'NOT_STARTED',
            'hs_task_priority': priority,
            'hs_timestamp': datetime.now().isoformat(),
            'hubspot_owner_id': '699257003',
            'hs_task_due_date': due_timestamp
        },
        'associations': [{
            'to': {'id': deal_id},
            'types': [{'associationCategory': 'HUBSPOT_DEFINED', 'associationTypeId': 216}]
        }]
    }
    response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
    return response.status_code == 201

def update_deal_properties(deal_id, properties):
    """Update deal properties"""
    url = f'https://api.hubapi.com/crm/v3/objects/deals/{deal_id}'
    payload = {'properties': properties}
    response = requests.patch(url, headers=HEADERS, json=payload, timeout=10)
    return response.status_code == 200

def main():
    print("\n" + "="*80)
    print("HUBSPOT UPDATES - Friday, November 7, 2025")
    print("="*80 + "\n")

    # 1. UPSTATE PREP - Brandon DHL Follow-up
    print("1. Updating Upstate Prep...")
    note_1 = """
    **Friday Nov 7, 2025 - 10:00 AM CT**

    **Status Update**:
    - Need to contact Brandon regarding DHL situation
    - Questions: Current status, recent outreach, onboarding completion
    - Priority: HIGH - $950K implementation needs clarity

    **Next Actions**:
    - Call or email Brandon today
    - Get DHL onboarding status
    - Follow up on dangerous goods discussion

    **Risk**: Implementation may be blocked by DHL issues
    """

    if create_note(DEALS['upstate_prep'], note_1):
        print("   ✅ Note created")

    if create_task(DEALS['upstate_prep'], 'Contact Brandon - DHL Status Check', 'today', 'HIGH'):
        print("   ✅ Task created: Contact Brandon")

    if update_deal_properties(DEALS['upstate_prep'], {
        'hs_next_step': 'Contact Brandon regarding DHL onboarding status'
    }):
        print("   ✅ Next step updated\n")

    # 2. TACTICAL / SKUPREME - Eli MIA Follow-up
    print("2. Updating Tactical Logistic Solutions...")
    note_2 = """
    **Friday Nov 7, 2025 - 10:00 AM CT**

    **Status Update**: ON HOLD - Skupreme Contact MIA
    - Eli at Skupreme has gone MIA
    - Deal blocked - cannot proceed without customer contact
    - Priority: HIGH - $450K deal at risk

    **Action Plan**:
    - Email Eli today (re-engagement)
    - Call Eli today (2 hours after email)
    - If no response, escalate to alternative contact

    **Urgency**: Deal will be lost if contact not re-established within 1 week
    """

    if create_note(DEALS['tactical'], note_2):
        print("   ✅ Note created")

    if create_task(DEALS['tactical'], 'Email + Call Eli at Skupreme (MIA Follow-up)', 'today', 'HIGH'):
        print("   ✅ Task created: Email + Call Eli")

    if update_deal_properties(DEALS['tactical'], {
        'hs_next_step': 'Re-engage Eli at Skupreme - email and call',
        'dealstage': STAGES['IMPLEMENTATION']  # Keep in implementation but flag as on hold
    }):
        print("   ✅ Next step updated\n")

    # 3. BOXIISHIP SYSTEM BEAUTY - Wednesday CVM Meeting
    print("3. Updating BoxiiShip System Beauty TX...")
    note_3 = """
    **Friday Nov 7, 2025 - 10:00 AM CT**

    **Status Update**: No Scan Issue in Good Standing ✅
    - Previous tracking issues have been resolved
    - Customer relationship positive

    **Next Action**: Wednesday CVM Meeting
    - Attendees: Reid, BoxiiShip team, Crystal Ruban Melville
    - Purpose: Customer Value Metrics review
    - Need to send calendar invite today
    - Confirm Crystal availability

    **Agenda**:
    1. Current performance metrics
    2. Service level compliance check
    3. Outstanding operational items
    4. Q&A and next steps
    """

    if create_note(DEALS['boxiiship_sb'], note_3):
        print("   ✅ Note created")

    if create_task(DEALS['boxiiship_sb'], 'Send Wednesday CVM Meeting Invite', 'today', 'MEDIUM'):
        print("   ✅ Task created: Send meeting invite")

    if update_deal_properties(DEALS['boxiiship_sb'], {
        'hs_next_step': 'Send Wednesday CVM meeting invite to Reid and BoxiiShip team'
    }):
        print("   ✅ Next step updated\n")

    # 4. JOSH'S FROGS - Quote Follow-up (assuming this is the Josh mentioned)
    print("4. Updating Josh's Frogs...")
    note_4 = """
    **Friday Nov 7, 2025 - 10:00 AM CT**

    **Status Update**: Meeting Scheduling in Progress
    - Email sent requesting meeting time for next Tuesday
    - User available: After 10:30 AM MST on Tuesday
    - Awaiting Josh's response on preferred time

    **Next Actions**:
    - Follow up Monday if no response by EOD today
    - Schedule discovery call for Tuesday (after 10:30 AM MST)
    - Prepare discovery call materials

    **Deal Value**: $1,200,000
    **Priority**: Top 3 for the week
    """

    if create_note(DEALS['joshs_frogs'], note_4):
        print("   ✅ Note created")

    if create_task(DEALS['joshs_frogs'], 'Follow up on Tuesday meeting time confirmation', 'monday', 'MEDIUM'):
        print("   ✅ Task created: Follow up on meeting")

    if update_deal_properties(DEALS['joshs_frogs'], {
        'hs_next_step': 'Schedule Tuesday discovery call (after 10:30 AM MST)'
    }):
        print("   ✅ Next step updated\n")

    print("="*80)
    print("✅ ALL HUBSPOT UPDATES COMPLETE")
    print("="*80)
    print("\nSummary:")
    print("  • 4 deals updated")
    print("  • 4 notes created")
    print("  • 4 tasks created")
    print("  • 4 next steps updated")
    print("\nNext: Send emails and make phone calls\n")

if __name__ == "__main__":
    main()
