# Python Helpers Library Documentation

A comprehensive collection of Python utilities and helper functions for common development tasks.

## 📚 Modules Overview

### 🗂️ File Operations (`python_helpers.file_ops`)

**Purpose**: Handle file and directory operations safely and efficiently.

**Key Functions**:
- `ensure_directory(path)` - Create directories safely
- `safe_copy(source, dest, overwrite=False)` - Copy files with protection
- `find_files(directory, pattern="*", recursive=True)` - Find files by pattern
- `read_json(file_path)` / `write_json(data, file_path)` - JSON file handling
- `get_file_info(file_path)` - Get detailed file information

**Example Usage**:
```python
from python_helpers.file_ops import ensure_directory, write_json, find_files

# Create directory and write data
data_dir = ensure_directory("data/processed")
sample_data = {"name": "test", "values": [1, 2, 3]}
write_json(sample_data, data_dir / "config.json")

# Find all Python files
py_files = find_files(".", "*.py")
print(f"Found {len(py_files)} Python files")
```

### 📊 Data Processing (`python_helpers.data_processing`)

**Purpose**: Clean, analyze, and transform data efficiently.

**Key Functions**:
- `clean_data(data, remove_empty=True, strip_strings=True)` - Clean data records
- `group_by(data, key)` - Group records by field
- `filter_data(data, filters)` - Filter records by criteria
- `calculate_stats(values)` - Calculate basic statistics
- `csv_to_dict(file_path)` / `dict_to_csv(data, file_path)` - CSV handling

**Example Usage**:
```python
from python_helpers.data_processing import clean_data, group_by, calculate_stats

# Clean messy data
raw_data = [
    {"name": " John ", "age": "25", "score": "85"},
    {"name": "Jane", "age": "", "score": "92"},
]
clean_records = clean_data(raw_data)

# Group by field
grouped = group_by(clean_records, "department")

# Calculate statistics
scores = [int(r["score"]) for r in clean_records if r["score"]]
stats = calculate_stats(scores)
print(f"Average score: {stats['mean']:.1f}")
```

### 🌐 Web Scraping (`python_helpers.web_scraping`)

**Purpose**: Handle web scraping and HTTP operations safely.

**Key Functions**:
- `safe_request(url, headers=None, timeout=10, retries=3)` - Make HTTP requests
- `parse_html(html_content, parser='html.parser')` - Parse HTML content
- `extract_links(soup_object, base_url="")` - Extract all links
- `extract_text(soup_object, tag=None, class_=None)` - Extract text content
- `download_file(url, filename, headers=None)` - Download files

**Example Usage**:
```python
from python_helpers.web_scraping import safe_request, parse_html, extract_links

# Fetch and parse webpage
response = safe_request("https://example.com")
if response:
    soup = parse_html(response.text)
    links = extract_links(soup, "https://example.com")
    print(f"Found {len(links)} links")
```

### ⚙️ Automation (`python_helpers.automation`)

**Purpose**: Automate tasks and system operations.

**Key Functions**:
- `run_command(command, shell=True, capture_output=True)` - Execute system commands
- `batch_commands(commands, continue_on_error=True)` - Run multiple commands
- `schedule_task(func, interval_seconds, max_runs=None)` - Simple task scheduler
- `monitor_directory(directory, callback, interval=5)` - Monitor file changes
- `backup_files(source_paths, backup_dir, compress=False)` - Create backups
- `cleanup_old_files(directory, days_old=30, pattern="*")` - Clean old files

**Example Usage**:
```python
from python_helpers.automation import run_command, backup_files, schedule_task

# Run system command
result = run_command("dir", shell=True)  # Windows
if result['success']:
    print(result['stdout'])

# Backup important files
backup_result = backup_files(
    ["config.json", "data/important.csv"], 
    "backups/"
)

# Schedule a task
def daily_cleanup():
    print("Running daily cleanup...")
    
schedule_task(daily_cleanup, interval_seconds=86400, max_runs=7)
```

### 🔧 Utilities (`python_helpers.utilities`)

**Purpose**: General-purpose utility functions.

**Key Functions**:
- `generate_password(length=12, include_symbols=True)` - Generate secure passwords
- `generate_uuid(version=4)` - Generate UUIDs
- `hash_string(text, algorithm='sha256')` - Hash strings
- `validate_email(email)` - Validate email addresses
- `clean_filename(filename, replacement='_')` - Clean filenames
- `format_bytes(bytes_size)` - Format file sizes
- `time_ago(timestamp)` - Human-readable time differences
- `flatten_dict(nested_dict, separator='.')` - Flatten nested dictionaries
- `chunk_list(lst, chunk_size)` - Split lists into chunks
- `retry_operation(func, max_attempts=3)` - Retry operations with backoff

**Example Usage**:
```python
from python_helpers.utilities import generate_password, format_bytes, clean_filename
from datetime import datetime, timedelta

# Generate secure password
password = generate_password(16, include_symbols=True)

# Format file size
size_str = format_bytes(1024 * 1024 * 500)  # "500.0 MB"

# Clean filename
safe_name = clean_filename("My File<>:?.txt")  # "My File____.txt"

# Time ago
old_time = datetime.now() - timedelta(hours=2)
print(time_ago(old_time))  # "2 hours ago"
```

## 🚀 Getting Started

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/Python-Helper.git
cd Python-Helper
```

2. **Install dependencies**:
```bash
# Basic installation
pip install -r requirements.txt

# Or install in development mode
pip install -e .

# With optional dependencies
pip install -e .[dev,data,docs]
```

3. **Run examples**:
```bash
# File operations example
python examples/file_operations_example.py

# Data processing example
python scripts/data_analysis/csv_processor.py
```

### Quick Start

```python
# Import the entire library
import python_helpers

# Or import specific modules
from python_helpers import file_ops, data_processing, utilities

# Use the functions
data_dir = file_ops.ensure_directory("my_project/data")
password = utilities.generate_password(12)
```

## 📁 Project Structure

```
Python-Helper/
├── python_helpers/          # Main library package
│   ├── __init__.py         # Package initialization
│   ├── file_ops/           # File operations module
│   ├── data_processing/    # Data processing module
│   ├── web_scraping/       # Web scraping module
│   ├── automation/         # Automation module
│   └── utilities/          # General utilities module
├── scripts/                # Ready-to-use scripts
│   ├── automation/         # Automation scripts
│   ├── data_analysis/      # Data analysis scripts
│   └── file_management/    # File management scripts
├── examples/               # Usage examples
├── learning/               # Learning materials
│   ├── tutorials/          # Step-by-step tutorials
│   ├── exercises/          # Practice exercises
│   └── projects/           # Learning projects
├── tests/                  # Unit tests
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
└── pyproject.toml         # Project configuration
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=python_helpers

# Run specific test category
pytest -m unit
pytest -m integration
```

## 📖 Learning Path

1. **Start with Examples**: Run the example scripts in `examples/`
2. **Practice with Scripts**: Use the practical scripts in `scripts/`
3. **Work Through Tutorials**: Follow tutorials in `learning/tutorials/`
4. **Build Projects**: Try the projects in `learning/projects/`
5. **Contribute**: Add your own utilities and improvements

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## 📝 Development Guidelines

- **Code Style**: Use `black` for formatting and `flake8` for linting
- **Type Hints**: Use type hints for all functions
- **Documentation**: Document all functions with docstrings
- **Testing**: Write tests for new functionality
- **Error Handling**: Use proper exception handling

## ⚡ Performance Tips

- Use built-in functions when possible
- Leverage generators for large data sets
- Cache expensive operations
- Use appropriate data structures
- Profile code for bottlenecks

## 🔍 Debugging Tips

- Use the `get_file_info()` function to inspect files
- Enable debug logging in your scripts
- Use the `retry_operation()` utility for flaky operations
- Check command results when using automation functions

## 📚 Additional Resources

- [Python Official Documentation](https://docs.python.org/3/)
- [Real Python Tutorials](https://realpython.com/)
- [Python Package User Guide](https://packaging.python.org/)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Create an issue for bugs or feature requests
- Check existing issues before creating new ones
- Provide detailed information when reporting issues