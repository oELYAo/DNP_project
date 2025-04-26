#!/usr/bin/env python3
"""
Mapper for Sentiment Analysis.
Reads text lines, assigns doc IDs, and emits (doc_id, sentiment_score)
"""

import sys
import os
import re
from lexicon_loader import load_lexicon

LEXICON_PATH = "lexicon.csv"
lexicon = load_lexicon(LEXICON_PATH)

def clean_and_tokenize(text):
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower().split()

def main():
    for idx, line in enumerate(sys.stdin):
        doc_id = f"doc_{idx}"
        words = clean_and_tokenize(line.strip())
        score = sum(lexicon.get(word, 0) for word in words)
        print(f"{doc_id}\t{score}")

if __name__ == "__main__":
    main()
