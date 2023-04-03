# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.comaddon import Addon, VSlog, SiteManager
from resources.lib.db import Db

import sys
import xbmcvfs


class cRechercheHandler:
    Count = 0

    def __init__(self):
        self.__sText = ""
        self.__sDisp = ""
        self.__sCat = ""
        self.__siteAdded = False

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

    def setText(self, text):
        if not text:
            return False
        self.__sText = text
        return self.__sText

    def getText(self):
        return self.__sText

    def setCat(self, cat):
        if not cat:
            return False
        self.__sCat = str(cat)
        return self.__sCat

    def getCat(self):
        return self.__sCat

    def setDisp(self, sDisp):
        if not sDisp:
            return False
        self.__sDisp = sDisp
        return self.__sDisp

    def getDisp(self):
        return self.__sDisp

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        items = xbmcvfs.listdir(sFolder)[1]
        items.remove("__init__.py")
        items.sort()

        for sItemName in items:
            sFilePath = "/".join([sFolder, sItemName])
            sFilePath = sFilePath.replace('\\', '/')

            if xbmcvfs.exists(sFilePath):
                if sFilePath.lower().endswith('py'):
                    sItemName = sItemName.replace('.py', '')
                    aNameList.append(sItemName)
        return aNameList

    def importPlugin(self, sName, cat):
        pluginData = {}

        if cat == '1':
            search = 'URL_SEARCH_MOVIES'
        elif cat == '2':
            search = 'URL_SEARCH_SERIES'
        elif cat == '3':
            search = 'URL_SEARCH_ANIMS'
        elif cat == '4':
            search = 'URL_SEARCH_SERIES'
        elif cat == '5':
            search = 'URL_SEARCH_MISC'
        elif cat == '6':
            search = 'URL_SEARCH_REPLAY'
        elif cat == '7':
            search = 'URL_SEARCH_MOVIES'
        elif cat == '8':
            search = 'URL_SEARCH_SERIES'
        elif cat == '9':
            search = 'URL_SEARCH_DRAMAS'
        else:
            search = 'URL_SEARCH'

        try:
            plugin = __import__('resources.sites.%s' % sName, fromlist=[sName])
            pluginData['identifier'] = plugin.SITE_IDENTIFIER
            pluginData['name'] = plugin.SITE_NAME
            pluginData['search'] = getattr(plugin, search)
            return pluginData
        except Exception as e:
            if ("has no attribute '%s'" % search) not in str(e):
                VSlog(str(e))
            return False

    def getAvailablePlugins(self):
        text = self.getText()
        if not text:
            return False
        cat = self.getCat()
        if not cat:
            return False

        # historique
        addons = Addon()
        try:
            if addons.getSetting("history-view") == 'true':
                meta = {'title': text, 'disp': cat}
                with Db() as db:
                    db.insert_history(meta)
        except Exception as e:
            VSlog(str(e))
            pass

        sFolder = "special://home/addons/plugin.video.vstream/resources/sites"
        sFolder = sFolder.replace('\\', '/')
        VSlog("Sites Folder: " + sFolder)

        sites_manager = SiteManager()

        list_plugins = []
        aFileNames = self.__getFileNamesFromFolder(sFolder)
        for file_name in aFileNames:
            if sites_manager.isEnable(file_name):
                if sites_manager.isActive(file_name):
                    plugin = self.importPlugin(file_name, cat)
                    if plugin:
                        list_plugins.append(plugin)

        return list_plugins

    def __createAvailablePluginsItem(
            self,
            sPluginName,
            sPluginIdentifier,
            sPluginDesc):
        aPluginEntry = [sPluginName, sPluginIdentifier, sPluginDesc]
        return aPluginEntry
