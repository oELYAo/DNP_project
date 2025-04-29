#!/usr/bin/env python3
"""
Mapper for Sentiment Analysis job.
Reads text input and emits (doc_id, score, pos_count, neg_count)
"""

import sys
import csv
import yaml
from mrjob.job import MRJob
from mrjob.step import MRStep

class SentimentMapper(MRJob):
    def configure_args(self):
        super(SentimentMapper, self).configure_args()
        self.add_file_arg('--config', help='Path to sentiment config YAML')
        self.add_file_arg('--lexicon', help='Path to lexicon file')

    def mapper_init(self):
        # Load lexicon
        with open(self.options.lexicon) as f:
            self.lexicon = {}
            for line in f:
                if line.strip() and not line.startswith('#'):
                    word, score, _ = line.strip().split(',')
                    self.lexicon[word.lower()] = int(score)

    def mapper(self, _, line):
        """
        Input: doc_id \t text
        Output: (doc_id, (score, pos_count, neg_count))
        """
        try:
            doc_id, text = line.strip().split('\t', 1)
            # Remove comments
            text = text.split('#')[0].strip()
            
            words = text.lower().split()
            total_score = 0
            pos_count = 0
            neg_count = 0
            
            for word in words:
                score = self.lexicon.get(word, 0)
                total_score += score
                if score > 0:
                    pos_count += 1
                elif score < 0:
                    neg_count += 1
                    
            yield doc_id, (total_score, pos_count, neg_count)
            
        except ValueError:
            # Skip malformed lines
            print(f"Skipping malformed line: {line}", file=sys.stderr)

if __name__ == '__main__':
    SentimentMapper.run()
