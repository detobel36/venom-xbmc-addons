# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import List, Dict, TYPE_CHECKING

from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject


# Permet de stocker le résultat d'une recherche
# L'idée est de pouvoir, à partir de cet élément, afficher un résultat à l'utilisateur
class SiteResult:

    def __init__(self, site: SiteObject):
        self._site = site
        self._year = None
        self._title = None
        self._thumb = None
        self._url = None
        self._content = None

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

    def update(self, other_result, erase=True):
        if isinstance(other_result, SiteResult):
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
                    self._content = other_result._content
        return self

    def _get_key(self, key_name: str) -> str | None:
        if key_name == 'title':
            return self._title
        elif key_name == 'year':
            return self._year
        elif key_name == 'thumb':
            return self._thumb
        elif key_name == 'url':
            return self._url
        return None

    def is_not_ignore_by_filters(self, list_filters: List[Dict[str, str]]) -> bool:
        """
        Permet de vérifier que le résultat actuel est valide et non ignoré à l'aide des filtres.

        :param list_filters: (List[Dict[str, str]]) Liste des filtres
        :return: bool True si le résultat est valide, False s'il doit être ignoré à cause des filtres
        """
        for item_filter in list_filters:
            if ('elem' in item_filter and
                    ('eq' in item_filter and self._get_key(item_filter['elem']) != item_filter['eq']) or
                    ('neq' in item_filter and self._get_key(item_filter['elem']) == item_filter['neq'])):
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
        return result

    def set_content(self, soup: BeautifulSoup):
        """
        Contient le contenu de la page qui permet d'avoir ces résultats

        :param soup: le contenu de la page (format donné par BeautifulSoup)
        """
        self._content = soup
