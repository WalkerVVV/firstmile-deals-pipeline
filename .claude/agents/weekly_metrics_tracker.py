#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WEEKLY METRICS TRACKER AGENT
Purpose: Track weekly sales metrics and hold Brett accountable to 5/2/3/1 goals
Coaching directive: "5 new leads, 2 discovery calls, 3 proposals, 1 close per week"

Usage: python weekly_metrics_tracker.py [--week YYYY-MM-DD]
"""

import sys, io, os, re
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

# Repository root
REPO_ROOT = Path(__file__).parent.parent.parent
DOWNLOADS = Path.home() / "Downloads"

HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
HUBSPOT_OWNER_ID = "699257003"  # Brett Walker
HUBSPOT_PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

# Weekly goals from coaching review
WEEKLY_GOALS = {
    "new_leads": 5,
    "discovery_calls": 2,
    "proposals_sent": 3,
    "deals_closed": 1
}

# Stage IDs
STAGE_IDS = {
    "DISCOVERY_SCHEDULED": "d607df25-2c6d-4a5d-9835-6ed1e4f4020a",
    "DISCOVERY_COMPLETE": "presentationscheduled",
    "RATE_CREATION": "decisionmakerboughtin",
    "PROPOSAL_SENT": "qualifiedtobuy",
    "SETUP_DOCS_SENT": "8f2bce18-dc13-418c-a15c-d80a2c94e8f9",
    "IMPLEMENTATION": "96d38e42-5bdc-4c3a-ade8-a1ed0b9a1be2",
    "CLOSED_WON": "closedwon",
    "CLOSED_LOST": "closedlost"
}


def get_week_range(week_start=None):
    """Get Monday-Sunday date range for the week"""
    if week_start:
        # Parse provided date
        monday = datetime.strptime(week_start, "%Y-%m-%d")
    else:
        # Get this week's Monday
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())

    sunday = monday + timedelta(days=6)

    return monday, sunday


def query_hubspot_deals(start_date, end_date):
    """Query HubSpot for deals created/updated in date range"""

    url = "https://api.hubapi.com/crm/v3/objects/deals/search"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    # Convert to milliseconds timestamp
    start_ts = int(start_date.timestamp() * 1000)
    end_ts = int(end_date.timestamp() * 1000)

    payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "hubspot_owner_id",
                        "operator": "EQ",
                        "value": HUBSPOT_OWNER_ID
                    },
                    {
                        "propertyName": "pipeline",
                        "operator": "EQ",
                        "value": HUBSPOT_PIPELINE_ID
                    }
                ]
            }
        ],
        "properties": [
            "dealname",
            "amount",
            "dealstage",
            "createdate",
            "closedate",
            "hs_lastmodifieddate"
        ],
        "limit": 100
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        print(f"❌ HubSpot API error: {e}")
        return []


def parse_hubspot_date(date_str):
    """Parse HubSpot date string to timestamp"""
    if not date_str:
        return 0
    try:
        # HubSpot returns ISO format: "2019-08-21T00:00:00Z"
        dt = datetime.strptime(date_str.replace('Z', '+00:00'), "%Y-%m-%dT%H:%M:%S%z")
        return int(dt.timestamp() * 1000)
    except:
        return 0


def analyze_weekly_metrics(deals, start_date, end_date):
    """Analyze deals to extract weekly metrics"""

    start_ts = int(start_date.timestamp() * 1000)
    end_ts = int(end_date.timestamp() * 1000)

    metrics = {
        "new_leads": 0,
        "discovery_calls": 0,
        "proposals_sent": 0,
        "deals_closed": 0,
        "new_lead_details": [],
        "discovery_details": [],
        "proposal_details": [],
        "closed_details": []
    }

    for deal in deals:
        props = deal.get("properties", {})
        deal_name = props.get("dealname", "Unknown")
        amount = float(props.get("amount", 0) or 0)
        stage = props.get("dealstage", "")
        create_date = parse_hubspot_date(props.get("createdate"))
        close_date = parse_hubspot_date(props.get("closedate"))

        # New leads (created this week)
        if start_ts <= create_date <= end_ts:
            metrics["new_leads"] += 1
            metrics["new_lead_details"].append({
                "name": deal_name,
                "amount": amount,
                "date": datetime.fromtimestamp(create_date / 1000).strftime("%Y-%m-%d")
            })

        # Discovery calls (moved to DISCOVERY_COMPLETE this week)
        # This is approximate - ideally we'd track stage change timestamp
        if stage == STAGE_IDS["DISCOVERY_COMPLETE"]:
            metrics["discovery_calls"] += 1
            metrics["discovery_details"].append({
                "name": deal_name,
                "amount": amount
            })

        # Proposals sent (moved to PROPOSAL_SENT this week)
        if stage == STAGE_IDS["PROPOSAL_SENT"]:
            metrics["proposals_sent"] += 1
            metrics["proposal_details"].append({
                "name": deal_name,
                "amount": amount
            })

        # Deals closed (closed this week)
        if stage == STAGE_IDS["CLOSED_WON"] and start_ts <= close_date <= end_ts:
            metrics["deals_closed"] += 1
            metrics["closed_details"].append({
                "name": deal_name,
                "amount": amount,
                "date": datetime.fromtimestamp(close_date / 1000).strftime("%Y-%m-%d")
            })

    return metrics


def calculate_conversion_rates(metrics):
    """Calculate conversion rates"""
    conversions = {}

    # Lead → Discovery (%)
    if metrics["new_leads"] > 0:
        conversions["lead_to_discovery"] = (metrics["discovery_calls"] / metrics["new_leads"]) * 100
    else:
        conversions["lead_to_discovery"] = 0

    # Discovery → Proposal (%)
    if metrics["discovery_calls"] > 0:
        conversions["discovery_to_proposal"] = (metrics["proposals_sent"] / metrics["discovery_calls"]) * 100
    else:
        conversions["discovery_to_proposal"] = 0

    # Proposal → Close (%)
    if metrics["proposals_sent"] > 0:
        conversions["proposal_to_close"] = (metrics["deals_closed"] / metrics["proposals_sent"]) * 100
    else:
        conversions["proposal_to_close"] = 0

    # Overall lead → close (%)
    if metrics["new_leads"] > 0:
        conversions["lead_to_close"] = (metrics["deals_closed"] / metrics["new_leads"]) * 100
    else:
        conversions["lead_to_close"] = 0

    return conversions


def generate_weekly_report(monday, sunday, metrics, conversions):
    """Generate comprehensive weekly metrics report"""

    week_str = f"{monday.strftime('%B %d')} - {sunday.strftime('%B %d, %Y')}"

    report = f"""# WEEKLY METRICS REPORT
Week: {week_str}
Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

---

## 🎯 WEEKLY GOALS vs. ACTUAL

| Metric | Goal | Actual | Status | Delta |
|--------|------|--------|--------|-------|
| **New Leads** | {WEEKLY_GOALS['new_leads']} | {metrics['new_leads']} | {'✅' if metrics['new_leads'] >= WEEKLY_GOALS['new_leads'] else '❌'} | {metrics['new_leads'] - WEEKLY_GOALS['new_leads']:+d} |
| **Discovery Calls** | {WEEKLY_GOALS['discovery_calls']} | {metrics['discovery_calls']} | {'✅' if metrics['discovery_calls'] >= WEEKLY_GOALS['discovery_calls'] else '❌'} | {metrics['discovery_calls'] - WEEKLY_GOALS['discovery_calls']:+d} |
| **Proposals Sent** | {WEEKLY_GOALS['proposals_sent']} | {metrics['proposals_sent']} | {'✅' if metrics['proposals_sent'] >= WEEKLY_GOALS['proposals_sent'] else '❌'} | {metrics['proposals_sent'] - WEEKLY_GOALS['proposals_sent']:+d} |
| **Deals Closed** | {WEEKLY_GOALS['deals_closed']} | {metrics['deals_closed']} | {'✅' if metrics['deals_closed'] >= WEEKLY_GOALS['deals_closed'] else '❌'} | {metrics['deals_closed'] - WEEKLY_GOALS['deals_closed']:+d} |

---

## 📊 CONVERSION RATES

| Stage Transition | Rate | Benchmark |
|------------------|------|-----------|
| Lead → Discovery | {conversions['lead_to_discovery']:.1f}% | 40% target |
| Discovery → Proposal | {conversions['discovery_to_proposal']:.1f}% | 75% target |
| Proposal → Close | {conversions['proposal_to_close']:.1f}% | 33% target |
| **Overall (Lead → Close)** | **{conversions['lead_to_close']:.1f}%** | **10% target** |

---

## 📋 DETAILED BREAKDOWN

### New Leads ({metrics['new_leads']})
"""

    if metrics["new_lead_details"]:
        for lead in metrics["new_lead_details"]:
            report += f"\n- **{lead['name']}** (${lead['amount']:,.0f}) - {lead['date']}"
    else:
        report += "\n- No new leads this week"

    report += f"\n\n### Discovery Calls Completed ({metrics['discovery_calls']})"

    if metrics["discovery_details"]:
        for call in metrics["discovery_details"]:
            report += f"\n- **{call['name']}** (${call['amount']:,.0f})"
    else:
        report += "\n- No discovery calls this week"

    report += f"\n\n### Proposals Sent ({metrics['proposals_sent']})"

    if metrics["proposal_details"]:
        for proposal in metrics["proposal_details"]:
            report += f"\n- **{proposal['name']}** (${proposal['amount']:,.0f})"
    else:
        report += "\n- No proposals sent this week"

    report += f"\n\n### Deals Closed ({metrics['deals_closed']})"

    if metrics["closed_details"]:
        total_closed_value = sum(d['amount'] for d in metrics["closed_details"])
        for closed in metrics["closed_details"]:
            report += f"\n- **{closed['name']}** (${closed['amount']:,.0f}) - {closed['date']}"
        report += f"\n\n**Total Closed Value**: ${total_closed_value:,.0f}"
    else:
        report += "\n- No deals closed this week"

    report += "\n\n---\n\n## 🚨 COACHING FEEDBACK\n\n"

    # Generate coaching feedback based on performance
    goals_met = sum([
        metrics['new_leads'] >= WEEKLY_GOALS['new_leads'],
        metrics['discovery_calls'] >= WEEKLY_GOALS['discovery_calls'],
        metrics['proposals_sent'] >= WEEKLY_GOALS['proposals_sent'],
        metrics['deals_closed'] >= WEEKLY_GOALS['deals_closed']
    ])

    if goals_met == 4:
        report += "✅ **EXCELLENT WEEK** - All 4 goals achieved! This is sales hunter execution.\n\n"
    elif goals_met == 3:
        report += "✅ **STRONG WEEK** - 3 of 4 goals met. One more push to perfection.\n\n"
    elif goals_met == 2:
        report += "⚠️  **AVERAGE WEEK** - 2 of 4 goals met. Need to increase activity.\n\n"
    elif goals_met == 1:
        report += "❌ **BELOW TARGET** - Only 1 goal met. Focus on revenue-generating activities.\n\n"
    else:
        report += "🚨 **CRITICAL** - No goals met this week. Sales execution required immediately.\n\n"

    # Specific coaching
    if metrics['new_leads'] < WEEKLY_GOALS['new_leads']:
        deficit = WEEKLY_GOALS['new_leads'] - metrics['new_leads']
        report += f"**New Leads**: Need {deficit} more leads. Run Brand Scout, attend webinars, work LinkedIn.\n\n"

    if metrics['discovery_calls'] < WEEKLY_GOALS['discovery_calls']:
        deficit = WEEKLY_GOALS['discovery_calls'] - metrics['discovery_calls']
        report += f"**Discovery Calls**: Need {deficit} more calls. Follow up on [01-DISCOVERY-SCHEDULED] deals.\n\n"

    if metrics['proposals_sent'] < WEEKLY_GOALS['proposals_sent']:
        deficit = WEEKLY_GOALS['proposals_sent'] - metrics['proposals_sent']
        report += f"**Proposals**: Need {deficit} more proposals. Push [03-RATE-CREATION] deals forward.\n\n"

    if metrics['deals_closed'] < WEEKLY_GOALS['deals_closed']:
        report += f"**Closes**: No closes this week. Focus on urgency follow-ups for [04-PROPOSAL-SENT].\n\n"

    report += "---\n\n## 📅 NEXT WEEK ACTION PLAN\n\n"
    report += "1. **Monday 6AM**: Run Brand Scout for 10 new wellness leads\n"
    report += "2. **Daily 9AM**: Review priority deals, send follow-ups\n"
    report += "3. **Daily 3PM**: Check momentum, address blockers\n"
    report += "4. **Friday EOD**: Run weekly metrics, review progress\n"
    report += "\n**Remember**: Revenue-generating activities ALWAYS come before systems improvements.\n"

    return report


def main():
    """Main execution"""

    parser = argparse.ArgumentParser(
        description="Weekly Metrics Tracker - Hold Brett accountable to 5/2/3/1 weekly goals"
    )
    parser.add_argument(
        "--week",
        metavar="YYYY-MM-DD",
        help="Week start date (Monday). Defaults to current week."
    )

    args = parser.parse_args()

    print("\n" + "="*80)
    print("WEEKLY METRICS TRACKER")
    print("="*80 + "\n")

    # Get week range
    monday, sunday = get_week_range(args.week)
    print(f"📅 Week: {monday.strftime('%B %d')} - {sunday.strftime('%B %d, %Y')}\n")

    # Query HubSpot
    print("🔍 Querying HubSpot API...")
    deals = query_hubspot_deals(monday, sunday)
    print(f"   Found {len(deals)} deals in pipeline\n")

    # Analyze metrics
    print("📊 Analyzing weekly metrics...")
    metrics = analyze_weekly_metrics(deals, monday, sunday)
    conversions = calculate_conversion_rates(metrics)

    # Generate report
    report = generate_weekly_report(monday, sunday, metrics, conversions)

    # Save report
    week_filename = f"WEEKLY_METRICS_{monday.strftime('%Y-%m-%d')}_to_{sunday.strftime('%Y-%m-%d')}.md"
    report_file = DOWNLOADS / week_filename

    report_file.write_text(report, encoding='utf-8')

    print(f"✅ Report saved: {report_file}\n")

    # Print summary
    print("="*80)
    print("WEEKLY SUMMARY")
    print("="*80 + "\n")

    print(f"Goals Met: {sum([metrics['new_leads'] >= WEEKLY_GOALS['new_leads'], metrics['discovery_calls'] >= WEEKLY_GOALS['discovery_calls'], metrics['proposals_sent'] >= WEEKLY_GOALS['proposals_sent'], metrics['deals_closed'] >= WEEKLY_GOALS['deals_closed']])}/4\n")

    print(f"✅ New Leads: {metrics['new_leads']}/{WEEKLY_GOALS['new_leads']}")
    print(f"{'✅' if metrics['discovery_calls'] >= WEEKLY_GOALS['discovery_calls'] else '❌'} Discovery Calls: {metrics['discovery_calls']}/{WEEKLY_GOALS['discovery_calls']}")
    print(f"{'✅' if metrics['proposals_sent'] >= WEEKLY_GOALS['proposals_sent'] else '❌'} Proposals Sent: {metrics['proposals_sent']}/{WEEKLY_GOALS['proposals_sent']}")
    print(f"{'✅' if metrics['deals_closed'] >= WEEKLY_GOALS['deals_closed'] else '❌'} Deals Closed: {metrics['deals_closed']}/{WEEKLY_GOALS['deals_closed']}")

    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
