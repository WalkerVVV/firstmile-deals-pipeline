#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BRAND SCOUT AUTOMATION AGENT
Purpose: Automated brand research and lead generation for wellness/D2C brands
Modes: On-demand (single brand) or scheduled (10 leads every Monday 6AM)

Usage:
    On-demand: python brand_scout_agent.py "Athleta"
    Scheduled: python brand_scout_agent.py --batch 10
"""

import sys, io, os, re
import json
import argparse
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

# Repository root
REPO_ROOT = Path(__file__).parent.parent.parent
BRAND_SCOUT_DIR = REPO_ROOT / ".claude" / "brand_scout"
OUTPUT_DIR = BRAND_SCOUT_DIR / "output"
INPUT_DIR = BRAND_SCOUT_DIR / "input"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_DIR.mkdir(parents=True, exist_ok=True)

HUBSPOT_API_KEY = os.getenv('HUBSPOT_API_KEY')

# Target industries for lead generation
TARGET_INDUSTRIES = [
    "wellness",
    "supplements",
    "vitamins",
    "health",
    "beauty",
    "cosmetics",
    "skincare",
    "fitness",
    "nutrition",
    "ecommerce"
]


def create_brand_profile_template(brand_name):
    """Create a structured brand profile template"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    template = f"""# Brand Scout Report: {brand_name}
Generated: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

## Company Overview

**Brand Name**: {brand_name}
**Industry**: [To be researched]
**Website**: [To be researched]
**Estimated Annual Revenue**: [To be researched]
**Employee Count**: [To be researched]

## Shipping Profile

**Current Carriers**: [To be researched]
- Carrier 1: [Name, service levels used]
- Carrier 2: [Name, service levels used]

**Estimated Monthly Volume**: [To be researched]
- Package count: [X packages/month]
- Service mix: [X% Ground, Y% Expedited, Z% Priority]

**Geographic Distribution**: [To be researched]
- Top 5 states by volume

**Weight Profile**: [To be researched]
- Average package weight: [X lbs]
- Weight distribution: [% under 1 lb, % 1-5 lbs, % over 5 lbs]

## Decision Makers

**Primary Contact**:
- Name: [To be researched]
- Title: [To be researched]
- Email: [To be researched]
- Phone: [To be researched]

**Secondary Contacts**:
- Name: [To be researched]
- Title: [To be researched]
- Email: [To be researched]

## FirstMile Opportunity

**Estimated Annual Shipping Spend**: $[X]
**Potential FirstMile Savings**: $[Y] (40% target)
**Service Fit**:
- Xparcel Ground: [Yes/No - reasoning]
- Xparcel Expedited: [Yes/No - reasoning]
- Xparcel Priority: [Yes/No - reasoning]

**Deal Size**: $[X]K - $[Y]K ARR

## Next Steps

1. [ ] Verify contact information
2. [ ] Create HubSpot lead
3. [ ] Research shipping patterns (if data available)
4. [ ] Prepare outreach email
5. [ ] Schedule discovery call

## Research Sources

- Company website: [URL]
- LinkedIn: [URL]
- Other sources: [List]

## Notes

[Add any additional context, competitive intelligence, or insights]

---

**Status**: Research in progress
**Owner**: Brett Walker
**Priority**: [To be assessed]
"""

    return template


def create_hubspot_lead_payload(brand_name, profile_data=None):
    """Create HubSpot API payload for lead creation"""

    payload = {
        "properties": {
            "firstname": profile_data.get("contact_first_name", "Unknown") if profile_data else "Unknown",
            "lastname": profile_data.get("contact_last_name", "Contact") if profile_data else "Contact",
            "email": profile_data.get("contact_email", "") if profile_data else "",
            "company": brand_name,
            "phone": profile_data.get("contact_phone", "") if profile_data else "",
            "lifecyclestage": "lead",
            "lead_source": "Brand Scout",
            "hs_lead_status": "NEW"
        }
    }

    return payload


def create_deal_folder(brand_name):
    """Create brand folder in _LEADS directory"""

    # Sanitize brand name for folder
    folder_name = brand_name.replace(' ', '_')
    leads_folder = REPO_ROOT / "_LEADS"
    leads_folder.mkdir(exist_ok=True)  # Ensure _LEADS exists

    deal_folder = leads_folder / folder_name

    if deal_folder.exists():
        print(f"⚠️  Folder already exists: _LEADS/{folder_name}")
        return deal_folder

    # Create folder
    deal_folder.mkdir(parents=True, exist_ok=True)

    # Create Customer_Relationship_Documentation.md
    doc_file = deal_folder / "Customer_Relationship_Documentation.md"

    doc_content = f"""# {brand_name} - Customer Relationship Documentation

## Account Overview
**Company Name**: {brand_name}
**Industry**: Wellness / D2C eCommerce
**Lead Source**: Brand Scout Automation
**Lead Date**: {datetime.now().strftime("%B %d, %Y")}
**Owner**: Brett Walker

## Contact Information
**Primary Contact**: [To be researched]
- Title: [To be researched]
- Email: [To be researched]
- Phone: [To be researched]
- LinkedIn: [To be researched]

## Shipping Profile (Estimated)
**Estimated Annual Volume**: [To be researched]
**Current Carriers**: [To be researched]
**Service Levels**: [To be researched]

## Opportunity Assessment
**Estimated Deal Size**: [To be calculated]
**Potential Savings**: [To be calculated]
**Service Fit**: Xparcel [Ground/Expedited/Priority]

## Next Steps
1. Complete brand research via Brand Scout report
2. Identify decision makers (Ops, Supply Chain, Finance)
3. Create HubSpot lead record
4. Draft outreach email
5. Schedule discovery call

## Relationship Timeline
- **{datetime.now().strftime("%Y-%m-%d")}**: Lead generated via Brand Scout Automation
- **[Date]**: First outreach
- **[Date]**: Discovery call scheduled

## Notes
[Add notes, insights, competitive intelligence, or other relevant context]
"""

    doc_file.write_text(doc_content, encoding='utf-8')

    print(f"✅ Created deal folder: {folder_name}")
    print(f"   📄 Customer_Relationship_Documentation.md")

    return deal_folder


def process_single_brand(brand_name):
    """Process a single brand - create profile, folder, and HubSpot lead"""

    print(f"\n{'='*80}")
    print(f"BRAND SCOUT: {brand_name}")
    print('='*80 + "\n")

    # Create brand profile template
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    profile_file = OUTPUT_DIR / f"{brand_name.replace(' ', '_')}_{timestamp}.md"

    profile_content = create_brand_profile_template(brand_name)
    profile_file.write_text(profile_content, encoding='utf-8')

    print(f"✅ Brand profile created: {profile_file.name}")

    # Create deal folder
    deal_folder = create_deal_folder(brand_name)

    print(f"\n📋 NEXT STEPS:")
    print(f"1. Research {brand_name} and complete brand profile:")
    print(f"   {profile_file}")
    print(f"2. Update Customer_Relationship_Documentation.md:")
    print(f"   {deal_folder / 'Customer_Relationship_Documentation.md'}")
    print(f"3. Create HubSpot lead via: qm hubspot create-lead")
    print(f"4. Move folder to [01-DISCOVERY-SCHEDULED] when call booked")

    return profile_file, deal_folder


def process_batch_brands(count=10):
    """Process a batch of brands from input list"""

    print(f"\n{'='*80}")
    print(f"BRAND SCOUT: BATCH MODE ({count} leads)")
    print('='*80 + "\n")

    # Check for input file with brand list
    brand_list_file = INPUT_DIR / "brand_list.txt"

    if not brand_list_file.exists():
        print(f"❌ Brand list not found: {brand_list_file}")
        print(f"\nCreate a brand list file with one brand per line:")
        print(f"   {brand_list_file}")
        return

    # Read brand list
    brands = brand_list_file.read_text(encoding='utf-8').strip().split('\n')
    brands = [b.strip() for b in brands if b.strip()]

    if not brands:
        print(f"❌ Brand list is empty: {brand_list_file}")
        return

    print(f"📊 Found {len(brands)} brands in list")
    print(f"🎯 Processing first {min(count, len(brands))} brands\n")

    results = []

    for i, brand_name in enumerate(brands[:count], 1):
        print(f"\n{'='*80}")
        print(f"BRAND {i}/{min(count, len(brands))}: {brand_name}")
        print('='*80)

        try:
            profile_file, deal_folder = process_single_brand(brand_name)
            results.append({
                'brand': brand_name,
                'status': 'success',
                'profile': str(profile_file),
                'folder': str(deal_folder)
            })
        except Exception as e:
            print(f"❌ Error processing {brand_name}: {e}")
            results.append({
                'brand': brand_name,
                'status': 'error',
                'error': str(e)
            })

    # Summary
    print(f"\n{'='*80}")
    print("BATCH SUMMARY")
    print('='*80 + "\n")

    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'error']

    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")

    if successful:
        print(f"\n📂 Created {len(successful)} deal folders:")
        for result in successful:
            print(f"   • {result['brand']}")

    if failed:
        print(f"\n⚠️  Failed brands:")
        for result in failed:
            print(f"   • {result['brand']}: {result['error']}")

    print(f"\n📋 NEXT STEPS:")
    print(f"1. Review brand profiles in: {OUTPUT_DIR}")
    print(f"2. Complete research for each brand")
    print(f"3. Create HubSpot leads")
    print(f"4. Begin outreach process")


def main():
    """Main execution"""

    parser = argparse.ArgumentParser(
        description="Brand Scout Automation Agent - Automated brand research and lead generation"
    )
    parser.add_argument(
        "brand_name",
        nargs='?',
        help="Brand name for on-demand research"
    )
    parser.add_argument(
        "--batch",
        type=int,
        metavar="COUNT",
        help="Process COUNT brands from brand_list.txt (scheduled mode)"
    )

    args = parser.parse_args()

    if args.batch:
        # Batch mode (scheduled)
        process_batch_brands(args.batch)
    elif args.brand_name:
        # On-demand mode (single brand)
        process_single_brand(args.brand_name)
    else:
        # Show usage
        parser.print_help()
        print("\nExamples:")
        print("  On-demand:  python brand_scout_agent.py 'Athleta'")
        print("  Batch:      python brand_scout_agent.py --batch 10")


if __name__ == "__main__":
    main()
