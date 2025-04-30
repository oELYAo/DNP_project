from src.wordcount.mapper_wordcount import map_wordcount
from io import StringIO

class TestMapperWordcount:
    def test_empty(self):
        input = StringIO('')
        output = [f"{word}\t{count}" for word, count in map_wordcount(input)]
        assert not output

    def test_single_string(self):
        input = StringIO('usual single input string')
        truth = ['usual\t1', 'single\t1', 'input\t1', 'string\t1']
        output = [f"{word}\t{count}" for word, count in map_wordcount(input)]
        assert len(truth) == len(output)
        for i in range(len(truth)):
            assert truth[i] == output[i]

    def test_repeating(self):
        input = StringIO('test test test test test')
        truth = ['test\t1', 'test\t1', 'test\t1', 'test\t1', 'test\t1']
        output = [f"{word}\t{count}" for word, count in map_wordcount(input)]
        assert len(truth) == len(output)
        for i in range(len(truth)):
            assert truth[i] == output[i]
