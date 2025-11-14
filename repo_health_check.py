#!/usr/bin/env python3
"""
Nebuchadnezzar v3.0 Repository Health Check
============================================
Comprehensive health check for FirstMile Deals Pipeline repository.
Checks code quality, dependencies, configuration, and system status.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import importlib.util


class HealthCheck:
    """Repository health check analyzer"""
    
    def __init__(self):
        self.repo_root = Path(__file__).parent
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'status': 'HEALTHY',
            'checks': [],
            'warnings': [],
            'errors': [],
            'stats': {}
        }
    
    def check_structure(self) -> bool:
        """Verify critical directory structure"""
        print("🔍 Checking repository structure...")
        
        critical_dirs = [
            '.claude',
            'HubSpot',
            'BULK_RATE_PROCESSING',
            'XPARCEL_NATIONAL_SELECT',
            '.github/workflows'
        ]
        
        missing_dirs = []
        for dir_name in critical_dirs:
            dir_path = self.repo_root / dir_name
            if dir_path.exists():
                print(f"  ✅ {dir_name}")
            else:
                print(f"  ❌ MISSING: {dir_name}")
                missing_dirs.append(dir_name)
                self.results['errors'].append(f"Missing critical directory: {dir_name}")
        
        if missing_dirs:
            self.results['status'] = 'UNHEALTHY'
            return False
        
        self.results['checks'].append('Repository structure verified')
        return True
    
    def check_files(self) -> bool:
        """Verify critical configuration files"""
        print("\n📋 Checking critical files...")
        
        critical_files = [
            '.gitignore',
            '.env.example',
            'CLAUDE.md',
            'requirements.txt',
            '.claude/README.md',
            '.claude/DOCUMENTATION_INDEX.md',
            '.claude/NEBUCHADNEZZAR_REFERENCE.md'
        ]
        
        missing_files = []
        for file_name in critical_files:
            file_path = self.repo_root / file_name
            if file_path.exists():
                print(f"  ✅ {file_name}")
            else:
                print(f"  ❌ MISSING: {file_name}")
                missing_files.append(file_name)
                self.results['errors'].append(f"Missing critical file: {file_name}")
        
        if missing_files:
            self.results['status'] = 'UNHEALTHY'
            return False
        
        self.results['checks'].append('Critical files verified')
        return True
    
    def check_security(self) -> bool:
        """Check for security issues"""
        print("\n🔒 Checking security...")
        
        # Check if .env is NOT in repo
        env_file = self.repo_root / '.env'
        if env_file.exists():
            print("  ❌ CRITICAL: .env file found in repository!")
            self.results['errors'].append("SECURITY RISK: .env file in repository")
            self.results['status'] = 'UNHEALTHY'
            return False
        else:
            print("  ✅ .env file properly excluded")
        
        # Check for hardcoded credentials in Python files
        print("  🔍 Scanning for hardcoded credentials...")
        suspicious_patterns = ['api_key =', 'password =', 'secret =', 'token =']
        issues_found = False
        
        for py_file in self.repo_root.glob('**/*.py'):
            # Skip excluded directories
            if self._should_exclude_path(py_file):
                continue
            
            try:
                content = py_file.read_text()
                for pattern in suspicious_patterns:
                    if pattern in content and 'config.py' not in str(py_file) and 'hubspot_config.py' not in str(py_file):
                        # Check if it's actually hardcoded (not loading from env)
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if pattern in line and 'os.getenv' not in line and 'Config.' not in line:
                                if self._should_check_credential_line(line):
                                    print(f"  ⚠️  Potential hardcoded credential in {py_file.name}:{i+1}")
                                    self.results['warnings'].append(f"Check {py_file.name}:{i+1} for hardcoded credential")
                                    issues_found = True
            except Exception:
                pass
        
        if not issues_found:
            print("  ✅ No hardcoded credentials detected")
        
        self.results['checks'].append('Security scan completed')
        return True
    
    def _should_exclude_path(self, path: Path) -> bool:
        """Check if path should be excluded from scanning"""
        path_str = str(path)
        return '.git' in path_str or 'venv' in path_str
    
    def _should_check_credential_line(self, line: str) -> bool:
        """Check if line should be flagged for potential credential"""
        # Skip comments, regex patterns, and documentation
        if line.strip().startswith('#'):
            return False
        if any(keyword in line.lower() for keyword in ['pattern', 'regex']):
            return False
        if 'r"' in line or "r'" in line:
            return False
        return True
    
    def _calculate_repo_size(self) -> str:
        """Calculate repository size in a cross-platform way"""
        # Try Unix du command first (faster)
        try:
            result = subprocess.run(['du', '-sh', str(self.repo_root)], 
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.split()[0]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # Fallback to cross-platform Python calculation
        try:
            total_size = sum(f.stat().st_size for f in self.repo_root.rglob('*') if f.is_file())
            # Convert to human-readable format
            for unit in ['B', 'K', 'M', 'G', 'T']:
                if total_size < 1024.0:
                    return f"{total_size:.0f}{unit}"
                total_size /= 1024.0
            return f"{total_size:.0f}P"
        except Exception:
            return "Unknown"
    
    def check_python_syntax(self) -> bool:
        """Check Python syntax of key files"""
        print("\n🐍 Checking Python syntax...")
        
        key_files = [
            'config.py',
            'hubspot_config.py',
            'hubspot_utils.py',
            'date_utils.py',
            'daily_9am_sync.py',
            'noon_sync.py',
            'eod_sync.py',
            'pipeline_sync_verification.py'
        ]
        
        syntax_errors = []
        for file_name in key_files:
            file_path = self.repo_root / file_name
            if not file_path.exists():
                continue
            
            try:
                # Try to compile the file
                with open(file_path, 'r') as f:
                    compile(f.read(), file_path, 'exec')
                print(f"  ✅ {file_name}")
            except SyntaxError as e:
                print(f"  ❌ SYNTAX ERROR in {file_name}: {e}")
                syntax_errors.append(file_name)
                self.results['errors'].append(f"Syntax error in {file_name}: {e}")
        
        if syntax_errors:
            self.results['status'] = 'UNHEALTHY'
            return False
        
        self.results['checks'].append('Python syntax validated')
        return True
    
    def check_imports(self) -> bool:
        """Check if core modules can be imported"""
        print("\n📦 Checking core module imports...")
        
        core_modules = [
            'config',
            'hubspot_config',
            'hubspot_utils',
            'date_utils'
        ]
        
        import_errors = []
        for module_name in core_modules:
            module_path = self.repo_root / f"{module_name}.py"
            if not module_path.exists():
                continue
            
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    print(f"  ✅ {module_name}")
            except Exception as e:
                print(f"  ⚠️  {module_name}: {str(e)[:60]}...")
                import_errors.append((module_name, str(e)))
                # Don't mark as error if it's just missing .env (expected)
                if '.env' not in str(e).lower() and 'configuration' not in str(e).lower():
                    self.results['warnings'].append(f"Import issue in {module_name}: {e}")
        
        self.results['checks'].append('Core modules import check completed')
        return True
    
    def check_dependencies(self) -> bool:
        """Check Python dependencies"""
        print("\n📚 Checking dependencies...")
        
        req_file = self.repo_root / 'requirements.txt'
        if not req_file.exists():
            print("  ⚠️  requirements.txt not found")
            self.results['warnings'].append("requirements.txt not found")
            return True
        
        requirements = req_file.read_text().split('\n')
        requirements = [r.strip() for r in requirements if r.strip() and not r.startswith('#')]
        
        print(f"  📦 Found {len(requirements)} dependencies")
        
        # Try to check installed packages
        try:
            import pandas
            print(f"  ✅ pandas {pandas.__version__}")
        except ImportError:
            print("  ⚠️  pandas not installed")
            self.results['warnings'].append("pandas not installed")
        
        try:
            import numpy
            print(f"  ✅ numpy {numpy.__version__}")
        except ImportError:
            print("  ⚠️  numpy not installed")
            self.results['warnings'].append("numpy not installed")
        
        try:
            import openpyxl
            print(f"  ✅ openpyxl {openpyxl.__version__}")
        except ImportError:
            print("  ⚠️  openpyxl not installed")
            self.results['warnings'].append("openpyxl not installed")
        
        try:
            import requests
            print(f"  ✅ requests {requests.__version__}")
        except ImportError:
            print("  ⚠️  requests not installed")
            self.results['warnings'].append("requests not installed")
        
        self.results['checks'].append('Dependencies checked')
        return True
    
    def gather_stats(self) -> None:
        """Gather repository statistics"""
        print("\n📊 Gathering statistics...")
        
        # Count Python files
        py_files = list(self.repo_root.glob('**/*.py'))
        py_files = [f for f in py_files if '.git' not in str(f) and 'venv' not in str(f)]
        self.results['stats']['python_files'] = len(py_files)
        print(f"  📝 Python files: {len(py_files)}")
        
        # Count markdown files
        md_files = list(self.repo_root.glob('**/*.md'))
        md_files = [f for f in md_files if '.git' not in str(f)]
        self.results['stats']['markdown_files'] = len(md_files)
        print(f"  📄 Markdown files: {len(md_files)}")
        
        # Count deal folders
        deal_folders = [d for d in self.repo_root.iterdir() if d.is_dir() and d.name.startswith('[')]
        self.results['stats']['deal_folders'] = len(deal_folders)
        print(f"  📁 Deal folders: {len(deal_folders)}")
        
        # Get repository size
        try:
            size = self._calculate_repo_size()
            if size:
                self.results['stats']['repo_size'] = size
                print(f"  💾 Repository size: {size}")
        except Exception:
            pass
        
        # Get git status
        try:
            os.chdir(self.repo_root)
            result = subprocess.run(['git', 'status', '--short'], 
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
                self.results['stats']['uncommitted_changes'] = uncommitted
                if uncommitted > 0:
                    print(f"  ⚠️  Uncommitted changes: {uncommitted}")
                else:
                    print(f"  ✅ No uncommitted changes")
        except Exception:
            pass
        
        # Get last commit
        try:
            result = subprocess.run(['git', 'log', '-1', '--format=%h - %s (%cr)'], 
                                    capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.results['stats']['last_commit'] = result.stdout.strip()
                print(f"  🔖 Last commit: {result.stdout.strip()}")
        except Exception:
            pass
    
    def generate_report(self) -> str:
        """Generate final health report"""
        print("\n" + "="*70)
        print("📊 NEBUCHADNEZZAR v3.0 HEALTH CHECK REPORT")
        print("="*70)
        print(f"Timestamp: {self.results['timestamp']}")
        print(f"Status: {self.results['status']}")
        print()
        
        print("✅ Checks Passed:")
        for check in self.results['checks']:
            print(f"  - {check}")
        print()
        
        if self.results['warnings']:
            print("⚠️  Warnings:")
            for warning in self.results['warnings']:
                print(f"  - {warning}")
            print()
        
        if self.results['errors']:
            print("❌ Errors:")
            for error in self.results['errors']:
                print(f"  - {error}")
            print()
        
        print("📊 Statistics:")
        for key, value in self.results['stats'].items():
            print(f"  - {key.replace('_', ' ').title()}: {value}")
        print()
        
        # Overall health score
        total_checks = len(self.results['checks'])
        warnings = len(self.results['warnings'])
        errors = len(self.results['errors'])
        
        if errors == 0 and warnings == 0:
            health_score = 100
            health_status = "EXCELLENT ✨"
        elif errors == 0 and warnings <= 3:
            health_score = 90
            health_status = "GOOD ✅"
        elif errors == 0:
            health_score = 75
            health_status = "FAIR ⚠️"
        else:
            health_score = 50
            health_status = "NEEDS ATTENTION ❌"
        
        print(f"🎯 Overall Health Score: {health_score}/100 - {health_status}")
        print("="*70)
        
        return json.dumps(self.results, indent=2)
    
    def run(self) -> bool:
        """Run all health checks"""
        print("🚀 Starting Nebuchadnezzar v3.0 Health Check...\n")
        
        checks = [
            self.check_structure,
            self.check_files,
            self.check_security,
            self.check_python_syntax,
            self.check_imports,
            self.check_dependencies
        ]
        
        for check in checks:
            try:
                check()
            except Exception as e:
                print(f"\n❌ Check failed with error: {e}")
                self.results['errors'].append(f"Check failed: {e}")
                self.results['status'] = 'UNHEALTHY'
        
        self.gather_stats()
        report = self.generate_report()
        
        # Save report
        report_file = self.repo_root / 'HEALTH_CHECK_REPORT.json'
        report_file.write_text(report)
        print(f"\n💾 Report saved to: {report_file}")
        
        return self.results['status'] == 'HEALTHY'


def main():
    """Main entry point"""
    checker = HealthCheck()
    is_healthy = checker.run()
    
    # Exit with appropriate code
    sys.exit(0 if is_healthy else 1)


if __name__ == '__main__':
    main()
