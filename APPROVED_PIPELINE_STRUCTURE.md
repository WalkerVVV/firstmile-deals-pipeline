# FirstMile Pipeline Workflow - APPROVED VERSION
*Last Updated: 2025-01-27*

## Pipeline Stages

### [00-LEAD]
- **Description:** Initial contact identified
- **Movement:** Manual entry
- **Required Fields:** None
- **Automation:** None

### [01-DISCOVERY-SCHEDULED]
- **Description:** Discovery call scheduled with prospect
- **Movement:** Manual
- **Required Fields:**
  - Deal Type (Existing or New Business)
  - Brands (FM, SN)
  - Lead Source (Optional)
- **Automation:** 
  - Sync contact lead source
  - Stale deal reminder

### [02-DISCOVERY-COMPLETE]
- **Description:** Call completed, info gathered, interest expressed
- **Movement:** Manual
- **Required Fields:**
  - Address
  - Lead Source
  - Type of Business (FM Product):
    - Xparcel (Domestic)
    - UPS
    - FedEx
    - International
    - LTL/FTL
    - Other (Flats, BPM, etc.)
  - Current Carrier/s (Multi-select):
    - USPS
    - UPS
    - FedEx
    - DHL eCommerce
    - OnTrac
    - Amazon Shipping
    - ePost Global
    - OSM Worldwide
    - RR Donnelley Logistics
    - EasyPost
    - Other
  - Average Monthly Shipments
- **Automation:** 30-day follow-up reminder

### [03-RATE-CREATION]
- **Description:** Rates being created or submitted via Jira
- **Movement:** Manual
- **Required Fields:**
  - Jira Ticket #
  - Amount
- **Automation:** 2-week follow-up reminder

### [04-PROPOSAL-SENT]
- **Description:** Rates emailed/presented for discussion
- **Movement:** Manual
- **Required Fields:** None
- **Automation:** 30-day follow-up reminder

### [05-SETUP-DOCS-SENT]
- **Description:** Verbal commit received, setup docs sent
- **Movement:** Manual
- **Required Fields:** None
- **Automation:** 2-week follow-up reminder

### [06-IMPLEMENTATION]
- **Description:** Operational setup, transition to new accounts team
- **Movement:** Manual
- **Required Fields:** None
- **Automation:** 30-day follow-up reminder

### [07-CLOSED-WON]
- **Description:** Customer started shipping
- **Movement:** Manual (marked Won)
- **Required Fields:** 
  - Won Reason
- **Post-Close:** Move to Active Customer tracking

### [08-CLOSED-LOST]
- **Description:** Deal lost
- **Movement:** Manual (marked Lost)
- **Required Fields:**
  - Lost Reason:
    - Lost to Competitor
    - No Decision / Non-Responsive
    - Rates Not Competitive Enough
    - Sticking with Current Carrier(s)
    - Operational Complexity / Tech Limitations
    - Poor Fit for Shipping Profile
    - Service Level Mismatch
    - Unrealistic Expectations
    - Delayed Decision / Project Paused
    - Moved to Fulfillment Provider (3PL)
    - Chose Marketplace Fulfillment (FBA, Walmart, etc.)
    - Other
  - Next Follow-Up Date (Optional)
- **Automation:** Follow-up reminder on specified date

### [09-WIN-BACK]
- **Description:** Re-engagement with lost deals
- **Movement:** Manual from Closed-Lost
- **Required Fields:** None
- **Automation:** Monthly check-in reminder

## Automation Rules

### Time-Based Reminders:
- **2 Weeks:** Rate Creation, Setup Docs Sent
- **30 Days:** Discovery Complete, Proposal Sent, Implementation
- **Custom:** Lost deals with follow-up dates
- **Monthly:** Win-Back opportunities

### Folder Structure:
```
C:\Users\BrettWalker\FirstMile_Deals\
├── [00-LEAD]_CompanyName
├── [01-DISCOVERY-SCHEDULED]_CompanyName
├── [02-DISCOVERY-COMPLETE]_CompanyName
├── [03-RATE-CREATION]_CompanyName
├── [04-PROPOSAL-SENT]_CompanyName
├── [05-SETUP-DOCS-SENT]_CompanyName
├── [06-IMPLEMENTATION]_CompanyName
├── [07-CLOSED-WON]_CompanyName
├── [08-CLOSED-LOST]_CompanyName
└── [09-WIN-BACK]_CompanyName
```

### N8N Automation Triggers:
- Folder movement detection
- Auto-update _PIPELINE_TRACKER.csv
- Deploy stage-appropriate templates
- Generate FOLLOW_UP_REMINDERS.txt
- Update AUTOMATION_MONITOR_LOCAL.html
