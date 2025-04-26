#!/usr/bin/env python3
"""
Synthetic dataset generator for WordCount stress testing.

This script generates a large text dataset with configurable properties
to test the performance and scalability of the WordCount MapReduce job.
"""

import argparse
import random
import string
import sys
from typing import List, TextIO

# Common English words with varying frequencies to simulate real text
COMMON_WORDS = [
    # Very common words (high frequency)
    "the", "of", "and", "to", "in", "a", "is", "that", "for", "it",
    # Common words (medium frequency)
    "with", "as", "this", "on", "from", "by", "be", "at", "or", "not",
    # Less common words (lower frequency)
    "data", "processing", "system", "file", "program", "code", "function", "class",
    "test", "performance", "memory", "network", "compute", "storage", "algorithm",
    "distributed", "parallel", "cluster", "node", "job", "task", "pipeline", "stream",
    "batch", "real-time", "analytics", "visualization", "dashboard", "report", "metric"
]

# Word frequency distribution parameters
WORD_FREQ_PARAMS = {
    "common": 0.6,      # 60% of words are common words
    "uncommon": 0.3,   # 30% are uncommon words (randomly generated)
    "rare": 0.1        # 10% are rare words (longer, randomly generated)
}

# Word length parameters
WORD_LENGTH_PARAMS = {
    "uncommon": (4, 8),    # Uncommon words are 4-8 characters
    "rare": (9, 15)       # Rare words are 9-15 characters
}

# Sentence length parameters
SENTENCE_LENGTH = (5, 20)  # Sentences have 5-20 words


def generate_random_word(min_length: int, max_length: int) -> str:
    """Generate a random word with the specified length range.
    
    Args:
        min_length: Minimum word length
        max_length: Maximum word length
        
    Returns:
        A random word
    """
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_sentence(skewed: bool = False) -> str:
    """Generate a random sentence.
    
    Args:
        skewed: If True, make the distribution more skewed (fewer unique words)
        
    Returns:
        A random sentence
    """
    sentence_length = random.randint(*SENTENCE_LENGTH)
    words = []
    
    for _ in range(sentence_length):
        r = random.random()
        
        if skewed:
            # More skewed distribution - higher chance of common words
            common_prob = 0.8
            uncommon_prob = 0.15
        else:
            common_prob = WORD_FREQ_PARAMS["common"]
            uncommon_prob = WORD_FREQ_PARAMS["uncommon"]
        
        if r < common_prob:
            # Use a common word
            words.append(random.choice(COMMON_WORDS))
        elif r < common_prob + uncommon_prob:
            # Generate an uncommon word
            words.append(generate_random_word(*WORD_LENGTH_PARAMS["uncommon"]))
        else:
            # Generate a rare word
            words.append(generate_random_word(*WORD_LENGTH_PARAMS["rare"]))
    
    # Capitalize first word and add period
    words[0] = words[0].capitalize()
    return ' '.join(words) + '.'


def generate_paragraph(num_sentences: int, skewed: bool = False) -> str:
    """Generate a random paragraph.
    
    Args:
        num_sentences: Number of sentences in the paragraph
        skewed: If True, make the distribution more skewed
        
    Returns:
        A random paragraph
    """
    return ' '.join(generate_sentence(skewed) for _ in range(num_sentences))


def generate_dataset(output_stream: TextIO, num_lines: int, skewed: bool = False) -> None:
    """Generate a synthetic dataset.
    
    Args:
        output_stream: Output stream to write to
        num_lines: Number of lines to generate
        skewed: If True, make the word distribution more skewed
    """
    for i in range(num_lines):
        # Generate a paragraph with 1-3 sentences
        paragraph = generate_paragraph(random.randint(1, 3), skewed)
        output_stream.write(paragraph + '\n')
        
        # Print progress every 10,000 lines
        if (i + 1) % 10000 == 0:
            print(f"Generated {i + 1} lines", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='Generate synthetic dataset for WordCount testing')
    parser.add_argument('--output', type=str, help='Output file path (default: stdout)')
    parser.add_argument('--lines', type=int, default=1000000, help='Number of lines to generate (default: 1,000,000)')
    parser.add_argument('--skewed', action='store_true', help='Generate skewed data with fewer unique words')
    args = parser.parse_args()
    
    # Determine output stream
    if args.output:
        with open(args.output, 'w') as f:
            print(f"Generating {args.lines} lines to {args.output}...", file=sys.stderr)
            generate_dataset(f, args.lines, args.skewed)
    else:
        print(f"Generating {args.lines} lines to stdout...", file=sys.stderr)
        generate_dataset(sys.stdout, args.lines, args.skewed)
    
    print("Dataset generation complete.", file=sys.stderr)


if __name__ == "__main__":
    main()