# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import os
import sys

import xbmcgui
import xbmcplugin
import xbmcvfs
import xbmc

from resources.lib.comaddon import addon, dialog, VSPath
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.util import QuotePlus

SITE_IDENTIFIER = 'Library'
SITE_NAME = 'Library'

# sources.xml


class Library:
    ADDON = addon()

    def __init__(self):
        self.__sMovieFolder = self.ADDON.getSetting('Library_folder_Movies')
        self.__sTVFolder = self.ADDON.getSetting('Library_folder_TVs')

        if not self.__sMovieFolder:
            self.__sMovieFolder = 'special://userdata/addon_data/plugin.video.vstream/Films'
            self.ADDON.setSetting('Library_folder_Movies', self.__sMovieFolder)
        if not xbmcvfs.exists(self.__sMovieFolder):
            xbmcvfs.mkdir(self.__sMovieFolder)

        if not self.__sTVFolder:
            self.__sTVFolder = 'special://userdata/addon_data/plugin.video.vstream/Series'
            self.ADDON.setSetting('Library_folder_TVs', self.__sTVFolder)
        if not xbmcvfs.exists(self.__sTVFolder):
            xbmcvfs.mkdir(self.__sTVFolder)

        self.__sTitle = ''

    def setLibrary(self):
        input_parameter_handler = InputParameterHandler()
        sHosterIdentifier = input_parameter_handler.getValue(
            'sHosterIdentifier')
        sFileName = input_parameter_handler.getValue('sFileName')
        sMediaUrl = input_parameter_handler.getValue('sMediaUrl')

        ret = dialog().VSselect(['Film', 'Série'],
                                'Sélectionner une catégorie')
        if ret == 0:
            sCat = '1'
        elif ret == -1:
            return
        else:
            sCat = '2'

        sMediaUrl = QuotePlus(sMediaUrl)
        # sFileName = QuotePlus(sFileName)

        sLink = 'plugin://plugin.video.vstream/?function=play&site=HosterGui&sFileName='
        sLink += sFileName + '&sMediaUrl=' + sMediaUrl + \
            '&sHosterIdentifier=' + sHosterIdentifier

        title = sFileName

        if sCat == '1':  # film
            # title = cUtil().CleanName(title)
            title = self.showKeyBoard(title, 'Nom du fichier')

            try:
                sPath = '/'.join([self.__sMovieFolder, title])

                if not xbmcvfs.exists(sPath):
                    xbmcvfs.mkdir(sPath)

                self.MakeFile(sPath, title, sLink)
            except BaseException:
                dialog().VSinfo('Rajout impossible')

        elif sCat == '2':  # serie
            # title = cUtil().CleanName(title)
            sFTitle = self.showKeyBoard(
                title, 'Saison : Recommandé NomDeSerie/Saison01')

            try:

                sPath = '/'.join([self.__sTVFolder, sFTitle])

                if not xbmcvfs.exists(sPath):
                    xbmcvfs.mkdir(sPath)

                title = self.showKeyBoard(
                    title, 'Épisode : Recommandé NomDeSerie S01E01')

                self.MakeFile(sPath, title, sLink)
            except BaseException:
                dialog().VSinfo('Rajout impossible')

    def MakeFile(self, folder, name, content):
        stream = '/'.join([folder, str(name)]) + '.strm'
        f = xbmcvfs.File(stream, 'w')
        result = f.write(str(content))
        f.close()
        if result:
            dialog().VSinfo('Elément rajouté à la librairie')
        else:
            dialog().VSinfo('Rajout impossible')

    def getLibrary(self):
        gui = Gui()
        output_parameter_handler = OutputParameterHandler()

        folder = self.ADDON.getSetting('Library_folder_Movies')
        output_parameter_handler.addParameter('siteUrl', folder)
        gui.addDir(
            SITE_IDENTIFIER,
            'openLibrary',
            self.ADDON.VSlang(30120),
            'films.png',
            output_parameter_handler)

        folder = self.ADDON.getSetting('Library_folder_TVs')
        output_parameter_handler.addParameter('siteUrl', folder)
        gui.addDir(
            SITE_IDENTIFIER,
            'openLibrary',
            self.ADDON.VSlang(30121),
            'series.png',
            output_parameter_handler)

        gui.setEndOfDirectory()

    def getRecords(self):
        gui = Gui()

        folder = self.ADDON.getSetting('path_enregistrement')
        if not folder:
            folder = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement"/>'
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', folder)
        gui.addDir(
            SITE_IDENTIFIER,
            'openLibrary',
            self.ADDON.VSlang(30225),
            'download.png',
            output_parameter_handler)

        gui.setEndOfDirectory()

    def openLibrary(self):
        gui = Gui()
        input_parameter_handler = InputParameterHandler()
        sFile = input_parameter_handler.getValue('siteUrl')

        listDir = xbmcvfs.listdir(sFile)

        if listDir[0]:
            data = listDir[0]
        else:
            data = listDir[1]

        addon_handle = None
        for i in data:
            # Suppression du special: pour plus tard
            path = VSPath(sFile + '/' + i)
            title = os.path.basename(path)  # Titre du fichier .strm

            if '.strm' in i:
                sHosterUrl = sFile + '/' + i
                addon_handle = int(sys.argv[1])
                xbmcplugin.setContent(addon_handle, 'video')
                li = xbmcgui.ListItem(title)
                xbmcplugin.addDirectoryItem(
                    handle=addon_handle, url=sHosterUrl, listitem=li)

            else:
                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter(
                    'siteUrl', sFile + '/' + i)
                gui.addDir(
                    SITE_IDENTIFIER,
                    'openLibrary',
                    title,
                    'films.png',
                    output_parameter_handler)

        if addon_handle:
            xbmcplugin.endOfDirectory(addon_handle)
        else:
            gui.setEndOfDirectory()

    def Delfile(self):
        input_parameter_handler = InputParameterHandler()
        sFile = input_parameter_handler.getValue('sFile')

        xbmcvfs.delete(sFile)

        runClean = self.DIALOG.VSyesno(
            'Voulez vous mettre à jour la librairie maintenant (non conseillé)',
            'Fichier supprimé')
        if not runClean:
            return

        xbmc.executebuiltin('CleanLibrary(video)')

    def ShowContent(self):
        input_parameter_handler = InputParameterHandler()
        sFolder = input_parameter_handler.getValue('folder')
        xbmc.executebuiltin('Container.Update(' + sFolder + ')')

    def showKeyBoard(self, sDefaultText='', Heading=''):
        keyboard = xbmc.Keyboard(sDefaultText)
        keyboard.setHeading(Heading)  # optional
        keyboard.doModal()
        if keyboard.isConfirmed():
            sSearchText = keyboard.getText()
            if (len(sSearchText)) > 0:
                return sSearchText

        return False
