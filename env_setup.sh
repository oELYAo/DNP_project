#!/bin/bash
# Setup environment for Distributed Text Mining Project (MapReduce + Sentiment Analysis)

set -e

echo "[1/6] Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "[2/6] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

echo "[3/6] Setting up HDFS directories..."
hdfs dfs -mkdir -p /data/input /data/cleaned /data/sentiment_output /data/wordcount_output
hdfs dfs -chmod -R 755 /data

echo "[4/6] Verifying lexicon file exists..."
if [ ! -f "lexicon.csv" ]; then
  echo "❌ lexicon.csv not found in project root."
  exit 1
fi

echo "[5/6] Checking Hadoop installation..."
if ! command -v hadoop &> /dev/null; then
  echo "❌ Hadoop not found in PATH."
  exit 1
fi
hadoop checknative -a || echo "⚠️ Some native libraries not loaded."

echo "[6/6] Setup complete! Ready to run pipeline."
