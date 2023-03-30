# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc

from resources.lib.db import Db
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import dialog, addon, isMatrix
from resources.lib.util import UnquotePlus

SITE_IDENTIFIER = 'cFav'
SITE_NAME = 'Fav'


class cFav:

    DIALOG = dialog()
    ADDON = addon()

    # Suppression d'un bookmark, d'une catégorie, ou tous les bookmarks
    def delBookmark(self):
        input_parameter_handler = InputParameterHandler()
        if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            return False

        sAll = input_parameter_handler.exist('sAll')
        sCat = input_parameter_handler.getValue('sCat')
        siteUrl = input_parameter_handler.getValue('siteUrl')
        title = input_parameter_handler.getValue('sCleanTitle')
        # title = cUtil().CleanName(title)
        with Db() as db:
            db.del_bookmark(siteUrl, title, sCat, sAll)
        return True

    # Suppression d'un bookmark depuis un Widget
    def delBookmarkMenu(self):
        if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            return False

        title = xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        siteUrl = xbmc.getInfoLabel('ListItem.Property(siteUrl)')
        with Db() as db:
            db.del_bookmark(siteUrl, title)

        return True

    def getBookmarks(self):
        gui = Gui()

        # Comptages des marque-pages
        with Db() as db:
            row = db.get_bookmark()

        compt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in row:
            compt[int(i[5])] = compt[int(i[5])] + 1

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sCat', '1')
        total = compt[1] + compt[7]
        gui.addDir(
            SITE_IDENTIFIER,
            'getFav',
            ('%s (%s)') %
            (self.ADDON.VSlang(30120),
             str(total)),
            'mark.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '2')
        total = compt[2] + compt[3] + compt[4] + compt[8] + compt[9]
        gui.addDir(
            SITE_IDENTIFIER,
            'getFav',
            ('%s/%s (%s)') %
            (self.ADDON.VSlang(30121),
             self.ADDON.VSlang(30122),
             str(total)),
            'mark.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '5')
        total = compt[5]
        gui.addDir(
            SITE_IDENTIFIER,
            'getFav',
            ('%s (%s)') %
            (self.ADDON.VSlang(30410),
             str(total)),
            'mark.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '6')
        total = compt[6]
        gui.addDir(
            SITE_IDENTIFIER,
            'getFav',
            ('%s (%s)') %
            (self.ADDON.VSlang(30332),
             str(total)),
            'mark.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('sAll', 'true')
        gui.addDir(
            SITE_IDENTIFIER,
            'delBookmark',
            self.ADDON.VSlang(30209),
            'trash.png',
            output_parameter_handler)

        gui.setEndOfDirectory()

    def getFav(self):
        gui = Gui()
        input_parameter_handler = InputParameterHandler()

        # Comptages des marque-pages
        with Db() as db:
            row = db.get_bookmark()

        if (input_parameter_handler.exist('sCat')):
            sCat = input_parameter_handler.getValue('sCat')

            # Série, Animes, Saison, Episodes et Dramas sont visibles dans les
            # marques-page "Séries"
            catList = ('2', '3', '4', '8', '9')
            if sCat in catList:
                sCat = 2
                Gui.CONTENT = 'tvshows'
            else:
                catList = ('1', '7')    # films, saga
                Gui.CONTENT = 'movies'
                if sCat in catList:
                    sCat = 1
                else:
                    catList = sCat
                    Gui.CONTENT = 'videos'
            gen = (x for x in row if x['cat'] in catList)
        else:
            gui.setEndOfDirectory()
            return

        for data in gen:

            try:
                title = data['title'].encode('utf-8')
            except BaseException:
                title = data['title']

            thumbnail = data['icon']

            try:
                try:
                    siteurl = data['siteurl'].encode('utf-8')
                except BaseException:
                    siteurl = data['siteurl']

                if isMatrix():
                    siteurl = UnquotePlus(siteurl.decode('utf-8'))
                    title = str(title, 'utf-8')
                else:
                    siteurl = UnquotePlus(siteurl)

                site = data['site']
                function = data['fav']
                cat = data['cat']
                fanart = data['fanart']

                if thumbnail == '':
                    thumbnail = 'False'

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('siteUrl', siteurl)
                output_parameter_handler.addParameter('sMovieTitle', title)
                output_parameter_handler.addParameter('searchtext', title)
                output_parameter_handler.addParameter('thumbnail', thumbnail)
                # Dans ajouter source c'est bien sThumb donc...
                output_parameter_handler.addParameter('sThumb', thumbnail)

                if (function == 'play'):
                    oHoster = HosterGui().checkHoster(siteurl)
                    output_parameter_handler.addParameter(
                        'sHosterIdentifier', oHoster.getPluginIdentifier())
                    output_parameter_handler.addParameter(
                        'sFileName', oHoster.getFileName())
                    output_parameter_handler.addParameter('sMediaUrl', siteurl)

                oGuiElement = GuiElement()
                oGuiElement.setSiteName(site)
                oGuiElement.setFunction(function)
                oGuiElement.setTitle(title)
                oGuiElement.setFileName(title)
                oGuiElement.setIcon("mark.png")
                if (cat == '1'):           # Films
                    oGuiElement.setMeta(1)
                    oGuiElement.setCat(1)
                elif (cat == '2'):          # Séries
                    oGuiElement.setMeta(2)
                    oGuiElement.setCat(2)
                elif (cat == '3'):          # Anime
                    oGuiElement.setMeta(4)
                    oGuiElement.setCat(3)
                elif (cat == '4'):          # Saisons
                    oGuiElement.setMeta(5)
                    oGuiElement.setCat(4)
                elif (cat == '5'):          # Divers
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(5)
                elif (cat == '6'):          # TV (Officiel)
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(6)
                elif (cat == '7'):          # Saga
                    oGuiElement.setMeta(3)
                    oGuiElement.setCat(7)
                elif (cat == '8'):          # Episodes
                    oGuiElement.setMeta(6)
                    oGuiElement.setCat(8)
                elif (cat == '9'):          # Drama
                    oGuiElement.setMeta(2)
                    oGuiElement.setCat(9)
                else:
                    oGuiElement.setMeta(0)
                    oGuiElement.setCat(cat)
                oGuiElement.setThumbnail(thumbnail)
                oGuiElement.setFanart(fanart)
                oGuiElement.addItemProperties('isBookmark', True)

                gui.createSimpleMenu(
                    oGuiElement,
                    output_parameter_handler,
                    'cFav',
                    'cFav',
                    'delBookmark',
                    self.ADDON.VSlang(30412))

                if (function == 'play'):
                    # addHost n'existe plus
                    gui.addHost(oGuiElement, output_parameter_handler)
                else:
                    gui.addFolder(oGuiElement, output_parameter_handler)

            except BaseException:
                output_parameter_handler = OutputParameterHandler()
                gui.addDir(
                    SITE_IDENTIFIER,
                    'DoNothing',
                    '[COLOR red]ERROR[/COLOR]',
                    'films.png',
                    output_parameter_handler)

        # La suppression n'est pas accessible lors de l'utilisation en Widget
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('sCat', sCat)
            gui.addDir(
                SITE_IDENTIFIER,
                'delBookmark',
                self.ADDON.VSlang(30211),
                'trash.png',
                output_parameter_handler)

        gui.setEndOfDirectory()

        return

    def setBookmark(self):
        input_parameter_handler = InputParameterHandler()

        sCat = input_parameter_handler.getValue('sCat') if input_parameter_handler.exist(
            'sCat') else xbmc.getInfoLabel('ListItem.Property(sCat)')
        iCat = 0
        if sCat:
            iCat = int(sCat)
        if iCat < 1 or iCat > 9:
            self.DIALOG.VSinfo('Error', self.ADDON.VSlang(30038))
            return

        meta = {}

        sSiteUrl = input_parameter_handler.getValue('siteUrl') if input_parameter_handler.exist(
            'siteUrl') else xbmc.getInfoLabel('ListItem.Property(siteUrl)')
        title = input_parameter_handler.getValue('sMovieTitle') if input_parameter_handler.exist(
            'sMovieTitle') else xbmc.getInfoLabel('ListItem.Property(sCleanTitle)')
        sSite = input_parameter_handler.getValue('sId') if input_parameter_handler.exist(
            'sId') else xbmc.getInfoLabel('ListItem.Property(sId)')
        sFav = input_parameter_handler.getValue('sFav') if input_parameter_handler.exist(
            'sFav') else xbmc.getInfoLabel('ListItem.Property(sFav)')

        if title == '':
            self.DIALOG.VSinfo('Error', 'Probleme sur le titre')
            return

        meta['siteurl'] = sSiteUrl
        meta['title'] = title
        meta['site'] = sSite
        meta['fav'] = sFav
        meta['cat'] = sCat

        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] = xbmc.getInfoLabel('ListItem.Art(fanart)')
        try:
            # Comptages des marque-pages
            with Db() as db:
                db.insert_bookmark(meta)
        except BaseException:
            pass
