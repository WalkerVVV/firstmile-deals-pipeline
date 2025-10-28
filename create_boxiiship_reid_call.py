#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Custom HubSpot Task - BoxiiShip Call with Reid
October 27, 2025 - 10 AM Tomorrow
"""

import sys
import io
import os
import requests
from datetime import datetime, timedelta

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("❌ HUBSPOT_API_KEY not in environment")
    sys.exit(1)

OWNER_ID = "699257003"

def search_deal_by_name(deal_name):
    """Search for deal by name and return deal ID"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [
                {"propertyName": "dealname", "operator": "CONTAINS_TOKEN", "value": deal_name},
                {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID}
            ]
        }],
        "properties": ["dealname", "dealstage", "hs_object_id"],
        "limit": 10
    }

    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/deals/search",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print(f"❌ Error searching for {deal_name}: {response.text}")
        return None

    results = response.json().get("results", [])

    if not results:
        print(f"⚠️  No deal found for: {deal_name}")
        print(f"Searched for deals containing: '{deal_name}'")
        return None

    deal = results[0]
    deal_id = deal["id"]
    deal_name_found = deal["properties"]["dealname"]

    print(f"✅ Found deal: {deal_name_found} (ID: {deal_id})")

    if len(results) > 1:
        print(f"ℹ️  Note: Found {len(results)} matches, using first one")
        for i, d in enumerate(results[:3], 1):
            print(f"   {i}. {d['properties']['dealname']}")

    return deal_id


def create_task(deal_id, subject, body, priority, due_date, task_type):
    """Create task and associate with deal"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    due_timestamp = int(due_date.timestamp() * 1000)

    task_data = {
        "properties": {
            "hs_task_subject": subject,
            "hs_task_body": body,
            "hs_task_type": task_type,
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": priority,
            "hubspot_owner_id": OWNER_ID,
            "hs_timestamp": due_timestamp
        }
    }

    print(f"\nCreating task...")
    print(f"  Subject: {subject}")
    print(f"  Type: {task_type}")
    print(f"  Due: {due_date.strftime('%Y-%m-%d %I:%M %p')}")

    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/tasks",
        headers=headers,
        json=task_data
    )

    if response.status_code not in [200, 201]:
        print(f"❌ Failed to create task: {response.text}")
        return False

    task = response.json()
    task_id = task["id"]
    print(f"✅ Task created (Task ID: {task_id})")

    # Associate task with deal
    assoc_data = [{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 216
    }]

    print(f"Associating task with deal...")

    assoc_response = requests.put(
        f"https://api.hubapi.com/crm/v4/objects/tasks/{task_id}/associations/deals/{deal_id}",
        headers=headers,
        json=assoc_data
    )

    if assoc_response.status_code not in [200, 201]:
        print(f"⚠️  Task created but failed to associate with deal: {assoc_response.text}")
        return True

    print(f"✅ Task associated with deal")
    return True


def main():
    print("\n" + "="*80)
    print("CREATE CUSTOM HUBSPOT TASK")
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

    # Task details
    deal_name = "BoxiiShip System Beauty"
    subject = "Call Reid at 10 AM - BoxiiShip System Beauty Logistics LLC"
    body = """Call Reid at 10 AM to discuss:
- BoxiiShip System Beauty Logistics LLC
- Follow up on account status
- Next steps for partnership

Contact: Reid
Company: BoxiiShip System Beauty Logistics LLC
"""
    priority = "HIGH"

    # Set due date to tomorrow at 10 AM
    tomorrow = datetime.now() + timedelta(days=1)
    due_date = tomorrow.replace(hour=10, minute=0, second=0, microsecond=0)

    task_type = "CALL"

    print(f"Task Details:")
    print(f"  Deal: {deal_name}")
    print(f"  Contact: Reid")
    print(f"  Action: {task_type}")
    print(f"  Due: {due_date.strftime('%A, %B %d at %I:%M %p')}")
    print()

    # Search for deal
    print(f"Searching for deal containing '{deal_name}'...")
    deal_id = search_deal_by_name(deal_name)

    if not deal_id:
        print("\n❌ Could not find deal. Exiting.")
        print("\nTip: Check deal name in HubSpot. Possible variations:")
        print("  - BoxiiShip System Beauty")
        print("  - BoxiiShip System Beauty TX")
        print("  - BoxiiShip System Beauty Logistics LLC")
        sys.exit(1)

    # Create task
    success = create_task(
        deal_id=deal_id,
        subject=subject,
        body=body,
        priority=priority,
        due_date=due_date,
        task_type=task_type
    )

    print("\n" + "="*80)
    if success:
        print("✅ SUCCESS! Task created and associated with deal.")
        print(f"\nCheck HubSpot:")
        print(f"  1. Go to Tasks")
        print(f"  2. Look for: '{subject}'")
        print(f"  3. Due: {due_date.strftime('%A, %B %d at %I:%M %p')}")
    else:
        print("❌ FAILED to create task. See errors above.")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
