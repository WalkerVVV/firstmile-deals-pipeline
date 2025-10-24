# BoxiiShip AF Folder Reorganization Guide
**Date**: October 10, 2025, 12:06 PM
**Action Required**: Rename and reorganize folder structure

---

## Current Structure (WRONG)
```
C:\Users\BrettWalker\FirstMile_Deals\
└── [08-CLOSED-LOST]_BoxiiShip AF\
    └── (all files)
```

## Target Structure (CORRECT)
```
C:\Users\BrettWalker\FirstMile_Deals\
└── Customer-BoxiiShip_AF\
    ├── Customer_Profile.md
    ├── Active_Business\
    │   └── (ongoing customer materials)
    └── Win-Back_Make_Wellness_2025\
        ├── README.md
        ├── RATE-1903_Taylar_Response.md
        ├── Strategic_Analysis_For_Nate.md
        └── (all win-back campaign materials)
```

---

## Step-by-Step Instructions

### Option 1: PowerShell Commands

```powershell
# Navigate to FirstMile_Deals
cd "C:\Users\BrettWalker\FirstMile_Deals"

# Rename main folder
Rename-Item "[08-CLOSED-LOST]_BoxiiShip AF" "Customer-BoxiiShip_AF"

# Create win-back subfolder
New-Item -ItemType Directory -Path "Customer-BoxiiShip_AF\Win-Back_Make_Wellness_2025"

# Create README in win-back folder
@"
# Make Wellness Volume Win-Back Campaign 2025

**Win-Back Deal ID**: 45692064076
**Customer Deal ID**: 36466918934 (BoxiiShip AF - Active 3PL Customer)

## Campaign Overview

Target: Get Make Wellness volume back to BoxiiShip AF
Current Carrier: UPS (direct)
Target Flow: Make Wellness → BoxiiShip AF → FirstMile

## Campaign Status

- [x] RATE-1903 completed (October 9, 2025)
- [x] Peer review complete
- [ ] Strategic presentation to Nate
- [ ] Customer re-engagement
- [ ] Proposal and close

## Financial Impact

- Annual Value: \$7,200,000
- Customer Savings: \$52K-\$58K/week
- Rate Advantage: Up to 11% vs UPS

## Parent Customer

BoxiiShip American Fork is an ACTIVE FirstMile customer (3PL).
They lost their customer Make Wellness to UPS.
This campaign helps BoxiiShip win back their customer.

## Documentation

All Make Wellness win-back materials are in this subfolder.
General BoxiiShip customer materials are in parent folder.
"@ | Out-File -FilePath "Customer-BoxiiShip_AF\Win-Back_Make_Wellness_2025\README.md" -Encoding UTF8

Write-Host "Folder reorganization complete!"
```

### Option 2: File Explorer (Manual)

1. **Rename main folder**:
   - Right-click `[08-CLOSED-LOST]_BoxiiShip AF`
   - Select "Rename"
   - Change to: `Customer-BoxiiShip_AF`

2. **Create win-back subfolder**:
   - Open `Customer-BoxiiShip_AF`
   - Right-click → New → Folder
   - Name: `Win-Back_Make_Wellness_2025`

3. **Move win-back materials**:
   - Move RATE-1903_Taylar_Response.md to win-back subfolder
   - Move any Make Wellness specific analysis to win-back subfolder
   - Keep general BoxiiShip customer materials in main folder

4. **Create README**:
   - Right-click in win-back subfolder → New → Text Document
   - Name: `README.md`
   - Copy content from template above

---

## File Organization

### Keep in Main Customer Folder:
```
Customer-BoxiiShip_AF/
├── Customer_Profile.md (general BoxiiShip info)
├── Contract_Documents/
├── Performance_Reports/
├── Onboarding_Materials/
└── (other ongoing customer materials)
```

### Move to Win-Back Subfolder:
```
Customer-BoxiiShip_AF/Win-Back_Make_Wellness_2025/
├── README.md (campaign overview)
├── RATE-1903_Taylar_Response.md
├── Strategic_Analysis_For_Nate.md
├── Make_Wellness_Volume_Analysis.md
├── Competitive_Analysis_vs_UPS.md
└── Win_Back_Campaign_Plan.md
```

---

## Verification Checklist

After reorganization, verify:

- [ ] Main folder renamed to `Customer-BoxiiShip_AF`
- [ ] Win-back subfolder created: `Win-Back_Make_Wellness_2025`
- [ ] README.md exists in win-back subfolder
- [ ] RATE-1903 materials moved to win-back subfolder
- [ ] Customer materials organized in main folder
- [ ] No files left in old `[08-CLOSED-LOST]_BoxiiShip AF` folder

---

## HubSpot Deal Summary

After this reorganization, you'll have:

### Customer Deal (Active Business)
- **ID**: 36466918934
- **Name**: BoxiiShip American Fork - 3PL Customer
- **Stage**: [07] Started Shipping
- **Folder**: Customer-BoxiiShip_AF/

### Win-Back Deal (Make Wellness Volume)
- **ID**: 45692064076
- **Name**: BoxiiShip AF - Make Wellness Volume WIN-BACK 2025
- **Stage**: [04] Proposal Sent
- **Folder**: Customer-BoxiiShip_AF/Win-Back_Make_Wellness_2025/

---

## Key Principle

**Customer folders** contain:
- Main customer business (ongoing)
- Win-back subfolders for specific lost volumes/customers

**Pipeline stage folders** ([01-DISCOVERY], [04-PROPOSAL-SENT], etc.) contain:
- Net-new prospects and opportunities
- NOT existing customer expansion/win-back work

---

*Reorganization Guide Created: 2025-10-10 12:06 PM*
*Folder reorganization should take < 5 minutes*
