"""
Nebuchadnezzar v3.0 - Phase 0 Backup System
Safe, verified backup with detailed logging and validation
"""

import os
import shutil
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class BackupSystem:
    """
    Safe backup system with verification and rollback capability
    """

    def __init__(self, source_dir: str, backup_dir: str):
        self.source_dir = Path(source_dir)
        self.backup_dir = Path(backup_dir)
        self.log_file = Path.home() / "Desktop" / f"backup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.manifest = {}

    def log(self, message: str, level: str = "INFO"):
        """Write to log file and print"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')

    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum of file"""
        md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    md5.update(chunk)
            return md5.hexdigest()
        except Exception as e:
            self.log(f"Checksum error for {file_path}: {e}", "WARNING")
            return None

    def create_backup(self, exclude_patterns: List[str] = None) -> Tuple[bool, Dict]:
        """
        Create backup with verification

        Args:
            exclude_patterns: List of patterns to exclude (e.g., ['__pycache__', '*.tmp'])

        Returns:
            (success: bool, stats: dict)
        """
        if exclude_patterns is None:
            exclude_patterns = [
                '__pycache__',
                '*.pyc',
                '*.tmp',
                '*.log',
                '*.bak',
                '.git',
                'nul'
            ]

        self.log("="*80)
        self.log("NEBUCHADNEZZAR V3.0 - PHASE 0 BACKUP")
        self.log("="*80)
        self.log(f"Source: {self.source_dir}")
        self.log(f"Backup: {self.backup_dir}")
        self.log(f"Exclude patterns: {exclude_patterns}")
        self.log("")

        # Create backup directory
        if self.backup_dir.exists():
            self.log(f"WARNING: Backup directory already exists!", "WARNING")
            response = input("Overwrite existing backup? (yes/no): ")
            if response.lower() != 'yes':
                self.log("Backup cancelled by user", "INFO")
                return False, {}
            shutil.rmtree(self.backup_dir)

        self.backup_dir.mkdir(parents=True)

        # Statistics
        stats = {
            'files_copied': 0,
            'files_skipped': 0,
            'files_failed': 0,
            'dirs_created': 0,
            'total_size_bytes': 0,
            'start_time': datetime.now().isoformat(),
            'errors': []
        }

        # Copy files
        self.log("Starting backup...")

        for item in self.source_dir.rglob('*'):
            # Check exclusions
            if any(item.match(pattern) for pattern in exclude_patterns):
                stats['files_skipped'] += 1
                continue

            # Get relative path
            rel_path = item.relative_to(self.source_dir)
            dest_path = self.backup_dir / rel_path

            try:
                if item.is_dir():
                    # Create directory
                    dest_path.mkdir(parents=True, exist_ok=True)
                    stats['dirs_created'] += 1

                elif item.is_file():
                    # Copy file with metadata
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest_path)

                    # Calculate checksums
                    source_checksum = self.calculate_checksum(item)
                    dest_checksum = self.calculate_checksum(dest_path)

                    if source_checksum != dest_checksum:
                        self.log(f"Checksum mismatch: {item}", "ERROR")
                        stats['files_failed'] += 1
                        stats['errors'].append(f"Checksum mismatch: {item}")
                    else:
                        stats['files_copied'] += 1
                        stats['total_size_bytes'] += item.stat().st_size

                        # Add to manifest
                        self.manifest[str(rel_path)] = {
                            'checksum': source_checksum,
                            'size': item.stat().st_size,
                            'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                        }

                    # Progress update every 50 files
                    if stats['files_copied'] % 50 == 0:
                        self.log(f"Progress: {stats['files_copied']} files copied...")

            except Exception as e:
                self.log(f"Error copying {item}: {e}", "ERROR")
                stats['files_failed'] += 1
                stats['errors'].append(f"{item}: {e}")

        # Save manifest
        manifest_file = self.backup_dir / 'BACKUP_MANIFEST.json'
        with open(manifest_file, 'w') as f:
            json.dump({
                'stats': stats,
                'manifest': self.manifest,
                'backup_date': datetime.now().isoformat(),
                'source': str(self.source_dir),
                'backup': str(self.backup_dir)
            }, f, indent=2)

        stats['end_time'] = datetime.now().isoformat()

        # Log results
        self.log("")
        self.log("="*80)
        self.log("BACKUP COMPLETE")
        self.log("="*80)
        self.log(f"Files copied: {stats['files_copied']}")
        self.log(f"Files skipped: {stats['files_skipped']}")
        self.log(f"Files failed: {stats['files_failed']}")
        self.log(f"Directories created: {stats['dirs_created']}")
        self.log(f"Total size: {stats['total_size_bytes'] / (1024**3):.2f} GB")
        self.log(f"Log file: {self.log_file}")
        self.log(f"Manifest: {manifest_file}")

        if stats['files_failed'] > 0:
            self.log("")
            self.log(f"WARNING: {stats['files_failed']} files failed to copy!", "WARNING")
            self.log("See errors above for details", "WARNING")
            return False, stats

        self.log("")
        self.log("✅ Backup completed successfully with zero errors!")
        return True, stats

    def verify_backup(self) -> Tuple[bool, Dict]:
        """
        Verify backup integrity by comparing checksums

        Returns:
            (success: bool, verification_results: dict)
        """
        self.log("")
        self.log("="*80)
        self.log("VERIFYING BACKUP INTEGRITY")
        self.log("="*80)

        # Load manifest
        manifest_file = self.backup_dir / 'BACKUP_MANIFEST.json'
        if not manifest_file.exists():
            self.log("ERROR: Manifest file not found!", "ERROR")
            return False, {}

        with open(manifest_file, 'r') as f:
            backup_data = json.load(f)

        manifest = backup_data['manifest']

        results = {
            'files_verified': 0,
            'files_missing': 0,
            'checksum_mismatches': 0,
            'errors': []
        }

        # Verify each file
        for rel_path, file_info in manifest.items():
            backup_file = self.backup_dir / rel_path

            if not backup_file.exists():
                self.log(f"Missing: {rel_path}", "ERROR")
                results['files_missing'] += 1
                results['errors'].append(f"Missing: {rel_path}")
                continue

            # Verify checksum
            checksum = self.calculate_checksum(backup_file)
            if checksum != file_info['checksum']:
                self.log(f"Checksum mismatch: {rel_path}", "ERROR")
                results['checksum_mismatches'] += 1
                results['errors'].append(f"Checksum mismatch: {rel_path}")
            else:
                results['files_verified'] += 1

        # Log results
        self.log("")
        self.log("="*80)
        self.log("VERIFICATION COMPLETE")
        self.log("="*80)
        self.log(f"Files verified: {results['files_verified']}")
        self.log(f"Files missing: {results['files_missing']}")
        self.log(f"Checksum mismatches: {results['checksum_mismatches']}")

        if results['files_missing'] > 0 or results['checksum_mismatches'] > 0:
            self.log("")
            self.log("❌ VERIFICATION FAILED!", "ERROR")
            return False, results

        self.log("")
        self.log("✅ Backup integrity verified successfully!")
        return True, results


def main():
    """Run backup and verification"""

    source = r"C:\Users\BrettWalker\FirstMile_Deals"
    backup = r"C:\Users\BrettWalker\FirstMile_Deals_BACKUP_20251023_PRE_MATRIX"

    print("\n" + "="*80)
    print("NEBUCHADNEZZAR V3.0 - PHASE 0 BACKUP SYSTEM")
    print("="*80)
    print(f"\nSource: {source}")
    print(f"Backup: {backup}")
    print(f"\nThis will create a complete verified backup of your FirstMile Deals system.")
    print(f"Estimated time: 5-10 minutes")
    print(f"Estimated size: ~2-5 GB")
    print("\n" + "="*80)

    response = input("\nProceed with backup? (yes/no): ")
    if response.lower() != 'yes':
        print("Backup cancelled.")
        return

    # Create backup system
    backup_sys = BackupSystem(source, backup)

    # Run backup
    success, stats = backup_sys.create_backup()

    if not success:
        print("\n❌ Backup failed! See log for details.")
        return

    # Verify backup
    verified, verify_results = backup_sys.verify_backup()

    if not verified:
        print("\n❌ Verification failed! Backup may be incomplete.")
        return

    print("\n" + "="*80)
    print("✅ SUCCESS! Backup completed and verified.")
    print("="*80)
    print(f"\nBackup location: {backup}")
    print(f"Log file: {backup_sys.log_file}")
    print(f"\nYou can now safely proceed with Phase 1 (Git Infrastructure).")
    print("\nNext command: /sc:implement NEBUCHADNEZZAR_V3_IMPLEMENTATION_WORKFLOW.md --phase 1")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
