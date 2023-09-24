# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from bs4 import Tag

from resources.site_v2.site_parser import SiteParser
from resources.site_v2.site_result_season import SiteResultSeason

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject


class SiteParserSeason(SiteParser):

    def __init__(self, site: SiteObject):
        super().__init__(site)

    # Override
    def _parse_result(self, elem: Tag, json_data) -> SiteResultSeason:
        site_result = super()._parse_result(elem, json_data)
        season_result = SiteResultSeason.from_result(site_result)

        if 'season' in json_data:
            season_result.set_season_number(elem.select_one(json_data['season']).text.strip())

        return season_result
