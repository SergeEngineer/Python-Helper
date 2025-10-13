"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import json


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_json_data():
    """Sample JSON data for testing."""
    return {
        "name": "Test Data",
        "version": "1.0",
        "items": ["item1", "item2", "item3"],
        "config": {
            "enabled": True,
            "max_count": 100
        }
    }


@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing."""
    return [
        {"name": "John Doe", "age": "25", "department": "Engineering"},
        {"name": "Jane Smith", "age": "30", "department": "Marketing"},
        {"name": "Bob Johnson", "age": "35", "department": "Engineering"},
        {"name": "Alice Brown", "age": "28", "department": "HR"}
    ]


@pytest.fixture
def sample_files(temp_dir):
    """Create sample files for testing."""
    files = {}
    
    # Create a text file
    text_file = temp_dir / "sample.txt"
    text_file.write_text("This is a sample text file.")
    files['text'] = text_file
    
    # Create a JSON file
    json_file = temp_dir / "sample.json"
    json_data = {"test": "data", "number": 42}
    json_file.write_text(json.dumps(json_data))
    files['json'] = json_file
    
    # Create a subdirectory with files
    sub_dir = temp_dir / "subdir"
    sub_dir.mkdir()
    sub_file = sub_dir / "nested.txt"
    sub_file.write_text("Nested file content")
    files['nested'] = sub_file
    
    return files


@pytest.fixture
def mock_web_content():
    """Mock web content for testing web scraping functions."""
    return """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Welcome to Test Page</h1>
            <p>This is a test paragraph.</p>
            <div class="content">
                <p>Content paragraph 1</p>
                <p>Content paragraph 2</p>
            </div>
            <ul>
                <li><a href="https://example.com/page1">Page 1</a></li>
                <li><a href="/page2">Page 2</a></li>
                <li><a href="relative.html">Relative Page</a></li>
            </ul>
        </body>
    </html>
    """