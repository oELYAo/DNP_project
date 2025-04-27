"""
Unit tests for data ingestion and preprocessing functionality.
"""

import json
import os
import tempfile
import unittest
from typing import Dict, List

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.data_ingestion import (
    read_records,
    clean_text,
    tokenize,
    preprocess_document,
    load_and_preprocess
)


class TestDataIngestion(unittest.TestCase):
    def setUp(self):
        """Set up temporary test files."""
        # Create temporary directory
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create sample text file
        self.text_file = os.path.join(self.temp_dir.name, "sample.txt")
        with open(self.text_file, "w") as f:
            f.write("Line 1 text document.\n")
            f.write("Line 2 with @mention and #hashtag.\n")
            f.write("Line 3 with URL https://example.com and punctuation!!\n")
        
        # Create sample CSV file
        self.csv_file = os.path.join(self.temp_dir.name, "sample.csv")
        with open(self.csv_file, "w") as f:
            f.write("id,text\n")
            f.write("1,CSV row 1\n")
            f.write("2,CSV row 2 with special chars!@#\n")
            f.write(",CSV row with no ID\n")
        
        # Create sample JSON file
        self.json_file = os.path.join(self.temp_dir.name, "sample.json")
        with open(self.json_file, "w") as f:
            f.write('{"id": 1, "text": "JSON doc 1"}\n')
            f.write('{"id": 2, "text": "JSON doc 2 with special chars!@#"}\n')
            f.write('{"text": "JSON doc with no ID"}\n')
            f.write('{"id": 4, "content": "JSON doc with content field"}\n')
    
    def tearDown(self):
        """Clean up temporary files."""
        self.temp_dir.cleanup()
    
    def test_read_records_txt(self):
        """Test reading records from a text file."""
        records = list(read_records(self.text_file))
        
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["id"], 0)
        self.assertEqual(records[0]["text"], "Line 1 text document.")
        self.assertEqual(records[1]["id"], 1)
        self.assertEqual(records[2]["id"], 2)
    
    def test_read_records_csv(self):
        """Test reading records from a CSV file."""
        records = list(read_records(self.csv_file))
        
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0]["id"], "1")
        self.assertEqual(records[0]["text"], "CSV row 1")
        self.assertEqual(records[1]["id"], "2")
        self.assertEqual(records[2]["id"], 0)  # Auto-generated ID
    
    def test_read_records_json(self):
        """Test reading records from a JSON file."""
        records = list(read_records(self.json_file))
        
        self.assertEqual(len(records), 4)
        self.assertEqual(records[0]["id"], 1)
        self.assertEqual(records[0]["text"], "JSON doc 1")
        self.assertEqual(records[1]["id"], 2)
        self.assertEqual(records[2]["id"], 0)  # Auto-generated ID
        self.assertEqual(records[3]["id"], 4)
        self.assertEqual(records[3]["text"], "JSON doc with content field")
    
    def test_clean_text(self):
        """Test text cleaning functionality."""
        text = "@user This is a #hashtag test with URL https://example.com and punctuation!!!"
        cleaned = clean_text(text)
        
        self.assertNotIn("@user", cleaned)
        self.assertNotIn("#hashtag", cleaned)
        self.assertNotIn("https://", cleaned)
        self.assertNotIn("!!!", cleaned)
        self.assertEqual(cleaned, "this is a test with url and punctuation")
    
    def test_tokenize(self):
        """Test tokenization functionality."""
        text = "this is a test with short words"
        tokens = tokenize(text)
        
        self.assertIn("this", tokens)
        self.assertIn("test", tokens)
        self.assertIn("with", tokens)
        self.assertIn("short", tokens)
        self.assertIn("words", tokens)
        # 'a' should be filtered out as it's a single character
        self.assertNotIn("a", tokens)
    
    def test_preprocess_document(self):
        """Test document preprocessing."""
        doc = {"id": 1, "text": "This is a Test with @mention and #hashtag!"}
        processed = preprocess_document(doc)
        
        self.assertEqual(processed["id"], 1)
        self.assertEqual(processed["text"], doc["text"])
        self.assertIn("clean_text", processed)
        self.assertIn("tokens", processed)
        self.assertNotIn("@mention", processed["clean_text"])
        self.assertNotIn("#hashtag", processed["clean_text"])
        self.assertIn("test", processed["tokens"])
    
    def test_load_and_preprocess(self):
        """Test end-to-end loading and preprocessing."""
        docs = list(load_and_preprocess(self.text_file))
        
        self.assertEqual(len(docs), 3)
        for doc in docs:
            self.assertIn("id", doc)
            self.assertIn("text", doc)
            self.assertIn("clean_text", doc)
            self.assertIn("tokens", doc)


if __name__ == "__main__":
    unittest.main()
