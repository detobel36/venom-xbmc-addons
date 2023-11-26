# Site V2

Ce fichier permet de spécifier les sites web pris en charge par vStream.
Pour chaque site, plusieurs informations seront préciser. Permettant à vStream de savoir comment interroger le site
web afin de récupérer les informations.

# Structure

## Structure globale

La structure globale est la suivante:

```JSON
{
  "sites": {
    "cle_site_1": {
      "...": "..."
    },
    "cle_site_2": {
      "...": "..."
    }
  }
}
```

Une liste de site. La clé est utilisé pour pouvoir "débug" et également pour savoir quel élément récupérer dans la
liste (par exemple pour désactiver un hoster depuis la configuration de Kodi).

## Structure pour chaque site

Pour chaque site, les paramètres suivants sont disponibles:

| **Clé**  | **Description**                            | **Requis** | **Choix Possible**                                      |
|----------|--------------------------------------------|------------|---------------------------------------------------------|
| `label`  | Nom affiché sur l'interface Kodi           | Oui        | `String`                                                |
| `active` | Activé ou non cette source                 | Oui        | `Boolean` (`True/False`)                                |
| `url`    | URL du site                                | Oui        | `String` (URL)                                          |
| `token`  | Récupérer un token XSRF avant chaque appel | Non        | Voir [Token structure](#structure-de-la-partie-token)   |
| `search` | Tous les éléments de recherches            | Oui        | Voir [Search Structure](#structure-de-la-partie-search) |

### Exemple

```JSON
{
  "cle_site_1": {
    "label": "1 SerieStreaming",
    "active": true,
    "url": "https://1seriestreaming.net/",
    "token": {
      "...": "..."
    },
    "search": {
      "...": "..."
    }
  },
  "...": {
    "...": "..."
  }
}
```

## Structure de la partie token

Certains sites ont mis en place la sécurité [CSRF](https://fr.wikipedia.org/wiki/Cross-site_request_forgery).  
Il s'agit d'une sécurité utile qui n'est pas la pour "embêter" la récupération d'informations mais bien pour sécurisé
le site web.

Pour faire simple, le CSRF ajoute un token dans tous les formulaires (on ne vas pas détailler ici comment ce token
est récupéré par votre navigateur. Partez du principe que lorsque vous avez un formulaire, vous avez un token).  
Ce token doit être envoyé en même temps que les réponses du formulaire. Lorsque vous recevez la réponse du formulaire,
vous recevez un nouveau token (qu'il faudra envoyer lorsque vous enverrez la réponse à un nouveau formulaire).
vStream ne "voit" pas réellement le formulaire. En fait, formulaire peut ici, être remplacé par requête POST.

Voilà les champs disponibles pour configurer la récupération du token:

| **Clé**            | **Description**                                                            | **Requis** | **Choix Possible** |
|--------------------|----------------------------------------------------------------------------|------------|--------------------|
| `url`              | URL utilisée pour récupérer le token (une requête GET est faite la dessus) | Oui        | `String` (URL)     |
| `html_token_input` | HTML Path permettant de récupérer l'input qui contient le token            | Oui        | `String`           |
| `data_key`         | Clé utilisée pour envoyer le token                                         | Oui        | `String`           |

<details> 
  <summary><b>Plus de détails</b></summary>
    Une requête va être faite à l'URL <code>url</code>.<br/><br/>
    La réponse de cette requête va être parser en utilisant <code>html_token_input</code>. On cherche à récupérer la
    valeur présente dans cet input. Si le HTML contient par exemple:<br/>  
    <code>
      &#60;input name="_token" value="superToken" />
    </code><br/>
    Nous voulons récupérer la valeur `superToken`. Il nous suffit donc de dire où se trouve cet <code>input</code> dans
    le HTML.<br/><br/>
    Enfin, ce token doit être envoyé dans la requête POST. Une requête POST contient en général plusieurs "data". Il
    s'agit de données envoyées au site. Le token doit également faire partie de ces données. Cependant, chaque donnée
    est associé à une clé. La valeur de <code>data_key</code> permet de dire à quelle clé doit être associé le token.
</details>

### Exemple

```JSON
{
  "...": "...",
  "token": {
    "url": "https://1seriestreaming.net/accueil-1",
    "html_token_input": "input[name='_token']",
    "data_key": "_token"
  },
  "....": "..."
}
```

## Structure de la partie `search`

La partie recherche à essentiellement 2 point d'entrés:

- `series`
- `movies` (_n'existe pas encore_)

L'idée est que pour chaque site, vous pouvez rechercher des informations. On commence en général par le nom d'une série
ou d'un film. Une fois cette première recherche faite, on continue à faire des recherches. On cherche les saisons
disponibles, la qualité du film, ...

Pour chaque section, on va donc parser le résultat. Certains champs sont communs à toutes les sections. Ceux-ci sont
développé dans la partie [Champs communs dans `results`](#champs-communs-dans-results).

Voici les sections disponibles dans la partie recherche:

- `series`
- `season`
- `episode`
- `hoster`
- `movies` (_Pas encore présent._ Sera développé dans le futur.)

A noter qu'il y a un héritage des sections (les valeurs de l'élément "au-dessus" sont présents également dans l'élément
en dessous). Voici la hiérarchie:  
`serie` :arrow_backward: `season` :arrow_backward: `episode` :arrow_backward: `hoster`

### Paramètre d'une recherche

Comme spécifié précédemment, la recherche peut se lancer à partir de plusieurs point d'entrer (par exemple "série" ou
"film").   
Pour faire une recherche, plusieurs paramètres sont nécessaires:

| **Clé**         | **Description**                                                                                                             | **Requis** | **Choix Possible**             |
|-----------------|-----------------------------------------------------------------------------------------------------------------------------|------------|--------------------------------|
| `url`           | URL utilisée pour faire la recherche                                                                                        | Oui        | `String` (URL)                 |
| `separator`     | Symbole à insérer entre chaque mot de la recherche.<br/>Si le séparateur est `+`, "titre du film" deviendra `titre+du+film` | Oui        | `String`                       |
| `request`       | Type de requête quoi doit être fait pour faire une recherche                                                                | Non        | `POST`/`GET` (défault: `POST`) |
| `search_param`  | Clé dans laquelle doit être mis le titre que l'on cherche                                                                   | Oui        | `String`                       |
| `static_params` | Liste de paramètre (clé/valeur) à rajouter à la requête                                                                     | Non        | `Dictionary`                   |

<details> 
  <summary><b>Exemple</b></summary>

```JSON
{
  "<site>": {
    "...": "...",
    "search": {
      "series": {
        "separator": "+",
        "request": "POST",
        "url": "<URL site>",
        "search_param": "story",
        "static_params": {
          "do": "search",
          "subaction": "search"
        },
        "results": {
          "...": "..."
        }
      }
    }
  }
}
```

</details>

Une fois la recherche faite, les résultats sont parsé. La section `results` décris comment parser les résultats de la
requête.

### Champs communs dans `results`

La partie résult a toujours un champ `list_results` qui donne un chemin (HTML Path) qui permet de récupérer une liste de
balise HTML. Chaque élément dans cette liste pourrait être un résultat différent.

Si on a le HTML suivant:

```HTML

<div class="list_results">
    <ul>
        <li>
            <span class="title">Film 1</span>
            <a href="#">Accéder</a>
        </li>
        <li>
            <span class="title">Film 2</span>
            <a href="#2">Accéder</a>
        </li>
    </ul>
</div>
```

`list_results` aura la valeur suivante: `.list_results ul li`. 2 éléments seront donc récupérés et parsé afin de
récupérer les résultats de la recherche.

| **Clé**        | **Description**                                                                                                                                     | **Requis** | **Choix possible**                            | **Résultat attendu**       |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|------------|-----------------------------------------------|----------------------------|
| `list_results` | Permet de récupérer la liste des résultats de la requêtes                                                                                           | Oui        | `HTML Path`                                   | -                          |
| `url`          | URL utilisée pour récupérer la page qui contient les informations                                                                                   | Oui        | [Custom selector type](#custom-selector-type) | `String` (URL)             |
| `thumb`        | URL utilisée pour récupérer la page qui contient les informations                                                                                   | Non        | [Custom selector type](#custom-selector-type) | `String` (URL)             |
| `title`        | Titre donné par le site                                                                                                                             | Non        | [Custom selector type](#custom-selector-type) | `String`                   |
| `year`         | Date de publication du titre (pas de mise en ligne sur le site)                                                                                     | Non        | [Custom selector type](#custom-selector-type) | `Integer` (Format: `YYYY`) |
| `lang`         | Langue du film (actuellement pas de norme, mais limité à une liste<br/>dans le future                                                               | Non        | [Custom selector type](#custom-selector-type) | `String`                   |
| `quality`      | Qualité du film (actuellement pas de norme, mais limité à une liste<br/>dans le future                                                              | Non        | [Custom selector type](#custom-selector-type) | `String`                   |
| `extra_data`   | Permet de récupérer des données additionnels qui n'ont pas vocation à<br/>être affichée                                                             | Non        | [Extra data](#extra-data)                     | -                          |
| `filters`      | Permet de filtrer les résultats                                                                                                                     | Non        | [Filters](#filters)                           | -                          |
| `remote_infos` | Permet de faire une requête en plus pour récupérer plus d'informations<br/>(Intéressant pour la première recherche, pour avoir l'année par exemple) | Non        | [Remote infos](#remote-infos)                 | -                          |

Les données décrites ici sont donc présent dans toutes les sections suivantes (par héritage). Il est important de
noter que tous les champs ne doivent pas être complétés après la première requête de recherche sur le site (typiquement,
la langue est en général un paramètre qu'on récupère seulement lorsqu'on choisit le player/hoster).

#### Custom selector type

Le but de cette structure et de pouvoir sélectionner n'importe quelle valeur présente dans le HTML.

Voici les champs possible:

| **Clé**                                                                 | **Description**                                                                                                    | **Remarques**                                                                                             |
|-------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| `value`                                                                 | Valeur fixe directement associé à la clé                                                                           | Si défini, aucun autre champ ne peut être utilisé.                                                        |
| `path`                                                                  | Chemin (HTML Path) vers un élément HTML                                                                            | -                                                                                                         |
| `attr`                                                                  | Attribut dans lequel la valeur se trouve                                                                           | Si par défini, la valeur dans la balise HTML est prise                                                    |
| `prefix`                                                                | Texte à ajouter au début de la valeur récupérée                                                                    | -                                                                                                         |
| `suffix`                                                                | Texte à ajouter à la fin de la valeur récupérée                                                                    | -                                                                                                         |
| `regex`<ul><li><code>pattern</code></li><li><code>repl</code></li></ul> | Applique un regex sur la valeur récupérée<ul><li>Pattern pour faire match</li><li>Valeur de remplacement</li></ul> | Il s'agit de la méthode python [`sub`](https://docs.python.org/3/library/re.html#re.sub) qui est utilisée |

<details> 
  <summary><b>Exemple</b></summary>

Pour le HTML suivant:

```HTML

<div class="serie">
    <span class="title">Super série</span>
    <span class="lang">
        <i class="flag-fr"></i>
    </span>
</div>
```

Pour récupérer le titre, on pourra juste faire:

```JSON
{
  "path": ".serie .title"
}
```

Pour récupérer la langue par contre, il faudra passer par un regex pour supprimer `flag` mais également utiliser `attr`:

```JSON
{
  "path": ".serie .lang i",
  "attr": "class",
  "regex": {
    "pattern": "flag-([a-Z]{2})",
    "repl": "\\1"
  }
}
```

</details>

#### Extra data

Le but des extra data est de pouvoir collecter des informations qui seront utile pour faire des requêtes.   
Les extra data ont les mêmes paramètres que [`Custom selector type`](#custom-selector-type). Seul le paramètre `key` est
rajouté pour savoir à quelle clé doit être associé la valeur.

<details> 
  <summary><b>Exemple</b></summary>

Pour le HTML suivant:

```HTML

<div class="serie">
    <span class="title">Super série</span>
    <span class="lang">
        <i class="flag-fr"></i>
    </span>
    <a href="/url_to_serie" data-id="12">Accéder</a>
</div>
```

Imaginons que la valeur présente dans `data-id` est requise pour pouvoir récupérer la série. On veut donc stocker cette
valeur.

```JSON
{
  "extra_data": [
    {
      "key": "serie_id",
      "path": ".serie a",
      "attr": "data-id"
    }
  ]
}
```

Cette information pourra être utilisée dans [Serie Structure](#serie-structure).

</details>

#### Filters

Il est possible de filtrer les résultats. Le champ filtre est une liste de filtre. Seuls les éléments qui ne sont pas
exclus par un des filtres seront conservés (c'est donc comme s'il y avait un opérateur "AND" entre chaque filtre).

Le filtre peut soit être basé sur un champ déjà parsé, soit sur le HTML.

Dans le premier cas, le champ `elem` permet de sélectionner la clé utilisée pour faire le filtre. Par exemple `title` ou
`url` ou encore dans les extra data: `extra_data.<variable>`.

Pour le second cas, les champs `path` et `attr` permettent de récupérer la valeur que l'on veut dans le HTML. Si le
champ `attr` n'est pas défini, la valeur contenue dans le HTML sera utilisée.

La valeur une fois récupérée, plusieurs conditions peuvent être appliquées. La condition est une clé, et la valeur
associée sera utilisée pour appliquer la condition.

- `eq`
  Vérifie que la valeur est égal à la valeur définie
- `neq`
  Vérifie que la valeur n'est pas égale à la valeur définie
- `contains`
  Vérifie que la valeur récupérée contient la valeur définie
- `not_contains`
  Vérifie que la valeur récupérée ne contient pas la valeur définie

<details> 
  <summary><b>Exemple</b></summary>

```HTML

<div class="series">
    <div class="no-infos">
        HTML element for website structure
    </div>
    <div class="serie1">
        <span>Title</span>
    </div>
</div>
```

```JSON
{
  "list_results": ".series div",
  "filters": [
    {
      "attr": "class",
      "contains": "serie"
    }
  ]
}
```

Ici, le filtre va donc ignorer la div contenant la class `no-infos` car le filtre ne prend que les éléments de "list
results" qui ont "serie" dans la valeur "class".

</details>

Récapitulatif des champs:

| **Clé**        | **Description**                                                 | **Type** |
|----------------|-----------------------------------------------------------------|----------|
| `elem`         | Élément récupéré précédemment et sur lequel appliquer le filtre | `String` |
| `path`         | TODO                                                            |          |
| `attr`         |                                                                 |          |
| `eq`           |                                                                 |          |
| `neq`          |                                                                 |          |
| `contains`     |                                                                 |          |
| `not_contains` |                                                                 |          |

#### Remote infos

### Serie Structure

### Season Structure

### Episode Structure

### Hoster Structure

### Movie Structure

_Pas encore développé_

# Améliorations possibles

Cette version Beta n'est pas complète. Voici quelques points à améliorer/faire:

- prendre en charge les films
- prendre en charge les autres types de contenu (drama/manga/...)
- définir un format pour la langue (devoir faire un parser pour n'avoir que VF, VOSTFR, ...)
- définir un format pour la qualité (devoir faire un parser pour n'avoir qu'une liste de format (à définir))
- permettre de faire des recherches complexes.  
  Certains sites proposent de faire des recherches avancées, en spécifiant l'année par exemple. Le système actuel ne
  gère pas cette possibilité.

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


