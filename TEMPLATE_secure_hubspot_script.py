#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SECURE TEMPLATE for HubSpot API Scripts
Copy this template when creating new scripts that need HubSpot API access

Usage:
    1. Copy this file
    2. Rename to your script name
    3. Update the docstring and script_purpose
    4. Add your script logic in the main() function
"""

import os
import sys
import io
from dotenv import load_dotenv
import requests
from datetime import datetime

# Fix Windows encoding for international characters and emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================================
# SECURITY: Load credentials from environment variables (NEVER hardcode!)
# ============================================================================

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment variables")
    print("\nTo fix this:")
    print("1. Make sure .env file exists in the project root")
    print("2. Add this line to .env file:")
    print("   HUBSPOT_API_KEY=pat-na1-YOUR-TOKEN-HERE")
    print("3. Never commit the .env file to git!")
    print()
    sys.exit(1)

# HubSpot Configuration
OWNER_ID = "699257003"  # Brett Walker
PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"  # FirstMile Pipeline
PORTAL_ID = "46526832"
BASE_URL = "https://api.hubapi.com"

# ============================================================================
# API Helper Functions
# ============================================================================

def get_headers():
    """Return standard headers for HubSpot API requests"""
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }


def search_deals(filters, properties=None, limit=100):
    """
    Search for deals with specified filters

    Args:
        filters: List of filter dicts with propertyName, operator, value
        properties: List of property names to return (default: dealname, dealstage)
        limit: Max results to return (default: 100)

    Returns:
        List of deal objects or empty list on error
    """
    if properties is None:
        properties = ["dealname", "dealstage", "hs_object_id"]

    payload = {
        "filterGroups": [{
            "filters": filters
        }],
        "properties": properties,
        "limit": limit
    }

    response = requests.post(
        f"{BASE_URL}/crm/v3/objects/deals/search",
        headers=get_headers(),
        json=payload
    )

    if response.status_code != 200:
        print(f"❌ Error searching deals: {response.text}")
        return []

    return response.json().get("results", [])


def create_task(deal_id, subject, body, task_type="EMAIL", priority="MEDIUM", due_days=0):
    """
    Create a task and associate it with a deal

    Args:
        deal_id: HubSpot deal ID
        subject: Task subject line
        body: Task description/body
        task_type: EMAIL, TODO, or CALL (default: EMAIL)
        priority: LOW, MEDIUM, or HIGH (default: MEDIUM)
        due_days: Days from now for due date (default: 0 = today)

    Returns:
        Task ID if successful, None otherwise
    """
    # Calculate due date timestamp
    due_date = datetime.now() + timedelta(days=due_days)
    due_timestamp = int(due_date.timestamp() * 1000)

    # Create task
    task_data = {
        "properties": {
            "hs_task_subject": subject,
            "hs_task_body": body,
            "hs_task_type": task_type,
            "hs_task_status": "NOT_STARTED",
            "hs_task_priority": priority,
            "hubspot_owner_id": OWNER_ID,
            "hs_timestamp": due_timestamp
        }
    }

    response = requests.post(
        f"{BASE_URL}/crm/v3/objects/tasks",
        headers=get_headers(),
        json=task_data
    )

    if response.status_code not in [200, 201]:
        print(f"❌ Failed to create task: {response.text}")
        return None

    task_id = response.json()["id"]

    # Associate task with deal
    assoc_data = [{
        "associationCategory": "HUBSPOT_DEFINED",
        "associationTypeId": 216  # Task to Deal association
    }]

    assoc_response = requests.put(
        f"{BASE_URL}/crm/v4/objects/tasks/{task_id}/associations/deals/{deal_id}",
        headers=get_headers(),
        json=assoc_data
    )

    if assoc_response.status_code not in [200, 201]:
        print(f"⚠️  Task created (ID: {task_id}) but failed to associate with deal")
        return task_id

    return task_id


def update_deal_stage(deal_id, stage_id):
    """
    Update a deal's stage

    Args:
        deal_id: HubSpot deal ID
        stage_id: New stage ID (from NEBUCHADNEZZAR_REFERENCE.md)

    Returns:
        True if successful, False otherwise
    """
    update_data = {
        "properties": {
            "dealstage": stage_id
        }
    }

    response = requests.patch(
        f"{BASE_URL}/crm/v3/objects/deals/{deal_id}",
        headers=get_headers(),
        json=update_data
    )

    if response.status_code != 200:
        print(f"❌ Failed to update deal stage: {response.text}")
        return False

    return True


# ============================================================================
# Main Script Logic
# ============================================================================

def main():
    """
    Main script logic goes here
    Replace this with your actual script functionality
    """
    script_purpose = "YOUR SCRIPT PURPOSE HERE"

    print("\n" + "="*80)
    print(f"{script_purpose}")
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80 + "\n")

    # Example: Search for deals in a specific stage
    filters = [
        {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID},
        {"propertyName": "pipeline", "operator": "EQ", "value": PIPELINE_ID},
        # Add more filters as needed
    ]

    deals = search_deals(filters)
    print(f"Found {len(deals)} deals\n")

    # Your script logic here
    # ...

    print("\n" + "="*80)
    print("✅ Script completed successfully")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
