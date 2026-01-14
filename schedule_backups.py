#!/usr/bin/env python3
"""
Backup Scheduler
Schedule automated backups at specific intervals
"""

import schedule
import time
import subprocess
from datetime import datetime

def run_backup():
    """Execute the backup script"""
    print(f"\n{'='*60}")
    print(f"Scheduled Backup Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            ['python3', 'backup_script.py'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Failed to run backup: {e}")

def main():
    """Schedule backups"""
    print("="*60)
    print("Network Backup Scheduler")
    print("="*60)
    print("\nScheduled backups:")
    print("  - Daily at 2:00 AM")
    print("  - Every 6 hours")
    print("\nPress Ctrl+C to stop the scheduler")
    print("="*60)
    
    # Schedule daily backup at 2 AM
    schedule.every().day.at("02:00").do(run_backup)
    
    # Schedule backup every 6 hours
    schedule.every(6).hours.do(run_backup)
    
    # Run once immediately for testing
    print("\nRunning initial backup...")
    run_backup()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user")
