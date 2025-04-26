#!/usr/bin/env python3
"""
Reducer for the Sentiment Analysis job.
Reads (doc_id, score) pairs and emits (doc_id, sentiment_label)
"""

import sys

def label(score):
    if score > 0.5:
        return "positive"
    elif score < -0.5:
        return "negative"
    else:
        return "neutral"

def main():
    current_doc_id = None
    current_score = 0.0

    for line in sys.stdin:
        try:
            doc_id, score = line.strip().split('\t')
            score = float(score)
            if current_doc_id == doc_id:
                current_score += score
            else:
                if current_doc_id:
                    print(f"{current_doc_id}\t{label(current_score)}")
                current_doc_id = doc_id
                current_score = score
        except:
            continue

    if current_doc_id:
        print(f"{current_doc_id}\t{label(current_score)}")

if __name__ == "__main__":
    main()
