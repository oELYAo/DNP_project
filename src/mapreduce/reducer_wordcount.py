#!/usr/bin/env python3
"""
Reducer for the WordCount MapReduce job.

This script reads (word, count) pairs from stdin, aggregates counts for each word,
and emits the final counts.
"""

import sys
import os
from collections import defaultdict

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_config import get_logger

logger = get_logger(__name__)

def reduce_counts():
    """
    Read (word, count) pairs from stdin, aggregate counts, and emit results.
    """
    current_word = None
    current_count = 0
    
    # Process each line from stdin
    for line in sys.stdin:
        try:
            # Parse the input
            word, count = line.strip().split('\t', 1)
            count = int(count)
            
            # If this is a new word, emit the previous word's count
            if current_word and current_word != word:
                print(f"{current_word}\t{current_count}")
                current_word = word
                current_count = count
            else:
                # Same word, accumulate the count
                current_word = word
                current_count += count
                
        except ValueError as e:
            logger.error(f"Error parsing line: {e}")
            continue
    
    # Emit the last word's count
    if current_word:
        print(f"{current_word}\t{current_count}")

if __name__ == "__main__":
    reduce_counts()