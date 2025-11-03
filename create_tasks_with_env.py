#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create HubSpot Tasks for Monday Morning Priorities - October 27, 2025
Uses environment variable for API key (works with GitHub Secrets)
"""

import sys
import io
import os
import requests
from datetime import datetime, timedelta

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Configuration - Load from environment (SECURE)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)

OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

# Task definitions for this morning
MORNING_TASKS = [
    {
        "deal_name": "DYLN",
        "subject": "🚨 CRITICAL: Verify RATE-1907 status and send if overdue",
        "body": "RATE-1907 was due Oct 10 (now 17 days overdue). Check JIRA status, check HubSpot for rate delivery, search email sent to ship@dyln3pl.com. If rates exist but not sent: send immediately with apology. If rates don't exist: escalate to rate team NOW. Contact: Dorian Ayres <ship@dyln3pl.com>. Deal value: $3.6M annual, 24K packages/month.",
        "priority": "HIGH",
        "due_date": datetime.now(),
        "task_type": "EMAIL"
    },
    {
        "deal_name": "Josh's Frogs",
        "subject": "Follow up on Friday 10/25 meeting outcome",
        "body": "3 time slots were sent for Friday meeting. Check if meeting happened, was rescheduled, or no-show. If meeting happened: document outcomes and next steps. If no-show: send gentle follow-up. Deal value: $289K annual savings, 29,255 packages/month. Analysis file ready in deal folder.",
        "priority": "HIGH",
        "due_date": datetime.now(),
        "task_type": "EMAIL"
    },
    {
        "deal_name": "Upstate Prep",
        "subject": "Push for go-live date - deal at finish line! ($950K)",
        "body": "Moved to [06-IMPLEMENTATION] on Oct 23. Check setup docs status, verify integration testing progress, push for go-live date THIS WEEK. GOAL: Close as WON by end of week. This is $950K annual sitting at the finish line - don't let it stall.",
        "priority": "HIGH",
        "due_date": datetime.now(),
        "task_type": "TODO"
    },
    {
        "deal_name": "BoxiiShip",
        "subject": "Follow up on credit approval (OVERDUE - promised customer)",
        "body": "Promised customer update by 4:30 PM Oct 23. Check with Brock on credit approval status. If approved: email customer with next steps. If pending: email with timeline. If denied: call to discuss alternatives. Log all activity.",
        "priority": "HIGH",
        "due_date": datetime.now(),
        "task_type": "EMAIL"
    },
    {
        "deal_name": "Stackd Logistics",
        "subject": "Send ZIP code request email (draft ready)",
        "body": "Draft email ready in STACKD_ZIP_CODE_REQUEST_20251023.md. Send to Landon Richards <landon@stackdlogistics.com> requesting top 50-100 destination ZIPs for Select Network optimization. Create follow-up task for Nov 1.",
        "priority": "MEDIUM",
        "due_date": datetime.now(),
        "task_type": "EMAIL"
    },
    {
        "deal_name": "COLDEST",
        "subject": "Weekly proposal follow-up - Halloween urgency",
        "body": "Check last contact date. If >7 days since last touch, send follow-up email. Use Halloween deadline (Oct 31 = 4 days) for urgency. Peak season starts in 3 days - decision time. Track response in HubSpot.",
        "priority": "MEDIUM",
        "due_date": datetime.now() + timedelta(days=1),
        "task_type": "EMAIL"
    },
    {
        "deal_name": "Caputron",
        "subject": "Weekly proposal follow-up - 69+ days in stage",
        "body": "Deal value: $477K. 69+ days in [04-PROPOSAL-SENT]. Check last contact date. Send follow-up with Halloween urgency. This deal needs attention - risk of going stale. Consider calling if no email response.",
        "priority": "MEDIUM",
        "due_date": datetime.now() + timedelta(days=1),
        "task_type": "EMAIL"
    },
    {
        "deal_name": "IronLink Logistics NJ - Skupreme",
        "subject": "Weekly proposal follow-up - high value deal",
        "body": "Deal value: $233K annual savings, 68,589 packages/year. Check last contact date. Send follow-up email with Halloween deadline urgency. Track response.",
        "priority": "MEDIUM",
        "due_date": datetime.now() + timedelta(days=1),
        "task_type": "EMAIL"
    },
    {
        "deal_name": "ODW Logistics",
        "subject": "Weekly proposal follow-up",
        "body": "Check last contact date. If >7 days, send follow-up. Use peak season urgency messaging. Track response in HubSpot.",
        "priority": "MEDIUM",
        "due_date": datetime.now() + timedelta(days=1),
        "task_type": "EMAIL"
    },
    {
        "deal_name": "OTW Shipping",
        "subject": "Weekly proposal follow-up - 156+ days in stage (OVERDUE)",
        "body": "156+ days in [04-PROPOSAL-SENT] - VERY OVERDUE. Send follow-up email with strong urgency. Consider: Does this deal need to move to [09-WIN-BACK]? If no response in 7 days, reassess.",
        "priority": "MEDIUM",
        "due_date": datetime.now() + timedelta(days=1),
        "task_type": "EMAIL"
    },
    {
        "deal_name": "Team Shipper",
        "subject": "Weekly proposal follow-up - $500K opportunity",
        "body": "Deal value: $500K. Check last contact date. Send follow-up email. Use Halloween deadline for urgency. Track response.",
        "priority": "MEDIUM",
        "due_date": datetime.now() + timedelta(days=1),
        "task_type": "EMAIL"
    }
]


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
        print(f"  ❌ Error searching for {deal_name}: {response.text}")
        return None

    results = response.json().get("results", [])

    if not results:
        print(f"  ⚠️  No deal found for: {deal_name}")
        return None

    deal = results[0]
    deal_id = deal["id"]
    deal_name_found = deal["properties"]["dealname"]

    if len(results) > 1:
        print(f"  ℹ️  Found {len(results)} matches for '{deal_name}', using: {deal_name_found}")

    return deal_id


def create_task(deal_id, deal_name, subject, body, priority, due_date, task_type):
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

    response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/tasks",
        headers=headers,
        json=task_data
    )

    if response.status_code not in [200, 201]:
        print(f"  ❌ Failed to create task: {response.text}")
        return False

    task = response.json()
    task_id = task["id"]

    assoc_data = [{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 216
    }]

    assoc_response = requests.put(
        f"https://api.hubapi.com/crm/v4/objects/tasks/{task_id}/associations/deals/{deal_id}",
        headers=headers,
        json=assoc_data
    )

    if assoc_response.status_code not in [200, 201]:
        print(f"  ⚠️  Task created (ID: {task_id}) but failed to associate with deal")
        return True

    print(f"  ✅ Task created and associated (Task ID: {task_id})")
    return True


def main():
    print("\n" + "="*80)
    print("CREATING MONDAY MORNING TASKS - October 27, 2025")
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {'***' + API_KEY[-8:] if API_KEY else 'NOT SET'}")
    print("="*80 + "\n")

    if not API_KEY:
        print("❌ No API key available. Exiting.")
        sys.exit(1)

    success_count = 0
    fail_count = 0
    skip_count = 0

    for i, task_def in enumerate(MORNING_TASKS, 1):
        deal_name = task_def["deal_name"]
        print(f"[{i}/{len(MORNING_TASKS)}] Processing: {deal_name}")

        deal_id = search_deal_by_name(deal_name)

        if not deal_id:
            skip_count += 1
            print()
            continue

        print(f"  ℹ️  Found deal ID: {deal_id}")

        success = create_task(
            deal_id=deal_id,
            deal_name=deal_name,
            subject=task_def["subject"],
            body=task_def["body"],
            priority=task_def["priority"],
            due_date=task_def["due_date"],
            task_type=task_def["task_type"]
        )

        if success:
            success_count += 1
        else:
            fail_count += 1

        print()

    print("="*80)
    print("TASK CREATION SUMMARY")
    print("="*80)
    print(f"✅ Successfully created: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"⚠️  Skipped (deal not found): {skip_count}")
    print(f"📊 Total: {len(MORNING_TASKS)}")
    print()
    print("✅ All tasks created! Check your HubSpot task list.")
    print()


if __name__ == "__main__":
    main()
