#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RUTHLESS PRIORITIZATION AGENT v2.0 - HUBSPOT API VERSION
Purpose: Ensure enterprise deals get 10x attention through scoring and time allocation
Coaching directive: "Enterprise deals require enterprise attention"

FIX: Now queries HubSpot API directly to avoid folder sync issues
Usage: python prioritization_agent_FIXED.py [--daily-reminder]
"""

import sys, io, os
from datetime import datetime
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

# Stage mapping (VERIFIED 2025-10-10 from HubSpot API)
STAGE_MAP = {
    '1090865183': '[01-DISCOVERY-SCHEDULED]',
    'd2a08d6f-cc04-4423-9215-594fe682e538': '[02-DISCOVERY-COMPLETE]',
    'e1c4321e-afb6-4b29-97d4-2b2425488535': '[03-RATE-CREATION]',
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a': '[04-PROPOSAL-SENT]',
    '4e549d01-674b-4b31-8a90-91ec03122715': '[05-SETUP-DOCS-SENT]',
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307': '[06-IMPLEMENTATION]',
    '3fd46d94-78b4-452b-8704-62a338a210fb': '[07-STARTED-SHIPPING]',
    '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8': '[08-CLOSED-LOST]'  # EXCLUDE THIS
}

# Active stages only (exclude CLOSED-LOST)
ACTIVE_STAGES = [
    '1090865183',  # [01-DISCOVERY-SCHEDULED]
    'd2a08d6f-cc04-4423-9215-594fe682e538',  # [02-DISCOVERY-COMPLETE]
    'e1c4321e-afb6-4b29-97d4-2b2425488535',  # [03-RATE-CREATION]
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a',  # [04-PROPOSAL-SENT]
    '4e549d01-674b-4b31-8a90-91ec03122715',  # [05-SETUP-DOCS-SENT]
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307'   # [06-IMPLEMENTATION]
]

# Priority scoring algorithm weights
SCORING_WEIGHTS = {
    "deal_size": 0.50,
    "stage": 0.20,
    "stagnation": 0.15,
    "complexity": 0.10,
    "strategic": 0.05
}

# Stage multipliers
STAGE_MULTIPLIERS = {
    "[01-DISCOVERY-SCHEDULED]": 0.3,
    "[02-DISCOVERY-COMPLETE]": 0.4,
    "[03-RATE-CREATION]": 0.6,
    "[04-PROPOSAL-SENT]": 0.8,
    "[05-SETUP-DOCS-SENT]": 0.9,
    "[06-IMPLEMENTATION]": 1.0,
    "[07-STARTED-SHIPPING]": 0.1
}

# Deal size thresholds
DEAL_TIERS = {
    "mega": 10_000_000,
    "enterprise": 1_000_000,
    "mid_market": 500_000,
    "small": 100_000,
    "micro": 0
}


def fetch_active_deals_from_hubspot():
    """Fetch active deals from HubSpot API (excluding CLOSED-LOST)"""

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'filterGroups': [{
            'filters': [
                {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': OWNER_ID},
                {'propertyName': 'pipeline', 'operator': 'EQ', 'value': PIPELINE_ID},
                {'propertyName': 'dealstage', 'operator': 'IN', 'values': ACTIVE_STAGES}  # ONLY ACTIVE
            ]
        }],
        'properties': ['dealname', 'dealstage', 'amount', 'createdate', 'hs_lastmodifieddate'],
        'limit': 100
    }

    try:
        response = requests.post(
            'https://api.hubapi.com/crm/v3/objects/deals/search',
            headers=headers,
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            print(f'❌ Error fetching deals: {response.status_code}')
            return []

        results = response.json()
        deals = results.get('results', [])

        return deals

    except Exception as e:
        print(f"⚠️  HubSpot API error: {e}")
        return []


def days_since(date_str):
    """Calculate days since date string"""
    if not date_str:
        return 999
    try:
        from dateutil import parser
        date = parser.parse(date_str)
        return (datetime.now(date.tzinfo) - date).days
    except:
        return 999


def calculate_priority_score(deal_name, deal_value, stage_name, days_stagnant):
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
    stage_multiplier = STAGE_MULTIPLIERS.get(stage_name, 0.5)
    stage_score = stage_multiplier * 20
    score += stage_score * SCORING_WEIGHTS["stage"]

    # 3. Stagnation urgency (0-15 points)
    if days_stagnant > 60:
        stagnation_score = 15
    elif days_stagnant > 21:
        stagnation_score = 12
    elif days_stagnant > 14:
        stagnation_score = 9
    elif days_stagnant > 7:
        stagnation_score = 6
    else:
        stagnation_score = 3

    score += stagnation_score * SCORING_WEIGHTS["stagnation"]

    # 4. Complexity multiplier (0-10 points)
    if deal_value >= DEAL_TIERS["enterprise"]:
        complexity_score = 10
    elif deal_value >= DEAL_TIERS["mid_market"]:
        complexity_score = 7
    else:
        complexity_score = 5

    score += complexity_score * SCORING_WEIGHTS["complexity"]

    # 5. Strategic account bonus (0-5 points)
    strategic_keywords = ["wellness", "vitamin", "supplement", "health", "beauty"]
    is_strategic = any(kw in deal_name.lower() for kw in strategic_keywords)

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

    weekly_hours = 40

    for deal in scored_deals:
        percentage = (deal['priority_score'] / total_score) * 100
        weekly_hours_allocated = (deal['priority_score'] / total_score) * weekly_hours

        deal['allocation_pct'] = round(percentage, 1)
        deal['weekly_hours'] = round(weekly_hours_allocated, 1)
        deal['daily_hours'] = round(weekly_hours_allocated / 5, 1)

    return scored_deals


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
        description="Ruthless Prioritization Agent v2.0 - HubSpot API Version"
    )
    parser.add_argument(
        "--daily-reminder",
        action="store_true",
        help="Generate short daily reminder (for 9AM sync)"
    )

    args = parser.parse_args()

    print("\n" + "="*80)
    print("RUTHLESS PRIORITIZATION AGENT v2.0 (HUBSPOT API)")
    print("="*80 + "\n")

    # Fetch active deals from HubSpot
    print("🔄 Fetching active deals from HubSpot API...")
    hubspot_deals = fetch_active_deals_from_hubspot()

    print(f"📊 Found {len(hubspot_deals)} active deals in pipeline (stages 1-6 only, CLOSED-LOST excluded)\n")

    # Score each deal
    scored_deals = []

    for deal in hubspot_deals:
        deal_name = deal['properties'].get('dealname', 'Unnamed')
        stage_id = deal['properties'].get('dealstage')
        stage_name = STAGE_MAP.get(stage_id, 'UNKNOWN')

        # Parse amount (handle null/empty)
        amount_str = deal['properties'].get('amount', '0')
        try:
            deal_value = int(float(amount_str)) if amount_str else 0
        except:
            deal_value = 0

        # Calculate days since last modified
        last_modified = deal['properties'].get('hs_lastmodifieddate')
        days_stagnant = days_since(last_modified)

        priority_score, tier = calculate_priority_score(deal_name, deal_value, stage_name, days_stagnant)

        scored_deals.append({
            'customer': deal_name,
            'value': deal_value,
            'stage': stage_name,
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
        # Print top 5
        print("="*80)
        print("TOP 5 PRIORITIES")
        print("="*80 + "\n")

        for i, deal in enumerate(scored_deals[:5], 1):
            print(f"{i}. {deal['customer']}")
            print(f"   Priority: {deal['priority_score']} | Value: ${deal['value']:,.0f} | Stage: {deal['stage']} | Daily: {deal['daily_hours']}h")
            print()

    print("="*80 + "\n")


if __name__ == "__main__":
    main()
