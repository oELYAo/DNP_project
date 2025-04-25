#!/usr/bin/env python3
"""
Film reviews collection script for the DNP project.

This script collects film reviews from Kaggle and saves them in a format
compatible with the data processing pipeline.
"""

import os
import json
import argparse
import pandas as pd
import sys
import subprocess

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_config import get_logger

logger = get_logger(__name__)

def download_kaggle_dataset(dataset_name, output_dir):
    """
    Download a dataset from Kaggle.
    
    Args:
        dataset_name: Name of the Kaggle dataset
        output_dir: Directory to save the dataset
    
    Returns:
        Path to the downloaded dataset directory
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Check if kaggle CLI is installed
    try:
        subprocess.run(["kaggle", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("Kaggle CLI not found. Please install it with: pip install kaggle")
        logger.info("Then configure your Kaggle API credentials.")
        return None
    
    # Download the dataset
    try:
        logger.info(f"Downloading dataset {dataset_name} from Kaggle")
        subprocess.run(
            ["kaggle", "datasets", "download", "-d", dataset_name, "-p", output_dir, "--unzip"],
            check=True
        )
        logger.info(f"Dataset downloaded to {output_dir}")
        return output_dir
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to download dataset: {e}")
        return None

def process_film_reviews(input_dir, output_file, limit=0):
    """
    Process film reviews from various formats into a standardized JSONL format.
    
    Args:
        input_dir: Directory containing the downloaded dataset
        output_file: Path to save the processed reviews
        limit: Maximum number of reviews to process (0 for all)
    
    Returns:
        Number of processed reviews
    """
    # Find CSV or TSV files in the input directory
    data_files = []
    for file in os.listdir(input_dir):
        if file.endswith('.csv') or file.endswith('.tsv'):
            data_files.append(os.path.join(input_dir, file))
    
    if not data_files:
        logger.error(f"No CSV or TSV files found in {input_dir}")
        return 0
    
    # Process the first data file
    data_file = data_files[0]
    logger.info(f"Processing {data_file}")
    
    # Determine the separator based on file extension
    sep = '\t' if data_file.endswith('.tsv') else ','
    
    # Read the data file
    try:
        df = pd.read_csv(data_file, sep=sep)
    except Exception as e:
        logger.error(f"Failed to read {data_file}: {e}")
        return 0
    
    # Identify text and sentiment columns
    text_col = None
    sentiment_col = None
    
    # Common column names for text and sentiment
    text_candidates = ['review', 'text', 'content', 'Review', 'comment', 'Comment']
    sentiment_candidates = ['sentiment', 'label', 'score', 'rating', 'Sentiment', 'Rating']
    
    for col in df.columns:
        if text_col is None and any(candidate in col.lower() for candidate in text_candidates):
            text_col = col
        if sentiment_col is None and any(candidate in col.lower() for candidate in sentiment_candidates):
            sentiment_col = col
    
    if text_col is None:
        logger.error(f"No text column found in {data_file}")
        return 0
    
    # Limit the number of reviews if specified
    if limit > 0:
        df = df.head(limit)
    
    # Write to JSONL format
    count = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, row in df.iterrows():
            review = {
                'id': int(i),
                'text': str(row[text_col])
            }
            
            # Add sentiment if available
            if sentiment_col:
                review['sentiment'] = row[sentiment_col]
            
            f.write(json.dumps(review) + '\n')
            count += 1
    
    logger.info(f"Processed {count} reviews and saved to {output_file}")
    return count

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Collect film reviews from Kaggle for the DNP project.'
    )
    
    parser.add_argument(
        '--dataset',
        default='lakshmi25npathi/imdb-dataset-of-50k-movie-reviews',
        help='Kaggle dataset name (default: IMDB 50K movie reviews)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        default='/Users/lana/Desktop/DNP-Lab/DNP_project/data/raw',
        help='Directory to save the raw dataset'
    )
    
    parser.add_argument(
        '--output-file', '-f',
        default='/Users/lana/Desktop/DNP-Lab/DNP_project/data/raw/film_reviews.jsonl',
        help='Path to save the processed reviews'
    )
    
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=10000,
        help='Maximum number of reviews to process (default: 10000, 0 for all)'
    )
    
    return parser.parse_args()

def main():
    """Main function."""
    args = parse_args()
    
    # Download the dataset
    dataset_dir = download_kaggle_dataset(args.dataset, args.output_dir)
    if not dataset_dir:
        sys.exit(1)
    
    # Process the reviews
    count = process_film_reviews(dataset_dir, args.output_file, args.limit)
    if count == 0:
        logger.error("No reviews were processed")
        sys.exit(1)
    
    logger.info(f"Successfully processed {count} film reviews")
    logger.info(f"You can now use this data with your WordCount mapper/reducer")
    logger.info(f"Example command: python src/mapreduce/run_wordcount.py -i {args.output_file} -o data/processed/wordcount.txt")

if __name__ == "__main__":
    main()