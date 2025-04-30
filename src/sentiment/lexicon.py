import os
import logging

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def load_lexicon(path: str) -> dict[str, int]:
    """
    Returns word → sentiment score map. Unknown words default to 0.
    
    Args:
        path (str): Path to lexicon CSV file with format: word,score,label
        
    Returns:
        dict[str, int]: Mapping of words to their sentiment scores
         
    Raises:
        FileNotFoundError: If lexicon file doesn't exist
        ValueError: If lexicon file format is invalid
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Lexicon file not found: {path}")
        
    lex = {}
    with open(path) as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            try:
                parts = line.split(',')
                if len(parts) < 2:
                    continue  # Skip lines without enough parts
                    
                word = parts[0].strip().lower()
                score = int(parts[1])
                if word:  # Skip empty words
                    lex[word] = score
            except (ValueError, IndexError) as e:
                logger.warning(f"Skipping malformed line {line_num} in lexicon: {line}")
                continue
                
    if not lex:
        logger.warning(f"No valid entries found in lexicon file: {path}")
        
    return lex