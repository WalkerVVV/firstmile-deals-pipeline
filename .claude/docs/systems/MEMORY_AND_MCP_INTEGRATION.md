# Memory & MCP Integration Guide
**Continuous Learning + HubSpot Integration for Nebuchadnezzar v2.0**

---

## Overview

This guide covers two critical systems:
1. **Claude Memory System** - Persistent learning across sessions
2. **HubSpot MCP Integration** - Direct HubSpot API access via MCP protocol

---

## Part 1: Claude Memory System

### What is Claude Memory?

Claude's memory system allows persistent storage of learnings, patterns, and context across sessions. Unlike temporary context, memories are:
- **Persistent**: Survive session restarts
- **Retrievable**: Automatically recalled when relevant
- **Updatable**: Can be refined based on new learnings

### Memory Categories for Nebuchadnezzar

#### 1. Pipeline Patterns & Best Practices
```
Memory Name: "Pipeline Best Practices - {Topic}"

Examples:
- "Pipeline Best Practices - Rate Creation"
- "Pipeline Best Practices - Discovery Calls"
- "Pipeline Best Practices - Follow-up Timing"
```

#### 2. Customer Relationship Insights
```
Memory Name: "Customer Pattern - {Pattern Type}"

Examples:
- "Customer Pattern - Decision Making Process"
- "Customer Pattern - Data Request Timing"
- "Customer Pattern - Pricing Sensitivity"
```

#### 3. Deal Execution Learnings
```
Memory Name: "Deal Learning - {Company} - {Topic}"

Examples:
- "Deal Learning - Stackd - Rate Presentation"
- "Deal Learning - DYLN - Multi-location Discovery"
- "Deal Learning - Driftaway - Recovery Strategy"
```

#### 4. System Optimizations
```
Memory Name: "System Optimization - {Area}"

Examples:
- "System Optimization - Email Templates"
- "System Optimization - Internal Dependencies"
- "System Optimization - SLA Management"
```

### How to Use Memory in Daily Syncs

#### EOD Sync Memory Capture

**After completing EOD sync, save learnings to memory:**

```markdown
## EOD Sync - {Date} - Memory Capture

### What Worked ✅ → Save to Memory
Pattern: Customer Relationship Documentation
Memory: "Pipeline Best Practices - Documentation"
Learning: "Creating Customer_Relationship_Documentation.md for all [01-QUALIFIED]+ deals saves 30min per deal and prevents information loss. Make this mandatory for all qualified opportunities."

### What Failed ❌ → Save to Memory
Pattern: Brock Data Dependency
Memory: "System Optimization - Internal Dependencies"
Learning: "Always pre-check internal dependencies (Brock data, JIRA status, pricing approvals) BEFORE communicating delivery timelines to customers. This prevents credibility gaps."

### Emerging Pattern → Save to Memory
Pattern: Multi-location Discovery
Memory: "Customer Pattern - Multi-location Opportunities"
Learning: "Asking 'Any other locations or brands?' during discovery can 3X deal value. DYLN went from $1.2M to $3.6M with this question. Add to standard discovery script."
```

**Command to save memory:**
```
Please save this to memory under the name "[Memory Name]": [Learning content]
```

#### 9AM Sync Memory Retrieval

**Start each day by asking:**
```
"Retrieve memories related to:
- Pipeline best practices
- [Specific deal name] learnings
- [Specific challenge] patterns"
```

**Example:**
```
User: "I'm working on Stackd Logistics proposal presentation today. What do we know?"

Claude retrieves:
- Memory: "Deal Learning - Stackd - Rate Presentation"
- Memory: "Pipeline Best Practices - Proposal Delivery"
- Memory: "Customer Pattern - Decision Making Process"
```

### Memory Update Workflow

**Weekly Memory Refinement (Friday EOD)**:

1. **Review Current Memories**
   ```
   "Show me all memories related to pipeline optimization"
   ```

2. **Update Based on New Data**
   ```
   "Update memory 'Pipeline Best Practices - Follow-up Timing' with:
   New learning: 7-day follow-up on proposals shows 40% higher response rate than 14-day"
   ```

3. **Archive Outdated Patterns**
   ```
   "Mark memory 'Old Process - Rate Creation' as superseded by SOP v3.2"
   ```

### Memory Categories & Naming Convention

```yaml
Naming Pattern: "{Category} - {Specific Topic} - {Optional Subcategory}"

Categories:
  - "Pipeline Best Practices"
  - "Customer Pattern"
  - "Deal Learning"
  - "System Optimization"
  - "SOP Evolution"
  - "Competitive Intelligence"
  - "Internal Process"

Examples:
  ✅ "Pipeline Best Practices - Discovery - Multi-location Questions"
  ✅ "Customer Pattern - Pricing - Discount Thresholds"
  ✅ "Deal Learning - DYLN - Multi-site Opportunity Discovery"
  ✅ "System Optimization - Email - Critical Ask Separation"
  ✅ "SOP Evolution - v3.1 - Customer Relationship Docs"
```

### Integration with Daily Sync Files

**EOD Sync Template Enhancement:**

```markdown
## EOD Sync - {Date}

### What Worked ✅
1. **{Pattern Name}**
   - What: {Description}
   - Impact: {Measurable result}
   - **MEMORY**: Save as "{Memory Name}"
   - **KEEP**: {Action to make permanent}

### What Failed ❌
1. **{Problem}**
   - What happened: {Description}
   - Risk: {Business impact}
   - **MEMORY**: Save as "{Memory Name}"
   - **FIX**: {Corrective action}

[At end of sync]
## Memory Capture Commands

```
Please save these learnings to memory:
1. Name: "Pipeline Best Practices - {Topic}"
   Content: "{Learning from What Worked}"

2. Name: "System Optimization - {Area}"
   Content: "{Learning from What Failed}"
```
```

---

## Part 2: HubSpot MCP Integration

### Current Status: NOT CONFIGURED ⚠️

**Available MCP Servers**:
- ✅ Notion MCP (Connected)
- ✅ Kapture MCP (Connected)
- ❌ HubSpot MCP (Not installed)

### Installing HubSpot MCP Server

#### Option 1: Official HubSpot MCP (@hubspot/mcp-server)

**Installation:**
```bash
# Install the official HubSpot MCP server
npm install -g @hubspot/mcp-server

# Or use via npx (no install needed)
npx @hubspot/mcp-server
```

**Configuration:**
```bash
# Add to Claude MCP config
claude mcp add @hubspot/mcp-server \
  --env HUBSPOT_API_KEY="${HUBSPOT_API_KEY}" \
  --env HUBSPOT_PORTAL_ID="46526832"
```

#### Option 2: Community HubSpot MCP (hubspot-mcp-server)

**Installation:**
```bash
# Install community version with more features
npm install -g hubspot-mcp-server

# Or use via npx
npx hubspot-mcp-server
```

**Configuration:**
```bash
# Add to Claude MCP config
claude mcp add hubspot-mcp-server \
  --env HUBSPOT_ACCESS_TOKEN="${HUBSPOT_API_KEY}"
```

### MCP Configuration File

**Location**: `~/.config/claude/mcp_config.json` or project `.claude/mcp_config.json`

**Add HubSpot server:**
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": [
        "@notionhq/notion-mcp-server",
        "-e",
        "NOTION_API_KEY=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"
      ]
    },
    "kapture": {
      "command": "npx",
      "args": ["-y", "kapture-mcp@latest", "bridge"]
    },
    "hubspot": {
      "command": "npx",
      "args": [
        "@hubspot/mcp-server"
      ],
      "env": {
        "HUBSPOT_API_KEY": "${HUBSPOT_API_KEY}",
        "HUBSPOT_PORTAL_ID": "46526832"
      }
    }
  }
}
```

### HubSpot MCP Capabilities

Once configured, the HubSpot MCP provides:

#### Available Tools
```yaml
hubspot-search-contacts:
  description: Search contacts by email, name, or company

hubspot-get-contact:
  description: Get contact details by ID

hubspot-create-contact:
  description: Create new contact

hubspot-update-contact:
  description: Update contact properties

hubspot-search-deals:
  description: Search deals by filters

hubspot-get-deal:
  description: Get deal details by ID

hubspot-create-deal:
  description: Create new deal

hubspot-update-deal:
  description: Update deal properties

hubspot-create-note:
  description: Add note to contact/deal

hubspot-create-task:
  description: Create task

hubspot-get-pipeline:
  description: Get pipeline stages
```

### Using HubSpot MCP in Daily Syncs

#### 9AM Sync with HubSpot MCP

**Instead of manual Python scripts:**
```markdown
## 9AM Sync - HubSpot MCP Integration

# Step 1: Get all active deals
Use: hubspot-search-deals
Filter: owner_id=699257003, pipeline=8bd9336b-4767-4e67-9fe2-35dfcad7c8be

# Step 2: Get deals by priority stages
Use: hubspot-search-deals
Filter: dealstage IN [1090865183, d607df25-2c6d-4a5d-9835-6ed1e4f4020a]

# Step 3: Create follow-up tasks
For each priority deal:
  Use: hubspot-create-task
  Properties: title, due_date, priority, deal_id
```

#### EOD Sync with HubSpot MCP

**Log activities directly:**
```markdown
# After customer touchpoint
Use: hubspot-create-note
Deal ID: {deal_id}
Note: "Call with Jordan - Discussed pricing, needs CFO approval. Follow-up Oct 14."

# Create next-day task
Use: hubspot-create-task
Deal ID: {deal_id}
Title: "Follow up post-CFO approval"
Due: 2025-10-14
Priority: HIGH
```

### Verification Commands

**Check MCP status:**
```bash
# List all MCP servers
claude mcp list

# Check HubSpot connection
claude mcp test hubspot

# View available tools
claude mcp describe hubspot
```

---

## Part 3: Integrated Memory + MCP Workflow

### Daily Sync with Memory & MCP

#### 9AM Sync - Complete Flow

**1. Retrieve Relevant Memories**
```
Claude, retrieve memories related to:
- Pipeline best practices for rate creation
- Stackd Logistics deal learnings
- Follow-up timing patterns
```

**2. Query HubSpot via MCP**
```
Use hubspot-search-deals to get:
- All deals in [03-RATE-CREATION] stage
- All deals in [04-PROPOSAL-SENT] stage
- Deals not modified in >14 days
```

**3. Generate Priority Actions**
```
Based on:
- Retrieved memories (what's worked before)
- Current HubSpot deal status
- SLA thresholds

Output: Priority action list with context from memory
```

#### EOD Sync - Complete Flow

**1. Log Activities to HubSpot**
```
For each customer touchpoint:
  Use: hubspot-create-note
  Deal ID: {id}
  Content: {summary}
```

**2. Create Tomorrow's Tasks**
```
Use: hubspot-create-task
Based on: Memory of optimal follow-up timing
```

**3. Capture Learnings to Memory**
```
Save to memory:
- What worked (with HubSpot deal examples)
- What failed (with corrective actions)
- Emerging patterns (for future deals)
```

**4. Update _DAILY_LOG_FEEDBACK.md**
```
Include:
- HubSpot activity summary
- Memory captures performed
- Cross-reference between memory and HubSpot
```

### Weekly Learning Archive

**Friday EOD - Memory + Saner.ai Integration**

**1. Export Week's Memories**
```
List all memories created this week:
- Pipeline best practices
- Customer patterns
- Deal learnings
- System optimizations
```

**2. Consolidate to Saner.ai**
```
Export format:
---
Week of {Date} - Pipeline Intelligence

## New Patterns Discovered
[Memories from "Customer Pattern" category]

## Process Improvements
[Memories from "System Optimization" category]

## Deal-Specific Insights
[Memories from "Deal Learning" category]

## SOP Evolution
[Memories from "SOP Evolution" category]
---
```

**3. Update Master Memory Index**
```
Create/update memory: "Memory Index - {Month}"
Content: List of all active memories with summaries
```

---

## Part 4: Implementation Checklist

### Phase 1: HubSpot MCP Setup (Do First)

- [ ] Choose HubSpot MCP server (@hubspot/mcp-server recommended)
- [ ] Install via npm or configure for npx usage
- [ ] Add to MCP config file with API credentials
- [ ] Verify connection: `claude mcp test hubspot`
- [ ] Test basic operations (search deals, create task)
- [ ] Update Python scripts to use MCP instead of direct API

### Phase 2: Memory System Setup

- [ ] Define memory naming conventions (already documented above)
- [ ] Create initial memories from existing learnings in _DAILY_LOG_FEEDBACK.md
- [ ] Update EOD sync template to include memory capture
- [ ] Update 9AM sync to retrieve relevant memories
- [ ] Test memory retrieval across sessions

### Phase 3: Integration

- [ ] Modify daily_9am_workflow.py to use HubSpot MCP
- [ ] Add memory retrieval to 9AM sync script
- [ ] Update EOD sync to save learnings to memory
- [ ] Create weekly memory export to Saner.ai workflow
- [ ] Document memory + MCP usage in DAILY_SYNC_OPERATIONS.md

### Phase 4: Validation

- [ ] Run 9AM sync with memory + MCP for 1 week
- [ ] Verify memories are recalled appropriately
- [ ] Confirm HubSpot MCP reduces API call complexity
- [ ] Test cross-session memory persistence
- [ ] Archive successful patterns to Saner.ai

---

## Part 5: Quick Reference

### Memory Commands

**Save Learning:**
```
"Save to memory as '{Category} - {Topic}': {Learning content}"
```

**Retrieve Memories:**
```
"Retrieve memories related to: {topic/deal/pattern}"
```

**Update Memory:**
```
"Update memory '{Name}' with: {new learning}"
```

**List Memories:**
```
"Show all memories in category: {category}"
```

### HubSpot MCP Commands

**Search Deals:**
```
Use: hubspot-search-deals
Filter: owner_id=699257003, dealstage=1090865183
```

**Create Task:**
```
Use: hubspot-create-task
Deal: {id}
Title: {title}
Due: {date}
Priority: HIGH
```

**Add Note:**
```
Use: hubspot-create-note
Deal: {id}
Note: {content}
```

### Configuration Files

**MCP Config**: `~/.config/claude/mcp_config.json`
**Memory Index**: Stored in Claude's persistent memory
**Daily Logs**: `C:\Users\BrettWalker\Downloads\_DAILY_LOG_FEEDBACK.md`
**Archive**: Saner.ai notes system

---

## Part 6: Migration from Current System

### Current State
- ✅ Python scripts: `daily_9am_workflow.py`, `daily_9am_sync.py`
- ✅ Manual API calls with hardcoded credentials
- ✅ File-based learning capture (`_DAILY_LOG_FEEDBACK.md`)
- ❌ No persistent memory across sessions
- ❌ No HubSpot MCP integration

### Target State
- ✅ HubSpot MCP for all CRM operations
- ✅ Claude Memory for persistent learnings
- ✅ Integrated daily sync with memory retrieval
- ✅ Automated learning capture to memory
- ✅ Weekly export to Saner.ai

### Migration Steps

**Week 1: HubSpot MCP**
1. Install and configure HubSpot MCP
2. Test all operations (search, create, update)
3. Run parallel: Python scripts + MCP validation

**Week 2: Memory System**
1. Migrate existing learnings from `_DAILY_LOG_FEEDBACK.md` to memories
2. Update daily sync templates for memory capture
3. Test memory retrieval in morning syncs

**Week 3: Integration**
1. Replace Python API calls with MCP tools
2. Add memory retrieval to 9AM sync
3. Automate memory capture in EOD sync

**Week 4: Validation & Optimization**
1. Verify all workflows using memory + MCP
2. Archive to Saner.ai
3. Document final patterns

---

## Troubleshooting

### HubSpot MCP Issues

**Issue**: MCP server not connecting
```bash
# Check server status
claude mcp list

# Restart server
claude mcp restart hubspot

# Check logs
claude mcp logs hubspot
```

**Issue**: Authentication errors
```
# Verify API key is valid
# Check HubSpot portal access
# Regenerate token if needed
```

### Memory Issues

**Issue**: Memories not persisting
```
# Verify memory was saved
"List all memories created today"

# Re-save if needed
"Save to memory as '{Name}': {Content}"
```

**Issue**: Memory retrieval not working
```
# Check memory name
"Show memory named '{exact name}'"

# Try broader search
"Retrieve all memories related to: {topic}"
```

---

**Last Updated**: October 7, 2025
**Status**: HubSpot MCP - Not Configured (needs setup)
**Status**: Memory System - Ready to implement
**Next Steps**: Install HubSpot MCP server and configure
