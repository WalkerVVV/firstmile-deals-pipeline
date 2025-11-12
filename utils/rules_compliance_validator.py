"""
Rules Compliance Validator

Automated validation of rules.md compliance for sync scripts and analysis operations.
Prevents common mistakes by enforcing quality gates before execution.

Usage:
    from utils.rules_compliance_validator import RulesComplianceValidator

    validator = RulesComplianceValidator()
    validator.validate_sync_operation(
        sync_type='9am',
        context_loaded=True,
        hubspot_data_fresh=True,
        previous_sync_path='/path/to/eod_sync.md'
    )
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json


class RulesComplianceValidator:
    """Validates operations against rules.md quality gates and best practices"""

    def __init__(self):
        self.violations = []
        self.warnings = []
        self.compliance_score = 100.0

    def reset(self):
        """Reset validator state for new operation"""
        self.violations = []
        self.warnings = []
        self.compliance_score = 100.0

    # ===================
    # SYNC FLOW VALIDATION
    # ===================

    def validate_sync_operation(
        self,
        sync_type: str,
        context_loaded: bool = False,
        hubspot_data_fresh: bool = False,
        previous_sync_path: Optional[str] = None,
        learnings_captured: bool = False,
        priorities_documented: bool = False
    ) -> Dict:
        """
        Validate sync operation compliance with rules.md

        Args:
            sync_type: One of ['9am', 'noon', '3pm', 'eod', 'weekly']
            context_loaded: Whether previous sync context was loaded
            hubspot_data_fresh: Whether fresh HubSpot data was fetched
            previous_sync_path: Path to previous sync output file
            learnings_captured: Whether learnings section is populated (required for EOD/weekly)
            priorities_documented: Whether priority actions are documented

        Returns:
            Dict with compliance status, violations, warnings, and score
        """
        self.reset()

        # Rule: Context Continuity Chain
        if sync_type != 'weekly':  # Weekly loads from multiple daily syncs
            if not context_loaded:
                self.violations.append(
                    f"VIOLATION: {sync_type.upper()} sync MUST load previous sync context (Rule: Context Continuity Chain)"
                )
                self.compliance_score -= 20

            if previous_sync_path and not Path(previous_sync_path).exists():
                self.warnings.append(
                    f"WARNING: Previous sync file not found at {previous_sync_path}. Request manual context."
                )
                self.compliance_score -= 10

        # Rule: Fresh HubSpot Data Required
        if not hubspot_data_fresh:
            self.violations.append(
                f"VIOLATION: {sync_type.upper()} sync requires fresh HubSpot data fetch (Rule: Agent Best Practices #2)"
                )
            self.compliance_score -= 15

        # Rule: Learning Gates (EOD and Weekly only)
        if sync_type in ['eod', 'weekly']:
            if not learnings_captured:
                self.violations.append(
                    f"VIOLATION: {sync_type.upper()} sync MUST capture learnings (Rule: Learning Gates #3)"
                )
                self.compliance_score -= 25

        # Rule: Priority Documentation (all except EOD)
        if sync_type != 'eod' and not priorities_documented:
            self.violations.append(
                f"VIOLATION: {sync_type.upper()} sync MUST document priority actions (Rule: Sync Flow Constraints)"
            )
            self.compliance_score -= 15

        return self._generate_report(f"{sync_type.upper()} Sync")

    # ==========================
    # HUBSPOT INTEGRATION VALIDATION
    # ==========================

    def validate_hubspot_operation(
        self,
        uses_shared_manager: bool = False,
        credentials_validated: bool = False,
        rate_limiter_enabled: bool = False,
        folder_verified: bool = False,
        operation_type: str = "general"
    ) -> Dict:
        """
        Validate HubSpot API operation compliance

        Args:
            uses_shared_manager: Whether using hubspot_sync_core.HubSpotSyncManager
            credentials_validated: Whether CredentialManager.load_and_validate() was called
            rate_limiter_enabled: Whether rate limiting is active
            folder_verified: Whether folder location verified (for stage updates)
            operation_type: One of ['search', 'create', 'update_stage', 'general']

        Returns:
            Dict with compliance status
        """
        self.reset()

        # Rule: Shared Code > Duplication
        if not uses_shared_manager:
            self.violations.append(
                "VIOLATION: ALL HubSpot operations MUST use hubspot_sync_core.HubSpotSyncManager (Rule #1)"
            )
            self.compliance_score -= 30

        # Rule: Credential Security
        if not credentials_validated:
            self.violations.append(
                "VIOLATION: Credentials MUST be validated before HubSpot operations (Rule #5)"
            )
            self.compliance_score -= 25

        # Rule: Rate Limiting (Critical for API health)
        if not rate_limiter_enabled:
            self.violations.append(
                "VIOLATION: HubSpot operations MUST use rate limiter (100 calls per 10 seconds) (Rule #1)"
            )
            self.compliance_score -= 35

        # Rule: Folder-HubSpot Consistency
        if operation_type == 'update_stage' and not folder_verified:
            self.violations.append(
                "VIOLATION: Deal stage updates MUST verify folder location (Rule #4)"
            )
            self.compliance_score -= 20

        return self._generate_report(f"HubSpot {operation_type.title()} Operation")

    # ========================
    # BRAND SCOUT VALIDATION
    # ========================

    def validate_brand_scout_operation(
        self,
        human_approval_received: bool = False,
        confidence_scores_calculated: bool = False,
        sources_documented: bool = False,
        output_saved: bool = False,
        is_business_hours: bool = False
    ) -> Dict:
        """
        Validate Brand Scout operation compliance

        Args:
            human_approval_received: Whether human approved leads before HubSpot creation
            confidence_scores_calculated: Whether confidence scores assigned
            sources_documented: Whether research sources documented
            output_saved: Whether output saved to .claude/brand_scout/output/
            is_business_hours: Whether running during business hours (prohibited)

        Returns:
            Dict with compliance status
        """
        self.reset()

        # Rule: Human Approval Gate
        if not human_approval_received:
            self.violations.append(
                "VIOLATION: Brand Scout MUST receive human approval before HubSpot creation (Rule #6)"
            )
            self.compliance_score -= 30

        # Rule: Confidence Scoring Required
        if not confidence_scores_calculated:
            self.violations.append(
                "VIOLATION: Brand Scout MUST calculate confidence scores (High/Medium/Low) for all leads"
            )
            self.compliance_score -= 15

        # Rule: Source Attribution
        if not sources_documented:
            self.warnings.append(
                "WARNING: Brand Scout should document research sources for verification"
            )
            self.compliance_score -= 10

        # Rule: Output Storage
        if not output_saved:
            self.warnings.append(
                "WARNING: Brand Scout output should be saved to .claude/brand_scout/output/ for review"
            )
            self.compliance_score -= 10

        # Rule: Overnight Execution Only
        if is_business_hours:
            self.violations.append(
                "VIOLATION: Brand Scout MUST run overnight only (not during business hours)"
            )
            self.compliance_score -= 20

        return self._generate_report("Brand Scout Operation")

    # =======================
    # ANALYSIS VALIDATION
    # =======================

    def validate_analysis_operation(
        self,
        follows_firstmile_framework: bool = False,
        sla_compliance_leads: bool = False,
        uses_network_terminology: bool = False,
        carrier_names_mentioned: bool = False,
        zone_distribution_included: bool = False,
        hub_mapping_included: bool = False,
        analysis_type: str = "general"
    ) -> Dict:
        """
        Validate analysis operation compliance with FIRSTMILE.md

        Args:
            follows_firstmile_framework: Whether analysis follows FIRSTMILE.md structure
            sla_compliance_leads: Whether SLA compliance is primary metric (not daily %)
            uses_network_terminology: Whether using "National" or "Select" (not carrier names)
            carrier_names_mentioned: Whether specific carriers named (UPS, FedEx, USPS) - PROHIBITED
            zone_distribution_included: Whether zone distribution analysis included
            hub_mapping_included: Whether geographic hub mapping included
            analysis_type: One of ['pld', 'performance_report', 'rate_comparison', 'general']

        Returns:
            Dict with compliance status
        """
        self.reset()

        # Rule: FIRSTMILE.md Framework Compliance
        if not follows_firstmile_framework:
            self.violations.append(
                "VIOLATION: ALL analysis MUST follow FIRSTMILE.md framework (Rule #7)"
            )
            self.compliance_score -= 25

        # Rule: SLA Compliance Leads (performance reports)
        if analysis_type == 'performance_report' and not sla_compliance_leads:
            self.violations.append(
                "VIOLATION: Performance reports MUST lead with SLA compliance (not daily %) (FIRSTMILE.md)"
            )
            self.compliance_score -= 30

        # Rule: Network Terminology Required
        if not uses_network_terminology:
            self.violations.append(
                "VIOLATION: Use 'National' or 'Select' network terminology (FIRSTMILE.md)"
            )
            self.compliance_score -= 15

        # Rule: NEVER Name Carriers
        if carrier_names_mentioned:
            self.violations.append(
                "VIOLATION: NEVER name specific carriers (UPS, FedEx, USPS) in reports (FIRSTMILE.md)"
            )
            self.compliance_score -= 35

        # Rule: Zone Distribution Required
        if analysis_type == 'pld' and not zone_distribution_included:
            self.violations.append(
                "VIOLATION: PLD analysis MUST include zone distribution (Rule #7)"
            )
            self.compliance_score -= 20

        # Rule: Hub Mapping Required
        if not hub_mapping_included:
            self.warnings.append(
                "WARNING: Analysis should include geographic hub mapping for top states"
            )
            self.compliance_score -= 10

        return self._generate_report(f"Analysis Operation ({analysis_type})")

    # =======================
    # EXCEL REPORT VALIDATION
    # =======================

    def validate_excel_report(
        self,
        has_9_tabs: bool = False,
        firstmile_blue_headers: bool = False,
        sla_tab_leads: bool = False,
        conditional_formatting: bool = False,
        auto_filters_enabled: bool = False,
        filename_follows_convention: bool = False
    ) -> Dict:
        """
        Validate Excel report compliance with brand standards

        Args:
            has_9_tabs: Whether report has all 9 required tabs
            firstmile_blue_headers: Whether FirstMile blue (#366092) applied to headers
            sla_tab_leads: Whether SLA Compliance is tab #2 (leads metrics)
            conditional_formatting: Whether red/yellow/green applied to SLA tab
            auto_filters_enabled: Whether auto-filters enabled on data tables
            filename_follows_convention: Whether filename follows FirstMile_Xparcel_Performance_{Customer}_{Date}.xlsx

        Returns:
            Dict with compliance status
        """
        self.reset()

        # Rule: 9-Tab Structure Required
        if not has_9_tabs:
            self.violations.append(
                "VIOLATION: Excel reports MUST have 9 tabs in specified order (Excel Reporting Standards)"
            )
            self.compliance_score -= 30

        # Rule: FirstMile Brand Colors
        if not firstmile_blue_headers:
            self.violations.append(
                "VIOLATION: All Excel headers MUST use FirstMile blue (#366092) (Excel Reporting Standards)"
            )
            self.compliance_score -= 20

        # Rule: SLA Compliance Leads
        if not sla_tab_leads:
            self.violations.append(
                "VIOLATION: SLA Compliance tab MUST be #2 and lead all metrics (Excel Reporting Standards)"
            )
            self.compliance_score -= 25

        # Rule: Conditional Formatting
        if not conditional_formatting:
            self.warnings.append(
                "WARNING: SLA tab should have conditional formatting (red/yellow/green)"
            )
            self.compliance_score -= 10

        # Rule: Auto-Filters
        if not auto_filters_enabled:
            self.warnings.append(
                "WARNING: Data tables should have auto-filters enabled"
            )
            self.compliance_score -= 5

        # Rule: Filename Convention
        if not filename_follows_convention:
            self.warnings.append(
                "WARNING: Filename should follow FirstMile_Xparcel_Performance_{Customer}_{YYYYMMDD_HHMM}.xlsx"
            )
            self.compliance_score -= 10

        return self._generate_report("Excel Report")

    # ====================
    # FOLDER OPERATIONS VALIDATION
    # ====================

    def validate_folder_operation(
        self,
        user_approval_requested: bool = False,
        hubspot_sync_verified: bool = False,
        operation_type: str = "move"
    ) -> Dict:
        """
        Validate folder operation compliance

        Args:
            user_approval_requested: Whether user approval requested before move
            hubspot_sync_verified: Whether HubSpot stage verified/updated
            operation_type: One of ['move', 'create', 'archive']

        Returns:
            Dict with compliance status
        """
        self.reset()

        # Rule: Ask Before Folder Moves
        if operation_type == 'move' and not user_approval_requested:
            self.violations.append(
                "VIOLATION: MUST ask before moving deal folders (Rule #8)"
            )
            self.compliance_score -= 25

        # Rule: Folder-HubSpot Consistency
        if operation_type == 'move' and not hubspot_sync_verified:
            self.violations.append(
                "VIOLATION: Folder moves MUST verify/update HubSpot stage (Rule #4)"
            )
            self.compliance_score -= 30

        return self._generate_report(f"Folder {operation_type.title()} Operation")

    # ======================
    # LEARNING LOOP VALIDATION
    # ======================

    def validate_learning_capture(
        self,
        insights_documented: bool = False,
        memory_updated: bool = False,
        patterns_recognized: bool = False,
        next_actions_identified: bool = False,
        context_saved_for_next_session: bool = False
    ) -> Dict:
        """
        Validate learning loop compliance

        Args:
            insights_documented: Whether insights captured in markdown
            memory_updated: Whether .claude/data/deal_memory/ updated
            patterns_recognized: Whether patterns identified (weekly sync only)
            next_actions_identified: Whether next actions documented
            context_saved_for_next_session: Whether context saved for next sync

        Returns:
            Dict with compliance status
        """
        self.reset()

        # Rule: Learning Gates
        if not insights_documented:
            self.violations.append(
                "VIOLATION: Learnings MUST be documented in markdown output (Rule #3)"
            )
            self.compliance_score -= 25

        # Rule: Memory Updates
        if not memory_updated:
            self.warnings.append(
                "WARNING: Deal memory database should be updated with new insights"
            )
            self.compliance_score -= 10

        # Rule: Next Actions Required
        if not next_actions_identified:
            self.violations.append(
                "VIOLATION: Next actions MUST be identified before marking complete (Rule #3)"
            )
            self.compliance_score -= 20

        # Rule: Context Continuity
        if not context_saved_for_next_session:
            self.violations.append(
                "VIOLATION: Context MUST be saved for next session (Rule #2)"
            )
            self.compliance_score -= 30

        return self._generate_report("Learning Capture")

    # ===================
    # REPORTING & UTILITIES
    # ===================

    def _generate_report(self, operation_name: str) -> Dict:
        """Generate compliance report with violations, warnings, and score"""
        status = "PASS" if self.compliance_score >= 90 else "WARNING" if self.compliance_score >= 70 else "FAIL"

        report = {
            'operation': operation_name,
            'status': status,
            'compliance_score': round(self.compliance_score, 1),
            'violations': self.violations,
            'warnings': self.warnings,
            'timestamp': datetime.now().isoformat()
        }

        return report

    def print_report(self, report: Dict):
        """Print formatted compliance report"""
        print("\n" + "="*60)
        print(f"RULES COMPLIANCE REPORT: {report['operation']}")
        print("="*60)
        print(f"Status: {report['status']}")
        print(f"Compliance Score: {report['compliance_score']}%")
        print(f"Timestamp: {report['timestamp']}")

        if report['violations']:
            print("\n🚨 VIOLATIONS (Must Fix):")
            for idx, violation in enumerate(report['violations'], 1):
                print(f"  {idx}. {violation}")

        if report['warnings']:
            print("\n⚠️  WARNINGS (Should Address):")
            for idx, warning in enumerate(report['warnings'], 1):
                print(f"  {idx}. {warning}")

        if report['status'] == 'PASS':
            print("\n✅ Operation complies with rules.md standards")
        elif report['status'] == 'WARNING':
            print("\n⚠️  Operation has warnings - review before proceeding")
        else:
            print("\n❌ Operation FAILS compliance - address violations before continuing")

        print("="*60 + "\n")

    def save_report(self, report: Dict, output_path: str):
        """Save compliance report to JSON file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✅ Compliance report saved to {output_file}")


# ======================
# CONVENIENCE FUNCTIONS
# ======================

def validate_9am_sync(context_loaded: bool, previous_eod_path: str, hubspot_fresh: bool) -> Dict:
    """Quick validation for 9AM sync"""
    validator = RulesComplianceValidator()
    report = validator.validate_sync_operation(
        sync_type='9am',
        context_loaded=context_loaded,
        hubspot_data_fresh=hubspot_fresh,
        previous_sync_path=previous_eod_path,
        priorities_documented=True  # Assumed for 9AM
    )
    validator.print_report(report)
    return report


def validate_eod_sync(context_loaded: bool, learnings_captured: bool, hubspot_fresh: bool) -> Dict:
    """Quick validation for EOD sync"""
    validator = RulesComplianceValidator()
    report = validator.validate_sync_operation(
        sync_type='eod',
        context_loaded=context_loaded,
        hubspot_data_fresh=hubspot_fresh,
        learnings_captured=learnings_captured,
        priorities_documented=False  # EOD doesn't need priorities
    )
    validator.print_report(report)
    return report


def validate_hubspot_call(uses_shared_manager: bool, credentials_validated: bool) -> Dict:
    """Quick validation for HubSpot API calls"""
    validator = RulesComplianceValidator()
    report = validator.validate_hubspot_operation(
        uses_shared_manager=uses_shared_manager,
        credentials_validated=credentials_validated,
        rate_limiter_enabled=uses_shared_manager  # If using shared manager, rate limiter is enabled
    )
    validator.print_report(report)
    return report


if __name__ == "__main__":
    # Example usage
    print("Rules Compliance Validator - Example Usage\n")

    # Example 1: Validate 9AM sync
    print("Example 1: Validating 9AM Sync")
    report_9am = validate_9am_sync(
        context_loaded=True,
        previous_eod_path="/path/to/eod_sync.md",
        hubspot_fresh=True
    )

    # Example 2: Validate HubSpot operation (with violation)
    print("\nExample 2: Validating HubSpot Operation (with violations)")
    report_hubspot = validate_hubspot_call(
        uses_shared_manager=False,  # VIOLATION
        credentials_validated=True
    )

    # Example 3: Validate Brand Scout
    print("\nExample 3: Validating Brand Scout Operation")
    validator = RulesComplianceValidator()
    report_scout = validator.validate_brand_scout_operation(
        human_approval_received=True,
        confidence_scores_calculated=True,
        sources_documented=True,
        output_saved=True,
        is_business_hours=False
    )
    validator.print_report(report_scout)
