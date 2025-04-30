#!/usr/bin/env python3
"""
Lexicon loader for sentiment analysis.

This module provides functions to load sentiment lexicons.
"""

import os
from typing import Dict

from utils.logging_config import get_logger

logger = get_logger(__name__)

def load_lexicon(path: str) -> Dict[str, int]:
    """
    Load a sentiment lexicon from a file.
    
    Args:
        path (str): Path to the lexicon file
        
    Returns:
        Dictionary mapping words to sentiment scores
    """
    logger.info(f"Loading lexicon from {path}")
    
    if not os.path.exists(path):
        logger.error(f"Lexicon file not found: {path}")
        raise FileNotFoundError(f"Lexicon file not found: {path}")
    
    lexicon = {}
    line_count = 0
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                parts = line.split('\t', 1)
                if len(parts) != 2:
                    logger.warning(f"Invalid lexicon entry: {line}")
                    continue
                
                word, score = parts
                try:
                    score = int(score)
                    lexicon[word.lower()] = score
                    line_count += 1
                except ValueError:
                    logger.warning(f"Invalid score in lexicon: {score}")
                    continue
    except Exception as e:
        logger.error(f"Error loading lexicon: {e}")
        raise
    
    logger.info(f"Loaded {line_count} entries from lexicon")
    return lexicon