"""
Automation Module

Utilities for task automation and scheduling.
"""

import time
import subprocess
from typing import List, Dict, Any, Optional, Callable
import os
from datetime import datetime, timedelta
import json


def run_command(command: str, shell: bool = True, capture_output: bool = True) -> Dict[str, Any]:
    """
    Run a system command and capture its output.
    
    Args:
        command: Command to execute
        shell: Whether to run through shell
        capture_output: Whether to capture stdout/stderr
        
    Returns:
        Dictionary with command results
    """
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            capture_output=capture_output, 
            text=True, 
            timeout=300  # 5 minute timeout
        )
        
        return {
            'success': result.returncode == 0,
            'return_code': result.returncode,
            'stdout': result.stdout if capture_output else '',
            'stderr': result.stderr if capture_output else '',
            'command': command
        }
        
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'return_code': -1,
            'stdout': '',
            'stderr': 'Command timed out',
            'command': command
        }
    except Exception as e:
        return {
            'success': False,
            'return_code': -1,
            'stdout': '',
            'stderr': str(e),
            'command': command
        }


def batch_commands(commands: List[str], continue_on_error: bool = True) -> List[Dict[str, Any]]:
    """
    Execute multiple commands in sequence.
    
    Args:
        commands: List of commands to execute
        continue_on_error: Whether to continue if a command fails
        
    Returns:
        List of command results
    """
    results = []
    
    for command in commands:
        result = run_command(command)
        results.append(result)
        
        if not result['success'] and not continue_on_error:
            break
            
    return results


def schedule_task(func: Callable, interval_seconds: int, max_runs: int = None) -> None:
    """
    Simple task scheduler that runs a function at regular intervals.
    
    Args:
        func: Function to execute
        interval_seconds: Seconds between executions
        max_runs: Maximum number of runs (None for infinite)
    """
    runs = 0
    
    while max_runs is None or runs < max_runs:
        try:
            func()
            runs += 1
            
            if max_runs is None or runs < max_runs:
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("Task scheduling interrupted by user")
            break
        except Exception as e:
            print(f"Error in scheduled task: {e}")
            time.sleep(interval_seconds)


def monitor_directory(directory: str, callback: Callable[[str], None], 
                     interval: int = 5) -> None:
    """
    Monitor a directory for changes and call callback when files change.
    
    Args:
        directory: Directory to monitor
        callback: Function to call with filename when change detected
        interval: Seconds between checks
    """
    try:
        import time
        
        # Get initial state
        initial_state = {}
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    initial_state[filepath] = os.path.getmtime(filepath)
                except OSError:
                    continue
        
        print(f"Monitoring {directory} for changes (Ctrl+C to stop)...")
        
        while True:
            time.sleep(interval)
            
            current_state = {}
            
            # Check current state
            for root, dirs, files in os.walk(directory):
                for file in files:
                    filepath = os.path.join(root, file)
                    try:
                        current_state[filepath] = os.path.getmtime(filepath)
                    except OSError:
                        continue
            
            # Find changes
            for filepath, mtime in current_state.items():
                if filepath not in initial_state or initial_state[filepath] != mtime:
                    callback(filepath)
                    initial_state[filepath] = mtime
            
            # Check for deleted files
            for filepath in list(initial_state.keys()):
                if filepath not in current_state:
                    callback(f"DELETED: {filepath}")
                    del initial_state[filepath]
                    
    except KeyboardInterrupt:
        print("Directory monitoring stopped")
    except Exception as e:
        print(f"Error monitoring directory: {e}")


def backup_files(source_paths: List[str], backup_dir: str, 
                compress: bool = False) -> Dict[str, Any]:
    """
    Create backups of specified files/directories.
    
    Args:
        source_paths: List of files/directories to backup
        backup_dir: Directory to store backups
        compress: Whether to compress the backup
        
    Returns:
        Dictionary with backup results
    """
    import shutil
    from pathlib import Path
    
    try:
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = {'success': True, 'backed_up': [], 'errors': []}
        
        for source in source_paths:
            source_path = Path(source)
            
            if not source_path.exists():
                results['errors'].append(f"Source not found: {source}")
                continue
            
            # Create backup filename
            backup_name = f"{source_path.name}_{timestamp}"
            backup_target = backup_path / backup_name
            
            try:
                if source_path.is_file():
                    shutil.copy2(source_path, backup_target)
                else:
                    shutil.copytree(source_path, backup_target)
                
                results['backed_up'].append(str(backup_target))
                
            except Exception as e:
                results['errors'].append(f"Error backing up {source}: {e}")
        
        if results['errors']:
            results['success'] = len(results['backed_up']) > 0
            
        return results
        
    except Exception as e:
        return {'success': False, 'backed_up': [], 'errors': [str(e)]}


def cleanup_old_files(directory: str, days_old: int = 30, 
                     pattern: str = "*") -> Dict[str, Any]:
    """
    Clean up old files in a directory.
    
    Args:
        directory: Directory to clean
        days_old: Files older than this many days will be deleted
        pattern: File pattern to match (e.g., "*.log", "*.tmp")
        
    Returns:
        Dictionary with cleanup results
    """
    from pathlib import Path
    
    try:
        dir_path = Path(directory)
        
        if not dir_path.exists():
            return {'success': False, 'deleted': [], 'errors': ['Directory not found']}
        
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        results = {'success': True, 'deleted': [], 'errors': []}
        
        for file_path in dir_path.glob(pattern):
            if file_path.is_file():
                try:
                    if file_path.stat().st_mtime < cutoff_time:
                        file_path.unlink()
                        results['deleted'].append(str(file_path))
                except Exception as e:
                    results['errors'].append(f"Error deleting {file_path}: {e}")
        
        return results
        
    except Exception as e:
        return {'success': False, 'deleted': [], 'errors': [str(e)]}


# Export main functions
__all__ = [
    'run_command',
    'batch_commands',
    'schedule_task',
    'monitor_directory',
    'backup_files',
    'cleanup_old_files'
]