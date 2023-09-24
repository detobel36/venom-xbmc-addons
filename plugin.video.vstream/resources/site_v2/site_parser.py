# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

from typing import List, TYPE_CHECKING

from bs4 import Tag, BeautifulSoup

from resources.site_v2.site_result import SiteResult

if TYPE_CHECKING:
    from resources.site_v2.site_object import SiteObject


class SiteParser:

    def __init__(self, site: SiteObject):
        self._site = site

    def parse_beautiful_soup_and_list_results(self, soup: BeautifulSoup, result_json_data) -> List[SiteResult]:
        results: List[SiteResult] = []
        for elem in soup.select(result_json_data['list_results']):
            if 'filters' in result_json_data:
                keep_this_elem = True
                for item_filter in result_json_data['filters']:
                    if 'path' in item_filter:
                        if elem.select_one(item_filter['path']).text.strip() != item_filter['eq']:
                            keep_this_elem = False
                            break
                    elif 'elem' not in item_filter:
                        print("[ERROR] don't find key 'path' or 'elem' in filters of ", self._site.get_site_key())
                if not keep_this_elem:
                    continue

            if "remote_infos" in result_json_data:
                result = self._parse_result(elem, result_json_data)

                # TODO: run in a thread
                response = self._site.get_site_request().request(result.get_url(), "GET")
                soup = BeautifulSoup(response.content, 'html.parser')
                result.update(self._parse_result(soup, result_json_data['remote_infos']))
                result.set_content(soup)
            else:
                result = self._parse_result(elem, result_json_data)

            # Si pas de filtre ou que les filtres ne rejettent pas le résultat
            if 'filters' not in result_json_data or result.is_not_ignore_by_filters(result_json_data['filters']):
                # On l'ajoute à la liste des résultats
                results.append(result)

        return results

    def _parse_result(self, elem: Tag, json_data) -> SiteResult:
        result = SiteResult(self._site)
        if 'url' in json_data:
            if 'path' in json_data['url']:
                elem = elem.select_one(json_data['url']['path'])
            result.set_url(elem.attrs[json_data['url']['attr']])

        if 'thumb' in json_data:
            thumb = elem.select_one(json_data['thumb']['path']).attrs[json_data['thumb']['attr']]
            if thumb[0] == '/':
                thumb = self._site.get_url() + thumb
            result.set_thumb(thumb)

        if 'title' in json_data:
            result.set_title(elem.select_one(json_data['title']).text.strip())

        if 'year' in json_data:
            str_year = elem.select_one(json_data['year']).text.strip()
            try:
                result.set_year(int(str_year))
            except ValueError:
                print("[WARN] Invalid year:", str_year, 'for site', self._site.get_site_key())

        return result

    def parse_response(self, content, json_data) -> List[SiteResult]:
        return self.parse_beautiful_soup_and_list_results(SiteParser.request_beautiful_soup(content), json_data)

    @staticmethod
    def request_beautiful_soup(content):
        return BeautifulSoup(content, 'html.parser')
