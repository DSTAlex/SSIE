output=output_total_vente_categorie
folder=total_vente_categorie

hadoop fs -mkdir -p input
hadoop fs -rm -r $output

echo -e "\n\n output will be in $output \n\n"

hadoop fs -put purchases.txt input

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $folder/mapper_total_vente_categorie.py -reducer $folder/reducer_total_vente_categorie.py -file $folder/mapper_total_vente_categorie.py -file $folder/reducer_total_vente_categorie.py -input input/purchases.txt -output $output