dir=${PWD##*/}

programe_path=programe

if [[ "$dir" = "exo" ]]
then
    programe_path=../$programe_path
fi

hadoop fs -rm -r sortie

spark-submit --deploy-mode client --master local[2] "$programe_path/wordcount.py" input/dracula

hadoop fs -rm -r sortieBis

spark-submit --deploy-mode client --master local[2] "$programe_path/wordcountBis.py" input/dracula 1000

echo -e "\n \n"

echo sortie
hadoop fs -ls sortie

echo sortieBis
hadoop fs -ls sortieBis

echo output are sortie and sortieBis