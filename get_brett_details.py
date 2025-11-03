#!/usr/bin/env python3
"""
Get Brett Walker's HubSpot details and pipeline info
"""

from hubspot_utils import HubSpotClient
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize HubSpot client
client = HubSpotClient()

print("Brett Walker HubSpot Details:")
print("=" * 60)
print(f"\nOwner ID: {client.owner_id}")
print(f"Default Pipeline ID: {client.pipeline_id}")

print("\n\nSearching for 'My Pipeline (FM) BW clone'...")

try:
    # Get all pipelines
    response = client._make_request('GET', '/crm/v3/pipelines/deals')
    pipelines = response.json()
    
    print(f"\nFound {len(pipelines.get('results', []))} deal pipelines:\n")
    
    for pipeline in pipelines.get('results', []):
        pipeline_id = pipeline['id']
        pipeline_label = pipeline['label']
        
        print(f"Pipeline: {pipeline_label}")
        print(f"  ID: {pipeline_id}")
        
        if 'BW clone' in pipeline_label or 'Brett Walker' in pipeline_label:
            print(f"  ** THIS IS YOUR PIPELINE **")
            print(f"\n  Stages:")
            for stage in pipeline.get('stages', []):
                print(f"    - {stage['label']}: {stage['id']}")
        print()

except Exception as e:
    print(f"Error getting pipeline details: {str(e)}")
    import traceback
    traceback.print_exc()

