"""
Unit tests for the utilities module.
"""

import pytest
import re
from datetime import datetime, timedelta
from python_helpers.utilities import (
    generate_password,
    generate_uuid,
    hash_string,
    validate_email,
    clean_filename,
    format_bytes,
    time_ago,
    flatten_dict,
    chunk_list,
    remove_duplicates,
    retry_operation
)


@pytest.mark.unit
class TestPasswordGeneration:
    """Tests for password generation."""
    
    def test_default_password_generation(self):
        """Test default password generation."""
        password = generate_password()
        
        assert len(password) == 12
        assert isinstance(password, str)
        # Should contain letters, digits, and symbols
        assert any(c.isalpha() for c in password)
        assert any(c.isdigit() for c in password)
    
    def test_custom_length_password(self):
        """Test password generation with custom length."""
        password = generate_password(length=20)
        
        assert len(password) == 20
    
    def test_password_without_symbols(self):
        """Test password generation without symbols."""
        password = generate_password(include_symbols=False)
        
        # Should only contain letters and digits
        assert password.isalnum()
    
    def test_password_uniqueness(self):
        """Test that generated passwords are unique."""
        passwords = [generate_password() for _ in range(10)]
        
        # All passwords should be different
        assert len(set(passwords)) == 10


@pytest.mark.unit
class TestUUIDGeneration:
    """Tests for UUID generation."""
    
    def test_uuid4_generation(self):
        """Test UUID v4 generation."""
        uuid_str = generate_uuid(4)
        
        assert isinstance(uuid_str, str)
        assert len(uuid_str) == 36  # Standard UUID length
        assert uuid_str.count('-') == 4
    
    def test_uuid1_generation(self):
        """Test UUID v1 generation."""
        uuid_str = generate_uuid(1)
        
        assert isinstance(uuid_str, str)
        assert len(uuid_str) == 36
    
    def test_uuid_uniqueness(self):
        """Test that generated UUIDs are unique."""
        uuids = [generate_uuid() for _ in range(10)]
        
        assert len(set(uuids)) == 10


@pytest.mark.unit
class TestHashString:
    """Tests for string hashing."""
    
    def test_sha256_hash(self):
        """Test SHA256 hashing."""
        text = "Hello, World!"
        hash_result = hash_string(text, "sha256")
        
        assert isinstance(hash_result, str)
        assert len(hash_result) == 64  # SHA256 hex length
        
        # Same input should produce same hash
        assert hash_string(text, "sha256") == hash_result
    
    def test_md5_hash(self):
        """Test MD5 hashing."""
        text = "Hello, World!"
        hash_result = hash_string(text, "md5")
        
        assert isinstance(hash_result, str)
        assert len(hash_result) == 32  # MD5 hex length
    
    def test_invalid_algorithm_fallback(self):
        """Test fallback to SHA256 for invalid algorithm."""
        text = "Hello, World!"
        hash_result = hash_string(text, "invalid_algorithm")
        
        # Should fallback to SHA256
        assert len(hash_result) == 64
        assert hash_result == hash_string(text, "sha256")


@pytest.mark.unit
class TestValidateEmail:
    """Tests for email validation."""
    
    def test_valid_emails(self):
        """Test with valid email addresses."""
        valid_emails = [
            "user@example.com",
            "test.email@domain.org",
            "user+tag@example.com",
            "user123@example.co.uk"
        ]
        
        for email in valid_emails:
            assert validate_email(email) is True
    
    def test_invalid_emails(self):
        """Test with invalid email addresses."""
        invalid_emails = [
            "invalid_email",
            "@example.com",
            "user@",
            "user@.com",
            "user..user@example.com",
            ""
        ]
        
        for email in invalid_emails:
            assert validate_email(email) is False


@pytest.mark.unit
class TestCleanFilename:
    """Tests for filename cleaning."""
    
    def test_clean_invalid_characters(self):
        """Test cleaning invalid characters."""
        dirty_name = "file<>:\"/\\|?*name.txt"
        clean_name = clean_filename(dirty_name)
        
        assert clean_name == "file_________name.txt"
    
    def test_strip_dots_and_spaces(self):
        """Test stripping leading/trailing dots and spaces."""
        dirty_name = "  ...filename...  "
        clean_name = clean_filename(dirty_name)
        
        assert clean_name == "filename"
    
    def test_empty_filename_handling(self):
        """Test handling of empty filename."""
        clean_name = clean_filename("")
        
        assert clean_name == "unnamed_file"
    
    def test_custom_replacement(self):
        """Test custom replacement character."""
        dirty_name = "file<>name.txt"
        clean_name = clean_filename(dirty_name, replacement="-")
        
        assert clean_name == "file--name.txt"


@pytest.mark.unit
class TestFormatBytes:
    """Tests for byte formatting."""
    
    def test_bytes_formatting(self):
        """Test various byte size formatting."""
        test_cases = [
            (0, "0.0 B"),
            (512, "512.0 B"),
            (1024, "1.0 KB"),
            (1536, "1.5 KB"),
            (1048576, "1.0 MB"),
            (1073741824, "1.0 GB"),
            (1099511627776, "1.0 TB")
        ]
        
        for bytes_size, expected in test_cases:
            assert format_bytes(bytes_size) == expected


@pytest.mark.unit
class TestTimeAgo:
    """Tests for time ago formatting."""
    
    def test_days_ago(self):
        """Test days ago formatting."""
        timestamp = datetime.now() - timedelta(days=5)
        result = time_ago(timestamp)
        
        assert "5 days ago" in result
    
    def test_hours_ago(self):
        """Test hours ago formatting."""
        timestamp = datetime.now() - timedelta(hours=3)
        result = time_ago(timestamp)
        
        assert "3 hours ago" in result
    
    def test_minutes_ago(self):
        """Test minutes ago formatting."""
        timestamp = datetime.now() - timedelta(minutes=30)
        result = time_ago(timestamp)
        
        assert "30 minutes ago" in result
    
    def test_just_now(self):
        """Test just now formatting."""
        timestamp = datetime.now() - timedelta(seconds=30)
        result = time_ago(timestamp)
        
        assert result == "Just now"


@pytest.mark.unit
class TestFlattenDict:
    """Tests for dictionary flattening."""
    
    def test_simple_flatten(self):
        """Test simple dictionary flattening."""
        nested_dict = {
            "a": 1,
            "b": {
                "c": 2,
                "d": 3
            }
        }
        
        flattened = flatten_dict(nested_dict)
        expected = {
            "a": 1,
            "b.c": 2,
            "b.d": 3
        }
        
        assert flattened == expected
    
    def test_custom_separator(self):
        """Test flattening with custom separator."""
        nested_dict = {"a": {"b": 1}}
        flattened = flatten_dict(nested_dict, separator="_")
        
        assert flattened == {"a_b": 1}
    
    def test_list_flattening(self):
        """Test flattening with lists."""
        nested_dict = {
            "items": [1, 2, {"nested": "value"}]
        }
        
        flattened = flatten_dict(nested_dict)
        expected = {
            "items.0": 1,
            "items.1": 2,
            "items.2.nested": "value"
        }
        
        assert flattened == expected


@pytest.mark.unit
class TestChunkList:
    """Tests for list chunking."""
    
    def test_even_chunks(self):
        """Test chunking with even division."""
        lst = [1, 2, 3, 4, 5, 6]
        chunks = chunk_list(lst, 2)
        
        expected = [[1, 2], [3, 4], [5, 6]]
        assert chunks == expected
    
    def test_uneven_chunks(self):
        """Test chunking with uneven division."""
        lst = [1, 2, 3, 4, 5]
        chunks = chunk_list(lst, 2)
        
        expected = [[1, 2], [3, 4], [5]]
        assert chunks == expected
    
    def test_chunk_larger_than_list(self):
        """Test chunk size larger than list."""
        lst = [1, 2, 3]
        chunks = chunk_list(lst, 5)
        
        expected = [[1, 2, 3]]
        assert chunks == expected


@pytest.mark.unit
class TestRemoveDuplicates:
    """Tests for duplicate removal."""
    
    def test_remove_duplicates_preserve_order(self):
        """Test removing duplicates while preserving order."""
        lst = [1, 2, 2, 3, 1, 4]
        result = remove_duplicates(lst, preserve_order=True)
        
        assert result == [1, 2, 3, 4]
    
    def test_remove_duplicates_no_order(self):
        """Test removing duplicates without preserving order."""
        lst = [1, 2, 2, 3, 1, 4]
        result = remove_duplicates(lst, preserve_order=False)
        
        # Should contain same elements but order may vary
        assert set(result) == {1, 2, 3, 4}
        assert len(result) == 4
    
    def test_no_duplicates(self):
        """Test with list that has no duplicates."""
        lst = [1, 2, 3, 4]
        result = remove_duplicates(lst)
        
        assert result == lst


@pytest.mark.unit
class TestRetryOperation:
    """Tests for retry operation."""
    
    def test_successful_operation(self):
        """Test successful operation on first try."""
        def success_func():
            return "success"
        
        result = retry_operation(success_func)
        assert result == "success"
    
    def test_operation_succeeds_after_retries(self):
        """Test operation that succeeds after failures."""
        call_count = {"count": 0}
        
        def failing_then_success():
            call_count["count"] += 1
            if call_count["count"] < 3:
                raise Exception("Temporary failure")
            return "success"
        
        result = retry_operation(failing_then_success, max_attempts=3)
        assert result == "success"
        assert call_count["count"] == 3
    
    def test_operation_fails_all_attempts(self):
        """Test operation that fails all attempts."""
        def always_fail():
            raise Exception("Always fails")
        
        with pytest.raises(Exception, match="Always fails"):
            retry_operation(always_fail, max_attempts=2)