#!/bin/bash

# Benchmark script for WordCount MapReduce job
# This script measures performance metrics for the WordCount job

set -e

# Configuration
INPUT_FILE="$1"
MIN_WORD_LENGTH="${2:-1}"
STOPWORDS_FILE="${3:-}"
OUTPUT_DIR="./benchmark_results"

# Validate input
if [ -z "$INPUT_FILE" ]; then
    echo "Usage: $0 <input_file> [min_word_length] [stopwords_file]"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' does not exist"
    exit 1
fi

if [ ! -z "$STOPWORDS_FILE" ] && [ ! -f "$STOPWORDS_FILE" ]; then
    echo "Error: Stopwords file '$STOPWORDS_FILE' does not exist"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Function to count lines in a file
count_lines() {
    wc -l < "$1" | tr -d ' '
}

# Get input file size and line count
INPUT_SIZE=$(du -h "$INPUT_FILE" | cut -f1)
INPUT_LINES=$(count_lines "$INPUT_FILE")

echo "=== WordCount Benchmark ==="
echo "Input file: $INPUT_FILE ($INPUT_SIZE, $INPUT_LINES lines)"
echo "Min word length: $MIN_WORD_LENGTH"
if [ ! -z "$STOPWORDS_FILE" ]; then
    echo "Stopwords file: $STOPWORDS_FILE"
fi
echo

# Run with time measurement
echo "Running WordCount job..."

# Create temporary files for output and metrics
TEMP_OUTPUT="$OUTPUT_DIR/wordcount_output.txt"
MAPPER_OUTPUT="$OUTPUT_DIR/mapper_output.txt"
SHUFFLE_OUTPUT="$OUTPUT_DIR/shuffle_output.txt"

# Measure mapper performance
echo "Measuring mapper performance..."
MAPPER_START=$(date +%s.%N)
cat "$INPUT_FILE" | python3 ./src/wordcount/mapper_wordcount.py --min-word-length "$MIN_WORD_LENGTH" ${STOPWORDS_FILE:+--stopwords-file "$STOPWORDS_FILE"} > "$MAPPER_OUTPUT"
MAPPER_END=$(date +%s.%N)
MAPPER_TIME=$(echo "$MAPPER_END - $MAPPER_START" | bc)
MAPPER_LINES=$(count_lines "$MAPPER_OUTPUT")
MAPPER_SIZE=$(du -h "$MAPPER_OUTPUT" | cut -f1)

# Measure shuffle performance
echo "Measuring shuffle performance..."
SHUFFLE_START=$(date +%s.%N)
sort "$MAPPER_OUTPUT" > "$SHUFFLE_OUTPUT"
SHUFFLE_END=$(date +%s.%N)
SHUFFLE_TIME=$(echo "$SHUFFLE_END - $SHUFFLE_START" | bc)

# Measure reducer performance
echo "Measuring reducer performance..."
REDUCER_START=$(date +%s.%N)
cat "$SHUFFLE_OUTPUT" | python3 ./src/wordcount/reducer_wordcount.py > "$TEMP_OUTPUT"
REDUCER_END=$(date +%s.%N)
REDUCER_TIME=$(echo "$REDUCER_END - $REDUCER_START" | bc)
OUTPUT_LINES=$(count_lines "$TEMP_OUTPUT")
OUTPUT_SIZE=$(du -h "$TEMP_OUTPUT" | cut -f1)

# Calculate total time
TOTAL_TIME=$(echo "$MAPPER_TIME + $SHUFFLE_TIME + $REDUCER_TIME" | bc)

# Calculate throughput (lines/sec)
if (( $(echo "$TOTAL_TIME > 0" | bc -l) )); then
    THROUGHPUT=$(echo "$INPUT_LINES / $TOTAL_TIME" | bc)
else
    THROUGHPUT="N/A (too fast to measure)"
fi

# Print results
echo
echo "=== Performance Results ==="
echo "Total execution time: ${TOTAL_TIME}s"
echo "Mapper time: ${MAPPER_TIME}s"
echo "Shuffle time: ${SHUFFLE_TIME}s"
echo "Reducer time: ${REDUCER_TIME}s"
echo "Throughput: ${THROUGHPUT} lines/sec"
echo
echo "=== Data Metrics ==="
echo "Input: $INPUT_LINES lines ($INPUT_SIZE)"
echo "Mapper output: $MAPPER_LINES lines ($MAPPER_SIZE)"
echo "Final output: $OUTPUT_LINES lines ($OUTPUT_SIZE)"
echo "Reduction ratio: $(echo "scale=2; $OUTPUT_LINES / $INPUT_LINES" | bc)"
echo
echo "Results saved to $TEMP_OUTPUT"

# Test with combiner
echo
echo "=== Testing with Combiner ==="
COMBINER_OUTPUT="$OUTPUT_DIR/combiner_output.txt"

echo "Running WordCount with combiner..."
COMBINER_START=$(date +%s.%N)
cat "$INPUT_FILE" | \
    python3 ./src/wordcount/mapper_wordcount.py --min-word-length "$MIN_WORD_LENGTH" ${STOPWORDS_FILE:+--stopwords-file "$STOPWORDS_FILE"} | \
    sort | \
    python3 ./src/wordcount/reducer_wordcount.py | \
    sort | \
    python3 ./src/wordcount/reducer_wordcount.py > "$COMBINER_OUTPUT"
COMBINER_END=$(date +%s.%N)
COMBINER_TIME=$(echo "$COMBINER_END - $COMBINER_START" | bc)

echo "Combiner execution time: ${COMBINER_TIME}s"

# Calculate speedup
if (( $(echo "$COMBINER_TIME > 0" | bc -l) )); then
    SPEEDUP=$(echo "scale=2; $TOTAL_TIME / $COMBINER_TIME" | bc)
    echo "Speedup: ${SPEEDUP}x"
else
    echo "Speedup: N/A (too fast to measure)"
fi

# Verify results are the same
diff -q "$TEMP_OUTPUT" "$COMBINER_OUTPUT"
if [ $? -eq 0 ]; then
    echo "Combiner validation: PASSED (outputs match)"
else
    echo "Combiner validation: FAILED (outputs differ)"
fi

echo
echo "Benchmark completed successfully"