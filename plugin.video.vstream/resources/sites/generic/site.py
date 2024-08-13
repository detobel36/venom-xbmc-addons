# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING
from resources.sites.generic.request_object import RequestObject
from resources.sites.generic.token_object import TokenObject

# from resources.site_v2.request_helper import RequestHelper

if TYPE_CHECKING:
    pass


class Site:
    """
    Représente toutes les informations liées à un site web

    Voici la structure du JSON:
    {
        url: str,
        label: str,
        active: bool,
        token: {
            enabled: bool,
            protection: bool
        },
        search_movies: RequestObject,
        search_series: RequestObject,
        search: RequestObject
    }
    Sont d'abord appelé "search_movies", "search_series" (en fonction du context). Si ces sesctions ne sont pas trouvé, on
    tombe automatiquement dans "search".
    """

    def __init__(self, site_key, json_data, is_matrix=True):
        """
        Constructeur

        :param site_key: clé qui identifie le site
        :param json_data: les données présentes dans le JSON lié à ce site
        :param is_matrix: True si on est sur Kodi version matrix
        """
        self._site_key = site_key
        self._json_data = json_data
        self._is_matrix = is_matrix

        # self._site_request = RequestHelper(self._is_matrix, self)

    def get_site_key(self) -> str:
        """
        Récupère la clé qui identifie le site
        :return: la clé
        """
        return self._site_key

    def get_url(self, subUrl: str = '') -> str:
        """
        Récupère l'url du site
        :return: l'url
        """
        result = self._json_data['url']
        if (len(result) > 0 and result[-1] != '/' and len(subUrl) > 0 and subUrl[0] != '/'):
            result += '/'
        return result + subUrl

    def get_label(self) -> str:
        """
        Récupère le nom du site qui doit être affiché
        :return: le nom du site
        """
        return self._json_data['label']
    
    def get_search_movies(self) -> RequestObject:
        """
        Récupère les informations lié à la section recherche pour les films
        :return: dict contenant toutes les informations lié à la recherche des films
        """
        if 'search_movies' in self._json_data:
            return RequestObject(self._json_data['search_movies'], self._is_matrix)
        return RequestObject(self._json_data['search'], self._is_matrix)
    
    def get_search_series(self) -> RequestObject:
        """
        Récupère les informations lié à la section recherche pour les series
        :return: dict contenant toutes les informations lié à la recherche des series
        """
        if 'search_series' in self._json_data:
            return RequestObject(self._json_data['search_series'], self._is_matrix)
        return RequestObject(self._json_data['search'], self._is_matrix)

    def is_enabled(self) -> bool:
        """
        Permet de savoir si le site est actif (on désactive les sites qui ne sont plus compatibles)
        :return: True si le site est actif, False sinon
        """
        return self._json_data['active']

    def is_token_protection_enabled(self) -> bool:
        """
        Permet de savoir si le site web actuelle utilise un système de protection
        par token (XSRF)

        :return: True s'il y a un système de token, False sinon
        """
        return 'token' in self._json_data

    def get_token_json(self) -> TokenObject:
        """
        Récupère les informations lié à la section token
        :return: dict contenant toutes les informations lié à la section token
        """
        return TokenObject(self._json_data['token'])

    # def get_site_request(self) -> RequestHelper:
    #     """
    #     Permet de récupérer le RequestHelper
    #     :return: RequestHelper
    #     """
    #     return self._site_request

    @staticmethod
    def from_json(data):
        return Site(data['_site_key'], data['_json_data'], data['_is_matrix'])
