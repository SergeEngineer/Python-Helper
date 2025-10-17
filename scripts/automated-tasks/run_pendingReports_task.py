#!/usr/bin/env python3
"""
Simple Daily report that check pending API jobs in [MY_TABLE1].[dbo].[Jobs] table

This script:
1. Query pending [Jobs]
2. Sends WARNING email report if exiding the limit
3. Sends RECOVERY email report if limit is back to normal.

Usage: python run_pendingReports_task.py
"""

import pyodbc
import requests
import smtplib
import json
import os
import socket
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# =============================================================================
# CONFIGURATION - Loaded from .env file
# =============================================================================

# Database settings
DB_SERVER = os.getenv('DB_SERVER')
DB_DATABASE = os.getenv('DB_DATABASE')
USE_WINDOWS_AUTH = os.getenv('USE_WINDOWS_AUTH', 'True').lower() == 'true'
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# API settings (if needed)
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

# Email settings
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', '25'))
USE_TLS = os.getenv('USE_TLS', 'False').lower() == 'true'
USE_AUTH = os.getenv('USE_AUTH', 'False').lower() == 'true'
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
FROM_EMAIL = os.getenv('FROM_EMAIL')
# Handle TO_EMAILS as a comma-separated string and convert to list
TO_EMAILS = [email.strip() for email in os.getenv('TO_EMAILS', '').split(',') if email.strip()]

# Alert threshold
ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', '50'))

# State file to track last alert state
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'alert_state.txt')


def log_message(message):
    """Simple logging function"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def connect_to_database():
    """Connect to SQL Server database"""
    try:
        if USE_WINDOWS_AUTH:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={DB_SERVER};"
                f"DATABASE={DB_DATABASE};"
                f"Trusted_Connection=yes;"
            )
        else:
            conn_str = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={DB_SERVER};"
                f"DATABASE={DB_DATABASE};"
                f"UID={DB_USERNAME};"
                f"PWD={DB_PASSWORD};"
            )
        
        connection = pyodbc.connect(conn_str)
        log_message(f"Successfully connected to database: {DB_DATABASE}")
        return connection
    except Exception as e:
        log_message(f"Failed to connect to database: {str(e)}")
        return None

def get_pending_records_from_database(connection):
    """Get Report records from database"""
    try:
        cursor = connection.cursor()
        
        # SQL query to get records - customize this for your table structure
        query = """
        SELECT
            I.tool_id,
            I.product_name,
            COUNT(*) AS Reports,
            J.StatusText
        FROM
            [MY_TABLE1].[dbo].[Jobs] as J WITH (NOLOCK)
        LEFT JOIN [MY_TABLE2].[dbo].[Inventory] as I WITH (NOLOCK)
            ON I.tool_id = J.ToolID
        WHERE
            J.CreatedDate > DATEADD(HOUR, -1, GETUTCDATE())
            AND StatusText NOT LIKE 'Success'
        GROUP BY
            I.tool_id, I.product_name, J.StatusText
        ORDER BY
            J.StatusText, I.product_name
        """
        
        cursor.execute(query)
        records = []
        total_count = 0
        
        for row in cursor.fetchall():
            try:
                tool_id = row[0]         # tool_id
                product_name = row[1]    # product_name
                count_reports = row[2]   # counter
                status_text = row[3]     # Status
                
                # Add to total count
                total_count += count_reports
                
                records.append({
                    'tool_id': tool_id,
                    'product_name': product_name,
                    'count_reports': count_reports,
                    'status_text': status_text
                })
            except Exception as e:
                log_message(f"Error processing record: {str(e)}")
                continue
        
        log_message(f"Found {len(records)} record groups with total of {total_count} reports")
        return records, total_count
        
    except Exception as e:
        log_message(f"Error getting records from database: {str(e)}")
        return [], 0


def create_email_report(records, total_count, alert_type):
    """Create HTML email report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    """Get computer name and path to make sure it's added to the email report"""
    server_name = socket.gethostname()
    execution_path = os.path.dirname(os.path.abspath(__file__))

    # Set colors based on alert type
    alert_color = "#e57373" if alert_type == "WARNING" else "#4CAF50"
    alert_class = "failure" if alert_type == "WARNING" else "success"

    html = f"""
    <html>
    <head>
    <style>
        body {{
            font-family: 'Segoe UI', Roboto, Arial, sans-serif;
            background-color: #fafafa;
            color: #333;
            margin: 20px;
        }}
        h2 {{
            color: {alert_color};
            border-bottom: 2px solid #ccc;
            padding-bottom: 6px;
        }}
        h3 {{
            color: #34495e;
            margin-top: 30px;
        }}
        p, li {{
            font-size: 14px;
            line-height: 1.6;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        ul li {{
            margin-bottom: 4px;
        }}
        .summary-list li strong {{
            color: #2c3e50;
        }}
        .success {{
            color: #4CAF50; /* soft green */
        }}
        .failure {{
            color: #e57373; /* soft red */
        }}
        .warning {{
            color: #ff9800; /* orange */
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 13px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px 10px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            color: #333;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        tr:hover {{
            background-color: #eef6ff;
        }}
        .footer {{
            margin-top: 40px;
            font-size: 13px;
            color: #666;
        }}
    </style>
    </head>
    <body>
        <h2>{alert_type}: Pending Reports Alert</h2>
        
        <p><strong>Execution Time:</strong> {timestamp}</p>
        <p><strong>Alert Type:</strong> <span class="{alert_class}">{alert_type}</span></p>
        <p><strong>Total Pending/Failed Reports:</strong> <span class="{alert_class}">{total_count}</span></p>
        <p><strong>Threshold:</strong> {ALERT_THRESHOLD}</p>
    """

    if records:
        html += f"""
        <h3>Pending/Failed Reports Details</h3>
        <table>
            <tr><th>Tool ID</th><th>Product Name</th><th>Report Count</th><th>Status</th></tr>
        """
        for record in records:
            status_class = "warning" if "pending" in record['status_text'].lower() else "failure"
            html += f"<tr><td>{record['tool_id']}</td><td>{record['product_name']}</td><td>{record['count_reports']}</td><td class='{status_class}'>{record['status_text']}</td></tr>"
        html += "</table>"
    else:
        html += "<p>No pending or failed reports found.</p>"

    html += f"""
        <div class="footer">
            <p><strong>Server Name:</strong> {server_name}</p>
            <p><strong>Execution Path:</strong> {execution_path}</p>
        </div>
    </body>
    </html>
    """
    return html

def read_last_alert_state():
    """Read the last alert state from file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return f.read().strip()
        return 'NORMAL'  # Default state if file doesn't exist
    except Exception as e:
        log_message(f"Error reading state file: {str(e)}")
        return 'NORMAL'

def write_alert_state(state):
    """Write the current alert state to file"""
    try:
        with open(STATE_FILE, 'w') as f:
            f.write(state)
        log_message(f"Alert state saved: {state}")
    except Exception as e:
        log_message(f"Error writing state file: {str(e)}")

def send_email_report(records, total_count, alert_type):
    """Send email report with appropriate subject based on alert type"""
    try:
        # Create email
        msg = MIMEMultipart()
        
        # Set subject based on alert type
        if alert_type == "WARNING":
            msg['Subject'] = f"WARNING: {total_count} pending or failed Reports (Threshold: {ALERT_THRESHOLD})"
        else:  # RECOVERY
            msg['Subject'] = f"RECOVERY: Reports back to normal ({total_count} reports)"
            
        msg['From'] = FROM_EMAIL
        msg['To'] = ", ".join(TO_EMAILS)
        
        # Add HTML content
        html_content = create_email_report(records, total_count, alert_type)
        msg.attach(MIMEText(html_content, 'html'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        # Use TLS if configured
        if USE_TLS:
            server.starttls()
        
        # Authenticate only if configured
        if USE_AUTH and EMAIL_USERNAME and EMAIL_PASSWORD:
            server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        
        server.send_message(msg)
        server.quit()
        
        log_message(f"{alert_type} email sent to {len(TO_EMAILS)} recipients")
        return True
        
    except Exception as e:
        log_message(f"Failed to send email: {str(e)}")
        return False

def main():
    """Main function"""
    log_message("=" * 50)
    log_message("Starting Reports monitoring")
    log_message("=" * 50)
    
    try:
        # Step 1: Connect to database
        connection = connect_to_database()
        if not connection:
            log_message("Cannot continue without database connection")
            return
        
        # Step 2: Get pnding records and total count
        records, total_count = get_pending_records_from_database(connection)
        connection.close()
        
        log_message(f"Total pending/failed reports: {total_count}")
        log_message(f"Alert threshold: {ALERT_THRESHOLD}")
        
        # Step 3: Read last alert state
        last_state = read_last_alert_state()
        log_message(f"Last alert state: {last_state}")
        
        # Step 4: Determine current state and send email if needed
        current_state = 'NORMAL'
        
        if total_count > ALERT_THRESHOLD:
            current_state = 'WARNING'
            log_message(f"WARNING: Total count ({total_count}) exceeds threshold ({ALERT_THRESHOLD} pending)")
            
            # Always send WARNING email (could be repeated warnings)
            send_email_report(records, total_count, "WARNING")
            write_alert_state('WARNING')
            
        elif total_count <= ALERT_THRESHOLD and total_count >= 0:
            current_state = 'NORMAL'
            
            # Only send RECOVERY email if we were previously in WARNING state
            if last_state == 'WARNING':
                log_message(f"RECOVERY: Total count ({total_count}) is back to normal (threshold: {ALERT_THRESHOLD} pending)")
                send_email_report(records, total_count, "RECOVERY")
                write_alert_state('NORMAL')
            else:
                log_message(f"Total count ({total_count}) is normal - no alert needed (last state: {last_state} pending)")
        
        # Step 4: Final summary
        log_message("=" * 50)
        log_message("PROCESSING COMPLETE")
        log_message(f"Total pending/failed reports: {total_count}")
        log_message(f"Record groups found: {len(records)}")
        log_message(f"Alert threshold: {ALERT_THRESHOLD}")
        log_message("=" * 50)
        
    except Exception as e:
        log_message(f"Unexpected error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
