#!/usr/bin/env python3
"""
Batch update remaining scripts to use secure environment variable pattern
"""

import os
import re

# Files remaining to update
remaining_files = [
    "create_morning_tasks_oct27.py",
    "create_tasks_with_env.py",
    "fix_boxiiship_correct_structure.py",
    "get_pipeline_stages.py",
    "get_task_details.py",
    "mark_boxiiship_winback.py",
    "add_winback_note.py",
    "update_boxiiship_winback.py",
    "update_team_shipper.py",
    "[CUSTOMER]_Driftaway_Coffee/update_hubspot_winback.py",
    "[CUSTOMER]_Driftaway_Coffee/update_hubspot_winback_v2.py"
]

def update_file(filepath):
    """Update a file to use secure environment variable pattern"""
    if not os.path.exists(filepath):
        print(f"  ⚠️  File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already updated
    if 'load_dotenv()' in content:
        print(f"  ✓ Already secured: {filepath}")
        return True

    # Pattern 1: API_KEY = 'pat-na1-...'
    pattern1 = r"API_KEY = ['\"]pat-na1-[a-zA-Z0-9-]+['\"]"
    # Pattern 2: api_key = "pat-na1-..."
    pattern2 = r"api_key = ['\"]pat-na1-[a-zA-Z0-9-]+['\"]"

    if not (re.search(pattern1, content) or re.search(pattern2, content)):
        print(f"  ⚠️  No hardcoded API_KEY found: {filepath}")
        return False

    # Find where to insert the secure imports
    # Look for existing import statements
    import_match = re.search(r'^import\s+', content, re.MULTILINE)
    if not import_match:
        print(f"  ❌ Could not find import section: {filepath}")
        return False

    # Check if 'os' import exists, if not add it
    if 'import os' not in content and 'from os import' not in content:
        content = re.sub(r'(^import\s+)', r'import os\n\1', content, count=1, flags=re.MULTILINE)

    # Check if 'sys' import exists
    has_sys = 'import sys' in content or 'from sys import' in content

    # Add dotenv import after existing imports
    if 'from dotenv import load_dotenv' not in content:
        # Find last import line
        import_lines = [i for i, line in enumerate(content.split('\n')) if line.strip().startswith(('import ', 'from '))]
        if import_lines:
            lines = content.split('\n')
            last_import_idx = import_lines[-1]
            lines.insert(last_import_idx + 1, 'from dotenv import load_dotenv')
            content = '\n'.join(lines)

    # Add load_dotenv() call and API_KEY loading before the hardcoded API_KEY line
    secure_code = """
# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment (SECURE)
API_KEY = os.environ.get('HUBSPOT_API_KEY')
if not API_KEY:
    print("\\n❌ ERROR: HUBSPOT_API_KEY not found in environment")
    print("   Please check .env file contains: HUBSPOT_API_KEY=pat-na1-...")
    sys.exit(1)
"""

    # If sys not imported, add it
    if not has_sys:
        secure_code = secure_code.replace('sys.exit(1)', 'raise SystemExit(1)')

    # Replace the hardcoded API_KEY line
    content = re.sub(pattern1, secure_code.strip(), content, count=1)
    content = re.sub(pattern2, secure_code.strip(), content, count=1)

    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"  ✅ Updated: {filepath}")
    return True

def main():
    print("\n" + "="*80)
    print("BATCH CREDENTIAL SECURITY UPDATE")
    print("="*80 + "\n")

    updated = 0
    skipped = 0
    failed = 0

    for filepath in remaining_files:
        result = update_file(filepath)
        if result:
            updated += 1
        elif result is None:
            skipped += 1
        else:
            failed += 1

    print("\n" + "="*80)
    print(f"✅ Updated: {updated}")
    print(f"⚠️  Skipped/Already done: {skipped}")
    print(f"❌ Failed: {failed}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
