# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from typing import List, Dict

from bs4 import BeautifulSoup

from resources.sites.generic.data_object import DataObject
from resources.sites.generic.result_object import ResultObject
from resources.sites.generic.token_object import TokenObject
from resources.sites.generic.request_helper import RequestHelper


class RequestObject:
    """
    Représente une requête qui doit être faite

    Voici la structure du JSON:
    {
        sub_url: str,
        method: str,
        data: DataObject[],
        result: ResultObject
    }
    A noter que data peut être une liste vide
    """

    def __init__(self, json_data, is_matrix: bool):
        self._json_data = json_data
        self._is_matrix = is_matrix

    def request(self, url: str, extra_data: Dict[str, str], token_object: TokenObject) -> dict:
        """
        Récupère les informations liées à la requête

        :param extra_data: données à rajouter aux données déjà enregistré dans cette requête
        :return: variables récupéré grace à la requête
        """
        request_helper = RequestHelper(self._is_matrix)
        list_data = self._build_data(extra_data)
        html_result = request_helper.request(url + self._get_sub_url(), self._get_method(), token_object, list_data)
        beautifulSoup = BeautifulSoup(html_result, 'html.parser')

        self._get_result().get_variables() # TOIDO continuer ici

    def _get_sub_url(self) -> str:
        return self._json_data.get('sub_url', '')

    def _get_method(self) -> str:
        return self._json_data.get('method', 'GET')

    def _get_data(self) -> List[DataObject]:
        return [DataObject(data) for data in self._json_data['data']]
    
    def _build_data(self, extra_data: Dict[str, str]) -> Dict[str, str]:
        result = {}
        for data in self._get_data():
            result[data.get_field_name()] = data.get_value(extra_data)
        return result

    def _get_result(self) -> ResultObject:
        return ResultObject(self._json_data['result'])
