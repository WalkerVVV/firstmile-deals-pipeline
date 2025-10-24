# Local Folder Structure vs HubSpot Pipeline
**Date**: October 10, 2025
**System**: Nebuchadnezzar v2.0

---

## Understanding the Two Systems

### 🗂️ Local Folder Structure (10 Stages)
**Purpose**: File organization for deal documentation, analysis, and tracking
**Location**: `C:\Users\BrettWalker\FirstMile_Deals\`

```
[00-LEAD]                   - Initial prospect contact
[01-DISCOVERY-SCHEDULED]    - Meeting booked
[02-DISCOVERY-COMPLETE]     - Requirements gathered
[03-RATE-CREATION]          - Pricing work in progress
[04-PROPOSAL-SENT]          - Rates delivered to customer
[05-SETUP-DOCS-SENT]        - Contracts/setup documents sent
[06-IMPLEMENTATION]         - Onboarding in progress
[07-CLOSED-WON]             - Active customer (moved to customer success)
[08-CLOSED-LOST]            - Deal lost (no longer pursuing)
[09-WIN-BACK]               - NEW DEAL for re-engagement campaign
```

### 🔗 HubSpot Pipeline (8 Stages)
**Purpose**: CRM deal tracking and automation
**Pipeline Name**: "FM" (FirstMile)
**Pipeline ID**: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

```
[01] Discovery Scheduled    (ID: 1090865183)
[02] Discovery Complete     (ID: d2a08d6f-cc04-4423-9215-594fe682e538)
[03] Rate Creation          (ID: e1c4321e-afb6-4b29-97d4-2b2425488535)
[04] Proposal Sent          (ID: d607df25-2c6d-4a5d-9835-6ed1e4f4020a)
[05] Setup Docs Sent        (ID: 4e549d01-674b-4b31-8a90-91ec03122715)
[06] Implementation         (ID: 08d9c411-5e1b-487b-8732-9c2bcbbd0307)
[07] Started Shipping       (ID: 3fd46d94-78b4-452b-8704-62a338a210fb)
[08] Closed Lost            (ID: 02d8a1d7-d0b3-41d9-adc6-44ab768a61b8)
```

---

## Key Differences

### Stages Not in HubSpot:
- **[00-LEAD]**: Use [01] Discovery Scheduled in HubSpot instead
- **[09-WIN-BACK]**: Create NEW DEAL in HubSpot (explained below)

### Naming Differences:
- Local: `[07-CLOSED-WON]` → HubSpot: `[07] Started Shipping`
- Functionally the same, different labels

---

## Win-Back Process (The Important Part)

### ❌ WRONG Approach:
- Move existing closed-lost deal to [09-WIN-BACK] stage
- Update the old deal

### ✅ CORRECT Approach:
1. **Original deal stays in [08-CLOSED-LOST]** (both HubSpot and local folder)
2. **Create NEW DEAL in HubSpot** for the win-back campaign
3. **Create NEW local folder** `[09-WIN-BACK]_CustomerName_WinBack`
4. **Link the two**: Note in each deal references the other

### Why Create a New Deal?

A win-back campaign is **new business development**:
- Fresh discovery of current situation
- New rate analysis and proposal
- Different decision makers potentially
- New timeline and objections
- Separate tracking for win-back metrics
- Clean separation of historical vs current efforts

---

## Example: BoxiiShip AF Win-Back

### Current Situation (INCORRECT):
- Updated existing deal (ID: 36466918934) with "WIN-BACK" in title
- Tried to move to non-existent [09-WIN-BACK] stage in HubSpot
- Mixed historical and current activity

### What Should Happen (CORRECT):

#### Original Deal:
**HubSpot**:
- Deal Name: `BoxiiShip- American Fork` (keep original name)
- Stage: [08] Closed Lost
- Status: Historical record of lost deal
- Notes: Why we lost, when we lost, to whom we lost (UPS)

**Local Folder**: `[08-CLOSED-LOST]_BoxiiShip AF/`
- Historical PLD analysis
- Original rates that didn't win
- Loss analysis documentation

#### NEW Win-Back Deal:
**HubSpot**:
- Deal Name: `BoxiiShip American Fork - WIN-BACK CAMPAIGN 2025`
- Stage: [03] Rate Creation (RATE-1903 in progress)
- Amount: $7,200,000
- Priority: HIGH
- Notes:
  - Link to original deal (ID: 36466918934)
  - RATE-1903 completion status
  - Win-back strategy and approach
  - Financial impact analysis

**Local Folder**: `[09-WIN-BACK]_BoxiiShip_AF_2025/`
- RATE-1903_Taylar_Response.md
- Win-back strategy document
- New competitive analysis vs UPS
- Strategic presentation for Nate
- Link to original deal folder

---

## Folder Movement Rules

### Local Folders:
Move folder to new stage directory when status changes:
```bash
# Example: Moving from Rate Creation to Proposal Sent
move "[03-RATE-CREATION]_CustomerName" "[04-PROPOSAL-SENT]_CustomerName"
```

### HubSpot:
Update `dealstage` property via API or manual update in HubSpot UI

### Synchronization:
- Local folder moves trigger N8N automation (if configured)
- Manual moves require corresponding HubSpot update
- Use scripts to keep both systems in sync

---

## Mapping Guide

| Local Folder Stage | HubSpot Stage | HubSpot Stage ID |
|-------------------|---------------|------------------|
| [00-LEAD] | [01] Discovery Scheduled | 1090865183 |
| [01-DISCOVERY-SCHEDULED] | [01] Discovery Scheduled | 1090865183 |
| [02-DISCOVERY-COMPLETE] | [02] Discovery Complete | d2a08d6f-cc04-4423-9215-594fe682e538 |
| [03-RATE-CREATION] | [03] Rate Creation | e1c4321e-afb6-4b29-97d4-2b2425488535 |
| [04-PROPOSAL-SENT] | [04] Proposal Sent | d607df25-2c6d-4a5d-9835-6ed1e4f4020a |
| [05-SETUP-DOCS-SENT] | [05] Setup Docs Sent | 4e549d01-674b-4b31-8a90-91ec03122715 |
| [06-IMPLEMENTATION] | [06] Implementation | 08d9c411-5e1b-487b-8732-9c2bcbbd0307 |
| [07-CLOSED-WON] | [07] Started Shipping | 3fd46d94-78b4-452b-8704-62a338a210fb |
| [08-CLOSED-LOST] | [08] Closed Lost | 02d8a1d7-d0b3-41d9-adc6-44ab768a61b8 |
| [09-WIN-BACK] | **NEW DEAL** starting at [03] Rate Creation | varies by stage |

---

## Best Practices

### For Win-Back Deals:

1. **Always create NEW deal** (don't update original)
2. **Naming convention**: `CompanyName - WIN-BACK CAMPAIGN YYYY`
3. **Cross-reference**: Link original and win-back deals in notes
4. **Start at appropriate stage**: Usually [03-RATE-CREATION] or [04-PROPOSAL-SENT]
5. **Local folder naming**: `[09-WIN-BACK]_CompanyName_YYYY/`

### For Stage Synchronization:

1. **Local folder moves first** (manual or automation)
2. **Update HubSpot second** (manual or script)
3. **Verify both systems** match after changes
4. **Use stage IDs** not names in API calls

### For Documentation:

1. **Original deal folder**: Keep historical analysis
2. **Win-back deal folder**: Only new campaign materials
3. **Cross-link**: README or notes pointing to related folder
4. **Avoid duplication**: Don't copy old analysis to new folder

---

## Action Required for BoxiiShip AF

### Step 1: Revert Current Deal
- Deal ID: 36466918934
- Change name back to: `BoxiiShip- American Fork`
- Move to stage: [08] Closed Lost
- Add note explaining why lost (to UPS)

### Step 2: Create NEW Win-Back Deal
- Name: `BoxiiShip American Fork - WIN-BACK CAMPAIGN 2025`
- Stage: [04] Proposal Sent (RATE-1903 completed)
- Amount: $7,200,000
- Priority: HIGH
- Notes: Link to original deal, RATE-1903 status, win-back strategy

### Step 3: Organize Local Folders
- Keep: `[08-CLOSED-LOST]_BoxiiShip AF/` (historical)
- Create: `[09-WIN-BACK]_BoxiiShip_AF_2025/`
- Move RATE-1903 materials to win-back folder
- Add README linking the two folders

---

*Documentation Date: 2025-10-10*
*System: Nebuchadnezzar v2.0*
