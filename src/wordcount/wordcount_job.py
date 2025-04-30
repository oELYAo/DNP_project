#!/usr/bin/env python3
from mrjob.job import MRJob
from mrjob.step import MRStep
import sys
import os
from typing import Set

class WordCountJob(MRJob):
    def configure_args(self):
        super(WordCountJob, self).configure_args()
        self.add_file_arg('--stopwords-file', help='File containing stopwords to exclude')
        self.add_passthru_arg('--min-word-length', type=int, default=1, help='Minimum word length to include')

    def load_stopwords(self):
        stopwords = set()
        if self.options.stopwords_file:
            with open(self.options.stopwords_file, 'r') as f:
                stopwords = {line.strip().lower() for line in f if line.strip()}
        return stopwords

    def mapper_init(self):
        self.stopwords = self.load_stopwords()
        self.min_word_length = self.options.min_word_length

    def mapper(self, _, line):
        for token in line.lower().split():
            if len(token) >= self.min_word_length and token not in self.stopwords:
                yield (token, 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))

    def steps(self):
        return [
            MRStep(
                mapper_init=self.mapper_init,
                mapper=self.mapper,
                combiner=self.combiner,
                reducer=self.reducer
            )
        ]

if __name__ == '__main__':
    WordCountJob.run()