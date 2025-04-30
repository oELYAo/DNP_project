#!/bin/bash
# Setup environment for sentiment MapReduce pipeline

set -e

echo "[1/6] Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "[2/6] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[3/6] Setting HDFS directories..."
hdfs dfs -mkdir -p /data/cleaned
hdfs dfs -mkdir -p /data/sentiment_output
hdfs dfs -chmod -R 755 /data/cleaned /data/sentiment_output

echo "[4/6] Verifying lexicon.csv exists..."
if [ ! -f "lexicon.csv" ]; then
  echo "lexicon.csv not found in project root."
  exit 1
fi

echo "[5/6] Validating Hadoop Streaming availability..."
hadoop checknative -a || echo "Warning: Some native libs not loaded."
which hadoop

echo "[6/6] Environment setup completed successfully."
