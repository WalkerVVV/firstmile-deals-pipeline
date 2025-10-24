# Claude.ai Mobile Integration Guide

## Overview

Configure Claude.ai mobile app for on-the-go FirstMile Deals pipeline management. This guide enables quick decision-making, branch reviews, and deal updates from anywhere.

**Key Capabilities**:
- Review overnight automation results
- Approve safe branch merges
- Add notes to deal folders
- Check pipeline status
- Flag branches for desktop review

**Typical Use Cases**:
- Morning gym: Review overnight automation before arriving at office
- Commute: Approve straightforward changes while in transit
- Travel: Maintain pipeline visibility and make quick decisions
- After-hours: Emergency deal updates without desktop access

---

## Prerequisites

1. Claude.ai mobile app installed (iOS or Android)
2. GitHub account access configured
3. Mobile review dashboard deployed to GitHub Pages
4. N8N automation workflows running (Phase 2 complete)

---

## Quick Actions Setup

### Quick Action 1: "Show overnight results"

**Purpose**: Review automation results from overnight N8N workflows

**Prompt**:
```
Check FirstMile_Deals_Pipeline repository for branches created overnight (automation/*).

Show me:
1. Pending reviews with deal name and action
2. Auto-merge candidates (≤3 files, no deletions, no Python/config)
3. Branches needing desktop review
4. Brief summary of each change

Format as a mobile-friendly list with approve/defer recommendations.
```

**When to use**: First thing in morning, review overnight automation before desktop login

**Expected output**:
```
OVERNIGHT AUTOMATION RESULTS
============================

AUTO-MERGE CANDIDATES (Safe):
✓ automation/caputron_pld_analysis
  - Files: 1 (PLD_Analysis_Summary.xlsx)
  - Action: Added PLD analysis results
  - Recommendation: APPROVE ✓

DESKTOP REVIEW NEEDED:
⚠ automation/stackd_rate_update
  - Files: 4 (includes Python script)
  - Action: Updated rate calculation logic
  - Recommendation: DESKTOP REVIEW

STATUS: 1 safe for mobile approval, 1 needs desktop
```

---

### Quick Action 2: "Approve pending branches"

**Purpose**: List all safe branches ready for immediate approval

**Prompt**:
```
List all automation/* branches in FirstMile_Deals_Pipeline that meet auto-merge criteria:
- ≤3 files changed
- No deletions
- No .py, .json, .yml, .yaml, or .env files

For each safe branch show:
1. Deal company name
2. Action taken
3. Files modified
4. Approve command

Present as numbered list with GitHub API merge commands I can execute.
```

**When to use**: When you have 5 minutes and want to clear low-risk approvals

**Expected output**:
```
SAFE FOR APPROVAL
=================

1. automation/caputron_pld_analysis
   Company: Caputron Medical Products
   Action: Added PLD analysis summary
   Files: PLD_Analysis_Summary.xlsx

   To approve, visit:
   https://walkervvv.github.io/firstmile-deals-pipeline/mobile_review_dashboard.html

2. automation/otw_followup_day14
   Company: OTW Shipping
   Action: Added 14-day follow-up email
   Files: Follow_Up_Emails/Day_14.md

   To approve, visit:
   https://walkervvv.github.io/firstmile-deals-pipeline/mobile_review_dashboard.html
```

---

### Quick Action 3: "Add note to deal"

**Purpose**: Quick deal folder updates from mobile

**Prompt**:
```
I want to add a note to a FirstMile deal's Customer_Relationship_Documentation.md file.

Ask me:
1. Company name (e.g., "Caputron", "OTW", "Stackd")
2. Note content (what happened, decisions, next steps)

Then:
1. Find the deal folder matching that company
2. Create mobile/[company]_note_[MMDD] branch
3. Append note to Customer_Relationship_Documentation.md with timestamp
4. Commit with message: "[MOBILE] Added note to [Company] - [brief summary]"
5. Give me the GitHub link to review and merge

Use conversational format with simple questions.
```

**When to use**: After phone calls, meetings, or quick updates while mobile

**Example conversation**:
```
Claude: Which company do you want to add a note for?

You: Caputron

Claude: Got it - Caputron Medical Products. What's the note?

You: Just got off call with John. He's ready to move forward, wants to schedule implementation call for next Tuesday at 2 PM EST. I'll send calendar invite Monday.

Claude: Perfect! I'll add this note to Caputron's relationship documentation.

Branch created: mobile/caputron_note_1024
Note added with timestamp: 2025-10-24 14:32 EST

Review and merge here:
https://github.com/WalkerVVV/firstmile-deals-pipeline/compare/mobile/caputron_note_1024

Would you like me to flag this for any follow-up actions?
```

---

### Quick Action 4: "Show pipeline status"

**Purpose**: High-level pipeline overview for quick status checks

**Prompt**:
```
Show me the current state of my FirstMile deals pipeline using the FirstMile_Deals_Pipeline repository.

Analyze all [##-STAGE]_CompanyName/ folders and provide:

1. DEAL COUNT BY STAGE:
   - Active deals per stage
   - Total pipeline count

2. RECENT ACTIVITY (Last 24 hours):
   - New commits by stage
   - Branches pending review
   - Automation actions

3. ATTENTION NEEDED:
   - Stale deals (no activity >14 days)
   - Pending reviews >48 hours
   - Failed automation (if any)

4. TODAY'S PRIORITIES:
   - Top 3 deals needing action
   - Recommended next steps

Format as mobile-friendly dashboard with emojis for quick scanning.
```

**When to use**: Morning overview, end-of-day check, or when asked "How's the pipeline?"

**Expected output**:
```
FIRSTMILE PIPELINE STATUS
=========================
📊 54 Active Deals | 🟢 Pipeline Healthy

BY STAGE:
--------
01-DISCOVERY-SCHEDULED: 8 deals
02-DISCOVERY-COMPLETE: 5 deals
03-RATE-CREATION: 12 deals ⚠ (bottleneck)
04-PROPOSAL-SENT: 15 deals
05-SETUP-DOCS-SENT: 3 deals
06-IMPLEMENTATION: 4 deals
07-CLOSED-WON: 7 deals

RECENT ACTIVITY (24h):
---------------------
✓ 3 automation commits
✓ 2 PLD analyses completed
⏳ 1 branch pending review

ATTENTION NEEDED:
-----------------
⚠ 3 deals stale >14 days (03-RATE-CREATION)
✓ No pending reviews >48h
✓ No failed automation

TODAY'S TOP 3:
--------------
1. Caputron - Approve PLD analysis
2. Stackd - Follow up on proposal (Day 14)
3. OTW - Complete rate sheet (in progress)
```

---

## Home Screen Shortcuts

### iOS (Siri Shortcuts)

**Setup**:
1. Open Shortcuts app
2. Create new shortcut
3. Add "Ask ChatGPT/Claude" action
4. Select Claude.ai app
5. Paste Quick Action prompt
6. Name shortcut (e.g., "Pipeline Status")
7. Add to Home Screen

**Recommended Shortcuts**:
- "Overnight Results" (morning routine)
- "Pipeline Status" (any time)
- "Add Deal Note" (after calls/meetings)

**Hey Siri Integration**:
- "Hey Siri, Overnight Results" → Automatic morning briefing
- "Hey Siri, Pipeline Status" → Instant overview

---

### Android (Google Assistant Routines)

**Setup**:
1. Open Google Assistant app
2. Settings → Routines
3. Create new routine
4. Trigger: Voice command or time-based
5. Action: Open Claude.ai with prompt
6. Name and save

**Recommended Routines**:
- Morning: 7:00 AM → "Show overnight results"
- Commute: Location-based → "Pipeline status"
- Evening: 6:00 PM → "Show today's activity"

---

## Mobile Workflow Examples

### Example 1: Morning Gym Approval (5 minutes)

**7:15 AM - Between sets**:
```
1. Say: "Hey Siri, Overnight Results"
2. Review: 2 branches created overnight
   - Caputron PLD analysis (1 file, SAFE)
   - OTW follow-up email (1 file, SAFE)
3. Open mobile dashboard on phone
4. Tap "Approve & Merge" for both
5. Done - back to workout
```

**Result**: Pipeline cleared before arriving at office

---

### Example 2: Commute Update (2 minutes)

**8:30 AM - On train**:
```
1. Just finished call with Stackd Logistics
2. Open Claude.ai mobile app
3. Tap "Add Deal Note" quick action
4. Input: "Stackd", "Rate approved! Scheduling implementation call"
5. Review branch on phone, approve merge
6. Done - note documented
```

**Result**: Call notes captured immediately, no desk work needed

---

### Example 3: After-Hours Emergency (10 minutes)

**7:45 PM - At home**:
```
1. HubSpot notification: Urgent Caputron question
2. Need to check deal status and recent analysis
3. Open Claude.ai mobile app
4. Ask: "Show me all recent activity for Caputron deal"
5. Review PLD analysis results from morning
6. Copy key savings numbers to respond to email
7. Add note about evening call
```

**Result**: Customer question answered without booting up desktop

---

## File Access Configuration

### Option 1: GitHub File Viewer API (Recommended)

Claude.ai can access files directly via GitHub API:

**Setup**:
```
In Claude.ai app:
1. Settings → Integrations
2. Add GitHub integration
3. Grant repository access: WalkerVVV/firstmile-deals-pipeline
4. Scope: Read repository content, branches, commits
5. Test access: Ask Claude to "show me README.md"
```

**Capabilities**:
- Read any file in repository
- View commit history
- Compare branches
- **Cannot**: Write files directly (use Quick Actions for branch creation)

---

### Option 2: Cloud Sync Access

If using OneDrive/Google Drive sync for FirstMile_Deals folder:

**Setup**:
```
1. Sync C:\Users\BrettWalker\FirstMile_Deals\ to cloud
2. In Claude.ai app, grant cloud storage access
3. File path: [Cloud]/FirstMile_Deals/
```

**Considerations**:
- Larger context window usage
- Sync delays (may see stale data)
- Better for deep file analysis
- GitHub API method preferred for real-time data

---

## Security Best Practices

### 1. GitHub PAT Management

**Mobile Dashboard Token**:
- Use read-only Personal Access Token
- Scope: `repo` (or `public_repo` if repository is public)
- **Never share** token in screenshots or messages
- Rotate token every 90 days
- Store in browser localStorage (auto-cleared on logout)

---

### 2. Claude.ai Conversation History

**Privacy Settings**:
```
Claude.ai App → Settings → Privacy:
- ✓ Enable conversation history (for context)
- ✓ Exclude sensitive data from training
- ✓ Auto-delete conversations > 30 days
```

**Sensitive Data**:
- Don't paste actual API keys in Claude.ai conversations
- Reference deals by company name, not customer contact details
- Use generic descriptions for confidential rate information

---

### 3. Mobile Device Security

**Requirements**:
- Phone passcode/biometric lock enabled
- Auto-lock timeout ≤ 2 minutes
- Claude.ai app protected by Face ID/Touch ID
- Regular OS security updates

---

## Troubleshooting

### Issue: Quick Actions not saving

**Solution**:
- Close and reopen Claude.ai app
- Re-create quick action with simpler prompt
- Check app version (update if needed)

---

### Issue: Mobile dashboard shows "Authentication Required"

**Solution**:
- Tap "Setup Token" in dashboard
- Generate new GitHub PAT with `repo` scope
- Paste token and save
- Refresh dashboard

---

### Issue: Claude.ai can't access repository files

**Solution**:
- Verify GitHub integration connected
- Check repository permissions in GitHub settings
- Try OAuth re-authentication
- Use file path format: `[CompanyName]/filename.md`

---

### Issue: Slow dashboard loading on mobile

**Solution**:
- Check mobile data/WiFi connection
- Clear browser cache
- Use GitHub Mobile app as backup
- Wait for auto-refresh (60 seconds)

---

## Performance Tips

### 1. Optimize Quick Action Prompts

**Good** (concise, specific):
```
"List automation/* branches created in last 24 hours that are safe to merge. Show: company, action, files."
```

**Bad** (verbose, vague):
```
"Please take a look at my repository and see if there are any branches that might have been created by the automation system overnight and let me know if any of them look safe to merge..."
```

---

### 2. Pre-load Common Views

Before leaving desktop:
1. Open mobile dashboard in phone browser
2. Authenticate with GitHub PAT
3. Bookmark page for instant access
4. Test approve/reject buttons work

---

### 3. Batch Approvals

Instead of:
- Approve branch 1
- Wait for merge
- Approve branch 2
- Wait for merge

Do:
- Review all branches first
- Approve safe ones in sequence
- Desktop review complex ones later

---

## Testing Checklist

After setup, test each workflow:

- [ ] **Overnight Results**: Can you see branches from automation?
- [ ] **Approve Branches**: Do approve buttons work?
- [ ] **Add Note**: Can you create mobile/* branch?
- [ ] **Pipeline Status**: Does it show accurate deal counts?
- [ ] **GitHub PAT**: Does mobile dashboard authenticate?
- [ ] **Push Notifications**: Do you get real-time alerts?
- [ ] **Quick Access**: Is dashboard bookmarked?
- [ ] **Siri/Google Shortcuts**: Do voice commands work?

---

## Next Steps

After completing this guide:

1. **Test Mobile Workflow** (Task 3.4):
   - Create test branches
   - Approve via mobile dashboard
   - Verify sync to desktop

2. **Daily Usage**:
   - Make "Overnight Results" part of morning routine
   - Use "Add Note" after every customer call
   - Check "Pipeline Status" daily

3. **Optimization**:
   - Refine Quick Action prompts based on usage
   - Add custom shortcuts for frequent tasks
   - Share successful patterns with team

---

## Support

**For issues**:
1. Check Troubleshooting section above
2. Review mobile/ folder in repository for updates
3. Test fallback: Use GitHub Mobile app directly
4. Emergency: Desktop access always available

**Feedback**:
- Document pain points in mobile workflow
- Suggest Quick Action improvements
- Share time-saving shortcuts discovered

---

**Phase 3 Status**: Task 3.3 Complete ✓
**Next**: Task 3.4 - Test Mobile Approval Workflow
