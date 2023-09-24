# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING, List

from resources.site_v2.site_parser import SiteParser
from resources.site_v2.site_parser_season import SiteParserSeason
from resources.site_v2.site_result import SiteResult

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject
    from resources.site_v2.site_result_season import SiteResultSeason


class SiteResultSerie(SiteResult):

    def __init__(self, site: SiteObject):
        super().__init__(site)

    def list_season(self) -> List[SiteResultSeason]:
        self._fetch_content_if_none()
        list_result = SiteParserSeason(self._site).parse_beautiful_soup_and_list_results(
            self._content, self._site.get_search_json()['season']['results'])
        return self._update_result_with_current_elem(list_result)

    def _fetch_content_if_none(self) -> None:
        if self._content is None:
            # Si on n'a pas le contenu, c'est qu'on arrive ici à cause d'une donnée stockée
            # On doit donc refaire la requête
            response = self._site.get_site_request().request(self._url, request_type='GET')
            self._content = SiteParser.request_beautiful_soup(response.content)

    def _update_result_with_current_elem(self, list_result) -> List[SiteResult]:
        for result_season in list_result:
            result_season.update(self, erase=False)
        return list_result

    def __str__(self) -> str:
        return "<serie> " + super().__str__()

    @staticmethod
    def from_result(result: SiteResult) -> SiteResultSerie:
        serie_result = SiteResultSerie(result._site)
        serie_result.update(result)
        return serie_result
