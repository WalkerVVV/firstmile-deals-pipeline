#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RUTHLESS PRIORITIZATION AGENT
Purpose: Ensure enterprise deals get 10x attention through scoring and time allocation
Coaching directive: "Enterprise deals require enterprise attention"

Usage: python prioritization_agent.py [--daily-reminder]
"""

import sys, io, os, re
from datetime import datetime
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Repository root
REPO_ROOT = Path(__file__).parent.parent.parent
DOWNLOADS = Path.home() / "Downloads"

# Priority scoring algorithm weights
SCORING_WEIGHTS = {
    "deal_size": 0.50,      # 50% - Deal value drives priority
    "stage": 0.20,          # 20% - Later stages need more attention
    "stagnation": 0.15,     # 15% - Stale deals need immediate action
    "complexity": 0.10,     # 10% - Complex deals need more time
    "strategic": 0.05       # 5% - Strategic accounts bonus
}

# Stage multipliers
STAGE_MULTIPLIERS = {
    "[00-LEAD]": 0.2,
    "[01-DISCOVERY-SCHEDULED]": 0.3,
    "[02-DISCOVERY-COMPLETE]": 0.4,
    "[03-RATE-CREATION]": 0.6,
    "[04-PROPOSAL-SENT]": 0.8,
    "[05-SETUP-DOCS-SENT]": 0.9,
    "[06-IMPLEMENTATION]": 1.0,
    "[07-CLOSED-WON]": 0.1,
    "[08-CLOSED-LOST]": 0.0,
    "[09-WIN-BACK]": 0.3
}

# Deal size thresholds (ARR)
DEAL_TIERS = {
    "mega": 10_000_000,      # $10M+ (Athleta, ODW)
    "enterprise": 1_000_000,  # $1M+ (Josh's Frogs, Upstate Prep)
    "mid_market": 500_000,    # $500K+ (Stackd, Logystico)
    "small": 100_000,         # $100K+ (smaller wellness brands)
    "micro": 0                # <$100K
}


def get_deal_folders():
    """Get all deal folders with stage prefix"""
    deal_folders = []

    for folder in REPO_ROOT.iterdir():
        # Skip _LEADS folder and other system folders
        if folder.name.startswith('_') or folder.name.startswith('.'):
            continue

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


def extract_deal_value(folder):
    """Extract deal value from ANY markdown file in folder"""
    deal_value = 0
    max_value = 0  # Track highest value found

    # Search ALL .md files in folder, not just specific names
    md_files = list(folder.glob('*.md'))

    for doc_path in md_files:
        try:
            content = doc_path.read_text(encoding='utf-8', errors='ignore')

            # Look for deal value patterns
            value_patterns = [
                (r'\$([0-9,.]+)M(?:\s+annual)?', 1000000),  # $2.34M, $25M annual
                (r'\$([0-9,.]+)K(?:\s+annual)?', 1000),     # $950K, $480K annual
                (r'([0-9,]+)\s+packages?(?:\s+annually)?', 100),  # 15,000 packages (rough $100/package assumption)
                (r'([0-9,]+)\s+shipments?(?:\s+annually)?', 100), # shipments
                (r'\$([0-9,.]+)\s+(?:annual|ARR|revenue)', 1),    # $2340000 annual revenue
            ]

            for pattern, multiplier in value_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    for match in matches:
                        value_str = match.replace(',', '').replace('.', '')
                        try:
                            # Handle decimal values (e.g., "2.34" in "$2.34M")
                            if '.' in match:
                                value = int(float(match.replace(',', '')) * multiplier)
                            else:
                                value = int(value_str) * multiplier

                            # Keep track of highest value found
                            if value > max_value:
                                max_value = value
                        except:
                            pass

        except:
            pass

    return max_value


def get_folder_last_modified_days(folder):
    """Get days since folder was last modified"""
    try:
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
            mtime = folder.stat().st_mtime
            last_modified = datetime.fromtimestamp(mtime)
            days_ago = (datetime.now() - last_modified).days
            return days_ago
    except:
        return 0


def calculate_priority_score(deal, deal_value, days_stagnant):
    """Calculate comprehensive priority score (0-100)"""

    score = 0

    # 1. Deal size score (0-50 points)
    if deal_value >= DEAL_TIERS["mega"]:
        size_score = 50
        tier = "MEGA"
    elif deal_value >= DEAL_TIERS["enterprise"]:
        size_score = 40
        tier = "ENTERPRISE"
    elif deal_value >= DEAL_TIERS["mid_market"]:
        size_score = 30
        tier = "MID-MARKET"
    elif deal_value >= DEAL_TIERS["small"]:
        size_score = 20
        tier = "SMALL"
    else:
        size_score = 10
        tier = "MICRO"

    score += size_score * SCORING_WEIGHTS["deal_size"]

    # 2. Stage score (0-20 points)
    stage_multiplier = STAGE_MULTIPLIERS.get(deal['stage'], 0.5)
    stage_score = stage_multiplier * 20
    score += stage_score * SCORING_WEIGHTS["stage"]

    # 3. Stagnation urgency (0-15 points)
    if days_stagnant > 60:
        stagnation_score = 15  # Critical
    elif days_stagnant > 21:
        stagnation_score = 12  # High urgency
    elif days_stagnant > 14:
        stagnation_score = 9   # Medium urgency
    elif days_stagnant > 7:
        stagnation_score = 6   # Low urgency
    else:
        stagnation_score = 3   # Recent activity

    score += stagnation_score * SCORING_WEIGHTS["stagnation"]

    # 4. Complexity multiplier (0-10 points)
    # Larger deals are more complex
    if deal_value >= DEAL_TIERS["enterprise"]:
        complexity_score = 10
    elif deal_value >= DEAL_TIERS["mid_market"]:
        complexity_score = 7
    else:
        complexity_score = 5

    score += complexity_score * SCORING_WEIGHTS["complexity"]

    # 5. Strategic account bonus (0-5 points)
    # Wellness brands, large ecommerce
    strategic_keywords = ["wellness", "vitamin", "supplement", "health", "beauty"]
    is_strategic = any(kw in deal['customer'].lower() for kw in strategic_keywords)

    if is_strategic:
        strategic_score = 5
    else:
        strategic_score = 0

    score += strategic_score * SCORING_WEIGHTS["strategic"]

    return round(score, 1), tier


def calculate_recommended_time_allocation(scored_deals):
    """Calculate recommended time allocation per deal"""

    total_score = sum(d['priority_score'] for d in scored_deals)

    if total_score == 0:
        return scored_deals

    # Assume 40 hours/week available for deal work
    weekly_hours = 40

    for deal in scored_deals:
        percentage = (deal['priority_score'] / total_score) * 100
        weekly_hours_allocated = (deal['priority_score'] / total_score) * weekly_hours

        deal['allocation_pct'] = round(percentage, 1)
        deal['weekly_hours'] = round(weekly_hours_allocated, 1)
        deal['daily_hours'] = round(weekly_hours_allocated / 5, 1)

    return scored_deals


def generate_prioritization_report(scored_deals):
    """Generate comprehensive prioritization report"""

    report = f"""# RUTHLESS PRIORITIZATION REPORT
Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

---

## 🎯 PRIORITY RANKING

**Total Active Deals**: {len(scored_deals)}
**Total Pipeline Value**: ${sum(d['value'] for d in scored_deals):,.0f}

| Rank | Deal | Value | Stage | Priority | Tier | Daily Hours |
|------|------|-------|-------|----------|------|-------------|
"""

    for i, deal in enumerate(scored_deals, 1):
        report += f"| {i} | **{deal['customer']}** | ${deal['value']:,.0f} | {deal['stage']} | **{deal['priority_score']}** | {deal['tier']} | {deal['daily_hours']}h |\n"

    report += "\n---\n\n## 🔥 TOP 5 PRIORITIES (Enterprise Focus)\n\n"

    for i, deal in enumerate(scored_deals[:5], 1):
        report += f"### {i}. {deal['customer']} (Priority: {deal['priority_score']})\n\n"
        report += f"- **Value**: ${deal['value']:,.0f} ({deal['tier']})\n"
        report += f"- **Stage**: {deal['stage']}\n"
        report += f"- **Stagnation**: {deal['days_stagnant']} days\n"
        report += f"- **Recommended Time**: {deal['daily_hours']} hours/day ({deal['allocation_pct']}% of time)\n"

        if deal['priority_score'] >= 80:
            report += f"- **⚠️  ACTION**: This is an enterprise deal requiring enterprise attention. Block calendar time daily.\n"
        elif deal['priority_score'] >= 60:
            report += f"- **🎯 ACTION**: High-value opportunity. Prioritize above smaller deals.\n"
        else:
            report += f"- **📋 ACTION**: Maintain steady progress, delegate where possible.\n"

        report += "\n"

    report += "---\n\n## 📊 TIME ALLOCATION SUMMARY\n\n"

    # Group by tier
    mega_deals = [d for d in scored_deals if d['tier'] == "MEGA"]
    enterprise_deals = [d for d in scored_deals if d['tier'] == "ENTERPRISE"]
    midmarket_deals = [d for d in scored_deals if d['tier'] == "MID-MARKET"]

    if mega_deals:
        mega_time = sum(d['allocation_pct'] for d in mega_deals)
        report += f"**Mega Deals ($10M+)**: {len(mega_deals)} deals, {mega_time:.1f}% of time\n"

    if enterprise_deals:
        enterprise_time = sum(d['allocation_pct'] for d in enterprise_deals)
        report += f"**Enterprise ($1M+)**: {len(enterprise_deals)} deals, {enterprise_time:.1f}% of time\n"

    if midmarket_deals:
        midmarket_time = sum(d['allocation_pct'] for d in midmarket_deals)
        report += f"**Mid-Market ($500K+)**: {len(midmarket_deals)} deals, {midmarket_time:.1f}% of time\n"

    report += "\n**Coaching Rule**: Enterprise deals should receive ≥20% of total time. Mega deals require daily touchpoints.\n"

    report += "\n---\n\n## 🚨 PRIORITIZATION RULES\n\n"
    report += "1. **Enterprise First**: Mega and Enterprise deals always come first\n"
    report += "2. **Block Time**: Calendar-block daily hours for top 3 priorities\n"
    report += "3. **Delegate Down**: Small deals (<$500K) should be delegated or automated\n"
    report += "4. **Daily Touch**: Top deal gets touched every single day\n"
    report += "5. **Stagnation Alert**: Deals >14 days stagnant need immediate action\n"

    report += "\n---\n\n## 📅 DAILY ACTION PLAN\n\n"

    if scored_deals:
        top_deal = scored_deals[0]
        report += f"### This Week's Focus: {top_deal['customer']}\n\n"
        report += f"**Priority Score**: {top_deal['priority_score']} ({top_deal['tier']})\n"
        report += f"**Daily Commitment**: {top_deal['daily_hours']} hours/day\n\n"
        report += "**Daily Actions**:\n"
        report += f"1. Review {top_deal['customer']} folder for progress\n"
        report += f"2. Identify next concrete action (follow-up, rate work, proposal)\n"
        report += f"3. Execute action before smaller deals\n"
        report += f"4. Log activity in HubSpot\n"
        report += f"5. Repeat tomorrow\n"

    report += "\n**Remember**: Revenue-generating activities ALWAYS come before systems improvements.\n"

    return report


def generate_daily_reminder(scored_deals):
    """Generate short daily reminder for morning review"""

    if not scored_deals:
        return "No active deals to prioritize."

    top_3 = scored_deals[:3]

    reminder = f"""# DAILY PRIORITY REMINDER
{datetime.now().strftime("%A, %B %d, %Y")}

## 🎯 YOUR TOP 3 TODAY

"""

    for i, deal in enumerate(top_3, 1):
        reminder += f"{i}. **{deal['customer']}** (${deal['value']:,.0f}) - {deal['daily_hours']}h today\n"

    reminder += f"\n**Focus Deal**: {top_3[0]['customer']} gets first {top_3[0]['daily_hours']} hours of your day.\n"
    reminder += "\n**Rule**: Don't touch smaller deals until top deal is moved forward.\n"

    return reminder


def main():
    """Main execution"""

    import argparse

    parser = argparse.ArgumentParser(
        description="Ruthless Prioritization Agent - Ensure enterprise deals get 10x attention"
    )
    parser.add_argument(
        "--daily-reminder",
        action="store_true",
        help="Generate short daily reminder (for 9AM sync)"
    )

    args = parser.parse_args()

    print("\n" + "="*80)
    print("RUTHLESS PRIORITIZATION AGENT")
    print("="*80 + "\n")

    # Get all deal folders
    deal_folders = get_deal_folders()

    # Filter to active deals (exclude LEAD, CLOSED-WON, CLOSED-LOST, WIN-BACK)
    # Focus only on deals in stages 1-6 (Discovery through Implementation)
    active_deals = [d for d in deal_folders if d['stage_num'] in [1, 2, 3, 4, 5, 6]]

    print(f"📊 Found {len(active_deals)} active deals in pipeline (stages 1-6 only)\n")

    # Score each deal
    scored_deals = []

    for deal in active_deals:
        deal_value = extract_deal_value(deal['folder'])
        days_stagnant = get_folder_last_modified_days(deal['folder'])

        priority_score, tier = calculate_priority_score(deal, deal_value, days_stagnant)

        scored_deals.append({
            'customer': deal['customer'],
            'value': deal_value,
            'stage': deal['stage'],
            'days_stagnant': days_stagnant,
            'priority_score': priority_score,
            'tier': tier
        })

    # Sort by priority score (highest first)
    scored_deals.sort(key=lambda x: x['priority_score'], reverse=True)

    # Calculate time allocation
    scored_deals = calculate_recommended_time_allocation(scored_deals)

    if args.daily_reminder:
        # Generate short daily reminder
        reminder = generate_daily_reminder(scored_deals)
        print(reminder)

        # Save to Downloads
        reminder_file = DOWNLOADS / "DAILY_PRIORITY_REMINDER.txt"
        reminder_file.write_text(reminder, encoding='utf-8')
        print(f"\n✅ Saved to: {reminder_file}")

    else:
        # Generate full report
        report = generate_prioritization_report(scored_deals)

        # Save report
        timestamp = datetime.now().strftime("%Y%m%d")
        report_file = DOWNLOADS / f"PRIORITIZATION_REPORT_{timestamp}.md"

        report_file.write_text(report, encoding='utf-8')

        print(f"✅ Report saved: {report_file}\n")

        # Print top 5
        print("="*80)
        print("TOP 5 PRIORITIES")
        print("="*80 + "\n")

        for i, deal in enumerate(scored_deals[:5], 1):
            print(f"{i}. {deal['customer']}")
            print(f"   Priority: {deal['priority_score']} | Value: ${deal['value']:,.0f} | Daily: {deal['daily_hours']}h")
            print()

    print("="*80 + "\n")


if __name__ == "__main__":
    main()
