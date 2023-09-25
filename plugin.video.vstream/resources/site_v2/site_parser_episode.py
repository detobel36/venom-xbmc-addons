# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING, List

from bs4 import Tag

from resources.site_v2.site_parser_season import SiteParserSeason
from resources.site_v2.site_result_episode import SiteResultEpisode
from resources.site_v2.site_result_season import SiteResultSeason

if TYPE_CHECKING:
    pass


class SiteParserEpisode(SiteParserSeason):

    # Override
    def _parse_result(self, elem: Tag, json_data) -> SiteResultEpisode:
        site_result = super()._parse_result(elem, json_data)
        episode_result = SiteResultEpisode.from_result(site_result)

        if 'episode' in json_data:
            if json_data['episode'] != '':
                episode_number = elem.select_one(json_data['episode']).text.strip()
            else:
                episode_number = elem.text.strip()
            episode_result.set_episode_number(episode_number)

        return episode_result

    def list_episode(self, season: SiteResultSeason) -> List[SiteResultEpisode]:
        list_result = self.parse_beautiful_soup_and_list_results(
            season.get_content(), self._site.get_search_json()['episode']['results'])
        for result_season in list_result:
            result_season.update(season, erase=False)
        return list_result
