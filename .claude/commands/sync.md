---
description: Run full sync with Chrome MCP email extraction (9am, noon, 3pm, eod, weekly, monthly)
---

Run the full **$ARGUMENTS** sync with complete email integration.

## Required Steps (Execute in Order)

### Step 1: Extract Superhuman Emails via Chrome MCP

1. Navigate to Superhuman:
   ```
   mcp__chrome-mcp-server__chrome_navigate → https://mail.superhuman.com/
   ```

2. Extract inbox content:
   ```
   mcp__chrome-mcp-server__chrome_get_web_content → textContent: true
   ```

3. Parse emails into structured format:
   - **critical**: Last few hours (urgent action needed)
   - **yesterday**: Previous day's emails
   - **last_week**: Last 7 days priorities

4. Save to `superhuman_emails.json` with format:
   ```json
   {
     "success": true,
     "timestamp": "ISO timestamp",
     "source": "Chrome MCP - Superhuman Important View",
     "critical": ["📧 **Sender** - Subject (time)"],
     "yesterday": [...],
     "last_week": [...],
     "mode": "live"
   }
   ```

### Step 2: Run Unified Sync

```bash
python unified_sync.py $ARGUMENTS
```

### Step 3: Report Results

Provide summary with:
- Email integration status
- Critical emails requiring action
- Top 3 pipeline priorities
- Pipeline snapshot (total deals, value, stage distribution)
- Any reminders from FOLLOW_UP_REMINDERS.txt

## Error Handling

**If Chrome MCP is unavailable**:
- Report the error clearly: "Chrome MCP server is not connected"
- Do NOT run partial sync without email data
- Do NOT create mock/placeholder email data

**If Superhuman requires login**:
- Report that authentication is needed
- Provide instructions to log in manually

## Valid Arguments

- `9am` - Morning priority report
- `noon` - Mid-day progress check
- `3pm` - Afternoon adjustment
- `eod` - End of day wrap-up
- `weekly` - Sunday comprehensive sync
- `monthly` - Month-end analysis

## Example Usage

```
/sync 9am
/sync eod
/sync noon
```
