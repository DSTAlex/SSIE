hadoop fs -mkdir -p input
hadoop fs -rm -r output_dracula

echo -e "\n\n output will be in output_dracula \n\n"

if [ ! -f /root/dracula ]; then
    wget http://www.textfiles.com/etext/FICTION/dracula
    hadoop fs -put dracula input
fi

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper mapper_dracula.py -reducer reducer_dracula.py -file mapper_dracula.py -file reducer_dracula.py -input input/dracula -output output_dracula 