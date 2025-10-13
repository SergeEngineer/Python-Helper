"""
Setup configuration for Python Helpers Library
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f 
                   if line.strip() and not line.startswith('#')]

setup(
    name="python-helpers",
    version="0.1.0",
    author="Serge",
    description="A collection of useful Python utilities and helper functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/Python-Helper",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies only
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
            'mypy>=1.5.0',
        ],
        'data': [
            'pandas>=2.0.0',
            'numpy>=1.24.0',
        ],
        'docs': [
            'sphinx>=7.1.0',
            'sphinx-rtd-theme>=1.3.0',
        ],
    },
    entry_points={
        'console_scripts': [
            # Add command-line scripts here if needed
            # 'python-helpers=python_helpers.cli:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)