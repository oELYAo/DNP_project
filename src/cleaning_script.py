#!/usr/bin/env python3
"""
Batch preprocessing script for the sentiment analysis MapReduce job.

This script reads input data from files, cleans the text,
and outputs JSON-lines with document IDs.
"""

import json
import sys
import os
import uuid
import argparse
from typing import Dict, List, Union

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_ingestion import load_and_preprocess, clean_text
from utils.logging_config import get_logger

logger = get_logger(__name__)

def process_files(input_path: str, assign_ids: bool = True) -> List[Dict[str, Union[str, int]]]:
    """
    Process files from the input path and generate cleaned documents.
    
    Args:
        input_path (str): Path to input file or directory
        assign_ids (bool): Whether to assign UUID document IDs
        
    Returns:
        List of processed documents
    """
    documents = []
    
    # Check if input_path is a directory
    if os.path.isdir(input_path):
        logger.info(f"Processing directory: {input_path}")
        for filename in os.listdir(input_path):
            file_path = os.path.join(input_path, filename)
            if os.path.isfile(file_path):
                documents.extend(process_files(file_path, assign_ids))
    else:
        logger.info(f"Processing file: {input_path}")
        try:
            for doc in load_and_preprocess(input_path):
                # Skip documents with empty text
                if not doc["clean_text"].strip():
                    logger.info(f"Skipping document with empty text: {doc.get('id', 'unknown')}")
                    continue
                    
                if assign_ids:
                    # Generate a UUID for the document
                    doc_id = str(uuid.uuid4())
                    documents.append({
                        "doc_id": doc_id,
                        "text": doc["clean_text"]
                    })
                else:
                    documents.append({
                        "id": doc["id"],
                        "text": doc["clean_text"]
                    })
        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
    
    return documents

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Clean text data and assign document IDs for sentiment analysis.'
    )
    
    parser.add_argument(
        'input_path',
        help='Path to the input file or directory'
    )
    
    parser.add_argument(
        '--assign-ids',
        action='store_true',
        help='Assign UUID document IDs to all documents'
    )
    
    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Path to the output file (if not provided, uses default processed directory)'
    )
    
    return parser.parse_args()

def main():
    """Main function."""
    args = parse_args()
    
    # Process files
    documents = process_files(args.input_path, args.assign_ids)
    
    # Set default output path if not provided
    if not args.output:
        # Create processed directory if it doesn't exist
        processed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'processed')
        os.makedirs(processed_dir, exist_ok=True)
        args.output = os.path.join(processed_dir, 'processed_docs.jsonl')
    
    # Output results
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    with open(args.output, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc) + '\n')
    logger.info(f"Processed {len(documents)} documents and saved to {args.output}")

if __name__ == "__main__":
    main()