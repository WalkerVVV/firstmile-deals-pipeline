#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BULK DEAL HYGIENE UPDATE
Updates all deals with missing next steps and next activity dates based on stage.

Usage:
    python bulk_update_deal_hygiene.py --dry-run   # Preview changes
    python bulk_update_deal_hygiene.py             # Execute updates
"""

import sys
import io
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

# Configuration
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    sys.exit(1)

OWNER_ID = "699257003"  # Brett Walker
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

# Stage definitions with next step templates
STAGE_CONFIG = {
    "1090865183": {
        "name": "[01-DISCOVERY-SCHEDULED]",
        "next_step": "Conduct discovery call - understand volume, pain points, timeline",
        "days_out": 3
    },
    "d2a08d6f-cc04-4423-9215-594fe682e538": {
        "name": "[02-DISCOVERY-COMPLETE]",
        "next_step": "Create custom rate card based on discovery insights",
        "days_out": 5
    },
    "e1c4321e-afb6-4b29-97d4-2b2425488535": {
        "name": "[03-RATE-CREATION]",
        "next_step": "Finalize rates and prepare proposal presentation",
        "days_out": 3
    },
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": {
        "name": "[04-PROPOSAL-SENT]",
        "next_step": "Follow up on proposal - address questions, negotiate terms",
        "days_out": 5
    },
    "4e549d01-674b-4b31-8a90-91ec03122715": {
        "name": "[05-SETUP-DOCS-SENT]",
        "next_step": "Confirm setup docs received - assist with completion",
        "days_out": 3
    },
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": {
        "name": "[06-IMPLEMENTATION]",
        "next_step": "Monitor implementation progress - resolve blockers",
        "days_out": 7
    },
    "3fd46d94-78b4-452b-8704-62a338a210fb": {
        "name": "[07-STARTED-SHIPPING]",
        "next_step": "QBR check-in - review performance, identify growth opportunities",
        "days_out": 30
    }
}

# Required fields to check
REQUIRED_FIELDS = [
    "dealname",
    "dealstage",
    "amount",
    "closedate",
    "hs_next_step",
    "notes_next_activity_date",
    "description"
]

def fetch_all_deals():
    """Fetch all active deals with required fields"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [
                {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
                {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID},
                {"propertyName": "dealstage", "operator": "IN", "values": list(STAGE_CONFIG.keys())}
            ]
        }],
        "properties": REQUIRED_FIELDS + ["hs_lastmodifieddate"],
        "limit": 100
    }

    try:
        response = requests.post(
            "https://api.hubapi.com/crm/v3/objects/deals/search",
            headers=headers,
            json=payload,
            timeout=15
        )

        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"❌ Error fetching deals: {e}")
        return []

def analyze_deals(deals):
    """Analyze deals and determine what needs updating"""
    updates_needed = []

    for deal in deals:
        props = deal.get("properties", {})
        deal_id = deal.get("id")
        deal_name = props.get("dealname", "Unknown")
        stage_id = props.get("dealstage", "")

        stage_config = STAGE_CONFIG.get(stage_id)
        if not stage_config:
            continue

        update = {
            "id": deal_id,
            "name": deal_name,
            "stage": stage_config["name"],
            "properties": {},
            "create_task": False,
            "task_due": None
        }

        # Check next step
        if not props.get("hs_next_step"):
            update["properties"]["hs_next_step"] = stage_config["next_step"]

        # Check next activity date - create a task instead (notes_next_activity_date is read-only)
        if not props.get("notes_next_activity_date"):
            next_date = datetime.now() + timedelta(days=stage_config["days_out"])
            # Skip weekends
            while next_date.weekday() >= 5:
                next_date += timedelta(days=1)
            update["create_task"] = True
            update["task_due"] = next_date
            update["task_subject"] = stage_config["next_step"][:100]  # Task subject limit

        # Check description (set a default if missing)
        if not props.get("description"):
            update["properties"]["description"] = f"FirstMile shipping opportunity - {stage_config['name']}"

        # Check amount (don't auto-set, just flag)
        if not props.get("amount") or props.get("amount") == "0":
            update["needs_amount"] = True

        # Check closedate (don't auto-set, just flag)
        if not props.get("closedate"):
            update["needs_closedate"] = True

        # Only include if there are properties to update or tasks to create
        if update["properties"] or update["create_task"]:
            updates_needed.append(update)

    return updates_needed

def update_deal(deal_id, properties):
    """Update a single deal in HubSpot"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.patch(
            f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}",
            headers=headers,
            json={"properties": properties},
            timeout=10
        )

        if response.status_code != 200:
            print(f"\n    API Error: {response.text[:100]}")
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def create_task_for_deal(deal_id, subject, due_date):
    """Create a task associated with a deal"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    due_timestamp = int(due_date.timestamp() * 1000)

    task_data = {
        "properties": {
            "hs_task_subject": subject,
            "hs_task_body": f"Follow-up task auto-created by Nebuchadnezzar v3.0\nDue: {due_date.strftime('%B %d, %Y')}",
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": "MEDIUM",
            "hs_timestamp": str(due_timestamp),
            "hubspot_owner_id": OWNER_ID,
            "hs_task_type": "TODO"
        },
        "associations": [{
            "to": {"id": deal_id},
            "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 216}]
        }]
    }

    try:
        response = requests.post(
            "https://api.hubapi.com/crm/v3/objects/tasks",
            headers=headers,
            json=task_data,
            timeout=10
        )

        return response.status_code == 201
    except Exception as e:
        print(f"  ❌ Task Error: {e}")
        return False

def main():
    dry_run = "--dry-run" in sys.argv

    print("=" * 70)
    print("🔧 BULK DEAL HYGIENE UPDATE")
    print("=" * 70)
    print("")

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print("")

    # Fetch all deals
    print("📥 Fetching deals from HubSpot...")
    deals = fetch_all_deals()
    print(f"   Found {len(deals)} active deals")
    print("")

    # Analyze what needs updating
    print("🔍 Analyzing deals for missing fields...")
    updates_needed = analyze_deals(deals)
    print(f"   {len(updates_needed)} deals need updates")
    print("")

    if not updates_needed:
        print("✅ All deals are complete! No updates needed.")
        return

    # Show preview
    print("=" * 70)
    print("📋 UPDATE PREVIEW")
    print("=" * 70)
    print("")

    for update in updates_needed:
        print(f"📁 **{update['name']}** {update['stage']}")
        for field, value in update["properties"].items():
            if field == "notes_next_activity_date":
                print(f"   → {field}: {value}")
            elif field == "hs_next_step":
                print(f"   → {field}: {value[:50]}...")
            else:
                print(f"   → {field}: {value[:50]}..." if len(str(value)) > 50 else f"   → {field}: {value}")

        if update.get("needs_amount"):
            print(f"   ⚠️  Still needs: amount (manual entry required)")
        if update.get("needs_closedate"):
            print(f"   ⚠️  Still needs: closedate (manual entry required)")
        print("")

    # Summary
    print("=" * 70)
    print("📊 UPDATE SUMMARY")
    print("=" * 70)
    print("")

    field_counts = {}
    for update in updates_needed:
        for field in update["properties"]:
            field_counts[field] = field_counts.get(field, 0) + 1

    for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {field}: {count} deals")

    needs_manual = sum(1 for u in updates_needed if u.get("needs_amount") or u.get("needs_closedate"))
    if needs_manual:
        print(f"\n   ⚠️  {needs_manual} deals still need manual updates (amount/closedate)")

    print("")

    if dry_run:
        print("=" * 70)
        print("🔍 DRY RUN COMPLETE")
        print("=" * 70)
        print("")
        print("To execute these updates, run:")
        print("   python bulk_update_deal_hygiene.py")
        return

    # Execute updates
    print("=" * 70)
    print("🚀 EXECUTING UPDATES")
    print("=" * 70)
    print("")

    success_count = 0
    fail_count = 0
    tasks_created = 0

    for i, update in enumerate(updates_needed, 1):
        print(f"[{i}/{len(updates_needed)}] {update['name'][:40]}...", end=" ")

        deal_success = True
        task_success = True

        # Update deal properties if any
        if update["properties"]:
            deal_success = update_deal(update["id"], update["properties"])

        # Create task if needed
        if update["create_task"] and update["task_due"]:
            task_success = create_task_for_deal(
                update["id"],
                update.get("task_subject", "Follow-up"),
                update["task_due"]
            )
            if task_success:
                tasks_created += 1

        if deal_success and task_success:
            print("✅")
            success_count += 1
        else:
            print("❌")
            fail_count += 1

    print("")
    print("=" * 70)
    print("📊 FINAL RESULTS")
    print("=" * 70)
    print("")
    print(f"   ✅ Successfully updated: {success_count} deals")
    if tasks_created:
        print(f"   📋 Tasks created: {tasks_created}")
    if fail_count:
        print(f"   ❌ Failed: {fail_count} deals")
    print("")

    print(f"   📈 Deal hygiene improved!")
    print(f"   Run 'python unified_sync.py weekly' to see updated audit")
    print("")

if __name__ == "__main__":
    main()
