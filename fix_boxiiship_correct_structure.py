#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix BoxiiShip structure - they're an ACTIVE CUSTOMER, not closed-lost"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
from datetime import datetime
import time

API_KEY = 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'
ORIGINAL_DEAL_ID = '36466918934'  # BoxiiShip AF customer deal
WINBACK_DEAL_ID = '45692064076'   # Make Wellness volume win-back

# Stage IDs (verified 2025-10-10)
STARTED_SHIPPING_STAGE = '3fd46d94-78b4-452b-8704-62a338a210fb'  # [07-STARTED-SHIPPING]
PROPOSAL_SENT_STAGE = 'd607df25-2c6d-4a5d-9835-6ed1e4f4020a'     # [04-PROPOSAL-SENT]

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

print('=' * 80)
print('CORRECTING BOXIISHIP STRUCTURE - ACTIVE CUSTOMER')
print('=' * 80)
print('Date: October 10, 2025, 12:06 PM')
print()
print('Issue: BoxiiShip AF is ACTIVE CUSTOMER (3PL), not closed-lost')
print('Context: Lost Make Wellness volume to UPS, but still our customer')
print()

# Step 1: Fix original customer deal
print('Step 1: Correcting original customer deal...')
print(f'  Deal ID: {ORIGINAL_DEAL_ID}')

customer_payload = {
    'properties': {
        'dealname': 'BoxiiShip American Fork - 3PL Customer',
        'dealstage': STARTED_SHIPPING_STAGE
    }
}

response = requests.patch(
    f'https://api.hubapi.com/crm/v3/objects/deals/{ORIGINAL_DEAL_ID}',
    headers=headers,
    json=customer_payload
)

if response.status_code == 200:
    print('  ✓ Customer deal corrected')
    print('    - Name: BoxiiShip American Fork - 3PL Customer')
    print('    - Stage: [07] Started Shipping (ACTIVE)')
else:
    print(f'  Error: {response.status_code}')
    print(response.text)

print()

# Step 2: Update customer deal note
print('Step 2: Updating customer deal context...')

timestamp_ms = int(time.time() * 1000)

customer_note = f"""ACTIVE 3PL CUSTOMER - Make Wellness Volume Lost

Deal Status: [07] Started Shipping - ACTIVE CUSTOMER
Customer Type: 3PL (Third-Party Logistics)
Update: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}

---

CUSTOMER CONTEXT

BoxiiShip American Fork is an ACTIVE FirstMile customer operating as a 3PL.

Business Model:
- BoxiiShip AF = 3PL provider (OUR CUSTOMER)
- Make Wellness = BoxiiShip's customer (end shipper)
- FirstMile = Carrier for BoxiiShip's customers

Revenue Flow:
Make Wellness (shipper) → BoxiiShip AF (3PL) → FirstMile (carrier)

---

MAKE WELLNESS VOLUME LOSS

Issue: Make Wellness moved $7.2M annual volume to UPS directly
Impact: Lost volume from our 3PL customer BoxiiShip AF
Competitor: UPS (bypassing BoxiiShip AF)
Annual Value: $7,200,000

Customer Savings Opportunity: $52K-$58K/week if back with FirstMile

---

WIN-BACK CAMPAIGN

A SEPARATE WIN-BACK DEAL has been created to track Make Wellness re-engagement:

Win-Back Deal ID: {WINBACK_DEAL_ID}
Deal Name: BoxiiShip AF - Make Wellness Volume WIN-BACK 2025
Stage: [04] Proposal Sent
Target: Get Make Wellness volume back to BoxiiShip AF (who uses FirstMile)

---

IMPORTANT NOTES

1. BoxiiShip AF remains ACTIVE FirstMile customer
2. This deal tracks ongoing 3PL customer relationship
3. Make Wellness win-back is tracked in separate deal
4. BoxiiShip AF likely still shipping other customer volumes with us

---

Local Folder Structure:
- Main: Customer-BoxiiShip_AF/
- Win-Back: Customer-BoxiiShip_AF/Win-Back_Make_Wellness_2025/

---

Updated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
Clarification: Active customer, not closed-lost
"""

customer_note_payload = {
    'properties': {
        'hs_note_body': customer_note,
        'hs_timestamp': timestamp_ms
    }
}

note_response = requests.post(
    'https://api.hubapi.com/crm/v3/objects/notes',
    headers=headers,
    json=customer_note_payload
)

if note_response.status_code == 201:
    note_id = note_response.json()['id']
    print(f'  ✓ Customer context note created (ID: {note_id})')

    # Associate with customer deal
    requests.put(
        f'https://api.hubapi.com/crm/v3/objects/notes/{note_id}/associations/deals/{ORIGINAL_DEAL_ID}/note_to_deal',
        headers=headers
    )
    print('    Associated with customer deal')
else:
    print(f'  Error: {note_response.status_code}')

print()

# Step 3: Update win-back deal name for clarity
print('Step 3: Clarifying win-back deal name...')
print(f'  Deal ID: {WINBACK_DEAL_ID}')

winback_payload = {
    'properties': {
        'dealname': 'BoxiiShip AF - Make Wellness Volume WIN-BACK 2025'
    }
}

response = requests.patch(
    f'https://api.hubapi.com/crm/v3/objects/deals/{WINBACK_DEAL_ID}',
    headers=headers,
    json=winback_payload
)

if response.status_code == 200:
    print('  ✓ Win-back deal name clarified')
    print('    - Name: BoxiiShip AF - Make Wellness Volume WIN-BACK 2025')
    print('    - Stage: [04] Proposal Sent (unchanged)')
else:
    print(f'  Error: {response.status_code}')
    print(response.text)

print()

# Step 4: Add clarification note to win-back deal
print('Step 4: Adding clarification to win-back deal...')

winback_clarification = f"""WIN-BACK CAMPAIGN - Make Wellness Volume

Campaign Target: Make Wellness (end shipper)
Parent Customer: BoxiiShip American Fork (3PL) - ACTIVE CUSTOMER
Customer Deal ID: {ORIGINAL_DEAL_ID}
Win-Back Deal ID: {WINBACK_DEAL_ID}

---

BUSINESS CONTEXT CLARIFICATION

BoxiiShip American Fork = ACTIVE FirstMile customer (3PL)
Make Wellness = BoxiiShip's customer (the actual shipper)
Lost To: UPS (Make Wellness went direct to UPS, bypassing BoxiiShip)

Goal: Get Make Wellness volume back to BoxiiShip AF, who will use FirstMile

---

REVENUE STRUCTURE

Current Flow (Lost):
Make Wellness → UPS (direct)

Target Flow (Win-Back):
Make Wellness → BoxiiShip AF (3PL) → FirstMile (carrier)

Annual Value: $7,200,000 (Make Wellness volume through BoxiiShip)

---

WIN-BACK CAMPAIGN STATUS

RATE-1903: ✅ COMPLETED (October 9, 2025)
Delivered By: Taylar (peer review complete)
Rate Advantage: Up to 11% savings vs UPS
Customer Savings: $52K-$58K/week

Current Stage: [04] Proposal Sent
Next Step: Strategic presentation to Nate for approval

---

PARENT CUSTOMER RELATIONSHIP

BoxiiShip AF Customer Status: ACTIVE (Deal {ORIGINAL_DEAL_ID})
BoxiiShip AF Stage: [07] Started Shipping
Impact on BoxiiShip: Lost significant customer volume (Make Wellness)
BoxiiShip Interest: High - wants to win back their customer

This win-back benefits both:
1. FirstMile: $7.2M annual revenue opportunity
2. BoxiiShip AF: Regain their customer Make Wellness

---

LOCAL FOLDER STRUCTURE

Customer Folder: Customer-BoxiiShip_AF/
Win-Back Subfolder: Customer-BoxiiShip_AF/Win-Back_Make_Wellness_2025/

RATE-1903 and all win-back materials should be in the win-back subfolder.

---

Updated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
Clarification: Make Wellness volume win-back for active customer BoxiiShip AF
"""

wb_note_payload = {
    'properties': {
        'hs_note_body': winback_clarification,
        'hs_timestamp': int(time.time() * 1000)
    }
}

wb_response = requests.post(
    'https://api.hubapi.com/crm/v3/objects/notes',
    headers=headers,
    json=wb_note_payload
)

if wb_response.status_code == 201:
    wb_note_id = wb_response.json()['id']
    print(f'  ✓ Clarification note created (ID: {wb_note_id})')

    # Associate with win-back deal
    requests.put(
        f'https://api.hubapi.com/crm/v3/objects/notes/{wb_note_id}/associations/deals/{WINBACK_DEAL_ID}/note_to_deal',
        headers=headers
    )
    print('    Associated with win-back deal')
else:
    print(f'  Error: {wb_response.status_code}')

print()
print('=' * 80)
print('STRUCTURE CORRECTION COMPLETE')
print('=' * 80)
print()
print('Customer Deal (Active 3PL):')
print(f'  ID: {ORIGINAL_DEAL_ID}')
print('  Name: BoxiiShip American Fork - 3PL Customer')
print('  Stage: [07] Started Shipping (ACTIVE)')
print()
print('Win-Back Deal (Make Wellness Volume):')
print(f'  ID: {WINBACK_DEAL_ID}')
print('  Name: BoxiiShip AF - Make Wellness Volume WIN-BACK 2025')
print('  Stage: [04] Proposal Sent')
print('  Target: Get Make Wellness back to BoxiiShip (who uses FirstMile)')
print()
print('Local Folder Structure:')
print('  1. Rename: [08-CLOSED-LOST]_BoxiiShip AF')
print('     To: Customer-BoxiiShip_AF')
print()
print('  2. Create subfolder: Customer-BoxiiShip_AF/Win-Back_Make_Wellness_2025/')
print()
print('  3. Move RATE-1903 materials to win-back subfolder')
print()
print('Next Steps:')
print('  - Schedule presentation with Nate')
print('  - Organize customer folder and win-back subfolder')
print('  - Track both deals in 9AM sync')
print()
print('=' * 80)
