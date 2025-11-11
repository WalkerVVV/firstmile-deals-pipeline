#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get all stage IDs and deal counts from pipeline
"""

import sys
import os
import io
import requests
from dotenv import load_dotenv
from collections import defaultdict

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    load_dotenv()
    API_KEY = os.environ.get('HUBSPOT_API_KEY')

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    PIPELINE_ID = "8bd9336b-4767-4e67-9fe2-35dfcad7c8be"

    print("\n" + "="*80)
    print("FETCHING ALL PIPELINE STAGES AND DEAL COUNTS")
    print("="*80 + "\n")

    # Get pipeline configuration
    pipeline_url = f"https://api.hubapi.com/crm/v3/pipelines/deals/{PIPELINE_ID}"
    response = requests.get(pipeline_url, headers=headers)

    if response.status_code == 200:
        pipeline = response.json()
        stages = pipeline.get('stages', [])

        print(f"Pipeline: {pipeline.get('label', 'Unknown')}\n")
        print("Stages:")
        print("-" * 80)

        for stage in stages:
            print(f"\nStage ID: {stage['id']}")
            print(f"Label: {stage['label']}")
            print(f"Display Order: {stage.get('displayOrder', 'N/A')}")

    # Get all deals and count by stage
    print("\n" + "="*80)
    print("DEAL COUNTS BY STAGE")
    print("="*80 + "\n")

    deals_url = f"https://api.hubapi.com/crm/v3/objects/deals"
    params = {
        "limit": 100,
        "properties": "dealname,dealstage,amount",
        "associations": "contacts"
    }

    all_deals = []
    after = None

    while True:
        if after:
            params['after'] = after

        response = requests.get(deals_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            deals = data.get('results', [])
            all_deals.extend(deals)

            paging = data.get('paging', {})
            after = paging.get('next', {}).get('after')

            if not after:
                break
        else:
            print(f"Error fetching deals: {response.status_code}")
            break

    # Filter to this pipeline and count by stage
    stage_counts = defaultdict(lambda: {'count': 0, 'total_value': 0, 'deals': []})

    for deal in all_deals:
        props = deal.get('properties', {})
        stage_id = props.get('dealstage')
        amount = float(props.get('amount', 0) or 0)
        deal_name = props.get('dealname', 'Unknown')

        if stage_id:
            stage_counts[stage_id]['count'] += 1
            stage_counts[stage_id]['total_value'] += amount
            stage_counts[stage_id]['deals'].append({
                'name': deal_name,
                'amount': amount,
                'id': deal.get('id')
            })

    # Match with stage labels
    stage_lookup = {s['id']: s['label'] for s in stages}

    for stage_id in sorted(stage_counts.keys(), key=lambda x: stage_lookup.get(x, 'ZZZ')):
        info = stage_counts[stage_id]
        label = stage_lookup.get(stage_id, f'Unknown Stage ({stage_id})')

        print(f"\n{label}")
        print(f"  Stage ID: {stage_id}")
        print(f"  Deal Count: {info['count']}")
        print(f"  Total Value: ${info['total_value']:,.0f}")

    print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
