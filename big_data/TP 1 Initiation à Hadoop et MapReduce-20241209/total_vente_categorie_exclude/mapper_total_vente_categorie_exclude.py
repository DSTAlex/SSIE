#!/usr/bin/env python3

import sys
import string
# reading entire line from STDIN (standard input)
exclude = set(string.punctuation)
for line in sys.stdin:
    line = line.strip()
    # split the line into words
    cost = line.split('\t')[4]
    categorie = line.split('\t')[3]
    if categorie != "Toys" and categorie != "Consumer Electronics":
        print ('{}\t{}'.format(categorie, cost))
