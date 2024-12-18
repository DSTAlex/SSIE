#!/usr/bin/env python3
from operator import itemgetter
import sys
current_magasin = None
current_moyen = None
current_count = 0
magasin = None
# read the entire line from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    # splitting the data on the basis of tab we have provided in mapper.py
    magasin, count = line.split('\t')
    # convert count (currently a string) to int


    try:
        count = float(count)
    except ValueError:
    # count was not a number, so silently
    # ignore/discard this line
        continue

    if current_magasin == magasin :
        current_count += count
    else:
        if current_magasin:
            # write result to STDOUT
            #print '%s\t%s' % (current_magasin, current_count)

            current_magasin, current_moyen = current_magasin.split('_')
            print('{}\t{}\t{}'.format(current_magasin, current_moyen, current_count))
        current_count = count
        current_magasin = magasin
if current_magasin == magasin:
    #print '%s\t%s' % (current_magasin, current_count)
    current_magasin, current_moyen = current_magasin.split('_')
    print('{}\t{}\t{}'.format(current_magasin, current_moyen, current_count)) 

