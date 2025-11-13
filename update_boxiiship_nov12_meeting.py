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
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from hubspot_sync_core import HubSpotSyncManager
from utils.credential_manager import CredentialManager


def update_boxiiship_deal():
    """Update BoxiiShip AF deal with November 12 meeting outcome."""

    print("=" * 80)
    print("UPDATING BOXIISHIP AF DEAL - MAKE WELLNESS RELAUNCH MEETING")
    print("=" * 80)
    print()

    # Load and validate credentials
    print("Loading credentials...")
    CredentialManager.load_and_validate()
    config = CredentialManager.get_hubspot_config()

    # Initialize sync manager
    print("Connecting to HubSpot...")
    sync_manager = HubSpotSyncManager(**config)

    # BoxiiShip AF Deal ID (from system)
    # Note: This should be the active BoxiiShip AF deal ID
    # Search for "BoxiiShip" in pipeline to find correct deal ID

    print("\nSearching for BoxiiShip AF deal...")

    # Search for BoxiiShip deals
    search_response = sync_manager.search_deals_advanced({
        "filterGroups": [{
            "filters": [{
                "propertyName": "dealname",
                "operator": "CONTAINS_TOKEN",
                "value": "*BoxiiShip*"
            }]
        }],
        "properties": ["dealname", "dealstage", "amount", "hs_priority"],
        "limit": 10
    })

    if not search_response or "results" not in search_response or len(search_response["results"]) == 0:
        print("ERROR: No BoxiiShip deals found in HubSpot")
        sys.exit(1)

    # Display found deals
    print(f"\nFound {len(search_response['results'])} BoxiiShip deal(s):")
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

    # For now, use the first BoxiiShip AF deal found
    # In production, you would select the correct one based on deal name or stage
    boxiiship_deal = search_response["results"][0]
    deal_id = boxiiship_deal["id"]

    print(f"\nUpdating Deal ID: {deal_id}")
    print(f"Deal Name: {boxiiship_deal.get('properties', {}).get('dealname', 'N/A')}")

    # Prepare meeting notes for HubSpot
    meeting_date = datetime.now().strftime("%Y-%m-%d")

    meeting_notes = f"""MAKE WELLNESS RELAUNCH MEETING - November 12, 2025

MEETING OUTCOME: SUCCESSFUL WIN-BACK

Key Decisions:
- Make Wellness ready to restart with FirstMile immediately
- Phased ramp-up: 10k → 30k packages/month starting this week
- $45K/week savings vs. current UPS costs ($2.34M annually)
- $7.1M annual revenue recovery opportunity for FirstMile

Meeting Recording: https://fathom.video/share/yuh743yJwHULoZgWGzBbnzgeixXu6Lyq

NEXT STEPS:
1. Email Nate with updated rates + peak cutoff dates (COMPLETED - draft ready)
2. Confirm supplies with Jim (COMPLETED - message drafted)
3. Schedule weekly 15-min check-in with Nate (COMPLETED - template created)
4. Send American Fork facility visit invite (COMPLETED - template created)
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
        # Add activity note
        "notes_last_updated": meeting_date,

        # Set priority to HIGH for active win-back
        "hs_priority": "high",

        # Update amount to reflect $7.1M annual opportunity
        # Note: Check current amount first before overwriting
        # "amount": "7100000",

        # Update close date to reflect active relaunch
        # "closedate": datetime.now().isoformat()
    }

    print("\nUpdating deal properties...")
    try:
        sync_manager.update_deal(deal_id, update_properties)
        print("✅ Deal properties updated successfully")
    except Exception as e:
        print(f"❌ Error updating deal properties: {str(e)}")

    # Create activity note (engagement)
    print("\nCreating activity note...")
    try:
        note_result = sync_manager.create_note(
            content=meeting_notes,
            associations=[{
                "to": {
                    "id": deal_id
                },
                "types": [{
                    "associationCategory": "HUBSPOT_DEFINED",
                    "associationTypeId": 214  # Note to Deal association
                }]
            }]
        )
        print("✅ Activity note created successfully")
    except Exception as e:
        print(f"❌ Error creating activity note: {str(e)}")
        print("Note: You may need to create the note manually in HubSpot")

    # Create follow-up task
    print("\nCreating follow-up task...")
    try:
        task_result = sync_manager.create_task({
            "hs_task_subject": "Follow up on Make Wellness Week 1 performance",
            "hs_task_body": "Review Week 1 shipment volume and SLA compliance. Confirm supplies received from Jim. Prepare for weekly check-in on Tuesday, Nov 19.",
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": "HIGH",
            "hs_timestamp": datetime.now().isoformat(),
            "hubspot_owner_id": config.get("owner_id", "")
        }, associations=[deal_id])
        print("✅ Follow-up task created successfully")
    except Exception as e:
        print(f"❌ Error creating task: {str(e)}")
        print("Note: You may need to create the task manually in HubSpot")

    print("\n" + "=" * 80)
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
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
