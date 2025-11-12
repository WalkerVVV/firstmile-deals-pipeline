# DAILY PIPELINE SYNC FLOWS - v3.0

**Self-Improving Schema with Continuous Feedback Loop**

---

## SYNC ARCHITECTURE CONSTANTS

### System Configuration
```yaml
OWNER_ID: 699257003
PIPELINE_ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
SYSTEM: NEBUCHADNEZZAR v3.0
MODE: QM3.1

FILE_PATHS:
  Context: C:\Users\BrettWalker\Downloads\_DAILY_LOG.md
  Actions: C:\Users\BrettWalker\Downloads\FOLLOW_UP_REMINDERS.txt
  Tracker: C:\Users\BrettWalker\Downloads\_PIPELINE_TRACKER.csv

HUBSPOT_FILTER_ALWAYS:
  hubspot_owner_id:eq:699257003 AND pipeline:eq:8bd9336b-4767-4e67-9fe2-35dfcad7c8be

STAGE_SLA_TARGETS:
  [01] Discovery Scheduled: 1 day
  [02] Discovery Complete: 48 hours
  [03] Rate Creation: 3-5 days
  [04] Proposal Sent: 14 days (Day 1/3/7/10/14 cadence)
  [05] Setup Docs: 48 hours
  [06] Implementation: 14 days
```

---

## 1. 9AM SYNC (Full Morning Context Load)

### TextExpander: `;9am` or `run 9am sync`

```markdown
run 9am sync

## NEBUCHADNEZZAR PIPELINE COMMAND
**OWNER LOCK: 699257003 | PIPELINE: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be**

### PHASE 1: CONTEXT LOADING (Yesterday → Today Continuity)

Load previous day's state:
1. Read _DAILY_LOG.md (yesterday's completions and context)
2. Load FOLLOW_UP_REMINDERS.txt (today's prioritized actions)
3. Execute memory:read_graph (load preserved conversation state)
4. Check desktop state (Windows-MCP:State-Tool with use_vision=true)

Acknowledge from yesterday's EOD:
- Deals moved/completed
- Unfinished action items (carry forward as Priority 1)
- Context to preserve (conversations, commits, objections)
- SLA deadlines that arrived today

### PHASE 2: LIVE DATA SYNC

Pull current pipeline state:
- HubSpot Pipeline: hubspot:search-objects
  FILTER: hubspot_owner_id:eq:699257003 AND pipeline:eq:8bd9336b-4767-4e67-9fe2-35dfcad7c8be
- Local tracker: filesystem:read_file(_PIPELINE_TRACKER.csv)
- Verify folder structure matches HubSpot stages

### PHASE 3: PRIORITY ANALYSIS

Stage priority sequence:
1. [04] PROPOSALS - Day 1/3/7/10/14 cadence check
2. [03] RATE CREATION - 3-5 day SLA verification
3. [05] SETUP DOCS - Contract acknowledgment status
4. [02] DISCOVERY COMPLETE - Rate request triggers
5. [01] DISCOVERY SCHEDULED - Meeting confirmations
6. [06] IMPLEMENTATION - Go-live readiness

Identify:
- SLA violations (overdue by stage)
- Follow-up triggers due today
- Deals needing immediate attention
- Pipeline bottlenecks

### PHASE 4: ACTION GENERATION

Generate:
- Priority action list (top 3-5 based on urgency + value)
- Overdue deal alerts with recommended actions
- Follow-up email templates by cadence day
- Task creation needs in HubSpot
- Voice briefing bullets (ADHD-friendly format)

### PHASE 5: DOCUMENTATION

Update:
- _DAILY_LOG.md with morning priorities
- Create missing HubSpot tasks
- Set next sync checkpoint (noon)

Output format:
- Bullet points for voice clarity
- Action items highlighted
- Summary before detail

End with:
- Pipeline health metrics (deal count by stage, total value)
- Critical deadlines approaching
- Next sync time: NOON (12:00 PM)

[MODE: QM3.1 ACTIVE]
[SYSTEM: NEBUCHADNEZZAR]
[OWNER: 699257003]
```

---

## 2. NOON SYNC (Quick Status Check)

### TextExpander: `;noon` or `run noon sync`

```markdown
run noon sync

## NEBUCHADNEZZAR MIDDAY CHECK
**OWNER LOCK: 699257003 | PIPELINE: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be**

### CONTEXT: Morning Progress Assessment

Load morning state:
1. Review 9am sync priorities (what was set as top 3-5)
2. Check HubSpot task completions since 9am
3. Review email inbox for prospect responses

### QUICK PULSE CHECK

Focus stages only:
- [04] PROPOSALS - Any responses received?
- [03] RATE CREATION - Progress on completions?

Pull from:
- HubSpot: FILTER: hubspot_owner_id:eq:699257003 AND pipeline:eq:8bd9336b-4767-4e67-9fe2-35dfcad7c8be
  AND dealstage:in:[Rate Creation, Proposal Sent]
- Recent email activity (last 3 hours)
- Completed tasks

### GENERATE

Morning completions:
- Emails sent
- Calls completed
- Tasks closed

Afternoon priorities (top 3 only):
- Urgent items requiring attention before 3pm
- Follow-ups that can't wait until EOD
- Quick wins available

Keep response under 5 bullet points for voice briefing.

[MODE: QM3.1 ACTIVE]
```

---

## 3. 3PM SYNC (Afternoon Checkpoint + Deal Documentation)

### TextExpander: `;3pm` or `run 3pm progress sync`

```markdown
run 3pm progress sync

## NEBUCHADNEZZAR AFTERNOON CHECKPOINT
**OWNER LOCK: 699257003 | PIPELINE: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be**

### CONTEXT: Today's Activity Documentation

Review since 9am:
1. Discovery calls completed
2. Proposals sent or acknowledged
3. Rate requests submitted
4. Any deal movements

### TODAY'S COMPLETIONS

Document:
- Discovery calls completed (add detailed notes to deals)
- Rate requests submitted to Jira (ticket numbers)
- Proposals acknowledged by prospects
- Follow-up emails sent (record in HubSpot)
- Verbal commits or objections received

### DEAL UPDATES REQUIRED

For each completed action:
- Add call outcome notes to HubSpot deal
- Update deal stage if criteria met
- Log verbal commits or objections
- Set next touch dates
- Create follow-up tasks if needed

Pull from:
- HubSpot: FILTER: hubspot_owner_id:eq:699257003 AND pipeline:eq:8bd9336b-4767-4e67-9fe2-35dfcad7c8be
- Today's call notes and email threads
- Jira ticket updates

### TOMORROW PREP

Calendar check:
- Tomorrow's scheduled calls/meetings
- Prep work needed tonight
- Materials to prepare

EOD priorities:
- What MUST finish today
- What can carry to tomorrow
- Critical deadlines approaching

Generate:
- Completed actions list
- EOD task list (what's left)
- Tomorrow's prep checklist

[MODE: QM3.1 ACTIVE]
[SYSTEM: NEBUCHADNEZZAR]
[OWNER: 699257003]
```

---

## 4. EOD SYNC (End of Day Wrap + Context Preservation)

### TextExpander: `;eod` or `run eod sync`

```markdown
run eod sync

## NEBUCHADNEZZAR END OF DAY WRAP
**OWNER LOCK: 699257003 | PIPELINE: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be**

### PHASE 1: TODAY'S SUMMARY

Full day accounting:

TODAY'S COMPLETIONS:
- Deals moved stages (FROM → TO with context)
- Follow-ups sent (who, what, expected response)
- Calls/meetings held (outcomes and next steps)
- Proposals delivered (deal value and details)
- Rate creations submitted (Jira tickets)
- Tasks completed in HubSpot

Pull from:
- HubSpot: FILTER: hubspot_owner_id:eq:699257003 AND pipeline:eq:8bd9336b-4767-4e67-9fe2-35dfcad7c8be
- Today's activity log
- Updated deal notes
- Email sent folder

### PHASE 2: TOMORROW PREP

MORNING PRIORITIES (for tomorrow's 9am sync):
- Unfinished items from today (carry forward as Priority 1)
- New urgent items discovered
- Scheduled calls/meetings tomorrow
- Follow-up triggers due tomorrow
- SLA deadlines approaching

CALENDAR CHECK:
- Tomorrow's meeting schedule
- Prep work needed
- Materials to gather

### PHASE 3: CONTEXT PRESERVATION (Critical for 9am continuity)

IMPORTANT CONVERSATIONS:
- Key discussions with prospects
- Pricing negotiations
- Technical requirements discovered
- Decision-maker insights

VERBAL COMMITS:
- Who committed to what
- Timeline expectations
- Next action dependencies

OBJECTIONS TO ADDRESS:
- Concerns raised
- Competitive pressures
- Budget constraints
- Internal approval processes

TECHNICAL REQUIREMENTS:
- Integration needs
- Custom reporting requests
- Special handling requirements
- Implementation dependencies

### PHASE 4: DOCUMENTATION

Update files for tomorrow's 9am sync:
1. _DAILY_LOG.md (full day summary with tomorrow's priorities)
2. FOLLOW_UP_REMINDERS.txt (tomorrow's action checklist)
3. memory:create_entities (save critical context)
4. Update _PIPELINE_TRACKER.csv if needed

File structure:
- Today's completions section
- Tomorrow's priorities section
- Context to preserve section
- SLA deadline tracking
- Pipeline health metrics

### PHASE 5: STATE CHECKPOINT

Generate tomorrow's opening checklist:
- Load these deals first
- Check these emails first
- Execute in this order
- Critical deadlines tomorrow

Pipeline health snapshot:
- Total deals by stage
- Pipeline value by priority
- Deals at risk (SLA violations)
- Win probability this week

Set next sync:
- Tomorrow 9:00 AM
- Expected priorities loaded
- Context ready for immediate execution

[MODE: QM3.1 ACTIVE]
[SYSTEM: NEBUCHADNEZZAR]
[OWNER: 699257003]
```

---

## 5. WEEKLY SYNC (Friday EOD - Full Diagnostic)

### TextExpander: `;weekly` or `run weekly pipeline analysis`

```markdown
run weekly pipeline analysis

## WEEKLY NEBUCHADNEZZAR DIAGNOSTIC
**OWNER LOCK: 699257003 | PIPELINE: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be**

### CONTEXT: Week in Review

Load week's activity:
1. Review all _DAILY_LOG.md entries from this week
2. Aggregate completions across Monday-Friday
3. Compare to weekly goals set last Friday

### PERFORMANCE METRICS

Win rate by stage:
- Lead → Discovery: X% (target: 25-30%)
- Discovery → Rate Creation: X% (target: 70-80%)
- Rate Creation → Proposal: X% (target: 95-100%)
- Proposal → Close: X% (target: 40-50%)
- Overall Lead → Active: X% (target: 7-12%)

Average days in stage (vs SLA targets):
- [01] Discovery Scheduled: X days (target: 1)
- [02] Discovery Complete: X days (target: 2)
- [03] Rate Creation: X days (target: 3-5)
- [04] Proposal Sent: X days (target: 14)
- [05] Setup Docs: X days (target: 2)
- [06] Implementation: X days (target: 14)

Stage velocity trends:
- Faster than last week (green flags)
- Slower than last week (red flags)
- Bottleneck identification

### PIPELINE HEALTH

Stuck deal analysis:
- Deals over 30 days in any stage
- Recommended actions (re-engage vs close-lost)
- Value at risk in stalled deals

Revenue forecast:
- Weighted by stage probability
- Expected closes next week
- Monthly target tracking
- Quarterly goal progress

Deal flow balance:
- Too heavy in one stage? (bottleneck warning)
- Healthy distribution across stages
- New lead generation needs

Follow-up compliance rate:
- Percentage of deals with active follow-up tasks
- Overdue tasks by deal
- SLA violation count

### STRATEGIC INSIGHTS

This week's wins:
- Top 3 deals closed or advanced
- Lessons learned from wins
- Replicable success patterns

This week's losses:
- Deals lost or stalled
- Why lost (competitive, pricing, timing)
- Process improvement opportunities

Emerging patterns:
- Common objections appearing
- Competitive threats increasing
- Market trends observed
- Process bottlenecks identified

### DATA SOURCES

Pull from:
- HubSpot: FILTER: hubspot_owner_id:eq:699257003 AND pipeline:eq:8bd9336b-4767-4e67-9fe2-35dfcad7c8be
- _PIPELINE_TRACKER.csv (historical comparison)
- All _DAILY_LOG.md entries from week
- Completed vs missed targets

### GENERATE

Weekly executive summary:
- Key performance indicators dashboard
- Week-over-week trend analysis
- Month-to-date tracking
- Action items for next week
- Stage-specific recommendations

Compare to:
- Last week's performance
- Monthly targets (progress %)
- Quarterly goals (on track?)
- Annual objectives

### NEXT WEEK PLANNING

Set priorities for Monday 9am:
- Top 3 deals to advance
- Critical follow-ups
- New lead outreach
- Process improvements to implement

[MODE: QM3.1 ACTIVE]
[SYSTEM: NEBUCHADNEZZAR]
[OWNER: 699257003]
```

---

## CONTINUOUS IMPROVEMENT SCHEMA

### Feedback Loop Architecture

```
EOD (Day N) → 9AM (Day N+1) → NOON → 3PM → EOD (Day N+1) → 9AM (Day N+2)
     ↓            ↓             ↓      ↓         ↓              ↓
  Context      Load         Quick   Document   Save         Load
  Save         Context      Check   Activity   Context      Context
     ↓            ↓             ↓      ↓         ↓              ↓
  DAILY_LOG → READ_LOG → UPDATE → ADD_NOTES → WRITE_LOG → READ_LOG
     ↓            ↓             ↓      ↓         ↓              ↓
Weekly Sync compiles all daily logs for trend analysis
```

### Self-Improvement Hooks

Each sync tracks:
- **What worked** - Successful patterns to replicate
- **What failed** - Process gaps to fix
- **What's unclear** - Ambiguities needing clarification
- **What's missing** - Tools or data needed

Weekly sync aggregates these to update:
- **SLA targets** (based on actual performance)
- **Priority scoring** (based on win patterns)
- **Follow-up cadence** (based on response rates)
- **Tool usage** (based on efficiency gains)

---

## TEXTEXPANDER SETUP

### Group Configuration
```yaml
Group Name: Daily Pipeline Sync Flows
Prefix: ; (semicolon)
```

### Abbreviations
| Abbreviation | Trigger | Timing | Purpose |
|--------------|---------|--------|---------|
| `9am` | `;9am` | Daily 9:00 AM | Full morning sync + consciousness |
| `noon` | `;noon` | Daily 12:00 PM | Quick status check |
| `3pm` | `;3pm` | Daily 3:00 PM | Afternoon checkpoint + notes |
| `eod` | `;eod` | Daily 5:00 PM | Day wrap + tomorrow prep |
| `weekly` | `;weekly` | Friday EOD | Full pipeline diagnostic |

---

## USAGE SCENARIOS

### Daily Flow
```
9am  → Load system, prioritize day
noon → Quick pulse check
3pm  → Document calls, prep tomorrow
eod  → Wrap day, preserve context
```

### Weekly Ritual (Fridays)
```
Run ;weekly at EOD
→ Review metrics vs targets
→ Identify stuck deals
→ Plan Monday priorities
```

---

## SYSTEM CONSTANTS (Always Applied)

### Owner/Pipeline Lock
Every sync MUST include:
```
hubspot_owner_id:eq:699257003
pipeline:eq:8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

This prevents pulling deals from:
- Other team members
- Other pipelines
- System-wide searches

### Tool Call Patterns
- **HubSpot**: `hubspot:search-objects` with owner/pipeline filters
- **Files**: `filesystem:read_file` for local context
- **Memory**: `memory:read_graph` for session continuity
- **Desktop**: `Windows-MCP:State-Tool` for visual state

### Data Sources Priority
1. Yesterday's EOD context (_DAILY_LOG.md)
2. Today's action items (FOLLOW_UP_REMINDERS.txt)
3. Live HubSpot state (API query)
4. Local tracker (_PIPELINE_TRACKER.csv)

---

## VERSION HISTORY

**v3.0** (October 2025)
- Added explicit context loading from previous day's EOD
- Continuous improvement schema with feedback loops
- Self-documenting architecture
- Consistent owner/pipeline locks across all syncs
- Clear phase structure for each sync

**v2.0** - Owner lock fix, TextExpander integration
**v1.0** - Initial sync flow structure

---

**Last Updated**: October 7, 2025
**System Status**: Active
**Maintained By**: Brett Walker
