import pytest
from src.sentiment.reducer_sentiment import SentimentReducer
import yaml
import tempfile
import os

@pytest.fixture
def config_file():
    """Create a temporary config file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({
            'threshold_positive': 2.0,
            'threshold_negative': -2.0
        }, f)
        return f.name

@pytest.fixture
def reducer(config_file):
    """Create a SentimentReducer instance with test config"""
    reducer = SentimentReducer(['--config', config_file])
    reducer.reducer_init()
    return reducer

def test_basic_positive_sentiment(reducer):
    """Test positive sentiment classification"""
    doc_id = "doc1"
    values = [(3.0, 2, 0)]  # score, pos_count, neg_count
    
    result = list(reducer.reducer(doc_id, values))
    assert len(result) == 1
    _, result_tuple = result[0]  # Unpack key, value pair
    assert result_tuple[4] == "positive"  # Check sentiment label

def test_basic_negative_sentiment(reducer):
    """Test negative sentiment classification"""
    doc_id = "doc2"
    values = [(-3.0, 0, 2)]
    
    result = list(reducer.reducer(doc_id, values))
    assert len(result) == 1
    _, result_tuple = result[0]
    assert result_tuple[4] == "negative"

def test_neutral_sentiment(reducer):
    """Test neutral sentiment classification"""
    doc_id = "doc3"
    values = [(0.5, 1, 1)]
    
    result = list(reducer.reducer(doc_id, values))
    assert len(result) == 1
    _, result_tuple = result[0]
    assert result_tuple[4] == "neutral"

def test_multiple_values_aggregation(reducer):
    """Test aggregation of multiple sentiment values"""
    doc_id = "doc4"
    values = [
        (1.0, 1, 0),
        (2.0, 2, 0),
        (-0.5, 0, 1)
    ]
    
    result = list(reducer.reducer(doc_id, values))
    assert len(result) == 1
    _, result_tuple = result[0]
    assert result_tuple[1] == 2.5  # total_score
    assert result_tuple[2] == 3    # total_pos
    assert result_tuple[3] == 1    # total_neg

def test_global_summary_mode(config_file):
    """Test global summary aggregation mode"""
    reducer = SentimentReducer(['--config', config_file, '--global-summary'])
    reducer.reducer_init()
    
    doc_id = "doc5"
    values = [(3.0, 2, 1)]
    
    result = list(reducer.reducer(doc_id, values))
    assert len(result) == 1
    key, result_tuple = result[0]
    assert key == 'ALL'
    assert len(result_tuple) == 5

def test_cli_threshold_override(config_file):
    """Test CLI threshold override functionality"""
    reducer = SentimentReducer([
        '--config', config_file,
        '--threshold-positive', '1.0',
        '--threshold-negative', '-1.0'
    ])
    reducer.reducer_init()
    
    doc_id = "doc6"
    values = [(1.5, 1, 0)]  # Would be neutral with default thresholds
    
    result = list(reducer.reducer(doc_id, values))
    _, result_tuple = result[0]
    assert result_tuple[4] == "positive"  # Should be positive with new threshold

def test_cleanup(config_file):
    """Clean up temporary files"""
    os.unlink(config_file)