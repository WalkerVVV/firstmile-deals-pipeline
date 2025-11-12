"""
HubSpot Priority Deals Report
Fetches all deals from "My Pipeline (FM) BW Clone" and organizes by stage urgency
Using Gritty-Rain Private App credentials
"""

import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"
OWNER_ID = "699257003"  # Brett Walker
BASE_URL = "https://api.hubapi.com"

# Stage mapping with priority order (highest to lowest)
STAGE_PRIORITY = {
    '08d9c411-5e1b-487b-8732-9c2bcbbd0307': {'name': '[06-IMPLEMENTATION]', 'priority': 1},
    '4e549d01-674b-4b31-8a90-91ec03122715': {'name': '[05-SETUP-DOCS-SENT]', 'priority': 2},
    'd607df25-2c6d-4a5d-9835-6ed1e4f4020a': {'name': '[04-PROPOSAL-SENT]', 'priority': 3},
    'e1c4321e-afb6-4b29-97d4-2b2425488535': {'name': '[03-RATE-CREATION]', 'priority': 4},
    'd2a08d6f-cc04-4423-9215-594fe682e538': {'name': '[02-DISCOVERY-COMPLETE]', 'priority': 5},
    '1090865183': {'name': '[01-DISCOVERY-SCHEDULED]', 'priority': 6},
    '3fd46d94-78b4-452b-8704-62a338a210fb': {'name': '[07-STARTED-SHIPPING]', 'priority': 7},
    '02d8a1d7-d0b3-41d9-adc6-44ab768a61b8': {'name': '[08-CLOSED-LOST]', 'priority': 8}
}


def fetch_deals():
    """Fetch all deals from the specified pipeline owned by Brett Walker"""
    url = f"{BASE_URL}/crm/v3/objects/deals/search"
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "filterGroups": [{
            "filters": [
                {
                    "propertyName": "pipeline",
                    "operator": "EQ",
                    "value": PIPELINE_ID
                },
                {
                    "propertyName": "hubspot_owner_id",
                    "operator": "EQ",
                    "value": OWNER_ID
                }
            ]
        }],
        "properties": [
            "dealname",
            "dealstage",
            "amount",
            "hs_lastmodifieddate",
            "notes_last_updated",
            "closedate",
            "hs_next_step",
            "createdate",
            "hubspot_owner_id"
        ],
        "limit": 100
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching deals: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return []


def calculate_days_idle(last_modified_date):
    """Calculate days since last modification"""
    if not last_modified_date:
        return 0

    last_modified = datetime.fromisoformat(last_modified_date.replace('Z', '+00:00'))
    now = datetime.now(last_modified.tzinfo)
    days = (now - last_modified).days
    return days


def format_currency(amount):
    """Format amount as currency"""
    if not amount:
        return "$0"
    try:
        return f"${float(amount):,.0f}"
    except:
        return "$0"


def organize_deals(deals):
    """Organize deals by stage priority and calculate metrics"""
    organized = {}

    for deal in deals:
        props = deal.get('properties', {})
        stage_id = props.get('dealstage')

        if stage_id not in STAGE_PRIORITY:
            continue

        stage_info = STAGE_PRIORITY[stage_id]
        stage_name = stage_info['name']
        priority = stage_info['priority']

        if stage_name not in organized:
            organized[stage_name] = {
                'priority': priority,
                'deals': []
            }

        last_modified = props.get('hs_lastmodifieddate')
        days_idle = calculate_days_idle(last_modified)

        deal_data = {
            'id': deal.get('id'),
            'name': props.get('dealname', 'Unnamed Deal'),
            'amount': format_currency(props.get('amount')),
            'amount_numeric': float(props.get('amount', 0) or 0),
            'last_modified': last_modified,
            'days_idle': days_idle,
            'next_step': props.get('hs_next_step', 'No next step defined'),
            'created': props.get('createdate')
        }

        organized[stage_name]['deals'].append(deal_data)

    # Sort deals within each stage by days idle (descending) then amount (descending)
    for stage in organized.values():
        stage['deals'].sort(key=lambda x: (-x['days_idle'], -x['amount_numeric']))

    return organized


def print_report(organized_deals):
    """Print formatted report"""
    print("\n" + "="*80)
    print("HUBSPOT PRIORITY DEALS REPORT")
    print(f"Pipeline: My Pipeline (FM) BW Clone")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

    # Sort stages by priority
    sorted_stages = sorted(organized_deals.items(), key=lambda x: x[1]['priority'])

    total_deals = sum(len(stage['deals']) for _, stage in sorted_stages)
    total_value = sum(
        deal['amount_numeric']
        for _, stage in sorted_stages
        for deal in stage['deals']
    )

    print(f"SUMMARY")
    print(f"Total Deals: {total_deals}")
    print(f"Total Pipeline Value: ${total_value:,.0f}")
    print(f"\n{'='*80}\n")

    # Print each stage
    for stage_name, stage_data in sorted_stages:
        deals = stage_data['deals']
        if not deals:
            continue

        stage_value = sum(d['amount_numeric'] for d in deals)

        print(f"\n{'='*80}")
        print(f"{stage_name} ({len(deals)} deals | ${stage_value:,.0f})")
        print(f"{'='*80}\n")

        for deal in deals:
            idle_flag = "*** URGENT *** " if deal['days_idle'] > 7 else ""
            print(f"{idle_flag}Deal: {deal['name']}")
            print(f"  Amount: {deal['amount']}")
            print(f"  Days Idle: {deal['days_idle']} days")
            print(f"  Next Step: {deal['next_step']}")
            print(f"  Deal ID: {deal['id']}")
            print()

    # Highlight urgent deals
    print(f"\n{'='*80}")
    print("*** URGENT: DEALS IDLE >7 DAYS ***")
    print(f"{'='*80}\n")

    urgent_deals = []
    for stage_name, stage_data in sorted_stages:
        for deal in stage_data['deals']:
            if deal['days_idle'] > 7:
                urgent_deals.append((stage_name, deal))

    if urgent_deals:
        for stage_name, deal in urgent_deals:
            print(f"{stage_name}: {deal['name']} ({deal['days_idle']} days idle)")
    else:
        print("No deals idle >7 days")

    print("\n" + "="*80 + "\n")


def main():
    """Main execution"""
    print("Fetching deals from HubSpot...")

    if not HUBSPOT_API_KEY:
        print("ERROR: HUBSPOT_API_KEY not found in .env file")
        return

    deals = fetch_deals()

    if not deals:
        print("ERROR: No deals found or error occurred")
        return

    print(f"SUCCESS: Fetched {len(deals)} deals\n")

    organized = organize_deals(deals)
    print_report(organized)

    # Save to file
    output_file = f"priority_deals_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = f
        print_report(organized)
        sys.stdout = old_stdout

    print(f"\nReport saved to: {output_file}")


if __name__ == "__main__":
    main()
