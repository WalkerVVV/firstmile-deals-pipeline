# Daily Sync Pre-Flight Checklist

**Purpose**: Ensure all systems are ready for automated sync workflows

---

## 🔧 System Requirements

### Required BEFORE Running Any Sync

#### 1. Chrome MCP Server Status
- [ ] **Chrome MCP server connected** in Claude Code
- [ ] Comet browser running with Superhuman open: `https://mail.superhuman.com/`
- [ ] Test connection: Ask Claude "List browser tabs" - should return Superhuman tab

**Why Critical**:
- EOD sync uses Chrome MCP to access Superhuman AI for email intelligence
- Without it, EOD sync cannot extract today's activity from emails
- This feeds into tomorrow's 9AM sync action queue

**If Disconnected**:
```
1. Check Comet browser is running
2. Open Superhuman: https://mail.superhuman.com/
3. In Claude Code, verify Chrome MCP server shows "Connected"
4. Test: "List browser tabs" should show Superhuman
```

#### 2. Environment Variables
- [ ] `.env` file exists in project root
- [ ] `HUBSPOT_API_KEY` is set and valid
- [ ] Test: `python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ Valid' if os.getenv('HUBSPOT_API_KEY') else '❌ Missing')"`

**If Missing**:
```bash
# Check .env file
cat .env | grep HUBSPOT_API_KEY

# If missing, add:
echo "HUBSPOT_API_KEY=pat-na1-your-token-here" >> .env
```

#### 3. File Locations
- [ ] `~/Downloads/_DAILY_LOG.md` exists (or will be created)
- [ ] `~/Downloads/FOLLOW_UP_REMINDERS.txt` exists (or will be created)
- [ ] `~/Downloads/_DAILY_LOG_FEEDBACK.md` exists (or will be created)

#### 4. HubSpot API Access
- [ ] Token is valid (not expired)
- [ ] Owner ID: 699257003
- [ ] Pipeline ID: 8bd9336b-4767-4e67-9fe2-35dfcad7c8be

**Test**:
```bash
python daily_9am_sync.py | grep "Total Priority Deals"
# Should show: "Total Priority Deals: XX"
# If error: Check HUBSPOT_API_KEY in .env
```

---

## ⚡ Quick Health Check

Run this one-liner to verify everything:

```bash
cd c:/Users/BrettWalker/FirstMile_Deals && python -c "
import os, sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
checks = {
    'HUBSPOT_API_KEY': bool(os.getenv('HUBSPOT_API_KEY')),
    '_DAILY_LOG.md': (Path.home() / 'Downloads' / '_DAILY_LOG.md').exists(),
    'FOLLOW_UP_REMINDERS.txt': (Path.home() / 'Downloads' / 'FOLLOW_UP_REMINDERS.txt').exists(),
    'eod_sync.py': Path('eod_sync.py').exists(),
    'daily_9am_sync.py': Path('daily_9am_sync.py').exists()
}
print('\\n=== SYNC SYSTEM HEALTH CHECK ===\\n')
for name, status in checks.items():
    print(f'{'✅' if status else '❌'} {name}')
print('\\n⚠️  MANUAL CHECK: Chrome MCP server connected?')
print('   (In Claude Code, ask: \"List browser tabs\")')
"
```

Expected output:
```
=== SYNC SYSTEM HEALTH CHECK ===

✅ HUBSPOT_API_KEY
✅ _DAILY_LOG.md
✅ FOLLOW_UP_REMINDERS.txt
✅ eod_sync.py
✅ daily_9am_sync.py

⚠️  MANUAL CHECK: Chrome MCP server connected?
   (In Claude Code, ask: "List browser tabs")
```

---

## 📅 Daily Workflow with Checks

### Morning (9:00 AM)

1. **Pre-flight**:
   ```bash
   # Quick check
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ Ready' if os.getenv('HUBSPOT_API_KEY') else '❌ Check .env')"
   ```

2. **Run 9AM Sync**:
   ```bash
   python daily_9am_sync.py
   ```

3. **Verify Output**: Should show yesterday's context, HubSpot deals, Brand Scout reports

---

### End of Day (5:00 PM)

1. **Pre-flight**:
   - [ ] Chrome MCP server connected (CRITICAL)
   - [ ] Superhuman open in browser
   - [ ] `_DAILY_LOG.md` has today's activity logged

2. **Option A: Automated EOD (via Chrome MCP)**:
   ```
   In Claude Code:
   "Run EOD sync for today: Use chrome-mcp-server to access Superhuman AI at mail.superhuman.com, extract email analysis for TODAY's date, query HubSpot API for pipeline activity, generate _DAILY_LOG.md with comprehensive activity summary, create FOLLOW_UP_REMINDERS.txt with tomorrow's action queue, validate all dates are correct, and save both files to C:\Users\BrettWalker\Downloads\"
   ```

3. **Option B: Manual EOD (if Chrome MCP unavailable)**:
   ```bash
   python eod_sync.py
   ```
   Note: Manual version uses `_DAILY_LOG.md` as-is, doesn't pull from Superhuman

4. **Verify Output**:
   - `FOLLOW_UP_REMINDERS.txt` updated with tomorrow's date
   - EOD summary appended to `_DAILY_LOG.md`

---

### Weekend (Sunday/Monday AM)

1. **Pre-flight**: Same as daily

2. **Run Weekly Sync**:
   ```bash
   python end_of_week_sync_COMPLETE.py
   ```

3. **Verify Output**:
   - `WEEKLY_SYNC_YYYY-MM-DD_to_YYYY-MM-DD_COMPLETE.md` created
   - Contains Monday action queue with priority scores

---

## 🚨 Common Issues

### Issue: "HUBSPOT_API_KEY not found"
**Fix**:
```bash
# Check .env exists
ls -la .env

# If missing, create it
echo "HUBSPOT_API_KEY=pat-na1-your-token-here" > .env

# Verify it loads
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('HUBSPOT_API_KEY'))"
```

### Issue: "Chrome MCP server not connected"
**Fix**:
1. Check Comet browser is running
2. Open new tab: `https://mail.superhuman.com/`
3. In Claude Code settings, verify Chrome MCP server is enabled
4. Restart Claude Code if needed
5. Test: "List browser tabs"

### Issue: "No HubSpot deals returned"
**Fix**:
1. Check API token is valid (not expired)
2. Verify Owner ID: 699257003
3. Test with curl:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.hubapi.com/crm/v3/objects/deals/search" \
  -X POST -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"hubspot_owner_id","operator":"EQ","value":"699257003"}]}],"limit":1}'
```

### Issue: "Weekly sync report not found on Monday"
**Fix**:
1. Check `~/Downloads/` for `WEEKLY_SYNC_*_COMPLETE.md`
2. If missing, run: `python end_of_week_sync_COMPLETE.py`
3. Monday 9AM sync will find it automatically

---

## 📊 Health Dashboard

Create this alias for quick checks:

```bash
# Add to .bashrc or .bash_aliases
alias sync-check='cd ~/FirstMile_Deals && python -c "
import os, sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
print('\n🔍 SYNC SYSTEM STATUS\n')
print(f'API Key: {'✅' if os.getenv('HUBSPOT_API_KEY') else '❌'}')
print(f'Daily Log: {'✅' if (Path.home() / 'Downloads' / '_DAILY_LOG.md').exists() else '❌'}')
print(f'Follow-ups: {'✅' if (Path.home() / 'Downloads' / 'FOLLOW_UP_REMINDERS.txt').exists() else '❌'}')
print(f'9AM Sync: {'✅' if Path('daily_9am_sync.py').exists() else '❌'}')
print(f'EOD Sync: {'✅' if Path('eod_sync.py').exists() else '❌'}')
print('\n⚠️  Chrome MCP: (manual check in Claude Code)\n')
"'

# Then just run:
sync-check
```

---

## 🎯 Success Criteria

Before considering syncs "ready":

- ✅ All health checks pass (green checkmarks)
- ✅ Chrome MCP server shows "Connected" in Claude Code
- ✅ Superhuman accessible in browser
- ✅ Test 9AM sync runs without errors
- ✅ Test EOD sync can access Superhuman (or use manual fallback)

---

**Last Updated**: October 29, 2025
**System**: Nebuchadnezzar v3.0.1
**Purpose**: Daily sync system prerequisites and health checks
