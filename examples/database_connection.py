import sys  
import os
from datetime import datetime
from dotenv import load_dotenv

# Add the parent directory to the Python path so we can import 'package"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from package.database import(
    connect_to_database
)

# Load environment variables
load_dotenv()

# Configure logging
def log_message(message):
    """Simple logging function"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def main():
    """Main function"""
    log_message("=" * 50)
    log_message("Starting database test")
    log_message("=" * 50)

    connected = connect_to_database(os.getenv('USE_WINDOWS_AUTH'), os.getenv('DB_SERVER'), os.getenv('DB_DATABASE'), os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'))
    
    if not connected:
        log_message("Cannot continue without database connection")
        return
    
    connected.close()

if __name__ == "__main__":
    main()