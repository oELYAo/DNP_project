"""
Unit tests for the WordCount MapReduce job.
"""

import io
import os
import sys
import unittest
from unittest.mock import patch

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mapreduce.mapper_wordcount import map_words
from src.mapreduce.reducer_wordcount import reduce_counts

class TestWordCount(unittest.TestCase):
    def test_mapper_with_json(self):
        """Test the mapper with JSON input."""
        test_input = '{"text": "This is a test document with some words"}\n'
        
        with patch('sys.stdin', io.StringIO(test_input)), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            map_words()
            
            output = mock_stdout.getvalue().strip().split('\n')
            self.assertIn("this\t1", output)
            self.assertIn("test\t1", output)
            self.assertIn("document\t1", output)
            self.assertIn("with\t1", output)
            self.assertIn("some\t1", output)
            self.assertIn("words\t1", output)
    
    def test_mapper_with_text(self):
        """Test the mapper with plain text input."""
        test_input = "This is another test with different words\n"
        
        with patch('sys.stdin', io.StringIO(test_input)), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            map_words()
            
            output = mock_stdout.getvalue().strip().split('\n')
            self.assertIn("this\t1", output)
            self.assertIn("another\t1", output)
            self.assertIn("test\t1", output)
            self.assertIn("with\t1", output)
            self.assertIn("different\t1", output)
            self.assertIn("words\t1", output)
    
    def test_reducer(self):
        """Test the reducer."""
        test_input = "apple\t1\napple\t1\nbanana\t1\napple\t1\ncherry\t1\nbanana\t1\n"
        
        with patch('sys.stdin', io.StringIO(test_input)), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            reduce_counts()
            
            output = mock_stdout.getvalue().strip().split('\n')
            self.assertEqual(len(output), 3)
            self.assertIn("apple\t3", output)
            self.assertIn("banana\t2", output)
            self.assertIn("cherry\t1", output)

if __name__ == '__main__':
    unittest.main()