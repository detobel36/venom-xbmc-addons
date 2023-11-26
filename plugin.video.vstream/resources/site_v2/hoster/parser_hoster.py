# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING, List, Any

from bs4 import Tag

from resources.site_v2.episode.parser_episode import ParserEpisode
from resources.site_v2.episode.result_episode import ResultEpisode
from resources.site_v2.hoster.result_hoster import ResultHoster
from resources.site_v2.parser import Parser

if TYPE_CHECKING:
    pass


class ParserHoster(ParserEpisode):

    # Override
    def _parse_result(self, elem: Tag, json_data) -> ResultHoster:
        site_result = super()._parse_result(elem, json_data)
        hoster_result = ResultHoster.from_result(site_result)

        if 'host_name' in json_data:
            hoster_result.set_host_name(Parser._read_element_data(elem, json_data['host_name']))

        return hoster_result

    def list_hosts(self, episode: ResultEpisode) -> List[Any]:
        if 'hoster' in self._site.get_search_json():
            # print("Search", self._site.get_search_json()['hoster']['results'])
            # print("IN:", episode.get_content())

            list_result = self.parse_beautiful_soup_and_list_results(
                episode.get_content(), self._site.get_search_json()['hoster']['results'])
            for result_hoster in list_result:
                result_hoster.update(episode, erase=False)
            return list_result
        else:
            return []
