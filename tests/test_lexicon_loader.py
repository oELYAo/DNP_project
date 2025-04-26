#!/usr/bin/env python3
"""
Unit tests for the lexicon loader.
"""

import os
import sys
import unittest
import tempfile

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.lexicon_loader import load_lexicon

class TestLexiconLoader(unittest.TestCase):
    def test_load_lexicon(self):
        """Test loading a lexicon from a file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("good\t2\nbad\t-2\n")
            lexicon_path = f.name
        
        try:
            lexicon = load_lexicon(lexicon_path)
            self.assertEqual(lexicon["good"], 2)
            self.assertEqual(lexicon["bad"], -2)
            self.assertEqual(len(lexicon), 2)
        finally:
            os.unlink(lexicon_path)
    
    def test_load_lexicon_with_comments(self):
        """Test loading a lexicon with comments."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("# This is a comment\ngood\t2\n# Another comment\nbad\t-2\n")
            lexicon_path = f.name
        
        try:
            lexicon = load_lexicon(lexicon_path)
            self.assertEqual(lexicon["good"], 2)
            self.assertEqual(lexicon["bad"], -2)
            self.assertEqual(len(lexicon), 2)
        finally:
            os.unlink(lexicon_path)
    
    def test_load_lexicon_with_invalid_entries(self):
        """Test loading a lexicon with invalid entries."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("good\t2\ninvalid\nbad\t-2\n")
            lexicon_path = f.name
        
        try:
            lexicon = load_lexicon(lexicon_path)
            self.assertEqual(lexicon["good"], 2)
            self.assertEqual(lexicon["bad"], -2)
            self.assertEqual(len(lexicon), 2)
        finally:
            os.unlink(lexicon_path)
    
    def test_load_lexicon_with_invalid_scores(self):
        """Test loading a lexicon with invalid scores."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("good\t2\nbad\t-2\nwrong\tnot_a_number\n")
            lexicon_path = f.name
        
        try:
            lexicon = load_lexicon(lexicon_path)
            self.assertEqual(lexicon["good"], 2)
            self.assertEqual(lexicon["bad"], -2)
            self.assertEqual(len(lexicon), 2)
        finally:
            os.unlink(lexicon_path)
    
    def test_load_nonexistent_lexicon(self):
        """Test loading a nonexistent lexicon."""
        with self.assertRaises(FileNotFoundError):
            load_lexicon("nonexistent_file.txt")

if __name__ == "__main__":
    unittest.main()