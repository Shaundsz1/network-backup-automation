# Network Configuration Backup System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Netmiko](https://img.shields.io/badge/Netmiko-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A professional-grade network automation tool for backing up Cisco device configurations. Built with Python and Netmiko, this system provides automated, timestamped backups with comprehensive logging, configuration comparison, and optional email notifications.

## 🚀 Features

- **Automated Configuration Backups**: Connect to network devices via SSH and retrieve running configurations
- **Multi-Device Support**: Manage multiple devices through YAML inventory
- **Timestamped Organization**: Backups organized by date with precise timestamps
- **Configuration Diff Tool**: Compare configurations between backups to track changes
- **Comprehensive Logging**: Detailed logs for troubleshooting and audit trails
- **Email Notifications**: Optional email reports on backup success/failure
- **Scheduled Backups**: Built-in scheduler for automated recurring backups
- **Error Handling**: Graceful failure handling with detailed error reporting

## 📋 Requirements

- Python 3.8 or higher
- Network devices with SSH enabled
- Valid credentials for device access

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/network-backup-automation.git
cd network-backup-automation
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Device Inventory

Edit `device_inventory.yaml` to add your network devices:
```yaml
devices:
  - device_type: cisco_ios
    host: 192.168.1.1
    username: admin
    password: your_password
    port: 22
    device_name: Router-01
  
  - device_type: cisco_ios
    host: 192.168.1.2
    username: admin
    password: your_password
    port: 22
    device_name: Switch-01
```

### Email Notifications (Optional)

Edit `email_config.yaml` to enable email notifications:
```yaml
sender_email: your-email@gmail.com
password: your-app-password
receiver_email: recipient@example.com
smtp_server: smtp.gmail.com
smtp_port: 587
```

**Note**: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## 🎯 Usage

### Basic Backup

Run a one-time backup of all devices:
```bash
python3 backup_script.py
```

### Disable Email Notifications
```bash
python3 backup_script.py --no-email
```

### Custom Inventory File
```bash
python3 backup_script.py --inventory custom_devices.yaml
```

### Compare Configurations

Check what changed between backups:
```bash
python3 config_diff.py
```

When prompted, enter the device name (e.g., `Router-01`)

### Scheduled Backups

Run automated backups on a schedule:
```bash
python3 schedule_backups.py
```

Default schedule:
- Daily at 2:00 AM
- Every 6 hours

Press `Ctrl+C` to stop the scheduler.

## 📁 Project Structure
```
network-backup-automation/
├── backup_script.py          # Main backup script
├── config_diff.py            # Configuration comparison tool
├── email_notification.py     # Email notification module
├── schedule_backups.py       # Backup scheduler
├── device_inventory.yaml     # Device inventory file
├── email_config.yaml         # Email configuration (optional)
├── requirements.txt          # Python dependencies
├── backups/                  # Backup storage (organized by date)
│   └── YYYY-MM-DD/
│       └── Device-Name_HH-MM-SS.txt
└── logs/                     # Log files
    └── backup_YYYY-MM-DD.log
```

## 📊 Output Example
```
================================================================================
NETWORK CONFIGURATION BACKUP SYSTEM
================================================================================
Start Time: 2026-01-13 21:22:54

Found 1 device(s) in inventory

[21:22:54] Connecting to Cat8k-Sandbox...
[21:22:56] Connected! Retrieving configuration...
[21:22:57] ✓ Backup saved: backups/2026-01-13/Cat8k-Sandbox_21-22-57.txt (6.9 KB)

================================================================================
BACKUP SUMMARY REPORT
================================================================================
Execution Time: 2026-01-13 21:22:57
Duration: 3.40 seconds

Results:
  ✓ Successful: 1
  ✗ Failed: 0
================================================================================
```

## 🔍 Supported Device Types

This tool uses Netmiko and supports 50+ device types including:

- `cisco_ios` - Cisco IOS
- `cisco_xe` - Cisco IOS-XE
- `cisco_nxos` - Cisco NX-OS
- `cisco_asa` - Cisco ASA
- `juniper_junos` - Juniper JunOS
- `arista_eos` - Arista EOS
- `hp_comware` - HP Comware
- And many more...

See [Netmiko documentation](https://github.com/ktbyers/netmiko) for full list.

## 🛡️ Security Best Practices

⚠️ **Important Security Notes:**

- **Never commit credentials** to version control
- Add `device_inventory.yaml` and `email_config.yaml` to `.gitignore`
- Use environment variables or secret management tools for production
- Consider using SSH keys instead of passwords where possible
- Restrict file permissions on configuration files: `chmod 600 device_inventory.yaml`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Your Name**

- LinkedIn: https://www.linkedin.com/in/shaundsz/

## 🙏 Acknowledgments

- Built with [Netmiko](https://github.com/ktbyers/netmiko) by Kirk Byers
- Tested on Cisco DevNet Sandbox infrastructure
- Inspired by real-world network operations challenges

## 📚 Future Enhancements

- [ ] Web-based dashboard for viewing backups
- [ ] Support for NETCONF/RESTCONF APIs
- [ ] Backup encryption
- [ ] Integration with Git for version control
- [ ] Slack/Teams notification support
- [ ] Configuration validation before backup
- [ ] Rollback functionality

---

**Star ⭐ this repository if you find it helpful!**
