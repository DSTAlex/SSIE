ip_add=172.17.0.1

port=9999

dir=${PWD##*/}

programe_path=programe

if [[ "$dir" = "exo" ]]
then
    programe_path=../$programe_path
fi

spark-submit --master local[2] $programe_path/wc_stream.py $ip_add $port
