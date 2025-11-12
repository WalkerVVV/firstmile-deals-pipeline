# Slash Commands Guide - FirstMile Deals

## 🎯 Available Slash Commands

You now have access to 5 custom slash commands from the wshobson/agents marketplace:

### 1. `/python-scaffold`
**Purpose**: Create production-ready Python project structures
**Use Cases**:
- Set up new analysis scripts with proper structure
- Create FastAPI microservices
- Build CLI tools for data processing
- Generate library packages

**Example**:
```
/python-scaffold Create a FastAPI project for PLD analysis API
```

### 2. `/data-pipeline`
**Purpose**: Build ETL data pipelines
**Use Cases**:
- Design data extraction workflows
- Transform shipping data (CSV → processed format)
- Load data into databases or Excel reports
- Automate daily data processing

**Example**:
```
/data-pipeline Build an ETL pipeline to process customer shipment CSVs and generate Excel reports
```

### 3. `/data-driven-feature`
**Purpose**: Create data-driven application features
**Use Cases**:
- Build analytics dashboards
- Create reporting endpoints
- Implement data visualization features
- Add KPI tracking

**Example**:
```
/data-driven-feature Create a customer shipping performance dashboard
```

### 4. `/doc-generate`
**Purpose**: Auto-generate documentation
**Use Cases**:
- Document Python analysis scripts
- Create API documentation
- Generate README files
- Write user guides

**Example**:
```
/doc-generate Document the PLD analysis workflow for team onboarding
```

### 5. `/code-explain`
**Purpose**: Explain code functionality
**Use Cases**:
- Understand complex analysis scripts
- Review inherited code
- Create code walkthroughs
- Training documentation

**Example**:
```
/code-explain Explain how the billable weight calculation works in apply_customer_rates.py
```

## 📦 Full Marketplace Location

All 42 plugins are available at:
```
C:\Users\BrettWalker\.claude\plugins\marketplaces\wshobson-agents\
```

## 🔧 Adding More Commands

To add more commands from the marketplace:

1. Browse available plugins:
   ```bash
   ls C:/Users/BrettWalker/.claude/plugins/marketplaces/wshobson-agents/plugins/
   ```

2. Check a plugin's commands:
   ```bash
   ls C:/Users/BrettWalker/.claude/plugins/marketplaces/wshobson-agents/plugins/[plugin-name]/commands/
   ```

3. Copy command to your project:
   ```bash
   cp "C:/Users/BrettWalker/.claude/plugins/marketplaces/wshobson-agents/plugins/[plugin-name]/commands/[command].md" "C:/Users/BrettWalker/FirstMile_Deals/.claude/commands/"
   ```

## 🌟 Recommended Plugins for FirstMile Work

### Currently Installed:
- ✅ python-development
- ✅ data-engineering
- ✅ code-documentation

### Worth Adding:
- **business-analytics** - KPI tracking, reporting, business metrics
- **git-pr-workflows** - PR enhancement, team collaboration
- **unit-testing** - Test generation and automation
- **debugging-toolkit** - Interactive debugging workflows
- **performance-testing-review** - Code performance analysis

## 💡 Usage Tips

1. **Start with `/` in chat**: Type `/` to see all available commands
2. **Provide context**: Include file paths or requirements after the command
3. **Iterate**: Commands can be run multiple times to refine output
4. **Combine**: Use multiple commands in sequence (e.g., `/python-scaffold` then `/doc-generate`)

## 📚 Command Arguments

Most commands accept `$ARGUMENTS` which means you can provide:
- **Requirements**: Detailed specifications of what you need
- **File paths**: Reference existing files with `@filename`
- **Context**: Explain your use case
- **Constraints**: Specify limitations or preferences

Example:
```
/data-pipeline @customer_data.csv
Process this CSV into zone analysis and create Excel output with SLA compliance metrics
Use FirstMile branding (#366092) and follow the performance report template
```

## 🔄 Reload Commands

After adding new commands, Claude Code should auto-detect them. If not:
1. Restart Claude Code
2. Or navigate away and back to this project

---

**Last Updated**: 2025-10-13
**Marketplace Version**: 1.2.0
**Plugins Installed**: 3 of 42 available
