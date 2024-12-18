import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

# Création d'une session Spark
spark = SparkSession.builder.appName("PythonStructuredStreamingWordCount").getOrCreate()
sc = spark.sparkContext
sc.setLogLevel("ERROR")

# Lire les données en streaming à partir d'un flux TCP (port spécifié dans les arguments)
lines = spark.readStream.format("socket") \
    .option("host", sys.argv[1]) \
    .option("port", int(sys.argv[2])) \
    .load()

# Traitement des lignes pour les découper en mots
words = lines.select(explode(split(lines["value"], " ")).alias("word"))

# Compter les occurrences de chaque mot
word_counts = words.groupBy("word").count()

# Écrire les résultats en continu dans la console
query = word_counts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
