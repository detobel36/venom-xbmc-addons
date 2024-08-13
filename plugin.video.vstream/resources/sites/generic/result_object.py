# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from typing import Dict, List

from resources.sites.generic.request_object import RequestObject
from resources.sites.generic.custom_select_type import CustomSelectType
from resources.sites.generic.filter_object import FilterObject


class ResultObject:
    """
    Représente la manière dont le résultat d'une requête va être parsé. Le but est de récupérer une liste de variables
    sur base de la configuration JSON et de la page de résultat récupéré.

    Voici la structure du JSON:
    {
        field_to_loop: CustomSelectType,
        filters: CustomSelectType[],
        list_variables: Dict[string: CustomSelectType],
        continue_request: RequestObject,
        next_request_path: string # nom de la requête suivante (généralement ce sera "season", "hoster", "episode" ect)
    }
    A noter que continue_request & next_request_path sont mutuellement exclusif.
    Le premier permet de continuer les requêtes pour l'état actuel alors que l'autre arrête le traitement pour afficher
    les informations.
    """

    def __init__(self, json_data):
        self._json_data = json_data

    def get_variables(self, content_request) -> Dict[str, str]:
        # TODO
        return {}

    def get_continue_request(self) -> RequestObject:
        # TODO
        # Possible que des paramètres doivent être rajouté. Ou que des valeurs doivent être passé à RequestObject
        return None

    def _get_field_to_loop(self) -> CustomSelectType:
        return CustomSelectType(self._json_data['field_to_loop'])
    
    def _get_filters(self) -> List[FilterObject]:
        return [FilterObject(filter) for filter in self._json_data['filters']]

    def _get_list_variables(self) -> Dict[str, CustomSelectType]:
        result = dict()
        for key in self._json_data['list_variables']:
            result[key] = CustomSelectType(self._json_data['list_variables'][key])
        return result

    def _get_continue_request(self) -> RequestObject:
        return RequestObject(self._json_data['continue_request'])

    def _get_next_request_path(self) -> str:
        return self._json_data['next_request_path']
