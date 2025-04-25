#!/usr/bin/env python3
"""
Unit tests for the WordCount CLI functionality.
"""

import os
import sys
import unittest
import tempfile
import json
import subprocess
from unittest.mock import patch

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestWordCountCLI(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        
        # Create a sample input file with film reviews
        self.input_file = os.path.join(self.temp_dir.name, "sample_reviews.jsonl")
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write('{"id": 1, "text": "This film was excellent and entertaining."}\n')
            f.write('{"id": 2, "text": "I hated this movie, it was terrible."}\n')
            f.write('{"id": 3, "text": "The acting was good but the plot was confusing."}\n')
        
        # Path to the output file
        self.output_file = os.path.join(self.temp_dir.name, "wordcount_output.txt")
        
        # Path to the mapper and reducer scripts
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.mapper_path = os.path.join(self.project_root, "src", "mapreduce", "mapper_wordcount.py")
        self.reducer_path = os.path.join(self.project_root, "src", "mapreduce", "reducer_wordcount.py")
        self.run_script_path = os.path.join(self.project_root, "src", "mapreduce", "run_wordcount.py")
    
    def tearDown(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    def test_mapper_output_format(self):
        """Test that the mapper produces correctly formatted output."""
        # Run the mapper on the sample input
        result = subprocess.run(
            f"cat {self.input_file} | python {self.mapper_path}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        # Check that the command succeeded
        self.assertEqual(result.returncode, 0, f"Mapper failed: {result.stderr}")
        
        # Check the output format
        lines = result.stdout.strip().split("\n")
        self.assertTrue(len(lines) > 0, "Mapper produced no output")
        
        for line in lines:
            parts = line.split("\t")
            self.assertEqual(len(parts), 2, f"Invalid mapper output format: {line}")
            self.assertEqual(parts[1], "1", f"Mapper count should be 1: {line}")
    
    def test_reducer_output_format(self):
        """Test that the reducer produces correctly formatted output."""
        # Create sample mapper output
        mapper_output = "film\t1\nfilm\t1\nwas\t1\nwas\t1\nwas\t1\ngood\t1\n"
        
        # Run the reducer on the sample mapper output
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(mapper_output)
            temp_file_path = temp_file.name
        
        result = subprocess.run(
            f"cat {temp_file_path} | sort | python {self.reducer_path}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        os.unlink(temp_file_path)
        
        # Check that the command succeeded
        self.assertEqual(result.returncode, 0, f"Reducer failed: {result.stderr}")
        
        # Check the output format
        lines = result.stdout.strip().split("\n")
        self.assertTrue(len(lines) > 0, "Reducer produced no output")
        
        expected_counts = {"film": 2, "was": 3, "good": 1}
        actual_counts = {}
        
        for line in lines:
            parts = line.split("\t")
            self.assertEqual(len(parts), 2, f"Invalid reducer output format: {line}")
            word, count = parts
            actual_counts[word] = int(count)
        
        for word, expected_count in expected_counts.items():
            self.assertEqual(actual_counts.get(word), expected_count, 
                            f"Count for '{word}' should be {expected_count}")
    
    def test_end_to_end_wordcount(self):
        """Test the entire WordCount pipeline from input to output."""
        # Run the WordCount job
        result = subprocess.run(
            f"python {self.run_script_path} -i {self.input_file} -o {self.output_file}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        # Check that the command succeeded
        self.assertEqual(result.returncode, 0, f"WordCount job failed: {result.stderr}")
        
        # Check that the output file exists
        self.assertTrue(os.path.exists(self.output_file), "Output file was not created")
        
        # Check the content of the output file
        with open(self.output_file, "r", encoding="utf-8") as f:
            lines = f.read().strip().split("\n")
        
        self.assertTrue(len(lines) > 0, "Output file is empty")
        
        # Check some expected words and their counts
        word_counts = {}
        for line in lines:
            parts = line.split("\t")
            self.assertEqual(len(parts), 2, f"Invalid output format: {line}")
            word, count = parts
            word_counts[word] = int(count)
        
        expected_words = ["film", "was", "good", "plot", "movie", "excellent"]
        for word in expected_words:
            self.assertIn(word, word_counts, f"Expected word '{word}' not found in output")
            self.assertTrue(word_counts[word] > 0, f"Count for '{word}' should be positive")

if __name__ == "__main__":
    unittest.main()