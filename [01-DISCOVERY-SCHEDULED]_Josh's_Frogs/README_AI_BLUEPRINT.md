# AI Agent Blueprint - Quick Start Guide

## What This Is

A comprehensive prompt framework that enables an AI agent to build a complete **Shipping Analytics & Rate Comparison System** from scratch in a single execution.

## Key Document: AI_AGENT_BLUEPRINT.md

**Size:** ~30KB of structured guidance
**Purpose:** Blueprint for recreating this entire Josh's Frogs analysis system
**Approach:** Infrastructure + Methodology + Neural Pathways + Sub-Agent Architecture

## What's Inside

### I. System Architecture Overview
- **Input Layer:** PLD CSV data, rate cards, business rules
- **Processing Layer:** 5 specialized engines (ingestion, calculations, analysis, reporting)
- **Output Layer:** Multi-tab Excel workbooks, Markdown docs, email drafts
- **Tech Stack:** Python, pandas, numpy, openpyxl

### II. Approach Methodology
4 phases with clear objectives:
1. **Data Understanding** - Comprehend customer shipping profile
2. **Rate Structure Modeling** - Build dual cost engines (current vs FirstMile)
3. **Savings Analysis** - Calculate opportunities across all dimensions
4. **Report Generation** - Create executive-ready deliverables

### III. Neural Pathway (The "One-Shot" Mental Model)
5-step cognitive flow:
- **Phase A: COMPREHENSION** - Understand the domain
- **Phase B: MODELING** - Build the cost engine
- **Phase C: ANALYSIS** - Find the opportunities
- **Phase D: SYNTHESIS** - Tell the story
- **Phase E: VALIDATION** - Check the work

### IV. Sub-Agent Architecture
6 specialized agents designed for parallel execution:

**Sub-Agent 1: Data Ingestion Specialist**
- Load PLD CSV, validate, standardize
- Output: Clean DataFrame with metadata

**Sub-Agent 2: Carrier Cost Calculator**
- Calculate current carrier costs using zone/weight formulas
- Output: DataFrame with 'current_cost' column

**Sub-Agent 3: FirstMile Rate Calculator**
- Calculate Xparcel rates from rate cards
- Output: DataFrame with 'xparcel_cost' column

**Sub-Agent 4: Savings Analyzer**
- Calculate savings across all dimensions
- Output: Aggregated savings summary

**Sub-Agent 5: Excel Report Generator**
- Create multi-tab workbook with FirstMile branding
- Output: Professional .xlsx file

**Sub-Agent 6: Markdown Summarizer**
- Generate executive summaries and technical docs
- Output: 3 Markdown/text files

### V. Orchestration Workflow
```
Sequential → Parallel → Sequential → Parallel → Final
   (Load)   (Calculate)  (Analyze)  (Report)  (Validate)
```
**Time Savings:** ~40% through parallel optimization

## How to Use This Blueprint

### For AI Agents
1. Read entire AI_AGENT_BLUEPRINT.md
2. Follow the neural pathway (Phase A → E)
3. Spawn sub-agents as defined
4. Execute orchestration workflow
5. Validate outputs against checklist

### For Human Developers
1. Use as system design specification
2. Implement sub-agents as microservices
3. Apply business rules and validation checks
4. Follow styling standards for outputs
5. Handle edge cases as documented

### For Project Managers
1. Understand scope and deliverables
2. Estimate timelines (~2 min execution for 150K shipments)
3. Review success metrics and quality standards
4. Plan for edge cases and limitations

## Key Business Rules Included

### Service Mapping
- Current carrier services → FirstMile Xparcel equivalents
- Dry goods (ground) separate from live animals (express)
- Zone-based pricing with weight tiers

### Rate Calculations
- **Current Carrier:** base × zone_mult × weight_mult × 1.12 (fuel)
- **FirstMile Xparcel:** zone_base + weight_tier_addon
- Realistic savings: 20-60% ground, 70-90% express

### Output Requirements
- FirstMile blue (#1E4C8B) branding
- Currency and percentage formatting
- Auto-sized columns, centered data
- 6-9 tabs per workbook

## Success Metrics

**Quantitative:**
- Execution time: <2 minutes
- Data accuracy: 100% match
- File quality: Opens without errors

**Qualitative:**
- Executive-ready (no edits needed)
- Brand-consistent (FirstMile blue throughout)
- Complete (all questions answered)

## Files in This Project

**Generated from Blueprint:**
- Joshs_Frogs_Complete_Audit_v3.1.xlsx (77 KB, 9 tabs)
- Joshs_Frogs_Carrier_Rate_Comparison_by_Weight.xlsx (16 KB, 6 zones)
- DRY_GOODS_SUMMARY.md (analysis of 139K shipments)
- RATE_COMPARISON_SUMMARY.md (10 weight tiers)
- Multiple email drafts and technical docs

**Blueprint Documents:**
- **AI_AGENT_BLUEPRINT.md** ← Main framework (this is what you share with AI)
- README_AI_BLUEPRINT.md ← This quick start guide

## Example Use Cases

### Use Case 1: New Customer Analysis
**Input:** PLD CSV from new ecommerce shipper
**Process:** Run full blueprint (all 6 sub-agents)
**Output:** Executive workbook, email draft, summary docs
**Time:** ~2 minutes

### Use Case 2: Rate Update
**Input:** New FirstMile rate card (quarterly update)
**Process:** Run Sub-Agents 3, 4, 5, 6 only (skip data ingestion)
**Output:** Updated workbooks with new savings calculations
**Time:** ~1 minute

### Use Case 3: Competitive Benchmark
**Input:** Multiple PLDs from different time periods
**Process:** Batch execution with trend analysis
**Output:** Comparative workbooks showing savings over time
**Time:** ~5 minutes (3 periods)

## Edge Cases Handled

1. **Missing zone information** → Assign default zone 4, flag estimate
2. **Heavy packages (>20 lbs)** → Custom formula, note if FirstMile more expensive
3. **Express services** → Separate dry goods from live animals
4. **International shipments** → Filter out, analyze domestic only
5. **Dimensional weight** → Calculate (L×W×H)/166, use greater value

## Validation Checklist

The blueprint includes 3-stage validation:
- **Pre-Execution** (5 checks) - Input validation
- **Mid-Execution** (5 checks) - Data processing validation
- **Post-Execution** (6 checks) - Output quality validation

Total: 16 automated validation checks

## Future Enhancements (Not in Current Build)

1. Real-time rate API integration
2. Automated zone calculator from ZIP pairs
3. ML-based seasonal forecasting
4. Interactive web dashboards
5. A/B testing framework for carrier strategies
6. Custom rate negotiation simulator

## Contact & Support

**Project:** FirstMile Deals - Josh's Frogs Analysis
**Stage:** [01-DISCOVERY-SCHEDULED]
**Sales Rep:** Brett Walker
**Generated:** September 29, 2025

## Quick Command Reference

```bash
# Navigate to project
cd "c:\Users\BrettWalker\FirstMile_Deals\[01-DISCOVERY-SCHEDULED]_Josh's_Frogs"

# View blueprint
cat AI_AGENT_BLUEPRINT.md

# Run existing analysis (example)
python invoice_audit_builder_v31.py

# Generate rate comparison
python carrier_rate_comparison_by_weight.py
```

---

**For AI Agents:** Start with Section III (Neural Pathway) to understand the cognitive flow, then proceed through Section IV (Sub-Agents) for implementation details.

**For Humans:** Start with Section II (Methodology) to understand the approach, then review Section VII (Edge Cases) and Section VIII (Validation) for production readiness.