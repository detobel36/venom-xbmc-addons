# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
import re

from resources.lib.comaddon import SiteManager
from resources.lib.gui.gui import Gui
from resources.lib.gui.hoster import HosterGui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'illimitestreaming'
SITE_NAME = 'Illimitestreaming'
SITE_DESC = 'Regarder Les Films & Séries VF. VOSTFR .VO'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

MOVIE_MOVIE = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = ('?post_types=movies', 'showGenres')
MOVIE_ANNEES = (True, 'showYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'tvshows/', 'showMovies')

SERIE_NETFLIX = (URL_MAIN + 'networks/netflix/', 'showMovies')
SERIE_CANAL = (URL_MAIN + 'networks/canal/', 'showMovies')
SERIE_AMAZON = (URL_MAIN + 'networks/amazon/', 'showMovies')
SERIE_DISNEY = (URL_MAIN + 'networks/disney/', 'showMovies')
SERIE_APPLE = (URL_MAIN + 'networks/apple-tv/', 'showMovies')
SERIE_YOUTUBE = (URL_MAIN + 'networks/youtube-premium/', 'showMovies')
SERIE_ARTE = (URL_MAIN + 'networks/arte/', 'showMovies')
# SERIE_ANNEES = (True, 'showSeriesYears')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?_type=movie&s=', 'showMovies')
URL_SEARCH_SERIES = (URL_MAIN + '?_type=tvshow&s=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuMovies',
        'Films',
        'films.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', 'http://venom/')
    gui.addDir(
        SITE_IDENTIFIER,
        'showMenuTvShows',
        'Séries',
        'series.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_ANNEES[1],
        'Films (Par années)',
        'annees.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche séries',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', URL_MAIN)
    gui.addDir(
        SITE_IDENTIFIER,
        'showNetwork',
        'Séries (Par diffuseurs)',
        'host.png',
        output_parameter_handler)

    # output_parameter_handler.addParameter('site_url', SERIE_ANNEES[0])
    # gui.addDir(SITE_IDENTIFIER, SERIE_ANNEES[1], 'Séries (Par années)', 'annees.png', output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()
    parser = Parser()

    url = URL_MAIN
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    start = '<a>genres</a>'
    end = '</ul><div class="clearfix"></div>'
    html_content = parser.abParse(html_content, start, end)
    pattern = 'taxonomy.+?href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)
    triAlpha = []
    if results[0]:
        for entry in results[1]:
            url = entry[0]
            title = entry[1].capitalize()
            triAlpha.append((title, url))

        # Trie des genres par ordre alphabétique
        triAlpha = sorted(triAlpha, key=lambda genre: genre[0])

        output_parameter_handler = OutputParameterHandler()
        for title, url in triAlpha:
            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showNetwork():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', SERIE_NETFLIX[0])
    output_parameter_handler.addParameter('tmdb_id', 213)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_NETFLIX[1],
        'Séries (Netflix)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_CANAL[0])
    output_parameter_handler.addParameter('tmdb_id', 285)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_CANAL[1],
        'Séries (Canal+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_AMAZON[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 1024)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_AMAZON[1],
        'Séries (Amazon Prime)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_DISNEY[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 2739)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_DISNEY[1],
        'Séries (Disney+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_APPLE[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 2552)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_APPLE[1],
        'Séries (Apple TV+)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_YOUTUBE[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 1436)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_YOUTUBE[1],
        'Séries (YouTube Originals)',
        'host.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_ARTE[0])
    output_parameter_handler.addParameter(
        'tmdb_id', 1628)    # Utilisé par TMDB
    gui.addNetwork(
        SITE_IDENTIFIER,
        SERIE_ARTE[1],
        'Séries (Arte)',
        'host.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showYears():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = '<a>Anneés</a>'
    end = '<a>genres</a>'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)
    results[1].insert(2, (URL_MAIN + 'release-year/2020/', '2020'))

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = entry[1].capitalize()
            _type = 'movie'

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('_type', _type)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showSeriesYears():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()
    start = '<a>Anneés</a>'
    end = '<a>genres</a>'
    html_content = parser.abParse(html_content, start, end)

    pattern = 'href="([^"]+)">([^<]+)'
    results = parser.parse(html_content, pattern)
    results[1].insert(2, (URL_MAIN + 'release-year/2020/', '2020'))
    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = entry[1].capitalize()
            _type = 'tvshow'

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('_type', _type)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)
        gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    search_text = gui.showKeyBoard()
    if search_text:
        url = url + search_text
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):
    gui = Gui()
    util = cUtil()

    _type = ''
    if search:
        url = search.replace(' ', '+')
        _type = re.search('_type=(.+?)&', url).group(1)
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
    else:
        input_parameter_handler = InputParameterHandler()
        url = input_parameter_handler.getValue('site_url')
        _type = input_parameter_handler.getValue('_type')

    pattern = 'data-movie-id="\\d+".+?href="([^"]+).+?oldtitle="([^"]+).+?data-original="([^ "]+).+?desc"><p>([^<]+)'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if not results[0]:
        gui.addText(SITE_IDENTIFIER)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            title = entry[1]
            if _type and 'movie' in _type and '/series' in url:
                continue
            elif _type and 'tvshow' in _type and '/series' not in url:
                continue
            if search and not util.CheckOccurence(search_text, title):
                continue    # Filtre de recherche

            thumb = entry[2]
            thumb = re.sub('/w\\d+', '/w342', thumb)

            desc = entry[3]
            try:
                desc = unicode(desc, 'utf-8')  # converti en unicode
                desc = util.unescape(desc).encode(
                    'utf-8')    # retire les balises HTML
            except BaseException:
                pass

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)

            if '/serie' in url:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

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
    parser = Parser()
    pattern = '<li class=\'active\'>.+?href=\'([^\']+).+?/(\\d+)/\'>Dernière'
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    # for the tvshows and the last page of movies
    pattern = "class=''>\\d+</a></li><li><a rel='nofollow' class='page larger' href='([^']+).+?>(\\d+)</a></li></ul"
    results = parser.parse(html_content, pattern)
    if results[0]:
        next_page = results[1][0][0]
        number_max = results[1][0][1]
        number_next = re.search('page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    site_url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')
    parser = Parser()
    request_handler = RequestHandler(site_url)
    html_content = request_handler.request()
    start = '<div class="tvseason">'
    end = '<!-- Micro data -->'
    html_content = parser.abParse(html_content, start, end)
    pattern = '<div class="tvseason">.+?<strong>(.+?)<'

    results = parser.parse(html_content, pattern)

    sSaison = ''
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for sSaison in results[1]:
            title = movie_title + ' ' + sSaison
            url = site_url + '&season=' + sSaison
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url, sSearchSeason = input_parameter_handler.getValue(
        'site_url').split('&season=')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')
    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    start = '<div class="tvseason">'
    end = '<!-- Micro data -->'
    html_content = parser.abParse(html_content, start, end)
    pattern = '<div class="tvseason">.+?<strong>(.+?)<|href="([^"]+)">([^<]+)'

    results = parser.parse(html_content, pattern)

    sSaison = ''
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                sSaison = entry[0]
                continue

            if sSaison != sSearchSeason:
                continue

            url = entry[1]
            SxE = entry[2]
            title = movie_title  # + ' ' + sSaison
            title += ' ' + SxE

            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showHosters',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request = RequestHandler(url)
    html_content = request.request()
    pattern = '<div class="movieplay">([^<]+)|lnk lnk-dl"><h6>([^<]*)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:

        tab = results[1]
        n = len(tab) // 3

        for i in range(n):

            hoster_url = tab[i][0]
            lang = tab[2 * i + n][1]
            qual = tab[2 * i + (n + 1)][1]

            title = ('%s [%s] (%s)') % (movie_title, qual, lang)
            input_parameter_handler.addParameter('qual', qual)

            # Petit hack pour conserver le nom de domaine du site
            # necessaire pour userload.
            if 'userload' in hoster_url:
                hoster_url = hoster_url + "|Referer=" + URL_MAIN

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(title)
                hoster.setFileName(title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
