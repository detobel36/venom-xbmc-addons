# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from bs4 import BeautifulSoup

class CustomSelectType:
    """
    Permet de récupérer n'importe quelle valeur sur un site web HTML sur base de différents critères.

    Voici la structure du JSON:
    {
        value: str, # Valeur fixe directement associé à la clé. Si défini, aucun autre champ ne peut être utilisé.
        path: str, # Chemin (HTML Path) vers un élément HTML
        attr: str, # Attribut dans lequel la valeur se trouve	
        prefix: str, # Texte à ajouter au début de la valeur récupérée
        suffix: str, # Texte à ajouter à la fin de la valeur récupérée
        regex: {
            pattern: str # Pattern pour faire match
            repl: str # Valeur de remplacement
        }
    }
    """

    def __init__(self, json_data):
        self._json_data = json_data

    def get_value(self, html_content: BeautifulSoup):
        pass
