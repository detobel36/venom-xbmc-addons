# -*- coding: utf-8 -*-
# vStream https://github.com/Kodi-vStream/venom-xbmc-addons
# return False

import re

from resources.lib.gui.hoster import HosterGui
from resources.lib.gui.gui import Gui
from resources.lib.handler.inputParameterHandler import InputParameterHandler
from resources.lib.handler.outputParameterHandler import OutputParameterHandler
from resources.lib.handler.requestHandler import RequestHandler
from resources.lib.parser import Parser
from resources.lib.comaddon import Progress, SiteManager
from resources.lib.util import cUtil

SITE_IDENTIFIER = 'hds_stream'
SITE_NAME = 'Hds-stream'
SITE_DESC = 'Film streaming HD complet en vf. Des films et séries pour les fan de streaming hds.'

URL_MAIN = SiteManager().getUrlMain(SITE_IDENTIFIER)
# URL_MAIN = dans sites.json

MOVIE_MOVIES = (True, 'showMenuMovies')
MOVIE_NEWS = (URL_MAIN + 'films/', 'showMovies')
MOVIE_GENRES = (URL_MAIN, 'showGenres')
MOVIE_EXCLUS = (URL_MAIN + 'tendance/', 'showMovies')
# MOVIE_ANNEES = (True, 'showMovieYears')

SERIE_SERIES = (True, 'showMenuTvShows')
SERIE_NEWS = (URL_MAIN + 'series/', 'showMovies')

URL_SEARCH = (URL_MAIN + '?s=', 'showMovies')
URL_SEARCH_MOVIES = (URL_SEARCH[0], 'showMovies')
URL_SEARCH_SERIES = (URL_SEARCH[0], 'showMovies')
FUNCTION_SEARCH = 'showMovies'


def load():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH[0])
    gui.addDir(
        SITE_IDENTIFIER,
        'showSearch',
        'Recherche',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Films (Populaire)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

#     output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
#     gui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuMovies():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_MOVIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_SEARCH_MOVIES[1],
        'Recherche Films',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_EXCLUS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_EXCLUS[1],
        'Films (Populaire)',
        'news.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_NEWS[1],
        'Films (Derniers ajouts)',
        'news.png',
        output_parameter_handler)

#     output_parameter_handler.addParameter('site_url', MOVIE_ANNEES[0])
#     gui.addDir(SITE_IDENTIFIER, MOVIE_ANNEES[1], 'Films (Par années)', 'annees.png', output_parameter_handler)

    output_parameter_handler.addParameter('site_url', MOVIE_GENRES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        MOVIE_GENRES[1],
        'Films (Genres)',
        'genres.png',
        output_parameter_handler)

    gui.setEndOfDirectory()


def showMenuTvShows():
    gui = Gui()

    output_parameter_handler = OutputParameterHandler()
    output_parameter_handler.addParameter('site_url', URL_SEARCH_SERIES[0])
    gui.addDir(
        SITE_IDENTIFIER,
        URL_SEARCH_SERIES[1],
        'Recherche Séries ',
        'search.png',
        output_parameter_handler)

    output_parameter_handler.addParameter('site_url', SERIE_NEWS[0])
    gui.addDir(
        SITE_IDENTIFIER,
        SERIE_NEWS[1],
        'Séries (Derniers ajouts)',
        'news.png',
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
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    parser = Parser()
    request_handler = RequestHandler(url)
    html_content = request_handler.request()

    pattern = 'menu-item-object-genres.+?<a href="([^"]+)".*?>(.+?)<'
    results = parser.parse(html_content, pattern)

    if results[0]:
        genres = set(results[1])
        genres = sorted(genres, key=lambda genre: genre[1])
        output_parameter_handler = OutputParameterHandler()
        for entry in genres:
            url = entry[0]
            title = entry[1]

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                title,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovieYears():
    gui = Gui()
    parser = Parser()
    request_handler = RequestHandler(URL_MAIN)
    html_content = request_handler.request()

    html_content = parser.abParse(
        html_content,
        '<h2>Films Par Années</h2>',
        '<h2>Films Par Genres</h2>')

    pattern = '<li><a href="([^"]+)">([^<]+)<'
    results = parser.parse(html_content, pattern)

    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url = entry[0]
            year = entry[1]

            output_parameter_handler.addParameter('site_url', url)
            gui.addDir(
                SITE_IDENTIFIER,
                'showMovies',
                year,
                'genres.png',
                output_parameter_handler)

    gui.setEndOfDirectory()


def showMovies(search=''):
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')

    if search:
        util = cUtil()
        search_text = search.replace(URL_SEARCH_MOVIES[0], '')
        search_text = search_text.replace(URL_SEARCH_SERIES[0], '')
        search_text = util.CleanName(search_text)
        url = search
        pattern = 'class="result-item">.*?href="([^"]+)"><img src="([^"]+).*?class="title"><a.*?>([^<]+).*?class="year">([^<]+).*?class="contenido"><p>([^<]+)'
    elif 'tendance/' in url:
        pattern = 'id="post-[0-9].+?<img src="([^"]+)".+?class="data".+?href="([^"]+)">([^<]+).*?, ([^<]+)</span>'
    else:
        pattern = 'id="post-[0-9].+?<img src="([^"]+)".+?class="data".+?href="([^"]+)">([^<]+).*?, ([^<]+)</span>.*?<div class="texto">([^<]*)'

    request_handler = RequestHandler(url)
    html_content = request_handler.request()

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

            if search:
                url2 = entry[0]
                thumb = entry[1]
                title = entry[2]
                year = entry[3]
                desc = entry[4]
                if not util.CheckOccurence(search_text, title):
                    continue    # Filtre de recherche
            else:
                thumb = entry[0]
                if thumb.startswith('//'):
                    thumb = 'https:' + thumb
                url2 = entry[1]
                title = entry[2]
                year = entry[3]
                if 'tendance/' in url:
                    desc = ''
                else:
                    desc = entry[4]

            display_title = ('%s (%s)') % (title, year)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('movie_title', title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('desc', desc)
            output_parameter_handler.addParameter('year', year)

            if '/series' in url2:
                gui.addTV(SITE_IDENTIFIER, 'showSxE', title, '',
                          thumb, desc, output_parameter_handler)
            else:
                gui.addMovie(
                    SITE_IDENTIFIER,
                    'showHosters',
                    display_title,
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
    parser = Parser()
    pattern = '>Page \\d+ de (\\d+)</span>.*?<span class="current.+?href=["\']([^"\']+/page/\\d+)/["\'] class="inactive'
    results = parser.parse(html_content, pattern)

    if results[0]:
        number_max = results[1][0][0]
        next_page = results[1][0][1]
        number_next = re.search('page/([0-9]+)', next_page).group(1)
        paging = number_next + '/' + number_max
        return next_page, paging

    return False, 'none'


def showSxE():
    gui = Gui()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    thumb = input_parameter_handler.getValue('thumb')
    movie_title = input_parameter_handler.getValue('movie_title')
    desc = input_parameter_handler.getValue('desc')

    request_handler = RequestHandler(url)
    html_content = request_handler.request()
    pattern = "span class='title'>([^<]+)|class='numerando'>\\d - ([^<]+).+?class='episodiotitle'><a href='([^']+)'>([^<]+)"
    parser = Parser()
    results = parser.parse(html_content, pattern)

    sSaison = ''
    if results[0]:
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            if entry[0]:
                sSaison = entry[0].replace('eason', 'aison')
                gui.addText(
                    SITE_IDENTIFIER,
                    '[COLOR crimson]' +
                    sSaison +
                    '[/COLOR]')
            else:
                url = entry[2]
                EpTitle = entry[3]
                Ep = entry[1]
                display_title = EpTitle + ' ' + sSaison + ' Episode ' + Ep
                title = movie_title + ' | ' + display_title

                output_parameter_handler.addParameter('site_url', url)
                output_parameter_handler.addParameter('movie_title', title)
                output_parameter_handler.addParameter('thumb', thumb)
                output_parameter_handler.addParameter('desc', desc)
                gui.addEpisode(
                    SITE_IDENTIFIER,
                    'showSeriesHosters',
                    display_title,
                    '',
                    thumb,
                    desc,
                    output_parameter_handler)

    gui.setEndOfDirectory()


def showHosters(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request = RequestHandler(url)
    html_content = request.request()

    pattern = "class='dooplay_player_option' data-type='([^']+)' data-post='([^']+)' data-nume='([^']+)'"
    results = parser.parse(html_content, pattern)
    if results[0]:
        url_main = GET_REAL_URLMAIN(url)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = url_main + 'wp-admin/admin-ajax.php'
            dType = entry[0]
            dPost = entry[1]
            dNum = entry[2]
            pdata = 'action=doo_player_ajax&post=' + \
                dPost + '&nume=' + dNum + '&type=' + dType
            host = 'Serveur ' + dNum

            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'showLink',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showSeriesHosters():
    gui = Gui()
    parser = Parser()
    input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    desc = input_parameter_handler.getValue('desc')

    request = RequestHandler(url)
    html_content = request.request()

    pattern = "id='player-option-.+?data-type='([^']+).+?data-post='([^']+).+?data-nume='([^']+).+?'server'>([^.|^<]+)"
    results = parser.parse(html_content, pattern)
    if results[0]:
        url_main = GET_REAL_URLMAIN(url)
        output_parameter_handler = OutputParameterHandler()
        for entry in results[1]:
            url2 = url_main + 'wp-admin/admin-ajax.php'
            dType = entry[0]
            dPost = entry[1]
            dNum = entry[2]
            pdata = 'action=doo_player_ajax&post=' + \
                dPost + '&nume=' + dNum + '&type=' + dType
            if (entry[3]).startswith('Unknown'):
                host = 'Serveur ' + dNum
            else:
                host = entry[3].capitalize()

            title = ('%s [COLOR coral]%s[/COLOR]') % (movie_title, host)

            output_parameter_handler.addParameter('site_url', url2)
            output_parameter_handler.addParameter('referer', url)
            output_parameter_handler.addParameter('movie_title', movie_title)
            output_parameter_handler.addParameter('thumb', thumb)
            output_parameter_handler.addParameter('host', host)
            output_parameter_handler.addParameter('pdata', pdata)
            gui.addLink(
                SITE_IDENTIFIER,
                'showLink',
                title,
                thumb,
                desc,
                output_parameter_handler,
                input_parameter_handler)

    gui.setEndOfDirectory()


def showLink(input_parameter_handler=False):
    gui = Gui()
    parser = Parser()
    if not input_parameter_handler:
        input_parameter_handler = InputParameterHandler()
    url = input_parameter_handler.getValue('site_url')
    movie_title = input_parameter_handler.getValue('movie_title')
    thumb = input_parameter_handler.getValue('thumb')
    referer = input_parameter_handler.getValue('referer')
    pdata = input_parameter_handler.getValue('pdata')

    request = RequestHandler(url)
    request.setRequestType(1)
    request.addHeaderEntry(
        'User-Agent',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:70.0) Gecko/20100101 Firefox/70.0')
    request.addHeaderEntry('Referer', referer)
    request.addHeaderEntry('Accept', '*/*')
    request.addHeaderEntry(
        'Accept-Language',
        'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7')
    request.addHeaderEntry(
        'Content-Type',
        'application/x-www-form-urlencoded')
    request.addParametersLine(pdata)

    html_content = request.request().replace('\\', '')

    pattern = '(http[^"]+)'
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


def GET_REAL_URLMAIN(url):
    sd = url.split('.')
    sdm = URL_MAIN.split('.')
    return URL_MAIN.replace(sdm[0], sd[0])
