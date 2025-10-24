# Deal Folder Structure Template
**Standardized Organization for All FirstMile Deals**

---

## Purpose

This template ensures every deal folder maintains consistent structure, complete documentation, and systematic analysis workflows across all 10 pipeline stages.

---

## Standard Folder Structure

```
[##-STAGE]_Company_Name/
├── CLAUDE.md                                    # AI context & deal-specific instructions
├── Customer_Relationship_Documentation.md       # Complete relationship history
├── README.md                                    # Deal overview & quick reference
├── PLD_Analysis/                               # Shipping data analysis
│   ├── raw_data/
│   │   ├── customer_pld_export.csv
│   │   ├── invoice_data.xlsx
│   │   └── carrier_invoices.pdf
│   ├── scripts/
│   │   ├── pld_analysis.py
│   │   ├── apply_firstmile_rates.py
│   │   ├── create_pricing_matrix.py
│   │   ├── revenue_calculator.py
│   │   └── invoice_audit_builder.py
│   ├── outputs/
│   │   ├── shipping_profile_report.xlsx
│   │   ├── analysis_summary.md
│   │   └── pld_discovery_report.md
│   └── README.md                               # Analysis methodology
├── Rate_Cards/                                 # Pricing documents
│   ├── current_rates_extracted.xlsx
│   ├── firstmile_pricing_matrix.xlsx
│   ├── savings_comparison.xlsx
│   └── tier_tool_output.xlsx
├── Proposals/                                  # Customer-facing deliverables
│   ├── proposal_v1.xlsx
│   ├── proposal_v2_revised.xlsx
│   ├── executive_summary.pdf
│   └── presentation_deck.pptx
├── Communications/                             # Email & meeting records
│   ├── EMAIL_TO_[CONTACT]_[SUBJECT].md
│   ├── MEETING_NOTES_[DATE]_[TOPIC].md
│   └── CALL_LOG_[DATE].md
├── Performance_Reports/                        # Post-win reports
│   ├── firstmile_performance_report.xlsx
│   └── sla_compliance_dashboard.xlsx
└── Reference/                                  # Supporting docs
    ├── competitive_analysis.md
    ├── network_coverage_analysis.md
    └── integration_requirements.md
```

---

## Required Files by Stage

### [00-LEAD] - Initial Contact
```
[00-LEAD]_Company_Name/
├── CLAUDE.md                    # Basic context
├── README.md                    # Company overview
└── Reference/
    └── lead_source_notes.md     # How we found them
```

**CLAUDE.md Template**:
```markdown
# [Company Name] - Lead

## Company Overview
- **Industry**: [e.g., DTC Apparel]
- **Estimated Volume**: [monthly packages]
- **Lead Source**: [BrandScout, referral, cold outreach]
- **Pain Points**: [known issues]

## Next Steps
- [ ] Research company website and shipping indicators
- [ ] Identify decision maker
- [ ] Schedule discovery call
```

### [01-DISCOVERY-SCHEDULED] - Meeting Booked
```
[01-DISCOVERY-SCHEDULED]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── Communications/
│   └── EMAIL_TO_[CONTACT]_DISCOVERY_CONFIRMATION.md
└── Reference/
    ├── discovery_agenda.md
    └── company_research.md
```

**Discovery Agenda Template**:
```markdown
# Discovery Call Agenda - [Company Name]

## Objectives
1. Understand current shipping operations
2. Identify pain points and opportunities
3. Qualify volume and fit for FirstMile
4. Secure PLD data for analysis

## Questions
### Volume & Profile
- Monthly package volume?
- Average weight and dimensions?
- Peak season patterns?

### Current Operations
- Current carriers and services?
- Average cost per package?
- Key pain points?

### Geography
- Warehouse locations?
- Top destination states/zones?
- International shipping?

### Decision Process
- Who's involved in carrier decisions?
- Current contract terms?
- Timeline for evaluation?

## Next Steps
- Request 3 months PLD data
- Schedule rate review call
- Timeline for proposal
```

### [02-DISCOVERY-COMPLETE] - Requirements Gathered
```
[02-DISCOVERY-COMPLETE]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── Communications/
│   ├── MEETING_NOTES_[DATE]_DISCOVERY.md
│   └── EMAIL_TO_[CONTACT]_DATA_REQUEST.md
└── Reference/
    ├── requirements_doc.md
    └── volume_assumptions.md
```

**Requirements Doc Template**:
```markdown
# Requirements Document - [Company Name]

## Customer Profile
- **Volume**: [packages/month]
- **Weight Profile**: [distribution]
- **Service Levels**: [current carriers/services]
- **Geography**: [warehouse → destinations]

## Pain Points
1. [Primary pain point with quantification]
2. [Secondary pain point]
3. [Additional concerns]

## Success Criteria
- Cost savings target: [%]
- Transit time improvement: [days]
- Integration requirements: [API, platform]
- Go-live timeline: [date]

## Data Requested
- [ ] 3 months PLD export
- [ ] Current rate card
- [ ] Invoice samples
- [ ] Volume projections

## Next Steps
- Data received by: [date]
- Rate creation target: [date]
- Proposal presentation: [date]
```

### [03-RATE-CREATION] - Pricing in Progress
```
[03-RATE-CREATION]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── PLD_Analysis/                    # Full analysis suite
├── Rate_Cards/                      # Pricing matrices
├── Communications/
│   └── EMAIL_TO_[CONTACT]_DATA_FOLLOWUP.md
└── Reference/
    ├── jira_ticket_reference.md     # JIRA RATE-#### link
    └── competitive_analysis.md
```

**JIRA Reference Template**:
```markdown
# JIRA Ticket Reference

**Ticket**: RATE-1897
**Status**: Peer Review
**Assigned**: Sales/Pricing Team
**Created**: Oct 3, 2025
**Target Completion**: Oct 7, 2025

## Data Provided
- [x] PLD export (3 months)
- [x] Current rate card
- [x] Volume assumptions
- [x] Service level requirements

## Analysis Complete
- [x] Weight distribution analysis
- [x] Zone analysis
- [x] Geographic coverage review
- [x] Savings calculation

## Blockers
- [ ] None

## Notes
Peer review in progress. Expected completion EOD Fri or Mon/Tue.
```

### [04-PROPOSAL-SENT] - Rates Delivered
```
[04-PROPOSAL-SENT]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── PLD_Analysis/
├── Rate_Cards/
├── Proposals/
│   ├── proposal_v1.xlsx
│   └── executive_summary.pdf
├── Communications/
│   ├── EMAIL_TO_[CONTACT]_PROPOSAL_DELIVERY.md
│   ├── EMAIL_TO_[CONTACT]_FOLLOWUP_DAY7.md
│   └── EMAIL_TO_[CONTACT]_FOLLOWUP_DAY14.md
└── Reference/
    └── objection_handling.md
```

**Objection Handling Template**:
```markdown
# Objection Handling - [Company Name]

## Anticipated Objections

### Price Concerns
**Objection**: "Rates seem higher than current carrier"
**Response**:
- Highlight all-in pricing (no accessorials)
- Show zone-skipping savings on cross-country
- Calculate total landed cost comparison

### Service Level Concerns
**Objection**: "Can you match 2-day to all zones?"
**Response**:
- Show SLA performance data (95% on-time)
- Highlight Select Network capabilities
- Offer pilot program

### Integration Concerns
**Objection**: "Integration seems complex"
**Response**:
- Single API vs multiple carriers
- 48-hour integration timeline
- Reference similar implementations

## Competitive Positioning
- vs UPS: 40% cost savings, similar transit
- vs USPS: Better tracking, comparable pricing
- vs Regional: National coverage + metro speed
```

### [05-SETUP-DOCS-SENT] - Verbal Commitment
```
[05-SETUP-DOCS-SENT]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── PLD_Analysis/
├── Rate_Cards/
├── Proposals/
├── Communications/
│   ├── EMAIL_TO_[CONTACT]_VERBAL_COMMIT.md
│   └── EMAIL_TO_[CONTACT]_SETUP_DOCS.md
└── Reference/
    ├── contract_terms.md
    └── implementation_plan.md
```

**Implementation Plan Template**:
```markdown
# Implementation Plan - [Company Name]

## Timeline
- **Contract Signed**: [target date]
- **API Integration**: [date range]
- **Testing Phase**: [date range]
- **Go-Live**: [target date]

## Integration Checklist
- [ ] API credentials issued
- [ ] Developer documentation shared
- [ ] Test environment configured
- [ ] First test shipment created
- [ ] Production credentials issued
- [ ] Monitoring dashboards configured

## Key Contacts
- **FirstMile Onboarding**: [name, email]
- **Customer Technical**: [name, email]
- **Customer Operations**: [name, email]

## Success Metrics
- Integration complete: <2 weeks
- First 100 shipments: 95% success rate
- SLA compliance: >90% in first month
```

### [06-IMPLEMENTATION] - Onboarding Active
```
[06-IMPLEMENTATION]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── PLD_Analysis/
├── Rate_Cards/
├── Proposals/
├── Communications/
│   └── EMAIL_TO_[CONTACT]_IMPLEMENTATION_UPDATE.md
└── Reference/
    ├── implementation_plan.md
    ├── integration_checklist.md
    └── test_results.md
```

### [07-CLOSED-WON] - Active Customer
```
[07-CLOSED-WON]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── PLD_Analysis/
├── Rate_Cards/
├── Proposals/
├── Performance_Reports/
│   ├── firstmile_performance_report.xlsx
│   └── monthly_sla_dashboard.xlsx
├── Communications/
│   └── EMAIL_TO_CS_HANDOFF.md
└── Reference/
    ├── account_summary.md
    └── expansion_opportunities.md
```

**Account Summary Template**:
```markdown
# Account Summary - [Company Name]

## Deal Details
- **Closed Date**: [date]
- **ARR**: $[value]
- **MRR**: $[value]
- **Contract Term**: [length]

## Performance Baseline
- **Projected Volume**: [pkgs/month]
- **Projected Revenue**: $[monthly]
- **Target SLA**: [%]
- **Key Services**: [list]

## Customer Success Handoff
- **CS Owner**: [name]
- **Onboarding Status**: Complete
- **First Month Goals**: [list]
- **Upsell Opportunities**: [list]

## Lessons Learned
### What Worked
- [Key success factor 1]
- [Key success factor 2]

### What Could Improve
- [Area for improvement 1]
- [Area for improvement 2]
```

### [08-CLOSED-LOST] - Lost Deal
```
[08-CLOSED-LOST]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── PLD_Analysis/
├── Rate_Cards/
├── Proposals/
└── Reference/
    ├── loss_analysis.md
    └── win_back_strategy.md
```

**Loss Analysis Template**:
```markdown
# Loss Analysis - [Company Name]

## Loss Details
- **Lost Date**: [date]
- **Stage Lost**: [stage]
- **Lost To**: [competitor or reason]
- **Deal Value**: $[ARR]

## Loss Reason
**Primary**: [main reason]
- [Specific details]

**Contributing Factors**:
1. [Factor 1]
2. [Factor 2]

## What We Could Have Done Differently
1. [Improvement 1]
2. [Improvement 2]

## Win-Back Potential
- **Likelihood**: High/Medium/Low
- **Timeline**: [when to re-engage]
- **Strategy**: [approach]

## Lessons for Future Deals
1. [Learning 1]
2. [Learning 2]
```

### [09-WIN-BACK] - Re-engagement
```
[09-WIN-BACK]_Company_Name/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md
├── README.md
├── Reference/
│   ├── original_loss_analysis.md
│   ├── market_changes.md
│   └── new_value_proposition.md
└── Communications/
    └── EMAIL_TO_[CONTACT]_REENGAGEMENT.md
```

**Re-engagement Strategy Template**:
```markdown
# Win-Back Strategy - [Company Name]

## Context
- **Original Loss Date**: [date]
- **Loss Reason**: [reason]
- **Time Since Loss**: [months]

## What's Changed
### Market Conditions
- [Change 1]
- [Change 2]

### FirstMile Capabilities
- [New capability 1]
- [New capability 2]

### Customer Situation (if known)
- [Insight 1]
- [Insight 2]

## Re-engagement Approach
**Angle**: [primary message]
**Proof Points**:
1. [Evidence 1]
2. [Evidence 2]

**Ask**: [specific next step]

## Timeline
- **First Outreach**: [date]
- **Follow-up 1**: [date +7d]
- **Follow-up 2**: [date +14d]
- **Decision Point**: [date +30d]
```

---

## Universal File Templates

### CLAUDE.md (All Stages)
```markdown
# [Company Name] - [Current Stage]

## Deal Context
- **Stage**: [##-STAGE-NAME]
- **Amount**: $[ARR]
- **Owner**: Brett Walker
- **HubSpot Deal ID**: [ID]
- **Created**: [date]
- **Last Updated**: [date]

## Company Profile
- **Industry**: [vertical]
- **Volume**: [monthly packages]
- **Key Contact**: [name, title, email]
- **Decision Maker**: [name, title]

## Current Status
[One-sentence status update]

## Next Actions
- [ ] [Action 1 with owner and date]
- [ ] [Action 2 with owner and date]
- [ ] [Action 3 with owner and date]

## Blockers
- [Blocker 1 with mitigation]
- [None]

## Key Files
- PLD Analysis: [path]
- Rate Card: [path]
- Proposal: [path]

## Notes
[Any important context for AI assistant]
```

### Customer_Relationship_Documentation.md (All Stages)
```markdown
# Customer Relationship Documentation - [Company Name]

## Overview
- **Company**: [Full legal name]
- **Industry**: [Vertical]
- **Website**: [URL]
- **HubSpot Contact ID**: [ID]
- **HubSpot Deal ID**: [ID]

## Key Stakeholders
### Primary Contact
- **Name**: [Full name]
- **Title**: [Role]
- **Email**: [Email]
- **Phone**: [Phone]
- **Best Contact Method**: [Email/Phone/Slack]

### Decision Makers
1. **[Name]** - [Title]
   - Role in decision: [Influence level]
   - Key concerns: [List]

### Technical Contacts
1. **[Name]** - [Title]
   - Responsibilities: [List]

## Relationship Timeline

### [Date] - Initial Contact
**Channel**: [Email/Call/Referral]
**Summary**: [What happened]
**Next Step**: [What was agreed]

### [Date] - Discovery Call
**Attendees**: [List]
**Key Takeaways**:
- [Point 1]
- [Point 2]
**Decisions Made**: [List]
**Action Items**:
- [ ] [Item 1]
- [ ] [Item 2]

### [Date] - [Event/Interaction]
**Summary**: [Details]
**Impact**: [How this moved the deal]

## Communication Preferences
- **Preferred Channel**: [Email/Phone/Text]
- **Best Times**: [When to reach out]
- **Response Pattern**: [How quickly they typically respond]
- **Communication Style**: [Formal/Casual/Data-driven]

## Pain Points & Motivations
### Current Challenges
1. **[Challenge 1]**
   - Impact: [Quantified if possible]
   - Urgency: [High/Medium/Low]

### Business Drivers
1. **[Driver 1]**
   - Why it matters: [Context]

## Competitive Landscape
- **Current Carriers**: [List]
- **Competitors Evaluated**: [List]
- **Key Differentiators**: [What matters to them]

## Deal Risks & Mitigations
### Risk 1: [Description]
- **Likelihood**: [High/Medium/Low]
- **Impact**: [High/Medium/Low]
- **Mitigation**: [Strategy]

## Notes & Insights
[Ongoing observations, patterns, important context]

## Archive
[Older interactions moved here for reference]
```

### README.md (Deal Overview)
```markdown
# [Company Name] Deal Overview

## Quick Stats
- **Stage**: [##-STAGE]
- **Value**: $[ARR]
- **Monthly Volume**: [packages]
- **Primary Contact**: [Name] ([email])
- **Status**: [One-line status]

## Deal Summary
[2-3 sentence deal summary]

## Key Files
- [Customer Relationship Doc](Customer_Relationship_Documentation.md)
- [PLD Analysis](PLD_Analysis/outputs/analysis_summary.md)
- [Rate Card](Rate_Cards/firstmile_pricing_matrix.xlsx)
- [Proposal](Proposals/proposal_v1.xlsx)

## Recent Activity
### [Date]
- [Activity description]

### [Date]
- [Activity description]

## Next Steps
1. [Step 1] - Due: [Date] - Owner: [Name]
2. [Step 2] - Due: [Date] - Owner: [Name]
```

---

## Folder Naming Conventions

### Format
```
[##-STAGE-NAME]_Company_Name
```

### Rules
1. **Stage Prefix**: Two-digit number + stage name
2. **Separator**: Single underscore
3. **Company Name**:
   - No spaces (use underscores)
   - No special characters
   - Title case preferred
4. **Examples**:
   - `[01-DISCOVERY-SCHEDULED]_Acme_Corp`
   - `[03-RATE-CREATION]_Stackd_Logistics`
   - `[07-CLOSED-WON]_JM_Group_NY`

### Renaming for Stage Movement
```bash
# From discovery to rate creation
mv "[01-DISCOVERY-SCHEDULED]_Acme_Corp" "[02-DISCOVERY-COMPLETE]_Acme_Corp"

# From proposal to setup
mv "[04-PROPOSAL-SENT]_Acme_Corp" "[05-SETUP-DOCS-SENT]_Acme_Corp"
```

---

## Best Practices

### File Naming
- **Dates**: YYYYMMDD format (e.g., 20251007)
- **Descriptive**: Include topic in filename
- **Version Control**: Use v1, v2, v3 suffixes
- **Email Templates**: `EMAIL_TO_[RECIPIENT]_[SUBJECT].md`
- **Meeting Notes**: `MEETING_NOTES_[DATE]_[TOPIC].md`

### Documentation Standards
1. **Update CLAUDE.md** after every major action
2. **Log all communications** in Customer Relationship Doc
3. **Version control proposals** (v1, v2, v3)
4. **Archive old files** but keep for reference

### Organization Tips
1. Keep active files in root of deal folder
2. Move completed analysis to appropriate subfolder
3. Archive superseded proposals with date suffix
4. Use README.md as navigation hub

---

## Automation Integration

### Folder Movement Triggers
When you move a folder (e.g., `[01]_Company` → `[02]_Company`):
1. N8N detects file system change
2. Updates `_PIPELINE_TRACKER.csv`
3. Updates HubSpot deal stage
4. Triggers email sequences
5. Creates follow-up tasks

### Template Auto-Deployment
When deal reaches certain stages:
- [01-DISCOVERY-SCHEDULED]: Discovery agenda template
- [02-DISCOVERY-COMPLETE]: Requirements doc template
- [03-RATE-CREATION]: Analysis script templates
- [04-PROPOSAL-SENT]: Follow-up email templates

### Daily Sync Integration
- 9AM: Scan all deal folders for priority actions
- NOON: Check for new files and updates
- EOD: Verify documentation completeness

---

## Quick Setup Commands

### Create New Deal Folder
```bash
# Set variables
STAGE="01-DISCOVERY-SCHEDULED"
COMPANY="Acme_Corp"

# Create folder structure
mkdir -p "[${STAGE}]_${COMPANY}"/{PLD_Analysis/{raw_data,scripts,outputs},Rate_Cards,Proposals,Communications,Performance_Reports,Reference}

# Copy templates
cp DEAL_FOLDER_TEMPLATE/CLAUDE_TEMPLATE.md "[${STAGE}]_${COMPANY}/CLAUDE.md"
cp DEAL_FOLDER_TEMPLATE/CUSTOMER_RELATIONSHIP_TEMPLATE.md "[${STAGE}]_${COMPANY}/Customer_Relationship_Documentation.md"
cp DEAL_FOLDER_TEMPLATE/README_TEMPLATE.md "[${STAGE}]_${COMPANY}/README.md"

# Initialize in HubSpot
qm hubspot convert-to-deal --contact-id [ID] --deal-name "${COMPANY} - Xparcel" --stage "${STAGE}"
```

### Copy Analysis Scripts
```bash
COMPANY="Acme_Corp"
cp Analysis_Templates/*.py "[03-RATE-CREATION]_${COMPANY}/PLD_Analysis/scripts/"
```

---

## Template Files Location

All template files stored in:
```
C:\Users\BrettWalker\FirstMile_Deals\DEAL_FOLDER_TEMPLATES\
├── CLAUDE_TEMPLATE.md
├── CUSTOMER_RELATIONSHIP_TEMPLATE.md
├── README_TEMPLATE.md
├── DISCOVERY_AGENDA_TEMPLATE.md
├── REQUIREMENTS_DOC_TEMPLATE.md
├── JIRA_REFERENCE_TEMPLATE.md
├── OBJECTION_HANDLING_TEMPLATE.md
├── IMPLEMENTATION_PLAN_TEMPLATE.md
└── LOSS_ANALYSIS_TEMPLATE.md
```

---

**Last Updated**: October 7, 2025
**System**: Nebuchadnezzar v2.0
**Purpose**: Ensure consistent, complete deal management across all stages
