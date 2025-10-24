# FirstMile Account Analysis: Caputron Medical Products

**Prepared for:** Robin Azzam, CEO  
**Analysis Date:** December 2, 2024  
**Data Period:** Current operational profile  

---

## 1. Account Snapshot

| Metric                 | Detail                          |
| ---------------------- | ------------------------------- |
| Annual volume          | **365,000 parcels**             |
| Daily average          | **1,000 parcels/day**           |
| Service mix            | **97% Ground, 3% Expedited**    |
| Weight profile         | **73% under 1 lb**              |
| Top destination states | **FL, CA, TX, PA, NY**          |
| Int'l share            | **<0.5%**                       |

### Volume & Profile Insights
- Consistent daily volume with lightweight medical device shipments
- Peak weight concentration at 15 oz (160 daily shipments)
- Standardized packaging dimensions: primarily 5" × 8" × 8" cartons
- 95% of shipments under 5 lbs, optimized for small parcel networks

---

## 2. FirstMile Network Fit

### 2.1 National vs Select Network Allocation

| Volume Segment                    | Current Service   | Proposed Network               | Daily Volume |
| --------------------------------- | ----------------- | ------------------------------ | ------------ |
| <1 lb to Select metros            | Ground (Mixed)    | **Select • Xparcel Ground**    | ~400         |
| <1 lb to National coverage        | Ground (Mixed)    | **National • Xparcel Ground**  | ~330         |
| 1-5 lb standard shipments         | Ground            | **National • Xparcel Ground**  | 220          |
| Time-sensitive/Priority           | Priority Mail     | **National • Xparcel Priority** | 30           |
| Heavy shipments (>5 lb)           | Ground            | **National • Xparcel Ground**  | 20           |

### 2.2 Routing Logic Implementation

```
IF weight < 16 oz AND dest_zip IN [Select_Metro_ZIPs]  => Select • Xparcel Ground
ELSE IF weight < 16 oz                                  => National • Xparcel Ground  
ELSE IF service_level = "PRIORITY"                      => National • Xparcel Priority
ELSE IF weight > 80 oz                                  => National • Xparcel Ground
ELSE                                                    => National • Xparcel Ground
```

### 2.3 FirstMile Differentiators Applied to Caputron

- **Dynamic Routing**: Leverage Select network for 40% of sub-1 lb volume to high-density metros (FL, CA, TX concentration)
- **Audit Queue**: Critical for 73% lightweight packages to prevent dimensional weight billing errors
- **Single Support Thread**: Consolidate current dual-carrier (UPS/USPS) exception handling into one system
- **eCommerce Optimization**: Purpose-built for Caputron's lightweight medical device profile

---

## 3. Quantified Savings & Service Improvements

### 3.1 Projected Cost Model

| Segment                    | Current Cost/Unit | FirstMile Cost/Unit | Savings  | Annual Impact    |
| -------------------------- | ----------------- | ------------------- | -------- | ---------------- |
| <1 lb Select (146K/yr)     | $3.40            | **$2.98**           | **-12%** | **-$61,320**     |
| <1 lb National (120K/yr)   | $3.55            | **$3.20**           | **-10%** | **-$42,000**     |
| 1-5 lb Ground (80K/yr)     | $5.25            | **$4.85**           | **-8%**  | **-$32,000**     |
| Priority Service (11K/yr)  | $9.20            | **$8.45**           | **-8%**  | **-$8,250**      |
| **Total Annual Savings**   | —                | —                   | —        | **-$143,570**    |

### 3.2 Service Level Enhancements

| Metric                      | Current Performance | With FirstMile      | Improvement |
| --------------------------- | ------------------- | ------------------- | ----------- |
| On-time delivery            | 94%                | **97%**             | +3%         |
| Claims processing time      | 15 days            | **7 days**          | -53%        |
| Invoice accuracy            | 92%                | **99%** (Audit Queue) | +7%        |
| Exception resolution        | 48 hours           | **24 hours**        | -50%        |

---

## 4. Next-Step Actions

| Owner                | Action                                                                    | Due Date     |
| -------------------- | ------------------------------------------------------------------------- | ------------ |
| **Sales**            | Present dual-tab rate card with Select/National routing logic            | Dec 9, 2024  |
| **Ops**              | Validate Ronkonkoma, NY facility pickup schedule & pallet requirements   | Dec 6, 2024  |
| **Tech**             | Configure WMS integration for Xparcel service mapping & Audit Queue      | Dec 11, 2024 |
| **Customer Success** | Schedule 30-day post-launch SLA review with KPI dashboard access         | Jan 15, 2025 |

---

## Implementation Timeline

### Phase 1: Foundation (Week 1-2)
- WMS integration and service level mapping
- Rate card finalization with Select/National logic
- Audit Queue configuration for dimensional validation

### Phase 2: Pilot Launch (Week 3-4)  
- 10% volume migration to validate routing
- Monitor Select network performance for top metros
- Calibrate Audit Queue for Caputron's standard dimensions

### Phase 3: Full Migration (Week 5-6)
- Complete transition of ground services
- Activate Claims portal and Returns workflows
- Enable real-time tracking integration

---

## Strategic Advantages for Caputron

1. **Lightweight Optimization**: FirstMile's Select network specifically designed for sub-1 lb eCommerce parcels matching 73% of volume
2. **Carrier Consolidation**: Replace UPS/USPS dual-carrier complexity with single platform maintaining coverage
3. **Medical Device Focus**: Audit Queue prevents common dimensional weight overcharges on small, high-value items
4. **Geographic Alignment**: Select network metros match Caputron's top 5 destination states perfectly

---

*This analysis demonstrates FirstMile's tailored approach to Caputron's unique shipping profile, leveraging our dual-network architecture and Xparcel services to deliver measurable cost savings and service improvements.*