# Official Anthropic Claude Code Plugins

**Source:** https://github.com/anthropics/claude-code

Successfully installed at: `C:\Users\BrettWalker\.claude\plugins\marketplaces\anthropics-claude-code\`

---

## 🎯 Available Official Plugins (5 Total)

### 1. **feature-dev** ⭐ (Most Comprehensive)
**Category:** Development
**Author:** Siddharth Bidasaria (Anthropic)

**Command:**
- `/feature-dev [description]` - Comprehensive 7-phase feature development workflow

**Agents:**
- `code-explorer` - Codebase exploration and pattern discovery
- `code-architect` - Architecture design with multiple approaches
- `code-reviewer` - Quality review focusing on simplicity, bugs, and conventions

**Workflow Phases:**
1. **Discovery** - Understand requirements
2. **Codebase Exploration** - Launch 2-3 explorer agents in parallel
3. **Clarifying Questions** - Fill gaps, resolve ambiguities (CRITICAL - don't skip)
4. **Architecture Design** - Present multiple approaches with trade-offs
5. **Implementation** - Build with user approval
6. **Quality Review** - Launch 3 reviewer agents for simplicity/bugs/conventions
7. **Summary** - Document what was built and key decisions

**Perfect For:**
- New feature development with unclear requirements
- Complex features requiring architecture decisions
- Projects where quality and maintainability matter

**Example:**
```
/feature-dev Add SLA compliance tracking dashboard for FirstMile shipping reports
```

---

### 2. **pr-review-toolkit**
**Category:** Productivity
**Author:** Anthropic

**Command:**
- `/review-pr [pr-number]` - Comprehensive PR review

**Agents:**
- Comments review specialist
- Test coverage specialist
- Error handling specialist
- Type design specialist
- Code quality specialist
- Code simplification specialist

**Perfect For:**
- Code review automation
- Ensuring PR quality before merge
- Team collaboration workflows

**Example:**
```
/review-pr 123
```

---

### 3. **commit-commands**
**Category:** Productivity
**Author:** Anthropic

**Commands:**
- `/commit` - Create git commit with best practices
- `/commit-push-pr` - Commit, push, and create PR in one command
- `/clean_gone` - Clean up merged/deleted branches

**Perfect For:**
- Streamlined git workflows
- Consistent commit messages
- Branch cleanup

**Example:**
```
/commit
/commit-push-pr Add FirstMile pipeline automation
```

---

### 4. **agent-sdk-dev**
**Category:** Development
**Author:** Anthropic

**Command:**
- `/new-sdk-app [description]` - Scaffold new Agent SDK application

**Perfect For:**
- Building new Agent SDK apps
- Learning Agent SDK patterns
- Quick SDK project setup

---

### 5. **security-guidance**
**Category:** Security
**Author:** David Dworken (Anthropic)

**Type:** Hook (no commands)
**Function:** Warns about security issues when editing files

**Detects:**
- Command injection vulnerabilities
- XSS (Cross-Site Scripting) risks
- Unsafe code patterns
- SQL injection
- Path traversal

**Perfect For:**
- Proactive security warnings
- Preventing common vulnerabilities
- Security-conscious development

---

## 🚀 How to Use Official Plugins

### Install Via Claude Code

The marketplace should already be available. Try:

```bash
/plugin install feature-dev
/plugin install pr-review-toolkit
/plugin install commit-commands
```

### Manual Installation (Alternative)

If plugin system doesn't recognize them, copy commands manually:

```bash
# Copy feature-dev command
cp "C:/Users/BrettWalker/.claude/plugins/marketplaces/anthropics-claude-code/plugins/feature-dev/commands/feature-dev.md" \
   "C:/Users/BrettWalker/FirstMile_Deals/.claude/commands/"
```

---

## 📖 Command File Format (Official Standard)

All official commands use this structure:

```markdown
---
description: Brief description of what this command does
argument-hint: Optional hint for arguments
---

# Command Title

Command instructions and workflow in structured markdown...

## Phase 1: Title
**Goal**: What this phase accomplishes

**Actions**:
1. Step one
2. Step two
```

**Key Elements:**
- **YAML Frontmatter** - Metadata for Claude Code to parse
- **Structured Phases** - Clear workflow steps
- **Goal Statements** - Purpose of each phase
- **Actionable Steps** - Numbered, specific instructions
- **Agent Integration** - Launch specialized agents for complex tasks

---

## 💡 Best Practices from Official Plugins

### 1. Multi-Agent Patterns
Launch specialized agents in parallel:
```markdown
Launch 2-3 code-explorer agents with different focuses:
- Agent 1: Similar features
- Agent 2: Architecture understanding
- Agent 3: UI patterns and testing
```

### 2. User Confirmation Points
Critical checkpoints before major actions:
```markdown
**DO NOT START WITHOUT USER APPROVAL**
```

### 3. TodoWrite Integration
Track progress throughout workflow:
```markdown
1. Create todo list with all phases
2. Update todos as you progress
3. Mark all todos complete at end
```

### 4. Clarifying Questions Phase
Prevent assumptions and ambiguities:
```markdown
**CRITICAL**: This is one of the most important phases. DO NOT SKIP.

Identify underspecified aspects:
- Edge cases
- Error handling
- Integration points
- Design preferences
```

### 5. Multiple Approach Presentation
Present options with trade-offs:
```markdown
Present to user:
- Approach A: Minimal changes
- Approach B: Clean architecture
- Approach C: Pragmatic balance
- **Your recommendation with reasoning**
```

---

## 🎯 Recommended Workflow for FirstMile Work

### For New Features
```
/feature-dev [description]
```
Example: `/feature-dev Add automated rate comparison calculator for zone-based pricing`

### For Code Review
```
/review-pr [pr-number]
```

### For Git Workflow
```
/commit-push-pr [description]
```

### For SDK Projects
```
/new-sdk-app [description]
```

---

## 🔧 Integration with Existing Plugins

You now have 3 marketplaces:

1. **Anthropic Official** (5 plugins) - Feature dev, PR review, commits
2. **claude-code-workflows** (42 plugins) - Data engineering, Python, backend
3. **claude-code-templates** (1 plugin) - Next.js/Vercel tools

**Combined Power:**
- Use `/feature-dev` for complex new features
- Use `/data-pipeline` for data processing workflows
- Use `/python-scaffold` for project structure
- Use `/commit-push-pr` for streamlined git workflow
- Use `/review-pr` before merging

---

## 📂 File Locations

```
C:\Users\BrettWalker\.claude\plugins\marketplaces\
├── anthropics-claude-code/          ← Official Anthropic plugins
│   └── plugins/
│       ├── feature-dev/             ← Comprehensive feature workflow
│       ├── pr-review-toolkit/       ← PR review automation
│       ├── commit-commands/         ← Git workflow commands
│       ├── agent-sdk-dev/           ← SDK scaffolding
│       └── security-guidance/       ← Security warnings
├── claude-code-workflows/           ← wshobson/agents (42 plugins)
└── claude-code-templates/           ← davila7 (Next.js tools)
```

---

## 🎓 Learning from Official Plugins

The **feature-dev** plugin is the gold standard for complex workflows. Study it for:
- Multi-phase structure with clear goals
- Parallel agent launches for efficiency
- User confirmation at key decision points
- TodoWrite integration throughout
- Comprehensive quality review process

Apply these patterns when creating custom commands for FirstMile work.

---

**Last Updated:** 2025-10-13
**Official Plugins:** 5
**Total Marketplaces:** 3
**Total Available Plugins:** 48+
