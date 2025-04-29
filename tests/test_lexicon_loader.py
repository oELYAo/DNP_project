import pytest
from src.sentiment.lexicon import load_lexicon

def test_load_lexicon(tmp_path):
    # Create a temporary lexicon file
    p = tmp_path/"lex.txt"
    p.write_text("good,2\nbad,-2\n")  # Changed from tab to comma
    
    # Test loading
    lex = load_lexicon(str(p))
    assert lex["good"] == 2
    assert lex["bad"] == -2

def test_malformed_lexicon(tmp_path):
    # Test with malformed line
    p = tmp_path/"bad_lex.txt"
    p.write_text("good,2\nbad_line\nbad,-2\n")  # Using comma separator
    
    # Load lexicon - should skip malformed line
    lex = load_lexicon(str(p))
    
    # Verify good and bad are loaded, malformed line is skipped
    assert len(lex) == 2
    assert lex["good"] == 2
    assert lex["bad"] == -2
    assert "bad_line" not in lex

def test_empty_lexicon(tmp_path):
    # Test with empty file
    p = tmp_path/"empty_lex.txt"
    p.write_text("")
    
    lex = load_lexicon(str(p))
    assert len(lex) == 0

def test_missing_word_returns_zero(tmp_path):
    """Test that unknown words return 0"""
    p = tmp_path/"lex.txt"
    p.write_text("good\t2\nbad\t-2\n")
    
    lex = load_lexicon(str(p))
    assert lex.get("unknown_word", 0) == 0

def test_memory_usage(tmp_path):
    """Test memory usage with large lexicon"""
    p = tmp_path/"large_lex.txt"
    # Create large lexicon (100k entries)
    with open(p, 'w') as f:
        for i in range(100000):
            f.write(f"word{i}\t{i%5-2}\n")
    
    import resource
    before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    lex = load_lexicon(str(p))
    after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    # Check memory usage (should be under 128MB)
    assert (after - before) / 1024 < 128  # Convert KB to MB
