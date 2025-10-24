# FirstMile Pipeline Integration Review
## Brett's Nebuchadnezzar System vs. Brock's HubSpot Pipeline

Generated: 2025-01-27

---

## CURRENT STATE: Brett's Nebuchadnezzar Pipeline

### Active Stages:
1. **[00-LEAD]** - Initial contact
2. **[01-DISCOVERY-SCHEDULED]** - Meeting booked  
3. **[02-DISCOVERY-COMPLETE]** - Post-discovery
4. **[03-RATE-CREATION]** - Building pricing
5. **[04-PROPOSAL-SENT]** - Awaiting response
6. **[05-NEGOTIATION]** - Active discussions
7. **[06-CLOSED-WON]** - Success (empty)
8. **[07-ACTIVE-SHIPPING]** - Live customers
9. **[08-CLOSED-LOST]** - Lost deals
10. **[WIN-BACK]** - Re-engagement

### Current Pipeline Status (19 deals):
- [00-LEAD]: 1 deal (Pendulums)
- [02-DISCOVERY-COMPLETE]: 1 deal (Team_Shipper)
- [03-RATE-CREATION]: 10 deals (**BOTTLENECK**)
- [04-PROPOSAL-SENT]: 2 deals (OTW_Shipping, The_Fulfillment_Lab)
- [05-NEGOTIATION]: 1 deal (JM_Group_NY)
- [07-ACTIVE-SHIPPING]: 2 deals (BoxiiShip_AF, Easy_Group_LLC)
- [08-CLOSED-LOST]: 1 deal (The_Only_Bean)
- [WIN-BACK]: 1 deal (Boxio)

---

## BROCK'S HUBSPOT PIPELINE STRUCTURE

### 1. DISCOVERY SCHEDULED
- **Description:** Discovery call scheduled with prospect
- **Movement:** Manual
- **Required Fields:**
  - Deal Type (Existing or New Business)
  - Brands (FM, SN)
  - Lead Source (Optional)
- **Automation:** Contact lead source sync + reminder if stale

### 2. DISCOVERY COMPLETE  
- **Description:** Call completed, info gathered, interest expressed
- **Movement:** Manual
- **Required Fields:**
  - Address
  - Lead Source
  - Type of Business (FM Product) - *To be Created*
    - Xparcel (Domestic)
    - UPS
    - FedEx
    - International
    - LTL/FTL
    - Other (Flats, BPM, etc.)
  - Current Carrier/s (Multi-select)
  - Average Monthly Shipments - *To be Created*
- **Automation:** 30-day reminder

### 3. RATE CREATION
- **Description:** Rates being created or submitted via Jira
- **Movement:** Manual
- **Required Fields:**
  - Jira Ticket # - *To be Created*
  - Amount
- **Automation:** 2-week reminder

### 4. PROPOSAL SENT
- **Description:** Rates emailed/presented for discussion
- **Movement:** Manual
- **Automation:** 30-day reminder

### 5. SETUP DOCS SENT
- **Description:** Verbal commit, setup docs sent
- **Movement:** Manual
- **Automation:** 2-week reminder

### 6. IMPLEMENTATION
- **Description:** Operational setup, emails to new accounts
- **Movement:** Manual
- **Automation:** 30-day reminder

### 7. CLOSED WON – STARTED SHIPPING
- **Description:** Customer shipping
- **Movement:** Manual (marked Won)
- **Required Fields:** Won Reason

### 8. CLOSED LOST
- **Description:** Deal lost
- **Movement:** Manual (marked Lost)
- **Required Fields:**
  - Lost Reason (11 options + Other)
  - Next Follow-Up Date (optional)
- **Automation:** Reminder on follow-up date

---

## INTEGRATION RECOMMENDATIONS

### Stage Mapping & Actions:

1. **KEEP Brett's [00-LEAD]** 
   - Not in Brock's system but valuable for initial tracking

2. **ALIGN [01-DISCOVERY-SCHEDULED] → DISCOVERY SCHEDULED**
   - Add Required Fields: Deal Type, Brands
   - Keep your folder automation

3. **ALIGN [02-DISCOVERY-COMPLETE] → DISCOVERY COMPLETE**
   - Add Required Fields: Type of Business, Current Carriers, Monthly Shipments
   - Implement 30-day reminder

4. **ALIGN [03-RATE-CREATION] → RATE CREATION**
   - Add Jira Ticket # field
   - **URGENT: 10 deals need 2-week reminder triggered**

5. **ALIGN [04-PROPOSAL-SENT] → PROPOSAL SENT**
   - Add 30-day reminder automation

6. **KEEP Brett's [05-NEGOTIATION]**
   - Not in Brock's system but critical for active deal management

7. **ADD NEW: SETUP DOCS SENT**
   - Insert after Negotiation
   - 2-week reminder

8. **ADD NEW: IMPLEMENTATION**
   - Final stage before close
   - 30-day reminder

9. **MERGE [06-CLOSED-WON] + [07-ACTIVE-SHIPPING] → CLOSED WON - STARTED SHIPPING**
   - Add Won Reason field

10. **ALIGN [08-CLOSED-LOST] → CLOSED LOST**
    - Add 11 Lost Reasons
    - Add Follow-Up Date field

11. **KEEP Brett's [WIN-BACK]**
    - Unique value not in Brock's system

---

## ACTION ITEMS

### Immediate (This Week):
1. Create missing HubSpot fields:
   - Type of Business (FM Product)
   - Average Monthly Shipments
   - Jira Ticket #
   - Lost Reasons dropdown

2. Add missing stages to folder structure:
   - [05.5-SETUP-DOCS-SENT]
   - [05.7-IMPLEMENTATION]

3. Update automation rules for time-based reminders

### Next Sprint:
1. Migrate existing deals to proper stages
2. Train team on new required fields
3. Update Nebuchadnezzar monitoring for new stages

---

## BENEFITS OF INTEGRATION

1. **Better Forecasting:** Setup Docs (80%) and Implementation (90%) stages
2. **Clearer Handoffs:** Implementation stage bridges Sales → Operations
3. **Data Capture:** Required fields ensure complete information
4. **Automation:** Time-based reminders prevent deal stagnation
5. **Flexibility:** Keep your unique Lead and Win-Back stages

---

## NOTES
- Your 10-deal Rate Creation bottleneck aligns with Brock's 2-week timer
- The_Fulfillment_Lab appears in [04-PROPOSAL-SENT] (not in original count)
- Total active deals: 19 (updated count)
