#!/usr/bin/env python3
"""
Mapper for the WordCount MapReduce job.

This script reads input data from stdin, cleans and tokenizes the text,
and emits (word, 1) pairs for each word in the text.
"""

import json
import sys
import os

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_ingestion import clean_text, tokenize
from utils.logging_config import get_logger

logger = get_logger(__name__)

def map_words():
    """
    Read input from stdin, tokenize text, and emit (word, 1) pairs.
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
                    elif 'clean_text' in record:
                        text = record['clean_text']
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
            
            # Clean and tokenize the text
            tokens = tokenize(text)
            
            # Emit (word, 1) pairs
            for word in tokens:
                print(f"{word}\t1")
                
        except Exception as e:
            logger.error(f"Error processing line: {e}")
            continue

if __name__ == "__main__":
    map_words()