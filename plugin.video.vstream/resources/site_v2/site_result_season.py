# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from resources.site_v2.site_result import SiteResult
from resources.site_v2.site_result_serie import SiteResultSerie

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject


class SiteResultSeason(SiteResultSerie):

    def __init__(self, site: SiteObject):
        super().__init__(site)
        self._season_number = None

    def set_season_number(self, season_number: str):
        self._season_number = season_number

    def __str__(self) -> str:
        result = "<season> " + super().__str__()
        if self._season_number is not None:
            result += f"\n\tSeason: {self._season_number}"
        return result

    def update(self, other_result, erase=True):
        super().update(other_result, erase)
        if isinstance(other_result, SiteResultSeason):
            if other_result._season_number is not None:
                if self._season_number is None or erase:
                    self._season_number = other_result._season_number

    @staticmethod
    def from_result(result: SiteResult) -> SiteResultSeason:
        season_result = SiteResultSeason(result._site)
        season_result.update(result)
        return season_result
