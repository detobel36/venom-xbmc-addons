# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from resources.site_v2.site_request import SiteRequest

if TYPE_CHECKING:
    pass


# Représente toutes les informations liées à un site web
class SiteObject:

    def __init__(self, site_key, json_data, is_matrix=True):
        self._site_key = site_key
        self._json_data = json_data
        self._is_matrix = is_matrix
        # Singleton, instancié que si on en a besoin
        self._site_search = None

        self._site_request = SiteRequest(self._is_matrix, self)

    def get_site_key(self) -> str:
        return self._site_key

    def get_url(self) -> str:
        return self._json_data['url']

    def get_search_json(self):
        return self._json_data['search']

    def is_enabled(self) -> bool:
        return self._json_data['active']

    def is_token_protection_enabled(self) -> bool:
        """
        Permet de savoir si le site web actuelle utilise un système de protection
        par token (XSRF)

        Returns:
            bool: True si il y a un système de token, False sinon
        """
        return 'token' in self._json_data

    def get_token_json(self):
        return self._json_data['token']

    def get_site_request(self) -> SiteRequest:
        return self._site_request
