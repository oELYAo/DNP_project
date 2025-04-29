#!/usr/bin/env python3
"""
Reducer for the Sentiment Analysis job.
Reads (doc_id, score) pairs and emits (doc_id, sentiment_label)
"""

import sys
import os
import csv
import yaml
from mrjob.job import MRJob

class SentimentReducer(MRJob):
    def configure_args(self):
        super(SentimentReducer, self).configure_args()
        self.add_file_arg('--config', help='Path to sentiment config YAML')
        self.add_passthru_arg('--threshold-positive', type=float, 
                             help='Positive sentiment threshold')
        self.add_passthru_arg('--threshold-negative', type=float,
                             help='Negative sentiment threshold')
        self.add_passthru_arg('--global-summary', action='store_true',
                             help='Generate global sentiment summary')
        self.add_passthru_arg('--output-csv', 
                             help='Path to output CSV file',
                             default='data/sentiment_output/final.csv')

    def reducer_init(self):
        with open(self.options.config) as f:
            config = yaml.safe_load(f)
            # Allow CLI override of thresholds
            self.TH_POS = float(self.options.threshold_positive or config['threshold_positive'])
            self.TH_NEG = float(self.options.threshold_negative or config['threshold_negative'])
            
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.options.output_csv), exist_ok=True)
        self.csv_file = open(self.options.output_csv, 'w')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['doc_id', 'total_score', 'total_pos', 'total_neg', 'label'])

    def reducer(self, doc_id, values):
        """
        Input: doc_id \t score \t pos_count \t neg_count
        Output: doc_id, total_score, total_pos, total_neg, label
        """
        total_score = 0
        total_pos = 0
        total_neg = 0
        
        try:
            for value in values:
                # Parse the input values safely
                if isinstance(value, (list, tuple)) and len(value) == 3:
                    score, pos, neg = value
                    total_score += float(score)
                    total_pos += int(pos)
                    total_neg += int(neg)
                else:
                    raise ValueError(f"Invalid input format: {value}")
                    
            # Determine sentiment label
            if total_score > self.TH_POS:
                label = "positive"
            elif total_score < self.TH_NEG:
                label = "negative"
            else:
                label = "neutral"
                
        except (ValueError, TypeError) as e:
            # Handle parsing errors
            print(f"Error processing values for doc_id {doc_id}: {e}", file=sys.stderr)
            return
            
        # Output format matching test expectations
        result = (doc_id, total_score, total_pos, total_neg, label)
        if self.options.global_summary:
            yield 'ALL', result
        else:
            yield doc_id, result

    def reducer_final(self):
        if hasattr(self, 'csv_file'):
            self.csv_file.close()

if __name__ == '__main__':
    SentimentReducer.run()
