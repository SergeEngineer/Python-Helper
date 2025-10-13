"""
Unit tests for the file_ops module.
"""

import pytest
import json
from pathlib import Path
from python_helpers.file_ops import (
    ensure_directory,
    safe_copy,
    find_files,
    read_json,
    write_json,
    get_file_info
)


@pytest.mark.unit
class TestEnsureDirectory:
    """Tests for ensure_directory function."""
    
    def test_create_new_directory(self, temp_dir):
        """Test creating a new directory."""
        new_dir = temp_dir / "new_directory"
        result = ensure_directory(new_dir)
        
        assert result.exists()
        assert result.is_dir()
        assert result == new_dir
    
    def test_create_nested_directory(self, temp_dir):
        """Test creating nested directories."""
        nested_dir = temp_dir / "level1" / "level2" / "level3"
        result = ensure_directory(nested_dir)
        
        assert result.exists()
        assert result.is_dir()
        assert result == nested_dir
    
    def test_existing_directory(self, temp_dir):
        """Test with existing directory."""
        result = ensure_directory(temp_dir)
        
        assert result.exists()
        assert result.is_dir()
        assert result == temp_dir


@pytest.mark.unit
class TestSafeCopy:
    """Tests for safe_copy function."""
    
    def test_successful_copy(self, sample_files, temp_dir):
        """Test successful file copy."""
        source = sample_files['text']
        dest = temp_dir / "copied.txt"
        
        result = safe_copy(source, dest)
        
        assert result is True
        assert dest.exists()
        assert dest.read_text() == source.read_text()
    
    def test_copy_with_overwrite_false(self, sample_files, temp_dir):
        """Test copy when destination exists and overwrite=False."""
        source = sample_files['text']
        dest = temp_dir / "existing.txt"
        dest.write_text("Existing content")
        
        result = safe_copy(source, dest, overwrite=False)
        
        assert result is False
        assert dest.read_text() == "Existing content"
    
    def test_copy_with_overwrite_true(self, sample_files, temp_dir):
        """Test copy when destination exists and overwrite=True."""
        source = sample_files['text']
        dest = temp_dir / "existing.txt"
        dest.write_text("Existing content")
        
        result = safe_copy(source, dest, overwrite=True)
        
        assert result is True
        assert dest.read_text() == source.read_text()
    
    def test_copy_nonexistent_source(self, temp_dir):
        """Test copy with nonexistent source file."""
        source = temp_dir / "nonexistent.txt"
        dest = temp_dir / "dest.txt"
        
        result = safe_copy(source, dest)
        
        assert result is False
        assert not dest.exists()


@pytest.mark.unit
class TestFindFiles:
    """Tests for find_files function."""
    
    def test_find_all_files(self, sample_files, temp_dir):
        """Test finding all files."""
        files = find_files(temp_dir, "*")
        
        # Should find at least the sample files
        file_names = [f.name for f in files]
        assert "sample.txt" in file_names
        assert "sample.json" in file_names
    
    def test_find_by_extension(self, sample_files, temp_dir):
        """Test finding files by extension."""
        txt_files = find_files(temp_dir, "*.txt")
        
        assert len(txt_files) >= 2  # sample.txt and nested.txt
        for file in txt_files:
            assert file.suffix == ".txt"
    
    def test_find_non_recursive(self, sample_files, temp_dir):
        """Test non-recursive file search."""
        files = find_files(temp_dir, "*.txt", recursive=False)
        
        # Should only find sample.txt, not nested.txt
        file_names = [f.name for f in files]
        assert "sample.txt" in file_names
        assert "nested.txt" not in file_names
    
    def test_find_in_nonexistent_directory(self, temp_dir):
        """Test finding files in nonexistent directory."""
        nonexistent_dir = temp_dir / "nonexistent"
        files = find_files(nonexistent_dir, "*")
        
        assert files == []


@pytest.mark.unit
class TestJsonOperations:
    """Tests for JSON read/write operations."""
    
    def test_write_and_read_json(self, temp_dir, sample_json_data):
        """Test writing and reading JSON data."""
        json_file = temp_dir / "test.json"
        
        # Write JSON
        write_result = write_json(sample_json_data, json_file)
        assert write_result is True
        assert json_file.exists()
        
        # Read JSON
        read_data = read_json(json_file)
        assert read_data == sample_json_data
    
    def test_read_nonexistent_json(self, temp_dir):
        """Test reading nonexistent JSON file."""
        nonexistent_file = temp_dir / "nonexistent.json"
        result = read_json(nonexistent_file)
        
        assert result is None
    
    def test_read_invalid_json(self, temp_dir):
        """Test reading invalid JSON file."""
        invalid_json_file = temp_dir / "invalid.json"
        invalid_json_file.write_text("{ invalid json content")
        
        result = read_json(invalid_json_file)
        
        assert result is None


@pytest.mark.unit
class TestGetFileInfo:
    """Tests for get_file_info function."""
    
    def test_get_file_info_success(self, sample_files):
        """Test getting file info for existing file."""
        file_path = sample_files['text']
        info = get_file_info(file_path)
        
        assert info is not None
        assert info['name'] == 'sample.txt'
        assert info['is_file'] is True
        assert info['is_directory'] is False
        assert info['extension'] == '.txt'
        assert info['size'] > 0
        assert 'absolute_path' in info
        assert 'modified' in info
        assert 'created' in info
    
    def test_get_directory_info(self, temp_dir):
        """Test getting info for directory."""
        info = get_file_info(temp_dir)
        
        assert info is not None
        assert info['is_file'] is False
        assert info['is_directory'] is True
        assert info['extension'] == ''
    
    def test_get_info_nonexistent_file(self, temp_dir):
        """Test getting info for nonexistent file."""
        nonexistent_file = temp_dir / "nonexistent.txt"
        info = get_file_info(nonexistent_file)
        
        assert info is None