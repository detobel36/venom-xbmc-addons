# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from resources.site_v2.request_helper import RequestHelper

if TYPE_CHECKING:
    pass


class Site:
    """
    Représente toutes les informations liées à un site web
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
        # Singleton, instancié que si on en a besoin
        self._site_search = None

        self._site_request = RequestHelper(self._is_matrix, self)

    def get_site_key(self) -> str:
        """
        Récupère la clé qui identifie le site
        :return: la clé
        """
        return self._site_key

    def get_url(self) -> str:
        """
        Récupère l'url du site
        :return: l'url
        """
        return self._json_data['url']

    def get_search_json(self):
        """
        Récupère les informations lié à la section recherche
        :return: dict contenant toutes les informations lié à la recherche
        """
        return self._json_data['search']

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

    def get_token_json(self):
        """
        Récupère les informations lié à la section token
        :return: dict contenant toutes les informations lié à la section token
        """
        return self._json_data['token']

    def get_site_request(self) -> RequestHelper:
        """
        Permet de récupérer le RequestHelper
        :return: RequestHelper
        """
        return self._site_request
