#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Update BoxiiShip documentation with detailed meeting notes"""

import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read current file
with open('Customer_Relationship_Documentation.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the meeting section and insert detailed notes after line 43
meeting_insert_index = None
for i, line in enumerate(lines):
    if '### October 2, 2025 - Performance Review Meeting' in line:
        meeting_insert_index = i
        break

if meeting_insert_index:
    # Prepare new meeting content
    new_meeting_lines = [
        '### October 2, 2025 - Performance Review & Operations Meeting\n',
        '**Attendees**:\n',
        '- **Customer**: Reid Malloch (System Beauty Logistics)\n',
        '- **FirstMile**: Brett Walker (Sales), Brock Hansen (VP/Leadership)\n',
        '**Recording**: https://fathom.video/share/whDyEH1nCg1spT1xk8crqxYbx6suaqJt\n',
        '\n',
        '**Customer Context** (Reid Malloch):\n',
        '- Manages logistics for TWO distinct customers under parent company in Southeast Asia\n',
        '- Very process-oriented and detail-focused manager\n',
        '- Coordinating across time zones (US operations to SE Asia customers)\n',
        '- Under significant pressure for specific performance data and hard dates\n',
        '\n',
        '**Critical Issues Discussed**:\n',
        '\n',
        '1. **Tracking Visibility Problems**\n',
        '   - Packages not showing movement in tracking updates\n',
        '   - Discrepancies between FirstMile and USPS tracking statuses\n',
        '   - Reid customers demanding specifics on package location and hard delivery dates\n',
        '\n',
        '2. **Recent System Failures**\n',
        '   - Sorting machine malfunction caused delivery delays\n',
        '   - Human error in handling the malfunction\n',
        '   - System integration challenges during recent merger\n',
        '   - Manual encoding issue still unresolved\n',
        '\n',
        '3. **ACI Direct Opportunity** 💰\n',
        '   - Volume: ~2,800 shipments eligible for routing change\n',
        '   - Savings: $0.30 per shipment\n',
        '   - Monthly impact: $840/month ($10,080 annually)\n',
        '   - Additional benefit: Minimizes peak season fee impact\n',
        '   - Next step: Kevin (Operations) feasibility evaluation\n',
        '\n',
        '4. **Custom Reporting Requirements**\n',
        '   - Need for customer-specific performance data (two separate customers)\n',
        '   - Reference Fields 1 & 2 tracking implementation\n',
        '   - Monthly transit reports with detailed analytics\n',
        '   - September data breakdown by customer\n',
        '\n',
        '**Meeting Outcomes**:\n',
        '1. ✅ JIRA ticket submitted for custom domestic transit report\n',
        '2. 📊 Brock to build pivot tables for transit analysis\n',
        '3. 📧 6 action items generated with clear owners and deadlines\n',
        '4. 🔧 Process improvements: New protocols, personnel changes\n',
        '5. 💰 ACI Direct evaluation in progress (Kevin)\n',
        '6. 📈 93.67% SLA compliance confirmed\n',
        '\n'
    ]

    # Replace old meeting header and content (next 10 lines)
    del lines[meeting_insert_index:meeting_insert_index + 11]
    lines[meeting_insert_index:meeting_insert_index] = new_meeting_lines

# Write updated file
with open('Customer_Relationship_Documentation.md', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✓ Documentation updated with detailed Oct 2 meeting notes')
print('✓ Added customer context (SE Asia, two customers, time zones)')
print('✓ Detailed tracking issues, system failures, ACI Direct opportunity')
print('✓ Meeting outcomes with clear action items')
