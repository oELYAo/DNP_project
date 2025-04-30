import io
import unittest
from unittest.mock import patch
import sys
import os

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.wordcount.mapper_wordcount import map_wordcount, load_stopwords
from src.wordcount.reducer_wordcount import reduce_wordcount


class TestWordCount(unittest.TestCase):
    def test_tokenize(self):
        """Test the tokenization function."""
        text = "Hello, world! This is a test."
        expected = ["hello", "world", "this", "is", "a", "test"]
        self.assertEqual(list(tokenize(text)), expected)
        
    def test_map_wordcount_basic(self):
        """Test basic word count mapping."""
        input_text = io.StringIO("Hello world\nHello test")
        result = list(map_wordcount(input_text))
        expected = [("hello", 1), ("world", 1), ("hello", 1), ("test", 1)]
        self.assertEqual(result, expected)
        
    def test_map_wordcount_min_length(self):
        """Test word count mapping with minimum word length."""
        input_text = io.StringIO("a ab abc abcd")
        result = list(map_wordcount(input_text, min_word_length=3))
        expected = [("abc", 1), ("abcd", 1)]
        self.assertEqual(result, expected)
        
    def test_map_wordcount_stopwords(self):
        """Test word count mapping with stopwords."""
        input_text = io.StringIO("the quick brown fox jumps over the lazy dog")
        stopwords = {"the", "over"}
        result = list(map_wordcount(input_text, stopwords=stopwords))
        expected = [("quick", 1), ("brown", 1), ("fox", 1), ("jumps", 1), ("lazy", 1), ("dog", 1)]
        self.assertEqual(result, expected)
        
    def test_reduce_wordcount(self):
        """Test word count reducing."""
        input_text = io.StringIO("hello\t1\nhello\t1\nworld\t1")
        result = list(reduce_wordcount(input_text))
        expected = [("hello", 2), ("world", 1)]
        self.assertEqual(result, expected)
        
    def test_combiner_correctness(self):
        """Test that reducer works correctly as a combiner."""
        # Simulate mapper output
        mapper_output = io.StringIO("hello\t1\nworld\t1\nhello\t1\ntest\t1\nworld\t1")
        
        # Sort the mapper output (as would happen in MapReduce)
        sorted_lines = sorted(mapper_output.getvalue().splitlines())
        sorted_output = io.StringIO("\n".join(sorted_lines))
        
        # Apply reducer as combiner
        combiner_result = list(reduce_wordcount(sorted_output))
        
        # Sort combiner output and apply reducer again
        combiner_output_lines = [f"{word}\t{count}" for word, count in combiner_result]
        sorted_combiner_output = io.StringIO("\n".join(sorted(combiner_output_lines)))
        final_result = list(reduce_wordcount(sorted_combiner_output))
        
        # Direct reducer application (without combiner)
        direct_input = io.StringIO("\n".join(sorted_lines))
        direct_result = list(reduce_wordcount(direct_input))
        
        # Results should be the same
        self.assertEqual(final_result, direct_result)
        
    def test_end_to_end_pipeline(self):
        """Test the entire word count pipeline with parameters."""
        # Input text with various words
        input_text = io.StringIO("The quick brown fox jumps over the lazy dog\n" 
                               "The fox is quick and the dog is lazy")
        
        # Apply mapper with min length 4 and stopwords
        stopwords = {"the", "and", "is", "over"}
        mapper_result = list(map_wordcount(input_text, min_word_length=4, stopwords=stopwords))
        
        # Convert to reducer input format and sort
        reducer_input_lines = [f"{word}\t{count}" for word, count in mapper_result]
        reducer_input = io.StringIO("\n".join(sorted(reducer_input_lines)))
        
        # Apply reducer
        reducer_result = list(reduce_wordcount(reducer_input))
        
        # Expected results: only words with length >= 4, excluding stopwords
        expected = [("brown", 1), ("jumps", 1), ("lazy", 2), ("quick", 2)]
        self.assertEqual(sorted(reducer_result, key=lambda x: x[0]), expected)


if __name__ == "__main__":
    unittest.main()