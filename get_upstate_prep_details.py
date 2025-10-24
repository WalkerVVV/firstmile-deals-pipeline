#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Get detailed notes and tasks for Upstate Prep deal"""

import requests
import json
import sys
from datetime import datetime
from hubspot_config import get_hubspot_config, get_api_headers

# Set stdout encoding to UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Get HubSpot configuration
config = get_hubspot_config()
headers = get_api_headers()

DEAL_ID = '42448709378'

print("=" * 80)
print("UPSTATE PREP DEAL - DETAILED ACTIVITIES & TASKS")
print("=" * 80)
print()

# Get notes
print("NOTES/ACTIVITIES:")
print("-" * 80)
notes_url = f"{config['BASE_URL']}/crm/v3/objects/deals/{DEAL_ID}/associations/notes"
notes_response = requests.get(notes_url, headers=headers)

if notes_response.status_code == 200:
    notes_data = notes_response.json()
    if notes_data.get('results'):
        note_ids = [note['id'] for note in notes_data['results']]

        # Get details for each note
        for note_id in note_ids:
            note_detail_url = f"{config['BASE_URL']}/crm/v3/objects/notes/{note_id}"
            note_detail_params = {
                'properties': 'hs_note_body,hs_timestamp,hs_createdate'
            }
            note_response = requests.get(note_detail_url, headers=headers, params=note_detail_params)

            if note_response.status_code == 200:
                note = note_response.json()
                props = note['properties']

                timestamp = props.get('hs_timestamp') or props.get('hs_createdate', 'N/A')
                if timestamp != 'N/A':
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = dt.strftime('%Y-%m-%d %H:%M')
                    except:
                        pass

                body = props.get('hs_note_body') or 'No content'
                # Truncate long notes
                if body and len(body) > 200:
                    body = body[:200] + '...'

                print(f"[{timestamp}] {body}")
                print()
    else:
        print("No notes found")
else:
    print(f"Error fetching notes: {notes_response.status_code}")

print()
print("TASKS:")
print("-" * 80)

# Get tasks
tasks_url = f"{config['BASE_URL']}/crm/v3/objects/deals/{DEAL_ID}/associations/tasks"
tasks_response = requests.get(tasks_url, headers=headers)

if tasks_response.status_code == 200:
    tasks_data = tasks_response.json()
    if tasks_data.get('results'):
        task_ids = [task['id'] for task in tasks_data['results']]

        # Get details for each task
        for task_id in task_ids:
            task_detail_url = f"{config['BASE_URL']}/crm/v3/objects/tasks/{task_id}"
            task_detail_params = {
                'properties': 'hs_task_subject,hs_task_body,hs_task_status,hs_task_type,hs_timestamp,hs_task_priority'
            }
            task_response = requests.get(task_detail_url, headers=headers, params=task_detail_params)

            if task_response.status_code == 200:
                task = task_response.json()
                props = task['properties']

                subject = props.get('hs_task_subject', 'Untitled Task')
                status = props.get('hs_task_status', 'N/A')
                task_type = props.get('hs_task_type', 'N/A')
                priority = props.get('hs_task_priority', 'N/A')
                due_date = props.get('hs_timestamp', 'N/A')

                if due_date != 'N/A':
                    try:
                        dt = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                        due_date = dt.strftime('%Y-%m-%d')
                    except:
                        pass

                print(f"Task ID: {task_id}")
                print(f"Subject: {subject}")
                print(f"Status: {status}")
                print(f"Type: {task_type}")
                print(f"Due: {due_date}")
                print(f"Priority: {priority}")

                body = props.get('hs_task_body', '')
                if body:
                    if len(body) > 150:
                        body = body[:150] + '...'
                    print(f"Body: {body}")

                print()
    else:
        print("No tasks found")
else:
    print(f"Error fetching tasks: {tasks_response.status_code}")

print("=" * 80)
