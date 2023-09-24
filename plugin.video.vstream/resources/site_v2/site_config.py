# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

from resources.lib.comaddon import VSPath, VSProfil
import json
import xbmcvfs

class SiteConfig:

    DEFAULT_SITE_PATH = 'special://home/addons/plugin.video.vstream/resources/sites.json'
    MASTER_SITE_PATH = 'special://home/userdata/addon_data/plugin.video.vstream/sites.json'
    USER_SITE_PATH_PART1 = 'special://home/userdata/profiles/'
    USER_SITE_PATH_PART2 = '/addon_data/plugin.video.vstream/sites.json'

    def get_json_data(self):
        # Propriétés par défaut
        default_path = VSPath(self.DEFAULT_SITE_PATH)

        # Propriétés selon le profil
        name = VSProfil()
        if name == 'Master user':   # Le cas par defaut
            path = VSPath(self.MASTER_SITE_PATH)
        else:
            path = VSPath(self.USER_SITE_PATH_PART1 + name + self.USER_SITE_PATH_PART2)

        # Résolution du chemin
        try:
            properties_path = VSPath(path).decode('utf-8')
        except AttributeError:
            properties_path = VSPath(path)

        # Chargement des properties
        try:
            with open(properties_path) as propertiesFile:
                return json.load(propertiesFile)
        except IOError:
            # le fichier n'existe pas, on le crée à partir des settings par défaut
            xbmcvfs.copy(default_path, path)
            with open(properties_path) as propertiesFile:
                return json.load(propertiesFile)
