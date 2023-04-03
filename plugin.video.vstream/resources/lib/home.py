# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.gui.guiElement import GuiElement
from resources.lib.search import Search
from resources.lib.handler.pluginHandler import PluginHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.comaddon import Addon, VSlog

SITE_IDENTIFIER = 'Home'
SITE_NAME = 'Home'


class Home:
    addons = Addon()

    def load(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showVOD',
            self.addons.VSlang(30131),
            'films.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showDirect',
            self.addons.VSlang(30132),
            'tv.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showReplay',
            self.addons.VSlang(30350),
            'replay.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMyVideos',
            self.addons.VSlang(30130),
            'star.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'ShowTools',
            self.addons.VSlang(30033),
            'tools.png',
            output_parameter_handler)

        view = False
        if self.addons.getSetting('active-view') == 'true':
            view = self.addons.getSetting('accueil-view')

        gui.setEndOfDirectory(view)

    def showVOD(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMenuSearch',
            self.addons.VSlang(30076),
            'search.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            self.addons.VSlang(30120),
            'films.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSeries',
            self.addons.VSlang(30121),
            'series.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showDocs',
            self.addons.VSlang(30112),
            'buzz.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showAnimes',
            self.addons.VSlang(30122),
            'animes.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showDramas',
            self.addons.VSlang(30124),
            'dramas.png',
            output_parameter_handler)

        # ininteressant
        # output_parameter_handler.addParameter('site_url', 'http://venom')
        # gui.addDir(SITE_IDENTIFIER, 'showNets', self.addons.VSlang(30114), 'buzz.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showMyVideos(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            'cViewing',
            'showMenu',
            self.addons.VSlang(30125),
            'replay.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            'cFav',
            'getBookmarks',
            self.addons.VSlang(30207),
            'mark.png',
            output_parameter_handler)

        gui.addDir(
            'cDownload',
            'getDownloadList',
            self.addons.VSlang(30229),
            'download.png',
            output_parameter_handler)

        # les enregistrements de chaines TV ne sont plus opérationnelles
        # folder = self.addons.getSetting('path_enregistrement')
        # if not folder:
        #     folder = 'special://userdata/addon_data/plugin.video.vstream/Enregistrement"/>'
        # output_parameter_handler.addParameter('site_url', folder)
        # gui.addDir('Library', 'openLibrary', self.addons.VSlang(30225), 'download.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            SITE_IDENTIFIER,
            'showUsers',
            self.addons.VSlang(30455),
            'user.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            'globalSources',
            'activeSources',
            self.addons.VSlang(30362),
            'host.png',
            output_parameter_handler)

        gui.setEndOfDirectory()

    def showMenuSearch(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(
            'themoviedb_org',
            'load',
            self.addons.VSlang(30088),
            'searchtmdb.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('cat', '1')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearchText',
            self.addons.VSlang(30078),
            'films.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('cat', '2')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearchText',
            self.addons.VSlang(30079),
            'series.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('cat', '3')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearchText',
            self.addons.VSlang(30118),
            'animes.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('cat', '9')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearchText',
            self.addons.VSlang(30123),
            'dramas.png',
            output_parameter_handler)

        output_parameter_handler.addParameter('cat', '5')
        gui.addDir(
            SITE_IDENTIFIER,
            'showSearchText',
            self.addons.VSlang(30080),
            'buzz.png',
            output_parameter_handler)

        if self.addons.getSetting('history-view') == 'true':
            output_parameter_handler.addParameter('site_url', 'http://venom')
            gui.addDir(
                'Home',
                'showHistory',
                self.addons.VSlang(30308),
                'annees.png',
                output_parameter_handler)

        gui.setEndOfDirectory()

    def showSearchText(self):
        gui = Gui()
        input_parameter_handler = InputParameterHandler()
        search_text = gui.showKeyBoard(heading=self.addons.VSlang(30076))
        if not search_text:
            return False

        cat = input_parameter_handler.getValue('cat')
        Search().searchGlobal(search_text, cat)
        gui.setEndOfDirectory()

    def showMovies(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('cat', '1')
        gui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30078), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'MOVIE_NEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30101)),
                   'news.png', output_parameter_handler)

        # output_parameter_handler.addParameter('site_url', 'MOVIE_HD')
        # gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' %
        #   (self.addons.VSlang(30120), self.addons.VSlang(30160)), 'hd.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'MOVIE_VIEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30102)),
                   'views.png', output_parameter_handler)

        # output_parameter_handler.addParameter('site_url', 'MOVIE_COMMENTS')
        # gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' %
        #   (self.addons.VSlang(30120), self.addons.VSlang(30103)), 'comments.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'MOVIE_GENRES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30105)),
                   'genres.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'MOVIE_ANNEES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30106)),
                   'annees.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'MOVIE_LIST')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30111)),
                   'az.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'MOVIE_NOTES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30104)),
                   'notes.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'ANIM_ENFANTS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30109)),
                   'enfants.png', output_parameter_handler)

        # output_parameter_handler.addParameter('site_url', 'MOVIE_VF')
        # gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' %
        #   (self.addons.VSlang(30120), self.addons.VSlang(30107)), 'vf.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'MOVIE_VOSTFR')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30120), self.addons.VSlang(30108)),
                   'vostfr.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'MOVIE_MOVIE')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30120)),
                   'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showSeries(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('cat', '2')
        gui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30079), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'SERIE_NEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30101)),
                   'news.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'SERIE_VIEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30102)),
                   'views.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'SERIE_GENRES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30105)),
                   'genres.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'SERIE_ANNEES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30106)),
                   'annees.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'SERIE_LIST')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30111)),
                   'az.png', output_parameter_handler)

        # output_parameter_handler.addParameter('site_url', 'SERIE_VFS')
        # gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' %
        #   (self.addons.VSlang(30121), self.addons.VSlang(30107)), 'vf.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'SERIE_VOSTFRS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30121), self.addons.VSlang(30108)),
                   'vostfr.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'SERIE_SERIES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30121)),
                   'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showAnimes(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('cat', '3')
        gui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30118), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'ANIM_NEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30101)),
                   'news.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'ANIM_VIEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30102)),
                   'views.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'ANIM_GENRES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30105)),
                   'genres.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'ANIM_ANNEES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30106)),
                   'annees.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'ANIM_LIST')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30111)),
                   'az.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'ANIM_VOSTFRS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30122), self.addons.VSlang(30108)),
                   'vf.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'ANIM_ANIMS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30122)),
                   'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showDramas(self):
        gui = Gui()

        # Affiche les Nouveautés Dramas
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('cat', '9')
        gui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30123), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'DRAMA_NEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30101)),
                   'news.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'DRAMA_VIEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30102)),
                   'views.png', output_parameter_handler)

        # Affiche les Genres Dramas
        output_parameter_handler.addParameter('site_url', 'DRAMA_GENRES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30105)),
                   'genres.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'DRAMA_ANNEES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30106)),
                   'annees.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'DRAMA_LIST')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30124), self.addons.VSlang(30111)),
                   'az.png', output_parameter_handler)

        # Affiche les Sources Dramas
        output_parameter_handler.addParameter('site_url', 'DRAMA_DRAMAS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30124)),
                   'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showDocs(self):
        gui = Gui()

        # Affiche les Nouveautés Documentaires
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('cat', '5')
        gui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30080), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'DOC_NEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30101)),
                   'news.png', output_parameter_handler)

        # Affiche les Genres Documentaires
        output_parameter_handler.addParameter('site_url', 'DOC_GENRES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30112), self.addons.VSlang(30105)),
                   'genres.png', output_parameter_handler)

        # Affiche les Sources Documentaires
        output_parameter_handler.addParameter('site_url', 'DOC_DOCS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30112)),
                   'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showSports(self):
        gui = Gui()

        # Affiche les live Sportifs
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'SPORT_LIVE')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30119)),
                   'news.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'SPORT_TV')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30200)),
                   'tv.png', output_parameter_handler)

        # Affiche les Genres Sportifs
        output_parameter_handler.addParameter('site_url', 'SPORT_GENRES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30113), self.addons.VSlang(30105)),
                   'genres.png', output_parameter_handler)

        # Affiche les Sources Sportives
        output_parameter_handler.addParameter('site_url', 'SPORT_SPORTS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30113)),
                   'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showDirect(self):
        gui = Gui()
        output_parameter_handler = OutputParameterHandler()
        gui.addDir(SITE_IDENTIFIER, 'showSports', self.addons.VSlang(30113), 'sport.png', output_parameter_handler)
        gui.addDir(SITE_IDENTIFIER, 'showMenuTV', self.addons.VSlang(30115), 'tv.png', output_parameter_handler)
        gui.addDir('freebox', 'showMenuMusic', self.addons.VSlang(30203), 'music.png', output_parameter_handler)
        gui.setEndOfDirectory()

    def showMenuTV(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()

        # SI plusieurs sources proposent la TNT
        # output_parameter_handler.addParameter('site_url', 'CHAINE_TV')
        # gui.addDir(SITE_IDENTIFIER, 'callpluging', self.addons.VSlang(30332), 'host.png', output_parameter_handler)
        # SINON accès direct à la seule source
        output_parameter_handler.addParameter('site_url', 'TV')
        gui.addDir('freebox', 'showWeb', self.addons.VSlang(30332), 'tv.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'CHAINE_CINE')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30200), self.addons.VSlang(30133)),
                   'films.png', output_parameter_handler)
        # gui.addDir(SITE_IDENTIFIER, 'callpluging',
        #   '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30113)), 'host.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'TV_TV')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30200)),
                   'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showReplay(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('cat', '6')
        gui.addDir(SITE_IDENTIFIER, 'showSearchText', self.addons.VSlang(30134), 'search.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'REPLAYTV_NEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30101)),
                   'news.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'REPLAYTV_GENRES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30105)),
                   'genres.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'SPORT_REPLAY')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30117), self.addons.VSlang(30113)),
                   'sport.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'REPLAYTV_REPLAYTV')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30117)),
                   'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showNets(self):
        gui = Gui()

        # Affiche les Nouveautés Vidéos
        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'NETS_NEWS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30114), self.addons.VSlang(30101)),
                   'news.png', output_parameter_handler)

        # Affiche les Genres Vidéos
        output_parameter_handler.addParameter('site_url', 'NETS_GENRES')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30114), self.addons.VSlang(30105)),
                   'genres.png', output_parameter_handler)

        # Affiche les Sources Vidéos
        output_parameter_handler.addParameter('site_url', 'NETS_NETS')
        gui.addDir(SITE_IDENTIFIER, 'callpluging', '%s (%s)' % (self.addons.VSlang(30138), self.addons.VSlang(30114)),
                   'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def showUsers(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'http://')
        gui.addDir('themoviedb_org', 'showMyTmdb', 'TMDB', 'tmdb.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://')
        gui.addDir('cTrakt', 'getLoad', self.addons.VSlang(30214), 'trakt.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://')
        gui.addDir('siteuptobox', 'load', 'Uptobox', 'sites/siteuptobox.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://')
        gui.addDir('siteonefichier', 'load', self.addons.VSlang(30327), 'sites/siteonefichier.png',
                   output_parameter_handler)

        gui.setEndOfDirectory()

    def ShowTools(self):
        gui = Gui()

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(SITE_IDENTIFIER, 'opensetting', self.addons.VSlang(30227), 'notes.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir('cDownload', 'getDownload', self.addons.VSlang(30224), 'download.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir('Library', 'getLibrary', self.addons.VSlang(30303), 'library.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir(SITE_IDENTIFIER, 'showHostDirect', self.addons.VSlang(30469), 'host.png', output_parameter_handler)

        output_parameter_handler.addParameter('site_url', 'http://venom')
        gui.addDir('globalSources', 'globalSources', self.addons.VSlang(30449), 'host.png', output_parameter_handler)

        gui.setEndOfDirectory()

    def opensetting(self):
        Addon().openSettings()

    def showHistory(self):
        gui = Gui()

        from resources.lib.db import Db
        with Db() as db:
            row = db.get_history()

        if row:
            gui.addText(SITE_IDENTIFIER, self.addons.VSlang(30416))
        else:
            gui.addText(SITE_IDENTIFIER)
        output_parameter_handler = OutputParameterHandler()
        for match in row:
            title = match['title']
            cat = match['disp']

            output_parameter_handler.addParameter('site_url', 'http://venom')
            output_parameter_handler.addParameter('searchtext', title)

            gui_element = GuiElement()
            gui_element.setSiteName('globalSearch')
            gui_element.setFunction('globalSearch')

            try:
                gui_element.setTitle('- ' + title)
            except BaseException as exception:
                gui_element.setTitle('- ' + str(title, 'utf-8'))
                VSlog("Error: " + str(exception))

            gui_element.setFileName(title)
            gui_element.setCat(cat)
            gui_element.setIcon('search.png')
            gui.createSimpleMenu(
                gui_element,
                output_parameter_handler,
                SITE_IDENTIFIER,
                'Home',
                'delSearch',
                self.addons.VSlang(30412))
            gui.addFolder(gui_element, output_parameter_handler)

        if row:
            output_parameter_handler.addParameter('site_url', 'http://venom')
            gui.addDir(
                SITE_IDENTIFIER,
                'delSearch',
                self.addons.VSlang(30413),
                'trash.png',
                output_parameter_handler)

        gui.setEndOfDirectory()

    def delSearch(self):
        from resources.lib.db import Db
        with Db() as db:
            db.del_history()
        return True

    def callpluging(self):
        gui = Gui()

        input_parameter_handler = InputParameterHandler()
        site_url = input_parameter_handler.getValue('site_url')

        plugin_handler = PluginHandler()
        list_plugins = plugin_handler.getAvailablePlugins(site_url)
        output_parameter_handler = OutputParameterHandler()
        for plugin in list_plugins:
            try:
                icon = 'sites/%s.png' % (plugin[2])
                output_parameter_handler.addParameter('site_url', plugin[0])
                gui.addDir(
                    plugin[2],
                    plugin[3],
                    plugin[1],
                    icon,
                    output_parameter_handler)
            except BaseException:
                pass

        gui.setEndOfDirectory()

    def showHostDirect(self):  # fonction de recherche
        gui = Gui()
        url = gui.showKeyBoard(heading=self.addons.VSlang(30045))
        if url:

            hoster = HosterGui().checkHoster(url)
            if hoster:
                hoster.setDisplayName(self.addons.VSlang(30046))
                hoster.setFileName(self.addons.VSlang(30046))
                HosterGui().showHoster(gui, hoster, url, '')

        gui.setEndOfDirectory()
