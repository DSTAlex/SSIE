#!/usr/bin/env python3
import sys
from pyspark import SparkContext
if len(sys.argv) != 2:
    print('Usage: PySpark_wc <file>', file=sys.stderr)
    sys.exit(-1)
sc = SparkContext(appName='Spark Count')
sc.setLogLevel('ERROR')
lines = sc.textFile(sys.argv[1])
counts = lines.flatMap(lambda x: x.split(' ')) \
    .map(lambda x : (x, 1)) \
    .reduceByKey(lambda v1, v2 : v1+v2)

counts.saveAsTextFile('sortie')
#Pour afficher sur la console le résultat
#output = counts.collect()
#for (word, count) in output :
# print('{0}:{1}'.format(word, count))

sc.stop()