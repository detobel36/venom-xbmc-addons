# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING, List, Any

from resources.site_v2.site_result import SiteResult
from resources.site_v2.site_result_season import SiteResultSeason

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject


class SiteResultEpisode(SiteResultSeason):

    def __init__(self, site: SiteObject):
        super().__init__(site)
        self._episode_number = None

    def set_episode_number(self, episode_number: str):
        self._episode_number = episode_number

    def __str__(self) -> str:
        result = "<episode> " + super().__str__()
        if self._episode_number is not None:
            result += f"\n\tEpisode: {self._episode_number}"
        return result

    def update(self, other_result, erase=True):
        super().update(other_result, erase)
        if isinstance(other_result, SiteResultEpisode):
            if other_result._episode_number is not None:
                if self._episode_number is None or erase:
                    self._episode_number = other_result._episode_number

    @staticmethod
    def from_result(result: SiteResult) -> SiteResultEpisode:
        season_result = SiteResultEpisode(result._site)
        season_result.update(result)
        return season_result

    def list_hosts(self) -> List[Any]:
        return []
