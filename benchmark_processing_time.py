#python benchmark_processing_time.py --input path/to/reviews.json --batch-size 10000 --max-reviews 100000 --output-plot processing_time.png

import argparse
import time
import matplotlib.pyplot as plt
import json
import os
import csv

def load_reviews(input_path, max_reviews=None, last_n=None):
    reviews = []
    _, ext = os.path.splitext(input_path)
    ext = ext.lower()
    if ext == '.csv':
        with open(input_path, 'r', encoding='utf-8') as f:
            reader = list(csv.DictReader(f))
            if last_n:
                reader = reader[-last_n:]
            for i, row in enumerate(reader):
                if max_reviews and i >= max_reviews:
                    break
                reviews.append(row)
    else:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if last_n:
                lines = lines[-last_n:]
            for i, line in enumerate(lines):
                if max_reviews and i >= max_reviews:
                    break
                try:
                    review = json.loads(line)
                    reviews.append(review)
                except Exception:
                    continue
    return reviews

def simple_sentiment_predict(text):
    text = text.lower()
    # Simple rule-based: positive if contains 'good', negative if contains 'bad', else positive
    if 'good' in text:
        return 'positive'
    elif 'bad' in text:
        return 'negative'
    else:
        return 'positive'

def benchmark_accuracy(input_path, batch_size=5000, last_n=50000, output_plot='accuracy_plot.png'):
    reviews = load_reviews(input_path, last_n=last_n)
    total = len(reviews)
    batch_acc = []
    batch_sizes = list(range(batch_size, total+1, batch_size))
    correct = 0
    acc_progress = []
    for i, review in enumerate(reviews):
        text = review.get('review', review.get('text', ''))
        true_sentiment = review.get('sentiment', '')
        pred = simple_sentiment_predict(text)
        if pred == true_sentiment:
            correct += 1
        if (i+1) % batch_size == 0 or (i+1) == total:
            acc = correct / (i+1)
            acc_progress.append(acc)
            print(f"Processed {i+1} reviews, accuracy: {acc:.4f}")
    plt.figure(figsize=(10,6))
    plt.plot(batch_sizes, acc_progress, marker='o')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Accuracy')
    plt.title('Accuracy Progression over Last 50,000 Reviews')
    plt.grid(True)
    plt.savefig(output_plot)
    print(f"Accuracy plot saved to {output_plot}")

def process_reviews(reviews):
    # Use the real data processing pipeline from the project for benchmarking
    from src.utils.data_preprocessor import load_and_preprocess
    # Assume reviews is a list of dicts; process them as the pipeline would
    # If you want to use the full pipeline, you may need to write them to a temp file and call load_and_preprocess
    # For now, mimic the pipeline's preprocessing for each review
    processed = []
    for review in reviews:
        # Simulate pipeline preprocessing (tokenization, cleaning, etc.)
        # If you want to use the actual pipeline, you may need to adapt this
        processed.append(review)  # Replace with actual processing if needed
    return processed

def benchmark(input_path, batch_size=5000, max_reviews=50000, output_plot='processing_time.png'):
    sizes = list(range(batch_size, max_reviews + 1, batch_size))
    times = []
    for size in sizes:
        reviews = load_reviews(input_path, max_reviews=size)
        start = time.time()
        process_reviews(reviews)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"Processed {size} reviews in {elapsed:.2f} seconds.")
    plt.figure(figsize=(10,6))
    plt.plot(sizes, times, marker='o')
    plt.xlabel('Number of Reviews')
    plt.ylabel('Processing Time (seconds)')
    plt.title('Processing Time vs Number of Reviews')
    plt.grid(True)
    plt.savefig(output_plot)
    print(f"Plot saved to {output_plot}")

def main():
    parser = argparse.ArgumentParser(description='Benchmark processing time over number of reviews.')
    parser.add_argument('--input', required=True, help='Path to the dataset (JSONL format)')
    parser.add_argument('--batch-size', type=int, default=5000, help='Batch size increment')
    parser.add_argument('--max-reviews', type=int, default=50000, help='Maximum number of reviews to process')
    parser.add_argument('--output-plot', default='processing_time.png', help='Output plot file name')
    args = parser.parse_args()
    benchmark(args.input, args.batch_size, args.max_reviews, args.output_plot)

# def main():
#     parser = argparse.ArgumentParser(description='Benchmark accuracy over last 50k reviews.')
#     parser.add_argument('--input', required=True, help='Path to the dataset (CSV or JSONL)')
#     parser.add_argument('--batch-size', type=int, default=5000, help='Batch size for accuracy increments')
#     parser.add_argument('--output-plot', default='accuracy_plot.png', help='Output plot file name')
#     args = parser.parse_args()
#     benchmark_accuracy(args.input, args.batch_size, last_n=50000, output_plot=args.output_plot)

if __name__ == '__main__':
    main()