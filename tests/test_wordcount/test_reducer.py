from src.wordcount.reducer_wordcount import reducer_wordcount

class TestReducerWordcout:
    def test_empty(self):
        input = []
        output = reducer_wordcount(input)
        assert not output

    def test_single_string(self):
        input = ['usual\t1', 'single\t1', 'input\t1', 'string\t1']
        truth = {'usual': 1, 'single': 1, 'input': 1, 'string': 1}
        output = reducer_wordcount(input)
        assert len(truth) == len(output)
        for key in truth:
            assert truth[key] == output[key]

    def test_repeating(self):
        input = ['test\t1', 'test\t1', 'test\t1', 'test\t1', 'test\t1']
        truth = {'test': 5}
        output = reducer_wordcount(input)
        assert len(truth) == len(output)
        for key in truth:
            assert truth[key] == output[key]
