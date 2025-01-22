#!/usr/bin/env python3

import sys
nbPosts = 0
for line in sys.stdin:
    nbPosts=nbPosts+1
print ('{0}\t{1}'.format("nbPosts",nbPosts))