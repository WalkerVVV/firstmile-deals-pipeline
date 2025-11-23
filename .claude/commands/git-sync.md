# Git Sync & Commit Command

Comprehensive git workflow: stage, commit, push with intelligent message generation.

---

## Execution Process

### Phase 1: Assess Repository State

1. **Check current status**:
   ```bash
   git status
   ```

2. **Review recent commits** for message style:
   ```bash
   git log --oneline -10
   ```

3. **View all changes** (staged and unstaged):
   ```bash
   git diff
   git diff --staged
   ```

4. **Identify untracked files**:
   ```bash
   git status --porcelain
   ```

---

### Phase 2: Analyze Changes

1. **Categorize changes by type**:
   - `feat:` - New feature or capability
   - `fix:` - Bug fix
   - `docs:` - Documentation only
   - `refactor:` - Code restructure without behavior change
   - `chore:` - Maintenance, dependencies, config
   - `test:` - Test additions or modifications
   - `perf:` - Performance improvement

2. **Identify primary change**:
   - What is the main purpose of these changes?
   - What problem does it solve?
   - What capability does it add?

3. **Check for sensitive files**:
   - `.env` files - NEVER commit
   - API keys, tokens, credentials
   - `settings.local.json`
   - Warn user if detected

---

### Phase 3: Stage Files

1. **Review each changed file**:
   - Is it intentional?
   - Should it be in this commit?
   - Does it belong in `.gitignore`?

2. **Stage appropriate files**:
   ```bash
   git add [specific-files]
   ```

3. **Or stage all**:
   ```bash
   git add .
   ```

4. **Verify staging**:
   ```bash
   git status
   ```

---

### Phase 4: Generate Commit Message

**Format**:
```
<type>: <concise description>

<detailed explanation of why, not what>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Message Guidelines**:
- First line: 50 chars max, imperative mood ("add" not "added")
- Body: Explain WHY the change was made
- Reference issues/tickets if applicable
- Focus on business value, not implementation details

**Use HEREDOC for proper formatting**:
```bash
git commit -m "$(cat <<'EOF'
type: concise description

Detailed explanation of the change rationale.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

### Phase 5: Handle Pre-Commit Hooks

1. **If commit fails due to hooks**:
   - Review hook output
   - Fix any issues (linting, formatting)
   - Re-stage modified files
   - Retry commit

2. **If hooks modify files**:
   - Check authorship: `git log -1 --format='%an %ae'`
   - Check not pushed: `git status` shows "ahead"
   - If both true: amend commit
   - Otherwise: create new commit

3. **Never skip hooks** unless explicitly requested:
   - No `--no-verify`
   - No `--no-gpg-sign`

---

### Phase 6: Push Changes

1. **Check remote status**:
   ```bash
   git status
   ```

2. **Push to remote**:
   ```bash
   git push
   ```

3. **If new branch, set upstream**:
   ```bash
   git push -u origin <branch-name>
   ```

4. **Never force push to main/master** without explicit user approval

---

### Phase 7: Verification

1. **Confirm push succeeded**:
   ```bash
   git status
   git log --oneline -3
   ```

2. **Report summary**:
   ```
   ## Git Sync Complete

   | Action | Result |
   |--------|--------|
   | Files staged | X files |
   | Commit | <hash> |
   | Branch | <name> |
   | Pushed | ✅/❌ |

   ### Commit Message
   <full message>
   ```

---

## Safety Protocols

### Never Do
- ❌ Update git config
- ❌ Force push without approval
- ❌ Skip hooks without approval
- ❌ Commit `.env` or credentials
- ❌ Use `-i` interactive flags
- ❌ Amend other developers' commits
- ❌ Commit without explicit user request

### Always Do
- ✅ Check authorship before amending
- ✅ Use HEREDOC for multi-line messages
- ✅ Verify staging before commit
- ✅ Include Claude attribution
- ✅ Check for sensitive files
- ✅ Confirm push success

---

## Usage Examples

### Basic commit and push
```bash
/git-sync
```

### Commit only (no push)
```bash
/git-sync --no-push
```

### With specific message focus
```bash
/git-sync --focus "HubSpot integration improvements"
```

---

## Commit Message Examples

### Feature
```
feat: add HubSpot deal hygiene automation

Implemented bulk update system for deal completeness:
- Stage-based next steps and due dates
- Task creation for read-only date fields
- 0% to 100% deal completeness achieved

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Documentation
```
docs: update RULES.md with HubSpot API patterns

Added learnings from production implementation:
- Custom field naming conventions
- Read-only field workarounds
- Required filters to avoid data explosion

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Bug Fix
```
fix: use correct field name for monthly volume

Changed from volume_monthly_parcels to monthly_volume__c.
HubSpot custom fields use __c suffix convention.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

*Command created: November 22, 2025*
*Based on Claude Code git workflow best practices*
