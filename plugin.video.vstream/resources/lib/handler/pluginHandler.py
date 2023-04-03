# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import sys
import xbmcvfs
import json

from resources.lib.comaddon import Addon, VSlog, VSPath, SiteManager


class PluginHandler:

    def getPluginHandle(self):
        try:
            return int(sys.argv[1])
        except BaseException:
            return 0

    def getPluginPath(self):
        try:
            return sys.argv[0]
        except BaseException:
            return ''

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        items = xbmcvfs.listdir(sFolder)[1]
        items.remove("__init__.py")
        items.sort()

        for sItemName in items:
            if not sItemName.endswith(".py"):
                continue

            sFilePath = "/".join([sFolder, sItemName])

            # xbox hack
            sFilePath = sFilePath.replace('\\', '/')

            if xbmcvfs.exists(sFilePath):
                if sFilePath.lower().endswith('py'):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def __importPlugin(self, sName, label=""):
        try:
            exec("from resources.sites import " + sName, globals())
            exec("site_name = " + sName + ".SITE_NAME", globals())
            if label:
                exec("search = " + sName + "." + label, globals())
                return search[0], search[1], site_name
            else:
                exec("sSiteDesc = " + sName + ".SITE_DESC", globals())
                return site_name, sSiteDesc
        except Exception as e:
            VSlog("Cannot import plugin " + str(sName))
            VSlog("Detail de l\'erreur " + str(e))
            return False, False

    def getAvailablePlugins(self, label="", force=False):

        addons = Addon()
        sites_manager = SiteManager()

        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
        sFolder = sFolder.replace('\\', '/')

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        list_plugins = []
        for file_name in aFileNames:
            if not sites_manager.isEnable(
                    file_name):    # Site désactivé par la team
                continue
            if force or sites_manager.isActive(file_name):
                # wir versuchen das plugin zu importieren
                if label:
                    plugin = self.__importPlugin(file_name, label)
                else:
                    plugin = self.__importPlugin(file_name)

                if plugin[0]:
                    sSiteDesc = plugin[1]
                    if label:
                        site_url = plugin[0]
                        site_name = plugin[2]
                        item = self.__createAvailablePluginsItem(
                            site_url, site_name, file_name, sSiteDesc)
                    else:
                        site_name = plugin[0]
                        item = self.__createAvailablePluginsItem(
                            "", site_name, file_name, sSiteDesc)

                    list_plugins.append(item)

        return list_plugins

    def getAllPlugins(self):
        sites_manager = SiteManager()
        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
        sFolder = sFolder.replace('\\', '/')

        aFileNames = self.__getFileNamesFromFolder(sFolder)

        list_plugins = []
        for file_name in aFileNames:
            if not sites_manager.isEnable(
                    file_name):    # Site désactivé par la team
                continue
            # wir versuchen das plugin zu importieren
            plugin = self.__importPlugin(file_name)
            if plugin[0]:
                site_name = plugin[0]
                sSiteDesc = plugin[1]

                # settings nicht gefunden, also schalten wir es trotzdem
                # sichtbar
                list_plugins.append(
                    self.__createAvailablePluginsItem(
                        "", site_name, file_name, sSiteDesc))

        return list_plugins

    def __createAvailablePluginsItem(
            self,
            site_url,
            sPluginName,
            sPluginIdentifier,
            sPluginDesc):
        aPluginEntry = []
        if site_url:
            aPluginEntry.append(site_url)
        aPluginEntry.append(sPluginName)
        aPluginEntry.append(sPluginIdentifier)
        aPluginEntry.append(sPluginDesc)
        return aPluginEntry
