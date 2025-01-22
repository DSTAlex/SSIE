#!/usr/bin/bash

hadoop fs -mkdir -p input
hadoop fs -put input/* input


echo "./run_all.sh         run all exercices"
echo "./run_all.sh 1       run count_nb_post"
echo "./run_all.sh 2       run get 10 biger post"
echo "./run_all.sh 3       run index all word"
echo "./run_all.sh 4       run occurence of difference"
echo "./run_all.sh 5       run node_id of do"
echo "./run_all.sh 6       run moyenne"
echo "./run_all.sh 7       run sum of weekday (without bombinator)"
echo "./run_all.sh 8       run sum of weekday (with combinator)"