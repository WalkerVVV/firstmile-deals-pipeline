# Brand Scout v3.7 - Automated Workflow Integration

**Complete automation from research → HubSpot → Deal folder → Daily sync**

---

## 🎯 Complete Workflow Overview

```
User Request → Brand Scout Research (25-35 min) →
Auto-Create Deal Folder → Generate Customer_Relationship.md →
Create HubSpot Contact → Create HubSpot Company →
Create HubSpot Lead → Associate All Records →
Add Notes → Ready for 9AM Sync
```

---

## 📋 Automated Workflow Steps

### Step 1: Generate Brand Scout Report

**User Command**:
```
"Scout [BRAND NAME] and set up complete deal folder with HubSpot integration"
```

**Claude Code Actions**:
1. Execute Brand Scout research protocol (25-35 min)
2. Generate complete 9-section report
3. Save to `.claude/brand_scout/output/[BRAND]_brand_scout_[DATE].md`

---

### Step 2: Auto-Create Deal Folder Structure

**Folder Name Format**: `[00-LEAD]_[BRAND_NAME]`

**Example**: `[00-LEAD]_Dr_Squatch`

**Create Directory Structure**:
```bash
[00-LEAD]_[BRAND_NAME]/
├── CLAUDE.md
├── Customer_Relationship_Documentation.md (auto-generated)
├── README.md (auto-generated)
├── Brand_Scout_Report_[DATE].md (copied from output)
└── Reference/
    └── Initial_Research/
```

---

### Step 3: Generate Customer_Relationship_Documentation.md

**Auto-populate from Brand Scout Report sections**:

```markdown
# Customer Relationship Documentation - [BRAND NAME]

**Last Updated**: [DATE]
**Deal Stage**: [00-LEAD] New Lead
**Owner**: Brett Walker
**Status**: Initial Research Complete

---

## 📊 Company Overview

### Basic Information
- **Company Name**: [From Section 3]
- **Website**: [From Section 1]
- **Founded**: [From Section 3]
- **Headquarters**: [From Section 3]
- **Industry**: eCommerce - [Category]

### Business Model
- **DTC vs Wholesale**: [From Section 3]
- **Annual Revenue**: [From Section 1]
- **Annual Ship Volume**: [From Section 1]
- **Average Order Value**: [From Section 1]
- **Growth Rate**: [From Section 1]

### Elevator Pitch
[From Section 1]

### Value Propositions
[From Section 3]

---

## 👥 Key Stakeholders

[From Section 4 - Full contact table]

**Primary Contact**: [Name] - [Title]
**Email**: [Email]
**Phone**: [Phone]
**LinkedIn**: [URL]

**Secondary Contact(s)**:
[Additional contacts from Section 4]

---

## 📦 Shipping & Logistics Intelligence

### Current Shipping Setup
- **Primary Carrier(s)**: [From Section 2]
- **Service Levels**: [From Section 2]
- **Delivery Promise**: [From Section 2]
- **Fulfillment Type**: [From Section 8 or Section 2]
- **3PL Partner**: [From Section 2 if identified]

### Customer Experience Insights
**Shipping-Related Pain Points**:
[From Section 2 - CX Pain Points]

**Complaint Analysis**:
[From Section 5 - Customer Complaints table]

---

## 🎯 Opportunity Assessment

### FirstMile Value Proposition
**Proposed Solution**: FirstMile Xparcel (Ground, Expedited, Priority)

**Expected Benefits**:
- Cost savings potential (target: 40%)
- SLA improvements
- Single support thread
- Dynamic routing optimization
- Audit Queue protection

### Competitive Context
**Current Carriers**: [From Section 2]
**Competitor Benchmarks**: [From Section 5]

### Risk Factors
[From Section 5 - Risk Factors]

---

## 📝 Communication History

### [DATE] - Initial Research (Brand Scout v3.7)
- **Action**: Completed automated brand research
- **Source**: Brand Scout autonomous research system
- **Key Findings**:
  - Company overview captured
  - [X] verified contacts identified
  - Current shipping: [Carriers]
  - Annual volume: [Volume] units
  - Revenue: [Revenue]
- **Data Confidence**: [HIGH/MEDIUM/LOW] ([XX]%)
- **Next Action**: Discovery call outreach

### Template for Future Entries
### [DATE] - [Interaction Type]
- **Contact**: [Name - Title]
- **Method**: [Email/Phone/Meeting]
- **Summary**: [What was discussed]
- **Key Points**:
  - [Point 1]
  - [Point 2]
- **Action Items**:
  - [ ] [Task 1] - Due: [Date]
  - [ ] [Task 2] - Due: [Date]
- **Next Steps**: [What happens next]

---

## 🔄 Deal Progression Tracking

### Current Stage: [00-LEAD] New Lead
**Date Entered**: [DATE]
**Stage Requirements**:
- [X] Brand Scout research complete
- [ ] Contact attempted
- [ ] Discovery call scheduled

**Stage Exit Criteria**:
- Discovery call scheduled → Move to [01-DISCOVERY-SCHEDULED]

### Historical Timeline
- **[DATE]**: Lead created via Brand Scout automation
- **[DATE]**: [Future milestone]

---

## 📊 Technical Integration Notes

### eCommerce Platform
- **Platform**: [From Section 8]
- **Integration Method**: [From Section 8]
- **API Capabilities**: [From Section 8]

### Data Requirements
- PLD data: [Available/Requested/Pending]
- Current rate card: [Available/Requested/Pending]
- Volume projections: [From Brand Scout estimates]

---

## 📁 Related Documents

### Brand Scout Report
- Location: `Brand_Scout_Report_[DATE].md`
- Confidence: [Score]
- Sections: 9 complete

### Future Documents
- Discovery call notes: `Communications/Discovery_Call_[DATE].md`
- PLD analysis: `PLD_Analysis/[BRAND]_pld_analysis_[DATE].xlsx`
- Rate proposal: `Proposals/Rate_Proposal_[DATE].xlsx`

---

## 🎯 Next Actions

### Immediate (This Week)
- [ ] Email outreach to [Primary Contact]
- [ ] LinkedIn connection request
- [ ] Schedule discovery call

### Short-term (1-2 Weeks)
- [ ] Discovery call execution
- [ ] Request PLD data
- [ ] Gather current rate card

### Medium-term (2-4 Weeks)
- [ ] Complete PLD analysis
- [ ] Generate FirstMile rate proposal
- [ ] Present proposal

---

## 📈 Success Metrics

### Lead Qualification Criteria
- **Annual Volume**: [Volume] units (Target: >10K)
- **Revenue**: [Revenue] (Target: >$1M)
- **Current Carrier Fit**: [Good/Fair/Poor]
- **Decision Maker Access**: [Yes/No]
- **Tier**: [A/B] (from Section 7)

### Conversion Probability
Based on initial research:
- Volume match: [Yes/No]
- Geographic fit: [HQ in target zone]
- Pain points identified: [Yes/No]
- Decision maker contact: [Yes/No]

**Initial Score**: [X/4] - [High/Medium/Low] priority

---

**Document Version**: 1.0 (Auto-generated from Brand Scout v3.7)
**Last Updated**: [DATE]
**Next Review**: [DATE + 7 days]
```

---

### Step 4: Create README.md for Deal Folder

**Auto-generate**:

```markdown
# [BRAND NAME] - Deal Documentation

**Stage**: [00-LEAD] New Lead
**Owner**: Brett Walker
**Created**: [DATE]
**Last Updated**: [DATE]

---

## 📂 Folder Structure

```
[00-LEAD]_[BRAND_NAME]/
├── CLAUDE.md (Project context)
├── Customer_Relationship_Documentation.md (Primary tracking doc)
├── README.md (This file)
├── Brand_Scout_Report_[DATE].md (Initial research)
└── Reference/
    └── Initial_Research/
```

---

## 🎯 Quick Reference

**Company**: [BRAND NAME]
**Website**: [URL]
**HQ**: [City, State]
**Contact**: [Primary Contact Name] ([Title])
**Email**: [Email]
**Phone**: [Phone]

**Current Carrier**: [Carriers]
**Annual Volume**: [Volume] units
**Revenue**: [Revenue]

---

## 📋 Current Status

**Stage**: [00-LEAD] New Lead
**Next Action**: Discovery call outreach
**Priority**: [High/Medium/Low]

---

## 📚 Key Documents

1. **Customer_Relationship_Documentation.md** - Complete relationship tracking
2. **Brand_Scout_Report_[DATE].md** - Detailed research findings

---

## 🚀 Next Steps

- [ ] Email outreach to [Contact]
- [ ] LinkedIn connection
- [ ] Schedule discovery call
- [ ] Request PLD data

---

**For full details, see Customer_Relationship_Documentation.md**
```

---

### Step 5: HubSpot Contact Creation

**Command Executed**:
```bash
qm hubspot create-contact \
  --email "[Primary Contact Email]" \
  --firstname "[First Name]" \
  --lastname "[Last Name]" \
  --jobtitle "[Title]" \
  --linkedin "[LinkedIn URL]" \
  --phone "[Phone]" \
  --owner "699257003"
```

**Capture Contact ID** for associations

---

### Step 6: HubSpot Company Creation

**Command Executed**:
```bash
qm hubspot create-company \
  --name "[Company Name]" \
  --domain "[domain.com]" \
  --website "[https://website.com]" \
  --city "[City]" \
  --state "[State]" \
  --zip "[ZIP]" \
  --country "United States" \
  --industry "eCommerce" \
  --annualrevenue "[Revenue]" \
  --owner "699257003"
```

**Capture Company ID** for associations

---

### Step 7: HubSpot Lead Creation

**Command Executed**:
```bash
qm hubspot create-lead \
  --leadname "[Company Name] – [Primary Contact Name]" \
  --leadsource "Brand Scout Automation" \
  --leadstatus "New" \
  --priority "[High/Medium/Low]" \
  --owner "699257003"
```

**Capture Lead ID** for associations

---

### Step 8: Associate Records

**HubSpot Associations**:

1. **Contact → Company**:
   ```bash
   qm hubspot associate \
     --from-type contact \
     --from-id [CONTACT_ID] \
     --to-type company \
     --to-id [COMPANY_ID] \
     --association-type "contact_to_company"
   ```

2. **Contact → Lead**:
   ```bash
   qm hubspot associate \
     --from-type contact \
     --from-id [CONTACT_ID] \
     --to-type lead \
     --to-id [LEAD_ID] \
     --association-type "contact_to_lead"
   ```

3. **Company → Lead**:
   ```bash
   qm hubspot associate \
     --from-type company \
     --from-id [COMPANY_ID] \
     --to-type lead \
     --to-id [LEAD_ID] \
     --association-type "company_to_lead"
   ```

---

### Step 9: Add Notes to All Records

**Note Content**:
```
Brand Scout Automation - Initial Research Complete

Generated: [DATE]
Research Duration: [XX] minutes
Data Confidence: [HIGH/MEDIUM/LOW] ([XX]%)

KEY FINDINGS:
- Current Carriers: [Carriers]
- Annual Volume: [Volume] units
- Revenue: [Revenue]
- Primary Contact: [Name] ([Title])
- Pain Points: [Top 2-3]

OPPORTUNITY:
- Tier [A/B] prospect
- Expected savings: ~40%
- Xparcel service recommendation: [Ground/Expedited/Priority]

NEXT ACTIONS:
- [ ] Discovery call outreach
- [ ] Request PLD data
- [ ] LinkedIn connection

Deal Folder: [00-LEAD]_[BRAND_NAME]
Brand Scout Report: .claude/brand_scout/output/[BRAND]_brand_scout_[DATE].md
```

**Add to each record**:
```bash
# Add to Contact
qm hubspot add-note \
  --object-type contact \
  --object-id [CONTACT_ID] \
  --note "[Note Content]"

# Add to Company
qm hubspot add-note \
  --object-type company \
  --object-id [COMPANY_ID] \
  --note "[Note Content]"

# Add to Lead
qm hubspot add-note \
  --object-type lead \
  --object-id [LEAD_ID] \
  --note "[Note Content]"
```

---

### Step 10: Update Pipeline Tracker

**Append to `_PIPELINE_TRACKER.csv`**:

```csv
[BRAND_NAME],[00-LEAD],[DATE],Brett Walker,[Primary Contact],[Email],[Phone],[CONTACT_ID],[COMPANY_ID],[LEAD_ID],[Volume],[Revenue],Brand Scout Automation,High
```

**Fields**:
- Company Name
- Stage
- Date Entered
- Owner
- Primary Contact
- Email
- Phone
- Contact ID
- Company ID
- Lead ID
- Annual Volume
- Revenue
- Source
- Priority

---

### Step 11: Update Daily Log

**Append to `_DAILY_LOG.md`**:

```markdown
### [DATE] - Brand Scout Lead Creation

**Company**: [BRAND NAME]
**Action**: Automated lead research and HubSpot setup
**Duration**: [XX] minutes

**Outputs Created**:
- ✅ Brand Scout Report (9 sections, [XX]% confidence)
- ✅ Deal Folder: `[00-LEAD]_[BRAND_NAME]`
- ✅ Customer_Relationship_Documentation.md
- ✅ HubSpot Contact: [CONTACT_ID]
- ✅ HubSpot Company: [COMPANY_ID]
- ✅ HubSpot Lead: [LEAD_ID]
- ✅ All records associated with notes

**Key Findings**:
- Current carriers: [Carriers]
- Volume: [Volume] units/year
- Revenue: [Revenue]
- Tier: [A/B]

**Next Action**: Discovery call outreach to [Contact Name]
**Priority**: [High/Medium/Low]
```

---

## 🔄 Integration with 9AM Daily Sync

### 9AM Sync Workflow Enhancement

**New Morning Routine Section**:

```markdown
## Brand Scout Lead Queue

### Overnight/Yesterday's Brand Scout Results
Check: `.claude/brand_scout/output/` for new reports

**Action Items**:
1. Review all reports generated yesterday
2. Verify data confidence ≥ 75%
3. Confirm HubSpot records created
4. Check deal folders exist
5. Validate associations complete

### Quality Check Each Report
- [ ] Company name correct
- [ ] Contact verified (✅ marker)
- [ ] Carrier identified
- [ ] HubSpot triple-record created (Contact/Company/Lead)
- [ ] Customer_Relationship_Documentation.md present
- [ ] Notes added to all records

### Priority Actions from Brand Scout
Extract from `_DAILY_LOG.md` overnight entries:

**High Priority** (Tier A, >$10M revenue or >100K volume):
- [Company 1]: Discovery outreach to [Contact] ([Email])
- [Company 2]: Discovery outreach to [Contact] ([Email])

**Medium Priority** (Tier B):
- [Company 3]: Discovery outreach to [Contact] ([Email])

### Batch Actions
```bash
# Send discovery call email templates
# Use Customer_Relationship_Documentation.md for context
# Reference shipping pain points from Brand Scout Section 5
# Highlight Xparcel benefits from Section 7
```
```

---

## 📋 Complete Automation Script Template

**Master Command for Claude Code**:

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

**Expected Execution Time**: 30-40 minutes total
- Research: 25-35 min
- Folder creation: 1 min
- HubSpot creation: 2-3 min
- Associations & notes: 1-2 min
- Logging: 1 min

---

## 🎯 Success Criteria

**Workflow is successful when**:
- ✅ Brand Scout report generated (80%+ confidence)
- ✅ Deal folder created with proper naming
- ✅ Customer_Relationship_Documentation.md populated
- ✅ README.md created
- ✅ Brand Scout report copied to folder
- ✅ HubSpot Contact created
- ✅ HubSpot Company created
- ✅ HubSpot Lead created
- ✅ All 3 records associated
- ✅ Notes added to all 3 records
- ✅ Pipeline tracker updated
- ✅ Daily log entry added
- ✅ Ready for 9AM sync review

---

## 📊 Example Output Structure

```
After automation completes:

FirstMile_Deals/
├── [00-LEAD]_Dr_Squatch/
│   ├── CLAUDE.md
│   ├── Customer_Relationship_Documentation.md (auto-generated)
│   ├── README.md (auto-generated)
│   ├── Brand_Scout_Report_2025-10-08.md (copied)
│   └── Reference/
│       └── Initial_Research/
├── .claude/brand_scout/output/
│   └── DrSquatch_brand_scout_2025-10-08.md (original)
└── Downloads/
    ├── _PIPELINE_TRACKER.csv (updated)
    └── _DAILY_LOG.md (updated)

HubSpot:
├── Contact: Jack Haldrup (ID: 12345)
├── Company: Dr. Squatch (ID: 67890)
├── Lead: Dr. Squatch - Jack Haldrup (ID: 11111)
└── All associated with notes
```

---

## 🚀 Daily Integration Example

### Monday 9AM Sync

**Review overnight Brand Scout automation**:

```
3 new leads processed:
1. [00-LEAD]_Dr_Squatch - HIGH priority
   - Contact: Jack Haldrup (jack@drsquatch.com)
   - Volume: 150K/year
   - Action: Discovery call email

2. [00-LEAD]_OLIPOP - HIGH priority
   - Contact: Ben Goodwin (ben@drinkolipop.com)
   - Volume: 200K/year
   - Action: Discovery call email

3. [00-LEAD]_Carbon38 - MEDIUM priority
   - Contact: Katie Warner (katie@carbon38.com)
   - Volume: 80K/year
   - Action: Discovery call email (after Tier A)
```

**Execute batch outreach**:
- Email templates referencing shipping pain points
- Personalized based on Customer_Relationship_Documentation.md
- Track in HubSpot as activities
- Schedule follow-ups

---

## 🔧 Troubleshooting Automated Workflow

### Issue: Deal Folder Not Created
**Check**: Folder naming format `[00-LEAD]_[BRAND_NAME]`
**Fix**: Remove special characters from brand name

### Issue: HubSpot Contact Already Exists
**Solution**: Use existing Contact ID, create Company and Lead, associate

### Issue: Missing Customer_Relationship_Documentation.md
**Fix**: Re-run generation from Brand Scout report

### Issue: Associations Failed
**Check**: Verify Contact ID, Company ID, Lead ID all captured
**Fix**: Retry associations manually

---

## 📈 Performance Metrics

**Track for each automated workflow**:
- Total time: Research → HubSpot complete
- Data confidence score
- HubSpot record creation success rate
- Association success rate
- 9AM sync review time
- Discovery call conversion rate

**Weekly Dashboard**:
```
Week of [DATE]:
- Leads processed: 15
- Avg time per lead: 32 min
- Avg confidence: 85%
- HubSpot success rate: 100%
- Discovery calls scheduled: 5 (33%)
```

---

## ✅ Automation Checklist

**Before running automation, verify**:
- [ ] Chrome DevTools MCP running
- [ ] HubSpot MCP configured
- [ ] Write access to FirstMile_Deals folder
- [ ] `_PIPELINE_TRACKER.csv` exists
- [ ] `_DAILY_LOG.md` exists

**After automation completes, verify**:
- [ ] Brand Scout report in output folder
- [ ] Deal folder created
- [ ] Customer_Relationship_Documentation.md exists
- [ ] README.md exists
- [ ] HubSpot Contact created (check ID)
- [ ] HubSpot Company created (check ID)
- [ ] HubSpot Lead created (check ID)
- [ ] All records associated
- [ ] Notes added to all records
- [ ] Pipeline tracker updated
- [ ] Daily log updated

---

**Workflow Version**: 1.0 (Automated)
**Last Updated**: October 8, 2025
**Integration**: Nebuchadnezzar v2.0 + Brand Scout v3.7
