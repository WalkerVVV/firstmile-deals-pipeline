#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily 9am Pipeline Sync Flow
Verifies EMAIL tasks exist for priority stages and creates missing ones
"""

import sys
import io
import os
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from dotenv import load_dotenv

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment (SECURE)
API_KEY = os.environ.get("HUBSPOT_API_KEY")
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)
OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

# Priority Stages to Monitor
PRIORITY_STAGES = {
    "1090865183": "[03-RATE-CREATION]",  # 2-week follow-up
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",  # 30-day follow-up
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]"  # Setup docs sent
}

# Task Templates by Stage
TASK_TEMPLATES = {
    "[03-RATE-CREATION]": {
        "subject": "Follow up on rate creation",
        "body": "Check status of rate creation and proposal development",
        "priority": "HIGH",
        "due_days": 14
    },
    "[04-PROPOSAL-SENT]": {
        "subject": "Follow up on proposal",
        "body": "Check if customer has reviewed proposal and answer any questions",
        "priority": "HIGH",
        "due_days": 30
    },
    "[06-IMPLEMENTATION]": {
        "subject": "Implementation check-in",
        "body": "Verify setup docs received and onboarding progress",
        "priority": "MEDIUM",
        "due_days": 14
    }
}

def fetch_priority_deals():
    """Fetch deals in priority stages"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [
                {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
                {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID},
                {"propertyName": "dealstage", "operator": "IN", "values": list(PRIORITY_STAGES.keys())}
            ]
        }],
        "properties": ["dealname", "dealstage", "hs_object_id"],
        "limit": 100
    }

    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/deals/search",
        headers=headers,
        json=payload
    )

    if response.status_code != 200:
        print(f"❌ Error fetching deals: {response.text}")
        return []

    return response.json()["results"]

def get_deal_tasks(deal_id):
    """Get all tasks associated with a deal"""
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(
        f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}/associations/tasks",
        headers=headers
    )

    if response.status_code != 200:
        return []

    task_associations = response.json().get("results", [])

    # Fetch task details
    tasks = []
    for assoc in task_associations:
        task_id = assoc["id"]
        task_response = requests.get(
            f"https://api.hubapi.com/crm/v3/objects/tasks/{task_id}",
            headers=headers,
            params={"properties": "hs_task_subject,hs_task_type,hs_task_status"}
        )

        if task_response.status_code == 200:
            tasks.append(task_response.json())

    return tasks

def create_email_task(deal_id, deal_name, stage_name):
    """Create EMAIL task for a deal"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    template = TASK_TEMPLATES.get(stage_name, TASK_TEMPLATES["[04-PROPOSAL-SENT]"])

    # Calculate due date
    due_date = datetime.now() + timedelta(days=template["due_days"])
    due_timestamp = int(due_date.timestamp() * 1000)

    task_data = {
        "properties": {
            "hs_task_subject": f"{template['subject']} - {deal_name}",
            "hs_task_body": template["body"],
            "hs_task_type": "EMAIL",
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": template["priority"],
            "hubspot_owner_id": OWNER_ID,
            "hs_timestamp": due_timestamp
        }
    }

    # Create task
    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/tasks",
        headers=headers,
        json=task_data
    )

    if response.status_code not in [200, 201]:
        print(f"  ❌ Failed to create task: {response.text}")
        return None

    task = response.json()
    task_id = task["id"]

    # Associate task with deal using v4 API
    assoc_data = [{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 216  # Task to Deal association type
    }]

    assoc_response = requests.put(
        f"https://api.hubapi.com/crm/v4/objects/tasks/{task_id}/associations/deals/{deal_id}",
        headers=headers,
        json=assoc_data
    )

    if assoc_response.status_code not in [200, 201]:
        print(f"  ⚠️  Task created but failed to associate: {assoc_response.text}")
        return task_id

    return task_id

def main():
    print("\n" + "="*80)
    print("DAILY 9AM PIPELINE SYNC - EMAIL TASK VERIFICATION")
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

    # Fetch priority deals
    print("[1/3] Fetching deals in priority stages...")
    deals = fetch_priority_deals()
    print(f"✅ Found {len(deals)} deals in priority stages\n")

    if not deals:
        print("✅ No deals in priority stages. Pipeline sync complete.\n")
        return

    # Group by stage
    by_stage = defaultdict(list)
    for deal in deals:
        stage_id = deal["properties"]["dealstage"]
        stage_name = PRIORITY_STAGES.get(stage_id, f"[UNKNOWN-{stage_id[:8]}]")
        by_stage[stage_name].append(deal)

    # Verify tasks
    print("[2/3] Verifying EMAIL tasks exist...")
    missing_tasks = []

    for stage_name, stage_deals in by_stage.items():
        print(f"\n{stage_name} ({len(stage_deals)} deals):")

        for deal in stage_deals:
            deal_id = deal["id"]
            deal_name = deal["properties"]["dealname"]

            tasks = get_deal_tasks(deal_id)
            email_tasks = [t for t in tasks if t["properties"].get("hs_task_type") == "EMAIL"]

            if not email_tasks:
                print(f"  ⚠️  {deal_name} - NO EMAIL TASK")
                missing_tasks.append((deal_id, deal_name, stage_name))
            else:
                print(f"  ✅ {deal_name} - {len(email_tasks)} EMAIL task(s)")

    # Create missing tasks
    if missing_tasks:
        print(f"\n[3/3] Creating {len(missing_tasks)} missing EMAIL tasks...")
        created_count = 0

        for deal_id, deal_name, stage_name in missing_tasks:
            task_id = create_email_task(deal_id, deal_name, stage_name)
            if task_id:
                print(f"  ✅ Created EMAIL task for: {deal_name}")
                created_count += 1
            else:
                print(f"  ❌ Failed to create task for: {deal_name}")

        print(f"\n📊 Created {created_count}/{len(missing_tasks)} tasks")
    else:
        print("\n[3/3] All deals have EMAIL tasks ✅")

    # Summary
    print("\n" + "="*80)
    print("SYNC SUMMARY")
    print("="*80)
    print(f"Priority Deals Checked: {len(deals)}")
    print(f"Missing Tasks Found:    {len(missing_tasks)}")
    print(f"Tasks Created:          {len(missing_tasks) if missing_tasks else 0}")
    print("\n✅ Daily 9am sync complete")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
