#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick script to fetch HubSpot task details
Task: Call Brock Hanson at 2:30 PM about Claude Code, VSCode setup
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment (SECURE)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Task ID from URL: https://app.hubspot.com/contacts/8210927/record/0-3/36605366386
task_id = '36605366386'

print('=' * 80)
print('📋 HUBSPOT TASK DETAILS')
print('=' * 80)
print()

# Get task details
response = requests.get(
    f'https://api.hubapi.com/crm/v3/objects/tasks/{task_id}',
    headers=headers,
    params={'properties': 'hs_task_subject,hs_task_body,hs_timestamp,hs_task_status,hs_task_priority,hs_task_type'}
)

if response.status_code == 200:
    task = response.json()
    props = task.get('properties', {})

    print(f'Task ID: {task_id}')
    print(f'Subject: {props.get("hs_task_subject", "N/A")}')
    print(f'Type: {props.get("hs_task_type", "N/A")}')
    print(f'Priority: {props.get("hs_task_priority", "N/A")}')
    print(f'Status: {props.get("hs_task_status", "N/A")}')

    # Parse timestamp
    timestamp = props.get('hs_timestamp')
    if timestamp:
        try:
            dt = datetime.fromtimestamp(int(timestamp) / 1000)
            print(f'Due: {dt.strftime("%Y-%m-%d %I:%M %p")}')
        except:
            print(f'Due: {timestamp}')

    body = props.get('hs_task_body', '')
    if body:
        print(f'\nTask Body:\n{body}')

    print()
    print('─' * 80)

    # Get associated contacts
    assoc_response = requests.get(
        f'https://api.hubapi.com/crm/v3/objects/tasks/{task_id}/associations/contacts',
        headers=headers
    )

    if assoc_response.status_code == 200:
        assoc_data = assoc_response.json()
        contacts = assoc_data.get('results', [])

        if contacts:
            print('📞 ASSOCIATED CONTACTS')
            print('─' * 80)

            for contact in contacts:
                contact_id = contact.get('id')
                contact_response = requests.get(
                    f'https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}',
                    headers=headers,
                    params={'properties': 'firstname,lastname,email,phone,jobtitle,company'}
                )

                if contact_response.status_code == 200:
                    contact_data = contact_response.json()
                    cprops = contact_data.get('properties', {})

                    print(f'\nContact: {cprops.get("firstname", "")} {cprops.get("lastname", "")}')
                    print(f'Title: {cprops.get("jobtitle", "N/A")}')
                    print(f'Company: {cprops.get("company", "N/A")}')
                    print(f'Email: {cprops.get("email", "N/A")}')
                    print(f'Phone: {cprops.get("phone", "N/A")}')

            print()
            print('─' * 80)

    # Get associated deals
    deal_response = requests.get(
        f'https://api.hubapi.com/crm/v3/objects/tasks/{task_id}/associations/deals',
        headers=headers
    )

    if deal_response.status_code == 200:
        deal_data = deal_response.json()
        deals = deal_data.get('results', [])

        if deals:
            print('💼 ASSOCIATED DEALS')
            print('─' * 80)

            for deal in deals:
                deal_id = deal.get('id')
                deal_detail = requests.get(
                    f'https://api.hubapi.com/crm/v3/objects/deals/{deal_id}',
                    headers=headers,
                    params={'properties': 'dealname,dealstage,amount,closedate'}
                )

                if deal_detail.status_code == 200:
                    deal_props = deal_detail.json().get('properties', {})
                    amount = deal_props.get('amount', '0')

                    print(f'\nDeal: {deal_props.get("dealname", "N/A")}')
                    print(f'Amount: ${amount}')
                    print(f'Close Date: {deal_props.get("closedate", "N/A")}')

            print()
            print('─' * 80)

    print()
    print('✅ Task information retrieved successfully')
    print()
    print('🔔 REMINDER:')
    print('   Call Brock Hanson at 2:30 PM today')
    print('   Topics: Claude Code, VSCode, setup assistance')
    print()

else:
    print(f'❌ Error fetching task: {response.status_code}')
    print(response.text)

print('=' * 80)
