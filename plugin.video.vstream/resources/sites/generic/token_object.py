# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

class TokenObject:
    """
    Information si il faut faire une requête préalable aux autres requêtes afin d'avoir un token et de pouvoir
    récupérer des informations.

    Voici la structure du JSON:
    {
        url: str, # URL utilisée pour récupérer le token (une requête GET est faite la dessus)	
        html_token_input: str, # HTML Path permettant de récupérer l'input qui contient le token
        data_key: str # Nom de la variable qui sera utilisée pour stocker le résultat
    }
    """

    def __init__(self, json_data):
        self._json_data = json_data

    def getUrl(self) -> str:
        return self._json_data.get('url')

    def isHtmlTokenInput(self) -> bool:
        return 'html_token_input' in self._json_data

    def getHtmlTokenInput(self) -> str:
        return self._json_data.get('html_token_input')

    def getDataKey(self) -> str:
        return self._json_data.get('data_key')
