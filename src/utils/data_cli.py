#!/usr/bin/env python3
"""
Command-line interface for the data ingestion and preprocessing module.

This script allows testing the data ingestion functionality with different file formats.
"""

import argparse
import json
import logging
import os
import sys
from typing import Dict, List, Union

# Add parent directory to path to import sibling modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_ingestion import load_and_preprocess
from utils.logging_config import get_logger


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Ingest and preprocess text data from various file formats.'
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to the input file (supported formats: .json, .csv, .txt)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Path to the output file (if not provided, prints to stdout)'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=10,
        help='Maximum number of documents to process (default: 10, use 0 for all)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()


def process_and_output(
    input_path: str, 
    output_path: str = None, 
    limit: int = 10,
    verbose: bool = False
):
    """Process input data and write to output file or stdout.
    
    Args:
        input_path (str): Path to the input file
        output_path (str, optional): Path to the output file
        limit (int, optional): Maximum number of documents to process
        verbose (bool, optional): Whether to enable verbose output
    """
    logger = get_logger(__name__)
    
    if verbose:
        logger.setLevel(logging.DEBUG)
    
    # Process documents
    documents = []
    count = 0
    
    try:
        for doc in load_and_preprocess(input_path):
            documents.append(doc)
            count += 1
            
            if verbose:
                logger.debug(f"Processed document {count}: {doc['id']}")
            
            if limit > 0 and count >= limit:
                break
    except Exception as e:
        logger.error(f"Error processing documents: {e}")
        sys.exit(1)
    
    # Output results
    if output_path:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for doc in documents:
                    f.write(json.dumps(doc) + '\n')
            logger.info(f"Processed {count} documents and saved to {output_path}")
        except Exception as e:
            logger.error(f"Error writing to output file: {e}")
            sys.exit(1)
    else:
        # Output to stdout
        for doc in documents:
            print(json.dumps(doc))
        
        logger.info(f"Processed {count} documents and printed to stdout")


def main():
    """Main function."""
    args = parse_args()
    
    process_and_output(
        input_path=args.input,
        output_path=args.output,
        limit=args.limit,
        verbose=args.verbose
    )


if __name__ == '__main__':
    main() 