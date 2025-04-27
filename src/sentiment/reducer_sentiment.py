import sys
import csv
import yaml
from mrjob.job import MRJob

class SentimentReducer(MRJob):
    def configure_args(self):
        super(SentimentReducer, self).configure_args()
        self.add_file_arg('--config', help='Path to sentiment config YAML')
        
    def reducer_init(self):
        with open(self.options.config) as f:
            config = yaml.safe_load(f)
            self.TH_POS = config['threshold_positive']
            self.TH_NEG = config['threshold_negative']
            
    def reducer(self, doc_id, values):
        """
        Input: doc_id \t score \t pos_count \t neg_count
        Output: CSV with doc_id,total_score,total_pos,total_neg,label
        """
        total_score = 0
        total_pos = 0
        total_neg = 0
        
        for score, pos, neg in values:
            total_score += score
            total_pos += pos
            total_neg += neg
            
        # Determine sentiment label
        if total_score > self.TH_POS:
            label = "positive"
        elif total_score < self.TH_NEG:
            label = "negative"
        else:
            label = "neutral"
            
        # Output as CSV
        writer = csv.writer(sys.stdout)
        writer.writerow([doc_id, total_score, total_pos, total_neg, label])

if __name__ == '__main__':
    SentimentReducer.run()