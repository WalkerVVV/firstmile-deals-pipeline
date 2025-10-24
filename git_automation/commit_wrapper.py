"""
Nebuchadnezzar v3.0 - Git Commit Wrapper
Provides automated Git operations for N8N workflows and automation agents
"""

import subprocess
import os
import json
from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path


class GitCommitWrapper:
    """
    Handles automated Git commits, branching, and merging
    for multi-agent pipeline operations
    """

    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getenv('FIRSTMILE_DEALS_PATH', r'C:\Users\BrettWalker\FirstMile_Deals')
        self.current_branch = self._get_current_branch()

    def _get_current_branch(self) -> str:
        """Get name of current Git branch"""
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()

    def create_branch(self, agent_type: str, deal_name: str, action: str) -> str:
        """
        Create new branch following naming convention

        Args:
            agent_type: One of 'automation', 'desktop', 'mobile', 'sync'
            deal_name: Company name (e.g., 'Caputron', 'OTW')
            action: Short action description (e.g., 'pld_analysis', 'followup')

        Returns:
            Branch name created
        """
        # Sanitize inputs
        deal_clean = deal_name.replace(' ', '_').replace("'", "").replace('"', '')
        action_clean = action.replace(' ', '_').lower()

        # Create branch name
        branch_name = f"{agent_type}/{deal_clean}_{action_clean}"

        # Ensure on main before creating branch
        subprocess.run(['git', 'checkout', 'main'], cwd=self.repo_path, capture_output=True)
        subprocess.run(['git', 'pull', 'origin', 'main'], cwd=self.repo_path, capture_output=True)

        # Create and checkout new branch
        subprocess.run(['git', 'checkout', '-b', branch_name], cwd=self.repo_path, capture_output=True)

        return branch_name

    def commit_changes(self,
                      deal_name: str,
                      agent_type: str,
                      action: str,
                      description: str,
                      files: Optional[List[str]] = None) -> Dict:
        """
        Stage and commit changes with standardized message format

        Args:
            deal_name: Company name
            agent_type: Agent type (automation, desktop, mobile, sync)
            action: Action type (ANALYSIS, PROPOSAL, NOTE, etc.)
            description: Detailed commit description
            files: Specific files to stage (None = stage all changes)

        Returns:
            Commit details dict
        """
        # Stage files
        if files:
            for file in files:
                subprocess.run(['git', 'add', file], cwd=self.repo_path, capture_output=True)
        else:
            subprocess.run(['git', 'add', '.'], cwd=self.repo_path, capture_output=True)

        # Create commit message
        commit_msg = f"[{agent_type.upper()}] [{deal_name}] [{action.upper()}]: {description}"

        # Commit
        result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        # Get commit hash
        commit_hash = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        ).stdout.strip()

        return {
            'commit_hash': commit_hash,
            'message': commit_msg,
            'timestamp': datetime.now().isoformat(),
            'files_changed': len(files) if files else 'all',
            'success': result.returncode == 0
        }

    def push_branch(self, branch_name: str = None) -> bool:
        """
        Push branch to remote GitHub repository

        Args:
            branch_name: Branch to push (None = current branch)

        Returns:
            Success boolean
        """
        branch = branch_name or self.current_branch

        result = subprocess.run(
            ['git', 'push', 'origin', branch],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        return result.returncode == 0

    def is_auto_mergeable(self, branch_name: str) -> bool:
        """
        Check if branch qualifies for automatic merge

        Auto-merge criteria:
        - Only additions, no deletions
        - Single file or markdown files only
        - No script or config changes
        - Simple text additions

        Returns:
            Boolean indicating auto-merge safety
        """
        # Get diff stats
        result = subprocess.run(
            ['git', 'diff', '--shortstat', 'main', branch_name],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        diff_stat = result.stdout.strip()

        # Check for deletions
        if 'deletion' in diff_stat.lower():
            return False

        # Get list of changed files
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'main', branch_name],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        changed_files = result.stdout.strip().split('\n')

        # More than 3 files = manual review
        if len(changed_files) > 3:
            return False

        # Any Python/config files = manual review
        unsafe_extensions = ['.py', '.json', '.yml', '.yaml', '.env']
        for file in changed_files:
            if any(file.endswith(ext) for ext in unsafe_extensions):
                return False

        return True

    def merge_to_main(self, branch_name: str, auto_merge: bool = False) -> Dict:
        """
        Merge branch to main

        Args:
            branch_name: Branch to merge
            auto_merge: If True, skip safety checks

        Returns:
            Merge result dict
        """
        # Safety check
        if not auto_merge and not self.is_auto_mergeable(branch_name):
            return {
                'success': False,
                'message': 'Branch requires manual review',
                'auto_mergeable': False
            }

        # Checkout main and pull latest
        subprocess.run(['git', 'checkout', 'main'], cwd=self.repo_path, capture_output=True)
        subprocess.run(['git', 'pull', 'origin', 'main'], cwd=self.repo_path, capture_output=True)

        # Merge with no-fast-forward (preserves branch history)
        result = subprocess.run(
            ['git', 'merge', '--no-ff', branch_name, '-m',
             f'Merge branch \'{branch_name}\' into main'],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                'success': False,
                'message': 'Merge conflict detected',
                'conflict': True,
                'details': result.stderr
            }

        # Push to remote
        push_success = self.push_branch('main')

        # Delete local branch
        subprocess.run(['git', 'branch', '-d', branch_name], cwd=self.repo_path, capture_output=True)

        return {
            'success': True,
            'message': f'Branch {branch_name} merged successfully',
            'pushed': push_success,
            'timestamp': datetime.now().isoformat()
        }


# Convenience functions for N8N integration
def quick_commit(deal_name: str, agent_type: str, action: str, description: str, files: List[str] = None):
    """
    One-shot commit operation for simple changes
    Creates branch → commits → pushes → returns branch name
    """
    wrapper = GitCommitWrapper()

    # Create branch
    branch_name = wrapper.create_branch(agent_type, deal_name, action)

    # Commit changes
    commit_result = wrapper.commit_changes(deal_name, agent_type, action, description, files)

    # Push to remote
    push_success = wrapper.push_branch(branch_name)

    return {
        'branch': branch_name,
        'commit': commit_result,
        'pushed': push_success,
        'auto_mergeable': wrapper.is_auto_mergeable(branch_name)
    }


if __name__ == "__main__":
    # Example usage and CLI interface
    import sys

    if len(sys.argv) < 5:
        print("Usage: python commit_wrapper.py <deal_name> <agent_type> <action> <description>")
        print("\nExample:")
        print('  python commit_wrapper.py "Caputron" automation pld_analysis "Completed overnight analysis"')
        sys.exit(1)

    deal = sys.argv[1]
    agent = sys.argv[2]
    action = sys.argv[3]
    desc = sys.argv[4]

    result = quick_commit(deal, agent, action, desc)
    print(json.dumps(result, indent=2))
