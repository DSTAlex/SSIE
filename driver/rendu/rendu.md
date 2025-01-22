L'objectif est la création d'un driver PCI en mode caractère fonctionnel pour le calcul de factorielle du périphérique EDU fournit par QEMU: https://www.qemu.org/docs/master/specs/edu.html

Seul la fonctionnalité de calcul de factorielle est requis pour ce projet. Les autres fonctions du driver (DMA et operateur d'inversion) ne sont pas attendues.


Le bon fonctionnement du driver est le suivant:

1.  Compilation OK
2.  Chargement du module OK
3.  Création d'un device node (/dev/edu-fact0)
4.  Ecriture d'un nombre dans le device créé (echo 8 > /dev/edu-fact0)
5.  Lecture du résultat (cat /dev/edu-fact0 -> 40320)
6.  Déchargement du module

