# Claude Mobile + GitHub Integration Workflow

**Complete guide for iPhone access to Nebuchadnezzar v3.0 via Claude mobile app with GitHub connection**

---

## Setup (One-Time, 10 Minutes)

### 1. Claude Mobile App Setup
- App Store → Search "Claude"
- Install official Anthropic Claude app
- Sign in with your Claude account
- **Verify GitHub integration is connected**

### 2. Connect GitHub to Claude Mobile
1. Open Claude mobile app
2. Go to Settings → Integrations
3. Connect GitHub account (if not already connected)
4. Authorize access to repositories
5. Verify `walkervvv/FirstMile_Deals` appears in repo list

### 3. Test Repository Access
1. Start new conversation in Claude mobile
2. Type: "Show me the FirstMile_Deals repository structure"
3. Verify Claude can access repo files
4. Test: "Read the latest entry from _DAILY_LOG.md"

### 4. Supplementary Tools (Optional)
- **GitHub Mobile app** (for visual file browsing)
- **Mobile Dashboard bookmark**: `https://walkervvv.github.io/firstmile-deals-pipeline/mobile_review_dashboard.html`

---

## Daily Mobile Workflows

### 🌅 9 AM Sync (Morning Check - 5 Minutes)

**Location:** Anywhere with iPhone

#### Step 1: Open Claude Mobile with Repo Context
1. Open Claude mobile app
2. Start new conversation or continue existing
3. Type: **"Run 9 AM sync on FirstMile_Deals repo"**

**Claude Will Automatically:**
- Check overnight commits and automation activity
- Read latest _DAILY_LOG.md entry
- Check agent lock status
- Review pending automation branches
- Summarize overnight activity

#### Step 2: Review Claude's Morning Report
**What You'll Get:**
- Overnight automation summary (what merged, what's pending)
- Lock status (active/expired locks cleaned)
- Daily log highlights from yesterday
- Any urgent items flagged for attention
- Today's priorities from follow-up reminders

**Sample Mobile Prompt:**
```
"Morning sync for FirstMile_Deals:
1. Check overnight automation branches
2. Read latest from _DAILY_LOG.md
3. Check .git/agent_locks/ status
4. Summarize what needs attention today"
```

#### Step 3: Approve Automation Branches (If Needed)
**If Claude flags pending approvals:**
1. Ask: "Show me the automation branches pending approval"
2. Review complexity scores and changes
3. For safe branches: "Approve and merge automation/[branch-name]"
4. For risky branches: "Flag this for desktop review with reason"

**Mobile Commands You Can Use:**
- "Approve all safe automation branches" (complexity <0.3)
- "Show me what changed in automation/Stackd_followup"
- "Merge automation/Caputron_pld_test into main"

#### Step 4: Set Daily Context
**Ask Claude:**
```
"Based on today's priorities in FOLLOW_UP_REMINDERS.txt:
1. What are my top 3 actions today?
2. Any urgent customer follow-ups?
3. Pipeline deals needing attention?"
```

**Time Investment:** 3-5 minutes
**Output:** Complete morning briefing, automation approved, mental model established

---

### ☀️ Noon Check (Midday Status - 2 Minutes)

**Location:** Quick check during lunch or between meetings

#### Claude Mobile Quick Status
1. Open Claude mobile app
2. Type: **"Quick noon status check on FirstMile_Deals"**

**Claude Will Show:**
- New commits since morning (desktop work synced)
- Any automation triggered during morning session
- Pipeline status changes
- Urgent items (if any)

**Sample Mobile Prompt:**
```
"Noon check:
- What commits happened this morning?
- Any automation branches created?
- Pipeline deal updates?"
```

**Time Investment:** 1-2 minutes
**Output:** Confirmation work is progressing, catch any issues early

---

### 🌆 EOD Review (End of Day - 5 Minutes)

**Location:** Commute home, evening wind-down

#### Claude Mobile EOD Sync
1. Open Claude mobile app
2. Type: **"Run EOD review for FirstMile_Deals"**

**Claude Will Provide:**
- Today's accomplishments (from _DAILY_LOG.md)
- System health check (locks, git status)
- Pending automation branches for approval
- Tomorrow's priorities (from FOLLOW_UP_REMINDERS.txt)
- Any blockers or issues flagged

**Sample Mobile Prompt:**
```
"EOD sync for FirstMile_Deals:
1. Read today's entry from _DAILY_LOG.md
2. Check for pending automation branches
3. Verify agent lock status (should be 0)
4. Show tomorrow's top priorities
5. Any issues I should know about?"
```

#### Approve Pending Automation (If Any)
**If Claude shows pending branches:**
- "Approve all safe automation branches for overnight processing"
- "What's blocking automation/[branch-name] from auto-merge?"
- "Merge automation/[branch-name] to unblock overnight work"

**Time Investment:** 3-5 minutes
**Output:** Complete day summary, automation ready for overnight, tomorrow planned

---

## Desktop-to-Mobile Conversation Continuity

**This is where Claude Mobile + GitHub integration shines.**

### Seamless Context Switching

**Scenario:** You're working in Claude Code on desktop, need to step away, want to continue on iPhone.

#### Method 1: Continue Existing Work
**On Desktop (Claude Code):**
```
Working on: "Update OTW Shipping rate analysis"
- Made changes to deal folder
- Updated pricing matrix
- Need to review later
```

**On Mobile (Claude App):**
1. Open Claude mobile app
2. Start conversation: **"Continue OTW Shipping rate analysis from FirstMile_Deals repo"**
3. Claude accesses same repo via GitHub integration
4. Sees your recent commits and changes
5. Picks up where desktop left off

#### Method 2: Reference Desktop Work
**Ask Claude Mobile:**
```
"What was I working on last in FirstMile_Deals repo?
Show me the latest commits and what needs to be completed."
```

**Claude Will:**
- Read recent commit messages
- Check _DAILY_LOG.md for context
- Review FOLLOW_UP_REMINDERS.txt
- Summarize where you left off
- Suggest next actions

#### Method 3: Mobile-Initiated Work
**On Mobile:**
```
"In FirstMile_Deals repo, update the Stackd follow-up notes:
- Meeting scheduled for Monday 10 AM
- Need to prepare rate comparison
- Flag this for desktop review"
```

**On Desktop (Later):**
- Git pull shows mobile changes
- Daily log updated with your mobile notes
- Claude Code has full context of mobile work

### Key Advantage: Git as Sync Layer

**Everything syncs through GitHub:**
- Mobile commits → Visible on desktop immediately
- Desktop commits → Visible on mobile via `git pull`
- Daily logs → Shared context across devices
- Branch work → Accessible from both places

**You're not switching "conversations" - you're accessing the same repo state from different devices.**

---

## GitHub Mobile Quick Actions

### Approve Automation Branch (Without Dashboard)
1. GitHub Mobile app → Repo
2. Tap "Branches" → Find `automation/*` branch
3. Tap branch → Review files
4. Tap "..." → "Merge into main"
5. Confirm merge

### Review Recent Changes
1. Tap "Commits"
2. Tap specific commit
3. Scroll through changed files
4. Add comments if needed

### Check Lock Status
1. Navigate to `.git/agent_locks/` folder
2. Check for any `.lock` files
3. Tap file to view JSON content
4. Verify timestamps and expiration

### View Deal Folders
1. Navigate to stage folders (e.g., `[04-PROPOSAL-SENT]_CustomerName`)
2. Browse files within deal folder
3. Quick review of customer data or analysis

---

## Mobile Workflow Patterns

### Pattern 1: Morning Approval Workflow (iPhone + Coffee)
```
1. Open mobile dashboard (1 min)
2. Approve 2-3 automation branches (2 min)
3. Check daily log for context (2 min)
4. Mental model established → Start desktop work
```

### Pattern 2: Commute Review (iPhone on train/bus)
```
1. GitHub Mobile → Scan commits (2 min)
2. Read daily log entry (3 min)
3. Check follow-up reminders (2 min)
4. Flag anything urgent for later
```

### Pattern 3: Quick Status Check (iPhone anywhere)
```
1. Open mobile dashboard (30 sec)
2. Glance at automation status (30 sec)
3. GitHub notifications check (1 min)
4. Back to other activities
```

### Pattern 4: Evening Cleanup (iPhone before bed)
```
1. Approve pending automation branches (2 min)
2. Review EOD log entry (2 min)
3. Prep mental model for tomorrow (1 min)
4. System ready for overnight automation
```

---

## Key Mobile Bookmarks (Save in Safari/Chrome)

### Essential URLs
```
Mobile Dashboard:
https://walkervvv.github.io/firstmile-deals-pipeline/mobile_review_dashboard.html

Daily Log (GitHub):
https://github.com/walkervvv/FirstMile_Deals/blob/main/Downloads/_DAILY_LOG.md

Pipeline Tracker:
https://github.com/walkervvv/FirstMile_Deals/blob/main/Downloads/_PIPELINE_TRACKER.csv

Agent Locks:
https://github.com/walkervvv/FirstMile_Deals/tree/main/.git/agent_locks

Claude.ai Mobile:
https://claude.ai
```

### Quick Access Setup
1. Open each URL in Safari
2. Tap Share → "Add to Home Screen"
3. Name each bookmark clearly
4. Now one-tap access from iPhone home screen

---

## Troubleshooting Mobile Issues

### "I can't see recent commits in GitHub Mobile"
- Pull down to refresh repo view
- Check internet connection
- Verify repo name is correct (walkervvv/FirstMile_Deals)

### "Mobile dashboard shows old data"
- Refresh browser page
- Check GitHub Pages deployment status
- Verify you're on correct branch (main)

### "Lock files showing on mobile but not on desktop"
- Git sync lag - wait 1-2 minutes
- Run `git pull` on desktop
- Check lock_monitor.py ran successfully

### "Claude.ai mobile won't access repo files"
- Claude.ai mobile can't directly read private GitHub repos
- Must provide file URLs or copy/paste content
- Use GitHub Mobile app to view files first

---

## Integration with Desktop Workflow

### Morning: Mobile → Desktop Handoff
```
9:00 AM (iPhone):
- Review overnight automation via mobile dashboard
- Approve safe branches
- Check daily log

9:30 AM (Desktop):
- Claude Code session starts
- All mobile approvals already synced via Git
- Continue from where mobile review left off
```

### Midday: Desktop → Mobile Check-In
```
12:00 PM (Desktop):
- Complete morning work
- Commit to Git
- Update daily log if needed

12:15 PM (iPhone):
- Quick GitHub Mobile check
- Verify commits synced
- Review progress
```

### Evening: Desktop → Mobile → Overnight
```
6:00 PM (Desktop):
- Run EOD sync
- Update daily log
- Commit all changes

6:30 PM (iPhone):
- Review EOD log entry
- Approve any pending automation
- System ready for overnight automation

2:00 AM (Automated):
- N8N triggers automation
- Creates automation branches
- Ready for 9 AM mobile review
```

---

## Pro Tips for Mobile Efficiency

### 1. Use GitHub Mobile Notifications
- Enable push notifications for commits
- Get alerted when automation completes
- Quick check without opening app

### 2. Create iPhone Shortcuts
- Siri Shortcut: "Check FirstMile status" → Opens mobile dashboard
- Siri Shortcut: "Approve automation" → Opens GitHub Mobile at branches view

### 3. Dictate Notes to Daily Log
- Open GitHub Mobile → Navigate to _DAILY_LOG.md
- Tap "..." → "Open in browser"
- Use voice-to-text for quick notes

### 4. Star Important Commits
- Star commits on GitHub Mobile for later desktop review
- View all starred items: GitHub Mobile → Profile → Stars

### 5. Use "Watch" Feature
- Watch FirstMile_Deals repo for all activity notifications
- Customize notification settings per activity type

---

## Mobile Workflow Success Metrics

**You Know It's Working When:**
- ✅ Morning mobile check takes <5 minutes
- ✅ You approve 2-3 automation branches before desktop login
- ✅ EOD review on mobile gives clear picture of day
- ✅ No surprises when you open desktop Claude Code
- ✅ Git sync is seamless (mobile actions visible on desktop immediately)

**Signs You Need to Adjust:**
- ❌ Spending >10 minutes on mobile reviews
- ❌ Confusion about what happened overnight
- ❌ Git sync conflicts between mobile and desktop actions
- ❌ Forgetting to check mobile dashboard
- ❌ Missing automation branch approvals

---

## Emergency Mobile Protocols

### Critical Issue Detected on Mobile
1. Open claude.ai on iPhone browser
2. Start urgent conversation: "Emergency: [describe issue]"
3. Get immediate guidance
4. Flag for deep desktop session
5. Document in daily log via GitHub Mobile

### System Down (Can't Access Desktop)
1. GitHub Mobile → Check if commits are syncing
2. Mobile dashboard → Verify automation still running
3. Claude.ai mobile → Get guidance on next steps
4. Use GitHub Mobile to comment on issues
5. Document outage in daily log

### Automation Branch Stuck
1. Mobile dashboard → Review complexity score
2. GitHub Mobile → Check branch files
3. If safe: Approve merge via mobile dashboard
4. If risky: Flag for desktop review, add comment in GitHub Mobile
5. Document decision in daily log

---

## Quick Reference Card (Screenshot This)

```
9 AM MOBILE CHECK (5 MIN):
□ GitHub Mobile: Check overnight commits
□ Mobile Dashboard: Approve automation branches
□ Daily Log: Read yesterday's summary
□ Claude.ai: Address any issues

NOON CHECK (2 MIN):
□ GitHub Mobile: Check new activity
□ Notifications: Review any alerts

EOD REVIEW (5 MIN):
□ Daily Log: Read today's summary
□ Mobile Dashboard: Approve pending branches
□ Tomorrow: Mental prep for morning

KEY URLS:
• Dashboard: walkervvv.github.io/...
• Daily Log: github.com/.../Downloads/_DAILY_LOG.md
• Claude.ai: claude.ai

EMERGENCY:
1. GitHub Mobile → Check sync
2. Claude.ai → Get guidance
3. Document in daily log
```

---

**Workflow Status:** Ready for iPhone deployment
**Next Step:** Install GitHub Mobile app, bookmark key URLs, test 9 AM workflow tomorrow
**Maintenance:** Update bookmarks when URLs change, adjust timing based on actual usage

The Matrix is now mobile. Operate from anywhere, Brett.
