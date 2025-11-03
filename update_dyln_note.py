#!/usr/bin/env python3
"""
Update DYLN deal with DHL partner context and volume constraints
"""

from hubspot_utils import HubSpotClient, format_currency
from datetime import datetime
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize HubSpot client
client = HubSpotClient()

# DYLN Deal - search first
deal_name = "DYLN"

try:
    print(f"Searching for {deal_name} deal...")
    
    # Search for DYLN deal
    filters = [
        {
            'propertyName': 'dealname',
            'operator': 'CONTAINS_TOKEN',
            'value': 'DYLN'
        }
    ]
    
    properties = ['dealname', 'amount', 'dealstage', 'pipeline']
    
    search_results = client.search_deals(filters, properties, limit=10)
    
    if search_results.get('results'):
        deal = search_results['results'][0]
        deal_id = deal['id']
        
        print(f"Found deal: {deal['properties']['dealname']} (ID: {deal_id})")
        print(f"   Amount: {format_currency(float(deal['properties'].get('amount', 0)))}")
        print(f"   Stage ID: {deal['properties'].get('dealstage', 'N/A')}\n")
        
        # Create detailed note about DHL situation
        note_body = f"""<h3>DYLN DHL Partnership Context - Updated {datetime.now().strftime('%m/%d/%Y')}</h3>

<p><strong>NOT URGENT - PARTNER RESPECT SITUATION</strong></p>

<h4>DHL Direct Engagement:</h4>
<ul>
<li>Dorian contacted DHL directly and engaged their sales rep</li>
<li>DHL called FirstMile for approval before engaging (proper partner protocol)</li>
<li>Dorian signed agreement directly with DHL</li>
<li>FirstMile approved - will <strong>NOT</strong> compete against partner DHL on this account</li>
</ul>

<h4>Volume Constraints:</h4>
<ul>
<li>DYLN ships ~35 parcels/day (below FirstMile minimum of 100/day)</li>
<li>This is why account was previously released</li>
<li>Current volume too low for Xparcel services</li>
</ul>

<h4>FirstMile Position:</h4>
<ul>
<li>Can offer all Xparcel services <strong>EXCEPT</strong> competing with DHL lanes</li>
<li>Waiting on Dorian to share destination ZIP codes</li>
<li>Need ZIP analysis to determine potential FirstMile volume (non-DHL lanes)</li>
<li>Dorian focused on DHL setup + Peak Season prep</li>
</ul>

<h4>Next Steps:</h4>
<ul>
<li>Wait for destination ZIP list from Dorian</li>
<li>Analyze volume potential for FirstMile services on non-DHL lanes</li>
<li>No urgency - let DHL partnership develop</li>
<li>Follow up when Dorian provides ZIP data</li>
</ul>

<p><strong>Status:</strong> Low priority, partner respect protocol in effect</p>"""

        # Create note
        note_result = client.create_note(
            deal_id=deal_id,
            note_body=note_body
        )
        
        print(f"Created note on deal (Note ID: {note_result['id']})")
        
        # Update deal to reflect low priority status
        update_props = {
            'notes_last_updated': datetime.now().isoformat()
        }
        
        client.update_deal(deal_id, update_props)
        
        print(f"\nDYLN deal updated successfully")
        print(f"   - Added context about DHL partnership")
        print(f"   - Marked as low priority (partner respect)")
        print(f"   - Documented volume constraints (~35/day vs 100 min)")
        print(f"   - Next step: Wait for ZIP list from Dorian")
        print(f"\nSummary:")
        print(f"   • NOT competing with DHL (partner respect)")
        print(f"   • Volume below threshold (35 vs 100 parcels/day)")
        print(f"   • Waiting on ZIP data for non-DHL lane analysis")
        print(f"   • Low urgency - let Peak Season pass")
        
    else:
        print(f"No deal found matching '{deal_name}'")

except Exception as e:
    print(f"Error updating DYLN deal: {str(e)}")
    import traceback
    traceback.print_exc()

