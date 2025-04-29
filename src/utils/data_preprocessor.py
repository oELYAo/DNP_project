"""
Data preprocessing module for MapReduce jobs.

This module provides functions to prepare data for MapReduce jobs,
specifically for word count and sentiment analysis.
"""

import json
import logging
import os
import sys
from typing import Dict, Iterator, List, Union, Tuple

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_ingestion import load_and_preprocess
from utils.logging_config import get_logger

# Set up logger
logger = get_logger(__name__)


def prepare_for_wordcount(
    input_path: str
) -> Iterator[Tuple[str, Dict[str, Union[str, int, List[str]]]]]:
    """Prepares documents for the word count MapReduce job.
    
    Formats documents as (None, document) pairs where document contains tokens.
    This is the format expected by the word count mapper.
    
    Args:
        input_path (str): Path to the input file
        
    Yields:
        Tuple of (None, document) where document contains 'tokens' field
    """
    logger.info(f"Preparing documents from {input_path} for word count MapReduce job")
    count = 0
    for document in load_and_preprocess(input_path):
        count += 1
        yield (None, document)
    logger.info(f"Prepared {count} documents for word count MapReduce job")


def prepare_for_sentiment(
    input_path: str
) -> Iterator[Tuple[str, Dict[str, Union[str, int, List[str]]]]]:
    """Prepares documents for the sentiment analysis MapReduce job.
    
    Formats documents as (doc_id, document) pairs.
    This is the format expected by the sentiment mapper.
    
    Args:
        input_path (str): Path to the input file
        
    Yields:
        Tuple of (doc_id, document)
    """
    logger.info(f"Preparing documents from {input_path} for sentiment analysis MapReduce job")
    count = 0
    for document in load_and_preprocess(input_path):
        count += 1
        doc_id = str(document["id"])
        yield (doc_id, document)
    logger.info(f"Prepared {count} documents for sentiment analysis MapReduce job")


def store_intermediate_data(
    documents: Iterator[Dict[str, Union[str, int, List[str]]]],
    output_path: str,
    limit: int = 0
) -> int:
    """Stores preprocessed documents as intermediate data for MapReduce jobs.
    
    Args:
        documents (Iterator): Iterator of preprocessed documents
        output_path (str): Path to the output file
        limit (int, optional): Maximum number of documents to store (0 for all)
        
    Returns:
        Number of documents stored
    """
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    logger.info(f"Storing intermediate data to {output_path}")
    count = 0
    with open(output_path, "w", encoding="utf-8") as f:
        for document in documents:
            f.write(json.dumps(document) + "\n")
            count += 1
            
            if limit > 0 and count >= limit:
                logger.info(f"Reached document limit of {limit}")
                break
    
    logger.info(f"Stored {count} documents to {output_path}")
    return count


def split_data(
    input_path: str,
    output_dir: str,
    n_parts: int = 4,
    max_docs: int = 0
) -> List[str]:
    """Splits data into multiple parts for parallel processing.
    
    Args:
        input_path (str): Path to the input file
        output_dir (str): Directory to store the split files
        n_parts (int, optional): Number of parts to split into
        max_docs (int, optional): Maximum number of documents to include (0 for all)
        
    Returns:
        List of paths to the split files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine input file name without extension
    input_name = os.path.splitext(os.path.basename(input_path))[0]
    
    logger.info(f"Splitting data from {input_path} into {n_parts} parts")
    
    # Load all documents into memory
    documents = list(load_and_preprocess(input_path))
    
    # Limit the number of documents if specified
    if max_docs > 0:
        logger.info(f"Limiting to {max_docs} documents")
        documents = documents[:max_docs]
    
    # Calculate documents per part
    n_docs = len(documents)
    docs_per_part = max(1, n_docs // n_parts)
    
    logger.info(f"Loaded {n_docs} documents, splitting into parts of approximately {docs_per_part} documents each")
    
    # Split into parts
    output_paths = []
    for i in range(n_parts):
        start_idx = i * docs_per_part
        end_idx = min(start_idx + docs_per_part, n_docs)
        
        # Skip empty parts
        if start_idx >= n_docs:
            break
        
        # Create output file path
        output_path = os.path.join(output_dir, f"{input_name}_part_{i+1}.json")
        output_paths.append(output_path)
        
        # Write documents to file
        with open(output_path, "w", encoding="utf-8") as f:
            for j in range(start_idx, end_idx):
                f.write(json.dumps(documents[j]) + "\n")
        
        logger.info(f"Created part {i+1}: {output_path} with {end_idx - start_idx} documents")
    
    return output_paths 