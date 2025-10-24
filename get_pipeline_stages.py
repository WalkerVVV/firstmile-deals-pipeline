#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch actual pipeline stages from HubSpot"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

API_KEY = 'pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764'
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
