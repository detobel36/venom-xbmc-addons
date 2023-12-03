# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import TYPE_CHECKING, List

from resources.site_v2.parser import Parser
from resources.site_v2.serie.result_serie import ResultSerie

if TYPE_CHECKING:
    pass


class ParserSerie(Parser):

    # Override
    def get_list_serie(self, title: str) -> List[ResultSerie]:
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
        request_type = 'POST'
        if 'request' in series_json_data:
            request_type = series_json_data['request']
        response = self._site.get_site_request().request(url, request_type=request_type, list_data=list_data)

        list_result = Parser(self._site).parse_response(response.content,
                                                        self._site.get_search_json()['series']['results'])
        return [ResultSerie.from_result(result) for result in list_result]
