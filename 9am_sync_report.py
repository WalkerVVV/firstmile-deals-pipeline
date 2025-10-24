"""
9AM Sync Report Generator
Analyzes pipeline status and generates daily sync report
"""

import os
from datetime import datetime
from collections import defaultdict

# Get current timestamp
now = datetime.now()
timestamp = now.strftime("%Y-%m-%d %I:%M %p MST")
date_str = now.strftime("%Y-%m-%d")

print("=" * 80)
print("NEBUCHADNEZZAR v2.0 - 9AM SYNC REPORT")
print("=" * 80)
print(f"Generated: {timestamp}")
print()

# Define pipeline stages
stages = {
    "00-LEAD": "Lead (New Inquiry)",
    "00-NEW-LEADS": "New Lead",
    "01-DISCOVERY-SCHEDULED": "Discovery Scheduled",
    "01-QUALIFIED": "Qualified Lead",
    "02-DISCOVERY": "Discovery Phase",
    "02-DISCOVERY-COMPLETE": "Discovery Complete",
    "03-RATE-CREATION": "Rate Creation (Bottleneck)",
    "04-PROPOSAL-SENT": "Proposal Sent",
    "05-SETUP-DOCS": "Setup Docs",
    "05-SETUP-DOCS-SENT": "Setup Docs Sent",
    "06-CLOSED-WON": "Closed Won",
    "06-IMPLEMENTATION": "Implementation",
    "07-CLOSED-WON": "Closed Won",
    "07-CLOSED-LOST": "Closed Lost",
    "08-CLOSED-LOST": "Closed Lost",
    "09-WIN-BACK": "Win Back",
    "WIN-BACK": "Win Back",
    "CUSTOMER": "Active Customer"
}

# Scan deal folders
deals_path = "C:\\Users\\BrettWalker\\FirstMile_Deals"
deals_by_stage = defaultdict(list)
templates = []
placeholders = []

for folder in os.listdir(deals_path):
    folder_path = os.path.join(deals_path, folder)
    if os.path.isdir(folder_path) and folder.startswith("["):
        # Extract stage
        if "]_" in folder:
            stage_part = folder.split("]")[0][1:]
            deal_name = folder.split("]_")[1]

            # Skip templates and placeholders
            if "TEMPLATE" in deal_name.upper() or "Template" in deal_name:
                templates.append(folder)
                continue
            if "PLACEHOLDER" in deal_name.upper():
                placeholders.append(folder)
                continue
            if deal_name == "PDR":
                continue

            deals_by_stage[stage_part].append(deal_name)

# Generate report
print("=" * 80)
print("PIPELINE SNAPSHOT")
print("=" * 80)
print()

# Sort stages
stage_order = [
    "00-LEAD", "00-NEW-LEADS", "01-DISCOVERY-SCHEDULED", "01-QUALIFIED",
    "02-DISCOVERY", "02-DISCOVERY-COMPLETE", "03-RATE-CREATION",
    "04-PROPOSAL-SENT", "05-SETUP-DOCS", "05-SETUP-DOCS-SENT",
    "06-IMPLEMENTATION", "06-CLOSED-WON", "07-CLOSED-WON", "07-CLOSED-LOST",
    "08-CLOSED-LOST", "09-WIN-BACK", "WIN-BACK", "CUSTOMER"
]

total_active_deals = 0
critical_stages = ["03-RATE-CREATION", "04-PROPOSAL-SENT", "06-IMPLEMENTATION"]

for stage in stage_order:
    if stage in deals_by_stage and len(deals_by_stage[stage]) > 0:
        stage_name = stages.get(stage, stage)
        count = len(deals_by_stage[stage])

        # Count active deals (exclude closed-lost and win-back)
        if stage not in ["07-CLOSED-LOST", "08-CLOSED-LOST", "09-WIN-BACK", "WIN-BACK"]:
            total_active_deals += count

        # Mark critical stages
        marker = " **CRITICAL**" if stage in critical_stages else ""

        print(f"{stage_name} [{stage}]: {count} deals{marker}")
        for deal in sorted(deals_by_stage[stage]):
            print(f"  - {deal}")
        print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()
print(f"Total Active Deals: {total_active_deals}")
print(f"Templates: {len(templates)}")
print(f"Placeholders: {len(placeholders)}")
print()

# Critical stages analysis
print("=" * 80)
print("CRITICAL STAGES REQUIRING ATTENTION")
print("=" * 80)
print()

bottleneck_count = len(deals_by_stage.get("03-RATE-CREATION", []))
proposal_count = len(deals_by_stage.get("04-PROPOSAL-SENT", []))
implementation_count = len(deals_by_stage.get("06-IMPLEMENTATION", []))

if bottleneck_count > 0:
    print(f"RATE CREATION BOTTLENECK: {bottleneck_count} deals")
    print("  Action: Prioritize rate creation to unblock pipeline")
    for deal in deals_by_stage.get("03-RATE-CREATION", []):
        print(f"    - {deal}")
    print()

if proposal_count > 0:
    print(f"PROPOSAL SENT: {proposal_count} deals awaiting response")
    print("  Action: Follow up on proposals (30-day follow-up cadence)")
    for deal in deals_by_stage.get("04-PROPOSAL-SENT", []):
        print(f"    - {deal}")
    print()

if implementation_count > 0:
    print(f"IMPLEMENTATION: {implementation_count} deals in onboarding")
    print("  Action: Complete before peak season (Halloween deadline)")
    for deal in deals_by_stage.get("06-IMPLEMENTATION", []):
        print(f"    - {deal}")
    print()

# Peak season urgency
print("=" * 80)
print("PEAK SEASON URGENCY (Halloween Deadline)")
print("=" * 80)
print()
print("Current Date: October 14, 2025")
print("Peak Season: Active (surcharges live since Oct 5)")
print("Onboarding Window: CLOSING (typically until Halloween)")
print()
print("URGENT ACTIONS:")
print("  - Complete all pending integrations before peak ramps up")
print("  - Send peak season surcharge notices to new customers")
print("  - Prioritize costume/decoration customers for quick close")
print()

# Top priority deals
print("=" * 80)
print("TOP PRIORITY DEALS (Next 24 Hours)")
print("=" * 80)
print()

priorities = []

# Discovery scheduled - need to complete discovery
discovery_scheduled = deals_by_stage.get("01-DISCOVERY-SCHEDULED", [])
if discovery_scheduled:
    print("1. DISCOVERY SCHEDULED - Complete meetings:")
    for deal in discovery_scheduled:
        print(f"   - {deal}")
    print()

# Discovery complete - move to rate creation
discovery_complete = deals_by_stage.get("02-DISCOVERY-COMPLETE", [])
if discovery_complete:
    print("2. DISCOVERY COMPLETE - Move to rate creation:")
    for deal in discovery_complete:
        print(f"   - {deal}")
    print()

# Rate creation - unblock pipeline
if bottleneck_count > 0:
    print("3. RATE CREATION - Unblock pipeline:")
    for deal in deals_by_stage.get("03-RATE-CREATION", []):
        print(f"   - {deal}")
    print()

# Proposal sent - follow up
if proposal_count > 0:
    print("4. PROPOSAL SENT - Follow up on pending proposals:")
    for deal in deals_by_stage.get("04-PROPOSAL-SENT", []):
        print(f"   - {deal} (30-day follow-up)")
    print()

print("=" * 80)
print("DOMAIN-MEMORY-AGENT INTEL")
print("=" * 80)
print()
print("Recent Intelligence Stored:")
print("  - Stackd Logistics: Final verified analysis (9.5% savings, $41,773 annual)")
print("  - Josh's Frogs: Small shipper, lightweight profile")
print("  - JM Group NY: Active customer, strong relationship")
print("  - Athleta (Gap Inc.): High-value opportunity, $40M spend")
print("  - Cleetus McFarland: YouTube creator, 138K volume")
print()
print("Foundational Knowledge:")
print("  - Xparcel Core Concepts")
print("  - Sales Call Cheat Sheet")
print("  - 2025 Peak Season Surcharges")
print("  - Sales Meeting Notes (Sept 17, Oct 1, Oct 8)")
print()

print("=" * 80)
print("END 9AM SYNC REPORT")
print("=" * 80)
