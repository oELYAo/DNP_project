from src.wordcount.mapper_wordcount import mapper_wordcount

class TestMapperWordcount:
    def test_empty(self):
        input = ''
        output = mapper_wordcount(input)
        assert not output

    def test_single_string(self):
        input = 'usual single input string'
        truth = ['usual\t1', 'single\t1', 'input\t1', 'string\t1']
        output = mapper_wordcount(input)
        assert len(truth) == len(output)
        for i in range(len(truth)):
            assert truth[i] == output[i]

    def test_repeating(self):
        input = 'test test test test test'
        truth = ['test\t1', 'test\t1', 'test\t1', 'test\t1', 'test\t1']
        output = mapper_wordcount(input)
        assert len(truth) == len(output)
        for i in range(len(truth)):
            assert truth[i] == output[i]
