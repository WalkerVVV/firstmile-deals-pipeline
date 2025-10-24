# FirstMile Pipeline Blueprint
*Complete Integration Guide: Folder Structure → HubSpot → n8n Automation*

**Last Updated:** September 24, 2025  
**Owner:** Brett Walker  
**Pipeline ID:** `8bd9336b-4767-4e67-9fe2-35dfcad7c8be`  
**Owner ID:** `699257003`

---

## FOLDER STRUCTURE ARCHITECTURE

### Physical Directory Structure:
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
├── [09-WIN-BACK]_CompanyName
├── _ARCHIVE\
├── HubSpot\
│   ├── HUBSPOT_MCP_CHEATSHEET.md
│   ├── CLAUDE.md
│   └── shipping_intel_companion_template.xlsx
├── BULK_RATE_PROCESSING\
└── XPARCEL_NATIONAL_SELECT\
```

### Current Active Deals Examples:
- `[01-DISCOVERY-SCHEDULED]_Josh's_Frogs`
- `[01-DISCOVERY-SCHEDULED]_Sparkle_In_Pink`
- `[04-PROPOSAL-SENT]_Caputron`
- `[04-PROPOSAL-SENT]_ODW_Logistics`
- `[07-CLOSED-WON]_BoxiiShip`
- `[09-WIN-BACK]_Brand_Bolt`

---

## HUBSPOT DEAL STAGES (Synchronized)

### Pipeline Configuration
- **Pipeline ID:** `8bd9336b-4767-4e67-9fe2-35dfcad7c8be`
- **Owner ID:** `699257003` (Brett Walker)

### Stage Mapping Table
| Stage # | Folder Prefix | HubSpot Stage Name | Stage ID | Description |
|---------|---------------|-------------------|----------|-------------|
| 00-01 | LEAD | Lead | `08d9c411-5e1b-487b-8732-9c2bcbbd0307` | Initial contact identified |
| 02 | DISCOVERY-COMPLETE | Discovery | `d2a08d6f-cc04-4423-9215-594fe682e538` | Call completed, interest expressed |
| 03 | RATE-CREATION | Rate Creation | `e1c4321e-afb6-4b29-97d4-2b2425488535` | Rates being created via Jira |
| 04 | PROPOSAL-SENT | Proposal | `d607df25-2c6d-4a5d-9835-6ed1e4f4020a` | Rates emailed/presented |
| 05 | SETUP-DOCS-SENT | Setup Docs | `4e549d01-674b-4b31-8a90-91ec03122715` | Verbal commit, docs sent |
| 06 | IMPLEMENTATION | Implementation | TBD | Operational setup phase |
| 07 | CLOSED-WON | Closed Won | `3fd46d94-78b4-452b-8704-62a338a210fb` | Customer started shipping |
| 08 | CLOSED-LOST | Closed Lost | `02d8a1d7-d0b3-41d9-adc6-44ab768a61b8` | Deal lost |
| 09 | WIN-BACK | Win-Back | TBD | Re-engagement with lost deals |

### Association IDs
```javascript
CONTACT→COMPANY: 279
LEAD→CONTACT: 608 (REQUIRED)
LEAD→COMPANY: 610
DEAL→COMPANY: 341
DEAL→CONTACT: 3
```

---

## N8N WORKFLOW AUTOMATION BLUEPRINT

### **Primary Workflow:** `FirstMile_HubSpot_Pipeline_Automation.json`

#### Workflow Architecture:
```
HubSpot Deal Trigger
        ↓
Deal Stage = Qualified?
        ↓
Get Contact & Company Details
        ↓
Calculate FirstMile Value
        ↓
Send Personalized Email
        ↓
Update Deal Properties
        ↓
Log to Pipeline Tracker
```

#### Node Structure:

**1. Trigger Node:** `HubSpot Deal Changes`
- **Events:** `deal.creation`, `deal.propertyChange`
- **Credentials:** HubSpot OAuth2

**2. Logic Node:** `If Deal Stage = Qualified`
- **Condition:** `dealstage == "qualifiedtobuy"`

**3. Data Nodes:**
- `Get Contact Details` - Pulls contact information
- `Get Company Details` - Pulls company data

**4. Processing Node:** `Calculate FirstMile Value`
```javascript
// FirstMile Pricing Logic
if (monthlyVolume > 75000) {
  estimatedSavings = monthlyVolume * 0.45; // 45% savings
} else if (monthlyVolume > 20000) {
  estimatedSavings = monthlyVolume * 0.40; // 40% savings  
} else {
  estimatedSavings = monthlyVolume * 0.35; // 35% savings
}
```

**5. Action Nodes:**
- `Send Personalized Email` - Microsoft Outlook integration
- `Update Deal Properties` - Sets automation flags
- `Log to Pipeline Tracker` - CSV tracking

### **Secondary Workflow:** `Daily_9AM_Pipeline_Power_Hour.json`
- **Schedule:** Daily at 9:00 AM
- **Function:** Pipeline health check and follow-up automation

---

## INTEGRATED WORKFLOW PROCESS

### Stage Movement Logic:
1. **Manual Folder Movement** → **HubSpot Stage Update**
2. **HubSpot Stage Change** → **n8n Automation Trigger**
3. **n8n Automation** executes:
   - Personalized email sequences
   - Deal property updates
   - CSV logging and tracking
   - Follow-up scheduling

### Automation Triggers by Stage:

| Stage | Automation Type | Timing | Action |
|-------|-----------------|--------|---------|
| Discovery Scheduled | Reminder | Custom | Stale deal alert |
| Discovery Complete | Follow-up | 30 days | Re-engagement email |
| Rate Creation | Follow-up | 2 weeks | Status check |
| Proposal Sent | Follow-up | 30 days | Decision follow-up |
| Setup Docs Sent | Follow-up | 2 weeks | Implementation check |
| Implementation | Follow-up | 30 days | Go-live status |
| Closed Lost | Custom | Manual date | Win-back opportunity |
| Win-Back | Check-in | Monthly | Re-engagement |

---

## DATA TRACKING & MONITORING

### Core Tracking Files:
- **`_PIPELINE_TRACKER.csv`** - Main deal progression tracking
- **`_DAILY_LOG.md`** - Daily automation activity log
- **`AUTOMATION_MONITOR_LOCAL.html`** - Real-time dashboard
- **`FOLLOW_UP_REMINDERS.txt`** - Action items and due dates

### Key Metrics Tracked:
- Deal stage progression timestamps
- Estimated savings calculations
- Email touchpoint history
- Follow-up due dates and completion
- Win/loss reasons and analysis
- Pipeline velocity metrics
- Automation success rates

### Required Fields by Stage:

**[02-DISCOVERY-COMPLETE]:**
- Address
- Lead Source
- Type of Business (FM Product)
- Current Carrier/s (Multi-select)
- Average Monthly Shipments

**[03-RATE-CREATION]:**
- Jira Ticket #
- Amount

**[07-CLOSED-WON]:**
- Won Reason

**[08-CLOSED-LOST]:**
- Lost Reason (from predefined list)
- Next Follow-Up Date (Optional)

---

## QUICK COMMAND REFERENCE

### HubSpot MCP Commands:
```bash
qm hubspot lead      # Single BrandScout → Lead creation
qm hubspot bulk      # Multiple leads batch processing  
qm hubspot deal      # Convert lead to deal
qm hubspot note      # Add engagement note to records
qm hubspot pipeline  # Move deals through stages
qm hubspot search    # Find existing leads/deals
```

### N8N Management:
- **Access URL:** `http://localhost:5678`
- **Import Workflow:** Upload JSON files from `C:\Users\BrettWalker\n8n-Workflows\`
- **Test Mode:** Use "Execute Workflow" button
- **Debug:** Click nodes to view input/output data
- **Emergency Stop:** Toggle workflow OFF

### Data Formats:

**BrandScout Single Lead:**
```json
{
  "company": {
    "name": "Acme Corp",
    "domain": "acme.com",
    "description": "Leading widget manufacturer",
    "annual_revenue": "10000000",
    "employee_count": "45",
    "industry": "Ecommerce"
  },
  "contact": {
    "email": "ops@acme.com",
    "firstname": "Jordan",
    "lastname": "Blake",
    "jobtitle": "Director of Ops",
    "phone": "+1 801-555-0200"
  },
  "shipping_intel": {
    "ships_physical": true,
    "product_types": "widgets",
    "estimated_volume": "12000",
    "current_carriers": "UPS; USPS"
  }
}
```

---

## CRITICAL SUCCESS FACTORS

### Deduplication Strategy:
1. Search company by domain
2. Search contact by email  
3. Create only if not found
4. Associate existing records if found

### Required Rules:
- Lead→Contact association (608) is MANDATORY
- Use Stage IDs not labels for automation
- Domain = lowercase, no http://
- Email = lowercase
- All API commands return raw JSON only

### API Call Efficiency:
- **Single Lead Creation:** 4-5 calls
- **Bulk Lead Creation (N leads):** 6-8 calls total
- **Deal Creation:** 1 call with inline associations
- **Note Creation:** 1 call (legacy engagement API)
- **Pipeline Update:** 1 call (batch up to 100)

---

## TROUBLESHOOTING & MAINTENANCE

### Common Issues:
1. **Folder movement not triggering HubSpot update**
   - Check file system monitoring
   - Verify API credentials

2. **n8n workflow failures**
   - Check execution history: Settings → Execution History
   - Verify OAuth2 tokens are valid
   - Test individual nodes

3. **Missing deal associations**
   - Ensure Lead→Contact (608) association exists
   - Verify company and contact IDs are valid

### Maintenance Schedule:
- **Weekly:** Review automation logs
- **Monthly:** Update workflow credentials
- **Quarterly:** Audit folder structure alignment
- **Annually:** Review and optimize automation rules

---

## FUTURE ENHANCEMENTS

### Planned Automations:
1. **Win-Back Intelligence** - Automated rate comparison for lost deals
2. **Competitive Analysis** - Auto-populate competitor research
3. **Pipeline Forecasting** - Predictive close date modeling
4. **Customer Success Handoff** - Automated transition for won deals

### Integration Roadmap:
- Jira ticket automation for rate creation
- Slack notifications for stage changes
- Calendar booking for discovery calls
- Document generation for proposals

---

**This blueprint transforms manual pipeline management into an automated revenue generation machine. The system integrates physical folder structure, HubSpot deal stages, and n8n automation workflows into a unified sales process.**