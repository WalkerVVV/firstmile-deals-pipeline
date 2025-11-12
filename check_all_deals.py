#!/usr/bin/env python3
import sys
sys.path.insert(0, '.claude/agents')
from prioritization_agent import fetch_active_deals_from_hubspot, STAGE_MAP, calculate_priority_score, days_since

deals = fetch_active_deals_from_hubspot()
results = []

for deal in deals:
    name = deal['properties']['dealname']
    stage_id = deal['properties']['dealstage']
    stage = STAGE_MAP.get(stage_id, 'UNKNOWN')
    amount = int(deal['properties'].get('amount', '0') or 0)
    hs_priority = deal['properties'].get('hs_priority', 'none')
    modified = deal['properties'].get('hs_lastmodifieddate')
    notes = deal['properties'].get('notes_last_updated')
    
    days_stag = days_since(modified)
    days_notes = days_since(notes)
    
    score, tier = calculate_priority_score(name, amount, stage, days_stag, hs_priority, days_notes)
    
    results.append((score, name, stage, hs_priority, amount))

results.sort(reverse=True)

print("\nALL DEALS (sorted by score):")
print("="*80)
for i, (score, name, stage, priority, amount) in enumerate(results, 1):
    priority_flag = f" [HS: {priority.upper()}]" if priority != 'none' else ""
    print(f"{i:2}. Score: {score:5.1f} | ${amount/1000:6.0f}K | {stage:25} | {name}{priority_flag}")

# Find Stackd
print("\n" + "="*80)
print("STACKD LOGISTICS DEALS:")
for i, (score, name, stage, priority, amount) in enumerate(results, 1):
    if 'stackd' in name.lower():
        print(f"#{i} - Score: {score} | {stage} | HS Priority: {priority} | ${amount:,}")
