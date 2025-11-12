# Prioritization Agent Skill

**Purpose**: Daily morning sync to prioritize active deals, review brand scout results, and set daily focus.

## Core Reference
→ **See [rules.md](../../rules.md) → Agent-Specific Rules → Prioritization Agent**

## Execution Workflow

### Phase 1: Context Loading (9:00 AM)
1. **CRITICAL**: Load yesterday's EOD sync markdown from standard location
2. Extract key learnings and carry-forward items
3. Load follow-up queue for items due today
4. Review any overnight brand scout results

### Phase 2: HubSpot Data Fetch (9:01 AM - 9:05 AM)
1. Use `hubspot_sync_core.HubSpotSyncManager` to fetch active deals
2. Query all pipeline stages (exclude Closed-Won/Closed-Lost unless recent)
3. Calculate "days in stage" for each deal
4. Flag deals approaching SLA thresholds (7+ days in current stage)

### Phase 3: Priority Scoring (9:05 AM - 9:10 AM)
**Priority Score Formula**:
```python
priority_score = (
    (days_in_stage * 2) +                    # Urgency (older deals = higher priority)
    (deal_value / 100000) +                   # Value (higher $ = higher priority)
    (stage_weight) +                          # Stage criticality
    (brand_scout_flag * 5)                    # New leads get boost
)

stage_weights = {
    "01-DISCOVERY-SCHEDULED": 10,             # Upcoming discovery = high priority
    "02-DISCOVERY-COMPLETE": 8,               # Need to move to rate creation
    "03-RATE-CREATION": 9,                    # Active work required
    "04-PROPOSAL-SENT": 10,                   # Awaiting response = follow-up needed
    "05-SETUP-DOCS-SENT": 7,                  # Awaiting signatures
    "06-IMPLEMENTATION": 8,                   # Technical setup in progress
    "00-LEAD": 3                              # Lower priority until qualified
}
```

### Phase 4: Report Generation (9:10 AM - 9:15 AM)
1. Generate priority report using standard markdown template
2. Identify top 3-5 actions for today
3. Update follow-up queue with new items
4. Save output to standard sync location

## Output Template

```markdown
# 9AM Priority Sync - {Day}, {Date}

## Yesterday's Context
**Key Learnings from EOD {Yesterday's Date}**:
- [Learning 1 from yesterday]
- [Learning 2 from yesterday]

**Carry-Forward Actions**:
- [Action that wasn't completed yesterday]

---

## Active Deals by Stage

### [01-DISCOVERY-SCHEDULED] (Count: X)
| Deal Name | Days in Stage | Deal Value | Next Action | Owner |
|-----------|---------------|------------|-------------|-------|
| Acme Corp | 3 days | $150K | Confirm discovery call time | Brett |
| BoxiiShip | 5 days | $200K | Send pre-call questionnaire | Brett |

### [02-DISCOVERY-COMPLETE] (Count: X)
| Deal Name | Days in Stage | Deal Value | Next Action | Owner |
|-----------|---------------|------------|-------------|-------|
| Easy Group | 2 days | $180K | Begin rate creation | Brett |

### [03-RATE-CREATION] (Count: X)
| Deal Name | Days in Stage | Deal Value | Next Action | Owner |
|-----------|---------------|------------|-------------|-------|
| Stackd | 4 days | $220K | Finalize Xparcel Ground rates | Brett |

### [04-PROPOSAL-SENT] (Count: X)
| Deal Name | Days in Stage | Deal Value | Next Action | Owner |
|-----------|---------------|------------|-------------|-------|
| Upstate Prep | 7 days ⚠️ | $175K | Follow-up call (7+ days) | Brett |

### [05-SETUP-DOCS-SENT] (Count: X)
| Deal Name | Days in Stage | Deal Value | Next Action | Owner |
|-----------|---------------|------------|-------------|-------|
| [Deal] | X days | $XXX | [Action] | [Owner] |

### [06-IMPLEMENTATION] (Count: X)
| Deal Name | Days in Stage | Deal Value | Next Action | Owner |
|-----------|---------------|------------|-------------|-------|
| [Deal] | X days | $XXX | [Action] | [Owner] |

**Total Active Deals**: {count across all stages}
**Total Pipeline Value**: ${sum of all deal values}

---

## Brand Scout Results (Awaiting Approval)

### High Priority (>$500K annual shipping)
- **[Company Name]** - {confidence} - [Brief description]
  - **Recommendation**: Pursue/Hold/Archive
  - **Action**: [If pursue, what's first step?]

### Medium Priority ($100K-$500K)
- **[Company Name]** - {confidence} - [Brief description]

### Low Priority (<$100K)
- **[Company Name]** - {confidence} - [Brief description]

**Human Decision Required**: Review recommendations above and approve HubSpot creation for selected leads.

---

## Priority Actions (Today)

**Based on priority scoring + urgency + brand scout results:**

1. **⚠️ URGENT**: Follow up with Upstate Prep (7+ days in Proposal-Sent) - call by 2 PM
2. **HIGH**: Create rates for Easy Group (Discovery complete, need to keep momentum)
3. **HIGH**: Approve Brand Scout leads and create HubSpot records for: [Company A, Company B]
4. **MEDIUM**: Confirm discovery call with Acme Corp (scheduled for tomorrow)
5. **MEDIUM**: Finalize Stackd Xparcel Ground rates (in progress)

---

## Follow-Up Queue (This Week)

**Today ({Date})**:
- [ ] Upstate Prep follow-up call
- [ ] Easy Group rate creation start
- [ ] Brand Scout approvals

**Tomorrow ({Date})**:
- [ ] Acme Corp discovery call (10 AM CT)
- [ ] Send Stackd proposal if rates finalized today

**Later This Week**:
- [ ] BoxiiShip pre-call questionnaire (due Thursday)
- [ ] Implementation check-in with [Customer] (Friday)

---

## Learning Capture (For EOD Sync)

**Patterns to Watch**:
- Deals in Proposal-Sent >7 days need aggressive follow-up
- Brand Scout leads from [industry X] converting well this month

**Context for Next Sync**:
- Focus on clearing Proposal-Sent backlog
- Monitor Acme Corp discovery call outcome (tomorrow)

---

**Generated**: {YYYY-MM-DD HH:MM AM/PM CT}
**Agent**: Prioritization Agent v3.0
```

## Strict Compliance Rules

### ✅ MUST DO
- Load yesterday's EOD markdown BEFORE fetching HubSpot data
- Reference previous sync context in output (show continuity)
- Calculate days in stage for every active deal
- Flag deals >7 days in current stage with ⚠️ warning
- Include brand scout results if any generated overnight
- Identify top 3-5 priority actions for today
- Update follow-up queue with due dates
- Save output to standard location for noon sync to load

### ❌ NEVER DO
- Skip loading previous sync context (breaks continuity chain)
- Generate priorities without fresh HubSpot data (stale info)
- Miss deals in any active stage (incomplete view)
- Mark sync complete without capturing learnings for EOD
- Auto-move deal folders (ask before moving)
- Auto-create HubSpot records from brand scout (approval gate)

## Quality Gates

Before marking 9AM sync complete:
- [ ] Yesterday's EOD context loaded and referenced
- [ ] All active deals fetched from HubSpot (verified count)
- [ ] Days in stage calculated for each deal
- [ ] Deals >7 days flagged with warnings
- [ ] Priority scoring applied and top 3-5 actions identified
- [ ] Brand scout results reviewed (if any)
- [ ] Follow-up queue updated with due dates
- [ ] Output saved in markdown format for noon sync

## Context Continuity Validation

**Required Context Elements from Yesterday's EOD**:
1. Key learnings captured
2. Incomplete actions to carry forward
3. Deals that progressed (stage changes)
4. Insights about deal patterns or trends

**If EOD file missing or incomplete**:
```python
# Alert user and request manual context
print("⚠️ Yesterday's EOD sync not found or incomplete.")
print("Please provide key context from yesterday:")
print("- What deals progressed?")
print("- What actions weren't completed?")
print("- Any important learnings?")

# Proceed with partial sync but flag as "degraded mode"
```

## HubSpot API Efficiency

**Batch Operations** (reduce API calls):
```python
from hubspot_sync_core import HubSpotSyncManager

sync_manager = HubSpotSyncManager(**config)

# Fetch all deals in one call with filters
active_deals = sync_manager.search_deals(
    filters=[
        {"propertyName": "dealstage", "operator": "IN", "values": [
            "01-discovery-scheduled",
            "02-discovery-complete",
            "03-rate-creation",
            "04-proposal-sent",
            "05-setup-docs-sent",
            "06-implementation"
        ]}
    ],
    properties=["dealname", "dealstage", "amount", "createdate", "hs_lastmodifieddate"],
    limit=100
)

# Calculate days in stage locally (no additional API calls)
for deal in active_deals:
    days_in_stage = calculate_days_between(
        deal['properties']['hs_lastmodifieddate'],
        today
    )
```

## Priority Score Tuning

**Adjust weights based on outcomes**:
- If deals in Discovery-Scheduled convert better → increase stage weight
- If high-value deals close faster → increase deal_value coefficient
- If brand scout leads need more nurturing → decrease brand_scout_flag multiplier

**Monthly Review** (during weekly sync on first Sunday of month):
- Analyze which priority scores correlated with closed-won deals
- Adjust formula coefficients for next month
- Document changes in `.claude/data/prioritization_tuning.md`

## Error Handling

**HubSpot API Failures**:
- Retry with exponential backoff (via `hubspot_sync_core.py`)
- If total failure, use cached data from yesterday + manual input
- Flag sync as "degraded mode" in output

**Missing EOD Context**:
- Request manual context summary from user
- Proceed with partial sync
- Document gap for future reference

**Brand Scout Output Issues**:
- If output folder missing, note "No new leads overnight"
- If output malformed, flag for manual review
- Don't block 9AM sync on brand scout issues

## Performance Metrics

**Target Benchmarks**:
- Sync completion: <5 minutes from start to saved output
- HubSpot API calls: <20 total (batch operations)
- Context loading: <30 seconds
- Report generation: <2 minutes

**Monthly Review**:
- Accuracy: Did prioritized actions align with closed-won outcomes?
- Completeness: Any deals missed in daily syncs?
- Timeliness: Were 7+ day warnings addressed promptly?

## Integration with Other Agents

**Feeds into**:
- **Noon Sync**: Loads 9AM priorities to track progress
- **3PM Sync**: References 9AM priorities for afternoon refinement
- **EOD Sync**: Uses 9AM context as starting point for learnings

**Receives from**:
- **EOD Sync** (previous day): Context, learnings, carry-forward actions
- **Brand Scout Agent**: Overnight research results for approval
- **Learning Agent**: Pattern insights for priority scoring adjustments

## Related Documentation

- [rules.md](../../rules.md) - Complete agent rules and sync flow constraints
- [.claude/docs/workflows/DAILY_SYNC_OPERATIONS.md](../docs/workflows/DAILY_SYNC_OPERATIONS.md) - Full sync workflow
- [.claude/docs/reference/NEBUCHADNEZZAR_REFERENCE.md](../docs/reference/NEBUCHADNEZZAR_REFERENCE.md) - Stage IDs and automation
