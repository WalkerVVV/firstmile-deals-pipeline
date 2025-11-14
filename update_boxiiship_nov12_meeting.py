#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update BoxiiShip AF Deal in HubSpot - Make Wellness Relaunch Meeting (Nov 12, 2025)

Updates BoxiiShip American Fork deal with:
- Meeting outcome and notes
- Next steps and action items
- Updated deal stage (if needed)
- Activity timeline entry

Usage:
    python update_boxiiship_nov12_meeting.py
"""

import os
import sys
import io
import requests
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding for emoji support
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    sys.exit(1)

OWNER_ID = "699257003"  # Brett Walker
HUBSPOT_API_BASE = "https://api.hubapi.com"


def make_api_request(method, endpoint, data=None):
    """Make authenticated HubSpot API request."""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    url = f"{HUBSPOT_API_BASE}{endpoint}"

    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {str(e)}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
        return None


def search_deals(search_term):
    """Search for deals by name."""
    endpoint = "/crm/v3/objects/deals/search"
    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "dealname",
                "operator": "CONTAINS_TOKEN",
                "value": f"*{search_term}*"
            }]
        }],
        "properties": ["dealname", "dealstage", "amount", "hs_priority"],
        "limit": 10,
        "sorts": [{"propertyName": "hs_lastmodifieddate", "direction": "DESCENDING"}]
    }

    return make_api_request("POST", endpoint, payload)


def update_deal(deal_id, properties):
    """Update deal properties."""
    endpoint = f"/crm/v3/objects/deals/{deal_id}"
    payload = {"properties": properties}

    return make_api_request("PATCH", endpoint, payload)


def create_note(content, deal_id):
    """Create an engagement note associated with a deal."""
    endpoint = "/crm/v3/objects/notes"

    # Convert to Unix timestamp in milliseconds
    timestamp_ms = int(datetime.now().timestamp() * 1000)

    payload = {
        "properties": {
            "hs_note_body": content,
            "hs_timestamp": str(timestamp_ms)
        },
        "associations": [{
            "to": {"id": deal_id},
            "types": [{
                "associationCategory": "HUBSPOT_DEFINED",
                "associationTypeId": 214  # Note to Deal association
            }]
        }]
    }

    return make_api_request("POST", endpoint, payload)


def create_task(subject, body, deal_id):
    """Create a task associated with a deal."""
    endpoint = "/crm/v3/objects/tasks"

    # Calculate due date (7 days from now for Week 1 review)
    from datetime import timedelta
    due_date = datetime.now() + timedelta(days=7)

    # Convert to Unix timestamp in milliseconds
    timestamp_ms = int(due_date.timestamp() * 1000)

    payload = {
        "properties": {
            "hs_task_subject": subject,
            "hs_task_body": body,
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": "HIGH",
            "hs_timestamp": str(timestamp_ms),
            "hubspot_owner_id": OWNER_ID
        },
        "associations": [{
            "to": {"id": deal_id},
            "types": [{
                "associationCategory": "HUBSPOT_DEFINED",
                "associationTypeId": 216  # Task to Deal association
            }]
        }]
    }

    return make_api_request("POST", endpoint, payload)


def update_boxiiship_deal():
    """Update BoxiiShip AF deal with November 12 meeting outcome."""

    print("=" * 80)
    print("UPDATING BOXIISHIP AF DEAL - MAKE WELLNESS RELAUNCH MEETING")
    print("=" * 80)
    print()

    print("Connecting to HubSpot...")
    print(f"Using API Key: {API_KEY[:8]}...{API_KEY[-4:]}")
    print(f"Owner ID: {OWNER_ID}")
    print()

    # Search for BoxiiShip AF Make Wellness WIN-BACK deal
    print("Searching for BoxiiShip AF Make Wellness WIN-BACK deal...")
    search_response = search_deals("WIN-BACK")

    if not search_response or "results" not in search_response or len(search_response["results"]) == 0:
        print("❌ ERROR: No WIN-BACK deals found in HubSpot")
        sys.exit(1)

    # Display found deals
    print(f"\n✅ Found {len(search_response['results'])} BoxiiShip deal(s):")
    for idx, deal in enumerate(search_response["results"], 1):
        deal_id = deal["id"]
        deal_name = deal.get("properties", {}).get("dealname", "N/A")
        deal_stage = deal.get("properties", {}).get("dealstage", "N/A")
        amount = deal.get("properties", {}).get("amount", "N/A")
        priority = deal.get("properties", {}).get("hs_priority", "N/A")

        print(f"\n{idx}. Deal ID: {deal_id}")
        print(f"   Name: {deal_name}")
        print(f"   Stage: {deal_stage}")
        print(f"   Amount: ${amount}")
        print(f"   Priority: {priority}")

    # Use the first BoxiiShip AF deal found
    boxiiship_deal = search_response["results"][0]
    deal_id = boxiiship_deal["id"]

    print(f"\n→ Updating Deal ID: {deal_id}")
    print(f"   Deal Name: {boxiiship_deal.get('properties', {}).get('dealname', 'N/A')}")
    print()

    # Prepare meeting notes for HubSpot
    meeting_date = datetime.now().strftime("%Y-%m-%d")

    meeting_notes = """MAKE WELLNESS RELAUNCH MEETING - November 12, 2025

MEETING OUTCOME: SUCCESSFUL WIN-BACK

Key Decisions:
- Make Wellness ready to restart with FirstMile immediately
- Phased ramp-up: 10k → 30k packages/month starting this week
- $45K/week savings vs. current UPS costs ($2.34M annually)
- $7.1M annual revenue recovery opportunity for FirstMile

Meeting Recording: https://fathom.video/share/yuh743yJwHULoZgWGzBbnzgeixXu6Lyq

NEXT STEPS:
1. Email Nate with updated rates + peak cutoff dates (COMPLETED - sent 11/13)
2. Confirm supplies with Jim (COMPLETED - sent 11/13)
3. Schedule weekly 15-min check-in with Nate (COMPLETED - sent 11/13)
4. Send American Fork facility visit invite (COMPLETED - sent 11/13)
5. Enable enhanced tracking visibility (PENDING - ops team)
6. Update HubSpot deal (THIS ACTION)

OPERATIONAL REQUIREMENTS:
- Weekly check-ins: Every Tuesday, 15 minutes
- Enhanced tracking: Real-time visibility for all Make Wellness shipments
- SLA monitoring: Daily tracking with automated alerts
- In-person visit: American Fork facility (Nov 19-21)

PERFORMANCE COMMITMENT:
- SLA compliance target: ≥95%
- Daily SLA monitoring
- Weekly performance reviews
- Immediate escalation path for issues

FINANCIAL IMPACT:
- Annual revenue recovery: $7.1M
- Make Wellness annual savings: $2.34M-$2.6M vs. UPS
- Weekly savings: $45K-$50K
- Premium paid to UPS since July: $1.17M-$1.3M

RISK MITIGATION:
- April 2025 performance issues fully resolved (ACI-WS removed from routing)
- 5+ months of stable performance (May-Oct 2025)
- Enhanced tracking and monitoring
- Weekly communication and relationship building

Deal folder: [CUSTOMER]_BoxiiShip_AF/MEETING_NOTES_NOV12_2025_MAKE_WELLNESS_RELAUNCH.md
"""

    # Prepare deal update properties
    update_properties = {
        # Set priority to HIGH for active win-back
        "hs_priority": "high",

        # Update close date to reflect active relaunch (current date)
        "closedate": datetime.now().strftime("%Y-%m-%d")
    }

    # Step 1: Update deal properties
    print("Step 1: Updating deal properties...")
    result = update_deal(deal_id, update_properties)
    if result:
        print("✅ Deal properties updated successfully")
        print(f"   - Priority set to HIGH")
        print(f"   - Close date updated to {update_properties['closedate']}")
    else:
        print("❌ Error updating deal properties")
    print()

    # Step 2: Create activity note
    print("Step 2: Creating activity note...")
    note_result = create_note(meeting_notes, deal_id)
    if note_result:
        print("✅ Activity note created successfully")
        print(f"   - Note ID: {note_result.get('id', 'N/A')}")
    else:
        print("❌ Error creating activity note")
        print("   Note: You may need to create the note manually in HubSpot")
    print()

    # Step 3: Create follow-up task
    print("Step 3: Creating follow-up task...")
    task_subject = "Follow up on Make Wellness Week 1 performance"
    task_body = """Review Week 1 shipment volume and SLA compliance with Make Wellness relaunch.

Action items:
- Review shipment volume (target: 10k-30k packages)
- Confirm SLA compliance (target: ≥95%)
- Verify supplies received from Jim
- Prepare for weekly check-in on Tuesday, Nov 19
- Confirm American Fork facility visit scheduled

Priority: HIGH - $7.1M annual revenue recovery at stake"""

    task_result = create_task(task_subject, task_body, deal_id)
    if task_result:
        print("✅ Follow-up task created successfully")
        print(f"   - Task ID: {task_result.get('id', 'N/A')}")
        print(f"   - Subject: {task_subject}")
    else:
        print("❌ Error creating task")
        print("   Note: You may need to create the task manually in HubSpot")
    print()

    print("=" * 80)
    print("BOXIISHIP AF DEAL UPDATE COMPLETE")
    print("=" * 80)
    print()
    print("Summary:")
    print(f"✅ Deal ID {deal_id} updated with meeting outcome")
    print("✅ Priority set to HIGH")
    print("✅ Activity note created with meeting details")
    print("✅ Follow-up task created for Week 1 performance review")
    print()
    print("Next Steps:")
    print("1. Review updated deal in HubSpot")
    print("2. Verify activity timeline shows meeting notes")
    print("3. Confirm task created for follow-up")
    print("4. Monitor Make Wellness Week 1 performance")
    print()


if __name__ == "__main__":
    try:
        update_boxiiship_deal()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
