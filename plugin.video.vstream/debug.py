# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

# Ce fichier permet de débug l'application.
# L'idée est de pouvoir lancer directement ce fichier en dehors d'un environment Kodi.
# Outre le fait de faciliter le test (les développeurs ne doivent plus obligatoirement installer Kodi pour pouvoir
# tester vStream), cela permet de lancer des tests automatisés.

import json

from resources.site_v2.site_object import SiteObject


def get_json_data(site_path):
    with open(site_path) as siteFile:
        return json.load(siteFile)


json_data = get_json_data('./resources/sites_v2.json')

for site_key, site_values in json_data['sites'].items():
    site = SiteObject(site_key, site_values, True)
    list_results = site.search_series("Lucifer")
    for result in list_results:
        print(result)

    if len(list_results) > 0:
        print("-------------------")
        print("List season for", site_key)
        list_season = list_results[0].list_season()
        for season in list_season:
            print(season)

        if len(list_season) > 0:
            print("-------------------")
            print("List episode for", site_key)
            list_episode = list_season[0].list_episode()
            for episode in list_episode:
                print(episode)

        print("-------------------")
