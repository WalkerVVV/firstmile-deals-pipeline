#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INTEGRATED 9AM SYNC v3.0 - Complete Morning Workflow with Superhuman Email Integration
Combines: Email responses + Yesterday's log + Follow-up queue + HubSpot + Brand Scout

CRITICAL: This is the CORRECT 9AM sync that includes Superhuman email checking via Chrome MCP
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

def print_header():
    """Print sync header"""
    print("\n" + "="*80)
    print("INTEGRATED 9AM SYNC v3.0 - COMPLETE MORNING WORKFLOW")
    print(f"Today: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
    print("="*80 + "\n")

def superhuman_email_check_instructions():
    """
    Return instructions for Claude Code to check Superhuman emails via Chrome MCP.
    This should be executed by Claude Code using the chrome-mcp-server tools.
    """
    instructions = """

================================================================================
📧 PHASE 1: SUPERHUMAN EMAIL CHECK (Chrome MCP Required)
================================================================================

INSTRUCTIONS FOR CLAUDE CODE:

Use chrome-mcp-server to check Superhuman for overnight email responses:

1. List all browser tabs to find Superhuman:
   Use: chrome_mcp_server__get_windows_and_tabs

2. Navigate to Superhuman (if not already open):
   Use: chrome_mcp_server__chrome_navigate
   URL: https://mail.superhuman.com/

3. Access the Superhuman search:
   - Look for search input or command bar
   - Use: chrome_mcp_server__chrome_get_web_content to find search elements

4. Execute search query:
   Search for: in:inbox after:now(today and prior 2 days)

5. Extract email list with:
   - Sender names
   - Subject lines
   - Timestamps
   - Whether it's a response to a pending item from FOLLOW_UP_REMINDERS.txt

6. Categorize emails:
   CUSTOMER RESPONSES: Direct replies to your pending follow-ups
   NEW INBOUND: New inquiries or conversations
   INTERNAL: Team communications

OUTPUT FORMAT NEEDED:

OVERNIGHT EMAIL RESPONSES (Last 3 Days):

CUSTOMER RESPONSES (X):
✅ [Company] - [Contact] - [Subject] - [Timestamp]
✅ [Company] - [Contact] - [Subject] - [Timestamp]
⏳ [Company] - No response yet (still pending)

NEW INBOUND (X):
🆕 [Company] - [Contact] - [Subject] - [Timestamp]

INTERNAL (X):
💬 [Person] - [Subject] - [Timestamp]

PENDING FROM YESTERDAY (Cross-reference with FOLLOW_UP_REMINDERS.txt):
1. [Company] - [Expected response] → STATUS
2. [Company] - [Expected response] → STATUS

================================================================================
"""
    return instructions

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

    return follow_ups[:10]  # Return all critical items (increased from 5)

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
    print_header()

    # PHASE 0: Superhuman Email Check Instructions
    print(superhuman_email_check_instructions())
    print("\n⚠️  WAITING FOR CLAUDE CODE TO COMPLETE EMAIL CHECK VIA CHROME MCP...")
    print("    (Claude Code should execute the above instructions using chrome-mcp-server tools)\n")
    print("="*80 + "\n")

    # Phase 1: Yesterday's Context
    print("\n📅 PHASE 2: YESTERDAY'S CONTEXT")
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
    print("\n🚨 PHASE 3: CRITICAL FOLLOW-UPS (From Action Queue)")
    print("-" * 80)
    follow_ups = extract_follow_up_queue()

    if follow_ups:
        print(f"Total pending items: {len(follow_ups)}\n")
        for i, item in enumerate(follow_ups, 1):
            print(f"{i}. {item['text']}")
            for detail in item['details'][:2]:
                print(f"   {detail}")
        print()
    else:
        print("✅ No critical follow-ups in queue\n")

    # Phase 3: HubSpot Priority Deals
    print("\n💼 PHASE 4: HUBSPOT PRIORITY DEALS (LIVE DATA)")
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
    print("\n🔍 PHASE 5: BRAND SCOUT OVERNIGHT RESULTS")
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
    print("\n💡 PHASE 6: KEY LEARNINGS (Apply Today)")
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
    print("🎯 PHASE 7: SALES DISCIPLINE AGENTS (Run These Next)")
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
    print("1. COMPLETE EMAIL CHECK (Phase 1 above) - Use Chrome MCP to check Superhuman")
    print("2. Review pending items from yesterday")
    print("3. Execute critical follow-ups from action queue")
    print("4. Check Brand Scout reports (if any)")
    print("5. Work priority deals in HubSpot")
    print("6. Run sales discipline agents (prioritization & stale proposal scanner)")
    print("7. Log progress in _DAILY_LOG.md throughout day")
    print("8. NOON SYNC: Check morning progress at 12PM")
    print("\n✅ Morning sync complete (pending email check via Chrome MCP)\n")

if __name__ == "__main__":
    main()
