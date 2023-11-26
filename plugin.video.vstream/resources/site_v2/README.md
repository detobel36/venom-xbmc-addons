## Beta-V3

L'idée de cette V3 est de se baser sur un fichier pour savoir quels fichiers doivent être parser et
comment les informations doivent être récupéré.

La séparation du parsing, de l'affichage et de la lecture de la vidéo permet également plusieurs
choses. Tout d'abord, la séparation du parsing (sans y inclure aucune fonction liée à Kodi) permet
de lancer automatiquement des tests. Cela pourra permettre, dans le future, de détecter les sites
ne fonctionnant plus afin de les corriger ou de les retirer.


## `sites_v2.json`

Le fichier [site_v2.MD](../sites_v2.MD) décris la structure pour chaque fichier.

## Fichiers

La class `Site` permet de représenter un site présent dans `site_v2.json`.

