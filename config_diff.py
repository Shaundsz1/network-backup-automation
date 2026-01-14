#!/usr/bin/env python3
"""
Configuration Diff Tool
Compares current config with previous backup
"""

import os
import difflib
from datetime import datetime
import glob

def find_latest_backup(device_name, backup_dir="backups"):
    """Find the most recent backup for a device"""
    pattern = f"{backup_dir}/*/{device_name}_*.txt"
    backups = glob.glob(pattern)
    
    if not backups:
        return None
    
    # Sort by modification time, most recent first
    backups.sort(key=os.path.getmtime, reverse=True)
    return backups

def compare_configs(device_name):
    """Compare the two most recent backups"""
    backups = find_latest_backup(device_name)
    
    if not backups:
        print(f"No backups found for {device_name}")
        return
    
    if len(backups) < 2:
        print(f"Only one backup exists for {device_name}. Need at least 2 to compare.")
        return
    
    current_backup = backups[0]
    previous_backup = backups[1]
    
    print(f"\nComparing:")
    print(f"  Current:  {current_backup}")
    print(f"  Previous: {previous_backup}")
    print("="*80)
    
    # Read both files
    with open(current_backup, 'r') as f:
        current_lines = f.readlines()
    
    with open(previous_backup, 'r') as f:
        previous_lines = f.readlines()
    
    # Generate diff
    diff = difflib.unified_diff(
        previous_lines,
        current_lines,
        fromfile=f'Previous ({os.path.basename(previous_backup)})',
        tofile=f'Current ({os.path.basename(current_backup)})',
        lineterm=''
    )
    
    # Display differences
    changes_found = False
    for line in diff:
        changes_found = True
        if line.startswith('+'):
            print(f"\033[92m{line}\033[0m")  # Green for additions
        elif line.startswith('-'):
            print(f"\033[91m{line}\033[0m")  # Red for removals
        elif line.startswith('@@'):
            print(f"\033[94m{line}\033[0m")  # Blue for location markers
        else:
            print(line)
    
    if not changes_found:
        print("\n✓ No differences found - configurations are identical!")
    
    print("="*80)

def main():
    """Main function"""
    print("="*80)
    print("Configuration Diff Tool")
    print("="*80)
    
    device_name = input("\nEnter device name (e.g., Cat8k-Sandbox): ").strip()
    
    if not device_name:
        print("Device name required!")
        return
    
    compare_configs(device_name)

if __name__ == "__main__":
    main()
