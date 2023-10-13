from typing import Dict


class FilterUtils:

    @staticmethod
    def is_not_ignore_by_filters(item_filter: Dict[str, str], value_used_to_filter) -> bool:
        """
        Permet de vérifier que le résultat actuel est valide et non ignoré à l'aide de filtre.

        :param item_filter: (Dict[str, str]) Filtre
        :param value_used_to_filter: (str) Valeur utilisée pour filtrer
        :return: bool True si le résultat est valide, False s'il doit être ignoré à cause du filtre
        """
        if (('eq' in item_filter and value_used_to_filter != item_filter['eq']) or
                ('neq' in item_filter and value_used_to_filter == item_filter['neq']) or
                ('contains' in item_filter and item_filter['contains'] not in value_used_to_filter) or
                ('not_contains' in item_filter and item_filter['not_contains'] in value_used_to_filter)):
            return False
        return True
