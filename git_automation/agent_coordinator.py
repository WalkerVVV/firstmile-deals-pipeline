"""
Nebuchadnezzar v3.0 - Agent Coordinator
Orchestrates multi-agent operations with conflict prevention
"""

import subprocess
import json
import os
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

try:
    from git_automation.commit_wrapper import GitCommitWrapper
    from git_automation.branch_manager import BranchManager
except ModuleNotFoundError:
    from commit_wrapper import GitCommitWrapper
    from branch_manager import BranchManager


class AgentCoordinator:
    """
    Coordinates multiple agents working on different deals simultaneously.

    Provides high-level orchestration with:
    - Automatic lock acquisition/release
    - Operation tracking
    - Conflict detection
    - Auto-merge decisioning
    """

    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        self.git_wrapper = GitCommitWrapper(self.repo_path)
        self.branch_manager = BranchManager(self.repo_path)
        self.active_operations = {}
        self.operation_log = []

    def start_operation(self,
                       deal_name: str,
                       agent_type: str,
                       action: str,
                       description: str,
                       timeout_minutes: int = 30) -> Dict:
        """
        Start new agent operation with automatic lock acquisition.

        Args:
            deal_name: Name of the deal (e.g., "Caputron", "Stackd")
            agent_type: Type of agent (automation/desktop/mobile/sync)
            action: Action being performed (e.g., "pld_analysis", "followup")
            description: Human-readable description of the operation
            timeout_minutes: Lock timeout in minutes (default: 30)

        Returns:
            Dict with operation status, ID, and branch name
        """
        # Try to acquire lock
        lock_result = self.branch_manager.acquire_lock(
            deal_name,
            agent_type,
            timeout_minutes=timeout_minutes
        )

        if not lock_result['success']:
            # Lock acquisition failed - another agent has the deal
            self.log_operation({
                'timestamp': datetime.now().isoformat(),
                'operation': 'start_failed',
                'deal_name': deal_name,
                'agent_type': agent_type,
                'reason': 'lock_conflict',
                'locked_by': lock_result.get('locked_by', 'unknown')
            })

            return {
                'success': False,
                'reason': 'lock_unavailable',
                'message': lock_result['message'],
                'locked_by': lock_result.get('locked_by', 'unknown'),
                'suggestion': f"Wait for {lock_result.get('locked_by')} to complete or timeout"
            }

        # Create branch for this operation
        try:
            branch_name = self.git_wrapper.create_branch(agent_type, deal_name, action)
        except Exception as e:
            # Branch creation failed - release lock and fail
            self.branch_manager.release_lock(deal_name, agent_type)
            return {
                'success': False,
                'reason': 'branch_creation_failed',
                'message': str(e)
            }

        # Register operation
        operation_id = f"{agent_type}_{deal_name}_{action}_{int(datetime.now().timestamp())}"
        self.active_operations[operation_id] = {
            'deal_name': deal_name,
            'agent_type': agent_type,
            'action': action,
            'description': description,
            'branch_name': branch_name,
            'started_at': datetime.now().isoformat(),
            'status': 'in_progress',
            'files_modified': [],
            'lock_timeout': timeout_minutes
        }

        self.log_operation({
            'timestamp': datetime.now().isoformat(),
            'operation': 'start_success',
            'operation_id': operation_id,
            'deal_name': deal_name,
            'agent_type': agent_type,
            'action': action,
            'branch_name': branch_name
        })

        return {
            'success': True,
            'operation_id': operation_id,
            'branch_name': branch_name,
            'lock_expires_in': timeout_minutes,
            'message': f"Operation started on branch {branch_name}"
        }

    def complete_operation(self,
                          operation_id: str,
                          files_changed: List[str],
                          commit_message: str,
                          auto_merge: bool = None) -> Dict:
        """
        Complete operation: commit changes, push, optionally auto-merge.

        Args:
            operation_id: ID returned from start_operation()
            files_changed: List of file paths that were modified
            commit_message: Commit message
            auto_merge: Force auto-merge decision (None = auto-detect)

        Returns:
            Dict with completion status and merge information
        """
        if operation_id not in self.active_operations:
            return {
                'success': False,
                'reason': 'operation_not_found',
                'message': f"Operation ID {operation_id} not found"
            }

        op = self.active_operations[operation_id]

        # Update operation status
        op['files_modified'] = files_changed
        op['status'] = 'committing'

        # Commit changes
        try:
            commit_result = self.git_wrapper.commit_changes(
                op['branch_name'],
                commit_message
            )

            if not commit_result['success']:
                op['status'] = 'commit_failed'
                return {
                    'success': False,
                    'reason': 'commit_failed',
                    'message': commit_result.get('error', 'Commit failed')
                }

        except Exception as e:
            op['status'] = 'commit_failed'
            return {
                'success': False,
                'reason': 'commit_exception',
                'message': str(e)
            }

        op['status'] = 'committed'

        # Determine if auto-merge is safe
        if auto_merge is None:
            auto_merge = self.git_wrapper.is_auto_mergeable(op['branch_name'])

        merge_result = None
        if auto_merge:
            # Attempt auto-merge
            try:
                merge_result = self.git_wrapper.merge_to_main(op['branch_name'])
                if merge_result['success']:
                    op['status'] = 'merged'
                    op['merged_at'] = datetime.now().isoformat()
                else:
                    op['status'] = 'merge_failed'
            except Exception as e:
                op['status'] = 'merge_failed'
                merge_result = {'success': False, 'error': str(e)}
        else:
            op['status'] = 'awaiting_review'
            merge_result = {
                'success': False,
                'reason': 'manual_review_required',
                'message': 'Branch requires manual review before merge'
            }

        # Release lock
        self.branch_manager.release_lock(op['deal_name'], op['agent_type'])

        # Mark operation complete
        op['completed_at'] = datetime.now().isoformat()

        self.log_operation({
            'timestamp': datetime.now().isoformat(),
            'operation': 'complete',
            'operation_id': operation_id,
            'deal_name': op['deal_name'],
            'agent_type': op['agent_type'],
            'status': op['status'],
            'auto_merged': auto_merge and merge_result.get('success', False),
            'files_count': len(files_changed)
        })

        return {
            'success': True,
            'operation_id': operation_id,
            'branch_name': op['branch_name'],
            'status': op['status'],
            'auto_merged': auto_merge and merge_result.get('success', False),
            'merge_result': merge_result,
            'lock_released': True,
            'message': f"Operation completed: {op['status']}"
        }

    def cancel_operation(self, operation_id: str, reason: str = "cancelled") -> Dict:
        """
        Cancel an in-progress operation and release lock.

        Args:
            operation_id: ID of operation to cancel
            reason: Reason for cancellation

        Returns:
            Dict with cancellation status
        """
        if operation_id not in self.active_operations:
            return {
                'success': False,
                'message': 'Operation not found'
            }

        op = self.active_operations[operation_id]

        # Delete branch if it exists
        try:
            subprocess.run(
                ['git', 'branch', '-D', op['branch_name']],
                cwd=self.repo_path,
                capture_output=True
            )
        except Exception:
            pass  # Branch might not exist yet

        # Release lock
        self.branch_manager.release_lock(op['deal_name'], op['agent_type'])

        # Mark cancelled
        op['status'] = 'cancelled'
        op['cancelled_at'] = datetime.now().isoformat()
        op['cancel_reason'] = reason

        self.log_operation({
            'timestamp': datetime.now().isoformat(),
            'operation': 'cancelled',
            'operation_id': operation_id,
            'deal_name': op['deal_name'],
            'agent_type': op['agent_type'],
            'reason': reason
        })

        return {
            'success': True,
            'operation_id': operation_id,
            'message': f"Operation cancelled: {reason}"
        }

    def get_active_operations(self) -> List[Dict]:
        """Get list of all active operations"""
        return [
            {
                'operation_id': op_id,
                **op_data
            }
            for op_id, op_data in self.active_operations.items()
            if op_data['status'] in ['in_progress', 'committing']
        ]

    def get_operation_status(self, operation_id: str) -> Optional[Dict]:
        """Get status of specific operation"""
        if operation_id in self.active_operations:
            return {
                'operation_id': operation_id,
                **self.active_operations[operation_id]
            }
        return None

    def log_operation(self, log_entry: Dict):
        """Log operation for debugging and audit trail"""
        self.operation_log.append(log_entry)

        # Keep last 1000 entries
        if len(self.operation_log) > 1000:
            self.operation_log = self.operation_log[-1000:]

    def get_operation_log(self, limit: int = 50) -> List[Dict]:
        """Get recent operation log entries"""
        return self.operation_log[-limit:]

    def get_coordination_stats(self) -> Dict:
        """Get statistics about agent coordination"""
        total_ops = len(self.operation_log)

        # Count by status
        by_status = {}
        for log in self.operation_log:
            status = log.get('operation', 'unknown')
            by_status[status] = by_status.get(status, 0) + 1

        # Count by agent type
        by_agent = {}
        for log in self.operation_log:
            agent = log.get('agent_type', 'unknown')
            by_agent[agent] = by_agent.get(agent, 0) + 1

        # Count active operations
        active = len([
            op for op in self.active_operations.values()
            if op['status'] in ['in_progress', 'committing']
        ])

        return {
            'total_operations_logged': total_ops,
            'active_operations': active,
            'operations_by_status': by_status,
            'operations_by_agent': by_agent,
            'last_updated': datetime.now().isoformat()
        }


def main():
    """Test agent coordinator"""
    coordinator = AgentCoordinator()

    # Display coordination stats
    stats = coordinator.get_coordination_stats()
    print("Agent Coordination Statistics:")
    print(f"  Total Operations: {stats['total_operations_logged']}")
    print(f"  Active Operations: {stats['active_operations']}")

    if stats['operations_by_agent']:
        print("\n  Operations by Agent:")
        for agent, count in stats['operations_by_agent'].items():
            print(f"    {agent}: {count}")


if __name__ == "__main__":
    main()
