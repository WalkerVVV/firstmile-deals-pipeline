#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Continuity management system for FirstMile sync system.

This module provides intelligent context management across sync cycles,
ensuring seamless handoff between 9AM, NOON, 3PM, and EOD operations.

Author: Claude Code
Created: 2025-11-17
"""

import sys
import io
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
from datetime import datetime, timedelta
import yaml

# NOTE: UTF-8 encoding wrapper is handled by calling script (unified_sync.py)
# Do not apply wrapper here to avoid conflicts

# Absolute paths
PROJECT_ROOT = Path("C:/Users/BrettWalker/FirstMile_Deals")
DAILY_LOG_PATH = PROJECT_ROOT / "_DAILY_LOG.md"
CONFIG_PATH = PROJECT_ROOT / ".claude/templates/ACTION_PRIORITY_CONFIG.yaml"


@dataclass
class ContinuityContext:
    """
    Represents context extracted from previous sync for continuity.

    Attributes:
        date: Log date
        last_sync_type: Most recent sync type (9am/noon/3pm/eod)
        completed_actions: Actions marked as completed
        in_progress_actions: Actions currently in progress
        blocked_items: Items marked as blocked
        carryover_actions: High-priority items not completed
        learnings: Yesterday's learnings (9am only)
        yesterday_completions: Yesterday's completions (9am only)
        validation_passed: Whether log passed validation
        missing_sections: List of missing required sections
    """
    date: str
    last_sync_type: str
    completed_actions: List[str]
    in_progress_actions: List[str]
    blocked_items: List[str]
    carryover_actions: List[str]
    learnings: List[str]
    yesterday_completions: List[str]
    validation_passed: bool
    missing_sections: List[str]


class ContinuityManager:
    """
    Intelligent continuity management for sync operations.

    Reads and writes _DAILY_LOG.md, validates required sections,
    extracts context for next sync, and maintains continuity chain.
    """

    def __init__(self, daily_log_path: Path = DAILY_LOG_PATH, config_path: Path = CONFIG_PATH):
        """
        Initialize continuity manager.

        Args:
            daily_log_path: Path to _DAILY_LOG.md
            config_path: Path to ACTION_PRIORITY_CONFIG.yaml
        """
        self.daily_log_path = daily_log_path
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from YAML file.

        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            return config
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing config file: {e}")

    def read_daily_log(self) -> Optional[str]:
        """
        Read current _DAILY_LOG.md content.

        Returns:
            Log content as string, or None if file doesn't exist
        """
        if not self.daily_log_path.exists():
            return None

        try:
            with open(self.daily_log_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"⚠️ Error reading daily log: {e}")
            return None

    def validate_log_for_sync(self, sync_type: str) -> Tuple[bool, List[str]]:
        """
        Validate that _DAILY_LOG.md has required sections for sync type.

        Args:
            sync_type: '9am', 'noon', '3pm', or 'eod'

        Returns:
            Tuple of (validation_passed, missing_sections)
        """
        log_content = self.read_daily_log()
        if log_content is None:
            return False, ["_DAILY_LOG.md does not exist"]

        # Get required sections from config
        validation_config = self.config.get('continuity_validation', {})
        required_sections = validation_config.get('required_sections', {}).get(sync_type, [])

        # Check for missing sections
        missing_sections = []
        for section in required_sections:
            if section not in log_content:
                missing_sections.append(section)

        validation_passed = len(missing_sections) == 0
        return validation_passed, missing_sections

    def extract_context(self, sync_type: str) -> ContinuityContext:
        """
        Extract relevant context from _DAILY_LOG.md for next sync.

        Args:
            sync_type: '9am', 'noon', '3pm', or 'eod'

        Returns:
            ContinuityContext object with extracted data
        """
        log_content = self.read_daily_log()
        if log_content is None:
            # Return empty context if no log exists
            return ContinuityContext(
                date="",
                last_sync_type="",
                completed_actions=[],
                in_progress_actions=[],
                blocked_items=[],
                carryover_actions=[],
                learnings=[],
                yesterday_completions=[],
                validation_passed=False,
                missing_sections=["_DAILY_LOG.md does not exist"]
            )

        # Validate log structure
        validation_passed, missing_sections = self.validate_log_for_sync(sync_type)

        # Extract date
        date = self._extract_date(log_content)

        # Extract last sync type
        last_sync_type = self._extract_last_sync_type(log_content)

        # Extract actions by status
        completed_actions = self._extract_section_items(log_content, "Completed")
        in_progress_actions = self._extract_section_items(log_content, "In Progress")
        blocked_items = self._extract_section_items(log_content, "Blocked")
        carryover_actions = self._extract_section_items(log_content, "Incomplete (Carry Forward)")

        # Extract learnings and yesterday's completions (for 9am sync)
        learnings = []
        yesterday_completions = []
        if sync_type == '9am':
            learnings = self._extract_section_items(log_content, "Learning Capture")
            yesterday_completions = self._extract_section_items(log_content, "Today's Completions")

        return ContinuityContext(
            date=date,
            last_sync_type=last_sync_type,
            completed_actions=completed_actions,
            in_progress_actions=in_progress_actions,
            blocked_items=blocked_items,
            carryover_actions=carryover_actions,
            learnings=learnings,
            yesterday_completions=yesterday_completions,
            validation_passed=validation_passed,
            missing_sections=missing_sections
        )

    def _extract_date(self, log_content: str) -> str:
        """Extract date from log header."""
        for line in log_content.split('\n'):
            if line.startswith('**Date**:'):
                return line.split(':', 1)[1].strip()
        return ""

    def _extract_last_sync_type(self, log_content: str) -> str:
        """Extract most recent sync type from log."""
        sync_markers = ['🌙 END OF DAY WRAP', '⚡ 3PM CHECK-IN', '📊 NOON CHECK-IN', '🌅 MORNING CONTEXT']
        sync_types = ['eod', '3pm', 'noon', '9am']

        for marker, sync_type in zip(sync_markers, sync_types):
            if marker in log_content:
                return sync_type
        return ""

    def _extract_section_items(self, log_content: str, section_keyword: str) -> List[str]:
        """
        Extract bullet points from a section containing keyword.

        Args:
            log_content: Full log content
            section_keyword: Keyword identifying the section

        Returns:
            List of extracted items
        """
        items = []
        in_section = False
        lines = log_content.split('\n')

        for line in lines:
            # Detect section start
            if section_keyword in line:
                in_section = True
                continue

            # Detect section end (next header or blank line after items)
            if in_section:
                if line.startswith('#') or line.startswith('**'):
                    break
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    items.append(line.strip().lstrip('-*').strip())
                elif line.strip() == '' and items:
                    # Blank line after items indicates section end
                    break

        return items

    def update_daily_log(self,
                        sync_type: str,
                        actions: List[Any],
                        additional_context: Dict[str, Any]) -> bool:
        """
        Update _DAILY_LOG.md with new sync results.

        Args:
            sync_type: '9am', 'noon', '3pm', or 'eod'
            actions: List of Action objects from prioritization
            additional_context: Dict with metrics, changes, blockers

        Returns:
            True if update successful, False otherwise
        """
        try:
            log_content = self.read_daily_log()
            timestamp = datetime.now().strftime('%Y-%m-%d %I:%M %p')

            if sync_type == '9am':
                # Update morning priorities
                updated_content = self._update_morning_priorities(log_content, actions, timestamp)
            elif sync_type == 'noon':
                # Update noon check-in
                updated_content = self._update_noon_checkin(log_content, actions, timestamp, additional_context)
            elif sync_type == '3pm':
                # Update 3pm check-in
                updated_content = self._update_3pm_checkin(log_content, timestamp, additional_context)
            elif sync_type == 'eod':
                # Update EOD wrap
                updated_content = self._update_eod_wrap(log_content, timestamp, additional_context)
            else:
                print(f"⚠️ Unknown sync type: {sync_type}")
                return False

            # Write updated content
            with open(self.daily_log_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            return True

        except Exception as e:
            print(f"⚠️ Error updating daily log: {e}")
            return False

    def _update_morning_priorities(self, log_content: str, actions: List[Any], timestamp: str) -> str:
        """Update TODAY'S TOP 3 PRIORITIES section with new actions."""
        # Implementation placeholder - full logic would parse and replace section
        # For now, return content unchanged
        return log_content

    def _update_noon_checkin(self, log_content: str, actions: List[Any], timestamp: str, context: Dict[str, Any]) -> str:
        """Update NOON CHECK-IN section with progress."""
        # Implementation placeholder
        return log_content

    def _update_3pm_checkin(self, log_content: str, timestamp: str, context: Dict[str, Any]) -> str:
        """Update 3PM CHECK-IN section with afternoon progress."""
        # Implementation placeholder
        return log_content

    def _update_eod_wrap(self, log_content: str, timestamp: str, context: Dict[str, Any]) -> str:
        """Update END OF DAY WRAP section with completions and learnings."""
        # Implementation placeholder
        return log_content

    def create_new_daily_log(self, date: str, carryover_actions: List[Any] = None) -> bool:
        """
        Create new _DAILY_LOG.md from template.

        Args:
            date: Date string for new log
            carryover_actions: Actions to carry over from previous day

        Returns:
            True if creation successful, False otherwise
        """
        template_path = PROJECT_ROOT / ".claude/templates/DAILY_LOG_TEMPLATE.md"

        if not template_path.exists():
            print(f"⚠️ Template not found: {template_path}")
            return False

        try:
            # Read template
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()

            # Replace date placeholder
            day_of_week = datetime.now().strftime('%A')
            content = template.replace('{DATE}', date)
            content = content.replace('{DAY_OF_WEEK}', day_of_week)

            # Add carryover actions if provided
            if carryover_actions:
                carryover_section = "\n".join([f"- {action.title}" for action in carryover_actions])
                content = content.replace('### Carryover Actions\n_(High-priority items not completed yesterday)_\n\n-',
                                        f'### Carryover Actions\n_(High-priority items not completed yesterday)_\n\n{carryover_section}')

            # Write new log
            with open(self.daily_log_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✅ Created new daily log: {self.daily_log_path}")
            return True

        except Exception as e:
            print(f"⚠️ Error creating daily log: {e}")
            return False


def main():
    """Test function for continuity manager."""
    print("🧪 Testing ContinuityManager...")

    # Initialize
    manager = ContinuityManager()
    print(f"✅ Loaded config from {manager.config_path}")

    # Test validation
    print("\n📊 Testing log validation...")
    for sync_type in ['9am', 'noon', '3pm', 'eod']:
        passed, missing = manager.validate_log_for_sync(sync_type)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {sync_type}: {status}")
        if not passed:
            print(f"    Missing: {', '.join(missing)}")

    # Test context extraction
    print("\n📥 Testing context extraction...")
    context = manager.extract_context('noon')
    print(f"  Date: {context.date}")
    print(f"  Last sync: {context.last_sync_type}")
    print(f"  Completed: {len(context.completed_actions)} actions")
    print(f"  In progress: {len(context.in_progress_actions)} actions")
    print(f"  Blocked: {len(context.blocked_items)} items")

    print("\n✅ Testing complete!")


if __name__ == "__main__":
    main()
