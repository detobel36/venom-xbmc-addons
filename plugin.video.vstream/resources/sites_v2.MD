# Site V2

Ce fichier permet de spécifier les sites web pris en charge par vStream.
Pour chaque site, plusieurs informations seront préciser. Permettant à vStream de savoir comment interroger le site
web afin de récupérer les informations.

Table des matières:

- [Structure](#structure)
    - [Structure globale](#structure-globale)
    - [Structure pour chaque site](#structure-pour-chaque-site)
    - [Structure de la partie token](#structure-de-la-partie-token)
    - [Structure de la partie `search`](#structure-de-la-partie-search)
        - [Paramètre d'une recherche](#paramètre-dune-recherche)
        - [Champs communs dans `results`](#champs-communs-dans-results)
            - [Custom selector type](#custom-selector-type)
            - [Extra data](#extra-data)
            - [Filters](#filters)
            - [Remote infos](#remote-infos)
            - [Data Field Value](#data-field-value)
        - [Serie Structure](#serie-structure)
        - [Season Structure](#season-structure)
        - [Episode Structure](#episode-structure)
        - [Hoster Structure](#hoster-structure)
        - [Movie Structure](#movie-structure)
- [Améliorations possibles](#améliorations-possibles)

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
  "cle_site_2": {
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

| **Clé**        | **Description**                                                       | **Type** |
|----------------|-----------------------------------------------------------------------|----------|
| `elem`         | Élément récupéré précédemment et sur lequel appliquer le filtre       | `String` |
| `path`         | Chemin (HTML Path) vers un élément HTML                               | `String` |
| `attr`         | Attribut dans lequel la valeur à filtrer se trouve                    | `String` |
| `eq`           | Valeur (string) à laquelle l'élément récupéré doit être égal          | `String` |
| `neq`          | Valeur (string) à laquelle l'élément récupéré ne doit pas être égal   | `String` |
| `contains`     | Valeur (string) qui doit être contenue dans l'élément récupéré        | `String` |
| `not_contains` | Valeur (string) qui ne doit pas être contenue dans l'élément récupéré | `String` |

#### Remote infos

Il faut parfois aller récupérer des informations sur "la page d'après".
En effet, imaginons un site qui affiche d'abord la liste des films avec juste leurs noms. Imaginons deux films ayant
le même nom, mais des dates de sortie complètement différente. Pour aider l'utilisateur à choisir "le bon film", on va
vouloir aller chercher cette date. Imaginons que cette date n'est visible qu'après avoir "choisi" le film.

On va utiliser `remote_infos` pour faire requête par film afin d'aller chercher les informations qu'ils nous manquent.

| **Clé**                | **Description**                                                                                                                                                                                          | **Type**                                                                               | **Default** |
|------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|-------------|
| `infos`                | Liste des informations à récupérer. Les champs dans cette liste vont dépendre du type d'élément récupéré (_serie_, _episode_...)<br/> :warning: Ne peut pas être utilisé si `parse_result` est sur `raw` | Dictionnaire clés (`String`) / valeurs ([Custom selector type](#custom-selector-type)) | Vide        |
| `parse_result`         | Indique en quel format le résultat doit être parser. Pour le HTML, Beautifulsoup est utilisé, pour raw, la donnée brute est directement exploitée.                                                       | `HTML`/`raw`                                                                           | `HTML`      |
| `parse_result_raw_key` | Clé dans laquelle sera stocké le résultat de la requête.<br/> N'est pris en compte que si `parse_result` est sur `raw`.                                                                                  | `String`                                                                               | Vide        |
| `method`               | Type de requête effectuée pour récupérer les informations                                                                                                                                                | `POST`/`GET`                                                                           | `GET`       |
| `data_field`           | Paramètres passés lorsque la requête sera exécutée                                                                                                                                                       | Dictionnaire clés (`String`) / valeurs ([Data field value](#data-field-value))         | Vide        |

En général, on va donc simplement définir une partie `infos` avec les champs que l'on veut récupérer. Cela peut être
des champs ["commun"](#champs-communs-dans-results) du genre `title`, `year`...

Un des seuls cas où `infos` n'est pas utilisé, c'est lorsqu'on va faire appel à une page qui n'est pas du HTML.

##### Data Field Value

Lorsqu'une requête est faite, des paramètres peuvent être ajoutées.

Pour les requêtes `POST`, cela se fait dans le body:

```BASH
curl -X POST -d 'param1=ok&param2=lol' https://mon-super-site-de-streaming.com
curl -X POST -H "Content-Type: application/json" -d '{"param1": "ok", "param2": "lol"}' https://mon-super-site-de-streaming.com
```

Pour les requêtes `GET`, cela se fait directement dans l'URL:

```
https://mon-super-site-de-streaming.com?param1=ok&param2=lol
```

Dans ces deux exemples, on passe 2 paramètres: `param1` et `param2` qui ont respectivement la valeur `ok` et `lol`.

| **Clé** | **Description**                                                            | **Type** |
|---------|----------------------------------------------------------------------------|----------|
| `key`   | Clé associé à la valeur                                                    | `String` |
| `value` | Valeur statique a associer à la clé                                        | `String` |
| `var`   | Récupère la valeur associée à la variable déjà récupéré dans les résultats | `String` |

Si `key` vaut `titre` et que `var` vaut `title`, alors la valeur associée à la clé sera le titre (récupéré
précédemment).

```JSON
{
  "key": "titre",
  "var": "title"
}
```

Pour la clé `value`, c'est exactement la même que ce qui se trouve dans `static_params` (dans la partie
[Paramètre d'une recherche](#paramètre-dune-recherche)).

### Serie Structure

La structure de la partie série suit donc ce qui est décrit dans la section
[Paramètre d'une recherche](#paramètre-dune-recherche).

Aucun champ propre à la partie serie n'existe pour l'instant. Seuls les champs décrient dans la section
[Champs communs dans `results`](#champs-communs-dans-results) peuvent être utilisés.

### Season Structure

La structure de la partie season suit donc ce qui est décrit dans la section
[Paramètre d'une recherche](#paramètre-dune-recherche).

La seule chose qui change ce sont les champs étant récupérés dans la partie `results` (voir la section
[Champs communs dans `results`](#champs-communs-dans-results)).

Un champ est rajouté pour cette partie:

| **Clé**  | **Description**     | **Choix possible**                            | **Résultat attendu** |
|----------|---------------------|-----------------------------------------------|----------------------|
| `season` | Numéro de la saison | [Custom selector type](#custom-selector-type) | `String`             |

Dans le futur, le résultat attendu sera un integer mais pour l'instant, c'est un string.

### Episode Structure

La structure de la partie episode suit donc ce qui est décrit dans la section
[Paramètre d'une recherche](#paramètre-dune-recherche).

La seule chose qui change ce sont les champs étant récupérés dans la partie `results` (voir la section
[Champs communs dans `results`](#champs-communs-dans-results)).

Un champ est rajouté pour cette partie:

| **Clé**   | **Description**     | **Choix possible**                            | **Résultat attendu** |
|-----------|---------------------|-----------------------------------------------|----------------------|
| `episode` | Numéro de l'épisode | [Custom selector type](#custom-selector-type) | `String`             |

Dans le futur, le résultat attendu sera un integer mais pour l'instant, c'est un string.

### Hoster Structure

La structure de la partie episode suit donc ce qui est décrit dans la section
[Paramètre d'une recherche](#paramètre-dune-recherche).

La seule chose qui change ce sont les champs étant récupérés dans la partie `results` (voir la section
[Champs communs dans `results`](#champs-communs-dans-results)).

Deux champs sont rajouté pour cette partie:

| **Clé**        | **Description**                                                                         | **Choix possible**                            | **Résultat attendu** |
|----------------|-----------------------------------------------------------------------------------------|-----------------------------------------------|----------------------|
| `host_name`    | Nom de l'hébergeur                                                                      | [Custom selector type](#custom-selector-type) | `String`             |
| `request_data` | Données devant être envoyée lors de la requête à l'hébergeur pour pouvoir voir la vidéo | [Custom selector type](#custom-selector-type) | Dictionnaire         |

En effet, plusieurs hébergeurs ont besoin d'avoir en paramètres plusieurs données pour être sûr que la requête "peut se
faire".

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
