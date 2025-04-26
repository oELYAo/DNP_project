#!/usr/bin/env python3
"""
Preprocessing script for the MapReduce jobs.

This script reads input data from stdin, cleans and tokenizes the text,
and outputs one cleaned record per line with a UUID as document ID.
"""

import json
import sys
import os
import uuid

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_ingestion import clean_text, tokenize
from utils.logging_config import get_logger

logger = get_logger(__name__)

def preprocess(assign_ids=True):
    """
    Read input from stdin, clean and tokenize text, and output cleaned records.
    
    Args:
        assign_ids (bool): Whether to assign UUID document IDs
    """
    for line in sys.stdin:
        try:
            # Try to parse as JSON first
            try:
                record = json.loads(line.strip())
                if isinstance(record, dict):
                    # Extract text from the record
                    if 'text' in record:
                        text = record['text']
                    else:
                        # Look for alternative text fields
                        text_fields = ['content', 'message', 'body', 'description']
                        for field in text_fields:
                            if field in record:
                                text = record[field]
                                break
                        else:
                            # No text field found, use the entire line
                            text = line.strip()
                else:
                    # JSON is not a dict, treat as text
                    text = line.strip()
            except json.JSONDecodeError:
                # Not JSON, treat as plain text
                text = line.strip()
            
            # Clean the text
            cleaned_text = clean_text(text)
            
            # Skip empty lines
            if not cleaned_text.strip():
                continue
                
            # Create output record
            if assign_ids:
                # Generate a UUID for the document
                doc_id = str(uuid.uuid4())
                output = {
                    "doc_id": doc_id,
                    "text": cleaned_text
                }
                print(json.dumps(output))
            else:
                # Output just the cleaned text
                print(cleaned_text)
                
        except Exception as e:
            logger.error(f"Error processing line: {e}")
            continue

if __name__ == "__main__":
    # Check if --assign-ids flag is present
    assign_ids = "--assign-ids" in sys.argv
    preprocess(assign_ids)