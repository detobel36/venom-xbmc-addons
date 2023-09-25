# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING, List

from bs4 import Tag

from resources.site_v2.site_parser import SiteParser
from resources.site_v2.site_result_season import SiteResultSeason
from resources.site_v2.site_result_serie import SiteResultSerie

if TYPE_CHECKING:
    pass


class SiteParserSeason(SiteParser):

    # Override
    def _parse_result(self, elem: Tag, json_data) -> SiteResultSeason:
        site_result = super()._parse_result(elem, json_data)
        season_result = SiteResultSeason.from_result(site_result)

        if 'season' in json_data:
            season_result.set_season_number(elem.select_one(json_data['season']).text.strip())

        return season_result

    def list_season(self, serie: SiteResultSerie) -> List[SiteResultSeason]:
        list_result = self.parse_beautiful_soup_and_list_results(
            serie.get_content(), self._site.get_search_json()['season']['results'])
        for result_season in list_result:
            result_season.update(serie, erase=False)
        return list_result
