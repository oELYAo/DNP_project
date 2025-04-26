#!/usr/bin/env python3
def map_wordcount(input_stream):
    for line in input_stream:
        for token in line.strip().split():
            print(f"{token}\t1")

if __name__ == "__main__":
    import sys
    map_wordcount(sys.stdin)