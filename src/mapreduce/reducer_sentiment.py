#!/usr/bin/env python3
"""
Reducer for the Sentiment Analysis job.

This script reads (doc_id, score) pairs from stdin,
and emits (doc_id, sentiment_label) pairs.
"""

import sys

def main():
    """Process each line from stdin and emit document sentiment labels."""
    current_doc_id = None
    current_score = 0
    
    for line in sys.stdin:
        try:
            # Parse the input line
            doc_id, score = line.strip().split('\t', 1)
            score = float(score)
            
            # If this is a new document, emit the previous one
            if current_doc_id and current_doc_id != doc_id:
                # Determine sentiment label
                if current_score > 0:
                    sentiment = "positive"
                elif current_score < 0:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                
                # Emit the result
                print(f"{current_doc_id}\t{sentiment}\t{current_score}")
                
                # Reset for the new document
                current_score = score
            else:
                # Accumulate score for the same document
                current_score += score
            
            current_doc_id = doc_id
            
        except Exception as e:
            sys.stderr.write(f"Error processing line: {e}\n")
            continue
    
    # Emit the last document
    if current_doc_id:
        # Determine sentiment label
        if current_score > 0:
            sentiment = "positive"
        elif current_score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Emit the result
        print(f"{current_doc_id}\t{sentiment}\t{current_score}")

if __name__ == "__main__":
    main()