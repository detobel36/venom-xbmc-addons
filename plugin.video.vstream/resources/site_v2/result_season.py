# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from resources.site_v2.result import Result
from resources.site_v2.result_serie import ResultSerie

if TYPE_CHECKING:
    from resources.site_v2.site import Site


class ResultSeason(ResultSerie):

    def __init__(self, site: Site):
        super().__init__(site)
        self._season_number = None

    def set_season_number(self, season_number: str):
        self._season_number = season_number

    def __str__(self) -> str:
        result = "<season> " + super().__str__()
        if self._season_number is not None:
            result += f"\n\tSeason: {self._season_number}"
        return result

    def get_key(self, key_name: str) -> str | None:
        result = super().get_key(key_name)
        if result is None:
            if key_name == 'season':
                result = self._season_number
        return result

    def set_key(self, key, value):
        if key == 'season':
            self.set_season_number(value)
        else:
            super().set_key(key, value)

    def update(self, other_result, erase=True):
        super().update(other_result, erase)
        if isinstance(other_result, ResultSeason):
            if other_result._season_number is not None:
                if self._season_number is None or erase:
                    self._season_number = other_result._season_number

    @staticmethod
    def from_result(result: Result) -> ResultSeason:
        season_result = ResultSeason(result._site)
        season_result.update(result)
        return season_result
