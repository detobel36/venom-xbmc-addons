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

-----------------------------

#### commun

- `list_results`: CSS Selector  
  Path dans la page qui sera utilisé pour faire la boucle des résultats
- `url`: Custom selector type
- `thumb`: Custom selector type  
  Si l'URL commence par `/`, alors l'URL du site est rajouté (l'URL initiale du site)
- `title`: Custom selector type (* pas encore le cas, pour l'instant juste le contenu text de l'elem)
- `year`: Custom selector type (* pas encore le cas, pour l'instant juste le contenu text de l'elem)  
  Une fonction `int` sera appliquée. Il faut donc que la valeur soit bien un entier.
- `extra_data`: List  
  Permet de récupérer des informations qui ne sont normalement pas affichées mais qui peuvent être utilisées par la
  suite
    - `key`: string  
      Clé qui sera utilisée pour retrouver cet élément
    - `+ Custom selector type`
- `filters`  
  Filtrer les résultats. Actuellement, seul un filtre peut être appliqué.
    - `path`: CSS Selector  
      Chemin vers l'élément à utiliser pour filter.  
      Fonctionne uniquement avec l'opérateur `eq`
    - `elem`: Element présent dans le résultat  
      Appliquer le filtre sur l'élément spécifié et déjà parsé (donc 'title' ou 'description' par exemple).
    - `attr`: string  
      Filtrer sur la valeur associé à l'attribut passé en paramètre
    - `eq`: string  
      Egal
    - `neq`: string  
      Pas égal
    - `contains`: string  
      Contient (opérateur `in` utilisé)
    - `not_contains`: string  
      Ne contient pas (opérateur `not in` utilisé)
- `remote_infos`
    - `infos`: Dict[key, Custom selector type]  
      Liste des informations à récupérer. Dépendant du type dans lequel on est ("hoster", "serie", "episode"...).    
      Ne peut pas être utilisé si `parse_result` est sur `raw`.
    - `parse_result`: HTML/raw  
      Indique en quel format le résultat doit être parser. Pour le HTML, Beautifulsoup est utilisé, pour raw, la donnée
      brute est directement exploitée.
    - `parse_result_raw_key`: string  
      Clé dans laquelle sera stocké le résultat de la requête.  
      Ne peut être défini que si le `parse_result` est sur `raw`.
    - `method`: GET/POST  
      Type de requête à faire (par défaut `GET`)
    - `data_field`: List  
      Permet de définir des données qui seront envoyées en même temps que la requête
        - `key`: string  
          Clé
        - `value`: string  
          Valeur statique à associer avec la clé
        - `var`: string  
          Récupère la valeur associée à la variable déjà récupéré dans les résultats. Si var vaut `title`, alors la
          valeur associée à la clé sera le titre (récupéré précédemment).

### Custom selector type

- `value`: string  
  Valeur statique
- `path`: CSS Selector  
  Chemin utilisé pour récupérer la valeur
- `attr`: string  
  Attribut utilisé pour récupérer la valeur
- `prefix`: string  
  Valeur à rajouter avant la valeur récupérée
- `suffix`: string  
  Valeur à rajouter après la valeur récupérée
- `regex`  
  Appliquer la méthode `re.sub` pour pouvoir remplacer un bout du string
    - `pattern`: string  
      Paterne qui sera utilisé par le regex pour savoir quoi remplacer
    - `repl`: string  
      Valeur utilisé pour remplacer le regex

Si ni `path`, ni `attr` n'est défini, alors ce sera le text de l'élément courant qui sera utilisé.

#### `episode`

- ``
- ``


