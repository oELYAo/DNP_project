import pytest
from pathlib import Path
from src.sentiment.lexicon import load_lexicon

tmp_path = Path('.')
tmp_path = tmp_path / 'tests' / 'test_sentiment' / 'lexicon'

def test_load_lexicon():
    global tmp_path
    # Create a temporary lexicon file
    p = tmp_path/"lex.txt"
    p.write_text("good\t2\nbad\t-2\n")
    
    # Test loading
    lex = load_lexicon(str(p))
    assert lex["good"] == 2
    assert lex["bad"] == -2

def test_malformed_lexicon():
    global tmp_path
    # Test with malformed line
    p = tmp_path/"bad_lex.txt"
    p.write_text("good\t2\nbad_line\nbad\t-2\n")
    
    with pytest.raises(ValueError):
        load_lexicon(str(p))

def test_empty_lexicon():
    global tmp_path
    # Test with empty file
    p = tmp_path/"empty_lex.txt"
    p.write_text("")
    
    lex = load_lexicon(str(p))
    assert len(lex) == 0
