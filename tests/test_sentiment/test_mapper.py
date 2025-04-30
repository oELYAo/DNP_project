from src.sentiment.mapper_sentiment import map_sentiment
from io import StringIO

class TestMapperSentiment:
    def test_first_lexicon(self):
        input_stream = StringIO('0 \t good bad good bad')
        result = list(map_sentiment(input_stream))
        assert len(result) == 1
        doc_id, score, pos, neg = result[0]
        assert doc_id == '0'
        assert score == 0  # good(1) + bad(-1) + good(1) + bad(-1) = 0
        assert pos == 2  # two 'good' words
        assert neg == 2  # two 'bad' words

    def test_second_lexicon(self):
        input_stream = StringIO('0 \t excellent test awful')
        result = list(map_sentiment(input_stream))
        assert len(result) == 1
        doc_id, score, pos, neg = result[0]
        assert doc_id == '0'
        assert score == 0  # excellent(2) + test(0) + awful(-2) = 0
        assert pos == 1  # one 'excellent' word
        assert neg == 1  # one 'awful' word
