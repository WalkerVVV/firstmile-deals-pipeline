# Domain Memory Agent Integration Guide
**Nebuchadnezzar v2.0 - Persistent Intelligence Layer**

---

## Overview

The domain-memory-agent MCP provides AI-powered semantic search and persistent storage across Claude Code sessions. This guide shows how to integrate it into your daily sync workflows for continuous learning and intelligent deal management.

### Benefits Over Static Files
- **Semantic Search**: Find deals by intent ("urgent at-risk customers") not just keywords
- **Context Preservation**: Deal intelligence persists across restarts
- **Learning Accumulation**: Build organizational knowledge over time
- **Query Efficiency**: Sub-second retrieval with relevance scoring
- **Tag-Based Filtering**: Multi-dimensional deal organization

---

## Integration Points

### 1. EOD Sync Integration (Evening)

**When**: End of day after Superhuman email analysis

**What to Store**:
1. Daily learnings (what worked, what failed)
2. Deal stage movements with context
3. Customer interaction summaries
4. Blocker resolutions and workarounds
5. SOP evolution updates

#### EOD Storage Workflow

**Step 1: Store Today's Learnings**
```javascript
// After generating _DAILY_LOG.md
mcp__domain-memory-agent__store_document({
  id: "daily-learning-2025-10-13",
  title: "Daily Learnings - October 13, 2025",
  content: `
# What Worked ✅
1. **Short dedicated emails for critical asks**
   - DYLN dimensions request buried in long email → no response
   - Sent dedicated 3-line email → immediate reply
   - Impact: 48hr faster data collection
   - Status: PERMANENT SOP

2. **Customer Relationship Docs saved 30min per deal**
   - Clear action items, zero info loss
   - Now standard for [01-QUALIFIED] and above

# What Failed ❌
1. **Told customer "rates submitted" but blocked internally (Brock data)**
   - Risk: Credibility gap if early follow-up
   - Fix: Pre-check internal dependencies before customer comms
   - Status: TESTING

# Blockers Resolved
- DYLN: Brock data finally received after escalation
- Stackd: Rate card delivered (JIRA RATE-1897)
  `,
  tags: ["daily-learning", "sop-evolution", "2025-10-13", "wins", "failures"],
  metadata: {
    date: "2025-10-13",
    customer_touchpoints: 6,
    deals_advanced: 1,
    active_blockers: 0
  }
})
```

**Step 2: Store Deal Updates**
```javascript
// For each deal with significant activity today
mcp__domain-memory-agent__store_document({
  id: "stackd-logistics-update-2025-10-13",
  title: "Stackd Logistics - Rate Card Delivered",
  content: `
**Update Date**: October 13, 2025
**Stage**: [04-PROPOSAL-SENT]
**Contact**: Landon Richards

## Today's Activity
- Rate card v1 delivered via email
- Showing 5-10% savings (conservative estimate)
- Data verification concerns noted in analysis
- Meeting scheduled: Tuesday Oct 15, 10AM CST

## Key Points
- Conservative approach due to DHL rate discrepancies
- Need to verify actual invoice rates during call
- Lightweight profile (89.9% under 1lb) is ideal for FirstMile
- ShipHero integration required

## Next Steps
- Prep materials for Tuesday presentation
- Sample 10-20 shipments for rate validation
- Confirm service level mapping

## Risk Assessment
- RED FLAGS: Rate data quality issues
- Mitigation: Conservative estimates, verify before aggressive pricing
  `,
  tags: ["stackd-logistics", "proposal-sent", "rate-card-delivered", "2025-10-13", "conservative-estimate"],
  metadata: {
    company: "Stackd Logistics",
    deal_stage: "04-proposal-sent",
    date: "2025-10-13",
    contact: "Landon",
    next_meeting: "2025-10-15"
  }
})
```

**Step 3: Store Pipeline Movements**
```javascript
// When deals change stages
mcp__domain-memory-agent__store_document({
  id: "team-shipper-stage-change-2025-10-13",
  title: "Team Shipper - Advanced to Proposal Sent",
  content: `
**Stage Change**: [03-RATE-CREATION] → [04-PROPOSAL-SENT]
**Date**: October 13, 2025
**Trigger**: Rate card completed and emailed

## Evidence
Email sent at 3:45 PM with subject "FirstMile Rate Card - 38% Savings Opportunity"

## Deal Context
- Annual value: $280K
- Customer savings: $106K (38%)
- Profile: Regional, lightweight
- Next: 7-day follow-up scheduled

## Actions Taken
- HubSpot stage updated
- Follow-up task created (Oct 20)
- Customer Relationship Doc updated
  `,
  tags: ["team-shipper", "stage-change", "proposal-sent", "2025-10-13"],
  metadata: {
    company: "Team Shipper",
    old_stage: "03-rate-creation",
    new_stage: "04-proposal-sent",
    date: "2025-10-13",
    annual_value: 280000
  }
})
```

---

### 2. 9AM Sync Integration (Morning)

**When**: Start of day priority generation

**What to Query**:
1. Recent learnings applicable to today's deals
2. Historical context for deals you'll work on
3. Patterns from similar deals
4. Blocker resolutions for reference

#### 9AM Query Workflow

**Step 1: Get Applicable Learnings**
```javascript
// Before generating today's priority list
mcp__domain-memory-agent__semantic_search({
  query: "what worked yesterday failed blockers resolved",
  tags: ["daily-learning"],
  limit: 3
})
```

**Example Output**:
```
Recent Learnings (Last 3 Days):
✅ Short dedicated emails → 48hr faster responses
✅ Pre-check internal dependencies before customer comms
❌ Long emails bury critical asks
```

**Step 2: Query Context for Priority Deals**
```javascript
// For each P1 deal on today's list
mcp__domain-memory-agent__semantic_search({
  query: "Stackd Logistics recent activity rate card meeting",
  limit: 1
})
```

**Example Output**:
```
Stackd Logistics Context:
- Rate card delivered Oct 13
- Meeting: Tuesday Oct 15, 10AM CST
- RED FLAGS: Data verification needed
- Action: Prep conservative presentation materials
```

**Step 3: Find Similar Deal Patterns**
```javascript
// When planning approach for new deal
mcp__domain-memory-agent__semantic_search({
  query: "3PL lightweight DHL competitive successful",
  tags: ["3pl", "lightweight"],
  limit: 3
})
```

---

### 3. Deal Progression Integration

**When**: Completing major milestones (discovery, analysis, proposal)

**What to Store**: Comprehensive analysis summaries

#### Discovery Complete Storage
```javascript
mcp__domain-memory-agent__store_document({
  id: "acme-corp-discovery-2025-10-13",
  title: "Acme Corp - Discovery Call Summary",
  content: `
**Discovery Date**: October 13, 2025
**Attendees**: Jordan Blake (Ops Director), Brett Walker (FirstMile)
**Stage**: [02-DISCOVERY-COMPLETE]

## Key Requirements
- Volume: ~20,000 packages/month
- Weight: Majority <1 lb (apparel)
- Geography: CA warehouse → East Coast heavy (NYC, BOS, DC)
- Pain Points:
  - UPS costs killing margins (avg $12/pkg)
  - Slow 5-7 day transit to East Coast
  - High zone 7-8 charges
- Timeline: Needs solution by Q4 peak (Nov 15)

## Decision Makers
- Jordan Blake: Ops Director (day-to-day authority)
- Sarah Chen: CFO (final approval >$100K)
- Monthly purchasing committee: 3rd Thursday

## Current State
- Carrier: UPS Ground 90%, USPS 10%
- Integration: ShipStation API
- Warehouse: Fontana, CA (single location)

## FirstMile Fit Assessment
✅ Excellent: Lightweight, high-volume, regional-heavy
✅ Strong: Single origin aligns with Select Network
⚠️ Watch: Timeline pressure (6 weeks to implementation)

## Next Steps
1. PLD data requested (3 months history)
2. Follow-up: Oct 20 (7 days)
3. Target rate delivery: Oct 27
4. Decision deadline: Nov 5 (before peak)

## Opportunity Size
- Estimated annual value: $2.1M
- Customer savings: $650K-$800K (30-38%)
  `,
  tags: ["acme-corp", "discovery-complete", "apparel", "california-origin", "east-coast-heavy", "lightweight", "Q4-2025-target"],
  metadata: {
    company: "Acme Corp",
    stage: "02-discovery-complete",
    discovery_date: "2025-10-13",
    annual_value: 2100000,
    monthly_volume: 20000,
    primary_contact: "Jordan Blake",
    decision_maker: "Sarah Chen",
    timeline_deadline: "2025-11-05"
  }
})
```

#### Analysis Complete Storage
```javascript
// After running PLD analysis
mcp__domain-memory-agent__store_document({
  id: "acme-corp-analysis-2025-10-20",
  title: "Acme Corp - Comprehensive Shipping Analysis",
  content: `
[Copy full analysis from pld_analysis.py output]

## Key Findings
- 78% under 1 lb (perfect for Xparcel Ground)
- 65% Zones 5-8 (Select Network zone-skipping opportunity)
- 8,200 packages at 15-15.99 oz threshold (weight optimization)
- Current avg cost: $11.85/pkg
- FirstMile projected: $7.20/pkg (39% savings)

## Service Recommendations
- Xparcel Ground: 85% of volume
- Xparcel Expedited: 10% (time-sensitive)
- Xparcel Priority: 5% (premium)

## Implementation Notes
- ShipStation API integration (standard 2-week timeline)
- Pilot program: 1,000 packages recommended
- Go-live target: Nov 8 (before Black Friday)
  `,
  tags: ["acme-corp", "analysis-complete", "pld-analysis", "39-percent-savings", "weight-optimization", "select-network-fit"],
  metadata: {
    company: "Acme Corp",
    analysis_date: "2025-10-20",
    savings_percentage: 39,
    annual_savings: 700000,
    weight_under_1lb: 78,
    select_network_percentage: 65
  }
})
```

---

### 4. Weekly Sync Integration (Friday EOD)

**When**: End of week reflection

**What to Store**: SOP evolution, pattern recognition, strategic insights

#### Weekly Learning Storage
```javascript
mcp__domain-memory-agent__store_document({
  id: "weekly-learning-2025-w41",
  title: "Week 41 (Oct 7-11) - Pipeline Learnings & SOP Evolution",
  content: `
# Week 41 Summary - October 7-11, 2025

## Pipeline Metrics
- Deals Advanced: 4 (Team Shipper, Stackd, Acme, BoxiiShip)
- New Deals Created: 2
- Closed Won: 0
- Closed Lost: 1 (Caputron - pricing concerns)

## Validated SOPs (Now PERMANENT ✅)
### v3.1: Customer Relationship Documentation
- Saved 30+ min per deal, zero info loss
- 7 docs created this week
- **Action**: Now mandatory for [01-QUALIFIED] and above

### v3.4: Internal Dependency Pre-Check
- Prevented 2 credibility gaps (DYLN, Upstate Prep)
- Add checklist: "Are rates actually submitted to JIRA?"
- **Action**: Pre-flight checklist before customer comms

## SOPs In Testing (Week 2) 🟡
### v3.2: Automated Stale Deal Alerts
- Flagged 3 deals: Upstate Prep (44d), Caputron (32d), DYLN (18d)
- All required immediate action
- **Status**: Extend testing 1 more week, then promote to PERMANENT

## Pattern Recognition - This Week
### Lightweight Deal Success Pattern
- 3 deals advanced: All >75% under 1 lb
- Avg savings: 38%
- Avg time to proposal: 12 days (vs 18d average)
- **Insight**: Prioritize lightweight prospects for faster velocity

### Price Sensitivity by Industry
- 3PL/Fulfillment: Sensitive to margin compression (5-10% acceptable)
- DTC Brands: Focus on service quality over pure cost (15%+ needed)
- **Insight**: Tailor savings messaging by industry

### East Coast Destination Advantage
- Select Network zone-skipping = 28% additional savings
- Messaging shift: Lead with transit time improvement, then cost
- **Insight**: Geographic profile should drive pitch strategy

## Bottlenecks Identified
- [03-RATE-CREATION]: Still 8 deals, 2 over SLA
- Root cause: JIRA queue + data quality issues
- **Proposed Fix**: Pre-qualify data before entering [03]

## At-Risk Deals Recovered
- Driftaway Coffee: Recovery call successful, back in [04]
- Action: Proactive service recovery within 48hrs prevents churn

## Strategic Insights
1. **Pipeline Velocity**: Lightweight deals move 33% faster
2. **Win Rate**: Data quality correlates with win rate (verified data = 68% win vs 42% unverified)
3. **Service Recovery**: 48-hour response window critical for at-risk customers

## Action Items for Next Week
1. Reduce [03] stage from 18d avg to 14d (target: clear 2 oldest deals)
2. Implement data pre-qualification checklist (prevent GIGO)
3. Test geographic pitch segmentation (East vs West)
  `,
  tags: ["weekly-learning", "2025-w41", "sop-evolution", "pattern-recognition", "pipeline-velocity"],
  metadata: {
    week: "2025-W41",
    deals_advanced: 4,
    sops_validated: 2,
    bottlenecks: ["rate-creation"],
    key_insight: "lightweight-deals-move-faster"
  }
})
```

---

### 5. Ad-Hoc Query Patterns

#### Find Similar Past Deals
```javascript
// When encountering new deal with specific profile
mcp__domain-memory-agent__semantic_search({
  query: "apparel DTC California origin East Coast heavy lightweight successful closed won",
  limit: 5
})
```

#### Find Solution to Current Problem
```javascript
// When stuck on issue
mcp__domain-memory-agent__semantic_search({
  query: "customer concerned about transit time zone 7-8 how resolved",
  tags: ["service-recovery", "closed-won"],
  limit: 3
})
```

#### Find Applicable Learnings
```javascript
// Before important customer call
mcp__domain-memory-agent__semantic_search({
  query: "3PL objection handling pricing concerns successful conversion",
  tags: ["3pl", "closed-won"],
  limit: 3
})
```

#### Review Past Performance
```javascript
// Monthly review
mcp__domain-memory-agent__semantic_search({
  query: "weekly learning pipeline velocity bottleneck resolution",
  tags: ["weekly-learning"],
  limit: 4  // Last 4 weeks
})
```

---

## Automation Integration

### Daily Sync Script Enhancement

**File**: `daily_9am_workflow.py`

Add MCP query phase:

```python
# After loading _PIPELINE_TRACKER.csv
# Before generating priority list

# Query recent learnings
learnings = mcp_semantic_search(
    query="daily learning yesterday what worked what failed",
    tags=["daily-learning"],
    limit=3
)

# Query context for P1 deals
for deal in priority_1_deals:
    context = mcp_semantic_search(
        query=f"{deal.name} recent activity status",
        limit=1
    )
    deal.context_summary = context[0].relevant_excerpts if context else None

# Generate enhanced priority list with context
```

### EOD Sync Script Enhancement

**File**: Add `eod_memory_storage.py`

```python
import json
from datetime import datetime

def store_eod_learnings(daily_log_path, learnings_summary):
    """Store EOD learnings in domain-memory-agent"""

    date_str = datetime.now().strftime("%Y-%m-%d")
    doc_id = f"daily-learning-{date_str}"

    # Extract sections from _DAILY_LOG.md
    with open(daily_log_path, 'r') as f:
        content = f.read()

    # Store in MCP
    mcp_store_document(
        id=doc_id,
        title=f"Daily Learnings - {date_str}",
        content=content,
        tags=["daily-learning", date_str, "auto-stored"],
        metadata={
            "date": date_str,
            "source": "eod_sync",
            "type": "learning"
        }
    )

    print(f"✅ Stored daily learnings: {doc_id}")

def store_deal_updates(deals_with_activity):
    """Store significant deal updates"""

    for deal in deals_with_activity:
        if deal.significance_score > 0.7:  # Major activity only
            doc_id = f"{deal.slug}-update-{datetime.now().strftime('%Y-%m-%d')}"

            mcp_store_document(
                id=doc_id,
                title=f"{deal.name} - {deal.activity_summary}",
                content=deal.full_context,
                tags=[deal.slug, deal.stage, "deal-update", "auto-stored"],
                metadata={
                    "company": deal.name,
                    "stage": deal.stage,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "annual_value": deal.amount
                }
            )

            print(f"✅ Stored deal update: {doc_id}")
```

---

## Best Practices

### Storage Principles
1. **Store Insights, Not Raw Data**: Summarize, don't dump
2. **Tag Aggressively**: More tags = better retrieval
3. **Include Context**: Why this matters, what it means
4. **Date Everything**: Chronological tracking critical
5. **Link Related Items**: Reference past deals/learnings

### Search Principles
1. **Intent-Based Queries**: Describe what you need, not keywords
2. **Filter with Tags**: Narrow scope before semantic search
3. **Review Multiple Results**: Relevance scoring may surprise you
4. **Iterate Queries**: Refine based on initial results
5. **Combine with Traditional Search**: Grep for precision, MCP for discovery

### Maintenance Principles
1. **Weekly Review**: Check stored content quality
2. **Archive Old Content**: Move historical data after 6 months
3. **Update Tags**: Add new categorizations as patterns emerge
4. **Consolidate Duplicates**: Merge similar learnings
5. **Summary Documents**: Create quarterly rollups

---

## Quick Command Reference

### Store Document
```javascript
mcp__domain-memory-agent__store_document({
  id: "unique-id",
  title: "Human-readable title",
  content: "Full markdown content",
  tags: ["tag1", "tag2"],
  metadata: {key: "value"}
})
```

### Semantic Search
```javascript
mcp__domain-memory-agent__semantic_search({
  query: "natural language query",
  tags: ["optional-filter"],
  limit: 5,
  minScore: 0.0
})
```

### Get Document
```javascript
mcp__domain-memory-agent__get_document({
  documentId: "unique-id"
})
```

### List All Documents
```javascript
mcp__domain-memory-agent__list_documents({
  tags: ["optional-filter"],
  sortBy: "updated",  // or "created", "title"
  limit: 50
})
```

### Summarize Document
```javascript
mcp__domain-memory-agent__summarize({
  documentId: "unique-id",
  maxSentences: 5
})
```

---

## Migration Checklist

- [x] 3 existing deals migrated (Josh's Frogs, Stackd, JM Group)
- [ ] Update `daily_9am_workflow.py` to query learnings
- [ ] Create `eod_memory_storage.py` script
- [ ] Add MCP queries to EOD sync workflow
- [ ] Store this week's learnings from _DAILY_LOG_FEEDBACK.md
- [ ] Test semantic search for priority deals
- [ ] Document common query patterns
- [ ] Train on weekly sync integration
- [ ] Archive JSON/Markdown backup system (optional)

---

**Last Updated**: October 13, 2025
**System**: Nebuchadnezzar v2.0
**Integration**: domain-memory-agent MCP v1.0
