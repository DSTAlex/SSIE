#!/usr/bin/env python3
import sys
from pyspark import SparkContext

if len(sys.argv) != 2:
    print('Usage: PySpark_wc <file>', file=sys.stderr)
    sys.exit(-1)

sc = SparkContext(appName='Spark Count')
sc.setLogLevel('ERROR')
lines = sc.textFile(sys.argv[1])
index_geo = 0 #lines[0].split(';').index("Geo point")
index_address = 6 #lines[0].split(';').index("addresse")
index_tall = 8# lines[0].split(';').index("hauteur en m")

counts = lines.flatMap(lambda x: x.split('\n')) \
    .filter(lambda x: len(x.split(';')[index_geo]) > 0 and len(x.split(';')[index_address]) > 0 and len(x.split(';')[index_tall]) > 0) \
    .map(lambda x : ((x.split(';')[index_geo], x.split(';')[index_address]), float(x.split(';')[index_tall]))) \
    .max(key=lambda x: x[1])



# Pour afficher sur la console le résultat
# output = counts.collect()
# max = output[0][1]
# arbre = output[0][0]
# for (word, count) in output[1:] :
#     if count > max:
#         max = count
#         arbre = word
# print(arbre, max)
result = sc.parallelize({counts}).saveAsTextFile('taller_tree_output')

sc.stop()