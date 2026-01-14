#!/usr/bin/env python3
"""
Email Notification Module
Sends backup reports via email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

def send_email_report(success_count, fail_count, failed_devices=None, email_config=None):
    """Send email report of backup results"""
    
    if email_config is None:
        print("Email configuration not provided. Skipping email notification.")
        return
    
    # Email configuration
    sender_email = email_config.get('sender_email')
    receiver_email = email_config.get('receiver_email')
    smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
    smtp_port = email_config.get('smtp_port', 587)
    password = email_config.get('password')
    
    if not all([sender_email, receiver_email, password]):
        print("Incomplete email configuration. Skipping notification.")
        return
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Network Backup Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Email body
    status = "✓ SUCCESS" if fail_count == 0 else "⚠ WARNING"
    
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2 style="color: {'green' if fail_count == 0 else 'orange'};">{status}</h2>
        <h3>Network Configuration Backup Report</h3>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <table style="border-collapse: collapse; margin: 20px 0;">
          <tr style="background-color: #f2f2f2;">
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Successful Backups:</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd; color: green;">{success_count}</td>
          </tr>
          <tr>
            <td style="padding: 10px; border: 1px solid #ddd;"><strong>Failed Backups:</strong></td>
            <td style="padding: 10px; border: 1px solid #ddd; color: red;">{fail_count}</td>
          </tr>
        </table>
        
        {'<h4 style="color: red;">Failed Devices:</h4><ul>' + ''.join([f'<li>{dev}</li>' for dev in failed_devices]) + '</ul>' if failed_devices else ''}
        
        <p style="color: #666; font-size: 12px; margin-top: 30px;">
          This is an automated message from your Network Backup System.
        </p>
      </body>
    </html>
    """
    
    part = MIMEText(html, "html")
    message.attach(part)
    
    # Send email
    try:
        print("\nSending email notification...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("✓ Email notification sent successfully!")
        return True
    except Exception as e:
        print(f"✗ Failed to send email: {e}")
        return False

def load_email_config():
    """Load email configuration from file"""
    config_file = "email_config.yaml"
    
    if not os.path.exists(config_file):
        return None
    
    import yaml
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)
