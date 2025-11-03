"""
Nebuchadnezzar v3.0 - Phase 0 Automated Backup
Non-interactive version for automated execution
"""

import os
import shutil
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


def log_message(message: str, log_file: Path):
    """Write to log file and print"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry + '\n')


def calculate_checksum(file_path: Path) -> str:
    """Calculate MD5 checksum of file"""
    md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception:
        return None


def create_backup():
    """Execute backup with verification"""

    source_dir = Path(r"C:\Users\BrettWalker\FirstMile_Deals")
    backup_dir = Path(r"C:\Users\BrettWalker\FirstMile_Deals_BACKUP_20251023_PRE_MATRIX")
    log_file = Path.home() / "Desktop" / f"backup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    exclude_patterns = ['__pycache__', '*.pyc', '*.tmp', '*.log', '*.bak', '.git', 'nul']

    log_message("="*80, log_file)
    log_message("NEBUCHADNEZZAR V3.0 - PHASE 0 AUTOMATED BACKUP", log_file)
    log_message("="*80, log_file)
    log_message(f"Source: {source_dir}", log_file)
    log_message(f"Backup: {backup_dir}", log_file)
    log_message("", log_file)

    # Create backup directory
    if backup_dir.exists():
        log_message("Removing existing backup directory...", log_file)
        shutil.rmtree(backup_dir)

    backup_dir.mkdir(parents=True)

    # Statistics
    stats = {
        'files_copied': 0,
        'files_skipped': 0,
        'files_failed': 0,
        'dirs_created': 0,
        'total_size_bytes': 0,
        'errors': []
    }

    manifest = {}

    log_message("Starting backup...", log_file)

    # Copy files
    for item in source_dir.rglob('*'):
        # Check exclusions
        if any(item.match(pattern) for pattern in exclude_patterns):
            stats['files_skipped'] += 1
            continue

        rel_path = item.relative_to(source_dir)
        dest_path = backup_dir / rel_path

        try:
            if item.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
                stats['dirs_created'] += 1

            elif item.is_file():
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)

                # Verify checksums
                source_checksum = calculate_checksum(item)
                dest_checksum = calculate_checksum(dest_path)

                if source_checksum == dest_checksum:
                    stats['files_copied'] += 1
                    stats['total_size_bytes'] += item.stat().st_size

                    manifest[str(rel_path)] = {
                        'checksum': source_checksum,
                        'size': item.stat().st_size
                    }
                else:
                    stats['files_failed'] += 1
                    stats['errors'].append(f"Checksum mismatch: {item}")

                # Progress update
                if stats['files_copied'] % 50 == 0:
                    log_message(f"Progress: {stats['files_copied']} files copied...", log_file)

        except Exception as e:
            stats['files_failed'] += 1
            stats['errors'].append(f"{item}: {e}")

    # Save manifest
    manifest_file = backup_dir / 'BACKUP_MANIFEST.json'
    with open(manifest_file, 'w') as f:
        json.dump({
            'stats': stats,
            'manifest': manifest,
            'backup_date': datetime.now().isoformat(),
            'source': str(source_dir),
            'backup': str(backup_dir)
        }, f, indent=2)

    # Log results
    log_message("", log_file)
    log_message("="*80, log_file)
    log_message("BACKUP COMPLETE", log_file)
    log_message("="*80, log_file)
    log_message(f"Files copied: {stats['files_copied']}", log_file)
    log_message(f"Files skipped: {stats['files_skipped']}", log_file)
    log_message(f"Files failed: {stats['files_failed']}", log_file)
    log_message(f"Directories created: {stats['dirs_created']}", log_file)
    log_message(f"Total size: {stats['total_size_bytes'] / (1024**3):.2f} GB", log_file)
    log_message(f"Log file: {log_file}", log_file)

    if stats['files_failed'] > 0:
        log_message(f"WARNING: {stats['files_failed']} files failed!", log_file)
        return False

    log_message("✅ Backup completed successfully!", log_file)
    return True


if __name__ == "__main__":
    success = create_backup()
    exit(0 if success else 1)
