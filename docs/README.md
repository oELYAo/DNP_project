# Distributed Text Mining & Sentiment Analysis

## Day 1: Setup & Data Pipeline

1. Follow 'docs/env_setup.md' to install dependencies
2. Review 'src/utils/data_ingestion.py' & 'src/utils/data_cli.py'
3. Run 'pytest' to ensure initial tests pass

## Installation of pre-commit hooks for black/flake8
```
pip install pre-commit
```

```
pre-commit install
```

## Data Ingestion Module

The data ingestion module (`src/utils/data_ingestion.py`) provides functionality to:

1. Read text data from multiple file formats (JSON, CSV, and plain text)
2. Clean and preprocess text (remove URLs, mentions, hashtags, and special characters)
3. Tokenize text into words for further analysis

### CLI Usage

The data ingestion module can be tested using the command-line interface:

```bash
# Process a text file and output to stdout (limited to 10 documents by default)
python3 src/utils/data_cli.py -i data/sample/sample.txt

# Process a CSV file and save to output file
python3 src/utils/data_cli.py -i data/sample/sample.csv -o data/processed/output.json

# Process a JSON file with verbose output and custom document limit
python3 src/utils/data_cli.py -i data/sample/sample.json -o data/processed/output.json -v -l 100
```

### Supported File Formats

- **JSON**: Expects objects with "id" and "text" fields (or similar)
- **CSV**: Expects CSV with header row and a "text" column
- **TXT**: One document per line, generates IDs automatically

### Output Format

The output is a JSON Lines file where each line contains a preprocessed document with the following fields:
- `id`: Document ID (original or auto-generated)
- `text`: Original document text
- `clean_text`: Cleaned text with special characters, mentions, hashtags, and URLs removed
- `tokens`: List of tokenized words from the cleaned text

## Data Preprocessor Module

The data preprocessor module (`src/utils/data_preprocessor.py`) prepares data for MapReduce jobs:

1. Formats documents for word count and sentiment analysis jobs
2. Splits data into multiple parts for parallel processing
3. Stores intermediate data in the format expected by MapReduce jobs

### Testing Preprocessor

You can test the data preprocessor module using the test script:

```bash
# Test the preprocessor with a text file
python3 src/utils/test_preprocessor.py -i data/sample/sample.txt -o data/processed

# Custom number of parts and document limit
python3 src/utils/test_preprocessor.py -i data/sample/sample.csv -o data/processed -p 4 -l 20
```

## Logging System

The project uses a centralized logging system (`src/utils/logging_config.py`) that provides:

1. Consistent logging across all modules
2. Log output to both console and file
3. Different log levels (INFO, DEBUG, WARNING, ERROR)

To use the logging system in a module:

```python
from utils.logging_config import get_logger

# Create a logger for the module
logger = get_logger(__name__)

# Use the logger
logger.info("Processing started")
logger.debug("Detailed information")
logger.warning("Warning message")
logger.error("Error message")
```

To enable verbose (DEBUG) output, use the `-v` flag with the CLI tools.
