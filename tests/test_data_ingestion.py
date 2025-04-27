"""
Tests for the data ingestion module.
"""

import os
import pytest
import tempfile
import json
import csv
from src.utils.data_ingestion import read_records, clean_text, tokenize, preprocess_document, load_and_preprocess

# Test data
SAMPLE_TEXT = "This is a sample text with @mentions and #hashtags and https://example.com links."
EXPECTED_CLEAN = "this is a sample text with  and  and  links"

class TestDataIngestion:
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        # Test normal text
        assert clean_text(SAMPLE_TEXT) == EXPECTED_CLEAN
        
        # Test empty text
        assert clean_text("") == ""
        
        # Test None input
        assert clean_text(None) == ""
        
        # Test non-string input
        assert clean_text(123) == "123"
        
        # Test very long text
        long_text = "a" * 200000
        cleaned = clean_text(long_text)
        assert len(cleaned) == 100000  # Should be truncated
    
    def test_tokenize(self):
        """Test tokenization functionality."""
        # Test normal text
        tokens = tokenize("This is a sample text")
        assert "sample" in tokens
        assert "text" in tokens
        assert "is" not in tokens  # Should be removed as stopword
        assert "a" not in tokens  # Should be removed as stopword
        
        # Test empty text
        assert tokenize("") == []
        
        # Test text with only stopwords
        assert tokenize("a the is") == []
    
    def test_read_records_json(self):
        """Test reading JSON records."""
        with tempfile.NamedTemporaryFile(suffix='.json', mode='w+', delete=False) as f:
            f.write('{"id": 1, "text": "Sample text 1"}\n')
            f.write('{"id": 2, "text": "Sample text 2"}\n')
            f.write('{"content": "Sample text 3"}\n')  # Alternative field
            f.write('{"id": 4}\n')  # Missing text field
            temp_path = f.name
        
        try:
            records = list(read_records(temp_path))
            assert len(records) == 4
            assert records[0]['id'] == 1
            assert records[0]['text'] == "Sample text 1"
            assert records[2]['text'] == "Sample text 3"  # Should use 'content' field
            assert records[3]['text'] == ""  # Should have empty text
        finally:
            os.unlink(temp_path)
    
    def test_read_records_csv(self):
        """Test reading CSV records."""
        with tempfile.NamedTemporaryFile(suffix='.csv', mode='w+', delete=False) as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'text'])
            writer.writerow(['1', 'Sample text 1'])
            writer.writerow(['2', 'Sample text 2'])
            writer.writerow(['', 'Sample text 3'])  # Empty ID
            temp_path = f.name
        
        try:
            records = list(read_records(temp_path))
            assert len(records) == 3
            assert records[0]['id'] == '1'
            assert records[0]['text'] == "Sample text 1"
            assert records[2]['id'] == 2  # Should be auto-assigned
        finally:
            os.unlink(temp_path)
    
    def test_read_records_txt(self):
        """Test reading TXT records."""
        with tempfile.NamedTemporaryFile(suffix='.txt', mode='w+', delete=False) as f:
            f.write("Line 1\n")
            f.write("Line 2\n")
            f.write("\n")  # Empty line should be skipped
            f.write("Line 3\n")
            temp_path = f.name
        
        try:
            records = list(read_records(temp_path))
            assert len(records) == 3
            assert records[0]['id'] == 0
            assert records[0]['text'] == "Line 1"
        finally:
            os.unlink(temp_path)
    
    def test_empty_file(self):
        """Test handling of empty files."""
        with tempfile.NamedTemporaryFile(suffix='.txt', mode='w+', delete=False) as f:
            temp_path = f.name
        
        try:
            with pytest.raises(Exception) as e:
                list(read_records(temp_path))
            assert "empty" in str(e.value).lower()
        finally:
            os.unlink(temp_path)
    
    def test_malformed_json(self):
        """Test handling of malformed JSON."""
        with tempfile.NamedTemporaryFile(suffix='.json', mode='w+', delete=False) as f:
            f.write('{"id": 1, "text": "Valid JSON"}\n')
            f.write('This is not valid JSON\n')
            temp_path = f.name
        
        try:
            with pytest.raises(Exception) as e:
                list(read_records(temp_path))
            assert "malformed json" in str(e.value).lower()
        finally:
            os.unlink(temp_path)
    
    def test_unsupported_format(self):
        """Test handling of unsupported file formats."""
        with tempfile.NamedTemporaryFile(suffix='.xyz', mode='w+', delete=False) as f:
            f.write("Some content")
            temp_path = f.name
        
        try:
            with pytest.raises(ValueError) as e:
                list(read_records(temp_path))
            assert "unsupported file format" in str(e.value).lower()
        finally:
            os.unlink(temp_path)