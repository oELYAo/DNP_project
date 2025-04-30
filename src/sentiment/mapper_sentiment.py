#!/usr/bin/env python3
import argparse
import sys
from typing import Iterator, Tuple, TextIO
from src.sentiment.lexicon import load_lexicon

def map_sentiment(input_stream: TextIO) -> Iterator[Tuple[str, float, int, int]]:
    """Map function for sentiment analysis.
    
    Args:
        input_stream: Input stream containing document text
        
    Returns:
        Iterator of (doc_id, sentiment_score, pos_count, neg_count) tuples
    """
    # Load lexicon
    lexicon = load_lexicon('tests/test_sentiment/lexicon/1.txt')
    
    for line in input_stream:
        # Split into doc_id and text
        try:
            doc_id, text = line.strip().split('\t', 1)
            doc_id = doc_id.strip()
        except ValueError:
            continue  # Skip malformed lines
            
        # Initialize counters
        pos_count = 0
        neg_count = 0
        total_score = 0.0
        
        # Process each word
        words = text.lower().split()
        for word in words:
            # Get sentiment score from lexicon
            score = lexicon.get(word, 0)
            if score > 0:
                pos_count += 1
            elif score < 0:
                neg_count += 1
            total_score += score
            
        yield (doc_id, total_score, pos_count, neg_count)

def main():
    parser = argparse.ArgumentParser(description='Sentiment Analysis Mapper')
    args = parser.parse_args()
    
    # Process input and emit sentiment scores
    for doc_id, score, pos, neg in map_sentiment(sys.stdin):
        print(f"{doc_id}\t{score}\t{pos}\t{neg}")

if __name__ == "__main__":
    main()
