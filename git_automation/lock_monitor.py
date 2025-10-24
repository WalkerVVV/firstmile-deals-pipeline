"""
Nebuchadnezzar v3.0 - Agent Lock Monitor
Real-time monitoring dashboard for multi-agent lock coordination
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class LockMonitor:
    """Real-time monitoring of agent locks with HTML dashboard generation"""

    def __init__(self, locks_dir: str = None, repo_path: str = None):
        self.repo_path = repo_path or os.getcwd()
        self.locks_dir = Path(self.repo_path) / ".git" / "agent_locks"

    def get_active_locks(self) -> List[Dict]:
        """Get all currently active locks with expiration status"""
        locks = []

        if not self.locks_dir.exists():
            return locks

        for lock_file in self.locks_dir.glob("*.lock"):
            try:
                with open(lock_file, 'r') as f:
                    lock_data = json.load(f)

                # Check if expired
                expires_at = datetime.fromisoformat(lock_data['expires_at'])
                is_expired = datetime.now() > expires_at

                # Calculate time remaining
                time_remaining = expires_at - datetime.now()
                minutes_remaining = int(time_remaining.total_seconds() / 60)

                locks.append({
                    **lock_data,
                    'is_expired': is_expired,
                    'minutes_remaining': max(0, minutes_remaining),
                    'lock_file': lock_file.name,
                    'lock_path': str(lock_file)
                })
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                # Skip corrupted lock files
                print(f"Warning: Skipping corrupted lock file {lock_file}: {e}")
                continue

        return sorted(locks, key=lambda x: x['locked_at'], reverse=True)

    def get_lock_statistics(self) -> Dict:
        """Get summary statistics for agent locks"""
        locks = self.get_active_locks()

        total = len(locks)
        active = sum(1 for lock in locks if not lock['is_expired'])
        expired = total - active

        # Count by agent type
        by_agent = {}
        for lock in locks:
            agent = lock['agent_type']
            if agent not in by_agent:
                by_agent[agent] = {'total': 0, 'active': 0, 'expired': 0}
            by_agent[agent]['total'] += 1
            if lock['is_expired']:
                by_agent[agent]['expired'] += 1
            else:
                by_agent[agent]['active'] += 1

        return {
            'total_locks': total,
            'active_locks': active,
            'expired_locks': expired,
            'by_agent_type': by_agent,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def cleanup_expired_locks(self) -> int:
        """Remove expired lock files"""
        locks = self.get_active_locks()
        removed_count = 0

        for lock in locks:
            if lock['is_expired']:
                try:
                    Path(lock['lock_path']).unlink()
                    removed_count += 1
                except Exception as e:
                    print(f"Error removing lock file {lock['lock_file']}: {e}")

        return removed_count

    def generate_dashboard_html(self, output_path: str = None) -> str:
        """Generate HTML dashboard of active locks"""
        locks = self.get_active_locks()
        stats = self.get_lock_statistics()

        if output_path is None:
            output_path = os.path.join(
                os.path.expanduser('~'),
                'Desktop',
                'AGENT_LOCK_MONITOR.html'
            )

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Nebuchadnezzar v3.0 - Agent Lock Monitor</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="10">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 30px;
        }}

        header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }}

        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}

        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .stat-label {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }}

        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }}

        .agent-summary {{
            background: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #ffc107;
        }}

        .locks-section {{
            margin-top: 20px;
        }}

        .section-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #eee;
        }}

        .lock {{
            background: white;
            border: 2px solid #ddd;
            padding: 20px;
            margin: 15px 0;
            border-radius: 8px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .lock:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}

        .lock.expired {{
            background: #ffebee;
            border-color: #ef5350;
            opacity: 0.7;
        }}

        .lock.active {{
            background: #e8f5e9;
            border-color: #66bb6a;
        }}

        .lock.warning {{
            background: #fff3e0;
            border-color: #ffa726;
        }}

        .lock-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .deal-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }}

        .status-badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
            text-transform: uppercase;
        }}

        .status-badge.active {{
            background: #66bb6a;
            color: white;
        }}

        .status-badge.expired {{
            background: #ef5350;
            color: white;
        }}

        .status-badge.warning {{
            background: #ffa726;
            color: white;
        }}

        .lock-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            color: #666;
            font-size: 0.95em;
        }}

        .detail-item {{
            padding: 8px 0;
        }}

        .detail-label {{
            font-weight: bold;
            color: #444;
        }}

        .agent-badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 5px;
        }}

        .agent-automation {{
            background: #667eea;
            color: white;
        }}

        .agent-desktop {{
            background: #48bb78;
            color: white;
        }}

        .agent-mobile {{
            background: #ed8936;
            color: white;
        }}

        .agent-sync {{
            background: #9f7aea;
            color: white;
        }}

        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }}

        .empty-state-icon {{
            font-size: 4em;
            margin-bottom: 20px;
        }}

        .refresh-info {{
            text-align: center;
            color: #999;
            font-size: 0.9em;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔒 Agent Lock Monitor</h1>
            <div class="subtitle">Nebuchadnezzar v3.0 Matrix Edition</div>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">Total Locks</div>
                <div class="stat-value">{stats['total_locks']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Active Locks</div>
                <div class="stat-value" style="color: #66bb6a;">{stats['active_locks']}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Expired Locks</div>
                <div class="stat-value" style="color: #ef5350;">{stats['expired_locks']}</div>
            </div>
        </div>
"""

        # Agent type summary
        if stats['by_agent_type']:
            html += '<div class="agent-summary">\n'
            html += '<div class="stat-label">Locks by Agent Type:</div>\n'
            for agent_type, counts in stats['by_agent_type'].items():
                html += f'<div style="margin-top: 10px;">\n'
                html += f'<span class="agent-badge agent-{agent_type}">{agent_type.upper()}</span> '
                html += f'Active: <strong>{counts["active"]}</strong> | '
                html += f'Expired: <strong>{counts["expired"]}</strong> | '
                html += f'Total: <strong>{counts["total"]}</strong>\n'
                html += '</div>\n'
            html += '</div>\n'

        html += '<div class="locks-section">\n'

        if not locks:
            html += """
            <div class="empty-state">
                <div class="empty-state-icon">🎉</div>
                <div style="font-size: 1.5em; margin-bottom: 10px;">No Active Locks</div>
                <div>All deals are available for editing</div>
            </div>
            """
        else:
            html += '<h2 class="section-title">Current Locks ({} total)</h2>\n'.format(len(locks))

            for lock in locks:
                # Determine lock status class
                if lock['is_expired']:
                    status_class = 'expired'
                    status_text = 'EXPIRED'
                elif lock['minutes_remaining'] <= 5:
                    status_class = 'warning'
                    status_text = f'EXPIRING ({lock["minutes_remaining"]}m)'
                else:
                    status_class = 'active'
                    status_text = f'ACTIVE ({lock["minutes_remaining"]}m)'

                html += f'<div class="lock {status_class}">\n'
                html += '<div class="lock-header">\n'
                html += f'<div class="deal-name">{lock["deal_name"]}</div>\n'
                html += f'<div class="status-badge {status_class}">{status_text}</div>\n'
                html += '</div>\n'

                html += '<div class="lock-details">\n'
                html += '<div class="detail-item">\n'
                html += '<span class="detail-label">Agent:</span>\n'
                html += f'<span class="agent-badge agent-{lock["agent_type"]}">{lock["agent_type"].upper()}</span>\n'
                html += '</div>\n'

                html += '<div class="detail-item">\n'
                html += '<span class="detail-label">Locked At:</span> '
                html += f'{lock["locked_at"]}\n'
                html += '</div>\n'

                html += '<div class="detail-item">\n'
                html += '<span class="detail-label">Expires At:</span> '
                html += f'{lock["expires_at"]}\n'
                html += '</div>\n'

                html += '<div class="detail-item">\n'
                html += '<span class="detail-label">PID:</span> '
                html += f'{lock.get("pid", "N/A")}\n'
                html += '</div>\n'

                html += '</div>\n'  # lock-details
                html += '</div>\n'  # lock

        html += '</div>\n'  # locks-section

        html += f"""
        <div class="refresh-info">
            Last Updated: {stats['last_updated']}<br>
            Auto-refreshes every 10 seconds
        </div>
    </div>
</body>
</html>
"""

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_path


def main():
    """Generate lock monitor dashboard"""
    monitor = LockMonitor()

    # Cleanup expired locks first
    removed = monitor.cleanup_expired_locks()
    if removed > 0:
        print(f"Cleaned up {removed} expired lock(s)")

    # Generate dashboard
    output_path = monitor.generate_dashboard_html()
    print(f"Lock monitor dashboard generated: {output_path}")

    # Print summary
    stats = monitor.get_lock_statistics()
    print(f"\nCurrent Status:")
    print(f"  Active Locks: {stats['active_locks']}")
    print(f"  Expired Locks: {stats['expired_locks']}")
    print(f"  Total Locks: {stats['total_locks']}")


if __name__ == "__main__":
    main()
