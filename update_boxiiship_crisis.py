#!/usr/bin/env python3
"""
Update BoxiiShip HubSpot deals with October 2025 crisis context
"""

from hubspot_utils import HubSpotClient, format_currency
from datetime import datetime
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize HubSpot client
client = HubSpotClient()

try:
    print("Searching for BoxiiShip deals...")
    
    # Search for BoxiiShip deals
    filters = [
        {
            'propertyName': 'dealname',
            'operator': 'CONTAINS_TOKEN',
            'value': 'BoxiiShip'
        }
    ]
    
    properties = ['dealname', 'amount', 'dealstage', 'pipeline', 'createdate']
    
    search_results = client.search_deals(filters, properties, limit=20)
    
    if search_results.get('results'):
        print(f"\nFound {len(search_results['results'])} BoxiiShip deals:\n")
        
        for deal in search_results['results']:
            deal_id = deal['id']
            deal_name = deal['properties']['dealname']
            amount = deal['properties'].get('amount', '0')
            stage = deal['properties'].get('dealstage', 'Unknown')
            
            print(f"Deal: {deal_name}")
            print(f"  ID: {deal_id}")
            print(f"  Amount: {format_currency(float(amount))}")
            print(f"  Stage: {stage}\n")
            
            # Create crisis note for each deal
            note_body = f"""<h2>October 2025 Service Crisis - CRITICAL SITUATION</h2>

<p><strong>Status:</strong> Active Crisis Management - Customer Escalation Required</p>
<p><strong>Updated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>

<h3>Crisis Summary</h3>
<ul>
<li><strong>Period:</strong> October 6-20, 2025</li>
<li><strong>Impact:</strong> 287 DHL packages + 305+ ACI packages delayed</li>
<li><strong>Root Cause:</strong> ACI partner last-mile provider (DoorDash) contract breach</li>
<li><strong>Customer Complaints:</strong> 35 tracking numbers submitted (83% with "No First Scan")</li>
<li><strong>Relationship Status:</strong> Severely damaged - CEO (Reed) demanding answers</li>
</ul>

<h3>Key Metrics (Stephen Lineberry Analysis)</h3>
<ul>
<li><strong>ACI First Scan Delays:</strong> 5.77 days (Expedited), 6.95 days (Ground) vs. 1.5-1.8 days normal</li>
<li><strong>29 Packages:</strong> Still showing "No First Scan" (critical issue)</li>
<li><strong>Network Stabilized:</strong> October 20, 2025</li>
<li><strong>Total Volume (30 days):</strong> 13,694 packages</li>
</ul>

<h3>Immediate Actions Required</h3>
<ol>
<li><strong>Customer Call:</strong> Schedule with Reed (CEO) + Chris (ACI) for Oct 29/30
   <ul>
   <li>Attendees: Brett, Brock, Chris Von Melville, Lindsay (ACI tracking)</li>
   <li>Objective: Transparent explanation, rebuild trust</li>
   </ul>
</li>
<li><strong>Tracking Intelligence:</strong> Lindsay must explain 29 "No First Scan" packages</li>
<li><strong>Communication Strategy:</strong> Transparent approach (Chris's recommendation)</li>
</ol>

<h3>At Risk</h3>
<ul>
<li>Top 20 revenue account relationship</li>
<li>$500K/month Make Wellness win-back opportunity (paused)</li>
<li>Referral partner agreement value</li>
<li>Potential "remove ACI" decision from customer</li>
</ul>

<h3>Value Proposition (When Working)</h3>
<ul>
<li><strong>ACI Direct vs DHL:</strong> 37-54% faster, 32-54% cheaper</li>
<li><strong>Crisis Context:</strong> Anomaly during partner transition, not normal performance</li>
<li><strong>Peak Season:</strong> High confidence in stable network (Oct 20+)</li>
</ul>

<h3>Documentation</h3>
<ul>
<li><a href="file:///C:/Users/BrettWalker/FirstMile_Deals/[07-CLOSED-WON]_Boxiiship/OCTOBER_2025_SERVICE_CRISIS_POSTMORTEM.md">Crisis Post-Mortem (Full Details)</a></li>
<li><a href="file:///C:/Users/BrettWalker/FirstMile_Deals/[07-CLOSED-WON]_Boxiiship/CRISIS_ACTION_TRACKER.md">Action Tracker</a></li>
<li><a href="https://fathom.video/share/4cKrKCoX7DqoDLPNyGhvPQ8HytVGsEth">Fathom Recording (Oct 28 - 34 mins)</a></li>
</ul>

<h3>Next Steps</h3>
<ol>
<li>Brett calls Reed to understand full complaint scope</li>
<li>Lindsay provides tracking data on 29 unscanned packages</li>
<li>Customer call Oct 29/30 with transparent communication</li>
<li>Weekly service monitoring through Dec 31</li>
<li>Win-back Make Wellness after 30 days of stable performance</li>
</ol>

<p><strong>Priority:</strong> CRITICAL - Daily Updates Required</p>
<p><strong>Owner:</strong> Brett Walker</p>"""

            # Create note
            note_result = client.create_note(
                deal_id=deal_id,
                note_body=note_body
            )
            
            print(f"  Created crisis note (Note ID: {note_result['id']})")
        
        print(f"\nAll {len(search_results['results'])} BoxiiShip deals updated with crisis context")
        print("\nNext Steps:")
        print("1. Schedule customer call with Reed + Chris for Oct 29/30")
        print("2. Request tracking intelligence from Lindsay (29 unscanned packages)")
        print("3. Prepare transparent communication deck")
        print("4. DO NOT send tracking report before call")
        
    else:
        print("No BoxiiShip deals found")

except Exception as e:
    print(f"Error updating BoxiiShip deals: {str(e)}")
    import traceback
    traceback.print_exc()

