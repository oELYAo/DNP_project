#!/usr/bin/env python3
import sys

current_word = None
total = 0
for line in sys.stdin:
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