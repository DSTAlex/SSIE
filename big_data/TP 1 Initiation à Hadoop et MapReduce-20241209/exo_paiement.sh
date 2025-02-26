output=output_paiement
folder=paiement

hadoop fs -mkdir -p input
hadoop fs -rm -r $output

echo -e "\n\n output will be in $output \n\n"

hadoop fs -put purchases.txt input

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $folder/mapper_paiement.py -reducer $folder/reducer_paiement.py -file $folder/mapper_paiement.py -file $folder/reducer_paiement.py -input input/purchases.txt -output $output