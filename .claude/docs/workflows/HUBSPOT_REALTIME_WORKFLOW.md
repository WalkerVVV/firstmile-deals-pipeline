# HUBSPOT REAL-TIME UPDATE WORKFLOW
**Keeping HubSpot in sync throughout the day**

---

## 🎯 PHILOSOPHY

**As we work through the day, I automatically update HubSpot to keep records current.**

Every action you complete triggers a HubSpot update:
- Email sent → Log in HubSpot
- Call completed → Log notes in HubSpot
- Deal moves stages → Update in HubSpot
- Next steps identified → Create tasks in HubSpot

**You focus on the work. I handle the documentation.**

---

## 🔄 AUTOMATIC UPDATE TRIGGERS

### When You Say: "Stackd email sent!"
**I automatically do:**
1. Log email in HubSpot deal
2. Add note with email subject and key points
3. Create follow-up task for response check (3-5 days)
4. Update deal last contact date

**Example:**
```python
python hubspot_realtime_updates.py email "Stackd Logistics" \
  --subject "FirstMile Xparcel Rates - 10.2% Savings Proposal" \
  --direction OUTBOUND \
  --text "Sent rates workbook with $4,522/month savings. Awaiting response."
```

### When You Say: "Just got off call with Reid at BoxiiShip"
**I ask you:**
- "How did the call go? What were the key points?"

**Then I do:**
1. Log call in HubSpot with your notes
2. Add deal note with call summary
3. Create tasks for any action items discussed
4. Update next contact date if scheduled

**Example:**
```python
python hubspot_realtime_updates.py call "BoxiiShip" \
  --text "Discussed ACI Direct routing activation. Reid confirmed encoding fix is working. Need to follow up with Melissa by EOD. Next call scheduled for Thursday 10am." \
  --outcome COMPLETED
```

### When You Say: "Move Tactical Logistic to Closed Won!"
**I automatically do:**
1. Update deal stage in HubSpot to [07-CLOSED-WON]
2. Add note documenting the win
3. Set close date to today
4. Create onboarding tasks if needed

**Example:**
```python
python hubspot_realtime_updates.py stage "Tactical Logistic" \
  --stage "[07-CLOSED-WON]"

python hubspot_realtime_updates.py note "Tactical Logistic" \
  --text "CLOSED WON - Setup complete, first shipment processed successfully. Customer confirmed ready for production volume."
```

### When We Identify Next Steps
**I automatically do:**
1. Create HubSpot task with clear subject
2. Set priority (HIGH/MEDIUM/LOW)
3. Set due date based on urgency
4. Associate with deal

**Example:**
```python
python hubspot_realtime_updates.py task "Upstate Prep" \
  --subject "Make final rate decision: complete or close-lost" \
  --body "48 days in rate creation stage. Need decision to clear bottleneck. Review customer responsiveness and close-lost if no engagement." \
  --priority HIGH \
  --due_days 1
```

---

## 📋 COMPLETE ACTION → UPDATE MAPPING

| Your Action | What I Update in HubSpot | Tools Used |
|-------------|-------------------------|------------|
| **Send email** | Log email engagement, add note, create follow-up task | `log_email()` + `add_deal_note()` + `create_task()` |
| **Make call** | Log call with notes, add summary, create action items | `log_call()` + `add_deal_note()` + `create_task()` |
| **Move deal stage** | Update stage, add transition note, update dates | `update_deal_stage()` + `add_deal_note()` |
| **Close deal (won)** | Update stage, set close date, add win note | `update_deal_stage()` + `update_deal_property()` |
| **Close deal (lost)** | Update stage, add loss reason, create win-back task | `update_deal_stage()` + `add_deal_note()` |
| **Schedule meeting** | Create task, add note with details | `create_task()` + `add_deal_note()` |
| **Receive response** | Add note, update status, create next action | `add_deal_note()` + `create_task()` |
| **Identify blocker** | Add note, create task to resolve, escalate if needed | `add_deal_note()` + `create_task()` |

---

## 🤖 HOW IT WORKS (Behind the Scenes)

### Script: `hubspot_realtime_updates.py`

**Available Functions:**
```python
add_deal_note(deal_name, note_text)
create_task(deal_name, subject, body, priority, due_days)
update_deal_stage(deal_name, new_stage_folder)
log_call(deal_name, call_notes, outcome)
log_email(deal_name, subject, direction, notes)
update_deal_property(deal_name, property_name, value)
```

**Authentication:**
- Uses your Private App Token from `hubspot_config.py`
- Owner Lock: `699257003` (Brett Walker)
- Pipeline Lock: `8bd9336b-4767-4e67-9fe2-35dfcad7c8be` (FM Pipeline)

**Search Strategy:**
- Searches by deal name/company name
- Filters to your deals only
- Returns first match (usually correct)

---

## 💬 SAMPLE CONVERSATION FLOW

**You:** "Hey Claude, I just sent the Stackd Logistics email!"

**Me:** "Awesome! 🎉 Let me update HubSpot..."

*I run:*
```bash
python hubspot_realtime_updates.py email "Stackd Logistics" \
  --subject "FirstMile Xparcel Rates - 10.2% Savings Proposal" \
  --direction OUTBOUND \
  --text "Sent complete rates workbook showing 10.2% savings ($4,522/month). Included customer workbook and email template. Awaiting response."
```

**Me:**
```
✅ Email logged in HubSpot
✅ Note added to Stackd deal
✅ Follow-up task created for Thursday (3 days)

What's next? Should we move to Team Shipper proposal?
```

---

**You:** "Yes! Let's send Team Shipper. Where's the proposal?"

**Me:** "Found it! Here's what we're sending..."

*[I show you the email and attachments]*

**You:** "Sent!"

**Me:** "Perfect! Updating HubSpot..."

*I run:*
```bash
python hubspot_realtime_updates.py email "Team Shipper" \
  --subject "FirstMile Xparcel Rate Proposal" \
  --direction OUTBOUND

python hubspot_realtime_updates.py note "Team Shipper" \
  --text "PROPOSAL SENT (34 days in stage, now current). Sent Xparcel domestic rates to Mohammad. Attachments: Team Shipper_FirstMile_Xparcel_08222025.xlsx, Team Shipper_Xparcel_Full File_08222025.xlsm. JIRA: RATE-1897"
```

**Me:**
```
✅ Team Shipper proposal logged
✅ Deal notes updated (marked as current after 34d delay)
✅ Follow-up task created

2 proposals sent today! 🎯 Ready for Priority 3: BoxiiShip Melissa follow-up?
```

---

## 🎯 BENEFITS

### For You
- **Zero manual HubSpot entry** - I do it automatically
- **Complete audit trail** - Every action documented
- **No forgotten tasks** - Automatically created
- **Up-to-date pipeline** - Real-time accuracy

### For Your Team
- **Visibility** - Anyone can see deal status
- **Consistency** - Standardized notes/tasks
- **Accountability** - Clear action owners
- **Reporting** - Accurate pipeline data

### For Your Manager
- **Activity tracking** - See your daily progress
- **Pipeline accuracy** - Trust the numbers
- **Forecasting** - Based on real data
- **No lag time** - Real-time updates

---

## ⚙️ CONFIGURATION

**Already Set Up:**
- ✅ Private App Token configured
- ✅ Owner Lock (699257003)
- ✅ Pipeline Lock (8bd9336b-4767-4e67-9fe2-35dfcad7c8be)
- ✅ Stage mapping verified
- ✅ Script tested and working

**No additional setup needed!** Just use Claude normally and I'll handle HubSpot updates automatically.

---

## 🆘 TROUBLESHOOTING

### "Deal not found"
**Cause:** Deal name might be slightly different in HubSpot
**Fix:** I'll search with broader terms and show you matches

### "Failed to create task"
**Cause:** API rate limit or connection issue
**Fix:** I'll retry with exponential backoff

### "Stage update failed"
**Cause:** Invalid stage ID or deal locked
**Fix:** I'll verify stage mapping and show error details

---

## 📊 DAILY SUMMARY

**At EOD sync, I'll show you:**
```
Today's HubSpot Updates:
✅ 7 emails logged
✅ 3 calls logged
✅ 2 deals moved stages
✅ 12 tasks created
✅ 15 notes added

All deals up-to-date in HubSpot! 🎉
```

---

**Last Updated:** October 7, 2025
**Version:** Nebuchadnezzar v3.0
**Script:** `hubspot_realtime_updates.py`
