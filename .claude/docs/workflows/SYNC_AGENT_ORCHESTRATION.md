# Sync Agent Orchestration Guide
**Automated Sub-Agent Execution for Daily Syncs**

---

## Overview

When a user requests to run a daily sync (9AM, NOON, 3PM, EOD), Claude Code should automatically orchestrate the following workflow:

1. **Run the primary sync script** to display context and priorities
2. **Spawn sub-agents in parallel** using the Task tool to execute sales discipline agents
3. **Aggregate results** and present a unified summary

This ensures the user never has to manually run agent scripts - they're automatically invoked as part of the sync workflow.

---

## Orchestration Patterns by Sync Type

### 9AM Sync Orchestration

**User Command**: "run 9am sync" or "run morning sync"

**Workflow**:

1. **Phase 1 - Main Sync** (Sequential):
   ```bash
   python daily_9am_sync.py
   ```
   Wait for completion and display output to user.

2. **Phase 2 - Sales Discipline Agents** (Parallel):

   Spawn 2 sub-agents simultaneously using Task tool:

   **Sub-Agent 1: Priority Reminder**
   ```
   Task tool with subagent_type: "general-purpose"
   Prompt: "Execute the prioritization agent for daily reminder:

   1. Navigate to C:\Users\BrettWalker\FirstMile_Deals
   2. Run: python .claude/agents/prioritization_agent.py --daily-reminder
   3. Capture and return the complete output
   4. If file is generated at ~/Downloads/DAILY_PRIORITY_REMINDER.txt, read and include its contents
   5. Summarize: What are today's top 3 priority deals and their recommended time allocation?"
   ```

   **Sub-Agent 2: Stale Proposal Scanner**
   ```
   Task tool with subagent_type: "general-purpose"
   Prompt: "Execute the sales execution agent to scan for stale proposals:

   1. Navigate to C:\Users\BrettWalker\FirstMile_Deals
   2. Run: python .claude/agents/sales_execution_agent.py
   3. Capture and return the complete output
   4. Identify: How many stale proposals need follow-up? Which are most urgent?
   5. If follow-up emails were generated, list the deal names and urgency levels"
   ```

3. **Phase 3 - Aggregate Results**:

   Once both sub-agents complete:
   - Display Priority Reminder results with top 3 deals
   - Display Stale Proposal Scanner results with urgency counts
   - Provide unified next-step recommendations

**Expected Output Format**:
```
[Main sync output from daily_9am_sync.py]

===============================================================================
🎯 SALES DISCIPLINE AGENTS - AUTOMATED EXECUTION COMPLETE
===============================================================================

📊 Priority Reminder Results:
   Top 3 Deals for Today:
   1. [Deal Name] ($XXM) - XX% time allocation
   2. [Deal Name] ($XXM) - XX% time allocation
   3. [Deal Name] ($XXM) - XX% time allocation

⚠️  Stale Proposal Scanner Results:
   - X deals need follow-up
   - X urgent (>14 days)
   - X critical (>30 days)

   Most Urgent: [Deal Name] - XX days stale

📋 Recommended Actions:
   1. Block calendar for #1 priority deal (XX hours)
   2. Send urgency follow-ups to X stale proposals
   3. Execute morning priorities in order

✅ All agents executed successfully in parallel
===============================================================================
```

---

### NOON Sync Orchestration

**User Command**: "run noon sync" or "run midday sync"

**Workflow**:

1. **Phase 1 - Main Sync** (Sequential):
   ```bash
   python noon_sync.py
   ```

2. **Phase 2 - Optional Agent** (Only if urgent):

   If user indicates stale proposals need attention, spawn:

   **Sub-Agent: Stale Proposal Scanner**
   ```
   Task tool with subagent_type: "general-purpose"
   Prompt: "Execute sales execution agent for urgent proposal follow-ups:

   1. Navigate to C:\Users\BrettWalker\FirstMile_Deals
   2. Run: python .claude/agents/sales_execution_agent.py
   3. Return only deals marked as URGENT (>14 days)
   4. Summarize immediate actions needed before EOD"
   ```

**Note**: NOON sync agents are optional and should only run if explicitly requested or if urgent issues are detected.

---

### 3PM Sync Orchestration

**User Command**: "run 3pm sync" or "run afternoon sync"

**Workflow**:

1. **Phase 1 - Main Sync** (Sequential):
   ```bash
   python 3pm_sync.py
   ```

2. **Phase 2 - Optional Verification** (Only if requested):

   If user wants to verify daily progress on #1 priority:

   **Sub-Agent: Priority Verification**
   ```
   Task tool with subagent_type: "general-purpose"
   Prompt: "Verify daily touchpoint on #1 priority deal:

   1. Navigate to C:\Users\BrettWalker\FirstMile_Deals
   2. Run: python .claude/agents/prioritization_agent.py --daily-reminder
   3. Check ~/Downloads/_DAILY_LOG.md for today's activities
   4. Verify: Was the #1 priority deal touched today?
   5. If not, generate urgent reminder with specific action needed"
   ```

**Note**: 3PM sync agents are optional but recommended to ensure daily discipline.

---

### EOD Sync Orchestration

**User Command**: "run eod sync" or "run end of day sync"

**Workflow**:

1. **Phase 1 - Main Sync** (Sequential):
   ```bash
   python eod_sync.py
   ```

2. **Phase 2 - Conditional Agent** (Friday only):

   If today is Friday, automatically spawn:

   **Sub-Agent: Weekly Metrics Tracker**
   ```
   Task tool with subagent_type: "general-purpose"
   Prompt: "Execute weekly metrics tracker for Friday EOD review:

   1. Navigate to C:\Users\BrettWalker\FirstMile_Deals
   2. Run: python .claude/agents/weekly_metrics_tracker.py
   3. Capture full output with 5/2/3/1 goal tracking
   4. Identify: Which goals were hit? Which were missed?
   5. Return coaching feedback and next week recommendations
   6. If report file generated at ~/Downloads/WEEKLY_METRICS_*.md, read and summarize"
   ```

3. **Phase 3 - Daily Verification** (Every day):

   **Sub-Agent: Priority Verification**
   ```
   Task tool with subagent_type: "general-purpose"
   Prompt: "Verify daily touchpoint completion:

   1. Read ~/Downloads/_DAILY_LOG.md for today's date
   2. Run: python .claude/agents/prioritization_agent.py --daily-reminder
   3. Verify: Was #1 priority deal touched today?
   4. Return: Yes/No with evidence from daily log
   5. If No: Generate urgent note for tomorrow's action queue"
   ```

**Expected Output Format** (Friday):
```
[Main sync output from eod_sync.py]

===============================================================================
🎯 SALES DISCIPLINE REVIEW - AUTOMATED EXECUTION COMPLETE
===============================================================================

📊 Weekly Metrics Tracker (Friday Review):
   Goals Achieved: X/4
   - New Leads: X/5 (XX%)
   - Discovery Calls: X/2 (XX%)
   - Proposals Sent: X/3 (XX%)
   - Deals Closed: X/1 (XX%)

   Conversion Rates:
   - Lead → Discovery: XX% (target 40%)
   - Discovery → Proposal: XX% (target 75%)
   - Proposal → Close: XX% (target 33%)

   Coaching Feedback: [Performance assessment]
   Next Week Plan: [Recommendations]

✅ Daily Priority Verification:
   #1 Priority Deal: [Deal Name]
   Today's Touchpoint: [Yes/No] - [Evidence]

📋 Recommended Actions:
   1. [Next week adjustment based on metrics]
   2. [Priority focus areas]
   3. [Process improvements needed]

✅ All agents executed successfully
===============================================================================
```

---

## Implementation Guidelines for Claude Code

### When User Says "Run [X] Sync"

**Step 1**: Identify sync type (9AM, NOON, 3PM, EOD)

**Step 2**: Execute main sync script with Bash tool:
```
Bash tool: python daily_9am_sync.py
Description: "Execute 9AM sync to load morning context"
```

**Step 3**: Display sync output to user

**Step 4**: Automatically spawn appropriate sub-agents (DON'T ask user if they want to run agents - just do it):

For 9AM sync - ALWAYS spawn both agents in parallel:
```
Use Task tool with 2 concurrent invocations:
- Task 1: Priority reminder agent
- Task 2: Stale proposal scanner agent
```

For NOON sync - Skip agents unless urgency detected

For 3PM sync - Skip agents unless user explicitly requests verification

For EOD sync:
- If Friday: Spawn weekly metrics tracker
- Always: Spawn daily verification agent

**Step 5**: Wait for sub-agent completion and aggregate results

**Step 6**: Present unified summary with:
- Agent execution status
- Key findings from each agent
- Recommended actions
- Next steps

### Error Handling

If a sub-agent fails:
1. Display error message
2. Continue with other agents (don't block on failures)
3. Note which agent failed and suggest manual execution
4. Complete the sync workflow

### Performance Optimization

- Always run sub-agents in parallel (never sequential unless dependencies exist)
- Use `subagent_type: "general-purpose"` for Python script execution
- Keep agent prompts concise and action-oriented
- Cache agent outputs for session reuse if user requests re-runs

---

## User Experience Goals

**What the user sees**:
```
User: "run 9am sync"

Claude: [Executes daily_9am_sync.py immediately]
        [Displays sync output]

        🎯 Now spawning sales discipline agents in parallel...

        [Sub-agents execute concurrently]
        [Results aggregate automatically]

        Here's your complete morning briefing:
        [Unified summary with all agent outputs]

        Ready to execute? Here are your top 3 priorities for today:
        1. [Priority 1 with time allocation]
        2. [Priority 2 with time allocation]
        3. [Priority 3 with time allocation]
```

**What the user does NOT see**:
- Manual agent invocation commands
- Separate agent outputs (they're aggregated)
- Complex orchestration details
- Task tool mechanics

**User benefit**:
- Single command ("run 9am sync") triggers complete workflow
- Automatic parallel execution saves time
- Unified summary provides clear next steps
- Zero manual agent management

---

## Testing Checklist

Before deploying orchestration:

- [ ] 9AM sync spawns 2 agents in parallel automatically
- [ ] NOON sync runs without agents (unless urgent)
- [ ] 3PM sync provides optional verification
- [ ] EOD sync spawns weekly metrics on Friday automatically
- [ ] EOD sync verifies daily priority touchpoint every day
- [ ] Error handling works (agent failures don't break sync)
- [ ] Results are aggregated in user-friendly format
- [ ] Total execution time <2 minutes for 9AM sync with 2 agents

---

**Last Updated**: October 30, 2025
**System**: Nebuchadnezzar v3.1.0
**Owner**: Brett Walker
