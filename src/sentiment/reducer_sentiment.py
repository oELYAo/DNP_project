import sys

def reducer():
    """
    Input format: doc_id \t sentiment_score
    Output format: doc_id \t final_sentiment_label
    """
    current_doc = None
    current_scores = []
    
    for line in sys.stdin:
        # TODO: Implement sentiment aggregation
        pass

if __name__ == "__main__":
    reducer()