# DAILY SYNC FLOWS - Quick Reference Card

**v3.0 - Self-Improving Pipeline Consciousness**

---

## ⚡ TEXTEXPANDER SHORTCUTS

| Time | Type | Command | Purpose |
|------|---------|---------|---------|
| 9:00 AM | `;9am` | `run 9am sync` | Full consciousness load + priorities |
| 12:00 PM | `;noon` | `run noon sync` | Quick progress check |
| 3:00 PM | `;3pm` | `run 3pm progress sync` | Document calls + tomorrow prep |
| 5:00 PM | `;eod` | `run eod sync` | Day wrap + context preservation |
| Friday EOD | `;weekly` | `run weekly pipeline analysis` | Full diagnostic + planning |

---

## 🔐 SYSTEM CONSTANTS (Always Applied)

```yaml
OWNER_ID: 699257003
PIPELINE_ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

FILTER (Every Query):
  hubspot_owner_id:eq:699257003 AND pipeline:eq:8bd9336b-4767-4e67-9fe2-35dfcad7c8be
```

---

## 🔄 FEEDBACK LOOP

```
EOD → Saves Context → 9AM → Loads Context → Acts → Documents → 3PM → Updates → EOD
  ↓                      ↓                        ↓               ↓         ↓
Daily Log           Read Log                 Add Notes      Document    Save State
```

**Critical Flow**:
1. **EOD** saves to `_DAILY_LOG.md` + `FOLLOW_UP_REMINDERS.txt` + memory
2. **9AM** loads all three sources + live HubSpot data
3. **3PM** documents activity + preps tomorrow
4. **EOD** preserves context for next day's 9AM

---

## 📊 9AM SYNC - Full Morning Load

**What It Does**:
- Loads yesterday's EOD context
- Pulls live HubSpot pipeline
- Generates priority action list (top 3-5)
- Identifies SLA violations
- Creates voice briefing bullets

**Key Phases**:
1. Context Loading (yesterday → today)
2. Live Data Sync (HubSpot + local files)
3. Priority Analysis (stage-based)
4. Action Generation (urgency + value)
5. Documentation (set next checkpoint)

**Output**: Priority list + overdue alerts + follow-up templates + pipeline health

---

## ⏱️ NOON SYNC - Quick Check

**What It Does**:
- Reviews morning priority completion
- Checks for prospect responses
- Sets afternoon focus (top 3 only)

**Keep It Short**: Under 5 bullet points for voice briefing

---

## 📝 3PM SYNC - Document & Prep

**What It Does**:
- Documents today's calls/emails/actions
- Updates HubSpot deal notes
- Checks tomorrow's calendar
- Creates EOD task list

**Critical**: Add call notes to HubSpot, set next touch dates

---

## 🌙 EOD SYNC - Context Preservation

**What It Does**:
- Full day summary (completions + movements)
- Tomorrow's priorities (for 9AM load)
- Context preservation (conversations, commits, objections)
- Files update (Daily Log, Reminders, Memory)

**Most Important Sync**: This feeds tomorrow's 9AM consciousness load

**Output**:
- Updated `_DAILY_LOG.md`
- Created `FOLLOW_UP_REMINDERS.txt`
- Saved to memory
- Tomorrow's opening checklist

---

## 📈 WEEKLY SYNC - Full Diagnostic

**What It Does**:
- Win rate by stage analysis
- Average days in stage vs SLA
- Stuck deal identification
- Revenue forecast
- Week-over-week trends
- Next week planning

**Run**: Friday EOD after daily EOD sync

---

## 🎯 STAGE PRIORITY ORDER

1. **[04] PROPOSALS** - Day 1/3/7/10/14 cadence
2. **[03] RATE CREATION** - 3-5 day SLA (BOTTLENECK)
3. **[05] SETUP DOCS** - 48-hour urgency
4. **[02] DISCOVERY COMPLETE** - Rate request triggers
5. **[01] DISCOVERY SCHEDULED** - Meeting confirmations
6. **[06] IMPLEMENTATION** - Go-live readiness

---

## 📁 FILE PATHS (v3.0 Schema)

```
Context:  C:\Users\BrettWalker\Downloads\_DAILY_LOG.md
Actions:  C:\Users\BrettWalker\Downloads\FOLLOW_UP_REMINDERS.txt
Tracker:  C:\Users\BrettWalker\Downloads\_PIPELINE_TRACKER.csv
```

---

## 🚨 SLA TARGETS

| Stage | Target | Alert Threshold |
|-------|--------|-----------------|
| [01] Discovery Scheduled | 1 day | >1 day |
| [02] Discovery Complete | 2 days | >2 days |
| [03] Rate Creation | 3-5 days | >5 days ⚠️ |
| [04] Proposal Sent | 14 days | >14 days |
| [05] Setup Docs | 2 days | >2 days ⚠️ |
| [06] Implementation | 14 days | >14 days |

---

## 🛠️ CONTINUOUS IMPROVEMENT

**Each sync captures**:
- ✅ What worked (replicate)
- ❌ What failed (fix)
- ❓ What's unclear (clarify)
- 🔧 What's missing (add)

**Weekly sync aggregates** → Updates SLA targets, priority scoring, follow-up cadence

---

## 💡 QUICK TIPS

1. **Always start with `;9am`** - It loads yesterday's context
2. **Never skip EOD** - It feeds tomorrow's 9AM
3. **3PM is for documentation** - Add notes BEFORE you forget
4. **Weekly sync on Fridays** - Sets Monday's priorities
5. **Voice briefing format** - Bullet points, summary before detail

---

## 🔗 FULL DOCUMENTATION

See [DAILY_SYNC_FLOWS_V3.md](DAILY_SYNC_FLOWS_V3.md) for complete prompts and workflows.

---

**Version**: 3.0
**Last Updated**: October 7, 2025
**System**: NEBUCHADNEZZAR
**Mode**: QM3.1
