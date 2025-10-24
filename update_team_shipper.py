import sys
import io
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_KEY = "pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764"
OWNER_ID = "699257003"
STAGE_PROPOSAL_SENT = "d607df25-2c6d-4a5d-9835-6ed1e4f4020a"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

search_payload = {
    "filterGroups": [{
        "filters": [
            {"propertyName": "dealname", "operator": "CONTAINS_TOKEN", "value": "Team Shipper"},
            {"propertyName": "hubspot_owner_id", "operator": "EQ", "value": OWNER_ID}
        ]
    }],
    "properties": ["dealname", "dealstage"],
    "limit": 10
}

print("Searching for Team Shipper deal...")
response = requests.post("https://api.hubapi.com/crm/v3/objects/deals/search", headers=headers, json=search_payload)

results = response.json().get("results", [])
team_shipper_deal = next((d for d in results if "New Deal" in d["properties"]["dealname"]), results[0] if results else None)

if not team_shipper_deal:
    print("[ERROR] Team Shipper deal not found")
    exit(1)

deal_id = team_shipper_deal["id"]
deal_name = team_shipper_deal["properties"]["dealname"]

print(f"[OK] Found: {deal_name} (ID: {deal_id})")
print("Updating to [04-PROPOSAL-SENT] with Jira ticket RATE-1897...")

update_payload = {"properties": {"dealstage": STAGE_PROPOSAL_SENT, "hs_ticket_id": "RATE-1897"}}
update_response = requests.patch(f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}", headers=headers, json=update_payload)

if update_response.status_code in [200, 201]:
    print("[SUCCESS] Team Shipper updated!")
    print("  - Stage: [04-PROPOSAL-SENT]")
    print("  - Jira: RATE-1897")
else:
    print(f"[ERROR] {update_response.text}")
