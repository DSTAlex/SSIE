#!/usr/bin/env python3
from operator import itemgetter
import sys
current_word = None
current_count = 0
word = None
current_number = 0
# read the entire line from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # splitting the data on the basis of tab we have provided in mapper.py
    count, number = line.split('\t', 1)
    # convert count (currently a string) to int
    try:
        count = float(count)
        number = int(number)
    except ValueError:
    # count was not a number, so silently
    # ignore/discard this line
        continue
    current_number += number
    current_count += count
    
print('{}\t{}'.format("money gained", current_count)) 
print('{}\t{}'.format("number of sels", current_number)) 

