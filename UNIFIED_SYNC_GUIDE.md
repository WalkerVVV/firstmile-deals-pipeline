# Unified Sync System - Quick Reference Guide

**Version**: 1.0
**Created**: November 11, 2025
**Purpose**: Single script for all sync times - eliminates format inconsistency

---

## 🎯 The Problem We Solved

**Before**: Multiple sync scripts with different formats
- `daily_9am_sync.py` → Comprehensive format ✅
- `eod_sync.py` → Basic format ❌
- `noon_sync.py` → Unknown format ❓
- `3pm_sync.py` → Unknown format ❓
- `end_of_week_sync_COMPLETE.py` → Weekly format ❓

**Result**: Format inconsistency, missing data, poor context preservation

**After**: ONE script (`unified_sync.py`) with comprehensive format for ALL syncs ✅

---

## 🚀 Quick Start

### Basic Usage

```bash
# Morning sync (with email integration)
python unified_sync.py 9am

# Mid-day progress check
python unified_sync.py noon

# Afternoon adjustment
python unified_sync.py 3pm

# End of day wrap
python unified_sync.py eod

# Weekly comprehensive sync
python unified_sync.py weekly

# Monthly analysis (future)
python unified_sync.py monthly
```

### Output Location

All syncs save to: `C:\Users\BrettWalker\Downloads\`

**Filename Format**: `[SYNC_TYPE]_SYNC_[TIMESTAMP].md`

Examples:
- `9AM_SYNC_20251111_090530.md`
- `NOON_SYNC_20251111_120145.md`
- `EOD_SYNC_20251111_170230.md`

---

## 📊 What Each Sync Includes

### ALL Syncs Include (Comprehensive Format):
✅ **HubSpot Priority Deals** - Live API data via prioritization agent
✅ **Pipeline Metrics** - Total deals, value, stage distribution
✅ **Recent Context** - Yesterday's activities and completions
✅ **Critical Follow-ups** - From FOLLOW_UP_REMINDERS.txt
✅ **System Status** - Chrome MCP, HubSpot API, agents

### 9AM Sync (ONLY):
✅ **Email Action Items** - Critical, yesterday, last 7 days (via Chrome MCP/Superhuman)
✅ **Brand Scout Results** - Overnight lead generation reports
✅ **Today's Execution Plan** - Morning & afternoon blocks

### NOON Sync:
✅ **Morning Progress Check** - What got completed
✅ **Afternoon Adjustments** - Updated priorities

### 3PM Sync:
✅ **Afternoon Status** - Today's completions
✅ **Final Push** - Items to complete before EOD

### EOD Sync:
✅ **Today's Completions** - Full day summary
✅ **Today's Learnings** - Key insights
✅ **Tomorrow's Priorities** - Top 3-5 for next day

### Weekly Sync:
✅ **Week in Review** - Major achievements
✅ **Pipeline Changes** - Deals moved, closed, added
✅ **Monday Priorities** - Week starter priorities

---

## 🔧 System Requirements

### Environment Variables (`.env`)
```bash
HUBSPOT_API_KEY=pat-na1-...  # Required
```

### Python Dependencies
```bash
python-dotenv
requests
```

### Optional Integrations
- **Chrome MCP** (port 12306) - For email integration in 9AM sync
- **Prioritization Agent** - `.claude/agents/prioritization_agent.py`
- **Brand Scout** - `.claude/brand_scout/` for overnight lead gen

---

## 📝 Daily Workflow Example

```bash
# Start your day
9:00 AM → python unified_sync.py 9am
# Review email action items, HubSpot priorities, execution plan

# Check progress
12:00 PM → python unified_sync.py noon
# Review morning completions, adjust afternoon plan

# Final check
3:00 PM → python unified_sync.py 3pm
# Ensure EOD priorities are clear

# Wrap up
5:00 PM → python unified_sync.py eod
# Document completions, learnings, tomorrow's priorities

# Weekend
Sunday EOD → python unified_sync.py weekly
# Week review and Monday preparation
```

---

## 🚨 Common Issues & Solutions

### Issue: "HUBSPOT_API_KEY not found"
**Solution**:
```bash
# Check .env file exists
ls .env

# Verify content
cat .env | grep HUBSPOT_API_KEY
```

### Issue: Chrome MCP disconnected (9AM sync)
**Symptoms**: Email action items unavailable
**Solution**:
```bash
# Restart Chrome MCP server
/mcp

# Or use manual email extraction from Superhuman
```

### Issue: Prioritization agent fails
**Symptoms**: "Prioritization agent failed to run"
**Solution**:
```bash
# Test agent directly
python .claude/agents/prioritization_agent.py

# Check for API errors or missing dependencies
```

### Issue: Old format syncs still running
**Problem**: Someone ran `eod_sync.py` instead of `unified_sync.py`
**Solution**:
- **Delete or rename** old sync scripts to prevent confusion:
  ```bash
  mv eod_sync.py eod_sync_DEPRECATED.py
  mv daily_9am_sync.py daily_9am_sync_DEPRECATED.py
  ```
- **Always use**: `python unified_sync.py [type]`

---

## 📋 Migration from Old Scripts

### Step 1: Backup Old Scripts
```bash
mkdir _DEPRECATED_SYNCS
mv daily_9am_sync.py _DEPRECATED_SYNCS/
mv eod_sync.py _DEPRECATED_SYNCS/
mv noon_sync.py _DEPRECATED_SYNCS/
mv 3pm_sync.py _DEPRECATED_SYNCS/
```

### Step 2: Update Automation
If you have any scheduled tasks (Task Scheduler, cron, etc.):

**Old**:
```bash
python daily_9am_sync.py
```

**New**:
```bash
python unified_sync.py 9am
```

### Step 3: Update Documentation
- Update `.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md`
- Update `CLAUDE.md` references
- Update any README files

---

## 🔍 Technical Details

### Architecture
- **Single Entry Point**: `unified_sync.py`
- **Parameter-Driven**: Sync type passed as CLI argument
- **Comprehensive Format**: ALL syncs use same rich format
- **Modular Functions**: Reusable across sync types

### Key Functions
- `run_prioritization_agent()` - HubSpot live data
- `check_chrome_mcp_status()` - Email integration status
- `extract_yesterday_context()` - Daily log parsing
- `extract_follow_up_reminders()` - Critical actions
- `check_brand_scout_reports()` - Overnight leads
- `generate_sync_report()` - Main report generator

### Output Format
- **Markdown** - Easy to read, version control friendly
- **Consistent Structure** - Same sections across all sync types
- **Timestamped** - Unique filename per sync
- **Comprehensive** - No data loss like old basic format

---

## 📊 Comparison: Old vs New

| Feature | Old System | Unified System |
|---------|------------|----------------|
| Scripts | 5+ separate files | 1 file |
| Format Consistency | ❌ Mixed | ✅ Unified |
| Email Integration | ❌ 9AM only | ✅ 9AM (expandable) |
| HubSpot Live Data | ⚠️ Sometimes | ✅ Always |
| Context Preservation | ⚠️ Basic format loses data | ✅ Comprehensive |
| Maintainability | ❌ Update 5 files | ✅ Update 1 file |
| Error Prone | ✅ High | ❌ Low |

---

## 🎯 Best Practices

### DO:
✅ Run `unified_sync.py` for ALL syncs
✅ Use correct sync type parameter
✅ Check Chrome MCP status before 9AM sync
✅ Review output file after each sync
✅ Keep `.env` file updated with valid API key

### DON'T:
❌ Use old sync scripts (daily_9am_sync.py, eod_sync.py, etc.)
❌ Skip sync types (run all: 9am, noon, 3pm, eod, weekly)
❌ Edit output files manually (regenerate if needed)
❌ Commit `.env` file to git (use `.env.example`)

---

## 🚀 Future Enhancements

### Planned Features:
- [ ] Automatic Chrome MCP restart if disconnected
- [ ] Email extraction automation (reduce manual work)
- [ ] Integration with N8N workflows
- [ ] Slack/Teams notifications for sync completion
- [ ] Monthly sync deep analysis
- [ ] Automated deal folder updates based on sync findings

---

## 📞 Support

### Issues?
1. Check this guide first
2. Review error message in terminal
3. Check `.env` file configuration
4. Test HubSpot API connection: `python test_hubspot_connection.py`
5. Verify Chrome MCP status: `netstat -ano | findstr "12306"`

### Documentation:
- **Main Docs**: `.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md`
- **HubSpot Integration**: `.claude/docs/workflows/HUBSPOT_WORKFLOW_GUIDE.md`
- **System Overview**: `CLAUDE.md`

---

## ✅ Quick Checklist

**Before First Use**:
- [ ] `.env` file exists with `HUBSPOT_API_KEY`
- [ ] Python dependencies installed (`pip install -r requirements.txt`)
- [ ] Prioritization agent working (`python .claude/agents/prioritization_agent.py`)
- [ ] Old sync scripts moved to `_DEPRECATED_SYNCS/`

**Daily Usage**:
- [ ] 9AM: `python unified_sync.py 9am` (with Chrome MCP)
- [ ] Noon: `python unified_sync.py noon`
- [ ] 3PM: `python unified_sync.py 3pm`
- [ ] EOD: `python unified_sync.py eod`

**Weekly**:
- [ ] Sunday EOD: `python unified_sync.py weekly`

---

**Version**: 1.0
**Last Updated**: November 11, 2025
**Script**: `unified_sync.py`
**Status**: ✅ Production Ready
