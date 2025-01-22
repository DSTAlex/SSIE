#!/usr/bin/python3
import sys

actual_word = None
actual_count = 0
actual_node = set()

for line in sys.stdin:
    
    word, occurence, node = line.split('\t')
    node = eval(node)
    occurence = int(occurence)
    
    if word != actual_word:
        if word != None:
            print ('{0}\t{1}\t{2}'.format(actual_word, actual_count, actual_node))
        actual_node = set()
        actual_word = word
        actual_count = 0
    
    actual_count += occurence
    actual_node = actual_node.union(node)

print ('{0}\t{1}\t{2}'.format(actual_word, actual_count, actual_node))