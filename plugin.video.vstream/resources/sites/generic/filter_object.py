# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from typing import Dict
from bs4 import BeautifulSoup

class FilterObject:
    """
    Représente un filtre qui doit être appliqué à une requête. L'objet est composé de deux partie: une partie
    permettant de récuperer la valeur à filter et la seconde qui permet de faire la comparaison (opération + valeur)

    Voici la structure du JSON:
    {
        source: {
            var: str, # Élément récupéré précédemment et sur lequel appliquer le filtre. Exclus les 2 champs suivants
            path: str, # Chemin (HTML Path) vers un élément HTML
            attr: str # Attribut dans lequel la valeur à filtrer se trouve
        },
        operation: str, # Choix possible: eq, neq, contains, not_contains
        value: str # valeur utilisé dans l'opération
    }
    """

    def __init__(self, json_data):
        self._json_data = json_data

    def is_filter(self, html_content: BeautifulSoup, variables: Dict[str, str]) -> bool:
        """
        Permet de savoir si le filtre actuel exclus le résultat actuel

        :param: html_content contenu HTML de l'objet récupéré
        :param: variables calculé pour cet élément
        :return: False si le résultat est exclus et True si il faut le garder
        """
        return True

