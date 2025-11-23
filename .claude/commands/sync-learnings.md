# System Documentation Update Command

Update all system documentation based on recent learnings and session work.

---

## Execution Process

### Phase 1: Gather Learnings

1. **Analyze current session** for:
   - API errors encountered and their solutions
   - Read-only fields discovered
   - Correct formats/patterns learned
   - New automation patterns implemented
   - Common mistakes to avoid

2. **Check memory** for recent stored learnings:
   ```
   mcp__plugin_episodic-memory_episodic-memory__search
   Query: ["hubspot", "learnings", "errors", "patterns"]
   ```

3. **Review recent sync reports** for issues:
   - `sync_reports/` - Latest reports
   - Error patterns in outputs

---

### Phase 2: Update Global Rules

**File**: `~/.claude/RULES.md`

1. **Read current rules**:
   ```
   Read ~/.claude/RULES.md
   ```

2. **Check for needed updates**:
   - New API patterns to add?
   - New "Do" items from successful patterns?
   - New "Don't" items from errors encountered?
   - Stale entries to clean up?
   - Auto-triggers to add?

3. **Add to appropriate sections**:
   - `### HubSpot API Rules` - API-specific patterns
   - `### Do` - Successful patterns
   - `### Don't` - Error prevention
   - `### Auto-Triggers` - Automation rules

4. **Clean up**:
   - Remove duplicate entries
   - Remove stale "add to memory" notes
   - Ensure consistent formatting

---

### Phase 3: Update Project CLAUDE.md

**File**: `FirstMile_Deals/CLAUDE.md`

1. **Read current file**:
   ```
   Read C:\Users\BrettWalker\FirstMile_Deals\CLAUDE.md
   ```

2. **Check alignment with RULES.md**:
   - Do Critical Field Rules match?
   - Are new patterns documented?
   - Are references to guides correct?

3. **Update sections**:
   - `**Critical Field Rules**` - API patterns
   - `### Known Issues & Solutions` - Error fixes
   - `## See Also` - Reference links

4. **Add cross-references** to detailed guides when created

---

### Phase 4: Create/Update Reference Guides

**Location**: `.claude/docs/reference/`

1. **If significant learnings exist**, create detailed guide:
   ```
   .claude/docs/reference/[TOPIC]_GUIDE.md
   ```

2. **Include in guide**:
   - Critical errors and solutions
   - Code patterns with examples
   - Common mistakes to avoid
   - Quick reference commands

3. **Update existing guides** if patterns evolved

---

### Phase 5: Store to Memory

1. **Create memory entry** with key learnings:
   ```
   mcp__plugin_domain-memory-agent_knowledge-base__store_document
   Title: "[Topic] Implementation Learnings"
   Tags: ["learnings", "patterns", relevant-tags]
   ```

2. **Include**:
   - Critical errors and fixes
   - Key patterns discovered
   - Reference to guide location

---

### Phase 6: Verification

1. **Confirm documentation chain**:
   - [ ] `~/.claude/RULES.md` - Global rules updated
   - [ ] `FirstMile_Deals/CLAUDE.md` - Project docs updated
   - [ ] `.claude/docs/reference/` - Detailed guide created/updated
   - [ ] Memory - Learnings stored for future sessions

2. **Check cross-references**:
   - CLAUDE.md references guide?
   - Guide referenced in relevant sections?

3. **Report summary**:
   ```
   ## Documentation Update Complete

   | File | Updates |
   |------|---------|
   | RULES.md | [summary] |
   | CLAUDE.md | [summary] |
   | Reference Guide | [filename] |
   | Memory | [document ID] |
   ```

---

## Key Patterns to Capture

### API Learnings
- Read-only fields and workarounds
- Correct timestamp/date formats
- Required filters to avoid data explosions
- Association type IDs
- Error codes and meanings

### Code Patterns
- Division by zero protection
- Windows encoding fixes
- Subprocess communication patterns
- Async/rate limiting patterns

### Automation Patterns
- Stage-based logic (next steps, due dates)
- Bulk update patterns
- Task creation for date fields

### Error Prevention
- Common mistakes that cause failures
- Validation patterns
- Pre-execution checks

---

## Usage

Run after any session with significant learnings:

```bash
/update-system-docs
```

Or when explicitly updating documentation:

```bash
/update-system-docs --focus hubspot
/update-system-docs --focus sync-system
/update-system-docs --focus api-patterns
```

---

## Example Output

```
## System Documentation Updated

### Learnings Captured
- HubSpot `notes_next_activity_date` is read-only
- Timestamps must be Unix ms as STRING
- Required Owner ID + Pipeline ID filters

### Files Updated
| File | Changes |
|------|---------|
| ~/.claude/RULES.md | +7 HubSpot rules, +6 Do/Don't |
| CLAUDE.md | +4 Critical Field Rules |
| HUBSPOT_DEAL_HYGIENE_GUIDE.md | Created (new) |

### Memory Stored
ID: 89d7f5336994517f
Tags: hubspot, deal-hygiene, api, lessons-learned

### Cross-References
- CLAUDE.md → HUBSPOT_DEAL_HYGIENE_GUIDE.md ✅
- RULES.md → Auto-triggers updated ✅
```

---

*Command created: November 22, 2025*
*Based on HubSpot Deal Hygiene implementation session*
