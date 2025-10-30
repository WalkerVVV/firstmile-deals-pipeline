#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SALES EXECUTION AGENT
Purpose: Force sales discipline - auto-generate urgency follow-ups, track stagnation
Coaching directive: "Revenue-generating activities ALWAYS come before systems improvements"
"""

import sys, io, os, re
from datetime import datetime, timedelta
from pathlib import Path
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Repository root
REPO_ROOT = Path(__file__).parent.parent.parent
DOWNLOADS = Path.home() / "Downloads"

# Stage folder patterns
PROPOSAL_SENT_STAGE = "[04-PROPOSAL-SENT]"
RATE_CREATION_STAGE = "[03-RATE-CREATION]"

# Stagnation rules (days)
SOFT_FOLLOWUP_DAYS = 7
URGENT_FOLLOWUP_DAYS = 14
FINAL_PUSH_DAYS = 21
WINBACK_MOVE_DAYS = 60

# Email templates
EMAIL_TEMPLATES = {
    "day_7": """Subject: Quick check-in - {customer_name} Xparcel proposal

Hi {contact_name},

Following up on the Xparcel rates I sent last week.

Have you had a chance to review the ${savings:,} annual savings projection?

Happy to jump on a quick call to answer any questions.

Best,
Brett
""",

    "day_14": """Subject: Peak season capacity update - {customer_name}

Hi {contact_name},

Peak season starts this week. Our Select Network is at 90% capacity for Xparcel Expedited.

To lock in the ${savings:,} savings we discussed, I need your verbal commit by EOD {deadline_date}.

Can you jump on a 15-minute call {tomorrow_date} to finalize?

Brett
""",

    "day_21": """Subject: Final pricing hold - {customer_name}

{contact_name},

I've held your Xparcel pricing for 3 weeks, but I need to release this capacity by {final_deadline}.

Two options:
1. Verbal commit by EOD {deadline_date} → lock in current rates
2. Pass for now → I'll circle back in Q1 2026

Which direction makes sense?

Brett
""",

    "day_60": """Subject: Reconnecting in 2026 - {customer_name}

{contact_name},

I haven't heard back since {original_date}, so I'm assuming the timing wasn't right.

I'll plan to reconnect in Q1 2026 when budgets reset.

If anything changes before then, you know where to find me.

Best,
Brett
"""
}


def get_deal_folders():
    """Get all deal folders with stage prefix"""
    deal_folders = []

    for folder in REPO_ROOT.iterdir():
        if folder.is_dir() and folder.name.startswith('['):
            # Extract stage, customer name, value from folder
            match = re.match(r'\[(\d+)-([^\]]+)\]_(.+)', folder.name)
            if match:
                stage_num = match.group(1)
                stage_name = match.group(2)
                customer_name = match.group(3).replace('_', ' ')

                deal_folders.append({
                    'folder': folder,
                    'stage': f"[{stage_num}-{stage_name}]",
                    'customer': customer_name,
                    'stage_num': int(stage_num)
                })

    return deal_folders


def get_folder_last_modified_days(folder):
    """Get days since folder was last modified"""
    try:
        # Check git log for last commit touching this folder
        import subprocess
        result = subprocess.run(
            ['git', 'log', '-1', '--format=%ct', '--', str(folder)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )

        if result.stdout.strip():
            last_commit_timestamp = int(result.stdout.strip())
            last_modified = datetime.fromtimestamp(last_commit_timestamp)
            days_ago = (datetime.now() - last_modified).days
            return days_ago
        else:
            # No git history, use filesystem mtime
            mtime = folder.stat().st_mtime
            last_modified = datetime.fromtimestamp(mtime)
            days_ago = (datetime.now() - last_modified).days
            return days_ago
    except:
        return 0


def extract_deal_value(folder):
    """Extract deal value from Customer_Relationship_Documentation.md or README"""
    deal_value = 0

    for doc_file in ['Customer_Relationship_Documentation.md', 'README.md']:
        doc_path = folder / doc_file
        if doc_path.exists():
            content = doc_path.read_text(encoding='utf-8', errors='ignore')

            # Look for deal value patterns
            value_patterns = [
                r'\$([0-9,]+)K',  # $950K
                r'\$([0-9,]+)M',  # $25M
                r'\$([0-9,]+)',   # $950000
                r'([0-9,]+)\s*shipments',  # 15,000 shipments
            ]

            for pattern in value_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    value_str = matches[0].replace(',', '')
                    try:
                        if 'K' in content:
                            deal_value = int(value_str) * 1000
                        elif 'M' in content:
                            deal_value = int(value_str) * 1000000
                        else:
                            deal_value = int(value_str)
                        break
                    except:
                        pass

    return deal_value


def extract_contact_info(folder):
    """Extract primary contact name from deal folder"""
    contact_name = "there"  # Default

    for doc_file in ['Customer_Relationship_Documentation.md', 'README.md']:
        doc_path = folder / doc_file
        if doc_path.exists():
            content = doc_path.read_text(encoding='utf-8', errors='ignore')

            # Look for contact name patterns
            contact_patterns = [
                r'Contact:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
                r'Primary Contact:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
                r'Name:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            ]

            for pattern in contact_patterns:
                match = re.search(pattern, content)
                if match:
                    contact_name = match.group(1)
                    break

            if contact_name != "there":
                break

    return contact_name


def generate_follow_up_email(deal, days_stagnant):
    """Generate urgency-based follow-up email based on stagnation days"""

    customer_name = deal['customer']
    contact_name = extract_contact_info(deal['folder'])
    deal_value = extract_deal_value(deal['folder'])
    savings = deal_value * 0.40  # 40% savings target

    # Determine which template to use
    if days_stagnant >= FINAL_PUSH_DAYS:
        template_key = "day_21"
    elif days_stagnant >= URGENT_FOLLOWUP_DAYS:
        template_key = "day_14"
    else:
        template_key = "day_7"

    template = EMAIL_TEMPLATES[template_key]

    # Fill in template variables
    tomorrow = datetime.now() + timedelta(days=1)
    deadline = datetime.now() + timedelta(days=2)
    final_deadline = datetime.now() + timedelta(days=7)
    original_date = datetime.now() - timedelta(days=days_stagnant)

    email = template.format(
        customer_name=customer_name,
        contact_name=contact_name,
        savings=int(savings),
        tomorrow_date=tomorrow.strftime('%A'),
        deadline_date=deadline.strftime('%A'),
        final_deadline=final_deadline.strftime('%B %d'),
        original_date=original_date.strftime('%B %d')
    )

    return email


def scan_stale_proposals():
    """Scan [04-PROPOSAL-SENT] for stale deals"""
    print("\n" + "="*80)
    print("SALES EXECUTION AGENT - STALE PROPOSAL SCANNER")
    print("="*80 + "\n")

    deal_folders = get_deal_folders()
    proposal_deals = [d for d in deal_folders if d['stage'] == PROPOSAL_SENT_STAGE]

    if not proposal_deals:
        print(f"✅ No deals in {PROPOSAL_SENT_STAGE}\n")
        return

    print(f"📊 Found {len(proposal_deals)} deals in {PROPOSAL_SENT_STAGE}\n")

    # Analyze each deal
    stale_deals = []

    for deal in proposal_deals:
        days_stagnant = get_folder_last_modified_days(deal['folder'])
        deal_value = extract_deal_value(deal['folder'])

        if days_stagnant >= SOFT_FOLLOWUP_DAYS:
            stale_deals.append({
                'deal': deal,
                'days': days_stagnant,
                'value': deal_value,
                'urgency': 'CRITICAL' if days_stagnant >= URGENT_FOLLOWUP_DAYS else 'MEDIUM'
            })

    if not stale_deals:
        print(f"✅ No stale deals (all < {SOFT_FOLLOWUP_DAYS} days)\n")
        return

    # Sort by urgency (days stagnant) and value
    stale_deals.sort(key=lambda x: (x['days'], -x['value']), reverse=True)

    print("="*80)
    print("🚨 STALE PROPOSALS REQUIRING FOLLOW-UP")
    print("="*80 + "\n")

    for i, item in enumerate(stale_deals, 1):
        deal = item['deal']
        days = item['days']
        value = item['value']
        urgency = item['urgency']

        urgency_emoji = "🔥" if urgency == "CRITICAL" else "⚠️"

        print(f"{urgency_emoji} {i}. {deal['customer']} - {days} days stagnant")
        print(f"   Value: ${value:,} | Stage: {deal['stage']}")
        print(f"   Action: {'URGENT FOLLOW-UP' if days >= URGENT_FOLLOWUP_DAYS else 'Follow-up needed'}")

        if days >= WINBACK_MOVE_DAYS:
            print(f"   ⚠️  60-DAY RULE: Consider moving to [09-WIN-BACK]")

        print()

    # Generate follow-up emails
    print("="*80)
    print("📧 AUTO-GENERATED FOLLOW-UP EMAILS (REVIEW & SEND)")
    print("="*80 + "\n")

    for i, item in enumerate(stale_deals[:5], 1):  # Top 5 most urgent
        deal = item['deal']
        days = item['days']

        print(f"\n{'='*80}")
        print(f"EMAIL {i}: {deal['customer']} ({days} days)")
        print('='*80)

        email = generate_follow_up_email(deal, days)
        print(email)

        # Save to file for easy copy-paste
        email_file = deal['folder'] / f"FOLLOWUP_EMAIL_{datetime.now().strftime('%Y%m%d')}.txt"
        email_file.write_text(email, encoding='utf-8')
        print(f"\n📄 Saved to: {email_file.relative_to(REPO_ROOT)}\n")

    print("\n" + "="*80)
    print(f"✅ Generated {min(len(stale_deals), 5)} follow-up emails")
    print("="*80 + "\n")


def main():
    """Main execution"""
    scan_stale_proposals()

    print("\n🎯 NEXT ACTIONS:")
    print("1. Review generated follow-up emails above")
    print("2. Customize if needed (add deal-specific details)")
    print("3. Send via email")
    print("4. Log activity in HubSpot")
    print("\n")


if __name__ == "__main__":
    main()
