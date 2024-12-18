dir=${PWD##*/}

programe_path=programe

if [[ "$dir" = "exo" ]]
then
    programe_path=../$programe_path
fi

sortie=taller_tree_output

hadoop fs -rm -r $sortie

spark-submit --deploy-mode client --master local[2] "$programe_path/taller_tree.py" input/arbresremarquablesparis2.csv

echo -e "\n \n"

echo $sortie
hadoop fs -ls $sortie


echo output is $sortie