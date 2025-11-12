# VERIFIED HUBSPOT STAGE IDs

**Source**: HubSpot API (Direct Query)
**Date**: October 7, 2025
**Pipeline**: FM (8bd9336b-4767-4e67-9fe2-35dfcad7c8be)

---

## ✅ VERIFIED STAGE MAPPING (FM Pipeline)

### Complete Stage List (Display Order)

| Display Order | Stage Label | Stage ID | Probability | Your Folder Name |
|---------------|-------------|----------|-------------|------------------|
| 0 | Discovery Scheduled | `1090865183` | 0.2 | [01-DISCOVERY-SCHEDULED] |
| 1 | Discovery Complete | `d2a08d6f-cc04-4423-9215-594fe682e538` | 0.2 | [02-DISCOVERY-COMPLETE] |
| 2 | Rate Creation | `e1c4321e-afb6-4b29-97d4-2b2425488535` | 0.4 | [03-RATE-CREATION] |
| 3 | Proposal Sent | `d607df25-2c6d-4a5d-9835-6ed1e4f4020a` | 0.6 | [04-PROPOSAL-SENT] |
| 4 | Setup Docs Sent | `4e549d01-674b-4b31-8a90-91ec03122715` | 0.8 | [05-SETUP-DOCS-SENT] |
| 5 | Implementation | `08d9c411-5e1b-487b-8732-9c2bcbbd0307` | 0.9 | [06-IMPLEMENTATION] |
| 6 | Started Shipping | `3fd46d94-78b4-452b-8704-62a338a210fb` | 1.0 (Closed Won) | [07-CLOSED-WON] |
| 7 | Closed Lost | `02d8a1d7-d0b3-41d9-adc6-44ab768a61b8` | 0.0 (Closed Lost) | [08-CLOSED-LOST] |

---

## 🔧 PYTHON MAPPING DICTIONARY

```python
# VERIFIED FROM HUBSPOT API - October 7, 2025
STAGE_MAPPING = {
    "1090865183": "[01-DISCOVERY-SCHEDULED]",
    "d2a08d6f-cc04-4423-9215-594fe682e538": "[02-DISCOVERY-COMPLETE]",
    "e1c4321e-afb6-4b29-97d4-2b2425488535": "[03-RATE-CREATION]",
    "d607df25-2c6d-4a5d-9835-6ed1e4f4020a": "[04-PROPOSAL-SENT]",
    "4e549d01-674b-4b31-8a90-91ec03122715": "[05-SETUP-DOCS-SENT]",
    "08d9c411-5e1b-487b-8732-9c2bcbbd0307": "[06-IMPLEMENTATION]",
    "3fd46d94-78b4-452b-8704-62a338a210fb": "[07-CLOSED-WON]",
    "02d8a1d7-d0b3-41d9-adc6-44ab768a61b8": "[08-CLOSED-LOST]"
}

# Reverse mapping (Folder name → Stage ID)
FOLDER_TO_STAGE_ID = {
    "[01-DISCOVERY-SCHEDULED]": "1090865183",
    "[02-DISCOVERY-COMPLETE]": "d2a08d6f-cc04-4423-9215-594fe682e538",
    "[03-RATE-CREATION]": "e1c4321e-afb6-4b29-97d4-2b2425488535",
    "[04-PROPOSAL-SENT]": "d607df25-2c6d-4a5d-9835-6ed1e4f4020a",
    "[05-SETUP-DOCS-SENT]": "4e549d01-674b-4b31-8a90-91ec03122715",
    "[06-IMPLEMENTATION]": "08d9c411-5e1b-487b-8732-9c2bcbbd0307",
    "[07-CLOSED-WON]": "3fd46d94-78b4-452b-8704-62a338a210fb",
    "[08-CLOSED-LOST]": "02d8a1d7-d0b3-41d9-adc6-44ab768a61b8"
}
```

---

## ❓ MISSING STAGES

### [00-LEAD] - Not in HubSpot Pipeline
Your folder structure has `[00-LEAD]` but HubSpot FM pipeline starts at "Discovery Scheduled".

**Options**:
1. Create new stage in HubSpot before Discovery Scheduled
2. Map [00-LEAD] folders to [01-DISCOVERY-SCHEDULED] stage
3. Use [00-LEAD] as local-only pre-pipeline stage

### [09-WIN-BACK] - Not in Current Pipeline
Your folder structure has `[09-WIN-BACK]` but it's not in the FM pipeline.

**Options**:
1. Add "Win Back" stage after Closed Lost in HubSpot
2. Map [09-WIN-BACK] folders to a custom property
3. Use [09-WIN-BACK] as local-only re-engagement tracking

---

## ✅ CONFLICTS RESOLVED

### Previous Conflict #1: [03-RATE-CREATION]
**RESOLVED**: Verified ID is `e1c4321e-afb6-4b29-97d4-2b2425488535`

**Sources Reconciled**:
- ✅ HubSpot API (Direct): `e1c4321e-afb6-4b29-97d4-2b2425488535`
- ❌ Old Source (pipeline_sync_verification.py): `1090865183` (This was actually Discovery Scheduled!)

**Finding**: The old script had Discovery Scheduled labeled as "Rate Creation" - wrong mapping.

### Previous Conflict #2: [06-IMPLEMENTATION]
**RESOLVED**: Verified ID is `08d9c411-5e1b-487b-8732-9c2bcbbd0307`

### Previous Unknown: [05-SETUP-DOCS-SENT]
**RESOLVED**: Verified ID is `4e549d01-674b-4b31-8a90-91ec03122715`

---

## 📊 METADATA INSIGHTS

### Stage Probabilities (Win Likelihood)
```yaml
Discovery Scheduled:  20%  (1 in 5 will close)
Discovery Complete:   20%  (same as above)
Rate Creation:        40%  (2 in 5 will close)
Proposal Sent:        60%  (3 in 5 will close)
Setup Docs Sent:      80%  (4 in 5 will close)
Implementation:       90%  (9 in 10 will close)
Started Shipping:    100%  (closed won)
Closed Lost:           0%  (closed lost)
```

### Pipeline Progression
- **Early Stage** (Discovery): 20% probability
- **Mid Stage** (Rate/Proposal): 40-60% probability
- **Late Stage** (Setup/Implementation): 80-90% probability
- **Closed**: 100% or 0%

### Bottleneck Analysis
Based on probability jumps:
- **Biggest Jump**: Rate Creation → Proposal Sent (40% → 60%) = +20%
  - This is where deals either commit or stall
- **Critical Stage**: Setup Docs Sent (80% probability)
  - Verbal commit received, high likelihood to close

---

## 🔄 MIGRATION ACTIONS

### Update These Files Immediately:

1. **pipeline_sync_verification.py**
   - Replace STAGE_MAPPING with verified version above
   - Note: Old script had Discovery Scheduled (1090865183) mislabeled

2. **NEBUCHADNEZZAR_REFERENCE.md**
   - Update stage ID section with verified IDs
   - Remove conflict warnings

3. **README.md**
   - Update STAGE_MAPPING code block
   - Verify all stage references

4. **DAILY_SYNC_FLOWS_V3.md**
   - Confirm stage references match verified labels
   - Update any hardcoded stage IDs

5. **CHANGELOG.md**
   - Add entry for stage ID verification completion

---

## 🧪 VERIFICATION COMMAND

To re-verify at any time:
```bash
curl -X GET "https://api.hubapi.com/crm/v3/pipelines/deals" \
  -H "Authorization: Bearer ${HUBSPOT_API_KEY}" \
  -H "Content-Type: application/json" | python -m json.tool
```

Or using HubSpot CLI:
```bash
hs api crm.pipelines.pipelinesApi.getAll --object-type=deals
```

---

## 📝 NOTES

1. **Pipeline Name**: "FM" (FirstMile)
2. **Pipeline ID**: `8bd9336b-4767-4e67-9fe2-35dfcad7c8be`
3. **Total Stages**: 8 (Discovery Scheduled → Closed Lost)
4. **Stage Type**: 6 open stages + 2 closed (Won/Lost)
5. **Last Updated in HubSpot**: June 10, 2025

**Second Pipeline Found**: "SN" pipeline exists but not used for FirstMile deals

---

**Verification Source**: Direct HubSpot API Query
**Verified By**: Claude Code (Sonnet 4.5)
**Date**: October 7, 2025
**Status**: ✅ AUTHORITATIVE
