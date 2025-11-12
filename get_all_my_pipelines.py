#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get all Brett Walker's pipelines to identify the correct active pipeline
"""

import sys
import os
import io
import requests
from dotenv import load_dotenv

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    load_dotenv()
    API_KEY = os.environ.get('HUBSPOT_API_KEY')

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print("\n" + "="*80)
    print("FETCHING ALL DEAL PIPELINES")
    print("="*80 + "\n")

    # Get all pipelines
    url = "https://api.hubapi.com/crm/v3/pipelines/deals"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        pipelines = data.get('results', [])

        print(f"Found {len(pipelines)} total pipelines\n")

        for pipeline in pipelines:
            pipeline_id = pipeline.get('id')
            label = pipeline.get('label')
            archived = pipeline.get('archived', False)
            stages = pipeline.get('stages', [])

            print(f"Pipeline: {label}")
            print(f"  ID: {pipeline_id}")
            print(f"  Archived: {archived}")
            print(f"  Stage Count: {len(stages)}")

            # Check if this matches the one we've been using
            if pipeline_id == "8bd9336b-4767-4e67-9fe2-35dfcad7c8be":
                print(f"  ⚠️  THIS IS THE PIPELINE WE'VE BEEN QUERYING!")

            # Identify Brett's pipelines
            if "BW" in label.upper() or "BRETT" in label.upper():
                print(f"  ✅ BRETT WALKER PIPELINE")

                if "CLONE" in label.upper() or "ACTIVE" in label.upper():
                    print(f"  🎯 THIS SHOULD BE YOUR ACTIVE PIPELINE")
                elif "CLOSED" in label.upper() or "LOST" in label.upper():
                    print(f"  📦 This is your closed/lost pipeline")
                elif "ALL" in label.upper():
                    print(f"  📚 This is your all-time historical pipeline")

            print()

    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    print("="*80 + "\n")

if __name__ == "__main__":
    main()
