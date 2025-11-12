# Cross-Device Workflow Guide

**Complete guide to sharing context between Claude Code (desktop) and Claude.ai mobile**

---

## 🏗️ Architecture Overview

```
┌─────────────────────┐         ┌──────────────────┐
│  Claude Code        │         │  Claude.ai       │
│  (VS Code Desktop)  │         │  (Mobile App)    │
│                     │         │                  │
│  ✅ File access     │         │  ❌ No files     │
│  ✅ Git commands    │         │  ❌ No Git       │
│  ✅ Python scripts  │         │  ❌ No scripts   │
│  ✅ Commits/Push    │         │  ✅ Analysis     │
│                     │         │  ✅ Planning     │
└──────────┬──────────┘         └────────┬─────────┘
           │                              │
           └──────────┬───────────────────┘
                      │
           ┌──────────▼──────────┐
           │   GitHub Repository  │
           │   (Context Bridge)   │
           │                      │
           │  • SESSION_CONTEXT   │
           │  • Deal folders      │
           │  • Mobile notes      │
           │  • Action plans      │
           └─────────────────────┘
```

**Key Concept**: Git repository is the "shared memory" between devices

---

## 📱 Complete Mobile Setup

### 1. Mobile Dashboard (Safari/Chrome)

**URL**: https://walkervvv.github.io/firstmile-deals-pipeline/

**Setup**:
```bash
# On iPhone:
1. Open Safari
2. Go to dashboard URL
3. Tap Share → "Add to Home Screen"
4. Name: "Pipeline Dashboard"

# Get GitHub Token (desktop):
1. Visit: https://github.com/settings/tokens
2. Generate new token (classic)
3. Scope: repo (full control)
4. Copy token

# Enter token in mobile dashboard:
1. Open dashboard
2. Tap "Setup Token"
3. Paste GitHub PAT
4. Token saves in browser
```

### 2. Claude.ai Mobile App

**Setup**:
```bash
# Download:
- iOS: App Store → "Claude"
- Android: Play Store → "Claude"

# No additional setup needed
# Just open app and start chatting
```

---

## 🔄 Context Sharing Patterns

### Pattern 1: Desktop → Mobile Handoff

**On Desktop (before switching to mobile)**:

```bash
# 1. Update session context
# Edit: .claude/SESSION_CONTEXT.md
# Update "Current Status" section with:
# - What you just did
# - What needs to happen next
# - Any blockers or decisions needed

# 2. Commit and push
git add .claude/SESSION_CONTEXT.md
git commit -m "[SESSION] Desktop handoff to mobile - [brief description]"
git push origin main

# 3. Note the key file paths
# Mobile Claude will need to know which files to reference
```

**On Mobile (starting session)**:

```
Say to Claude mobile:
"I'm continuing work from desktop. Read the context from .claude/SESSION_CONTEXT.md in my firstmile-deals-pipeline repository. The repo structure is:
- 25 deal folders: [##-STAGE]_Company_Name/
- Documentation: .claude/ folder
- Current focus: [describe current task]

What's the status and what should I work on?"
```

**How it works**:
- Mobile Claude can't read files directly
- But you can describe file contents or copy/paste sections
- Mobile Claude analyzes and provides guidance

### Pattern 2: Mobile → Desktop Handoff

**On Mobile (during session)**:

```
Say to Claude mobile:
"Create a handoff note for desktop. I need to:
1. [action item]
2. [action item]
3. [action item]

Format it as a markdown file I can commit when back on desktop."
```

**Claude will generate**:
```markdown
# Mobile Session Notes - 2025-10-24 2:30 PM

## Actions Taken
- Analyzed DYLN deal status
- Drafted follow-up email
- Prioritized 3 urgent deals

## Decisions Made
- Focus on DYLN first (14 days overdue)
- Josh's Frogs meeting confirmed for Friday
- Upstate Prep ready to close

## Desktop TODO
- [ ] Send DYLN follow-up email (draft ready)
- [ ] Verify Josh's Frogs meeting time
- [ ] Push Upstate Prep toward close

## Email Draft: DYLN Follow-up
[email content here]

## Follow-ups Needed
- Check RATE-1907 completion status
- Confirm BoxiiShip credit approval
- Review 7 proposal-stage deals
```

**Copy this output and save locally**

**On Desktop (when returning)**:

```bash
# 1. Create the mobile note file
# Copy the content from mobile
cat > mobile_notes/20251024_1430_mobile_session.md << 'EOF'
[paste mobile Claude's output]
EOF

# 2. Commit the note
git add mobile_notes/
git commit -m "[MOBILE] Session notes from mobile - [brief description]"
git push origin main

# 3. Execute the action items
# Read the mobile note in Claude Code and implement
```

### Pattern 3: Real-Time Reference

**On Mobile (any time)**:

```
"What's in the deal folder for [Customer Name]?
Based on the FirstMile Deals repo structure:
- Deal folders: [##-STAGE]_Company_Name/
- Typical files: PLD analysis, rate sheets, emails

What files should I ask you to check on desktop?"
```

**On Desktop (any time)**:

```bash
# You can ask Claude Code:
"Create a summary of the DYLN deal folder for mobile reference"

# Claude will read files and create summary:
# - Deal status
# - Key metrics
# - Recent activity
# - Next actions
```

---

## 🎯 Common Workflows

### Workflow 1: Morning Mobile Review → Desktop Execution

**9 AM - Mobile (on commute)**:
```
Mobile Claude prompt:
"Morning pipeline review:
- What deals need attention today?
- Any overdue follow-ups?
- Meetings scheduled?
- Top 3 priorities for desktop work?

Format as bullet list, under 100 words."
```

**Mobile Dashboard**:
- Review overnight automation branches
- Approve safe auto-merges
- Flag complex changes for desktop

**10 AM - Desktop (at office)**:
```bash
# Pull latest changes
git pull origin main

# Read mobile priorities
# Ask Claude Code:
"Read mobile_notes/ for today's session and execute the priority list"

# Claude implements:
# - Sends emails
# - Updates HubSpot
# - Runs Python scripts
# - Commits changes
```

### Workflow 2: Desktop Implementation → Mobile Review

**Desktop (during work)**:
```bash
# Do complex work:
# - Rate calculations
# - PLD analysis
# - Report generation

# Update context:
# Edit .claude/SESSION_CONTEXT.md

# Commit and push:
git commit -m "[WORK] Completed rate analysis for [Customer]"
git push origin main
```

**Mobile (later that day)**:
```
Mobile Claude prompt:
"Check SESSION_CONTEXT.md - what work was completed?
Review the [Customer] rate analysis results.
Should I send the proposal now or wait?"

Mobile Claude analyzes and provides guidance.
```

### Workflow 3: Mobile Planning → Desktop Execution

**Mobile (anywhere)**:
```
Mobile Claude prompt:
"Create an implementation plan for the Josh's Frogs discovery call:
1. Pre-meeting research
2. Questions to ask
3. Data to gather
4. Follow-up actions

Format as checklist for desktop execution."
```

**Mobile Claude generates**:
```markdown
## Josh's Frogs Discovery Call - Implementation Plan

### Pre-Meeting (Desktop - 30 mins before)
- [ ] Review PLD analysis: [01-DISCOVERY-SCHEDULED]_Josh's_Frogs/
- [ ] Check savings calculations
- [ ] Prepare questions list
- [ ] Load HubSpot deal: [ID]

### During Meeting (45 mins)
- [ ] Confirm volume: 29,255 packages/month
- [ ] Verify service mix: 80% live insects (excluded), 20% dry goods
- [ ] Ask about current carrier experience
- [ ] Discuss FirstMile value props

### Post-Meeting (Desktop - immediate)
- [ ] Create meeting notes
- [ ] Update HubSpot deal stage
- [ ] Send follow-up email
- [ ] Create next steps tasks
```

**Copy to mobile_notes/, commit on desktop, execute**

---

## 📝 File-Based Context Patterns

### Key Context Files

| File | Purpose | Updated By |
|------|---------|------------|
| `.claude/SESSION_CONTEXT.md` | Current session status | Both (desktop commits) |
| `mobile_notes/YYYYMMDD_HHMM.md` | Mobile session notes | Mobile (create), Desktop (commit) |
| `TOMORROW_MORNING_ACTIONS_OCT24.md` | Action plans | Both |
| `.claude/DAILY_SYNC_OPERATIONS.md` | Daily workflows | Reference only |
| `mobile/CLAUDE_MOBILE_GUIDE.md` | Mobile prompts library | Reference only |

### Context Loading Patterns

**Desktop Claude Code**:
```
"Read .claude/SESSION_CONTEXT.md and continue from where mobile left off"
```

**Mobile Claude.ai**:
```
"I'm working on the FirstMile Deals pipeline repo.
Current status from SESSION_CONTEXT.md:
[copy/paste relevant section]

What should I focus on?"
```

---

## 🚦 Decision Framework

**Use Mobile For**:
- ✅ Planning and strategy
- ✅ Email drafting
- ✅ Deal analysis and prioritization
- ✅ Meeting preparation
- ✅ Quick status checks
- ✅ Branch approval (via dashboard)

**Use Desktop For**:
- ✅ Python script execution
- ✅ File editing and commits
- ✅ Complex rate calculations
- ✅ HubSpot API calls
- ✅ Git operations
- ✅ Report generation

**Use Both Together**:
- 📱 Mobile: Analyze deal status → create priority list
- 💻 Desktop: Execute priority list → commit results
- 📱 Mobile: Review results → provide next guidance
- 💻 Desktop: Implement guidance → update context

---

## 🔧 Setup Checklist

### One-Time Setup

**Desktop**:
```bash
# 1. Ensure repo is up to date
cd C:\Users\BrettWalker\FirstMile_Deals
git pull origin main

# 2. Verify context files exist
ls .claude/SESSION_CONTEXT.md
ls .claude/CROSS_DEVICE_WORKFLOW.md
ls mobile_notes/README.md

# 3. Commit any pending changes
git add .
git commit -m "[SETUP] Cross-device workflow configured"
git push origin main
```

**Mobile**:
```bash
# 1. Install Claude app (if not already)
# iOS: App Store
# Android: Play Store

# 2. Set up mobile dashboard
# Safari: https://walkervvv.github.io/firstmile-deals-pipeline/
# Add to home screen
# Enter GitHub PAT

# 3. Bookmark quick reference
# Save this file path in Notes app:
# .claude/CROSS_DEVICE_WORKFLOW.md
```

### Daily Sync Pattern

**Morning (Mobile)**:
```bash
# 1. Open mobile dashboard
# 2. Review overnight branches
# 3. Chat with Claude mobile:
"Morning review - check SESSION_CONTEXT.md for overnight work"
```

**During Day (Desktop)**:
```bash
# 1. Pull latest
git pull origin main

# 2. Execute mobile priorities
# 3. Update SESSION_CONTEXT.md
# 4. Commit and push
git push origin main
```

**Evening (Mobile)**:
```bash
# 1. Final dashboard check
# 2. Claude mobile:
"EOD review - what's pending for tomorrow?"
# 3. Create mobile notes for tomorrow's desktop work
```

---

## 💡 Pro Tips

### Tip 1: Use Voice Input on Mobile
```
Mobile Claude with voice:
- Walk and dictate email drafts
- Hands-free deal analysis while commuting
- Quick status checks between meetings
```

### Tip 2: Screenshot and Reference
```
Take screenshots of:
- Claude mobile analysis
- Dashboard branch lists
- Priority rankings

Reference in desktop session
```

### Tip 3: Bookmark Key Prompts
```
Save in iPhone Notes:
- "Morning pipeline review [short format]"
- "Draft follow-up for [Customer] in [Stage]"
- "Check SESSION_CONTEXT.md status"
- "Meeting prep for [Customer] in 30 mins"
```

### Tip 4: Use SESSION_CONTEXT as Central Hub
```
Always update SESSION_CONTEXT.md:
- After completing major work (desktop)
- Before switching devices
- When creating new priorities
- When making important decisions

It's the "single source of truth" for both devices
```

### Tip 5: Mobile Notes Template
```
Keep template in Notes app for quick copy:

---
# Mobile Session - [Date] [Time]

## What I analyzed:
-

## Decisions:
-

## Desktop TODO:
-

## Email drafts:
-
---

Copy to mobile_notes/ when back on desktop
```

---

## 🔗 Related Documentation

- `.claude/SESSION_CONTEXT.md` - Current session status (UPDATE THIS OFTEN)
- `mobile/CLAUDE_MOBILE_GUIDE.md` - 638 lines of mobile prompts
- `mobile/GITHUB_PAGES_SETUP.md` - Dashboard setup guide
- `.claude/DAILY_SYNC_OPERATIONS.md` - 9AM, NOON, EOD workflows
- `.claude/DOCUMENTATION_INDEX.md` - Complete doc map

---

## 🎯 Quick Start

**Right Now**:

1. **On Desktop** (commit this setup):
```bash
git add .claude/SESSION_CONTEXT.md
git add .claude/CROSS_DEVICE_WORKFLOW.md
git add mobile_notes/README.md
git commit -m "[CONFIG] Cross-device context sharing system"
git push origin main
```

2. **On Mobile** (test the system):
```
Open Claude mobile app and say:

"I'm setting up cross-device workflow for my FirstMile Deals pipeline.

The system uses:
- .claude/SESSION_CONTEXT.md for current status
- mobile_notes/ for mobile session notes
- GitHub repo as shared context

Test: What should I work on based on recent context?"
```

3. **Verify** (check sync works):
```bash
# Desktop: Update context
# Mobile: Reference context
# Desktop: Read mobile notes
# Full circle! ✅
```

---

**Last Updated**: 2025-10-24 12:55 PM
**Status**: Cross-device workflow configured and ready to test
**Next**: Test mobile → desktop handoff with real deal work
