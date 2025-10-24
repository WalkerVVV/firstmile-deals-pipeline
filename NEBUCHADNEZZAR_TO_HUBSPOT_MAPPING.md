# Nebuchadnezzar to HubSpot Pipeline Mapping
*Keep Brett's system AS-IS - This is a translation guide*

## NO CHANGES TO YOUR FOLDERS - This is how they map to HubSpot:

| Your Nebuchadnezzar Folders | Maps to Brock's HubSpot Stage | Notes |
|----------------------------|-------------------------------|-------|
| [00-LEAD] | *(Create as Lead in HubSpot)* | Keep using this |
| [01-DISCOVERY-SCHEDULED] | DISCOVERY SCHEDULED | Already aligned ✓ |
| [02-DISCOVERY-COMPLETE] | DISCOVERY COMPLETE | Already aligned ✓ |
| [03-RATE-CREATION] | RATE CREATION | Already aligned ✓ |
| [04-PROPOSAL-SENT] | PROPOSAL SENT | Already aligned ✓ |
| [05-NEGOTIATION] | PROPOSAL SENT *(same stage)* | Keep your folder, map to Proposal |
| [06-CLOSED-WON] | SETUP DOCS SENT | Your stage = their 80% |
| [07-ACTIVE-SHIPPING] | CLOSED WON - STARTED SHIPPING | Your active = their won |
| [08-CLOSED-LOST] | CLOSED LOST | Already aligned ✓ |
| [WIN-BACK] | *(Custom field in HubSpot)* | Keep using this |

## What Brock Has That You Don't Need Folders For:
- **IMPLEMENTATION** - Track in HubSpot only if needed

## Your Current Pipeline Stays Exactly As-Is:
```
C:\Users\BrettWalker\FirstMile_Deals\
├── [00-LEAD]_Pendulums
├── [02-DISCOVERY-COMPLETE]_Team_Shipper  
├── [03-RATE-CREATION]_* (10 deals)
├── [04-PROPOSAL-SENT]_* (2 deals)
├── [05-NEGOTIATION]_JM_Group_NY
├── [07-ACTIVE-SHIPPING]_* (2 deals)
├── [08-CLOSED-LOST]_The_Only_Bean
└── [WIN-BACK]_Boxio
```

## HubSpot Fields to Add (No Folder Changes):

### For [01-DISCOVERY-SCHEDULED]:
- Deal Type (Existing/New)
- Brands (FM, SN)

### For [02-DISCOVERY-COMPLETE]:
- Type of Business (FM Product)
- Current Carrier/s
- Average Monthly Shipments

### For [03-RATE-CREATION]:
- Jira Ticket #
- Amount

### For [08-CLOSED-LOST]:
- Lost Reason (11 options)
- Next Follow-Up Date

## Automation Timers to Implement:
- **Your [03-RATE-CREATION]**: 2-week reminder (10 deals overdue!)
- **Your [02-DISCOVERY-COMPLETE]**: 30-day reminder
- **Your [04-PROPOSAL-SENT]**: 30-day reminder
- **Your [05-NEGOTIATION]**: Treat as Proposal Sent (30-day)

## NO CHANGES NEEDED TO:
- Your folder structure
- Your file names
- Your automation paths
- Your Nebuchadnezzar system
- AUTOMATION_MONITOR_LOCAL.html
- _PIPELINE_TRACKER.csv

## Just tell Brock:
"We're keeping our folder structure as-is. Here's how our stages map to yours..."
