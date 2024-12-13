#!/usr/bin/env python3

import sys
import string
# reading entire line from STDIN (standard input)
exclude = set(string.punctuation)
for line in sys.stdin:
    line = line.strip()
    # split the line into words
    cost = line.split('\t')[4]
    magasin = line.split('\t')[2]
    moyen_paiement = line.split('\t')[5]
    # j'ai pas reussi a faire un reducer qui prend 3 parametre par line car les lines ete trié que par le nom du magasin et pas le moyen de paiement
    # donc je lie les deux pour qu'il les trie quand meme :)
    print ('{}_{}\t{}'.format(magasin, moyen_paiement, cost))
