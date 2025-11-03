#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INTEGRATED 9AM SYNC v2.0 - Context-Aware Day Start with Weekly Continuity
Combines: Weekly sync action queue + Yesterday's log + Follow-up queue + HubSpot + Brand Scout
Goal: TRUE WORKFLOW CONTINUITY from weekend → Monday → Tuesday → ...
"""

import sys, io, os, re, json
from datetime import datetime, timedelta
from pathlib import Path
import requests
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    sys.exit(1)

OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
DOWNLOADS = Path.home() / "Downloads"
DAILY_LOG = DOWNLOADS / "_DAILY_LOG.md"
FEEDBACK_LOG = DOWNLOADS / "_DAILY_LOG_FEEDBACK.md"
FOLLOW_UP = DOWNLOADS / "FOLLOW_UP_REMINDERS.txt"
BRAND_SCOUT_DIR = Path("c:/Users/BrettWalker/FirstMile_Deals/.claude/brand_scout/output")

PRIORITY_STAGES = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]"
}

def find_most_recent_weekly_sync():
    """Find the most recent weekly sync report (for Monday continuity)"""
    try:
        weekly_reports = sorted(DOWNLOADS.glob("WEEKLY_SYNC_*_COMPLETE.md"), reverse=True)
        if weekly_reports:
            return weekly_reports[0]
    except:
        pass
    return None

def extract_monday_action_queue(weekly_report_path):
    """Extract Monday morning action queue from weekend comprehensive sync"""
    if not weekly_report_path or not weekly_report_path.exists():
        return {"found": False, "priorities": [], "context": []}

    content = weekly_report_path.read_text(encoding='utf-8')
    action_queue = {"found": True, "report_date": None, "priorities": [], "context": []}

    date_match = re.search(r'Week of (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})', content)
    if date_match:
        action_queue["report_date"] = f"{date_match.group(1)} to {date_match.group(2)}"

    priority_section = re.search(r'## 🚨 CRITICAL ROLLED-OVER PRIORITIES.*?\n(.*?)(?=\n##)', content, re.DOTALL)
    if priority_section:
        priority_text = priority_section.group(1)
        for match in re.finditer(r'### (\d+)\.\s+(.*?)\(Priority:\s+(\d+)\).*?Context\*\*:\s+(.*?)(?=\n###|\n---|\Z)', priority_text, re.DOTALL):
            action_queue["priorities"].append({
                "rank": int(match.group(1)),
                "title": match.group(2).strip(),
                "priority": int(match.group(3)),
                "context": match.group(4).strip()
            })

    context_section = re.search(r'## 🔍 PIPELINE HEALTH INSIGHTS.*?\n(.*?)(?=\n##)', content, re.DOTALL)
    if context_section:
        for line in context_section.group(1).split('\n'):
            if line.strip().startswith('-'):
                action_queue["context"].append(line.strip('- ').strip())

    return action_queue

def extract_yesterday_context():
    """Extract what you were working on yesterday"""
    if not DAILY_LOG.exists():
        return {"priorities": [], "completed": [], "pending": []}

    content = DAILY_LOG.read_text(encoding='utf-8')
    context = {"date": None, "priorities": [], "completed": [], "pending": [], "afternoon_notes": []}

    date_match = re.search(r'##\s+(\w+day),\s+(\w+\s+\d+,\s+\d+)', content)
    if date_match:
        context["date"] = date_match.group(0).replace("## ", "")

    completed_section = re.search(r'COMPLETED.*?\n(.*?)(?=\n##|PRIORITY|\Z)', content, re.DOTALL)
    if completed_section:
        for line in completed_section.group(1).split('\n'):
            if '✅' in line:
                context["completed"].append(line.strip())

    afternoon_section = re.search(r'AFTERNOON.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if afternoon_section:
        for line in afternoon_section.group(1).split('\n'):
            if line.strip() and ('**' in line or '🚨' in line or line.strip().startswith(tuple('123456789'))):
                context["afternoon_notes"].append(line.strip())

    return context

def extract_follow_up_queue():
    """Extract critical follow-ups from action queue"""
    if not FOLLOW_UP.exists():
        return []

    content = FOLLOW_UP.read_text(encoding='utf-8')
    follow_ups, current_item = [], None

    for line in content.split('\n'):
        if re.match(r'^\d+\.', line.strip()):
            if current_item:
                follow_ups.append(current_item)
            current_item = {"text": line.strip(), "details": []}
        elif current_item and line.strip() and not line.startswith('='):
            current_item["details"].append(line.strip())
        if '=================' in line and current_item:
            follow_ups.append(current_item)
            break

    if current_item:
        follow_ups.append(current_item)

    return follow_ups[:5]

def fetch_hubspot_priorities():
    """Fetch priority deals from HubSpot"""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "filterGroups": [{
            "filters": [
                {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
                {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID},
                {"propertyName": "dealstage", "operator": "IN", "values": list(PRIORITY_STAGES.keys())}
            ]
        }],
        "properties": ["dealname", "dealstage", "amount", "createdate"],
        "limit": 100
    }

    try:
        response = requests.post("https://api.hubapi.com/crm/v3/objects/deals/search", headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            deals = response.json().get("results", [])
            by_stage = {}
            for deal in deals:
                stage_id = deal["properties"]["dealstage"]
                stage_name = PRIORITY_STAGES.get(stage_id, "UNKNOWN")
                if stage_name not in by_stage:
                    by_stage[stage_name] = []
                by_stage[stage_name].append({
                    "name": deal["properties"]["dealname"],
                    "amount": deal["properties"].get("amount", "0"),
                    "created": deal["properties"]["createdate"]
                })
            return by_stage
        else:
            return {}
    except Exception as e:
        print(f"⚠️  HubSpot API error: {e}")
        return {}

def check_brand_scout_reports():
    """Check for new Brand Scout reports from overnight"""
    if not BRAND_SCOUT_DIR.exists():
        return []
    yesterday = datetime.now() - timedelta(days=1)
    new_reports = []
    try:
        for report_file in BRAND_SCOUT_DIR.glob("*.md"):
            if report_file.stat().st_mtime > yesterday.timestamp():
                new_reports.append(report_file.name)
    except:
        pass
    return new_reports

def extract_learnings():
    """Extract key learnings from feedback log"""
    if not FEEDBACK_LOG.exists():
        return []
    content = FEEDBACK_LOG.read_text(encoding='utf-8')
    learnings = []
    for line in content.split('\n')[-20:]:
        if any(marker in line for marker in ['✅', '❌', '🔧', '💡']):
            learnings.append(line.strip())
    return learnings[-5:]

def main():
    print("\n" + "="*80)
    print("INTEGRATED 9AM SYNC v2.0 - CONTEXT-AWARE DAY START")
    print(f"Today: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
    print("="*80 + "\n")

    is_monday = (datetime.now().weekday() == 0)

    # PHASE 0: Weekly Sync Continuity (Monday only)
    if is_monday:
        weekly_report = find_most_recent_weekly_sync()
        if weekly_report:
            print("📋 WEEKLY SYNC CONTINUITY (FROM WEEKEND COMPREHENSIVE SYNC)")
            print("-" * 80)
            action_queue = extract_monday_action_queue(weekly_report)

            if action_queue["found"]:
                print(f"Source: {weekly_report.name}")
                if action_queue["report_date"]:
                    print(f"Period: {action_queue['report_date']}\n")

                if action_queue["priorities"]:
                    print("🚨 CRITICAL ROLLED-OVER PRIORITIES (FROM WEEKEND):")
                    for priority in action_queue["priorities"]:
                        print(f"\n{priority['rank']}. {priority['title']} (Priority: {priority['priority']})")
                        print(f"   Context: {priority['context']}")
                    print()

                if action_queue["context"]:
                    print("📊 PIPELINE CONTEXT:")
                    for insight in action_queue["context"][:5]:
                        print(f"  • {insight}")
                    print()
            else:
                print("⚠️  Weekly sync report found but couldn't parse action queue\n")
        else:
            print("ℹ️  No weekly sync report found (expected on Monday)\n")

    # Phase 1: Yesterday's Context
    print("\n📅 YESTERDAY'S CONTEXT")
    print("-" * 80)
    yesterday = extract_yesterday_context()

    if yesterday["date"]:
        print(f"Last Update: {yesterday['date']}\n")

    if yesterday["completed"]:
        print("✅ COMPLETED:")
        for item in yesterday["completed"][:5]:
            print(f"  {item}")
        print()

    if yesterday["afternoon_notes"]:
        print("⏳ PENDING FROM YESTERDAY:")
        for item in yesterday["afternoon_notes"][:5]:
            print(f"  {item}")
        print()

    # Phase 2: Critical Follow-Ups
    print("\n🚨 CRITICAL FOLLOW-UPS (From Action Queue)")
    print("-" * 80)
    follow_ups = extract_follow_up_queue()

    if follow_ups:
        for i, item in enumerate(follow_ups, 1):
            print(f"{i}. {item['text']}")
            for detail in item['details'][:2]:
                print(f"   {detail}")
        print()
    else:
        print("✅ No critical follow-ups in queue\n")

    # Phase 3: HubSpot Priority Deals
    print("\n💼 HUBSPOT PRIORITY DEALS (LIVE DATA)")
    print("-" * 80)
    deals = fetch_hubspot_priorities()

    if deals:
        total = sum(len(stage_deals) for stage_deals in deals.values())
        print(f"Total Priority Deals: {total}\n")

        for stage, stage_deals in deals.items():
            print(f"{stage} ({len(stage_deals)} deals)")
            for deal in stage_deals[:3]:
                amount = f"${int(deal['amount']):,}" if deal['amount'] != '0' else "No amount"
                print(f"  • {deal['name']} - {amount}")
            if len(stage_deals) > 3:
                print(f"  ... and {len(stage_deals) - 3} more")
            print()
    else:
        print("⚠️  Could not fetch HubSpot deals\n")

    # Phase 4: Brand Scout Overnight
    print("\n🔍 BRAND SCOUT OVERNIGHT RESULTS")
    print("-" * 80)
    new_reports = check_brand_scout_reports()

    if new_reports:
        print(f"✅ {len(new_reports)} new reports generated:")
        for report in new_reports:
            print(f"  • {report}")
        print("\n📁 Location: .claude/brand_scout/output/")
        print("   Action: Review reports and prioritize discovery outreach\n")
    else:
        print("No new Brand Scout reports overnight\n")

    # Phase 5: Key Learnings
    print("\n💡 KEY LEARNINGS (Apply Today)")
    print("-" * 80)
    learnings = extract_learnings()

    if learnings:
        for learning in learnings:
            print(f"  {learning}")
        print()
    else:
        print("No recent learnings logged\n")

    # Phase 6: Sales Discipline Agents
    print("\n" + "="*80)
    print("🎯 SALES DISCIPLINE AGENTS (Run These Next)")
    print("="*80)
    print("\nAutomated sales discipline enforcement - forces 5/2/3/1 weekly goals:\n")
    print("1. Priority Reminder (Top 3 deals for today):")
    print("   python .claude/agents/prioritization_agent.py --daily-reminder\n")
    print("2. Stale Proposal Scanner (Urgency follow-ups):")
    print("   python .claude/agents/sales_execution_agent.py\n")
    print("💡 TIP: These agents run independently and generate actionable outputs")
    print("        Review their reports before starting your day")

    # Summary
    print("\n" + "="*80)
    print("🎯 NEXT STEPS")
    print("="*80)
    if is_monday:
        print("1. Address critical rolled-over priorities from weekend sync (if any)")
        print("2. Review pending items from Friday")
    else:
        print("1. Review pending items from yesterday")
    print("2. Execute critical follow-ups from action queue")
    print("3. Check Brand Scout reports (if any)")
    print("4. Work priority deals in HubSpot")
    print("5. Log progress in _DAILY_LOG.md throughout day")
    print("6. NOON SYNC: Check morning progress at 12PM")
    print("\n✅ You're now up to speed with full context\n")

if __name__ == "__main__":
    main()
