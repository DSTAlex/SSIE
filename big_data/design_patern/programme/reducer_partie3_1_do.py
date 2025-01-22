#!/usr/bin/python3
import sys

actual_word = "do"
actual_node = []

for line in sys.stdin:
    
    word, node = line.split('\t')
    node  = node.strip().replace('"', '')

    if word == actual_word:
        if node not in actual_node:
            actual_node.append(node)

actual_node.sort()
print ('{0}\t{1}'.format(actual_word, actual_node))