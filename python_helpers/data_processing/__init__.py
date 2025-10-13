"""
Data Processing Module

Utilities for data manipulation, analysis, and processing.
"""

from typing import List, Dict, Any, Optional, Union
import csv
from collections import Counter
import statistics
import json


def clean_data(data: List[Dict[str, Any]], 
               remove_empty: bool = True, 
               strip_strings: bool = True) -> List[Dict[str, Any]]:
    """
    Clean data by removing empty values and stripping strings.
    
    Args:
        data: List of dictionaries to clean
        remove_empty: Remove entries with empty/None values
        strip_strings: Strip whitespace from string values
        
    Returns:
        Cleaned list of dictionaries
    """
    cleaned = []
    
    for item in data:
        clean_item = {}
        
        for key, value in item.items():
            # Skip empty values if requested
            if remove_empty and (value is None or value == ""):
                continue
                
            # Strip strings if requested
            if strip_strings and isinstance(value, str):
                value = value.strip()
                
            clean_item[key] = value
            
        # Only add item if it has content after cleaning
        if clean_item:
            cleaned.append(clean_item)
            
    return cleaned


def group_by(data: List[Dict[str, Any]], key: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group list of dictionaries by a specific key.
    
    Args:
        data: List of dictionaries to group
        key: Key to group by
        
    Returns:
        Dictionary with grouped data
    """
    groups = {}
    
    for item in data:
        if key in item:
            group_key = item[key]
            
            if group_key not in groups:
                groups[group_key] = []
                
            groups[group_key].append(item)
            
    return groups


def filter_data(data: List[Dict[str, Any]], 
                filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filter data based on key-value pairs.
    
    Args:
        data: List of dictionaries to filter
        filters: Dictionary of key-value pairs to filter by
        
    Returns:
        Filtered list of dictionaries
    """
    filtered = []
    
    for item in data:
        match = True
        
        for filter_key, filter_value in filters.items():
            if filter_key not in item or item[filter_key] != filter_value:
                match = False
                break
                
        if match:
            filtered.append(item)
            
    return filtered


def get_unique_values(data: List[Dict[str, Any]], key: str) -> List[Any]:
    """
    Get unique values for a specific key across all dictionaries.
    
    Args:
        data: List of dictionaries
        key: Key to extract unique values for
        
    Returns:
        List of unique values
    """
    values = set()
    
    for item in data:
        if key in item and item[key] is not None:
            values.add(item[key])
            
    return list(values)


def calculate_stats(values: List[Union[int, float]]) -> Dict[str, float]:
    """
    Calculate basic statistics for a list of numbers.
    
    Args:
        values: List of numeric values
        
    Returns:
        Dictionary with statistical measures
    """
    if not values:
        return {}
    
    numeric_values = [v for v in values if isinstance(v, (int, float))]
    
    if not numeric_values:
        return {}
    
    return {
        'count': len(numeric_values),
        'sum': sum(numeric_values),
        'mean': statistics.mean(numeric_values),
        'median': statistics.median(numeric_values),
        'min': min(numeric_values),
        'max': max(numeric_values),
        'std_dev': statistics.stdev(numeric_values) if len(numeric_values) > 1 else 0
    }


def count_occurrences(data: List[Dict[str, Any]], key: str) -> Dict[Any, int]:
    """
    Count occurrences of values for a specific key.
    
    Args:
        data: List of dictionaries
        key: Key to count values for
        
    Returns:
        Dictionary with value counts
    """
    values = []
    
    for item in data:
        if key in item and item[key] is not None:
            values.append(item[key])
            
    return dict(Counter(values))


def csv_to_dict(file_path: str, delimiter: str = ',') -> List[Dict[str, str]]:
    """
    Convert CSV file to list of dictionaries.
    
    Args:
        file_path: Path to the CSV file
        delimiter: CSV delimiter character
        
    Returns:
        List of dictionaries representing CSV rows
    """
    try:
        with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            return list(reader)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []


def dict_to_csv(data: List[Dict[str, Any]], file_path: str, 
                delimiter: str = ',') -> bool:
    """
    Write list of dictionaries to CSV file.
    
    Args:
        data: List of dictionaries to write
        file_path: Output CSV file path
        delimiter: CSV delimiter character
        
    Returns:
        True if successful, False otherwise
    """
    if not data:
        return False
        
    try:
        fieldnames = list(data[0].keys())
        
        with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, 
                                  delimiter=delimiter)
            writer.writeheader()
            writer.writerows(data)
            
        return True
    except Exception as e:
        print(f"Error writing CSV file: {e}")
        return False


# Export main functions
__all__ = [
    'clean_data',
    'group_by',
    'filter_data',
    'get_unique_values',
    'calculate_stats',
    'count_occurrences',
    'csv_to_dict',
    'dict_to_csv'
]