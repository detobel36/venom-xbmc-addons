# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import List, Dict, TYPE_CHECKING

from bs4 import BeautifulSoup

from resources.site_v2.filter_utils import FilterUtils

if TYPE_CHECKING:
    from resources.site_v2.site import Site


# Permet de stocker le résultat d'une recherche
# L'idée est de pouvoir, à partir de cet élément, afficher un résultat à l'utilisateur
class Result:

    def __init__(self, site: Site):
        self._site = site
        self._year = None
        self._title = None
        self._thumb = None
        self._url = None
        self._content = None
        self._extra_data = dict()

    def set_title(self, title: str):
        self._title = title

    def set_year(self, year: int):
        self._year = year

    def set_thumb(self, thumb: str):
        self._thumb = thumb

    def set_url(self, url: str):
        self._url = url

    def get_url(self):
        return self._url

    def add_extra_data(self, key, data):
        self._extra_data[key] = data

    def update(self, other_result, erase=True):
        if isinstance(other_result, Result):
            if other_result._title is not None:
                if self._title is None or erase:
                    self._title = other_result._title
            if other_result._year is not None:
                if self._year is None or erase:
                    self._year = other_result._year
            if other_result._thumb is not None:
                if self._thumb is None or erase:
                    self._thumb = other_result._thumb
            if other_result._url is not None:
                if self._url is None or erase:
                    self._url = other_result._url
            if other_result._content is not None:
                if self._content is None or erase:
                    self.set_content(other_result._content, other_result._url)
            if other_result._extra_data is not None and len(other_result._extra_data) > 0:
                if len(self._extra_data) == 0 or erase:
                    for key, value in other_result._extra_data.items():
                        self._extra_data[key] = value
        return self

    def get_key(self, key_name: str) -> str | None:
        if key_name == 'title':
            return self._title
        elif key_name == 'year':
            return self._year
        elif key_name == 'thumb':
            return self._thumb
        elif key_name == 'url':
            return self._url
        elif key_name.startswith('extra_data.'):
            split_key_name = key_name.split('.')
            if len(split_key_name) == 2:
                extra_data_key = split_key_name[1]
                if extra_data_key in self._extra_data:
                    return self._extra_data[extra_data_key]
                else:
                    print("[ERROR] don't find key '" + extra_data_key + "' in extra_data of ",
                          self._site.get_site_key())
            else:
                print("[ERROR] extra_data key needs to define key in the extra_data", key_name)
                return None
        return None

    def set_key(self, key, value):
        if key == 'title':
            self.set_title(value)
        elif key == 'year':
            self.set_year(value)
        elif key == 'thumb':
            self.set_thumb(value)
        elif key == 'url':
            self.set_url(value)
        elif key.startswith('extra_data.'):
            split_key_name = key.split('.')
            if len(split_key_name) == 2:
                extra_data_key = split_key_name[1]
                self._extra_data[extra_data_key] = value
            else:
                print("[ERROR] extra_data key needs to define key in the extra_data", key)
        else:
            print("[ERROR] don't find key '" + key + "' in parameters of ", self._site.get_site_key())

    def is_not_ignore_by_filters(self, list_filters: List[Dict[str, str]]) -> bool:
        """
        Permet de vérifier que le résultat actuel est valide et non ignoré à l'aide des filtres.

        :param list_filters: (List[Dict[str, str]]) Liste des filtres
        :return: bool True si le résultat est valide, False s'il doit être ignoré à cause des filtres
        """
        for item_filter in list_filters:
            if 'elem' in item_filter:
                result = FilterUtils.is_not_ignore_by_filters(item_filter, self.get_key(item_filter['elem']))
                if result is False:
                    return False
        return True

    def __str__(self) -> str:
        result = f"[{self._site.get_site_key()}] "
        if self._title is not None:
            result += self._title.upper()
        if self._year is not None:
            result += f" ({self._year})"
        if self._url is not None:
            result += f"\n\tURL: {self._url}"
        if self._thumb is not None:
            result += f"\n\tImg: {self._thumb}"
        if self._content is not None:
            result += "\n\tContent defined"
        return result

    def set_content(self, soup: BeautifulSoup, url_from: str):
        """
        Contient le contenu de la page qui permet d'avoir ces résultats

        :param soup: le contenu de la page (format donné par BeautifulSoup)
        :param url_from: URL lié au contenu passé au premier paramètre
        """
        if url_from == self._url:
            self._content = soup

    def _fetch_content_if_none(self) -> None:
        if self._content is None:
            # Si on n'a pas le contenu, c'est qu'on arrive ici à cause d'une donnée stockée
            # On doit donc refaire la requête
            response = self._site.get_site_request().request(self._url, request_type='GET')
            self.set_content(BeautifulSoup(response.content, 'html.parser'), self._url)
