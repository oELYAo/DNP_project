# Environment Setup Guide

This project uses **MapReduce** (via Hadoop Streaming) to perform **word frequency analysis** and **sentiment classification** on large text corpora like tweets, reviews, or headlines.

### Requirements

- Python 3.8+
- Java 8+
- Hadoop (with streaming support)
- Running HDFS (local or remote)

## 1. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# OR
.venv\Scripts\activate.bat       # Windows
```

## 2. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## 3. Set Up HDFS Directories
```bash
hdfs dfs -mkdir -p /data/input
hdfs dfs -mkdir -p /data/cleaned
hdfs dfs -mkdir -p /data/sentiment_output
hdfs dfs -mkdir -p /data/wordcount_output
hdfs dfs -chmod -R 755 /data
```

## 4. Verify Required Files
Ensure that the following file exists in the project root:
- **lexicon.csv**  — Pre-labeled sentiment word list (used for classification)

## 5. Run the Pipeline
You can run MapReduce jobs using the unified runner script:
```bash
python src/run_pipeline.py --input data/sample/sample.txt --job wordcount
python src/run_pipeline.py --input data/sample/sample.txt --job sentiment
```

## 6. Check Hadoop Setup (Optional)
To verify that Hadoop is correctly installed and available:

```bash
which hadoop
hadoop checknative -a
```
If you see *warnings* about native libraries, *most can be ignored* for development use.
