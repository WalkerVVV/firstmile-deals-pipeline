"""
Nebuchadnezzar v3.0 - Conflict Detector
Advanced conflict detection and prevention for multi-agent operations
"""

import subprocess
import os
from typing import List, Dict, Tuple, Set
from pathlib import Path


class ConflictDetector:
    """
    Detects and prevents potential merge conflicts before they occur.

    Provides:
    - File-level conflict detection
    - Deal-level conflict detection
    - Auto-merge safety validation
    - Merge order recommendations
    """

    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()

    def detect_file_conflicts(self, branch1: str, branch2: str) -> Dict:
        """
        Check if two branches modify the same files.

        Args:
            branch1: First branch name
            branch2: Second branch name

        Returns:
            Dict with conflict information
        """
        # Get changed files in branch1
        result1 = subprocess.run(
            ['git', 'diff', '--name-only', 'main', branch1],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        files1 = set(f for f in result1.stdout.strip().split('\n') if f)

        # Get changed files in branch2
        result2 = subprocess.run(
            ['git', 'diff', '--name-only', 'main', branch2],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        files2 = set(f for f in result2.stdout.strip().split('\n') if f)

        # Find overlapping files
        conflicts = files1.intersection(files2)

        return {
            'has_conflicts': len(conflicts) > 0,
            'conflicting_files': sorted(list(conflicts)),
            'branch1_files': sorted(list(files1)),
            'branch2_files': sorted(list(files2)),
            'total_conflicts': len(conflicts),
            'conflict_severity': self._assess_severity(conflicts)
        }

    def detect_deal_conflicts(self, pending_branches: List[str]) -> List[Tuple[str, str]]:
        """
        Detect if multiple branches are working on the same deal.

        Args:
            pending_branches: List of branch names to check

        Returns:
            List of (branch1, branch2) tuples that conflict on same deal
        """
        deal_branches = {}
        conflicts = []

        for branch in pending_branches:
            if '/' not in branch:
                continue

            # Parse branch name: agent_type/deal_name_action
            agent_type, deal_action = branch.split('/', 1)

            # Extract deal name (first part before underscore)
            parts = deal_action.split('_')
            if not parts:
                continue

            deal_name = parts[0]

            if deal_name in deal_branches:
                # Conflict: multiple branches for same deal
                conflicts.append((deal_branches[deal_name], branch))
            else:
                deal_branches[deal_name] = branch

        return conflicts

    def can_auto_merge_group(self, branches: List[str]) -> Dict:
        """
        Determine if a group of branches can be safely auto-merged together.

        Args:
            branches: List of branch names to evaluate

        Returns:
            Dict with merge safety information and recommended order
        """
        # Check each pair for conflicts
        safe_to_merge = []
        unsafe_pairs = []
        file_conflicts = {}

        for i, branch1 in enumerate(branches):
            for branch2 in branches[i+1:]:
                conflict_info = self.detect_file_conflicts(branch1, branch2)

                if conflict_info['has_conflicts']:
                    unsafe_pairs.append((branch1, branch2))
                    file_conflicts[f"{branch1}+{branch2}"] = conflict_info['conflicting_files']
                else:
                    safe_to_merge.append((branch1, branch2))

        # Determine merge order recommendation
        merge_order = self._calculate_merge_order(branches, unsafe_pairs)

        all_safe = len(unsafe_pairs) == 0

        return {
            'all_safe_to_merge': all_safe,
            'safe_pairs': safe_to_merge,
            'unsafe_pairs': unsafe_pairs,
            'file_conflicts': file_conflicts,
            'recommended_merge_order': merge_order,
            'total_branches': len(branches),
            'conflict_count': len(unsafe_pairs)
        }

    def analyze_merge_complexity(self, branch_name: str) -> Dict:
        """
        Analyze complexity of merging a specific branch.

        Args:
            branch_name: Branch to analyze

        Returns:
            Dict with complexity metrics and safety recommendations
        """
        # Get diff stats
        result = subprocess.run(
            ['git', 'diff', '--shortstat', 'main', branch_name],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        diff_stat = result.stdout.strip()

        # Parse stats
        files_changed = 0
        insertions = 0
        deletions = 0

        if diff_stat:
            parts = diff_stat.split(',')
            for part in parts:
                if 'file' in part:
                    files_changed = int(part.split()[0])
                elif 'insertion' in part:
                    insertions = int(part.split()[0])
                elif 'deletion' in part:
                    deletions = int(part.split()[0])

        # Get list of changed files
        result2 = subprocess.run(
            ['git', 'diff', '--name-only', 'main', branch_name],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        changed_files = [f for f in result2.stdout.strip().split('\n') if f]

        # Check for risky file types
        risky_files = [
            f for f in changed_files
            if f.endswith(('.py', '.json', '.yml', '.yaml', '.env', '.config'))
        ]

        # Calculate complexity score
        complexity = self._calculate_complexity_score(
            files_changed,
            insertions,
            deletions,
            len(risky_files)
        )

        return {
            'branch_name': branch_name,
            'files_changed': files_changed,
            'insertions': insertions,
            'deletions': deletions,
            'risky_files': risky_files,
            'complexity_score': complexity,
            'auto_merge_safe': complexity < 0.5 and deletions == 0,
            'recommendation': self._get_merge_recommendation(complexity)
        }

    def get_merge_conflicts_preview(self, branch_name: str) -> Dict:
        """
        Preview what conflicts would occur if branch was merged now.

        Args:
            branch_name: Branch to preview merge for

        Returns:
            Dict with conflict preview information
        """
        # Try merge with --no-commit to preview
        result = subprocess.run(
            ['git', 'merge', '--no-commit', '--no-ff', branch_name],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        has_conflicts = result.returncode != 0

        # Get list of conflicting files
        conflicting_files = []
        if has_conflicts:
            status_result = subprocess.run(
                ['git', 'diff', '--name-only', '--diff-filter=U'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            conflicting_files = [f for f in status_result.stdout.strip().split('\n') if f]

        # Abort the test merge
        subprocess.run(
            ['git', 'merge', '--abort'],
            cwd=self.repo_path,
            capture_output=True
        )

        return {
            'branch_name': branch_name,
            'has_conflicts': has_conflicts,
            'conflicting_files': conflicting_files,
            'can_auto_merge': not has_conflicts,
            'conflict_count': len(conflicting_files)
        }

    def _assess_severity(self, conflicting_files: Set[str]) -> str:
        """Assess severity of file conflicts"""
        if not conflicting_files:
            return 'none'

        # Check for critical files
        critical_patterns = ['.py', '.json', '.yml', '.yaml', '.env']
        has_critical = any(
            any(f.endswith(pat) for pat in critical_patterns)
            for f in conflicting_files
        )

        if has_critical:
            return 'high'
        elif len(conflicting_files) > 5:
            return 'medium'
        else:
            return 'low'

    def _calculate_merge_order(self,
                               branches: List[str],
                               conflicts: List[Tuple[str, str]]) -> List[str]:
        """
        Calculate optimal merge order to minimize conflicts.

        Returns branches sorted by safest-to-merge-first.
        """
        if not conflicts:
            # No conflicts - any order is fine
            return branches

        # Count conflicts per branch
        conflict_counts = {branch: 0 for branch in branches}
        for branch1, branch2 in conflicts:
            conflict_counts[branch1] += 1
            conflict_counts[branch2] += 1

        # Sort by fewest conflicts first
        return sorted(branches, key=lambda b: conflict_counts.get(b, 0))

    def _calculate_complexity_score(self,
                                    files: int,
                                    insertions: int,
                                    deletions: int,
                                    risky_files: int) -> float:
        """
        Calculate merge complexity score (0.0 = simple, 1.0 = complex).
        """
        # Normalize each factor
        file_score = min(files / 10, 1.0) * 0.3
        insertion_score = min(insertions / 100, 1.0) * 0.2
        deletion_score = min(deletions / 50, 1.0) * 0.3
        risky_score = min(risky_files / 3, 1.0) * 0.2

        return file_score + insertion_score + deletion_score + risky_score

    def _get_merge_recommendation(self, complexity: float) -> str:
        """Get human-readable merge recommendation"""
        if complexity < 0.3:
            return "SAFE: Auto-merge recommended"
        elif complexity < 0.6:
            return "MODERATE: Review before merge"
        else:
            return "COMPLEX: Requires careful review"


def main():
    """Test conflict detector"""
    detector = ConflictDetector()

    # Get current branches
    result = subprocess.run(
        ['git', 'branch', '-a'],
        capture_output=True,
        text=True
    )

    branches = [
        b.strip().replace('* ', '').replace('remotes/origin/', '')
        for b in result.stdout.split('\n')
        if b.strip() and 'HEAD' not in b
    ]

    # Filter to only automation/* branches
    automation_branches = [b for b in branches if b.startswith('automation/')]

    print("Conflict Detector - Status Report")
    print("=" * 50)
    print(f"\nTotal automation branches: {len(automation_branches)}")

    if automation_branches:
        print("\nBranches:")
        for branch in automation_branches[:5]:  # Show first 5
            print(f"  - {branch}")

        # Check for deal conflicts
        if len(automation_branches) > 1:
            deal_conflicts = detector.detect_deal_conflicts(automation_branches)
            if deal_conflicts:
                print(f"\n⚠ Deal Conflicts Found: {len(deal_conflicts)}")
                for b1, b2 in deal_conflicts:
                    print(f"  - {b1} ↔ {b2}")
            else:
                print("\n✓ No deal conflicts detected")


if __name__ == "__main__":
    main()
