#!/usr/bin/env python3
import sys
from typing import TextIO, Iterator, Tuple


def reduce_wordcount(input_stream: TextIO) -> Iterator[Tuple[str, int]]:
    """Reduce function for word count.
    
    This function can be used as both a reducer and a combiner.
    
    Args:
        input_stream: Input stream to read from
        
    Returns:
        Iterator of (word, count) pairs
    """
    current_word = None
    total = 0
    
    for line in input_stream:
        word, count = line.strip().split('\t', 1)
        count = int(count)
        
        if word != current_word:
            if current_word:
                yield (current_word, total)
            current_word, total = word, count
        else:
            total += count
            
    if current_word:
        yield (current_word, total)


def main():
    # Process input and emit word counts
    for word, count in reduce_wordcount(sys.stdin):
        print(f"{word}\t{count}")


if __name__ == "__main__":
    main()