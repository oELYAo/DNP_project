"""
Data ingestion and preprocessing module for text mining and sentiment analysis.

This module provides functions to read various text file formats and preprocess 
the text for further analysis.
"""

import csv
import json
import os
import re
import sys
from typing import Dict, Iterator, List, Union
import logging

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_config import get_logger

# Set up logger
logger = get_logger(__name__)


def read_records(path):
    """
    Read records from a file based on its extension.
    
    Args:
        path: Path to the file
        
    Returns:
        Generator yielding records as dictionaries
        
    Raises:
        FileNotFoundError: If the file does not exist
        ValueError: If the file format is not supported
        Exception: If the file is empty or malformed
    """
    file_ext = os.path.splitext(path)[1].lower()
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    # Raise Exception if file is empty
    if os.stat(path).st_size == 0:
        raise Exception("Input file is empty")
    
    # Check if file is too large (over 1GB)
    file_size_mb = os.stat(path).st_size / (1024 * 1024)
    if file_size_mb > 1000:  # 1000MB = 1GB
        logger.warning(f"File is very large ({file_size_mb:.2f} MB). Processing may take a long time.")
    
    doc_id = 0  # For formats that don't have IDs
    
    logger.info(f"Reading records from {path} (format: {file_ext})")
    
    if file_ext == '.json':
        with open(path, 'r', encoding='utf-8') as file:  # FIX: use 'path'
            for line in file:
                try:
                    record = json.loads(line.strip())
                    # Ensure the record has an 'id' field
                    if 'id' not in record:
                        record['id'] = doc_id
                        doc_id += 1
                    # Ensure the record has a 'text' field
                    if 'text' not in record:
                        # Look for alternative text fields
                        text_fields = ['content', 'message', 'body', 'description']
                        for field in text_fields:
                            if field in record:
                                record['text'] = record[field]
                                break
                        else:
                            logger.warning(f"No text field found in record: {record}")
                            record['text'] = ""
                    yield {'id': record['id'], 'text': record['text']}
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON in line: {line}")
                    raise Exception(f"Malformed JSON: {line}")  # <-- Add this
                    continue
    
    elif file_ext == '.csv':
        try:
            with open(path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if not reader.fieldnames:
                    raise Exception("CSV file has no headers")
                
                for row in reader:
                    # Check if 'text' column exists
                    if 'text' not in row:
                        # Look for alternative text columns
                        text_fields = ['content', 'message', 'body', 'description']
                        for field in text_fields:
                            if field in row:
                                row['text'] = row[field]
                                break
                        else:
                            logger.warning(f"No text field found in row: {row}")
                            row['text'] = ""  # Use empty string instead of skipping
                    
                    # Check if 'id' column exists, otherwise generate one
                    if 'id' in row and row['id'] != '':
                        doc_id_value = row['id']
                    else:
                        # Use the current counter value for auto-incrementing ID
                        doc_id_value = doc_id
                    
                    # Increment the counter after using it
                    doc_id += 1
                    
                    yield {'id': doc_id_value, 'text': row['text']}
        except csv.Error as e:
            logger.error(f"CSV parsing error in {path}: {e}")
            raise Exception(f"Malformed CSV: {e}")
    
    elif file_ext == '.txt':
        with open(path, 'r', encoding='utf-8') as file:  # FIX: use 'path'
            for line in file:
                if line.strip():  # Skip empty lines
                    yield {'id': doc_id, 'text': line.strip()}
                    doc_id += 1
    
    else:
        logger.error(f"Unsupported file format: {file_ext}")
        raise ValueError(f"Unsupported file format: {file_ext}")
    
    logger.info(f"Finished reading records from {path}")  # FIX: use 'path'


def clean_text(text):
    """Cleans the input text by removing special characters and normalizing.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        Cleaned text
        
    Note:
        This function preserves alphanumeric characters and basic punctuation
        while removing URLs, mentions, and hashtags.
    """
    if not text:
        return ""
    
    # Handle non-string inputs
    if not isinstance(text, str):
        try:
            text = str(text)
        except:
            logger.warning(f"Could not convert {type(text)} to string")
            return ""
    
    text = text.lower()
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    # Remove mentions
    text = re.sub(r'@\w+', '', text)
    # Remove hashtags entirely (including the word)
    text = re.sub(r'#\w+', '', text)
    # Remove special characters but preserve spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Check if text is too long (potential memory issue)
    if len(text) > 100000:  # 100K characters
        logger.warning(f"Very long text detected ({len(text)} chars). Truncating to 100K chars.")
        text = text[:100000]
    
    return text


def tokenize(text: str) -> List[str]:
    """
    Tokenize text into individual words, removing stopwords.
    
    Args:
        text: Input text to tokenize
        
    Returns:
        List of tokens
        
    Note:
        This function removes common English stopwords and single-letter words.
        For more advanced tokenization, consider using NLTK or spaCy.
    """
    if not text:
        return []
    
    # Clean the text first
    cleaned = clean_text(text)
    
    # Define stopwords to filter out (reduced list - keep "with" and "this")
    stopwords = [
        "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
        "in", "on", "at", "to", "for", "by", "of", "and", "or", "not", 
        "it", "its", "as", "from"
    ]
    
    # Split into tokens and filter out stopwords and single-letter words
    tokens = [word for word in cleaned.split() if word not in stopwords and len(word) > 1]
    
    # Warn if no tokens were found
    if not tokens and cleaned:
        logger.warning(f"No tokens extracted from text: '{cleaned[:50]}...'")
    
    return tokens


def preprocess_document(document: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int, List[str]]]:
    """Preprocesses a document by cleaning and tokenizing its text.
    
    Args:
        document (Dict): Document with 'id' and 'text' fields
        
    Returns:
        Document with additional 'clean_text' and 'tokens' fields
    """
    result = document.copy()
    
    # Clean text
    result['clean_text'] = clean_text(document['text'])
    
    # Tokenize
    result['tokens'] = tokenize(result['clean_text'])
    
    return result


def load_and_preprocess(path: str) -> Iterator[Dict[str, Union[str, int, List[str]]]]:
    """Loads and preprocesses documents from a file.
    
    Args:
        path (str): Path to the input file
        
    Yields:
        Preprocessed documents with 'id', 'text', 'clean_text', and 'tokens' fields
    """
    logger.info(f"Loading and preprocessing documents from {path}")
    count = 0
    
    for document in read_records(path):
        count += 1
        yield preprocess_document(document)
    
    logger.info(f"Preprocessed {count} documents from {path}")