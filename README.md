# Python Helpers Library 🐍

A comprehensive collection of Python utilities and helper functions designed for learning and practical development tasks.

## 🎯 Purpose

This repository serves as both a **learning resource** and a **practical utility library** for Python developers. Whether you're just starting your Python journey or looking for reusable code snippets for common tasks, this library has you covered.

## ✨ Features

- **🗂️ File Operations**: Safe file handling, JSON processing, directory management
- **📊 Data Processing**: Clean, analyze, and transform data with ease
- **🌐 Web Scraping**: HTTP requests, HTML parsing, and content extraction
- **⚙️ Automation**: Task scheduling, system commands, and file monitoring
- **🔧 Utilities**: Password generation, hashing, validation, and more
- **🧪 Well Tested**: Comprehensive test suite with pytest
- **📖 Educational**: Clear documentation and learning materials

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/Python-Helper.git
cd Python-Helper

# Install dependencies
pip install -r requirements.txt

# Run an example
python examples/file_operations_example.py
```

### Basic Usage

```python
# Import the helpers you need
from python_helpers.file_ops import ensure_directory, write_json
from python_helpers.utilities import generate_password
from python_helpers.data_processing import clean_data

# Create a directory and save some data
data_dir = ensure_directory("my_project/data")
config = {"api_key": generate_password(32), "version": "1.0"}
write_json(config, data_dir / "config.json")

# Clean messy data
raw_data = [{"name": " John ", "age": "", "score": "85"}]
clean_records = clean_data(raw_data)
print(clean_records)  # [{"name": "John", "score": "85"}]
```

## 📁 Project Structure

```
Python-Helper/
├── 📦 python_helpers/     # Core library modules
│   ├── file_ops/          # File & directory operations
│   ├── data_processing/   # Data cleaning & analysis
│   ├── web_scraping/      # HTTP requests & HTML parsing
│   ├── automation/        # Task automation & scheduling
│   └── utilities/         # General-purpose utilities
├── 📜 scripts/            # Ready-to-use practical scripts
├── 🎯 examples/           # Usage examples & demonstrations
├── 📚 learning/           # Tutorials & educational content
├── 🧪 tests/             # Comprehensive test suite
└── 📖 docs/              # Detailed documentation
```

## 🎓 Learning Path

### For Beginners:
1. **Start Here**: Run `python examples/file_operations_example.py`
2. **Learn by Example**: Explore the `examples/` directory
3. **Practice**: Try the tutorials in `learning/tutorials/`
4. **Build Something**: Work on projects in `learning/projects/`

### For Experienced Developers:
1. **Browse the API**: Check out `docs/README.md` for full documentation
2. **Use in Projects**: Install with `pip install -e .` for development
3. **Extend**: Add your own modules and utilities
4. **Contribute**: Submit pull requests with improvements

## 🛠️ Available Modules

| Module | Purpose | Key Functions |
|--------|---------|---------------|
| `file_ops` | File operations | `ensure_directory`, `safe_copy`, `read_json`, `write_json` |
| `data_processing` | Data manipulation | `clean_data`, `group_by`, `calculate_stats`, `csv_to_dict` |
| `web_scraping` | Web scraping | `safe_request`, `parse_html`, `extract_links`, `download_file` |
| `automation` | Task automation | `run_command`, `schedule_task`, `backup_files`, `monitor_directory` |
| `utilities` | General utilities | `generate_password`, `hash_string`, `validate_email`, `format_bytes` |

## 📋 Quick Examples

### File Operations
```python
from python_helpers.file_ops import find_files, get_file_info

# Find all Python files
py_files = find_files(".", "*.py")

# Get detailed file information
for file in py_files:
    info = get_file_info(file)
    print(f"{info['name']}: {info['size']} bytes")
```

### Data Processing
```python
from python_helpers.data_processing import group_by, calculate_stats

employees = [
    {"name": "John", "dept": "Engineering", "salary": 75000},
    {"name": "Jane", "dept": "Engineering", "salary": 80000},
    {"name": "Bob", "dept": "Marketing", "salary": 65000}
]

# Group by department
dept_groups = group_by(employees, "dept")

# Calculate salary statistics
salaries = [emp["salary"] for emp in employees]
stats = calculate_stats(salaries)
print(f"Average salary: ${stats['mean']:,.2f}")
```

### Web Scraping
```python
from python_helpers.web_scraping import safe_request, parse_html, extract_links

# Fetch and parse webpage
response = safe_request("https://example.com")
if response:
    soup = parse_html(response.text)
    links = extract_links(soup)
    print(f"Found {len(links)} links")
```

### Automation
```python
from python_helpers.automation import backup_files, cleanup_old_files

# Backup important files
backup_files(["config.json", "data.csv"], "backups/")

# Clean up old log files
cleanup_old_files("logs/", days_old=7, pattern="*.log")
```

### Utilities
```python
from python_helpers.utilities import generate_password, format_bytes, time_ago
from datetime import datetime, timedelta

# Generate secure password
password = generate_password(16, include_symbols=True)

# Format file sizes
print(format_bytes(1024 * 1024))  # "1.0 MB"

# Human-readable time differences
old_time = datetime.now() - timedelta(hours=2)
print(time_ago(old_time))  # "2 hours ago"
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=python_helpers

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: Found a bug? Create an issue
2. **Suggest Features**: Have an idea? We'd love to hear it
3. **Add Utilities**: Write new helper functions
4. **Improve Documentation**: Help make things clearer
5. **Write Tests**: Help us maintain quality

### Development Setup

```bash
# Install in development mode
pip install -e .[dev]

# Install pre-commit hooks (optional)
pre-commit install

# Run tests before committing
pytest
```

## 🎯 Use Cases

This library is perfect for:

- **Learning Python**: Understand practical coding patterns
- **Rapid Prototyping**: Get common tasks done quickly
- **Automation Scripts**: Build reliable automation tools
- **Data Processing**: Handle CSV files and data cleaning
- **File Management**: Organize and process files safely
- **Web Scraping Projects**: Extract data from websites
- **System Administration**: Automate system tasks

## 📖 Documentation

For detailed documentation, examples, and tutorials:
- **API Reference**: See `docs/README.md`
- **Examples**: Browse the `examples/` directory
- **Tutorials**: Check `learning/tutorials/`
- **Projects**: Try `learning/projects/`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star This Repo!

If you find this library helpful, please give it a star! It helps others discover the project and motivates continued development.

---

**Happy Coding!** 🚀

Built with ❤️ for the Python community

# Python-Helper
python samples
