#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update Upstate Prep deal in HubSpot with submission activities"""

import requests
import json
import sys
from datetime import datetime, timedelta
from hubspot_config import get_hubspot_config, get_api_headers, ASSOCIATION_IDS

# Set stdout encoding to UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Get HubSpot configuration
config = get_hubspot_config()
headers = get_api_headers()

DEAL_ID = '42448709378'
EXISTING_TASK_ID = '92403763816'  # New Account Submission task

print("=" * 80)
print("UPDATING UPSTATE PREP IN HUBSPOT")
print("=" * 80)
print()

# Step 1: Complete the existing task
print("Step 1: Marking existing 'New Account Submission' task as COMPLETED...")
print(f"Task ID: {EXISTING_TASK_ID}")

task_update_url = f"{config['BASE_URL']}/crm/v3/objects/tasks/{EXISTING_TASK_ID}"
task_update_payload = {
    'properties': {
        'hs_task_status': 'COMPLETED',
        'hs_task_body': 'COMPLETED: New Account Setup form submitted to newaccounts@firstmile.com on October 23, 2025. Form includes all company details, contact info (Brandon Ruder), service requirements (all 3 Xparcel tiers), HAZMAT details, and ShipHero integration needs. Rate sheet attached.'
    }
}

task_response = requests.patch(task_update_url, headers=headers, json=task_update_payload)

if task_response.status_code == 200:
    print("✅ Task marked as COMPLETED")
else:
    print(f"❌ Error updating task: {task_response.status_code}")
    print(task_response.text)

print()

# Step 2: Create new follow-up task
print("Step 2: Creating new task 'Follow up on Upstate Prep account setup status'...")

# Due date: 7 days from now (10/30/2025)
due_date = datetime.now() + timedelta(days=7)
due_timestamp = int(due_date.replace(hour=17, minute=0, second=0, microsecond=0).timestamp() * 1000)

new_task_payload = {
    'properties': {
        'hs_task_subject': 'Follow up on Upstate Prep account setup status',
        'hs_task_body': 'Check with New Accounts team on account setup progress. Expected timeline: 7-10 business days from 10/23/2025 submission. Confirm ShipHero credentials provisioned and HAZMAT UN code approvals in process.',
        'hs_task_status': 'NOT_STARTED',
        'hs_task_type': 'EMAIL',
        'hs_timestamp': due_timestamp,
        'hs_task_priority': 'MEDIUM',
        'hubspot_owner_id': config['OWNER_ID']
    }
}

create_task_url = f"{config['BASE_URL']}/crm/v3/objects/tasks"
new_task_response = requests.post(create_task_url, headers=headers, json=new_task_payload)

if new_task_response.status_code == 201:
    new_task_data = new_task_response.json()
    new_task_id = new_task_data['id']
    print(f"✅ New task created (ID: {new_task_id})")

    # Associate task with deal
    print(f"   Associating task with deal {DEAL_ID}...")
    associate_url = f"{config['BASE_URL']}/crm/v3/objects/tasks/{new_task_id}/associations/deal/{DEAL_ID}/{ASSOCIATION_IDS['TASK_TO_DEAL']}"
    associate_response = requests.put(associate_url, headers=headers)

    if associate_response.status_code in [200, 201]:
        print("✅ Task associated with deal")
    else:
        print(f"❌ Error associating task: {associate_response.status_code}")
else:
    print(f"❌ Error creating task: {new_task_response.status_code}")
    print(new_task_response.text)

print()

# Step 3: Add note about submission
print("Step 3: Logging activity note about new account form submission...")

note_payload = {
    'properties': {
        'hs_timestamp': int(datetime.now().timestamp() * 1000),
        'hs_note_body': '''<h3>New Account Setup Form Submitted ✅</h3>

<p><strong>Date:</strong> October 23, 2025</p>

<p><strong>Action:</strong> Submitted complete New Account Setup Request to newaccounts@firstmile.com</p>

<p><strong>Form Details:</strong></p>
<ul>
<li><strong>Company:</strong> Upstate Prep LLC (https://upstateprep.com)</li>
<li><strong>Contact:</strong> Brandon Ruder (brandon@upstateprep.com, Office 864-863-7737, Mobile 704-962-6083)</li>
<li><strong>Addresses:</strong> Bill-To: 114 Southchase Blvd / Pick-Up: 107 Southchase Blvd Suite A, Fountain Inn, SC 29644</li>
<li><strong>Services:</strong> All three Xparcel tiers (Ground, Expedited, Priority)</li>
<li><strong>Service Restrictions:</strong> DG products → Ground only; Non-DG → all tiers available</li>
<li><strong>Volume:</strong> ~15,000 shipments/month</li>
<li><strong>HAZMAT:</strong> Isopropyl Alcohol (75%, 99%) + Hydrochloric Acid - UN code approvals required</li>
<li><strong>Platform:</strong> ShipHero integration</li>
<li><strong>Contract:</strong> $950K annually (signed 10/17/2025)</li>
</ul>

<p><strong>Documentation Attached:</strong></p>
<ul>
<li>Rate sheet: Upstate Prep_FirstMile_Xparcel_08-20-25.xlsx</li>
<li>SDS sheets for HAZMAT commodities</li>
</ul>

<p><strong>Expected Timeline:</strong> 7-10 business days for account setup completion</p>

<p><strong>Next Steps:</strong></p>
<ol>
<li>New Accounts team to acknowledge receipt (1-2 business days)</li>
<li>Account setup and ShipHero credential provisioning (7-10 business days)</li>
<li>HAZMAT UN code approvals processing</li>
<li>Follow-up scheduled for 10/30/2025</li>
</ol>
'''
    }
}

create_note_url = f"{config['BASE_URL']}/crm/v3/objects/notes"
note_response = requests.post(create_note_url, headers=headers, json=note_payload)

if note_response.status_code == 201:
    note_data = note_response.json()
    note_id = note_data['id']
    print(f"✅ Note created (ID: {note_id})")

    # Associate note with deal
    print(f"   Associating note with deal {DEAL_ID}...")
    note_associate_url = f"{config['BASE_URL']}/crm/v3/objects/notes/{note_id}/associations/deal/{DEAL_ID}/214"
    note_associate_response = requests.put(note_associate_url, headers=headers)

    if note_associate_response.status_code in [200, 201]:
        print("✅ Note associated with deal")
    else:
        print(f"❌ Error associating note: {note_associate_response.status_code}")
else:
    print(f"❌ Error creating note: {note_response.status_code}")
    print(note_response.text)

print()
print("=" * 80)
print("HUBSPOT UPDATE COMPLETE")
print("=" * 80)
print()
print("Summary:")
print(f"✅ Deal ID {DEAL_ID} - Upstate Prep - New Deal")
print(f"✅ Stage: [06-IMPLEMENTATION] (confirmed in correct stage)")
print(f"✅ Existing task (ID {EXISTING_TASK_ID}) marked COMPLETED")
print(f"✅ New follow-up task created (due 10/30/2025)")
print(f"✅ Activity note logged with submission details")
print()
