import sys
from lexicon import load_lexicon

def mapper():
    """
    Input format: doc_id \t token1 token2 token3...
    Output format: doc_id \t sentiment_score
    """
    lex = load_lexicon("path/to/lexicon.txt")
    
    for line in sys.stdin:
        doc_id, *tokens = line.strip().split()
        # TODO: Implement sentiment calculation
        pass

if __name__ == "__main__":
    mapper()