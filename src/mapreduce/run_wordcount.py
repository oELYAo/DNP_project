#!/usr/bin/env python3
"""
Script to run the WordCount MapReduce job locally or on Hadoop.

This script provides a command-line interface to run the WordCount job
on input data and save the results to an output file.
"""

import argparse
import os
import subprocess
import sys

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_config import get_logger

logger = get_logger(__name__)

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Run the WordCount MapReduce job.'
    )
    
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Path to the input file or directory'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Path to the output directory'
    )
    
    parser.add_argument(
        '--hadoop', '-H',
        action='store_true',
        help='Run on Hadoop (default: run locally)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()

def run_local(input_path, output_path, verbose=False):
    """Run the WordCount job locally."""
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Get the absolute paths to the mapper and reducer scripts
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mapper_path = os.path.join(current_dir, 'mapper_wordcount.py')
    reducer_path = os.path.join(current_dir, 'reducer_wordcount.py')
    
    # Make sure the scripts are executable
    os.chmod(mapper_path, 0o755)
    os.chmod(reducer_path, 0o755)
    
    # Build the command
    cmd = f"cat {input_path} | {mapper_path} | sort | {reducer_path} > {output_path}"
    
    logger.info(f"Running WordCount job locally: {cmd}")
    
    # Run the command
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Error running WordCount job: {result.stderr}")
        sys.exit(1)
    
    if verbose:
        logger.info(f"Command output: {result.stdout}")
    
    logger.info(f"WordCount job completed successfully. Results saved to {output_path}")

def run_hadoop(input_path, output_path, verbose=False):
    """Run the WordCount job on Hadoop."""
    # Check if Hadoop is installed
    hadoop_check = subprocess.run("which hadoop", shell=True, capture_output=True, text=True)
    if hadoop_check.returncode != 0:
        logger.error("Hadoop command not found. Make sure Hadoop is installed and in your PATH.")
        logger.info("Falling back to local execution...")
        return run_local(input_path, output_path, verbose)
    
    # Get the absolute paths to the mapper and reducer scripts
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mapper_path = os.path.join(current_dir, 'mapper_wordcount.py')
    reducer_path = os.path.join(current_dir, 'reducer_wordcount.py')
    
    # Make sure the scripts are executable
    os.chmod(mapper_path, 0o755)
    os.chmod(reducer_path, 0o755)
    
    # Build the Hadoop streaming command
    hadoop_streaming_jar = "$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar"
    
    cmd = f"""
    hadoop jar {hadoop_streaming_jar} \\
      -input {input_path} \\
      -output {output_path} \\
      -mapper {mapper_path} \\
      -reducer {reducer_path}
    """
    
    logger.info(f"Running WordCount job on Hadoop: {cmd}")
    
    # Run the command
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        logger.error(f"Error running WordCount job on Hadoop: {result.stderr}")
        sys.exit(1)
    
    if verbose:
        logger.info(f"Command output: {result.stdout}")
    
    logger.info(f"WordCount job completed successfully. Results saved to {output_path}")

def main():
    """Main function."""
    args = parse_args()
    
    if args.hadoop:
        run_hadoop(args.input, args.output, args.verbose)
    else:
        run_local(args.input, args.output, args.verbose)

if __name__ == "__main__":
    main()