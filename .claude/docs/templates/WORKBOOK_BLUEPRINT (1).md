# WORKBOOK_BLUEPRINT.md

## TL;DR
This workbook ingests PLD (Package-Level Detail) files, cleans and stages shipment data, and produces discovery-ready analytics: carrier/service mix, billed-weight frequency, cost outliers, and geographic distribution. It is structured for quick import, pivot-driven analysis, and visual inspection. The design is functional but can be hardened with layered architecture, governance, and automation.

---

## A. Executive Summary
**Purpose:** Provide a repeatable, discovery-focused analysis of a prospect’s shipping profile (without FirstMile pricing).  
**Audience:** Sales engineers, solutions consultants, and analysts preparing for prospect calls.  
**Top 5 Findings:**
1. Workbook is lightweight (.xlsx), structured for manual paste → pivot workflow.
2. Core logic resides in PivotTables; minimal formulas outside pivot layers.
3. No VBA or macros; relies on manual refresh.
4. Input normalization and weight-band frequency are handled via staging sheet and pivot config.
5. Architecture is simple but fragile — lacks centralized parameters, validation, and error handling.

---

## B. Workbook Map

| Sheet Name              | Role       | Key Inputs/Outputs                  | Dependencies              |
|--------------------------|------------|-------------------------------------|---------------------------|
| **Raw_Data**            | Input      | PLD data (Ship Date, Carrier, Cost, Bill Weight) | Source data pasted manually |
| **Weight_Frequency_Pivot** | Output    | PivotTable of Bill Weight × COUNT × % | Raw_Data                  |

**Calc/Refresh Order:**  
- Raw_Data → Weight_Frequency_Pivot (PivotTable refresh)

---

## C. Logic Catalog

### Formula/Pattern Usage
- Minimal formulas (staging only).  
- Normalization: weight values coerced into numeric, blanks flagged.  
- No volatile or recursive functions detected.

### PivotTables
- **Weight Frequency Pivot**  
  - Rows: Bill Weight  
  - Values: Count, % of column total  
  - Filters: None  
  - Outputs: Frequency table with Grand Total  

No charts, slicers, or advanced Excel models present.

---

## D. Data Contracts

### Input Schema (Raw_Data)
| Field              | Type     | Constraints |
|--------------------|----------|-------------|
| Ship Date          | Date     | Required, non-blank |
| Carrier – Service  | Text     | Split into two fields if needed |
| Bill Weight        | Decimal  | May include blanks; normalize |
| Cost               | Currency | Positive numeric |

Parameters: None centralized (recommend adding).

---

## E. Rebuild Instructions (Neural Pathway)

1. **Sheet scaffolding:** Create `Raw_Data` (input) and `Weight_Frequency_Pivot` (output).  
2. **Input contract:** Define columns: Ship Date, Carrier – Service, Bill Weight, Cost.  
3. **Validation:** Add simple checks for blanks, numeric weights.  
4. **Pivot setup:**  
   - Rows: Bill Weight (ascending, blanks visible).  
   - Values: Count of Bill Weight, % of column total.  
   - Grand Total enabled.  
5. **Output formatting:** COUNT = whole numbers, % = 2 decimals.  
6. **Acceptance test:** Table should sum to 100% in % column.  

---

## F. Performance & Risk Register

- **Risks:** Manual refresh → error prone; no central parameters; no error handling.  
- **Performance:** Scales to ~50k rows fine; beyond that, pivot responsiveness degrades.  
- **Privacy:** PLD may contain PII; currently no protection in workbook.  

Mitigations: Introduce Power Query ETL, parameterized inputs, data validation, and optional sheet protection.

---

## G. Runbook

- **Refresh order:** Paste new PLD data → Refresh PivotTable.  
- **Manual vs Automatic:** Manual paste/refresh. Could automate with Power Query.  
- **Error handling:** Currently none. Add simple QA checks (row count, blank %).  
- **Schedule:** On-demand before discovery calls.  

---

## H. Governance

- **Naming conventions:** Prefix by role (`In_`, `Out_`, `Stage_`).  
- **Versioning:** Split template (input logic) vs working file (prospect data).  
- **Backup:** Archive prospect PLD + workbook snapshot with timestamp.  
- **Documentation:** Add README sheet with usage notes.  

---

## I. Backlog

- **Now:** Add Power Query import to eliminate paste errors.  
- **Next:** Introduce Data Quality Report sheet.  
- **Later:** Layer semantic model in Power BI for scalability; automate refresh pipeline.  

---

## Acceptance Tests

- **Data parity:** Row counts in pivot = row counts in Raw_Data.  
- **Measure parity:** % column sums to 100.00%.  
- **Visual parity:** Bill Weight categories align with raw unique values.  
- **Performance:** Pivot refresh < 5s for 10k rows.  

---

## Parallel Sub-Agents (Prompts)

1. **Inventory Agent**  
   “List all sheets, pivots, and named ranges. Capture dependencies and purpose.”  

2. **ETL Agent**  
   “Define Power Query connection for Raw_Data CSV import. Document transform steps.”  

3. **Data Model Agent**  
   “Propose normalized data model (fact shipments, dim carriers, dim dates).”  

4. **Calculation Patterns Agent**  
   “Refactor weight frequency into reusable block; parameterize weight bands.”  

5. **QA Agent**  
   “Run acceptance tests: parity checks on counts and percentages.”  

---

## Glossary

- **PLD:** Package-Level Detail file (shipment-level record of date, carrier, weight, cost).  
- **Bill Weight:** The weight on which cost was calculated (may differ from actual).  
- **Pivot:** Excel PivotTable object used for aggregation.  

---

## Next 5 Actions

1. Replace manual paste with Power Query import.  
2. Add Data Quality Report sheet.  
3. Introduce validation for Ship Date and Weight.  
4. Protect sheets containing pivots.  
5. Document process in a README sheet inside workbook.  

