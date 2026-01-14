#!/usr/bin/env python3
"""
Professional Network Device Configuration Backup Script
Features: Multi-device support, logging, timestamped backups, email notifications
"""

import yaml
from netmiko import ConnectHandler
from datetime import datetime
import os
import logging
import argparse

# Import email module if available
try:
    from email_notification import send_email_report, load_email_config
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False

# Set up logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_file = f"{log_dir}/backup_{datetime.now().strftime('%Y-%m-%d')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def load_devices(inventory_file):
    """Load device inventory from YAML file"""
    try:
        with open(inventory_file, 'r') as file:
            data = yaml.safe_load(file)
            return data['devices']
    except FileNotFoundError:
        logging.error(f"Inventory file {inventory_file} not found!")
        return []
    except Exception as e:
        logging.error(f"Failed to load inventory: {e}")
        return []

def backup_device(device, output_dir="backups"):
    """Connect to device and backup configuration"""
    device_name = device.pop('device_name', device['host'])
    
    try:
        logging.info(f"Connecting to {device_name}...")
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Connecting to {device_name}...")
        
        # Connect to device
        connection = ConnectHandler(**device)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Connected! Retrieving configuration...")
        logging.info(f"Successfully connected to {device_name}")
        
        # Get running configuration
        config = connection.send_command('show running-config')
        
        # Get additional info for documentation
        hostname = connection.send_command('show version | include hostname')
        
        # Create backup directory structure
        today = datetime.now().strftime('%Y-%m-%d')
        backup_dir = f"{output_dir}/{today}"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%H-%M-%S')
        filename = f"{backup_dir}/{device_name}_{timestamp}.txt"
        
        # Save configuration with header
        with open(filename, 'w') as backup_file:
            backup_file.write(f"! Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            backup_file.write(f"! Device: {device_name}\n")
            backup_file.write(f"! Host: {device.get('host', 'N/A')}\n")
            backup_file.write("!"*60 + "\n\n")
            backup_file.write(config)
        
        file_size = os.path.getsize(filename) / 1024  # Size in KB
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Backup saved: {filename} ({file_size:.1f} KB)")
        logging.info(f"Backup successful for {device_name}: {filename} ({file_size:.1f} KB)")
        
        # Disconnect
        connection.disconnect()
        
        return True, device_name
        
    except Exception as e:
        error_msg = f"Failed to backup {device_name}: {str(e)}"
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ {error_msg}")
        logging.error(error_msg)
        return False, device_name

def generate_report(success_count, fail_count, failed_devices, duration):
    """Generate and display summary report"""
    print("\n" + "="*80)
    print("BACKUP SUMMARY REPORT")
    print("="*80)
    print(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"\nResults:")
    print(f"  ✓ Successful: {success_count}")
    print(f"  ✗ Failed: {fail_count}")
    
    if failed_devices:
        print(f"\nFailed Devices:")
        for device in failed_devices:
            print(f"  - {device}")
    
    print("="*80)
    print(f"\nLog file: {log_file}")
    print(f"Backup location: backups/{datetime.now().strftime('%Y-%m-%d')}/")
    print("="*80)

def main():
    """Main function to orchestrate backups"""
    parser = argparse.ArgumentParser(description='Network Configuration Backup Script')
    parser.add_argument('--inventory', default='device_inventory.yaml', 
                       help='Device inventory file (default: device_inventory.yaml)')
    parser.add_argument('--no-email', action='store_true',
                       help='Disable email notifications')
    args = parser.parse_args()
    
    start_time = datetime.now()
    
    print("="*80)
    print("NETWORK CONFIGURATION BACKUP SYSTEM")
    print("="*80)
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Load devices from inventory
    devices = load_devices(args.inventory)
    
    if not devices:
        print("\n✗ No devices found in inventory!")
        logging.error("No devices in inventory")
        return
    
    print(f"\nFound {len(devices)} device(s) in inventory")
    logging.info(f"Starting backup for {len(devices)} device(s)")
    
    # Backup each device
    success_count = 0
    fail_count = 0
    failed_devices = []
    
    for device in devices:
        success, device_name = backup_device(device)
        if success:
            success_count += 1
        else:
            fail_count += 1
            failed_devices.append(device_name)
    
    # Calculate duration
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # Generate report
    generate_report(success_count, fail_count, failed_devices, duration)
    
    # Send email notification if configured
    if EMAIL_AVAILABLE and not args.no_email:
        email_config = load_email_config()
        if email_config:
            send_email_report(success_count, fail_count, failed_devices, email_config)
    
    logging.info(f"Backup run completed in {duration:.2f}s - Success: {success_count}, Failed: {fail_count}")

if __name__ == "__main__":
    main()
