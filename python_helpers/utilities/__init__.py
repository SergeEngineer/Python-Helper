"""
Utilities Module

General purpose utility functions.
"""

import re
import hashlib
import secrets
import string
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
import uuid


def generate_password(length: int = 12, include_symbols: bool = True) -> str:
    """
    Generate a secure random password.
    
    Args:
        length: Password length
        include_symbols: Whether to include special characters
        
    Returns:
        Generated password string
    """
    characters = string.ascii_letters + string.digits
    
    if include_symbols:
        characters += "!@#$%^&*"
    
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_uuid(version: int = 4) -> str:
    """
    Generate a UUID string.
    
    Args:
        version: UUID version (1 or 4)
        
    Returns:
        UUID string
    """
    if version == 1:
        return str(uuid.uuid1())
    else:
        return str(uuid.uuid4())


def hash_string(text: str, algorithm: str = 'sha256') -> str:
    """
    Hash a string using specified algorithm.
    
    Args:
        text: String to hash
        algorithm: Hash algorithm ('md5', 'sha1', 'sha256', 'sha512')
        
    Returns:
        Hexadecimal hash string
    """
    try:
        hash_obj = hashlib.new(algorithm)
        hash_obj.update(text.encode('utf-8'))
        return hash_obj.hexdigest()
    except ValueError:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()


def validate_email(email: str) -> bool:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def clean_filename(filename: str, replacement: str = '_') -> str:
    """
    Clean filename by removing/replacing invalid characters.
    
    Args:
        filename: Original filename
        replacement: Character to replace invalid chars with
        
    Returns:
        Cleaned filename
    """
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*]'
    cleaned = re.sub(invalid_chars, replacement, filename)
    
    # Remove leading/trailing dots and spaces
    cleaned = cleaned.strip('. ')
    
    # Ensure it's not empty
    if not cleaned:
        cleaned = 'unnamed_file'
    
    return cleaned


def format_bytes(bytes_size: int) -> str:
    """
    Format bytes into human readable string.
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted string (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"


def time_ago(timestamp: datetime) -> str:
    """
    Get human readable time difference from now.
    
    Args:
        timestamp: DateTime to compare
        
    Returns:
        Human readable time difference
    """
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    
    hours = diff.seconds // 3600
    if hours > 0:
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    
    minutes = diff.seconds // 60
    if minutes > 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    
    return "Just now"


def flatten_dict(nested_dict: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested dictionary.
    
    Args:
        nested_dict: Dictionary to flatten
        separator: Separator for nested keys
        
    Returns:
        Flattened dictionary
    """
    def _flatten(obj, parent_key=''):
        items = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                new_key = f"{parent_key}{separator}{key}" if parent_key else key
                items.extend(_flatten(value, new_key).items())
        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                new_key = f"{parent_key}{separator}{i}" if parent_key else str(i)
                items.extend(_flatten(value, new_key).items())
        else:
            return {parent_key: obj}
            
        return dict(items)
    
    return _flatten(nested_dict)


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.
    
    Args:
        lst: List to chunk
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def remove_duplicates(lst: List[Any], preserve_order: bool = True) -> List[Any]:
    """
    Remove duplicates from a list.
    
    Args:
        lst: List to process
        preserve_order: Whether to preserve original order
        
    Returns:
        List without duplicates
    """
    if preserve_order:
        seen = set()
        return [x for x in lst if not (x in seen or seen.add(x))]
    else:
        return list(set(lst))


def retry_operation(func, max_attempts: int = 3, delay: float = 1.0, 
                   backoff: float = 2.0) -> Any:
    """
    Retry an operation with exponential backoff.
    
    Args:
        func: Function to retry
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts
        backoff: Backoff multiplier
        
    Returns:
        Function result if successful
        
    Raises:
        Exception: If all attempts fail
    """
    import time
    
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            last_exception = e
            
            if attempt < max_attempts - 1:
                time.sleep(delay)
                delay *= backoff
            else:
                raise last_exception


# Export main functions
__all__ = [
    'generate_password',
    'generate_uuid',
    'hash_string',
    'validate_email',
    'clean_filename',
    'format_bytes',
    'time_ago',
    'flatten_dict',
    'chunk_list',
    'remove_duplicates',
    'retry_operation'
]