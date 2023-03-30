# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.search import cSearch
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import addon, window

SITE_IDENTIFIER = 'cHome'
SITE_NAME = 'Home'


class cHome:

    addons = addon()

    def load(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showVOD', self.addons.VSlang(30131), 'films.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDirect', self.addons.VSlang(30132), 'tv.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showReplay', self.addons.VSlang(30350), 'replay.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMyVideos', self.addons.VSlang(30130), 'star.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'ShowTools', self.addons.VSlang(30033), 'tools.png', output_parameter_handler)

        view = False
        if (self.addons.getSetting('active-view') == 'true'):
            view = self.addons.getSetting('accueil-view')

        oGui.setEndOfDirectory(view)

    def showVOD(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMenuSearch', self.addons.VSlang(30076), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', self.addons.VSlang(30120), 'films.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showSeries', self.addons.VSlang(30121), 'series.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDocs', self.addons.VSlang(30112), 'buzz.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showAnimes', self.addons.VSlang(30122), 'animes.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showDramas', self.addons.VSlang(30124), 'dramas.png', output_parameter_handler)

        # ininteressant
        # output_parameter_handler.addParameter('siteUrl', 'http://venom')
        # oGui.addDir(SITE_IDENTIFIER, 'showNets', self.addons.VSlang(30114), 'buzz.png', output_parameter_handler)

        oGui.setEndOfDirectory()

    def showMyVideos(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cViewing', 'showMenu', self.addons.VSlang(30125), 'replay.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('Fav', 'getBookmarks', self.addons.VSlang(30207), 'mark.png', output_parameter_handler)

        oGui.addDir('cDownload', 'getDownloadList', self.addons.VSlang(30229), 'download.png', output_parameter_handler)

        # les enregistrements de chaines TV ne sont plus opérationnelles
        # folder = self.addons.getSetting('path_enregistrement')
        # if not folder:
        #     folder = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement"/>'
        # output_parameter_handler.addParameter('siteUrl', folder)
        # oGui.addDir('cLibrary', 'openLibrary', self.addons.VSlang(30225), 'download.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showUsers', self.addons.VSlang(30455), 'user.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'activeSources', self.addons.VSlang(30362), 'host.png', output_parameter_handler)

        oGui.setEndOfDirectory()

    def showMenuSearch(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('themoviedb_org', 'load', self.addons.VSlang(30088), 'searchtmdb.png', output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30078), 'films.png', output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30079), 'series.png', output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '3')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30118), 'animes.png', output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '9')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30123), 'dramas.png', output_parameter_handler)

        output_parameter_handler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30080), 'buzz.png', output_parameter_handler)

        if (self.addons.getSetting('history-view') == 'true'):
            output_parameter_handler.addParameter('siteUrl', 'http://venom')
            oGui.addDir('cHome', 'showHistory', self.addons.VSlang(30308), 'annees.png', output_parameter_handler)

        oGui.setEndOfDirectory()

    def showSearchText(self):
        oGui = Gui()
        input_parameter_handler = InputParameterHandler()
        sSearchText = oGui.showKeyBoard(heading=self.addons.VSlang(30076))
        if not sSearchText:
            return False

        oSearch = cSearch()
        sCat = input_parameter_handler.getValue('sCat')
        oSearch.searchGlobal(sSearchText, sCat)
        oGui.setEndOfDirectory()

    def showMovies(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sCat', '1')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30078), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'MOVIE_NEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30120),
             self.addons.VSlang(30101)),
            'news.png',
            output_parameter_handler)

        # output_parameter_handler.addParameter('siteUrl', 'MOVIE_HD')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30160)), 'hd.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'MOVIE_VIEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30120),
             self.addons.VSlang(30102)),
            'views.png',
            output_parameter_handler)

        # output_parameter_handler.addParameter('siteUrl', 'MOVIE_COMMENTS')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30103)), 'comments.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'MOVIE_GENRES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30120),
             self.addons.VSlang(30105)),
            'genres.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'MOVIE_ANNEES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30120),
             self.addons.VSlang(30106)),
            'annees.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'MOVIE_LIST')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30120),
             self.addons.VSlang(30111)),
            'az.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'MOVIE_NOTES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30120),
             self.addons.VSlang(30104)),
            'notes.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'ANIM_ENFANTS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30120),
             self.addons.VSlang(30109)),
            'enfants.png',
            output_parameter_handler)

        # output_parameter_handler.addParameter('siteUrl', 'MOVIE_VF')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30107)), 'vf.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'MOVIE_VOSTFR')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30120),
             self.addons.VSlang(30108)),
            'vostfr.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'MOVIE_MOVIE')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30138),
             self.addons.VSlang(30120)),
            'host.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def showSeries(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sCat', '2')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30079), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'SERIE_NEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30121),
             self.addons.VSlang(30101)),
            'news.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'SERIE_VIEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30121),
             self.addons.VSlang(30102)),
            'views.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'SERIE_GENRES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30121),
             self.addons.VSlang(30105)),
            'genres.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'SERIE_ANNEES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30121),
             self.addons.VSlang(30106)),
            'annees.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'SERIE_LIST')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30121),
             self.addons.VSlang(30111)),
            'az.png',
            output_parameter_handler)

        # output_parameter_handler.addParameter('siteUrl', 'SERIE_VFS')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30107)), 'vf.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'SERIE_VOSTFRS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30121),
             self.addons.VSlang(30108)),
            'vostfr.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'SERIE_SERIES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30138),
             self.addons.VSlang(30121)),
            'host.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def showAnimes(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sCat', '3')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30118), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'ANIM_NEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30122),
             self.addons.VSlang(30101)),
            'news.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'ANIM_VIEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30122),
             self.addons.VSlang(30102)),
            'views.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'ANIM_GENRES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30122),
             self.addons.VSlang(30105)),
            'genres.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'ANIM_ANNEES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30122),
             self.addons.VSlang(30106)),
            'annees.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'ANIM_LIST')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30122),
             self.addons.VSlang(30111)),
            'az.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'ANIM_VOSTFRS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30122),
             self.addons.VSlang(30108)),
            'vf.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'ANIM_ANIMS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30138),
             self.addons.VSlang(30122)),
            'host.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def showDramas(self):
        oGui = Gui()

        # Affiche les Nouveautés Dramas
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sCat', '9')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30123), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'DRAMA_NEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30124),
             self.addons.VSlang(30101)),
            'news.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'DRAMA_VIEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30124),
             self.addons.VSlang(30102)),
            'views.png',
            output_parameter_handler)

        # Affiche les Genres Dramas
        output_parameter_handler.addParameter('siteUrl', 'DRAMA_GENRES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30124),
             self.addons.VSlang(30105)),
            'genres.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'DRAMA_ANNEES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30124),
             self.addons.VSlang(30106)),
            'annees.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'DRAMA_LIST')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30124),
             self.addons.VSlang(30111)),
            'az.png',
            output_parameter_handler)

        # Affiche les Sources Dramas
        output_parameter_handler.addParameter('siteUrl', 'DRAMA_DRAMAS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30138),
             self.addons.VSlang(30124)),
            'host.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def showDocs(self):
        oGui = Gui()

        # Affiche les Nouveautés Documentaires
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sCat', '5')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30080), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'DOC_NEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30112),
             self.addons.VSlang(30101)),
            'news.png',
            output_parameter_handler)

        # Affiche les Genres Documentaires
        output_parameter_handler.addParameter('siteUrl', 'DOC_GENRES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30112),
             self.addons.VSlang(30105)),
            'genres.png',
            output_parameter_handler)

        # Affiche les Sources Documentaires
        output_parameter_handler.addParameter('siteUrl', 'DOC_DOCS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30138),
             self.addons.VSlang(30112)),
            'host.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def showSports(self):
        oGui = Gui()

        # Affiche les live Sportifs
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'SPORT_LIVE')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30113),
             self.addons.VSlang(30119)),
            'news.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'SPORT_TV')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30113),
             self.addons.VSlang(30200)),
            'tv.png',
            output_parameter_handler)

        # Affiche les Genres Sportifs
        output_parameter_handler.addParameter('siteUrl', 'SPORT_GENRES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30113),
             self.addons.VSlang(30105)),
            'genres.png',
            output_parameter_handler)

        # Affiche les Sources Sportives
        output_parameter_handler.addParameter('siteUrl', 'SPORT_SPORTS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30138),
             self.addons.VSlang(30113)),
            'host.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def showDirect(self):
        oGui = Gui()
        output_parameter_handler = OutputParameterHandler()
        oGui.addDir(SITE_IDENTIFIER, 'showSports', self.addons.VSlang(30113), 'sport.png', output_parameter_handler)
        oGui.addDir(SITE_IDENTIFIER, 'showMenuTV', self.addons.VSlang(30115), 'tv.png', output_parameter_handler)
        oGui.addDir('freebox', 'showMenuMusic', self.addons.VSlang(30203), 'music.png', output_parameter_handler)
        oGui.setEndOfDirectory()

    def showMenuTV(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()

        # SI plusieurs sources proposent la TNT
        # output_parameter_handler.addParameter('siteUrl', 'CHAINE_TV')
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30332), 'host.png', output_parameter_handler)
        # SINON accès direct à la seule source
        output_parameter_handler.addParameter('siteUrl', 'TV')
        oGui.addDir('freebox', 'showWeb', self.addons.VSlang(30332), 'tv.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'CHAINE_CINE')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30200),
             self.addons.VSlang(30133)),
            'films.png',
            output_parameter_handler)
        # oGui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30113)), 'host.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'TV_TV')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30138),
             self.addons.VSlang(30200)),
            'host.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def showReplay(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('sCat', '6')
        oGui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30134), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'REPLAYTV_NEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30117),
             self.addons.VSlang(30101)),
            'news.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'REPLAYTV_GENRES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30117),
             self.addons.VSlang(30105)),
            'genres.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'SPORT_REPLAY')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30117),
             self.addons.VSlang(30113)),
            'sport.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'REPLAYTV_REPLAYTV')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30138),
             self.addons.VSlang(30117)),
            'host.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def showNets(self):
        oGui = Gui()

        # Affiche les Nouveautés Vidéos
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'NETS_NEWS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30114),
             self.addons.VSlang(30101)),
            'news.png',
            output_parameter_handler)

        # Affiche les Genres Vidéos
        output_parameter_handler.addParameter('siteUrl', 'NETS_GENRES')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30114),
             self.addons.VSlang(30105)),
            'genres.png',
            output_parameter_handler)

        # Affiche les Sources Vidéos
        output_parameter_handler.addParameter('siteUrl', 'NETS_NETS')
        oGui.addDir(
            SITE_IDENTIFIER,
            'callpluging',
            '%s (%s)' %
            (self.addons.VSlang(30138),
             self.addons.VSlang(30114)),
            'host.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def showUsers(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'http://')
        oGui.addDir('themoviedb_org', 'showMyTmdb', 'TMDB', 'tmdb.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://')
        oGui.addDir('cTrakt', 'getLoad', self.addons.VSlang(30214), 'trakt.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://')
        oGui.addDir('siteuptobox', 'load', 'Uptobox', 'sites/siteuptobox.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://')
        oGui.addDir(
            'siteonefichier',
            'load',
            self.addons.VSlang(30327),
            'sites/siteonefichier.png',
            output_parameter_handler)

        oGui.setEndOfDirectory()

    def ShowTools(self):
        oGui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'opensetting', self.addons.VSlang(30227), 'notes.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cDownload', 'getDownload', self.addons.VSlang(30224), 'download.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('cLibrary', 'getLibrary', self.addons.VSlang(30303), 'library.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir(SITE_IDENTIFIER, 'showHostDirect', self.addons.VSlang(30469), 'host.png', output_parameter_handler)

        output_parameter_handler.addParameter('siteUrl', 'http://venom')
        oGui.addDir('globalSources', 'globalSources', self.addons.VSlang(30449), 'host.png', output_parameter_handler)

        oGui.setEndOfDirectory()

    def opensetting(self):
        addon().openSettings()

    def showHistory(self):
        oGui = Gui()

        from resources.lib.db import Db
        with Db() as db:
            row = db.get_history()

        if row:
            oGui.addText(SITE_IDENTIFIER, self.addons.VSlang(30416))
        else:
            oGui.addText(SITE_IDENTIFIER)
        output_parameter_handler = OutputParameterHandler()
        for match in row:
            sTitle = match['title']
            sCat = match['disp']

            output_parameter_handler.addParameter('siteUrl', 'http://venom')
            output_parameter_handler.addParameter('searchtext', sTitle)

            oGuiElement = GuiElement()
            oGuiElement.setSiteName('globalSearch')
            oGuiElement.setFunction('globalSearch')

            try:
                oGuiElement.setTitle('- ' + sTitle)
            except BaseException:
                oGuiElement.setTitle('- ' + str(sTitle, 'utf-8'))

            oGuiElement.setFileName(sTitle)
            oGuiElement.setCat(sCat)
            oGuiElement.setIcon('search.png')
            oGui.createSimpleMenu(
                oGuiElement,
                output_parameter_handler,
                SITE_IDENTIFIER,
                'cHome',
                'delSearch',
                self.addons.VSlang(30412))
            oGui.addFolder(oGuiElement, output_parameter_handler)

        if row:
            output_parameter_handler.addParameter('siteUrl', 'http://venom')
            oGui.addDir(SITE_IDENTIFIER, 'delSearch', self.addons.VSlang(30413), 'trash.png', output_parameter_handler)

        oGui.setEndOfDirectory()

    def delSearch(self):
        from resources.lib.db import Db
        with Db() as db:
            db.del_history()
        return True

    def callpluging(self):
        oGui = Gui()

        input_parameter_handler = InputParameterHandler()
        sSiteUrl = input_parameter_handler.getValue('siteUrl')

        oPluginHandler = cPluginHandler()
        aPlugins = oPluginHandler.getAvailablePlugins(sSiteUrl)
        output_parameter_handler = OutputParameterHandler()
        for aPlugin in aPlugins:
            try:
                icon = 'sites/%s.png' % (aPlugin[2])
                output_parameter_handler.addParameter('siteUrl', aPlugin[0])
                oGui.addDir(aPlugin[2], aPlugin[3], aPlugin[1], icon, output_parameter_handler)
            except BaseException:
                pass

        oGui.setEndOfDirectory()

    def showHostDirect(self):  # fonction de recherche
        oGui = Gui()
        sUrl = oGui.showKeyBoard(heading=self.addons.VSlang(30045))
        if (sUrl):

            oHoster = HosterGui().checkHoster(sUrl)
            if (oHoster):
                oHoster.setDisplayName(self.addons.VSlang(30046))
                oHoster.setFileName(self.addons.VSlang(30046))
                HosterGui().showHoster(oGui, oHoster, sUrl, '')

        oGui.setEndOfDirectory()
