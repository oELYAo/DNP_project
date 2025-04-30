from src.sentiment.lexicon import load_lexicon

class TestLexiconLoader():
    def test_first(self):
        truth = {'excellent': 2, 'good': 1, 'neutral': 0, 'bad': -1, 'awful': -2}
        dct = load_lexicon('tests/test_sentiment/lexicon/1.txt')
        assert len(truth) == len(dct)
        for key in truth:
            assert truth[key] == dct[key]

    def test_second(self):
        truth = {'excellent': 2, 'good': 1, 'neutral': 0, 'bad': -1, 'awful': -2}
        dct = load_lexicon('tests/test_sentiment/lexicon/1.txt')
        assert len(truth) == len(dct)
        for key in truth:
            assert truth[key] == dct[key]
