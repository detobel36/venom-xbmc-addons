# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

# Ce fichier permet de débug l'application.
# L'idée est de pouvoir lancer directement ce fichier en dehors d'un environment Kodi.
# Outre le fait de faciliter le test (les développeurs ne doivent plus obligatoirement installer Kodi pour pouvoir
# tester vStream), cela permet de lancer des tests automatisés.

import json

from resources.site_v2.episode.parser_episode import ParserEpisode
from resources.site_v2.hoster.parser_hoster import ParserHoster
from resources.site_v2.season.parser_season import ParserSeason
from resources.site_v2.serie.parser_serie import ParserSerie
from resources.site_v2.site import Site


def get_json_data(site_path):
    with open(site_path) as siteFile:
        return json.load(siteFile)


json_data = get_json_data('./resources/sites_v2.json')

for site_key, site_values in json_data['sites'].items():
    site = Site(site_key, site_values, True)
    if site.is_enabled():
        list_results = ParserSerie(site).get_list_serie("Lucifer")
        for result in list_results:
            print(result)

        if len(list_results) > 0:
            print("-------------------")
            print("List season for", site_key)
            list_season = ParserSeason(site).list_season(list_results[0])
            for season in list_season:
                print(season)

            if len(list_season) > 0:
                # print("-------------------")
                # print("List episode for", site_key)
                list_episode = ParserEpisode(site).list_episode(list_season[0])
                # for episode in list_episode:
                #     print(episode)

                if len(list_episode) > 0:
                    print("List host for ", list_episode[0])
                    print("-------------------")
                    print("List hoster for", site_key)
                    list_hoster = ParserHoster(site).list_hosts(list_episode[0])
                    for hoster in list_hoster:
                        print(hoster)

            print("-------------------")
