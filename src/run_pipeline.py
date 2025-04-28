"""
Distributed Text Mining Pipeline Runner

This script orchestrates the execution of MapReduce jobs for text analysis,
including word count and sentiment analysis. It handles job chaining,
configuration, logging, and basic error handling.

Usage Examples:

# Run only the WordCount job on sample data, outputting to 'output/wordcount'
python src/run_pipeline.py --input data/processed/processed_docs.jsonl --job wordcount --output-dir output/wordcount --num-reducers 2

# Run only the Sentiment Analysis job, taking input from a previous WordCount run
python src/run_pipeline.py --input output/wordcount/part-* --job sentiment --output-dir output/sentiment --num-reducers 2

# Run both jobs sequentially (WordCount -> Sentiment Analysis)
python src/run_pipeline.py --input data/processed/processed_docs.jsonl --job all --output-dir output/pipeline --intermediate-dir hdfs:///user/hadoop/intermediate --num-reducers 4 --cleanup

# Run Sentiment Analysis using specific memory settings
python src/run_pipeline.py --input output/wordcount/part-* --job sentiment --output-dir output/sentiment --mr-opt mapreduce.map.memory.mb=4096 --mr-opt mapreduce.reduce.memory.mb=8192
"""

import argparse
import logging
import os
import subprocess
import sys
import time
from datetime import timedelta

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.logging_config import setup_logging, get_logger
# Assuming MRJob classes are defined in these locations
from jobs.wordcount_job import WordCountJob
from jobs.sentiment_job import SentimentAnalysisJob

logger = get_logger(__name__)

def run_mrjob(job_cls, job_args, step_name):
    """
    Runs an MRJob class with the given arguments.

    Args:
        job_cls: The MRJob class to run.
        job_args (list): List of command-line arguments for the job.
        step_name (str): Name of the pipeline step for logging.

    Returns:
        str: The output path of the job if successful, None otherwise.
    """
    logger.info(f"--- Starting Step: {step_name} ---")
    start_time = time.time()

    # Add runner type if not specified (default to local for easier testing)
    if not any(arg.startswith('--runner') for arg in job_args):
        job_args.insert(0, '--runner=local') # or 'hadoop', 'emr'

    logger.info(f"Running {job_cls.__name__} with args: {' '.join(job_args)}")

    # Instantiate and run the job
    mr_job = job_cls(args=job_args)
    output_path = None
    success = False

    try:
        with mr_job.make_runner() as runner:
            runner.run()
            # Assuming the output path is retrievable or known based on args
            # For simplicity, let's assume the output dir is the last arg starting with --output-dir
            output_arg = next((arg for arg in reversed(job_args) if arg.startswith('--output-dir=')), None)
            if output_arg:
                output_path = output_arg.split('=', 1)[1]
            else:
                # Fallback or alternative method to get output path if needed
                # This might involve inspecting runner.get_output_dir() if available
                # or constructing it based on conventions.
                logger.warning("Could not determine exact output path from job args.")
                # As a convention, let's assume the last positional arg might be the output if no --output-dir
                if not job_args[-1].startswith('-'):
                     output_path = job_args[-1] # This is a guess, adjust as needed

            success = True
            logger.info(f"Successfully ran {job_cls.__name__}.")
            if output_path:
                logger.info(f"Output generated at: {output_path}")

    except Exception as e:
        logger.error(f"Error running {job_cls.__name__}: {e}", exc_info=True)
        # Optionally re-raise or handle specific exceptions
    finally:
        end_time = time.time()
        duration = timedelta(seconds=end_time - start_time)
        logger.info(f"--- Finished Step: {step_name} (Duration: {duration}) ---")

    return output_path if success else None


def cleanup_path(path, is_hdfs):
    """Removes a path (local or HDFS)."""
    if not path:
        return
    try:
        if is_hdfs:
            logger.info(f"Attempting HDFS cleanup: {path}")
            # Ensure HADOOP_HOME/bin is in PATH or use full path to hdfs command
            # Example: /path/to/hadoop/bin/hdfs dfs -rm -r {path}
            process = subprocess.run(['hdfs', 'dfs', '-rm', '-r', path], check=True, capture_output=True, text=True)
            logger.info(f"HDFS cleanup successful for {path}.")
        else:
            # Local cleanup (use with caution, maybe shutil.rmtree is better)
            logger.warning(f"Local cleanup not implemented for path: {path}")
            # Example using os (careful with directories):
            # if os.path.isdir(path):
            #     shutil.rmtree(path)
            # elif os.path.isfile(path):
            #     os.remove(path)
    except subprocess.CalledProcessError as e:
        logger.error(f"HDFS cleanup failed for {path}: {e.stderr}")
    except Exception as e:
        logger.error(f"Cleanup failed for {path}: {e}")


def main():
    setup_logging() # Setup root logger configuration
    parser = argparse.ArgumentParser(
        description="Distributed Text Mining Pipeline Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__ # Use the module docstring as epilog
    )
    parser.add_argument("--input", required=True, help="Input file path or pattern (e.g., data/input.txt, hdfs:///user/data/input*)")
    parser.add_argument(
        "--job",
        choices=["wordcount", "sentiment", "all"],
        required=True,
        help="Job type to run ('all' runs wordcount then sentiment)",
    )
    parser.add_argument("--output-dir", required=True, help="Base directory for final job outputs")
    parser.add_argument("--intermediate-dir", help="Directory for intermediate data (e.g., HDFS path for chaining). Required if job='all'.")
    parser.add_argument("--num-reducers", type=int, default=1, help="Number of reducers for MapReduce jobs")
    # Allow passing arbitrary mrjob options
    parser.add_argument('--mr-opt', action='append', default=[],
                        help='Pass option=value directly to MRJob jobs (e.g., --mr-opt mapreduce.map.memory.mb=4096)')
    parser.add_argument('--cleanup', action='store_true', help='Clean up intermediate HDFS directories on failure or completion')

    args = parser.parse_args()

    # --- Basic Argument Validation ---
    if args.job == 'all' and not args.intermediate_dir:
        parser.error("--intermediate-dir is required when --job='all'")

    is_hdfs_intermediate = args.intermediate_dir and args.intermediate_dir.startswith("hdfs://")

    # --- Prepare Job Arguments ---
    common_job_args = []
    # Add reducer config - mrjob uses jobconf for this
    common_job_args.extend([
        f'--jobconf=mapreduce.job.reduces={args.num_reducers}'
    ])
    # Add custom mrjob options
    for opt in args.mr_opt:
         # Assuming format 'option=value'
        if '=' in opt:
             common_job_args.append(f'--jobconf={opt}')
        else:
             logger.warning(f"Ignoring invalid --mr-opt: {opt}. Expected format 'option=value'.")


    # --- Job Execution Logic ---
    wordcount_output_path = None
    sentiment_output_path = None
    final_output_path = None
    pipeline_successful = True

    # 1. Word Count Job
    if args.job in ["wordcount", "all"]:
        wc_output = os.path.join(args.intermediate_dir if args.job == 'all' else args.output_dir, "wordcount")
        wc_args = common_job_args + [
            f'--output-dir={wc_output}',
            args.input # Input path for wordcount
        ]
        wordcount_output_path = run_mrjob(WordCountJob, wc_args, "Word Count")
        if not wordcount_output_path:
            logger.error("WordCount job failed. Aborting pipeline.")
            pipeline_successful = False
            if args.cleanup:
                 cleanup_path(wc_output, is_hdfs_intermediate)
            sys.exit(1)
        # If only running wordcount, this is the final output
        if args.job == "wordcount":
            final_output_path = wordcount_output_path


    # 2. Sentiment Analysis Job
    if args.job in ["sentiment", "all"] and pipeline_successful:
        # Determine input for sentiment analysis
        if args.job == "all":
            # Chain from wordcount output
            sentiment_input = os.path.join(wordcount_output_path, "part-*") # Assuming MRJob output format
            if not wordcount_output_path:
                 logger.error("Cannot run Sentiment Analysis: WordCount output path is missing.")
                 pipeline_successful = False
                 sys.exit(1) # Or handle differently
        else:
            # Use the main input provided for standalone sentiment run
            sentiment_input = args.input

        sa_output = os.path.join(args.output_dir, "sentiment")
        sa_args = common_job_args + [
            f'--output-dir={sa_output}',
            sentiment_input # Input path for sentiment
        ]
        sentiment_output_path = run_mrjob(SentimentAnalysisJob, sa_args, "Sentiment Analysis")
        if not sentiment_output_path:
            logger.error("Sentiment Analysis job failed.")
            pipeline_successful = False
            if args.cleanup:
                 cleanup_path(sa_output, sa_output.startswith("hdfs://")) # Check if output is HDFS
            # Optionally cleanup wordcount intermediate data if chaining failed
            if args.job == "all" and args.cleanup:
                 cleanup_path(os.path.join(args.intermediate_dir, "wordcount"), is_hdfs_intermediate)
            sys.exit(1)
        final_output_path = sentiment_output_path # Final output is sentiment if 'all' or 'sentiment'

    # --- Pipeline Completion ---
    if pipeline_successful:
        logger.info("Pipeline completed successfully.")
        logger.info(f"Final output available at: {final_output_path}")
        # Optional: Cleanup intermediate data on successful completion if requested
        if args.job == "all" and args.cleanup:
             logger.info("Cleaning up intermediate WordCount data...")
             cleanup_path(os.path.join(args.intermediate_dir, "wordcount"), is_hdfs_intermediate)
    else:
        logger.error("Pipeline finished with errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()
