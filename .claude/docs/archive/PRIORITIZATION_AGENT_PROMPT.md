# Production-Ready Prioritization Agent - Complete Prompt

**Use this prompt when creating or fixing the prioritization agent for FirstMile Deals pipeline.**

---

## 📋 Requirements

Create a prioritization agent that:

1. **Queries HubSpot API directly** (never parse folders) for all deal data
2. **Filters to active stages 1-6** (Discovery Scheduled through Implementation)
3. **Excludes cold leads** (stage 0), closed won (stage 7), and closed lost (stage 8)
4. **Calculates priority scores** based on deal size, stage, stagnation, complexity, and strategic fit
5. **Generates actionable reports** with time allocation recommendations
6. **Supports daily reminder mode** for morning sync integration

---

## 🎯 Core Architecture

### Data Source: HubSpot API (REQUIRED)

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('HUBSPOT_API_KEY')
OWNER_ID = "699257003"
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

# VERIFIED Stage IDs (from HubSpot API 2025-10-10)
ACTIVE_STAGES = [
    '1090865183',                               # [01-DISCOVERY-SCHEDULED]
    'd2a08d6f-cc04-4423-9215-594fe682e538',     # [02-DISCOVERY-COMPLETE]
    'e1c4321e-afb6-4b29-97d4-2b2425488535',     # [03-RATE-CREATION]
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a',     # [04-PROPOSAL-SENT]
    '4e549d01-674b-4b31-8a90-91ec03122715',     # [05-SETUP-DOCS-SENT]
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307'      # [06-IMPLEMENTATION]
]

def fetch_active_deals_from_hubspot():
    """Fetch active deals from HubSpot (stages 1-6 only)"""

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'filterGroups': [{
            'filters': [
                {'propertyName': 'hubspot_owner_id', 'operator': 'EQ', 'value': OWNER_ID},
                {'propertyName': 'pipeline', 'operator': 'EQ', 'value': PIPELINE_ID},
                {'propertyName': 'dealstage', 'operator': 'IN', 'values': ACTIVE_STAGES}
            ]
        }],
        'properties': [
            'dealname',
            'dealstage',
            'amount',
            'createdate',
            'hs_lastmodifieddate'
        ],
        'limit': 100
    }

    response = requests.post(
        'https://api.hubapi.com/crm/v3/objects/deals/search',
        headers=headers,
        json=payload,
        timeout=10
    )

    if response.status_code != 200:
        print(f'❌ HubSpot API Error: {response.status_code}')
        return []

    return response.json().get('results', [])
```

**Why HubSpot API?**
- ✅ Always current (no folder sync delays)
- ✅ Single source of truth (authoritative data)
- ✅ Accurate deal values from `amount` property
- ✅ Real stagnation tracking via `hs_lastmodifieddate`
- ✅ No regex parsing bugs or file search limitations

---

## 🎯 Priority Scoring Algorithm

### Weights (Total = 100 points)

```python
SCORING_WEIGHTS = {
    "deal_size": 0.50,      # 50% - Deal value drives priority
    "stage": 0.20,          # 20% - Later stages need more attention
    "stagnation": 0.15,     # 15% - Stale deals need immediate action
    "complexity": 0.10,     # 10% - Complex deals need more time
    "strategic": 0.05       # 5% - Strategic accounts bonus
}
```

### Deal Tiers

```python
DEAL_TIERS = {
    "mega": 10_000_000,      # $10M+ (top priority)
    "enterprise": 1_000_000,  # $1M+
    "mid_market": 500_000,    # $500K+
    "small": 100_000,         # $100K+
    "micro": 0                # <$100K
}
```

### Stage Multipliers

```python
STAGE_MULTIPLIERS = {
    "[01-DISCOVERY-SCHEDULED]": 0.3,
    "[02-DISCOVERY-COMPLETE]": 0.4,
    "[03-RATE-CREATION]": 0.6,      # Bottleneck - needs attention
    "[04-PROPOSAL-SENT]": 0.8,       # High urgency - follow-up needed
    "[05-SETUP-DOCS-SENT]": 0.9,     # Near close - critical
    "[06-IMPLEMENTATION]": 1.0,      # Highest priority - customer retention
}
```

### Stagnation Urgency

```python
def calculate_stagnation_score(days_stagnant):
    """Calculate urgency based on days since last activity"""
    if days_stagnant > 60:
        return 15  # CRITICAL - deal at risk
    elif days_stagnant > 21:
        return 12  # HIGH - needs immediate attention
    elif days_stagnant > 14:
        return 9   # MEDIUM - schedule follow-up
    elif days_stagnant > 7:
        return 6   # LOW - monitor
    else:
        return 3   # RECENT - maintain momentum
```

### Complete Scoring Function

```python
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
    stagnation_score = calculate_stagnation_score(days_stagnant)
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
    strategic_score = 5 if is_strategic else 0
    score += strategic_score * SCORING_WEIGHTS["strategic"]

    return round(score, 1), tier
```

---

## 📊 Time Allocation Calculation

```python
def calculate_recommended_time_allocation(scored_deals):
    """Calculate recommended weekly/daily hours per deal"""

    total_score = sum(d['priority_score'] for d in scored_deals)

    if total_score == 0:
        return scored_deals

    weekly_hours = 40  # Available hours for deal work

    for deal in scored_deals:
        percentage = (deal['priority_score'] / total_score) * 100
        weekly_hours_allocated = (deal['priority_score'] / total_score) * weekly_hours

        deal['allocation_pct'] = round(percentage, 1)
        deal['weekly_hours'] = round(weekly_hours_allocated, 1)
        deal['daily_hours'] = round(weekly_hours_allocated / 5, 1)

    return scored_deals
```

---

## 📝 Report Generation

### Full Prioritization Report

```python
def generate_prioritization_report(scored_deals):
    """Generate comprehensive markdown report"""

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
        report += f"| {i} | **{deal['customer']}** | ${deal['value']:,.0f} | "
        report += f"{deal['stage']} | **{deal['priority_score']}** | "
        report += f"{deal['tier']} | {deal['daily_hours']}h |\n"

    # Add TOP 5 PRIORITIES section
    report += "\n---\n\n## 🔥 TOP 5 PRIORITIES (Enterprise Focus)\n\n"

    for i, deal in enumerate(scored_deals[:5], 1):
        report += f"### {i}. {deal['customer']} (Priority: {deal['priority_score']})\n\n"
        report += f"- **Value**: ${deal['value']:,.0f} ({deal['tier']})\n"
        report += f"- **Stage**: {deal['stage']}\n"
        report += f"- **Stagnation**: {deal['days_stagnant']} days\n"
        report += f"- **Recommended Time**: {deal['daily_hours']} hours/day ({deal['allocation_pct']}% of time)\n\n"

        # Add action recommendations based on priority
        if deal['priority_score'] >= 80:
            report += f"- **⚠️ ACTION**: Enterprise deal requiring enterprise attention. Block calendar time daily.\n\n"
        elif deal['priority_score'] >= 60:
            report += f"- **🎯 ACTION**: High-value opportunity. Prioritize above smaller deals.\n\n"
        else:
            report += f"- **📋 ACTION**: Maintain steady progress, delegate where possible.\n\n"

    # Add TIME ALLOCATION SUMMARY
    mega_deals = [d for d in scored_deals if d['tier'] == "MEGA"]
    enterprise_deals = [d for d in scored_deals if d['tier'] == "ENTERPRISE"]
    midmarket_deals = [d for d in scored_deals if d['tier'] == "MID-MARKET"]

    report += "---\n\n## 📊 TIME ALLOCATION SUMMARY\n\n"

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

    return report
```

### Daily Reminder (for 9AM Sync)

```python
def generate_daily_reminder(scored_deals):
    """Generate short daily reminder with top 3 priorities"""

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
```

---

## 🔧 Main Execution Logic

```python
import argparse
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"

def main():
    """Main execution with CLI argument parsing"""

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

    print(f"📊 Found {len(hubspot_deals)} active deals (stages 1-6, CLOSED-LOST excluded)\n")

    # Score each deal
    scored_deals = []

    for deal in hubspot_deals:
        deal_name = deal['properties'].get('dealname', 'Unnamed')
        stage_id = deal['properties'].get('dealstage')
        stage_name = STAGE_MAP.get(stage_id, 'UNKNOWN')

        # Parse amount (handle null/empty values)
        amount_str = deal['properties'].get('amount', '0')
        try:
            deal_value = int(float(amount_str)) if amount_str else 0
        except:
            deal_value = 0

        # Calculate days since last modified
        last_modified = deal['properties'].get('hs_lastmodifieddate')
        days_stagnant = days_since(last_modified)

        priority_score, tier = calculate_priority_score(
            deal_name, deal_value, stage_name, days_stagnant
        )

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
            print(f"   Priority: {deal['priority_score']} | Value: ${deal['value']:,.0f} | Stage: {deal['stage']} | Daily: {deal['daily_hours']}h")
            print()

    print("="*80 + "\n")


if __name__ == "__main__":
    main()
```

---

## ✅ Critical Implementation Rules

### DO ✅

1. **Query HubSpot API directly** - Never parse folder structure
2. **Use ACTIVE_STAGES list** - Filter to stages 1-6 only
3. **Map stage IDs to names** - Use STAGE_MAP dictionary
4. **Parse amount safely** - Handle null/empty with try/except
5. **Calculate stagnation from hs_lastmodifieddate** - Not git logs
6. **Sort by priority_score DESC** - Highest priority first
7. **Generate both reports** - Full report AND daily reminder
8. **Save to Downloads folder** - Consistent location
9. **Handle errors gracefully** - API timeouts, null values
10. **Use environment variables** - HUBSPOT_API_KEY from .env

### DON'T ❌

1. **Don't parse folder names** - Folders can be out of sync
2. **Don't search markdown files** - HubSpot has authoritative data
3. **Don't include stage 0** - No [00-LEAD] in HubSpot
4. **Don't include stage 7** - [07-STARTED-SHIPPING] is closed won
5. **Don't include stage 8** - [08-CLOSED-LOST] is inactive
6. **Don't use git logs** - Not accurate for deal activity
7. **Don't hardcode deal values** - Always from HubSpot amount
8. **Don't skip null handling** - Many fields can be empty
9. **Don't use relative paths** - Always absolute paths
10. **Don't commit API keys** - Use .env file

---

## 📋 Expected Output

### Console Output
```
================================================================================
RUTHLESS PRIORITIZATION AGENT v2.0 (HUBSPOT API)
================================================================================

🔄 Fetching active deals from HubSpot API...
📊 Found 30 active deals (stages 1-6, CLOSED-LOST excluded)

✅ Report saved: C:\Users\BrettWalker\Downloads\PRIORITIZATION_REPORT_20251103.md

================================================================================
TOP 5 PRIORITIES
================================================================================

1. Caputron
   Priority: 29.6 | Value: $36,500,000 | Stage: [04-PROPOSAL-SENT] | Daily: 0.6h

2. ODW Logistics
   Priority: 29.6 | Value: $22,000,000 | Stage: [04-PROPOSAL-SENT] | Daily: 0.6h

3. Stackd Logistics
   Priority: 29.6 | Value: $20,203,200 | Stage: [04-PROPOSAL-SENT] | Daily: 0.6h

4. Josh's Frogs
   Priority: 27.6 | Value: $32,400,000 | Stage: [01-DISCOVERY-SCHEDULED] | Daily: 0.5h

5. Upstate Prep
   Priority: 25.4 | Value: $1,042,800 | Stage: [06-IMPLEMENTATION] | Daily: 0.5h

================================================================================
```

---

## 🧪 Testing Checklist

- [ ] API key loads from environment
- [ ] HubSpot API returns 200 status
- [ ] Deal count matches HubSpot UI
- [ ] Only stages 1-6 are included
- [ ] Deal values match HubSpot amounts
- [ ] Stagnation calculated correctly
- [ ] Priority scores are logical
- [ ] Top 5 matches business expectations
- [ ] Report saves to Downloads/
- [ ] Daily reminder mode works
- [ ] Null values handled gracefully
- [ ] Stage mapping is accurate

---

## 📚 Reference

- **HubSpot Stage IDs**: See `.claude/NEBUCHADNEZZAR_REFERENCE.md`
- **Complete Learnings**: See `.claude/PRIORITIZATION_AGENT_LEARNINGS.md`
- **Workflow Integration**: Used in `daily_9am_sync.py` and `noon_sync.py`

---

**Version**: 2.0 (HubSpot API)
**Status**: Production-Ready ✅
**Last Updated**: November 3, 2025
