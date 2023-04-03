# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons

import re

from resources.lib.comaddon import Progress, SiteManager
from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'zone_streaming'
SITE_NAME = 'Zone Streaming'
SITE_DESC = 'Médiathèque de chaînes officielles'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)

MOVIE_MOVIE = (URL_MAIN + 'category/films/', 'showMovies')
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenres')

SERIE_SERIES = (URL_MAIN + 'category/seriesweb/', 'showMovies')
WEB_SERIES = (URL_MAIN + 'category/webseries/', 'showMovies')
SERIE_GENRES = (True, 'showSeriesGenres')

REPLAYTV_REPLAYTV = (True, 'load')
REPLAYTV_NEWS = (URL_MAIN + 'category/emissions/', 'showMovies')
REPLAYTV_GENRES = (True, 'showReplayGenres')
SHOW_SHOWS = (URL_MAIN + 'category/spectaclesweb/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_REPLAY = (URL_SEARCH[0], 'showMovies')
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

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_MOVIE[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_MOVIE[1],
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_SERIES[1],
        'Séries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', WEB_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        WEB_SERIES[1],
        'Webséries',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries & Webséries (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', REPLAYTV_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_NEWS[1],
        'Emissions',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SHOW_SHOWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SHOW_SHOWS[1],
        'Spectacles',
        'tv.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', REPLAYTV_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        REPLAYTV_GENRES[1],
        'Replay (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()

    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text.replace(' ', '+')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showGenres():
    gui = Gui()

    liste = []

    # Catégorie Longs métrages
    liste.append(['[COLOR yellow]Longs métrages[/COLOR]',
                 'category/films/longs-metrages/'])
    liste.append(
        ['Action', 'category/films/longs-metrages/action-longs-metrages/'])
    liste.append(
        ['Animation', 'category/films/longs-metrages/animation-longs-metrages/'])
    liste.append(
        ['Aventure', 'category/films/longs-metrages/aventure-longs-metrages/'])
    liste.append(
        ['Cinématiques', 'category/films/longs-metrages/cinematiques-jeux-video-longs-metrages/'])
    liste.append(
        ['Comédie', 'category/films/longs-metrages/comedies-longs-metrages/'])
    liste.append(
        ['Documentaires', 'category/films/longs-metrages/documentaires/'])
    liste.append(
        ['Drame', 'category/films/longs-metrages/drame-longs-metrages/'])
    liste.append(
        ['Historique', 'category/films/longs-metrages/historique-longs-metrages/'])
    liste.append(
        ['Horreur', 'category/films/longs-metrages/horreur-longs-metrages/'])
    liste.append(
        ['Romance', 'category/films/longs-metrages/romance-longs-metrages/'])
    liste.append(['Science fiction',
                  'category/films/longs-metrages/science-fiction-longs-metrages/'])
    liste.append(
        ['Thriller', 'category/films/longs-metrages/thriller-longs-metrages/'])

    # Catégorie Moyens métrages
    liste.append(['[COLOR yellow]Moyens métrages[/COLOR]',
                 'category/films/moyens-metrages/'])
    liste.append(
        ['Aventure', 'category/films/moyens-metrages/aventure-moyens-metrages/'])
    liste.append(
        ['Comédie', 'category/films/moyens-metrages/comedie-moyens-metrages/'])
    liste.append(
        ['Documentaires', 'category/films/moyens-metrages/documentaire-moyens-metrages/'])
    liste.append(
        ['Horreur', 'category/films/moyens-metrages/horreur-moyens-metrages/'])
    liste.append(
        ['Thriller', 'category/films/moyens-metrages/thriller-moyens-metrages/'])

    # Catégorie Courts métrages
    liste.append(['[COLOR yellow]Courts métrages[/COLOR]',
                 'category/films/courts-metrages/'])
    liste.append(
        ['Action', 'category/films/courts-metrages/action-courts-metrages/'])
    liste.append(
        ['Aventure', 'category/films/courts-metrages/aventure-courts-metrages/'])
    liste.append(
        ['Comédie', 'category/films/courts-metrages/comedie-courts-metrages/'])
    liste.append(
        ['Documentaires', 'category/films/courts-metrages/documentaires-courts-metrages/'])
    liste.append(
        ['Drame', 'category/films/courts-metrages/drame-courts-metrages/'])
    liste.append(
        ['Fantastique', 'category/films/courts-metrages/fantastique-courts-metrages/'])
    liste.append(
        ['Guerre', 'category/films/courts-metrages/guerre-courts-metrages/'])
    liste.append(
        ['Horreur', 'category/films/courts-metrages/horreur-courts-metrages/'])
    liste.append(['Science fiction',
                  'category/films/courts-metrages/science-fiction-courts-metrages/'])
    liste.append(
        ['Thriller', 'category/films/courts-metrages/thriller-courts-metrages/'])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:

        output_parameter_handler.addParameter('site_url', URL_MAIN + url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesGenres():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    liste = []

    # Catégorie Series
    liste.append(['[COLOR yellow]Séries[/COLOR]', 'category/seriesweb/'])
    liste.append(['Action', 'category/seriesweb/action-series/'])
    liste.append(['Animation', 'category/seriesweb/animation-series/'])
    liste.append(['Aventure', 'category/seriesweb/aventure-series/'])
    liste.append(['Comédie', 'category/seriesweb/comedie-series/'])
    liste.append(['Documentaires', 'category/seriesweb/documentaires-series/'])
    liste.append(['Drame', 'category/seriesweb/drame-series/'])
    liste.append(['Fantastique', 'category/seriesweb/fantastique-series/'])
    liste.append(['Manga', 'category/seriesweb/manga-series/'])
    liste.append(['Romance', 'category/seriesweb/romance-series/'])
    liste.append(['Science fiction',
                  'category/seriesweb/science-fiction-series/'])
    liste.append(['Thriller', 'category/seriesweb/thriller-series/'])

    # Catégorie Webseries
    liste.append(['[COLOR yellow]WebSéries[/COLOR]', 'category/webseries/'])
    liste.append(['Action', 'category/webseries/action-webseries/'])
    liste.append(['Comédie', 'category/webseries/comedie-webseries/'])
    liste.append(
        ['Documentaires', 'category/webseries/documentaires-webseries/'])
    liste.append(['Drame', 'category/webseries/drame-webseries/'])
    liste.append(['Fantastique', 'category/webseries/fantastique-webseries/'])
    liste.append(['Histoire', 'category/webseries/histoire-webseries/'])
    liste.append(['Musical', 'category/webseries/musical-webseries/'])
    liste.append(['Romance', 'category/webseries/romance-webseries/'])
    liste.append(['Science fiction',
                  'category/webseries/science-fiction-webseries/'])
    liste.append(['Social', 'category/webseries/social-webseries/'])
    liste.append(['Sport', 'category/webseries/sport-webseries/'])
    liste.append(['Thriller', 'category/webseries/thriller-webseries/'])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:

        output_parameter_handler.addParameter('site_url', URL_MAIN + url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showReplayGenres():
    gui = Gui()

    liste = []
    # Catégorie emission
    liste.append(['[COLOR yellow]Emissions[/COLOR]', 'category/emissions/'])
    liste.append(['Actualité', 'category/emissions/actualite-emissions/'])
    liste.append(['Automobile', 'category/emissions/automobile-emissions/'])
    liste.append(['Cuisine', 'category/emissions/cuisine-emissions/'])
    liste.append(['Culture', 'category/emissions/culture-emissions/'])
    liste.append(['Découverte', 'category/emissions/decouverte-emissions/'])
    liste.append(['Histoire', 'category/emissions/histoire-emissions/'])
    liste.append(
        ['Investigation', 'category/emissions/investigation-emissions/'])
    liste.append(['Jardinage', 'category/emissions/jardinage-emissions/'])
    liste.append(['Société', 'category/emissions/societe-emissions/'])
    liste.append(['Sport', 'category/emissions/sport-emissions/'])
    liste.append(
        ['Télé-réalité', 'category/emissions/tele-realite-emissions/'])
    liste.append(['Voyage', 'category/emissions/voyage-emissions/'])
    # Catégorie spectacle
    liste.append(['[COLOR yellow]Spectacles[/COLOR]',
                 'category/spectaclesweb/'])
    liste.append(['Concerts', 'category/spectaclesweb/concerts/'])
    liste.append(['Humour', 'category/spectaclesweb/humour-spectacles/'])

    output_parameter_handler = OutputParameterHandler()
    for title, url in liste:

        output_parameter_handler.addParameter('site_url', URL_MAIN + url)
        gui.addDir(
            SITE_IDENTIFIER,
            'showMovies',
            title,
            'genres.png',
            output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = util.CleanName(search_text)
        url = search
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()
    pattern = 'post-thumbnail".+?href="([^"]+).+?src="(http[^"]+).+?bookmark">([^<]+).+?<p>([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    else:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()

        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            url = entry[0]
            thumb = entry[1]
            title = entry[2]
            desc = entry[3].replace('&#46;', '.')

            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)

            gui.addMovie(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

        progress_.VSclose(progress_)

    if not search:
        next_page, paging = __checkForNextPage(html_content)
        if next_page:
            output_parameter_handler = OutputParameterHandler()
            output_parameter_handler.addParameter('site_url', next_page)
            gui.addNext(
                SITE_IDENTIFIER,
                'showMovies',
                'Page ' + paging,
                output_parameter_handler)

        gui.setEndOfDirectory()


def __checkForNextPage(html_content):
    # &raquo; == >> traité dans parser
    pattern = 'pages\'>Page.+?sur ([^<]+?)<.+?href="([^"]+?)">>><'
    parser = Parser()
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page.([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showHosters(input_parameter_handler=False):
    gui = Gui()

    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = '<iframe.+?src="([^"]+)'

    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:
            watchUrl = 'https://www.youtube.com/watch?v='

            if 'videoseries?list=' in entry:
                idList = re.sub('https:.+?list=', '', entry)

                url = 'https://invidious.fdn.fr/playlist?list=' + idList
                request_handler = RequestHandler(url)
                html_content = request_handler.request()

                sPattern1 = ' class="thumbnail" src="(.+?)".+?<p dir="auto">(.+?)</p>.+? <a.+?href="(.+?)"'
                aResult1 = parser.parse(html_content, sPattern1)

                if aResult1[0] is True:
                    for entry in aResult1[1]:
                        hoster_url = entry[2]
                        thumb = 'https://invidious.fdn.fr' + entry[0]
                        title = entry[1].replace(
                            'EP.',
                            'E').replace(
                            'Ep. ',
                            'E').replace(
                            'Ep ',
                            'E')
                        title = title.replace('|', '-')

                        hoster = HosterGui().checkHoster(hoster_url)
                        if hoster:
                            hoster.setDisplayName(title)
                            hoster.setFileName(title)
                            HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                                   input_parameter_handler=input_parameter_handler)

            else:
                link = re.sub('.+?embed/', '', entry)
                link = link.replace('?rel=0', '')
                hoster_url = watchUrl + link
                hoster = HosterGui().checkHoster(hoster_url)
                if hoster:
                    hoster.setDisplayName(movie_title)
                    hoster.setFileName(movie_title)
                    HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                           input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
