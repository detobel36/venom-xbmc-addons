# Site V2

Ce fichier permet de spécifier les sites web pris en charge par vStream.
Pour chaque site, plusieurs informations seront préciser. Permettant 
à vStream de savoir comment interroger le site web afin de récupérer les
informations.

## Structure

```JSON
"<nom technique du site>": {
    "label": "<nom à afficher>",
    "active": "<True/False>",
    "url": "<URL du site>",
    "token": "<True/False>",
    "menus": [
        "series",
        "series_news",
        "movies",
        "movies_news"
    ]
}
```

| **Clé**  | **Description**                            | **Requis**            | **Choix Possible**                            |
|----------|--------------------------------------------|-----------------------|-----------------------------------------------|
| `label`  | Nom affiché sur l'interface Kodi           | Oui                   | `String`                                      |
| `active` | Activé ou non cette source                 | Oui                   | `True/False`                                  |
| `url`    | URL du site                                | Oui                   | `String`                                      |
| `token`  | Récupérer un token XSRF avant chaque appel | Non (Default `False`) | `True/False`                                  |
| `menus`  | Liste des menus disponible pour ce site    | Oui                   | `[series, series_news, movies, movies_,news]` |


