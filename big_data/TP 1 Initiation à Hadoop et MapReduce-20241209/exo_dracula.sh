folder=dracula

hadoop fs -mkdir -p input
hadoop fs -rm -r output_dracula

echo -e "\n\n output will be in output_dracula \n\n"


hadoop fs -put $folder/dracula input


hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $folder/mapper_dracula.py -reducer $folder/reducer_dracula.py -file $folder/mapper_dracula.py -file $folder/reducer_dracula.py -input input/dracula -output output_dracula 