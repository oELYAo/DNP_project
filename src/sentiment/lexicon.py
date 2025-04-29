def load_lexicon(path: str) -> dict[str, int]:
    """Returns word → sentiment score or label."""
    lex = {}
    with open(path) as f:
        for line in f:
            word, score = line.strip().split()
            lex[word] = int(score)
    return lex