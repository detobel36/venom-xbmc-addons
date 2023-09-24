# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import List, TYPE_CHECKING

from resources.site_v2.site_parser import SiteParser
from resources.site_v2.site_result_serie import SiteResultSerie

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject


class SiteSearch:

    def __init__(self, is_matrix: bool, site: SiteObject):
        self._is_matrix = is_matrix
        self._site = site

    def search_series(self, title: str) -> List[SiteResultSerie]:
        series_json_data = self._site.get_search_json()['series']
        if 'url' not in series_json_data:
            url = self._site.get_url()
        else:
            url = series_json_data['url']

        formatted_title = title
        if 'separator' in series_json_data:
            separator = series_json_data['separator']
            formatted_title = title.replace(' ', separator).replace('&20', separator)

        list_data = {}
        if 'search_param' in series_json_data:
            list_data[series_json_data['search_param']] = formatted_title
        if 'static_params' in series_json_data:
            list_data.update(series_json_data['static_params'])
        response = self._site.get_site_request().request(url, request_type=series_json_data['request'],
                                                         list_data=list_data)

        list_result = SiteParser(self._site).parse_response(response.content,
                                                            self._site.get_search_json()['series']['results'])
        return [SiteResultSerie.from_result(result) for result in list_result]
