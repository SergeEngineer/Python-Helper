#!/usr/bin/env python3
"""
Simple Daily Task that check Database table for stuck Jobs and resends them to API webhook

This script:
1. Gets JSON data from SQL Server database
2. Sends each record to API webhook
3. Sends email report with results

Usage: python run_DbCheck_sendToAPI_task.py
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

# API settings
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

# =============================================================================
# MAIN SCRIPT - No need to modify below this line
# =============================================================================

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

def get_records_from_database(connection):
    """Get JSON records from database"""
    try:
        cursor = connection.cursor()
        
        # SQL query to get records - customize this for your table structure
        query = """
        SELECT R.CleansedResponseValues, A.assessmentLink, A.catalogId, R.LastUpdate, A.status, A.AssessmentDate
        FROM [MY_TABLE1].[dbo].[Results] as R with (nolock)
        left join [MY_TABLE2].[dbo].[Assessments] as A with (nolock) on A.Id = R.SessionID 
        WHERE R.LastUpdate > CAST(GETDATE()-31 as date)  
          and A.AssessmentDate is null 
          and A.id is not null
        ORDER BY R.LastUpdate desc
        """
        
        cursor.execute(query)
        records = []
        
        for row in cursor.fetchall():
            try:
                cleansed_response = row[0]  # CleansedResponseValues
                assessment_link = row[1]    # assessmentLink
                catalog_id = row[2]         # catalogId
                last_update = row[3]        # LastUpdate
                
                # Parse JSON to validate it
                json_data = json.loads(cleansed_response)
                
                records.append({
                    'assessment_link': assessment_link,
                    'json_data': json_data,
                    'last_update': last_update
                })
            except json.JSONDecodeError:
                log_message(f"Invalid JSON for assessment {assessment_link}, skipping")
                continue
        
        log_message(f"Found {len(records)} valid records to process")
        return records
        
    except Exception as e:
        log_message(f"Error getting records from database: {str(e)}")
        return []

def send_to_api(record):
    """Send a single record to the Portal API"""
    try:
        headers = {
            "Content-Type": "application/json",
            "ApiKey": API_KEY
        }
        
        response = requests.post(
            API_URL,
            json=record['json_data'],
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return True, f"Success (HTTP {response.status_code})"
        else:
            return False, f"HTTP {response.status_code}: {response.text}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def process_all_records(records):
    """Process all records through the API"""
    results = {
        'total': len(records),
        'successful': [],
        'failed': [],
        'start_time': datetime.now()
    }
    
    for i, record in enumerate(records, 1):
        assessment_link = record['assessment_link']
        log_message(f"Processing {i}/{len(records)}: {assessment_link}")
        
        success, message = send_to_api(record)
        
        result_record = {
            'assessment_link': assessment_link,
            'message': message,
            'timestamp': datetime.now(),
            'last_update': record['last_update']
        }
        
        if success:
            results['successful'].append(result_record)
            log_message(f"✓ Success: {assessment_link}")
        else:
            results['failed'].append(result_record)
            log_message(f"✗ Failed: {assessment_link} - {message}")
    
    results['end_time'] = datetime.now()
    return results

def create_email_report(results):
    """Create HTML email report"""
    start_time = results['start_time'].strftime("%Y-%m-%d %H:%M:%S")
    end_time = results['end_time'].strftime("%Y-%m-%d %H:%M:%S")
    duration = results['end_time'] - results['start_time']
    
    successful_count = len(results['successful'])
    failed_count = len(results['failed'])
    total_count = results['total']
    
    """Get computer name and path to make sure it's added to the email report"""
    server_name = socket.gethostname()
    execution_path = os.path.dirname(os.path.abspath(__file__))

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
            color: #2c3e50;
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
        <h2>Task: JSON reprocessing via API</h2>
        
        <p><strong>Execution:</strong> {start_time} to {end_time}</p>
        <p><strong>Duration:</strong> {str(duration).split('.')[0]}</p>
        
        <h3>Summary</h3>
        <ul class="summary-list">
            <li><strong>Total Records:</strong> {total_count}</li>
            <li class="success"><strong>Successful:</strong> {successful_count}</li>
            <li class="failure"><strong>Failed:</strong> {failed_count}</li>
            <li><strong>Success Rate:</strong> {(successful_count/total_count*100):.1f}%</li>
        </ul>
    """

    if results['successful']:
        html += """
        <h3 class="success">Successful Records</h3>
        <table>
            <tr><th>Assessment Link</th><th>Assessment Date</th><th>Status</th></tr>
        """
        for record in results['successful']:
            time_str = record['last_update'].strftime("%Y-%m-%d %H:%M:%S")
            html += f"<tr><td>{record['assessment_link']}</td><td>{time_str}</td><td class='success'>{record['message']}</td></tr>"
        html += "</table>"

    if results['failed']:
        html += """
        <h3 class="failure">Failed Records</h3>
        <table>
            <tr><th>Assessment Link</th><th>Assessment Date</th><th>Error</th></tr>
        """
        for record in results['failed']:
            time_str = record['last_update'].strftime("%Y-%m-%d %H:%M:%S")
            html += f"<tr><td>{record['assessment_link']}</td><td>{time_str}</td><td class='failure'>{record['message']}</td></tr>"
        html += "</table>"

    html += f"""
        <div class="footer">
            <p><strong>Server Name:</strong> {server_name}</p>
            <p><strong>Execution Path:</strong> {execution_path}</p>
        </div>
    </body>
    </html>
    """
    return html

def send_email_report(results):
    """Send email report"""
    try:
        # Create email
        msg = MIMEMultipart()
        msg['Subject'] = "Task: JSON to API Processing Report"
        msg['From'] = FROM_EMAIL
        msg['To'] = ", ".join(TO_EMAILS)
        
        # Add HTML content
        html_content = create_email_report(results)
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
        
        log_message(f"Email report sent to {len(TO_EMAILS)} recipients")
        return True
        
    except Exception as e:
        log_message(f"Failed to send email: {str(e)}")
        return False

def main():
    """Main function"""
    log_message("=" * 50)
    log_message("Starting Conners4 to Portal API processing")
    log_message("=" * 50)
    
    try:
        # Step 1: Connect to database
        connection = connect_to_database()
        if not connection:
            log_message("Cannot continue without database connection")
            return
        
        # Step 2: Get records
        records = get_records_from_database(connection)
        connection.close()
        
        if not records:
            log_message("No records to process")
            # Still send email report for zero records
            results = {
                'total': 0,
                'successful': [],
                'failed': [],
                'start_time': datetime.now(),
                'end_time': datetime.now()
            }
        else:
            # Step 3: Process records through API
            results = process_all_records(records)
        
        # Step 4: Send email report
        send_email_report(results)
        
        # Step 5: Final summary
        log_message("=" * 50)
        log_message("PROCESSING COMPLETE")
        log_message(f"Total: {results['total']}")
        log_message(f"Successful: {len(results['successful'])}")
        log_message(f"Failed: {len(results['failed'])}")
        log_message("=" * 50)
        
    except Exception as e:
        log_message(f"Unexpected error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
