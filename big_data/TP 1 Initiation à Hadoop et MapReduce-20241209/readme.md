run ./start_docker.sh for create all dockers, copy files in it and open a terminal in hadoop-master

run ./end_docker.sh to deleate all docker

in hadoop-master 
```
    run ./start-hadoop.sh to lunch hadoop

    run ./exo_dracula.sh to do the exercice of dracula
    see the result with:
        hadoop fs -cat output_dracula/part-00000

    run ./exo_total_vente_magasin.sh to do the exercice of
        déterminer le total des ventes par magasin
    see the result with:
        hadoop fs -cat output_total_vente_magasin/part-00000

    run ./exo_dtotal_vente_categorie.sh to do the exercice of
        déterminer le total des ventes dans chaque catégorie
    see the result with:
        hadoop fs -cat output_total_vente_categorie/part-00000

    run ./exo_total_vente_categorie_exclude.sh to do the exercice of
        déterminer le total des ventes dans chaque catégorie en ajoutant un filtrage vertical (pour extraire sauf la catégorie "Costumer Electronics" et "Toys" ).
    see the result with:
        hadoop fs -cat output_total_vente_categorie_exclude/part-00000

    run ./exo_paiement.sh to do the exercice of
        déterminer la somme dépensée dans chaque magasin pour chaque moyen de paiement
    see the result with:
        hadoop fs -cat output_paiement/part-00000

    run ./exo_total_vente.sh to do the exercice of
        calculer le total des ventes et son nombre dans tous les magasins confendus.
    see the result with:
        hadoop fs -cat output_total_vente/part-00000
```





