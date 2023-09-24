# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import Tag

from resources.site_v2.site_parser_season import SiteParserSeason
from resources.site_v2.site_result_episode import SiteResultEpisode

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject


class SiteParserEpisode(SiteParserSeason):

    def __init__(self, site: SiteObject):
        super().__init__(site)

    # Override
    def _parse_result(self, elem: Tag, json_data) -> SiteResultEpisode:
        site_result = super()._parse_result(elem, json_data)
        episode_result = SiteResultEpisode.from_result(site_result)

        if 'episode' in json_data:
            episode_result.set_episode_number(elem.select_one(json_data['episode']).text.strip())

        return episode_result
