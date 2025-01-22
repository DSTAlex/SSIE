#!/usr/bin/python3
import sys

actual_word = "difference"
actual_count = 0

for line in sys.stdin:
    
    word, node = line.split('\t')

    if word == actual_word:
        actual_count += 1
    
print ('{0}\t{1}'.format(actual_word, actual_count))