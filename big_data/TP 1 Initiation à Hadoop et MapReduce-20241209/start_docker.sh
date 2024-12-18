network=hadoop_alex_dst


echo create network
docker network create --driver=bridge $network

echo run containers
docker run -itd --net=$network -p 9870:9870 -p 8088:8088 -p 7077:7077 -p 16010:16010 --name hadoop-master --hostname hadoop-master liliasfaxi/hadoop-cluster:latest
docker run -itd -p 8040:8042 --net=$network --name hadoop-worker1 --hostname hadoop-worker1 liliasfaxi/hadoop-cluster:latest
docker run -itd -p 8041:8042 --net=$network --name hadoop-worker2 --hostname hadoop-worker2 liliasfaxi/hadoop-cluster:latest 

echo copy files
docker cp exo_dracula.sh hadoop-master:/root/
docker cp dracula/ hadoop-master:/root/
docker cp exo_total_vente_magasin.sh hadoop-master:/root/
docker cp total_vente_magasin hadoop-master:/root/
docker cp exo_total_vente_categorie.sh hadoop-master:/root/
docker cp total_vente_categorie hadoop-master:/root/
docker cp exo_total_vente_categorie_exclude.sh hadoop-master:/root/
docker cp total_vente_categorie_exclude hadoop-master:/root/
docker cp exo_paiement.sh hadoop-master:/root/
docker cp paiement hadoop-master:/root/
docker cp exo_total_vente.sh hadoop-master:/root/
docker cp total_vente hadoop-master:/root/


echo run ./start-hadoop
docker exec hadoop-master ./start-hadoop.sh

docker exec -it hadoop-master bash

