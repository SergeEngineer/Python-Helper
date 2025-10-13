#!/usr/bin/env python3
"""
File Operations Example

This script demonstrates how to use the file_ops module from python_helpers.
"""

import sys
import os

# Add the parent directory to the Python path so we can import python_helpers
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from python_helpers.file_ops import (
    ensure_directory,
    safe_copy,
    find_files,
    read_json,
    write_json,
    get_file_info
)


def demonstrate_file_operations():
    """Demonstrate various file operations."""
    print("=== Python Helpers - File Operations Example ===\n")
    
    # 1. Create directories
    print("1. Creating test directories...")
    test_dir = ensure_directory("temp/test_files")
    print(f"Created directory: {test_dir}")
    
    # 2. Create and write JSON files
    print("\n2. Creating sample JSON files...")
    sample_data = {
        "name": "Python Helper Example",
        "version": "1.0",
        "features": ["file_ops", "data_processing", "web_scraping"],
        "config": {
            "debug": True,
            "max_retries": 3
        }
    }
    
    json_file = test_dir / "sample.json"
    if write_json(sample_data, json_file):
        print(f"Created JSON file: {json_file}")
    
    # 3. Read JSON file
    print("\n3. Reading JSON file...")
    data = read_json(json_file)
    if data:
        print(f"Read data: {data['name']} v{data['version']}")
        print(f"Features: {', '.join(data['features'])}")
    
    # 4. Get file information
    print("\n4. File information...")
    info = get_file_info(json_file)
    if info:
        print(f"File: {info['name']}")
        print(f"Size: {info['size']} bytes")
        print(f"Extension: {info['extension']}")
        print(f"Is file: {info['is_file']}")
    
    # 5. Copy file
    print("\n5. Copying file...")
    backup_file = test_dir / "sample_backup.json"
    if safe_copy(json_file, backup_file):
        print(f"File copied to: {backup_file}")
    
    # 6. Find files
    print("\n6. Finding JSON files...")
    json_files = find_files(test_dir, "*.json")
    print(f"Found {len(json_files)} JSON files:")
    for file in json_files:
        print(f"  - {file.name}")
    
    # 7. Cleanup (optional)
    print("\n7. Cleanup...")
    try:
        import shutil
        shutil.rmtree("temp")
        print("Cleaned up temporary files")
    except Exception as e:
        print(f"Cleanup failed: {e}")


if __name__ == "__main__":
    demonstrate_file_operations()