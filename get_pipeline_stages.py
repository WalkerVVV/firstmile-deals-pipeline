#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch actual pipeline stages from HubSpot"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment (SECURE)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)
PIPELINE_ID = '8bd9336b-4767-4e67-9fe2-35dfcad7c8be'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

print('=' * 80)
print('FETCHING ACTUAL PIPELINE STAGES FROM HUBSPOT')
print('=' * 80)
print(f'Pipeline ID: {PIPELINE_ID}')
print()

# Get pipeline with stages
response = requests.get(
    f'https://api.hubapi.com/crm/v3/pipelines/deals/{PIPELINE_ID}',
    headers=headers
)

if response.status_code == 200:
    pipeline = response.json()

    print(f"Pipeline Name: {pipeline.get('label', 'N/A')}")
    print()
    print('STAGES:')
    print('-' * 80)

    stages = pipeline.get('stages', [])

    for i, stage in enumerate(stages, 1):
        stage_id = stage.get('id')
        stage_label = stage.get('label')
        stage_display_order = stage.get('displayOrder', i)

        print(f"{stage_display_order}. {stage_label}")
        print(f"   ID: {stage_id}")
        print()

    print('=' * 80)
    print('PYTHON MAPPING DICTIONARY')
    print('=' * 80)
    print()
    print('STAGE_MAP = {')
    for stage in stages:
        stage_id = stage.get('id')
        stage_label = stage.get('label')
        print(f"    '{stage_id}': '{stage_label}',")
    print('}')
    print()

else:
    print(f'Error: {response.status_code}')
    print(response.text)
