import pytest
from src.mapreduce.mapper_wordcount import mapper

def test_mapper_single_line():
    line = "foo bar foo"
    expected = [("foo", 1), ("bar", 1), ("foo", 1)]
    assert list(mapper(line)) == expected

def test_mapper_mixed_case():
    line = "Apple apple APPLE"
    expected = [("apple", 1), ("apple", 1), ("apple", 1)]
    assert list(mapper(line)) == expected

def test_mapper_with_punctuation():
    line = "hello, world! hello."
    expected = [("hello,", 1), ("world!", 1), ("hello.", 1)]
    # punctuation preserved unless cleaned elsewhere
    assert list(mapper(line)) == expected

def test_mapper_empty_line():
    line = ""
    expected = []
    assert list(mapper(line)) == expected

def test_mapper_numbers_and_symbols():
    line = "42 times #awesome @mention"
    expected = [("42", 1), ("times", 1), ("#awesome", 1), ("@mention", 1)]
    assert list(mapper(line)) == expected
