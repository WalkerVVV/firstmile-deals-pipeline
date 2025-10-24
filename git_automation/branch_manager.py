"""
Branch lifecycle management and conflict prevention
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple


class BranchManager:
    """
    Manages branch lifecycle, locks, and conflict prevention
    """

    def __init__(self, repo_path: str = None):
        self.repo_path = repo_path or os.getenv('FIRSTMILE_DEALS_PATH', r'C:\Users\BrettWalker\FirstMile_Deals')
        self.locks_dir = Path(self.repo_path) / '.git' / 'agent_locks'
        self.locks_dir.mkdir(exist_ok=True)

    def acquire_lock(self, deal_name: str, agent_type: str, timeout_minutes: int = 30) -> Dict:
        """
        Acquire exclusive lock on a deal folder
        Prevents multiple agents from working on same deal simultaneously
        """
        lock_file = self.locks_dir / f"{deal_name}.lock"

        # Check if lock exists and is still valid
        if lock_file.exists():
            with open(lock_file, 'r') as f:
                lock_data = json.load(f)

            locked_at = datetime.fromisoformat(lock_data['locked_at'])
            expires_at = datetime.fromisoformat(lock_data['expires_at'])

            if datetime.now() < expires_at:
                # Lock is still valid
                return {
                    'success': False,
                    'locked_by': lock_data['agent_type'],
                    'locked_at': lock_data['locked_at'],
                    'expires_at': lock_data['expires_at'],
                    'message': f"Deal {deal_name} locked by {lock_data['agent_type']}"
                }
            else:
                # Lock expired, remove it
                lock_file.unlink()

        # Create new lock
        lock_data = {
            'deal_name': deal_name,
            'agent_type': agent_type,
            'locked_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(minutes=timeout_minutes)).isoformat(),
            'pid': os.getpid()
        }

        with open(lock_file, 'w') as f:
            json.dump(lock_data, f, indent=2)

        return {
            'success': True,
            'lock_file': str(lock_file),
            'expires_in_minutes': timeout_minutes
        }

    def release_lock(self, deal_name: str) -> bool:
        """Release lock on deal folder"""
        lock_file = self.locks_dir / f"{deal_name}.lock"

        if lock_file.exists():
            lock_file.unlink()
            return True

        return False

    def get_active_branches(self) -> List[Dict]:
        """
        Get list of all active branches by type
        """
        result = subprocess.run(
            ['git', 'branch', '-a'],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        branches = []
        for line in result.stdout.split('\n'):
            line = line.strip('* ').strip()
            if line and not line.startswith('remotes/'):
                # Parse branch name
                if '/' in line:
                    agent_type, deal_action = line.split('/', 1)
                    branches.append({
                        'name': line,
                        'agent_type': agent_type,
                        'deal_action': deal_action
                    })

        return branches

    def cleanup_stale_branches(self, days_old: int = 30) -> List[str]:
        """
        Remove merged branches older than specified days
        Returns list of deleted branch names
        """
        result = subprocess.run(
            ['git', 'branch', '--merged', 'main'],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )

        merged_branches = [b.strip() for b in result.stdout.split('\n') if b.strip() and b.strip() != 'main']
        deleted_branches = []

        for branch in merged_branches:
            # Get branch age
            result = subprocess.run(
                ['git', 'log', '-1', '--format=%ci', branch],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                last_commit_date = result.stdout.strip()
                # Parse date and check age
                branch_date = datetime.fromisoformat(last_commit_date.replace(' +', '+'))
                age_days = (datetime.now() - branch_date.replace(tzinfo=None)).days

                if age_days > days_old:
                    # Delete branch
                    subprocess.run(['git', 'branch', '-d', branch], cwd=self.repo_path, capture_output=True)
                    deleted_branches.append(branch)

        return deleted_branches

    def get_lock_status(self) -> List[Dict]:
        """Get all active locks and their status"""
        locks = []

        if not self.locks_dir.exists():
            return locks

        for lock_file in self.locks_dir.glob("*.lock"):
            try:
                with open(lock_file, 'r') as f:
                    lock_data = json.load(f)

                expires_at = datetime.fromisoformat(lock_data['expires_at'])
                is_expired = datetime.now() > expires_at

                locks.append({
                    **lock_data,
                    'is_expired': is_expired,
                    'lock_file': lock_file.name
                })
            except Exception as e:
                # Corrupted lock file, skip
                continue

        return locks


if __name__ == "__main__":
    import sys

    manager = BranchManager()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "acquire":
            if len(sys.argv) < 4:
                print("Usage: python branch_manager.py acquire <deal_name> <agent_type> [timeout_minutes]")
                sys.exit(1)

            deal = sys.argv[2]
            agent = sys.argv[3]
            timeout = int(sys.argv[4]) if len(sys.argv) > 4 else 30

            result = manager.acquire_lock(deal, agent, timeout)
            print(json.dumps(result, indent=2))

        elif command == "release":
            if len(sys.argv) < 3:
                print("Usage: python branch_manager.py release <deal_name>")
                sys.exit(1)

            deal = sys.argv[2]
            success = manager.release_lock(deal)
            print(json.dumps({'success': success, 'deal_name': deal}, indent=2))

        elif command == "list":
            branches = manager.get_active_branches()
            print(json.dumps(branches, indent=2))

        elif command == "cleanup":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            deleted = manager.cleanup_stale_branches(days)
            print(f"Deleted {len(deleted)} stale branches (>{days} days old)")
            print(json.dumps(deleted, indent=2))

        elif command == "locks":
            locks = manager.get_lock_status()
            print(json.dumps(locks, indent=2))

        else:
            print(f"Unknown command: {command}")
            print("Available commands: acquire, release, list, cleanup, locks")

    else:
        # Example usage
        print("Branch Manager - Example usage:")
        print("\nAcquire lock:")
        print('  python branch_manager.py acquire "Caputron" automation 60')
        print("\nRelease lock:")
        print('  python branch_manager.py release "Caputron"')
        print("\nList branches:")
        print('  python branch_manager.py list')
        print("\nCleanup old branches:")
        print('  python branch_manager.py cleanup 30')
        print("\nShow lock status:")
        print('  python branch_manager.py locks')
