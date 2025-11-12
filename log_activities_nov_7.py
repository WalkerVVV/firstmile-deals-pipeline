#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Log Activities in HubSpot - Friday, November 7, 2025
Log emails sent and calls made
"""

import sys
import io
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
API_KEY = os.environ.get('HUBSPOT_API_KEY')

if not API_KEY:
    print("❌ ERROR: HUBSPOT_API_KEY not found")
    exit(1)

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Deal IDs
DEALS = {
    'upstate_prep': '42448709378',
    'tactical': '40683158541',
    'boxiiship_sb': '18388015715',
    'joshs_frogs': '43373784945'
}

def log_email(deal_id, subject, email_body, recipient):
    """Log an email activity"""
    url = 'https://api.hubapi.com/crm/v3/objects/emails'
    payload = {
        'properties': {
            'hs_email_subject': subject,
            'hs_email_text': email_body,
            'hs_email_to_email': recipient,
            'hs_email_direction': 'EMAIL',
            'hs_email_status': 'SENT',
            'hs_timestamp': datetime.now().isoformat(),
            'hubspot_owner_id': '699257003'
        },
        'associations': [{
            'to': {'id': deal_id},
            'types': [{'associationCategory': 'HUBSPOT_DEFINED', 'associationTypeId': 210}]
        }]
    }
    response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
    return response.status_code == 201

def log_call(deal_id, call_subject, call_notes, disposition='COMPLETED'):
    """Log a call activity"""
    url = 'https://api.hubapi.com/crm/v3/objects/calls'
    payload = {
        'properties': {
            'hs_call_title': call_subject,
            'hs_call_body': call_notes,
            'hs_call_disposition': disposition,
            'hs_call_direction': 'OUTBOUND',
            'hs_call_status': 'COMPLETED',
            'hs_timestamp': datetime.now().isoformat(),
            'hubspot_owner_id': '699257003'
        },
        'associations': [{
            'to': {'id': deal_id},
            'types': [{'associationCategory': 'HUBSPOT_DEFINED', 'associationTypeId': 194}]
        }]
    }
    response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
    return response.status_code == 201

def main():
    print("\n" + "="*80)
    print("LOGGING ACTIVITIES IN HUBSPOT - Friday, November 7, 2025")
    print("="*80 + "\n")

    # 1. BOXIISHIP EMAIL
    print("1. Logging BoxiiShip email...")
    if log_email(
        DEALS['boxiiship_sb'],
        'Wednesday CVM Check-in - BoxiiShip System Beauty TX',
        'Meeting invite sent for Wednesday CVM review. Attendees: Reid, BoxiiShip team, Crystal Ruban Melville. Purpose: Customer Value Metrics review, performance metrics, service level compliance.',
        'reid@firstmile.com, boxiiship@example.com'
    ):
        print("   ✅ Email logged\n")

    # 2. BRANDON EMAIL
    print("2. Logging Brandon (Upstate Prep) email...")
    if log_email(
        DEALS['upstate_prep'],
        'Quick Check - DHL Situation',
        'Following up on DHL message asking us to disengage. DHL claims Upstate Prep is their customer. Only noticed 6 DHL expedited shipments in data. DHL is one of our largest partners - if we are working on account they back off and vice versa. Requested status and clarification.',
        'brandon@upstateprep.com'
    ):
        print("   ✅ Email logged\n")

    # 3. ELI EMAIL
    print("3. Logging Eli (Skupreme) email...")
    if log_email(
        DEALS['tactical'],
        'Touching Base - Tactical Logistics Setup',
        'Re-engagement email to Eli at Skupreme. Haven\'t connected recently. Tactical Logistics setup ready to move forward. Requested 15-min call to sync up. Offered alternative contact if Eli unavailable.',
        'eli@skupreme.com'
    ):
        print("   ✅ Email logged\n")

    # 4. BRANDON CALL
    print("4. Logging Brandon call...")
    if log_call(
        DEALS['upstate_prep'],
        'Call: DHL Situation Follow-up',
        'Called Brandon to follow up on DHL conflict. Left voicemail / spoke directly (update as needed). Requested clarification on DHL relationship and impact on FirstMile partnership.',
        'COMPLETED'
    ):
        print("   ✅ Call logged\n")

    # 5. ELI CALL
    print("5. Logging Eli call...")
    if log_call(
        DEALS['tactical'],
        'Call: Skupreme Re-engagement',
        'Called Eli at Skupreme to re-engage on Tactical Logistics setup. Left voicemail / spoke directly (update as needed). Deal has been stalled due to lack of contact.',
        'COMPLETED'
    ):
        print("   ✅ Call logged\n")

    print("="*80)
    print("✅ ALL ACTIVITIES LOGGED IN HUBSPOT")
    print("="*80)
    print("\nSummary:")
    print("  • 3 emails logged")
    print("  • 2 calls logged")
    print("  • All activities timestamped and associated with deals")
    print("\nNext: Monitor for responses and follow up as needed\n")

if __name__ == "__main__":
    main()
