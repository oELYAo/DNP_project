def load_lexicon(path):
    """
    Returns word → sentiment score map. Unknown words default to 0.
    
    Args:
        path (str): Path to lexicon CSV file with format: word,score,label
        
    Returns:
        dict[str, int]: Mapping of words to their sentiment scores
    """
    lexicon = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) != 2:
                raise ValueError(f"Malformed lexicon line: {line}")
            word, score = parts
            lexicon[word.lower()] = int(score)
    return lexicon