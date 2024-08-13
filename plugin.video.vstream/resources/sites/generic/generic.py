# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import json

from resources.lib.comaddon import isMatrix, VSPath, VSlog
from resources.sites.generic.site import Site
from resources.sites.generic.request_object import RequestObject

from typing import List


class Generic:

    def __init__(self):
        """
        Constructeur
        """
        self._dict_sites = []
        self._init_list_sites()

    def _init_list_sites(self) -> None:
        """
        Initialise la liste des sites
        """
        path = VSPath('special://home/addons/plugin.video.vstream/resources/sites_generic.json')
        json_data = Generic._get_json_data(path)
        for site_key, site_values in json_data['sites'].items():
            site = Site(site_key, site_values, isMatrix())
            if site.is_enabled():
                self._dict_sites[site_key] = site

    def search_serie(self, search_query: str) -> list:
        return []

    def search_movie(self, search_query: str) -> list:
        list_requests = [] # Use a list to be able to use thread in future
        for site in self._dict_sites.values():
            list_requests.append(site.get_search_movies())
        
        return self._execute_requests_queries(list_requests, {'query': search_query})
        
    
    def _execute_requests_queries(list_requests: List[RequestObject], params: dict) -> list:
        results = []
        for request in list_requests:
            results.append(request.request(params))

        return results

    def show_hosters(self, site_key: str, parameters: dict) -> list:
        site = self._dict_sites.get(site_key)
        if site is None:
            return []

        return []
    
    def show_seasons(self, site_key: str, parameters: dict) -> list:
        site = self._dict_sites.get(site_key)
        if site is None:
            return []

        return []
    
    def show_episodes(self, site_key: str, parameters: dict) -> list:
        site = self._dict_sites.get(site_key)
        if site is None:
            return []

        return []

    @staticmethod
    def _get_json_data(site_path: str) -> dict:
        """
        Charge un fichier json contenant la liste des sites

        :param site_path: chemin du fichier
        :return: la liste des sites
        """
        with open(site_path, encoding='utf-8') as siteFile:
            return json.load(siteFile)
