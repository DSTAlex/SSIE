folder=programme
all_output=()

if [[ $# != 1 || $1 == '1' ]]
then
    mapper=$folder/mapper_partie2_1.py
    reducer=$folder/reducer_partie2_1.py
    input=input/clean_forum.tsv 
    output=output_partie_2_nb_post 
    hadoop fs -rm -r $output
    all_output+=$output
    hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $mapper -reducer $reducer -file $mapper -file $reducer -input $input -output $output
fi
if [[ $# != 1 || $1 == '2' ]]
then
    mapper=$folder/mapper_partie2_2.py
    reducer=$folder/reducer_partie2_2.py
    input=input/clean_forum.tsv 
    output=output_partie_2_biger_post
    hadoop fs -rm -r $output
    all_output+=$output
    hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $mapper -reducer $reducer -file $mapper -file $reducer -input $input -output $output
fi
if [[ $# != 1 || $1 == '3' ]]
then
    mapper=$folder/mapper_partie3_1.py
    reducer=$folder/reducer_partie3_1.py
    input=input/clean_forum.tsv 
    output=output_partie_3_general
    hadoop fs -rm -r $output
    all_output+=$output
    hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $mapper -reducer $reducer -file $mapper -file $reducer -input $input -output $output
fi
if [[ $# != 1 || $1 == '4' ]]
then
    mapper=$folder/mapper_partie3_1_diference_do.py
    reducer=$folder/reducer_partie3_1_diference.py
    input=input/clean_forum.tsv 
    output=output_occurence_difference
    hadoop fs -rm -r $output
    all_output+=$output
    hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $mapper -reducer $reducer -file $mapper -file $reducer -input $input -output $output
fi
if [[ $# != 1 || $1 == '5' ]]
then
    mapper=$folder/mapper_partie3_1_diference_do.py
    reducer=$folder/reducer_partie3_1_do.py
    input=input/clean_forum.tsv 
    output=output_node_id_do
    hadoop fs -rm -r $output
    all_output+=$output
    hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $mapper -reducer $reducer -file $mapper -file $reducer -input $input -output $output
fi
if [[ $# != 1 || $1 == '6' ]]
then
    mapper=$folder/mapper_partie3_2.py
    reducer=$folder/reducer_partie3_2.py
    input=input/purchases.txt
    output=output_moyenne
    hadoop fs -rm -r $output
    all_output+=$output
    hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $mapper -reducer $reducer -file $mapper -file $reducer -input $input -output $output
fi
if [[ $# != 1 || $1 == '7' ]]
then
    mapper=$folder/mapper_partie3_3.py
    reducer=$folder/reducer_partie3_3.py
    input=input/purchases.txt
    output=output_sum_weekday_basic
    hadoop fs -rm -r $output
    all_output+=$output
    hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $mapper -reducer $reducer -file $mapper -file $reducer -input $input -output $output
fi
if [[ $# != 1 || $1 == '8' ]]
then
    mapper=$folder/mapper_partie3_3.py
    reducer=$folder/reducer_partie3_3.py
    input=input/purchases.txt
    output=output_sum_weekday_combinator
    hadoop fs -rm -r $output
    all_output+=$output
    hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -mapper $mapper -reducer $reducer -combiner $reducer -file $mapper -file $reducer -input $input -output $output
fi

echo outputs:
for a in ${all_output[@]}
do
    echo "  $a"
done