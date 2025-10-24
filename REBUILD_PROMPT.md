# NEBUCHADNEZZAR v2.0 - AI Agent Rebuild Blueprint

## System Overview

Build a fully automated sales pipeline management system called "The Nebuchadnezzar v2.0" that manages FirstMile shipping solution deals through a 10-stage pipeline with zero manual data entry, real-time tracking, and intelligent workflow automation.

**Core Philosophy**: Pipeline consciousness through folder-based state management synced with HubSpot CRM, where moving folders triggers automation workflows and AI agents maintain complete context across sessions.

---

## Infrastructure Requirements

### 1. Data Layer Architecture

**HubSpot CRM Integration**
- API v3/v4 connectivity with personal access token authentication
- Owner lock: 699257003 (Brett Walker)
- Pipeline lock: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be
- Real-time deal search, stage updates, task creation, note association
- Association type 214 for deal-to-note linking

**Local Filesystem Structure**
```
C:/Users/BrettWalker/FirstMile_Deals/
├── [00-LEAD]_CompanyName/
├── [01-DISCOVERY-SCHEDULED]_CompanyName/
├── [02-DISCOVERY-COMPLETE]_CompanyName/
├── [03-RATE-CREATION]_CompanyName/
├── [04-PROPOSAL-SENT]_CompanyName/
├── [05-SETUP-DOCS-SENT]_CompanyName/
├── [06-IMPLEMENTATION]_CompanyName/
├── [07-CLOSED-WON]_CompanyName/
├── [08-CLOSED-LOST]_CompanyName/
└── [09-WIN-BACK]_CompanyName/
```

**State Persistence Layer**
```
C:/Users/BrettWalker/Downloads/
├── _PIPELINE_TRACKER.csv          # Master pipeline database
├── _DAILY_LOG.md                  # Context carry-forward document
└── FOLLOW_UP_REMINDERS.txt        # Next-day action queue
```

**Control Interfaces**
```
C:/Users/BrettWalker/Desktop/
├── AUTOMATION_MONITOR_LOCAL.html  # Real-time dashboard
└── NEBUCHADNEZZAR_CONTROL.bat    # Command center
```

### 2. Integration Points

**MCP Server Configuration**
- Notion integration via `@notionhq/notion-mcp-server` (stdio transport)
- API token: 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
- Configuration in `~/.claude/mcp_config.json`

**External Systems**
- Jira ticket tracking (RATE-1897 pattern for rate creation workflow)
- Email template generation (Markdown format)
- Excel report generation (firstmile_orchestrator.py pattern)

**N8N Automation Triggers**
- Watch folder: `C:/Users/BrettWalker/FirstMile_Deals/`
- Folder movement detection triggers stage-specific workflows
- Auto-update _PIPELINE_TRACKER.csv on folder changes

---

## Approach Methodology

### Core Design Patterns

**1. Pipeline-First Thinking**
- Folder location = source of truth for deal stage
- HubSpot mirrors folder structure (not vice versa)
- Moving folder = explicit stage transition signal
- Every stage has defined SLA window (14d or 30d)

**2. Urgency-Based Prioritization**

Urgency scoring algorithm (0-100 scale):
```
Base Score: 50

Modifiers:
+ Days in stage exceeds SLA → +30
+ Deal amount tier ($100K+) → +20
+ Recent activity (7d) → +20
+ Finish line stages (04-06) → +15
+ Engagement frequency → +10

Cap: 100 maximum
```

Scoring factors create actionable priority queues for daily workflow execution.

**3. Context Carry-Forward Architecture**

Every EOD wrap must preserve:
- Deals advanced with stage transitions
- Rate creations completed with Jira tickets
- Customer meetings held with action items
- Tasks created across all priority deals
- Value advanced (monthly + annual revenue)
- Tomorrow's morning priorities (6 items max)

State preservation enables AI agent to resume with full context at 9am sync.

**4. Workflow-Driven Task Management**

Stage-specific workflow templates:
```yaml
DISCOVERY-COMPLETE:
  sla_days: 30
  action: "Schedule follow-up call to discuss rate creation timeline"
  urgency_base: 60

RATE-CREATION:
  sla_days: 14  # Bottleneck stage
  action: "Complete rate calculation and prepare proposal materials"
  urgency_base: 75

PROPOSAL-SENT:
  sla_days: 30
  action: "Follow up on proposal review and schedule decision call"
  urgency_base: 70
```

**5. Visual Priority System Integration**

Three-tier priority system from HubSpot board screenshot:
- **Priority 1**: Red outline, immediate action required (today/tomorrow)
- **Priority 2**: Active follow-up, weekly progress expected
- **Priority 3**: Monitor and maintain, strategic advancement

AI agent translates visual board priorities into urgency scores and action queues.

**6. State-Based Automation**

Folder movement triggers:
```
[02] → [03]: Create rate calculation task, set 14-day SLA, add Jira ticket
[03] → [04]: Generate proposal email template, update HubSpot, create follow-up task
[04] → [05]: Mark verbal commitment, send setup docs, assign implementation owner
```

**7. Evidence-Based Deal Progression**

Required artifacts per stage:
- **[02-DISCOVERY-COMPLETE]**: PLD analysis report (`stackd_pld_discovery_report.md`)
- **[03-RATE-CREATION]**: Jira ticket reference (RATE-1897), rate calculation script
- **[04-PROPOSAL-SENT]**: Email template (`EMAIL_TO_MOHAMMAD.md`), rate comparison Excel
- **[05-SETUP-DOCS-SENT]**: Signed agreement, implementation plan

No stage advancement without evidence artifacts.

**8. Customer Intelligence Capture**

Meeting notes pattern (BoxiiShip example):
```markdown
## Meeting Context
- Attendees, date, duration
- Current performance metrics (93.67% SLA)
- Specific issues raised with examples

## Action Items Generated
1. Internal follow-up (Melissa encoding fix)
2. External opportunity (ACI Direct routing)
3. System improvements (JIRA ticket)
4. Data requests (pivot table creation)

## Financial Impact
- Opportunity sizing ($0.30/pkg × 2,800/mo = $840/mo)
- Implementation timeline
- Risk assessment
```

Transform meeting notes into HubSpot tasks with urgency scoring.

---

## Neural Pathway: One-Shot Build Sequence

### Phase 1: Foundation Layer (Steps 1-3)

**Step 1: HubSpot API Connectivity**
- Establish authentication with personal access token
- Verify owner lock (699257003) and pipeline lock (8bd9336b...)
- Create `fetch_priority_deals()` function with filters:
  - Owner ID match
  - Pipeline ID match
  - Stage filters for priority stages ([01] through [06])
- Test with deal count verification (109 total deals expected)

**Step 2: Local Filesystem Sync**
- Scan `C:/Users/BrettWalker/FirstMile_Deals/` for [STAGE]_CompanyName folders
- Build local pipeline inventory (30 active folders expected)
- Create mapping: folder location → HubSpot deal stage
- Identify discrepancies (79 deals = historical/closed, not in active folders)
- Establish folder movement detection mechanism

**Step 3: State Persistence Framework**
- Create `_PIPELINE_TRACKER.csv` schema:
  - deal_id, company_name, stage, days_in_stage, last_activity, deal_amount, jira_ticket
- Initialize `_DAILY_LOG.md` template with sections:
  - Pipeline status summary
  - Today's completions
  - Friday morning priorities
  - Context preserved
  - Success metrics
- Create `FOLLOW_UP_REMINDERS.txt` format:
  - Priority 1 (immediate)
  - Priority 2 (active)
  - Priority 3 (monitor)

### Phase 2: Intelligence Layer (Steps 4-6)

**Step 4: Urgency Scoring Engine**
- Implement `calculate_urgency_score(deal, workflow)` with factors:
  - Base score: 50
  - SLA overage: +30 if `days_in_stage > workflow["sla_days"]`
  - Deal amount: +20 if amount > $100K
  - Recent activity: +20 if last_activity < 7 days
  - Finish line bonus: +15 if stage in [04, 05, 06]
  - Engagement: +10 based on task completion rate
  - Cap at 100 maximum

**Step 5: Workflow Automation**
- Define stage-specific workflow templates (8 active stages)
- Create `create_email_task(deal_id, workflow)` function:
  - Subject: workflow["action"]
  - Priority: based on urgency score (HIGH >80, MEDIUM 60-80, LOW <60)
  - Due date: today + workflow["sla_days"]
  - Task type: EMAIL
  - Association: deal_id

**Step 6: Daily 9am Sync Flow**
- Build `daily_9am_workflow.py` orchestration:
  1. Fetch priority deals from HubSpot
  2. Calculate urgency scores for each deal
  3. Generate workflow-driven task recommendations
  4. Create missing EMAIL tasks in HubSpot
  5. Output formatted report with next steps
  6. Update _PIPELINE_TRACKER.csv with current state

### Phase 3: Intelligence Amplification (Steps 7-9)

**Step 7: Customer Meeting Intelligence**
- Create `parse_meeting_notes(notes_text)` function:
  - Extract attendees, date, context
  - Identify action items with regex/NLP
  - Calculate opportunity sizing from financial mentions
  - Assign urgency based on due dates and impact
- Implement `create_boxiiship_tasks(action_items, deal_id)`:
  - Convert action items to HubSpot tasks
  - Link to deal via association
  - Set priority (HIGH/MEDIUM/LOW)
  - Add detailed body with context

**Step 8: Deal Progression Automation**
- Build `move_deal_stage(company_name, from_stage, to_stage)`:
  1. Validate folder exists in from_stage
  2. Move folder to to_stage directory
  3. Update HubSpot deal stage via API
  4. Create stage-specific tasks (rate calc, proposal follow-up)
  5. Add Jira ticket if stage = [03-RATE-CREATION]
  6. Generate email template if stage = [04-PROPOSAL-SENT]
  7. Update _PIPELINE_TRACKER.csv
  8. Log to _DAILY_LOG.md

**Step 9: EOD Wrap Protocol**
- Implement `execute_eod_wrap()`:
  1. Scan _DAILY_LOG.md for today's activity
  2. Count deals advanced with stage transitions
  3. List rate creations completed with Jira tickets
  4. Summarize meetings held with action counts
  5. Calculate total value advanced (monthly + annual)
  6. Generate 6 Friday morning priorities based on:
     - Priority 1: Immediate actions (send proposal, follow-up due)
     - Priority 2: Active advancement (close deals, get commitments)
     - Priority 3: Strategic monitoring (schedule calls, maintain engagement)
  7. Write formatted _DAILY_LOG.md with context preservation
  8. Write FOLLOW_UP_REMINDERS.txt with opening checklist

### Phase 4: Integration & Resilience (Step 10)

**Step 10: Error Handling & Resilience**
- Implement encoding fix for Windows:
  ```python
  import io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
  ```
- Handle HubSpot API errors:
  - 401: OAuth token expired → prompt user to `/login`
  - 404: Property doesn't exist → fallback to notes (association type 214)
  - 429: Rate limit → exponential backoff
- Manage file locks on folder moves:
  - Catch "Device or resource busy" errors
  - Update HubSpot first, log folder move for manual completion
  - Add reminder to FOLLOW_UP_REMINDERS.txt
- Validate data integrity:
  - Verify deal counts match expected ranges
  - Check for orphaned folders (in filesystem but not HubSpot)
  - Alert on SLA violations (>30 days in RATE-CREATION)

---

## Success Criteria

**Daily Operation Metrics**
- 9am sync completes in <60 seconds
- All priority deals have EMAIL tasks in HubSpot
- Urgency scores accurately reflect manual priority rankings
- _DAILY_LOG.md preserves full context for next session

**Deal Progression Metrics**
- Stage transitions update both folder and HubSpot within 5 minutes
- Required artifacts present before stage advancement
- Jira tickets automatically added at [03-RATE-CREATION]
- Email templates auto-generated at [04-PROPOSAL-SENT]

**Intelligence Quality Metrics**
- Meeting notes parse with >90% action item extraction accuracy
- Opportunity sizing calculations match manual review
- Task priority assignments align with user confirmation
- Context carry-forward enables session resumption without clarification questions

**System Resilience Metrics**
- Graceful handling of HubSpot API failures
- File lock detection and workaround execution
- Encoding errors eliminated on Windows
- Data integrity validation catches discrepancies

---

## Sub-Agent Prompts for Parallel Work

### Agent 1: HubSpot Integration Specialist

**Objective**: Build robust HubSpot CRM API layer with authentication, deal management, task creation, and note association.

**Context**: You are integrating with HubSpot CRM v3/v4 API using personal access token authentication. The system manages 109 total deals across a 10-stage pipeline, with 30 active deals in priority stages. Owner lock is 699257003, pipeline lock is 8bd9336b-4767-4e67-9fe2-35dfcad7c8be.

**Deliverables**:
1. `hubspot_client.py` module with:
   - `authenticate()`: Handle personal access token, detect 401 errors
   - `fetch_priority_deals(owner_id, pipeline_id, stages)`: Search deals with filters
   - `update_deal_stage(deal_id, new_stage)`: Stage transition via API
   - `create_email_task(deal_id, subject, body, priority, due_date)`: Task creation with association
   - `create_note(deal_id, note_text)`: Note creation with association type 214

2. Error handling patterns:
   - OAuth token expiration detection and user prompts
   - Rate limiting with exponential backoff
   - Property validation fallback strategies
   - Detailed logging for debugging

3. Test coverage:
   - Verify 109 total deal count
   - Confirm 30 active deals in stages [01] through [06]
   - Validate task creation and association
   - Test note creation when properties don't exist

**Key Technical Constraints**:
- Use `requests` library for HTTP calls
- Base URL: `https://api.hubapi.com`
- Headers: `Authorization: Bearer {token}`, `Content-Type: application/json`
- Association type 214 for deal-to-note linking
- Windows encoding: UTF-8 with io.TextIOWrapper

**Success Criteria**:
- All API calls handle errors gracefully
- Authentication failures prompt user action
- 100% of tasks successfully associated with deals
- No data loss on API failures

---

### Agent 2: Workflow Automation Engineer

**Objective**: Build daily 9am sync workflow with urgency scoring, task creation, and actionable next-step recommendations.

**Context**: You are creating an automated workflow that runs every morning at 9am to analyze priority deals, calculate urgency scores, generate next-step actions, and create missing tasks in HubSpot. The system processes 14 priority deals totaling $187.9M across 3 active stages.

**Deliverables**:
1. `daily_9am_workflow.py` with:
   - `calculate_urgency_score(deal, workflow)`: 0-100 scoring algorithm
   - `generate_workflow_report(deals)`: Formatted report with next steps
   - `ensure_email_tasks_exist(deals)`: Create missing tasks
   - `main()`: Orchestration function

2. Urgency scoring implementation:
   ```python
   def calculate_urgency_score(deal, workflow):
       score = 50  # Base
       days_in_stage = calculate_deal_age(deal["properties"].get("createdate"))

       if days_in_stage > workflow["sla_days"]:
           score += 30

       deal_amount = float(deal["properties"].get("amount", 0))
       if deal_amount > 100000:
           score += 20

       last_activity = deal["properties"].get("notes_last_updated")
       if last_activity and days_since(last_activity) < 7:
           score += 20

       stage = deal["properties"].get("dealstage")
       if stage in ["proposal_sent", "setup_docs_sent", "implementation"]:
           score += 15

       return min(score, 100)
   ```

3. Stage-specific workflow templates:
   ```python
   WORKFLOWS = {
       "discovery_complete": {
           "sla_days": 30,
           "action": "Schedule follow-up call to discuss rate creation timeline",
           "goal": "Advance to rate creation stage"
       },
       "rate_creation": {
           "sla_days": 14,
           "action": "Complete rate calculation and prepare proposal materials",
           "goal": "Move to proposal sent stage"
       },
       # ... 6 more stages
   }
   ```

4. Formatted output report:
   ```
   === DAILY WORKFLOW REPORT ===
   Generated: 2025-10-02 09:00 MST

   PRIORITY 1 - IMMEDIATE ACTION
   1. [PROPOSAL-SENT] Team Shipper | $500K | Urgency: 95
      → Send proposal email with rate comparison Excel
      → Goal: Schedule decision call within 7 days

   PRIORITY 2 - ACTIVE ADVANCEMENT
   # ... additional deals
   ```

**Key Technical Constraints**:
- Run time: <60 seconds for 14 deals
- Output: Console report + HubSpot task creation
- Logging: All actions logged to _DAILY_LOG.md
- Dependencies: hubspot_client.py, datetime, json

**Success Criteria**:
- Urgency scores match manual priority rankings (1-2-3 system)
- All priority deals have EMAIL tasks after execution
- Report format is scannable in <30 seconds
- Zero duplicate task creation

---

### Agent 3: Priority Scoring Analyst

**Objective**: Translate visual HubSpot board priorities (red-outlined deals with 1-2-3 rankings) into algorithmic urgency scores and action queues.

**Context**: You are building the intelligence layer that converts subjective human prioritization into objective scoring criteria. The user marks deals on HubSpot board with red outlines and numbers 1, 2, or 3. You must reverse-engineer these patterns into scoring factors.

**Deliverables**:
1. `priority_analysis.py` with:
   - `analyze_visual_priorities(screenshot_data)`: Extract priority markers
   - `map_to_urgency_factors(priority_tier)`: Convert 1-2-3 to score modifiers
   - `validate_scoring_accuracy(predicted, actual)`: Compare AI scores to human rankings
   - `recommend_threshold_adjustments()`: Tune scoring algorithm

2. Priority tier mapping:
   ```python
   PRIORITY_MAPPING = {
       1: {  # Immediate action (red outline, number 1)
           "urgency_boost": +25,
           "due_date": "today or tomorrow",
           "action_type": "send proposal, close deal, critical follow-up"
       },
       2: {  # Active advancement (red outline, number 2)
           "urgency_boost": +15,
           "due_date": "this week",
           "action_type": "schedule call, get verbal commitment"
       },
       3: {  # Strategic monitoring (red outline, number 3)
           "urgency_boost": +5,
           "due_date": "this month",
           "action_type": "maintain engagement, prepare materials"
       }
   }
   ```

3. Scoring validation report:
   ```
   === PRIORITY SCORING VALIDATION ===

   Deal: Team Shipper
   Human Priority: 1
   AI Urgency Score: 95
   Factors: days_in_stage (+30), deal_amount (+20), finish_line (+15), priority_1 (+25)
   Match: ✓ Aligned

   Deal: Stackd Logistics
   Human Priority: 3
   AI Urgency Score: 72
   Factors: days_in_stage (+30), deal_amount (+20), priority_3 (+5)
   Match: ✓ Aligned
   ```

4. Threshold tuning recommendations based on mismatches

**Key Technical Constraints**:
- Input: Visual board screenshot + manual priority rankings
- Output: Urgency score adjustments for algorithm
- Validation: >90% alignment between AI scores and human priorities
- Feedback loop: Continuous learning from corrections

**Success Criteria**:
- Priority 1 deals always score >85 urgency
- Priority 2 deals score 70-85 urgency
- Priority 3 deals score 55-70 urgency
- Zero Priority 1 deals missed in action queue

---

### Agent 4: State Management Architect

**Objective**: Build state persistence layer that preserves complete context across sessions, enabling AI agent to resume at 9am with zero clarification questions.

**Context**: You are creating the memory system for "The Nebuchadnezzar v2.0" that maintains pipeline consciousness. Every night at EOD, the system must capture the day's activity and tomorrow's priorities such that the next morning's AI agent can execute without asking "where were we?"

**Deliverables**:
1. `state_manager.py` with:
   - `capture_eod_state()`: Scan day's activity and create summary
   - `load_morning_state()`: Read previous EOD state and initialize context
   - `update_pipeline_tracker(deal_updates)`: Maintain CSV database
   - `generate_follow_up_queue(priorities)`: Create next-day action list

2. _DAILY_LOG.md template:
   ```markdown
   # NEBUCHADNEZZAR DAILY LOG

   ## {DayOfWeek}, {Date} - END OF DAY WRAP

   ### PIPELINE STATUS
   - Total Deals: {total_deals} in HubSpot
   - Active Local Folders: {active_folders} deals
   - Pipeline Value (Priority 1-3): ${value}M across {count} deals
   - Owner Lock: {owner_id} ✓
   - Pipeline Lock: {pipeline_id} ✓

   ## ✅ TODAY'S COMPLETIONS

   ### DEALS MOVED STAGES ({count})
   1. {Company} (${value}) → [{stage}] ({jira_ticket})

   ### RATE CREATIONS COMPLETED ({count})
   - {Company}: {description}

   ### MEETINGS HELD ({count})
   - {Company} {contact}: {key_outcomes}

   ### FOLLOW-UPS
   - {Company}: {action_count} action tasks created

   ## 🎯 {NextDay} MORNING PRIORITIES ({date}, 9AM)

   PRIORITY 1 - IMMEDIATE:
   1. {Action} - {Details}

   PRIORITY 2 - ACTIVE:
   3. {Action} - {Details}

   PRIORITY 3 - MONITOR:
   5. {Action} - {Details}

   ## 💡 CONTEXT PRESERVED

   {Key_Deal}: {Critical_Context}

   ## 📊 SUCCESS METRICS - {Date}

   - Deals Advanced: {count}
   - Rate Creations: {count}
   - Tasks Created: {count}
   - Meetings: {count}
   - Value Advanced: ${monthly_value}K monthly (${annual_value}M annual)

   **[NEBUCHADNEZZAR v2.0 OPERATIONAL]**
   **[EOD: {timestamp}]**
   **State saved for {next_day} 9am sync**
   ```

3. FOLLOW_UP_REMINDERS.txt format:
   ```
   NEBUCHADNEZZAR v2.0 - {NextDay} MORNING ACTION QUEUE
   Generated: {timestamp}

   === OPENING CHECKLIST ===
   [ ] Check email for overnight responses
   [ ] Review HubSpot task queue
   [ ] Verify {critical_deal} readiness

   === PRIORITY 1 - IMMEDIATE ({count} actions) ===

   1. {Company} - {ACTION_TYPE}
      Deadline: {date}
      Context: {brief_context}
      Owner: {name}

   === PRIORITY 2 - ACTIVE ({count} actions) ===
   # ... similar structure

   === PRIORITY 3 - MONITOR ({count} actions) ===
   # ... similar structure

   === BLOCKERS & DEPENDENCIES ===
   - {Company}: {blocker_description}
   ```

4. _PIPELINE_TRACKER.csv schema:
   ```csv
   deal_id,company_name,stage,days_in_stage,last_activity,deal_amount,jira_ticket,priority,urgency_score,next_action,due_date
   ```

**Key Technical Constraints**:
- State capture must complete in <10 seconds
- Context preservation: 100% of critical details
- Morning load time: <5 seconds
- Format: Markdown for human readability, CSV for machine processing

**Success Criteria**:
- AI agent resumes next morning with zero clarification questions
- 100% of completed actions captured in EOD wrap
- 100% of tomorrow's actions in follow-up queue
- No context loss across sessions

---

### Agent 5: Email Template Generator

**Objective**: Auto-generate professional email templates for proposal delivery, follow-ups, and customer communications based on deal stage and context.

**Context**: You are creating the communication layer that transforms deal data and rate calculations into ready-to-send email templates. When a deal moves to [04-PROPOSAL-SENT], the system must generate a complete email with attachments guide, meeting scheduler, and value proposition.

**Deliverables**:
1. `email_generator.py` with:
   - `generate_proposal_email(company_name, contact_name, deal_context)`: Create proposal delivery template
   - `generate_follow_up_email(company_name, days_since_proposal, context)`: Follow-up reminders
   - `generate_setup_email(company_name, next_steps)`: Onboarding instructions
   - `insert_dynamic_content(template, variables)`: Variable substitution

2. EMAIL_TO_{CONTACT}.md template for proposals:
   ```markdown
   # Proposal Delivery Email - {Company}

   **To**: {contact_email}
   **Subject**: FirstMile Xparcel Rates - {Company} Shipping Solution
   **Attachments**:
   - Xparcel_Rate_Card_{Company}.xlsx
   - FirstMile_Service_Overview.pdf

   ---

   Hi {contact_first_name},

   Thank you for the opportunity to present FirstMile's Xparcel shipping solution for {Company}. Based on our discovery call and analysis of your shipping profile ({volume} shipments/month, {weight_profile}% under 1lb), I've prepared a customized rate proposal.

   ## What's Included

   **Rate Comparison Excel** (Tab 1 - Rate Card)
   - Zone-based pricing by weight tier (1-8 oz, 9-15 oz, 1-5 lbs)
   - Xparcel Ground (3-8 day), Expedited (2-5 day), Priority (1-3 day)

   **Savings Analysis** (Tab 2)
   - Current spend vs FirstMile projected costs
   - Estimated {savings_pct}% reduction = ${monthly_savings}K/month savings

   **Service Levels** (Tab 3)
   - National Network (100% ZIP coverage)
   - Select Network (metro injection points)
   - SLA windows and money-back guarantees

   ## How to Read the Rates

   1. **Find your destination zone** (Zones 1-8, based on origin-destination distance)
   2. **Select weight tier** (billable weight rounds UP to next tier)
   3. **Choose service level** (Ground for economy, Priority for speed)

   Example: 8 oz package to Zone 5 via Xparcel Ground = ${rate}

   ## Next Steps

   I'd like to schedule a 30-minute call to walk through the rates and answer any questions:

   **[Schedule Meeting Link]**

   In the meantime, feel free to review the attached materials. I'm available at {phone} or {email} if you'd like to discuss before our call.

   Looking forward to partnering with {Company}!

   Best regards,
   {sender_name}
   {sender_title}
   FirstMile
   ```

3. Follow-up email templates with stage-specific content:
   ```python
   FOLLOW_UP_TEMPLATES = {
       "proposal_sent_7_days": {
           "subject": "Following up - {Company} Xparcel Rates",
           "body": "Hi {name}, wanted to check if you had a chance to review..."
       },
       "proposal_sent_14_days": {
           "subject": "Quick question - {Company} shipping solution",
           "body": "Hi {name}, checking in to see if any questions came up..."
       },
       "proposal_sent_30_days": {
           "subject": "Touching base - FirstMile rates for {Company}",
           "body": "Hi {name}, wanted to reconnect on the Xparcel proposal..."
       }
   }
   ```

4. Dynamic content insertion with validation:
   ```python
   def insert_dynamic_content(template, variables):
       """
       Replace {variable_name} placeholders with actual values.
       Validate all required variables are provided.
       Return completed template or raise error on missing variables.
       """
       required = extract_placeholders(template)
       missing = [v for v in required if v not in variables]

       if missing:
           raise ValueError(f"Missing required variables: {missing}")

       return template.format(**variables)
   ```

**Key Technical Constraints**:
- Templates must be Markdown format for readability
- Variable placeholders: `{variable_name}` syntax
- Validation: All placeholders must be filled before output
- Attachments: List references, not actual files

**Success Criteria**:
- Zero manual email composition required
- 100% of proposal emails include rate card guide
- Follow-up timing matches stage SLA windows
- All dynamic content validated before sending

---

## System Integration Map

```
┌─────────────────────────────────────────────────────────────┐
│                    NEBUCHADNEZZAR v2.0                      │
│                 Pipeline Consciousness System                │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│   HubSpot    │      │  Filesystem  │     │     N8N      │
│   CRM API    │◄────►│    Sync      │◄───►│  Automation  │
│              │      │   (Folders)  │     │   Triggers   │
└──────────────┘      └──────────────┘     └──────────────┘
        │                     │                     │
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────────────────────────────────────────────────┐
│              State Persistence Layer                      │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────┐   │
│  │ _DAILY_LOG │  │ _PIPELINE_ │  │  FOLLOW_UP_     │   │
│  │    .md     │  │ TRACKER.csv│  │ REMINDERS.txt   │   │
│  └────────────┘  └────────────┘  └─────────────────┘   │
└──────────────────────────────────────────────────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │      Intelligence Layer                  │
        │  ┌──────────────────────────────────┐   │
        │  │  Urgency Scoring Engine          │   │
        │  │  Workflow Automation             │   │
        │  │  Email Template Generator        │   │
        │  │  Meeting Intelligence Parser     │   │
        │  └──────────────────────────────────┘   │
        └─────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────┐
        │       Daily 9am Sync Orchestrator       │
        │                                          │
        │  1. Fetch priority deals                │
        │  2. Calculate urgency scores            │
        │  3. Generate workflow tasks             │
        │  4. Create missing EMAIL tasks          │
        │  5. Output action queue                 │
        └─────────────────────────────────────────┘
```

---

## Rebuild Verification Checklist

### Infrastructure Layer
- [ ] HubSpot API authentication working with personal access token
- [ ] Folder structure created: [00-LEAD] through [09-WIN-BACK]
- [ ] State files initialized: _DAILY_LOG.md, _PIPELINE_TRACKER.csv, FOLLOW_UP_REMINDERS.txt
- [ ] MCP server configured: Notion integration via stdio
- [ ] Windows encoding fixed: UTF-8 with io.TextIOWrapper

### Intelligence Layer
- [ ] Urgency scoring algorithm implemented with 0-100 scale
- [ ] Stage-specific workflow templates defined (8 stages)
- [ ] Priority tier mapping created (1-2-3 system)
- [ ] Visual board priority translation working

### Automation Layer
- [ ] Daily 9am sync workflow functional
- [ ] Deal progression automation (folder move → HubSpot update)
- [ ] EOD wrap protocol generating _DAILY_LOG.md
- [ ] Follow-up queue creation for next morning

### Communication Layer
- [ ] Proposal email template auto-generation
- [ ] Follow-up email timing based on stage SLA
- [ ] Meeting notes parsing with action item extraction
- [ ] HubSpot task creation from action items

### Integration Layer
- [ ] Jira ticket auto-add at [03-RATE-CREATION]
- [ ] Email template generation at [04-PROPOSAL-SENT]
- [ ] Note association when properties don't exist (type 214)
- [ ] File lock handling for folder moves

### Validation Layer
- [ ] 109 total deals fetched from HubSpot
- [ ] 30 active folders match priority stages
- [ ] Urgency scores align with manual priorities (>90%)
- [ ] Context carry-forward enables zero-question resume

---

## Neural Pathway Summary

**Problem**: Manual pipeline management with fragmented context across HubSpot, local files, and memory.

**Solution**: Folder-based state machine synced with HubSpot, where physical folder location = source of truth, movement = state transition, and AI agent maintains consciousness across sessions through EOD state capture.

**Core Insight**: Pipeline management is fundamentally a state persistence problem. By externalizing state to filesystem structure and daily logs, the system achieves "stateless" AI agents with "stateful" pipeline consciousness.

**Implementation Path**: Build from foundation up (API → folders → state), add intelligence layer (scoring → workflows), automate daily operations (9am sync → EOD wrap), then amplify with communication templates and meeting intelligence.

**Success Metric**: AI agent executing Friday 9am sync with zero clarification questions after reading Wednesday EOD wrap = complete context preservation achieved.

---

**End of Rebuild Blueprint**
