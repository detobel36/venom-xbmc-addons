# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING

from resources.site_v2.episode.result_episode import ResultEpisode
from resources.site_v2.result import Result

if TYPE_CHECKING:
    from resources.site_v2.site import Site


class ResultHoster(ResultEpisode):

    def __init__(self, site: Site):
        super().__init__(site)
        self._host_name = None
        self._request_data = None

    def set_host_name(self, host_name: str):
        self._host_name = host_name

    def set_request_data(self, request_data: str):
        self._request_data = request_data

    def get_key(self, key_name: str) -> str | None:
        result = super().get_key(key_name)
        if result is None:
            if key_name == 'host_name':
                result = self._host_name
            elif key_name == 'request_data':
                result = self._request_data
        return result

    def set_key(self, key, value):
        if key == 'host_name':
            self.set_host_name(value)
        elif key == 'request_data':
            self.set_request_data(value)
        else:
            super().set_key(key, value)

    def __str__(self) -> str:
        result = "<hoster> " + super().__str__()
        if self._host_name is not None:
            result += f"\n\tHost: {self._host_name}"
        return result

    def update(self, other_result, erase=True):
        super().update(other_result, erase)
        if isinstance(other_result, ResultHoster):
            if other_result._host_name is not None:
                if self._host_name is None or erase:
                    self._host_name = other_result._host_name
            if other_result._request_data is not None:
                if self._request_data is None or erase:
                    self._request_data = other_result._request_data

    @staticmethod
    def from_result(result: Result) -> ResultHoster:
        hoster_result = ResultHoster(result._site)
        hoster_result.update(result)
        return hoster_result
