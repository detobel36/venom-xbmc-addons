# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from __future__ import annotations

import re
from typing import List, TYPE_CHECKING

from bs4 import Tag, BeautifulSoup

from resources.site_v2.filter_utils import FilterUtils
from resources.site_v2.result import Result

if TYPE_CHECKING:
    from resources.site_v2.site import Site


class Parser:
    """
    Analyse une page web et récupère des informations
    """

    def __init__(self, site: Site):
        """
        Constructeur
        :param site: information sur le site
        """
        self._site = site

    def parse_beautiful_soup_and_list_results(self, soup: BeautifulSoup, result_json_data) -> List[Result]:
        """
        Analyse une page web et récupère des informations
        :param soup: instance de beautifulSoup qui contient les informations
        :param result_json_data: json qui dit comment analyser les données
        :return: une liste de résultats
        """
        results: List[Result] = []
        for elem in soup.select(result_json_data['list_results']):
            if 'filters' in result_json_data:
                keep_this_elem = True
                for item_filter in result_json_data['filters']:
                    if 'elem' not in item_filter:
                        filter_elem = elem
                        if 'path' in item_filter and item_filter['path'] != '':
                            filter_elem = filter_elem.select_one(item_filter['path'])

                        if 'attr' in item_filter and item_filter['attr']:
                            value_filter_elem = filter_elem.attrs[item_filter['attr']]
                        else:
                            value_filter_elem = filter_elem.text.strip()

                        if not FilterUtils.is_not_ignore_by_filters(item_filter, value_filter_elem):
                            keep_this_elem = False
                            break

                if not keep_this_elem:
                    continue

            if "remote_infos" in result_json_data:
                result = self._parse_result(elem, result_json_data)

                method = 'GET'
                list_data = None
                if 'method' in result_json_data['remote_infos']:
                    method = result_json_data['remote_infos']['method']

                if 'data_field' in result_json_data['remote_infos']:
                    list_data = {}
                    for data_field in result_json_data['remote_infos']['data_field']:
                        if 'var' in data_field:
                            list_data[data_field['key']] = result.get_key(data_field['var'])
                        elif 'value' in data_field:
                            list_data[data_field['key']] = data_field['value']

                # TODO: run in a thread
                response = self._site.get_site_request().request(result.get_url(), method, list_data=list_data)
                if ('parse_result' not in result_json_data['remote_infos'] or
                        result_json_data['remote_infos']['parse_result'] == 'HTML'):
                    soup = BeautifulSoup(response.content, 'html.parser')
                    result.update(self._parse_result(soup, result_json_data['remote_infos']['infos']))
                elif ('parse_result' in result_json_data['remote_infos'] and
                      result_json_data['remote_infos']['parse_result'] == 'raw'):
                    result.set_key(result_json_data['remote_infos']['parse_result_raw_key'],
                                   response.content.decode('utf-8').strip())
                else:
                    print('[ERROR] No valid parsing method for site', self._site.get_site_key())

                result.set_content(soup, result.get_url())

            else:
                result = self._parse_result(elem, result_json_data)

            # Si pas de filtre ou que les filtres ne rejettent pas le résultat
            if 'filters' not in result_json_data or result.is_not_ignore_by_filters(result_json_data['filters']):
                # On l'ajoute à la liste des résultats
                results.append(result)

        return results

    def _parse_result(self, elem: Tag, json_data) -> Result:
        result = Result(self._site)
        if 'url' in json_data:
            result.set_url(Parser._read_element_data(elem, json_data['url']))

        if 'thumb' in json_data:
            thumb = Parser._read_element_data(elem, json_data['thumb'])
            if thumb[0] == '/':
                thumb = self._site.get_url() + thumb
            result.set_thumb(thumb)

        if 'title' in json_data:
            result.set_title(Parser._read_element_data(elem, json_data['title']))

        if 'year' in json_data:
            str_year = Parser._read_element_data(elem, json_data['year'])
            try:
                result.set_year(int(str_year))
            except ValueError:
                print("[WARN] Invalid year:", str_year, 'for site', self._site.get_site_key())

        if 'lang' in json_data:
            result.set_lang(Parser._read_element_data(elem, json_data['lang']))

        if 'quality' in json_data:
            result.set_quality(Parser._read_element_data(elem, json_data['quality']))

        if 'extra_data' in json_data:
            for json_data_elem in json_data['extra_data']:
                result.add_extra_data(json_data_elem['key'], Parser._read_element_data(elem, json_data_elem))

        return result

    def parse_response(self, content, json_data) -> List[Result]:
        return self.parse_beautiful_soup_and_list_results(Parser.request_beautiful_soup(content), json_data)

    @staticmethod
    def _read_element_data(elem: Tag, json_data_element) -> str:
        if 'value' in json_data_element and json_data_element['value'] != '':
            return json_data_element['value']

        if 'path' in json_data_element and json_data_element['path'] != '':
            elem = elem.select_one(json_data_element['path'])
        if 'attr' in json_data_element and json_data_element['attr'] != '':
            result = elem.attrs[json_data_element['attr']]
        else:
            result = elem.text.strip()
        if 'prefix' in json_data_element and json_data_element['prefix'] != '':
            result = json_data_element['prefix'] + result
        if 'suffix' in json_data_element and json_data_element['suffix'] != '':
            result += json_data_element['suffix']

        if 'regex' in json_data_element:
            result = re.sub(json_data_element['regex']['pattern'], json_data_element['regex']['repl'], result)

        return result

    @staticmethod
    def request_beautiful_soup(content):
        return BeautifulSoup(content, 'html.parser')
