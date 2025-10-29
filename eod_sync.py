#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EOD SYNC - End of Day Rollover
Rolls over incomplete items from today to tomorrow's action queue
Ensures workflow continuity: Today → Tomorrow
"""

import sys, io, os, re
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DOWNLOADS = Path.home() / "Downloads"
DAILY_LOG = DOWNLOADS / "_DAILY_LOG.md"
FOLLOW_UP = DOWNLOADS / "FOLLOW_UP_REMINDERS.txt"

def extract_todays_context():
    """Extract today's completed and pending items"""
    if not DAILY_LOG.exists():
        return {"completed": [], "pending": []}

    content = DAILY_LOG.read_text(encoding='utf-8')
    context = {"completed": [], "pending": []}

    # Extract completed items
    completed_section = re.search(r'COMPLETED.*?\n(.*?)(?=\n##|PRIORITY|\Z)', content, re.DOTALL)
    if completed_section:
        for line in completed_section.group(1).split('\n'):
            if '✅' in line:
                context["completed"].append(line.strip())

    # Extract afternoon/pending items
    afternoon_section = re.search(r'AFTERNOON.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if afternoon_section:
        for line in afternoon_section.group(1).split('\n'):
            if line.strip() and ('**' in line or '🚨' in line or line.strip().startswith(tuple('123456789'))):
                context["pending"].append(line.strip())

    return context

def generate_tomorrow_action_queue(todays_context):
    """Generate prioritized action queue for tomorrow"""
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%A, %B %d, %Y')

    queue = []
    queue.append(f"# FOLLOW-UP REMINDERS - {tomorrow_str}")
    queue.append("")
    queue.append("## 🚨 CRITICAL (Do First)")
    queue.append("")

    if todays_context["pending"]:
        for i, item in enumerate(todays_context["pending"][:5], 1):
            queue.append(f"{i}. {item}")
    else:
        queue.append("✅ No critical items rolled over from today")

    queue.append("")
    queue.append("=" * 80)
    queue.append("")
    queue.append("## 📋 HIGH PRIORITY (This Week)")
    queue.append("")
    queue.append("(Add additional items as needed)")
    queue.append("")

    return "\n".join(queue)

def append_to_daily_log(todays_context):
    """Append EOD summary to daily log"""
    eod_summary = []
    eod_summary.append("")
    eod_summary.append("## EOD SUMMARY")
    eod_summary.append("")
    eod_summary.append(f"**Completed Today**: {len(todays_context['completed'])} items")
    eod_summary.append(f"**Rolled to Tomorrow**: {len(todays_context['pending'])} items")
    eod_summary.append("")

    if todays_context["pending"]:
        eod_summary.append("### Pending Items (Rolled Over):")
        for item in todays_context["pending"]:
            eod_summary.append(f"  • {item}")

    eod_summary.append("")

    with open(DAILY_LOG, 'a', encoding='utf-8') as f:
        f.write("\n".join(eod_summary))

def main():
    print("\n" + "="*80)
    print("EOD SYNC - END OF DAY ROLLOVER")
    print(f"Today: {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
    print("="*80 + "\n")

    # Extract today's context
    print("📊 Analyzing today's activities...")
    todays_context = extract_todays_context()

    print(f"✅ Completed: {len(todays_context['completed'])} items")
    print(f"⏳ Pending: {len(todays_context['pending'])} items\n")

    # Generate tomorrow's action queue
    print("🔄 Generating tomorrow's action queue...")
    tomorrow_queue = generate_tomorrow_action_queue(todays_context)

    # Write to FOLLOW_UP_REMINDERS.txt
    with open(FOLLOW_UP, 'w', encoding='utf-8', newline='\n') as f:
        f.write(tomorrow_queue)

    print(f"✅ Updated: {FOLLOW_UP}")

    # Append to daily log
    print("📝 Appending EOD summary to daily log...")
    append_to_daily_log(todays_context)
    print(f"✅ Updated: {DAILY_LOG}\n")

    # Show tomorrow's top priorities
    tomorrow = datetime.now() + timedelta(days=1)
    print("=" * 80)
    print(f"🎯 TOMORROW'S TOP PRIORITIES ({tomorrow.strftime('%A, %B %d')})")
    print("=" * 80)

    if todays_context["pending"]:
        for i, item in enumerate(todays_context["pending"][:5], 1):
            print(f"{i}. {item}")
    else:
        print("✅ Clean slate - no pending items from today")

    print("\n✅ EOD sync complete. Tomorrow's 9AM sync will start with these priorities.\n")

if __name__ == "__main__":
    main()
