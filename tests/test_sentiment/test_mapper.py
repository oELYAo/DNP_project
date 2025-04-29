from src.sentiment.mapper import mapper

class TestMapperSentiment:
    def test_first_lexicon(self):
        # First
        input = '0 \t good bad good bad'
        truth = '0 \t 0'
        output = mapper(input)
        assert output == truth
        # Second
        input = '1 \t good good good'
        truth = '1 \t 3'
        output = mapper(input)
        assert output == truth
        # Third
        input = '2 \t bad bad good'
        truth = '2 \t -1'
        output = mapper(input)
        assert output == truth

    def test_second_lexicon(self):
        # First
        input = '0 \t excellent test awful'
        truth = '0 \t 0'
        output = mapper(input)
        assert output == truth
        # Second
        input = '1 \t excellent test good'
        truth = '1 \t 3'
        output = mapper(input)
        assert output == truth
        # Third
        input = '2 \t awful bad test'
        truth = '2 \t -3'
        output = mapper(input)
        assert output == truth
        # Fourth
        input = '3 \t excellent bad bad test good excellent bad awful'
        truth = '3 \t 0'
        output = mapper(input)
        assert output == truth
