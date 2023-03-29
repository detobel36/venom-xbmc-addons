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
        oInputParameterHandler = InputParameterHandler()
        sTitleWatched = oInputParameterHandler.getValue('sTitleWatched')
        sCat = oInputParameterHandler.getValue('sCat')

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
        sTitle = xbmc.getInfoLabel('ListItem.OriginalTitle')
        if not sTitle:    # confirmation if delete ALL
            if not self.DIALOG.VSyesno(self.ADDON.VSlang(30456)):
                return False
        sCat = xbmc.getInfoLabel('ListItem.Property(sCat)')
        meta = {}
        meta['titleWatched'] = sTitle
        meta['cat'] = sCat
        with Db() as db:
            if db.del_viewing(meta):
                self.DIALOG.VSinfo(addon().VSlang(30072))
                Gui().updateDirectory()

            return True

    def showMenu(self):
        oGui = Gui()
        addons = addon()

        oOutputParameterHandler = OutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'getViewing', addons.VSlang(30126), 'genres.png', oOutputParameterHandler)

        oOutputParameterHandler = OutputParameterHandler()
        oOutputParameterHandler.addParameter('sCat', '1')       # films
        oGui.addDir(SITE_IDENTIFIER, 'getViewing', addons.VSlang(30120), 'films.png', oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '4')       # saisons
        oGui.addDir(
            SITE_IDENTIFIER,
            'getViewing',
            '%s/%s' %
            (self.ADDON.VSlang(30121),
             self.ADDON.VSlang(30122)),
            'series.png',
            oOutputParameterHandler)

        oOutputParameterHandler.addParameter('sCat', '5')       # Divers
        oGui.addDir(SITE_IDENTIFIER, 'getViewing', self.ADDON.VSlang(30410), 'buzz.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

    def getViewing(self):
        oGui = Gui()

        oInputParameterHandler = InputParameterHandler()
        catFilter = oInputParameterHandler.getValue('sCat')

        with Db() as DB:
            row = DB.get_viewing()
            if not row:
                oGui.setEndOfDirectory()
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

                    oOutputParameterHandler = OutputParameterHandler()
                    oOutputParameterHandler.addParameter('siteUrl', siteurl)
                    oOutputParameterHandler.addParameter('sMovieTitle', title)
                    oOutputParameterHandler.addParameter('sTmdbId', sTmdbId)
                    oOutputParameterHandler.addParameter('sTitleWatched', sTitleWatched)
                    oOutputParameterHandler.addParameter('sSeason', sSeason)
                    oOutputParameterHandler.addParameter('sCat', cat)
                    oOutputParameterHandler.addParameter('isViewing', True)

                    # pourcentage de lecture
                    meta = {}
                    meta['title'] = sTitleWatched
                    resumetime, totaltime = DB.get_resume(meta)
                    oOutputParameterHandler.addParameter('ResumeTime', resumetime)
                    oOutputParameterHandler.addParameter('TotalTime', totaltime)

                    if cat == '1':
                        oListItem = oGui.addMovie(site, function, title, 'films.png',
                                                  '', title, oOutputParameterHandler)
                    elif cat == '4':
                        oListItem = oGui.addSeason(site, function, title, 'series.png',
                                                   '', title, oOutputParameterHandler)
                    elif cat == '5':
                        oListItem = oGui.addMisc(site, function, title, 'buzz.png', '', title, oOutputParameterHandler)
                    else:
                        oListItem = oGui.addTV(site, function, title, 'series.png', '', title, oOutputParameterHandler)

                    oOutputParameterHandler.addParameter('sTitleWatched', sTitleWatched)
                    oOutputParameterHandler.addParameter('sCat', cat)
                    oListItem.addMenu(SITE_IDENTIFIER, 'delViewing', self.ADDON.VSlang(30412), oOutputParameterHandler)

                except Exception as e:
                    pass

        # Vider toute la catégorie n'est pas accessible lors de l'utilisation en Widget
        if not xbmc.getCondVisibility('Window.IsActive(home)'):
            oOutputParameterHandler = OutputParameterHandler()
            oOutputParameterHandler.addParameter('sCat', catFilter)
            oGui.addDir(SITE_IDENTIFIER, 'delViewing', self.ADDON.VSlang(30211), 'trash.png', oOutputParameterHandler)

        oGui.setEndOfDirectory()

        return
