#!/usr/bin/env python3
"""
Pipeline runner for MapReduce jobs.

This script runs the MapReduce pipeline for word count or sentiment analysis.
"""

import os
import sys
import argparse
import subprocess
from typing import List

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_config import get_logger

logger = get_logger(__name__)

def run_hadoop_streaming(
    job_type: str,
    input_path: str,
    output_path: str,
    num_mappers: int = 4,
    num_reducers: int = 2
) -> bool:
    """
    Run a Hadoop streaming job.
    
    Args:
        job_type (str): Type of job ('wordcount' or 'sentiment')
        input_path (str): HDFS input path
        output_path (str): HDFS output path
        num_mappers (int): Number of mappers
        num_reducers (int): Number of reducers
        
    Returns:
        bool: True if the job succeeded, False otherwise
    """
    # Determine mapper and reducer scripts
    if job_type == 'wordcount':
        mapper_script = os.path.join(os.path.dirname(__file__), 'mapreduce', 'mapper_wordcount.py')
        reducer_script = os.path.join(os.path.dirname(__file__), 'mapreduce', 'reducer_wordcount.py')
        files = []
    elif job_type == 'sentiment':
        mapper_script = os.path.join(os.path.dirname(__file__), 'mapreduce', 'mapper_sentiment.py')
        reducer_script = os.path.join(os.path.dirname(__file__), 'mapreduce', 'reducer_sentiment.py')
        lexicon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'lexicon', 'afinn-111.txt')
        files = [lexicon_path]
        
        # Default to processed_docs.jsonl if input path is a directory
        if os.path.isdir(input_path):
            input_path = os.path.join(input_path, 'processed_docs.jsonl')
    else:
        logger.error(f"Unknown job type: {job_type}")
        return False
    
    # Build the Hadoop streaming command
    hadoop_home = os.environ.get('HADOOP_HOME', '/usr/local/hadoop')
    hadoop_streaming_jar = os.path.join(hadoop_home, 'share', 'hadoop', 'tools', 'lib', 'hadoop-streaming-*.jar')
    
    cmd = [
        'hadoop', 'jar', hadoop_streaming_jar,
        '-D', f'mapreduce.job.maps={num_mappers}',
        '-D', f'mapreduce.job.reduces={num_reducers}',
        '-input', input_path,
        '-output', output_path,
        '-mapper', mapper_script,
        '-reducer', reducer_script
    ]
    
    # Add files to be distributed
    for file_path in files:
        cmd.extend(['-files', file_path])
    
    # Run the command
    logger.info(f"Running Hadoop streaming job: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        logger.info(f"Job completed successfully. Output in {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Job failed: {e}")
        return False

def run_mrjob(
    job_type: str,
    input_path: str,
    output_path: str,
    num_mappers: int = 4,
    num_reducers: int = 2
) -> bool:
    """
    Run an MRJob job.
    
    Args:
        job_type (str): Type of job ('wordcount' or 'sentiment')
        input_path (str): Input path
        output_path (str): Output path
        num_mappers (int): Number of mappers
        num_reducers (int): Number of reducers
        
    Returns:
        bool: True if the job succeeded, False otherwise
    """
    # Determine job script
    if job_type == 'wordcount':
        job_script = os.path.join(os.path.dirname(__file__), 'mapreduce', 'run_wordcount.py')
    elif job_type == 'sentiment':
        job_script = os.path.join(os.path.dirname(__file__), 'mapreduce', 'run_sentiment.py')
    else:
        logger.error(f"Unknown job type: {job_type}")
        return False
    
    # Build the MRJob command
    cmd = [
        'python', job_script,
        '-r', 'hadoop',
        '--num-mappers', str(num_mappers),
        '--num-reducers', str(num_reducers),
        '--input', input_path,
        '--output', output_path
    ]
    
    # Run the command
    logger.info(f"Running MRJob: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
        logger.info(f"Job completed successfully. Output in {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Job failed: {e}")
        return False

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Run MapReduce pipeline for word count or sentiment analysis.'
    )
    
    parser.add_argument(
        '--job',
        choices=['wordcount', 'sentiment'],
        required=True,
        help='Type of job to run'
    )
    
    parser.add_argument(
        '--input',
        required=True,
        help='Input path (HDFS or local)'
    )
    
    parser.add_argument(
        '--output',
        required=True,
        help='Output path (HDFS or local)'
    )
    
    parser.add_argument(
        '--runner',
        choices=['hadoop', 'mrjob'],
        default='mrjob',
        help='Runner to use (hadoop or mrjob)'
    )
    
    parser.add_argument(
        '--num-mappers',
        type=int,
        default=4,
        help='Number of mappers'
    )
    
    parser.add_argument(
        '--num-reducers',
        type=int,
        default=2,
        help='Number of reducers'
    )
    
    return parser.parse_args()

def main():
    """Main function."""
    args = parse_args()
    
    # Run the job
    if args.runner == 'hadoop':
        success = run_hadoop_streaming(
            args.job,
            args.input,
            args.output,
            args.num_mappers,
            args.num_reducers
        )
    else:  # mrjob
        success = run_mrjob(
            args.job,
            args.input,
            args.output,
            args.num_mappers,
            args.num_reducers
        )
    
    # Exit with appropriate status
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
