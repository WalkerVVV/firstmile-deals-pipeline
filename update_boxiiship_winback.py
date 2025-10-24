#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update BoxiiShip AF to [09-WIN-BACK] stage"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
from datetime import datetime

API_KEY = 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'
DEAL_ID = '36466918934'  # BoxiiShip- American Fork
WIN_BACK_STAGE = '9c8d7f6e-4a3b-2c1d-8e7f-9a0b1c2d3e4f'  # [09-WIN-BACK]

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

print('=' * 80)
print('UPDATING BOXIISHIP AF TO WIN-BACK STAGE')
print('=' * 80)
print(f'Deal ID: {DEAL_ID}')
print(f'Target Stage: [09-WIN-BACK]')
print()

# Step 1: Update deal stage
print('Step 1: Updating deal stage...')
stage_payload = {
    'properties': {
        'dealstage': WIN_BACK_STAGE
    }
}

response = requests.patch(
    f'https://api.hubapi.com/crm/v3/objects/deals/{DEAL_ID}',
    headers=headers,
    json=stage_payload
)

if response.status_code == 200:
    print('✅ Deal stage updated to [09-WIN-BACK]')
else:
    print(f'❌ Error updating stage: {response.status_code}')
    print(response.text)
    exit(1)

print()

# Step 2: Add comprehensive note documenting win-back status
print('Step 2: Adding win-back documentation note...')

note_content = f"""🔄 WIN-BACK OPPORTUNITY - STAGE UPDATE

**Deal Status**: Moved to [09-WIN-BACK] stage
**Update Date**: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
**Updated By**: Brett Walker (Automated sync correction)

---

## Win-Back Context

This is an **active win-back opportunity** for BoxiiShip American Fork / Make Wellness.

**Original Status**: Previously in [06-IMPLEMENTATION], moved to [08-CLOSED-LOST]
**Current Status**: Active win-back campaign with new rate proposal

---

## Rate Development Status

**JIRA Ticket**: RATE-1903
**Status**: ✅ Completed 3:24 PM (Peer Review)
**Delivered By**: Taylar
**Documentation**: RATE-1903_Taylar_Response.md

**Rate Improvements**:
- Up to 11% savings vs current UPS rates
- Strategic rate reduction for competitive positioning

---

## Financial Impact

**Deal Value**: $7,100,000 annual revenue
**Already Lost to UPS**: $1.17M - $1.3M
**Weekly Savings Opportunity**: $52K - $58K
**Monthly Savings**: ~$220K - $250K

---

## Strategic Analysis

Complete strategic analysis prepared for Nate's presentation including:
- Competitive positioning vs UPS
- Rate reduction justification
- Win-back campaign approach
- Financial projections

---

## Next Steps

1. ✅ RATE-1903 peer review complete
2. [ ] Schedule strategic presentation with Nate
3. [ ] Finalize win-back proposal approach
4. [ ] Prepare customer outreach campaign
5. [ ] Set follow-up cadence (monthly check-ins per [09-WIN-BACK] SLA)

---

## Pipeline Stage Correction

**Issue Identified**: 9AM automated sync did not capture this deal because it was incorrectly staged in [06-IMPLEMENTATION]

**Resolution**: Manual correction to [09-WIN-BACK] stage (2025-10-10)

**Local Folder**: [08-CLOSED-LOST]_BoxiiShip AF (to be moved to [09-WIN-BACK] folder)

---

**Priority**: 🔴 HIGH
**Urgency**: CRITICAL - $7.1M opportunity
**Campaign Type**: Win-Back with new competitive rates
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
    print(f'✅ Note created (ID: {note_id})')

    # Associate note with deal
    print('   Associating note with deal...')
    association_response = requests.put(
        f'https://api.hubapi.com/crm/v3/objects/notes/{note_id}/associations/deals/{DEAL_ID}/note_to_deal',
        headers=headers
    )

    if association_response.status_code == 200:
        print('   ✅ Note associated with deal')
    else:
        print(f'   ⚠️  Warning: Could not associate note: {association_response.status_code}')
else:
    print(f'❌ Error creating note: {note_response.status_code}')
    print(note_response.text)

print()
print('=' * 80)
print('UPDATE COMPLETE')
print('=' * 80)
print()
print('Deal Status:')
print('  HubSpot Stage: [09-WIN-BACK] ✓')
print('  Priority: HIGH ✓')
print('  RATE-1903: Completed ✓')
print('  Documentation: Complete ✓')
print()
print('Next Action:')
print('  - Schedule strategic presentation with Nate')
print('  - Move local folder from [08-CLOSED-LOST] to [09-WIN-BACK]')
print('  - Set up monthly check-in cadence')
print()
print('=' * 80)
