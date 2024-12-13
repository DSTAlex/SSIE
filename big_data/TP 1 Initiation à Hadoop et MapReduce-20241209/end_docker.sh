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