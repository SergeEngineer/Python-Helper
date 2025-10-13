"""
File Operations Module

Common file and directory operations utilities.
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Union
import json
import csv


def ensure_directory(directory_path: Union[str, Path]) -> Path:
    """
    Create directory if it doesn't exist.
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        Path object of the created/existing directory
    """
    path = Path(directory_path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_copy(source: Union[str, Path], destination: Union[str, Path], 
              overwrite: bool = False) -> bool:
    """
    Safely copy a file with optional overwrite protection.
    
    Args:
        source: Source file path
        destination: Destination file path
        overwrite: Whether to overwrite existing files
        
    Returns:
        True if copy was successful, False otherwise
    """
    try:
        source_path = Path(source)
        dest_path = Path(destination)
        
        if not source_path.exists():
            print(f"Source file {source_path} does not exist")
            return False
            
        if dest_path.exists() and not overwrite:
            print(f"Destination {dest_path} exists. Use overwrite=True to replace.")
            return False
            
        # Ensure destination directory exists
        ensure_directory(dest_path.parent)
        
        shutil.copy2(source_path, dest_path)
        return True
        
    except Exception as e:
        print(f"Error copying file: {e}")
        return False


def find_files(directory: Union[str, Path], pattern: str = "*", 
               recursive: bool = True) -> List[Path]:
    """
    Find files matching a pattern in a directory.
    
    Args:
        directory: Directory to search in
        pattern: File pattern to match (e.g., "*.py", "*.txt")
        recursive: Whether to search subdirectories
        
    Returns:
        List of Path objects matching the pattern
    """
    path = Path(directory)
    
    if not path.exists():
        return []
    
    if recursive:
        return list(path.rglob(pattern))
    else:
        return list(path.glob(pattern))


def read_json(file_path: Union[str, Path]) -> Optional[dict]:
    """
    Safely read a JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary if successful, None if failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON file {file_path}: {e}")
        return None


def write_json(data: dict, file_path: Union[str, Path], indent: int = 2) -> bool:
    """
    Safely write data to a JSON file.
    
    Args:
        data: Dictionary to write
        file_path: Path to the JSON file
        indent: JSON indentation level
        
    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        ensure_directory(path.parent)
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error writing JSON file {file_path}: {e}")
        return False


def get_file_info(file_path: Union[str, Path]) -> Optional[dict]:
    """
    Get detailed information about a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information or None if file doesn't exist
    """
    try:
        path = Path(file_path)
        
        if not path.exists():
            return None
            
        stat = path.stat()
        
        return {
            'name': path.name,
            'size': stat.st_size,
            'modified': stat.st_mtime,
            'created': stat.st_ctime,
            'is_file': path.is_file(),
            'is_directory': path.is_dir(),
            'extension': path.suffix,
            'absolute_path': str(path.absolute())
        }
        
    except Exception as e:
        print(f"Error getting file info: {e}")
        return None


# Export main functions
__all__ = [
    'ensure_directory',
    'safe_copy', 
    'find_files',
    'read_json',
    'write_json',
    'get_file_info'
]