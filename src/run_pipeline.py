import argparse
import os
import subprocess
import sys
import time
from typing import List, Optional

from utils.logging_config import setup_logging, get_logger

# Set up logger
logger = get_logger(__name__)


def run_wordcount_job(input_file: str, min_word_length: int = 1, stopwords_file: Optional[str] = None) -> None:
    """Run the wordcount MapReduce job.
    
    Args:
        input_file: Path to input file
        min_word_length: Minimum word length to include
        stopwords_file: Path to file containing stopwords to exclude
    """
    logger.info(f"Running wordcount job on {input_file}")
    start_time = time.time()
    
    # Build mapper command with parameters
    mapper_cmd = [sys.executable, os.path.join(os.path.dirname(__file__), "wordcount/mapper_wordcount.py")]
    if min_word_length > 1:
        mapper_cmd.extend(["--min-word-length", str(min_word_length)])
    if stopwords_file:
        mapper_cmd.extend(["--stopwords-file", stopwords_file])
    
    # Build reducer command
    reducer_cmd = [sys.executable, os.path.join(os.path.dirname(__file__), "wordcount/reducer_wordcount.py")]
    
    # Run the pipeline: cat input | mapper | sort | reducer
    with open(input_file, 'r') as input_stream:
        # Start mapper process
        mapper_process = subprocess.Popen(
            mapper_cmd,
            stdin=input_stream,
            stdout=subprocess.PIPE,
            text=True
        )
        
        # Start sort process
        sort_process = subprocess.Popen(
            ["sort"],
            stdin=mapper_process.stdout,
            stdout=subprocess.PIPE,
            text=True
        )
        mapper_process.stdout.close()  # Allow mapper to receive SIGPIPE
        
        # Start reducer process
        reducer_process = subprocess.Popen(
            reducer_cmd,
            stdin=sort_process.stdout,
            stdout=sys.stdout,
            text=True
        )
        sort_process.stdout.close()  # Allow sort to receive SIGPIPE
        
        # Wait for processes to complete
        mapper_status = mapper_process.wait()
        sort_status = sort_process.wait()
        reducer_status = reducer_process.wait()
        
        # Check for errors
        if mapper_status != 0 or sort_status != 0 or reducer_status != 0:
            logger.error(f"Pipeline failed: mapper={mapper_status}, sort={sort_status}, reducer={reducer_status}")
            sys.exit(1)
    
    elapsed_time = time.time() - start_time
    logger.info(f"Wordcount job completed in {elapsed_time:.2f} seconds")


def run_sentiment_job(input_file: str) -> None:
    """Run the sentiment analysis MapReduce job.
    
    Args:
        input_file: Path to input file
    """
    logger.info(f"Running sentiment analysis job on {input_file}")
    # TODO: Implement sentiment analysis job
    logger.info("Sentiment analysis job not yet implemented")


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Distributed Text Mining Pipeline")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument(
        "--job",
        choices=["wordcount", "sentiment"],
        required=True,
        help="Job type to run",
    )
    
    # Add wordcount-specific arguments
    parser.add_argument("--min-word-length", type=int, default=1, help="Minimum word length to include (wordcount only)")
    parser.add_argument("--stopwords-file", type=str, help="File containing stopwords to exclude (wordcount only)")
    
    args = parser.parse_args()
    
    # Dispatch to job modules
    if args.job == "wordcount":
        run_wordcount_job(args.input, args.min_word_length, args.stopwords_file)
    elif args.job == "sentiment":
        run_sentiment_job(args.input)


if __name__ == "__main__":
    main()
