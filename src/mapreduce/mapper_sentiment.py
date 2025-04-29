#!/usr/bin/env python3
"""
Mapper for the Sentiment Analysis job.

This script reads input lines in the format of JSON with doc_id and text,
calculates sentiment scores using a lexicon, and emits (doc_id, score) pairs.
"""

import sys
import json
import os

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.lexicon_loader import load_lexicon

def main():
    """Process each line from stdin and emit document sentiment scores."""
    # Load the sentiment lexicon
    lexicon_path = "lexicon.csv"  # This will be distributed via -files
    lexicon = load_lexicon(lexicon_path)
    
    for line in sys.stdin:
        try:
            # Parse the input line
            record = json.loads(line.strip())
            
            # Extract doc_id and text
            doc_id = record.get("doc_id", "unknown")
            text = record.get("text", "")
            
            if not text:
                continue
            
            # Calculate sentiment score
            words = text.lower().split()
            score = sum(lexicon.get(word, 0) for word in words)
            
            # Emit the result
            print(f"{doc_id}\t{score}")
            
        except Exception as e:
            sys.stderr.write(f"Error processing line: {e}\n")
            continue

if __name__ == "__main__":
    main()