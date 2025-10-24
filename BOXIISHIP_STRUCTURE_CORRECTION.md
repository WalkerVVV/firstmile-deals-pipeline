# BoxiiShip AF Structure Correction
**Date**: October 10, 2025, 12:06 PM
**System**: Nebuchadnezzar v2.0

---

## ⚠️ IMPORTANT CORRECTION

BoxiiShip AF is **NOT** a closed-lost deal. They are an **ACTIVE CUSTOMER** (3PL).

### Actual Situation:
- **BoxiiShip AF**: Active FirstMile customer (3PL)
- **Make Wellness**: Their customer (volume lost to UPS)
- **Issue**: BoxiiShip lost Make Wellness volume to UPS
- **Win-Back**: Trying to get Make Wellness volume back to BoxiiShip (who will use FirstMile)

---

## Correct Folder Structure

### Main Customer Folder:
```
Customer-BoxiiShip_AF/
├── Customer_Profile.md
├── Active_Contracts/
├── Performance_Reports/
├── Historical_Analysis/
└── Win-Back_Make_Wellness_2025/    ← NEW subfolder for win-back campaign
    ├── README.md
    ├── RATE-1903_Taylar_Response.md
    ├── Strategic_Analysis_For_Nate.md
    ├── Make_Wellness_Volume_Analysis.md
    ├── Competitive_Analysis_vs_UPS.md
    └── Win_Back_Campaign_Plan.md
```

**NOT**: `[08-CLOSED-LOST]_BoxiiShip AF/` ❌
**YES**: `Customer-BoxiiShip_AF/Win-Back_Make_Wellness_2025/` ✅

---

## HubSpot Deal Structure

### Original Deal (Already Exists)
**Deal ID**: 36466918934
**Current Name**: `BoxiiShip- American Fork`
**Correct Stage**: [07-STARTED-SHIPPING] (active customer)
**Correct Name**: Should remain as customer deal

### Win-Back Deal (Just Created - ID: 45692064076)
**Name**: `BoxiiShip American Fork - Make Wellness WIN-BACK 2025`
**Stage**: [04] Proposal Sent
**Context**: Win back Make Wellness volume for BoxiiShip customer
**Parent Customer**: BoxiiShip AF (active)
**Lost Volume Customer**: Make Wellness (to UPS)

---

## What Needs to Change

### 1. Original Deal (36466918934)
**Current (WRONG)**:
- Stage: [08] Closed Lost
- Implication: BoxiiShip is not a customer

**Should Be (CORRECT)**:
- Stage: [07] Started Shipping (active customer)
- Name: `BoxiiShip American Fork - 3PL Customer`
- Notes: Active customer, but lost Make Wellness volume to UPS

### 2. Win-Back Deal (45692064076)
**Current**:
- Name: `BoxiiShip American Fork - WIN-BACK CAMPAIGN 2025`

**Should Be (MORE SPECIFIC)**:
- Name: `BoxiiShip AF - Make Wellness Volume WIN-BACK 2025`
- Makes clear it's Make Wellness volume, not BoxiiShip customer

### 3. Local Folder Structure
**Current (WRONG)**:
```
[08-CLOSED-LOST]_BoxiiShip AF/    ← Implies they're not a customer
```

**Should Be (CORRECT)**:
```
Customer-BoxiiShip_AF/
└── Win-Back_Make_Wellness_2025/
```

---

## Corrective Actions Required

### HubSpot Updates

1. **Revert original deal AGAIN** (36466918934)
   - Move to [07] Started Shipping (active customer)
   - Update name to clarify they're active 3PL customer
   - Note: Lost Make Wellness volume to UPS, but still our customer

2. **Update win-back deal** (45692064076)
   - Clarify it's Make Wellness volume win-back
   - Keep in [04] Proposal Sent
   - Add context: Parent customer BoxiiShip AF is active

### Local Folder Reorganization

1. **Rename existing folder**:
   ```
   FROM: [08-CLOSED-LOST]_BoxiiShip AF
   TO:   Customer-BoxiiShip_AF
   ```

2. **Create win-back subfolder**:
   ```
   Customer-BoxiiShip_AF/Win-Back_Make_Wellness_2025/
   ```

3. **Organize materials**:
   - Customer profile and active business: Main folder
   - Make Wellness win-back campaign: Subfolder
   - RATE-1903: Win-back subfolder

---

## Business Context

**BoxiiShip American Fork** = 3PL customer who uses FirstMile
**Make Wellness** = BoxiiShip's customer (end shipper)
**UPS** = Competitor who won Make Wellness volume

### Revenue Structure:
```
Make Wellness (shipper)
    └─> BoxiiShip AF (3PL) ← OUR CUSTOMER
           └─> FirstMile (carrier)
```

**What happened**: Make Wellness moved volume to UPS directly, bypassing BoxiiShip AF

**Win-back goal**: Get Make Wellness back to BoxiiShip AF, who will use FirstMile

**Annual value**: $7.2M (Make Wellness volume through BoxiiShip)

---

## Correct Understanding

### BoxiiShip AF Status:
- ✅ Active FirstMile customer
- ✅ Still shipping other volumes with us
- ❌ Lost Make Wellness volume to UPS (competitor)
- 🎯 Win-back: Get Make Wellness volume back

### Pipeline Classification:
- **Main Customer Deal**: [07] Started Shipping (active business)
- **Win-Back Campaign**: [04] Proposal Sent (Make Wellness volume)

---

## Next Steps

1. Fix HubSpot deals (revert to correct stages and names)
2. Rename local folder from closed-lost to customer folder
3. Create win-back subfolder structure
4. Move RATE-1903 materials to win-back subfolder
5. Update documentation to clarify customer vs lost volume

---

*Correction Date: 2025-10-10 12:06 PM*
*Issue: Misunderstood BoxiiShip AF as closed customer vs active customer with lost volume*
