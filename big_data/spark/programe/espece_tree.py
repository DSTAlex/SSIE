#!/usr/bin/env python3
import sys
from pyspark import SparkContext

if len(sys.argv) != 2:
    print('Usage: PySpark_wc <file>', file=sys.stderr)
    sys.exit(-1)

sc = SparkContext(appName='Spark Count')
sc.setLogLevel('ERROR')
lines = sc.textFile(sys.argv[1])
index_genre =  11
index_espece = 12

counts = lines.flatMap(lambda x: x.split('\n')) \
    .filter(lambda x: len(x.split(';')[index_genre]) > 0 and len(x.split(';')[index_espece]) > 0 ) \
    .map(lambda x : ( x.split(';')[index_genre], x.split(';')[index_espece])) \
    .sortByKey() \
    .distinct()

counts.saveAsTextFile('espece_tree_output')

sc.stop()