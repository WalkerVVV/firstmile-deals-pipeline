"""
Superhuman EOD Email Intelligence Workflow
Uses Chrome DevTools MCP to automate Superhuman AI email analysis

Usage:
    Run during EOD Sync to gather email intelligence from today's activity

Prerequisites:
    - Superhuman.com open in Chrome browser
    - Chrome DevTools MCP server running
    - Mail.superhuman.com logged in
"""

import json
from datetime import datetime

# Superhuman AI EOD Analysis Prompt
EOD_PROMPT = """
SEARCH QUERY: in:sent OR in:inbox after:today

Analyze all emails sent and received today to provide a comprehensive end-of-day summary.

PART 1: WHAT I WORKED ON TODAY
For each deal/customer/project mentioned in today's emails, document:
- Customer/Deal Name & Current Stage
- Action Taken (email sent, meeting held, data received, issue resolved)
- Key Details (what was discussed/decided, what was delivered, issues resolved, meetings scheduled)
- Email Type: Sent vs Received
- Time of interaction
- Status Change: Did this move the deal forward?

Format:
## TODAY'S ACTIVITY SUMMARY - {date}

### Priority 1 Deals
- **[Customer]** ([Stage])
  - Action: [What you did]
  - Details: [Key points]
  - Time: [HH:MM]
  - Next Step: [What's needed]

### Priority 2 Deals
[Same format]

### Priority 3 Deals
[Same format]

### New Inbound
[New leads/inquiries]

### Internal/Team Communications
[Team discussions, coordination]

PART 2: WHAT'S NEXT TO WORK ON
Identify based on today's email activity:

1. IMMEDIATE FOLLOW-UPS (within 24h):
   - Customer expecting response
   - Meeting confirmations pending
   - Data/reports promised
   - Questions requiring answers

2. THIS WEEK'S PRIORITIES:
   - Proposals to finalize
   - Rates to create
   - Meetings to schedule
   - Analysis to complete

3. BLOCKERS IDENTIFIED:
   - Waiting on customer data
   - Waiting on internal resources
   - Technical issues
   - Decision delays

4. OPPORTUNITIES SPOTTED:
   - Upsell mentions
   - Referrals
   - Expansion conversations
   - Competitive wins

Format:
## TOMORROW'S ACTION PLAN - {tomorrow}

### 🔥 URGENT (Do First)
1. [Action] - [Customer] - [Why urgent]

### 📋 HIGH PRIORITY (This Week)
1. [Action] - [Customer] - [Timeline]

### ⏳ WAITING ON
1. [What waiting for] - [From whom] - [What it unblocks]

### 💡 OPPORTUNITIES
1. [Opportunity] - [Customer] - [Potential value]

PART 3: DEAL STAGE MOVEMENTS
Identify deals that moved stages today based on email evidence:

Evidence to look for:
- Discovery meeting confirmed → [01-DISCOVERY-SCHEDULED]
- Discovery completed, data received → [02-DISCOVERY-COMPLETE]
- Rates created and sent → [04-PROPOSAL-SENT]
- Setup docs sent, verbal commit → [05-SETUP-DOCS-SENT]
- Customer "yes"/"let's move forward" → [06-IMPLEMENTATION]
- First live shipment → [07-CLOSED-WON]
- Customer declines/goes dark → [08-CLOSED-LOST]

Format:
## PIPELINE MOVEMENTS - {date}

### Stage Changes Detected
- **[Customer]**: [Old Stage] → [New Stage]
  - Evidence: [Quote from email or action]
  - Action Required: [Update HubSpot, move folder, tasks]

PART 4: METRICS & INSIGHTS

1. EMAIL VOLUME:
   - Total sent today
   - Total received today
   - Customers contacted
   - New conversations started

2. DEAL VALUE ACTIVITY:
   - Total annual value of deals worked today
   - Proposals sent
   - Meetings held
   - Follow-ups completed

3. RESPONSE QUALITY:
   - Average response time to customer emails
   - Emails >24h old needing response
   - Missed follow-ups from previous commitments

Format:
## TODAY'S METRICS - {date}

📧 EMAIL ACTIVITY
- Sent: [count]
- Received: [count]
- Customers contacted: [count]
- New threads: [count]

💰 DEAL ACTIVITY
- Deals worked: [count] ($[value])
- Proposals sent: [count] ($[value])
- Meetings: [count]
- Follow-ups: [count]

⏱️ RESPONSE PERFORMANCE
- Avg response time: [hours/min]
- Overdue responses: [count]
- On-time commitments: [count]/[total]

SPECIAL INSTRUCTIONS:
1. Focus on actionable intelligence - what it means for deal progress
2. Identify patterns - multiple emails = urgency or blocker
3. Flag risks - frustration, delays, competitive threats
4. Celebrate wins - positive responses, deals advancing, problems solved
5. Be specific - use quotes, numbers, dates from emails
6. Cross-reference - if "as discussed", find original context

OUTPUT: Comprehensive EOD summary in markdown, ready to paste into _DAILY_LOG.md, FOLLOW_UP_REMINDERS.txt, and daily status updates. Aim for 2-3 pages, scannable format, professional tone, action-oriented.
"""

def get_prompt_with_dates():
    """Generate prompt with current date filled in"""
    today = datetime.now().strftime("%B %d, %Y")
    tomorrow = datetime.now().strftime("%B %d, %Y")  # Will be next business day in reality

    return EOD_PROMPT.format(date=today, tomorrow=tomorrow)

def main():
    """
    Main workflow - to be executed via Claude Code with MCP tools

    Steps:
    1. Navigate to Superhuman
    2. Access Superhuman AI
    3. Run search query
    4. Copy prompt
    5. Capture response
    6. Save to _DAILY_LOG.md
    """

    print("="*80)
    print("SUPERHUMAN EOD EMAIL INTELLIGENCE WORKFLOW")
    print("="*80)

    print("\nStep 1: Navigate to Superhuman")
    print("   Tool: mcp__chrome-devtools__navigate_page")
    print("   URL: https://mail.superhuman.com/")

    print("\nStep 2: Wait for page load")
    print("   Tool: mcp__chrome-devtools__wait_for")
    print("   Text: 'Inbox'")

    print("\nStep 3: Take snapshot to identify AI button")
    print("   Tool: mcp__chrome-devtools__take_snapshot")

    print("\nStep 4: Copy EOD Analysis Prompt")
    prompt = get_prompt_with_dates()

    # Save prompt to file for easy copy-paste
    prompt_file = r"C:\Users\BrettWalker\Downloads\SUPERHUMAN_EOD_PROMPT_TODAY.txt"
    with open(prompt_file, 'w', encoding='utf-8') as f:
        f.write(prompt)

    print(f"   Saved to: {prompt_file}")
    print("   Status: Ready to paste into Superhuman AI")

    print("\n" + "="*80)
    print("PROMPT READY - MANUAL STEPS:")
    print("="*80)
    print("1. Open Superhuman.com in Chrome")
    print("2. Click Superhuman AI button")
    print("3. Paste prompt from: SUPERHUMAN_EOD_PROMPT_TODAY.txt")
    print("4. Review AI response")
    print("5. Copy response sections to:")
    print("   - _DAILY_LOG.md (Activity Summary, Pipeline Movements, Metrics)")
    print("   - FOLLOW_UP_REMINDERS.txt (Tomorrow's Action Plan)")
    print("="*80)

    return prompt

if __name__ == "__main__":
    prompt = main()
    print("\nPrompt generated successfully!")
    print("\nPreview (first 500 chars):")
    print(prompt[:500])
    print("\n[...prompt continues...]")
