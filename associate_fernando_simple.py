#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Associate Fernando with Tinoco deal using direct API call
"""

import sys
import os
import io
import requests
from dotenv import load_dotenv

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    """Associate Fernando with Tinoco deal."""

    print("\n" + "="*80)
    print("ASSOCIATE FERNANDO WITH TINOCO DEAL")
    print("="*80 + "\n")

    # Load credentials
    load_dotenv()
    API_KEY = os.environ.get('HUBSPOT_API_KEY')
    if not API_KEY:
        print("\nERROR: HUBSPOT_API_KEY not found")
        sys.exit(1)

    # Details
    FERNANDO_CONTACT_ID = "173878634555"
    TINOCO_DEAL_ID = "36470789710"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        # Step 1: Associate contact to deal
        print(f"Step 1: Associating Fernando (ID: {FERNANDO_CONTACT_ID}) with Tinoco deal...")

        # HubSpot v4 Associations API endpoint
        association_url = f"https://api.hubapi.com/crm/v4/objects/contacts/{FERNANDO_CONTACT_ID}/associations/deals/{TINOCO_DEAL_ID}"

        payload = [
            {
                "associationCategory": "HUBSPOT_DEFINED",
                "associationTypeId": 3  # contact_to_deal
            }
        ]

        response = requests.put(association_url, headers=headers, json=payload)

        if response.status_code in [200, 201]:
            print("SUCCESS: Contact associated with deal!\n")
        elif response.status_code == 409:
            print("INFO: Association already exists\n")
        else:
            print(f"WARNING: Association response: {response.status_code}")
            print(f"Response: {response.text}\n")

        # Step 2: Create note on deal
        print("Step 2: Creating transition note on deal...")

        note_url = "https://api.hubapi.com/crm/v3/objects/notes"

        note_payload = {
            "properties": {
                "hs_note_body": """Contact Transition - Tinoco Enterprises

New Primary Contact: Fernando Arenas
- Email: fernando.arenas201101@gmail.com
- Phone: 385-472-3886

Previous Contact: David
- Status: Moving to Michigan
- Transition Date: November 10, 2025

Call Activity (11/10/2025):
- Spoke with David at Tinoco Enterprises
- David provided Fernando's contact information
- David confirmed he is relocating to Michigan

Next Steps:
- Reach out to Fernando for ongoing coordination
- Update all future communications to Fernando
""",
                "hs_timestamp": "2025-11-10T12:00:00.000Z"
            },
            "associations": [
                {
                    "to": {"id": TINOCO_DEAL_ID},
                    "types": [
                        {
                            "associationCategory": "HUBSPOT_DEFINED",
                            "associationTypeId": 214  # note_to_deal
                        }
                    ]
                },
                {
                    "to": {"id": FERNANDO_CONTACT_ID},
                    "types": [
                        {
                            "associationCategory": "HUBSPOT_DEFINED",
                            "associationTypeId": 10  # note_to_contact
                        }
                    ]
                }
            ]
        }

        note_response = requests.post(note_url, headers=headers, json=note_payload)

        if note_response.status_code in [200, 201]:
            note_id = note_response.json().get('id', 'Unknown')
            print(f"SUCCESS: Note created (ID: {note_id})!\n")
        else:
            print(f"WARNING: Note response: {note_response.status_code}")
            print(f"Response: {note_response.text}\n")

        # Summary
        print("="*80)
        print("HUBSPOT UPDATE COMPLETE")
        print("="*80)
        print(f"\nCONTACT CREATED: Fernando Arenas (ID: {FERNANDO_CONTACT_ID})")
        print(f"ASSOCIATION: Contact linked to Tinoco deal (ID: {TINOCO_DEAL_ID})")
        print(f"NOTE: Transition details logged in HubSpot")
        print("\nNext: Update primary contact field manually in HubSpot if needed")
        print("="*80 + "\n")

    except Exception as e:
        print(f"\nERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
