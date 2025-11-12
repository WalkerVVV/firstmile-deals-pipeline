# Missing Stages Recommendation

**Issue**: [00-LEAD] and [09-WIN-BACK] folder stages exist locally but are not in the HubSpot FM pipeline

**Date**: October 7, 2025

---

## Current Situation

### What We Found

**HubSpot FM Pipeline** has 8 stages (verified via API):
1. Discovery Scheduled (ID: `1090865183`)
2. Discovery Complete (ID: `d2a08d6f-cc04-4423-9215-594fe682e538`)
3. Rate Creation (ID: `e1c4321e-afb6-4b29-97d4-2b2425488535`)
4. Proposal Sent (ID: `d607df25-2c6d-4a5d-9835-6ed1e4f4020a`)
5. Setup Docs Sent (ID: `4e549d01-674b-4b31-8a90-91ec03122715`)
6. Implementation (ID: `08d9c411-5e1b-487b-8732-9c2bcbbd0307`)
7. Started Shipping (ID: `3fd46d94-78b4-452b-8704-62a338a210fb`) - **Closed Won**
8. Closed Lost (ID: `02d8a1d7-d0b3-41d9-adc6-44ab768a61b8`)

**Your Local Folder Structure** has 10 stages:
- [00-LEAD] ⚠️ Not in HubSpot
- [01-DISCOVERY-SCHEDULED] ✅ In HubSpot
- [02-DISCOVERY-COMPLETE] ✅ In HubSpot
- [03-RATE-CREATION] ✅ In HubSpot
- [04-PROPOSAL-SENT] ✅ In HubSpot
- [05-SETUP-DOCS-SENT] ✅ In HubSpot
- [06-IMPLEMENTATION] ✅ In HubSpot
- [07-CLOSED-WON] ✅ In HubSpot
- [08-CLOSED-LOST] ✅ In HubSpot
- [09-WIN-BACK] ⚠️ Not in HubSpot

---

## Impact Analysis

### Current Impact: **MINIMAL**

Your system is working fine because:

1. **[00-LEAD]**: Acts as a pre-pipeline "holding area"
   - Deals here aren't ready for Discovery yet
   - Local-only tracking until they're qualified
   - When qualified → Move to [01-DISCOVERY-SCHEDULED]

2. **[09-WIN-BACK]**: Re-engagement tracking
   - Deals move here from [08-CLOSED-LOST] when there's renewed interest
   - Local-only tracking for win-back campaigns
   - When re-qualified → Move back to [02-DISCOVERY-COMPLETE]

### Sync Implications

**`pipeline_sync_verification.py` will show discrepancies**:
- Deals in [00-LEAD] folders won't be in HubSpot (expected)
- Deals in [09-WIN-BACK] folders won't match HubSpot (expected)

**This is OKAY** as long as you understand these are local-only stages.

---

## Recommended Actions

### ✅ Option 1: Keep Current System (RECOMMENDED)

**Rationale**: The 2-stage gap actually provides useful flexibility

**How It Works**:
- **[00-LEAD]**: Pre-qualification area (local tracking only)
  - Use for prospects that need more research before Discovery
  - No HubSpot record needed yet (might not even qualify)
  - When ready → Create HubSpot deal at [01-DISCOVERY-SCHEDULED]

- **[09-WIN-BACK]**: Re-engagement tracking (local tracking only)
  - Closed-Lost deals that show renewed interest
  - Track win-back attempts without cluttering main pipeline
  - When re-engaged → Update HubSpot to appropriate stage

**Advantages**:
- ✅ No changes needed (system already works)
- ✅ Keeps HubSpot pipeline clean and focused on active deals
- ✅ Pre-qualification doesn't inflate pipeline metrics
- ✅ Win-back tracking separate from new business

**Implementation**:
1. Document in README.md that [00] and [09] are local-only
2. Update `pipeline_sync_verification.py` to skip these stages in sync checks
3. Add note in VERIFIED_STAGE_IDS.md (already done)
4. Communicate to team that these stages don't sync to HubSpot

### Option 2: Add Stages to HubSpot

**Add [00-LEAD] as first stage in HubSpot**:
```
Pros:
- Complete alignment between folders and HubSpot
- All deals tracked in CRM from first contact
- Better reporting on lead volume

Cons:
- Clutters pipeline with unqualified leads
- Inflates deal count metrics
- May need to archive/delete many unqualified leads
- HubSpot becomes the bottleneck for early stage tracking
```

**Add [09-WIN-BACK] as stage after Closed Lost**:
```
Pros:
- Formal win-back process tracking in HubSpot
- Better reporting on re-engagement success rate
- Complete folder-to-HubSpot alignment

Cons:
- Reopening closed-lost deals may mess with reporting
- Win-back success rate typically low (<10%)
- Could create noise in pipeline metrics
```

**How to Add** (if you choose this):
1. Go to HubSpot Settings → Objects → Deals → Pipelines
2. Edit FM Pipeline
3. Add new stage:
   - **For [00-LEAD]**: Insert before "Discovery Scheduled"
     - Name: "Lead"
     - Probability: 0.1 (10%)
   - **For [09-WIN-BACK]**: Insert after "Closed Lost"
     - Name: "Win Back"
     - Probability: 0.05 (5%)
4. Note the new stage IDs
5. Update VERIFIED_STAGE_IDS.md
6. Update pipeline_sync_verification.py

### Option 3: Hybrid Approach

**For [00-LEAD]**: Keep local-only (pre-qualification)
**For [09-WIN-BACK]**: Add to HubSpot (formal re-engagement)

**Rationale**:
- [00-LEAD] is truly pre-pipeline (not worth tracking in CRM)
- [09-WIN-BACK] is a formal process that deserves CRM tracking

---

## Recommendation Matrix

| Stage | Recommendation | Reason |
|-------|---------------|--------|
| **[00-LEAD]** | Keep local-only | Pre-qualification area, many won't qualify, no need to clutter HubSpot |
| **[09-WIN-BACK]** | Keep local-only OR add to HubSpot | Depends on: Do you actively track win-back success rate? |

### Decision Factors for [09-WIN-BACK]

**Add to HubSpot if**:
- You have formal win-back campaigns
- You track re-engagement metrics
- You want CRM reporting on win-back success rate
- You have >10 win-back attempts per quarter

**Keep local-only if**:
- Win-backs are rare and ad-hoc
- You don't formally track win-back metrics
- You prefer clean closed-lost reporting
- Most win-backs are opportunistic (not systematic)

---

## Implementation: Keep Current System

### Step 1: Update Documentation

Add to README.md:
```markdown
### Local-Only Stages

Two stages exist in folder structure but not in HubSpot:

- **[00-LEAD]**: Pre-qualification holding area
  - Prospects needing research before Discovery
  - Not yet qualified for CRM tracking
  - Move to [01] when Discovery scheduled

- **[09-WIN-BACK]**: Re-engagement tracking
  - Closed-Lost deals showing renewed interest
  - Track win-back attempts locally
  - Update HubSpot when deal re-qualifies
```

### Step 2: Update Sync Script

Modify `pipeline_sync_verification.py`:

```python
# Stages that are local-only (expected to not be in HubSpot)
LOCAL_ONLY_STAGES = ["[00-LEAD]", "[09-WIN-BACK]"]

# In comparison logic, skip local-only stages:
for stage in all_stages:
    if stage in LOCAL_ONLY_STAGES:
        print(f"{stage:<30} {'N/A':>12} {local_count:>12} {'LOCAL ONLY':>15}")
        continue

    # ... rest of sync logic
```

### Step 3: Update VERIFIED_STAGE_IDS.md

Already done! The file notes:
```
# Note: [00-LEAD] and [09-WIN-BACK] are local-only stages (not in HubSpot FM pipeline)
```

### Step 4: Update Daily Sync Prompts

Ensure 9AM/NOON/EOD syncs understand these stages are local-only:
- Don't expect HubSpot data for [00] or [09]
- Focus HubSpot queries on stages [01-08] only

---

## Alternative: Add [09-WIN-BACK] to HubSpot

**If you decide to add it**, here's the step-by-step:

### HubSpot Configuration

1. Go to: Settings → Objects → Deals → Pipelines
2. Select: FM Pipeline
3. Click: Add Stage (after Closed Lost)
4. Configure:
   ```yaml
   Stage Name: Win Back
   Stage Order: 9 (after Closed Lost)
   Probability: 0.05 (5% - low success rate)
   Stage Type: Open (not closed won/lost)
   ```
5. Save and note the Stage ID

### Update System

1. Add stage ID to VERIFIED_STAGE_IDS.md
2. Add to STAGE_MAPPING in pipeline_sync_verification.py
3. Update HUBSPOT_WORKFLOW_GUIDE.md
4. Update DAILY_SYNC_FLOWS_V3.md

### Create Win-Back Workflow

1. Define win-back criteria (timeframe, signals)
2. Create follow-up SLA (30 days?)
3. Build win-back playbook
4. Track success metrics

---

## Summary & Decision

**Current State**: 8 HubSpot stages, 10 local folders (2-stage gap)

**Recommended**: **Keep current system** with [00] and [09] as local-only

**Why**:
- ✅ System already works perfectly
- ✅ Clean HubSpot pipeline focused on qualified deals
- ✅ Local flexibility for pre-qual and re-engagement
- ✅ No changes or migrations needed
- ✅ Simpler system overall

**Action Required**: Document the local-only nature of [00] and [09] in README and sync scripts

**Alternative**: Add [09-WIN-BACK] to HubSpot only if you run formal win-back campaigns with metrics tracking

---

**Decision Owner**: Brett Walker
**Default Recommendation**: Keep current local-only system
**Review Date**: After running system for 30 days to validate workflow
