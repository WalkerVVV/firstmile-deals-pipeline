#!/usr/bin/env python3
"""
Move ODW Logistics to [09-WIN-BACK] stage - went silent
"""

from hubspot_utils import HubSpotClient, format_currency
from datetime import datetime
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize HubSpot client
client = HubSpotClient()

# Stage IDs
WINBACK_STAGE_ID = "d607df25-2c6d-4a5d-9835-6ed1e4f4020a"  # [01-DISCOVERY-SCHEDULED] used as WIN-BACK

try:
    print("Searching for ODW Logistics deal...")
    
    # Search for ODW deal
    filters = [
        {
            'propertyName': 'dealname',
            'operator': 'CONTAINS_TOKEN',
            'value': 'ODW'
        }
    ]
    
    properties = ['dealname', 'amount', 'dealstage', 'pipeline', 'closedate']
    
    search_results = client.search_deals(filters, properties, limit=10)
    
    if search_results.get('results'):
        for deal in search_results['results']:
            deal_id = deal['id']
            deal_name = deal['properties']['dealname']
            amount = deal['properties'].get('amount', '0')
            current_stage = deal['properties'].get('dealstage', 'Unknown')
            
            print(f"\nFound: {deal_name}")
            print(f"  ID: {deal_id}")
            print(f"  Amount: {format_currency(float(amount))}")
            print(f"  Current Stage: {current_stage}")
            
            if 'ODW' in deal_name or 'Logistics' in deal_name:
                # Update to win-back stage
                update_props = {
                    'dealstage': WINBACK_STAGE_ID,
                    'closedate': datetime.now().isoformat()
                }
                
                client.update_deal(deal_id, update_props)
                print(f"  Updated to [09-WIN-BACK] stage")
                
                # Create note
                note_body = f"""<h3>Moved to Win-Back - Went Silent</h3>
<p><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
<p><strong>Reason:</strong> Prospect went silent after proposal sent</p>

<h4>Context:</h4>
<ul>
<li>Deal Amount: {format_currency(float(amount))}</li>
<li>Status: Mega deal ($25M) - Brock to prioritize</li>
<li>Last Activity: Proposal sent, no response</li>
<li>Communication: Went silent, no engagement</li>
</ul>

<h4>Win-Back Strategy:</h4>
<ul>
<li>Wait 30-60 days before re-engagement</li>
<li>Monitor for trigger events (funding, new leadership, peak season pain)</li>
<li>Coordinate with Brock on timing and approach</li>
<li>Consider different decision-maker outreach</li>
</ul>

<p><strong>Next Action:</strong> Passive monitoring, wait for re-engagement opportunity</p>"""

                note_result = client.create_note(
                    deal_id=deal_id,
                    note_body=note_body
                )
                
                print(f"  Created win-back note (Note ID: {note_result['id']})")
                print(f"\nODW Logistics moved to [09-WIN-BACK] successfully")
                break
    else:
        print("No ODW deals found")

except Exception as e:
    print(f"Error moving ODW deal: {str(e)}")
    import traceback
    traceback.print_exc()

