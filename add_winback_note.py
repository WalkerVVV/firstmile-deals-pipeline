#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add WIN-BACK documentation note to BoxiiShip deal"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
from datetime import datetime
import time

API_KEY = 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'
DEAL_ID = '36466918934'  # BoxiiShip American Fork

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

print('Adding WIN-BACK documentation note...')

# Use Unix timestamp in milliseconds
timestamp_ms = int(time.time() * 1000)

note_content = f"""WIN-BACK OPPORTUNITY - ACTIVE CAMPAIGN

Deal Status: [08-CLOSED-LOST] with ACTIVE WIN-BACK
Update Date: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
Updated By: Brett Walker

---

WIN-BACK CONTEXT

This is an ACTIVE WIN-BACK opportunity for BoxiiShip American Fork / Make Wellness.

Status Timeline:
- Previously: Active customer
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

- Deal name updated to include "WIN-BACK" designation
- Local folder: [08-CLOSED-LOST]_BoxiiShip AF
- Pipeline limitation: No [09-WIN-BACK] stage in HubSpot pipeline
- Workaround: Using [08-CLOSED-LOST] with WIN-BACK tag in title and notes
- Tracking: Monthly follow-ups via manual monitoring

This deal requires special tracking as an active win-back opportunity within the Closed-Lost stage.
"""

note_payload = {
    'properties': {
        'hs_note_body': note_content,
        'hs_timestamp': timestamp_ms
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
    print(f'Note created (ID: {note_id})')

    # Associate note with deal
    print('Associating note with deal...')
    association_response = requests.put(
        f'https://api.hubapi.com/crm/v3/objects/notes/{note_id}/associations/deals/{DEAL_ID}/note_to_deal',
        headers=headers
    )

    if association_response.status_code == 200:
        print('Note associated with deal successfully')
        print()
        print('WIN-BACK documentation complete!')
    else:
        print(f'Warning: Could not associate note: {association_response.status_code}')
else:
    print(f'Error creating note: {note_response.status_code}')
    print(note_response.text)
