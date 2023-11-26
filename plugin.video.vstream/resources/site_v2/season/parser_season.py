# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING, List

from bs4 import Tag

from resources.site_v2.parser import Parser
from resources.site_v2.season.result_season import ResultSeason
from resources.site_v2.serie.parser_serie import ParserSerie
from resources.site_v2.serie.result_serie import ResultSerie

if TYPE_CHECKING:
    pass


class ParserSeason(ParserSerie):

    # Override
    def _parse_result(self, elem: Tag, json_data) -> ResultSeason:
        site_result = super()._parse_result(elem, json_data)
        season_result = ResultSeason.from_result(site_result)

        if 'season' in json_data:
            season_result.set_season_number(Parser._read_element_data(elem, json_data['season']))

        return season_result

    def list_season(self, serie: ResultSerie) -> List[ResultSeason]:
        list_result = self.parse_beautiful_soup_and_list_results(
            serie.get_content(), self._site.get_search_json()['season']['results'])
        for result_season in list_result:
            result_season.update(serie, erase=False)
        return list_result
