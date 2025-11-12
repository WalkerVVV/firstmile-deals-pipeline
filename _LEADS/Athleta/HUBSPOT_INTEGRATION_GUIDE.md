# HUBSPOT INTEGRATION GUIDE - Athleta Deal

**Deal Created:** October 8, 2025
**HubSpot API:** Private Access Token - "Gritty-Rain"
**Integration Method:** Python scripts with `hubspot_realtime_updates.py`
**Part of:** Brand Scout v3.7 Full Integration System

---

## 🤖 BRAND SCOUT v3.7 INTEGRATION

This deal was created through the **Brand Scout v3.7 automated lead research and HubSpot integration system**.

### How This Deal Was Created
1. ✅ Brand Scout v3.7 report generated (35-minute autonomous web research)
2. ✅ [00-LEAD]_Athleta folder created with complete structure
3. ✅ Customer_Relationship.md documentation auto-generated
4. ✅ HubSpot Company, Contacts, Deal, and Task created automatically
5. ✅ All records associated and notes added with key findings
6. ✅ Pipeline tracker updated with deal entry
7. ✅ Ready for 9AM daily sync review

### Brand Scout System Files
- **Main Documentation:** `.claude/BRAND_SCOUT_SYSTEM.md`
- **Automation Guide:** `.claude/brand_scout/AUTOMATED_WORKFLOW.md`
- **Command Reference:** `.claude/brand_scout/COMMAND_REFERENCE.md`
- **Brand Scout Report:** `ATHLETA_Brand_Scout_20251008.md`
- **Relationship Doc:** `Customer_Relationship.md`

### Master Command for New Leads
```
"Scout [BRAND NAME] with full automation"
```

This command triggers the complete workflow:
- 30-40 minute autonomous web research
- 9-section Brand Scout report with 80%+ confidence
- Deal folder creation with complete structure
- HubSpot Contact, Company, and Deal setup
- Pipeline tracking and 9AM sync preparation

**Example:** `"Scout Dr. Squatch with full automation"`

---

## ✅ CREATED IN HUBSPOT

### Company
- **Name:** Athleta
- **HubSpot ID:** 41146889221
- **Domain:** athleta.com
- **View:** [Athleta Company Record](https://app.hubspot.com/contacts/8210927/company/41146889221)

### Contacts
1. **Maggie Gauger** (President & CEO)
   - **HubSpot ID:** 162103696559
   - **Email:** maggiegauger@athleta.com
   - **View:** [Maggie Gauger Contact](https://app.hubspot.com/contacts/8210927/contact/162103696559)

2. **Chris Blakeslee** (Former President & CEO)
   - **HubSpot ID:** 162069910660
   - **Email:** chrisblakeslee@gap.com
   - **View:** [Chris Blakeslee Contact](https://app.hubspot.com/contacts/8210927/contact/162069910660)

### Deal
- **Name:** Athleta - Parcel Shipping Optimization
- **HubSpot ID:** 45514409032
- **Amount:** $40,000,000
- **Stage:** [01-DISCOVERY-SCHEDULED]
- **Owner:** Brett Walker (699257003)
- **View:** [Athleta Deal Record](https://app.hubspot.com/contacts/8210927/deal/45514409032)

### Initial Task
- **Task ID:** 90867474712
- **Subject:** LinkedIn research - Gap Inc. Supply Chain leadership
- **Due Date:** October 15, 2025
- **Priority:** HIGH

---

## 🔌 HUBSPOT CONNECTION METHOD

**ALWAYS use this method for HubSpot integration:**

### Authentication
- **Private App Token:** "Gritty-Rain"
- **API Key:** Stored in `hubspot_config.py`
- **Token:** `pat-na1-3044b6ba-1d68-4ad0-9bca-de8904bb0764`
- **Owner ID:** 699257003 (Brett Walker)
- **Pipeline ID:** 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

### Configuration File
**Location:** `C:\Users\BrettWalker\FirstMile_Deals\hubspot_config.py`

```python
from hubspot_config import get_hubspot_config, get_api_headers

config = get_hubspot_config()
# Returns: API_KEY, OWNER_ID, PIPELINE_ID, PORTAL_ID, BASE_URL
```

---

## 📝 REAL-TIME HUBSPOT UPDATES

**Master Workflow:** `C:\Users\BrettWalker\FirstMile_Deals\.claude\HUBSPOT_REALTIME_WORKFLOW.md`

### Primary Script: `hubspot_realtime_updates.py`

**Available Actions:**
```bash
python hubspot_realtime_updates.py {action} {deal_name} [options]
```

#### Actions:
- `note` - Add note to deal
- `task` - Create task associated with deal
- `stage` - Update deal stage
- `call` - Log call engagement
- `email` - Log email engagement
- `property` - Update deal property

---

## 🎯 COMMON HUBSPOT OPERATIONS FOR ATHLETA

### 1. Add Note to Deal
```bash
python hubspot_realtime_updates.py note "Athleta" \
  --text "Completed Brand Scout v3.7 report. Identified $40M shipping spend opportunity with 50% delivery failure rate. New CEO Maggie Gauger started Aug 2025 - perfect timing for operational review."
```

### 2. Create Follow-Up Task
```bash
python hubspot_realtime_updates.py task "Athleta" \
  --subject "Prepare CEO-level outreach email for Maggie Gauger" \
  --body "Draft LinkedIn InMail focusing on delivery reliability issues and $10-14M savings opportunity. Reference new CEO's first 100 days and turnaround mandate." \
  --priority HIGH \
  --due_days 3
```

### 3. Log Outbound Email
```bash
python hubspot_realtime_updates.py email "Athleta" \
  --subject "FirstMile Xparcel - Solving Athleta's Delivery Reliability Issues" \
  --direction OUTBOUND \
  --text "Sent LinkedIn InMail to Maggie Gauger introducing FirstMile's Xparcel solution. Highlighted 50% delivery failure rate from customer reviews and $10-14M annual savings opportunity."
```

### 4. Log Discovery Call
```bash
python hubspot_realtime_updates.py call "Athleta" \
  --text "Discovery call with [Contact Name]. Discussed current 6-carrier complexity and delivery failures. Confirmed ~9M packages/year volume. Next step: Request sample PLD data for rate analysis." \
  --outcome COMPLETED
```

### 5. Move Deal Stage
```bash
# Move to Discovery Complete
python hubspot_realtime_updates.py stage "Athleta" \
  --stage "[02-DISCOVERY-COMPLETE]"

# Move to Rate Creation
python hubspot_realtime_updates.py stage "Athleta" \
  --stage "[03-RATE-CREATION]"

# Move to Proposal Sent
python hubspot_realtime_updates.py stage "Athleta" \
  --stage "[04-PROPOSAL-SENT]"
```

### 6. Update Deal Property
```bash
python hubspot_realtime_updates.py property "Athleta" \
  --property "closedate" \
  --value "2026-06-30"
```

---

## 📊 STAGE MAPPING REFERENCE

| Stage Folder | Stage ID | HubSpot Stage Name |
|--------------|----------|-------------------|
| [00-LEAD] | N/A | Not in pipeline yet |
| [01-DISCOVERY-SCHEDULED] | 1090865183 | Discovery Scheduled |
| [02-DISCOVERY-COMPLETE] | d2a08d6f-cc04-4423-9215-594fe682e538 | Discovery Complete |
| [03-RATE-CREATION] | e1c4321e-afb6-4b29-97d4-2b2425488535 | Rate Creation |
| [04-PROPOSAL-SENT] | d607df25-2c6d-4a5d-9835-6ed1e4f4020a | Proposal Sent |
| [05-SETUP-DOCS-SENT] | 4e549d01-674b-4b31-8a90-91ec03122715 | Setup Docs Sent |
| [06-IMPLEMENTATION] | 08d9c411-5e1b-487b-8732-9c2bcbbd0307 | Implementation |
| [07-CLOSED-WON] | 3fd46d94-78b4-452b-8704-62a338a210fb | Closed Won |
| [08-CLOSED-LOST] | 02d8a1d7-d0b3-41d9-adc6-44ab768a61b8 | Closed Lost |

**Source:** `hubspot_config.py` - `STAGE_MAPPING` dictionary

---

## 🔄 TYPICAL WORKFLOW FOR ATHLETA DEAL

### Week 1 (Oct 8-15, 2025)
```bash
# Day 1: Add initial research note
python hubspot_realtime_updates.py note "Athleta" \
  --text "Brand Scout v3.7 completed. Key findings: 50% delivery failure rate, 6-carrier complexity, $40M annual spend, $10-14M savings opportunity. New CEO started Aug 2025."

# Day 3: LinkedIn research complete
python hubspot_realtime_updates.py note "Athleta" \
  --text "LinkedIn research complete. Identified Gap Inc. supply chain contacts. Maggie Gauger active on LinkedIn. Preparing outreach strategy."

# Create outreach task
python hubspot_realtime_updates.py task "Athleta" \
  --subject "Send LinkedIn InMail to Maggie Gauger" \
  --priority HIGH \
  --due_days 2
```

### Week 2 (Oct 16-22, 2025)
```bash
# Log outbound email
python hubspot_realtime_updates.py email "Athleta" \
  --subject "FirstMile Introduction - Parcel Shipping Optimization" \
  --direction OUTBOUND

# Create follow-up task
python hubspot_realtime_updates.py task "Athleta" \
  --subject "Follow up on Maggie Gauger LinkedIn message" \
  --due_days 5
```

### Week 3-4 (Oct 23 - Nov 5, 2025)
```bash
# Response received
python hubspot_realtime_updates.py note "Athleta" \
  --text "Maggie Gauger responded. Expressed interest in learning more. Scheduling discovery call."

# Move to Discovery Scheduled
python hubspot_realtime_updates.py stage "Athleta" \
  --stage "[01-DISCOVERY-SCHEDULED]"

# Create discovery prep task
python hubspot_realtime_updates.py task "Athleta" \
  --subject "Prepare discovery call agenda and questions" \
  --priority HIGH \
  --due_days 2
```

---

## 🚫 WHAT NOT TO DO

### ❌ Never Use Manual HubSpot Entry
- Don't log into HubSpot web interface to add notes manually
- Don't create tasks through HubSpot UI
- **ALWAYS use `hubspot_realtime_updates.py` script**

### ❌ Never Skip Documentation
- Every action (email, call, meeting) MUST be logged in HubSpot
- Use the script immediately after the action
- Don't batch updates at end of day

### ❌ Never Modify hubspot_config.py Directly
- API key, Owner ID, Pipeline ID are locked
- Stage mappings are verified and should not be changed
- Use environment variables if configuration changes needed

---

## 🔍 TROUBLESHOOTING

### "Deal not found" Error
```bash
# Search is case-sensitive and looks for exact deal name match
# If error occurs, check deal name in HubSpot:
# Deal Name: "Athleta - Parcel Shipping Optimization"

# Script searches by deal name or company name
# Both "Athleta" and "Athleta - Parcel Shipping Optimization" should work
```

### API Rate Limit
```bash
# Script has automatic retry with exponential backoff
# If rate limit hit, wait 5-10 minutes before retry
# Max 150 requests per 10 seconds (should never hit this)
```

### Authentication Error
```bash
# Verify API key in hubspot_config.py
# Check Private App "Gritty-Rain" is active in HubSpot
# Settings > Integrations > Private Apps > Gritty-Rain
```

---

## 📚 ADDITIONAL RESOURCES

### Brand Scout v3.7 System Files
- **System Overview:** `.claude/BRAND_SCOUT_SYSTEM.md` - Complete system integration
- **Automated Workflow:** `.claude/brand_scout/AUTOMATED_WORKFLOW.md` ⭐ - Full automation guide
- **Command Reference:** `.claude/brand_scout/COMMAND_REFERENCE.md` ⭐ - All available commands
- **Quick Start:** `.claude/brand_scout/QUICKSTART.md` - 5-minute getting started guide
- **System Check:** `.claude/brand_scout/SYSTEM_CHECK.md` - Health check & validation
- **Integration Summary:** `BRAND_SCOUT_COMPLETE_INTEGRATION.md` ⭐ - Full integration overview

### HubSpot Integration Files
- **Main Workflow:** `.claude/HUBSPOT_REALTIME_WORKFLOW.md`
- **Configuration:** `hubspot_config.py`
- **Real-Time Script:** `hubspot_realtime_updates.py`
- **Batch Updates:** `hubspot_batch_updates_tuesday_am.py`
- **Pipeline Verify:** `hubspot_pipeline_verify.py`

### Daily Operations
- **9AM Sync:** `.claude/DAILY_SYNC_OPERATIONS.md` - Phase 0.5 includes Brand Scout review
- **Pipeline Tracker:** `_PIPELINE_TRACKER.csv` (downloads folder)
- **Daily Log:** `_DAILY_LOG.md` (downloads folder)
- **Action Queue:** `FOLLOW_UP_REMINDERS.txt` (downloads folder)

### HubSpot API Documentation
- **Portal ID:** 8210927
- **API Docs:** https://developers.hubspot.com/docs/api/overview
- **Private Apps:** https://app.hubspot.com/private-apps/8210927

### Deal Links
- **All Deals:** https://app.hubspot.com/contacts/8210927/deals/board/view/all/
- **Athleta Deal:** https://app.hubspot.com/contacts/8210927/deal/45514409032
- **Athleta Company:** https://app.hubspot.com/contacts/8210927/company/41146889221

---

## 🎯 QUICK REFERENCE CHEAT SHEET

### Most Common Commands for Athleta:

```bash
# Add note
python hubspot_realtime_updates.py note "Athleta" --text "Your note here"

# Create task (due in 3 days)
python hubspot_realtime_updates.py task "Athleta" --subject "Task subject" --due_days 3

# Log email sent
python hubspot_realtime_updates.py email "Athleta" --subject "Email subject" --direction OUTBOUND

# Log call
python hubspot_realtime_updates.py call "Athleta" --text "Call notes" --outcome COMPLETED

# Move to next stage
python hubspot_realtime_updates.py stage "Athleta" --stage "[02-DISCOVERY-COMPLETE]"
```

---

**Last Updated:** October 8, 2025
**Deal Status:** [01-DISCOVERY-SCHEDULED]
**Next Action:** LinkedIn research for Gap Inc. supply chain contacts (Due: Oct 15)
**Created via:** Brand Scout v3.7 Full Automation
**System Status:** ✅ PRODUCTION READY

---

## 🚀 9AM DAILY SYNC WORKFLOW (Phase 0.5)

This deal is now part of your 9AM daily sync workflow with Brand Scout review:

### Phase 0.5: Brand Scout Results Review (15-20 minutes)
**Time:** 9:02 AM - 9:20 AM

1. **Check Overnight Results** (9:02 AM)
   - Open `.claude/brand_scout/output/` for new reports
   - Review automation summary

2. **Quality Check** (9:07 AM)
   - Verify data confidence score (target: 80%+)
   - Confirm HubSpot records created ✅
   - Validate deal folders created ✅

3. **Extract Actions** (9:10 AM)
   - Review Customer_Relationship.md for pain points
   - Identify discovery email opportunities
   - Prioritize by deal size and opportunity quality

4. **Execute Outreach** (9:15 AM)
   - Send discovery emails using Brand Scout insights
   - Log all emails via hubspot_realtime_updates.py
   - Create follow-up tasks

### Athleta Next Steps (9AM Tomorrow)
- [ ] Review Brand Scout findings with fresh perspective
- [ ] Draft LinkedIn InMail to Maggie Gauger (new CEO)
- [ ] Emphasize delivery reliability pain point (50% failure rate)
- [ ] Reference $10-14M savings opportunity
- [ ] Log outreach in HubSpot immediately

**Result:** Qualified leads ready for discovery calls within 24 hours of Brand Scout completion

---

## 🔐 SECURITY NOTES

- **API Token:** Stored in `hubspot_config.py` (not version controlled if in .gitignore)
- **Private App:** "Gritty-Rain" has read/write access to:
  - CRM Objects (contacts, companies, deals)
  - Engagements (emails, calls, notes, tasks)
  - Timelines
- **Owner Lock:** All operations locked to Brett Walker (699257003)
- **Pipeline Lock:** All deals locked to FM Pipeline (8bd9336b-4767-4e67-9fe2-35dfcad7c8be)

**Never share the API token or commit it to public repositories.**

---

*This integration guide ensures all HubSpot interactions follow the established "Gritty-Rain" Private App method with `hubspot_realtime_updates.py` script.*
