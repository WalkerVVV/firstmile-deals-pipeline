# FirstMile Account Analysis Template

*Internal reference for Solution Engineering, Sales, and Operations*

> **Purpose**\
> Provide a repeatable Markdown framework—ready to drop into Claude or any LLM—that synthesizes shipment data through the FirstMile lens. Copy from this file, insert account‑specific numbers, and you will automatically meet brand, tone, and structural guidelines.

---

## Key Constraints (always include verbatim)

- Refer to services as **“Xparcel Ground (3‑8 d), Xparcel Expedited (2‑5 d), Xparcel Priority (1‑3 d)”**.
- Frame carrier capacity as **“National”** (all ZIPs) and **“Select”** (metro ZIP list); **do not name UPS, USPS, FedEx, etc.**
- Emphasize FirstMile advantages: **dynamic routing, Audit Queue, Claims, Returns, single support team**.
- Spell **“eCommerce”** exactly as shown (camel‑case ‘C’).
- **Never** present Xparcel as a separate company; it is a **ship‑method under FirstMile**.

Copy the above block unchanged when prompting external LLMs.

---

## Output Sections (structure)

1. **Account Snapshot**
2. **FirstMile Network Fit**
3. **Quantified Savings / Service Improvements**
4. **Next‑Step Actions for Sales, Ops, Tech**

---

## 1 · Account Snapshot

| Metric                 | Required Detail                 | Example (Caputron)\*   |
| ---------------------- | ------------------------------- | ---------------------- |
| Annual volume          | Total parcels last 12 mo        | **365 K**              |
| Daily average          | Typical ship days × avg parcels | **≈1 K / day**         |
| Service mix            | % Ground vs expedited           | **97 % Ground**        |
| Weight profile         | % by 0‑1 lb, 1‑5 lb, >5 lb      | **73 % <1 lb**         |
| Top destination states | ≥5 states, rank‑ordered         | **FL, CA, TX, PA, NY** |
| Int’l share            | % of total                      | **<0.5 %**             |

*Replace values with account data—Caputron numbers shown only for reference.*

### Narrative bullet points

- Highlight seasonality, spikes, or notable SKU weight groupings.
- Call out any packaging standardization (e.g., 5 × 8 × 8 cartons).

---

## 2 · FirstMile Network Fit

> Map volumes to our two‑tier network and the three Xparcel services.

### 2.1 National vs Select Allocation

- **National network**: all ZIPs, leveraged for long‑tail & rural deliveries.
- **Select network**: predefined metro ZIP list (LA, DAL, ATL, ORD, EWR, etc.) used for zone‑skipping and faster hand‑offs.

| Volume Segment                        | Proposed Network                | Rationale                                     |
| ------------------------------------- | ------------------------------- | --------------------------------------------- |
| <1 lb parcels outside Select ZIPs     | **National → Xparcel Ground**   | Lowest cost per ounce; ground‑intent.         |
| <1 lb parcels to Select ZIPs          | **Select → Xparcel Ground**     | Higher density enables blended regional rate. |
| 1‑3 lb premium SKUs                   | **Select → Xparcel Expedited**  | 2‑5 d SLA; avoid air overpay.                 |
| Time‑sensitive orders / CS exceptions | **National → Xparcel Priority** | 1‑3 d guarantee, routed dynamically.          |

### 2.2 Logic Triggers

```
IF weight < 1 lb AND dest_zip IN Select_List   => Select • Xparcel Ground
ELSE IF weight < 1 lb                             => National • Xparcel Ground
ELSE IF expedited_flag = TRUE                    => Select • Xparcel Expedited
ELSE IF cs_override = TRUE                       => National • Xparcel Priority
ELSE                                             => National • Xparcel Ground
```

*(Pseudo‑code resides in our routing microservice; include for technical audiences.)*

### 2.3 FirstMile Differentiators (tie back to data)

- **Dynamic Routing:** Auto‑selects best induction point nightly based on SLA & cost.
- **Audit Queue:** Blocks mis‑rated labels before invoice hits A/P.
- **Single Support Thread:** Claims, returns, exceptions managed via one FirstMile ticket.

---

## 3 · Quantified Savings / Service Improvements

> Show both cost and service deltas—use tables for clarity.

### 3.1 Cost Model (illustrative)

| Lane                 | Current Cost (¢) | Proposed Cost (¢) | Delta        | Vol/Day |
| -------------------- | ---------------- | ----------------- | ------------ | ------- |
| <1 lb Select         | 340              | **298**           | **‑12 %**    | 450     |
| <1 lb National       | 355              | **320**           | **‑10 %**    | 280     |
| Expedited 1‑3 lb     | 920              | **845**           | **‑8 %**     | 30      |
| **Annualized Total** | —                | —                 | **‑\$185 K** | —       |

### 3.2 Service Uplift

- 96 → 98 % on‑time within Select metros (historical SLA uplift).
- Cuts claims ratio from 0.6 % → 0.3 % after Audit Queue‑driven file.

---

## 4 · Next‑Step Actions

| Owner                | Action                                                                          | Due‑by           |
| -------------------- | ------------------------------------------------------------------------------- | ---------------- |
| **Sales**            | Present two‑tab rate card (National & Select) with auto‑toggle logic explained. | 14 Aug 2025      |
| **Ops**              | Validate pickup window, pallet count, and dock access at origin DC.             | 09 Aug 2025      |
| **Tech**             | Supply ShipStation mapping guide; enable Audit Queue & Claims in sandbox.       | 16 Aug 2025      |
| **Customer Success** | Schedule KPI review 30‑days post‑launch.                                        | +30 days go‑live |

---

## Appendix

### A. Glossary

| Term                  | Definition                                                                 |
| --------------------- | -------------------------------------------------------------------------- |
| **Xparcel Ground**    | 3‑8 day, economy ground service routed through National or Select network. |
| **Xparcel Expedited** | 2‑5 day, faster ground solution for weights 1‑20 lb.                       |
| **Xparcel Priority**  | 1‑3 day premium option with money‑back guarantee.                          |
| **National Network**  | Nationwide induction partners covering 100 % U.S. ZIPs.                    |
| **Select Network**    | High‑density metro injection points for zone‑skipping.                     |
| **Audit Queue**       | FirstMile subsystem that verifies rates & dimensions pre‑invoice.          |

### B. Data Sources & Refresh Cadence

- **Shipment file**: SFTP nightly drop (UTC‑5).
- **Tracking events**: Webhook streams every 15 min.
- **Cost files**: Rated once per invoice cycle (weekly).

---

### C. Pre‑formatted SQL Query Set

> **Usage**: Replace `:account_id`, `:start_date`, and `:end_date` with the appropriate values. These queries assume a Snowflake‑style warehouse with the following core tables:
>
> *`shipments`* (id, account\_id, ship\_date, weight\_oz, service\_level, dest\_state, dest\_zip)
>
> *`tracking_events`* (shipment\_id, event\_time, status\_code)
>
> *`invoice_lines`* (shipment\_id, rated\_amount\_cents)

| Report Metric                                                              | SQL Snippet |
| -------------------------------------------------------------------------- | ----------- |
| **Annual volume**                                                          | \`\`\`sql   |
| SELECT COUNT(\*) AS annual\_parcels                                        |             |
| FROM shipments                                                             |             |
| WHERE account\_id = \:account\_id                                          |             |
| AND ship\_date BETWEEN DATEADD(year, -1, CURRENT\_DATE) AND CURRENT\_DATE; |             |

````|
| **Daily average** | ```sql
SELECT AVG(daily_count) AS parcels_per_day
FROM (
  SELECT ship_date, COUNT(*) AS daily_count
  FROM shipments
  WHERE account_id = :account_id
    AND ship_date BETWEEN :start_date AND :end_date
  GROUP BY ship_date);
``` |
| **Service mix** | ```sql
SELECT service_level,
       COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS pct
FROM shipments
WHERE account_id = :account_id
  AND ship_date BETWEEN :start_date AND :end_date
GROUP BY service_level;
``` |
| **Weight profile** | ```sql
SELECT CASE
         WHEN weight_oz < 16 THEN '<1 lb'
         WHEN weight_oz < 80 THEN '1‑5 lb'
         ELSE '>5 lb'
       END AS weight_band,
       COUNT(*) AS parcels,
       COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS pct
FROM shipments
WHERE account_id = :account_id
  AND ship_date BETWEEN :start_date AND :end_date
GROUP BY weight_band;
``` |
| **Top destination states** | ```sql
SELECT dest_state,
       COUNT(*) AS parcels
FROM shipments
WHERE account_id = :account_id
  AND ship_date BETWEEN :start_date AND :end_date
GROUP BY dest_state
ORDER BY parcels DESC
LIMIT 10;
``` |
| **On‑time % (Ground)** | ```sql
WITH last_event AS (
  SELECT s.id,
         MAX(te.event_time) AS delivery_time
  FROM shipments s
  JOIN tracking_events te ON te.shipment_id = s.id
  WHERE s.account_id = :account_id
    AND s.service_level = 'GROUND'
    AND s.ship_date BETWEEN :start_date AND :end_date
  GROUP BY s.id)
SELECT COUNT(CASE WHEN DATE_DIFF('day', s.ship_date, le.delivery_time) <= 8 THEN 1 END) * 100.0 / COUNT(*) AS on_time_pct
FROM shipments s
JOIN last_event le ON le.id = s.id;
``` |
| **Average cost / parcel** | ```sql
SELECT AVG(rated_amount_cents) / 100.0 AS usd_per_parcel
FROM invoice_lines il
JOIN shipments s ON s.id = il.shipment_id
WHERE s.account_id = :account_id
  AND s.ship_date BETWEEN :start_date AND :end_date;
``` |

---

*Internal use only. Do not distribute externally without Marketing review.*

````
