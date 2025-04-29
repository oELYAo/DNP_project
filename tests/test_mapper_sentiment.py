import json
import pytest
import src.sentiment.mapper_sentiment 
from src.sentiment.lexicon import load_lexicon

@pytest.fixture
def lexicon():
    # Пример простого лексикона
    return {
        "good": 2,
        "bad": -2,
        "neutral": 0,
        "excellent": 3
    }

def test_mapper_positive_sentiment(lexicon):
    line = json.dumps({
        "doc_id": "1",
        "text": "This is a good and excellent example"
    })
    results = list(mapper(line, lexicon))
    assert results == [("1", 5)]

def test_mapper_negative_sentiment(lexicon):
    line = json.dumps({
        "doc_id": "2",
        "text": "bad example and another bad case"
    })
    results = list(mapper(line, lexicon))
    assert results == [("2", -4)]

def test_mapper_neutral_sentiment(lexicon):
    line = json.dumps({
        "doc_id": "3",
        "text": "just a neutral word here"
    })
    results = list(mapper(line, lexicon))
    assert results == [("3", 0)]

def test_mapper_ignores_unknown_words(lexicon):
    line = json.dumps({
        "doc_id": "4",
        "text": "unknown and meaningless words"
    })
    results = list(mapper(line, lexicon))
    assert results == [("4", 0)]

def test_mapper_mixed_sentiment(lexicon):
    line = json.dumps({
        "doc_id": "5",
        "text": "good bad neutral unknown excellent"
    })
    results = list(mapper(line, lexicon))
    assert results == [("5", 3)]
