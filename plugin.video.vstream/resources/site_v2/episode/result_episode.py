# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from resources.site_v2.result import Result
from resources.site_v2.season.result_season import ResultSeason

if TYPE_CHECKING:
    from resources.site_v2.site import Site


class ResultEpisode(ResultSeason):

    def __init__(self, site: Site):
        super().__init__(site)
        self._episode_number = None

    def set_episode_number(self, episode_number: str):
        self._episode_number = episode_number

    def get_key(self, key_name: str) -> str | None:
        result = super().get_key(key_name)
        if result is None:
            if key_name == 'episode':
                result = self._episode_number
        return result

    def set_key(self, key, value):
        if key == 'episode':
            self.set_episode_number(value)
        else:
            super().set_key(key, value)

    def __str__(self) -> str:
        result = "<episode> " + super().__str__()
        if self._episode_number is not None:
            result += f"\n\tEpisode: {self._episode_number}"
        return result

    def update(self, other_result, erase=True):
        super().update(other_result, erase)
        if isinstance(other_result, ResultEpisode):
            if other_result._episode_number is not None:
                if self._episode_number is None or erase:
                    self._episode_number = other_result._episode_number

    @staticmethod
    def from_result(result: Result) -> ResultEpisode:
        episode_result = ResultEpisode(result._site)
        episode_result.update(result)
        return episode_result
