"""
Unit tests for text cleaning functionality.
"""

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.data_ingestion import clean_text, tokenize


class TestCleaner(unittest.TestCase):
    def test_clean_text_basic(self):
        """Test basic text cleaning."""
        test_cases = [
            ("Hello, world!", "hello world"),
            ("This is a TEST.", "this is a test"),
            ("Multiple   spaces  here", "multiple spaces here"),
            ("", ""),  # Empty string
            (None, ""),  # None value
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(clean_text(input_text), expected)
    
    def test_clean_text_social_media(self):
        """Test cleaning social media elements."""
        test_cases = [
            ("@username mentioned", "mentioned"),
            ("#hashtag test", "test"),
            ("Multiple @user1 @user2 mentions", "multiple mentions"),
            ("Multiple #tag1 #tag2 hashtags", "multiple hashtags"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(clean_text(input_text), expected)
    
    def test_clean_text_urls(self):
        """Test cleaning URLs."""
        test_cases = [
            ("Check https://example.com website", "check website"),
            ("URL at end http://test.org", "url at end"),
            ("Multiple https://site1.com and http://site2.org URLs", "multiple and urls"),
            ("www.example.com should be removed", "should be removed"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(clean_text(input_text), expected)
    
    def test_clean_text_punctuation(self):
        """Test cleaning punctuation and special characters."""
        test_cases = [
            ("Hello, world!", "hello world"),
            ("Text with commas, periods. and semicolons;", "text with commas periods and semicolons"),
            ("Special !@#$%^&*() characters", "special characters"),
            ("Numbers 123 456", "numbers 123 456"),
        ]
        
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                self.assertEqual(clean_text(input_text), expected)
    
    def test_tokenize_basic(self):
        """Test basic tokenization."""
        test_text = "this is a simple test of tokenization"
        tokens = tokenize(test_text)
        
        expected_tokens = ["this", "simple", "test", "tokenization"]
        self.assertListEqual(sorted(tokens), sorted(expected_tokens))
        # 'is', 'a', 'of' should be filtered out as they are too short (< 2 chars)
        self.assertNotIn("a", tokens)
        self.assertNotIn("is", tokens)
        self.assertNotIn("of", tokens)
    
    def test_tokenize_empty(self):
        """Test tokenization of empty string."""
        self.assertEqual(tokenize(""), [])
        self.assertEqual(tokenize(None), [])
    
    def test_tokenize_filtering(self):
        """Test token filtering."""
        test_text = "a b c long words should remain"
        tokens = tokenize(test_text)
        
        self.assertIn("long", tokens)
        self.assertIn("words", tokens)
        self.assertIn("should", tokens)
        self.assertIn("remain", tokens)
        
        self.assertNotIn("a", tokens)
        self.assertNotIn("b", tokens)
        self.assertNotIn("c", tokens)
    
    def test_real_world_samples(self):
        samples = [
            ("Check out https://example.com! #amazing @user", "check out amazing"),
            ("RT @someone: Hello!!! #fun", "rt hello fun"),
            ("", ""),
            ("    ", ""),
            ("Special chars: $%^&*()", "special chars"),
        ]
        for input_text, expected in samples:
            with self.subTest(input_text=input_text):
                self.assertEqual(clean_text(input_text), expected)


if __name__ == "__main__":
    unittest.main()
