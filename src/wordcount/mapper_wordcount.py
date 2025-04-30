#!/usr/bin/env python3
import sys
for line in sys.stdin:
    for token in line.strip().split():
        print(f"{token}\t1")