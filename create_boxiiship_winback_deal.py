#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Create NEW BoxiiShip AF Win-Back Deal (proper approach)"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
from datetime import datetime
import time

API_KEY = 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'
OWNER_ID = '699257003'
PIPELINE_ID = '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'
ORIGINAL_DEAL_ID = '36466918934'  # Original closed-lost deal

# Stage IDs (verified 2025-10-10)
PROPOSAL_SENT_STAGE = 'd607df25-2c6d-4a5d-9835-6ed1e4f4020a'  # [04-PROPOSAL-SENT]
CLOSED_LOST_STAGE = '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8'   # [08-CLOSED-LOST]

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

print('=' * 80)
print('CREATING NEW WIN-BACK DEAL - PROPER APPROACH')
print('=' * 80)
print()

# Step 1: Revert original deal
print('Step 1: Reverting original deal to historical state...')
print(f'  Deal ID: {ORIGINAL_DEAL_ID}')

revert_payload = {
    'properties': {
        'dealname': 'BoxiiShip- American Fork',
        'dealstage': CLOSED_LOST_STAGE
    }
}

response = requests.patch(
    f'https://api.hubapi.com/crm/v3/objects/deals/{ORIGINAL_DEAL_ID}',
    headers=headers,
    json=revert_payload
)

if response.status_code == 200:
    print('  ✓ Original deal reverted')
    print('    - Name: BoxiiShip- American Fork')
    print('    - Stage: [08] Closed Lost')
else:
    print(f'  Error: {response.status_code}')
    print(response.text)

print()

# Step 2: Add note to original deal explaining the loss
print('Step 2: Documenting original deal loss...')

timestamp_ms = int(time.time() * 1000)

loss_note = f"""DEAL CLOSED-LOST - Historical Record

Date Lost: 2024 (estimated)
Lost To: UPS
Reason: [To be documented]

---

IMPORTANT: This deal remains as historical record only.

A NEW WIN-BACK DEAL has been created to track re-engagement efforts.
The win-back campaign is a separate deal with:
- New rate analysis (RATE-1903)
- Fresh discovery and strategy
- Current 2025 competitive positioning

Do not update this deal. All win-back activity is tracked in the new deal.

---

Historical Context:
- Annual Value: $7.1M
- Service: Xparcel shipping
- Lost revenue to date: $1.17M - $1.3M

Win-back opportunity: $52K-$58K/week in customer savings vs current UPS rates.

---

Updated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
"""

loss_note_payload = {
    'properties': {
        'hs_note_body': loss_note,
        'hs_timestamp': timestamp_ms
    }
}

note_response = requests.post(
    'https://api.hubapi.com/crm/v3/objects/notes',
    headers=headers,
    json=loss_note_payload
)

if note_response.status_code == 201:
    note_id = note_response.json()['id']
    print(f'  ✓ Loss documentation note created (ID: {note_id})')

    # Associate with original deal
    requests.put(
        f'https://api.hubapi.com/crm/v3/objects/notes/{note_id}/associations/deals/{ORIGINAL_DEAL_ID}/note_to_deal',
        headers=headers
    )
    print('    Associated with original deal')
else:
    print(f'  Error: {note_response.status_code}')

print()

# Step 3: Create NEW win-back deal
print('Step 3: Creating NEW win-back deal...')

new_deal_payload = {
    'properties': {
        'dealname': 'BoxiiShip American Fork - WIN-BACK CAMPAIGN 2025',
        'dealstage': PROPOSAL_SENT_STAGE,  # Start at [04] since RATE-1903 is complete
        'amount': '7200000',
        'pipeline': PIPELINE_ID,
        'hubspot_owner_id': OWNER_ID,
        'hs_priority': 'high',
        'closedate': ''  # Leave open
    }
}

deal_response = requests.post(
    'https://api.hubapi.com/crm/v3/objects/deals',
    headers=headers,
    json=new_deal_payload
)

if deal_response.status_code == 201:
    new_deal_id = deal_response.json()['id']
    print(f'  ✓ NEW deal created!')
    print(f'    Deal ID: {new_deal_id}')
    print(f'    Name: BoxiiShip American Fork - WIN-BACK CAMPAIGN 2025')
    print(f'    Stage: [04] Proposal Sent')
    print(f'    Amount: $7,200,000')
    print(f'    Priority: HIGH')

    print()

    # Step 4: Add comprehensive win-back note to NEW deal
    print('Step 4: Adding win-back campaign documentation...')

    winback_note = f"""WIN-BACK CAMPAIGN 2025 - Active Engagement

Campaign Start: October 2025
Original Deal: ID {ORIGINAL_DEAL_ID} (BoxiiShip- American Fork)
Current Stage: [04] Proposal Sent - RATE-1903 Complete
Priority: HIGH - Critical $7.1M opportunity

---

CAMPAIGN STRATEGY

Objective: Re-engage BoxiiShip American Fork / Make Wellness with competitive rates
Competitor: UPS (current carrier)
Lost Revenue YTD: $1.17M - $1.3M
Win-back Value Proposition: $52K - $58K/week in savings ($2.7M - $3M annually)

---

RATE DEVELOPMENT STATUS

JIRA Ticket: RATE-1903
Status: ✅ COMPLETED (Peer Review)
Delivered By: Taylar
Completion: October 9, 2025 at 3:24 PM
Documentation: RATE-1903_Taylar_Response.md

Rate Improvements:
- Up to 11% savings vs current UPS rates
- Competitive positioning specifically for win-back
- Strategic rate design for Make Wellness volume profile

---

FINANCIAL IMPACT ANALYSIS

Annual Revenue Opportunity: $7,100,000
Customer Current Spend: $7.1M/year with UPS
Customer Potential Savings: $2.7M - $3M annually with FirstMile
Weekly Savings: $52K - $58K
Monthly Savings: $220K - $250K

FirstMile Revenue Impact:
- Immediate: $7.1M annual contract value
- Lost opportunity cost: $1.17M - $1.3M (already lost to UPS)
- Market positioning: Win-back from major competitor

---

STRATEGIC APPROACH

Phase 1: Rate Development ✅ COMPLETE
- RATE-1903 completed with peer review
- Competitive analysis vs UPS rates
- Up to 11% savings demonstrated

Phase 2: Internal Approval (CURRENT)
- [ ] Strategic presentation to Nate
- [ ] Review win-back approach and profitability
- [ ] Approve customer outreach strategy

Phase 3: Customer Engagement (PENDING)
- [ ] Identify primary decision maker
- [ ] Schedule re-engagement meeting
- [ ] Present competitive rate comparison
- [ ] Address objections from previous loss

Phase 4: Proposal & Close (PENDING)
- [ ] Formal proposal delivery
- [ ] Negotiation and objection handling
- [ ] Contract execution
- [ ] Implementation planning

---

WIN-BACK CAMPAIGN NOTES

Why We Lost Originally:
- [To be documented from original deal analysis]
- Lost to UPS
- Timing, pricing, or service concerns

Why We Can Win Now:
- Competitive rates (11% savings vs UPS)
- Proven service track record since loss
- Strong financial case for customer
- Market conditions may have changed

Risks & Mitigation:
- Customer satisfaction with UPS: Position as cost optimization, not service issue
- Decision maker change: Re-qualify contacts and buying process
- Contract lock-in: Understand UPS contract terms and renewal dates

---

NEXT ACTIONS

Immediate (This Week):
1. [ ] Schedule strategic presentation with Nate
2. [ ] Get approval for win-back approach
3. [ ] Confirm profitability at proposed rates

Short-term (Next 2 Weeks):
4. [ ] Research current BoxiiShip contacts and decision makers
5. [ ] Understand UPS contract status and renewal timing
6. [ ] Prepare customer-facing materials

Follow-up Cadence:
- Internal: Weekly check-ins on approval process
- Customer: TBD after internal approval

---

LOCAL FOLDER STRUCTURE

Original Deal Folder: [08-CLOSED-LOST]_BoxiiShip AF/
- Historical PLD analysis
- Original rates and proposals
- Loss analysis

Win-Back Campaign Folder: [09-WIN-BACK]_BoxiiShip_AF_2025/
- RATE-1903_Taylar_Response.md
- Strategic analysis for Nate
- Win-back campaign materials
- New competitive analysis

---

CROSS-REFERENCES

Original Closed-Lost Deal: {ORIGINAL_DEAL_ID}
Win-Back Deal: {new_deal_id} (this deal)

Link between deals maintains historical context while tracking new campaign separately.

---

Campaign Created: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
Created By: Brett Walker
System: Nebuchadnezzar v2.0
"""

    winback_note_payload = {
        'properties': {
            'hs_note_body': winback_note,
            'hs_timestamp': int(time.time() * 1000)
        }
    }

    wb_note_response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/notes',
        headers=headers,
        json=winback_note_payload
    )

    if wb_note_response.status_code == 201:
        wb_note_id = wb_note_response.json()['id']
        print(f'  ✓ Win-back documentation created (ID: {wb_note_id})')

        # Associate with new deal
        requests.put(
            f'https://api.hubapi.com/crm/v3/objects/notes/{wb_note_id}/associations/deals/{new_deal_id}/note_to_deal',
            headers=headers
        )
        print('    Associated with new deal')
    else:
        print(f'  Error: {wb_note_response.status_code}')

    print()
    print('=' * 80)
    print('WIN-BACK DEAL CREATION COMPLETE')
    print('=' * 80)
    print()
    print('Original Deal:')
    print(f'  ID: {ORIGINAL_DEAL_ID}')
    print('  Name: BoxiiShip- American Fork')
    print('  Stage: [08] Closed Lost')
    print('  Status: Historical record')
    print()
    print('NEW Win-Back Deal:')
    print(f'  ID: {new_deal_id}')
    print('  Name: BoxiiShip American Fork - WIN-BACK CAMPAIGN 2025')
    print('  Stage: [04] Proposal Sent')
    print('  Amount: $7,200,000')
    print('  Priority: HIGH')
    print()
    print('Next Steps:')
    print('  1. Create local folder: [09-WIN-BACK]_BoxiiShip_AF_2025/')
    print('  2. Move RATE-1903 materials to new folder')
    print('  3. Schedule strategic presentation with Nate')
    print('  4. Update 9AM sync to track this new deal')
    print()
    print('=' * 80)

else:
    print(f'  Error creating deal: {deal_response.status_code}')
    print(deal_response.text)
