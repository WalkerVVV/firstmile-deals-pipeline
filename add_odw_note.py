#!/usr/bin/env python3
"""
Add win-back note to ODW Logistics deal
"""

from hubspot_utils import HubSpotClient, format_currency
from datetime import datetime
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize HubSpot client
client = HubSpotClient()

deal_id = "38741787982"
amount = "$25M"

try:
    print(f"Adding win-back note to ODW Logistics (ID: {deal_id})...")
    
    # Create note
    note_body = f"""<h3>Confirmed Win-Back Status - Went Silent</h3>
<p><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
<p><strong>Reason:</strong> Prospect went silent after proposal sent</p>

<h4>Context:</h4>
<ul>
<li>Deal Amount: {amount}</li>
<li>Status: Mega deal - Brock to prioritize</li>
<li>Last Activity: Proposal sent, no response</li>
<li>Communication: Went silent, no engagement</li>
<li>Stage: Already in [09-WIN-BACK] (correct placement)</li>
</ul>

<h4>Win-Back Strategy:</h4>
<ul>
<li>Wait 30-60 days before re-engagement</li>
<li>Monitor for trigger events (funding, new leadership, peak season pain)</li>
<li>Coordinate with Brock on timing and approach</li>
<li>Consider different decision-maker outreach</li>
</ul>

<p><strong>Next Action:</strong> Passive monitoring, wait for re-engagement opportunity</p>
<p><strong>Updated by:</strong> Brett Walker - Oct 30, 2025</p>"""

    note_result = client.create_note(
        deal_id=deal_id,
        note_body=note_body
    )
    
    print(f"Successfully created win-back note (Note ID: {note_result['id']})")
    print(f"\nODW Logistics confirmed in [09-WIN-BACK] with documentation")

except Exception as e:
    print(f"Error adding note: {str(e)}")
    import traceback
    traceback.print_exc()

