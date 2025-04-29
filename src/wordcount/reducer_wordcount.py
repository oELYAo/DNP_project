#!/usr/bin/env python3

def reduce_wordcount(input_stream):
    current_word = None
    total = 0
    for line in input_stream:
        word, count = line.strip().split('\t', 1)
        count = int(count)
        if word != current_word:
            if current_word:
                print(f"{current_word}\t{total}")
            current_word, total = word, count
        else:
            total += count
    if current_word:
        print(f"{current_word}\t{total}")

if __name__ == "__main__":
    import sys
    reduce_wordcount(sys.stdin)
