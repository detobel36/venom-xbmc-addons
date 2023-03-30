# -*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.comaddon import dialog, addon, xbmc, isMatrix
from resources.lib.db import Db
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.util import UnquotePlus

SITE_IDENTIFIER = 'cViewing'
SITE_NAME = 'Viewing'


class cViewing:

    DIALOG = dialog()
    ADDON = addon()

    # Suppression d'un bookmark, d'une catégorie, ou tous les bookmarks
    def delViewing(self):
        input_parameter_handler = InputParameterHandler()
        sTitleWatched = input_parameter_handler.getValue('sTitleWatched')
        sCat = input_parameter_handler.getValue('sCat')

        if not sTitleWatched:  # confirmation if delete ALL
            if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return False

        meta = {}
        meta['titleWatched'] = sTitleWatched
        if sCat:
            meta['cat'] = sCat

        with Db() as db:
            if db.del_viewing(meta):
                self.DIALOG.VSinfo(addon().VSlang(30072))
                Gui().updateDirectory()
            return True

    # Suppression d'un bookmark depuis un Widget
    def delViewingMenu(self):
        title = xbmc.getInfoLabel('ListItem.OriginalTitle')
        if not title:    # confirmation if delete ALL
            if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return False
        sCat = xbmc.getInfoLabel('ListItem.Property(sCat)')
        meta = {}
        meta['titleWatched'] = title
        meta['cat'] = sCat
        with Db() as db:
            if db.del_viewing(meta):
                self.DIALOG.VSinfo(addon().VSlang(30072))
                Gui().updateDirectory()

            return True

    def showMenu(self):
        gui = Gui()
        addons = addon()

        output_parameter_handler = OutputParameterHandler()
        gui.addDir(
            SITE_IDENTIFIER,
            'getViewing',
            addons.VSlang(30126),
            'genres.png',
            output_parameter_handler)

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sCat', '1')       # films
        gui.addDir(
            SITE_IDENTIFIER,
            'getViewing',
            addons.VSlang(30120),
            'films.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '4')       # saisons
        gui.addDir(
            SITE_IDENTIFIER,
            'getViewing',
            '%s/%s' %
            (self.ADDON.VSlang(30121),
             self.ADDON.VSlang(30122)),
            'series.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '5')       # Divers
        gui.addDir(
            SITE_IDENTIFIER,
            'getViewing',
            self.ADDON.VSlang(30410),
            'buzz.png',
            output_parameter_handler)

        gui.setEndOfDirectory()

    def getViewing(self):
        gui = Gui()

        input_parameter_handler = InputParameterHandler()
        catFilter = input_parameter_handler.getValue('sCat')

        with Db() as DB:
            row = DB.get_viewing()
            if not row:
                gui.setEndOfDirectory()
                return

            for data in row:

                try:
                    title = data['title'].encode('utf-8')
                except BaseException:
                    title = data['title']

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

                    sTitleWatched = data['title_id']
                    site = data['site']
                    function = data['fav']
                    cat = data['cat']
                    sSeason = data['season']
                    sTmdbId = data['tmdb_id'] if data['tmdb_id'] != '0' else None

                    if catFilter is not False and cat != catFilter:
                        continue

                    output_parameter_handler = OutputParameterHandler()
                    output_parameter_handler.addParameter('siteUrl', siteurl)
                    output_parameter_handler.addParameter('sMovieTitle', title)
                    output_parameter_handler.addParameter('sTmdbId', sTmdbId)
                    output_parameter_handler.addParameter(
                        'sTitleWatched', sTitleWatched)
                    output_parameter_handler.addParameter('sSeason', sSeason)
                    output_parameter_handler.addParameter('sCat', cat)
                    output_parameter_handler.addParameter('isViewing', True)

                    # pourcentage de lecture
                    meta = {}
                    meta['title'] = sTitleWatched
                    resumetime, totaltime = DB.get_resume(meta)
                    output_parameter_handler.addParameter(
                        'ResumeTime', resumetime)
                    output_parameter_handler.addParameter(
                        'TotalTime', totaltime)

                    if cat == '1':
                        oListItem = gui.addMovie(
                            site, function, title, 'films.png', '', title, output_parameter_handler)
                    elif cat == '4':
                        oListItem = gui.addSeason(
                            site, function, title, 'series.png', '', title, output_parameter_handler)
                    elif cat == '5':
                        oListItem = gui.addMisc(
                            site, function, title, 'buzz.png', '', title, output_parameter_handler)
                    else:
                        oListItem = gui.addTV(
                            site,
                            function,
                            title,
                            'series.png',
                            '',
                            title,
                            output_parameter_handler)

                    output_parameter_handler.addParameter(
                        'sTitleWatched', sTitleWatched)
                    output_parameter_handler.addParameter('sCat', cat)
                    oListItem.addMenu(
                        SITE_IDENTIFIER,
                        'delViewing',
                        self.ADDON.VSlang(30412),
                        output_parameter_handler)

                except Exception as e:
                    pass

        # Vider toute la catégorie n'est pas accessible lors de l'utilisation
        # en Widget
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('sCat', catFilter)
            gui.addDir(
                SITE_IDENTIFIER,
                'delViewing',
                self.ADDON.VSlang(30211),
                'trash.png',
                output_parameter_handler)

        gui.setEndOfDirectory()

        return
