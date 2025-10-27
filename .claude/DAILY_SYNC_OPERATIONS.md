# Daily Sync Operations Guide
**Nebuchadnezzar v3.0 - Continuous Execution & Learning System**

---

## Overview

The Daily Sync system ensures systematic pipeline management, customer engagement, and continuous improvement through structured touchpoints at 9AM, NOON, EOD, and End of Week.

### Purpose
- **Pipeline Visibility**: Real-time deal status and priorities
- **Action Generation**: Systematic next-step identification
- **Learning Capture**: Document what works, what fails
- **Velocity Optimization**: Reduce friction, increase win rate

### Core Principle
> "Measure → Execute → Reflect → Improve → Repeat"

---

## 9AM Sync - Day Start

### Purpose
Generate priority-ranked action list with urgency scoring for optimal daily execution.

### Execution

**Script**: `daily_9am_workflow.py`

```bash
cd C:\Users\BrettWalker\FirstMile_Deals
python daily_9am_workflow.py
```

### Process Flow

#### Phase 0: Load Previous Day Learnings
```
Input: _DAILY_LOG_FEEDBACK.md from Downloads folder
Action: Review what worked, what failed, what to apply today
Output: Context for today's execution
```

**Example Learnings**:
- ✅ Customer Relationship Docs saved 30min per deal
- ❌ Long emails bury critical asks → use dedicated emails
- 🔧 Pre-check internal dependencies before customer comms

#### Phase 0.5: Brand Scout Overnight Processing Review
```
Check: .claude/brand_scout/output/ for new reports
Action: Review automated lead creation results
Output: Priority list for discovery outreach
```

**Brand Scout Quality Check**:
1. **Review New Reports**: Check all reports generated overnight/yesterday
   - Data confidence ≥ 75% threshold
   - Verified contacts present (✅ marker)
   - Carriers identified

2. **Verify HubSpot Setup**: Check automation completed successfully
   - Contact record created
   - Company record created
   - Lead record created
   - All records associated with notes

3. **Validate Deal Folders**: Confirm folder structure correct
   - `[00-LEAD]_[BRAND_NAME]` exists
   - `Customer_Relationship_Documentation.md` present
   - `Brand_Scout_Report_[DATE].md` copied

4. **Extract Priority Actions**: From `_DAILY_LOG.md` Brand Scout entries
   - **Tier A** (High Priority): >$10M revenue OR >100K volume
   - **Tier B** (Medium Priority): All others
   - Note shipping pain points for personalized outreach

**Output Format**:
```
BRAND SCOUT OVERNIGHT RESULTS (3 new leads):

HIGH PRIORITY (Tier A):
1. Dr. Squatch - Jack Haldrup (jack@drsquatch.com)
   - Volume: 150K/year | Revenue: $100M
   - Current: USPS, UPS | Pain: Late delivery 25%
   - Action: Discovery email emphasizing SLA improvements
   - Folder: [00-LEAD]_Dr_Squatch ✅
   - HubSpot: Contact(12345), Company(67890), Lead(11111) ✅

MEDIUM PRIORITY (Tier B):
2. Carbon38 - Katie Warner (katie@carbon38.com)
   - Volume: 80K/year | Revenue: $8M
   - Current: FedEx | Pain: High costs
   - Action: Discovery email emphasizing cost savings
   - Folder: [00-LEAD]_Carbon38 ✅
   - HubSpot: Contact(12346), Company(67891), Lead(11112) ✅
```

#### Phase 1: Check Overnight Email Responses (Automated)

**Tool**: Chrome DevTools MCP + Superhuman AI

**Automated Command** (Run in Claude Code):
```
"Use chrome-mcp-server to check Superhuman for overnight email responses:
1. Navigate to open Superhuman tab
2. Search for: in:inbox after:yesterday
3. Extract email list with senders, subjects, and timestamps
4. Identify customer responses to pending items from yesterday's FOLLOW_UP_REMINDERS.txt
5. Display prioritized list of responses requiring action today"
```

**Output Format**:
```
OVERNIGHT EMAIL RESPONSES:

CUSTOMER RESPONSES (3):
✅ Stackd Logistics - Landon confirmed Tue Oct 8 10AM meeting
✅ Team Shipper - No response (still pending)
📧 BoxiiShip - Reminder email (not a response)

NEW INBOUND (2):
🆕 Carbon38 - Katie Warner inquiry about rates
🆕 Dr. Squatch - Jack Haldrup PLD data shared

INTERNAL (1):
💬 Stephen - DYLN rate card ready for review
```

**Manual Fallback**:
```
Review:
1. Pending customer responses (list all by name)
2. Active blockers (internal dependencies)
3. Expected deliverables due today
```

**Cross-Reference with FOLLOW_UP_REMINDERS.txt**:
```
PENDING RESPONSES (from yesterday):
1. Stackd Logistics - Landon meeting confirmation → ✅ CONFIRMED
2. Driftaway Coffee - Suyog recovery call (Mon/Tue) → ⏳ PENDING
3. DYLN - Dorian dimensions & discount threshold → ⏳ PENDING
...

ACTIVE BLOCKERS:
- DYLN: Brock data needed for JIRA submission (CRITICAL)
```

#### Phase 2: Live Pipeline Sync
```
HubSpot Query:
  Owner ID: 699257003
  Pipeline: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

Actions:
1. Fetch all active deals
2. Group by stage
3. Identify SLA violations (>14 days in [03], >30 days in [04])
```

**Output**:
```
PRIORITY PIPELINE: 22 active deals

STAGE BREAKDOWN:
  [02-DISCOVERY-COMPLETE]: 7 deals
  [03-RATE-CREATION]: 8 deals
  [04-PROPOSAL-SENT]: 3 deals
  [05-SETUP-DOCS-SENT]: 4 deals
```

#### Phase 3: Priority Analysis

**Urgency Scoring Algorithm** (0-100):
```python
score = 50  # Base

# Factor 1: Days in stage vs SLA (max +30)
if days_in_stage > sla_days:
    score += 30
elif days_in_stage > sla_days * 0.75:
    score += 20

# Factor 2: Deal amount (max +20)
if amount > $50K:
    score += 20
elif amount > $25K:
    score += 10

# Factor 3: Last activity (max +20)
if days_since_activity > 14:
    score += 20

# Factor 4: Stage bonus
if stage == [06-IMPLEMENTATION]:
    score += 15  # At finish line
```

**Priority Tiers**:
- **P1 (Score 80-100)**: Action required TODAY
- **P2 (Score 60-79)**: Action within 3 days
- **P3 (Score <60)**: Monitor closely

**Output**:
```
PRIORITY 1 - IMMEDIATE ACTIONS:
1. CHECK EMAIL FOR 6 CUSTOMER RESPONSES
2. BLOCKER: Follow up with Brock (DYLN data)
3. CHECK STACKD RATE STATUS (JIRA RATE-1897)

PRIORITY 2 - ACTIVE DEAL FOLLOW-UPS:
4. UPSTATE PREP ($950K) - 44+ days in [03]
5. DRIFTAWAY COFFEE - Recovery call if confirmed
```

#### Phase 4: Action Generation
```
Output: HubSpot tasks due today with context

Format:
- Deal name
- Action required
- Contact info
- Next stage goal
- Success criteria
```

#### Phase 5: Pipeline Health
```
Metrics:
- Critical deals this week
- SLA violations
- Stage bottlenecks (count [03] > 10)
- Pipeline value at risk
```

**Output**:
```
CRITICAL DEALS THIS WEEK:
- DYLN: $3.6M (blocked on Brock data)
- Upstate Prep: $950K (44+ days, needs attention)
- Stackd: Rate delivery imminent

SLA WATCH:
- Upstate Prep: 44+ days in [03] (VIOLATION)
```

### Next Sync
**NOON (12:00 PM)** - Progress check

---

## NOON Sync - Midday Progress Check

### Purpose
Review morning execution, process new developments, plan afternoon priorities.

### Execution

**Manual Check** (No automated script)

```bash
# Quick pipeline check
python hubspot_pipeline_verify.py
```

### Process Flow

#### Phase 1: Morning Execution Review
```
Questions:
1. Which P1 actions were completed?
2. What new customer responses arrived?
3. Any blocker status updates?
4. Unexpected developments?
```

**Checklist**:
- ✅ Email inbox checked
- ✅ Blockers addressed or escalated
- ✅ Customer responses logged in HubSpot
- ✅ Deal notes updated

#### Phase 2: Pipeline Changes
```
Check for:
1. Deals moved between stages (folder movements)
2. New leads created
3. Lost/won deals
4. HubSpot sync status
```

**Verification**:
```bash
python pipeline_sync_verification.py
```

#### Phase 3: Afternoon Priorities
```
Identify:
1. Remaining P1 actions from morning
2. New urgent items from customer responses
3. EOD prep needs (data gathering, analysis)
```

**Example Output**:
```
AFTERNOON PRIORITIES:

CARRYOVER FROM MORNING:
1. Upstate Prep follow-up (not completed)
2. Logystico Day 2 check (no response yet)

NEW URGENT:
1. Stackd - Landon confirmed Tue meeting (prep materials)
2. Driftaway - Suyog requested Mon 2pm call (send invite)

EOD PREP:
1. Run Stackd PLD analysis for Tue meeting
2. Update Customer Relationship Docs
```

### Next Sync
**EOD (5:00 PM)** - Learning capture

---

## EOD Sync - End of Day Learning Capture

### Purpose
Capture daily learnings, setup tomorrow, feed continuous improvement loop.

### Execution

**File**: `_DAILY_LOG_FEEDBACK.md` (Downloads folder)

### Process Flow

#### Phase 0: Superhuman Email Intelligence Gathering

**Tool**: Chrome DevTools MCP + Superhuman AI (Automated via Claude Code with Sonnet 4.5)

**📚 MASTER REFERENCE**: [EOD_SYNC_MASTER_PROMPT.md](EOD_SYNC_MASTER_PROMPT.md)

**Process**:
1. Ensure Superhuman is open in Comet browser: `https://mail.superhuman.com/`
2. Run automated EOD email analysis via Claude Code using master prompt
3. AI processes email activity and generates structured reports
4. Output automatically saved to `_DAILY_LOG.md` and `FOLLOW_UP_REMINDERS.txt`

**🚀 ONE-LINE AUTOMATION COMMAND** (Copy-paste into Claude Code):
```
Run EOD sync for today: Use chrome-mcp-server to access Superhuman AI at mail.superhuman.com, extract email analysis for TODAY's date, query HubSpot API for pipeline activity, generate _DAILY_LOG.md with comprehensive activity summary, create FOLLOW_UP_REMINDERS.txt with tomorrow's action queue, validate all dates are correct, and save both files to C:\Users\BrettWalker\Downloads\
```

**📋 QUALITY CHECKLIST** (Auto-validated by S4):
- [ ] Today's date verified in 3 places (Superhuman, report header, system)
- [ ] All pipeline movements have evidence quotes
- [ ] All urgent actions have Who, What, When, Why
- [ ] HubSpot API queried (or fallback noted)
- [ ] Files saved to correct location
- [ ] Tomorrow's date in FOLLOW_UP_REMINDERS.txt header

**Full EOD Analysis Prompt** (See: `C:\Users\BrettWalker\Downloads\SUPERHUMAN_EOD_SEARCH_PROMPT.md`):

```
SEARCH QUERY: in:sent OR in:inbox after:today

Analyze all emails sent and received today to provide a comprehensive end-of-day summary.

PART 1: WHAT I WORKED ON TODAY
For each deal/customer/project mentioned in today's emails, document:
- Customer/Deal Name & Current Stage
- Action Taken (email sent, meeting held, data received, issue resolved)
- Key Details (what was discussed/decided, what was delivered, issues resolved, meetings scheduled)
- Email Type: Sent vs Received
- Time of interaction
- Status Change: Did this move the deal forward?

Format:
## TODAY'S ACTIVITY SUMMARY - [Date]

### Priority 1 Deals
- **[Customer]** ([Stage])
  - Action: [What you did]
  - Details: [Key points]
  - Time: [HH:MM]
  - Next Step: [What's needed]

### Priority 2 Deals
[Same format]

### Priority 3 Deals
[Same format]

### New Inbound
[New leads/inquiries]

### Internal/Team Communications
[Team discussions, coordination]

PART 2: WHAT'S NEXT TO WORK ON
Identify based on today's email activity:

1. IMMEDIATE FOLLOW-UPS (within 24h):
   - Customer expecting response
   - Meeting confirmations pending
   - Data/reports promised
   - Questions requiring answers

2. THIS WEEK'S PRIORITIES:
   - Proposals to finalize
   - Rates to create
   - Meetings to schedule
   - Analysis to complete

3. BLOCKERS IDENTIFIED:
   - Waiting on customer data
   - Waiting on internal resources
   - Technical issues
   - Decision delays

4. OPPORTUNITIES SPOTTED:
   - Upsell mentions
   - Referrals
   - Expansion conversations
   - Competitive wins

Format:
## TOMORROW'S ACTION PLAN - [Next Day]

### 🔥 URGENT (Do First)
1. [Action] - [Customer] - [Why urgent]

### 📋 HIGH PRIORITY (This Week)
1. [Action] - [Customer] - [Timeline]

### ⏳ WAITING ON
1. [What waiting for] - [From whom] - [What it unblocks]

### 💡 OPPORTUNITIES
1. [Opportunity] - [Customer] - [Potential value]

PART 3: DEAL STAGE MOVEMENTS
Identify deals that moved stages today based on email evidence:

Evidence to look for:
- Discovery meeting confirmed → [01-DISCOVERY-SCHEDULED]
- Discovery completed, data received → [02-DISCOVERY-COMPLETE]
- Rates created and sent → [04-PROPOSAL-SENT]
- Setup docs sent, verbal commit → [05-SETUP-DOCS-SENT]
- Customer "yes"/"let's move forward" → [06-IMPLEMENTATION]
- First live shipment → [07-CLOSED-WON]
- Customer declines/goes dark → [08-CLOSED-LOST]

Format:
## PIPELINE MOVEMENTS - [Date]

### Stage Changes Detected
- **[Customer]**: [Old Stage] → [New Stage]
  - Evidence: [Quote from email or action]
  - Action Required: [Update HubSpot, move folder, tasks]

PART 4: METRICS & INSIGHTS

1. EMAIL VOLUME:
   - Total sent today
   - Total received today
   - Customers contacted
   - New conversations started

2. DEAL VALUE ACTIVITY:
   - Total annual value of deals worked today
   - Proposals sent
   - Meetings held
   - Follow-ups completed

3. RESPONSE QUALITY:
   - Average response time to customer emails
   - Emails >24h old needing response
   - Missed follow-ups from previous commitments

Format:
## TODAY'S METRICS - [Date]

📧 EMAIL ACTIVITY
- Sent: [count]
- Received: [count]
- Customers contacted: [count]
- New threads: [count]

💰 DEAL ACTIVITY
- Deals worked: [count] ($[value])
- Proposals sent: [count] ($[value])
- Meetings: [count]
- Follow-ups: [count]

⏱️ RESPONSE PERFORMANCE
- Avg response time: [hours/min]
- Overdue responses: [count]
- On-time commitments: [count]/[total]

SPECIAL INSTRUCTIONS:
1. Focus on actionable intelligence - what it means for deal progress
2. Identify patterns - multiple emails = urgency or blocker
3. Flag risks - frustration, delays, competitive threats
4. Celebrate wins - positive responses, deals advancing, problems solved
5. Be specific - use quotes, numbers, dates from emails
6. Cross-reference - if "as discussed", find original context

OUTPUT: Comprehensive EOD summary in markdown, ready to paste into _DAILY_LOG.md, FOLLOW_UP_REMINDERS.txt, and daily status updates. Aim for 2-3 pages, scannable format, professional tone, action-oriented.
```

**Quick Access Workflow**:
```bash
# Generate today's prompt with dates filled in
cd C:\Users\BrettWalker\FirstMile_Deals\.claude
python superhuman_eod_workflow.py

# Opens: SUPERHUMAN_EOD_PROMPT_TODAY.txt in Downloads folder
# Ready to copy-paste into Superhuman AI
```

**Output Integration**:
1. Copy Superhuman AI response
2. Parse into _DAILY_LOG.md sections
3. Update FOLLOW_UP_REMINDERS.txt with tomorrow's urgent items
4. Flag stage movements for HubSpot sync

---

#### Phase 1: Daily Summary
```
Metrics to capture:
- Total actions completed
- Customer touchpoints (calls, emails)
- Pipeline movements (deals advanced)
- HubSpot notes/tasks created
- Pending responses carried to tomorrow
```

**Template**:
```markdown
## [DAY] [DATE] METRICS

- Customer Touchpoints: 6
- Docs Created: 4
- HubSpot Notes: 4
- Stage Progressions: 1 (Team Shipper → [04])
- Monday Tasks: 5
- Pending Responses: 6
- Active Blockers: 1 (Brock data)
```

#### Phase 2: Learnings & Insights

**Four Categories**:

**1. WHAT WORKED ✅**
```markdown
### WHAT WORKED ✅

1. **[Pattern Name]**
   - [What you did]
   - Impact: [Measurable result]
   - Time Saved: [If applicable]
   - **KEEP**: [Action to make permanent]
```

**Example**:
```markdown
1. **Customer Relationship Documentation Pattern**
   - Created 4 comprehensive customer docs
   - Impact: Clear action items, no information loss
   - Time Saved: ~30 min per deal vs email searches
   - **KEEP**: Make standard for all [01-QUALIFIED] and above
```

**2. WHAT FAILED ❌**
```markdown
### WHAT FAILED ❌

1. **[Problem Description]**
   - [What happened]
   - Risk: [Business impact]
   - **FIX**: [Immediate corrective action]
```

**Example**:
```markdown
1. **Brock Data Dependency (DYLN)**
   - Told customer "rates submitted" but blocked internally
   - Risk: Credibility gap if early follow-up
   - **FIX**: Pre-check dependencies before customer comms
```

**3. WHAT'S UNCLEAR ❓**
```markdown
### WHAT'S UNCLEAR ❓

1. **[Decision Needed]**
   - [Context/question]
   - [Why it matters]
```

**Example**:
```markdown
1. **USPS Cubic Pricing Strategy**
   - How aggressive vs USPS Tier 2 NSA?
   - Decision needed for DYLN rates
```

**4. WHAT'S MISSING 🔧**
```markdown
### WHAT'S MISSING 🔧

1. **[Gap/Need]**
   - [Specific requirement]
   - [Expected outcome]
```

**Example**:
```markdown
1. **Automated Stale Deal Alerts**
   - Need: >14 days in [04], >10 days in [03], >40 days any stage
   - Auto-flag in daily sync
```

#### Phase 3: Tomorrow's Setup
```markdown
## [NEXT DAY] PRIORITIES ([TIME])

1. [Known meeting/call with time]
2. [Expected deliverable]
3. [Pending responses to monitor]
4. [Blockers to resolve]
5. [Follow-up actions]
```

**Example**:
```markdown
## MONDAY PRIORITIES (Oct 7, 9AM)

1. Monitor 6 customer responses
2. **BLOCKER**: Brock data for DYLN
3. Stackd rate check (JIRA RATE-1897)
4. Upstate Prep follow-up
5. Execute 5 HubSpot tasks
```

#### Phase 4: SOP Evolution Tracking

**Version Control**:
```markdown
## SOP EVOLUTION LOG

### v3.X - [DATE] [STATUS]
**Changed**: [What changed]
**Reason**: [Why it matters]
**Result**: [What happened]
**Status**: PERMANENT | TESTING | PROPOSED
```

**Status Definitions**:
- **✅ PERMANENT**: Validated, now standard operating procedure
- **🟡 TESTING**: In trial period (1-2 weeks)
- **🔴 PROPOSED**: Identified, not yet implemented

**Example**:
```markdown
### v3.1 - Oct 3, 2025 ✅ PERMANENT
**Changed**: Customer Relationship Documentation mandatory for [01-QUALIFIED]+
**Reason**: Saved 30+ min per deal, zero info loss
**Result**: 4 docs created, clear action items
**Status**: PERMANENT
```

### Archive & Handoff

**Daily Archive**:
1. Save `_DAILY_LOG_FEEDBACK.md` to Downloads
2. Update `FOLLOW_UP_REMINDERS.txt` for tomorrow
3. Note critical blockers for 9AM sync

---

## End of Week Sync - Friday EOD

### Purpose
Weekly reflection, pipeline velocity analysis, next week planning, archive to Saner.ai.

### Execution

**File**: `_DAILY_LOG_FEEDBACK.md` (special Friday section)

### Process Flow

#### Phase 1: Week Summary Metrics
```markdown
## WEEK OF [DATE] SUMMARY

### Pipeline Metrics
- Deals Advanced: [count by stage transition]
- New Deals Created: [count]
- Closed Won: [count + value]
- Closed Lost: [count + loss reasons]

### Activity Metrics
- Total Customer Touchpoints: [count]
- Discovery Calls: [count]
- Proposal Presentations: [count]
- Rate Cards Delivered: [count]

### Efficiency Metrics
- Avg Days in [03-RATE-CREATION]: [days]
- Response Rate to Proposals: [%]
- Win Rate: [%]
```

#### Phase 2: SOP Evolution Summary
```markdown
## SOP CHANGES THIS WEEK

### Validated & Made Permanent ✅
- v3.1: Customer Relationship Docs
- v3.4: Internal dependency pre-check

### In Testing 🟡
- v3.2: Automated stale deal alerts (Week 2)
- v3.3: Multi-location discovery question (Week 1)

### Newly Proposed 🔴
- v3.5: Dedicated email for critical asks
```

#### Phase 3: Pipeline Health Analysis
```markdown
## PIPELINE HEALTH

### Bottlenecks Identified
- [03-RATE-CREATION]: 8 deals (2 over SLA)
- [04-PROPOSAL-SENT]: 3 deals (1 at 30 days)

### At-Risk Deals (>SLA)
1. Upstate Prep: $950K, 44 days in [03]
2. Caputron: $480K, 32 days in [04]

### Velocity Trends
- Avg time [02]→[03]: 12 days (target: <10)
- Avg time [03]→[04]: 18 days (target: <14)
- Avg time [04]→[07]: 45 days (target: <30)
```

#### Phase 4: Next Week Planning
```markdown
## WEEK OF [NEXT WEEK] PRIORITIES

### Critical Deals
1. DYLN: $3.6M - Unblock with Brock data
2. Stackd: Tue Oct 8 proposal presentation
3. Upstate Prep: $950K - Urgent reactivation

### Strategic Initiatives
1. Reduce [03] stage avg from 18d to 14d
2. Implement v3.2 (stale deal alerts)
3. Create competitor pricing database

### Known Meetings
- Tue Oct 8, 10AM: Stackd Logistics proposal
- [Other scheduled meetings]
```

#### Phase 5: Archive to Saner.ai

**Export Process**:
1. Copy week's learnings from `_DAILY_LOG_FEEDBACK.md`
2. Format for Saner.ai notes system
3. Tag with: `#sales #pipeline #learning #[week-of]`
4. Cross-reference with deal folders if needed

**Saner.ai Note Structure**:
```markdown
# Week of [DATE] - Pipeline Learnings

## Key Wins
[What worked this week]

## Critical Failures
[What failed and fixes implemented]

## Pattern Recognition
[Emerging patterns across deals]

## Strategic Insights
[Broader observations about sales process]

## Action Items for Next Week
[Carried forward priorities]
```

---

## Automated EOD Email Analysis Workflow

### Using Chrome DevTools MCP + Superhuman AI

**Prerequisites**:
1. Superhuman open in Comet browser at `https://mail.superhuman.com/`
2. Chrome MCP server connected to Claude Code
3. EOD analysis prompt saved at: `C:\Users\BrettWalker\Downloads\SUPERHUMAN_EOD_SEARCH_PROMPT.md`

**Step-by-Step Automation** (Run in Claude Code):

```
Step 1: List browser tabs
"List all open browser tabs using chrome-mcp-server"

Step 2: Navigate to Superhuman (if needed)
"Navigate to https://mail.superhuman.com/ using chrome-mcp-server"

Step 3: Access Superhuman AI
"In the open Superhuman tab, click the Superhuman AI button (selector: [data-test-id='ai-button'] or similar)"

Step 4: Enter search query
"Fill the search input with: in:sent OR in:inbox after:today"

Step 5: Submit EOD analysis prompt
"Read C:\Users\BrettWalker\Downloads\SUPERHUMAN_EOD_SEARCH_PROMPT.md and submit the full prompt to Superhuman AI"

Step 6: Extract AI response
"Wait for Superhuman AI to complete analysis, then extract the full response text"

Step 7: Parse and structure output
"Parse the AI response into 4 parts:
- Part 1 (Activity Summary) → Save to _DAILY_LOG.md
- Part 2 (Action Plan) → Save to FOLLOW_UP_REMINDERS.txt
- Part 3 (Pipeline Movements) → Append to _DAILY_LOG.md
- Part 4 (Metrics) → Display for review"

Step 8: Verify output
"Display summary of what was saved and confirm completion"
```

**Expected Output Files**:
- `C:\Users\BrettWalker\Downloads\_DAILY_LOG.md` - Updated with today's activity & pipeline movements
- `C:\Users\BrettWalker\Downloads\FOLLOW_UP_REMINDERS.txt` - Tomorrow's prioritized action plan
- Console display of daily metrics for review

**Simplified Command** (One-Shot):
```
"Run EOD sync: Use chrome-mcp-server to access Superhuman AI, execute the EOD email analysis prompt from SUPERHUMAN_EOD_SEARCH_PROMPT.md, and save structured output to _DAILY_LOG.md and FOLLOW_UP_REMINDERS.txt"
```

**Manual Fallback** (If automation fails):
1. Open Superhuman manually: `https://mail.superhuman.com/`
2. Click Superhuman AI button
3. Paste search query: `in:sent OR in:inbox after:today`
4. Copy full prompt from `SUPERHUMAN_EOD_SEARCH_PROMPT.md`
5. Paste prompt into Superhuman AI
6. Copy response and manually structure into output files

---

## Integration with Other Systems

### HubSpot Sync
**Frequency**: Real-time + Daily verification

**Daily Sync Check**:
```bash
python pipeline_sync_verification.py
```

**Outputs**:
- Stage alignment report (Folder vs HubSpot)
- Mismatch detection
- Recommended reconciliation actions

### N8N Automation
**Triggers**:
- Folder movement → HubSpot stage update
- Deal stage change → Email sequences
- Daily 9AM → Follow-up reminders

**Monitoring**:
- Check `AUTOMATION_MONITOR_LOCAL.html` (Desktop)
- Review `_DAILY_LOG.md` for automation activity

### Task Management
**HubSpot Tasks**:
- Created automatically by `daily_9am_sync.py`
- EMAIL type for follow-ups
- Due dates based on stage SLAs
- Associated with specific deals

**Verification**:
```bash
python daily_9am_sync.py  # Creates missing tasks
```

---

## Best Practices

### Timing Discipline
- **9AM Sync**: First thing, before email
- **NOON Check**: Set calendar reminder
- **EOD Sync**: Last 30min of workday
- **Friday EOD**: Extra 30min for week reflection

### Learning Capture Quality
**Good Learning**:
```markdown
✅ **Short, Dedicated Emails for Critical Asks**
   - DYLN dimensions request buried in long email → no response
   - Sent dedicated 3-line email → immediate reply
   - Impact: 48hr faster data collection
   - **KEEP**: One ask = one email for critical needs
```

**Poor Learning**:
```markdown
❌ "Emails sometimes don't work well"
   - No specificity
   - No measurable impact
   - No actionable fix
```

### Action Item Quality
**Good Action**:
```markdown
1. **Stackd Logistics - Proposal Presentation**
   - When: Tue Oct 8, 10AM CST
   - Who: Landon Richards (landon@stackdlogistics.com)
   - What: Present peer-reviewed rates (JIRA RATE-1897)
   - Prep: Run final PLD analysis, create deck
   - Goal: Verbal commitment to move [04]→[05]
```

**Poor Action**:
```markdown
1. "Follow up with Stackd"
   - No specificity
   - No timeline
   - No success criteria
```

### Blocker Management
**Escalation Criteria**:
- Blocking >$500K deal value
- Preventing >3 deals from advancing
- Delaying >7 days beyond SLA
- External dependency (customer data)

**Documentation**:
```markdown
ACTIVE BLOCKERS:
- **DYLN ($3.6M)**: Brock data needed for JIRA submission
  - Requested: Oct 3
  - Follow-up: Oct 7 (escalate if no response)
  - Impact: Cannot send rates to customer
  - Mitigation: None available
```

---

## Troubleshooting

### Sync Script Failures

**Issue**: `daily_9am_workflow.py` returns 401 error

**Fix**:
```bash
# Refresh HubSpot OAuth
/login

# Verify authentication
qm hubspot get-deal --deal-id [ANY-ID]

# Retry sync
python daily_9am_workflow.py
```

**Issue**: Pipeline sync shows mismatches

**Fix**:
```bash
# Run detailed verification
python pipeline_sync_verification.py

# Review mismatch report
# Manually reconcile folders vs HubSpot
```

### Learning Capture Issues

**Issue**: Forgot to capture EOD learnings

**Recovery**:
1. Review HubSpot activity log for the day
2. Check email sent folder for customer touchpoints
3. Reconstruct from memory (less ideal)
4. Set calendar reminder for tomorrow

**Issue**: Too many proposed SOPs, none implemented

**Fix**:
- Limit to 2-3 testing SOPs at a time
- Set 1-week validation period
- Force decision: PERMANENT, MODIFY, or ABANDON
- Clear old proposals monthly

---

## Metrics & KPIs

### Daily Sync Effectiveness
- **Execution Rate**: Actions completed / Actions planned
- **Target**: >85% completion daily

### Learning Velocity
- **SOPs Validated**: Count moved to PERMANENT
- **Target**: 1-2 per week

### Pipeline Health
- **SLA Compliance**: Deals within stage SLA / Total deals
- **Target**: >90% compliance

### Response Time
- **Customer Response**: Avg hours to respond
- **Target**: <4 hours business days

---

## Quick Reference Commands

### Daily Sync Scripts
```bash
# Morning sync
python daily_9am_workflow.py

# Task verification
python daily_9am_sync.py

# Pipeline alignment check
python pipeline_sync_verification.py

# HubSpot verification
python hubspot_pipeline_verify.py
```

### HubSpot MCP Commands
```bash
# Search deals
qm hubspot search-deals --owner-id 699257003

# Update deal stage
qm hubspot update-deal --deal-id [ID] --stage "[STAGE]"

# Create task
qm hubspot create-task --deal-id [ID] --title "[TITLE]" --due-date "YYYY-MM-DD"
```

### File Locations
```
Daily Logs: C:\Users\BrettWalker\Downloads\_DAILY_LOG_FEEDBACK.md
Pipeline DB: C:\Users\BrettWalker\Downloads\_PIPELINE_TRACKER.csv
Reminders: C:\Users\BrettWalker\Downloads\FOLLOW_UP_REMINDERS.txt
Dashboard: C:\Users\BrettWalker\Desktop\AUTOMATION_MONITOR_LOCAL.html
```

---

## Summary

The Daily Sync Operations system ensures:
1. **Morning Clarity**: Know exactly what to do each day
2. **Midday Adjustment**: Course-correct based on developments
3. **Evening Reflection**: Capture learnings while fresh
4. **Weekly Evolution**: Continuous improvement of sales process

**Success Formula**:
> Consistent Execution + Ruthless Learning Capture = Pipeline Velocity

---

**Last Updated**: October 7, 2025
**System**: Nebuchadnezzar v3.0
**Status**: Production Active
