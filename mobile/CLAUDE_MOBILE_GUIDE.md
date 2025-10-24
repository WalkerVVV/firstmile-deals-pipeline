# Claude.ai Mobile Integration Guide

**Phase 3, Task 3.3 - Mobile Claude Code Workflow**

This guide shows you how to use Claude.ai on mobile devices to coordinate with your desktop Git automation and mobile review dashboard.

## Overview

The Nebuchadnezzar v3.0 Matrix system enables three ways to interact with your pipeline:

1. **Desktop (Claude Code)**: Full development environment with Git automation
2. **Mobile Dashboard**: Quick branch approval/rejection via GitHub Pages
3. **Mobile Claude.ai**: Analysis, planning, and coordination on-the-go

This guide focuses on #3: Using Claude.ai mobile for pipeline management.

## Mobile Claude.ai Capabilities

### What You CAN Do on Mobile:
- ✅ Analyze deal status and performance data
- ✅ Draft follow-up emails and proposals
- ✅ Review rate calculations and savings projections
- ✅ Plan next actions and strategy
- ✅ Coordinate with desktop Git automation
- ✅ Monitor pipeline health and priorities
- ✅ Generate reports and summaries
- ✅ Create task lists for desktop execution

### What You CANNOT Do on Mobile:
- ❌ Run Python scripts directly
- ❌ Execute Git commands
- ❌ Edit files in repository
- ❌ Create commits
- ❌ Access local file system

### The Mobile + Desktop Pattern:
Mobile Claude creates the plan → Desktop Claude executes the plan → Mobile Dashboard reviews the results

## Quick Actions for Mobile

### 1. Pipeline Status Check
**Prompt:**
```
What deals need attention today? Check:
- [04-PROPOSAL-SENT] deals >7 days old
- [01-DISCOVERY-SCHEDULED] meetings this week
- [03-RATE-CREATION] bottleneck status
- Any follow-ups due
```

**Claude will:**
- Review pipeline structure from memory
- Identify stale deals by stage
- Flag upcoming meetings
- List overdue actions

### 2. Follow-Up Email Draft
**Prompt:**
```
Draft a follow-up email for [Customer Name] in [04-PROPOSAL-SENT]:
- Sent proposal on [Date]
- Emphasized [Key Value Prop]
- Need response by [Target Date]
- Tone: professional but friendly
```

**Claude will:**
- Generate email following FirstMile brand voice
- Include relevant deal context
- Add clear call-to-action
- Format for easy copy-paste

### 3. Deal Performance Summary
**Prompt:**
```
Summarize the current performance of [Customer Name]:
- Volume and service mix
- Current carrier costs
- FirstMile savings projection
- Key selling points for next meeting
```

**Claude will:**
- Pull deal context from memory
- Summarize key metrics
- Highlight competitive advantages
- Suggest talking points

### 4. Rate Analysis Review
**Prompt:**
```
Review the rate analysis for [Customer Name]:
- Is the savings percentage compelling?
- Any red flags in the data?
- Should we adjust pricing strategy?
- Ready to send or needs revision?
```

**Claude will:**
- Analyze rate comparison data
- Validate savings calculations
- Identify potential issues
- Recommend next steps

### 5. Daily Priority List
**Prompt:**
```
Create my daily priority list:
- Top 3 deals to move forward today
- Follow-ups that are overdue
- Rate creation requests to process
- Meetings to prepare for
```

**Claude will:**
- Scan entire pipeline
- Prioritize by urgency and impact
- Generate actionable task list
- Include estimated time per task

### 6. Competitive Response
**Prompt:**
```
Customer says: "[Competitor offer]"
How should I respond? Deal: [Customer Name], Stage: [04-PROPOSAL-SENT]
```

**Claude will:**
- Analyze competitor positioning
- Suggest counter-arguments
- Highlight FirstMile differentiators
- Draft response email

### 7. Meeting Prep
**Prompt:**
```
Prepare me for discovery call with [Customer Name] at [Time]:
- Their shipping profile
- Key pain points to probe
- Questions to ask
- FirstMile value props to emphasize
```

**Claude will:**
- Review deal folder context
- Generate question list
- Identify likely objections
- Prepare value proposition talking points

### 8. Pipeline Health Check
**Prompt:**
```
Analyze pipeline health:
- Conversion rates by stage
- Average time in each stage
- Bottlenecks and stalled deals
- Recommendations for improvement
```

**Claude will:**
- Aggregate pipeline metrics
- Identify trends and patterns
- Flag problem areas
- Suggest process improvements

## Mobile Workflow Examples

### Morning Review (9 AM - On Commute)

**Mobile Claude Prompt:**
```
Morning pipeline review:
1. What deals need attention today?
2. Any overnight automation activity?
3. Meetings scheduled for today
4. Priority actions for first 2 hours

Format as bullet list for quick review.
```

**Mobile Dashboard:**
- Open dashboard
- Review overnight automation branches
- Approve safe auto-merges
- Flag complex changes for desktop

**Result:** You arrive at desk knowing exactly what to tackle first

### Lunch Break Deal Check

**Mobile Claude Prompt:**
```
Quick status on [Customer Name]:
- Last activity date
- Current stage
- Next action needed
- Should I follow up now or wait?

Give me a yes/no answer with 1-sentence reasoning.
```

**Action:** If yes, ask Claude to draft follow-up email

### Afternoon Meeting Prep

**Mobile Claude Prompt:**
```
I have a call with [Customer Name] in 30 minutes.
Quick prep sheet:
- Their current situation
- Our proposal summary
- Likely objections
- 3 key talking points

Keep it under 200 words - I need to scan it quickly.
```

**Result:** Walk into call confident and prepared

### Evening Strategy Session

**Mobile Claude Prompt:**
```
End-of-day planning:
- What did I accomplish today?
- What's still pending?
- Top 3 priorities for tomorrow morning
- Any deals that need urgent attention?

Also flag any patterns or trends you notice.
```

**Mobile Dashboard:**
- Final branch review
- Approve accumulated changes
- Verify no stuck branches

### Weekend Deal Review

**Mobile Claude Prompt:**
```
Weekend pipeline check (no actions, just awareness):
- Any deals at risk of going stale?
- Upcoming deadlines next week
- Prep work I should think about over weekend
- Overall pipeline trajectory

Be honest about any concerns.
```

**Result:** Monday morning you hit the ground running

## Coordinating Mobile + Desktop

### Pattern: Mobile Plans, Desktop Executes

**Mobile Claude (on phone):**
```
Create implementation plan for [Customer Name] rate analysis:
1. Extract data from their CSV
2. Apply FirstMile rates
3. Calculate savings
4. Generate Excel report
5. Draft proposal email

List the exact Python scripts to run on desktop.
```

**Desktop Claude (when back at desk):**
Execute the plan Claude generated:
```bash
python [customer]/pld_analysis.py
python [customer]/apply_firstmile_rates.py
python [customer]/create_pricing_matrix.py
# etc.
```

### Pattern: Desktop Executes, Mobile Reviews

**Desktop Claude (automated overnight):**
- N8N triggers rate creation workflow
- Git automation creates branch: `automation/Customer_Name_rate_creation`
- Files committed and pushed

**Mobile Dashboard (morning):**
- Review automation branch
- Check generated files
- Approve and merge or flag for desktop review

**Mobile Claude (if issues):**
```
The automation created rates for [Customer], but I see [Issue].
What's the problem and how should I fix it when I get to desktop?
```

### Pattern: Mobile Coordinates, Dashboard Approves, Desktop Refines

**Mobile Claude (during meeting):**
```
Customer just agreed to pilot! Create action plan:
1. Move deal folder to [06-IMPLEMENTATION]
2. Create onboarding tasks in HubSpot
3. Send welcome email
4. Schedule kickoff call

What order should I do these in?
```

**Mobile Dashboard:**
- Approve folder move branch when automation creates it

**Desktop Claude (detailed work):**
- Execute full onboarding workflow
- Generate implementation docs
- Configure integrations

## Mobile-Friendly Prompts

### Format for Quick Scanning

**Good** (mobile-friendly):
```
Deal Status:
✓ Proposal sent: Oct 15
✓ Follow-up: Oct 22
⚠ No response (7 days)

Action: Send 2nd follow-up today
Email draft ready below:
[email text]
```

**Bad** (too verbose):
```
After analyzing the situation with the customer,
I've determined that based on the date when we initially
sent the proposal and subsequently followed up...
[continues for paragraphs]
```

### Use Bullet Lists, Not Paragraphs

**Good:**
- Proposal sent Oct 15
- Customer expressed interest
- Awaiting procurement approval
- Follow up this Friday

**Bad:**
The proposal was sent on October 15th, and during our subsequent conversation, the customer expressed considerable interest in our solution. They mentioned that they need to get procurement approval, so we should follow up with them this Friday to check on the status...

### Ask for Specific Formats

**Examples:**
- "Give me a bullet list"
- "Format as a table"
- "Yes/No answer with 1-sentence reasoning"
- "Under 200 words"
- "Just the key numbers"
- "Top 3 only"

## Mobile Tips & Best Practices

### 1. Use Voice Input
Claude.ai mobile supports voice input - great for hands-free use:
- Morning commute pipeline review
- Drafting emails while walking
- Quick status checks between meetings

### 2. Bookmark Common Prompts
Save frequently-used prompts in your phone's notes app:
- "Morning pipeline review" template
- "Draft follow-up email for..." template
- "Meeting prep for..." template

### 3. Screenshot and Share
Take screenshots of Claude's responses to:
- Share with team members
- Reference in meetings
- Save for later review

### 4. Chain Prompts for Deep Dives
Build on previous responses:
```
Prompt 1: "Summarize [Customer] deal"
Prompt 2: "What's the biggest risk with this deal?"
Prompt 3: "How should I mitigate that risk?"
Prompt 4: "Draft an email addressing that concern"
```

### 5. Use Context from Memory
Claude remembers your pipeline structure:
```
"You know the structure of my FirstMile Deals pipeline.
Which deals in [04-PROPOSAL-SENT] have been there longest?"
```

### 6. Request Desktop Actions
Claude can't execute, but can prepare:
```
"Create a bash command I can copy-paste on desktop to:
1. Move [Customer] to [05-SETUP-DOCS-SENT]
2. Create HubSpot task for follow-up
3. Update pipeline tracker

Give me the exact commands to run."
```

## Integration with Git Automation

### Understanding Branch Notifications

When you get a GitHub notification on mobile:

**Branch name:** `automation/Stackd_Logistics_rate_update`

**Means:**
- **Agent:** Automation (N8N triggered)
- **Deal:** Stackd_Logistics
- **Action:** rate_update

**Your options:**
1. **Mobile Dashboard:** Quick approve/reject
2. **Mobile Claude:** Analyze what changed and why
3. **Desktop:** Detailed review and refinement

### Prompt for Branch Analysis

```
I see a GitHub branch: automation/Stackd_Logistics_rate_update

Based on my pipeline context:
1. What triggered this automation?
2. Is this expected or unusual?
3. Safe to auto-merge or needs review?
4. If I approve, what happens next?
```

## Troubleshooting Mobile Workflow

### "Claude doesn't remember my pipeline"

**Solution:** Provide context in prompt:
```
Context: I manage a FirstMile Deals sales pipeline with 47 deals
across 10 stages ([00-LEAD] through [09-WIN-BACK]).
Each deal has a folder with customer data and analysis.

Now, my question: [your question]
```

### "Responses are too long for mobile"

**Solution:** Request shorter formats:
```
[Your question]

Format: Bullet list, max 5 items, under 100 words total.
```

### "Need to reference specific files"

**Solution:** Desktop has files, Mobile has memory:
```
When I get to desktop, which files should I check for [Customer]?
List the file paths in order of priority.
```

### "Can't execute Claude's suggestions"

**Solution:** Create action list for desktop:
```
I can't run these commands now (on mobile).
Create a TODO list I can execute when I'm back at desktop.
Number the steps and include exact commands.
```

## Mobile + Dashboard + Desktop Workflow

### Complete Multi-Channel Example

**9 AM - Mobile Claude (in Uber to office):**
```
Morning review: What needs attention today?
```

**Claude response:**
- 3 proposals sent >7 days ago need follow-up
- Josh's Frogs discovery call at 2 PM
- Stackd Logistics rate automation ran overnight

**9:05 AM - Mobile Dashboard (still in Uber):**
- See `automation/Stackd_Logistics_rate_update` branch
- Quick review: looks good
- Tap "Approve & Merge"

**9:30 AM - Desktop Claude (arrived at office):**
```
Execute follow-up workflow for:
1. Caputron (8 days since proposal)
2. OTW Shipping (10 days since proposal)
3. Team Shipper (7 days since proposal)

Draft emails and update HubSpot tasks.
```

**1:45 PM - Mobile Claude (15 min before meeting):**
```
Quick prep for Josh's Frogs call at 2 PM:
- Their shipping profile summary
- Key pain points
- 3 qualifying questions to ask
- FirstMile value props

Under 200 words, bullet format.
```

**2:00 PM - Meeting (Josh's Frogs)**
*(Reference Claude's prep notes on phone during call)*

**2:30 PM - Mobile Claude (right after meeting):**
```
Meeting debrief - capture notes before I forget:

Josh's Frogs call went well. They ship:
- 80% live insects (excluded from FirstMile)
- 20% dry goods (feed, supplies) - PERFECT FIT
- Current carrier: UPS
- Volume: ~500 dry good shipments/month
- Interested in FirstMile for dry goods only

Next steps: Rate analysis for dry goods portion only.

Create action plan for desktop.
```

**3:00 PM - Desktop Claude (detailed work):**
- Filter Josh's Frogs data for dry goods only
- Run PLD analysis
- Generate rate comparison
- Draft proposal

**5:00 PM - Mobile Dashboard (end of day):**
- Review any new automation branches
- Approve safe merges
- Flag anything complex for tomorrow

## Advanced Mobile Patterns

### Chain of Thought for Complex Analysis

```
Let's think through the [Customer] deal step-by-step:

1. First, what's their current situation?
2. What are we proposing?
3. What's the savings percentage?
4. Is that compelling for their industry?
5. What objections might they have?
6. How do we overcome those objections?
7. Bottom line: Should we adjust our approach?

Walk me through each step.
```

### Comparative Analysis

```
Compare these 3 deals side-by-side:
- Stackd Logistics
- OTW Shipping
- Team Shipper

Table format:
| Deal | Stage | Days in Stage | Savings % | Risk Level | Priority |

Then: Which one should I focus on first and why?
```

### Pattern Recognition

```
Look at my [04-PROPOSAL-SENT] deals that converted to
[07-CLOSED-WON]. What patterns do you see?

Common factors:
- Savings percentage range
- Time from proposal to close
- Industries
- Objections that came up

What does this tell me about my current [04-PROPOSAL-SENT] deals?
```

## Mobile Productivity Hacks

### 1. Commute Optimization
- Review pipeline during commute
- Draft emails with voice input
- Plan daily priorities before arriving

### 2. Meeting Prep Anywhere
- 15-minute prep between meetings
- Quick context refresh before calls
- Post-meeting debrief capture

### 3. Async Coordination
- Mobile Claude plans work
- Desktop Claude executes overnight automation
- Mobile Dashboard approves results next morning

### 4. Weekend Strategy
- Casual pipeline review without pressure
- Think through complex deals
- Plan Monday priorities

## Next Steps

After reading this guide:

1. ✅ Test mobile Claude with simple pipeline query
2. ✅ Bookmark 3-5 common prompts in phone notes
3. ✅ Practice voice input for email drafting
4. ✅ Try morning review workflow tomorrow
5. ✅ Coordinate mobile + desktop on one deal

## Phase 3 Progress

- ✅ Task 3.1: GitHub Mobile Setup Guide
- ✅ Task 3.2: Mobile Review Dashboard (deployed, awaiting Pages config)
- ✅ Task 3.3: Claude.ai Mobile Integration Guide (this document)
- ⏳ Task 3.4: Test Mobile Approval Workflow

---

**Mobile Dashboard**: https://walkervvv.github.io/firstmile-deals-pipeline/
**Mobile Claude**: https://claude.ai (iOS/Android apps available)
**Last Updated**: Phase 3, October 24, 2025
