def load_lexicon(path: str) -> dict[str, int]:
    """
    Returns word → sentiment score map. Unknown words default to 0.
    
    Args:
        path (str): Path to lexicon CSV file with format: word,score,label
        
    Returns:
        dict[str, int]: Mapping of words to their sentiment scores
    """
    lex = {}
    with open(path) as f:
        for line in f:
            try:
                word, score, _ = line.strip().split(',')
                lex[word] = int(score)
            except ValueError:
                # Skip header or malformed lines
                continue
    return lex