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

SITE_IDENTIFIER = 'o1streaming'
SITE_NAME = '01 Streaming'
SITE_DESC = 'Films & Séries'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

FUNCTION_SEARCH = 'showMovies'
URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')

MOVIE_NEWS = (URL_MAIN + 'films-en-streaming/', 'showMovies')
MOVIE_GENRES = ('?type=movies', 'showGenres')
MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_NEWS = (URL_MAIN + 'series-streaming/', 'showMovies')
SERIE_GENRES = ('?type=series', 'showGenres')


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
        'films.png',
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
        'Films & Séries (Par années)',
        'annees.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'series.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_GENRES[1],
        'Séries (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()
    request_handler = RequestHandler(URL_MAIN + 'accueil/')
    html_content = request_handler.request()

    pattern = 'class="btn sm" href="([^"]+)">([^<]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in reversed(results[1]):
            url = entry[0]
            Year = entry[1]

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                Year,
                'annees.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showGenres():
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    site_url = input_parameter_handler.getValue('site_url')

    request_handler = RequestHandler(URL_MAIN + 'accueil/')
    html_content = request_handler.request()

    pattern = '<li class="cat-item cat-item-.+?href="([^"]+)">([^<]+)<'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0] + site_url
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showSearch():
    gui = Gui()
    search_text = gui.showKeyBoard()
    if search_text:
        url = URL_SEARCH[0] + search_text.replace(' ', '%20')
        showMovies(url)
        gui.setEndOfDirectory()
        return


def showMovies(search=''):
    gui = Gui()

    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    if search:
        util = cUtil()
        url = search
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'entry-header"> *<h2 class="entry-title">([^<]+).+?src="([^"]+).+?class="year">([^<]+).+?href="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        total = len(results[1])
        progress_ = Progress().VScreate(SITE_NAME)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            thumb = entry[1]
            if thumb.startswith('//'):
                thumb = 'http:' + thumb
            year = entry[2]
            url2 = entry[3]
            title = entry[0]
            if search:
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche
            display_title = title
            if '/release/' in url or search:
                if '/serie' in url2:
                    display_title += ' {Série}'
                else:
                    display_title += ' {Film}'

            if year:
                display_title += ' (%s)' % year

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('year', year)

            if '/serie' in url2:
                gui.addTV(
                    SITE_IDENTIFIER,
                    'showSaisons',
                    display_title,
                    'series.png',
                    thumb,
                    '',
                    output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showLinks',
                    display_title,
                    'films.png',
                    thumb,
                    '',
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
    parser = Parser()
    pattern = '>([^<]+)</a><a href="([^"]+)"\\s*>SUIVANT</a>'
    results = parser.parse(html_content, pattern)
    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('/page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        if next_page.startswith('/'):
            return URL_MAIN[:-1] + next_page, paging
        else:
            return next_page, paging

    return False, 'none'


def showSaisons():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    # récupération du Synopsis
    desc = ''
    try:
        pattern = 'description"><p>(.+?)</p>'
        results = parser.parse(html_content, pattern)
        if results[0]:
            desc = results[1][0]
    except BaseException:
        pass

    pattern = 'choose-season"><a href="([^"]+).+?inline">([^<]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            url = entry[0]
            movie_title = movie_title + ' Saison ' + entry[1]

            # output_parameter_handler.addParameter('site_url', URL_MAIN + 'wp-admin/admin-ajax.php')
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('movie_title', movie_title)
            gui.addSeason(
                SITE_IDENTIFIER,
                'showEpisodes',
                movie_title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showEpisodes():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    pattern = 'h2 class="entry-title">([^<]+).+?href="([^"]+)'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:

            title = entry[0]
            url = entry[1]
            # if url.startswith('/'):
            # url = URL_MAIN + url

            # title = re.sub('- Saison \d+', '', title)  # double affichage
            # de la saison

            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('site_url', url)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            gui.addEpisode(
                SITE_IDENTIFIER,
                'showLinks',
                title,
                '',
                thumb,
                desc,
                output_parameter_handler)

    gui.setEndOfDirectory()


def showLinks(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    parser = Parser()

    numUrl = 0

    # récupération du Synopsis
    if desc is False:
        try:
            pattern = 'description"><p>(.+?)</p>'
            results = parser.parse(html_content, pattern)
            if results[0]:
                desc = results[1][0]
        except BaseException:
            pass

    sPatternUrl = '<iframe (?:data-)*src="([^"]+)"'
    aResultUrl = parser.parse(html_content, sPatternUrl)
    if aResultUrl[0]:
        sPatternHost = 'class="btn(| on)" href="([^"]+).+?class="server">([^<]+) <'
        aResultHost = parser.parse(html_content, sPatternHost)
        if aResultHost[0]:
            output_parameter_handler = OutputParameterHandler()
            for entry in aResultHost[1]:

                url2 = aResultUrl[1][numUrl]
                numUrl += 1
                host = entry[2]
                lang = 'VF'
                if '-VOSTFR' in host:
                    lang = 'VOSTFR'
                host = host.replace(
                    'VF',
                    '').replace(
                    'VOSTFR',
                    '').replace(
                    ' -',
                    '')

                hoster = HosterGui().checkHoster(host)
                if hoster:
                    display_title = (
                        '%s [COLOR coral]%s[/COLOR] (%s)') % (movie_title, host, lang)
                    output_parameter_handler.addParameter('site_url', url2)
                    output_parameter_handler.addParameter('thumb', thumb)
                    output_parameter_handler.addParameter('desc', desc)
                    output_parameter_handler.addParameter('host', host)
                    output_parameter_handler.addParameter('lang', lang)
                    output_parameter_handler.addParameter(
                        'movie_title', movie_title)
                    gui.addLink(
                        SITE_IDENTIFIER,
                        'showHosters',
                        display_title,
                        thumb,
                        desc,
                        output_parameter_handler,
                        input_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = 'src="([^"]+)'
    parser = Parser()
    results = parser.parse(html_content, pattern)

    if results[0]:
        for entry in results[1]:

            hoster_url = entry

            hoster = HosterGui().checkHoster(hoster_url)
            if hoster:
                hoster.setDisplayName(movie_title)
                hoster.setFileName(movie_title)
                HosterGui().showHoster(gui, hoster, hoster_url, thumb,
                                       input_parameter_handler=input_parameter_handler)

    gui.setEndOfDirectory()
