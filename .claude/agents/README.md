# Sales Discipline Agents

**Purpose**: Four specialized agents that force sales discipline and ensure revenue-generating activities always come before systems improvements.

**Coaching Context**: Based on coaching review that identified core issue: "Acting like systems engineer when need to act like sales hunter."

---

## 🎯 Core Philosophy

**Primary Directive**: "Revenue-generating activities ALWAYS come before systems improvements"

**Weekly Goals**: 5 new leads, 2 discovery calls, 3 proposals, 1 close per week

**Enterprise Focus**: Mega and enterprise deals ($1M+) require 10x attention and daily touchpoints

---

## 📦 The Four Agents

### 1. Sales Execution Agent

**Purpose**: Auto-generate urgency-based follow-up emails for stale proposals

**File**: `sales_execution_agent.py`

**Usage**:
```bash
python sales_execution_agent.py
```

**Features**:
- Scans `[04-PROPOSAL-SENT]` for stale deals
- Generates urgency emails based on stagnation days:
  - **Day 7**: Soft follow-up (check-in on proposal)
  - **Day 14**: Urgent follow-up (peak season capacity pressure)
  - **Day 21**: Final push (release capacity or reconnect Q1 2026)
  - **Day 60**: Win-back email (move to `[09-WIN-BACK]`)
- Extracts deal values and contact names from markdown docs
- Saves emails to deal folders for easy copy-paste

**Output**:
- `[04-PROPOSAL-SENT]_CustomerName/FOLLOWUP_EMAIL_YYYYMMDD.txt`
- Console report with stale deal rankings

**Automation**: Run daily or weekly to identify stagnant proposals

---

### 2. Brand Scout Automation Agent

**Purpose**: Automated brand research and lead generation for wellness/D2C brands

**File**: `brand_scout_agent.py`

**Usage**:

**On-demand mode** (single brand):
```bash
python brand_scout_agent.py "Athleta"
```

**Batch mode** (scheduled for Monday 6AM, 10 leads):
```bash
python brand_scout_agent.py --batch 10
```

**Features**:
- Creates structured brand profile templates
- Auto-generates `[00-LEAD]_BrandName` folders with `Customer_Relationship_Documentation.md`
- Identifies research gaps: company info, contacts, shipping carriers, decision makers
- Prepares HubSpot lead payloads
- Tracks research progress and next steps

**Input**:
- `.claude/brand_scout/input/brand_list.txt` (one brand per line)
- Includes sample list with 10 wellness/D2C brands

**Output**:
- Brand profiles: `.claude/brand_scout/output/BrandName_YYYYMMDD_HHMMSS.md`
- Deal folders: `[00-LEAD]_BrandName/`
- Batch summary with success/failure tracking

**Automation**:
- Schedule for Monday 6AM using Windows Task Scheduler or cron
- Run on-demand when discovering new leads

---

### 3. Weekly Metrics Tracker Agent

**Purpose**: Track weekly sales metrics and hold Brett accountable to 5/2/3/1 goals

**File**: `weekly_metrics_tracker.py`

**Usage**:

**Current week**:
```bash
python weekly_metrics_tracker.py
```

**Specific week**:
```bash
python weekly_metrics_tracker.py --week 2025-10-27
```

**Features**:
- Queries HubSpot API for deals in date range
- Tracks metrics: new leads, discovery calls, proposals sent, deals closed
- Calculates conversion rates:
  - Lead → Discovery (40% target)
  - Discovery → Proposal (75% target)
  - Proposal → Close (33% target)
  - Overall Lead → Close (10% target)
- Generates coaching feedback based on performance
- Creates actionable next week plan

**Output**:
- `~/Downloads/WEEKLY_METRICS_YYYY-MM-DD_to_YYYY-MM-DD.md`

**Performance Thresholds**:
- **4/4 goals**: Excellent week (sales hunter execution)
- **3/4 goals**: Strong week
- **2/4 goals**: Average week (increase activity)
- **1/4 goals**: Below target (focus on revenue activities)
- **0/4 goals**: Critical (sales execution required)

**Automation**: Run every Friday EOD or Monday 9AM for weekly review

---

### 4. Ruthless Prioritization Agent

**Purpose**: Ensure enterprise deals get 10x attention through scoring and time allocation

**File**: `prioritization_agent.py`

**Usage**:

**Full prioritization report**:
```bash
python prioritization_agent.py
```

**Daily reminder** (for 9AM sync):
```bash
python prioritization_agent.py --daily-reminder
```

**Features**:
- Comprehensive priority scoring algorithm (0-100):
  - **Deal size (50%)**: $10M+ mega, $1M+ enterprise, $500K+ mid-market
  - **Stage (20%)**: Later stages need more attention
  - **Stagnation (15%)**: Stale deals need immediate action
  - **Complexity (10%)**: Larger deals more complex
  - **Strategic (5%)**: Wellness/D2C bonus
- Calculates recommended time allocation per deal
- Generates daily priority reminders
- Tracks enterprise deal focus (target: ≥20% of time)

**Output**:
- Full report: `~/Downloads/PRIORITIZATION_REPORT_YYYYMMDD.md`
- Daily reminder: `~/Downloads/DAILY_PRIORITY_REMINDER.txt`

**Prioritization Rules**:
1. **Enterprise First**: Mega/Enterprise deals always come first
2. **Block Time**: Calendar-block daily hours for top 3 priorities
3. **Delegate Down**: Small deals (<$500K) should be delegated or automated
4. **Daily Touch**: Top deal gets touched every single day
5. **Stagnation Alert**: Deals >14 days stagnant need immediate action

**Automation**: Run daily during 9AM sync for priority reminder

---

## 🔄 Integration with Daily Sync System

### 9AM Sync
```bash
# Priority reminder
python .claude/agents/prioritization_agent.py --daily-reminder

# Check stale proposals
python .claude/agents/sales_execution_agent.py
```

### NOON Sync
- Review morning progress on top priority deal
- Address any blockers for enterprise deals

### 3PM Sync
- Ensure top priority moved forward today
- Generate urgency follow-ups if needed

### EOD Sync
- Log today's activity
- Prepare tomorrow's action queue

### Weekly (Friday EOD or Monday 9AM)
```bash
# Weekly metrics review
python .claude/agents/weekly_metrics_tracker.py

# Brand Scout batch (Monday 6AM)
python .claude/agents/brand_scout_agent.py --batch 10
```

---

## 📊 Expected Outcomes

### Sales Discipline
- ✅ No proposal sits >7 days without follow-up
- ✅ Enterprise deals receive 10x attention
- ✅ Weekly goals tracked and visible
- ✅ 5/2/3/1 cadence maintained

### Time Allocation
- ✅ Top deal gets daily touchpoint
- ✅ Enterprise deals blocked on calendar
- ✅ Small deals delegated or automated
- ✅ Priority drives daily schedule

### Pipeline Health
- ✅ Fresh leads added weekly (Brand Scout)
- ✅ Stagnant deals moved to win-back after 60 days
- ✅ Conversion rates tracked and improving
- ✅ Revenue activities always prioritized

---

## 🚀 Quick Start

1. **Morning Priority Check** (2 minutes):
   ```bash
   python .claude/agents/prioritization_agent.py --daily-reminder
   ```

2. **Weekly Proposal Scan** (5 minutes):
   ```bash
   python .claude/agents/sales_execution_agent.py
   ```

3. **Friday Metrics Review** (10 minutes):
   ```bash
   python .claude/agents/weekly_metrics_tracker.py
   ```

4. **Monday Lead Generation** (scheduled, 6AM):
   ```bash
   python .claude/agents/brand_scout_agent.py --batch 10
   ```

---

## 📝 Configuration

### Environment Variables
Agents use `.env` file for API credentials:
```bash
HUBSPOT_API_KEY=pat-na1-your-token-here
```

### Dependencies
All agents use standard library + requests:
```bash
pip install requests python-dotenv
```

### Customization
- **Stagnation rules**: Edit days in `sales_execution_agent.py`
- **Weekly goals**: Edit `WEEKLY_GOALS` in `weekly_metrics_tracker.py`
- **Priority scoring**: Edit `SCORING_WEIGHTS` in `prioritization_agent.py`
- **Brand list**: Edit `.claude/brand_scout/input/brand_list.txt`

---

## 🎯 Success Metrics

Track these over 4 weeks to measure agent impact:

1. **Proposal Velocity**: Average days from proposal to close
2. **Weekly Goal Achievement**: % of weeks hitting 5/2/3/1
3. **Enterprise Focus**: % of time on $1M+ deals
4. **Pipeline Health**: New leads per week, conversion rates
5. **Stagnation Reduction**: Deals >14 days in [04-PROPOSAL-SENT]

**Target**: Within 4 weeks, all 4 agents become daily habits and weekly metrics show consistent 3-4 goal achievement.

---

## 💡 Coaching Insights Integration

These agents directly implement coaching review findings:

> "You're acting like a systems engineer when you need to act like a sales hunter."

**Solution**: Agents force sales behavior by automating the discipline, not enabling more systems tinkering.

> "Revenue-generating activities ALWAYS come before systems improvements."

**Solution**: All 4 agents focus exclusively on revenue activities: follow-ups, lead generation, metrics tracking, prioritization.

> "5 new leads, 2 discovery calls, 3 proposals, 1 close per week"

**Solution**: Weekly Metrics Tracker holds Brett accountable to exact goals with coaching feedback.

> "Enterprise deals require enterprise attention"

**Solution**: Ruthless Prioritization Agent ensures $1M+ deals get 20%+ time allocation and daily touchpoints.

---

**Last Updated**: October 30, 2025
**System**: Nebuchadnezzar v3.0
**Owner**: Brett Walker
