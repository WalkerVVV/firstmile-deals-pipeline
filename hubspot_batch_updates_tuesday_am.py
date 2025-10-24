#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HubSpot Batch Updates - Tuesday Morning 9AM Sync
Based on Superhuman email context from October 7, 2025

Updates all Priority 1 and 2 deals with latest email context, action items, and notes.
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hubspot_realtime_updates import (
    add_deal_note,
    create_task,
    update_deal_property,
    search_deal
)

def update_stackd_logistics():
    """Update Stackd Logistics with rates approved status"""
    deal_name = "Stackd Logistics"

    print(f"\n{'='*80}")
    print(f"UPDATING: {deal_name}")
    print('='*80)

    # Add note about rates approved
    note = """**RATES APPROVED - JIRA RATE-1897 COMPLETE (Oct 6)**

From: Taylar Schmitt
Status: DONE

Rate Details:
- Focusing on Ground volume
- Aggressive with Select network
- Rates approved and in folder
- Customer workbook ready: Stackd_Logistics_FirstMile_Xparcel_Savings_Analysis_20251006_1813.xlsx
- 10.2% savings verified ($4,522/month)
- Volume: 19,200 packages/month
- Profile: 89.9% under 1 lb

Next Action:
- Send meeting request to Landon Richards
- Task reminder active (Oct 6)
- Meeting to review Xparcel Domestic rates
"""

    add_deal_note(deal_name, note)

    # Create task for meeting request
    create_task(
        deal_name=deal_name,
        task_subject="SEND Meeting Request to Landon - Rate Review",
        task_body="""Send meeting request to Landon Richards to review Xparcel rates.

Email template: EMAIL_TO_LANDON_RATE_UPDATE.md
Workbook: Stackd_Logistics_FirstMile_Xparcel_Savings_Analysis_20251006_1813.xlsx

Meeting agenda:
1. Rate card walkthrough
2. Savings analysis ($4,522/month, 10.2%)
3. Service level comparison
4. Peak season strategy
5. Implementation timeline""",
        priority="HIGH",
        due_days=0  # Today
    )

    # Update last contact date
    update_deal_property(deal_name, "notes_last_updated", "2025-10-07")

    print(f"✅ {deal_name} updated successfully\n")

def update_boxiiship():
    """Update BoxiiShip with Stephen Lineberry email context"""
    deal_name = "BoxiiShip System Beauty"

    print(f"\n{'='*80}")
    print(f"UPDATING: {deal_name}")
    print('='*80)

    # Add note about transit report and issue resolutions
    note = """**TRANSIT REPORT & ISSUE RESOLUTION UPDATE (Oct 3-6)**

From: Stephen Lineberry (Senior Partnership Manager)

RESOLVED ISSUES:
✅ Manual Encoding/Sorting: Fully resolved, parcels cleared within 24 hours
✅ Tracking Visibility: Labels never physically received/scanned (not cancelled)
✅ Transit Report: July-Sept 2025 delivered

TRANSIT REPORT FINDINGS (July-Sept 2025):
- Average days in transit: 2.96 days
- 99.9% delivered by Day 8
- 97% delivered by Day 5
- Ground slowest, DHL Expedited <1lb most used
- Strong SLEs overall except USPS GA >1lb in July/Aug
- Label-to-scan: 1.03 days (higher than average)
- Max August delays (12.23 days): TSA Known Shipper status unknown after DFW move

PENDING ACTIONS (48-hour deadline from Oct 2):
1. Coordinate ACI DFW pickup logistics for peak season
2. Provide September data breakdown by customer
3. Weight data fix timeline (Melissa follow-up)
4. Daily reconciliation reports request
5. Confirm BOL receipt (Robert Kruse, Oct 3)

Contact: Reid Malloch
Next Step: Send summary email with transit report findings
"""

    add_deal_note(deal_name, note)

    # Create tasks for pending actions
    create_task(
        deal_name=deal_name,
        task_subject="URGENT: Complete BoxiiShip Action Items (48hr deadline passed)",
        task_body="""Complete pending action items from Oct 2 email:

1. Coordinate ACI DFW pickup logistics for peak season routing
2. Provide September data breakdown by customer
3. Follow up with Melissa on weight data fix timeline
4. Request daily reconciliation reports
5. Confirm BOL receipt to Robert Kruse (Oct 3 email)

Context: 48-hour deadline from Oct 2 has passed - escalated priority""",
        priority="HIGH",
        due_days=0  # Today
    )

    create_task(
        deal_name=deal_name,
        task_subject="Send Transit Report Summary Email to Reid Malloch",
        task_body="""Draft and send email to Reid with:

1. Manual encoding issue RESOLVED
2. Tracking visibility clarified
3. Transit report findings (2.96 avg days, 99.9% by Day 8)
4. Max August delays explained (TSA Known Shipper after DFW move)
5. Next steps for refund/reship on missing scans

Attachment: Transit report from Stephen Lineberry (Oct 6)""",
        priority="HIGH",
        due_days=0  # Today
    )

    # Log email from Stephen Lineberry
    update_deal_property(deal_name, "notes_last_updated", "2025-10-07")

    print(f"✅ {deal_name} updated successfully\n")

def update_team_shipper():
    """Update Team Shipper with status verification note"""
    deal_name = "Team Shipper"

    print(f"\n{'='*80}")
    print(f"UPDATING: {deal_name}")
    print('='*80)

    # Add note about email search results
    note = """**STATUS VERIFICATION NEEDED (Oct 7)**

Email Search Results:
- NO recent emails found mentioning "Team Shipper" or "Mohammad"
- HubSpot shows: [05-SETUP-DOCS-SENT] (last modified Oct 3)
- EOD Log indicates: 34 days in stage, urgency 95/100

Available Materials:
- Email: [04-PROPOSAL-SENT]_Team_Shipper/EMAIL_TO_MOHAMMAD.md
- Workbooks: Team Shipper_FirstMile_Xparcel_08222025.xlsx
- Workbooks: Team Shipper_Xparcel_Full File_08222025.xlsm
- JIRA: RATE-1897

Next Action:
- Verify if proposal was actually sent
- If not sent, send immediately (34 days overdue)
- If sent, follow up on status

Deal Value: $500K
Contact: Mohammad (new 3PL with operational details provided)
"""

    add_deal_note(deal_name, note)

    # Create task for verification
    create_task(
        deal_name=deal_name,
        task_subject="VERIFY Team Shipper Proposal Status - Send if Needed",
        task_body="""Verify proposal status for Team Shipper:

1. Check if proposal was sent (no emails found in Superhuman search)
2. If NOT sent: Send immediately with attachments
   - EMAIL_TO_MOHAMMAD.md
   - Team Shipper_FirstMile_Xparcel_08222025.xlsx
   - Team Shipper_Xparcel_Full File_08222025.xlsm
3. If sent: Follow up (34 days in stage, urgency 95/100)

Deal value: $500K
Contact: Mohammad (new 3PL)""",
        priority="HIGH",
        due_days=0  # Today
    )

    print(f"✅ {deal_name} updated successfully\n")

def update_tactical_logistic():
    """Update Tactical Logistic with Skupreme tech agreement blocker"""
    deal_name = "Tactical Logistic"

    print(f"\n{'='*80}")
    print(f"UPDATING: {deal_name}")
    print('='*80)

    # Add note about blocker
    note = """**CRITICAL BLOCKER: SKUPREME TECH AGREEMENT NOT SIGNED (Oct 7)**

Status: CANNOT CLOSE AS WON until agreement signed

From: Ely Liberov (Skupreme)
Quote: "No new business will start until anti-raiding provisions in place"
Quote: "Where is our JM tech fee?"

Tech Agreement Details:
- Agreement between Skupreme-FirstMile for referral/commission fees
- Sent via Adobe Sign to Peter Li (Skupreme) and Scott Hale (FirstMile)
- Multiple follow-ups sent (June-July)
- Javier confirmed signing for JM Group, but Skupreme agreement still pending

Skupreme Position:
- Skupreme is billing party for all referred accounts (JM Group, Tactical, Coldest)
- Expects referral/tech fees for all accounts they bring
- Requires anti-poaching provisions before proceeding

Tactical Status (from Aug 25):
- Tactical experiencing internal delays
- Joseph Ausch to provide start date when ready
- All communications ON HOLD until Tactical reaches out
- Javier Viejo (Skupreme) managing relationship

Next Actions:
1. Follow up with Peter Li, Javier, Ely on tech agreement signature
2. Finalize anti-poaching provisions
3. Once signed, wait for Tactical internal delays to resolve
4. Then close as WON

Deal Value: $450K
Stage: [06-IMPLEMENTATION] - ON HOLD
"""

    add_deal_note(deal_name, note)

    # Create task for agreement follow-up
    create_task(
        deal_name=deal_name,
        task_subject="CRITICAL: Follow Up on Skupreme Tech Agreement Signature",
        task_body="""Follow up with Skupreme team on tech agreement signature:

Recipients:
- Peter Li (Skupreme) - primary signer
- Javier Viejo (Skupreme)
- Ely Liberov (Skupreme)

Key Points:
1. Agreement sent via Adobe Sign (June)
2. Multiple follow-ups sent
3. Ely stated: "No new business until anti-raiding provisions in place"
4. Javier confirmed JM Group signing but Skupreme agreement pending
5. Blocking Tactical close ($450K)

Action: Resend agreement, emphasize urgency, include anti-poaching provisions""",
        priority="HIGH",
        due_days=1  # Tomorrow
    )

    print(f"✅ {deal_name} updated successfully\n")

def update_joshs_frogs():
    """Update Josh's Frogs with Priority 1 status"""
    deal_name = "Josh's Frogs"

    print(f"\n{'='*80}")
    print(f"UPDATING: {deal_name}")
    print('='*80)

    # Add note about Priority 1 addition
    note = """**ADDED TO PRIORITY 1 - READY TO SEND (Oct 7)**

Deal Value: $2.34M/year opportunity
Volume: 27,000 packages/month (324,000 annual)
Savings: 12-15% ($26-32K/month for customer)

Analysis Complete:
- Summary: Joshs_Frogs_Analysis_Summary.md
- Email draft: Email_to_Josh.txt
- Workbook: Joshs_Frogs_PLD_Analysis.xlsx

Profile:
- 43.7% under 1 lb (lightweight profile)
- Consistent volume
- Ideal for Xparcel services

Special Consideration:
- Live insect shipping requirements (verify compliance)

Next Action:
- Send proposal immediately (Priority 1 #3)
- Review email draft and workbook
- Verify live insect shipping requirements

Status: READY TO SEND TODAY
Stage: [03-RATE-CREATION] (HubSpot shows, but analysis complete)
"""

    add_deal_note(deal_name, note)

    # Create task for proposal send
    create_task(
        deal_name=deal_name,
        task_subject="SEND Josh's Frogs Proposal ($2.34M Opportunity)",
        task_body="""Send proposal to Josh's Frogs:

Email: [01-DISCOVERY-SCHEDULED]_Josh's_Frogs/Email_to_Josh.txt
Workbook: Joshs_Frogs_PLD_Analysis.xlsx

Key Points:
- 27,000 packages/month (324,000 annual)
- 12-15% savings ($26-32K/month)
- Lightweight profile (43.7% <1lb)
- VERIFY: Live insect shipping requirements

Priority 1 #3 - High-value opportunity
Send TODAY""",
        priority="HIGH",
        due_days=0  # Today
    )

    print(f"✅ {deal_name} updated successfully\n")

def main():
    """Execute all HubSpot updates"""
    print("="*80)
    print("HUBSPOT BATCH UPDATES - TUESDAY 9AM SYNC")
    print("Based on Superhuman Email Context - October 7, 2025")
    print("="*80)

    try:
        # Update Priority 1 deals
        update_stackd_logistics()
        update_boxiiship()
        update_team_shipper()
        update_joshs_frogs()

        # Update Priority 2 deals
        update_tactical_logistic()

        print("\n" + "="*80)
        print("BATCH UPDATE COMPLETE")
        print("="*80)
        print("\nSummary:")
        print("✅ Stackd Logistics - Rates approved, meeting request task created")
        print("✅ BoxiiShip - Transit report notes added, action item tasks created")
        print("✅ Team Shipper - Verification task created")
        print("✅ Josh's Frogs - Priority 1 addition documented, send task created")
        print("✅ Tactical Logistic - Skupreme blocker documented, follow-up task created")
        print("\nAll deals updated with latest email context from Superhuman.")

    except Exception as e:
        print(f"\n❌ ERROR during batch update: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
