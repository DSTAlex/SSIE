network=hadoop_alex_dst


echo create network
docker network create --driver=bridge $network

echo run containers
docker run -itd --net=$network -p 9870:9870 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/hadoop-cluster:latest
docker run -itd -p 8040:8042 --net=$network --name hadoop-worker1 --hostname hadoop-worker1 liliasfaxi/hadoop-cluster:latest
docker run -itd -p 8041:8042 --net=$network --name hadoop-worker2 --hostname hadoop-worker2 liliasfaxi/hadoop-cluster:latest 


echo copy file
docker cp input/ hadoop-master:root/
docker cp programme/ hadoop-master:root/
docker cp set_up.sh hadoop-master:root/
docker cp run_all.sh hadoop-master:root/

echo run ./start-hadoop
docker exec hadoop-master ./start-hadoop.sh

docker exec hadoop-master ./set_up.sh

docker exec -it hadoop-master bash


echo stop containers
docker stop hadoop-worker1
docker stop hadoop-worker2
docker stop hadoop-master


echo rm containers
docker rm hadoop-worker1
docker rm hadoop-worker2
docker rm hadoop-master


echo rm network
docker network rm hadoop_alex_dst
