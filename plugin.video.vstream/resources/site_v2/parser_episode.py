# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING, List

from bs4 import Tag

from resources.site_v2.parser import Parser
from resources.site_v2.parser_season import ParserSeason
from resources.site_v2.result_episode import ResultEpisode
from resources.site_v2.result_season import ResultSeason

if TYPE_CHECKING:
    pass


class ParserEpisode(ParserSeason):

    # Override
    def _parse_result(self, elem: Tag, json_data) -> ResultEpisode:
        site_result = super()._parse_result(elem, json_data)
        episode_result = ResultEpisode.from_result(site_result)

        if 'episode' in json_data:
            episode_result.set_episode_number(Parser._read_element_data(elem, json_data['episode']))

        return episode_result

    def list_episode(self, season: ResultSeason) -> List[ResultEpisode]:
        list_result = self.parse_beautiful_soup_and_list_results(
            season.get_content(), self._site.get_search_json()['episode']['results'])
        for result_season in list_result:
            result_season.update(season, erase=False)
        return list_result
