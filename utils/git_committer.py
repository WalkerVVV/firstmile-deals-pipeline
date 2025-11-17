#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git auto-commit system for FirstMile sync operations.

This module provides intelligent git commit automation for EOD syncs,
generating descriptive commit messages with daily summaries.

Author: Claude Code
Created: 2025-11-17
"""

import sys
import io
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

# NOTE: UTF-8 encoding wrapper is handled by calling script (unified_sync.py)
# Do not apply wrapper here to avoid conflicts

# Absolute paths
PROJECT_ROOT = Path("C:/Users/BrettWalker/FirstMile_Deals")


@dataclass
class CommitSummary:
    """
    Represents a daily commit summary.

    Attributes:
        date: Commit date (YYYY-MM-DD)
        sync_count: Number of syncs completed today
        actions_completed: Count of completed actions
        deals_updated: Count of deals with activity
        emails_processed: Count of emails reviewed
        files_modified: List of modified files
        key_activities: List of major activities/completions
    """
    date: str
    sync_count: int
    actions_completed: int
    deals_updated: int
    emails_processed: int
    files_modified: List[str]
    key_activities: List[str]


class GitCommitter:
    """
    Intelligent git commit automation for daily sync operations.

    Generates descriptive commit messages with daily summaries,
    handles staging of sync reports and daily log updates.
    """

    def __init__(self, project_root: Path = PROJECT_ROOT):
        """
        Initialize git committer.

        Args:
            project_root: Path to project root directory
        """
        self.project_root = project_root

    def check_git_available(self) -> bool:
        """
        Check if git is available and repository initialized.

        Returns:
            True if git is available, False otherwise
        """
        try:
            result = subprocess.run(
                ['git', '--version'],
                cwd=self.project_root,
                capture_output=True,
                encoding='utf-8',
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            print(f"⚠️ Git not available: {e}")
            return False

    def get_git_status(self) -> Dict[str, List[str]]:
        """
        Get current git status (modified, untracked files).

        Returns:
            Dict with 'modified', 'untracked', 'staged' lists
        """
        if not self.check_git_available():
            return {'modified': [], 'untracked': [], 'staged': []}

        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.project_root,
                capture_output=True,
                encoding='utf-8',
                timeout=10
            )

            if result.returncode != 0:
                print(f"⚠️ Git status failed: {result.stderr}")
                return {'modified': [], 'untracked': [], 'staged': []}

            # Parse git status output
            modified = []
            untracked = []
            staged = []

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue

                status = line[:2]
                filename = line[3:].strip()

                if status[0] in ['M', 'A', 'D', 'R', 'C']:
                    staged.append(filename)
                elif status[1] == 'M':
                    modified.append(filename)
                elif status == '??':
                    untracked.append(filename)

            return {
                'modified': modified,
                'untracked': untracked,
                'staged': staged
            }

        except Exception as e:
            print(f"⚠️ Error getting git status: {e}")
            return {'modified': [], 'untracked': [], 'staged': []}

    def stage_sync_files(self) -> bool:
        """
        Stage sync-related files for commit.

        Stages:
        - sync_reports/ directory
        - _DAILY_LOG.md
        - FOLLOW_UP_REMINDERS.txt

        Returns:
            True if staging successful, False otherwise
        """
        if not self.check_git_available():
            return False

        files_to_stage = [
            'sync_reports/',
            '_DAILY_LOG.md',
            'FOLLOW_UP_REMINDERS.txt'
        ]

        try:
            for file_path in files_to_stage:
                full_path = self.project_root / file_path
                if full_path.exists():
                    result = subprocess.run(
                        ['git', 'add', file_path],
                        cwd=self.project_root,
                        capture_output=True,
                        encoding='utf-8',
                        timeout=10
                    )

                    if result.returncode != 0:
                        print(f"⚠️ Failed to stage {file_path}: {result.stderr}")
                        return False

            return True

        except Exception as e:
            print(f"⚠️ Error staging files: {e}")
            return False

    def generate_commit_message(self, summary: CommitSummary) -> str:
        """
        Generate descriptive commit message from daily summary.

        Args:
            summary: CommitSummary with daily activity data

        Returns:
            Formatted commit message
        """
        date_str = datetime.strptime(summary.date, '%Y-%m-%d').strftime('%b %d, %Y')

        # Header with emoji
        message = f"eod: {date_str} daily sync\n\n"

        # Summary statistics
        message += f"Daily Summary:\n"
        message += f"- {summary.sync_count} sync operations (9AM/NOON/3PM/EOD)\n"
        message += f"- {summary.actions_completed} actions completed\n"
        message += f"- {summary.deals_updated} deals with activity\n"
        message += f"- {summary.emails_processed} emails processed\n\n"

        # Key activities
        if summary.key_activities:
            message += f"Key Activities:\n"
            for activity in summary.key_activities:
                message += f"- {activity}\n"
            message += "\n"

        # Files modified
        if summary.files_modified:
            message += f"Modified Files:\n"
            for file in summary.files_modified[:5]:  # Limit to top 5
                message += f"- {file}\n"
            if len(summary.files_modified) > 5:
                message += f"- ... and {len(summary.files_modified) - 5} more\n"

        return message.strip()

    def create_commit(self, summary: CommitSummary) -> bool:
        """
        Create git commit with daily summary.

        Args:
            summary: CommitSummary with daily activity data

        Returns:
            True if commit successful, False otherwise
        """
        if not self.check_git_available():
            print("⚠️ Git not available, skipping commit")
            return False

        # Stage files
        if not self.stage_sync_files():
            print("⚠️ Failed to stage files, skipping commit")
            return False

        # Check if there's anything to commit
        status = self.get_git_status()
        if not status['staged']:
            print("ℹ️ No changes to commit")
            return True

        # Generate commit message
        commit_message = self.generate_commit_message(summary)

        try:
            # Create commit
            result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=self.project_root,
                capture_output=True,
                encoding='utf-8',
                timeout=30
            )

            if result.returncode != 0:
                print(f"⚠️ Commit failed: {result.stderr}")
                return False

            print(f"✅ Created commit: {summary.date}")
            print(f"   Files committed: {len(status['staged'])}")
            return True

        except Exception as e:
            print(f"⚠️ Error creating commit: {e}")
            return False

    def extract_summary_from_sync_data(self,
                                      sync_reports: List[str],
                                      actions: List[Any],
                                      continuity_context: Any) -> CommitSummary:
        """
        Extract commit summary from sync data.

        Args:
            sync_reports: List of sync report filenames from today
            actions: List of Action objects processed today
            continuity_context: ContinuityContext from continuity manager

        Returns:
            CommitSummary object
        """
        date = datetime.now().strftime('%Y-%m-%d')

        # Count syncs (based on report files)
        sync_count = len(sync_reports)

        # Count completed actions from continuity context
        actions_completed = len(continuity_context.completed_actions) if hasattr(continuity_context, 'completed_actions') else 0

        # Count deals and emails from actions
        deals_updated = sum(1 for action in actions if hasattr(action, 'type') and action.type == 'deal')
        emails_processed = sum(1 for action in actions if hasattr(action, 'type') and action.type == 'email')

        # Get modified files from git status
        status = self.get_git_status()
        files_modified = status['modified'] + status['untracked']

        # Extract key activities from completed actions
        key_activities = []
        if hasattr(continuity_context, 'completed_actions'):
            key_activities = continuity_context.completed_actions[:5]  # Top 5

        return CommitSummary(
            date=date,
            sync_count=sync_count,
            actions_completed=actions_completed,
            deals_updated=deals_updated,
            emails_processed=emails_processed,
            files_modified=files_modified,
            key_activities=key_activities
        )


def main():
    """Test function for git committer."""
    print("🧪 Testing GitCommitter...")

    # Initialize
    committer = GitCommitter()

    # Check git availability
    if committer.check_git_available():
        print("✅ Git is available")
    else:
        print("❌ Git not available")
        return

    # Get git status
    print("\n📊 Git Status:")
    status = committer.get_git_status()
    print(f"  Modified: {len(status['modified'])} files")
    print(f"  Untracked: {len(status['untracked'])} files")
    print(f"  Staged: {len(status['staged'])} files")

    # Test commit message generation
    print("\n📝 Testing commit message generation...")
    test_summary = CommitSummary(
        date=datetime.now().strftime('%Y-%m-%d'),
        sync_count=4,
        actions_completed=8,
        deals_updated=3,
        emails_processed=12,
        files_modified=['_DAILY_LOG.md', 'sync_reports/EOD_SYNC_20251117.md'],
        key_activities=[
            'Completed BoxiiShip rate analysis',
            'Updated System Beauty TX proposal',
            'Responded to Lindsey email'
        ]
    )

    commit_msg = committer.generate_commit_message(test_summary)
    print("\nGenerated commit message:")
    print("=" * 60)
    print(commit_msg)
    print("=" * 60)

    print("\n✅ Testing complete!")
    print("\nℹ️ To create actual commit, call committer.create_commit(summary)")


if __name__ == "__main__":
    main()
