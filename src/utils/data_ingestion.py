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


def read_records(path: str) -> Iterator[Dict[str, Union[str, int]]]:
    """Reads records from different file formats and yields them as dictionaries.
    
    Supported formats:
    - .json: Expects objects with "id" and "text" fields (or similar)
    - .csv: Expects CSV with header row and a "text" column
    - .txt: One document per line, generates IDs automatically
    
    Args:
        path (str): Path to the input file
        
    Yields:
        Dict with 'id' and 'text' fields for each document
        
    Raises:
        ValueError: If the file format is not supported
    """
    file_ext = os.path.splitext(path)[1].lower()
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    doc_id = 0  # For formats that don't have IDs
    
    logger.info(f"Reading records from {path} (format: {file_ext})")
    
    if file_ext == '.json':
        with open(path, 'r', encoding='utf-8') as file:
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
                    continue
    
    elif file_ext == '.csv':
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
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
                        continue
                
                # Check if 'id' column exists, otherwise generate one
                doc_id_value = row.get('id', doc_id)
                doc_id += 1
                
                yield {'id': doc_id_value, 'text': row['text']}
    
    elif file_ext == '.txt':
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():  # Skip empty lines
                    yield {'id': doc_id, 'text': line.strip()}
                    doc_id += 1
    
    else:
        logger.error(f"Unsupported file format: {file_ext}")
        raise ValueError(f"Unsupported file format: {file_ext}")
    
    logger.info(f"Finished reading records from {path}")


def clean_text(text: str) -> str:
    """Cleans the input text by removing special characters and normalizing.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove mentions and hashtags (common in tweets)
    text = re.sub(r'@\w+|#\w+', '', text)
    
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def tokenize(text: str) -> List[str]:
    """Tokenizes the input text into words.
    
    Args:
        text (str): Input text to tokenize
        
    Returns:
        List of tokens
    """
    if not text:
        return []
    
    # Simple whitespace-based tokenization
    tokens = text.split()
    
    # Filter out empty tokens and very short ones (like single characters)
    tokens = [token for token in tokens if len(token) > 1]
    
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