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
index_arrondissement = 3 #lines[0].split(';').index("addresse")
index_circonference = 7

counts = lines.flatMap(lambda x: x.split('\n')) \
    .filter(lambda x: len(x.split(';')[index_geo]) > 0 and len(x.split(';')[index_arrondissement]) > 0 and len(x.split(';')[index_circonference]) > 0) \
    .map(lambda x : ( x.split(';')[index_arrondissement], (x.split(';')[index_geo], float(x.split(';')[index_circonference])))) \
    .reduceByKey(lambda v1,v2 : max(v1, v2))


counts.saveAsTextFile('circonference_tree_output')

sc.stop()