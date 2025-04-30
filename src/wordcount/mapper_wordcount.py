#!/usr/bin/env python3
import argparse
import re
import sys
from typing import Set, TextIO, Iterator, Tuple


def load_stopwords(stopwords_file: str) -> Set[str]:
    """Load stopwords from a file.
    
    Args:
        stopwords_file: Path to file containing stopwords (one per line)
        
    Returns:
        Set of stopwords
    """
    try:
        with open(stopwords_file, 'r') as f:
            return {line.strip().lower() for line in f if line.strip()}
    except FileNotFoundError:
        print(f"Warning: Stopwords file {stopwords_file} not found. No stopwords will be used.", file=sys.stderr)
        return set()


# Tokenization function removed as data is already preprocessed
def tokenize(text: str) -> list[str]:
    return re.findall(r'\b\w+\b', text.lower())


def map_wordcount(input_stream: TextIO, min_word_length: int = 1, stopwords: Set[str] = None) -> Iterator[Tuple[str, int]]:
    """Map function for word count.
    
    Args:
        input_stream: Input stream to read from
        min_word_length: Minimum word length to include
        stopwords: Set of stopwords to exclude
        
    Returns:
        Iterator of (word, count) pairs
    """
    if stopwords is None:
        stopwords = set()
        
    for line in input_stream:
        for token in tokenize(line):
            if len(token) >= min_word_length and token not in stopwords:
                yield (token, 1)


def main():
    parser = argparse.ArgumentParser(description='Word Count Mapper')
    parser.add_argument('--min-word-length', type=int, default=1, help='Minimum word length to include')
    parser.add_argument('--stopwords-file', type=str, help='File containing stopwords to exclude')
    args = parser.parse_args()
    
    # Load stopwords if file is provided
    stopwords = load_stopwords(args.stopwords_file) if args.stopwords_file else set()
    
    # Process input and emit word counts
    for word, count in map_wordcount(sys.stdin, args.min_word_length, stopwords):
        print(f"{word}\t{count}")


if __name__ == "__main__":
    main()
