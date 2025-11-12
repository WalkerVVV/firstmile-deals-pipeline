"""
Example: 9AM Sync with Rules Compliance Validation

Demonstrates how to integrate rules_compliance_validator.py into sync scripts
to enforce quality gates before execution.

Usage:
    python examples/sync_with_compliance_validation.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils.credential_manager import CredentialManager
from hubspot_sync_core import HubSpotSyncManager
from utils.rules_compliance_validator import RulesComplianceValidator


def load_previous_eod_context(eod_path: Path) -> dict:
    """Load yesterday's EOD context from markdown file"""
    if not eod_path.exists():
        print(f"⚠️  Yesterday's EOD not found at {eod_path}")
        return None

    with open(eod_path, 'r') as f:
        content = f.read()

    # Parse learnings and carry-forward actions from markdown
    context = {
        'learnings': extract_section(content, '## Learnings Captured'),
        'carry_forward': extract_section(content, '## Context for Next Session'),
        'loaded_at': datetime.now().isoformat()
    }

    print(f"✅ Loaded EOD context from {eod_path}")
    return context


def extract_section(markdown: str, heading: str) -> str:
    """Extract markdown section content by heading"""
    if heading not in markdown:
        return ""

    start = markdown.find(heading)
    # Find next heading or end of file
    next_heading = markdown.find('\n## ', start + len(heading))
    if next_heading == -1:
        return markdown[start + len(heading):].strip()
    return markdown[start + len(heading):next_heading].strip()


def run_9am_sync_with_validation():
    """
    Execute 9AM sync with full rules compliance validation

    Quality Gates:
    1. Load yesterday's EOD context BEFORE HubSpot fetch
    2. Validate credentials before API calls
    3. Use shared HubSpotSyncManager (rate limited)
    4. Document priority actions
    5. Save context for noon sync
    """

    print("\n" + "="*60)
    print("9AM PRIORITY SYNC - WITH COMPLIANCE VALIDATION")
    print("="*60 + "\n")

    # ==================
    # PHASE 1: CONTEXT LOADING
    # ==================
    print("PHASE 1: Loading Previous Context...")

    # Find yesterday's EOD file
    yesterday = datetime.now() - timedelta(days=1)
    eod_filename = f"eod_sync_{yesterday.strftime('%Y%m%d')}.md"
    eod_path = Path(f"sync_outputs/{eod_filename}")

    previous_context = load_previous_eod_context(eod_path)

    # ==================
    # PHASE 2: COMPLIANCE VALIDATION (Pre-Flight)
    # ==================
    print("\nPHASE 2: Validating Compliance (Pre-Flight)...")

    validator = RulesComplianceValidator()

    # Validate sync operation BEFORE execution
    pre_flight_report = validator.validate_sync_operation(
        sync_type='9am',
        context_loaded=previous_context is not None,
        hubspot_data_fresh=False,  # Not fetched yet
        previous_sync_path=str(eod_path) if eod_path.exists() else None,
        priorities_documented=False  # Will be documented after fetch
    )

    validator.print_report(pre_flight_report)

    # STOP if critical violations
    if pre_flight_report['status'] == 'FAIL':
        print("❌ Pre-flight validation FAILED. Address violations before continuing.")
        print("\nSuggested Actions:")
        if not previous_context:
            print("  - Request manual context summary from user")
            print("  - Document that yesterday's EOD is missing")
        sys.exit(1)

    # ==================
    # PHASE 3: CREDENTIAL VALIDATION
    # ==================
    print("\nPHASE 3: Validating Credentials...")

    try:
        CredentialManager.load_and_validate()
        config = CredentialManager.get_hubspot_config()
        credentials_valid = True
        print("✅ Credentials validated")
    except Exception as e:
        print(f"❌ Credential validation failed: {e}")
        credentials_valid = False
        sys.exit(1)

    # Validate HubSpot operation setup
    hubspot_validation = validator.validate_hubspot_operation(
        uses_shared_manager=True,  # We're using HubSpotSyncManager below
        credentials_validated=credentials_valid,
        rate_limiter_enabled=True,  # Shared manager includes rate limiter
        operation_type='search'
    )

    validator.print_report(hubspot_validation)

    if hubspot_validation['status'] == 'FAIL':
        print("❌ HubSpot operation validation FAILED.")
        sys.exit(1)

    # ==================
    # PHASE 4: HUBSPOT DATA FETCH
    # ==================
    print("\nPHASE 4: Fetching Active Deals from HubSpot...")

    sync_manager = HubSpotSyncManager(**config)

    try:
        active_deals = sync_manager.search_deals(
            filters=[
                {
                    "propertyName": "dealstage",
                    "operator": "IN",
                    "values": [
                        "01-discovery-scheduled",
                        "02-discovery-complete",
                        "03-rate-creation",
                        "04-proposal-sent",
                        "05-setup-docs-sent",
                        "06-implementation"
                    ]
                }
            ],
            properties=["dealname", "dealstage", "amount", "createdate", "hs_lastmodifieddate"],
            limit=100
        )
        print(f"✅ Fetched {len(active_deals)} active deals")
    except Exception as e:
        print(f"❌ HubSpot fetch failed: {e}")
        sys.exit(1)

    # ==================
    # PHASE 5: PRIORITY SCORING
    # ==================
    print("\nPHASE 5: Calculating Priority Scores...")

    # Simple priority scoring (days in stage * 2 + deal value weight)
    for deal in active_deals:
        props = deal.get('properties', {})
        last_modified = props.get('hs_lastmodifieddate', '')
        amount = float(props.get('amount', 0))

        # Calculate days in stage (simplified)
        days_in_stage = 5  # Placeholder - would calculate from last_modified

        priority_score = (days_in_stage * 2) + (amount / 100000)
        deal['priority_score'] = round(priority_score, 2)
        deal['days_in_stage'] = days_in_stage

    # Sort by priority score
    active_deals.sort(key=lambda x: x['priority_score'], reverse=True)

    print(f"✅ Priority scores calculated for {len(active_deals)} deals")

    # ==================
    # PHASE 6: GENERATE REPORT
    # ==================
    print("\nPHASE 6: Generating Priority Report...")

    top_priorities = active_deals[:5]

    report_content = f"""# 9AM Priority Sync - {datetime.now().strftime('%A, %B %d, %Y')}

## Yesterday's Context
{previous_context['learnings'] if previous_context else 'No previous context available'}

**Carry-Forward Actions**:
{previous_context['carry_forward'] if previous_context else 'None'}

---

## Active Deals by Priority

| Deal Name | Stage | Days in Stage | Deal Value | Priority Score |
|-----------|-------|---------------|------------|----------------|
"""

    for deal in active_deals:
        props = deal['properties']
        report_content += f"| {props['dealname']} | {props['dealstage']} | {deal['days_in_stage']} days | ${props.get('amount', 0)} | {deal['priority_score']} |\n"

    report_content += f"""
**Total Active Deals**: {len(active_deals)}

---

## Priority Actions (Today)

"""

    for idx, deal in enumerate(top_priorities, 1):
        props = deal['properties']
        report_content += f"{idx}. **{props['dealname']}** - Priority Score: {deal['priority_score']}\n"
        report_content += f"   - Stage: {props['dealstage']} ({deal['days_in_stage']} days)\n"
        report_content += f"   - Action: [Define action based on stage]\n\n"

    report_content += f"""
---

## Follow-Up Queue (This Week)

**Today ({datetime.now().strftime('%B %d')})**:
- [ ] Action 1 from top priorities
- [ ] Action 2 from top priorities

**Later This Week**:
- [ ] Follow-up items

---

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M %p CT')}
**Agent**: Prioritization Agent with Compliance Validation
"""

    # ==================
    # PHASE 7: SAVE OUTPUT
    # ==================
    print("\nPHASE 7: Saving Output...")

    output_dir = Path("sync_outputs")
    output_dir.mkdir(exist_ok=True)

    output_filename = f"9am_sync_{datetime.now().strftime('%Y%m%d')}.md"
    output_path = output_dir / output_filename

    with open(output_path, 'w') as f:
        f.write(report_content)

    print(f"✅ Report saved to {output_path}")

    # ==================
    # PHASE 8: POST-EXECUTION VALIDATION
    # ==================
    print("\nPHASE 8: Post-Execution Compliance Validation...")

    post_execution_report = validator.validate_sync_operation(
        sync_type='9am',
        context_loaded=previous_context is not None,
        hubspot_data_fresh=True,  # Just fetched
        previous_sync_path=str(eod_path) if eod_path.exists() else None,
        priorities_documented=True  # Report includes priority actions
    )

    validator.print_report(post_execution_report)

    # Save compliance report
    compliance_dir = Path("compliance_reports")
    compliance_dir.mkdir(exist_ok=True)
    compliance_filename = f"9am_sync_compliance_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    validator.save_report(post_execution_report, str(compliance_dir / compliance_filename))

    # ==================
    # PHASE 9: FINAL STATUS
    # ==================
    print("\n" + "="*60)
    if post_execution_report['status'] == 'PASS':
        print("✅ 9AM SYNC COMPLETE - ALL QUALITY GATES PASSED")
    elif post_execution_report['status'] == 'WARNING':
        print("⚠️  9AM SYNC COMPLETE - REVIEW WARNINGS")
    else:
        print("❌ 9AM SYNC COMPLETE - VIOLATIONS DETECTED")

    print("="*60 + "\n")

    print(f"Output: {output_path}")
    print(f"Compliance Report: {compliance_dir / compliance_filename}")
    print(f"Next Sync: Load context from {output_path}\n")


if __name__ == "__main__":
    run_9am_sync_with_validation()
