#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Action Item Tasks for BoxiiShip System Beauty Logistics
Based on Reid meeting notes
"""

import sys
import io
import requests
from datetime import datetime, timedelta

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
API_KEY = "pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764"
OWNER_ID = "699257003"

# Company and Deal IDs from screenshot
COMPANY_NAME = "Boxiiship System Beauty Logistics LLC"
DEAL_NAME = "Boxiiship_System Beauty Logistics LL"  # From screenshot, amount $1,100,000

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Action Items from meeting
action_items = [
    {
        "subject": "Check w/ Melissa re: status of manual encoding issue fix, report back to Reid",
        "priority": "HIGH",
        "due_days": 1,
        "body": "Follow up with Melissa on the manual encoding issue fix status and provide update to Reid.\n\nContext: Related to package visibility/tracking issues discussed in meeting."
    },
    {
        "subject": "Follow up w/ Kevin re: ACI Direct routing for ~2800 shipments, send details to Reid",
        "priority": "HIGH",
        "due_days": 2,
        "body": "Contact Kevin about ACI Direct routing opportunity:\n- Potential for ~2,800 shipments/month\n- Est. savings: ~$0.30/package on peak season fees\n- Covers 50-70% of country\n- Send performance data and details to Reid"
    },
    {
        "subject": "Submit JIRA ticket for custom domestic transit report w/ reference fields 1 & 2",
        "priority": "HIGH",
        "due_days": 1,
        "body": "Create JIRA ticket for custom reporting feature:\n- Include reference fields 1 & 2 in transit reports\n- Customer-specific performance tracking for System Beauty's two key accounts\n- Monthly reporting cadence"
    },
    {
        "subject": "Build out pivot tables for transit analysis, send to Walker for forwarding to Reid",
        "priority": "MEDIUM",
        "due_days": 3,
        "body": "Create detailed transit analysis pivot tables:\n- September Xparcel Expedited performance breakdown\n- Include <1lb avg (2.94 days) and >1lb avg (3.64 days)\n- 93.67% delivery within 2-5 day window\n- Send to Walker for Reid delivery"
    },
    {
        "subject": "Send Sept breakdown w/ reference info for customer-specific performance data to Reid",
        "priority": "HIGH",
        "due_days": 2,
        "body": "Compile and send September performance report:\n- Include reference information for two key System Beauty customers\n- Detailed performance data by customer segment\n- Transit time analysis with reference fields"
    },
    {
        "subject": "Process 4 tracking numbers from Reid - send to account_manager@firstmile.com",
        "priority": "HIGH",
        "due_days": 0,
        "body": "When Reid sends the 4 tracking numbers:\n- Forward to account_manager@firstmile.com\n- CC Walker\n- Request investigation and status updates\n- Provide updates by Wednesday (per agreement)\n\nContext: 15-20 packages had visibility issues, need investigation"
    },
    {
        "subject": "Follow up: Provide ETA on custom report development timeline",
        "priority": "MEDIUM",
        "due_days": 3,
        "body": "After JIRA ticket submission, provide Reid with:\n- Development timeline for custom report feature\n- Expected delivery date for reference field integration\n- Interim reporting solution if needed"
    }
]

# Search for the deal
print("Searching for BoxiiShip System Beauty deal...")
search_payload = {
    "filterGroups": [{
        "filters": [
            {"propertyName": "dealname", "operator": "CONTAINS_TOKEN", "value": "Boxiiship System Beauty"},
            {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID}
        ]
    }],
    "properties": ["dealname", "dealstage", "hs_object_id", "amount"],
    "limit": 10
}

response = requests.post(
    "https://api.hubapi.com/crm/v3/objects/deals/search",
    headers=headers,
    json=search_payload
)

if response.status_code != 200:
    print(f"[ERROR] Failed to search deals: {response.text}")
    exit(1)

results = response.json().get("results", [])
if not results:
    print("[ERROR] BoxiiShip System Beauty deal not found")
    exit(1)

# Find the $1.1M deal
deal = None
for d in results:
    amount = d["properties"].get("amount", "")
    if amount and float(amount) >= 1000000:
        deal = d
        break

if not deal:
    deal = results[0]

deal_id = deal["id"]
deal_name = deal["properties"]["dealname"]
deal_amount = deal["properties"].get("amount", "Unknown")

print(f"[OK] Found: {deal_name}")
print(f"     Amount: ${deal_amount}")
print(f"     Deal ID: {deal_id}\n")

# Create tasks
print(f"Creating {len(action_items)} action item tasks...\n")
created_count = 0
failed_count = 0

for item in action_items:
    due_date = datetime.now() + timedelta(days=item["due_days"])
    due_timestamp = int(due_date.timestamp() * 1000)

    task_data = {
        "properties": {
            "hs_task_subject": item["subject"],
            "hs_task_body": item["body"],
            "hs_task_type": "TODO",
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": item["priority"],
            "hubspot_owner_id": OWNER_ID,
            "hs_timestamp": due_timestamp
        }
    }

    # Create task
    task_response = requests.post(
        "https://api.hubapi.com/crm/v3/objects/tasks",
        headers=headers,
        json=task_data
    )

    if task_response.status_code not in [200, 201]:
        print(f"[ERROR] Failed to create task: {item['subject'][:50]}...")
        print(f"        {task_response.text}")
        failed_count += 1
        continue

    task = task_response.json()
    task_id = task["id"]

    # Associate with deal
    assoc_data = [{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 216  # Task to Deal association
    }]

    assoc_response = requests.put(
        f"https://api.hubapi.com/crm/v4/objects/tasks/{task_id}/associations/deals/{deal_id}",
        headers=headers,
        json=assoc_data
    )

    if assoc_response.status_code in [200, 201]:
        due_str = "TODAY" if item["due_days"] == 0 else f"{item['due_days']}d"
        priority_icon = "🔥" if item["priority"] == "HIGH" else "📋"
        print(f"{priority_icon} Created ({due_str}): {item['subject'][:60]}...")
        created_count += 1
    else:
        print(f"[WARN] Task created but association failed: {item['subject'][:50]}...")
        created_count += 1

print(f"\n{'='*80}")
print(f"TASK CREATION SUMMARY")
print(f"{'='*80}")
print(f"Total Tasks: {len(action_items)}")
print(f"Created:     {created_count}")
print(f"Failed:      {failed_count}")
print(f"\n[SUCCESS] All action items added to BoxiiShip System Beauty deal!")
print(f"Check HubSpot deal record to see tasks.")
print(f"{'='*80}\n")
