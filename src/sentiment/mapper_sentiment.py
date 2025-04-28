import sys
from mrjob.job import MRJob
from .lexicon import load_lexicon

class SentimentMapper(MRJob):
    def configure_args(self):
        super(SentimentMapper, self).configure_args()
        self.add_file_arg('--lexicon', help='Path to sentiment lexicon file')
        
    def mapper_init(self):
        self.lex = load_lexicon(self.options.lexicon)
    
    def mapper(self, _, line):
        """
        Input format: doc_id \t token1 token2 token3...
        Output format: doc_id \t score \t pos_count \t neg_count
        """
        doc_id, text = line.strip().split('\t')
        tokens = text.split()
        
        score = sum(self.lex.get(t, 0) for t in tokens)
        pos_count = sum(1 for t in tokens if self.lex.get(t, 0) > 0)
        neg_count = sum(1 for t in tokens if self.lex.get(t, 0) < 0)
        
        yield doc_id, (score, pos_count, neg_count)
    
    def combiner(self, doc_id, values):
        """Sum partial scores and counts for each document"""
        total_score = 0
        total_pos = 0
        total_neg = 0
        
        for score, pos, neg in values:
            total_score += score
            total_pos += pos
            total_neg += neg
            
        yield doc_id, (total_score, total_pos, total_neg)

if __name__ == '__main__':
    SentimentMapper.run()