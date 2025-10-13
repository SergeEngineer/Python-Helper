# Getting Started with Python Helpers

Welcome to the Python Helpers tutorial series! This tutorial will guide you through your first steps with the library.

## What You'll Learn

- How to set up and use the Python Helpers library
- Basic file operations and data processing
- How to run your first automation script
- Best practices for organizing your code

## Prerequisites

- Basic knowledge of Python (variables, functions, loops)
- Python 3.8+ installed on your system
- A text editor or IDE (VS Code, PyCharm, etc.)

## Step 1: Setting Up Your Environment

First, let's make sure you have everything set up correctly:

1. **Clone the repository** (if you haven't already):
```bash
git clone https://github.com/your-username/Python-Helper.git
cd Python-Helper
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Test the installation** by running an example:
```bash
python examples/file_operations_example.py
```

If you see output without errors, you're ready to go!

## Step 2: Your First Helper Script

Let's create a simple script that demonstrates the key features. Create a new file called `my_first_helper_script.py`:

```python
#!/usr/bin/env python3
"""
My First Python Helper Script

This script demonstrates basic usage of the Python Helpers library.
"""

import sys
from pathlib import Path

# Add the Python Helper library to our path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import the helper modules we need
from python_helpers.file_ops import ensure_directory, write_json, read_json
from python_helpers.utilities import generate_password, format_bytes
from python_helpers.data_processing import clean_data, calculate_stats

def main():
    print("🐍 Welcome to Python Helpers!")
    print("=" * 40)
    
    # Step 1: File Operations
    print("\n📁 Step 1: Working with files")
    
    # Create a directory for our project
    project_dir = ensure_directory("my_helper_project")
    print(f"Created directory: {project_dir}")
    
    # Generate some configuration data
    config = {
        "project_name": "My First Helper Project",
        "version": "1.0.0",
        "api_key": generate_password(32, include_symbols=False),
        "created": "2024-01-01",
        "features": ["file_ops", "data_processing", "utilities"]
    }
    
    # Save configuration to JSON file
    config_file = project_dir / "config.json"
    if write_json(config, config_file):
        print(f"Configuration saved to: {config_file}")
    
    # Read it back to verify
    loaded_config = read_json(config_file)
    if loaded_config:
        print(f"Project: {loaded_config['project_name']}")
        print(f"Version: {loaded_config['version']}")
        print(f"Features: {', '.join(loaded_config['features'])}")
    
    # Step 2: Data Processing
    print("\n📊 Step 2: Processing data")
    
    # Some messy sample data
    messy_data = [
        {"name": " John Doe ", "age": "25", "score": "85", "department": ""},
        {"name": "Jane Smith", "age": "", "score": "92", "department": "Engineering"},
        {"name": " Bob Johnson ", "age": "30", "score": "", "department": "Marketing"},
        {"name": "Alice Brown", "age": "28", "score": "78", "department": "Engineering"},
    ]
    
    print(f"Original data has {len(messy_data)} records")
    
    # Clean the data
    clean_records = clean_data(messy_data, remove_empty=True, strip_strings=True)
    print(f"After cleaning: {len(clean_records)} records")
    
    # Calculate some statistics on the scores
    scores = [int(record["score"]) for record in clean_records 
              if record.get("score") and record["score"].isdigit()]
    
    if scores:
        stats = calculate_stats(scores)
        print(f"Score statistics:")
        print(f"  Average: {stats['mean']:.1f}")
        print(f"  Median: {stats['median']:.1f}")
        print(f"  Range: {stats['min']} - {stats['max']}")
    
    # Step 3: Utilities
    print("\n🔧 Step 3: Using utilities")
    
    # Generate a secure password
    secure_password = generate_password(16, include_symbols=True)
    print(f"Generated password: {secure_password}")
    
    # Format some file sizes
    file_sizes = [1024, 1048576, 1073741824]
    print("File sizes:")
    for size in file_sizes:
        formatted = format_bytes(size)
        print(f"  {size} bytes = {formatted}")
    
    # Step 4: Save our results
    print("\n💾 Step 4: Saving results")
    
    # Create a summary of what we did
    summary = {
        "tutorial": "Getting Started with Python Helpers",
        "steps_completed": [
            "Created project directory",
            "Generated configuration file",
            "Cleaned messy data",
            "Calculated statistics",
            "Generated secure password",
            "Formatted file sizes"
        ],
        "clean_data_count": len(clean_records),
        "average_score": stats.get('mean', 0) if scores else 0,
        "password_generated": True
    }
    
    summary_file = project_dir / "tutorial_summary.json"
    if write_json(summary, summary_file):
        print(f"Tutorial summary saved to: {summary_file}")
    
    print(f"\n✅ Tutorial completed successfully!")
    print(f"Check the '{project_dir}' directory for generated files.")

if __name__ == "__main__":
    main()
```

## Step 3: Run Your Script

Save the script and run it:

```bash
python my_first_helper_script.py
```

You should see output showing each step of the process, and a new directory called `my_helper_project` will be created with your generated files.

## Step 4: Explore What You Created

Look at the files that were created:

1. **config.json**: Contains your project configuration with a generated API key
2. **tutorial_summary.json**: Contains a summary of what the script accomplished

Open these files in your text editor to see the JSON data that was created.

## Step 5: Understanding What Happened

Let's break down what your script did:

### File Operations
- **`ensure_directory()`**: Created a directory safely (won't fail if it already exists)
- **`write_json()` and `read_json()`**: Handled JSON files with proper error handling

### Data Processing
- **`clean_data()`**: Cleaned messy data by removing empty values and stripping whitespace
- **`calculate_stats()`**: Calculated statistical measures from numeric data

### Utilities
- **`generate_password()`**: Created a secure password
- **`format_bytes()`**: Formatted file sizes in human-readable format

## Common Patterns You Learned

1. **Safe File Operations**: Always use the helper functions instead of raw file operations
2. **Data Validation**: Clean and validate data before processing
3. **Error Handling**: The helper functions handle errors gracefully
4. **Configuration Management**: Use JSON files for storing configuration

## Next Steps

Now that you've completed your first tutorial, you can:

1. **Try More Examples**: Run other scripts in the `examples/` directory
2. **Modify the Script**: Change the data processing logic or add new features
3. **Learn More Modules**: Explore web scraping and automation features
4. **Build a Project**: Use the helpers in a real project

## Troubleshooting

### Common Issues:

**Import Error**: If you get import errors, make sure you're running the script from the correct directory and that all dependencies are installed.

**Permission Error**: On some systems, you might need to run with different permissions or choose a different directory for file operations.

**Module Not Found**: Ensure the `sys.path.insert()` line is correct and points to the right directory.

## What's Next?

In the next tutorial, we'll dive deeper into:
- Web scraping with the `web_scraping` module
- Task automation with the `automation` module
- Building more complex data processing pipelines

## Practice Exercises

Try these exercises to reinforce what you learned:

1. **Modify the data**: Change the sample data to include your own information
2. **Add more statistics**: Calculate additional statistics like standard deviation
3. **Create a backup**: Use the file operations to create backup copies of your files
4. **Generate multiple configs**: Create configuration files for different environments

## Summary

Congratulations! You've successfully:
- ✅ Set up the Python Helpers library
- ✅ Used file operations to create directories and handle JSON files
- ✅ Processed and cleaned messy data
- ✅ Generated secure passwords and formatted file sizes
- ✅ Created a complete working script

You're now ready to explore more advanced features of the Python Helpers library!