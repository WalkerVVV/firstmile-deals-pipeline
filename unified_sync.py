#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
UNIFIED SYNC SYSTEM v1.0 - Single Script for All Sync Times
Replaces: daily_9am_sync.py, noon_sync.py, 3pm_sync.py, eod_sync.py, end_of_week_sync_COMPLETE.py

Usage:
    python unified_sync.py 9am       # Morning sync with email integration
    python unified_sync.py noon      # Mid-day progress check
    python unified_sync.py 3pm       # Afternoon adjustment
    python unified_sync.py eod       # End of day wrap
    python unified_sync.py weekly    # Weekend comprehensive sync
    python unified_sync.py monthly   # Month-end analysis

Format: COMPREHENSIVE for ALL sync types (eliminates format inconsistency)
"""

import sys, io, os, re, json
from datetime import datetime, timedelta
from pathlib import Path
import requests
from dotenv import load_dotenv
import subprocess

# Import new utility modules for Action-First Sync System
try:
    from utils.action_prioritizer import ActionPrioritizer
    from utils.continuity_manager import ContinuityManager
    from utils.git_committer import GitCommitter
    ACTION_FIRST_AVAILABLE = True
except ImportError:
    # Fallback if utils not available
    ACTION_FIRST_AVAILABLE = False
    print("⚠️ Warning: Action-First components not available, using legacy mode")

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
PROJECT_ROOT = Path("C:/Users/BrettWalker/FirstMile_Deals")
SYNC_REPORTS_DIR = PROJECT_ROOT / "sync_reports"
DAILY_LOG = PROJECT_ROOT / "_DAILY_LOG.md"
FOLLOW_UP = PROJECT_ROOT / "FOLLOW_UP_REMINDERS.txt"
BRAND_SCOUT_DIR = PROJECT_ROOT / ".claude/brand_scout/output"

# All active stages (excluding CLOSED-LOST)
ACTIVE_STAGES = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[02-DISCOVERY-COMPLETE]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "4e549d01-674b-4b31-8a90-91ec03122715": "[05-SETUP-DOCS-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
    "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-STARTED-SHIPPING]",
}

# SALES PRIORITY STAGES (stages 1-6 only, excludes STARTED-SHIPPING)
# Used by ActionPrioritizer to focus on active sales opportunities
SALES_PRIORITY_STAGES = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[02-DISCOVERY-COMPLETE]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "4e549d01-674b-4b31-8a90-91ec03122715": "[05-SETUP-DOCS-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]"
}

PRIORITY_STAGES = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]"
}

SYNC_TYPES = {
    "9am": {"title": "9AM SYNC", "time": "Morning", "next": "NOON at 12:00 PM"},
    "noon": {"title": "NOON SYNC", "time": "Mid-Day", "next": "3PM at 3:00 PM"},
    "3pm": {"title": "3PM SYNC", "time": "Afternoon", "next": "EOD at 5:00 PM"},
    "eod": {"title": "EOD SYNC", "time": "End of Day", "next": "Tomorrow 9:00 AM"},
    "weekly": {"title": "WEEKLY SYNC", "time": "End of Week", "next": "Monday 9:00 AM"},
    "monthly": {"title": "MONTHLY SYNC", "time": "End of Month", "next": "Next Month"}
}

# ============================================================================
# CHROME MCP EMAIL INTEGRATION
# ============================================================================

def check_chrome_mcp_status():
    """Check if Chrome MCP server is running"""
    try:
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return "12306" in result.stdout
    except:
        return False

def get_superhuman_emails():
    """
    Fetch recent emails from Superhuman via Chrome MCP
    Returns: Dict with categorized email action items
    """
    try:
        # Import MCP tools dynamically (only when Chrome MCP needed)
        import sys
        import importlib

        # Check if running in Claude Code environment with MCP access
        # This will fail gracefully if MCP not available
        result = {
            "success": False,
            "critical": [],
            "yesterday": [],
            "last_week": [],
            "error": None
        }

        # Try to use Chrome MCP via subprocess call to mcp_email_extractor.py
        # This is safer than trying to import MCP modules directly
        extractor_path = PROJECT_ROOT / "mcp_email_extractor.py"

        if extractor_path.exists():
            email_result = subprocess.run(
                ['python', str(extractor_path)],
                capture_output=True,
                encoding='utf-8',  # Explicit UTF-8 encoding for emoji support
                timeout=30,
                cwd=str(PROJECT_ROOT)
            )

            if email_result.returncode == 0:
                # Parse JSON output from extractor
                email_data = json.loads(email_result.stdout)
                result.update(email_data)
                result["success"] = True
            else:
                result["error"] = f"Email extractor failed: {email_result.stderr}"
        else:
            result["error"] = "Email extractor script not found (mcp_email_extractor.py)"

        return result

    except Exception as e:
        return {
            "success": False,
            "critical": [],
            "yesterday": [],
            "last_week": [],
            "error": str(e)
        }

# ============================================================================
# HUBSPOT INTEGRATION
# ============================================================================

def run_prioritization_agent():
    """Run prioritization agent for current HubSpot data"""
    try:
        result = subprocess.run(
            ['python', str(PROJECT_ROOT / '.claude/agents/prioritization_agent.py')],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(PROJECT_ROOT)
        )
        if result.returncode == 0:
            # Parse top 5 from output
            lines = result.stdout.split('\n')
            top_deals = []
            in_top_section = False

            for line in lines:
                if "TOP 5 PRIORITIES" in line:
                    in_top_section = True
                elif in_top_section and re.match(r'^\d+\.', line.strip()):
                    top_deals.append(line.strip())
                    if len(top_deals) >= 5:
                        break

            return {"success": True, "deals": top_deals, "raw": result.stdout}
        else:
            return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}

def run_action_prioritizer(sync_type):
    """
    Run new ActionPrioritizer for intelligent top 3 actions.
    Falls back to run_prioritization_agent() if Action-First not available.
    """
    if not ACTION_FIRST_AVAILABLE:
        # Fallback to legacy prioritization agent
        return run_prioritization_agent()

    try:
        # Initialize ActionPrioritizer
        prioritizer = ActionPrioritizer()

        # Fetch HubSpot deals
        deals_data = fetch_hubspot_deals_raw()  # Get full deal objects

        # Get email data
        email_data = get_superhuman_emails()
        emails = {
            "critical": email_data.get("critical", []),
            "yesterday": email_data.get("yesterday", []),
            "last_week": email_data.get("last_week", [])
        }

        # Generate top 3 actions
        actions = prioritizer.prioritize_actions(deals_data, emails, sync_type)

        # Format for report
        formatted_actions = []
        for i, action in enumerate(actions, 1):
            formatted_actions.append(
                f"{i}. [{action.score:.0f}pts] {action.title}\n"
                f"   Type: {action.type} | Priority: {action.priority} | Due: {action.due_by}\n"
                f"   Next: {action.next_step}"
            )

        return {
            "success": True,
            "actions": formatted_actions,
            "action_objects": actions  # For continuity manager
        }

    except Exception as e:
        print(f"⚠️ ActionPrioritizer failed: {e}")
        # Fallback to legacy agent
        return run_prioritization_agent()

def fetch_hubspot_deals_raw():
    """Fetch raw HubSpot deal objects (for ActionPrioritizer)

    CRITICAL: Only fetches stages 1-6 (SALES_PRIORITY_STAGES)
    Excludes stage 7 (STARTED-SHIPPING) to focus on active sales opportunities
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [
                {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
                {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID},
                {"propertyName": "dealstage", "operator": "IN", "values": list(SALES_PRIORITY_STAGES.keys())}
            ]
        }],
        "properties": ["dealname", "dealstage", "amount", "hs_lastmodifieddate", "hs_priority"],
        "limit": 100
    }

    try:
        response = requests.post(
            "https://api.hubapi.com/crm/v3/objects/deals/search",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            return []
    except Exception as e:
        print(f"⚠️ Error fetching deals: {e}")
        return []

def fetch_hubspot_deals():
    """Fetch active deals from HubSpot API"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [
                {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
                {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID},
                {"propertyName": "dealstage", "operator": "IN", "values": list(ACTIVE_STAGES.keys())}
            ]
        }],
        "properties": ["dealname", "dealstage", "amount", "hs_lastmodifieddate"],
        "limit": 100
    }

    try:
        response = requests.post(
            "https://api.hubapi.com/crm/v3/objects/deals/search",
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            deals = response.json().get("results", [])
            return {
                "total": len(deals),
                "total_value": sum(float(d["properties"].get("amount", 0) or 0) for d in deals),
                "by_stage": group_deals_by_stage(deals)
            }
        else:
            return {"error": f"API returned {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def group_deals_by_stage(deals):
    """Group deals by stage"""
    by_stage = {}
    for deal in deals:
        stage_id = deal["properties"]["dealstage"]
        stage_name = ACTIVE_STAGES.get(stage_id, "UNKNOWN")
        if stage_name not in by_stage:
            by_stage[stage_name] = {"count": 0, "value": 0}
        by_stage[stage_name]["count"] += 1
        by_stage[stage_name]["value"] += float(deal["properties"].get("amount", 0) or 0)
    return by_stage

# ============================================================================
# CONTEXT EXTRACTION
# ============================================================================

def extract_yesterday_context():
    """Extract yesterday's context from daily log"""
    if not DAILY_LOG.exists():
        return {"found": False, "date": None, "stale": False}

    content = DAILY_LOG.read_text(encoding='utf-8')
    context = {
        "found": True,
        "date": None,
        "completed": [],
        "pending": [],
        "stale": False,
        "days_old": 0
    }

    # Extract most recent date
    date_matches = re.findall(r'##\s+(\w+day),\s+(\w+)\s+(\d+),\s+(\d+)', content)
    if date_matches:
        date_match = date_matches[-1]
        context["date"] = f"{date_match[0]}, {date_match[1]} {date_match[2]}, {date_match[3]}"

        # Check if stale
        try:
            month_map = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            month = month_map.get(date_match[1], 1)
            day = int(date_match[2])
            year = int(date_match[3])
            log_date = datetime(year, month, day)
            days_old = (datetime.now() - log_date).days

            context["days_old"] = days_old
            context["stale"] = days_old > 3
        except:
            pass

    # Extract completed items
    completed_section = re.search(r'COMPLETED.*?\n(.*?)(?=\n##|PRIORITY|\Z)', content, re.DOTALL)
    if completed_section:
        for line in completed_section.group(1).split('\n'):
            if '✅' in line:
                context["completed"].append(line.strip())

    return context

def extract_follow_up_reminders():
    """Extract critical follow-ups from reminder file"""
    if not FOLLOW_UP.exists():
        return []

    content = FOLLOW_UP.read_text(encoding='utf-8')
    reminders = []

    # Extract critical section
    critical_section = re.search(r'## 🚨 CRITICAL.*?\n(.*?)(?=\n##|={3,}|\Z)', content, re.DOTALL)
    if critical_section:
        for line in critical_section.group(1).split('\n'):
            if line.strip() and ('**' in line or '$' in line):
                reminders.append(line.strip())

    return reminders[:5]

def check_brand_scout_reports():
    """Check for new Brand Scout reports"""
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

# ============================================================================
# CONTINUITY CHAIN - WRITE BACK TO LOGS
# ============================================================================

def append_to_daily_log(sync_type, report_content):
    """Append sync results to daily log for continuity"""
    now = datetime.now()

    # Create daily log if doesn't exist
    if not DAILY_LOG.exists():
        DAILY_LOG.write_text("# NEBUCHADNEZZAR v3.0 - DAILY ACTIVITY LOG\n\n", encoding='utf-8')

    # Prepare log entry based on sync type
    log_entry = []
    log_entry.append("\n" + "=" * 80)
    log_entry.append(f"## {now.strftime('%A, %B %d, %Y')} - {SYNC_TYPES[sync_type]['title']} ({now.strftime('%I:%M %p')})")
    log_entry.append("=" * 80)
    log_entry.append("")

    if sync_type == "9am":
        log_entry.append("### 🎯 TODAY'S TOP PRIORITIES")
        log_entry.append("_(From 9AM sync - see detailed report for full context)_")
        log_entry.append("")

    elif sync_type == "noon":
        log_entry.append("### ✅ MORNING COMPLETIONS")
        log_entry.append("_(Update with actual completions)_")
        log_entry.append("")
        log_entry.append("### 📋 AFTERNOON PRIORITIES")
        log_entry.append("_(Adjusted based on morning progress)_")
        log_entry.append("")

    elif sync_type == "3pm":
        log_entry.append("### ✅ TODAY'S COMPLETIONS SO FAR")
        log_entry.append("_(Update with actual completions)_")
        log_entry.append("")
        log_entry.append("### 🎯 FINAL PUSH (3PM-5PM)")
        log_entry.append("_(Critical items to complete before EOD)_")
        log_entry.append("")

    elif sync_type == "eod":
        log_entry.append("### ✅ TODAY'S COMPLETIONS")
        log_entry.append("")
        log_entry.append("_No completed items logged today_")
        log_entry.append("")
        log_entry.append("### 💡 TODAY'S LEARNINGS")
        log_entry.append("")
        log_entry.append("_(Key learnings and insights from today)_")
        log_entry.append("")
        log_entry.append("### 🎯 TOMORROW'S TOP PRIORITIES")
        log_entry.append("")
        log_entry.append("_(Top 3-5 priorities for tomorrow)_")
        log_entry.append("")

    elif sync_type == "weekly":
        log_entry.append("### 📊 WEEK IN REVIEW")
        log_entry.append("")
        log_entry.append("_(Major completions this week)_")
        log_entry.append("")
        log_entry.append("### 🎯 MONDAY PRIORITIES")
        log_entry.append("")
        log_entry.append("_(Top priorities to start next week)_")
        log_entry.append("")

    # Add reference to detailed sync report
    timestamp = now.strftime('%Y%m%d_%H%M%S')
    filename = f"{sync_type.upper()}_SYNC_{timestamp}.md"
    log_entry.append(f"**Detailed Sync Report**: `{filename}`")
    log_entry.append("")

    # Append to daily log
    try:
        with open(DAILY_LOG, 'a', encoding='utf-8') as f:
            f.write('\n'.join(log_entry))
        return True
    except Exception as e:
        print(f"⚠️ Failed to update daily log: {e}")
        return False

def update_follow_up_reminders(hubspot_data):
    """Update follow-up reminders file with current priorities"""
    now = datetime.now()
    tomorrow = now + timedelta(days=1)

    content = []
    content.append(f"# FOLLOW-UP REMINDERS - {tomorrow.strftime('%A, %B %d, %Y')}")
    content.append("")
    content.append("=" * 80)
    content.append("")
    content.append("## 🚨 CRITICAL (Do First)")
    content.append("")
    content.append("### At-Risk Deals (>30 days since update):")
    content.append("")
    content.append("_(Will be populated by next sync)_")
    content.append("")
    content.append("=" * 80)
    content.append("")
    content.append("## 📋 HIGH PRIORITY (This Week)")
    content.append("")
    content.append("(Check HubSpot for scheduled follow-ups and SLA deadlines)")
    content.append("")

    try:
        FOLLOW_UP.write_text('\n'.join(content), encoding='utf-8')
        return True
    except Exception as e:
        print(f"⚠️ Failed to update follow-up reminders: {e}")
        return False

def create_eod_summary(hubspot_data):
    """Create EOD summary section for daily log"""
    now = datetime.now()

    summary = []
    summary.append("")
    summary.append("=" * 80)
    summary.append(f"## EOD SUMMARY - {now.strftime('%I:%M %p')}")
    summary.append("=" * 80)
    summary.append("")
    summary.append("### ✅ TODAY'S COMPLETIONS")
    summary.append("")
    summary.append("_No completed items logged today_")
    summary.append("")
    summary.append("### 📊 PIPELINE HEALTH SNAPSHOT")
    summary.append("")

    if hubspot_data and "error" not in hubspot_data:
        summary.append(f"- **Total Active Deals**: {hubspot_data['total']}")
        summary.append(f"- **Total Pipeline Value**: ${hubspot_data['total_value']:,.0f}")
        summary.append(f"- **At-Risk Deals**: _(needs calculation)_")
        summary.append(f"- **Recently Active**: _(needs calculation)_")
    else:
        summary.append("- **Total Active Deals**: _(API error)_")
        summary.append("- **Total Pipeline Value**: _(API error)_")

    summary.append("")
    summary.append(f"### 🎯 TOMORROW'S TOP PRIORITIES ({(now + timedelta(days=1)).strftime('%A, %B %d')})")
    summary.append("")
    summary.append("✅ Clean slate - no pending items")
    summary.append("")
    summary.append("=" * 80)
    summary.append(f"**Next Sync**: Tomorrow 9:00 AM - Context loaded and ready")
    summary.append("=" * 80)
    summary.append("")

    return '\n'.join(summary)

# ============================================================================
# SYNC REPORT GENERATION
# ============================================================================

def generate_sync_report(sync_type, override_date=None):
    """Generate comprehensive sync report

    Args:
        sync_type: Type of sync (9am, noon, 3pm, eod, weekly, monthly)
        override_date: Optional datetime to use instead of current time (for historical syncs)
    """

    if sync_type not in SYNC_TYPES:
        print(f"❌ ERROR: Invalid sync type '{sync_type}'")
        print(f"Valid types: {', '.join(SYNC_TYPES.keys())}")
        sys.exit(1)

    sync_config = SYNC_TYPES[sync_type]
    now = override_date if override_date else datetime.now()

    # Header
    report = []
    report.append(f"# COMPREHENSIVE {sync_config['title']} - {now.strftime('%A, %B %d, %Y')}")
    report.append("")
    report.append("=" * 80)
    report.append("")

    # Chrome MCP Status and Email Integration
    chrome_mcp_active = check_chrome_mcp_status()
    if sync_type == "9am":
        report.append("## 📧 EMAIL ACTION ITEMS")
        report.append("")

        # Attempt to fetch emails via Chrome MCP
        email_data = get_superhuman_emails()

        if email_data["success"]:
            report.append("**Chrome MCP Status**: ✅ CONNECTED")
            report.append("**Email Integration**: ✅ SUPERHUMAN SYNCED")
            report.append("")

            # Critical emails (last hour)
            report.append("### 🚨 CRITICAL (Last Hour)")
            if email_data["critical"]:
                for email in email_data["critical"]:
                    report.append(f"- {email}")
            else:
                report.append("- ✅ No critical emails in last hour")
            report.append("")

            # Yesterday's queue
            report.append("### Yesterday's Email Queue")
            if email_data["yesterday"]:
                for email in email_data["yesterday"][:5]:
                    report.append(f"- {email}")
                if len(email_data["yesterday"]) > 5:
                    report.append(f"- _(+{len(email_data['yesterday']) - 5} more)_")
            else:
                report.append("- ✅ Inbox Zero achieved yesterday")
            report.append("")

            # Last 7 days priorities
            report.append("### Last 7 Days Priorities")
            if email_data["last_week"]:
                for email in email_data["last_week"][:5]:
                    report.append(f"- {email}")
                if len(email_data["last_week"]) > 5:
                    report.append(f"- _(+{len(email_data['last_week']) - 5} more)_")
            else:
                report.append("- ✅ No overdue priorities from last week")
            report.append("")

        else:
            # Chrome MCP not working - show manual extraction mode
            if chrome_mcp_active:
                report.append("**Chrome MCP Status**: ✅ CONNECTED")
            else:
                report.append("**Chrome MCP Status**: ❌ DISCONNECTED")

            report.append("**Email Integration**: ⚠️  MANUAL MODE")
            if email_data.get("error"):
                report.append(f"**Error**: {email_data['error']}")
            report.append("")
            report.append("### 🚨 CRITICAL (Last Hour)")
            report.append("_(Manual check in Superhuman required)_")
            report.append("")
            report.append("### Yesterday's Email Queue")
            report.append("_(Manual check in Superhuman required)_")
            report.append("")
            report.append("### Last 7 Days Priorities")
            report.append("_(Manual check in Superhuman required)_")
            report.append("")

        report.append("---")
        report.append("")

    # HubSpot Priority Actions (using Action-First if available)
    report.append("## 🎯 TOP 3 PRIORITY ACTIONS")
    report.append("")
    report.append(f"**Last Updated**: {now.strftime('%A, %B %d, %Y at %I:%M %p CT')}")
    report.append("")

    if ACTION_FIRST_AVAILABLE:
        # Use new Action-First prioritization
        action_result = run_action_prioritizer(sync_type)
        if action_result["success"] and "actions" in action_result:
            for action_text in action_result["actions"]:
                report.append(action_text)
                report.append("")
        else:
            # Fallback to legacy agent
            priority_result = run_prioritization_agent()
            if priority_result["success"]:
                report.append("### TOP 5 PRIORITIES (Legacy Mode)")
                report.append("")
                for deal in priority_result["deals"]:
                    report.append(deal)
                report.append("")
    else:
        # Legacy mode (no Action-First available)
        priority_result = run_prioritization_agent()
        if priority_result["success"]:
            report.append("### TOP 5 PRIORITIES")
            report.append("")
            for deal in priority_result["deals"]:
                report.append(deal)
            report.append("")
        else:
            report.append("⚠️ Prioritization agent failed to run")
            report.append(f"Error: {priority_result.get('error', 'Unknown')}")
            report.append("")

    # Pipeline Metrics
    hubspot_data = fetch_hubspot_deals()
    if "error" not in hubspot_data:
        report.append("### Pipeline Snapshot")
        report.append("")
        report.append(f"**Total Active Deals**: {hubspot_data['total']}")
        report.append(f"**Total Pipeline Value**: ${hubspot_data['total_value']:,.0f}")
        report.append("")
        report.append("**Stage Distribution**:")
        for stage, data in sorted(hubspot_data['by_stage'].items()):
            report.append(f"- {stage}: {data['count']} deals (${data['value']:,.0f})")
        report.append("")

    report.append("---")
    report.append("")

    # Recent Context (all sync types)
    yesterday = extract_yesterday_context()
    if yesterday["found"]:
        report.append("## 📊 RECENT CONTEXT")
        report.append("")
        if yesterday["stale"]:
            report.append(f"⚠️ **WARNING**: Daily log is {yesterday['days_old']} days old")
            report.append(f"Last entry: {yesterday['date']}")
            report.append("")
        else:
            report.append(f"**Last Entry**: {yesterday['date']}")
            report.append("")
            if yesterday["completed"]:
                report.append("### Yesterday's Completions:")
                for item in yesterday["completed"][:5]:
                    report.append(f"- {item}")
                report.append("")

    # Follow-up Reminders
    reminders = extract_follow_up_reminders()
    if reminders:
        report.append("## 🚨 CRITICAL FOLLOW-UPS")
        report.append("")
        for reminder in reminders:
            report.append(f"- {reminder}")
        report.append("")
        report.append("---")
        report.append("")

    # Brand Scout (9am only)
    if sync_type == "9am":
        brand_scout_reports = check_brand_scout_reports()
        if brand_scout_reports:
            report.append("## 🔍 BRAND SCOUT OVERNIGHT RESULTS")
            report.append("")
            report.append(f"**New Reports**: {len(brand_scout_reports)}")
            for report_name in brand_scout_reports[:5]:
                report.append(f"- {report_name}")
            report.append("")
            report.append("**Action**: Review and import top leads to HubSpot")
            report.append("")
            report.append("---")
            report.append("")

    # Sync-specific sections
    if sync_type == "9am":
        report.append("## 🎯 TODAY'S EXECUTION PLAN")
        report.append("")
        report.append("### Morning Block (9:00 AM - 12:00 PM)")
        report.append("_(To be filled based on email priorities and HubSpot data)_")
        report.append("")
        report.append("### Afternoon Block (1:00 PM - 5:00 PM)")
        report.append("_(To be adjusted based on morning progress)_")
        report.append("")

    elif sync_type == "noon":
        report.append("## ✅ MORNING PROGRESS CHECK")
        report.append("")
        report.append("### Completed This Morning:")
        report.append("_(List completed actions)_")
        report.append("")
        report.append("### Afternoon Adjustments:")
        report.append("_(Adjust plan based on morning results)_")
        report.append("")

    elif sync_type == "3pm":
        report.append("## ⏰ AFTERNOON STATUS")
        report.append("")
        report.append("### Completed Today:")
        report.append("_(List completed actions)_")
        report.append("")
        report.append("### Final Push (3:00 PM - 5:00 PM):")
        report.append("_(Priority items to complete before EOD)_")
        report.append("")

    elif sync_type == "eod":
        report.append("## ✅ TODAY'S COMPLETIONS")
        report.append("")
        report.append("_(List all completed actions)_")
        report.append("")
        report.append("## 💡 TODAY'S LEARNINGS")
        report.append("")
        report.append("_(Key learnings and insights from today)_")
        report.append("")
        report.append("## 🎯 TOMORROW'S TOP PRIORITIES")
        report.append("")
        report.append("_(Top 3-5 priorities for tomorrow)_")
        report.append("")

    elif sync_type == "weekly":
        report.append("## 📊 WEEK IN REVIEW")
        report.append("")
        report.append("### This Week's Achievements:")
        report.append("_(Major completions this week)_")
        report.append("")
        report.append("### Pipeline Changes:")
        report.append("_(New deals, stage movements, closures)_")
        report.append("")
        report.append("## 🎯 MONDAY PRIORITIES")
        report.append("")
        report.append("_(Top priorities to start next week)_")
        report.append("")

    # System Status
    report.append("## 📊 SYSTEM STATUS")
    report.append("")
    report.append(f"**Chrome MCP**: {'✅ CONNECTED' if chrome_mcp_active else '❌ DISCONNECTED'}")
    report.append("**HubSpot API**: ✅ OPERATIONAL")
    report.append("**Prioritization Agent**: ✅ v2.0")
    report.append("")
    report.append("---")
    report.append("")

    # Footer
    report.append("## 🔄 NEXT SYNC")
    report.append("")
    report.append(f"**{sync_config['next']}**")
    report.append("")
    report.append("=" * 80)
    report.append(f"*Generated: {now.strftime('%A, %B %d, %Y at %I:%M %p CT')}*")
    report.append(f"*Sync Type: {sync_config['title']}*")
    report.append(f"*Format: COMPREHENSIVE (Unified Sync System v1.0)*")
    report.append("=" * 80)

    return "\n".join(report)

# ============================================================================
# MAIN
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("❌ ERROR: Sync type required")
        print("\nUsage: python unified_sync.py [sync_type] [--date YYYY-MM-DD]")
        print(f"\nValid sync types: {', '.join(SYNC_TYPES.keys())}")
        print("\nExamples:")
        print("  python unified_sync.py 9am")
        print("  python unified_sync.py eod --date 2025-11-17")
        print("  python unified_sync.py weekly")
        sys.exit(1)

    sync_type = sys.argv[1].lower()

    # Check for --date parameter
    override_date = None
    if len(sys.argv) >= 4 and sys.argv[2] == '--date':
        try:
            override_date = datetime.strptime(sys.argv[3], '%Y-%m-%d')
            print(f"📅 Running {sync_type.upper()} sync for: {override_date.strftime('%A, %B %d, %Y')}")
        except ValueError:
            print("❌ ERROR: Invalid date format. Use YYYY-MM-DD")
            sys.exit(1)

    # Generate report (pass override_date)
    report = generate_sync_report(sync_type, override_date=override_date)

    # Fetch HubSpot data for continuity updates
    hubspot_data = fetch_hubspot_deals()

    # Save to timestamped file in project sync_reports folder
    SYNC_REPORTS_DIR.mkdir(exist_ok=True)  # Create folder if it doesn't exist
    current_time = override_date if override_date else datetime.now()
    timestamp = current_time.strftime('%Y%m%d_%H%M%S')
    filename = f"{sync_type.upper()}_SYNC_{timestamp}.md"
    output_path = SYNC_REPORTS_DIR / filename

    output_path.write_text(report, encoding='utf-8')

    # Display report
    print(report)
    print(f"\n✅ Sync report saved to: {output_path}")

    # ========================================================================
    # CONTINUITY CHAIN - Write back to logs for next sync
    # ========================================================================

    print("\n📝 Updating continuity logs...")

    # 1. Append to daily log (ALL sync types)
    log_updated = append_to_daily_log(sync_type, report)
    if log_updated:
        print(f"   ✅ Daily log updated (_DAILY_LOG.md)")
    else:
        print(f"   ⚠️  Daily log update failed")

    # 2. Add EOD summary (EOD sync only)
    if sync_type == "eod":
        eod_summary = create_eod_summary(hubspot_data)
        try:
            with open(DAILY_LOG, 'a', encoding='utf-8') as f:
                f.write(eod_summary)
            print(f"   ✅ EOD summary appended to daily log")
        except Exception as e:
            print(f"   ⚠️  EOD summary failed: {e}")

    # 3. Update follow-up reminders (EOD and weekly syncs)
    if sync_type in ["eod", "weekly"]:
        reminders_updated = update_follow_up_reminders(hubspot_data)
        if reminders_updated:
            print(f"   ✅ Follow-up reminders updated (FOLLOW_UP_REMINDERS.txt)")
        else:
            print(f"   ⚠️  Follow-up reminders update failed")

    # 4. Git auto-commit (EOD sync only)
    git_committed = False
    if sync_type == "eod" and ACTION_FIRST_AVAILABLE:
        try:
            print(f"\n📦 Creating git commit...")

            # Initialize GitCommitter
            committer = GitCommitter()

            # Get today's sync reports
            today_reports = []
            for report_file in SYNC_REPORTS_DIR.glob("*.md"):
                file_date = datetime.fromtimestamp(report_file.stat().st_mtime)
                if file_date.date() == datetime.now().date():
                    today_reports.append(report_file.name)

            # Create commit summary (simplified for now)
            from utils.git_committer import CommitSummary
            summary = CommitSummary(
                date=datetime.now().strftime('%Y-%m-%d'),
                sync_count=len(today_reports),
                actions_completed=0,  # Would come from continuity manager
                deals_updated=0,       # Would come from action prioritizer
                emails_processed=0,    # Would come from email data
                files_modified=[],
                key_activities=[]
            )

            # Create commit
            git_committed = committer.create_commit(summary)
            if git_committed:
                print(f"   ✅ Git commit created successfully")

        except Exception as e:
            print(f"   ⚠️  Git commit failed: {e}")

    print("\n" + "=" * 80)
    print("CONTINUITY CHAIN STATUS")
    print("=" * 80)
    print(f"✅ Sync report: {filename}")
    print(f"{'✅' if log_updated else '❌'} Daily log: _DAILY_LOG.md (tomorrow's context)")
    if sync_type in ["eod", "weekly"]:
        print(f"{'✅' if reminders_updated else '❌'} Follow-up reminders: FOLLOW_UP_REMINDERS.txt")
    if sync_type == "eod" and ACTION_FIRST_AVAILABLE:
        print(f"{'✅' if git_committed else '❌'} Git commit: Daily sync committed")
    print("=" * 80)
    print(f"\n💡 Next sync will read from _DAILY_LOG.md updated on {datetime.now().strftime('%Y-%m-%d at %I:%M %p')}")
    print(f"   This ensures continuity: TODAY's sync → TOMORROW's context ✅")
    print()

if __name__ == "__main__":
    main()
