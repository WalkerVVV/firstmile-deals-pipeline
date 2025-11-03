#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily 9am Workflow Report - Action-Oriented Pipeline Management
Goal: Progress each deal quickly and timely to next stage → account creation → win
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
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)
OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

# Stage Workflow Definitions
STAGE_WORKFLOWS = {
    "1090865183": {
        "name": "[03-RATE-CREATION]",
        "goal": "Complete rate analysis and build proposal",
        "next_stage": "[04-PROPOSAL-SENT]",
        "actions": [
            "🔍 Review customer PLD data and shipping profile",
            "💰 Run rate calculations and savings analysis",
            "📊 Create pricing matrix and proposal deck",
            "✅ Schedule proposal delivery meeting"
        ],
        "urgency": "HIGH - Bottleneck Stage",
        "sla_days": 14,
        "blockers": ["Missing PLD data", "Waiting on customer volume info", "Rate card not finalized"]
    },
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": {
        "name": "[04-PROPOSAL-SENT]",
        "goal": "Get customer commitment and move to setup",
        "next_stage": "[05-SETUP-DOCS-SENT]",
        "actions": [
            "📧 Send follow-up email to decision maker",
            "📞 Schedule call to discuss proposal questions",
            "💡 Address objections and concerns",
            "📝 Get verbal commitment and send setup docs"
        ],
        "urgency": "HIGH - Revenue at Risk",
        "sla_days": 30,
        "blockers": ["Waiting on customer decision", "Budget approval pending", "Competing with other carriers"]
    },
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": {
        "name": "[06-IMPLEMENTATION]",
        "goal": "Complete onboarding and go live",
        "next_stage": "[07-CLOSED-WON]",
        "actions": [
            "📋 Verify setup docs received and signed",
            "🔗 Complete integration setup and testing",
            "📦 Process first shipment batch",
            "✅ Mark as CLOSED-WON and transition to customer success"
        ],
        "urgency": "CRITICAL - At Finish Line",
        "sla_days": 14,
        "blockers": ["IT integration delays", "Waiting on customer testing", "Account setup incomplete"]
    }
}

def fetch_priority_deals():
    """Fetch deals in priority stages with full details"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [
                {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
                {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID},
                {"propertyName": "dealstage", "operator": "IN", "values": list(STAGE_WORKFLOWS.keys())}
            ]
        }],
        "properties": [
            "dealname", "dealstage", "hs_object_id", "amount",
            "createdate", "notes_last_updated", "hs_lastmodifieddate",
            "closedate", "hs_deal_stage_probability"
        ],
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
    """Get all tasks for a deal"""
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(
        f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}/associations/tasks",
        headers=headers
    )

    if response.status_code != 200:
        return []

    task_associations = response.json().get("results", [])
    tasks = []

    for assoc in task_associations:
        task_id = assoc["id"]
        task_response = requests.get(
            f"https://api.hubapi.com/crm/v3/objects/tasks/{task_id}",
            headers=headers,
            params={"properties": "hs_task_subject,hs_task_type,hs_task_status,hs_timestamp"}
        )

        if task_response.status_code == 200:
            tasks.append(task_response.json())

    return tasks

def calculate_deal_age(create_date):
    """Calculate days since deal created"""
    if not create_date:
        return 0

    created = datetime.fromisoformat(create_date.replace('Z', '+00:00'))
    return (datetime.now(created.tzinfo) - created).days

def calculate_urgency_score(deal, workflow):
    """Calculate urgency score (0-100) based on multiple factors"""
    score = 50  # Base score

    # Factor 1: Days in stage (max +30)
    create_date = deal["properties"].get("createdate")
    days_in_stage = calculate_deal_age(create_date)
    if days_in_stage > workflow["sla_days"]:
        score += 30
    elif days_in_stage > workflow["sla_days"] * 0.75:
        score += 20
    elif days_in_stage > workflow["sla_days"] * 0.5:
        score += 10

    # Factor 2: Deal amount (max +20)
    amount = deal["properties"].get("amount")
    if amount:
        try:
            amount_val = float(amount)
            if amount_val > 50000:
                score += 20
            elif amount_val > 25000:
                score += 10
        except:
            pass

    # Factor 3: Last activity (max +20)
    last_modified = deal["properties"].get("hs_lastmodifieddate")
    if last_modified:
        modified = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
        days_since_activity = (datetime.now(modified.tzinfo) - modified).days
        if days_since_activity > 14:
            score += 20
        elif days_since_activity > 7:
            score += 10

    # Factor 4: Close to finish line bonus
    if workflow["name"] == "[06-IMPLEMENTATION]":
        score += 15

    return min(score, 100)

def create_email_task(deal_id, deal_name, stage_name, workflow):
    """Create EMAIL task with workflow-specific actions"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    due_date = datetime.now() + timedelta(days=workflow["sla_days"])
    due_timestamp = int(due_date.timestamp() * 1000)

    task_body = f"""Goal: {workflow['goal']}

Next Actions:
{chr(10).join(workflow['actions'])}

Next Stage: {workflow['next_stage']}
SLA: {workflow['sla_days']} days
"""

    task_data = {
        "properties": {
            "hs_task_subject": f"🎯 {workflow['name']} - {deal_name}",
            "hs_task_body": task_body,
            "hs_task_type": "EMAIL",
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": "HIGH" if workflow["urgency"].startswith("HIGH") else "MEDIUM",
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
        return None

    task = response.json()
    task_id = task["id"]

    # Associate task with deal
    assoc_data = [{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 216
    }]

    requests.put(
        f"https://api.hubapi.com/crm/v4/objects/tasks/{task_id}/associations/deals/{deal_id}",
        headers=headers,
        json=assoc_data
    )

    return task_id

def main():
    print("\n" + "="*90)
    print("DAILY 9AM WORKFLOW REPORT - ACTION-ORIENTED PIPELINE MANAGEMENT")
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Goal: Progress each deal → next stage → account creation → WIN")
    print("="*90 + "\n")

    # Fetch priority deals
    print("📊 Fetching priority stage deals...")
    deals = fetch_priority_deals()
    print(f"✅ Found {len(deals)} active opportunities\n")

    if not deals:
        print("✅ No deals in priority stages. Pipeline clear!\n")
        return

    # Analyze and score deals
    deal_analysis = []
    missing_tasks = []

    for deal in deals:
        deal_id = deal["id"]
        deal_name = deal["properties"]["dealname"]
        stage_id = deal["properties"]["dealstage"]
        workflow = STAGE_WORKFLOWS[stage_id]

        # Calculate urgency
        urgency_score = calculate_urgency_score(deal, workflow)
        days_in_stage = calculate_deal_age(deal["properties"].get("createdate"))

        # Check tasks
        tasks = get_deal_tasks(deal_id)
        email_tasks = [t for t in tasks if t["properties"].get("hs_task_type") == "EMAIL"]
        has_task = len(email_tasks) > 0

        deal_analysis.append({
            "deal_id": deal_id,
            "deal_name": deal_name,
            "workflow": workflow,
            "urgency_score": urgency_score,
            "days_in_stage": days_in_stage,
            "has_task": has_task,
            "amount": deal["properties"].get("amount", "Unknown")
        })

        if not has_task:
            missing_tasks.append((deal_id, deal_name, workflow))

    # Sort by urgency (highest first)
    deal_analysis.sort(key=lambda x: x["urgency_score"], reverse=True)

    # Display workflow report by stage
    by_stage = defaultdict(list)
    for analysis in deal_analysis:
        stage_name = analysis["workflow"]["name"]
        by_stage[stage_name].append(analysis)

    for stage_name in ["[03-RATE-CREATION]", "[04-PROPOSAL-SENT]", "[06-IMPLEMENTATION]"]:
        if stage_name not in by_stage:
            continue

        stage_deals = by_stage[stage_name]
        workflow = stage_deals[0]["workflow"]

        print("="*90)
        print(f"{stage_name} - {len(stage_deals)} DEALS | {workflow['urgency']}")
        print(f"Goal: {workflow['goal']}")
        print(f"Next Stage: {workflow['next_stage']} | SLA: {workflow['sla_days']} days")
        print("="*90 + "\n")

        for i, analysis in enumerate(stage_deals, 1):
            urgency_icon = "🔥" if analysis["urgency_score"] >= 80 else "⚡" if analysis["urgency_score"] >= 60 else "📌"
            task_status = "✅" if analysis["has_task"] else "❌ NO TASK"

            print(f"{urgency_icon} PRIORITY #{i} | Score: {analysis['urgency_score']}/100 | {analysis['days_in_stage']}d in stage")
            print(f"   Deal: {analysis['deal_name']}")
            print(f"   Amount: ${analysis['amount']}")
            print(f"   Task Status: {task_status}")
            print(f"\n   📋 NEXT ACTIONS:")
            for action in workflow["actions"]:
                print(f"      {action}")
            print(f"\n   🎯 SUCCESS CRITERIA: Move to {workflow['next_stage']}\n")
            print("-" * 90 + "\n")

    # Create missing tasks
    if missing_tasks:
        print("="*90)
        print(f"🔧 CREATING {len(missing_tasks)} MISSING WORKFLOW TASKS")
        print("="*90 + "\n")

        created = 0
        for deal_id, deal_name, workflow in missing_tasks:
            task_id = create_email_task(deal_id, deal_name, workflow["name"], workflow)
            if task_id:
                print(f"✅ Created workflow task: {deal_name}")
                created += 1
            else:
                print(f"❌ Failed: {deal_name}")

        print(f"\n✅ Created {created}/{len(missing_tasks)} tasks\n")

    # Executive Summary
    print("="*90)
    print("📊 EXECUTIVE SUMMARY")
    print("="*90)

    high_priority = [d for d in deal_analysis if d["urgency_score"] >= 80]
    medium_priority = [d for d in deal_analysis if 60 <= d["urgency_score"] < 80]

    print(f"\n🔥 HIGH PRIORITY (Score 80+):     {len(high_priority)} deals - ACTION REQUIRED TODAY")
    print(f"⚡ MEDIUM PRIORITY (Score 60-79): {len(medium_priority)} deals - Action within 3 days")
    print(f"📌 STANDARD PRIORITY (Score <60): {len(deal_analysis) - len(high_priority) - len(medium_priority)} deals - Monitor closely")

    print(f"\n📈 PIPELINE VELOCITY:")
    print(f"   • {len(by_stage.get('[03-RATE-CREATION]', []))} deals need proposals created")
    print(f"   • {len(by_stage.get('[04-PROPOSAL-SENT]', []))} deals waiting for customer commitment")
    print(f"   • {len(by_stage.get('[06-IMPLEMENTATION]', []))} deals in implementation (CLOSE TO WIN!)")

    total_amount = sum(float(d["amount"]) if d["amount"] != "Unknown" and d["amount"] else 0 for d in deal_analysis)
    if total_amount > 0:
        print(f"\n💰 PIPELINE VALUE: ${total_amount:,.0f}")

    print("\n✅ Daily 9am workflow report complete")
    print("="*90 + "\n")

if __name__ == "__main__":
    main()
