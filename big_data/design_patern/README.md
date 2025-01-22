run .start.sh to:
- start all dockers
- copy all files
- set up hadoop
- oppen aa terminal in hadoop-master


./run_all.sh         run all exercices  
./run_all.sh 1       run count_nb_post  
./run_all.sh 2       run get 10 biger post  
./run_all.sh 3       run index all word  
./run_all.sh 4       run occurence of difference  
./run_all.sh 5       run node_id of do  
./run_all.sh 6       run moyenne  
./run_all.sh 7       run sum of weekday (without bombinator)  
./run_all.sh 8       run sum of weekday (with combinator)  


exemple nb post partie 2:
    mapper_partie2_1.py
    reducer_partie2_1.py
    clean_forum.tsv

10 biger post partie 2:
    mapper_partie2_2.py
    reducer_partie2_2.py
    clean_forum.tsv

partie 3.1 index ocurence + node_id:
    mapper_partie3_1.py
    reducer_partie3_1.py
    clean_forum.tsv

partie 3.1 occurence of "difference":
    mapper_partie3_1_diference_do.py
    reducer_partie3_1_diference.py
    clean_forum.tsv

partie 3.1 node of "do":
    mapper_partie3_1_diference_do.py
    reducer_partie3_1_do.py
    clean_forum.tsv

partie 3.2 moyenne:
    mapper_partie3_2.py
    reducer_partie3_2.py
    purchases.txt

partie 3.3:
    mapper_partie_3.3.py
    reducer_partie3.3.py (for reducer and combiner)
    purchases.txt

