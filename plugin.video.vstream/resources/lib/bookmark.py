# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
import xbmc

from resources.lib.db import Db
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import dialog, Addon, isMatrix
from resources.lib.util import UnquotePlus

SITE_IDENTIFIER = 'cFav'
SITE_NAME = 'Fav'


class cFav:

    DIALOG = dialog()
    ADDON = Addon()

    # Suppression d'un bookmark, d'une catégorie, ou tous les bookmarks
    def delBookmark(self):
        input_parameter_handler = InputParameterHandler()
        if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            return False

        for_all = input_parameter_handler.exist('for_all')
        cat = input_parameter_handler.getValue('cat')
        site_url = input_parameter_handler.getValue('site_url')
        title = input_parameter_handler.getValue('clean_title')
        # title = cUtil().CleanName(title)
        with Db() as db:
            db.del_bookmark(site_url, title, cat, for_all)
        return True

    # Suppression d'un bookmark depuis un Widget
    def delBookmarkMenu(self):
        if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
            return False

        title = xbmc.getInfoLabel('ListItem.Property(clean_title)')
        site_url = xbmc.getInfoLabel('ListItem.Property(site_url)')
        with Db() as db:
            db.del_bookmark(site_url, title)

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
        output_parameter_handler.addParameter('cat', '1')
        total = compt[1] + compt[7]
        gui.addDir(SITE_IDENTIFIER, 'getFav', '%s (%s)' % (self.ADDON.VSlang(30120), str(total)), 'mark.png',
                   output_parameter_handler)

        output_parameter_handler.addParameter('cat', '2')
        total = compt[2] + compt[3] + compt[4] + compt[8] + compt[9]
        gui.addDir(SITE_IDENTIFIER, 'getFav', '%s/%s (%s)' % (self.ADDON.VSlang(30121), self.ADDON.VSlang(30122),
                                                              str(total)), 'mark.png', output_parameter_handler)

        output_parameter_handler.addParameter('cat', '5')
        total = compt[5]
        gui.addDir(SITE_IDENTIFIER, 'getFav', '%s (%s)' % (self.ADDON.VSlang(30410), str(total)), 'mark.png',
                   output_parameter_handler)

        output_parameter_handler.addParameter('cat', '6')
        total = compt[6]
        gui.addDir(SITE_IDENTIFIER, 'getFav', '%s (%s)' % (self.ADDON.VSlang(30332), str(total)), 'mark.png',
                   output_parameter_handler)

        output_parameter_handler.addParameter('for_all', 'true')
        gui.addDir(SITE_IDENTIFIER, 'delBookmark', self.ADDON.VSlang(30209), 'trash.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def getFav(self):
        gui = Gui()
        input_parameter_handler = InputParameterHandler()

        # Comptages des marque-pages
        with Db() as db:
            row = db.get_bookmark()

        if input_parameter_handler.exist('cat'):
            cat = input_parameter_handler.getValue('cat')

            # Série, Animes, Saison, Episodes et Dramas sont visibles dans les
            # marques-page "Séries"
            cat_list = ('2', '3', '4', '8', '9')
            if cat in cat_list:
                cat = 2
                Gui.CONTENT = 'tvshows'
            else:
                cat_list = ('1', '7')    # films, saga
                Gui.CONTENT = 'movies'
                if cat in cat_list:
                    cat = 1
                else:
                    cat_list = cat
                    Gui.CONTENT = 'videos'
            gen = (x for x in row if x['cat'] in cat_list)
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
                    site_url = data['siteurl'].encode('utf-8')
                except BaseException:
                    site_url = data['siteurl']

                if isMatrix():
                    site_url = UnquotePlus(site_url.decode('utf-8'))
                    title = str(title, 'utf-8')
                else:
                    site_url = UnquotePlus(site_url)

                site = data['site']
                function = data['fav']
                cat = data['cat']
                fanart = data['fanart']

                if thumbnail == '':
                    thumbnail = 'False'

                output_parameter_handler = OutputParameterHandler()
                output_parameter_handler.addParameter('site_url', site_url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('searchtext', title)
                output_parameter_handler.addParameter('thumbnail', thumbnail)
                # Dans ajouter source c'est bien thumb donc...
                output_parameter_handler.addParameter('thumb', thumbnail)

                if function == 'play':
                    hoster = HosterGui().checkHoster(site_url)
                    output_parameter_handler.addParameter('hoster_identifier', hoster.getPluginIdentifier())
                    output_parameter_handler.addParameter('file_name', hoster.getFileName())
                    output_parameter_handler.addParameter('media_url', site_url)

                gui_element = GuiElement()
                gui_element.setSiteName(site)
                gui_element.setFunction(function)
                gui_element.setTitle(title)
                gui_element.setFileName(title)
                gui_element.setIcon("mark.png")
                if cat == '1':           # Films
                    gui_element.setMeta(1)
                    gui_element.setCat(1)
                elif cat == '2':          # Séries
                    gui_element.setMeta(2)
                    gui_element.setCat(2)
                elif cat == '3':          # Anime
                    gui_element.setMeta(4)
                    gui_element.setCat(3)
                elif cat == '4':          # Saisons
                    gui_element.setMeta(5)
                    gui_element.setCat(4)
                elif cat == '5':          # Divers
                    gui_element.setMeta(0)
                    gui_element.setCat(5)
                elif cat == '6':          # TV (Officiel)
                    gui_element.setMeta(0)
                    gui_element.setCat(6)
                elif cat == '7':          # Saga
                    gui_element.setMeta(3)
                    gui_element.setCat(7)
                elif cat == '8':          # Episodes
                    gui_element.setMeta(6)
                    gui_element.setCat(8)
                elif cat == '9':          # Drama
                    gui_element.setMeta(2)
                    gui_element.setCat(9)
                else:
                    gui_element.setMeta(0)
                    gui_element.setCat(cat)
                gui_element.setThumbnail(thumbnail)
                gui_element.setFanart(fanart)
                gui_element.addItemProperties('isBookmark', True)

                gui.createSimpleMenu(gui_element, output_parameter_handler, 'cFav', 'cFav', 'delBookmark',
                                     self.ADDON.VSlang(30412))

                if function == 'play':
                    # addHost n'existe plus
                    gui.addHost(gui_element, output_parameter_handler)
                else:
                    gui.addFolder(gui_element, output_parameter_handler)

            except BaseException:
                output_parameter_handler = OutputParameterHandler()
                gui.addDir(SITE_IDENTIFIER, 'DoNothing', '[COLOR red]ERROR[/COLOR]', 'films.png',
                           output_parameter_handler)

        # La suppression n'est pas accessible lors de l'utilisation en Widget
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('cat', cat)
            gui.addDir(SITE_IDENTIFIER, 'delBookmark', self.ADDON.VSlang(30211), 'trash.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def setBookmark(self):
        input_parameter_handler = InputParameterHandler()

        cat = input_parameter_handler.getValue('cat') if input_parameter_handler.exist(
            'cat') else xbmc.getInfoLabel('ListItem.Property(cat)')
        cat_number = 0
        if cat:
            cat_number = int(cat)
        if cat_number < 1 or cat_number > 9:
            self.DIALOG.VSinfo('Error', self.ADDON.VSlang(30038))
            return

        meta = {}

        site_url = cFav.get_input_default_xbmc(input_parameter_handler, 'site_url')
        title = cFav.get_input_default_xbmc(input_parameter_handler, 'movie_title', 'clean_title')
        site = cFav.get_input_default_xbmc(input_parameter_handler, 's_id')
        fav = cFav.get_input_default_xbmc(input_parameter_handler, 'fav')

        if title == '':
            self.DIALOG.VSinfo('Error', 'Probleme sur le titre')
            return

        meta['siteurl'] = site_url
        meta['title'] = title
        meta['site'] = site
        meta['fav'] = fav
        meta['cat'] = cat

        meta['icon'] = xbmc.getInfoLabel('ListItem.Art(thumb)')
        meta['fanart'] = xbmc.getInfoLabel('ListItem.Art(fanart)')
        try:
            # Comptages des marque-pages
            with Db() as db:
                db.insert_bookmark(meta)
        except BaseException:
            pass

    @staticmethod
    def get_input_default_xbmc(input_parameter_handler, key, key2=None):
        if input_parameter_handler.exist(key):
            return input_parameter_handler.getValue(key)
        else:
            if key2 is None:
                key2 = key
            return xbmc.getInfoLabel('ListItem.Property(' + key2 + ')')
