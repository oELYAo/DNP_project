from mrjob.job import MRJob
from mrjob.step import MRStep

class SentimentAnalysisJob(MRJob):

    JOBCONF = {
        'mapreduce.job.reduces': '10',
        'mapreduce.input.fileinputformat.split.maxsize': '67108864',  # 64MB
        'mapreduce.map.memory.mb': '2048',
        'mapreduce.reduce.memory.mb': '4096',
        'mapreduce.map.java.opts': '-Xmx1638m',
        'mapreduce.reduce.java.opts': '-Xmx3277m',
        'mapreduce.map.speculative': 'false',
        'mapreduce.reduce.speculative': 'false',
        'dfs.blocksize': '134217728'  # 128MB
    }

    def mapper(self, _, line):
        # Простейший пример обработки строки
        words = line.strip().split()
        for word in words:
            yield (word.lower(), 1)

    def combiner(self, word, counts):
        yield (word, sum(counts))

    def reducer(self, word, counts):
        yield (word, sum(counts))

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer)
        ]

if __name__ == '__main__':
    SentimentAnalysisJob.run()
