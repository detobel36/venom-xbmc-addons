# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import BeautifulSoup

from resources.site_v2.site_result import SiteResult

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject


class SiteResultSerie(SiteResult):

    def __init__(self, site: SiteObject):
        super().__init__(site)

    def __str__(self) -> str:
        return "<serie> " + super().__str__()

    @staticmethod
    def from_result(result: SiteResult) -> SiteResultSerie:
        serie_result = SiteResultSerie(result._site)
        serie_result.update(result)
        return serie_result

    def get_content(self) -> BeautifulSoup:
        self._fetch_content_if_none()
        return self._content
