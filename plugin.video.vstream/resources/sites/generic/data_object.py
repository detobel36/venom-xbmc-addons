# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from typing import Dict


class DataObject:
    """
    Représente les données qui doivent être passée pour faire une requête

    Voici la structure du JSON:
    {
        field_name: str, # Le nom dans laquelle cette donnée doit être mis
        variable: str, # La variable qui doit être mis comme valeur
        # Le séparateur à utilisé pour replacer les espaces dans la valeur. Seulement pris en compte si variable est
        # défini
        separator: str,
        static: str # Une valeur static (fixe) à mettre comme valeur
    }
    """

    def __init__(self, json_data, parameters: dict):
        """
        Constructeur

        :param: json_data données JSON contenue dans la config
        :param: parameters paramètres déjà calculés qui peuvent être utilisé pour définir les valeurs des paramètres
        """
        self._json_data = json_data
        self._parameters = parameters

    def get_field_name(self) -> str:
        return self._json_data['field_name']

    def get_value(self, variables: Dict[str, str]) -> str:
        """
        Récupération d'un string contenant les données encodée. Sur base de la configuration JSON, cette fonction créé
        les données et les encodes.

        :return: string contenant les données encodées
        """
        result = ""
        if 'variable' in self._json_data:
            result = variables[self._json_data['variable']]
            if 'separator' in self._json_data:
                result = result.replace(' ', self._json_data['separator'])
        elif 'static' in self._json_data:
            result = self._json_data['static']
        else:
            # TODO raise an exception
            print("Error in DataObject, no variable and no static")
        return result
