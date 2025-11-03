#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mark BoxiiShip AF as WIN-BACK within [08-CLOSED-LOST] stage"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment (SECURE)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)
DEAL_ID = '36466918934'  # BoxiiShip- American Fork
CLOSED_LOST_STAGE = '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8'  # [08-CLOSED-LOST]

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

print('=' * 80)
print('MARKING BOXIISHIP AF AS ACTIVE WIN-BACK')
print('=' * 80)
print(f'Deal ID: {DEAL_ID}')
print(f'Stage: [08-CLOSED-LOST] (win-back opportunity)')
print()

# Step 1: Get current deal info and update
print('Step 1: Getting deal info...')
response = requests.get(
    f'https://api.hubapi.com/crm/v3/objects/deals/{DEAL_ID}?properties=dealstage,dealname',
    headers=headers
)

if response.status_code == 200:
    current_stage = response.json()['properties'].get('dealstage')
    current_name = response.json()['properties'].get('dealname')
    print(f'   Current name: {current_name}')
    print(f'   Current stage: {current_stage}')

    # Update both stage and name
    new_name = 'BoxiiShip American Fork - Make Wellness - WIN-BACK'

    update_payload = {
        'properties': {
            'dealstage': CLOSED_LOST_STAGE,
            'dealname': new_name
        }
    }

    print(f'   Updating to: {new_name}')
    print(f'   Moving to stage: [08-CLOSED-LOST]')

    update_response = requests.patch(
        f'https://api.hubapi.com/crm/v3/objects/deals/{DEAL_ID}',
        headers=headers,
        json=update_payload
    )

    if update_response.status_code == 200:
        print('   Deal updated successfully')
        print('     - Name: WIN-BACK added')
        print('     - Stage: [08-CLOSED-LOST]')
    else:
        print(f'   Error: {update_response.status_code}')
        print(update_response.text)
        exit(1)
else:
    print(f'   Error fetching deal: {response.status_code}')
    exit(1)

print()

# Step 2: Add WIN-BACK documentation note
print('Step 2: Adding WIN-BACK documentation...')

note_content = f"""WIN-BACK OPPORTUNITY - ACTIVE CAMPAIGN

Deal Status: [08-CLOSED-LOST] with ACTIVE WIN-BACK
Update Date: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
Updated By: Brett Walker

---

WIN-BACK CONTEXT

This is an ACTIVE WIN-BACK opportunity for BoxiiShip American Fork / Make Wellness.

Status Timeline:
- Previously: Active customer ([06-IMPLEMENTATION])
- Lost to: UPS
- Current: Win-back campaign with new competitive rates
- Stage: [08-CLOSED-LOST] (Note: [09-WIN-BACK] stage not available in pipeline)

---

RATE DEVELOPMENT STATUS

JIRA Ticket: RATE-1903
Status: COMPLETED 3:24 PM (Peer Review)
Delivered By: Taylar
Documentation: RATE-1903_Taylar_Response.md

Rate Improvements:
- Up to 11% savings vs current UPS rates
- Strategic rate reduction for competitive positioning
- Designed specifically for win-back campaign

---

FINANCIAL IMPACT

Deal Value: $7,100,000 annual revenue
Already Lost to UPS: $1.17M - $1.3M
Weekly Savings Opportunity: $52K - $58K
Monthly Savings: ~$220K - $250K
Annual Impact: $2.7M - $3M in customer savings

---

STRATEGIC ANALYSIS

Complete strategic analysis prepared for Nate including:
- Competitive positioning vs UPS rates
- Rate reduction justification and profitability analysis
- Win-back campaign approach and timing
- Financial projections and ROI
- Customer pain points and value proposition

---

NEXT STEPS

1. [DONE] RATE-1903 peer review complete
2. [PENDING] Schedule strategic presentation with Nate
3. [PENDING] Finalize win-back proposal approach
4. [PENDING] Prepare customer outreach campaign
5. [PENDING] Set follow-up cadence (monthly check-ins)

---

PRIORITY CLASSIFICATION

Priority Level: HIGH (Critical)
Deal Type: Win-Back
Urgency: CRITICAL - $7.1M opportunity
Campaign Status: Active - rates ready, awaiting strategic approval

---

SYSTEM NOTES

- Local folder: [08-CLOSED-LOST]_BoxiiShip AF
- Pipeline limitation: No [09-WIN-BACK] stage in HubSpot pipeline
- Workaround: Using [08-CLOSED-LOST] with WIN-BACK tag in notes
- Tracking: Monthly follow-ups via manual monitoring

---

CONTACT INFORMATION

Primary Contact: Make Wellness / BoxiiShip American Fork team
Decision Maker: [To be confirmed]
Last Contact: [To be updated]

This deal requires special tracking as an active win-back opportunity within the Closed-Lost stage.
"""

note_payload = {
    'properties': {
        'hs_note_body': note_content,
        'hs_timestamp': datetime.now().isoformat()
    }
}

# Create note
note_response = requests.post(
    'https://api.hubapi.com/crm/v3/objects/notes',
    headers=headers,
    json=note_payload
)

if note_response.status_code == 201:
    note_id = note_response.json()['id']
    print(f'   Note created (ID: {note_id})')

    # Associate note with deal
    print('   Associating note with deal...')
    association_response = requests.put(
        f'https://api.hubapi.com/crm/v3/objects/notes/{note_id}/associations/deals/{DEAL_ID}/note_to_deal',
        headers=headers
    )

    if association_response.status_code == 200:
        print('   Note associated with deal')
    else:
        print(f'   Warning: Could not associate note: {association_response.status_code}')
else:
    print(f'   Error creating note: {note_response.status_code}')
    print(note_response.text)

print()
print('=' * 80)
print('WIN-BACK MARKING COMPLETE')
print('=' * 80)
print()
print('Deal Status:')
print('  HubSpot Stage: [08-CLOSED-LOST]')
print('  Win-Back Status: ACTIVE (documented in notes)')
print('  Priority: HIGH')
print('  RATE-1903: COMPLETED')
print()
print('Important Notes:')
print('  - [09-WIN-BACK] stage does not exist in your HubSpot pipeline')
print('  - Using [08-CLOSED-LOST] with WIN-BACK documentation instead')
print('  - Deal requires manual tracking for monthly follow-ups')
print('  - Local folder [08-CLOSED-LOST]_BoxiiShip AF is correctly placed')
print()
print('Next Actions:')
print('  1. Schedule strategic presentation with Nate')
print('  2. Set monthly reminder for win-back follow-up')
print('  3. Consider creating [09-WIN-BACK] stage in HubSpot for future deals')
print()
print('=' * 80)
