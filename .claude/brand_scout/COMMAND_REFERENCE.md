# Brand Scout v3.7 - Command Reference

**Complete command library for autonomous lead research and HubSpot integration**

---

## 🎯 Master Commands

### Full Automation (Recommended)

```
"Scout [BRAND NAME] with full automation:
1. Generate Brand Scout report
2. Create [00-LEAD]_[BRAND_NAME] folder
3. Generate Customer_Relationship_Documentation.md
4. Create HubSpot Contact, Company, and Lead
5. Associate all records
6. Add notes with key findings
7. Update pipeline tracker
8. Log to daily sync
9. Prepare for 9AM review"
```

**Time**: 30-40 minutes
**Output**: Complete deal folder + HubSpot triple-record + pipeline tracking

---

## 📊 Research Commands

### Standard Research

```
"Generate Brand Scout report for [BRAND NAME]"
"Scout this brand: https://example.com"
"Research [BRAND] and create lead intelligence"
```

**Time**: 25-35 minutes
**Output**: 9-section report in `.claude/brand_scout/output/`

### Quick Research (Time-Limited)

```
"Quick scout (15 min) for [BRAND] - focus on contacts"
"Fast research [BRAND] - shipping intelligence only"
"Quick brand profile for [BRAND]"
```

**Time**: 10-15 minutes
**Output**: Core sections only, medium confidence

### Emphasis Research

```
"Scout [BRAND] with emphasis on shipping intelligence"
"Research [BRAND] focusing on competitor analysis"
"Deep dive [BRAND] - contact discovery priority"
```

**Time**: 30-40 minutes
**Output**: Enhanced target sections, high detail

### Batch Processing

```
"Scout these brands: [BRAND1], [BRAND2], [BRAND3]"
"Generate reports for all brands in research_queue.txt"
"Batch research: Dr. Squatch, OLIPOP, Carbon38"
```

**Time**: 25-35 min per brand (parallel processing)
**Output**: Multiple reports, separate files

---

## 📁 Folder Management Commands

### Create Deal Folder Only

```
"Create [00-LEAD]_[BRAND_NAME] folder structure from Brand Scout report"
```

**Creates**:
- Deal folder with proper naming
- Customer_Relationship_Documentation.md
- README.md
- Reference/ subdirectories

### Copy Report to Folder

```
"Copy latest [BRAND] Brand Scout report to deal folder"
```

**Action**: Copies from `.claude/brand_scout/output/` to `[00-LEAD]_[BRAND]/`

### Generate Customer Relationship Doc

```
"Generate Customer_Relationship_Documentation.md for [BRAND] from Brand Scout report"
```

**Output**: Fully populated relationship tracking document

---

## 🔗 HubSpot Integration Commands

### Create Contact

```
"Create HubSpot contact for [PRIMARY CONTACT NAME] from [BRAND] Brand Scout report"
```

**Fields Populated**:
- First Name, Last Name
- Email, Phone
- Job Title
- LinkedIn URL
- Owner: Brett Walker

**Capture**: Contact ID for associations

### Create Company

```
"Create HubSpot company for [BRAND] from Brand Scout report"
```

**Fields Populated**:
- Company Name
- Domain, Website
- Address (City, State, ZIP)
- Industry: eCommerce
- Annual Revenue
- Owner: Brett Walker

**Capture**: Company ID for associations

### Create Lead

```
"Create HubSpot lead for [BRAND] - [PRIMARY CONTACT] from Brand Scout report"
```

**Fields Populated**:
- Lead Name: "[Company] – [Contact]"
- Lead Source: "Brand Scout Automation"
- Lead Status: "New"
- Priority: High/Medium/Low
- Owner: Brett Walker

**Capture**: Lead ID for associations

### Associate Records

```
"Associate HubSpot records for [BRAND]:
- Contact ID: [ID]
- Company ID: [ID]
- Lead ID: [ID]"
```

**Creates**:
- Contact → Company association
- Contact → Lead association
- Company → Lead association

### Add Notes to All Records

```
"Add Brand Scout summary notes to all [BRAND] HubSpot records"
```

**Note Content**:
- Research findings
- Key metrics
- Pain points
- Next actions

---

## 📊 Pipeline & Tracking Commands

### Update Pipeline Tracker

```
"Update _PIPELINE_TRACKER.csv with [BRAND] from Brand Scout report"
```

**Adds Row**: Company, Stage, Date, Owner, Contact, HubSpot IDs, Volume, Revenue

### Update Daily Log

```
"Log [BRAND] Brand Scout automation to _DAILY_LOG.md"
```

**Entry Format**: Date, action, outputs, findings, next steps

### Generate Follow-Up Reminders

```
"Create follow-up reminder for [BRAND] discovery call"
```

**Adds to**: `FOLLOW_UP_REMINDERS.txt` with date and action

---

## 🔍 Quality Control Commands

### Review Report Quality

```
"Review Brand Scout report for [BRAND] and verify data confidence"
```

**Checks**:
- Data confidence score
- Verified contacts count
- Mandatory fields present
- HubSpot section completeness

### Validate HubSpot Setup

```
"Validate HubSpot setup for [BRAND]:
- Contact: [ID]
- Company: [ID]
- Lead: [ID]"
```

**Verifies**:
- Records exist
- Associations correct
- Notes present
- Owner assigned

### Check Deal Folder Structure

```
"Verify [00-LEAD]_[BRAND] folder structure completeness"
```

**Validates**:
- Required files present
- Customer_Relationship_Documentation.md populated
- Brand Scout report copied
- README.md accurate

---

## 🚀 Daily Sync Commands

### 9AM Sync - Brand Scout Review

```
"Review overnight Brand Scout results and generate priority outreach list"
```

**Output**:
- List of new leads
- Tier A vs Tier B priority
- Recommended actions
- Quality check status

### Generate Discovery Email Templates

```
"Generate personalized discovery email for [BRAND] using Brand Scout insights"
```

**Includes**:
- Reference to shipping pain points
- Relevant value propositions
- Xparcel service recommendation
- Call to action

### Batch Outreach Preparation

```
"Prepare batch discovery outreach for all yesterday's Brand Scout leads"
```

**Creates**:
- Email templates for each lead
- LinkedIn connection messages
- Follow-up task list

---

## 🛠️ Utility Commands

### Find Brand Scout Report

```
"Find Brand Scout report for [BRAND]"
```

**Searches**: `.claude/brand_scout/output/` directory

### List All Reports

```
"List all Brand Scout reports from last [7/14/30] days"
```

**Output**: Report list with dates and confidence scores

### Regenerate Report Section

```
"Regenerate Section [X] of [BRAND] Brand Scout report"
```

**Use Case**: Update outdated information or improve specific section

### Export to Excel

```
"Export [BRAND] Brand Scout report to Excel format"
```

**Output**: Formatted Excel with 9 tabs (one per section)

---

## 📋 Workflow Combinations

### Complete New Lead Setup (Recommended)

```
"Complete new lead setup for [BRAND]:
1. Scout brand and generate report
2. Create deal folder structure
3. Set up HubSpot triple-record
4. Update pipeline tracker
5. Add to 9AM sync queue"
```

**One command → Full automation**

### Research + Folder Only (No HubSpot)

```
"Scout [BRAND] and create deal folder (skip HubSpot)"
```

**Use Case**: Want to review before HubSpot import

### Folder + HubSpot Only (Existing Report)

```
"Set up [BRAND] in HubSpot and create folder using existing Brand Scout report from [DATE]"
```

**Use Case**: Report already generated, just need setup

### Quality Check + Fix

```
"Quality check [BRAND] Brand Scout automation and fix any issues"
```

**Actions**:
- Review all components
- Identify missing pieces
- Fix or regenerate as needed

---

## 🎯 Advanced Commands

### Competitor Analysis

```
"Scout [BRAND] and generate detailed competitor comparison with [COMPETITOR1], [COMPETITOR2]"
```

**Enhanced Section 5**: Detailed benchmarking

### Contact Deep Dive

```
"Scout [BRAND] with maximum emphasis on stakeholder and contact discovery"
```

**Enhanced Section 4**: Extended contact research

### Shipping Intelligence Focus

```
"Scout [BRAND] prioritizing shipping carrier detection and logistics analysis"
```

**Enhanced Section 2**: Deep carrier analysis, 3PL identification

### Financial Analysis

```
"Scout [BRAND] with focus on revenue, volume, and growth metrics"
```

**Enhanced Section 1**: Detailed financial modeling

---

## 🔄 Batch Operations

### Weekly Batch Research

```
"Generate Brand Scout reports for all [00-LEAD] folders missing reports"
```

**Scans**: All lead folders, generates missing reports

### Refresh Outdated Reports

```
"Refresh Brand Scout reports older than [30/60/90] days"
```

**Updates**: Contacts, revenue, shipping info

### Batch HubSpot Import

```
"Import all pending Brand Scout leads to HubSpot from last week"
```

**Processes**: All reports without HubSpot IDs

---

## 📊 Reporting Commands

### Weekly Summary

```
"Generate weekly Brand Scout summary report"
```

**Includes**:
- Total leads researched
- Average confidence score
- Discovery call conversion rate
- Top pain points identified

### Performance Metrics

```
"Show Brand Scout performance metrics for last [7/30/90] days"
```

**Metrics**:
- Time per report
- Confidence trends
- HubSpot success rate
- Pipeline conversion

---

## 🆘 Troubleshooting Commands

### Debug Failed Report

```
"Debug Brand Scout report generation failure for [BRAND]"
```

**Analyzes**: Error logs, missing data, tool failures

### Fix HubSpot Associations

```
"Fix broken HubSpot associations for [BRAND] (Contact: [ID], Company: [ID], Lead: [ID])"
```

**Repairs**: Missing or incorrect associations

### Regenerate Customer Relationship Doc

```
"Regenerate Customer_Relationship_Documentation.md for [BRAND] from Brand Scout report"
```

**Use Case**: File corrupted or outdated

### Verify System Health

```
"Run Brand Scout system health check"
```

**Checks**:
- Chrome DevTools MCP status
- HubSpot connection
- File permissions
- Template accessibility

---

## 🎓 Examples by Use Case

### Use Case 1: Web Form Submission

**Command**:
```
"Scout Carbon38 (https://carbon38.com) with full automation"
```

**Result**:
- Complete report
- [00-LEAD]_Carbon38 folder
- HubSpot Contact, Company, Lead
- Ready for 9AM sync

### Use Case 2: LinkedIn Prospecting

**Command**:
```
"Quick scout Dr. Squatch - focus on contacts and LinkedIn presence"
```

**Result**:
- 15-minute research
- Contact-heavy report
- LinkedIn profiles validated

### Use Case 3: Competitor Intelligence

**Command**:
```
"Scout OLIPOP with emphasis on competitor analysis vs Poppi, Culture Pop"
```

**Result**:
- Detailed benchmarking
- Competitive positioning insights
- Market analysis

### Use Case 4: Batch Weekly Research

**Command**:
```
"Scout these 5 brands with full automation:
1. Dr. Squatch
2. OLIPOP
3. Carbon38
4. Chamberlain Coffee
5. Athletic Greens"
```

**Result**:
- 5 complete reports (~2 hours)
- 5 deal folders
- 15 HubSpot records (5 each)
- All ready for Monday 9AM sync

---

## ⚙️ Configuration Commands

### Set Default Parameters

```
"Set Brand Scout defaults:
- Time limit: 30 minutes
- Confidence threshold: 80%
- Auto-HubSpot: true
- Auto-folder: true"
```

### Customize Template

```
"Customize Brand Scout template to add [SECTION/FIELD]"
```

**Use Case**: Company-specific data requirements

### Enable/Disable Features

```
"Disable HubSpot automation for Brand Scout"
"Enable screenshot capture in Brand Scout reports"
```

---

## 📈 Integration Commands

### Sync to Saner.ai

```
"Export [BRAND] Customer_Relationship_Documentation.md to Saner.ai"
```

**Tags**: Lead, [BRAND], Brand Scout, [DATE]

### Export to CRM (Alternative)

```
"Export [BRAND] Brand Scout data to Salesforce/Pipedrive format"
```

**Output**: CSV with standard CRM fields

### Slack Notification

```
"Send Slack notification when [BRAND] Brand Scout automation completes"
```

**Message**: Summary with key metrics and next actions

---

## 🔐 Security Commands

### Redact Sensitive Data

```
"Redact proprietary information from [BRAND] Brand Scout report for external sharing"
```

**Removes**: Revenue, volume, contacts (optional)

### Encrypt Report

```
"Encrypt [BRAND] Brand Scout report and Customer Relationship doc"
```

**Use Case**: Highly sensitive competitive intelligence

---

## 📚 Help Commands

### Show Command List

```
"Show all Brand Scout commands"
"Brand Scout command reference"
```

**Output**: This document

### Explain Command

```
"Explain Brand Scout command: [COMMAND]"
```

**Output**: Detailed description, parameters, examples

### Show Examples

```
"Show Brand Scout examples for [USE CASE]"
```

**Use Cases**: Research, automation, troubleshooting, batch

---

**Last Updated**: October 8, 2025
**Version**: Brand Scout v3.7
**Integration**: Nebuchadnezzar v2.0 + HubSpot CRM
