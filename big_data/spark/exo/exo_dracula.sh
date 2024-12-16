hadoop fs -rm -r sortie

spark-submit --deploy-mode client --master local[2] ../programe/wordcount.py input/dracula

hadoop fs -rm -r sortieBis

spark-submit --deploy-mode client --master local[2] ../programe/wordcountBis.py input/dracula 1000

echo -e "\n \n"

echo sortie
hadoop fs -ls sortie

echo sortieBis
hadoop fs -ls sortieBis

echo output are sortie and sortieBis