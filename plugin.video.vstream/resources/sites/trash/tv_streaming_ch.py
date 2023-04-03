# -*- coding: utf-8 -*-
# Vstream https://github.com/Kodi-vStream/venom-xbmc-addons
# Venom.
# site HS le 03/06/18
import urllib
import re
from resources.lib.config import cConfig
from resources.lib.parser import Parser
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
return False
# from resources.lib.util import cUtil

SITE_IDENTIFIER = 'tv_streaming_ch'
SITE_NAME = 'Tv-streaming'
SITE_DESC = 'Films/Séries/Animés/Documentaires/ReplayTV en streaming'

URL_MAIN = 'http://www.streamania.xyz/'

MOVIE_NEWS = (URL_MAIN + 'category/films-vf/', 'showMovies')
MOVIE_MOVIE = (URL_MAIN + 'category/films-vf/', 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_NEWS = (URL_MAIN + 'category/series-tv', 'showMovies')
SERIE_SERIES = (URL_MAIN + 'category/series-tv', 'showMovies')
SERIE_VFS = (URL_MAIN + 'category/series-tv/serie-vf/', 'showMovies')
SERIE_VOSTFRS = (URL_MAIN + 'category/series-tv/serie-vostfr/', 'showMovies')

ANIM_ANIMS = (URL_MAIN + 'category/manga/', 'showMovies')
ANIM_VFS = (URL_MAIN + 'category/manga/manga-vf/', 'showMovies')
ANIM_VOSTFRS = (URL_MAIN + 'category/manga/manga-vostfr/', 'showMovies')
ANIM_ENFANTS = (URL_MAIN + 'category/dessin-anime/', 'showMovies')

DOC_NEWS = (URL_MAIN + 'category/television/documentaire/', 'showMovies')
DOC_DOCS = ('http://', 'load')

SPORT_SPORTS = (URL_MAIN + 'category/sport/', 'showMovies')

REPLAYTV_GENRES = (True, 'ReplayTV')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MISC = (URL_MAIN + '?s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VFS[1],
        'Séries (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_VOSTFRS[1],
        'Séries (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter(
        'site_url', URL_MAIN + 'category/sitcoms/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMovies',
        'Sitcoms',
        'series.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VFS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VFS[1],
        'Animés (VF)',
        'vf.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_VOSTFRS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_VOSTFRS[1],
        'Animés (VOSTFR)',
        'vostfr.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', ANIM_ENFANTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        ANIM_ENFANTS[1],
        'Dessins animés',
        'animes.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', DOC_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        DOC_NEWS[1],
        'Documentaires',
        'doc.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', REPLAYTV_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_GENRES[1],
        'Replay TV (Genres)',
        'replay.png',
        output_parameter_handler)

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SPORT_SPORTS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SPORT_SPORTS[1],
        'Sport',
        'sport.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if (search_text):
        url = URL_SEARCH[0] + urllib.quote(search_text)
        showMovies(url)
        gui.setEndOfDirectory()
        return


def ReplayTV():
    gui = Gui()

    liste = []
    liste.append(['Concert', URL_MAIN + 'category/television/concert/'])
    liste.append(['Documentaires', URL_MAIN +
                  'category/television/documentaire/'])
    liste.append(['Emissions TV', URL_MAIN +
                  'category/television/emission-tv/'])
    liste.append(['Karaoké', URL_MAIN + 'karaoke/'])
    liste.append(['One Man Show', URL_MAIN + 'television/one-man-sohw/'])
    liste.append(['Rétro', URL_MAIN + 'category/television/retro/'])
    liste.append(['Rétro Souvenir', URL_MAIN +
                  'category/television/retro-souvenir/'])
    liste.append(['TV réalité', URL_MAIN + 'television/tv-realite/'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'tv.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    liste = []
    liste.append(['Action', URL_MAIN + 'category/films-vf/action-films/'])
    liste.append(['Animation', URL_MAIN +
                  'category/films-vf/animation-films/'])
    liste.append(['Arts Martiaux', URL_MAIN +
                  'category/films-vf/arts-martiaux-films/'])
    liste.append(['Aventure', URL_MAIN + 'category/films-vf/aventure-films/'])
    liste.append(['Comédie', URL_MAIN + 'category/films-vf/comedie-films/'])
    liste.append(['Disney', URL_MAIN + 'category/dessin-anime/disney/'])
    liste.append(['Drame', URL_MAIN + 'category/films-vf/drame-films/'])
    liste.append(['Epouvante-Horreur', URL_MAIN +
                  'category/films-vf/epouvante-horreur/'])
    liste.append(['Espionnage', URL_MAIN + 'category/films-vf/espionnage/'])
    liste.append(['Famille', URL_MAIN + 'category/films-vf/famille/'])
    liste.append(['Fantastique', URL_MAIN + 'category/films-vf/fantastique/'])
    liste.append(['Guerre', URL_MAIN + 'category/films-vf/guerre/'])
    liste.append(['Historique', URL_MAIN +
                  'category/films-vf/historique-streaming/'])
    liste.append(['Musical', URL_MAIN + 'category/films-vf/musical/'])
    liste.append(['Policier', URL_MAIN + 'category/films-vf/policier/'])
    liste.append(['Romance', URL_MAIN + 'category/films-vf/romance/'])
    liste.append(['Science-fiction', URL_MAIN +
                  'category/films-vf/science-fiction/'])
    liste.append(['Sentaï', URL_MAIN + 'sentai/'])
    liste.append(['Téléfilms', URL_MAIN + 'category/films-vf/telefilms/'])
    liste.append(['Thriller', URL_MAIN + 'category/films-vf/thriller/'])
    liste.append(['Western', URL_MAIN + 'western/'])

    for title, url in liste:

        output_parameter_handler = OutputParameterHandler()
        output_parameter_handler.addParameter('site_url', url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    parser = Parser()
    gui = Gui()
    if search:
        url = search

    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<div.*?class="moviefilm">.+?href="([^<]+)".*?img src="([^<]+)" alt="(.+?)"'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            url = str(entry[0])
            thumb = str(entry[1])
            title = str(entry[2])

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            if '- Saison' in title:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSeries',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif '-saison-' in url or '/manga' in url or '/sentai/' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSeries',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            elif '/films' in url in url or '/sport/' in url or '/western/' in url:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMisc(
                    SITE_IDENTIFIER,
                    'showSeries',
                    title,
                    '',
                    thumb,
                    '',
                    output_parameter_handler)

        cConfig().finishDialog(dialog)

    if not search:
        next_page = __checkForNextPage(html_content)
        if (next_page):
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                '[COLOR teal]Next >>>[/COLOR]',
                output_parameter_handler)

    if not search:
        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    pattern = '<a class="nextpostslink" rel="next" href="(.+?)">(?:»|&raquo;)<\\/a>'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        return results[1][0]

    return False


def showSeries(sLoop=False):
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    if url.endswith('/'):
        url = url + '100/'
    else:
        url = url + '/100/'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<a *href="([^<]+)"><span>.+?<font class="">(.+?)<\\/font><\\/font>'
    results = parser.parse(html_content, pattern)

    # astuce en cas d'episode unique
    if not results[0] and (sLoop == False):
        showHosters(True)
        return

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            episode = ''
            if entry[1]:
                episode = entry[1] + ' '

            url = str(entry[0])
            title = episode + movie_title

            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            gui.addTV(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                '',
                output_parameter_handler)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()


def showHosters(sLoop=False):
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    html_content = html_content.replace('facebook', '<>')

    pattern = '<iframe.+?src="(http[^<>]+?)" [^<>]+?><\\/iframe>'
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        dialog = cConfig().createDialog(SITE_NAME)
        for entry in results[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break

            if 'dailymotion' in entry:
                continue

            hoster_url = str(entry)
            hoster = HosterGui().checkHoster(hoster_url)
            if (hoster):
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb)

        cConfig().finishDialog(dialog)

    gui.setEndOfDirectory()
