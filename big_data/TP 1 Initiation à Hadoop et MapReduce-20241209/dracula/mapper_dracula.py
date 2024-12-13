#!/usr/bin/env python3

import sys
import string
# reading entire line from STDIN (standard input)
exclude = set(string.punctuation)
for line in sys.stdin:
    line = line.strip()
    # split the line into words
    words = line.split()
    for word in words:
        word = word.lower()
        word = ''.join(ch for ch in word if ch not in exclude)
        if len(word) >= 1:
            print ('{}\t{}'.format(word, 1))
