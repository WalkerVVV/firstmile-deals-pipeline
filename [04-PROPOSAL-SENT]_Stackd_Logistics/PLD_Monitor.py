import os
import time
from datetime import datetime
import shutil

# Stackd Logistics PLD Monitor
# Created: September 18, 2025
# Purpose: Watch for Landon's PLD file and auto-process

WATCH_FOLDERS = [
    r"C:\Users\BrettWalker\Downloads",
    r"C:\Users\BrettWalker\Desktop",
    r"C:\Users\BrettWalker\OneDrive\Desktop"
]

TARGET_FOLDER = r"C:\Users\BrettWalker\FirstMile_Deals\[02-DISCOVERY-COMPLETE]_Stackd_Logistics"
KEYWORDS = ["stackd", "landon", "richards", "pld", "shiphero", "30 day", "30-day"]

print("=" * 60)
print("STACKD LOGISTICS PLD MONITOR")
print("Watching for Landon's 30-day shipping data...")
print("=" * 60)
print(f"Started: {datetime.now().strftime('%I:%M %p')}")
print(f"Monitoring folders:")
for folder in WATCH_FOLDERS:
    print(f"  - {folder}")
print("\nLooking for files containing:", ", ".join(KEYWORDS))
print("\nPress Ctrl+C to stop monitoring")
print("-" * 60)

found_files = set()

while True:
    try:
        for folder in WATCH_FOLDERS:
            if not os.path.exists(folder):
                continue
            
            for filename in os.listdir(folder):
                # Skip if we've already found this file
                if filename in found_files:
                    continue
                
                # Check if filename matches any keyword
                filename_lower = filename.lower()
                if any(keyword in filename_lower for keyword in KEYWORDS):
                    # Check if it's a data file
                    if filename.endswith(('.xlsx', '.xls', '.csv', '.zip', '.txt')):
                        full_path = os.path.join(folder, filename)
                        file_size = os.path.getsize(full_path) / 1024 / 1024  # MB
                        
                        print(f"\n🎯 FOUND POTENTIAL PLD FILE!")
                        print(f"   File: {filename}")
                        print(f"   Size: {file_size:.2f} MB")
                        print(f"   Location: {folder}")
                        print(f"   Time: {datetime.now().strftime('%I:%M %p')}")
                        
                        # Copy to deal folder
                        dest_path = os.path.join(TARGET_FOLDER, filename)
                        shutil.copy2(full_path, dest_path)
                        print(f"   ✅ Copied to: {TARGET_FOLDER}")
                        
                        # Mark as found
                        found_files.add(filename)
                        
                        # Create processing script
                        process_script = f'''
# STACKD LOGISTICS PROCESSING SCRIPT
# File: {filename}
# Received: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}

import pandas as pd
import sys
sys.path.append(r'C:\\Users\\BrettWalker\\Desktop\\shipping_analysis')
from firstmile_universal_analyzer import UniversalAnalyzer

# Load and process
analyzer = UniversalAnalyzer()
results = analyzer.process_file(r"{dest_path}")

# Generate proposal
print("Generating Stackd Logistics proposal...")
# Add proposal generation code here

print("\\n✅ READY FOR IN-PERSON DELIVERY!")
'''
                        
                        script_path = os.path.join(TARGET_FOLDER, "process_stackd_pld.py")
                        with open(script_path, 'w') as f:
                            f.write(process_script)
                        
                        print(f"   ✅ Processing script created")
                        print(f"\n🚀 ACTION REQUIRED:")
                        print(f"   1. Run: python \"{script_path}\"")
                        print(f"   2. Submit to pricing team")
                        print(f"   3. Prepare for IN-PERSON delivery!")
                        print("-" * 60)
        
        # Check every 10 seconds
        time.sleep(10)
        
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)

print(f"Ended: {datetime.now().strftime('%I:%M %p')}")
