#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HubSpot Real-Time Update Helper
Used by Claude during daily workflow to keep HubSpot updated in real-time

Functions:
- add_deal_note(deal_name, note_text)
- create_task(deal_name, task_subject, task_body, priority, due_days)
- update_deal_stage(deal_name, new_stage)
- log_call(deal_name, call_notes, outcome)
- log_email(deal_name, subject, direction, notes)
- update_deal_property(deal_name, property_name, value)
"""

import sys
import io
import requests
import json
from datetime import datetime, timedelta
from hubspot_config import get_hubspot_config, get_api_headers, STAGE_MAPPING, FOLDER_TO_STAGE_ID

# Fix Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load configuration
config = get_hubspot_config()
API_KEY = config['API_KEY']
OWNER_ID = config['OWNER_ID']
PIPELINE_ID = config['PIPELINE_ID']
BASE_URL = config['BASE_URL']

headers = get_api_headers(API_KEY)

def search_deal(deal_name):
    """
    Search for a deal by name

    Args:
        deal_name (str): Deal name or company name

    Returns:
        dict: Deal object or None if not found
    """
    print(f"🔍 Searching for deal: {deal_name}")

    search_payload = {
        "filterGroups": [{
            "filters": [
                {"propertyName": "dealname", "operator": "CONTAINS_TOKEN", "value": deal_name},
                {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID}
            ]
        }],
        "properties": ["dealname", "dealstage", "hs_object_id", "amount", "pipeline"],
        "limit": 10
    }

    response = requests.post(
        f"{BASE_URL}/crm/v3/objects/deals/search",
        headers=headers,
        json=search_payload
    )

    if response.status_code != 200:
        print(f"❌ Failed to search deals: {response.text}")
        return None

    results = response.json().get("results", [])
    if not results:
        print(f"❌ Deal not found: {deal_name}")
        return None

    deal = results[0]
    print(f"✅ Found deal: {deal['properties']['dealname']} (ID: {deal['id']})")
    return deal

def add_deal_note(deal_name, note_text):
    """
    Add a note/engagement to a deal

    Args:
        deal_name (str): Deal name
        note_text (str): Note content

    Returns:
        bool: Success status
    """
    deal = search_deal(deal_name)
    if not deal:
        return False

    deal_id = deal['id']

    print(f"📝 Adding note to deal: {deal_name}")

    engagement_payload = {
        "engagement": {
            "active": True,
            "type": "NOTE",
            "timestamp": int(datetime.now().timestamp() * 1000)
        },
        "associations": {
            "dealIds": [int(deal_id)]
        },
        "metadata": {
            "body": note_text
        }
    }

    response = requests.post(
        f"{BASE_URL}/engagements/v1/engagements",
        headers=headers,
        json=engagement_payload
    )

    if response.status_code in [200, 201]:
        print(f"✅ Note added successfully")
        return True
    else:
        print(f"❌ Failed to add note: {response.text}")
        return False

def create_task(deal_name, task_subject, task_body, priority="HIGH", due_days=1):
    """
    Create a task associated with a deal

    Args:
        deal_name (str): Deal name
        task_subject (str): Task title
        task_body (str): Task description
        priority (str): HIGH, MEDIUM, or LOW
        due_days (int): Days from now for due date

    Returns:
        bool: Success status
    """
    deal = search_deal(deal_name)
    if not deal:
        return False

    deal_id = deal['id']

    # Calculate due date timestamp
    due_date = datetime.now() + timedelta(days=due_days)
    due_timestamp = int(due_date.timestamp() * 1000)

    print(f"✅ Creating task: {task_subject}")

    task_payload = {
        "engagement": {
            "active": True,
            "type": "TASK",
            "timestamp": int(datetime.now().timestamp() * 1000)
        },
        "associations": {
            "dealIds": [int(deal_id)],
            "ownerIds": [int(OWNER_ID)]
        },
        "metadata": {
            "body": task_body,
            "subject": task_subject,
            "status": "NOT_STARTED",
            "forObjectType": "DEAL",
            "priority": priority,
            "taskType": "TODO"
        }
    }

    response = requests.post(
        f"{BASE_URL}/engagements/v1/engagements",
        headers=headers,
        json=task_payload
    )

    if response.status_code in [200, 201]:
        print(f"✅ Task created successfully")
        return True
    else:
        print(f"❌ Failed to create task: {response.text}")
        return False

def update_deal_stage(deal_name, new_stage_folder):
    """
    Update a deal's stage

    Args:
        deal_name (str): Deal name
        new_stage_folder (str): Stage folder name like "[07-CLOSED-WON]"

    Returns:
        bool: Success status
    """
    deal = search_deal(deal_name)
    if not deal:
        return False

    deal_id = deal['id']

    # Get stage ID from folder name
    stage_id = FOLDER_TO_STAGE_ID.get(new_stage_folder)
    if not stage_id:
        print(f"❌ Invalid stage folder: {new_stage_folder}")
        return False

    print(f"🔄 Moving deal to stage: {new_stage_folder}")

    update_payload = {
        "properties": {
            "dealstage": stage_id
        }
    }

    response = requests.patch(
        f"{BASE_URL}/crm/v3/objects/deals/{deal_id}",
        headers=headers,
        json=update_payload
    )

    if response.status_code == 200:
        print(f"✅ Deal stage updated successfully")
        return True
    else:
        print(f"❌ Failed to update stage: {response.text}")
        return False

def log_call(deal_name, call_notes, outcome="COMPLETED"):
    """
    Log a call to a deal

    Args:
        deal_name (str): Deal name
        call_notes (str): Call notes/summary
        outcome (str): COMPLETED, NO_ANSWER, LEFT_VOICEMAIL, etc.

    Returns:
        bool: Success status
    """
    deal = search_deal(deal_name)
    if not deal:
        return False

    deal_id = deal['id']

    print(f"📞 Logging call for: {deal_name}")

    call_payload = {
        "engagement": {
            "active": True,
            "type": "CALL",
            "timestamp": int(datetime.now().timestamp() * 1000)
        },
        "associations": {
            "dealIds": [int(deal_id)]
        },
        "metadata": {
            "body": call_notes,
            "disposition": outcome,
            "status": "COMPLETED"
        }
    }

    response = requests.post(
        f"{BASE_URL}/engagements/v1/engagements",
        headers=headers,
        json=call_payload
    )

    if response.status_code in [200, 201]:
        print(f"✅ Call logged successfully")
        return True
    else:
        print(f"❌ Failed to log call: {response.text}")
        return False

def log_email(deal_name, subject, direction="OUTBOUND", notes=""):
    """
    Log an email to a deal

    Args:
        deal_name (str): Deal name
        subject (str): Email subject
        direction (str): OUTBOUND or INBOUND
        notes (str): Additional notes

    Returns:
        bool: Success status
    """
    deal = search_deal(deal_name)
    if not deal:
        return False

    deal_id = deal['id']

    print(f"📧 Logging email for: {deal_name}")

    email_payload = {
        "engagement": {
            "active": True,
            "type": "EMAIL",
            "timestamp": int(datetime.now().timestamp() * 1000)
        },
        "associations": {
            "dealIds": [int(deal_id)]
        },
        "metadata": {
            "subject": subject,
            "html": notes if notes else f"{direction} email: {subject}",
            "text": notes if notes else f"{direction} email: {subject}"
        }
    }

    response = requests.post(
        f"{BASE_URL}/engagements/v1/engagements",
        headers=headers,
        json=email_payload
    )

    if response.status_code in [200, 201]:
        print(f"✅ Email logged successfully")
        return True
    else:
        print(f"❌ Failed to log email: {response.text}")
        return False

def update_deal_property(deal_name, property_name, value):
    """
    Update a specific deal property

    Args:
        deal_name (str): Deal name
        property_name (str): Property name (e.g., "amount", "closedate")
        value: Property value

    Returns:
        bool: Success status
    """
    deal = search_deal(deal_name)
    if not deal:
        return False

    deal_id = deal['id']

    print(f"🔄 Updating {property_name} for: {deal_name}")

    update_payload = {
        "properties": {
            property_name: str(value)
        }
    }

    response = requests.patch(
        f"{BASE_URL}/crm/v3/objects/deals/{deal_id}",
        headers=headers,
        json=update_payload
    )

    if response.status_code == 200:
        print(f"✅ Property updated successfully")
        return True
    else:
        print(f"❌ Failed to update property: {response.text}")
        return False

if __name__ == '__main__':
    # Test functions if needed
    import argparse

    parser = argparse.ArgumentParser(description='HubSpot Real-Time Update Helper')
    parser.add_argument('action', choices=['note', 'task', 'stage', 'call', 'email', 'property'])
    parser.add_argument('deal_name', help='Deal name')
    parser.add_argument('--text', help='Note text, call notes, or email notes')
    parser.add_argument('--subject', help='Task or email subject')
    parser.add_argument('--body', help='Task body')
    parser.add_argument('--priority', default='HIGH', help='Task priority')
    parser.add_argument('--due_days', type=int, default=1, help='Task due in days')
    parser.add_argument('--stage', help='New stage folder name')
    parser.add_argument('--outcome', default='COMPLETED', help='Call outcome')
    parser.add_argument('--direction', default='OUTBOUND', help='Email direction')
    parser.add_argument('--property', help='Property name to update')
    parser.add_argument('--value', help='Property value')

    args = parser.parse_args()

    if args.action == 'note':
        add_deal_note(args.deal_name, args.text)
    elif args.action == 'task':
        create_task(args.deal_name, args.subject, args.body, args.priority, args.due_days)
    elif args.action == 'stage':
        update_deal_stage(args.deal_name, args.stage)
    elif args.action == 'call':
        log_call(args.deal_name, args.text, args.outcome)
    elif args.action == 'email':
        log_email(args.deal_name, args.subject, args.direction, args.text)
    elif args.action == 'property':
        update_deal_property(args.deal_name, args.property, args.value)
