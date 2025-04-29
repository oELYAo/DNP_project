#!/usr/bin/env python3
"""
Test script for the data preprocessor module.
"""

import argparse
import json
import os
import sys

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_preprocessor import split_data, prepare_for_wordcount, prepare_for_sentiment
from utils.logging_config import get_logger

logger = get_logger(__name__)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Test the data preprocessor module.'
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to the input file'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        required=True,
        help='Directory to store the output files'
    )
    
    parser.add_argument(
        '--parts', '-p',
        type=int,
        default=2,
        help='Number of parts to split the data into'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=10,
        help='Maximum number of documents to process'
    )
    
    return parser.parse_args()


def main():
    """Main function."""
    args = parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Test split_data
    logger.info("Testing split_data function")
    split_files = split_data(
        input_path=args.input,
        output_dir=args.output_dir,
        n_parts=args.parts,
        max_docs=args.limit
    )
    logger.info(f"Split data into {len(split_files)} parts: {split_files}")
    
    # Test prepare_for_wordcount
    logger.info("Testing prepare_for_wordcount function")
    wordcount_output = os.path.join(args.output_dir, "wordcount_input.json")
    with open(wordcount_output, "w", encoding="utf-8") as f:
        count = 0
        for _, doc in prepare_for_wordcount(args.input):
            f.write(json.dumps(doc) + "\n")
            count += 1
            if args.limit > 0 and count >= args.limit:
                break
    logger.info(f"Wrote {count} documents to {wordcount_output}")
    
    # Test prepare_for_sentiment
    logger.info("Testing prepare_for_sentiment function")
    sentiment_output = os.path.join(args.output_dir, "sentiment_input.json")
    with open(sentiment_output, "w", encoding="utf-8") as f:
        count = 0
        for doc_id, doc in prepare_for_sentiment(args.input):
            f.write(f"{doc_id}: {json.dumps(doc)}\n")
            count += 1
            if args.limit > 0 and count >= args.limit:
                break
    logger.info(f"Wrote {count} documents to {sentiment_output}")
    
    logger.info("All tests completed successfully")


if __name__ == "__main__":
    main() 